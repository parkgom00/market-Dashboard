"""대표 기업 실적 발표 예정일 수집 (yfinance, 무료) → out/earnings.json.

scanner/earnings_watch.json 의 기업만 봅니다. 발표 시각은 한국시간으로 바꿔 날짜를 정합니다
(미국 장 마감 후 발표는 한국시간 다음 날 새벽). 예정일은 데이터 제공처 추정이라 바뀔 수 있어
제목에 '(예정)'을 붙입니다. 확정일은 calendar_manual.json 에 직접 적으면 우선합니다.
"""
import json
import os
from datetime import datetime, timedelta, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = timezone(timedelta(hours=9))


def to_kst_date(ts):
    """tz 있는 시각 → 한국 날짜. 자정(시각 없음)은 개장 전 발표로 보고 오전 8시로 간주."""
    ts = pd.Timestamp(ts)
    if ts.tzinfo is None:
        ts = ts.tz_localize("America/New_York")
    if ts.hour == 0 and ts.minute == 0:
        ts = ts.replace(hour=8)
    return ts.tz_convert(KST).strftime("%Y-%m-%d")


def upcoming(dates, today, horizon_days=130):
    """오늘 이후 horizon 안의 날짜 중 가장 이른 것 하나 (지난 분기 기록과 먼 미래 추정은 제외)."""
    lo = today.strftime("%Y-%m-%d")
    hi = (today + timedelta(days=horizon_days)).strftime("%Y-%m-%d")
    c = sorted(d for d in dates if lo <= d <= hi)
    return c[:1]


def kr_business_days(start, n):
    """start 다음 날부터 센 한국 영업일 n번째 날 (주말·공휴일 제외)."""
    try:
        import holidays
        hol = holidays.country_holidays("KR", years=[start.year, start.year + 1])
    except Exception:
        hol = {}
    d, k = start, 0
    while k < n:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in hol:
            k += 1
    return d


def prelim_estimate(today, nth=5):
    """잠정실적(삼성전자·LG전자처럼 분기 끝나고 1~2주 안에 먼저 내는 곳)의 다음 예상일: 분기 마지막 날 뒤 n번째 영업일."""
    from datetime import date
    for y in (today.year, today.year + 1):
        for m in (1, 4, 7, 10):
            q_end = date(y, m, 1) - timedelta(days=1)
            d = kr_business_days(q_end, nth)
            if d >= today:
                return d.isoformat()
    return None


def build_events(found, watch, today):
    """found: {ticker: [KST 날짜...]} → 캘린더 이벤트 목록."""
    out = []
    for market, items in watch.items():
        for it in items:
            label = "확정실적·컨퍼런스콜" if it.get("prelim") else "실적 발표"
            for d in upcoming(found.get(it["ticker"], []), today):
                out.append({"date": d, "type": "earnings", "market": market, "title": f"{it['name']} {label} (예정)"})
            if it.get("prelim"):
                d = prelim_estimate(today)
                if d:
                    out.append({"date": d, "type": "earnings", "market": market, "title": f"{it['name']} 잠정실적 (예상일·하루이틀 차이 가능)"})
    return out


def main():
    import yfinance as yf
    with open(os.path.join(HERE, "earnings_watch.json"), encoding="utf-8") as f:
        watch = json.load(f)
    found, errs = {}, []
    for items in watch.values():
        for it in items:
            try:
                ed = yf.Ticker(it["ticker"]).get_earnings_dates(limit=8)
                found[it["ticker"]] = [to_kst_date(i) for i in ed.index] if ed is not None else []
            except Exception as e:
                errs.append(f"{it['ticker']}: {e}")
    events = build_events(found, watch, datetime.now(KST).date())
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "earnings.json"), "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=1)
    print(f"실적 예정 {len(events)}건", ("경고 " + str(len(errs)) + "건: " + "; ".join(errs[:3])) if errs else "")


if __name__ == "__main__":
    main()
