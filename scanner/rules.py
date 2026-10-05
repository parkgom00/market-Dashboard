"""4장 중장기 규칙 판정 (순수 계산 함수).

입력: 날짜 오름차순 DataFrame, 컬럼 open/high/low/close/volume
출력: 규칙에 해당하면 설명용 dict, 아니면 None
"""
import numpy as np
import pandas as pd

from config import MA_LIST, P, Params


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for n in MA_LIST:
        df[f"ma{n}"] = df["close"].rolling(n).mean()
    # 돌파일 거래량 비교용: 당일을 뺀 직전 20일 평균
    df["vol_avg20"] = df["volume"].rolling(20).mean().shift(1)
    return df


# ───────────────────────── 규칙 1 ─────────────────────────
def rule_trend_support(df: pd.DataFrame, p: Params = P):
    """5>10>20>60>120>240>480일선 정배열 + 20/60일선 상승 + 최근 20/60일선 지지 확인."""
    if len(df) < 480 + p.slope_days:
        return None
    last = df.iloc[-1]
    mas = [last[f"ma{n}"] for n in MA_LIST]
    if any(pd.isna(mas)):
        return None
    if not all(mas[i] > mas[i + 1] for i in range(len(mas) - 1)):
        return None

    prev = df.iloc[-1 - p.slope_days]
    if not (last["ma20"] > prev["ma20"] and last["ma60"] > prev["ma60"]):
        return None
    if last["close"] < last["ma60"]:
        return None

    recent = df.iloc[-p.support_lookback:]
    touched = []
    for n in (20, 60):
        m = recent[f"ma{n}"]
        near = (recent["low"] <= m * (1 + p.touch_tol)) & (recent["close"] >= m * (1 - p.break_tol))
        if near.any():
            touched.append(f"{n}일선")
    if not touched:
        return None
    return {"support": "·".join(touched)}


# ───────────────────────── 규칙 2 ─────────────────────────
def rule_pullback_to_ma60(df: pd.DataFrame, p: Params = P):
    """급등 후 조정을 받아 60일선에서 지지받는 모양."""
    need = p.search_days + p.surge_window + 1
    if len(df) < max(need, 60 + p.ma60_slope_days + 1):
        return None
    last = df.iloc[-1]
    if pd.isna(last["ma60"]):
        return None

    close = df["close"]
    low_prior = close.rolling(p.surge_window).min().shift(1)  # 직전 20일 최저 종가
    gain = (close / low_prior - 1).iloc[-p.search_days:]
    if gain.isna().all():
        return None
    best_pos = int(np.argmax(gain.values))
    best_gain = float(gain.values[best_pos])
    if best_gain < p.surge_pct:
        return None

    after = close.iloc[-p.search_days:].iloc[best_pos:]
    peak_price = float(after.max())
    peak_pos = best_pos + int(np.argmax(after.values))
    days_since_peak = p.search_days - 1 - peak_pos
    drawdown = 1 - float(last["close"]) / peak_price
    if days_since_peak < p.min_days_since_peak or drawdown < p.min_drawdown:
        return None

    prev = df.iloc[-1 - p.ma60_slope_days]
    if not last["ma60"] > prev["ma60"]:
        return None

    rec = df.iloc[-p.ma60_touch_days:]
    near = (rec["low"] <= rec["ma60"] * (1 + p.ma60_touch_tol)) & (rec["close"] >= rec["ma60"] * (1 - p.ma60_break_tol))
    if not near.any():
        return None
    return {
        "surge_pct": round(best_gain * 100, 1),
        "drawdown_pct": round(drawdown * 100, 1),
        "gap_ma60_pct": round((float(last["close"]) / float(last["ma60"]) - 1) * 100, 1),
    }


# ───────────────────────── 규칙 3 ─────────────────────────
def rule_breakout(df: pd.DataFrame, n: int, p: Params = P):
    """거래량을 동반해 n일선(240 또는 480)을 아래→위로 돌파."""
    col = f"ma{n}"
    if len(df) < n + p.prior_window + 1:
        return None
    last = df.iloc[-1]
    if pd.isna(last[col]) or last["close"] <= last[col]:
        return None

    total = len(df)
    for k in range(1, p.breakout_days + 1):
        i = total - k
        c, m = df["close"].iloc[i], df[col].iloc[i]
        c0, m0 = df["close"].iloc[i - 1], df[col].iloc[i - 1]
        if pd.isna(m) or pd.isna(m0):
            continue
        if c > m and c0 <= m0:
            # 돌파 전 20일 중 선 아래에 있던 날 수
            seg = df.iloc[i - p.prior_window:i]
            below = int((seg["close"] <= seg[col]).sum())
            if below < p.prior_below_days:
                continue
            avg = df["vol_avg20"].iloc[i]
            if pd.isna(avg) or avg <= 0:
                continue
            ratio = float(df["volume"].iloc[i] / avg)
            if ratio >= p.vol_mult:
                return {"days_ago": k - 1, "vol_ratio": round(ratio, 1)}
    return None


def evaluate(df: pd.DataFrame, p: Params = P) -> dict:
    """한 종목에 대해 모든 규칙을 평가. {규칙ID: 설명dict} (해당하는 것만)."""
    df = add_indicators(df)
    out = {}
    r = rule_trend_support(df, p)
    if r:
        out["L1"] = r
    r = rule_pullback_to_ma60(df, p)
    if r:
        out["L2"] = r
    r = rule_breakout(df, 240, p)
    if r:
        out["L3a"] = r
    r = rule_breakout(df, 480, p)
    if r:
        out["L3b"] = r
    return out


NOTE_FMT = {
    "L1": lambda d: f"정배열 상승 중, 최근 {d['support']} 지지 확인",
    "L2": lambda d: f"급등 +{d['surge_pct']}% 후 고점 대비 -{d['drawdown_pct']}% 조정, 60일선 대비 {d['gap_ma60_pct']:+}%",
    "L3a": lambda d: f"240일선 돌파({'오늘' if d['days_ago'] == 0 else str(d['days_ago']) + '일 전'}), 거래량 평균의 {d['vol_ratio']}배",
    "L3b": lambda d: f"480일선 돌파({'오늘' if d['days_ago'] == 0 else str(d['days_ago']) + '일 전'}), 거래량 평균의 {d['vol_ratio']}배",
}
