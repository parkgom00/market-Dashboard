"""5장 유형 A '종가배팅주' 판정 (순수 계산, 인터넷 불필요).

전날까지의 일봉에서 미리 뽑아 둔 기준값(base_features)과 장 마감 직전의 현재 시세를 합쳐서
오늘 종가 기준 이동평균 등을 계산하고, 3개 세부 유형(A1·A2·A3)을 판정합니다.
"""
from config import CP


def base_features(df):
    """일봉(오래된 것부터, 마지막 봉 = 기준일 종가) → 다음 거래일 판정용 기준값. 데이터가 모자라면 None."""
    n = len(df)
    if n < 30:
        return None
    c, v = df["close"], df["volume"]
    last = df.iloc[-1]
    out = {
        "prevClose": float(last["close"]), "prevOpen": float(last["open"]), "prevVolume": int(last["volume"]),
        "prevPct": float((c.iloc[-1] / c.iloc[-2] - 1) * 100) if c.iloc[-2] else 0.0,
        "s9": float(c.tail(9).sum()), "s19": float(c.tail(19).sum()),
        "avgAmt20": float((c * v).tail(20).mean()),
        "hi250": float(df["high"].tail(250).max()), "lo250": float(df["low"].tail(250).min()),
    }
    if n >= 240:
        out["s239"] = float(c.tail(239).sum())
    if n >= 480:
        out["s479"] = float(c.tail(479).sum())
    return {k: round(x, 2) if isinstance(x, float) else x for k, x in out.items()}


def mas_today(base, price):
    """오늘 현재가를 오늘 종가로 보고 만든 이동평균 {ma10, ma20, ma240, ma480} (재료가 없으면 None)."""
    return {
        "ma10": (base["s9"] + price) / 10 if "s9" in base else None,
        "ma20": (base["s19"] + price) / 20 if "s19" in base else None,
        "ma240": (base["s239"] + price) / 240 if "s239" in base else None,
        "ma480": (base["s479"] + price) / 480 if "s479" in base else None,
    }


def body_ratio(o, h, l, c):
    rng = h - l
    return abs(c - o) / rng if rng > 0 else 0.0


# ───────────── 1차 거름 (네이버 실시간 값만 사용: 가격·거래량·거래대금) ─────────────
def prefilter(q, base):
    """q: {price, volume, value, pct}. 반환: 가능성이 있는 유형 집합 {'A1','A2','A3'} (분봉을 받아 확인할 후보)."""
    out = set()
    if q["price"] < CP.min_price or q["value"] < CP.min_value:
        return out
    if q["pct"] >= CP.a1_min_pct:
        out.add("A1")
    if not base:
        return out
    ma = mas_today(base, q["price"])
    if (base["prevPct"] >= CP.a2_prev_pct and base["prevVolume"] > 0 and q["volume"] <= base["prevVolume"] * CP.a2_vol_ratio
            and ma["ma10"] and ma["ma20"] and q["price"] >= ma["ma10"] and q["price"] >= ma["ma20"]):
        out.add("A2")
    m = CP.a3_cross_margin
    if (q["value"] >= CP.a3_min_value and base["avgAmt20"] > 0 and q["value"] >= base["avgAmt20"] * CP.a3_value_mult
            and q["pct"] >= CP.a3_body_pct and ma["ma240"] and ma["ma480"]
            and q["price"] >= ma["ma240"] * (1 + m) and q["price"] >= ma["ma480"] * (1 + m)):
        out.add("A3")
    return out


# ───────────── 2차 판정 (오늘 분봉으로 만든 시가·고가·저가·종가 사용) ─────────────
def judge_a1(q, bars, flow=None):
    """A1. bars: {open, high, low, close, lateShare}. flow: 외국인+기관 순매수 대금(원) 또는 None."""
    if q["pct"] < CP.a1_min_pct or q["value"] < CP.min_value:
        return None
    if q["price"] < bars["high"] * (1 - CP.a1_high_gap):
        return None
    if bars.get("lateShare") is not None and bars["lateShare"] < CP.a1_late_share:
        return None
    flow_ok = None
    if flow is not None:
        flow_ok = flow >= q["value"] * CP.a1_flow_share
        if not flow_ok:
            return None
    score = (flow / q["value"] if flow is not None else 0) + (bars.get("lateShare") or 0)
    note = f"고가 마감권(고가 대비 {(1 - q['price'] / bars['high']) * 100:.2f}% 아래)"
    if bars.get("lateShare") is not None:
        note += f" · {CP.a1_late_from} 이후 거래량 비중 {bars['lateShare'] * 100:.0f}%"
    note += f" · 외국인+기관 순매수 {flow / 1e8:+.0f}억" if flow is not None else " · 수급 자료 확인 전"
    return {"score": score, "note": note}


def judge_a2(q, bars, base):
    if not base or base["prevPct"] < CP.a2_prev_pct or q["volume"] > base["prevVolume"] * CP.a2_vol_ratio:
        return None
    o, h, l, c = bars["open"], bars["high"], bars["low"], q["price"]
    if o <= 0 or (h - l) / o < CP.a2_min_range or body_ratio(o, h, l, c) > CP.a2_doji_body:
        return None
    ma = mas_today(base, c)
    if not (ma["ma10"] and ma["ma20"]) or c < ma["ma10"] or c < ma["ma20"]:
        return None
    ratio = q["volume"] / base["prevVolume"]
    note = (f"전일 +{base['prevPct']:.1f}% 급등 · 오늘 거래량 전일의 {ratio * 100:.0f}% · 도지(몸통 {body_ratio(o, h, l, c) * 100:.0f}%) · "
            f"10일선 {ma['ma10']:,.0f} / 20일선 {ma['ma20']:,.0f} 위 마감")
    return {"score": base["prevPct"], "note": note}


def judge_a3(q, bars, base):
    if not base or "s239" not in base or "s479" not in base:
        return None
    o, h, l, c = bars["open"], bars["high"], bars["low"], q["price"]
    ma = mas_today(base, c)
    m = CP.a3_cross_margin
    if c < ma["ma240"] * (1 + m) or c < ma["ma480"] * (1 + m):
        return None
    # 오늘 돌파: 전일 종가는 두 선 중 높은 쪽 아래
    if base["prevClose"] >= max(ma["ma240"], ma["ma480"]):
        return None
    rng = base["hi250"] - base["lo250"]
    pos = (base["prevClose"] - base["lo250"]) / rng if rng > 0 else 1.0
    if pos > CP.a3_pos_max:
        return None
    if base["avgAmt20"] <= 0 or q["value"] < max(CP.a3_min_value, base["avgAmt20"] * CP.a3_value_mult):
        return None
    if o <= 0 or (c / o - 1) * 100 < CP.a3_body_pct or body_ratio(o, h, l, c) < CP.a3_body_ratio or c < o:
        return None
    mult = q["value"] / base["avgAmt20"]
    note = (f"바닥권(250일 범위 하단 {pos * 100:.0f}%) · 거래대금 {q['value'] / 1e8:,.0f}억(20일 평균의 {mult:.1f}배) · "
            f"장대양봉(+{(c / o - 1) * 100:.1f}%) · 240일선 {ma['ma240']:,.0f}, 480일선 {ma['ma480']:,.0f} 돌파")
    return {"score": mult, "note": note}


def a1_reason(q, bars, flow=None):
    """A1 탈락 사유(진단용). 통과면 'ok'."""
    if q["pct"] < CP.a1_min_pct or q["value"] < CP.min_value:
        return "등락률·거래대금 미달"
    if q["price"] < bars["high"] * (1 - CP.a1_high_gap):
        return "고가에서 멂"
    if bars.get("lateShare") is not None and bars["lateShare"] < CP.a1_late_share:
        return "막판 거래량 비중 부족"
    if flow is not None and flow < q["value"] * CP.a1_flow_share:
        return "외국인·기관 순매수 부족"
    return "ok(수급 확인)" if flow is not None else "ok(수급 자료 없음)"
