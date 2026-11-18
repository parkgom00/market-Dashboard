"""특징주 탭의 뉴스·공시 → out/live_news.json (build_live.py 가 data/live.js 에 합침)

1) 종목별 최신 기사 1건: 등락률·거래대금 상위 종목 (네이버 증권 종목 뉴스)  → 종목 아래 한 줄
2) [특징주] 기사 모음, 시장 속보: 구글 뉴스 RSS (제목·언론사·시간·링크만, 본문은 가져오지 않음)
3) 주요 공시: 금융감독원 OpenDART (DART_API_KEY 가 있을 때만). 주가에 영향이 큰 공시 종류만 골라 호재/주의/변동으로 분류.
"""
import datetime as dt
import email.utils
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = dt.timezone(dt.timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"}
DIAG = {}

STOCK_NEWS_N = 20         # 상위 종목 몇 개까지 기사를 붙일지 (등락률·거래대금 각각)
FEATURE_MAX = 40
MARKET_MAX = 15

# 공시 종류 → (분류 이름, 성격). 성격: good 호재성 / bad 주의 / move 변동·확인 필요 / info 참고
DART_KINDS = [
    ("단일판매ㆍ공급계약체결", "수주·공급계약", "good"),
    ("단일판매·공급계약체결", "수주·공급계약", "good"),
    ("자기주식취득결정", "자사주 매입", "good"),
    ("자기주식취득신탁계약체결결정", "자사주 매입(신탁)", "good"),
    ("주식소각결정", "주식 소각", "good"),
    ("무상증자결정", "무상증자", "good"),
    ("유상증자결정", "유상증자", "bad"),
    ("전환사채권발행결정", "전환사채(CB) 발행", "bad"),
    ("신주인수권부사채권발행결정", "신주인수권부사채(BW) 발행", "bad"),
    ("교환사채권발행결정", "교환사채(EB) 발행", "bad"),
    ("감자결정", "감자", "bad"),
    ("횡령ㆍ배임", "횡령·배임", "bad"),
    ("매매거래정지", "거래정지", "bad"),
    ("상장폐지", "상장폐지 관련", "bad"),
    ("관리종목", "관리종목 관련", "bad"),
    ("불성실공시법인", "불성실공시", "bad"),
    ("최대주주변경", "최대주주 변경", "move"),
    ("회사합병결정", "합병", "move"),
    ("회사분할결정", "분할", "move"),
    ("조회공시", "조회공시(급등락 사유)", "move"),
    ("소송등의제기", "소송", "move"),
    ("투자판단관련주요경영사항", "주요 경영사항", "move"),
    ("영업(잠정)실적", "잠정실적", "info"),
    ("매출액또는손익구조", "실적 변동(30%↑)", "info"),
    ("타법인주식및출자증권취득결정", "타법인 지분 취득", "info"),
    ("현금ㆍ현물배당결정", "배당", "info"),
]


def now():
    return dt.datetime.now(KST)


def get(url, params=None, timeout=15, raw=False):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        b = r.read()
    return b if raw else json.loads(b.decode("utf-8", "replace"))


# ───────────── 1) 종목별 최신 기사 ─────────────
def _flatten_naver_news(js):
    """네이버 종목 뉴스 응답(묶음 목록 또는 항목 목록) → 기사 dict 목록."""
    out = []
    groups = js if isinstance(js, list) else (js.get("items") or js.get("result") or [])
    for g in groups:
        items = g.get("items") if isinstance(g, dict) and isinstance(g.get("items"), list) else [g]
        for it in items:
            if not isinstance(it, dict):
                continue
            title = html.unescape(re.sub(r"<[^>]+>", "", str(it.get("title") or it.get("tit") or ""))).strip()
            if not title:
                continue
            oid, aid = it.get("officeId") or it.get("oid"), it.get("articleId") or it.get("aid")
            url = f"https://n.news.naver.com/mnews/article/{oid}/{aid}" if oid and aid else (it.get("linkUrl") or it.get("url") or "")
            t = str(it.get("datetime") or it.get("dt") or "")
            out.append({"title": title, "src": it.get("officeName") or it.get("ohnm") or "", "time": t[:12], "url": url})
    return out


def stock_news(code):
    try:
        js = get(f"https://m.stock.naver.com/api/news/stock/{code}", {"pageSize": 5, "page": 1})
    except Exception as e:
        DIAG.setdefault("stockErr", []).append(f"{code}:{type(e).__name__}")
        return []
    if "stockSample" not in DIAG:
        DIAG["stockSample"] = json.dumps(js, ensure_ascii=False)[:600]
    return _flatten_naver_news(js)


def pick_recent(arts, since):
    """since(YYYYMMDDHHMM) 이후 기사 중 [특징주] 를 우선, 없으면 가장 최근 것 1건."""
    fresh = [a for a in arts if a["time"] and a["time"] >= since]
    if not fresh:
        return None
    feat = [a for a in fresh if "특징주" in a["title"]]
    a = sorted(feat or fresh, key=lambda x: x["time"], reverse=True)[0]
    t = a["time"]
    return {"title": a["title"], "src": a["src"], "time": f"{t[8:10]}:{t[10:12]}" if len(t) >= 12 else "", "url": a["url"]}


def since_stamp(n):
    """직전 거래일 장 마감(15:30) 이후 기사만 '오늘 움직임'의 이유로 본다. 월요일이면 금요일 15:30."""
    d = n - dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d.strftime("%Y%m%d") + "1530"


def movers_news(rank):
    codes = []
    for key in ("gainers", "value"):
        for r in (rank.get(key) or [])[:STOCK_NEWS_N]:
            if r.get("code") and r["code"] not in codes:
                codes.append(r["code"])
    since = since_stamp(now())
    with ThreadPoolExecutor(6) as ex:
        res = dict(zip(codes, ex.map(stock_news, codes)))
    out = {}
    for c, arts in res.items():
        p = pick_recent(arts, since)
        if p:
            out[c] = p
    DIAG["movers"] = f"{len(out)}/{len(codes)}"
    return out


# ───────────── 2) 구글 뉴스 RSS ─────────────
def google_news(query, limit):
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": query, "hl": "ko", "gl": "KR", "ceid": "KR:ko"})
    try:
        root = ET.fromstring(get(url, raw=True))
    except Exception as e:
        DIAG[f"rss:{query}"] = f"{type(e).__name__}: {e}"
        return []
    out, seen = [], set()
    for it in root.iter("item"):
        title = html.unescape(it.findtext("title") or "").strip()
        src = (it.find("source").text if it.find("source") is not None else "") or ""
        if src and title.endswith(" - " + src):
            title = title[: -len(" - " + src)].strip()
        key = re.sub(r"\W", "", title)[:40]
        if not title or key in seen:
            continue
        seen.add(key)
        try:
            ts = email.utils.parsedate_to_datetime(it.findtext("pubDate")).astimezone(KST)
        except Exception:
            ts = None
        out.append({"title": title, "src": src, "ts": ts.strftime("%Y-%m-%d %H:%M") if ts else "", "url": it.findtext("link") or ""})
    out.sort(key=lambda x: x["ts"], reverse=True)
    DIAG[f"rss:{query}"] = len(out)
    return out[:limit]


def feature_news():
    items = google_news("특징주 when:1d", FEATURE_MAX * 2)
    return [x for x in items if "특징주" in x["title"]][:FEATURE_MAX]


def market_news():
    items = google_news("(코스피 OR 코스닥 OR 증시) (마감 OR 속보 OR 급락 OR 급등) when:1d", MARKET_MAX * 2)
    return [x for x in items if "특징주" not in x["title"]][:MARKET_MAX]


# ───────────── 3) OpenDART 주요 공시 ─────────────
def classify(report_nm):
    nm = report_nm.replace(" ", "")
    if nm.startswith("[기재정정]") or nm.startswith("[첨부정정]") or nm.startswith("[첨부추가]"):
        return None
    for key, label, tone in DART_KINDS:
        if key.replace(" ", "") in nm:
            return label, tone
    return None


def dart_list(key, day):
    rows, page = [], 1
    while page <= 40:
        js = get("https://opendart.fss.or.kr/api/list.json",
                 {"crtfc_key": key, "bgn_de": day, "end_de": day, "page_count": 100, "page_no": page, "last_reprt_at": "Y"})
        st = str(js.get("status"))
        if st == "013":          # 조회된 데이터 없음
            break
        if st != "000":
            DIAG["dart"] = f"status {st}: {js.get('message')}"
            break
        rows += js.get("list") or []
        if page >= int(js.get("total_page") or 1):
            break
        page += 1
    return rows


def naver_price(code):
    try:
        js = get(f"https://m.stock.naver.com/api/stock/{code}/basic")
        pct = js.get("fluctuationsRatio")
        return float(str(pct).replace(",", "")) if pct not in (None, "") else None
    except Exception:
        return None


def dart_disclosures():
    key = os.environ.get("DART_API_KEY")
    if not key:
        DIAG["dart"] = "키 없음"
        return None
    day = now().strftime("%Y%m%d")
    try:
        rows = dart_list(key, day)
    except Exception as e:
        DIAG["dart"] = f"{type(e).__name__}"
        return None
    out = []
    for r in rows:
        if r.get("corp_cls") not in ("Y", "K") or not r.get("stock_code"):
            continue
        c = classify(r.get("report_nm", ""))
        if not c:
            continue
        out.append({"code": r["stock_code"], "name": r.get("corp_name", ""), "market": "KOSPI" if r["corp_cls"] == "Y" else "KOSDAQ",
                    "title": re.sub(r"\s+", " ", r.get("report_nm", "")).strip(), "kind": c[0], "tone": c[1],
                    "no": r.get("rcept_no", ""), "url": "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + r.get("rcept_no", "")})
    out.sort(key=lambda x: x["no"], reverse=True)       # 접수번호가 클수록 나중 공시
    codes = list(dict.fromkeys(x["code"] for x in out))[:120]
    with ThreadPoolExecutor(6) as ex:
        pcts = dict(zip(codes, ex.map(naver_price, codes)))
    for x in out:
        x["pct"] = pcts.get(x["code"])
    DIAG["dart"] = f"전체 {len(rows)}건 중 {len(out)}건"
    return {"date": day, "items": out}


def main():
    try:
        with open(os.path.join(OUT, "live_kr_rank.json"), encoding="utf-8") as f:
            rank = json.load(f)
    except Exception:
        rank = {}
    path = os.path.join(OUT, "live_news.json")
    try:
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        old = {}
    payload = {"asOf": now().strftime("%Y-%m-%d %H:%M"), "items": [],
               "stock": movers_news(rank) if rank else {}, "feature": feature_news(), "market": market_news()}
    d = dart_disclosures()
    if d is None and (old.get("dart") or {}).get("date") == now().strftime("%Y%m%d"):
        d = old["dart"]          # 공시 조회가 잠깐 실패하면 오늘 받아 둔 것 유지
    if d is not None:
        payload["dart"] = d
    payload["diag"] = {k: v for k, v in DIAG.items() if k != "stockSample"} if "--quiet" in sys.argv else DIAG
    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("뉴스:", {k: (len(v) if hasattr(v, "__len__") else v) for k, v in payload.items() if k in ("stock", "feature", "market")},
          "공시:", len((payload.get("dart") or {}).get("items", [])), DIAG.get("dart"))
    import build_live
    build_live.build()


if __name__ == "__main__":
    main()
