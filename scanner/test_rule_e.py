"""중장기 e (기관 연속 순매수 + 240일선 돌파 + 저점 상승) 점검."""
import numpy as np
import pandas as pd

import rules2
from rules import add_indicators

ok = fail = 0


def check(name, cond):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        print("FAIL", name)


def make(closes):
    c = np.array(closes, dtype=float)
    idx = pd.bdate_range("2024-01-01", periods=len(c))
    df = pd.DataFrame({"open": c, "high": c * 1.01, "low": c * 0.99, "close": c, "volume": 1e6}, index=idx)
    return add_indicators(df)


# 1년 넘게 100 근처 횡보 → 60일 동안 계단식 상승해 10일 전 240일선(≈100) 돌파
base = [100 + (i % 5 - 2) * 0.3 for i in range(300)]
up = list(np.linspace(94, 99, 50)) + list(np.linspace(101, 106, 10))
df = make(base + up)
r = rules2.long_e_price(df)
check("price pass", r is not None and r["lows"][0] < r["lows"][1] < r["lows"][2])
check("cross recent", r and r["cross"].endswith("일 전"))

# 이미 20일 넘게 240일선 위 → 돌파 아님
df2 = make(base + list(np.linspace(101, 110, 60)))
check("no fresh cross", rules2.long_e_price(df2) is None)

# 저점이 낮아짐 → 탈락
down = list(np.linspace(99, 92, 50)) + list(np.linspace(101, 103, 10))
check("falling lows", rules2.long_e_price(make(base + down)) is None)

# 240일선이 크게 하락 중 → 탈락
fall = list(np.linspace(160, 95, 300))
check("ma240 falling", rules2.long_e_price(make(fall + up)) is None)

# 돌파 후 2% 넘게 이탈 → 탈락
brk = list(np.linspace(94, 99, 50)) + [101, 102, 103, 95, 101, 102, 103, 104, 105, 106]
check("broke back", rules2.long_e_price(make(base + brk)) is None)


def rows(o, f=None):
    f = f or [0] * len(o)
    return [{"date": f"10/{10 - i:02d}", "o": a * 1e8, "f": b * 1e8} for i, (a, b) in enumerate(zip(o, f))]


good = rows([5, 3, 2, 4, -1, 3, 2, -2, 4, 3])
fl = rules2.inst_flow_ok(good)
check("flow pass", fl and fl["streak"] == 4 and fl["pos"] == 8 and round(fl["o"] / 1e8) == 23)
check("flow short", rules2.inst_flow_ok(good[:9]) is None)
check("flow no streak", rules2.inst_flow_ok(rows([5, -1, 2, 4, 1, 3, 2, 2, 4, 3])) is None)
check("flow too small", rules2.inst_flow_ok(rows([0.2] * 10)) is None)
check("flow foreign leads", rules2.inst_flow_ok(rows([3] * 10, [5] * 10)) is None)
check("flow few days", rules2.inst_flow_ok(rows([5, 5, 5, -1, -1, -1, -1, 5, 5, 5])) is None)
note = rules2.LONG_NOTE["L5"](dict(r, **fl))
check("note", "기관 4일 연속" in note and "240일선" in note and "→" in note)
print(note)
print(f"{ok}/{ok + fail}")
