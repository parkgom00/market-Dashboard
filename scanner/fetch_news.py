"""네이버 검색 API(뉴스)로 [특징주] 헤드라인을 수집합니다.

준비 (한 번만):
  1) https://developers.naver.com 에서 애플리케이션 등록 → '검색' API 사용 선택
  2) 발급된 Client ID / Client Secret 을 환경변수로 설정
       Windows(PowerShell):  $env:NAVER_CLIENT_ID="..."; $env:NAVER_CLIENT_SECRET="..."
       GitHub Actions:       저장소 Settings → Secrets 에 같은 이름으로 등록 (코드나 파일에 절대 적지 마세요)

실행:  python fetch_news.py
결과:  scanner/out/live_news.json 저장 후 ../data/live.js 를 다시 만듭니다.

제목과 원문 링크만 저장합니다 (기사 본문은 가져오지 않음).
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = timezone(timedelta(hours=9))
TAG = re.compile(r"<[^>]+>")
KEYWORD = "[특징주]"


def clean(text: str) -> str:
    return html.unescape(TAG.sub("", text or "")).strip()


def parse_items(payload: dict, keyword: str = KEYWORD, limit: int = 30, now=None):
    """API 응답(dict) → 화면용 뉴스 목록. 제목에 keyword 가 있는 것만, 중복 제목 제거, 최신순."""
    now = now or datetime.now(KST)
    seen, rows = set(), []
    for it in payload.get("items", []):
        title = clean(it.get("title", ""))
        if keyword not in title:
            continue
        key = re.sub(r"\s+", "", title)
        if key in seen:
            continue
        seen.add(key)
        try:
            dt = parsedate_to_datetime(it["pubDate"]).astimezone(KST)
        except Exception:
            dt = None
        url = it.get("originallink") or it.get("link") or ""
        rows.append({
            "ts": dt.timestamp() if dt else 0,
            "time": "" if not dt else (dt.strftime("%H:%M") if dt.date() == now.date() else dt.strftime("%m/%d %H:%M")),
            "title": title,
            "source": urlparse(url).netloc.replace("www.", ""),
            "url": url,
        })
    rows.sort(key=lambda r: -r["ts"])
    for r in rows:
        r.pop("ts")
    return rows[:limit]


def fetch_payload(client_id: str, client_secret: str, pages: int = 2) -> dict:
    items = []
    for i in range(pages):
        q = urllib.parse.urlencode({"query": "특징주", "display": 100, "start": 1 + i * 100, "sort": "date"})
        req = urllib.request.Request(
            "https://openapi.naver.com/v1/search/news.json?" + q,
            headers={"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            items += json.load(r).get("items", [])
    return {"items": items}


def main():
    cid, sec = os.environ.get("NAVER_CLIENT_ID"), os.environ.get("NAVER_CLIENT_SECRET")
    if not cid or not sec:
        print("환경변수 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 이 없습니다. 파일 상단 설명을 참고하세요.")
        sys.exit(1)
    rows = parse_items(fetch_payload(cid, sec))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "live_news.json"), "w", encoding="utf-8") as f:
        json.dump({"items": rows}, f, ensure_ascii=False)
    print(f"[특징주] 뉴스 {len(rows)}건 저장")
    import build_live
    build_live.build()
    print("data/live.js 갱신 완료")


if __name__ == "__main__":
    main()
