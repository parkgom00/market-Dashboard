"""data/calendar.js 생성.

합치는 것 (겹치는 같은 날짜·시장의 휴장은 하나만 남김):
  1) calendar_fixed.json   공식 사이트에서 확인한 일정 (미국 휴장, FOMC, CPI, 고용보고서 등)
  2) holidays 라이브러리    한국·미국 공휴일 자동 보충 (설치되어 있을 때만)
  3) 한국거래소 추가 휴장   5/1 근로자의 날, 연말 마지막 영업일
  4) calendar_manual.json  사용자가 직접 적는 일정 (확정 실적 발표일, 기타 이벤트)
  5) out/earnings.json     대표 기업 실적 예정일 (collect_earnings.py, 자동·추정)
  + out/econ_results.json  발표 완료된 지표의 결과 (collect_econ.py) → 해당 일정의 result

calendar_manual.json 형식:
  [{"date": "2026-10-21", "type": "earnings", "market": "US", "title": "테슬라 실적 발표"}]
  type: holiday(휴장) | econ(경제지표) | earnings(실적) | event(이벤트)   market: KR | US
"""
import json
import os
from datetime import date, datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "data", "calendar.js")
KST = timezone(timedelta(hours=9))
TYPES = {"holiday", "econ", "earnings", "event"}


def _read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def library_holidays(years):
    """holidays 라이브러리의 한국 공휴일. 설치되어 있지 않으면 빈 목록."""
    try:
        import holidays
    except ImportError:
        return []
    try:
        kr = holidays.country_holidays("KR", years=years, language="ko")
    except Exception:
        kr = holidays.country_holidays("KR", years=years)
    return [{"date": d.isoformat(), "type": "holiday", "market": "KR", "title": f"{name} (증시 휴장)"} for d, name in kr.items()]


def krx_extra_closures(years):
    """한국거래소는 공휴일이 아니어도 5/1(근로자의 날)과 연말 마지막 영업일에 쉽니다."""
    out = []
    for y in years:
        may1 = date(y, 5, 1)
        out.append({"date": may1.isoformat(), "type": "holiday", "market": "KR", "title": "근로자의 날 (증시 휴장)"})
        d = date(y, 12, 31)
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        out.append({"date": d.isoformat(), "type": "holiday", "market": "KR", "title": "연말 휴장 (증시)"})
    return out


def merge(fixed, extra_lists, manual):
    """휴장은 (날짜, 시장) 당 하나만, 나머지는 그대로. 주말 휴장은 제외. 형식 오류는 건너뜀."""
    events, seen_holiday = [], set()
    for e in list(fixed) + [x for lst in extra_lists for x in lst] + list(manual):
        try:
            d = date.fromisoformat(e["date"])
        except Exception:
            continue
        if e.get("type") not in TYPES or not e.get("title"):
            continue
        if e["type"] == "holiday":
            if d.weekday() >= 5:
                continue
            key = (e["date"], e.get("market"))
            if key in seen_holiday:
                continue
            seen_holiday.add(key)
        ev = {"date": e["date"], "type": e["type"], "market": e.get("market", ""), "title": e["title"]}
        for k in ("ind", "ref"):
            if e.get(k):
                ev[k] = e[k]
        events.append(ev)
    events.sort(key=lambda e: (e["date"], e["market"], e["title"]))
    return events


def _load_out(name):
    path = os.path.join(HERE, "out", name)
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except ValueError:
            pass
    return None


def attach_results(events, results, today):
    """발표일이 지난 지표에 결과 줄(result)을 붙이고, 내부용 ind/ref 는 제거."""
    for e in events:
        ind, ref = e.pop("ind", None), e.pop("ref", None)
        if not ind or e["date"] > today.isoformat():
            continue
        key = f"FOMC|{e['date']}" if ind == "FOMC" else f"{ind}|{ref}"
        if results.get(key):
            e["result"] = results[key]
    return events


def dedupe_earnings(events):
    """같은 날 같은 제목은 하나만 (자동 수집 + 수동 입력 중복 방지). 수동 입력(제목에 '(예정)' 없음)을 남김."""
    best = {}
    for e in events:
        if e["type"] != "earnings":
            continue
        name = e["title"].replace(" (예정)", "")
        k = (e["market"], name)
        if k in best:
            old = best[k]
            if "(예정)" in old["title"] and "(예정)" not in e["title"]:
                best[k] = e
            continue
        best[k] = e
    keep = set(id(v) for v in best.values())
    return [e for e in events if e["type"] != "earnings" or id(e) in keep]


def build(target=TARGET, today=None):
    today = today or datetime.now(KST).date()
    years = [today.year, today.year + 1]
    events = merge(_read("calendar_fixed.json")["events"],
                   [library_holidays(years), krx_extra_closures(years)],
                   _read("calendar_manual.json") + (_load_out("earnings.json") or []))
    events = dedupe_earnings(events)
    events = attach_results(events, _load_out("econ_results.json") or {}, today)
    payload = {"generatedAt": datetime.now(KST).strftime("%Y-%m-%d %H:%M"), "events": events}
    with open(target, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/build_calendar.py). 직접 고치지 마세요. 일정을 더하려면 scanner/calendar_manual.json 을 수정하세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.calendar = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    return payload


if __name__ == "__main__":
    p = build()
    print(f"캘린더 {len(p['events'])}건 생성")
