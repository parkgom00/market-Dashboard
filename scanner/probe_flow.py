import json, os, re, urllib.parse, urllib.request, http.cookiejar, datetime as dt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
KST = dt.timezone(dt.timedelta(hours=9))
today = dt.datetime.now(KST).strftime("%Y%m%d")
res = {"at": dt.datetime.now(KST).strftime("%H:%M"), "today": today}
def tryit(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:300]
        except Exception:
            pass
        res[name] = f"ERR {type(e).__name__}: {e} {body}"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
def krx(scheme, bld, **p):
    ref = f"{scheme}://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020303"
    op.open(urllib.request.Request(ref, headers={"User-Agent": UA}), timeout=30).read()
    data = urllib.parse.urlencode(dict(bld=bld, **p)).encode()
    req = urllib.request.Request(f"{scheme}://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd", data=data,
        headers={"User-Agent": UA, "Referer": ref, "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    with op.open(req, timeout=40) as r:
        txt = r.read().decode("utf-8", "replace")
    try:
        j = json.loads(txt); k = [x for x in j if isinstance(j[x], list)]; rows = j[k[0]] if k else []
        return {"keys": list(j.keys()), "n": len(rows), "rows": rows[:2]}
    except Exception:
        return {"raw": txt[:300]}
for sch in ("http", "https"):
    tryit(f"krx_{sch}_top_foreign", lambda: krx(sch, "dbms/MDC/STAT/standard/MDCSTAT02401", locale="ko_KR", mktId="ALL", invstTpCd="9000", strtDd=today, endDd=today, share="1", money="1", csvxls_isNo="false"))
    tryit(f"krx_{sch}_listing", lambda: krx(sch, "dbms/MDC/STAT/standard/MDCSTAT01501", locale="ko_KR", mktId="ALL", trdDd=today, share="1", money="1", csvxls_isNo="false"))
def page(url, enc="euc-kr"):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://finance.naver.com/"}), timeout=30) as r:
        return r.read().decode(enc, "replace")
def naver_frgn():
    h = page("https://finance.naver.com/item/frgn.naver?code=005930")
    return {"dates": re.findall(r'(20\d\d\.\d\d\.\d\d)', h)[:6], "len": len(h)}
tryit("naver_pc_frgn", naver_frgn)
def naver_rank(gubun):
    h = page("https://finance.naver.com/sise/sise_deal_rank_iframe.naver?sosok=01&investor_gubun=" + gubun + "&type=buy")
    txt = re.sub(r"<[^>]+>", " ", h); txt = re.sub(r"\s+", " ", txt)
    return {"len": len(h), "dates": re.findall(r'(\d\d\.\d\d\.\d\d)', txt)[:4], "text": txt[:500]}
tryit("naver_deal_rank_foreign", lambda: naver_rank("9000"))
tryit("naver_deal_rank_inst", lambda: naver_rank("1000"))
def naver_main():
    h = page("https://finance.naver.com/item/main.naver?code=005930")
    i = h.find("외국인·기관"); j = h.find("잠정")
    seg = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h[i:i + 3000])) if i > 0 else ""
    return {"len": len(h), "idx": i, "잠정_idx": j, "seg": seg[:700]}
tryit("naver_main", naver_main)
json.dump(res, open(os.path.join(OUT, "flow_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
