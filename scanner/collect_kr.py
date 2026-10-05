"""국내 시세 수집: 등락률 상위, 거래대금 상위, 테마별 강약.

FinanceDataReader 의 KRX 전 종목 시세표(StockListing)를 한 번 받아서 계산합니다.
이 표는 KRX 가 제공하는 시점의 값이라 '완전한 실시간'이 아닙니다 (장중에는 지연될 수 있음).
결과는 scanner/out/ 에 저장되고 data/live.js 로 합쳐집니다.
"""
import json
import os
from datetime import datetime, timedelta, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = timezone(timedelta(hours=9))

MIN_AMOUNT = 1e9   # 거래대금 10억 원 미만은 순위에서 제외 (소형 종목의 일시적 급등 제거)
TOP_N = 20


def normalize(raw: pd.DataFrame) -> pd.DataFrame:
    """KRX 시세표 → code, name, market, close, amount, pct 로 정리."""
    cols = {c.lower(): c for c in raw.columns}

    def pick(*names):
        for n in names:
            if n.lower() in cols:
                return cols[n.lower()]
        return None

    code, name, mk = pick("Code", "Symbol"), pick("Name"), pick("Market")
    close, amt = pick("Close"), pick("Amount")
    ratio, chg = pick("ChagesRatio", "ChangesRatio"), pick("Changes")
    if not all([code, name, close, amt]) or not (ratio or chg):
        raise ValueError(f"필요한 컬럼을 찾지 못했습니다. 받은 컬럼: {list(raw.columns)}")

    df = pd.DataFrame({
        "code": raw[code].astype(str).str.zfill(6),
        "name": raw[name].astype(str),
        "market": raw[mk].astype(str) if mk else "",
        "close": pd.to_numeric(raw[close], errors="coerce"),
        "amount": pd.to_numeric(raw[amt], errors="coerce"),
    })
    if ratio:
        df["pct"] = pd.to_numeric(raw[ratio], errors="coerce")
    else:
        changes = pd.to_numeric(raw[chg], errors="coerce")
        df["pct"] = changes / (df["close"] - changes) * 100

    if mk:
        df = df[df["market"].str.upper().str.startswith(("KOSPI", "KOSDAQ"))]
    df = df[(df["close"] > 0) & (df["amount"] > 0) & df["pct"].notna()]
    df = df[~df["name"].str.contains("스팩")]   # 기업인수목적회사 제외
    return df.reset_index(drop=True)


def _row(r, with_value=False):
    out = {"code": r["code"], "name": r["name"], "price": int(r["close"]), "changePct": round(float(r["pct"]), 2)}
    if with_value:
        out["valueEok"] = int(round(r["amount"] / 1e8))
    return out


def top_gainers(df, n=TOP_N, min_amount=MIN_AMOUNT):
    d = df[df["amount"] >= min_amount].sort_values("pct", ascending=False).head(n)
    return [_row(r) for _, r in d.iterrows()]


def top_value(df, n=TOP_N):
    d = df.sort_values("amount", ascending=False).head(n)
    return [_row(r, True) for _, r in d.iterrows()]


def theme_strength(df, themes, min_stocks=2):
    """테마 표의 국내 종목 중 시세표에 있는 종목만 모아 등락률을 붙인다."""
    by_code = df.set_index("code")
    out = []
    for t in themes:
        stocks = []
        for s in t.get("kr", []):
            if s["code"] in by_code.index:
                stocks.append({"name": by_code.loc[s["code"], "name"], "changePct": round(float(by_code.loc[s["code"], "pct"]), 2)})
        if len(stocks) >= min_stocks:
            out.append({"name": t["name"], "stocks": stocks})
    return out


def now_kst():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M")


def load_themes():
    with open(os.path.join(HERE, "theme_map.json"), encoding="utf-8") as f:
        return json.load(f)["themes"]


def main():
    import FinanceDataReader as fdr
    import build_live

    df = normalize(fdr.StockListing("KRX"))
    os.makedirs(OUT, exist_ok=True)
    stamp = now_kst()
    with open(os.path.join(OUT, "live_kr_rank.json"), "w", encoding="utf-8") as f:
        json.dump({"asOf": stamp, "gainers": top_gainers(df), "value": top_value(df)}, f, ensure_ascii=False)
    with open(os.path.join(OUT, "live_themes_kr.json"), "w", encoding="utf-8") as f:
        json.dump({"asOf": stamp, "themes": theme_strength(df, load_themes())}, f, ensure_ascii=False)
    build_live.build()
    print(f"[국내] {len(df)}개 종목 처리, {stamp}")


if __name__ == "__main__":
    main()
