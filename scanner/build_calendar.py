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
  결과를 함께 적으려면 "extra": ["매출 …", "영업이익 …"] (날짜를 누르면 아래에 표시)
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
        for k in ("ind", "ref", "time", "major", "extra"):
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


def _market_of(title):
    for pre, m in (("한국", "KR"), ("BOJ", "JP"), ("중국", "CN")):
        if title.startswith(pre):
            return m
    return "US"


def attach_nasdaq(events, nas):
    """나스닥 캘린더를 합침. 공식 일정(ind)이 있는 지표 계열은 그 일정에 예상/실제/이전 줄(extra)로 붙이고,
    그 밖의 지표·실적은 독립 일정으로 추가."""
    import collect_nasdaq_calendar as nc
    by = {(e["ind"], e["date"]): e for e in events if e.get("ind")}
    out = list(events)
    for n in nas:
        lines = nc.lines_for(n)
        fam = nc.family_of(n["title"]) if n["kind"] == "econ" else None
        host = by.get((fam, n["date"])) if fam else None
        if host is not None:
            if lines:
                host.setdefault("extra", []).append(f"{n['title']}: {lines[0]}")
            if n.get("time") and not host.get("time"):
                host["time"] = n["time"]
            continue
        ev = {"date": n["date"], "type": "earnings" if n["kind"] == "earnings" else "econ", "market": _market_of(n["title"]) if n["kind"] == "econ" else "US",
              "title": n["title"]}
        if n.get("time"):
            ev["time"] = n["time"]
        if n.get("level") == "major":
            ev["major"] = True
        if lines:
            ev["extra"] = lines
        out.append(ev)
    return out


def attach_results(events, results, today):
    """발표일이 지난 지표에 FRED 결과를, 모든 일정에 나스닥 예상/실제 줄(extra)을 result 로 합쳐 붙임. 내부용 ind/ref 는 제거."""
    for e in events:
        ind, ref = e.pop("ind", None), e.pop("ref", None)
        lines = []
        if ind and e["date"] <= today.isoformat():
            key = f"FOMC|{e['date']}" if ind == "FOMC" else f"{ind}|{ref}"
            lines += results.get(key, [])
        lines += e.pop("extra", [])
        if lines:
            e["result"] = lines
    return events


def expiry_events(years, closed_kr):
    """규칙으로 정해지는 만기일. 한국 옵션 만기=매월 둘째 목요일(휴장이면 앞 영업일, 3·6·9·12월은 선물옵션 동시만기),
    미국 옵션 만기=매월 셋째 금요일(3·6·9·12월은 쿼드러플 위칭)."""
    out = []
    for y in years:
        for m in range(1, 13):
            d = date(y, m, 1)
            thu = [d + timedelta(days=i) for i in range(31) if (d + timedelta(days=i)).month == m and (d + timedelta(days=i)).weekday() == 3][1]
            while thu.weekday() >= 5 or thu.isoformat() in closed_kr:
                thu -= timedelta(days=1)
            quad = m in (3, 6, 9, 12)
            out.append({"date": thu.isoformat(), "type": "event", "market": "KR",
                        "title": "선물옵션 동시만기일 (변동성 주의)" if quad else "옵션 만기일"})
            fri = [d + timedelta(days=i) for i in range(31) if (d + timedelta(days=i)).month == m and (d + timedelta(days=i)).weekday() == 4][2]
            out.append({"date": fri.isoformat(), "type": "event", "market": "US",
                        "title": "미국 쿼드러플 위칭 (한국시간 토요일 새벽 마감)" if quad else "미국 옵션 만기일"})
    return out


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
    closed_kr = {e["date"] for e in events if e["type"] == "holiday" and e.get("market") == "KR"}
    events += [x for x in expiry_events(years, closed_kr) if date.fromisoformat(x["date"]).weekday() < 6]
    events = attach_nasdaq(events, _load_out("nasdaq_calendar.json") or [])
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
