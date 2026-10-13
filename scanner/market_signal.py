"""시장 신호등 (캘린더 탭 '🚦 시장 신호등' 화면) → data/signal.js

하락 경계 신호 9개와 재진입 신호 6개를 매일 계산해 🟢 공격 / 🟡 조심 / 🔴 쉬기 로 묶는다.
- 지수(코스피·코스닥) 일봉: FinanceDataReader
- 시장 폭: 장마감 스캔이 만든 out/breadth_kr.json
- VIX·원/달러·필라델피아 반도체·EWY: yfinance
- 외국인·기관 순매수(코스피 시장 전체): 한국투자 API (--flows 일 때만 받고, 아니면 지난번 값 사용)
판단 기준은 아래 상수로 모아 두었다. 예측이 아니라 '지금 시장이 어떤 상태인지'를 보여주는 도구다.
"""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_JS = os.path.join(HERE, "..", "data", "signal.js")
KST = dt.timezone(dt.timedelta(hours=9))

DIST_DROP = -0.2        # 분산일: 지수 -0.2% 이하 하락 + 거래량 전일보다 증가
DIST_WIN = 25           # 최근 25거래일 안에서 센다
DIST_YELLOW, DIST_RED = 3, 5
FTD_MIN_DAY, FTD_PCT = 4, 1.5   # 반등 확인일: 저점 뒤 4일째 이후 +1.5% 이상 + 거래량 증가
FTD_MAX_DAY, FTD_LOOK = 15, 20  # 저점 = 최근 20거래일 최저 종가, 확인일은 저점 뒤 15일째까지만 인정
BREADTH_GREEN, BREADTH_RED = 50, 30   # 20일선 위 종목 비율(%)
VIX_GREEN, VIX_RED = 18, 25
FX_RED, FX_YELLOW = 2.0, 0.7          # 원/달러 20일 상승률(%)
US_RED, US_YELLOW = -2.5, -1.0        # 간밤 반도체·EWY 하루 등락률(%)
FLOW_RED = -10000                     # 외국인 5일 누적 순매수(억 원) -1조 이하
HIST_DAYS = 30


def ma(xs, n, i):
    if i + 1 < n:
        return None
    return sum(xs[i + 1 - n:i + 1]) / n


def light(c):
    return {"g": "green", "y": "yellow", "r": "red"}[c]


# ───────────── 지수 ─────────────
def index_series(sym, start):
    import FinanceDataReader as fdr
    df = fdr.DataReader(sym, start)
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    return [{"date": d.strftime("%Y-%m-%d"), "o": float(r.Open), "h": float(r.High), "l": float(r.Low), "c": float(r.Close), "v": float(r.Volume)}
            for d, r in df.iterrows()]


def trend_at(bars, i):
    cs = [b["c"] for b in bars]
    c, m20, m60, m200 = cs[i], ma(cs, 20, i), ma(cs, 60, i), ma(cs, 200, i)
    m60_old = ma(cs, 60, i - 5)
    if None in (m20, m60, m200, m60_old):
        return None
    up60 = m60 > m60_old
    if c > m60 and c > m200 and up60:
        st = "g"
    elif (c < m60 and c < m200) or (c < m200 and not up60):
        st = "r"
    else:
        st = "y"
    return {"st": st, "c": c, "ma20": m20, "ma60": m60, "ma200": m200, "up60": up60}


def dist_days(bars, i):
    out = []
    for k in range(max(1, i - DIST_WIN + 1), i + 1):
        p = (bars[k]["c"] / bars[k - 1]["c"] - 1) * 100
        if p <= DIST_DROP and bars[k]["v"] > bars[k - 1]["v"] > 0:
            out.append(bars[k]["date"])
    return out


def follow_through(bars, i):
    """지금 조정의 저점(최근 20거래일 최저 종가) 뒤에 반등 확인일(FTD)이 나왔는지. 오닐 기준: 저점 뒤 4~15일째."""
    lo_i = min(range(max(0, i - FTD_LOOK + 1), i + 1), key=lambda k: bars[k]["c"])
    days_since = i - lo_i
    lo_txt = bars[lo_i]["date"][5:].replace("-", "/")
    if days_since == 0:
        return {"state": "low", "ok": False, "text": f"오늘이 최근 {FTD_LOOK}일 최저 종가 · 반등 시작 전"}
    for k in range(lo_i + FTD_MIN_DAY, min(i, lo_i + FTD_MAX_DAY) + 1):
        p = (bars[k]["c"] / bars[k - 1]["c"] - 1) * 100
        if p >= FTD_PCT and bars[k]["v"] > bars[k - 1]["v"]:
            return {"state": "ftd", "date": bars[k]["date"], "ok": True,
                    "text": f"{bars[k]['date'][5:].replace('-', '/')} 반등 확인일 (저점 {lo_txt} 뒤 {k - lo_i}일째 +{p:.1f}%, 거래량 증가)"}
    if days_since < FTD_MIN_DAY:
        return {"state": "attempt", "ok": False, "text": f"저점({lo_txt}) 뒤 {days_since}일째 · {FTD_MIN_DAY}일째부터 확인일(+{FTD_PCT}% & 거래량 증가) 확인"}
    if days_since <= FTD_MAX_DAY:
        return {"state": "attempt", "ok": False, "text": f"저점({lo_txt}) 뒤 {days_since}일째 · 확인일(+{FTD_PCT}% & 거래량 증가) 아직 없음"}
    return {"state": "none", "ok": False, "text": f"저점({lo_txt}) 뒤 {FTD_MAX_DAY}일 안에 확인일 없음"}


def kis_index(iscd, days=420):
    """한국투자 업종 일봉 (코스피 0001, 코스닥 1001). 100개씩 거꾸로 받아 이어 붙임."""
    import kis
    if not kis.enabled():
        return []
    got, end = {}, dt.datetime.now(KST)
    stop = end - dt.timedelta(days=days)
    for _ in range(6):
        start = end - dt.timedelta(days=140)
        r = kis.get("/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice", "FHKUP03500100",
                    {"FID_COND_MRKT_DIV_CODE": "U", "FID_INPUT_ISCD": iscd, "FID_INPUT_DATE_1": start.strftime("%Y%m%d"),
                     "FID_INPUT_DATE_2": end.strftime("%Y%m%d"), "FID_PERIOD_DIV_CODE": "D"})
        rows = (r or {}).get("output2") or []
        n0 = len(got)
        for x in rows:
            d = str(x.get("stck_bsop_date") or "")
            try:
                bar = {"date": f"{d[:4]}-{d[4:6]}-{d[6:]}", "o": float(x["bstp_nmix_oprc"]), "h": float(x["bstp_nmix_hgpr"]),
                       "l": float(x["bstp_nmix_lwpr"]), "c": float(x["bstp_nmix_prpr"]), "v": float(x.get("acml_vol") or 0)}
            except (KeyError, TypeError, ValueError):
                continue
            if len(d) == 8 and bar["c"] > 0:
                got[bar["date"]] = bar
        if len(got) == n0:
            break
        oldest = min(got)
        end = dt.datetime.strptime(oldest, "%Y-%m-%d").replace(tzinfo=KST) - dt.timedelta(days=1)
        if end < stop:
            break
    return [got[k] for k in sorted(got)]


def load_index(fetch):
    """코스피·코스닥 일봉. 장마감 작업(fetch=True)은 한국투자에서 받아 저장, 아침 작업은 저장본 사용. 안 되면 FinanceDataReader."""
    path = os.path.join(OUT, "index_bars.json")
    src = {}
    if fetch:
        try:
            src = {"kospi": kis_index("0001"), "kosdaq": kis_index("1001")}
            if len(src["kospi"]) >= 210 and len(src["kosdaq"]) >= 210:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(src, f, separators=(",", ":"))
                return src, "한국투자"
        except Exception as e:
            print("한국투자 지수 실패:", type(e).__name__, e)
    try:
        with open(path, encoding="utf-8") as f:
            src = json.load(f)
        if len(src.get("kospi", [])) >= 210:
            return src, "저장본(한국투자)"
    except Exception:
        pass
    start = (dt.datetime.now(KST) - dt.timedelta(days=500)).strftime("%Y-%m-%d")
    return {"kospi": index_series("KS11", start), "kosdaq": index_series("KQ11", start)}, "FinanceDataReader"


# ───────────── 미국·환율 (yfinance) ─────────────
def yf_series(sym):
    import yfinance as yf
    h = yf.Ticker(sym).history(period="1y", auto_adjust=False)
    return [(d.strftime("%Y-%m-%d"), float(c)) for d, c in zip(h.index, h["Close"]) if c == c]


def last_before(series, day, strict=True):
    """series[(date, v)] 에서 day 보다 앞선(strict) 마지막 위치."""
    idx = None
    for k, (d, _) in enumerate(series):
        if (d < day) if strict else (d <= day):
            idx = k
    return idx


# ───────────── 외국인 수급 (한국투자) ─────────────
def kis_flows(days=60):
    import kis
    if not kis.enabled():
        return None, "키 없음"
    end = dt.datetime.now(KST).strftime("%Y%m%d")
    start = (dt.datetime.now(KST) - dt.timedelta(days=days * 2)).strftime("%Y%m%d")
    best = []
    for d1, d2 in ((end, start), (start, end), (end, end)):
        r = kis.get("/uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market", "FHPTJ04040000",
                    {"FID_COND_MRKT_DIV_CODE": "U", "FID_INPUT_ISCD": "0001", "FID_INPUT_DATE_1": d1, "FID_INPUT_ISCD_1": "KSP",
                     "FID_INPUT_DATE_2": d2, "FID_INPUT_ISCD_2": "0001"})
        rows = (r or {}).get("output") or []
        if isinstance(rows, dict):
            rows = [rows]
        if len(rows) > len(best):
            best = rows
        if len(best) >= 10:
            break
    out = {}
    for row in best:
        d = str(row.get("stck_bsop_date") or "")
        try:
            f = float(row.get("frgn_ntby_tr_pbmn"))
            o = float(row.get("orgn_ntby_tr_pbmn"))
        except (TypeError, ValueError):
            continue
        if len(d) == 8:
            out[f"{d[:4]}-{d[4:6]}-{d[6:]}"] = {"f": f / 100, "o": o / 100}   # 백만 원 → 억 원
    sample = {k: best[0].get(k) for k in ("stck_bsop_date", "frgn_ntby_tr_pbmn", "orgn_ntby_tr_pbmn", "bstp_nmix_prpr")} if best else {}
    return out, {"rows": len(best), "sample": sample, "kis": dict(kis.STATS)}


# ───────────── 판정 ─────────────
def evaluate(day, kospi, kosdaq, breadth, us, flows):
    """day 기준 신호 목록과 종합 판정. us: {"vix","krw","sox","ewy": [(date, v)]}"""
    ik = next((k for k, b in enumerate(kospi) if b["date"] == day), None)
    iq = next((k for k, b in enumerate(kosdaq) if b["date"] == day), None)
    bi = next((k for k, b in enumerate(breadth) if b["date"] == day), None)
    sig, re = [], []

    def add(key, title, st, value, text):
        sig.append({"key": key, "title": title, "light": light(st), "value": value, "text": text})

    tk = trend_at(kospi, ik) if ik is not None else None
    for name, bars, i, t in (("코스피", kospi, ik, tk), ("코스닥", kosdaq, iq, trend_at(kosdaq, iq) if iq is not None else None)):
        if not t:
            continue
        pos = lambda m: "위" if t["c"] > m else "아래"
        add("trend_" + name, f"{name} 추세", t["st"], f"{t['c']:,.0f}",
            f"20일선 {pos(t['ma20'])} · 60일선 {pos(t['ma60'])}({'상승' if t['up60'] else '하락'} 중) · 200일선 {pos(t['ma200'])}")
    if ik is not None:
        dd = dist_days(kospi, ik)
        n = len(dd)
        add("dist", "분산일 (기관 매도 흔적)", "r" if n >= DIST_RED else "y" if n >= DIST_YELLOW else "g", f"{n}일",
            f"최근 {DIST_WIN}거래일 중 코스피가 {DIST_DROP}% 이상 빠지면서 거래량이 늘어난 날" + (f" · 최근 {', '.join(x[5:].replace('-', '/') for x in dd[-3:])}" if dd else ""))
    if bi is not None:
        b = breadth[bi]
        pa = b["above20"] / b["n"] * 100 if b["n"] else 0
        add("breadth", "시장 폭 (20일선 위 종목)", "g" if pa >= BREADTH_GREEN else "r" if pa < BREADTH_RED else "y", f"{pa:.0f}%",
            f"전 종목 {b['n']:,}개 중 {b['above20']:,}개 · 오늘 상승 {b['up']:,} / 하락 {b['down']:,}")
        hi5 = sum(x["newHigh"] for x in breadth[max(0, bi - 4):bi + 1])
        lo5 = sum(x["newLow"] for x in breadth[max(0, bi - 4):bi + 1])
        add("hilo", "신고가 vs 신저가 (5일 합)", "g" if hi5 > lo5 else "r" if lo5 > max(1, hi5) * 2 else "y", f"{hi5} : {lo5}",
            "52주 신고가 종목 수 : 신저가 종목 수. 신저가가 신고가의 2배를 넘으면 빨강")
    if flows:
        fd = sorted(d for d in flows if d <= day)[-5:]
        if fd:
            fs = sum(flows[d]["f"] for d in fd)
            os_ = sum(flows[d]["o"] for d in fd)
            add("flow", "외국인 수급 (코스피 5일)", "g" if fs > 0 else "r" if fs <= FLOW_RED else "y", f"{fs:+,.0f}억",
                f"외국인 {fs:+,.0f}억 · 기관 {os_:+,.0f}억 ({fd[0][5:].replace('-', '/')}~{fd[-1][5:].replace('-', '/')})")
    krw = us.get("krw") or []
    k = last_before(krw, day, strict=False)
    if k is not None and k >= 20:
        ch = (krw[k][1] / krw[k - 20][1] - 1) * 100
        add("fx", "원/달러 환율 (20일 변화)", "r" if ch >= FX_RED else "y" if ch >= FX_YELLOW else "g", f"{krw[k][1]:,.1f}원",
            f"20거래일 전보다 {ch:+.1f}% · 원화가 빠르게 약해지면 외국인 매도가 길어지는 경우가 많음")
    parts, worst = [], None
    for key, nm in (("sox", "필라델피아 반도체"), ("ewy", "한국 ETF(EWY)")):
        s = us.get(key) or []
        j = last_before(s, day)
        if j is not None and j >= 1:
            p = (s[j][1] / s[j - 1][1] - 1) * 100
            worst = p if worst is None else min(worst, p)
            parts.append(f"{nm} {p:+.2f}%")
    if parts:
        add("us", "간밤 미국 반도체·EWY", "r" if worst <= US_RED else "y" if worst <= US_YELLOW else "g", f"{worst:+.1f}%", " · ".join(parts) + " (한국장 전날 밤)")
    vx = us.get("vix") or []
    j = last_before(vx, day)
    if j is not None:
        v = vx[j][1]
        add("vix", "VIX 공포지수", "g" if v < VIX_GREEN else "r" if v > VIX_RED else "y", f"{v:.1f}",
            f"{VIX_GREEN} 아래 안정 · {VIX_RED} 넘으면 공포 구간")

    reds = sum(1 for x in sig if x["light"] == "red")
    yell = sum(1 for x in sig if x["light"] == "yellow")
    tr = next((x for x in sig if x["key"] == "trend_코스피"), None)
    brd = next((x for x in sig if x["key"] == "breadth"), None)
    if (tr and tr["light"] == "red" and brd and brd["light"] == "red") or reds >= 5:
        overall = "red"
    elif tr and tr["light"] == "green" and (not brd or brd["light"] == "green") and reds <= 1:
        overall = "green"
    else:
        overall = "yellow"

    # 재진입 체크리스트
    if ik is not None:
        ft = follow_through(kospi, ik)
        re.append({"title": "반등 확인일 (오닐 FTD)", "ok": ft["ok"], "text": ft["text"]})
        t = tk
        if t:
            run = 0
            for k2 in range(ik, -1, -1):
                m = ma([b["c"] for b in kospi], 20, k2)
                if m is None or kospi[k2]["c"] <= m:
                    break
                run += 1
            re.append({"title": "코스피 20일선 회복", "ok": run >= 2, "text": f"20일선 위 {run}일째" if run else f"20일선({t['ma20']:,.0f}) 아래"})
    if bi is not None and bi >= 10:
        pas = [x["above20"] / x["n"] * 100 for x in breadth[bi - 10:bi + 1] if x["n"]]
        mn = min(pas)
        ok = pas[-1] >= BREADTH_RED + 10 and pas[-1] >= mn + 15
        re.append({"title": "시장 폭 회복", "ok": ok, "text": f"20일선 위 종목 {pas[-1]:.0f}% (최근 10일 최저 {mn:.0f}%) · 40% 이상이면서 최저보다 15%p 이상 회복"})
        lo_now = sum(x["newLow"] for x in breadth[bi - 4:bi + 1])
        lo_prev = sum(x["newLow"] for x in breadth[max(0, bi - 9):bi - 4])
        re.append({"title": "신저가 종목 감소", "ok": lo_now < lo_prev * 0.5 or lo_now <= 5,
                   "text": f"최근 5일 신저가 {lo_now}개 (그 전 5일 {lo_prev}개)"})
    if vx:
        j = last_before(vx, day)
        if j is not None:
            peak = max(v for _, v in vx[max(0, j - 20):j + 1])
            re.append({"title": "VIX 안정", "ok": vx[j][1] < 20, "text": f"현재 {vx[j][1]:.1f} (최근 20일 최고 {peak:.1f}) · 20 아래면 안정"})
    if flows:
        fd = sorted(d for d in flows if d <= day)[-3:]
        if len(fd) == 3:
            re.append({"title": "외국인 순매수 전환", "ok": all(flows[d]["f"] > 0 for d in fd),
                       "text": "최근 3일 외국인 " + " · ".join(f"{flows[d]['f']:+,.0f}억" for d in fd)})
    return {"overall": overall, "reds": reds, "yellows": yell, "signals": sig, "reentry": re}


def chart(bars, n=120):
    cs = [b["c"] for b in bars]
    out = []
    for i in range(max(0, len(bars) - n), len(bars)):
        out.append([bars[i]["date"], round(cs[i], 2), *(round(m, 2) if m else None for m in (ma(cs, 20, i), ma(cs, 60, i), ma(cs, 200, i)))])
    return out


def main(fetch_flows=False):
    now = dt.datetime.now(KST)
    diag = {}
    idx, diag["indexSource"] = load_index(fetch_flows)
    kospi, kosdaq = idx["kospi"], idx["kosdaq"]
    drop_today = (now.hour, now.minute) < (15, 40)
    if drop_today:   # 장중에는 오늘 봉이 미완성이라 뺀다
        today = now.strftime("%Y-%m-%d")
        kospi = [b for b in kospi if b["date"] < today]
        kosdaq = [b for b in kosdaq if b["date"] < today]
    try:
        with open(os.path.join(OUT, "breadth_kr.json"), encoding="utf-8") as f:
            breadth = json.load(f)
    except Exception:
        breadth = []
    us = {}
    for key, sym in (("vix", "^VIX"), ("krw", "KRW=X"), ("sox", "^SOX"), ("ewy", "EWY")):
        try:
            us[key] = yf_series(sym)
        except Exception as e:
            diag[key] = f"{type(e).__name__}: {e}"
    flows_path = os.path.join(OUT, "market_flows.json")
    flows = {}
    try:
        with open(flows_path, encoding="utf-8") as f:
            flows = json.load(f)
    except Exception:
        pass
    if fetch_flows:
        try:
            got, info = kis_flows()
            diag["flows"] = {k: v for k, v in info.items() if k != "sample"} if isinstance(info, dict) else info
            if got:
                flows.update(got)
                with open(flows_path, "w", encoding="utf-8") as f:
                    json.dump(dict(sorted(flows.items())[-120:]), f)
        except Exception as e:
            diag["flows"] = f"{type(e).__name__}: {e}"
    day = kospi[-1]["date"]
    cur = evaluate(day, kospi, kosdaq, breadth, us, flows)
    hist = []
    for b in kospi[-HIST_DAYS:]:
        try:
            e = evaluate(b["date"], kospi, kosdaq, breadth, us, flows)
            hist.append({"date": b["date"], "overall": e["overall"], "reds": e["reds"]})
        except Exception:
            pass
    bh = [{"date": x["date"], "pct": round(x["above20"] / x["n"] * 100, 1), "hi": x["newHigh"], "lo": x["newLow"]} for x in breadth[-60:] if x["n"]]
    payload = {"asOf": day, "generatedAt": now.strftime("%Y-%m-%d %H:%M"), **cur, "history": hist,
               "charts": {"kospi": chart(kospi), "kosdaq": chart(kosdaq)}, "breadth": bh, "diag": diag}
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/market_signal.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.signal = ")
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print("시장 신호등:", day, cur["overall"], {x["title"]: x["light"] for x in cur["signals"]}, diag)


if __name__ == "__main__":
    main(fetch_flows="--flows" in sys.argv)
