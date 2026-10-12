"""한국투자증권(KIS) Open API 시세 조회 (실전 서버, 조회 전용 — 주문 기능은 쓰지 않음).

키는 깃허브 Secrets 의 KIS_APP_KEY / KIS_APP_SECRET 환경변수로만 받는다. 키·토큰은 절대 화면(로그)에 찍지 않는다.
키가 없거나 호출이 실패하면 각 함수는 None / 빈 값을 돌려주고, 부르는 쪽은 네이버 자료로 대신한다.

- 접근토큰: 하루 유효. 발급할 때마다 한국투자 알림톡이 가므로, 같은 실행기(작업) 안에서는
  /tmp 파일에 저장해 두고 다시 쓴다 (작업이 끝나면 실행기와 함께 사라짐, 저장소에는 올라가지 않음).
- 초당 호출 한도(실전 20건)를 넘지 않게 전역으로 간격을 둔다.
"""
import datetime as dt
import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://openapi.koreainvestment.com:9443"
KST = dt.timezone(dt.timedelta(hours=9))
TOKEN_FILE = os.environ.get("KIS_TOKEN_FILE", "/tmp/kis_token.json")
MIN_GAP = 1 / 15          # 초당 15건 이하로 시작
MAX_GAP = 0.5             # 한도 초과가 나면 간격을 늘려 감 (신규 앱키는 한도가 더 낮을 수 있음)
STATS = {"calls": 0, "ok": 0, "err": {}}   # 진단용 (키·토큰 없음)

_lock = threading.Lock()
_last = [0.0]
_token = [None]
_gap = [MIN_GAP]


def enabled():
    return bool(os.environ.get("KIS_APP_KEY") and os.environ.get("KIS_APP_SECRET"))


def _err(tag):
    STATS["err"][tag] = STATS["err"].get(tag, 0) + 1


def _http(req, timeout=15):
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def token(force=False):
    """접근토큰. 실패하면 None."""
    if not enabled():
        return None
    if _token[0] and not force:
        return _token[0]
    if not force:
        try:
            with open(TOKEN_FILE, encoding="utf-8") as f:
                t = json.load(f)
            if t.get("exp", 0) - time.time() > 600:
                _token[0] = t["token"]
                return _token[0]
        except Exception:
            pass
    body = json.dumps({"grant_type": "client_credentials", "appkey": os.environ["KIS_APP_KEY"],
                       "appsecret": os.environ["KIS_APP_SECRET"]}).encode()
    try:
        res = _http(urllib.request.Request(BASE + "/oauth2/tokenP", data=body, method="POST",
                                           headers={"content-type": "application/json; charset=utf-8"}))
        tok = res.get("access_token")
        if not tok:
            _err("token:" + str(res.get("error_code") or res.get("msg_cd") or "empty"))
            return None
        exp = time.time() + int(res.get("expires_in") or 86400)
        try:
            fd = os.open(TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w") as f:
                json.dump({"token": tok, "exp": exp}, f)
        except Exception:
            pass
        _token[0] = tok
        return tok
    except urllib.error.HTTPError as e:
        _err(f"token:http{e.code}")
    except Exception as e:
        _err("token:" + type(e).__name__)
    return None


def get(path, tr_id, params, tries=3):
    """GET 조회 → 응답 dict (rt_cd == '0') 또는 None."""
    tok = token()
    if not tok:
        return None
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        with _lock:                       # 전역 호출 간격
            wait = _last[0] + _gap[0] - time.time()
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        STATS["calls"] += 1
        hdr = {"content-type": "application/json; charset=utf-8", "authorization": "Bearer " + tok,
               "appkey": os.environ["KIS_APP_KEY"], "appsecret": os.environ["KIS_APP_SECRET"],
               "tr_id": tr_id, "custtype": "P"}
        try:
            res = _http(urllib.request.Request(url, headers=hdr))
        except urllib.error.HTTPError as e:
            try:
                res = json.loads(e.read().decode())
            except Exception:
                _err(f"{tr_id}:http{e.code}")
                time.sleep(0.5 * (i + 1))
                continue
        except Exception as e:
            _err(f"{tr_id}:{type(e).__name__}")
            time.sleep(0.5 * (i + 1))
            continue
        if str(res.get("rt_cd")) == "0":
            STATS["ok"] += 1
            return res
        code = str(res.get("msg_cd") or "?")
        _err(f"{tr_id}:{code}")
        if code == "EGW00201":            # 초당 거래건수 초과 → 간격을 넓히고 잠깐 쉬고 다시
            with _lock:
                _gap[0] = min(MAX_GAP, _gap[0] * 1.5)
            STATS["gap"] = round(_gap[0], 3)
            time.sleep(1.0 + i)
            continue
        if code in ("EGW00123", "EGW00121"):   # 토큰 만료/무효 → 새로 발급
            tok = token(force=True)
            if not tok:
                return None
            continue
        return None
    return None


def _f(v):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


# ───────────── 현재가 ─────────────
def price(code):
    """{open, high, low, price, volume, value, pct} (KRX 정규장) 또는 None."""
    r = get("/uapi/domestic-stock/v1/quotations/inquire-price", "FHKST01010100",
            {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": code})
    o = (r or {}).get("output") or {}
    p = _f(o.get("stck_prpr"))
    if not p:
        return None
    return {"open": _f(o.get("stck_oprc")), "high": _f(o.get("stck_hgpr")), "low": _f(o.get("stck_lwpr")), "price": p,
            "volume": _f(o.get("acml_vol")) or 0, "value": _f(o.get("acml_tr_pbmn")) or 0, "pct": _f(o.get("prdy_ctrt"))}


# ───────────── 분봉 ─────────────
def _minute_rows(out2):
    rows = []
    for b in out2 or []:
        d, t = str(b.get("stck_bsop_date") or ""), str(b.get("stck_cntg_hour") or "")
        c = _f(b.get("stck_prpr"))
        if len(d) != 8 or len(t) < 4 or not c:
            continue
        rows.append((d, t[:4], _f(b.get("stck_oprc")) or c, _f(b.get("stck_hgpr")) or c, _f(b.get("stck_lwpr")) or c, c,
                     _f(b.get("cntg_vol")) or 0.0))
    return rows


def recent_minutes(code, hhmmss):
    """오늘 hhmmss 까지의 최근 1분봉 최대 30개 [(날짜, HHMM, 시, 고, 저, 종, 거래량)] (시간순)."""
    r = get("/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice", "FHKST03010200",
            {"FID_ETC_CLS_CODE": "", "FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": code,
             "FID_INPUT_HOUR_1": hhmmss, "FID_PW_DATA_INCU_YN": "N"})
    return sorted(_minute_rows((r or {}).get("output2")))


def day_minutes(code, yyyymmdd, until="153000"):
    """그날 09:00~until 정규장 1분봉 전부 (한 번에 120개씩 거꾸로 받아 이어 붙임). 그날 자료가 없으면 []."""
    got, hour = {}, until
    for _ in range(5):                    # 391개 = 120 × 4 이면 충분
        r = get("/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice", "FHKST03010230",
                {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": code, "FID_INPUT_HOUR_1": hour,
                 "FID_INPUT_DATE_1": yyyymmdd, "FID_PW_DATA_INCU_YN": "N", "FID_FAKE_TICK_INCU_YN": ""})
        rows = [b for b in _minute_rows((r or {}).get("output2")) if b[0] == yyyymmdd and "0900" <= b[1] <= "1530"]
        new = [b for b in rows if b[1] not in got]
        if not new:
            break
        for b in new:
            got[b[1]] = b
        first = min(b[1] for b in new)
        if first <= "0900":
            break
        t = dt.datetime.strptime(first, "%H%M") - dt.timedelta(minutes=1)
        hour = t.strftime("%H%M") + "00"
    return [got[k] for k in sorted(got)]


def recent_day_has_data(code, yyyymmdd):
    """그날 정규장 분봉이 있는지(휴장일 확인용, 1회 호출)."""
    r = get("/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice", "FHKST03010230",
            {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": code, "FID_INPUT_HOUR_1": "153000",
             "FID_INPUT_DATE_1": yyyymmdd, "FID_PW_DATA_INCU_YN": "N", "FID_FAKE_TICK_INCU_YN": ""})
    return any(b[0] == yyyymmdd for b in _minute_rows((r or {}).get("output2")))


def daily_closes(code, start, end):
    """일봉 정규장 종가 {YYYYMMDD: 종가} (수정주가). 실패하면 {}."""
    r = get("/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice", "FHKST03010100",
            {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": code, "FID_INPUT_DATE_1": start, "FID_INPUT_DATE_2": end,
             "FID_PERIOD_DIV_CODE": "D", "FID_ORG_ADJ_PRC": "0"})
    out = {}
    for row in (r or {}).get("output2") or []:
        d, c = str(row.get("stck_bsop_date") or ""), _f(row.get("stck_clpr"))
        if len(d) == 8 and c:
            out[d] = c
    return out


def day_minutes_closed(code, yyyymmdd, close):
    """지난 거래일 정규장 분봉. 한국투자 분봉에는 15:20 이후 동시호가 체결 봉이 빠져 있어,
    15:30 봉을 그날 정규장 종가로 하나 붙인다 (480분선의 마지막 값과 '전일 종가'가 맞도록)."""
    bars = day_minutes(code, yyyymmdd)
    if bars and close and bars[-1][1] < "1530":
        bars.append((yyyymmdd, "1530", close, close, close, close, 0.0))
    return bars


# ───────────── 외국인·기관 장중 추정 가집계 ─────────────
def flow_estimate(code, price_now):
    """오늘 장중 추정 순매수 → {"sum","f","o"}(원, 수량×현재가), "est": True, "gb": 입력구분} 또는 None (아직 입력 전)."""
    r = get("/uapi/domestic-stock/v1/quotations/investor-trend-estimate", "HHPTJ04160200", {"MKSC_SHRN_ISCD": code})
    best = None
    for row in (r or {}).get("output2") or []:
        f, o = _f(row.get("frgn_fake_ntby_qty")), _f(row.get("orgn_fake_ntby_qty"))
        if f is None and o is None:
            continue
        if not (f or o):
            continue
        gb = str(row.get("bsop_hour_gb") or "")
        if best is None or gb > best[0]:
            best = (gb, f or 0.0, o or 0.0)
    if not best or not price_now:
        return None
    gb, f, o = best
    return {"sum": (f + o) * price_now, "f": f * price_now, "o": o * price_now, "est": True, "gb": gb}


def flow_estimates(cands):
    """cands: {code: 현재가} → {code: dict 또는 None}. 순서대로 부르며 전역 간격을 지킨다."""
    return {c: flow_estimate(c, p) for c, p in cands.items()}
