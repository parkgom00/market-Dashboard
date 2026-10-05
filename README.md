# 마켓 대시보드

카카오톡에서 링크로 여는 모바일 대시보드입니다. 6개 탭으로 구성됩니다.

| 탭 | 내용 | 데이터 파일 |
|---|---|---|
| 캘린더 | 휴장, 경제지표, 실적발표, 주요 이벤트 | `data/calendar.js` |
| 미국장 | 전날 지수, 이슈, 특징주, 국내 연관주 | `data/usmarket.js` |
| 특징주 | 국내: [특징주] 뉴스 · 등락률 상위 · 거래대금 상위 · 테마별 강약 / 미국: 테마별 강약만 (새로고침 버튼) | `data/live.js` |
| 유튜브 | 채널별 최신 영상 요약 | `data/youtube.js` |
| 중장기 | 240일선·480일선 등 조건 충족 종목 (국내/미국) | `data/longterm.js` |
| 단기 | 유형별 단기 트레이딩 조건 충족 종목 (국내/미국) | `data/shortterm.js` |

현재 모든 데이터는 **화면 확인용 샘플**입니다. 실제 시세와 일정이 아닙니다.

## 주소

https://parkgom00.github.io/market-Dashboard/ (GitHub Pages, main 브랜치에 푸시하면 1~2분 뒤 반영)

## 지금 확인하는 방법

`index.html` 을 더블클릭하면 브라우저에서 열립니다. 서버가 필요 없습니다.
특정 탭으로 바로 열려면 주소 뒤에 `#us`, `#live`, `#youtube`, `#long`, `#short` 를 붙이세요.

## 데이터를 바꾸는 방법

`data/` 폴더의 파일은 화면과 분리되어 있습니다. 나중에 자동 수집 스크립트가 이 파일들만 새로 써 주면 화면은 그대로 최신 내용으로 바뀝니다.
`data/meta.js` 의 `isSample` 을 `false` 로 바꾸면 상단의 샘플 배너가 사라집니다.

## 규칙 추가 위치

- 4장: `data/longterm.js` 의 `rules` 에 규칙을 적고, 스캐너가 `items` 를 채웁니다.
- 5장: `data/shortterm.js` 의 `types` 에 유형을 하나씩 추가합니다. 각 유형에 `timeframe` (일봉 또는 1분봉) 을 표시합니다.

## 공유할 때 주의

- 주소를 아는 사람은 누구나 볼 수 있습니다. 페이지에는 검색 제외(noindex) 표시를 넣어 두었지만 접근 제한은 아닙니다.
- 화면 문구는 "추천"이 아니라 "조건 충족 종목" 입니다. 공유 범위를 넓히거나 유료화할 계획이라면 관련 규제를 먼저 확인하세요.

## 4장 스캐너 실행 (사용자 PC에서)

```
cd scanner
pip install -r requirements.txt
python test_rules.py          # 규칙 판정 검증 (합성 차트, 인터넷 불필요)
python run_scan.py --market kr --limit 30   # 국내 30종목만 시험
python run_scan.py --market kr              # 국내 전 종목 (장 마감 후)
python run_scan.py --market us              # 미국 (S&P 500, 미국장 마감 후)
```

결과는 `data/longterm.js` 로 저장되고 대시보드 4장에 표시됩니다.
규칙의 숫자 기준(이평선 터치 허용 폭, 급등 기준 %, 거래량 배수 등)은 `scanner/config.py` 에서 바꿉니다.
국내/미국 데이터는 각각 FinanceDataReader, yfinance 를 사용하며, 이 코드는 아직 실제 데이터로 시험하지 못했습니다.

## 특징주 탭: [특징주] 뉴스 수집 (네이버 검색 API)

1. https://developers.naver.com 에서 애플리케이션을 등록하고 '검색' API를 선택해 Client ID/Secret 을 발급받습니다.
2. 환경변수 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 에 넣습니다 (코드나 파일에 직접 적지 마세요).
3. `cd scanner && python fetch_news.py` → `data/live.js` 가 갱신됩니다. 제목과 원문 링크만 저장합니다.
4. `python test_news.py` 로 파싱 로직을 인터넷 없이 검증할 수 있습니다.

`data/live.js` 는 `scanner/build_live.py` 가 `scanner/out/` 의 조각 파일을 합쳐 만듭니다.
조각이 없는 항목(등락률·거래대금·테마)은 화면에서 숨겨집니다. 이 항목들의 수집기는 아직 없습니다.
이 코드는 실제 네이버 API 로는 아직 시험하지 못했습니다.

## 다음 단계

1. 4장 규칙 입력 → 일봉 스캐너(pykrx, yfinance 등)로 `longterm.js` 자동 생성
2. 2장 테마 연결표 작성 → 미국 특징주와 국내 연관주 자동 연결
3. GitHub Pages 등에 올려 카카오톡용 URL 만들기, 스케줄러로 매일 갱신
4. 1장 일정, 3장 유튜브 자동 수집
5. 5장 단기 유형별 규칙 입력
