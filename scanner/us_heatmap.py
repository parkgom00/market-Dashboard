"""미국 히트맵 자료: 나스닥 공식 스크리너(api.nasdaq.com, 키 불필요)에서 종목별 시가총액·등락률을 받아
S&P 500 구성종목 중 시가총액 상위 종목만 골라 저장합니다. (화면에서 시총 크기 = 네모 크기, 등락률 = 색)
"""
import json
import re
import time
import urllib.request

URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&download=true"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
           "Accept": "application/json"}
TOP_N = 100
SECTOR_KR = {
    # S&P(GICS) 분류
    "Information Technology": "기술", "Communication Services": "커뮤니케이션", "Consumer Discretionary": "경기소비재",
    "Consumer Staples": "필수소비재", "Health Care": "헬스케어", "Financials": "금융", "Industrials": "산업재",
    "Energy": "에너지", "Utilities": "유틸리티", "Real Estate": "부동산", "Materials": "소재",
    # 나스닥 자체 분류 (S&P 분류를 못 받았을 때)
    "Technology": "기술", "Finance": "금융", "Telecommunications": "커뮤니케이션", "Basic Materials": "소재",
    "Miscellaneous": "기타",
}
NAME_CUT = re.compile(r"\s+(Common Stock|Class [A-Z]\b|Ordinary Shares|American Depositary|Depositary Shares|Capital Stock|\(.*\)).*$", re.I)
DUP_DROP = {"GOOG": "GOOGL", "FOX": "FOXA", "NWS": "NWSA", "BRK/A": "BRK/B"}   # 같은 회사의 다른 주식 종류


def _num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[$,%\s]", "", str(v))
    if s in ("", "NA", "N/A", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def key(sym):
    return re.sub(r"[^A-Z0-9]", "", str(sym).upper())


def fetch_rows(tries=3):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL, headers=HEADERS), timeout=40) as r:
                d = json.loads(r.read().decode()).get("data") or {}
            rows = d.get("rows") or (d.get("table") or {}).get("rows") or []
            if rows:
                return rows
            last = ValueError("빈 응답")
        except Exception as e:
            last = e
        time.sleep(2 * (i + 1))
    raise last


def parse_rows(rows):
    out = []
    for r in rows:
        sym = str(r.get("symbol") or "").strip()
        cap, pct = _num(r.get("marketCap")), _num(r.get("pctchange"))
        if not sym or not cap or cap <= 0 or pct is None:
            continue
        out.append({"t": sym, "n": NAME_CUT.sub("", str(r.get("name") or sym)).strip(), "cap": cap, "p": pct,
                    "sec": str(r.get("sector") or "").strip(), "price": _num(r.get("lastsale"))})
    return out


def sp500_members():
    """{정규화한 티커: GICS 섹터}. 실패하면 빈 dict (그 경우 전체 미국 상장 종목 중 시총 상위를 씀)."""
    try:
        import FinanceDataReader as fdr
        lst = fdr.StockListing("S&P500")
        col = "Sector" if "Sector" in lst.columns else None
        return {key(s): (str(sec) if col else "") for s, sec in zip(lst["Symbol"], lst[col] if col else [""] * len(lst))}
    except Exception as e:
        print("S&P 500 목록 실패:", type(e).__name__, e)
        return {}


def build(parsed, members, top_n=TOP_N):
    have = {x["t"] for x in parsed}
    items = []
    for x in parsed:
        if x["t"] in DUP_DROP and DUP_DROP[x["t"]] in have:
            continue
        if members and key(x["t"]) not in members:
            continue
        sec = (members.get(key(x["t"])) if members else "") or x["sec"]
        items.append({"t": x["t"].replace("/", "."), "n": x["n"], "s": SECTOR_KR.get(sec, sec or "기타"),
                      "c": round(x["cap"] / 1e9, 1), "p": round(x["p"], 2)})
    items.sort(key=lambda i: -i["c"])
    return items[:top_n]


def apply_changes(items, changes, date):
    """등락률을 야후 종가 기준 값으로 바꾼다. 나스닥 스크리너의 등락률은 하루 늦게 갱신되는 경우가 있어 쓰지 않는다.
    changes: {야후 티커: {"pct", "date"}}. 기준일(date) 종가가 없는 종목은 뺀다."""
    out = []
    for it in items:
        ch = changes.get(it["t"].replace(".", "-"))
        if ch and ch["date"] >= date:
            out.append(dict(it, p=round(ch["pct"], 2)))
    return out


def collect(parsed=None):
    if parsed is None:
        parsed = parse_rows(fetch_rows())
    members = sp500_members()
    items = build(parsed, members)
    if len(items) < 30:
        raise ValueError(f"히트맵 종목이 {len(items)}개뿐")
    return {"source": ("S&P 500 시총 상위" if members else "미국 상장 시총 상위") + " · 시총 Nasdaq, 등락률 Yahoo 종가", "items": items}
