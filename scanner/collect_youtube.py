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
        cid = old.get("channelId") or ""
        try:
            if not cid:
                cid = find_channel_id(fetch("https://www.youtube.com/" + urllib.parse.quote(ch["handle"]))) or ""
                if not cid:
                    raise ValueError("채널 ID를 찾지 못함")
            videos = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
            if not videos:
                raise ValueError("영상 목록이 비어 있음")
            result.append({"name": ch["name"], "channelId": cid, "handle": ch["handle"], "videos": videos})
        except Exception as e:  # 한 채널 실패가 전체를 막지 않게
            errors.append(f"{ch['name']}: {e}")
            result.append({"name": ch["name"], "channelId": cid, "handle": ch["handle"], "videos": old.get("videos", [])})
    return result, errors


def write(channels, path=TARGET):
    payload = {"asOf": datetime.now(KST).strftime("%Y-%m-%d %H:%M"), "channels": channels}
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
    write(result)
    for e in errors:
        print("경고:", e)
    print("유튜브 갱신:", ", ".join(f"{c['name']} {len(c['videos'])}개" for c in result))


if __name__ == "__main__":
    main()
