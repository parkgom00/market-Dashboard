"""수집기·캘린더·합치기 로직을 가짜 데이터로 검증합니다 (인터넷 불필요). 실행: python test_collect.py"""
import json
import os
import tempfile
from datetime import date

import pandas as pd

import build_calendar
import build_live
import collect_kr
import collect_us

ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


# ── 국내 ────────────────────────────────────────────────
raw = pd.DataFrame({
    "Code": ["5930", "000660", "111111", "222222", "333333", "444444"],
    "Name": ["삼성전자", "SK하이닉스", "급등소형주", "OO스팩1호", "코넥스종목", "정상종목"],
    "Market": ["KOSPI", "KOSPI", "KOSDAQ", "KOSDAQ", "KONEX", "KOSDAQ"],
    "Close": [70000, 180000, 1000, 2000, 5000, 30000],
    "ChagesRatio": [1.5, 6.2, 29.9, 25.0, 20.0, 9.1],
    "Amount": [9e11, 7e11, 3e8, 5e10, 5e10, 4e10],   # 급등소형주는 거래대금 3억
})
df = collect_kr.normalize(raw)
check("종목코드 6자리 보정 (5930 → 005930)", "005930" in set(df["code"]))
check("스팩·코넥스 제외", set(df["name"]) == {"삼성전자", "SK하이닉스", "급등소형주", "정상종목"})
g = collect_kr.top_gainers(df)
check("등락률 상위: 거래대금 10억 미만 종목 제외 + 내림차순", [r["name"] for r in g] == ["정상종목", "SK하이닉스", "삼성전자"])
v = collect_kr.top_value(df)
check("거래대금 상위: 내림차순, 억 단위 반올림", v[0]["name"] == "삼성전자" and v[0]["valueEok"] == 9000)

raw2 = raw.drop(columns=["ChagesRatio"]).assign(Changes=[1000, 10000, 200, 400, 800, 2500])
df2 = collect_kr.normalize(raw2)
check("등락률 컬럼이 없으면 등락폭으로 직접 계산 (SK하이닉스 10000/170000 = 5.88%)",
      abs(df2.set_index("code").loc["000660", "pct"] - 5.88) < 0.01)

try:
    collect_kr.normalize(pd.DataFrame({"foo": [1]}))
    check("필요 컬럼이 없으면 오류로 알림", False)
except ValueError:
    check("필요 컬럼이 없으면 오류로 알림", True)

themes = [
    {"name": "반도체", "kr": [{"code": "005930"}, {"code": "000660"}, {"code": "999999"}]},
    {"name": "한 종목뿐", "kr": [{"code": "005930"}, {"code": "888888"}]},
]
ts = collect_kr.theme_strength(df, themes)
check("테마 강약: 시세표에 없는 종목은 빼고, 종목이 2개 미만인 테마는 숨김", len(ts) == 1 and len(ts[0]["stocks"]) == 2)

# ── 미국 ────────────────────────────────────────────────
idx = pd.date_range("2026-09-28", periods=5, freq="B")
closes = pd.DataFrame({
    "NVDA": [100, 101, 102, 103, 106.0],
    "AVGO": [200, 200, 201, 202, 206.0],
    "XOM": [100, 100, 100, 100, 99.0],
    "NEW": [None, None, None, None, 5.0],     # 데이터 부족
}, index=idx)
ch = collect_us.compute_changes(closes)
check("미국 등락률: 마지막 종가 vs 직전 종가", abs(ch["NVDA"]["pct"] - (106 / 103 - 1) * 100) < 1e-9 and ch["NVDA"]["date"] == "2026-10-02")
check("데이터가 하루뿐인 종목은 제외", "NEW" not in ch)
check("기준일 문구에 요일 포함 (2026-10-02 = 금)", collect_us.as_of_text("2026-10-02") == "2026-10-02 (금) 미국 정규장 기준")

umap = [
    {"name": "AI", "us": [{"ticker": "NVDA", "name": "엔비디아"}, {"ticker": "AVGO", "name": "브로드컴"}],
     "kr": [{"code": "000660", "name": "SK하이닉스", "link": "HBM 공급"}]},
    {"name": "에너지", "us": [{"ticker": "XOM", "name": "엑슨"}, {"ticker": "NEW", "name": "신규"}], "kr": []},
]
res = collect_us.build_us_themes(ch, umap)
check("급등 테마만(평균 +1% 이상) 선택, 미국 종목 내림차순, 국내 연관주 연결 포함",
      [r["name"] for r in res] == ["AI"] and res[0]["usStocks"][0]["ticker"] == "NVDA" and res[0]["krStocks"][0]["link"] == "HBM 공급")
flat = pd.DataFrame({"NVDA": [100, 100.2], "AVGO": [100, 99.9]}, index=idx[:2])
fb = collect_us.build_us_themes(collect_us.compute_changes(flat), umap)
check("급등 테마가 없으면 상위 테마를 대신 표시", len(fb) == 1 and fb[0]["name"] == "AI")

with tempfile.TemporaryDirectory() as d:
    collect_us.OUT = d
    json.dump({"forDate": "2026-10-01", "lines": ["어제 요약"]}, open(os.path.join(d, "us_summary.json"), "w", encoding="utf-8"))
    idx_ch = {"^IXIC": {"close": 20000.0, "pct": 1.2, "date": "2026-10-02"},
              "^GSPC": {"close": 6000.0, "pct": 0.8, "date": "2026-10-02"},
              "^DJI": {"close": 45000.0, "pct": 0.3, "date": "2026-10-02"}}
    p = collect_us.build_payload(idx_ch, ch, umap)
    check("요약 파일 날짜가 다르면 오래된 요약은 쓰지 않음", p["summary"] == [])
    json.dump({"forDate": "2026-10-02", "lines": ["오늘 요약"]}, open(os.path.join(d, "us_summary.json"), "w", encoding="utf-8"))
    check("날짜가 맞으면 요약 포함, 지수 3개 순서 유지",
          collect_us.build_payload(idx_ch, ch, umap)["summary"] == ["오늘 요약"] and [i["name"] for i in p["indices"]] == ["나스닥", "S&P 500", "다우"])

# ── 특징주 합치기 ───────────────────────────────────────
with tempfile.TemporaryDirectory() as d:
    for name, body in [("live_kr_rank.json", {"asOf": "2026-10-05 16:10", "gainers": [1], "value": [2]}),
                       ("live_themes_kr.json", {"asOf": "2026-10-05 16:10", "themes": [3]}),
                       ("live_themes_us.json", {"asOf": "2026-10-05 07:30", "themes": [4]}),
                       ("live_news.json", {"asOf": "2026-10-05 16:30", "items": [5]})]:
        json.dump(body, open(os.path.join(d, name), "w", encoding="utf-8"))
    out = build_live.build(d, os.path.join(d, "live.js"))
    check("특징주 합치기: 국내 4개 항목 + 미국 테마", set(out["kr"]) == {"news", "gainers", "value", "themes"} and set(out["us"]) == {"themes"})
    check("데이터 기준 시각은 가장 최근 조각의 시각", out["asOf"] == "2026-10-05 16:30")

# ── 캘린더 ──────────────────────────────────────────────
fx = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar_fixed.json"), encoding="utf-8"))["events"]
titles = {(e["date"], e["title"]) for e in fx}
check("FOMC 10/28(미국) → 한국 날짜 10/29", any(d == "2026-10-29" and "FOMC" in t for d, t in titles))
check("CPI 9월분은 10/14", any(d == "2026-10-14" and "CPI" in t for d, t in titles))
check("미국 휴장 7/3(독립기념일 대체) 포함", any(d == "2026-07-03" and "미국 증시 휴장" in t for d, t in titles))

ex = build_calendar.krx_extra_closures([2026, 2028])
dates = {e["date"] for e in ex}
check("한국거래소 추가 휴장: 5/1, 연말 마지막 영업일 (2026-12-31 목, 2028-12-31 일 → 12-29 금)",
      {"2026-05-01", "2026-12-31", "2028-05-01", "2028-12-29"} <= dates)

m = build_calendar.merge(
    [{"date": "2026-10-09", "type": "holiday", "market": "KR", "title": "한글날 (증시 휴장)"}],
    [[{"date": "2026-10-09", "type": "holiday", "market": "KR", "title": "한글날"},
      {"date": "2026-10-03", "type": "holiday", "market": "KR", "title": "개천절"}]],     # 토요일
    [{"date": "2026-10-21", "type": "earnings", "market": "US", "title": "테슬라 실적"},
     {"date": "잘못된날짜", "type": "event", "title": "무시"},
     {"date": "2026-10-22", "type": "없는유형", "title": "무시"}])
check("같은 날 같은 시장 휴장 중복 제거, 주말 휴장 제외, 수동 일정 유지, 형식 오류 건너뜀",
      [e["title"] for e in m] == ["한글날 (증시 휴장)", "테슬라 실적"])

with tempfile.TemporaryDirectory() as d:
    out = build_calendar.build(os.path.join(d, "calendar.js"), today=date(2026, 10, 5))
    txt = open(os.path.join(d, "calendar.js"), encoding="utf-8").read()
    check("calendar.js 생성 (window.DASH.calendar)", "window.DASH.calendar = " in txt and len(out["events"]) > 50)

# ── 지표 결과·실적 합치기 ────────────────────────────────
evs = [{"date": "2026-09-11", "type": "econ", "market": "US", "title": "CPI", "ind": "CPI", "ref": "2026-08"},
       {"date": "2026-10-14", "type": "econ", "market": "US", "title": "CPI2", "ind": "CPI", "ref": "2026-09"}]
r = build_calendar.attach_results(evs, {"CPI|2026-08": ["전체 +0.3%"], "CPI|2026-09": ["x"]}, date(2026, 10, 6))
check("발표일이 지난 지표에만 결과 첨부, 내부 필드 제거", r[0].get("result") == ["전체 +0.3%"] and "result" not in r[1] and "ind" not in r[0])
d = build_calendar.dedupe_earnings([
    {"date": "2026-11-20", "type": "earnings", "market": "US", "title": "엔비디아 실적 발표 (예정)"},
    {"date": "2026-11-19", "type": "earnings", "market": "US", "title": "엔비디아 실적 발표"}])
check("실적 중복 시 수동 입력(확정) 우선", len(d) == 1 and d[0]["date"] == "2026-11-19")
check("PCE 발표일 포함 (10/29)", any(e["date"] == "2026-10-29" and "PCE" in e["title"] for e in fx))

import collect_econ
import collect_earnings
from datetime import date as _d
idx = pd.date_range("2025-08-01", periods=14, freq="MS")
ser = pd.Series([100 + i * 0.3 for i in range(14)], index=idx)
res = collect_econ.build_results({"CPIAUCSL": ser, "CPILFESL": ser}, [{"ind": "CPI", "ref": "2026-09"}, {"ind": "CPI", "ref": "2027-05"}])
check("CPI 결과: 전월 대비 계산, 데이터 없는 기준월은 건너뜀", list(res) == ["CPI|2026-09"] and "+0.29%" in res["CPI|2026-09"][0])
check("실적 날짜: 미국 장 마감 후(16:20 ET) → 한국 다음 날", collect_earnings.to_kst_date("2026-11-19 16:20:00-05:00") == "2026-11-20")
check("실적: 지난 분기·너무 먼 날짜 제외", collect_earnings.upcoming(["2026-08-27", "2026-11-20", "2027-08-01"], _d(2026, 10, 6)) == ["2026-11-20"])

# ── 미국장 확장 ─────────────────────────────────────────
import us_brief
chg = {"^IXIC": {"close": 20000.0, "pct": 1.2, "date": "2026-10-02", "diff": 240.0},
       "^TNX": {"close": 4.25, "pct": -1.3, "date": "2026-10-02", "diff": -0.056},
       "XLK": {"close": 200.0, "pct": 1.5, "date": "2026-10-02", "diff": 3.0}}
ix = collect_us.build_indices(chg)
check("금리는 bp 로 표시, 없는 심볼은 건너뜀", [i["name"] for i in ix] == ["나스닥", "미국 10년물 금리"] and ix[1]["changeText"] == "4.25% (-5.6bp)" and ix[1]["changeBp"] == -5.6)
sc = collect_us.build_sectors(chg)
check("업종 목록: 시세 있는 것만, 한국 연결 키워드 포함", len(sc) == 1 and sc[0]["name"] == "기술" and sc[0]["kr"])
b = us_brief.clean_brief({"us_market": "m", "connections": [{"us_ticker": "mu", "us_name": "마이크론", "korea_picks": [{"name": "SK하이닉스", "strength": "9"}]}, {"us_name": "티커없음"}]})
us_brief.fill_changes(b, {"MU": 3.004})
check("브리핑 정리: 티커 없는 연결 제거, strength 1~3 보정, 등락률은 실제 시세로 채움",
      len(b["connections"]) == 1 and b["connections"][0]["koreaPicks"][0]["strength"] == 3 and b["connections"][0]["usChange"] == 3.0)
check("필수 항목이 없으면 브리핑 폐기", us_brief.clean_brief({"news": []}) is None)
calls = []
def gen_fail_then_ok(prompt, system, search):
    calls.append(search)
    if search:
        raise RuntimeError("tools unsupported")
    return {"us_market": "ok"}
r = us_brief.generate_brief("2026-10-02", collect_us.build_indices(chg), collect_us.build_sectors(chg), [], gen_fail_then_ok)
check("검색 실패 시 검색 없이 재시도하고 grounded=False 표시", calls == [True, False] and r["grounded"] is False)

# ── 나스닥 캘린더·만기일 ─────────────────────────────────
import collect_nasdaq_calendar as nc
check("나스닥 시각 변환: CPI(api 10/15, 08:30) → 한국 10/14 21:30", nc.to_kst(date(2026, 10, 15), "08:30") == ("2026-10-14", "21:30"))
check("FOMC(api 10/29, 14:00) → 한국 10/29 03:00 (공식 일정과 일치)", nc.to_kst(date(2026, 10, 29), "14:00") == ("2026-10-29", "03:00"))
rows = [{"country": "United States", "eventName": "Core CPI MoM", "gmt": "08:30", "consensus": "0.3%", "actual": "", "previous": "0.2%"},
        {"country": "United States", "eventName": "Cleveland CPI", "gmt": "08:30"}, {"country": "Brazil", "eventName": "CPI"}]
pe = nc.parse_econ(rows, date(2026, 10, 15))
check("지표 필터: 화이트리스트만, 제외어·타국 제외, 전월비 꼬리표", len(pe) == 1 and pe[0]["title"] == "미국 근원 CPI (전월비)" and pe[0]["level"] == "major")
er = nc.parse_earnings([{"symbol": "NVDA", "time": "time-after-hours", "epsForecast": "$1.0", "eps": "$1.1", "surprise": "10"},
                        {"symbol": "ZZZZ", "time": ""}], date(2026, 11, 19), {"NVDA": "엔비디아"})
check("실적: 관심 종목만, 장마감 후는 한국 다음 날, 서프라이즈 문구", len(er) == 1 and er[0]["date"] == "2026-11-20" and "서프라이즈 10%" in nc.lines_for(er[0])[0])
host = [{"date": "2026-10-14", "type": "econ", "market": "US", "title": "CPI 발표", "ind": "CPI", "ref": "2026-09"}]
nas = [dict(pe[0], date="2026-10-14", time="21:30"), {"date": "2026-10-15", "time": "21:30", "title": "미국 소매판매", "level": "macro", "kind": "econ", "consensus": "0.4%", "actual": "", "previous": "0.1%"}]
mg = build_calendar.attach_results(build_calendar.attach_nasdaq(host, nas), {}, date(2026, 10, 6))
check("공식 일정에는 예상/이전 줄을 붙이고, 그 밖의 지표는 독립 일정으로 추가",
      len(mg) == 2 and "예상 0.3%" in mg[0]["result"][0] and mg[0]["time"] == "21:30" and mg[1]["title"] == "미국 소매판매" and mg[1]["market"] == "US")
ex = build_calendar.expiry_events([2026], {"2026-10-08"})
exd = {(e["market"], e["date"]): e["title"] for e in ex}
check("옵션 만기: 한국 둘째 목요일(9/10 동시만기), 휴장이면 앞 영업일(10/8→10/7), 미국 셋째 금요일(9/18 쿼드러플)",
      "동시만기" in exd[("KR", "2026-09-10")] and ("KR", "2026-10-07") in exd and "쿼드러플" in exd[("US", "2026-09-18")])

# ── 네이버 테마 ─────────────────────────────────────────
import naver_themes
groups = [{"no": 1, "name": "A", "changeRate": 5.0, "totalCount": 10, "riseCount": 8},
          {"no": 2, "name": "B", "changeRate": 9.0, "totalCount": 3, "riseCount": 3},
          {"no": 3, "name": "C", "changeRate": -4.0, "totalCount": 12, "riseCount": 1},
          {"no": 4, "name": "D", "changeRate": 1.0, "totalCount": 8, "riseCount": 5}]
pg = naver_themes.pick_groups(groups, strong=1, weak=1)
check("테마 선택: 종목 5개 미만 제외, 상위 + 하위(음수만)", [g["no"] for g in pg] == [1, 3])
check("구성종목 코드 추출", naver_themes.members_codes({"stocks": [{"itemCode": "005930"}, {}]}) == ["005930"])
bt = naver_themes.build_themes(pg, {1: ["005930", "000660", "999999"], 3: ["111111"]}, df)
check("테마 구성: 시세표에 있는 종목만, 거래대금 큰 순, 종목 2개 미만 테마 숨김, 테마 등락률·상승종목 수 유지",
      len(bt) == 1 and bt[0]["name"] == "A" and [s["name"] for s in bt[0]["stocks"]] == ["삼성전자", "SK하이닉스"] and bt[0]["rise"] == 8 and bt[0]["rate"] == 5.0)

print(f"\n{sum(ok)}/{len(ok)} 통과")
raise SystemExit(0 if all(ok) else 1)
