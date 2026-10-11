"""한국투자 API 연결 확인 (수동 실행용). 키·토큰은 출력하지 않고, 받아온 자료의 개수와 오류 코드만 보여준다."""
import datetime as dt

import kis

KST = dt.timezone(dt.timedelta(hours=9))
now = dt.datetime.now(KST)
print("키 등록:", "예" if kis.enabled() else "아니오 (Secrets 에 KIS_APP_KEY / KIS_APP_SECRET 필요)")
if kis.enabled():
    print("토큰 발급:", "성공" if kis.token() else "실패")
    p = kis.price("005930")
    print("삼성전자 현재가:", p and {k: p[k] for k in ("price", "pct", "volume")})
    m = kis.recent_minutes("005930", min(now.strftime("%H%M%S"), "153000"))
    print("최근 1분봉:", len(m), "개", m[-1][:2] if m else "")
    d = now - dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    print("직전 평일 분봉:", d.strftime("%Y%m%d"), len(kis.day_minutes("005930", d.strftime("%Y%m%d"))), "개")
    fe = kis.flow_estimate("005930", p["price"] if p else 0)
    print("외국인·기관 추정 가집계:", "자료 있음 (입력구분 " + fe["gb"] + ")" if fe else "없음 (장중 09:30 이후 입력됨)")
    print("호출 통계:", kis.STATS)
