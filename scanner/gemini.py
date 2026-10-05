"""제미나이(Gemini) API 호출 도우미. 키는 환경변수 GEMINI_API_KEY (GitHub Secrets) 로만 읽습니다.

- 모델 이름은 API 의 모델 목록에서 가장 최신 'flash' 를 자동 선택합니다 (GEMINI_MODEL 로 고정 가능).
- 무료 사용량 초과(429)·구글 혼잡(503)은 GeminiBusy 로 알려서 호출한 쪽이 '다음 실행에 다시' 하도록 합니다.
- 응답에서 JSON 을 꺼내는 extract_json 은 코드블록·앞뒤 설명이 섞여도 동작합니다.
"""
import json
import os
import re
import time
import urllib.error
import urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta"


class GeminiBusy(Exception):
    """한도 초과·혼잡. 나중에 다시 시도하면 되는 오류."""


class GeminiError(Exception):
    """그 밖의 오류."""


def api_key():
    return os.environ.get("GEMINI_API_KEY", "").strip()


def _request(url, body=None, key=None, timeout=240):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "x-goog-api-key": key or api_key()})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")[:300]
        if e.code in (429, 500, 502, 503, 504):
            raise GeminiBusy(f"HTTP {e.code}: {msg}")
        raise GeminiError(f"HTTP {e.code}: {msg}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise GeminiBusy(f"네트워크: {e}")


def choose_model(names):
    """모델 이름 목록에서 가장 최신의 일반 flash 를 고릅니다 (lite·preview·실험판은 후순위)."""
    best = None
    for n in names:
        n = n.replace("models/", "")
        m = re.fullmatch(r"gemini-(\d+(?:\.\d+)?)-flash(-lite)?", n)
        if not m:
            continue
        score = (float(m.group(1)), 0 if m.group(2) else 1)
        if best is None or score > best[0]:
            best = (score, n)
    if best:
        return best[1]
    for n in names:   # 정확히 맞는 게 없으면 flash 가 들어간 아무거나
        if "flash" in n and "image" not in n and "tts" not in n:
            return n.replace("models/", "")
    return None


def rank_models(names):
    """일반 flash 모델을 최신순으로(같은 버전이면 일반판이 lite 보다 먼저). 혼잡할 때 순서대로 갈아타는 용도."""
    scored = []
    for n in names:
        n = n.replace("models/", "")
        m = re.fullmatch(r"gemini-(\d+(?:\.\d+)?)-flash(-lite)?", n)
        if m:
            scored.append(((float(m.group(1)), 0 if m.group(2) else 1), n))
    scored.sort(reverse=True)
    return [n for _, n in scored]


_model_cache = {}


def get_models(limit=4):
    env = os.environ.get("GEMINI_MODEL", "").strip()
    if env:
        return [env]
    if "list" not in _model_cache:
        res = _request(f"{BASE}/models?pageSize=200")
        names = [m["name"] for m in res.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
        ranked = rank_models(names)
        if not ranked:
            one = choose_model(names)
            ranked = [one] if one else []
        if not ranked:
            raise GeminiError("사용 가능한 flash 모델을 찾지 못했습니다")
        _model_cache["list"] = ranked
    return _model_cache["list"][:limit]


def get_model():
    env = os.environ.get("GEMINI_MODEL", "").strip()
    if env:
        return env
    if "m" not in _model_cache:
        res = _request(f"{BASE}/models?pageSize=200")
        names = [m["name"] for m in res.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
        model = choose_model(names)
        if not model:
            raise GeminiError("사용 가능한 flash 모델을 찾지 못했습니다")
        _model_cache["m"] = model
    return _model_cache["m"]


def extract_json(text):
    """응답 문자열에서 JSON 객체/배열을 꺼냅니다. 실패하면 ValueError."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        return json.loads(t)
    except ValueError:
        pass
    for open_c, close_c in (("{", "}"), ("[", "]")):
        a, b = t.find(open_c), t.rfind(close_c)
        if a != -1 and b > a:
            try:
                return json.loads(t[a:b + 1])
            except ValueError:
                continue
    raise ValueError("JSON 을 찾지 못함: " + t[:80])


def _text_of(res):
    cands = res.get("candidates") or []
    if not cands:
        raise GeminiError("응답 없음: " + json.dumps(res.get("promptFeedback", {}), ensure_ascii=False)[:200])
    parts = (cands[0].get("content") or {}).get("parts") or []
    out = "".join(p.get("text", "") for p in parts)
    if not out.strip():
        raise GeminiError("빈 응답 (finishReason=%s)" % cands[0].get("finishReason"))
    return out


def generate(prompt, system=None, video_url=None, want_json=False, search=False, max_tokens=8192, temperature=0.3, retries=2):
    """텍스트(또는 JSON 파싱한 객체)를 돌려줍니다.
    video_url: 유튜브 주소를 영상 그대로 읽게 함. search: 구글 검색 근거 사용(이 경우 JSON 모드는 못 쓰므로 본문에서 추출)."""
    if not api_key():
        raise GeminiError("GEMINI_API_KEY 가 없습니다")
    parts = []
    if video_url:
        parts.append({"file_data": {"file_uri": video_url}})
    parts.append({"text": prompt})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    if search:
        body["tools"] = [{"google_search": {}}]
    elif want_json:
        body["generationConfig"]["responseMimeType"] = "application/json"
    last = None
    errs = []
    for rnd in range(retries + 1):
        for model in get_models():
            url = f"{BASE}/models/{model}:generateContent"
            try:
                text = _text_of(_request(url, body))
                _model_cache["used"] = model
                return extract_json(text) if want_json else text
            except GeminiBusy as e:    # 이 모델이 혼잡/한도 → 다음 모델로
                last = e
                errs.append(f"{model}: {_short(e)}")
            except ValueError as e:    # JSON 파싱 실패 → 다음 모델로
                last = GeminiError(str(e))
                errs.append(f"{model}: JSON 형식 오류")
        if rnd < retries:
            time.sleep(20 * (rnd + 1))
    detail = " | ".join(errs[-4:])
    raise (GeminiBusy if isinstance(last, GeminiBusy) else GeminiError)(detail or str(last))


def _short(e):
    """오류 문구를 짧게: 'HTTP 503 ... high demand' 정도만."""
    t = " ".join(str(e).split())
    m = re.search(r'"message":\s*"([^"]{0,90})', t)
    code = re.match(r"HTTP (\d+)", t)
    return ((code.group(0) + " ") if code else "") + (m.group(1) if m else t[:90])


def used_model():
    return _model_cache.get("used") or (_model_cache.get("list") or ["?"])[0]
