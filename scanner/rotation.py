"""테마 순환매: 테마별로 최근 며칠 동안 '가격이 오르면서 거래대금이 늘었는지'를 계산합니다 (순수 계산, 인터넷 불필요).

입력
  hist   {종목코드: {"name", "bars": {날짜: (종가, 거래대금)}}}  ← 장마감 스캔이 받은 일봉에서 최근 약 32일치
  themes {테마명: [종목코드, ...]}                              ← 네이버 테마 구성종목
계산
  테마 등락률  = 구성종목 일간 등락률의 단순 평균 (한 종목이 ±30% 를 넘으면 ±30% 로 자름)
  테마 거래대금 = 구성종목 거래대금 합계
  거래대금 배수 = 그날(또는 최근 n일 평균) 거래대금 ÷ 그 직전 20거래일 평균 거래대금
  유입 점수    = 등락률(%) × 거래대금 배수(최대 5배까지 인정)   → 오르면서 돈이 몰린 테마일수록 큼
"""
SHOW_DAYS = 10      # 화면에 보여줄 거래일 수
BASE_DAYS = 20      # 거래대금 배수의 비교 기간
MIN_MEMBERS = 5
MIN_AMOUNT = 3e10   # 테마 하루 거래대금 300억 원 미만은 순위에서 제외
RATIO_CAP = 5.0
CLIP = 30.0


def trading_days(hist, need=SHOW_DAYS + BASE_DAYS + 1):
    """거래가 가장 많은 날짜들(= 실제 거래일) 중 최근 need 일."""
    cnt = {}
    for h in hist.values():
        for d in h["bars"]:
            cnt[d] = cnt.get(d, 0) + 1
    if not cnt:
        return []
    top = max(cnt.values())
    days = sorted(d for d, c in cnt.items() if c >= top * 0.5)
    return days[-need:]


def stock_series(h, days):
    """종목의 날짜별 (등락률 또는 None, 거래대금). 첫 날은 직전 종가가 없어 등락률 None."""
    out, prev = [], None
    for d in days:
        b = h["bars"].get(d)
        if not b:
            out.append((None, 0.0))
            prev = None
            continue
        pct = (b[0] / prev - 1) * 100 if prev else None
        if pct is not None:
            pct = max(-CLIP, min(CLIP, pct))
        out.append((pct, float(b[1])))
        prev = b[0]
    return out


def theme_series(codes, series, n):
    """테마의 날짜별 (평균 등락률, 거래대금 합계)."""
    rets, amts = [], []
    for i in range(n):
        ps = [series[c][i][0] for c in codes if series[c][i][0] is not None]
        rets.append(sum(ps) / len(ps) if ps else 0.0)
        amts.append(sum(series[c][i][1] for c in codes))
    return rets, amts


def score(ret, ratio):
    return ret * min(max(ratio, 0.0), RATIO_CAP)


def build(hist, themes, show=SHOW_DAYS, base=BASE_DAYS):
    days = trading_days(hist, show + base + 1)
    if len(days) < base + 2:
        return None
    n = len(days)
    show = min(show, n - base - 1)
    series = {c: stock_series(h, days) for c, h in hist.items()}
    rows = []
    for name, codes in themes.items():
        codes = [c for c in dict.fromkeys(codes) if c in series]
        if len(codes) < MIN_MEMBERS:
            continue
        rets, amts = theme_series(codes, series, n)
        ratio = []
        for i in range(n):
            b = amts[max(0, i - base):i]
            avg = sum(b) / len(b) if b else 0
            ratio.append(amts[i] / avg if avg > 0 else 0.0)
        per = {}
        for k in (1, 3, 5):
            if n - k - base < 0:
                continue
            r = sum(rets[n - k:])
            cur = sum(amts[n - k:]) / k
            b = amts[n - k - base:n - k]
            avg = sum(b) / len(b) if b else 0
            rt = cur / avg if avg > 0 else 0.0
            per[k] = {"ret": round(r, 2), "ratio": round(rt, 2), "score": round(score(r, rt), 2), "amt": round(cur / 1e8)}
        last = n - 1
        leaders = sorted(codes, key=lambda c: -series[c][last][1])[:5]
        rows.append({"name": name, "members": len(codes), "rets": rets, "amts": amts, "ratio": ratio, "per": per,
                     "stocks": [{"code": c, "name": hist[c]["name"], "pct": round(series[c][last][0] or 0, 2),
                                 "amt": round(series[c][last][1] / 1e8)} for c in leaders]})
    if not rows:
        return None
    sd = list(range(n - show, n))                      # 화면에 보여줄 날짜 위치

    def day_top(i, k=3):
        ok = [r for r in rows if r["amts"][i] >= MIN_AMOUNT and r["rets"][i] >= 1.0]      # 평균 +1% 이상 오른 테마만
        ok.sort(key=lambda r: -score(r["rets"][i], r["ratio"][i]))
        return ok[:k]

    daily, picked = [], []
    for i in reversed(sd):
        top = day_top(i)
        daily.append({"date": days[i], "top": [{"name": r["name"], "ret": round(r["rets"][i], 2), "ratio": round(r["ratio"][i], 2),
                                                  "amt": round(r["amts"][i] / 1e8)} for r in top]})
        picked += [r["name"] for r in top]

    def rank(k, sign):
        ok = [r for r in rows if k in r["per"] and r["per"][k]["amt"] * 1e8 >= MIN_AMOUNT and r["per"][k]["ret"] * sign > 0
              and (sign < 0 or r["per"][k]["ratio"] >= 1.1)]      # '들어온' 쪽은 거래대금이 평소보다 10% 이상 늘어난 테마만
        ok.sort(key=lambda r: -sign * r["per"][k]["score"])
        return [dict(name=r["name"], members=r["members"], stocks=r["stocks"], **r["per"][k]) for r in ok[:10]]

    order = list(dict.fromkeys(picked))[:14]           # 히트맵에 올릴 테마: 최근 날짜에 1~3위였던 테마부터
    by = {r["name"]: r for r in rows}
    heat = [{"name": nm, "rets": [round(by[nm]["rets"][i], 2) for i in sd],
             "top": [1 if nm in [t["name"] for t in d["top"]] else 0 for d in reversed(daily)]} for nm in order]
    return {"days": [days[i] for i in sd], "daily": daily, "heat": heat,
            "inflow": {str(k): rank(k, 1) for k in (1, 3, 5)}, "outflow": {str(k): rank(k, -1)[:5] for k in (1, 3, 5)},
            "themeCount": len(rows)}
