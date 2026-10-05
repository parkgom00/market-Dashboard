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

INDICES = [("나스닥", "^IXIC"), ("S&P 500", "^GSPC"), ("다우", "^DJI")]


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


def build_payload(idx_changes: dict, th_changes: dict, themes: list) -> dict:
    indices = [{"name": n, "close": round(idx_changes[t]["close"], 2), "changePct": round(idx_changes[t]["pct"], 2)}
               for n, t in INDICES if t in idx_changes]
    date = max((idx_changes[t]["date"] for _, t in INDICES if t in idx_changes), default="")
    return {
        "asOf": as_of_text(date) if date else "",
        "forDate": date,
        "indices": indices,
        "summary": load_summary(date) if date else [],
        "themes": build_us_themes(th_changes, themes),
    }


def main():
    import yfinance as yf
    import build_live

    with open(os.path.join(HERE, "theme_map.json"), encoding="utf-8") as f:
        themes = json.load(f)["themes"]
    tickers = sorted({s["ticker"] for t in themes for s in t.get("us", [])})

    idx = yf.download([t for _, t in INDICES], period="15d", auto_adjust=True, progress=False)["Close"]
    th = yf.download(tickers, period="15d", auto_adjust=True, progress=False)["Close"]
    payload = build_payload(compute_changes(idx), compute_changes(th), themes)
    if not payload["indices"]:
        raise SystemExit("지수 데이터를 받지 못했습니다. (기존 파일은 그대로 둡니다)")

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
    print(f"[미국] 기준 {payload['asOf']}, 테마 {len(payload['themes'])}개")


if __name__ == "__main__":
    main()
