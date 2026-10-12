"""D램 현물가 (TrendForce DRAMeXchange 첫 화면의 'DRAM Spot Price' 표, 키 불필요).

반환: [{"name","item","avg","changePct"}], 갱신 시각 문자열. 실패하면 ([], "").
가격 단위는 달러(칩 1개 기준)이며, 대만 시간으로 하루 한 번(18시 무렵) 갱신된다.
"""
import html
import json
import re
import sys
import urllib.request

URL = "https://www.dramexchange.com/"
ITEMS = [   # (화면 이름, 사이트 표기)
    ("D램 DDR5 16Gb", "DDR5 16Gb (2Gx8) 4800/5600"),
    ("D램 DDR4 16Gb", "DDR4 16Gb (2Gx8) 3200"),
    ("D램 DDR4 8Gb", "DDR4 8Gb (1Gx8) 3200"),
]
NUM = r"\s*([-+]?[\d,]*\.?\d+)"


def page_text(raw):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def parse(raw):
    t = page_text(raw)
    i = t.find("DRAM Spot Price Last Update")
    if i < 0:
        i = t.find("DRAM Spot Price")
    if i < 0:
        return [], ""
    sec = t[i:i + 4000]
    m = re.search(r"Last Update:?\s*([A-Za-z]{3}\.?\s*\d{1,2},?\s*\d{4}\s*\d{1,2}:\d{2})", sec)
    out = []
    for name, item in ITEMS:
        r = re.search(re.escape(item) + r"((?:\s*[-+]?[\d,]*\.?\d+){4,6})\s*%", sec)
        if not r:
            continue
        nums = [float(x.replace(",", "")) for x in r.group(1).split()]
        hi, lo, avg, chg = nums[0], nums[1], nums[-2], nums[-1]
        out.append({"name": name, "item": item, "high": hi, "low": lo, "avg": avg, "changePct": chg})
    return out, (m.group(1) if m else "")


def fetch():
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read().decode("utf-8", "replace")
        rows, upd = parse(raw)
        if not rows:
            t = page_text(raw)
            i = max(0, t.find("DDR5 16Gb"))
            print("D램 표를 찾지 못함. 페이지 일부:", t[max(0, i - 300):i + 900])
        return rows, upd
    except Exception as e:
        print("D램 현물가 조회 실패:", type(e).__name__, e)
        return [], ""


if __name__ == "__main__":
    rows, upd = fetch()
    print(upd, rows)
    if "--save" in sys.argv:
        import os
        os.makedirs("out", exist_ok=True)
        with open("out/dram.json", "w", encoding="utf-8") as f:
            json.dump({"updated": upd, "rows": rows}, f, ensure_ascii=False, indent=1)
