import json, os
import collect_m480 as m, naver_live
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
day = "20261007"
uni, _ = naver_live.fetch_universe()
cands = sorted(uni, key=lambda c: -(uni[c].get("value") or 0))[:300]
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(6) as ex:
    bars = dict(zip(cands, ex.map(lambda c: m.fetch_bars(c, day), cands)))
res = {"n_bars": sum(1 for b in bars.values() if b), "sample_len": len(next(iter(bars.values()), [])), "slots": {}}
rose = []
for c in cands:
    td = [b for b in bars[c] if b[0] == day]; pv = [b for b in bars[c] if b[0] < day]
    if td and pv and max(b[3] for b in td) / pv[-1][5] - 1 >= 0.15:
        rose.append(uni[c]["name"])
res["rose15"] = rose
for upto in ("1000", "1030", "1100", "1130", "1200", "1400"):
    rows, why = [], {}
    for c in cands:
        d, reason = m.judge(bars[c], day, upto)
        if d:
            rows.append((uni[c]["name"], m.note(d)))
        elif reason not in ("장중 +15% 미달", "오늘 분봉 부족"):
            why[reason] = why.get(reason, 0) + 1
    res["slots"][upto] = {"hits": rows, "why_among_rose": why}
json.dump(res, open(os.path.join(OUT, "m480_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
