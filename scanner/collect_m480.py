"""단기 유형 C '480분선 지지' (1분봉 기준, 10:00~12:00 사이 30분 간격으로 갱신).

찾는 모양: 오늘 장중에 전일 종가 대비 +15% 이상 올랐던 종목이 1분봉 480분 이동평균선 근처까지 내려왔지만
그 선을 이탈하지 않고 몇 분째 옆으로 기는(횡보) 상태.

동작: 워크플로가 09:00 무렵부터 2~3분마다 이 스크립트를 부른다.
  · 부를 때마다 네이버 실시간 시세를 받아 '많이 오른 종목'을 감시 목록에 쌓아 두고 (깃허브 실행기의 임시 파일),
  · 10:00, 10:30, 11:00, 11:30, 12:00 이 지나면 그 회차에 한 번, 후보들의 1분봉을 받아 판정해 저장한다.
480분선은 정규장(09:00~15:30) 1분봉 종가 480개의 평균이라 전 거래일 분봉까지 이어서 계산한다.
숫자 기준은 아래 상수이며, 말로 정해지지 않은 부분은 제가 정한 기본값이다.
"""
import datetime as dt
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KST = dt.timezone(dt.timedelta(hours=9))
STATE = os.environ.get("M480_STATE", "/tmp/m480_watch.json")
MARK = os.environ.get("M480_MARK", "/tmp/m480_reported")
MIN_URL = "https://api.stock.naver.com/chart/domestic/item/{code}/minute?startDateTime={a}&endDateTime={b}"

SLOTS = ("10:00", "10:30", "11:00", "11:30", "12:00")
RISE_PCT = 15.0        # 오늘 장중 고가가 전일 정규장 종가 대비 +15% 이상
MA_N = 480             # 1분봉 480개 평균
NEAR_ABOVE = 0.015     # 현재가가 480분선 위 1.5% 이내 ('부근')
NEAR_BELOW = 0.005     # 현재가가 480분선 아래 0.5% 까지는 '이탈 아님'으로 봄
BREAK_TOL = 0.01       # 횡보 구간의 저가가 480분선 아래로 1% 넘게 내려간 적이 있으면 이탈
MIN_PULLBACK = 0.03    # 고가 대비 3% 이상 내려온 상태
SIDE_WINDOW = 20       # 횡보를 살피는 최대 구간(분)
SIDE_MIN = 3           # 최소 3분 이상 옆으로 기어야 함
SIDE_BAND = 0.012      # 그 구간의 고저폭이 현재가의 1.2% 이내
WATCH_PCT = 12.0       # 실시간 시세에서 +12% 이상인 종목은 감시 목록에 올림 (분봉으로 +15% 여부를 다시 확인)
ALT_PCT, ALT_VALUE = 5.0, 3e9    # 감시 목록에 없어도 지금 +5% 이상·거래대금 30억 이상이면 후보에 넣어 확인
MAX_CANDS = 250
TOP_N = 15


def parse_minutes(rows):
    """네이버 1분봉 → 정규장(09:00~15:30) 봉만 [(날짜YYYYMMDD, HHMM, 시, 고, 저, 종, 거래량)] (시간순)."""
    out = []
    for r in rows or []:
        try:
            t = str(r["localDateTime"])
            hm = t[8:12]
            if not ("0900" <= hm <= "1530"):
                continue
            out.append((t[:8], hm, float(r["openPrice"]), float(r["highPrice"]), float(r["lowPrice"]), float(r["currentPrice"]),
                        float(r.get("accumulatedTradingVolume") or 0)))
        except (KeyError, TypeError, ValueError):
            continue
    out.sort()
    return out


def judge(bars, today, upto=None):
    """bars: parse_minutes 결과. today: 'YYYYMMDD'. upto: 'HHMM' 이면 그 시각까지만 본다(재현용).
    해당하면 설명 dict, 아니면 (None, 사유)."""
    if upto:
        bars = [b for b in bars if b[0] < today or b[1] <= upto]
    td = [b for b in bars if b[0] == today]
    prev = [b for b in bars if b[0] < today]
    if len(td) < 20 or not prev:
        return None, "오늘 분봉 부족"
    if len(bars) < MA_N:
        return None, "480분선 계산 자료 부족"
    prev_close = prev[-1][5]
    hi_i = max(range(len(td)), key=lambda i: td[i][3])
    day_high = td[hi_i][3]
    rise = (day_high / prev_close - 1) * 100 if prev_close else 0
    if rise < RISE_PCT:
        return None, "장중 +15% 미달"
    closes = [b[5] for b in bars]
    ma = sum(closes[-MA_N:]) / MA_N
    price = td[-1][5]
    if price > ma * (1 + NEAR_ABOVE):
        return None, "480분선보다 아직 높음"
    if price < ma * (1 - NEAR_BELOW):
        return None, "480분선 이탈"
    if 1 - price / day_high < MIN_PULLBACK:
        return None, "고가에서 덜 내려옴"
    # 횡보 길이: 지금부터 거꾸로, 고저폭이 SIDE_BAND 안에 머문 분 수
    hi = lo = None
    side = 0
    for b in reversed(td[-SIDE_WINDOW:]):
        h2 = b[3] if hi is None else max(hi, b[3])
        l2 = b[4] if lo is None else min(lo, b[4])
        if (h2 - l2) / price > SIDE_BAND:
            break
        hi, lo, side = h2, l2, side + 1
    if side < SIDE_MIN:
        return None, "횡보 아님"
    if lo < ma * (1 - BREAK_TOL):
        return None, "횡보 중 480분선 이탈"
    if len(td) - 1 - hi_i < side:          # 고가가 횡보 구간 안에 있으면 아직 내려온 게 아님
        return None, "고가 직후"
    return {"rise": round(rise, 1), "high": day_high, "highAt": td[hi_i][1][:2] + ":" + td[hi_i][1][2:], "prevClose": prev_close,
            "ma": ma, "price": price, "gap": round((price / ma - 1) * 100, 2), "pull": round((1 - price / day_high) * 100, 1),
            "side": side, "band": round((hi - lo) / price * 100, 2), "pct": round((price / prev_close - 1) * 100, 2),
            "lastAt": td[-1][1][:2] + ":" + td[-1][1][2:]}, ""


def note(d):
    return (f"장중 고가 +{d['rise']}%({d['highAt']}) → 고가 대비 -{d['pull']}% 내려와 480분선({d['ma']:,.0f}) 대비 {d['gap']:+.2f}% · "
            f"{d['side']}분{'+' if d['side'] >= SIDE_WINDOW else ''}째 횡보(고저폭 {d['band']}%) · {d['lastAt']} 기준")


def due_slot(now, last_slot):
    """지금 판정해야 할 회차(가장 최근에 지난 회차). 이미 한 회차면 None."""
    hm = now.strftime("%H:%M")
    passed = [s for s in SLOTS if s <= hm]
    if not passed or hm > "12:20":
        return None
    return passed[-1] if passed[-1] != last_slot else None


def fetch_bars(code, today, days_back=5):
    import naver_live
    a = (dt.datetime.strptime(today, "%Y%m%d") - dt.timedelta(days=days_back)).strftime("%Y%m%d") + "0900"
    try:
        return parse_minutes(naver_live._get(MIN_URL.format(code=code, a=a, b=today + "1600"), tries=2))
    except Exception:
        return []


def evaluate(cands, uni, today, sectors=None, upto=None, fetch=fetch_bars):
    """cands: 종목코드 목록. 반환: (화면용 목록, 진단)."""
    with ThreadPoolExecutor(6) as ex:
        bars = dict(zip(cands, ex.map(lambda c: fetch(c, today), cands)))
    rows, why = [], {}
    for c in cands:
        d, reason = judge(bars.get(c) or [], today, upto)
        if not d:
            why[reason] = why.get(reason, 0) + 1
            continue
        u = uni.get(c, {})
        rows.append({"code": c, "name": u.get("name", c), "market": u.get("market", ""), "sector": (sectors or {}).get(c, ""),
                     "marcap": round(u["marcap"] / 1e8) if u.get("marcap") else 0, "value": round(u["value"] / 1e8) if u.get("value") else 0,
                     "prevClose": d["prevClose"], "close": d["price"], "changePct": d["pct"], "note": note(d), "_rise": d["rise"]})
    rows.sort(key=lambda x: -x["_rise"])
    return [{k: v for k, v in x.items() if k != "_rise"} for x in rows[:TOP_N]], {"후보": len(cands), "분봉": sum(1 for b in bars.values() if b), "사유": why}


def load_state(today):
    try:
        with open(STATE, encoding="utf-8") as f:
            s = json.load(f)
        if s.get("day") == today:
            return s
    except Exception:
        pass
    return {"day": today, "watch": [], "slot": ""}


def main(force=False):
    import naver_live
    import shortterm_build
    now = dt.datetime.now(KST)
    today = now.strftime("%Y%m%d")
    hm = now.strftime("%H:%M")
    if not force and not (now.weekday() < 5 and "08:55" <= hm <= "12:20"):
        print("시간대 밖", hm)
        return
    uni, _ = naver_live.fetch_universe()
    days = [u.get("day") for u in uni.values() if u.get("day")]
    if days and sum(1 for d in days if d == now.strftime("%Y-%m-%d")) / len(days) < 0.4:
        print("휴장일로 보여 건너뜀")
        return
    st = load_state(today)
    watch = set(st["watch"]) | {c for c, u in uni.items() if (u.get("pct") or 0) >= WATCH_PCT}
    st["watch"] = sorted(watch)
    slot = due_slot(now, st.get("slot", "")) or ("강제" if force else None)
    if slot:
        alt = [c for c, u in uni.items() if (u.get("pct") or 0) >= ALT_PCT and (u.get("value") or 0) >= ALT_VALUE]
        cands = sorted(watch | set(alt), key=lambda c: -(uni.get(c, {}).get("value") or 0))[:MAX_CANDS]
        sectors = {}
        try:
            with open(os.path.join(OUT, "kr_sector.json"), encoding="utf-8") as f:
                sectors = json.load(f).get("map", {})
        except Exception:
            pass
        rows, diag = evaluate(cands, uni, today, sectors)
        payload = {"asOf": now.strftime("%Y-%m-%d %H:%M"), "slot": slot, "kr": rows, "diag": diag,
                   "status": f"감시 {len(watch)}개 포함 후보 {diag['후보']}개 점검 → {len(rows)}개 해당"}
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, "m480_kr.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        shortterm_build.build()
        st["slot"] = slot
        open(MARK, "w").write(slot)
        print("판정 완료", slot, payload["status"], diag)
    else:
        print(f"{hm} 감시 목록 {len(watch)}개 (다음 회차 대기)")
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f)


if __name__ == "__main__":
    main(force="--force" in sys.argv)
