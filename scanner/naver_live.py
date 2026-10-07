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

# 참고: /api/stock/{code}/trend (외국인·기관 순매수)는 장이 끝난 뒤에야 당일 값이 들어온다 → 장중에는 None
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
    if exclude_etf and str(r.get("stockEndType") or "stock") != "stock":   # ETF·ETN 등
        return None
    price = num(r.get("closePriceRaw")) or num(r.get("closePrice"))
    volume = num(r.get("accumulatedTradingVolumeRaw")) or num(r.get("accumulatedTradingVolume"))
    if not price or not volume:
        return None
    pct = num(r.get("fluctuationsRatioRaw"))
    if pct is None:
        pct = num(r.get("fluctuationsRatio"))
    out = {"code": code, "name": name, "price": price, "volume": volume, "pct": pct}
    chg = num(r.get("compareToPreviousClosePriceRaw"))
    if chg is None:
        chg = num(r.get("compareToPreviousClosePrice"))
    if chg is not None:
        out["prev"] = price - chg                      # 네이버 화면과 같은 전일종가
        if pct is None and out["prev"] > 0:
            out["pct"] = chg / out["prev"] * 100
    val = num(r.get("accumulatedTradingValueRaw"))     # 원 단위 거래대금
    out["value"] = val if val else price * volume
    cap = num(r.get("marketValueRaw"))                 # 원 단위 시가총액
    if cap:
        out["marcap"] = cap
    out["day"] = str(r.get("localTradedAt") or "")[:10]   # 마지막 체결일 (휴장일 판별용)
    return out


SAMPLE = {}   # 진단용: 시장별 원본 앞 3행


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
            if p == 1:
                SAMPLE[mk] = rows[:3]
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


def parse_flow_detail(payload, price, today=None):
    """trend 응답 → {"sum", "f"(외국인), "o"(기관)} 순매수 대금(원). 오늘 자료가 없으면 None."""
    rows = payload if isinstance(payload, list) else (payload or {}).get("trends") or (payload or {}).get("items") or []
    if not rows:
        return None
    r = sorted(rows, key=lambda x: str(x.get("bizdate") or ""), reverse=True)[0]
    if today and str(r.get("bizdate") or "") != today:
        return None
    f, o = num(r.get("foreignerPureBuyQuant")), num(r.get("organPureBuyQuant"))
    if f is None and o is None:
        return None
    return {"f": (f or 0) * price, "o": (o or 0) * price, "sum": ((f or 0) + (o or 0)) * price}


def fetch_flow(code, price):
    try:
        import datetime as dt
        today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y%m%d")
        return parse_flow_detail(_get(TREND_URL.format(code=code), {"pageSize": 3}), price, today)
    except Exception:
        return None


def fetch_flows(cands, workers=6):
    """cands: {code: price} → {code: {"sum","f","o"} 또는 None}"""
    with ThreadPoolExecutor(workers) as ex:
        return dict(zip(cands, ex.map(lambda c: fetch_flow(c, cands[c]), cands)))


# ───────────── 업종 (종목코드 → 네이버 업종명) ─────────────
IND_LIST_URL = "https://m.stock.naver.com/api/stocks/industry"
IND_MEMBERS_URL = "https://m.stock.naver.com/api/stocks/industry/{no}"


def _rows(payload, *names):
    if isinstance(payload, list):
        return payload
    for n in names:
        v = (payload or {}).get(n)
        if isinstance(v, list):
            return v
    return []


def fetch_industries(workers=6):
    """{종목코드: 업종명}. 네이버 업종 목록과 구성종목으로 만든다. 실패하면 예외."""
    groups = []
    for p in range(1, 4):
        rows = _rows(_get(IND_LIST_URL, {"page": p, "pageSize": 100}), "groups", "industries", "result")
        if not rows:
            break
        groups += rows
        if len(rows) < 100:
            break
    SAMPLE["industryGroups"] = groups[:2]
    groups = [g for g in groups if g.get("no") is not None and g.get("name")]
    if not groups:
        raise ValueError("업종 목록이 비어 있음")

    def one(g):
        codes = []
        try:
            for p in range(1, 8):
                rows = _rows(_get(IND_MEMBERS_URL.format(no=g["no"]), {"page": p, "pageSize": 100}), "stocks", "result")
                codes += [str(r.get("itemCode")) for r in rows if r.get("itemCode")]
                if len(rows) < 100:
                    break
        except Exception:
            pass
        return str(g["name"]), codes

    out = {}
    with ThreadPoolExecutor(workers) as ex:
        for name, codes in ex.map(one, groups):
            for c in codes:
                out.setdefault(c, name)
    if len(out) < 500:
        raise ValueError(f"업종 구성종목이 {len(out)}개뿐")
    return out


def parse_flow_history(payload, n=6):
    """trend 응답 → 최근 날짜부터 [{"date": "MM/DD", "f": 외국인 순매수 대금, "o": 기관 순매수 대금}] (그날 종가 × 수량)."""
    rows = payload if isinstance(payload, list) else (payload or {}).get("trends") or (payload or {}).get("items") or []
    out = []
    for r in sorted(rows, key=lambda x: str(x.get("bizdate") or ""), reverse=True)[:n]:
        d, price = str(r.get("bizdate") or ""), num(r.get("closePrice"))
        f, o = num(r.get("foreignerPureBuyQuant")), num(r.get("organPureBuyQuant"))
        if len(d) != 8 or not price or (f is None and o is None):
            continue
        out.append({"date": d[4:6] + "/" + d[6:8], "f": (f or 0) * price, "o": (o or 0) * price})
    return out


def fetch_flow_histories(codes, workers=6):
    """{code: 최근 수급 이력}. 실패한 종목은 빈 목록."""
    def one(c):
        try:
            return parse_flow_history(_get(TREND_URL.format(code=c), {"pageSize": 10}, tries=2))
        except Exception:
            return []
    with ThreadPoolExecutor(workers) as ex:
        return dict(zip(codes, ex.map(one, codes)))
