import json, os
import naver_live as nl
HERE = os.path.dirname(os.path.abspath(__file__))
picks = json.load(open(os.path.join(HERE, "out", "short_picks.json"), encoding="utf-8"))
codes = sorted({r["code"] for v in picks.values() for r in v["rows"]})
out = {}
for c in codes:
    try:
        rows = nl._get(f"https://api.stock.naver.com/chart/domestic/item/{c}/day?startDateTime=202610010000&endDateTime=202610130000", tries=2)
        out[c] = {r["localDate"]: [r["openPrice"], r["highPrice"], r["lowPrice"], r["closePrice"]] for r in rows}
    except Exception as e:
        out[c] = f"ERR {e}"
json.dump(out, open(os.path.join(HERE, "out", "short_next_prices.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
