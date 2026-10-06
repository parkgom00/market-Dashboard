"""네이버 증권 모바일의 테마 목록·구성종목으로 '오늘 강한/약한 국내 테마'를 만듭니다.

주의: 공식 개방 API 가 아니라 네이버 증권 모바일 화면이 쓰는 주소를 직접 호출합니다 (키 불필요).
네이버가 주소를 바꾸거나 막으면 실패하며, 그 경우 collect_kr.py 는 scanner/theme_map.json 기반 테마로 대신합니다.
시세(등락률)는 이 모듈이 아니라 KRX 시세표(df)의 값을 씁니다. 테마 안에서는 거래대금 큰 종목 위주로 보여줍니다.
"""
import json
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

LIST_URL = "https://m.stock.naver.com/api/stocks/theme"
MEMBERS_URL = "https://m.stock.naver.com/api/stocks/theme/{no}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
           "Accept": "application/json", "Referer": "https://m.stock.naver.com/"}
PAGE_SIZE = 100     # 네이버 상한 (200 이상은 400)
PAGES = 3
MIN_TOTAL = 5       # 구성종목이 너무 적은 테마는 등락률이 튀어서 제외
TOP_STRONG, TOP_WEAK, SHOW_STOCKS = 20, 8, 10


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


def fetch_groups():
    groups = []
    for p in range(1, PAGES + 1):
        rows = (_get(LIST_URL, {"page": p, "pageSize": PAGE_SIZE}) or {}).get("groups") or []
        if not rows:
            break
        groups += rows
    return groups


def pick_groups(groups, strong=TOP_STRONG, weak=TOP_WEAK):
    """구성종목 수 조건을 통과한 테마 중 등락률 상위 strong개 + 하위 weak개."""
    ok = [g for g in groups if g.get("totalCount", 0) >= MIN_TOTAL and g.get("name") and g.get("no") is not None]
    ok.sort(key=lambda g: -float(g.get("changeRate") or 0))
    top = ok[:strong]
    bottom = [g for g in ok[strong:] if float(g.get("changeRate") or 0) < 0][-weak:]
    return top + bottom


def members_codes(payload):
    return [s["itemCode"] for s in (payload or {}).get("stocks") or [] if s.get("itemCode")]


def build_themes(groups, members_by_no, df, show=SHOW_STOCKS):
    """groups: pick_groups 결과, members_by_no: {no: [종목코드]}, df: normalize 된 KRX 시세표."""
    by_code = df.set_index("code")
    out = []
    for g in groups:
        codes = [c for c in members_by_no.get(g["no"], []) if c in by_code.index]
        if len(codes) < 2:
            continue
        sub = by_code.loc[codes].sort_values("amount", ascending=False).head(show)
        out.append({"name": g["name"], "rate": round(float(g.get("changeRate") or 0), 2),
                    "rise": int(g.get("riseCount") or 0), "total": int(g.get("totalCount") or 0),
                    "stocks": [{"name": n, "changePct": round(float(p), 2)} for n, p in zip(sub["name"], sub["pct"])]})
    out.sort(key=lambda t: -t["rate"])
    return out


def collect(df, workers=6):
    """네이버 테마 → 화면용 목록. 실패하면 예외 (호출한 쪽이 대체 처리)."""
    groups = pick_groups(fetch_groups())
    if not groups:
        raise ValueError("테마 목록이 비어 있음")

    def one(g):
        try:
            return g["no"], members_codes(_get(MEMBERS_URL.format(no=g["no"])))
        except Exception:
            return g["no"], []
    with ThreadPoolExecutor(workers) as ex:
        members = dict(ex.map(one, groups))
    themes = build_themes(groups, members, df)
    if not themes:
        raise ValueError("구성종목을 하나도 받지 못함")
    return themes


def fetch_all_members(workers=8, min_total=MIN_TOTAL):
    """모든 테마의 구성종목 {테마명: [종목코드]} (순환매 계산용). 테마 약 260개 → 요청 수백 번."""
    groups = [g for g in fetch_groups() if g.get("totalCount", 0) >= min_total and g.get("name") and g.get("no") is not None]
    if not groups:
        raise ValueError("테마 목록이 비어 있음")

    def one(g):
        codes = []
        try:
            for p in range(1, 4):
                rows = (_get(MEMBERS_URL.format(no=g["no"]), {"page": p, "pageSize": 100}) or {}).get("stocks") or []
                new = [s["itemCode"] for s in rows if s.get("itemCode") and s["itemCode"] not in codes]
                codes += new
                if len(rows) < 100 or not new:
                    break
        except Exception:
            pass
        return g["name"], codes
    with ThreadPoolExecutor(workers) as ex:
        out = {name: codes for name, codes in ex.map(one, groups) if codes}
    if len(out) < 30:
        raise ValueError(f"구성종목을 받은 테마가 {len(out)}개뿐")
    return out
