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


def parse_bars(res):
    ts = res.get("timestamp") or []
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    rows = [(t, o, h, l, c, v) for t, o, h, l, c, v in zip(ts, q.get("open", []), q.get("high", []), q.get("low", []),
                                                           q.get("close", []), q.get("volume", []))
            if None not in (o, h, l, c) and (v or 0) >= 0]
    if not rows:
        return None
    tot = sum(r[5] or 0 for r in rows)
    late = 0
    h_, m_ = map(int, CP.a1_late_from.split(":"))
    for t, o, h, l, c, v in rows:
        k = dt.datetime.fromtimestamp(t, KST)
        if (k.hour, k.minute) >= (h_, m_):
            late += v or 0
    return {"open": rows[0][1], "high": max(r[2] for r in rows), "low": min(r[3] for r in rows), "close": rows[-1][4],
            "lateShare": (late / tot) if tot > 0 else None, "lastTs": rows[-1][0]}


def run(universe, base, now, fetch_bars=yahoo_bars, fetch_flows=None, meta=None):
    """universe: {code:{name,price,volume,pct?,market}}, base: {code:features}. 반환: (subtype별 목록, 진단)."""
    qs = {}
    for code, u in universe.items():
        b = base.get(code)
        pct = (u["price"] / b["prevClose"] - 1) * 100 if b and b.get("prevClose") else u.get("pct")
        if pct is None:
            continue
        qs[code] = {"price": u["price"], "volume": u["volume"], "value": u["price"] * u["volume"], "pct": pct}
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
    res = {"A1": [], "A2": [], "A3": []}
    nbars = 0
    for code, kinds in cands.items():
        b = bars.get(code)
        if not b:
            continue
        nbars += 1
        q = qs[code]
        stale = (now.timestamp() - b["lastTs"]) > 25 * 60
        bb = dict(b)
        bb["high"] = max(b["high"], q["price"])
        bb["low"] = min(b["low"], q["price"])
        if stale:
            bb["lateShare"] = None
        jobs = {"A1": lambda: closing.judge_a1(q, bb, flows.get(code)),
                "A2": lambda: closing.judge_a2(q, bb, base.get(code)),
                "A3": lambda: closing.judge_a3(q, bb, base.get(code))}
        for k in kinds:
            r = jobs[k]()
            if r:
                mt = (meta or {}).get(code, {})
                res[k].append({"code": code, "name": universe[code]["name"], "close": q["price"],
                               "market": universe[code].get("market", ""), "sector": mt.get("sector", ""),
                               "marcap": mt.get("marcap", 0),
                               "prevClose": (base.get(code) or {}).get("prevClose"),
                               "changePct": round(q["pct"], 2), "value": round(q["value"] / 1e8), "note": r["note"],
                               "score": r["score"]})
    diag["bars"] = nbars
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


def main(force=False):
    from naver_live import fetch_flows, fetch_universe
    now = dt.datetime.now(KST)
    stamp = now.strftime("%Y-%m-%d %H:%M")
    if not force and not (now.weekday() < 5 and (15, 5) <= (now.hour, now.minute) <= (15, 50)):
        print("장 마감 직전 시간대가 아니라 건너뜀", stamp)
        return
    path = os.path.join(OUT, "closing_base_kr.json")
    if not os.path.exists(path):
        write_js(to_payload({}, stamp, "기준 데이터(일봉 요약)가 아직 없습니다. 장마감 작업이 먼저 실행되어야 합니다."))
        return
    with open(path, encoding="utf-8") as f:
        bj = json.load(f)
    today = now.strftime("%Y-%m-%d")
    if bj["asOf"] >= today:
        print("기준일이 오늘 → 이미 오늘 마감 데이터가 반영됨, 건너뜀")
        return
    try:
        uni, keys = fetch_universe()
    except Exception as e:
        write_js(to_payload({}, stamp, f"네이버 실시간 시세 조회 실패: {type(e).__name__}"))
        print("fail", e)
        return
    print("naver row keys:", keys)
    base = bj["base"]
    same = sum(1 for c, u in uni.items() if c in base and abs(u["price"] - base[c]["prevClose"]) < 1e-9)
    common = sum(1 for c in uni if c in base)
    if common and same / common > 0.6:
        write_js(to_payload({}, stamp, "휴장일이거나 시세가 갱신되지 않은 것으로 보여 건너뜁니다."))
        return
    meta = {}
    try:
        with open(os.path.join(OUT, "kr_meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
    except Exception:
        pass
    res, diag = run(uni, base, now, fetch_flows=fetch_flows, meta=meta)
    print(diag, {k: len(v) for k, v in res.items()})
    write_js(to_payload(res, stamp, f"전 종목 {diag['quotes']}개 중 후보 {diag['candidates']}개 점검 (기준 일봉 {bj['asOf']})"))


if __name__ == "__main__":
    main(force="--force" in sys.argv)
