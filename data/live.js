// 실시간 특징주 탭 데이터 (화면의 새로고침 버튼이 이 파일을 다시 불러옵니다)
// 지금은 모두 화면 확인용 샘플입니다. 나중에 수집 스크립트가 이 파일을 계속 덮어씁니다.
//
// strong / weak 기준(%)은 화면에서 정합니다 (app.js 의 LIVE_STRONG, LIVE_WEAK).
window.DASH = window.DASH || {};
window.DASH.live = {
  sample: true,   // 실제 수집이 연결되면 이 줄은 자동으로 사라집니다
  asOf: "2026-10-05 16:00",   // 데이터가 만들어진 시각 (화면에 그대로 표시되어 얼마나 오래된 값인지 알 수 있음)
  kr: {
    news: [
      { time: "15:42", title: "[특징주] [샘플] 국내 기업 A, 수주 소식에 강세", source: "[샘플] 언론사", url: "#" },
      { time: "15:10", title: "[특징주] [샘플] 국내 기업 B, 실적 우려에 약세", source: "[샘플] 언론사", url: "#" }
    ],
    gainers: [
      { code: "000000", name: "[샘플] 종목 A", price: 12300, changePct: 18.4 },
      { code: "000001", name: "[샘플] 종목 B", price: 8450,  changePct: 11.2 },
      { code: "000002", name: "[샘플] 종목 C", price: 45100, changePct: 7.9 }
    ],
    value: [
      { code: "000003", name: "[샘플] 종목 D", price: 71200, changePct: 2.1,  valueEok: 15230 },
      { code: "000004", name: "[샘플] 종목 E", price: 33500, changePct: -3.5, valueEok: 9810 },
      { code: "000000", name: "[샘플] 종목 A", price: 12300, changePct: 18.4, valueEok: 7420 }
    ],
    themes: [
      { name: "[샘플] 반도체", stocks: [
        { name: "[샘플] 종목 D", changePct: 2.1 }, { name: "[샘플] 종목 F", changePct: 5.3 }, { name: "[샘플] 종목 G", changePct: -2.4 }
      ] },
      { name: "[샘플] 2차전지", stocks: [
        { name: "[샘플] 종목 E", changePct: -3.5 }, { name: "[샘플] 종목 H", changePct: -1.2 }, { name: "[샘플] 종목 I", changePct: 0.3 }
      ] }
    ]
  },
  us: {
    // 미국은 테마별 강약만 표시합니다 (뉴스·순위는 사용하지 않음)
    themes: [
      { name: "[샘플] AI 인프라", stocks: [
        { name: "[샘플] US 종목 C", changePct: 1.4 }, { name: "[샘플] US 종목 J", changePct: 4.8 }, { name: "[샘플] US 종목 K", changePct: -2.9 }
      ] }
    ]
  }
};
