// 1장: 마켓 캘린더
// type: holiday(휴장) | econ(경제지표) | earnings(실적발표) | event(주요 이벤트)
// market: KR | US
window.DASH = window.DASH || {};
window.DASH.calendar = {
  events: [
    { date: "2026-10-05", type: "holiday",  market: "KR", title: "개천절 대체공휴일 (휴장, 확인 필요)" },
    { date: "2026-10-09", type: "holiday",  market: "KR", title: "한글날 (휴장, 확인 필요)" },
    { date: "2026-10-13", type: "econ",     market: "US", title: "[샘플] 미국 소비자물가지수(CPI) 발표" },
    { date: "2026-10-15", type: "earnings", market: "US", title: "[샘플] 대형 은행주 실적 발표" },
    { date: "2026-10-16", type: "event",    market: "KR", title: "[샘플] 옵션 만기일" },
    { date: "2026-10-21", type: "earnings", market: "US", title: "[샘플] 대형 기술주 실적 발표" },
    { date: "2026-10-28", type: "econ",     market: "US", title: "[샘플] FOMC 결과 발표" },
    { date: "2026-10-28", type: "earnings", market: "KR", title: "[샘플] 국내 대형주 실적 발표" }
  ]
};
