"""5장 유형 A '종가배팅주' 수집 (장 마감 직전 15:10~15:45 사이 5분 간격 실행).

1) 어제까지 일봉으로 만든 기준값(out/closing_base_kr.json, 장 마감 후 run_scan 이 생성)
2) 네이버 실시간 시세로 1차 거름 → 후보만 야후 1분봉으로 오늘 시·고·저·종가와 15시 이후 거래량 비중 계산
3) A1 후보는 네이버 투자자별 매매동향(외국인+기관 잠정 순매수)을 확인
4) 세 유형별 상위 5개를 data/shortterm.js 로 저장
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import closing
from config import CP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_JS = os.path.join(HERE, "..", "data", "shortterm.js")
KST = dt.timezone(dt.timedelta(hours=9))
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1m"

SUBTYPES = [
    {"id": "A1", "name": "장 마감 직전 대형수급 + 당일 고가 마감",
     "desc": f"마감 직전 외국인·기관 순매수(거래대금의 {CP.a1_flow_share * 100:g}% 이상)가 몰리고, 고가 대비 {CP.a1_high_gap * 100:g}% 이내로 마감하는 종목"},
    {"id": "A2", "name": "급등 후 거래량 반토막 + 도지, 10·20일선 사수",
     "desc": f"전일 +{CP.a2_prev_pct:g}% 이상 급등 → 오늘 거래량 {CP.a2_vol_ratio * 100:g}% 이하, 도지형 캔들, 종가가 10일선·20일선 위"},
    {"id": "A3", "name": "바닥권 거래대금 폭발 장대양봉 + 240·480일선 돌파",
     "desc": f"250일 범위 하단 {CP.a3_pos_max * 100:g}% 이내 → 거래대금 20일 평균의 {CP.a3_value_mult:g}배 이상, +{CP.a3_body_pct:g}% 이상 장대양봉으로 240·480일선 동시 돌파"},
]


def yahoo_bars(code, market, now=None):
    """야후 1분봉 → {open, high, low, close, lateShare, lastTs}. 실패하면 None."""
    sym = code + (".KS" if market == "KOSPI" else ".KQ")
    try:
        req = urllib.request.Request(YAHOO.format(sym=sym), headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            res = json.loads(r.read().decode())["chart"]["result"][0]
        return parse_bars(res)
    except Exception:
        return None


NAVER_MIN = "https://api.stock.naver.com/chart/domestic/item/{code}/minute?startDateTime={d}0900&endDateTime={d}1600"


def parse_naver_minutes(rows):
    """네이버 1분봉(실시간) → {open, high, low, close, lateShare, lastTs}. 비어 있으면 None."""
    bars = []
    for r in rows or []:
        try:
            t = dt.datetime.strptime(str(r["localDateTime"])[:12], "%Y%m%d%H%M").replace(tzinfo=KST).timestamp()
            bars.append((t, float(r["openPrice"]), float(r["highPrice"]), float(r["lowPrice"]), float(r["currentPrice"]),
                         float(r.get("accumulatedTradingVolume") or 0)))
        except (KeyError, TypeError, ValueError):
            continue
    if not bars:
        return None
    bars.sort()
    tot = sum(b[5] for b in bars)
    cut = bars[-1][0] - CP.a1_late_min * 60
    late = sum(b[5] for b in bars if b[0] > cut)
    return {"open": bars[0][1], "high": max(b[2] for b in bars), "low": min(b[3] for b in bars), "close": bars[-1][4],
            "lateShare": (late / tot) if tot > 0 else None, "lastTs": bars[-1][0], "src": "naver"}


def naver_bars(code, market=None, now=None):
    try:
        import naver_live
        d = (now or dt.datetime.now(KST)).strftime("%Y%m%d")
        return parse_naver_minutes(naver_live._get(NAVER_MIN.format(code=code, d=d), tries=2))
    except Exception:
        return None


def live_bars(code, market):
    """실시간인 네이버 분봉을 먼저 쓰고, 안 되면 야후(약 20분 지연)."""
    return naver_bars(code, market) or yahoo_bars(code, market)


def parse_bars(res):
    ts = res.get("timestamp") or []
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    rows = [(t, o, h, l, c, v) for t, o, h, l, c, v in zip(ts, q.get("open", []), q.get("high", []), q.get("low", []),
                                                           q.get("close", []), q.get("volume", []))
            if None not in (o, h, l, c) and (v or 0) >= 0]
    if not rows:
        return None
    tot = sum(r[5] or 0 for r in rows)
    cut = rows[-1][0] - CP.a1_late_min * 60          # 받은 분봉 중 마지막 a1_late_min 분
    late = sum((v or 0) for t, o, h, l, c, v in rows if t > cut)
    return {"open": rows[0][1], "high": max(r[2] for r in rows), "low": min(r[3] for r in rows), "close": rows[-1][4],
            "lateShare": (late / tot) if tot > 0 else None, "lastTs": rows[-1][0]}


def run(universe, base, now, fetch_bars=live_bars, fetch_flows=None, meta=None, final=False):
    """universe: {code:{name,price,volume,pct?,market}}, base: {code:features}. 반환: (subtype별 목록, 진단)."""
    qs = {}
    for code, u in universe.items():
        b = base.get(code)
        pct = u.get("pct")     # 네이버 화면과 같은 등락률 우선
        if pct is None and b and b.get("prevClose"):
            pct = (u["price"] / b["prevClose"] - 1) * 100
        if pct is None:
            continue
        qs[code] = {"price": u["price"], "volume": u["volume"],
                    "value": u.get("value") or u["price"] * u["volume"], "pct": pct}
    diag = {"quotes": len(qs)}
    cands = {}
    for code, q in qs.items():
        s = closing.prefilter(q, base.get(code))
        if s:
            cands[code] = s
    diag["candidates"] = len(cands)
    if len(cands) > 150:   # 분봉 호출 상한
        top = sorted(cands, key=lambda c: -qs[c]["value"])[:150]
        cands = {c: cands[c] for c in top}
    with ThreadPoolExecutor(6) as ex:
        bars = dict(zip(cands, ex.map(lambda c: fetch_bars(c, universe[c]["market"]), cands)))
    flows = {}
    if fetch_flows:
        a1 = {c: qs[c]["price"] for c, s in cands.items() if "A1" in s and bars.get(c)}
        flows = fetch_flows(a1) if a1 else {}
    fdet = {c: v for c, v in flows.items() if isinstance(v, dict)}
    flows = {c: (v["sum"] if isinstance(v, dict) else v) for c, v in flows.items()}
    res = {"A1": [], "A2": [], "A3": []}
    nbars = 0
    why, stale_n, late_vals = {}, 0, []
    for code, kinds in cands.items():
        b = bars.get(code)
        if not b:
            continue
        nbars += 1
        q = qs[code]
        stale = (not final) and (now.timestamp() - b["lastTs"]) > 25 * 60   # 마감 후에는 15:30 봉이 마지막이라 지연으로 보지 않음
        bb = dict(b)
        bb["high"] = max(b["high"], q["price"])
        bb["low"] = min(b["low"], q["price"])
        if stale:
            bb["lateShare"] = None
            stale_n += 1
        if "A1" in kinds:
            r1 = closing.a1_reason(q, bb, flows.get(code))
            why[r1] = why.get(r1, 0) + 1
            if bb.get("lateShare") is not None:
                late_vals.append(round(bb["lateShare"], 3))
        jobs = {"A1": lambda: closing.judge_a1(q, bb, flows.get(code), fdet.get(code)),
                "A2": lambda: closing.judge_a2(q, bb, base.get(code)),
                "A3": lambda: closing.judge_a3(q, bb, base.get(code))}
        for k in kinds:
            r = jobs[k]()
            if r:
                mt = (meta or {}).get(code, {})
                res[k].append({"code": code, "name": universe[code]["name"], "close": q["price"],
                               "market": universe[code].get("market", ""), "sector": mt.get("sector", ""),
                               "marcap": round(universe[code]["marcap"] / 1e8) if universe[code].get("marcap") else mt.get("marcap", 0),
                               "prevClose": universe[code].get("prev") or (base.get(code) or {}).get("prevClose"),
                               "changePct": round(q["pct"], 2), "value": round(q["value"] / 1e8), "note": r["note"],
                               "score": r["score"]})
    diag["bars"] = nbars
    diag["naverBars"] = sum(1 for b in bars.values() if b and b.get("src") == "naver")
    late_vals.sort()
    diag["a1"] = {"후보": sum(1 for s in cands.values() if "A1" in s), "분봉지연": stale_n, "사유": why,
                  "수급자료": sum(1 for v in flows.values() if v is not None), "막판비중_중앙값": late_vals[len(late_vals) // 2] if late_vals else None,
                  "막판비중_최대": late_vals[-1] if late_vals else None}
    for k in res:
        res[k].sort(key=lambda x: -x["score"])
        res[k] = [{kk: vv for kk, vv in x.items() if kk != "score"} for x in res[k][:CP.top_n]]
    return res, diag


def to_payload(res, as_of, status):
    return {"asOf": as_of, "window": "15:20~15:40", "status": status,
            "types": [{"id": "A", "name": "종가배팅주", "timeframe": "일봉·분봉",
                       "desc": "장 마감 직전(15:20~15:40)에 확인하는 종목. 자동으로 5분마다 갱신됩니다.",
                       "subtypes": [dict(s, kr=res.get(s["id"], [])) for s in SUBTYPES]}]}


def write_js(payload):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "closing_kr.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/collect_closing.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.shortterm = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")


def pick_base(today):
    """오늘 판정에 쓸 '어제까지의 일봉 요약'. 장마감 스캔이 이미 오늘 것으로 덮어썼으면 보관해 둔 직전 것을 쓴다."""
    for name in ("closing_base_kr.json", "closing_base_kr_prev.json"):
        try:
            with open(os.path.join(OUT, name), encoding="utf-8") as f:
                bj = json.load(f)
            if bj.get("asOf") and bj["asOf"] < today:
                return bj
        except Exception:
            continue
    return None


def main(mode="auto"):
    """mode: auto(15:05~15:50 에만) / force(시간 무관, 장중 방식) / final(장 마감 후: 종가 확정 + 외국인·기관 수급 반영)"""
    from naver_live import fetch_flows, fetch_universe
    now = dt.datetime.now(KST)
    stamp = now.strftime("%Y-%m-%d %H:%M")
    hm = (now.hour, now.minute)
    if mode == "auto" and not (now.weekday() < 5 and (15, 5) <= hm <= (15, 50)):
        print("장 마감 직전 시간대가 아니라 건너뜀", stamp)
        return
    if mode == "final" and not (now.weekday() < 5 and hm >= (15, 45)):
        print("마감 후 시간대가 아니라 건너뜀", stamp)
        return
    today = now.strftime("%Y-%m-%d")
    bj = pick_base(today)
    if not bj:
        if not os.path.exists(os.path.join(OUT, "closing_kr.json")):
            write_js(to_payload({}, stamp, "기준 데이터(일봉 요약)가 아직 없습니다. 장마감 작업이 먼저 실행되어야 합니다."))
        print("어제까지의 기준 데이터가 없음 → 건너뜀")
        return
    try:
        uni, keys = fetch_universe()
    except Exception as e:
        write_js(to_payload({}, stamp, f"네이버 실시간 시세 조회 실패: {type(e).__name__}"))
        print("fail", e)
        return
    print("naver row keys:", keys)
    base = bj["base"]
    days = [u.get("day") for u in uni.values() if u.get("day")]
    traded_today = sum(1 for d in days if d == today)
    if days and traded_today / len(days) < 0.4:
        write_js(to_payload({}, stamp, "휴장일이거나 시세가 갱신되지 않은 것으로 보여 건너뜁니다."))
        return
    meta = {}
    try:
        with open(os.path.join(OUT, "kr_meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
    except Exception:
        pass
    try:   # 업종은 네이버 업종표(장중 갱신 작업이 만듦)를 우선 사용
        with open(os.path.join(OUT, "kr_sector.json"), encoding="utf-8") as f:
            for c, name in json.load(f).get("map", {}).items():
                meta.setdefault(c, {})["sector"] = name
    except Exception:
        pass
    res, diag = run(uni, base, now, fetch_flows=fetch_flows, meta=meta, final=(mode == "final"))
    try:   # 진단용 표본 (응답 형식 확인)
        import naver_live
        smp = {}
        for name, url in (("trend", "https://m.stock.naver.com/api/stock/005930/trend"),
                          ("minute", "https://api.stock.naver.com/chart/domestic/item/005930/minute?startDateTime=" + now.strftime("%Y%m%d") + "1500&endDateTime=" + now.strftime("%Y%m%d") + "1600"),
                          ("integration", "https://m.stock.naver.com/api/stock/005930/integration")):
            try:
                v = naver_live._get(url, tries=1)
                smp[name] = v[-4:] if isinstance(v, list) else {k: (v[k][:3] if isinstance(v[k], list) else v[k]) for k in list(v)[:40]}
            except Exception as e:
                smp[name] = f"ERR {type(e).__name__}: {e}"
        with open(os.path.join(OUT, "closing_sample.json"), "w", encoding="utf-8") as f:
            json.dump(smp, f, ensure_ascii=False, indent=1)
    except Exception as e:
        print("표본 저장 실패", e)
    print(diag, {k: len(v) for k, v in res.items()})
    n_flow = diag.get("a1", {}).get("수급자료", 0)
    if mode == "final" and n_flow == 0:
        try:   # 수급이 아직 공개 전이면 이미 확정 수급으로 만든 결과를 덮어쓰지 않는다
            with open(os.path.join(OUT, "closing_kr.json"), encoding="utf-8") as f:
                old = json.load(f)
            if old.get("flowConfirmed") and str(old.get("asOf", ""))[:10] == today:
                print("수급 자료 없음 → 기존 확정 결과 유지")
                return
        except Exception:
            pass
    payload = to_payload(res, stamp, f"전 종목 {diag['quotes']}개 중 후보 {diag['candidates']}개 점검 (기준 일봉 {bj['asOf']})")
    payload["diag"] = diag
    payload["flowConfirmed"] = bool(n_flow)
    if mode == "final":
        payload["phase"] = ("장 마감 후 · 종가 확정 · 외국인·기관 수급 반영" if n_flow else "장 마감 후 · 종가 확정 · 수급 자료는 아직 공개 전")
    else:
        payload["phase"] = "장중 · 수급 자료는 마감 후(16시 이후) 반영됩니다"
    write_js(payload)


if __name__ == "__main__":
    main("final" if "--final" in sys.argv else "force" if "--force" in sys.argv else "auto")
