"""세이브로(예탁결제원) 해외주식 상위 종목 응답 형식을 확인하는 임시 진단 스크립트."""
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "seibro_probe")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
PAGE = "https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/ovsSec/BIP_CNTS10013V.xml&menuNo=921"


def save(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text[:200000])


def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": PAGE})
        with urllib.request.urlopen(req, timeout=40) as r:
            return f"HTTP {r.status}\n" + r.read().decode("utf-8", "replace")
    except Exception as e:
        return f"ERR {type(e).__name__}: {e}"


def post(body):
    try:
        req = urllib.request.Request("https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp",
                                     data=body.encode("utf-8"),
                                     headers={"User-Agent": UA, "Referer": PAGE, "Content-Type": "application/xml; charset=UTF-8",
                                              "Accept": "application/xml", "Origin": "https://seibro.or.kr"})
        with urllib.request.urlopen(req, timeout=40) as r:
            return f"HTTP {r.status}\n" + r.read().decode("utf-8", "replace")
    except Exception as e:
        return f"ERR {type(e).__name__}: {e}"


save("page_xml.txt", get("https://seibro.or.kr/IPORTAL/user/ovsSec/BIP_CNTS10013V.xml"))
save("page_html.txt", get(PAGE))
COMMON = ('<MENU_NO value="921"/><CMM_BTN_ABBR_NM value="total_search,openall,print,hwp,word,pdf,seach,xls,"/>'
          '<W2XPATH value="/IPORTAL/user/ovsSec/BIP_CNTS10013V.xml"/>')
i = 0
for action in ("getImptFrcurStkCusRemaList", "getImptFrcurStkSetlAmtList"):
    for extra in ('<PG_START value="1"/><PG_END value="50"/><START_DT value="20260925"/><END_DT value="20261002"/><S_TYPE value="2"/><S_COUNTRY value="US"/><D_TYPE value="1"/>',
                  '<PG_START value="1"/><PG_END value="50"/><START_DT value="20260901"/><END_DT value="20261002"/><S_TYPE value="2"/><S_COUNTRY value="ALL"/><D_TYPE value="2"/>'):
        i += 1
        body = f'<reqParam action="{action}" task="ksd.safe.bip.cnts.OvsSec.process.OvsSecIsinPTask">{COMMON}{extra}</reqParam>'
        save(f"post_{i}_{action}.txt", body + "\n\n" + post(body))
print(os.listdir(OUT))
