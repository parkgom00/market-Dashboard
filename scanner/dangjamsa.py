"""한국경제TV 유튜브의 아침 방송 '#당잠사'(당신이 잠든 사이: 간밤 미국 증시 정리)를 찾아 제미나이로 요약합니다.

- 채널 안 검색 화면에서 오늘 날짜(제목의 MM/DD)가 붙은 #당잠사 영상을 찾고,
- 영상이 길면 40분 단위 구간으로 나눠 요약한 뒤 파트로 이어 붙입니다 (화면은 드물게, 소리 위주로 읽어 토큰 절약).
- 하루에 한 번만 만들고, 실패하면 다음 실행에서 다시 시도합니다 (하루 최대 MAX_TRY 번).
결과: out/dangjamsa.json, data/dangjamsa.js
"""
import datetime as dt
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_JS = os.path.join(HERE, "..", "data", "dangjamsa.js")
KST = dt.timezone(dt.timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0 (compatible; market-dashboard)", "Accept-Language": "ko"}
SEARCH_URL = "https://www.youtube.com/@hkwowtv/search?query=" + urllib.parse.quote("당잠사")
SEG = 2400          # 한 번에 읽는 구간 길이(초)
MAX_SEG = 4
MAX_TRY = 6

SYSTEM = ("너는 한국 개인투자자를 위한 미국 증시 방송 요약가다. 영상에서 실제로 말한 내용만 정리하고, 영상에 없는 종목·수치·전망을 지어내지 않는다. "
          "투자 권유가 아니라 방송 내용 요약임을 유지한다.")
PROMPT = """이 영상은 한국경제TV의 아침 방송 '당잠사'(간밤 미국 증시 정리)다. {scope} 내용을 한국어로 요약해 JSON 으로만 답해라. 형식:
{{"headline": "간밤 미국장을 한 문장으로 (지수 방향과 가장 큰 이유)",
  "parts": [{{"title": "파트 제목 (예: 지수·금리·유가 / 반도체·AI / 개별 종목 이슈 / 오늘 일정·체크포인트)",
             "points": ["**핵심 이슈·종목·지표 이름**을 굵게 표시하고, 수치와 원인을 넣은 한두 문장", "..."]}}]}}
규칙:
- 주제가 여러 개면 파트를 2~5개로 나눠라. 파트마다 요점은 3~6개.
- 요점마다 가장 중요한 이슈·종목·지표 이름 한두 군데를 **별표 두 개**로 감싸 굵게 표시해라.
- 지수·금리·환율·유가 등 수치는 방송에서 말한 그대로 넣어라. 광고·인사말·구독 안내는 뺀다.
- 방송에 없는 내용은 쓰지 마라. 해당 구간에 시황 내용이 없으면 {{"headline": "", "parts": []}} 로 답해라."""


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return r.read().decode("utf-8", "replace")


def _unesc(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s


def length_sec(text):
    """'1:02:33' → 3753"""
    try:
        sec = 0
        for p in str(text).split(":"):
            sec = sec * 60 + int(p)
        return sec
    except ValueError:
        return 0


def parse_search(html):
    """검색 화면 → [{videoId, title, length(초, 없으면 0)}]"""
    out, seen = [], set()
    for chunk in html.split('"videoRenderer":{"videoId":"')[1:]:
        vid, chunk = chunk[:11], chunk[:7000]
        mt = re.search(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', chunk)
        if not re.fullmatch(r"[\w-]{11}", vid) or not mt or vid in seen:
            continue
        seen.add(vid)
        ml = re.search(r'"lengthText":\{.{0,300}?"simpleText":"([\d:]+)"', chunk)
        out.append({"videoId": vid, "title": _unesc(mt.group(1)).strip(), "length": length_sec(ml.group(1)) if ml else 0})
    return out


def pick_today(videos, today):
    """제목에 #당잠사 와 오늘 날짜(MM/DD)가 들어 있는 영상."""
    tag = today.strftime("%m/%d")
    for v in videos:
        if "당잠사" in v["title"] and tag in v["title"]:
            return v
    return None


def segments(length):
    """영상 길이(초) → [(시작, 끝)] . 길이를 모르면 [None] (통째로 한 번)."""
    if not length:
        return [None]
    n = min(MAX_SEG, max(1, math.ceil(length / SEG)))
    if n == 1:
        return [None]
    return [(i * SEG, min(length, (i + 1) * SEG)) for i in range(n)]


def clean(obj):
    """모델 응답을 화면용으로 정리: {"headline", "parts":[{"title","points":[...]}]}"""
    if not isinstance(obj, dict):
        return {"headline": "", "parts": []}
    parts = []
    for p in obj.get("parts") or []:
        if not isinstance(p, dict):
            continue
        pts = [str(x).strip() for x in (p.get("points") or []) if str(x).strip()]
        if pts:
            parts.append({"title": str(p.get("title") or "").strip(), "points": pts[:8]})
    return {"headline": str(obj.get("headline") or "").strip(), "parts": parts}


def summarize(video, generate, wait=65):
    """generate(prompt, video_url, video_meta) → dict. 구간별 요약을 이어 붙인다."""
    url = "https://www.youtube.com/watch?v=" + video["videoId"]
    segs = segments(video.get("length", 0))
    headline, parts = "", []
    for i, seg in enumerate(segs):
        if seg is None:
            scope, meta = "영상 전체의", {"fps": 0.1}
        else:
            scope = f"영상의 {seg[0] // 60}분~{seg[1] // 60}분 구간"
            meta = {"start_offset": f"{seg[0]}s", "end_offset": f"{seg[1]}s", "fps": 0.1}
        res = clean(generate(PROMPT.format(scope=scope), url, meta))
        headline = headline or res["headline"]
        parts += res["parts"]
        if i < len(segs) - 1:
            time.sleep(wait)      # 분당 토큰 한도를 넘지 않게 간격을 둠
    if not parts:
        raise ValueError("요약 결과가 비어 있음")
    return {"headline": headline, "parts": parts[:12]}


def load():
    try:
        with open(os.path.join(OUT, "dangjamsa.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save(state):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "dangjamsa.json"), "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/dangjamsa.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.dangjamsa = ")
        json.dump({k: v for k, v in state.items() if k != "attempts"}, f, ensure_ascii=False, indent=1)
        f.write(";\n")


def main(force=False):
    import gemini
    now = dt.datetime.now(KST)
    today = now.date()
    state = load()
    if state.get("forDate") == today.isoformat() and state.get("parts") and not force:
        print("오늘 요약은 이미 있음")
        return
    try:
        video = pick_today(parse_search(_get(SEARCH_URL)), today)
    except Exception as e:
        print("검색 실패:", type(e).__name__, e)
        return
    if not video:
        print("오늘 날짜의 #당잠사 영상이 아직 없음")
        return
    tries = state.get("attempts", 0) if state.get("tryDate") == today.isoformat() else 0
    base = {"tryDate": today.isoformat(), "attempts": tries + 1, "videoId": video["videoId"], "title": video["title"],
            "url": "https://www.youtube.com/watch?v=" + video["videoId"], "length": video["length"]}
    keep = {k: state[k] for k in ("forDate", "headline", "parts", "generatedAt", "sumTitle", "sumUrl") if k in state}   # 어제 요약은 새 요약이 나올 때까지 유지
    if not video["length"]:
        st = dict(keep, **base)
        st.update(attempts=tries, status="오늘 방송이 아직 진행 중이라 끝난 뒤 요약합니다.")
        save(st)
        print("방송 진행 중(길이 정보 없음)")
        return
    if tries >= MAX_TRY and not force:
        print("오늘 시도 횟수 초과")
        return
    if not gemini.api_key():
        save(dict(keep, **base, status="제미나이 키를 찾지 못했습니다."))
        return
    gemini.set_deadline(900)

    def gen(prompt, url, meta):
        return gemini.generate(prompt, system=SYSTEM, video_url=url, want_json=True, max_tokens=8192, video_meta=meta, low_res=True, retries=1)
    try:
        res = summarize(video, gen)
    except Exception as e:
        msg = re.sub(r"AIza[\w-]{10,}", "[키]", str(e))[:300]
        save(dict(keep, **base, status=f"요약 실패 (다음 실행에 재시도 {tries + 1}/{MAX_TRY}): {msg}"))
        print("요약 실패:", msg)
        return
    save(dict(base, forDate=today.isoformat(), headline=res["headline"], parts=res["parts"], sumTitle=video["title"], sumUrl=base["url"],
              generatedAt=now.strftime("%Y-%m-%d %H:%M"), model=gemini.used_model() or "", status=""))
    print(f"요약 완료: 파트 {len(res['parts'])}개")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
