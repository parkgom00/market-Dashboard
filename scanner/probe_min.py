import json, os
import naver_live as nl
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
res = {}
def tryit(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        res[name] = f"ERR {type(e).__name__}: {e}"
def minutes(code, a, b):
    rows = nl._get(f"https://api.stock.naver.com/chart/domestic/item/{code}/minute?startDateTime={a}&endDateTime={b}", tries=1)
    days = {}
    for r in rows:
        d = str(r["localDateTime"])[:8]; days[d] = days.get(d, 0) + 1
    return {"n": len(rows), "per_day": days, "first": rows[0] if rows else None, "last": rows[-1] if rows else None}
tryit("min_2days", lambda: minutes("005930", "202610060900", "202610071600"))
tryit("min_3days", lambda: minutes("005930", "202610020900", "202610071600"))
def up(mk):
    j = nl._get(f"https://m.stock.naver.com/api/stocks/up/{mk}", {"page": 1, "pageSize": 100}, tries=1)
    rows = j.get("stocks") or []
    return {"n": len(rows), "keys": sorted(rows[0].keys()) if rows else [], "top": [(r.get("stockName"), r.get("fluctuationsRatio"), r.get("highPrice")) for r in rows[:5]]}
tryit("up_KOSPI", lambda: up("KOSPI"))
tryit("up_KOSDAQ", lambda: up("KOSDAQ"))
def day(code):
    j = nl._get(f"https://api.stock.naver.com/chart/domestic/item/{code}/day?startDateTime=202609300000&endDateTime=202610080000", tries=1)
    return j[-3:] if isinstance(j, list) else str(j)[:300]
tryit("day_chart", lambda: day("042510"))
json.dump(res, open(os.path.join(OUT, "min_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
