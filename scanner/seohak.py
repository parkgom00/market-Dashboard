"""서학개미(국내 투자자) 미국주식 상위 종목: 한국예탁결제원 세이브로(seibro.or.kr)의 외화증권 종목별 내역 TOP 50.

- 보관금액 상위 50 (국내 투자자가 지금 가장 많이 들고 있는 종목, 달러 기준)
- 최근 1주 순매수 결제 상위 50 (최근에 가장 많이 사들인 종목)
세이브로는 ISIN(국제증권번호)만 주므로 OpenFIGI(무료, 키 불필요)로 티커를 찾고, 실패하면 야후 검색으로 찾습니다.
티커 대응표는 out/isin_ticker.json 에 쌓아 두어 다음부터는 다시 묻지 않습니다.
"""
import datetime as dt
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = dt.timezone(dt.timedelta(hours=9))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
PAGE = "https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/ovsSec/BIP_CNTS10013V.xml&menuNo=921"
SERVLET = "https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp"
TASK = "ksd.safe.bip.cnts.OvsSec.process.OvsSecIsinPTask"
ETF_NAME = re.compile(r"\b(ETF|ETN|ETP|TRUST|PROSHARES|DIREXION|ISHARES|VANGUARD|SPDR|INVESCO|GRANITESHARES|YIELDMAX|T-REX|TRADR|DEFIANCE|ROUNDHILL|SHS ETF|FUND|INDEX)\b", re.I)
NAME_JUNK = re.compile(r"\s+(MRGR|SPLR|SPLT|NMCH)\b.*$|\s+\d{6,}.*$")


def _post(action, params):
    body = (f'<reqParam action="{action}" task="{TASK}"><MENU_NO value="921"/>'
            '<CMM_BTN_ABBR_NM value="total_search,openall,print,hwp,word,pdf,seach,xls,"/>'
            '<W2XPATH value="/IPORTAL/user/ovsSec/BIP_CNTS10013V.xml"/>'
            + "".join(f'<{k} value="{v}"/>' for k, v in params.items()) + "</reqParam>")
    req = urllib.request.Request(SERVLET, data=body.encode("utf-8"),
                                 headers={"User-Agent": UA, "Referer": PAGE, "Origin": "https://seibro.or.kr",
                                          "Content-Type": "application/xml; charset=UTF-8", "Accept": "application/xml"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def parse_rows(xml):
    """세이브로 응답 → [{필드: 값}]"""
    rows = []
    for block in re.findall(r"<data[^>]*>(.*?)</data>", xml, flags=re.S):
        row = dict(re.findall(r'<(\w+) value="([^"]*)"', block))
        if row.get("ISIN"):
            rows.append(row)
    return rows


def clean_name(n):
    import html
    n = NAME_JUNK.sub("", html.unescape(str(n or ""))).strip()
    return re.sub(r"\s+", " ", n)


def kr_names():
    try:
        with open(os.path.join(HERE, "us_names_kr.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load():
    """마지막으로 저장한 결과 (없으면 None)."""
    try:
        with open(os.path.join(OUT, "seohak.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def display_rows(rows, changes=None, date=""):
    """화면용: 한글 이름, 금액, 등락률(기준일 종가가 있는 종목만)."""
    names = kr_names()
    out = []
    for x in rows:
        ch = (changes or {}).get(x["ticker"])
        out.append({"rank": x["rank"], "ticker": x["ticker"], "name": names.get(x["ticker"]) or x["name"].title(),
                    "usd": x["usd"], "etf": x["etf"],
                    "changePct": round(ch["pct"], 2) if ch and ch["date"] >= date else None})
    return out


def is_etf(name, sec_type=""):
    st = sec_type or ""
    return bool(ETF_NAME.search(name or "")) or "ETP" in st or "ETF" in st or "Mutual Fund" in st


def bdays_back(day, n):
    out = []
    d = day
    while len(out) < n:
        d -= dt.timedelta(days=1)
        if d.weekday() < 5:
            out.append(d)
    return out


def fetch_holdings(today, post=_post):
    """보관금액 상위 50 (미국). 최근 영업일부터 거슬러 올라가며 자료가 있는 첫 날을 쓴다. (기준일, rows)"""
    for d in bdays_back(today, 7)[1:]:      # 당일 기준 2영업일 전부터 조회 가능
        ymd = d.strftime("%Y%m%d")
        rows = parse_rows(post("getImptFrcurStkCusRemaList", {"PG_START": 1, "PG_END": 50, "START_DT": ymd, "END_DT": ymd,
                                                              "S_TYPE": 1, "S_COUNTRY": "US"}))
        if rows:
            return d.isoformat(), rows
    return "", []


def fetch_netbuy(today, days=7, post=_post):
    """최근 days일 순매수 결제 상위 50 (미국). (기간 문자열, rows)"""
    end = bdays_back(today, 1)[0]
    start = end - dt.timedelta(days=days - 1)
    rows = parse_rows(post("getImptFrcurStkSetlAmtList", {"PG_START": 1, "PG_END": 50, "START_DT": start.strftime("%Y%m%d"),
                                                         "END_DT": end.strftime("%Y%m%d"), "S_TYPE": 2, "S_COUNTRY": "US", "D_TYPE": 4}))
    return f"{start.isoformat()}~{end.isoformat()}", rows


# ───────────── ISIN → 티커 ─────────────
def figi_lookup(isins):
    """OpenFIGI: {isin: (ticker, securityType)}. 키 없이 한 번에 10건, 분당 25회."""
    out = {}
    for i in range(0, len(isins), 10):
        chunk = isins[i:i + 10]
        body = json.dumps([{"idType": "ID_ISIN", "idValue": x, "exchCode": "US"} for x in chunk]).encode()
        try:
            req = urllib.request.Request("https://api.openfigi.com/v3/mapping", data=body,
                                         headers={"Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                res = json.loads(r.read().decode())
            for isin, item in zip(chunk, res):
                data = (item or {}).get("data") or []
                if data and data[0].get("ticker"):
                    out[isin] = (str(data[0]["ticker"]), str(data[0].get("securityType2") or data[0].get("securityType") or ""))
        except Exception as e:
            print("OpenFIGI 실패:", type(e).__name__, e)
        time.sleep(2.6)
    return out


def yahoo_lookup(isin):
    try:
        url = "https://query2.finance.yahoo.com/v1/finance/search?" + urllib.parse.urlencode({"q": isin, "quotesCount": 3, "newsCount": 0})
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=20) as r:
            qs = json.loads(r.read().decode()).get("quotes") or []
        for q in qs:
            sym = str(q.get("symbol") or "")
            if sym and "." not in sym:      # 미국 상장 (해외 거래소는 .DE 같은 꼬리표가 붙음)
                return sym, str(q.get("quoteType") or "")
    except Exception:
        pass
    return None


def resolve_tickers(isins, cache, figi=figi_lookup, yahoo=yahoo_lookup):
    """cache({isin: [ticker, type]})를 채워서 돌려준다."""
    need = [x for x in dict.fromkeys(isins) if x not in cache]
    if need:
        got = figi(need)
        for isin in need:
            hit = got.get(isin) or yahoo(isin)
            if hit:
                cache[isin] = [hit[0].replace("/", "-").replace(".", "-"), hit[1]]
    return cache


def build_list(rows, cache, amount_key):
    out = []
    for r in rows:
        isin = r["ISIN"]
        tk = cache.get(isin)
        name = clean_name(r.get("KOR_SECN_NM"))
        try:
            amt = float(r.get(amount_key) or 0)
        except ValueError:
            amt = 0.0
        out.append({"rank": int(r.get("RNUM") or len(out) + 1), "isin": isin, "ticker": tk[0] if tk else "",
                    "name": name, "usd": round(amt), "etf": is_etf(name, tk[1] if tk else "")})
    return out


def collect(today=None):
    today = today or dt.datetime.now(KST).date()
    path = os.path.join(OUT, "isin_ticker.json")
    cache = {}
    try:
        with open(path, encoding="utf-8") as f:
            cache = json.load(f)
    except Exception:
        pass
    hold_day, hold_rows = fetch_holdings(today)
    period, net_rows = fetch_netbuy(today)
    if not hold_rows and not net_rows:
        raise ValueError("세이브로 응답이 비어 있음")
    resolve_tickers([r["ISIN"] for r in hold_rows + net_rows], cache)
    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0)
    res = {"generatedAt": dt.datetime.now(KST).strftime("%Y-%m-%d %H:%M"), "holdAsOf": hold_day, "netPeriod": period,
           "hold": build_list(hold_rows, cache, "SUM_FRSEC_AMT"), "netbuy": build_list(net_rows, cache, "SUM_FRSEC_NET_BUY_AMT")}
    with open(os.path.join(OUT, "seohak.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = collect()
    miss = [x["name"] for x in r["hold"] + r["netbuy"] if not x["ticker"]]
    print(f"보관 {len(r['hold'])}개({r['holdAsOf']}), 순매수 {len(r['netbuy'])}개({r['netPeriod']}), 티커 못 찾음 {len(miss)}개: {miss[:10]}")
