"""네이버 증권 모바일의 실시간 시세 (키 불필요, 비공식 주소 — 바뀌면 실패할 수 있음).

- fetch_universe(): 시가총액순 전 종목의 현재가·거래량 (장중에도 갱신됨. KRX 시세표는 장중에 비어 있는 경우가 있음)
- fetch_flow(code): 오늘 외국인·기관 순매수(잠정, 주수)
"""
import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
           "Accept": "application/json", "Referer": "https://m.stock.naver.com/"}
MV_URL = "https://m.stock.naver.com/api/stocks/marketValue/{mk}"
TREND_URL = "https://m.stock.naver.com/api/stock/{code}/trend"
BAD_NAME = re.compile(r"(스팩|SPAC|리츠)", re.I)
ETF_WORD = re.compile(r"(ETN|ETF)", re.I)
ETF_BRAND = re.compile(r"^(KODEX|TIGER|ACE|RISE|SOL|KBSTAR|ARIRANG|HANARO|PLUS|KOSEF|TIMEFOLIO|WON|1Q|마이티|히어로즈|KIWOOM|BNK|UNICORN|FOCUS|HK|TRUSTON|VITA|파워|에셋플러스|대신|메리츠)\s", re.I)


def _get(url, params=None, tries=3):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
            time.sleep(0.8 * (i + 1))
    raise last


def num(v):
    """'70,000' / '+1,234' / 1234 / None → float 또는 None"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "").replace("+", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def parse_row(r, exclude_etf=True):
    """네이버 한 종목 행 → {code,name,price,volume,pct} 또는 None (보통주가 아니면 None)."""
    code = str(r.get("itemCode") or "")
    name = str(r.get("stockName") or "")
    if not re.fullmatch(r"\d{5}0", code) or BAD_NAME.search(name) or (exclude_etf and (ETF_BRAND.match(name) or ETF_WORD.search(name))):   # 우선주(끝자리≠0)·스팩·ETF 제외
        return None
    price = num(r.get("closePriceRaw")) or num(r.get("closePrice"))
    volume = num(r.get("accumulatedTradingVolumeRaw")) or num(r.get("accumulatedTradingVolume"))
    if not price or not volume:
        return None
    pct = num(r.get("fluctuationsRatioRaw"))
    if pct is None:
        pct = num(r.get("fluctuationsRatio"))
    return {"code": code, "name": name, "price": price, "volume": volume, "pct": pct}


def fetch_universe(max_pages=30, exclude_etf=True):
    out, keys = {}, []
    for mk in ("KOSPI", "KOSDAQ"):
        for p in range(1, max_pages + 1):
            try:
                rows = (_get(MV_URL.format(mk=mk), {"page": p, "pageSize": 100}) or {}).get("stocks") or []
            except Exception:
                if p == 1:
                    raise
                break
            if not rows:
                break
            if not keys:
                keys = sorted(rows[0].keys())
            for r in rows:
                q = parse_row(r, exclude_etf)
                if q:
                    q["market"] = mk
                    out[q["code"]] = q
    return out, keys


def parse_flow(payload, price, today=None):
    """trend 응답 → 오늘(가장 최근 일자) 외국인+기관 순매수 대금(원). 못 읽으면 None."""
    rows = payload if isinstance(payload, list) else (payload or {}).get("trends") or (payload or {}).get("items") or []
    if not rows:
        return None
    rows = sorted(rows, key=lambda r: str(r.get("bizdate") or ""), reverse=True)
    r = rows[0]
    if today and str(r.get("bizdate") or "") != today:   # 오늘 자료가 아직 없으면 어제 값을 쓰지 않음
        return None
    f = num(r.get("foreignerPureBuyQuant"))
    o = num(r.get("organPureBuyQuant"))
    if f is None and o is None:
        return None
    return ((f or 0) + (o or 0)) * price


def fetch_flow(code, price):
    try:
        import datetime as dt
        today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y%m%d")
        return parse_flow(_get(TREND_URL.format(code=code), {"pageSize": 3}), price, today)
    except Exception:
        return None


def fetch_flows(cands, workers=6):
    """cands: {code: price} → {code: 순매수대금 또는 None}"""
    with ThreadPoolExecutor(workers) as ex:
        return dict(zip(cands, ex.map(lambda c: fetch_flow(c, cands[c]), cands)))
