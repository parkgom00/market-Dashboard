"""종가배팅주(5장 A) 판정 로직 검증 (가짜 데이터). 실행: python test_closing.py"""
import datetime as dt
import numpy as np
import pandas as pd

import closing
import collect_closing as cc
import naver_live as nl

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def mk(closes, vols, opens=None):
    idx = pd.bdate_range(end="2026-10-05", periods=len(closes))
    c = np.array(closes, float)
    o = np.array(opens, float) if opens is not None else c
    return pd.DataFrame({"open": o, "high": np.maximum(o, c) * 1.01, "low": np.minimum(o, c) * 0.99, "close": c, "volume": vols}, index=idx)

# A2: 20일 횡보 후 전일 +12%
c = [1000] * 59 + [1120]
df = mk(c, [100000] * 59 + [1000000])
b = closing.base_features(df)
check("base prevPct", abs(b["prevPct"] - 12) < 0.01)
q = {"price": 1115, "volume": 300000, "value": 1115 * 300000 * 1.0, "pct": (1115 / 1120 - 1) * 100}
bars = {"open": 1118, "high": 1135, "low": 1100, "close": 1115, "lateShare": 0.2}
q["value"] = 6e9
r = closing.judge_a2(q, bars, b)
check("A2 통과", r is not None)
check("A2 prefilter", "A2" in closing.prefilter(q, b))
check("A2 거래량 많으면 탈락", closing.judge_a2(dict(q, volume=900000), bars, b) is None)
check("A2 장대 몸통이면 탈락", closing.judge_a2(q, dict(bars, open=1050, high=1120, low=1045), b) is None)
check("A2 20일선 아래 탈락", closing.judge_a2(dict(q, price=900), dict(bars, open=905, high=915, low=890), b) is None)

# A1
q1 = {"price": 10000, "volume": 1e6, "value": 1e10, "pct": 5.0}
b1 = {"open": 9700, "high": 10020, "low": 9650, "close": 10000, "lateShare": 0.25}
check("A1 통과(수급 확인)", closing.judge_a1(q1, b1, 5e8) is not None)
check("A1 수급 부족 탈락", closing.judge_a1(q1, b1, 1e7) is None)
check("A1 고가에서 멀면 탈락", closing.judge_a1(dict(q1, price=9800), b1, 5e8) is None)
check("A1 수급 모름이면 통과+표시", "확인 전" in closing.judge_a1(q1, b1, None)["note"])

# A3: 500일 하락 후 바닥 → 급등
c = list(np.linspace(5000, 1000, 520)) + [1000] * 0
df = mk(c, [100000] * 520)
b3 = closing.base_features(df)
check("base 480", "s479" in b3 and "s239" in b3)
ma = closing.mas_today(b3, 3000)
price = ma["ma240"] * 1.5
price = max(price, ma["ma480"] * 1.5)
q3 = {"price": price, "volume": 5e6, "value": price * 5e6, "pct": (price / b3["prevClose"] - 1) * 100}
bars3 = {"open": b3["prevClose"] * 1.01, "high": price * 1.005, "low": b3["prevClose"], "close": price, "lateShare": 0.1}
r3 = closing.judge_a3(q3, bars3, b3)
check("A3 통과 또는 바닥 조건 확인", r3 is not None)
check("A3 prefilter 키", isinstance(closing.prefilter(q3, b3), set))

# 네이버 파싱
check("parse 보통주", nl.parse_row({"itemCode": "005930", "stockName": "삼성전자", "closePrice": "70,000", "accumulatedTradingVolume": "1,000", "fluctuationsRatio": "1.5"})["price"] == 70000)
check("parse 우선주 제외", nl.parse_row({"itemCode": "005935", "stockName": "삼성전자우", "closePrice": "1", "accumulatedTradingVolume": "1"}) is None)
check("parse 스팩 제외", nl.parse_row({"itemCode": "123450", "stockName": "한국제1호스팩", "closePrice": "1", "accumulatedTradingVolume": "1"}) is None)
pf = nl.parse_flow([{"bizdate": "20261005", "foreignerPureBuyQuant": "-5", "organPureBuyQuant": "1"}, {"bizdate": "20261006", "foreignerPureBuyQuant": "+1,000", "organPureBuyQuant": "500"}], 100, "20261006")
check("parse_flow", pf == 150000)
check("parse_flow 오늘 아님", nl.parse_flow([{"bizdate": "20261005", "foreignerPureBuyQuant": "1"}], 100, "20261006") is None)

# run 통합
now = dt.datetime(2026, 10, 6, 15, 30, tzinfo=cc.KST)
uni = {"111110": {"name": "후보", "price": 1115, "volume": 300000, "market": "KOSPI"},
       "222220": {"name": "무관", "price": 500, "volume": 10, "market": "KOSDAQ"}}
base = {"111110": b, "222220": dict(b, prevClose=500)}
def fb(code, mk_):
    return dict(bars, lastTs=now.timestamp() - 60)
# value = 1115*300000 = 3.3e8 < 5e9 → 전체 탈락 확인 후 큰 거래량으로
res, d = cc.run(uni, base, now, fetch_bars=fb)
check("거래대금 작으면 후보 없음", d["candidates"] == 0)
uni["111110"]["volume"] = 6_000_000
base["111110"]["prevVolume"] = 20_000_000
res, d = cc.run(uni, base, now, fetch_bars=fb)
check("run A2 결과", len(res["A2"]) == 1 and res["A2"][0]["name"] == "후보")
p = cc.to_payload(res, "x", "ok")
check("payload 구조", p["types"][0]["subtypes"][1]["id"] == "A2" and len(p["types"][0]["subtypes"]) == 3)
check("전체 통과", all(ok))
print(f"{sum(ok)}/{len(ok)}")
raise SystemExit(0 if all(ok) else 1)
