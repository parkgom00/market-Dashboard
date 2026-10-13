"""시장 폭(얼마나 많은 종목이 함께 오르내리는지) 집계. 장마감 스캔에서 종목 일봉을 하나씩 넣는다.

날짜별로: 20일선 위 종목 수, 상승·하락 종목 수, 52주 신고가·신저가 종목 수.
"""
import json
import os

DAYS = 80          # 최근 80거래일 날짜별 집계


class Breadth:
    def __init__(self):
        self.d = {}     # 날짜 → [종목수, 20일선 위, 상승, 하락, 신고가, 신저가]

    def add(self, df):
        n = len(df)
        if n < 25:
            return
        c = df["close"]
        ma20 = c.rolling(20).mean().values
        hi = df["high"].rolling(250, min_periods=120).max().shift(1).values
        lo = df["low"].rolling(250, min_periods=120).min().shift(1).values
        cv, hv, lv = c.values, df["high"].values, df["low"].values
        days = [d.strftime("%Y-%m-%d") for d in df.index[max(20, n - DAYS):]]
        for j, i in enumerate(range(max(20, n - DAYS), n)):
            row = self.d.setdefault(days[j], [0, 0, 0, 0, 0, 0])
            ci, pi = cv[i], cv[i - 1]
            row[0] += 1
            if ci > ma20[i]:
                row[1] += 1
            if ci > pi:
                row[2] += 1
            elif ci < pi:
                row[3] += 1
            if hi[i] == hi[i] and hv[i] > hi[i]:
                row[4] += 1
            if lo[i] == lo[i] and lv[i] < lo[i]:
                row[5] += 1

    def save(self, path):
        rows = sorted(self.d.items())
        if rows:   # 종목 수가 너무 적은 날(자료가 덜 들어온 날)은 뺀다
            top = max(r[0] for _, r in rows)
            rows = [(k, v) for k, v in rows if v[0] >= top * 0.8]
        out = [{"date": k, "n": v[0], "above20": v[1], "up": v[2], "down": v[3], "newHigh": v[4], "newLow": v[5]} for k, v in rows[-DAYS:]]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f)
        return out
