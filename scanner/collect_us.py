"""미국 시세 수집: 3대 지수, 테마별 등락 → 미국장 탭(data/usmarket.js)과 특징주 탭의 미국 테마.

yfinance 의 일봉(마지막 종가 vs 직전 종가)으로 계산합니다. 미국 정규장 마감 후에 실행하세요.
이슈 요약 문장은 scanner/out/us_summary.json (AI 요약 단계)이 있고 날짜가 맞을 때만 포함됩니다.
"""
import json
import os
from datetime import datetime, timedelta, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA = os.path.join(HERE, "..", "data")
KST = timezone(timedelta(hours=9))
DOW = ["월", "화", "수", "목", "금", "토", "일"]

from us_assets import INDICES as ASSET_INDICES, SECTORS, MAIN_INDICES

INDICES = [(a["name"], a["symbol"]) for a in ASSET_INDICES]


def compute_changes(closes: pd.DataFrame) -> dict:
    """종가 표(열=티커) → {티커: {"close", "pct", "date"}} (마지막 종가 vs 직전 종가)."""
    out = {}
    for t in closes.columns:
        s = closes[t].dropna()
        if len(s) < 2 or s.iloc[-2] == 0:
            continue
        out[str(t)] = {
            "close": float(s.iloc[-1]),
            "pct": float((s.iloc[-1] / s.iloc[-2] - 1) * 100),
            "date": pd.Timestamp(s.index[-1]).strftime("%Y-%m-%d"),
            "diff": float(s.iloc[-1] - s.iloc[-2]),
        }
    return out


def build_us_themes(changes: dict, themes: list, top_n: int = 5, hot_pct: float = 1.0, min_stocks: int = 2):
    """미국 종목이 있는 테마만 평균 등락률로 정렬. 평균 +hot_pct% 이상인 테마만(없으면 상위 3개)."""
    rows = []
    for t in themes:
        us = [(s, changes[s["ticker"]]) for s in t.get("us", []) if s["ticker"] in changes]
        if len(us) < min_stocks:
            continue
        avg = sum(c["pct"] for _, c in us) / len(us)
        us.sort(key=lambda x: -x[1]["pct"])
        rows.append({
            "name": t["name"],
            "changePct": round(avg, 2),
            "why": "",
            "usStocks": [{"ticker": s["ticker"], "name": s["name"], "changePct": round(c["pct"], 2)} for s, c in us[:4]],
            "krStocks": [{"code": k["code"], "name": k["name"], "link": k.get("link", "")} for k in t.get("kr", [])[:3]],
        })
    rows.sort(key=lambda r: -r["changePct"])
    hot = [r for r in rows if r["changePct"] >= hot_pct][:top_n]
    return hot if hot else rows[:3]


def theme_strength_us(changes: dict, themes: list, min_stocks: int = 2):
    out = []
    for t in themes:
        stocks = [{"name": s["name"], "changePct": round(changes[s["ticker"]]["pct"], 2)} for s in t.get("us", []) if s["ticker"] in changes]
        if len(stocks) >= min_stocks:
            out.append({"name": t["name"], "stocks": stocks})
    return out


def as_of_text(date_str: str) -> str:
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{date_str} ({DOW[d.weekday()]}) 미국 정규장 기준"


def load_summary(for_date: str):
    path = os.path.join(OUT, "us_summary.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            s = json.load(f)
        if s.get("forDate") == for_date:
            return s.get("lines", [])
    return []


def index_text(a, ch):
    """화면·AI 입력용 한 줄 (금리는 bp, 나머지는 %)."""
    if a["kind"] == "yield":
        return f"{ch['close']:.2f}% ({ch['diff'] * 100:+.1f}bp)"
    return f"{ch['close']:,.2f} ({ch['pct']:+.2f}%)"


def build_indices(changes: dict) -> list:
    out = []
    for a in ASSET_INDICES:
        ch = changes.get(a["symbol"])
        if not ch:
            continue
        row = {"group": a["group"], "name": a["name"], "kind": a["kind"], "close": round(ch["close"], 2),
               "changePct": round(ch["pct"], 2), "changeText": index_text(a, ch)}
        if a["kind"] == "yield":
            row["changeBp"] = round(ch["diff"] * 100, 1)
        out.append(row)
    return out


def build_sectors(changes: dict) -> list:
    return [{"group": s["group"], "name": s["name"], "symbol": s["symbol"], "kr": s.get("kr", ""),
             "changePct": round(changes[s["symbol"]]["pct"], 2)} for s in SECTORS if s["symbol"] in changes]


def load_brief(for_date: str):
    path = os.path.join(OUT, "us_brief.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                b = json.load(f)
            if b.get("forDate") == for_date:
                return b
        except ValueError:
            pass
    return None


def build_payload(all_changes: dict, th_changes: dict, themes: list) -> dict:
    """all_changes: 지수·업종·원자재 등 모든 심볼의 변화, th_changes: 테마 종목."""
    main = [t for t in MAIN_INDICES if t in all_changes]
    date = max((all_changes[t]["date"] for t in main), default="")
    brief = load_brief(date) if date else None
    return {
        "asOf": as_of_text(date) if date else "",
        "forDate": date,
        "indices": build_indices(all_changes),
        "sectors": build_sectors(all_changes),
        "summary": load_summary(date) if date else [],
        "brief": brief,
        "themes": build_us_themes(th_changes, themes),
    }


def kr_hint_lines(themes):
    out = []
    for t in themes:
        us = ", ".join(s["ticker"] for s in t.get("us", []))
        kr = ", ".join(k["name"] for k in t.get("kr", []))
        if us and kr:
            out.append(f"{t['name']}: 미국 {us} ↔ 국내 {kr}")
    return out


def ensure_brief(payload, themes):
    """AI 브리핑이 없으면 만들어 out/us_brief.json 에 저장하고 payload 에 넣음. 실패해도 나머지는 그대로."""
    if payload.get("brief") or not payload["forDate"]:
        return
    import gemini
    import us_brief
    if not gemini.api_key():
        print("GEMINI_API_KEY 없음: AI 브리핑 건너뜀")
        return
    def gen(prompt, system, search):
        return gemini.generate(prompt, system=system, search=search, want_json=True, max_tokens=16384)
    try:
        brief = us_brief.generate_brief(payload["forDate"], payload["indices"], payload["sectors"], kr_hint_lines(themes), gen)
    except Exception as e:
        print("경고: AI 브리핑 실패 (다음 실행에 재시도):", e)
        return
    tickers = sorted({c["usTicker"] for c in brief["connections"]})
    pct = {}
    if tickers:
        try:
            import yfinance as yf
            closes = yf.download(tickers, period="15d", auto_adjust=True, progress=False)["Close"]
            if hasattr(closes, "to_frame") and not hasattr(closes, "columns"):
                closes = closes.to_frame(tickers[0])
            pct = {t: c["pct"] for t, c in compute_changes(closes).items()}
        except Exception as e:
            print("경고: 연결 종목 시세 조회 실패:", e)
    us_brief.fill_changes(brief, pct)
    us_brief.fill_sector_changes(brief, payload["sectors"])
    names_path = os.path.join(OUT, "kr_names.json")
    if os.path.exists(names_path):
        try:
            n_before = len(brief["connections"])
            us_brief.validate_picks(brief, json.load(open(names_path, encoding="utf-8")))
            print(f"국내 종목명 검증: 연결 {n_before}개 → {len(brief['connections'])}개")
        except Exception as e:
            print("경고: 국내 종목명 검증 건너뜀:", e)
    stored = dict(brief, forDate=payload["forDate"], generatedAt=datetime.now(KST).strftime("%Y-%m-%d %H:%M"))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "us_brief.json"), "w", encoding="utf-8") as f:
        json.dump(stored, f, ensure_ascii=False, indent=1)
    payload["brief"] = stored
    print("AI 브리핑 생성 완료")


def main():
    import yfinance as yf
    import build_live

    with open(os.path.join(HERE, "theme_map.json"), encoding="utf-8") as f:
        themes = json.load(f)["themes"]
    th_tickers = sorted({s["ticker"] for t in themes for s in t.get("us", [])})
    asset_symbols = sorted({a["symbol"] for a in ASSET_INDICES} | {s["symbol"] for s in SECTORS})

    allc = yf.download(asset_symbols, period="15d", auto_adjust=True, progress=False)["Close"]
    th = yf.download(th_tickers, period="15d", auto_adjust=True, progress=False)["Close"]
    all_changes = compute_changes(allc)
    payload = build_payload(all_changes, compute_changes(th), themes)
    if not [i for i in payload["indices"] if i["name"] in ("나스닥", "S&P 500", "다우")]:
        raise SystemExit("지수 데이터를 받지 못했습니다. (기존 파일은 그대로 둡니다)")
    ensure_brief(payload, themes)

    with open(os.path.join(DATA, "usmarket.js"), "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/collect_us.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.usmarket = ")
        json.dump({k: v for k, v in payload.items() if k != "forDate"}, f, ensure_ascii=False, indent=1)
        f.write(";\n")

    os.makedirs(OUT, exist_ok=True)
    stamp = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(OUT, "live_themes_us.json"), "w", encoding="utf-8") as f:
        json.dump({"asOf": stamp, "themes": theme_strength_us(compute_changes(th), themes)}, f, ensure_ascii=False)
    build_live.build()
    print(f"[미국] 기준 {payload['asOf']}, 지수 {len(payload['indices'])}개, 업종 {len(payload['sectors'])}개, 테마 {len(payload['themes'])}개, AI {'있음' if payload['brief'] else '없음'}")


if __name__ == "__main__":
    main()
