"""스윙(4장 1번 화면) · 중장기 새 규칙 · 단기 유형 B(전고점 돌파) 판정 (순수 계산, 인터넷 불필요).

입력: rules.add_indicators() 를 거친 일봉 DataFrame (오래된 것부터, 마지막 줄 = 기준일).
말로 주신 규칙에서 숫자가 정해지지 않은 부분은 아래 기본값으로 제가 정했습니다. 바꾸려면 이 파일 위쪽 숫자만 고치세요.
"""
import numpy as np
import pandas as pd

# ── 공통 ─────────────────────────────────────────────────────────
LIMIT_UP_PCT = 29.0        # 종가가 전일 대비 +29% 이상이면 상한가로 봄 (국내만 해당)
SURGE_PCT = 0.30           # '급등' = 20거래일 안에 저점 대비 +30% 이상
SURGE_WINDOW = 20
SURGE_SEARCH = 60          # 그 급등은 최근 60거래일 안에 있어야 함
MIN_DRAWDOWN = 0.10        # '조정' = 고점 종가 대비 10% 이상 하락한 적이 있음

# ── 스윙 A·B: 상한가 → 조정 → 20일선(A) / 60일선(B) 반등 ──────────────
LU_LOOKBACK = {20: 40, 60: 120}   # 상한가를 찾는 범위(거래일): 20일선은 40일, 60일선은 120일
LU_MIN_DAYS_AFTER_PEAK = 3        # 고점 이후 최소 3거래일은 지나야 조정으로 봄
REBOUND_TOUCH_DAYS = 5            # 최근 5거래일 안에 저가가 이평선 +2% 이내까지 내려왔고
REBOUND_TOUCH_TOL = 0.02
REBOUND_BREAK_TOL = 0.03          # 그동안 종가가 이평선 아래로 3% 넘게 이탈하지 않았고, 오늘 종가는 이평선 위 + 전일보다 상승

# ── 스윙 C: 급등 후 10일 이상 조정 + 10일선 부근 지지 ────────────────
C_MIN_DAYS = 10
C_NEAR = 0.03                     # 종가가 10일선 ±3% 이내
# ── 스윙 D: 급등 후 거래량 감소 + 20일선 지지 ────────────────────────
D_MIN_DAYS = 5
D_VOL_RATIO = 0.5                 # 최근 5일 평균 거래량이 급등 막바지 5일 평균의 50% 이하
D_TOUCH_TOL = 0.03
# ── 스윙 E(가격 부분): 10일선을 이탈하지 않고 상승 ───────────────────
E_HOLD_DAYS = 10                  # 최근 10거래일 종가가 모두 10일선의 -1% 이상
E_MIN_GAIN = 0.03                 # 10거래일 전보다 3% 이상 상승
E_FLOW_DAYS = 5                   # 수급: 최근 5거래일 중
E_FLOW_POS = 4                    # 4일 이상 외국인+기관 합계 순매수이고
E_FLOW_MIN = 1e9                  # 그 5일 누적 순매수가 10억 원 이상

# ── 중장기 d · 단기 B 공통: 신고가(전고점) ───────────────────────────
PEAK_WINDOW = 250                 # 52주(약 250거래일) 안의 최고가를 전고점으로 봄
PEAK_MIN_AGE = 20                 # 전고점은 최소 20거래일 전
PEAK_DRAWDOWN = 0.15              # 전고점 이후 15% 이상 하락한 적이 있어야 '찍고 하락'
LONG_MA_TOUCH = 0.05              # 조정 중 저가가 240/480일선 +5% 이내까지 내려왔고
LONG_MA_BREAK = 0.03              # 종가는 그 선 아래로 3% 넘게 이탈하지 않았으면 '지지'
D_REBOUND = 0.08                  # 중장기 d: 저점 대비 8% 이상 반등
D_MAX_BELOW_PEAK = 0.25           # 중장기 d: 전고점 대비 -25% 이내까지 올라온 상태
B_BREAK_DAYS = 2                  # 단기 B: 최근 2거래일 안에 처음으로 전고점을 종가로 넘김
B1_BODY_PCT = 5.0                 # 단기 B1: 돌파일 몸통 +5% 이상
B1_BODY_RATIO = 0.6               # 몸통이 그날 고저폭의 60% 이상
B1_VOL_MULT = 2.0                 # 거래량이 직전 20일 평균의 2배 이상


def _d(ts):
    return pd.Timestamp(ts).strftime("%m/%d")


def touched(df, col, days, touch_tol, break_tol):
    """최근 days 일 안에 저가가 이평선 근처까지 내려왔고, 그동안 종가가 선을 크게 이탈하지 않음."""
    rec = df.iloc[-days:]
    m = rec[col]
    if m.isna().any():
        return False
    return bool((rec["low"] <= m * (1 + touch_tol)).any() and (rec["close"] >= m * (1 - break_tol)).all())


def rising(df, col, days=5):
    if len(df) <= days:
        return False
    a, b = df[col].iloc[-1], df[col].iloc[-1 - days]
    return bool(pd.notna(a) and pd.notna(b) and a > b)


def find_surge(df, search=SURGE_SEARCH):
    """최근 search 일 안의 급등과 그 뒤 고점. {gain, peak, peak_pos(끝에서 며칠 전), drawdown} 또는 None."""
    if len(df) < search + SURGE_WINDOW + 1:
        return None
    close = df["close"]
    low_prior = close.rolling(SURGE_WINDOW).min().shift(1)
    gain = (close / low_prior - 1).iloc[-search:]
    if gain.isna().all():
        return None
    best = int(np.nanargmax(gain.values))
    g = float(gain.values[best])
    if g < SURGE_PCT:
        return None
    after = close.iloc[-search:].iloc[best:]
    peak = float(after.max())
    ppos = best + int(np.argmax(after.values))
    return {"gain": g, "peak": peak, "days": search - 1 - ppos, "abs_pos": len(df) - search + ppos,
            "drawdown": 1 - float(close.iloc[-1]) / peak}


# ───────────────────────── 스윙 ─────────────────────────
def swing_limit_up(df, n):
    """A(n=20)·B(n=60): 상한가 → 조정 → n일선 반등."""
    col, look = f"ma{n}", LU_LOOKBACK[n]
    if len(df) < max(look, n) + 10 or pd.isna(df[col].iloc[-1]):
        return None
    close = df["close"]
    pct = close.pct_change() * 100
    win = pct.iloc[-look:-LU_MIN_DAYS_AFTER_PEAK]
    hits = np.where(win.values >= LIMIT_UP_PCT)[0]
    if not len(hits):
        return None
    lu = len(df) - look + int(hits[-1])              # 가장 최근 상한가 위치
    seg = close.iloc[lu:]
    peak = float(seg.max())
    ppos = lu + int(np.argmax(seg.values))
    if len(df) - 1 - ppos < LU_MIN_DAYS_AFTER_PEAK:
        return None
    trough = float(close.iloc[ppos:].min())
    if 1 - trough / peak < MIN_DRAWDOWN or close.iloc[-1] >= peak:
        return None
    if not touched(df, col, REBOUND_TOUCH_DAYS, REBOUND_TOUCH_TOL, REBOUND_BREAK_TOL):
        return None
    last, prev = df.iloc[-1], df.iloc[-2]
    if not (last["close"] >= last[col] and last["close"] > prev["close"]):
        return None
    return {"lu_date": _d(df.index[lu]), "days": len(df) - 1 - lu, "dd": round((1 - trough / peak) * 100, 1),
            "gap": round((float(last["close"]) / float(last[col]) - 1) * 100, 1), "n": n}


def swing_c(df):
    s = find_surge(df)
    if not s or s["days"] < C_MIN_DAYS or s["drawdown"] < 0.05:
        return None
    last = df.iloc[-1]
    if pd.isna(last["ma10"]) or abs(last["close"] / last["ma10"] - 1) > C_NEAR or last["close"] < last["ma10"] * 0.99:
        return None
    if not touched(df, "ma10", 3, 0.02, 0.02):
        return None
    return {"gain": round(s["gain"] * 100, 1), "days": s["days"], "dd": round(s["drawdown"] * 100, 1),
            "gap": round((float(last["close"]) / float(last["ma10"]) - 1) * 100, 1)}


def swing_d(df):
    s = find_surge(df)
    if not s or s["days"] < D_MIN_DAYS or s["drawdown"] < 0.05:
        return None
    last = df.iloc[-1]
    if pd.isna(last["ma20"]) or last["close"] < last["ma20"] * 0.99 or not rising(df, "ma20"):
        return None
    if not touched(df, "ma20", 3, D_TOUCH_TOL, 0.01):
        return None
    v = df["volume"]
    surge_vol = float(v.iloc[max(0, s["abs_pos"] - 4): s["abs_pos"] + 1].mean())
    recent = float(v.iloc[-5:].mean())
    if surge_vol <= 0 or recent > surge_vol * D_VOL_RATIO:
        return None
    return {"gain": round(s["gain"] * 100, 1), "days": s["days"], "vol": round(recent / surge_vol * 100),
            "gap": round((float(last["close"]) / float(last["ma20"]) - 1) * 100, 1)}


def swing_e_price(df):
    """E 의 가격 조건(수급은 별도 확인): 10일선을 이탈하지 않고 상승 중."""
    if len(df) < 40:
        return None
    rec = df.iloc[-E_HOLD_DAYS:]
    if rec["ma10"].isna().any() or not (rec["close"] >= rec["ma10"] * 0.99).all():
        return None
    last = df.iloc[-1]
    if not rising(df, "ma10") or pd.isna(last["ma20"]) or last["ma10"] <= last["ma20"]:
        return None
    gain = float(last["close"]) / float(df["close"].iloc[-1 - E_HOLD_DAYS]) - 1
    if gain < E_MIN_GAIN:
        return None
    return {"gain": round(gain * 100, 1), "gap": round((float(last["close"]) / float(last["ma10"]) - 1) * 100, 1)}


def flow_ok(rows):
    """rows: 최근 날짜부터 [{"date","f","o"}] (순매수 대금, 원). 지속 유입이면 설명 dict."""
    rows = rows[:E_FLOW_DAYS]
    if len(rows) < E_FLOW_DAYS:
        return None
    tot = [r["f"] + r["o"] for r in rows]
    pos = sum(1 for x in tot if x > 0)
    if pos < E_FLOW_POS or sum(tot) < E_FLOW_MIN:
        return None
    return {"pos": pos, "sum": sum(tot), "f": sum(r["f"] for r in rows), "o": sum(r["o"] for r in rows), "asof": rows[0]["date"]}


# ───────────────────────── 전고점(신고가) 공통 ─────────────────────────
def find_peak(df):
    """52주 안의 전고점(고가 기준)과 그 뒤 조정. 전고점이 그 시점의 52주 신고가였는지도 확인."""
    n = len(df)
    if n < PEAK_WINDOW + 40:
        return None
    hi = df["high"]
    win = hi.iloc[-PEAK_WINDOW:-PEAK_MIN_AGE]
    P = float(win.max())
    pos = n - PEAK_WINDOW + int(np.argmax(win.values))
    before = hi.iloc[max(0, pos - PEAK_WINDOW):pos]
    if len(before) >= 60 and float(before.max()) >= P:      # 그 전 1년에 더 높은 가격이 있었으면 신고가가 아님
        return None
    after = df.iloc[pos + 1:]
    if len(after) < PEAK_MIN_AGE:
        return None
    tpos_rel = int(np.argmin(after["low"].values))
    T = float(after["low"].iloc[tpos_rel])
    if 1 - T / P < PEAK_DRAWDOWN:
        return None
    all_time = bool(P >= float(hi.iloc[:pos].max())) if pos > 0 else True
    return {"P": P, "pos": pos, "T": T, "tpos": pos + 1 + tpos_rel, "all_time": all_time}


def long_ma_support(seg, cols=("ma240", "ma480")):
    """조정 구간(seg)에서 240/480일선 지지를 받았는지. 받은 선 이름 목록."""
    out = []
    for col in cols:
        m = seg[col]
        if m.isna().all():
            continue
        ok = m.notna()
        s = seg[ok]
        if len(s) < 5:
            continue
        if (s["low"] <= s[col] * (1 + LONG_MA_TOUCH)).any() and (s["close"] >= s[col] * (1 - LONG_MA_BREAK)).all():
            out.append(col[2:] + "일선")
    return out


def long_d(df):
    """중장기 d: 신고가 → 240일선 지지 조정 → 추세 전환 → 전고점 향해 상승 (20일선 미이탈)."""
    pk = find_peak(df)
    if not pk:
        return None
    n = len(df)
    last = df.iloc[-1]
    if n - 1 - pk["tpos"] < 5 or pd.isna(last["ma20"]) or pd.isna(last["ma240"]):
        return None
    seg = df.iloc[pk["pos"] + 1:]
    if "240일선" not in long_ma_support(seg, ("ma240",)):
        return None
    c = float(last["close"])
    if c >= pk["P"] or c < pk["P"] * (1 - D_MAX_BELOW_PEAK) or c < pk["T"] * (1 + D_REBOUND):
        return None
    rec = df.iloc[-5:]
    if not (rec["close"] >= rec["ma20"] * 0.99).all() or not rising(df, "ma20") or c < float(last["ma240"]):
        return None
    return {"peak_date": _d(df.index[pk["pos"]]), "kind": "역사적 신고가" if pk["all_time"] else "52주 신고가",
            "dd": round((1 - pk["T"] / pk["P"]) * 100, 1), "to_peak": round((c / pk["P"] - 1) * 100, 1)}


def breakout(df):
    """단기 유형 B: 신고가 후 하락했던 전고점을 다시 돌파. {"B1": {...}, "B2": {...}} (해당하는 것만)."""
    pk = find_peak(df)
    if not pk:
        return {}
    n = len(df)
    close = df["close"]
    P = pk["P"]
    if float(close.iloc[-1]) <= P:
        return {}
    since = close.iloc[pk["pos"] + 1:]
    above = np.where(since.values > P)[0]
    first = pk["pos"] + 1 + int(above[0])
    if n - 1 - first >= B_BREAK_DAYS:            # 이미 며칠 전에 넘긴 종목은 제외
        return {}
    if pk["tpos"] >= first:
        return {}
    out = {}
    b = df.iloc[first]
    kind = "역사적 신고가" if pk["all_time"] else "52주 신고가"
    common = {"peak_date": _d(df.index[pk["pos"]]), "kind": kind, "dd": round((1 - pk["T"] / P) * 100, 1),
              "when": "오늘" if first == n - 1 else f"{n - 1 - first}일 전", "over": round((float(close.iloc[-1]) / P - 1) * 100, 1)}
    rng = float(b["high"] - b["low"])
    body = float(b["close"] - b["open"])
    avg = b["vol_avg20"]
    if (b["open"] > 0 and body / float(b["open"]) * 100 >= B1_BODY_PCT and rng > 0 and body / rng >= B1_BODY_RATIO
            and pd.notna(avg) and avg > 0 and float(b["volume"]) / float(avg) >= B1_VOL_MULT):
        out["B1"] = dict(common, body=round(body / float(b["open"]) * 100, 1), vol=round(float(b["volume"]) / float(avg), 1))
    sup = long_ma_support(df.iloc[pk["pos"] + 1:first])
    if sup:
        out["B2"] = dict(common, sup="·".join(sup))
    return out


def evaluate_swing(df, market="kr"):
    out = {}
    if market == "kr":
        for key, n in (("S1", 20), ("S2", 60)):
            r = swing_limit_up(df, n)
            if r:
                out[key] = r
    r = swing_c(df)
    if r:
        out["S3"] = r
    r = swing_d(df)
    if r:
        out["S4"] = r
    return out


SWING_NOTE = {
    "S1": lambda d: f"{d['lu_date']} 상한가({d['days']}일 전) 후 -{d['dd']}% 조정, 20일선 대비 {d['gap']:+}%에서 반등",
    "S2": lambda d: f"{d['lu_date']} 상한가({d['days']}일 전) 후 -{d['dd']}% 조정, 60일선 대비 {d['gap']:+}%에서 반등",
    "S3": lambda d: f"급등 +{d['gain']}% 후 {d['days']}일째 조정(-{d['dd']}%), 10일선 대비 {d['gap']:+}%",
    "S4": lambda d: f"급등 +{d['gain']}% 후 거래량이 급등 때의 {d['vol']}%로 감소, 20일선 대비 {d['gap']:+}%",
    "S5": lambda d: (f"10일선 위에서 10일간 +{d['gain']}% · 최근 5일 중 {d['pos']}일 외국인+기관 순매수, "
                     f"누적 {d['sum'] / 1e8:+,.0f}억(외국인 {d['f'] / 1e8:+,.0f}억 · 기관 {d['o'] / 1e8:+,.0f}억, {d['asof']}까지)"),
}
LONG_NOTE = {
    "L3": lambda d: (f"240일선 돌파({'오늘' if d['a']['days_ago'] == 0 else str(d['a']['days_ago']) + '일 전'}, 거래량 {d['a']['vol_ratio']}배) · "
                     f"480일선 돌파({'오늘' if d['b']['days_ago'] == 0 else str(d['b']['days_ago']) + '일 전'}, 거래량 {d['b']['vol_ratio']}배)"),
    "L4": lambda d: f"{d['peak_date']} {d['kind']} 후 -{d['dd']}% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 {d['to_peak']}%)",
}
BREAK_NOTE = {
    "B1": lambda d: f"{d['peak_date']} {d['kind']}(이후 -{d['dd']}% 조정)를 {d['when']} 돌파 · 장대양봉 +{d['body']}%, 거래량 {d['vol']}배 · 전고점 대비 {d['over']:+}%",
    "B2": lambda d: f"{d['peak_date']} {d['kind']}(이후 -{d['dd']}% 조정)를 {d['when']} 돌파 · 조정 중 {d['sup']} 지지 · 전고점 대비 {d['over']:+}%",
}
