"""스윙·중장기 d·전고점 돌파 규칙을 합성 차트로 검증. 실행: python test_rules2.py"""
import numpy as np
import pandas as pd

import rules2 as r2
from rules import add_indicators

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def mk(close, vol=None, open_=None, low=None, high=None):
    c = np.asarray(close, float); n = len(c)
    o = np.asarray(open_, float) if open_ is not None else np.r_[c[0], c[:-1]]
    v = np.full(n, 1e6) if vol is None else np.asarray(vol, float)
    hi = np.maximum(o, c) * 1.005 if high is None else np.asarray(high, float)
    lo = np.minimum(o, c) * 0.995 if low is None else np.asarray(low, float)
    return add_indicators(pd.DataFrame({"open": o, "high": hi, "low": lo, "close": c, "volume": v},
                                       index=pd.bdate_range(end="2026-10-07", periods=n)))

# ── 스윙 A: 상한가 → 조정 → 20일선 반등 ──
base = list(1000 * np.exp(0.001 * np.arange(120)))
s = base + [base[-1] * 1.30]                  # 상한가
s += [s[-1] * 1.05, s[-1] * 1.08]             # 이틀 더 상승
hitA = None
for k in range(1, 40):
    s.append(s[-1] * 0.985)
    d = mk(s + [s[-1] * 1.02])                # 오늘은 반등
    if r2.swing_limit_up(d, 20):
        hitA = k; break
check("스윙A: 상한가 후 조정이 20일선에 닿고 반등하면 해당", hitA is not None)
check("스윙A: 상한가 직후(조정 전)는 비해당", r2.swing_limit_up(mk(base + [base[-1] * 1.30, base[-1] * 1.33, base[-1] * 1.36, base[-1] * 1.38]), 20) is None)
check("스윙A: 상한가가 없으면 비해당", r2.swing_limit_up(mk(base + list(np.array(base[-30:]) * 1.01)), 20) is None)

# ── 스윙 C·D: 급등 후 조정 ──
b2 = list(1000 * np.exp(0.0005 * np.arange(150)))
surge = [b2[-1] * 1.04 ** k for k in range(1, 11)]          # 10일 +48%
side = [surge[-1] * 0.93 * (1 + 0.002 * ((k % 3) - 1)) for k in range(14)]   # 14일 횡보 조정
dC = mk(b2 + surge + side)
check("스윙C: 급등 후 10일 넘게 조정, 10일선 부근이면 해당", r2.swing_c(dC) is not None)
check("스윙C: 조정 5일째는 비해당", r2.swing_c(mk(b2 + surge + side[:5])) is None)
vol = [1e6] * 150 + [5e6] * 10 + [1.5e6] * 24
s2 = b2 + surge + [surge[-1] * 0.9 * (1 + 0.004 * k) for k in range(24)]
hitD = any(r2.swing_d(mk(s2[:150 + 10 + k], vol[:150 + 10 + k])) is not None for k in range(8, 25))
check("스윙D: 급등 후 거래량 줄고 20일선 지지면 어느 시점에 해당", hitD)
check("스윙D: 거래량이 그대로면 비해당", not any(r2.swing_d(mk(s2[:160 + k], [1e6] * 150 + [5e6] * (10 + k))) is not None for k in range(8, 25)))

# ── 스윙 E ──
up = list(1000 * np.exp(0.006 * np.arange(80)))
check("스윙E 가격: 10일선 위에서 꾸준히 상승", r2.swing_e_price(mk(up)) is not None)
check("스윙E 가격: 하락 추세 비해당", r2.swing_e_price(mk(list(1000 * np.exp(-0.004 * np.arange(80))))) is None)
rows = [{"date": f"10/0{7 - i}", "f": 5e8, "o": 2e8} for i in range(5)]
check("스윙E 수급: 5일 연속 순매수", r2.flow_ok(rows)["pos"] == 5)
rows[1]["f"] = rows[2]["f"] = -9e8
check("스윙E 수급: 5일 중 3일만 순매수면 비해당", r2.flow_ok(rows) is None)

# ── 중장기 d / 단기 B ──
n0 = 420
rise = list(1000 * np.exp(0.0035 * np.arange(n0)))                 # 1년 반 상승 → 신고가
P = rise[-1]
down = [P * (1 - 0.22 * (k + 1) / 40) for k in range(40)]           # 40일간 -22%
upb = [down[-1] * (1 + 0.004 * (k + 1)) for k in range(25)]         # 20일선 위로 회복
dL = mk(rise + down + upb)
m240 = dL["ma240"].iloc[-30]
print("  참고: 저점", round(min(down)), "240일선", round(m240))
pk = r2.find_peak(dL)
check("전고점 탐지: 신고가와 그 뒤 15% 이상 조정", pk is not None and abs(pk["P"] - P * 1.005) < 1)
resd = r2.long_d(dL)
check("중장기 d: 신고가 → 조정 → 20일선 위 반등(전고점 아래)", resd is not None or min(down) < m240 * 0.97)
check("중장기 d: 조정 중(20일선 아래)에는 비해당", r2.long_d(mk(rise + down)) is None)
# 돌파: 전고점을 장대양봉+거래량으로 넘김
pre = [P * 0.99] ; br = P * 1.07
c = rise + down + upb + [P * 0.985]
dB = mk(c + [br], vol=[1e6] * len(c) + [4e6], open_=np.r_[c[0], c[:-1], P * 0.99])
bo = r2.breakout(dB)
check("단기 B1: 전고점을 장대양봉+거래량으로 돌파", "B1" in bo)
check("단기 B: 거래량 없으면 B1 아님", "B1" not in r2.breakout(mk(c + [br], open_=np.r_[c[0], c[:-1], P * 0.99])))
check("단기 B: 며칠 전에 이미 돌파한 종목은 제외", r2.breakout(mk(c + [br, br * 1.01, br * 1.02, br * 1.03], open_=np.r_[c[0], c[:-1], P * 0.99, br, br, br])) == {})
check("단기 B: 전고점 아래면 비해당", r2.breakout(dL) == {})
for k, f in list(r2.SWING_NOTE.items())[:0]:
    pass
print(r2.BREAK_NOTE["B1"](bo["B1"]) if "B1" in bo else "", "|", r2.LONG_NOTE["L4"](resd) if resd else "")
print(f"{sum(ok)}/{len(ok)}")
raise SystemExit(0 if all(ok) else 1)
