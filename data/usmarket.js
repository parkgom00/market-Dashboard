// 2장: 전날 미국장 정리 + 특징주 + 국내 연관주
// 숫자와 설명은 모두 화면 확인용 샘플입니다.
// krStocks 는 '테마 연결표(data/theme_map.js, 추후 추가)'를 근거로 채우는 것을 권장합니다.
window.DASH = window.DASH || {};
window.DASH.usmarket = {
  asOf: "2026-10-02 (금) 미국 정규장 기준",
  indices: [
    { name: "나스닥",   close: 0, changePct: 0.0 },
    { name: "S&P 500", close: 0, changePct: 0.0 },
    { name: "다우",     close: 0, changePct: 0.0 }
  ],
  summary: [
    "[샘플] 여기에 전날 미국장 핵심 이슈 3~5줄이 들어갑니다.",
    "[샘플] 금리·환율·주요 경제지표 등 시장 분위기를 한눈에 보여줍니다."
  ],
  themes: [
    {
      name: "[샘플] 반도체 / AI 인프라",
      changePct: 0.0,
      why: "[샘플] 해당 테마가 오른 이유를 한두 문장으로 설명합니다.",
      usStocks: [
        { ticker: "NVDA", name: "엔비디아", changePct: 0.0 },
        { ticker: "AVGO", name: "브로드컴", changePct: 0.0 }
      ],
      krStocks: [
        { code: "000000", name: "[샘플] 국내 연관주 A", link: "미국 대표주와 같은 공급망에 속한 이유를 간략히 설명합니다." },
        { code: "000001", name: "[샘플] 국내 연관주 B", link: "연결 근거(납품 관계, 동일 업황 등)를 적습니다." }
      ]
    }
  ]
};
