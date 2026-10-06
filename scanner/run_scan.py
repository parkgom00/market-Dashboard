"""중장기(4장) 스캐너 실행.

사용 예:
  python run_scan.py --market kr          # 국내 전 종목 (장 마감 후, 예: 16:00 이후)
  python run_scan.py --market us          # 미국 (미국장 마감 후 = 한국 아침)
  python run_scan.py --market kr --limit 30   # 앞 30개 종목만 빠르게 시험

결과는 scanner/out/longterm_kr.json, longterm_us.json 에 저장되고,
두 파일을 합쳐 ../data/longterm.js 를 새로 씁니다.
"""
import argparse
import datetime as dt
import json
import os

from config import P
import closing
from rules import NOTE_FMT, evaluate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_JS = os.path.join(HERE, "..", "data", "longterm.js")

RULES = [
    {"id": "L1", "label": "정배열 상승 + 이평선 지지",
     "desc": "5>10>20>60>120>240>480일선 정배열, 20·60일선 상승 중, 최근 20일 안에 20일선 또는 60일선에서 지지"},
    {"id": "L2", "label": "급등 후 60일선 지지",
     "desc": f"20일 안에 +{int(P.surge_pct * 100)}% 이상 급등 후 고점 대비 -{int(P.min_drawdown * 100)}% 이상 조정, 60일선(상승 중)에서 지지"},
    {"id": "L3a", "label": "240일선 거래량 돌파",
     "desc": f"최근 {P.breakout_days}일 안에 240일선을 아래→위로 돌파, 돌파일 거래량이 직전 20일 평균의 {P.vol_mult:g}배 이상"},
    {"id": "L3b", "label": "480일선 거래량 돌파",
     "desc": f"최근 {P.breakout_days}일 안에 480일선을 아래→위로 돌파, 돌파일 거래량이 직전 20일 평균의 {P.vol_mult:g}배 이상"},
]


def _r(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return None if v != v else round(v, 2)


def scan_market(market: str, limit: int = 0):
    import fetch
    from rules import add_indicators

    uni = fetch.kr_universe() if market == "kr" else fetch.us_universe()
    if limit:
        uni = uni.head(limit)
    names = dict(zip(uni["code"], uni["name"]))
    meta = {}
    if market == "kr" and "market" in uni.columns:
        for c, mk, mc, sc in zip(uni["code"], uni["market"], uni["marcap"], uni["sector"]):
            try:
                meta[c] = {"market": mk, "sector": str(sc or ""), "marcap": round(float(mc) / 1e8)}
            except (TypeError, ValueError):
                meta[c] = {"market": mk, "sector": str(sc or ""), "marcap": 0}
    gen = fetch.kr_prices(uni["code"]) if market == "kr" else fetch.us_prices(uni["code"])
    min_value = P.min_value_kr if market == "kr" else P.min_value_us

    items, scanned, as_of = [], 0, ""
    base = {}
    for code, df in gen:
        scanned += 1
        as_of = max(as_of, df.index[-1].strftime("%Y-%m-%d"))
        value20 = (df["close"] * df["volume"]).tail(20).mean()
        if market == "kr" and value20 >= 5e8:   # 종가배팅주(5장 A) 판정용 기준값
            try:
                bf = closing.base_features(df)
                if bf:
                    base[code] = bf
            except Exception:
                pass
        if value20 < min_value:
            continue
        hits = evaluate(df, P)
        if not hits:
            continue
        ind = add_indicators(df).iloc[-1]
        prev = float(df["close"].iloc[-2]) if len(df) > 1 else 0.0
        last = float(df["close"].iloc[-1])
        m = meta.get(code, {})
        items.append({
            "code": code, "name": names.get(code, code),
            "market": m.get("market", ""), "sector": m.get("sector", ""), "marcap": m.get("marcap", 0),
            "prevClose": _r(prev), "changePct": _r((last / prev - 1) * 100) if prev else None,
            "value": round(last * float(df["volume"].iloc[-1]) / 1e8) if market == "kr" else None,
            "close": _r(ind["close"]), "ma240": _r(ind["ma240"]), "ma480": _r(ind["ma480"]),
            "matched": list(hits.keys()),
            "note": " / ".join(NOTE_FMT[k](v) for k, v in hits.items()),
        })
    items.sort(key=lambda x: (-len(x["matched"]), x["name"]))
    if market == "kr":
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, "kr_meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, separators=(",", ":"))
        with open(os.path.join(OUT, "closing_base_kr.json"), "w", encoding="utf-8") as f:
            json.dump({"asOf": as_of, "base": base}, f, ensure_ascii=False, separators=(",", ":"))
    return {"asOf": as_of, "scanned": scanned, "items": items}


def build_js():
    def load(m):
        path = os.path.join(OUT, f"longterm_{m}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {"asOf": "", "scanned": 0, "items": []}

    kr, us = load("kr"), load("us")
    payload = {
        "rules": RULES,
        "scanInfo": {"kr": {"asOf": kr["asOf"], "scanned": kr["scanned"]},
                     "us": {"asOf": us["asOf"], "scanned": us["scanned"]}},
        "kr": kr["items"], "us": us["items"],
    }
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/run_scan.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.longterm = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["kr", "us", "all"], default="all")
    ap.add_argument("--limit", type=int, default=0, help="시험용: 앞에서 N개 종목만")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    for m in (["kr", "us"] if a.market == "all" else [a.market]):
        print(f"[{m}] 스캔 시작 {dt.datetime.now():%H:%M:%S}")
        res = scan_market(m, a.limit)
        with open(os.path.join(OUT, f"longterm_{m}.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False)
        print(f"[{m}] 기준일 {res['asOf']}, 스캔 {res['scanned']}개, 조건 충족 {len(res['items'])}개")
    build_js()
    print("data/longterm.js 갱신 완료")


if __name__ == "__main__":
    main()
