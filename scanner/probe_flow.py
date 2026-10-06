import json, os, re, urllib.parse, urllib.request, datetime as dt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y%m%d")
res = {"at": dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%H:%M"), "today": today}
def tryit(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        res[name] = f"ERR {type(e).__name__}: {e}"
def krx(bld, **p):
    data = urllib.parse.urlencode(dict(bld=bld, locale="ko_KR", share="1", money="1", csvxls_isNo="false", **p)).encode()
    req = urllib.request.Request("http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd", data=data,
        headers={"User-Agent": UA, "Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020303", "X-Requested-With": "XMLHttpRequest"})
    with urllib.request.urlopen(req, timeout=40) as r:
        txt = r.read().decode("utf-8", "replace")
    try:
        j = json.loads(txt)
        k = [x for x in j if isinstance(j[x], list)]
        rows = j[k[0]] if k else []
        return {"keys": list(j.keys()), "n": len(rows), "rows": rows[:3]}
    except Exception:
        return {"raw": txt[:400]}
for name, inv in (("krx_top_foreign", "9000"), ("krx_top_inst", "7050")):
    tryit(name + "_today", lambda: krx("dbms/MDC/STAT/standard/MDCSTAT02401", mktId="ALL", invstTpCd=inv, strtDd=today, endDd=today))
tryit("krx_top_foreign_1002", lambda: krx("dbms/MDC/STAT/standard/MDCSTAT02401", mktId="ALL", invstTpCd="9000", strtDd="20261002", endDd="20261002"))
tryit("krx_stock_daily", lambda: krx("dbms/MDC/STAT/standard/MDCSTAT02302", isuCd="KR7005930003", strtDd="20261001", endDd=today, inqTpCd="2", trdVolVal="2", askBid="3"))
def daum():
    req = urllib.request.Request("https://finance.daum.net/api/investor/days?symbolCode=A005930&page=1&perPage=4",
        headers={"User-Agent": UA, "Referer": "https://finance.daum.net/quotes/A005930"})
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.loads(r.read().decode())
    return [{k: x.get(k) for k in ("date", "foreignStraightPurchaseVolume", "institutionStraightPurchaseVolume", "tradePrice")} for x in j.get("data", [])]
tryit("daum", daum)
def naver_pc():
    req = urllib.request.Request("https://finance.naver.com/item/frgn.naver?code=005930", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        h = r.read().decode("euc-kr", "replace")
    return {"dates": re.findall(r'<span class="tah p10 gray03">(\d{4}\.\d{2}\.\d{2})</span>', h)[:4], "len": len(h)}
tryit("naver_pc", naver_pc)
def naver_m(path):
    req = urllib.request.Request("https://m.stock.naver.com/api/stock/005930/" + path, headers={"User-Agent": UA, "Referer": "https://m.stock.naver.com/"})
    with urllib.request.urlopen(req, timeout=30) as r:
        t = r.read().decode()
    return t[:500]
for p in ("trend?pageSize=2", "investor", "investors", "dealTrend", "provisional"):
    tryit("naver_m_" + p, lambda: naver_m(p))
json.dump(res, open(os.path.join(OUT, "flow_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
