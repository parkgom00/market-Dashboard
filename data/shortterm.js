// 5장: 단기 트레이딩
// types 는 사용자가 유형별로 규칙을 알려줄 때마다 하나씩 추가합니다.
// timeframe: "일봉" | "1분봉" (1분봉은 실시간 연동이 필요해서 2차 단계)
window.DASH = window.DASH || {};
window.DASH.shortterm = {
  types: [
    {
      id: "A",
      name: "유형 A (규칙 입력 대기)",
      timeframe: "일봉",
      desc: "책 내용을 정리해서 알려주시면 이 유형의 조건이 여기에 표시됩니다.",
      kr: [
        { code: "000000", name: "[샘플] 국내 종목 A", close: 0, changePct: 0.0, note: "[샘플] 조건 충족 사유 메모" }
      ],
      us: []
    },
    {
      id: "B",
      name: "유형 B (규칙 입력 대기)",
      timeframe: "일봉",
      desc: "",
      kr: [],
      us: []
    }
  ]
};
