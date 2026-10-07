"""규칙별 과거 성과 점검 (국내 전 종목, 일봉).

방법
  · 종목마다 약 6년치 일봉을 받아, 최근 TEST_DAYS 거래일 동안 STEP 일 간격의 날짜를 '신호일'로 본다.
  · 신호일 종가까지의 자료만으로 규칙을 판정하고(미래 자료 사용 없음), 해당하면
    다음 날 시가에 사서 5·10·20거래일 뒤 종가에 판 것으로 수익률을 잰다.
  · 같은 날 거래대금 조건을 통과한 모든 종목의 평균(시장 평균)도 구해, 규칙 수익률에서 뺀 '초과 수익'을 함께 본다.
한계: 지금 상장돼 있는 종목만 대상(상장폐지 종목 제외 → 실제보다 좋게 나올 수 있음), 수수료·세금·슬리피지 미반영,
      스윙 E(외국인·기관 수급)는 과거 수급 자료가 없어 가격 조건만 점검.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import rules
import rules2
from config import P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TEST_DAYS = 500
STEP = 3
HORIZONS = (5, 10, 20)
MIN_VALUE = P.min_value_kr

RULES = ["L1", "L2", "L3", "L4", "S1", "S2", "S3", "S4", "S5p", "B1", "B2"]
LABEL = {"L1": "중장기 a 정배열+이평선 지지", "L2": "중장기 b 급등 후 60일선 지지", "L3": "중장기 c 240·480 동시 돌파",
         "L4": "중장기 d 신고가 후 240일선 지지 반등", "S1": "스윙 A 상한가 후 20일선 반등", "S2": "스윙 B 상한가 후 60일선 반등",
         "S3": "스윙 C 급등 후 10일선 지지", "S4": "스윙 D 급등 후 거래량 감소+20일선", "S5p": "스윙 E 가격조건만(수급 제외)",
         "B1": "단기 B1 전고점 돌파+장대양봉", "B2": "단기 B2 전고점 돌파+장기이평 지지"}


def signals(sub):
    out = []
    try:
        if rules.rule_trend_support(sub):
            out.append("L1")
        if rules.rule_pullback_to_ma60(sub):
            out.append("L2")
        if rules.rule_breakout(sub, 240) and rules.rule_breakout(sub, 480):
            out.append("L3")
        if rules2.long_d(sub):
            out.append("L4")
        if rules2.swing_limit_up(sub, 20):
            out.append("S1")
        if rules2.swing_limit_up(sub, 60):
            out.append("S2")
        if rules2.swing_c(sub):
            out.append("S3")
        if rules2.swing_d(sub):
            out.append("S4")
        if rules2.swing_e_price(sub):
            out.append("S5p")
        out += list(rules2.breakout(sub).keys())
    except Exception:
        pass
    return out


def one_stock(args):
    """한 종목의 (날짜, 규칙목록, 수익률들) 목록과 기준(전체) 수익률."""
    code, df = args
    n = len(df)
    hmax = max(HORIZONS)
    if n < 300:
        return []
    ind = rules.add_indicators(df)
    val20 = (df["close"] * df["volume"]).rolling(20).mean().values
    o, c, hi, lo = df["open"].values, df["close"].values, df["high"].values, df["low"].values
    dates = df.index
    rows = []
    start = max(260, n - TEST_DAYS - hmax)
    # 모든 종목이 같은 달력 날짜를 쓰도록 날짜 번호(서수)를 STEP 으로 나눠 고른다
    for t in range(start, n - hmax - 1):
        if dates[t].toordinal() % STEP:
            continue
        if not (val20[t] >= MIN_VALUE) or o[t + 1] <= 0:
            continue
        entry = o[t + 1]
        rets = [c[t + h] / entry - 1 for h in HORIZONS]
        mfe = hi[t + 1:t + 1 + hmax].max() / entry - 1
        mae = lo[t + 1:t + 1 + hmax].min() / entry - 1
        rows.append((dates[t].strftime("%Y-%m-%d"), signals(ind.iloc[:t + 1]), rets, mfe, mae))
    return rows


def summarize(all_rows):
    base = {}                       # 날짜별 시장 평균
    for d, _, rets, _, _ in all_rows:
        b = base.setdefault(d, [0, [0.0] * len(HORIZONS)])
        b[0] += 1
        for i, r in enumerate(rets):
            b[1][i] += r
    base_mean = {d: [x / b[0] for x in b[1]] for d, b in base.items()}
    res = {}
    for rule in RULES:
        sel = [(d, rets, mfe, mae) for d, sig, rets, mfe, mae in all_rows if rule in sig]
        if not sel:
            res[rule] = {"label": LABEL[rule], "n": 0}
            continue
        r = {"label": LABEL[rule], "n": len(sel), "dates": len({d for d, _, _, _ in sel})}
        for i, h in enumerate(HORIZONS):
            xs = np.array([rets[i] for _, rets, _, _ in sel]) * 100
            ex = np.array([rets[i] - base_mean[d][i] for d, rets, _, _ in sel]) * 100
            r[f"d{h}"] = {"mean": round(float(xs.mean()), 2), "median": round(float(np.median(xs)), 2),
                          "win": round(float((xs > 0).mean() * 100), 1), "excess": round(float(ex.mean()), 2),
                          "beat": round(float((ex > 0).mean() * 100), 1)}
        r["maxGain20"] = round(float(np.mean([m for _, _, m, _ in sel]) * 100), 2)
        r["maxLoss20"] = round(float(np.mean([m for _, _, _, m in sel]) * 100), 2)
        # 앞 절반 / 뒤 절반 기간으로 나눠 20일 초과 수익이 양쪽에서 비슷한지 (우연인지 가늠)
        ds = sorted({d for d, _, _, _ in sel})
        mid = ds[len(ds) // 2]
        for name, part in (("firstHalf", [x for x in sel if x[0] < mid]), ("secondHalf", [x for x in sel if x[0] >= mid])):
            r[name] = round(float(np.mean([x[1][-1] - base_mean[x[0]][-1] for x in part]) * 100), 2) if part else None
        res[rule] = r
    allr = np.array([rets for _, _, rets, _, _ in all_rows]) * 100
    market = {f"d{h}": {"mean": round(float(allr[:, i].mean()), 2), "median": round(float(np.median(allr[:, i])), 2),
                        "win": round(float((allr[:, i] > 0).mean() * 100), 1)} for i, h in enumerate(HORIZONS)}
    ds = sorted(base)
    return {"period": [ds[0], ds[-1]] if ds else [], "signalDates": len(ds), "samples": len(all_rows), "market": market, "rules": res}


def main(limit=0):
    import fetch
    uni = fetch.kr_universe()
    if limit:
        uni = uni.sample(limit, random_state=1)
    data = [(c, df) for c, df in fetch.kr_prices(uni["code"], years=6.2)]
    print("받은 종목", len(data))
    rows = []
    with ProcessPoolExecutor(4) as ex:
        for r in ex.map(one_stock, data, chunksize=20):
            rows += r
    res = summarize(rows)
    res["stocks"] = len(data)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "backtest.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: (v.get("n"), v.get("d20")) for k, v in res["rules"].items()}, ensure_ascii=False))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
