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
import rules2
from rules import NOTE_FMT, evaluate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_JS = os.path.join(HERE, "..", "data", "longterm.js")

RULES = [
    {"id": "L1", "label": "정배열 상승 + 이평선 지지",
     "desc": "5>10>20>60>120>240>480일선 정배열, 20·60일선 상승 중, 최근 20일 안에 20일선 또는 60일선에서 지지"},
    {"id": "L2", "label": "급등 후 60일선 지지",
     "desc": f"20일 안에 +{int(P.surge_pct * 100)}% 이상 급등 후 고점 대비 -{int(P.min_drawdown * 100)}% 이상 조정, 60일선(상승 중)에서 지지"},
    {"id": "L3", "label": "240·480일선 동시 거래량 돌파",
     "desc": f"최근 {P.breakout_days}일 안에 240일선과 480일선을 모두 아래→위로 돌파, 각 돌파일 거래량이 직전 20일 평균의 {P.vol_mult:g}배 이상"},
    {"id": "L4", "label": "신고가 후 240일선 지지 → 전고점 향해 반등",
     "desc": (f"52주 신고가(받아 둔 3년치 자료 안에서 최고가면 '3년 내 최고가'로 표시)를 찍고 -{int(rules2.PEAK_DRAWDOWN * 100)}% 이상 조정, 조정 중 240일선 지지, "
              f"저점 대비 +{int(rules2.D_REBOUND * 100)}% 이상 반등해 전고점 아래에서 상승 중이며 최근 5일 종가가 20일선을 이탈하지 않음")},
]
SWING_RULES = [
    {"id": "S1", "label": "상한가 후 조정 → 20일선 반등",
     "desc": f"최근 {rules2.LU_LOOKBACK[20]}거래일 안에 상한가, 고점 대비 -{int(rules2.MIN_DRAWDOWN * 100)}% 이상 조정 후 최근 5일 안에 20일선까지 내려왔다가 오늘 20일선 위에서 상승 마감 (국내만)"},
    {"id": "S2", "label": "상한가 후 조정 → 60일선 반등",
     "desc": f"최근 {rules2.LU_LOOKBACK[60]}거래일 안에 상한가, 고점 대비 -{int(rules2.MIN_DRAWDOWN * 100)}% 이상 조정 후 최근 5일 안에 60일선까지 내려왔다가 오늘 60일선 위에서 상승 마감 (국내만)"},
    {"id": "S3", "label": "급등 후 10일 이상 조정, 10일선 지지",
     "desc": f"20일 안에 +{int(rules2.SURGE_PCT * 100)}% 이상 급등, 고점 이후 {rules2.C_MIN_DAYS}거래일 이상 조정, 종가가 10일선 ±{int(rules2.C_NEAR * 100)}% 이내에서 지지"},
    {"id": "S4", "label": "급등 후 거래량 감소, 20일선 지지",
     "desc": f"급등 후 최근 5일 평균 거래량이 급등 막바지의 {int(rules2.D_VOL_RATIO * 100)}% 이하로 줄고, 상승 중인 20일선에서 지지"},
    {"id": "S5", "label": "외국인·기관 지속 유입 + 10일선 위 상승",
     "desc": (f"최근 {rules2.E_HOLD_DAYS}거래일 종가가 10일선을 이탈하지 않고 +{int(rules2.E_MIN_GAIN * 100)}% 이상 상승, "
              f"최근 {rules2.E_FLOW_DAYS}거래일 중 {rules2.E_FLOW_POS}일 이상 외국인+기관 합계 순매수이고 누적 {rules2.E_FLOW_MIN / 1e8:g}억 원 이상 (국내만, 수급은 네이버 공개분까지)")},
]
BREAK_SUBTYPES = [
    {"id": "B1", "name": "전고점 돌파 + 거래량 동반 장대양봉",
     "desc": (f"52주 신고가(3년치 자료 안에서 최고가면 '3년 내 최고가')를 찍고 -{int(rules2.PEAK_DRAWDOWN * 100)}% 이상 하락했던 전고점을 최근 {rules2.B_BREAK_DAYS}일 안에 종가로 돌파, "
              f"돌파일 몸통 +{rules2.B1_BODY_PCT:g}% 이상·거래량 20일 평균의 {rules2.B1_VOL_MULT:g}배 이상")},
    {"id": "B2", "name": "전고점 돌파 + 장기 이평선 지지",
     "desc": "같은 전고점 돌파 종목 중, 조정 구간에서 240일선 또는 480일선 지지를 받았던 종목"},
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
    tags, kr_rank = {}, {}
    if market == "us":   # 지수에 없어도 국내 투자자 관심이 큰 테마 종목(theme_map.json 의 미국 종목)을 스캔 대상에 추가
        try:
            import pandas as pd
            with open(os.path.join(HERE, "theme_map.json"), encoding="utf-8") as f:
                themes = json.load(f)["themes"]
            kr_name = {}
            for t in themes:
                for s in t.get("us", []):
                    c = s["ticker"].replace(".", "-")
                    kr_name.setdefault(c, s["name"])
                    tags.setdefault(c, []).append(t["name"])
            try:   # 서학개미 보관금액·순매수 상위 종목 (ETF 제외)
                import seohak
                sh = seohak.load() or {}
                more = seohak.kr_names()
                for key, label in (("hold", "보관"), ("netbuy", "순매수")):
                    for x in sh.get(key, []):
                        if x.get("ticker") and not x.get("etf"):
                            kr_name.setdefault(x["ticker"], more.get(x["ticker"]) or x["name"].title())
                            kr_rank.setdefault(x["ticker"], f"서학개미 {label} {x['rank']}위")
            except Exception as e:
                print("서학개미 종목 추가 실패:", type(e).__name__, e)
            extra = [c for c in kr_name if c not in set(uni["code"])]
            if not limit:
                uni = pd.concat([uni, pd.DataFrame({"code": extra, "name": [kr_name[c] for c in extra]})], ignore_index=True)
            uni["name"] = [kr_name.get(c, n) for c, n in zip(uni["code"], uni["name"])]
            print(f"관심 테마 종목 {len(kr_name)}개 (지수 밖 {len(extra)}개 추가) → 스캔 대상 {len(uni)}개")
        except Exception as e:
            print("관심 테마 종목 추가 실패:", type(e).__name__, e)
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

    sectors = {}
    if market == "kr":
        try:
            with open(os.path.join(OUT, "kr_sector.json"), encoding="utf-8") as f:
                sectors = json.load(f).get("map", {})
        except Exception:
            pass

    def make_item(code, df, ind_df):
        ind = ind_df.iloc[-1]
        prev = float(df["close"].iloc[-2]) if len(df) > 1 else 0.0
        last = float(df["close"].iloc[-1])
        m = meta.get(code, {})
        return {
            "_d": df.index[-1].strftime("%Y-%m-%d"),
            "code": code, "name": names.get(code, code),
            "market": m.get("market", ""), "sector": m.get("sector", "") or sectors.get(code, ""), "marcap": m.get("marcap", 0),
            "themes": tags.get(code, [])[:2], "krRank": kr_rank.get(code, ""),
            "prevClose": _r(prev), "changePct": _r((last / prev - 1) * 100) if prev else None,
            "value": round(last * float(df["volume"].iloc[-1]) / 1e8) if market == "kr" else None,
            "close": _r(ind["close"]), "ma10": _r(ind["ma10"]), "ma20": _r(ind["ma20"]), "ma60": _r(ind["ma60"]),
            "ma240": _r(ind["ma240"]), "ma480": _r(ind["ma480"]),
        }

    items, swing, breaks, e_cands, scanned, as_of = [], [], [], [], 0, ""
    base = {}
    hist = {}      # 테마 순환매 계산용: 최근 33일의 (종가, 거래대금)
    for code, df in gen:
        scanned += 1
        as_of = max(as_of, df.index[-1].strftime("%Y-%m-%d"))
        value20 = (df["close"] * df["volume"]).tail(20).mean()
        if market == "kr":
            t = df.tail(33)
            hist[code] = {"name": names.get(code, code),
                          "bars": {d.strftime("%Y-%m-%d"): (float(c), float(c) * float(v)) for d, c, v in zip(t.index, t["close"], t["volume"])}}
        if market == "kr" and value20 >= 5e8:   # 종가배팅주(5장 A) 판정용 기준값
            try:
                bf = closing.base_features(df)
                if bf:
                    base[code] = bf
            except Exception:
                pass
        if value20 < min_value or len(df) < 30:
            continue
        ind_df = add_indicators(df)
        # ── 중장기: a=L1, b=L2, c=L3(240·480 동시 돌파), d=L4(신고가 후 240일선 지지 반등) ──
        old = evaluate(df, P)
        hits, notes = {}, []
        for k in ("L1", "L2"):
            if k in old:
                hits[k] = old[k]
                notes.append(NOTE_FMT[k](old[k]))
        if "L3a" in old and "L3b" in old:
            hits["L3"] = {"a": old["L3a"], "b": old["L3b"]}
            notes.append(rules2.LONG_NOTE["L3"](hits["L3"]))
        try:
            r = rules2.long_d(ind_df)
            if r:
                hits["L4"] = r
                notes.append(rules2.LONG_NOTE["L4"](r))
        except Exception:
            pass
        if hits:
            items.append(dict(make_item(code, df, ind_df), matched=list(hits.keys()), note=" / ".join(notes)))
        # ── 스윙: A~D 는 가격만으로, E 는 수급 확인이 필요해 후보로 모아 둠 ──
        try:
            sw = rules2.evaluate_swing(ind_df, market)
            if sw:
                swing.append(dict(make_item(code, df, ind_df), matched=list(sw.keys()),
                                  note=" / ".join(rules2.SWING_NOTE[k](v) for k, v in sw.items())))
            if market == "kr":
                ep = rules2.swing_e_price(ind_df)
                if ep:
                    e_cands.append((float(value20), code, make_item(code, df, ind_df), ep))
                bo = rules2.breakout(ind_df)
                for k, v in bo.items():
                    breaks.append(dict(make_item(code, df, ind_df), sub=k, note=rules2.BREAK_NOTE[k](v), _vol=v.get("vol", 0), _over=v.get("over", 0)))
        except Exception as e:
            print("새 규칙 판정 오류:", code, type(e).__name__, e)

    if market == "kr" and e_cands:      # 스윙 E: 가격 조건을 통과한 종목만 외국인·기관 수급 확인
        try:
            import naver_live
            e_cands.sort(key=lambda x: -x[0])
            top = e_cands[:400]
            flows = naver_live.fetch_flow_histories([c for _, c, _, _ in top])
            by_code = {x["code"]: x for x in swing}
            n_e = 0
            for _, code, item, ep in top:
                fl = rules2.flow_ok(flows.get(code) or [])
                if not fl:
                    continue
                n_e += 1
                note = rules2.SWING_NOTE["S5"](dict(ep, **fl))
                if code in by_code:
                    by_code[code]["matched"].append("S5")
                    by_code[code]["note"] += " / " + note
                else:
                    swing.append(dict(item, matched=["S5"], note=note))
            print(f"스윙 E: 가격 후보 {len(e_cands)}개 중 {len(top)}개 수급 확인 → {n_e}개 충족")
        except Exception as e:
            print("스윙 E 수급 확인 실패:", type(e).__name__, e)

    def fresh(rows):
        late = [x["code"] for x in rows if x["_d"] < as_of]
        if late:
            print(f"기준일({as_of})보다 시세가 오래된 종목 {len(late)}개 제외: {late[:10]}")
        return [{k: v for k, v in x.items() if k != "_d"} for x in rows if x["_d"] >= as_of]
    items, swing, breaks = fresh(items), fresh(swing), fresh(breaks)
    items.sort(key=lambda x: (-len(x["matched"]), x["name"]))
    swing.sort(key=lambda x: (-len(x["matched"]), x["matched"][0], x["name"]))
    if market == "kr":
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, "kr_meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, separators=(",", ":"))
        cb = os.path.join(OUT, "closing_base_kr.json")
        try:   # 마감 후 판정(수급 반영)에 '어제까지의 기준'이 필요하므로, 날짜가 바뀔 때 직전 파일을 보관
            with open(cb, encoding="utf-8") as f:
                old_asof = json.load(f).get("asOf", "")
            if old_asof and old_asof < as_of:
                os.replace(cb, os.path.join(OUT, "closing_base_kr_prev.json"))
        except Exception:
            pass
        with open(cb, "w", encoding="utf-8") as f:
            json.dump({"asOf": as_of, "base": base}, f, ensure_ascii=False, separators=(",", ":"))
        try:
            write_rotation(hist, as_of)
        except Exception as e:
            print("테마 순환매 계산 실패:", type(e).__name__, e)
        try:      # 단기 유형 B(전고점 돌파): 세부 유형별로 정리해 저장하고 단기 탭 파일을 다시 만든다
            import shortterm_build
            subs = []
            for st in BREAK_SUBTYPES:
                rows = sorted([x for x in breaks if x["sub"] == st["id"]], key=lambda x: (-x["_vol"], -x["_over"]))[:20]
                subs.append(dict(st, kr=[{k: v for k, v in x.items() if k not in ("sub", "_vol", "_over")} for x in rows]))
            with open(os.path.join(OUT, "breakout_kr.json"), "w", encoding="utf-8") as f:
                json.dump({"asOf": as_of, "subtypes": subs}, f, ensure_ascii=False)
            shortterm_build.build()
            print("전고점 돌파:", {x["id"]: len(x["kr"]) for x in subs})
        except Exception as e:
            print("전고점 돌파 저장 실패:", type(e).__name__, e)
    return {"asOf": as_of, "scanned": scanned, "items": items, "swing": swing}


def write_rotation(hist, as_of):
    """네이버 테마 구성종목 + 일봉으로 테마 순환매 자료(data/rotation.js)를 만든다."""
    import naver_themes
    import rotation
    mpath = os.path.join(OUT, "theme_members.json")
    try:
        themes = naver_themes.fetch_all_members()
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump(themes, f, ensure_ascii=False, separators=(",", ":"))
    except Exception as e:      # 네이버가 막히면 지난번에 받아 둔 구성종목을 씀
        print("테마 구성종목 수집 실패(지난 자료 사용):", type(e).__name__, e)
        with open(mpath, encoding="utf-8") as f:
            themes = json.load(f)
    res = rotation.build(hist, themes)
    if not res:
        print("테마 순환매: 계산할 자료 부족")
        return
    res["asOf"] = as_of
    with open(os.path.join(HERE, "..", "data", "rotation.js"), "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/run_scan.py → rotation.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.rotation = ")
        json.dump(res, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"테마 순환매: 테마 {res['themeCount']}개, 기준일 {as_of}")


def build_js():
    def load(m):
        path = os.path.join(OUT, f"longterm_{m}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {"asOf": "", "scanned": 0, "items": []}

    kr, us = load("kr"), load("us")
    valid = {r["id"] for r in RULES}      # 규칙 개편 전 결과 파일에 남아 있는 예전 규칙(L3a·L3b)은 화면에서 뺀다
    for d in (kr, us):
        d["items"] = [dict(x, matched=[m for m in x["matched"] if m in valid]) for x in d.get("items", [])]
        d["items"] = [x for x in d["items"] if x["matched"]]
    payload = {
        "swingRules": SWING_RULES,
        "swing": {"kr": kr.get("swing", []), "us": us.get("swing", [])},
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
