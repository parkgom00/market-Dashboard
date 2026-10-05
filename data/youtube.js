// 3장: 유튜브 최신 영상 요약
// 영상 제목/링크/요약은 자동 수집 후 채워집니다. 지금은 모두 샘플입니다.
// channelId 는 실제 채널 ID(UC로 시작)를 확인해서 넣어주세요.
window.DASH = window.DASH || {};
window.DASH.youtube = {
  sample: true,   // 실제 수집이 연결되면 이 줄은 자동으로 사라집니다
  channels: [
    { name: "815머니톡",        channelId: "", videos: [{ title: "[샘플] 최신 영상 제목", publishedAt: "2026-10-05", url: "#", summary: ["[샘플] 핵심 요약 1", "[샘플] 핵심 요약 2"] }] },
    { name: "올렌도킴 미국주식", channelId: "", videos: [{ title: "[샘플] 최신 영상 제목", publishedAt: "2026-10-05", url: "#", summary: ["[샘플] 핵심 요약 1", "[샘플] 핵심 요약 2"] }] },
    { name: "IT의 신 이형수",    channelId: "", videos: [{ title: "[샘플] 최신 영상 제목", publishedAt: "2026-10-05", url: "#", summary: ["[샘플] 핵심 요약 1", "[샘플] 핵심 요약 2"] }] },
    { name: "경제 사냥꾼",       channelId: "", videos: [{ title: "[샘플] 최신 영상 제목", publishedAt: "2026-10-05", url: "#", summary: ["[샘플] 핵심 요약 1", "[샘플] 핵심 요약 2"] }] }
  ],
  // 채널 간 의견이 엇갈리는 지점 (확증편향 방지용)
  divergences: [
    "[샘플] 채널마다 시각이 갈리는 쟁점을 여기에 따로 모아 보여줍니다."
  ]
};
