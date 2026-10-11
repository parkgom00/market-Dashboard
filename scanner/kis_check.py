"""한국투자 API 연결 확인 (수동 실행용). 키·토큰은 출력하지 않고, 받아온 자료의 개수와 오류 코드만 보여준다."""
import datetime as dt
import json
import os

import kis

KST = dt.timezone(dt.timedelta(hours=9))
now = dt.datetime.now(KST)
R = {}
_p = print


def print(*a):
    _p(*a)
    R[str(a[0])] = " ".join(str(x) for x in a[1:])


print("키 등록:", "예" if kis.enabled() else "아니오 (Secrets 에 KIS_APP_KEY / KIS_APP_SECRET 필요)")
if kis.enabled():
    print("토큰 발급:", "성공" if kis.token() else "실패")
    p = kis.price("005930")
    print("삼성전자 현재가:", p and {k: p[k] for k in ("price", "pct", "volume")})
    m = kis.recent_minutes("005930", min(now.strftime("%H%M%S"), "153000"))
    print("최근 1분봉:", len(m), "개", m[-1][:2] if m else "")
    d, n = now - dt.timedelta(days=1), 0
    for _ in range(7):
        if d.weekday() < 5:
            n = len(kis.day_minutes("005930", d.strftime("%Y%m%d")))
            if n:
                break
        d -= dt.timedelta(days=1)
    print("직전 거래일 분봉:", d.strftime("%Y%m%d"), n, "개 (정상 391개)")
    if n:
        dm = kis.day_minutes("005930", d.strftime("%Y%m%d"))
        hs = [b[1] for b in dm]
        t, miss = dt.datetime(2000, 1, 1, 9, 0), []
        while t.strftime("%H%M") <= "1530":
            if t.strftime("%H%M") not in hs:
                miss.append(t.strftime("%H%M"))
            t += dt.timedelta(minutes=1)
        print("빠진 분:", ",".join(miss))
        print("마지막 봉:", dm[-1])
        r = kis.get("/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice", "FHKST03010230",
                    {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": "005930", "FID_INPUT_HOUR_1": "160000",
                     "FID_INPUT_DATE_1": d.strftime("%Y%m%d"), "FID_PW_DATA_INCU_YN": "N", "FID_FAKE_TICK_INCU_YN": ""})
        o2 = (r or {}).get("output2") or []
        print("160000 요청 첫 3개:", [(x.get("stck_bsop_date"), x.get("stck_cntg_hour"), x.get("stck_prpr")) for x in o2[:3]])
        print("output1 전일종가/현재가:", {k: (r or {}).get("output1", {}).get(k) for k in ("stck_prdy_clpr", "stck_prpr")})
    fe = kis.flow_estimate("005930", p["price"] if p else 0)
    print("외국인·기관 추정 가집계:", "자료 있음 (입력구분 " + fe["gb"] + ")" if fe else "없음 (장중 09:30 이후 입력됨)")
    print("호출 통계:", kis.STATS)

R["asOf"] = now.strftime("%Y-%m-%d %H:%M")
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"), exist_ok=True)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "kis_check.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
