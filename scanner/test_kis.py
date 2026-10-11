"""kis.py 와 그 연결부를 가짜 응답으로 점검 (인터넷·키 불필요)."""
import datetime as dt
import json
import os
import tempfile
import urllib.parse

os.environ["KIS_APP_KEY"] = "test-key"
os.environ["KIS_APP_SECRET"] = "test-secret"
os.environ["KIS_TOKEN_FILE"] = os.path.join(tempfile.mkdtemp(), "tok.json")
os.environ["M480_KIS_CACHE"] = os.path.join(tempfile.mkdtemp(), "c.json")

import kis  # noqa: E402

kis.MIN_GAP = 0
KST = dt.timezone(dt.timedelta(hours=9))
CALLS = {"token": 0, "rate": 0}
ok = fail = 0


def check(name, cond):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        print("FAIL", name)


def day_bars(date, until="1530", base=10000):
    t = dt.datetime.strptime(date + "0900", "%Y%m%d%H%M")
    end = dt.datetime.strptime(date + until, "%Y%m%d%H%M")
    out = []
    while t <= end:
        p = base + (t.hour * 60 + t.minute) % 7
        out.append({"stck_bsop_date": date, "stck_cntg_hour": t.strftime("%H%M%S"), "stck_prpr": str(p), "stck_oprc": str(p),
                    "stck_hgpr": str(p + 5), "stck_lwpr": str(p - 5), "cntg_vol": "100"})
        t += dt.timedelta(minutes=1)
    return out


TRADING = {"20261007", "20261008", "20261012"}   # 10/09 휴장


def fake_http(req, timeout=15):
    url = req.full_url
    if url.endswith("/oauth2/tokenP"):
        CALLS["token"] += 1
        return {"access_token": "TOK", "expires_in": 86400}
    q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    tr = req.headers.get("Tr_id")
    if req.headers.get("Authorization") != "Bearer TOK":
        return {"rt_cd": "1", "msg_cd": "EGW00123"}
    if tr == "FHKST01010100":
        if q["FID_INPUT_ISCD"] == "RATE" and CALLS["rate"] == 0:
            CALLS["rate"] += 1
            return {"rt_cd": "1", "msg_cd": "EGW00201"}
        return {"rt_cd": "0", "output": {"stck_prpr": "10500", "stck_oprc": "10000", "stck_hgpr": "10520", "stck_lwpr": "9900",
                                         "acml_vol": "10000", "acml_tr_pbmn": "105000000", "prdy_ctrt": "5.00"}}
    if tr == "FHKST03010200":
        rows = [b for b in day_bars("20261012", q["FID_INPUT_HOUR_1"][:4]) if b["stck_cntg_hour"] <= q["FID_INPUT_HOUR_1"]]
        return {"rt_cd": "0", "output2": list(reversed(rows[-30:]))}
    if tr == "FHKST03010230":
        d, h = q["FID_INPUT_DATE_1"], q["FID_INPUT_HOUR_1"]
        if d not in TRADING:
            return {"rt_cd": "0", "output2": list(reversed(day_bars("20261008")[-120:]))}   # 휴장일엔 직전 거래일 자료가 오는 경우 흉내
        rows = [b for b in day_bars(d) if b["stck_cntg_hour"] <= h]
        return {"rt_cd": "0", "output2": list(reversed(rows[-120:]))}
    if tr == "HHPTJ04160200":
        if q["MKSC_SHRN_ISCD"] == "NONE":
            return {"rt_cd": "0", "output2": [{"bsop_hour_gb": "1", "frgn_fake_ntby_qty": "0", "orgn_fake_ntby_qty": "0"}]}
        return {"rt_cd": "0", "output2": [{"bsop_hour_gb": "1", "frgn_fake_ntby_qty": "100", "orgn_fake_ntby_qty": "0"},
                                          {"bsop_hour_gb": "4", "frgn_fake_ntby_qty": "3000", "orgn_fake_ntby_qty": "-1000"},
                                          {"bsop_hour_gb": "5", "frgn_fake_ntby_qty": "0", "orgn_fake_ntby_qty": "0"}]}
    return {"rt_cd": "1", "msg_cd": "UNKNOWN"}


kis._http = fake_http

# 토큰: 한 번만 발급, 파일로 재사용
p = kis.price("005930")
check("price", p and p["price"] == 10500 and p["open"] == 10000 and p["volume"] == 10000)
kis._token[0] = None
kis.price("005930")
check("token cached in file", CALLS["token"] == 1)
check("token file private", oct(os.stat(os.environ["KIS_TOKEN_FILE"]).st_mode & 0o777) == "0o600")
# 초당 한도 초과 → 다시 시도
check("rate retry", kis.price("RATE") is not None and CALLS["rate"] == 1)
# 만료 토큰 → 재발급
kis._token[0] = "OLD"
check("expired token reissued", kis.price("005930") is not None and CALLS["token"] == 2)

# 하루 분봉 이어 붙이기
dm = kis.day_minutes("005930", "20261008")
check("day minutes full", len(dm) == 391 and dm[0][1] == "0900" and dm[-1][1] == "1530")
check("day minutes sorted unique", len({b[1] for b in dm}) == 391)
check("holiday empty", kis.day_minutes("005930", "20261009") == [])
check("partial today", len(kis.day_minutes("005930", "20261012", "103000")) == 91)

# 추정 가집계
fe = kis.flow_estimate("005930", 10000)
check("estimate latest nonzero row", fe and fe["gb"] == "4" and fe["f"] == 3000 * 10000 and fe["o"] == -1000 * 10000
      and fe["sum"] == 2000 * 10000 and fe["est"])
check("estimate none before entry", kis.flow_estimate("NONE", 10000) is None)

# 종가배팅: 한국투자 분봉
import collect_closing  # noqa: E402

b = collect_closing.kis_bars("005930", "KOSPI", now=dt.datetime(2026, 10, 12, 15, 10, tzinfo=KST))
check("kis_bars", b and b["src"] == "kis" and b["open"] == 10000 and b["close"] == 10500 and 0 < b["lateShare"] <= 1)
check("lateShare 20min", abs(b["lateShare"] - 20 * 100 / 10000) < 1e-9)

# judge_a1 메모에 '장중 추정' 표기
import closing  # noqa: E402

q = {"price": 10500, "pct": 5.0, "value": 2e10, "volume": 1}
r = closing.judge_a1(q, {"high": 10500, "lateShare": 0.2}, 1e9, {"f": 8e8, "o": 2e8, "sum": 1e9, "est": True})
check("a1 est note", r and "장중 추정" in r["note"])

# CK480: 전 거래일 2일(휴장일 건너뜀) + 오늘
import collect_m480  # noqa: E402

bars = collect_m480.kis_fetch_bars("005930", "20261012", now=dt.datetime(2026, 10, 12, 10, 30, tzinfo=KST))
days = sorted({x[0] for x in bars})
check("m480 days", days == ["20261007", "20261008", "20261012"])
check("m480 count", len(bars) == 391 * 2 + 91)
check("m480 sorted", [tuple(x[:2]) for x in bars] == sorted(tuple(x[:2]) for x in bars))
n0 = kis.STATS["calls"]
collect_m480.kis_fetch_bars("005930", "20261012", now=dt.datetime(2026, 10, 12, 11, 0, tzinfo=KST))
check("m480 prev cached", kis.STATS["calls"] - n0 <= 2)
collect_m480.save_kis_cache("20261012")
check("cache saved", json.load(open(os.environ["M480_KIS_CACHE"]))["day"] == "20261012")

# 키가 없으면 꺼짐
del os.environ["KIS_APP_KEY"]
check("disabled without key", not kis.enabled() and collect_closing.kis_bars("005930") is None)

# 로그에 키/토큰이 남지 않음 (STATS 에는 오류 코드만)
check("no secrets in stats", "TOK" not in json.dumps(kis.STATS) and "test-key" not in json.dumps(kis.STATS))
print(f"{ok}/{ok + fail}")
