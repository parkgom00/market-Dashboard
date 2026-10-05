"""네이버 응답 형식을 흉내 낸 가짜 데이터로 파싱·조립을 검증합니다 (인터넷 불필요). 실행: python test_news.py"""
import json
import os
import tempfile
from datetime import datetime, timedelta, timezone

import build_live
from fetch_news import KST, parse_items

NOW = datetime(2026, 10, 5, 16, 0, tzinfo=KST)
payload = {"items": [
    {"title": "<b>[특징주]</b> 에이사 &quot;수주 소식&quot;에 강세", "originallink": "https://www.news-a.co.kr/1",
     "link": "https://n.news.naver.com/x", "pubDate": "Mon, 05 Oct 2026 15:42:00 +0900"},
    {"title": "[특징주] 비사 실적 우려에 약세", "originallink": "https://news-b.com/2",
     "link": "", "pubDate": "Sun, 04 Oct 2026 10:05:00 +0900"},
    {"title": "[특징주] 비사 실적 우려에 약세", "originallink": "https://news-b.com/dup",
     "link": "", "pubDate": "Sun, 04 Oct 2026 10:06:00 +0900"},                      # 중복 제목
    {"title": "오늘의 증시 전망", "originallink": "https://news-c.com/3",
     "link": "", "pubDate": "Mon, 05 Oct 2026 09:00:00 +0900"},                      # 키워드 없음
    {"title": "[특징주] 해외시각 기사", "originallink": "https://news-d.com/4",
     "link": "", "pubDate": "Mon, 05 Oct 2026 06:30:00 +0000"},                      # UTC → KST 변환
]}

ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


rows = parse_items(payload, now=NOW)
check("키워드 없는 기사 제외 + 중복 제목 제거 (5건 → 3건)", len(rows) == 3)
check("HTML 태그·엔티티 제거", rows[0]["title"] == '[특징주] 에이사 "수주 소식"에 강세')
check("최신순 정렬", [r["source"] for r in rows] == ["news-a.co.kr", "news-d.com", "news-b.com"])
check("오늘 기사는 시:분, 이전 기사는 월/일 시:분", rows[0]["time"] == "15:42" and rows[2]["time"] == "10/04 10:05")
check("UTC 시각을 한국시간으로 변환 (06:30 UTC → 15:30)", rows[1]["time"] == "15:30")
check("출처는 도메인(www 제거)", rows[0]["source"] == "news-a.co.kr")
check("조각 없음 → 빈 응답", parse_items({}, now=NOW) == [])

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "live_news.json"), "w", encoding="utf-8") as f:
        json.dump({"items": rows}, f, ensure_ascii=False)
    target = os.path.join(d, "live.js")
    out = build_live.build(d, target)
    txt = open(target, encoding="utf-8").read()
    check("뉴스만 있으면 국내 news 만 생기고 순위·테마 키는 없음 (화면에서 숨김)", set(out["kr"]) == {"news"} and out["us"] == {})
    check("live.js 가 window.DASH.live 로 시작", "window.DASH.live = " in txt)

print(f"\n{sum(ok)}/{len(ok)} 통과")
raise SystemExit(0 if all(ok) else 1)
