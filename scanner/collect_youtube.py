"""유튜브 채널별 최신 영상 목록 수집 → data/youtube.js (API 키 불필요, 무료).

채널 핸들(@이름) → 채널 ID 를 채널 페이지에서 찾고, 공식 RSS(videos.xml)에서 최신 영상을 읽습니다.
채널 하나가 실패해도 나머지는 갱신하고, 실패한 채널은 이전 목록을 그대로 둡니다.
요약은 화면의 '재미나이로 요약' 버튼이 담당합니다 (서버에서 요약하지 않음).
"""
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "data", "youtube.js")
KST = timezone(timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0 (compatible; market-dashboard)", "Accept-Language": "ko"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
PER_CHANNEL = 5


def _get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def find_channel_id(html):
    for pat in (r'"externalId":"(UC[\w-]{22})"', r'"channelId":"(UC[\w-]{22})"',
                r'youtube\.com/channel/(UC[\w-]{22})', r'<meta itemprop="identifier" content="(UC[\w-]{22})"'):
        m = re.search(pat, html)
        if m:
            return m.group(1)
    return None


def parse_feed(xml_text, limit=PER_CHANNEL):
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("a:entry", NS)[:limit]:
        vid = e.findtext("yt:videoId", default="", namespaces=NS)
        title = e.findtext("a:title", default="", namespaces=NS).strip()
        pub = e.findtext("a:published", default="", namespaces=NS)
        if not vid or not title:
            continue
        try:
            dt = datetime.fromisoformat(pub.replace("Z", "+00:00")).astimezone(KST)
            when = dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            when = pub[:10]
        out.append({"title": title, "publishedAt": when, "url": f"https://www.youtube.com/watch?v={vid}"})
    return out


REL = [(r"(\d+)\s*분 전", 60), (r"(\d+)\s*시간 전", 3600), (r"(\d+)\s*일 전", 86400), (r"(\d+)\s*주 전", 7 * 86400),
       (r"(\d+)\s*개월 전", 30 * 86400), (r"(\d+)\s*년 전", 365 * 86400),
       (r"(\d+)\s*minutes? ago", 60), (r"(\d+)\s*hours? ago", 3600), (r"(\d+)\s*days? ago", 86400),
       (r"(\d+)\s*weeks? ago", 7 * 86400), (r"(\d+)\s*months? ago", 30 * 86400), (r"(\d+)\s*years? ago", 365 * 86400)]


def rel_to_time(text, now=None):
    """'3시간 전' 같은 상대 시각 → 'YYYY-MM-DD HH:MM' (하루 이상 전이면 날짜만). 못 읽으면 ''."""
    from datetime import timedelta
    now = now or datetime.now(KST)
    for pat, sec in REL:
        m = re.search(pat, text or "")
        if m:
            t = now - timedelta(seconds=int(m.group(1)) * sec)
            return t.strftime("%Y-%m-%d %H:%M") if sec < 86400 else t.strftime("%Y-%m-%d")
    return ""


def _unesc(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s


def parse_videos_tab(html, limit=PER_CHANNEL, now=None):
    """채널의 '동영상'·'라이브' 탭 화면에서 최신 영상 목록을 읽습니다 (RSS 가 막혔을 때의 대체 수단)."""
    out, seen = [], set()
    for chunk in html.split('"lockupViewModel":{')[1:]:
        chunk = chunk[:16000]
        mid = re.search(r'"contentId":"([\w-]{11})"', chunk)
        mt = re.search(r'"lockupMetadataViewModel":\{"title":\{"content":"((?:[^"\\]|\\.)*)"', chunk)
        if not mid or not mt or mid.group(1) in seen:
            continue
        seen.add(mid.group(1))
        when = ""
        for txt in re.findall(r'"content":"((?:[^"\\]|\\.)*)"', chunk[mt.end():mt.end() + 3000]):   # 제목 바로 뒤의 조회수·시각
            when = rel_to_time(_unesc(txt), now)
            if when:
                break
        out.append({"title": _unesc(mt.group(1)).strip(), "publishedAt": when, "url": f"https://www.youtube.com/watch?v={mid.group(1)}"})
        if len(out) >= limit:
            break
    return out


def scrape_channel(cid, fetch, old_videos=None, limit=PER_CHANNEL):
    """동영상 탭 + 라이브 탭을 합쳐 최신순으로. 이미 알던 영상은 예전에 저장한 정확한 시각을 유지."""
    items, seen = [], set()
    for tab in ("videos", "streams"):
        try:
            for v in parse_videos_tab(fetch(f"https://www.youtube.com/channel/{cid}/{tab}"), limit=limit * 2):
                if v["url"] not in seen:
                    seen.add(v["url"])
                    items.append(v)
        except Exception:
            continue
    items = merge_times(items, old_videos)
    items.sort(key=lambda v: v.get("publishedAt") or "", reverse=True)
    return items[:limit]


def merge_times(videos, old_videos):
    """화면에서 읽은 시각은 대략값이라, 이미 알고 있던 영상은 예전에 저장한 시각을 유지합니다."""
    known = {v["url"]: v.get("publishedAt", "") for v in old_videos or []}
    for v in videos:
        if known.get(v["url"]):
            v["publishedAt"] = known[v["url"]]
    return videos


def load_previous(path=TARGET):
    """이전 data/youtube.js 에서 채널별 영상 목록과 채널 ID 를 읽습니다 (실패 시 빈 값)."""
    try:
        txt = open(path, encoding="utf-8").read()
        body = txt.split("window.DASH.youtube = ", 1)[1].rsplit(";", 1)[0]
        data = json.loads(body)
        return {c["name"]: c for c in data.get("channels", [])}
    except Exception:
        return {}


def build(channels, prev, fetch=_get):
    result, errors = [], []
    for ch in channels:
        old = prev.get(ch["name"], {})
        cid = old.get("channelId") or ch.get("channelId") or ""
        try:
            if not cid:
                cid = find_channel_id(fetch("https://www.youtube.com/" + urllib.parse.quote(ch["handle"]))) or ""
                if not cid:
                    raise ValueError("채널 ID를 찾지 못함")
            try:
                videos = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
            except Exception as e_rss:   # RSS 가 막히면 채널의 '동영상' 탭 화면에서 읽음
                videos = scrape_channel(cid, fetch, old.get("videos", []))
                if not videos:
                    raise ValueError(f"RSS 실패({e_rss}), 동영상 탭도 비어 있음")
            if not videos:
                raise ValueError("영상 목록이 비어 있음")
            result.append({"name": ch["name"], "channelId": cid, "handle": ch.get("handle", ""),
                           "videos": carry_summaries(videos, old.get("videos", []))})
        except Exception as e:  # 한 채널 실패가 전체를 막지 않게
            errors.append(f"{ch['name']}: {e}")
            result.append({"name": ch["name"], "channelId": cid, "handle": ch.get("handle", ""), "videos": old.get("videos", [])})
    return result, errors


SYSTEM = ("너는 한국 개인투자자를 위한 증시 리서치 요약가다. 영상에서 실제로 말한 내용만 정리하고, 영상에 없는 종목·수치·전망을 지어내지 않는다. "
          "종목명은 영상에서 부른 이름 그대로 쓴다. 투자 권유가 아니라 영상 내용 요약임을 유지한다.")
PROMPT = """이 유튜브 영상을 한국어로 요약해 JSON 으로만 답해라. 형식:
{"skip": false,
 "key_summary": "영상 전체를 한두 문장으로 (결론 중심)",
 "market": ["시장·거시 진단 요점 (수치·발언 포함)", ...],
 "sectors": [{"name": "섹터/테마명", "point": "영상이 말한 핵심 논리 1~2문장", "stocks": [{"name": "종목명", "note": "언급된 이유·전망 한 줄"}]}],
 "checkpoints": ["영상이 짚은 앞으로의 체크포인트·리스크", ...]}
영상이 투자·시황과 무관하면 {"skip": true} 만 답해라. 항목이 없으면 빈 배열로 둬라."""


def clean_summary(obj):
    """모델 응답을 화면용 구조로 정리 (이상한 타입은 버림). skip/빈 응답이면 None."""
    if not isinstance(obj, dict) or obj.get("skip") or not str(obj.get("key_summary", "")).strip():
        return None
    def strs(v):
        return [str(x).strip() for x in v if str(x).strip()] if isinstance(v, list) else []
    sectors = []
    for sec in obj.get("sectors") if isinstance(obj.get("sectors"), list) else []:
        if not isinstance(sec, dict) or not str(sec.get("name", "")).strip():
            continue
        stocks = [{"name": str(s.get("name", "")).strip(), "note": str(s.get("note", "")).strip()}
                  for s in (sec.get("stocks") if isinstance(sec.get("stocks"), list) else [])
                  if isinstance(s, dict) and str(s.get("name", "")).strip()]
        sectors.append({"name": str(sec["name"]).strip(), "point": str(sec.get("point", "")).strip(), "stocks": stocks})
    return {"keySummary": str(obj["key_summary"]).strip(), "market": strs(obj.get("market")),
            "sectors": sectors, "checkpoints": strs(obj.get("checkpoints"))}


def carry_summaries(videos, old_videos):
    """이전에 만든 요약·실패 횟수를 같은 영상(url)에 이어 붙임."""
    old = {v.get("url"): v for v in old_videos}
    for v in videos:
        o = old.get(v["url"])
        if o:
            for k in ("ai", "aiFail"):
                if k in o:
                    v[k] = o[k]
    return videos


def summarize_new(channels, summarize, max_new=4, max_fail=2, budget_sec=840):
    """채널별 가장 최신 영상 1개만(요약이 없을 때) 요약. summarize(url)->obj. 혼잡이면 중단(다음 실행에 재시도)."""
    import time as _t
    t0 = _t.time()
    done, notes = 0, []
    pending = [(c["name"], v) for c in channels for v in c["videos"][:1] if "ai" not in v and v.get("aiFail", 0) < max_fail]
    pending.sort(key=lambda x: x[1]["publishedAt"], reverse=True)
    for name, v in pending:
        if done >= max_new:
            break
        if _t.time() - t0 > budget_sec:
            notes.append("시간 제한(14분)에 도달: 남은 영상은 다음 실행에 요약")
            break
        try:
            res = clean_summary(summarize(v["url"]))
        except Exception as e:
            if e.__class__.__name__ == "GeminiBusy":
                notes.append(f"제미나이 혼잡/한도(다음 실행에 재시도): {str(e)[:160]}")
                break
            v["aiFail"] = v.get("aiFail", 0) + 1
            notes.append(f"{name} 요약 실패: {e}")
            continue
        if res is None:
            v["ai"] = {"skip": True}
        else:
            v["ai"] = res
        done += 1
    return done, notes


def safe_status(lines):
    """화면에 보일 AI 상태 메시지. 키처럼 보이는 문자열은 가리고 길이를 제한."""
    import re
    out = []
    for l in lines:
        l = re.sub(r"AIza[\w-]{10,}", "[키]", str(l))
        out.append(l[:220])
    return out[:6]


def write(channels, path=TARGET, status=None):
    payload = {"asOf": datetime.now(KST).strftime("%Y-%m-%d %H:%M"), "channels": channels}
    if status:
        payload["aiStatus"] = safe_status(status)
    with open(path, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/collect_youtube.py). 직접 고치지 마세요. 채널은 scanner/youtube_channels.json 에서 바꿉니다.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.youtube = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")


def main():
    with open(os.path.join(HERE, "youtube_channels.json"), encoding="utf-8") as f:
        channels = json.load(f)
    result, errors = build(channels, load_previous())
    if not any(c["videos"] for c in result):
        raise SystemExit("영상을 하나도 받지 못했습니다: " + "; ".join(errors))
    status = []
    try:
        import gemini
        if os.environ.get("YOUTUBE_AI", "").strip() not in ("1", "true", "on"):
            print("유튜브 AI 요약 꺼짐 (켜려면 워크플로 환경변수 YOUTUBE_AI=1)")
        elif gemini.api_key():
            gemini.set_deadline(780)   # 13분 안에 끝냄 (워크플로 제한 30분 대비 여유)
            n, notes = summarize_new(result, lambda url: gemini.generate(PROMPT, system=SYSTEM, video_url=url, want_json=True, max_tokens=8192, retries=1))
            print(f"AI 요약 {n}건 생성")
            errors += notes
            try:
                model = gemini.used_model()
            except Exception as e:
                model = f"모델 조회 실패 {e}"
            status = [f"모델 {model} · 이번 실행에서 {n}건 요약"] + notes
        else:
            print("GEMINI_API_KEY 없음: 요약 건너뜀")
            status = ["제미나이 키를 못 찾음: GitHub Settings → Secrets and variables → Actions 의 'Repository secrets' 에 GEMINI_API_KEY 로 등록했는지 확인"]
    except Exception as e:
        errors.append(f"AI 요약 단계 오류: {e}")
        status = [f"AI 요약 단계 오류: {e}"]
    write(result, status=status)
    for e in errors:
        print("경고:", e)
    print("유튜브 갱신:", ", ".join(f"{c['name']} {len(c['videos'])}개" for c in result))


if __name__ == "__main__":
    main()
