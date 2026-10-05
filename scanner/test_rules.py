"""합성 차트로 규칙 판정을 검증합니다. 실행: python test_rules.py"""
import numpy as np
import pandas as pd

from config import P
from rules import add_indicators, evaluate, rule_breakout, rule_pullback_to_ma60, rule_trend_support

rng = np.random.default_rng(7)


def make_df(close, vol=None):
    close = np.asarray(close, dtype=float)
    n = len(close)
    vol = np.full(n, 1e6) if vol is None else np.asarray(vol, dtype=float)
    idx = pd.bdate_range(end="2026-10-02", periods=n)
    return pd.DataFrame({"open": close, "high": close * 1.01, "low": close * 0.99,
                         "close": close, "volume": vol}, index=idx)


def noisy(x, s=0.004):
    return x * (1 + rng.normal(0, s, len(x)))


results = []


def check(name, cond):
    results.append(cond)
    print(("PASS " if cond else "FAIL ") + name)


# ── 규칙 1 ──────────────────────────────────────────────
t = np.arange(700)
up = noisy(100 * np.exp(0.0025 * t))
df = add_indicators(make_df(up))
# 최근에 20일선까지 눌렸다가 지지받은 상황을 만든다 (저가를 20일선 근처로)
df.iloc[-5, df.columns.get_loc("low")] = df["ma20"].iloc[-5] * 1.005
check("R1 정배열 상승 + 20일선 터치 → 해당", rule_trend_support(df) is not None)

df_no_touch = add_indicators(make_df(100 * np.exp(0.0025 * t)))  # 노이즈 없는 매끈한 상승: 이평선까지 안 내려옴
check("R1 이평선까지 안 내려온 급한 상승 → 비해당(지지 확인 없음)", rule_trend_support(df_no_touch) is None)

down = noisy(300 * np.exp(-0.0015 * t))
check("R1 하락 추세 → 비해당", rule_trend_support(add_indicators(make_df(down))) is None)

# ── 규칙 2 ──────────────────────────────────────────────
base = list(noisy(100 * np.exp(0.0012 * np.arange(300))))  # 완만한 상승으로 60일선 우상향
surge = [base[-1] * (1.03 ** k) for k in range(1, 13)]      # 12일 동안 약 +42%
peak = surge[-1]
series = base + surge
# 고점 후 하루 -1.5% 씩 빠지며 60일선에 닿을 때까지 시뮬레이션
hit_day = None
for k in range(1, 60):
    series.append(peak * (0.985 ** k))
    d = add_indicators(make_df(series))
    if rule_pullback_to_ma60(d) is not None:
        hit_day = k
        break
check("R2 급등 후 조정이 60일선에 닿으면 어느 시점에 해당", hit_day is not None)
check("R2 고점 직후(조정 전)에는 비해당", rule_pullback_to_ma60(add_indicators(make_df(base + surge + [peak * 0.999]))) is None)
if hit_day:
    print(f"     (고점 후 {hit_day}거래일째에 해당)")

flat = noisy(np.full(400, 100.0), 0.01)
check("R2 급등 없는 횡보 → 비해당", rule_pullback_to_ma60(add_indicators(make_df(flat))) is None)

# ── 규칙 3 ──────────────────────────────────────────────
def breakout_series(n_ma, vol_boost):
    # 오래 하락하다가 반등해서 n_ma 일선을 처음 넘는 날 거래량을 vol_boost 배로
    down_len = 700
    s = list(noisy(300 * np.exp(-0.0012 * np.arange(down_len)), 0.003))
    v = [1e6] * down_len
    while True:
        s.append(s[-1] * 1.015)
        v.append(1e6)
        d = add_indicators(make_df(s, v))
        last = d.iloc[-1]
        if last["close"] > last[f"ma{n_ma}"]:
            v[-1] = 1e6 * vol_boost
            return make_df(s, v)
        if len(s) > down_len + 400:
            return None


df240 = breakout_series(240, 3.0)
d = add_indicators(df240)
check("R3 240일선 돌파 + 거래량 3배 → 해당", rule_breakout(d, 240) is not None)
df240_low = breakout_series(240, 1.0)
check("R3 240일선 돌파 + 거래량 증가 없음 → 비해당", rule_breakout(add_indicators(df240_low), 240) is None)

df480 = breakout_series(480, 3.0)
check("R3 480일선 돌파 + 거래량 3배 → 해당", df480 is not None and rule_breakout(add_indicators(df480), 480) is not None)

# 이미 한참 위에 있는 종목은 돌파가 아님
long_up = add_indicators(make_df(noisy(100 * np.exp(0.0025 * t))))
check("R3 이미 선 위에서 계속 상승 중 → 비해당", rule_breakout(long_up, 240) is None)

# 선 근처를 왔다갔다(휩쏘)하는 경우 제외
wob = np.concatenate([np.full(600, 100.0), 100 + 2 * np.sin(np.arange(100) / 2)])
wob = noisy(wob, 0.002)
check("R3 선 근처 왔다갔다 → 비해당", rule_breakout(add_indicators(make_df(wob, np.full(700, 5e6))), 240) is None)

# ── evaluate 통합, 데이터 부족 ───────────────────────────
check("짧은 데이터(100일) → 에러 없이 빈 결과", evaluate(make_df(noisy(np.full(100, 50.0)))) == {})
check("evaluate 통합 호출 동작", isinstance(evaluate(df), dict))

print(f"\n{sum(results)}/{len(results)} 통과")
raise SystemExit(0 if all(results) else 1)
