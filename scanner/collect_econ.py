"""발표된 경제지표의 결과를 FRED(세인트루이스 연준, 키 불필요 CSV)에서 받아 out/econ_results.json 으로 저장.

키 "IND|기준월" → 표시할 줄 목록. 예) "CPI|2026-09": ["전월 대비 +0.3%", "전년 대비 +2.9%", ...]
FOMC 는 "FOMC|발표일(한국)" → 정책금리 상단 변화.
build_calendar.py 가 발표일이 지난 일정에만 이 결과를 붙입니다.
"""
import io
import json
import os
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="


def fetch_series(sid):
    req = urllib.request.Request(FRED + sid, headers={"User-Agent": "Mozilla/5.0 (market-dashboard)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        df = pd.read_csv(io.StringIO(r.read().decode()))
    df.columns = ["date", "v"]
    df["v"] = pd.to_numeric(df["v"], errors="coerce")
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["v"]


def _sgn(x, unit="%", nd=1):
    return f"{x:+.{nd}f}{unit}"


def month_rows(s, ym):
    """월별 시리즈 s 에서 기준월 ym('2026-09')의 (값, 직전월 값, 전년동월 값). 없으면 None."""
    idx = pd.Period(ym, "M")
    ser = s.copy()
    ser.index = ser.index.to_period("M")
    if idx not in ser.index:
        return None
    prev = ser.get(idx - 1)
    yoy = ser.get(idx - 12)
    return float(ser[idx]), (None if prev is None else float(prev)), (None if yoy is None else float(yoy))


def price_lines(head, cur, core):
    out = []
    for label, r in ((head, cur), ("근원", core)):
        if r is None:
            continue
        v, p, y = r
        parts = []
        if p:
            parts.append("전월 대비 " + _sgn((v / p - 1) * 100, nd=2))
        if y:
            parts.append("전년 대비 " + _sgn((v / y - 1) * 100, nd=1))
        if parts:
            out.append(f"{label}: " + " · ".join(parts))
    return out


def jobs_lines(payems_r, unrate_r):
    out = []
    if payems_r and payems_r[1] is not None:
        d = payems_r[0] - payems_r[1]
        out.append(f"비농업 고용: 전월 대비 {d:+,.0f}천 명")
    if unrate_r:
        v, p, _ = unrate_r
        s = f"실업률: {v:.1f}%"
        if p is not None:
            s += f" (전월 {p:.1f}%, {v - p:+.1f}%p)"
        out.append(s)
    return out


def fomc_lines(upper, date_str, prev_date_str):
    """정책금리 상단(DFEDTARU): 결정일 직후 값과 직전 회의 직후 값."""
    def at(ds):
        x = upper[upper.index <= pd.Timestamp(ds)]
        return None if x.empty else float(x.iloc[-1])
    cur, prev = at(date_str), at(prev_date_str) if prev_date_str else None
    if cur is None:
        return []
    if prev is None or abs(cur - prev) < 1e-9:
        return [f"기준금리 상단 {cur:.2f}% (동결)"]
    return [f"기준금리 상단 {cur:.2f}% (직전 {prev:.2f}%, {(cur - prev) * 100:+.0f}bp)"]


def build_results(series, events):
    """series: {FRED id: Series}. events: calendar_fixed 의 이벤트 목록."""
    res = {}
    for e in events:
        ind, ref = e.get("ind"), e.get("ref")
        if ind == "CPI" and "CPIAUCSL" in series:
            lines = price_lines("전체", month_rows(series["CPIAUCSL"], ref), month_rows(series["CPILFESL"], ref))
        elif ind == "PCE" and "PCEPI" in series:
            lines = price_lines("전체", month_rows(series["PCEPI"], ref), month_rows(series["PCEPILFE"], ref))
        elif ind == "JOBS" and "PAYEMS" in series:
            lines = jobs_lines(month_rows(series["PAYEMS"], ref), month_rows(series["UNRATE"], ref))
        else:
            continue
        if lines:
            res[f"{ind}|{ref}"] = lines
    fomc = sorted(e["date"] for e in events if e.get("ind") == "FOMC")
    if "DFEDTARU" in series:
        for i, d in enumerate(fomc):
            # 한국 날짜 기준 새벽 발표 = 미국 전날 결정. 값은 해당 한국 날짜 기준으로 조회
            lines = fomc_lines(series["DFEDTARU"], d, fomc[i - 1] if i else None)
            if lines:
                res[f"FOMC|{d}"] = lines
    return res


def main():
    with open(os.path.join(HERE, "calendar_fixed.json"), encoding="utf-8") as f:
        events = json.load(f)["events"]
    series, errs = {}, []
    for sid in ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE", "PAYEMS", "UNRATE", "DFEDTARU"]:
        try:
            series[sid] = fetch_series(sid)
        except Exception as e:
            errs.append(f"{sid}: {e}")
    res = build_results(series, events)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "econ_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(f"경제지표 결과 {len(res)}건", ("경고: " + "; ".join(errs)) if errs else "")


if __name__ == "__main__":
    main()
