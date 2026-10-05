# 마켓 대시보드

카카오톡에서 링크로 여는 모바일 대시보드입니다. 6개 탭으로 구성됩니다.

| 탭 | 내용 | 데이터 파일 |
|---|---|---|
| 캘린더 | 휴장, 경제지표, 실적발표, 주요 이벤트 | `data/calendar.js` |
| 미국장 | 전날 지수, 이슈, 특징주, 국내 연관주 | `data/usmarket.js` |
| 특징주 | 국내: 등락률 상위 · 거래대금 상위 (처음 10위, 더보기로 20위) · 테마별 강약 / 미국: 테마별 강약만 (새로고침 버튼) | `data/live.js` |
| 유튜브 | 채널별 최신 영상 목록 + 재미나이 요약 버튼 | `data/youtube.js` |
| 중장기 | 240일선·480일선 등 조건 충족 종목 (국내/미국) | `data/longterm.js` |
| 단기 | 유형별 단기 트레이딩 조건 충족 종목 (국내/미국) | `data/shortterm.js` |

## 데이터 연결 상태

| 탭 | 상태 |
|---|---|
| 캘린더 | 공식 일정(FOMC·CPI·PCE·고용) + 휴장일 + 발표 후 결과 + 대표 기업 실적 예정일 (자동 수집분은 첫 실행 대기, 미확인) |
| 미국장 | 지수·테마 등락 **연결됨**, 이슈 요약 문장은 AI 요약 단계 필요(미연결) |
| 특징주 | 국내 등락률·거래대금·테마 강약 **동작 확인됨**(2026-10-05 첫 자동 실행), 미국 테마 연결됨(미확인) |
| 유튜브 | 영상 목록·링크 + 재미나이 요약 버튼 (첫 자동 실행 대기, 미확인) |
| 중장기 | 국내 **동작 확인됨**(2,711종목 스캔), 미국은 첫 실행 대기 |
| 단기 | 규칙 대기 (샘플) |

샘플인 탭에는 화면 위쪽에 "샘플 데이터" 안내가 표시됩니다 (`data/*.js` 의 `sample: true`).

## 자동 갱신 (GitHub Actions)

`.github/workflows/` 의 일정에 따라 GitHub 서버가 수집 코드를 돌리고, 바뀐 `data/` 파일을 저장하면 사이트가 1~2분 안에 반영됩니다.

| 워크플로 | 실행 시각 (한국시간) | 하는 일 |
|---|---|---|
| kr-intraday | 평일 09:00~16:00, 20분마다 | 국내 등락률·거래대금·테마 강약, 뉴스 |
| kr-close | 평일 16:30 | 위 + 중장기 국내 전 종목 스캔 |
| us-close | 평일(미국 장 마감 후) 07:30 | 미국 지수·테마, 중장기 미국 스캔 |
| calendar | 6시간마다 | 캘린더, 지표 결과(FRED), 대표 기업 실적 예정일 |
| youtube | 3시간마다 | 유튜브 최신 영상 목록 (키 불필요) |

GitHub 의 정기 실행은 몇 분씩 늦어질 수 있습니다. 직접 돌리려면 저장소의 Actions 탭 → 워크플로 선택 → Run workflow.
저장소에 활동이 60일 동안 없으면 GitHub 이 정기 실행을 멈출 수 있습니다.

## 비밀 키 등록 (GitHub Secrets)

저장소 Settings → Secrets and variables → Actions → New repository secret 에 등록합니다. 파일에는 절대 적지 마세요.
등록해 둔 비밀 키: `GEMINI_API_KEY` (유튜브 AI 요약, 미국장 AI 브리핑). 없으면 AI 요약만 건너뛰고 나머지는 그대로 동작합니다.
제미나이 키는 https://aistudio.google.com/apikey 에서 무료로 발급하며, GitHub 저장소 Settings → Secrets and variables → Actions → New repository secret 에 등록합니다.

## 테마 연결표 (`scanner/theme_map.json`)

미국 종목 → 국내 연관주 연결과 테마 구성은 이 파일 하나로 관리합니다. **지금 내용은 초안입니다.** 틀린 연결은 지우고 빠진 종목은 추가하세요.

## 일정 직접 추가 (`scanner/calendar_manual.json`)

```
[{"date": "2026-10-21", "type": "earnings", "market": "US", "title": "테슬라 실적 발표"}]
```
type: `holiday`(휴장) `econ`(경제지표) `earnings`(실적) `event`(이벤트) / market: `KR` `US`

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
python test_collect.py        # 수집·캘린더 로직 검증 (가짜 데이터)
python run_scan.py --market kr --limit 30   # 국내 30종목만 시험
python run_scan.py --market kr              # 국내 전 종목 (장 마감 후)
python run_scan.py --market us              # 미국 (S&P 500, 미국장 마감 후)
```

결과는 `data/longterm.js` 로 저장되고 대시보드 4장에 표시됩니다.
규칙의 숫자 기준(이평선 터치 허용 폭, 급등 기준 %, 거래량 배수 등)은 `scanner/config.py` 에서 바꿉니다.
국내/미국 데이터는 각각 FinanceDataReader, yfinance 를 사용하며, 이 코드는 아직 실제 데이터로 시험하지 못했습니다.

## 다음 단계

1. 4장 규칙 입력 → 일봉 스캐너(pykrx, yfinance 등)로 `longterm.js` 자동 생성
2. 2장 테마 연결표 작성 → 미국 특징주와 국내 연관주 자동 연결
3. GitHub Pages 등에 올려 카카오톡용 URL 만들기, 스케줄러로 매일 갱신
4. 1장 일정, 3장 유튜브 자동 수집
5. 5장 단기 유형별 규칙 입력


## 국내 테마 (네이버 증권 모바일 주소 사용)
특징주 탭의 국내 테마는 네이버 증권 모바일 화면이 쓰는 주소(`m.stock.naver.com/api/stocks/theme`)로 받습니다. 키는 필요 없지만 **공식 개방 API가 아니라서 네이버가 막거나 바꾸면 실패**할 수 있습니다. 실패하면 `scanner/theme_map.json` 의 기본 테마로 자동 대체됩니다. 시세 값은 KRX 시세표를 쓰고, 테마 안에서는 거래대금이 큰 종목 10개를 보여줍니다.
