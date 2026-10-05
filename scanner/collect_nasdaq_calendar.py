"""나스닥 공개 캘린더(api.nasdaq.com, 키 불필요)에서 경제지표·실적 일정과 예상/실제/이전 값을 모아
out/nasdaq_calendar.json 으로 저장. build_calendar.py 가 이것을 캘린더에 합칩니다.

알려진 특성(다른 대시보드 코드와 실제 데이터 대조로 확인된 것):
  · 경제지표 API 의 date 는 실제 발표일보다 하루 뒤로 들어오고,
  · gmt 필드는 서머타임과 무관하게 항상 UTC-4 로 고정된 시각이다. → 한국시간은 (date-1일, gmt 를 UTC-4 로 보고) 변환.
  · 실적 API 는 날짜가 미 동부 기준 그대로이고 time 에 pre-market / after-hours 가 들어온다.
이 규칙이 틀어졌는지 확인하려고, 우리가 공식 사이트에서 확인한 날짜(calendar_fixed.json)와 비교해 어긋나면 경고를 출력합니다.
"""
import html
import json
import os
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = timezone(timedelta(hours=9))
API_TZ = timezone(timedelta(hours=-4))   # 서머타임 보정 금지 (위 설명)
ECON_URL = "https://api.nasdaq.com/api/calendar/economicevents"
EARN_URL = "https://api.nasdaq.com/api/calendar/earnings"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
           "Accept": "application/json"}

# 국가별로 볼 지표: (영문 키워드, 한글 이름, 중요도 major|macro). 앞에 있는 것이 우선(긴 이름을 먼저 둠).
RULES = {
    "United States": [
        ("Interest Rate Decision", "FOMC 금리결정", "major"), ("FOMC Meeting Minutes", "FOMC 의사록", "major"),
        ("FOMC Economic Projections", "FOMC 점도표", "major"), ("FOMC Press Conference", "FOMC 기자회견", "major"),
        ("Fed Chair", "연준 의장 연설", "major"),
        ("Core CPI", "미국 근원 CPI", "major"), ("CPI", "미국 CPI", "major"),
        ("Core PPI", "미국 근원 PPI", "macro"), ("PPI", "미국 PPI", "macro"),
        ("Core PCE Price Index", "미국 근원 PCE", "major"), ("PCE Price Index", "미국 PCE", "major"),
        ("Nonfarm Payrolls", "미국 비농업 고용", "major"), ("Unemployment Rate", "미국 실업률", "major"),
        ("Initial Jobless Claims", "미국 신규 실업수당 청구", "macro"), ("ADP Nonfarm", "ADP 민간고용", "macro"),
        ("JOLTS Job Openings", "JOLTS 구인", "macro"), ("GDP (QoQ)", "미국 GDP", "major"),
        ("Retail Sales", "미국 소매판매", "macro"), ("ISM Manufacturing PMI", "ISM 제조업", "macro"),
        ("ISM Non-Manufacturing PMI", "ISM 서비스업", "macro"), ("S&P Global Manufacturing PMI", "S&P글로벌 제조업 PMI", "macro"),
        ("S&P Global Services PMI", "S&P글로벌 서비스업 PMI", "macro"), ("Durable Goods Orders", "미국 내구재 주문", "macro"),
        ("Michigan Consumer Sentiment", "미시간 소비심리", "macro"), ("CB Consumer Confidence", "미국 소비자신뢰", "macro"),
        ("Philadelphia Fed Manufacturing Index", "필라델피아 연은지수", "macro"), ("Richmond Manufacturing Index", "리치먼드 연은지수", "macro"),
        ("Existing Home Sales", "미국 기존주택판매", "macro"), ("New Home Sales", "미국 신규주택판매", "macro"),
        ("Building Permits", "미국 건축허가", "macro"), ("Housing Starts", "미국 주택착공", "macro"),
        ("Trade Balance", "미국 무역수지", "macro"), ("Industrial Production", "미국 산업생산", "macro"),
        ("Import Price", "미국 수입물가", "macro"), ("Nonfarm Productivity", "미국 생산성", "macro"),
    ],
    "South Korea": [
        ("Interest Rate Decision", "한국 금통위 금리결정", "major"), ("CPI", "한국 CPI", "macro"), ("PPI", "한국 PPI", "macro"),
        ("GDP", "한국 GDP", "macro"), ("Exports", "한국 수출", "major"), ("Imports", "한국 수입", "macro"),
        ("Trade Balance", "한국 무역수지", "macro"), ("Industrial Production", "한국 산업생산", "macro"),
        ("Unemployment Rate", "한국 실업률", "macro"), ("Retail Sales", "한국 소매판매", "macro"),
        ("Manufacturing PMI", "한국 제조업 PMI", "macro"), ("Consumer Confidence", "한국 소비자심리", "macro"),
        ("Current Account", "한국 경상수지", "macro"),
    ],
    "Japan": [("BoJ Interest Rate Decision", "BOJ 금리결정", "major")],
    "China": [("Manufacturing PMI", "중국 제조업 PMI", "macro"), ("CPI", "중국 CPI", "macro")],
}
EXCLUDE = ("gdpnow", "atlanta fed", "redbook", "api weekly", "cushing", "cleveland", "consumer price index ex", "revised")
FAMILY = [("FOMC 금리결정", "FOMC"), ("CPI", "CPI"), ("PCE", "PCE"), ("비농업 고용", "JOBS"), ("실업률", "JOBS")]


def match_rule(country, name):
    low = name.lower()
    if any(x in low for x in EXCLUDE):
        return None
    for key, label, level in RULES.get(country, []):
        if key.lower() in low:
            return label, level
    return None


def family_of(label):
    # (전월비) 같은 꼬리표는 무시하고 계열만 판단
    """공식 일정(ind)과 겹치는 지표 계열이면 그 계열 이름. 미국 지표만 대상."""
    if not label.startswith(("미국", "FOMC")):
        return None
    for key, fam in FAMILY:
        if key in label:
            return fam
    return None


def to_kst(api_date, gmt_str):
    """경제지표 API 날짜/시각 → 한국 (YYYY-MM-DD, HH:MM). 시각이 없으면 (전날 날짜, '')."""
    base = api_date - timedelta(days=1)
    try:
        hh, mm = (int(x) for x in (gmt_str or "").split(":")[:2])
    except ValueError:
        return base.isoformat(), ""
    k = datetime(base.year, base.month, base.day, hh, mm, tzinfo=API_TZ).astimezone(KST)
    return k.date().isoformat(), k.strftime("%H:%M")


def _clean(v):
    v = html.unescape(str(v or "")).strip()
    return "" if v.upper() in ("", "N/A", "NA", "-", "--") else v


def _rows(payload):
    data = (payload or {}).get("data") or {}
    rows = data.get("rows") if isinstance(data, dict) else data
    return rows if isinstance(rows, list) else []


def parse_econ(rows, api_date):
    out = []
    for r in rows:
        m = match_rule((r.get("country") or "").strip(), (r.get("eventName") or "").strip())
        if not m:
            continue
        d, t = to_kst(api_date, r.get("gmt"))
        raw = (r.get("eventName") or "")
        suffix = " (전월비)" if "mom" in raw.lower() else " (전년비)" if "yoy" in raw.lower() else " (전기비)" if "qoq" in raw.lower() else ""
        out.append({"date": d, "time": t, "title": m[0] + suffix, "level": m[1], "kind": "econ",
                    "consensus": _clean(r.get("consensus")), "actual": _clean(r.get("actual")), "previous": _clean(r.get("previous"))})
    return out


def parse_earnings(rows, api_date, watch):
    """watch: {티커: 한글명}. 장마감 후 발표는 한국에선 다음 날."""
    out = []
    for r in rows:
        sym = (r.get("symbol") or "").strip().upper()
        if sym not in watch:
            continue
        when = (r.get("time") or "").lower()
        d = api_date + timedelta(days=1) if "after" in when else api_date
        out.append({"date": d.isoformat(), "time": "", "title": f"{watch[sym]} 실적 발표", "level": "earnings", "kind": "earnings",
                    "note": "장마감 후(한국 다음 날 새벽)" if "after" in when else ("장 시작 전" if "pre" in when else ""),
                    "epsForecast": _clean(r.get("epsForecast")), "eps": _clean(r.get("eps")), "surprise": _clean(r.get("surprise"))})
    return out


def lines_for(e):
    """화면에 보일 줄. 발표 전엔 예상·이전, 발표 후엔 실제 포함."""
    if e["kind"] == "earnings":
        out = []
        if e.get("eps"):
            s = f"EPS 실제 {e['eps']}" + (f" (예상 {e['epsForecast']})" if e.get("epsForecast") else "")
            if e.get("surprise"):
                s += f" · 서프라이즈 {e['surprise']}%"
            out.append(s)
        elif e.get("epsForecast"):
            out.append(f"EPS 예상 {e['epsForecast']}")
        if e.get("note"):
            out.append(e["note"])
        return out
    parts = []
    if e.get("actual"):
        parts.append(f"실제 {e['actual']}")
    if e.get("consensus"):
        parts.append(f"예상 {e['consensus']}")
    if e.get("previous"):
        parts.append(f"이전 {e['previous']}")
    return [" · ".join(parts)] if parts else []


def _get(url, day, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url + "?" + urllib.parse.urlencode({"date": day.isoformat()}), headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def fetch_day(day, watch):
    out, fails = [], 0
    for url, parser in ((ECON_URL, lambda p: parse_econ(_rows(p), day)), (EARN_URL, lambda p: parse_earnings(_rows(p), day, watch))):
        try:
            out += parser(_get(url, day))
        except Exception:
            fails += 1
    return out, fails


def merge_store(old, new, keep_from):
    """이전 저장분과 합침. 같은 (날짜, 제목)은 새 값으로 덮어쓰되, 새 값이 비어 있으면 이전 값을 유지."""
    store = {(e["date"], e["title"]): e for e in old if e["date"] >= keep_from}
    for e in new:
        k = (e["date"], e["title"])
        prev = store.get(k)
        if prev:
            for f in ("consensus", "actual", "previous", "eps", "epsForecast", "surprise", "time"):
                if not e.get(f) and prev.get(f):
                    e[f] = prev[f]
        store[k] = e
    return sorted(store.values(), key=lambda e: (e["date"], e["time"], e["title"]))


def check_against_fixed(events, fixed):
    """공식 확인 일정과 날짜가 다르면 경고 문자열 목록."""
    warns = []
    fx = {}
    for f in fixed:
        if f.get("ind"):
            fx.setdefault(f["ind"], set()).add(f["date"])
    for e in events:
        fam = family_of(e["title"])
        if fam in ("CPI", "FOMC") and fx.get(fam) and e["date"] not in fx[fam]:
            near = [d for d in fx[fam] if abs((date.fromisoformat(d) - date.fromisoformat(e["date"])).days) <= 3]
            if near:
                warns.append(f"{e['title']} {e['date']} ≠ 공식 {sorted(near)}")
    return warns


def main(back=7, ahead=75, workers=6):
    with open(os.path.join(HERE, "earnings_watch.json"), encoding="utf-8") as f:
        w = json.load(f)
    watch = {x["ticker"]: x["name"] for x in w["US"]}
    today = datetime.now(KST).date()
    days = [today + timedelta(days=i) for i in range(-back, ahead)]
    new, fails = [], 0
    with ThreadPoolExecutor(workers) as ex:
        for got, f in ex.map(lambda d: fetch_day(d, watch), days):
            new += got
            fails += f
    if fails > len(days):   # 절반 넘게 실패 = 차단/오류. 기존 파일 유지
        raise SystemExit(f"나스닥 캘린더 조회 실패가 너무 많음({fails}회). 기존 파일을 유지합니다.")
    path = os.path.join(OUT, "nasdaq_calendar.json")
    old = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else []
    # 조회 구간 안의 옛 항목은 이번 조회가 최신이므로, 구간 밖만 이전 저장분에서 유지
    lo, hi = (today - timedelta(days=back)).isoformat(), (today + timedelta(days=ahead)).isoformat()
    kept_old = [e for e in old if not (lo <= e["date"] <= hi)]
    merged = merge_store(kept_old + [e for e in old if lo <= e["date"] <= hi], new, (today - timedelta(days=60)).isoformat())
    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
    fixed = json.load(open(os.path.join(HERE, "calendar_fixed.json"), encoding="utf-8"))["events"]
    for wmsg in check_against_fixed(merged, fixed):
        print("경고(날짜 불일치):", wmsg)
    print(f"나스닥 캘린더 {len(new)}건 수집 (실패 {fails}회), 저장 {len(merged)}건")


if __name__ == "__main__":
    main()
