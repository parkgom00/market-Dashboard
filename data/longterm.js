// 자동 생성 파일 (scanner/run_scan.py). 직접 고치지 마세요.
window.DASH = window.DASH || {};
window.DASH.longterm = {
 "rules": [
  {
   "id": "L1",
   "label": "정배열 상승 + 이평선 지지",
   "desc": "5>10>20>60>120>240>480일선 정배열, 20·60일선 상승 중, 최근 20일 안에 20일선 또는 60일선에서 지지"
  },
  {
   "id": "L2",
   "label": "급등 후 60일선 지지",
   "desc": "20일 안에 +30% 이상 급등 후 고점 대비 -10% 이상 조정, 60일선(상승 중)에서 지지"
  },
  {
   "id": "L3a",
   "label": "240일선 거래량 돌파",
   "desc": "최근 3일 안에 240일선을 아래→위로 돌파, 돌파일 거래량이 직전 20일 평균의 2배 이상"
  },
  {
   "id": "L3b",
   "label": "480일선 거래량 돌파",
   "desc": "최근 3일 안에 480일선을 아래→위로 돌파, 돌파일 거래량이 직전 20일 평균의 2배 이상"
  }
 ],
 "scanInfo": {
  "kr": {
   "asOf": "2026-10-02",
   "scanned": 2711
  },
  "us": {
   "asOf": "2026-10-05",
   "scanned": 501
  }
 },
 "kr": [
  {
   "code": "001250",
   "name": "GS글로벌",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 2840.0,
   "changePct": 4.75,
   "value": 39,
   "close": 2975.0,
   "ma240": 2769.04,
   "ma480": 2750.79,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 6.4배 / 480일선 돌파(2일 전), 거래량 평균의 6.4배"
  },
  {
   "code": "011790",
   "name": "SKC",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 104200.0,
   "changePct": 2.5,
   "value": 671,
   "close": 106800.0,
   "ma240": 104096.62,
   "ma480": 105583.74,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 3.2배 / 480일선 돌파(오늘), 거래량 평균의 3.7배"
  },
  {
   "code": "263600",
   "name": "덕우전자",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 4410.0,
   "changePct": 17.91,
   "value": 345,
   "close": 5200.0,
   "ma240": 4488.85,
   "ma480": 4683.46,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 146.3배 / 480일선 돌파(오늘), 거래량 평균의 146.3배"
  },
  {
   "code": "026960",
   "name": "동서",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 26200.0,
   "changePct": 5.15,
   "value": 65,
   "close": 27550.0,
   "ma240": 26333.12,
   "ma480": 26415.15,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 4.6배 / 480일선 돌파(오늘), 거래량 평균의 4.6배"
  },
  {
   "code": "065530",
   "name": "와이어블",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 1283.0,
   "changePct": 18.32,
   "value": 128,
   "close": 1518.0,
   "ma240": 1467.32,
   "ma480": 1394.3,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 45.3배 / 480일선 돌파(오늘), 거래량 평균의 45.3배"
  },
  {
   "code": "086390",
   "name": "유니테스트",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 14980.0,
   "changePct": 1.54,
   "value": 45,
   "close": 15210.0,
   "ma240": 14756.12,
   "ma480": 13337.54,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 2.1배 / 480일선 돌파(2일 전), 거래량 평균의 2.1배"
  },
  {
   "code": "079370",
   "name": "제우스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 14370.0,
   "changePct": -0.07,
   "value": 97,
   "close": 14360.0,
   "ma240": 13705.92,
   "ma480": 13433.21,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 4.3배 / 480일선 돌파(1일 전), 거래량 평균의 4.3배"
  },
  {
   "code": "079160",
   "name": "CJ CGV",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 5020.0,
   "changePct": -0.2,
   "value": 11,
   "close": 5010.0,
   "ma240": 5195.19,
   "ma480": 5129.06,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.4% 후 고점 대비 -11.6% 조정, 60일선 대비 -2.0%"
  },
  {
   "code": "005830",
   "name": "DB손해보험",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 183000.0,
   "changePct": -0.27,
   "value": 463,
   "close": 182500.0,
   "ma240": 155340.83,
   "ma480": 132810.21,
   "matched": [
    "L2"
   ],
   "note": "급등 +30.5% 후 고점 대비 -10.1% 조정, 60일선 대비 +4.5%"
  },
  {
   "code": "007340",
   "name": "DN오토모티브",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 49600.0,
   "changePct": 1.81,
   "value": 53,
   "close": 50500.0,
   "ma240": 35330.0,
   "ma480": 28580.25,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "900290",
   "name": "GRT",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3650.0,
   "changePct": -4.66,
   "value": 12,
   "close": 3480.0,
   "ma240": 3702.38,
   "ma480": 3536.76,
   "matched": [
    "L2"
   ],
   "note": "급등 +79.2% 후 고점 대비 -17.3% 조정, 60일선 대비 +2.9%"
  },
  {
   "code": "078930",
   "name": "GS",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 102100.0,
   "changePct": 2.94,
   "value": 412,
   "close": 105100.0,
   "ma240": 74427.08,
   "ma480": 58376.25,
   "matched": [
    "L2"
   ],
   "note": "급등 +52.7% 후 고점 대비 -18.7% 조정, 60일선 대비 +0.8%"
  },
  {
   "code": "006360",
   "name": "GS건설",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 33100.0,
   "changePct": 0.15,
   "value": 379,
   "close": 33150.0,
   "ma240": 26592.29,
   "ma480": 22705.06,
   "matched": [
    "L2"
   ],
   "note": "급등 +70.3% 후 고점 대비 -13.9% 조정, 60일선 대비 +1.5%"
  },
  {
   "code": "012630",
   "name": "HDC",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 24750.0,
   "changePct": -5.05,
   "value": 29,
   "close": 23500.0,
   "ma240": 21660.04,
   "ma480": 19190.04,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.5% 후 고점 대비 -17.4% 조정, 60일선 대비 +3.3%"
  },
  {
   "code": "294870",
   "name": "IPARK현대산업개발",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 22650.0,
   "changePct": -1.32,
   "value": 14,
   "close": 22350.0,
   "ma240": 21103.71,
   "ma480": 21099.75,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.2% 후 고점 대비 -10.1% 조정, 60일선 대비 +3.1%"
  },
  {
   "code": "001060",
   "name": "JW중외제약",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 27100.0,
   "changePct": -1.11,
   "value": 6,
   "close": 26800.0,
   "ma240": 27796.88,
   "ma480": 25433.83,
   "matched": [
    "L2"
   ],
   "note": "급등 +36.4% 후 고점 대비 -10.7% 조정, 60일선 대비 +3.2%"
  },
  {
   "code": "016380",
   "name": "KG스틸",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 5630.0,
   "changePct": 1.6,
   "value": 26,
   "close": 5720.0,
   "ma240": 5628.67,
   "ma480": 5828.12,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 7.8배"
  },
  {
   "code": "003550",
   "name": "LG",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 109800.0,
   "changePct": 1.46,
   "value": 115,
   "close": 111400.0,
   "ma240": 97001.67,
   "ma480": 85101.67,
   "matched": [
    "L2"
   ],
   "note": "급등 +68.7% 후 고점 대비 -32.8% 조정, 60일선 대비 +2.5%"
  },
  {
   "code": "417200",
   "name": "LS머트리얼즈",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 14020.0,
   "changePct": 9.13,
   "value": 425,
   "close": 15300.0,
   "ma240": 15505.88,
   "ma480": 13540.31,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(2일 전), 거래량 평균의 3.9배"
  },
  {
   "code": "036570",
   "name": "NC",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 230500.0,
   "changePct": 6.07,
   "value": 465,
   "close": 244500.0,
   "ma240": 230532.5,
   "ma480": 208936.67,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 3.0배"
  },
  {
   "code": "181710",
   "name": "NHN",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 56300.0,
   "changePct": 1.78,
   "value": 76,
   "close": 57300.0,
   "ma240": 39622.92,
   "ma480": 30825.88,
   "matched": [
    "L2"
   ],
   "note": "급등 +124.1% 후 고점 대비 -23.8% 조정, 60일선 대비 +7.9%"
  },
  {
   "code": "060250",
   "name": "NHN KCP",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 13690.0,
   "changePct": 1.24,
   "value": 19,
   "close": 13860.0,
   "ma240": 16394.04,
   "ma480": 13145.71,
   "matched": [
    "L2"
   ],
   "note": "급등 +43.2% 후 고점 대비 -14.2% 조정, 60일선 대비 +1.7%"
  },
  {
   "code": "178920",
   "name": "PI첨단소재",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 19470.0,
   "changePct": 3.49,
   "value": 14,
   "close": 20150.0,
   "ma240": 19870.58,
   "ma480": 18871.04,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 2.2배"
  },
  {
   "code": "010950",
   "name": "S-Oil",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 151300.0,
   "changePct": 8.99,
   "value": 769,
   "close": 164900.0,
   "ma240": 110667.08,
   "ma480": 84520.83,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "010955",
   "name": "S-Oil우",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 81100.0,
   "changePct": 8.14,
   "value": 28,
   "close": 87700.0,
   "ma240": 56584.79,
   "ma480": 47828.23,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "096770",
   "name": "SK이노베이션",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 141100.0,
   "changePct": 7.23,
   "value": 1815,
   "close": 151300.0,
   "ma240": 118589.58,
   "ma480": 114557.29,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "399720",
   "name": "가온칩스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 48400.0,
   "changePct": 0.21,
   "value": 64,
   "close": 48500.0,
   "ma240": 54684.58,
   "ma480": 48925.0,
   "matched": [
    "L2"
   ],
   "note": "급등 +56.3% 후 고점 대비 -15.2% 조정, 60일선 대비 +6.4%"
  },
  {
   "code": "013580",
   "name": "계룡건설",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 21600.0,
   "changePct": -0.23,
   "value": 8,
   "close": 21550.0,
   "ma240": 22112.83,
   "ma480": 19624.23,
   "matched": [
    "L2"
   ],
   "note": "급등 +40.6% 후 고점 대비 -16.5% 조정, 60일선 대비 +2.6%"
  },
  {
   "code": "950190",
   "name": "고스트스튜디오",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 9750.0,
   "changePct": -0.1,
   "value": 1,
   "close": 9740.0,
   "ma240": 8664.62,
   "ma480": 8832.06,
   "matched": [
    "L2"
   ],
   "note": "급등 +33.8% 후 고점 대비 -13.3% 조정, 60일선 대비 +2.7%"
  },
  {
   "code": "204620",
   "name": "글로벌텍스프리",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 5800.0,
   "changePct": -2.41,
   "value": 46,
   "close": 5660.0,
   "ma240": 5105.44,
   "ma480": 4976.28,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "053260",
   "name": "금강철강",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7450.0,
   "changePct": -2.68,
   "value": 35,
   "close": 7250.0,
   "ma240": 4908.92,
   "ma480": 4566.12,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "073240",
   "name": "금호타이어",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 6890.0,
   "changePct": 0.0,
   "value": 34,
   "close": 6890.0,
   "ma240": 5966.4,
   "ma480": 5337.57,
   "matched": [
    "L2"
   ],
   "note": "급등 +81.2% 후 고점 대비 -15.4% 조정, 60일선 대비 -1.2%"
  },
  {
   "code": "459510",
   "name": "나우로보틱스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 15600.0,
   "changePct": 1.73,
   "value": 6,
   "close": 15870.0,
   "ma240": 21248.29,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +58.2% 후 고점 대비 -10.9% 조정, 60일선 대비 +6.0%"
  },
  {
   "code": "036800",
   "name": "나이스정보통신",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7840.0,
   "changePct": 8.16,
   "value": 38,
   "close": 8480.0,
   "ma240": 5496.5,
   "ma480": 4725.46,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "212560",
   "name": "네오오토",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 10420.0,
   "changePct": 8.45,
   "value": 91,
   "close": 11300.0,
   "ma240": 9068.71,
   "ma480": 7319.93,
   "matched": [
    "L2"
   ],
   "note": "급등 +90.8% 후 고점 대비 -27.4% 조정, 60일선 대비 +8.1%"
  },
  {
   "code": "007390",
   "name": "네이처셀",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 25000.0,
   "changePct": -0.2,
   "value": 48,
   "close": 24950.0,
   "ma240": 22997.92,
   "ma480": 22881.9,
   "matched": [
    "L2"
   ],
   "note": "급등 +99.6% 후 고점 대비 -27.8% 조정, 60일선 대비 +3.7%"
  },
  {
   "code": "144960",
   "name": "뉴파워프라즈마",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 13140.0,
   "changePct": 0.68,
   "value": 115,
   "close": 13230.0,
   "ma240": 7371.06,
   "ma480": 6167.61,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "323350",
   "name": "다원넥스뷰",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 9830.0,
   "changePct": 2.95,
   "value": 28,
   "close": 10120.0,
   "ma240": 9974.88,
   "ma480": 8253.48,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 4.5배"
  },
  {
   "code": "045390",
   "name": "대아티아이",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3035.0,
   "changePct": 2.14,
   "value": 14,
   "close": 3100.0,
   "ma240": 3766.62,
   "ma480": 3822.76,
   "matched": [
    "L2"
   ],
   "note": "급등 +51.2% 후 고점 대비 -18.3% 조정, 60일선 대비 +6.1%"
  },
  {
   "code": "006340",
   "name": "대원전선",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 13210.0,
   "changePct": 1.67,
   "value": 264,
   "close": 13430.0,
   "ma240": 8215.06,
   "ma480": 5598.14,
   "matched": [
    "L2"
   ],
   "note": "급등 +126.9% 후 고점 대비 -16.2% 조정, 60일선 대비 +2.1%"
  },
  {
   "code": "003490",
   "name": "대한항공",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 31050.0,
   "changePct": -0.64,
   "value": 576,
   "close": 30850.0,
   "ma240": 25104.38,
   "ma480": 24224.17,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "224060",
   "name": "더코디",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 4320.0,
   "changePct": -1.27,
   "value": 11,
   "close": 4265.0,
   "ma240": 4191.35,
   "ma480": 3836.29,
   "matched": [
    "L2"
   ],
   "note": "급등 +245.8% 후 고점 대비 -56.9% 조정, 60일선 대비 -5.8%"
  },
  {
   "code": "005160",
   "name": "동국산업",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3360.0,
   "changePct": 18.01,
   "value": 301,
   "close": 3965.0,
   "ma240": 2845.06,
   "ma480": 3545.25,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(오늘), 거래량 평균의 3.0배"
  },
  {
   "code": "028100",
   "name": "동아지질",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 19770.0,
   "changePct": 0.46,
   "value": 3,
   "close": 19860.0,
   "ma240": 16876.17,
   "ma480": 15758.9,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "228340",
   "name": "동양파일",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3445.0,
   "changePct": -2.03,
   "value": 8,
   "close": 3375.0,
   "ma240": 2298.02,
   "ma480": 2079.11,
   "matched": [
    "L2"
   ],
   "note": "급등 +267.3% 후 고점 대비 -45.9% 조정, 60일선 대비 +4.8%"
  },
  {
   "code": "023790",
   "name": "동일스틸럭스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 1615.0,
   "changePct": -0.12,
   "value": 7,
   "close": 1613.0,
   "ma240": 2557.2,
   "ma480": 2331.66,
   "matched": [
    "L2"
   ],
   "note": "급등 +119.8% 후 고점 대비 -27.3% 조정, 60일선 대비 +10.2%"
  },
  {
   "code": "092200",
   "name": "디아이씨",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 5650.0,
   "changePct": 2.12,
   "value": 10,
   "close": 5770.0,
   "ma240": 7875.54,
   "ma480": 6122.72,
   "matched": [
    "L2"
   ],
   "note": "급등 +74.8% 후 고점 대비 -14.4% 조정, 60일선 대비 +9.5%"
  },
  {
   "code": "110990",
   "name": "디아이티",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 18930.0,
   "changePct": 1.48,
   "value": 28,
   "close": 19210.0,
   "ma240": 18660.83,
   "ma480": 16152.52,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 2.2배"
  },
  {
   "code": "068930",
   "name": "디지털대성",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 9490.0,
   "changePct": -1.58,
   "value": 6,
   "close": 9340.0,
   "ma240": 7999.46,
   "ma480": 7748.58,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "089860",
   "name": "롯데렌탈",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 50900.0,
   "changePct": 0.98,
   "value": 57,
   "close": 51400.0,
   "ma240": 34467.08,
   "ma480": 32328.65,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "000400",
   "name": "롯데손해보험",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 2120.0,
   "changePct": 5.19,
   "value": 24,
   "close": 2230.0,
   "ma240": 1980.28,
   "ma480": 1919.4,
   "matched": [
    "L2"
   ],
   "note": "급등 +58.3% 후 고점 대비 -15.8% 조정, 60일선 대비 +6.5%"
  },
  {
   "code": "280360",
   "name": "롯데웰푸드",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 122400.0,
   "changePct": -1.88,
   "value": 16,
   "close": 120100.0,
   "ma240": 116753.33,
   "ma480": 116352.71,
   "matched": [
    "L2"
   ],
   "note": "급등 +46.0% 후 고점 대비 -19.2% 조정, 60일선 대비 -1.2%"
  },
  {
   "code": "377450",
   "name": "리파인",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 14380.0,
   "changePct": 0.63,
   "value": 2,
   "close": 14470.0,
   "ma240": 12360.21,
   "ma480": 13159.73,
   "matched": [
    "L2"
   ],
   "note": "급등 +59.6% 후 고점 대비 -15.9% 조정, 60일선 대비 +3.4%"
  },
  {
   "code": "094800",
   "name": "맵스리얼티",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 7900.0,
   "changePct": -0.38,
   "value": 2,
   "close": 7870.0,
   "ma240": 6113.21,
   "ma480": 5258.32,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "446540",
   "name": "메가터치",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 11240.0,
   "changePct": -3.11,
   "value": 56,
   "close": 10890.0,
   "ma240": 5523.62,
   "ma480": 4670.46,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "254490",
   "name": "미래반도체",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 18540.0,
   "changePct": 1.83,
   "value": 32,
   "close": 18880.0,
   "ma240": 18567.75,
   "ma480": 16427.35,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 2.1배"
  },
  {
   "code": "457600",
   "name": "벡트",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3570.0,
   "changePct": 10.64,
   "value": 9,
   "close": 3950.0,
   "ma240": 2685.76,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +91.9% 후 고점 대비 -27.8% 조정, 60일선 대비 -0.6%"
  },
  {
   "code": "018290",
   "name": "브이티",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 12560.0,
   "changePct": 0.32,
   "value": 15,
   "close": 12600.0,
   "ma240": 16255.17,
   "ma480": 25859.25,
   "matched": [
    "L2"
   ],
   "note": "급등 +38.3% 후 고점 대비 -15.5% 조정, 60일선 대비 +3.1%"
  },
  {
   "code": "086670",
   "name": "비엠티",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 19220.0,
   "changePct": -1.72,
   "value": 6,
   "close": 18890.0,
   "ma240": 14449.54,
   "ma480": 11870.96,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "122350",
   "name": "삼기",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 1648.0,
   "changePct": 2.25,
   "value": 12,
   "close": 1685.0,
   "ma240": 1473.17,
   "ma480": 1372.92,
   "matched": [
    "L2"
   ],
   "note": "급등 +134.7% 후 고점 대비 -14.1% 조정, 60일선 대비 +3.0%"
  },
  {
   "code": "006660",
   "name": "삼성공조",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 13070.0,
   "changePct": 0.84,
   "value": 19,
   "close": 13180.0,
   "ma240": 12938.04,
   "ma480": 13116.04,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 2.7배"
  },
  {
   "code": "018260",
   "name": "삼성에스디에스",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 222500.0,
   "changePct": -1.57,
   "value": 245,
   "close": 219000.0,
   "ma240": 189799.17,
   "ma480": 165484.79,
   "matched": [
    "L2"
   ],
   "note": "급등 +119.7% 후 고점 대비 -39.5% 조정, 60일선 대비 +0.0%"
  },
  {
   "code": "0120G0",
   "name": "삼양바이오팜",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 49200.0,
   "changePct": -1.52,
   "value": 11,
   "close": 48450.0,
   "ma240": null,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +83.2% 후 고점 대비 -22.0% 조정, 60일선 대비 +3.4%"
  },
  {
   "code": "482630",
   "name": "삼양엔씨켐",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 15460.0,
   "changePct": 1.42,
   "value": 77,
   "close": 15680.0,
   "ma240": 14624.96,
   "ma480": null,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 5.4배"
  },
  {
   "code": "001820",
   "name": "삼화콘덴서",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 158900.0,
   "changePct": -0.69,
   "value": 958,
   "close": 157800.0,
   "ma240": 70204.58,
   "ma480": 49059.38,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 60일선 지지 확인"
  },
  {
   "code": "252990",
   "name": "샘씨엔에스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 20300.0,
   "changePct": -1.87,
   "value": 130,
   "close": 19920.0,
   "ma240": 11002.88,
   "ma480": 7929.99,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "007540",
   "name": "샘표",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 46200.0,
   "changePct": 0.76,
   "value": 3,
   "close": 46550.0,
   "ma240": 48780.21,
   "ma480": 46339.48,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.2% 후 고점 대비 -19.0% 조정, 60일선 대비 +3.3%"
  },
  {
   "code": "079650",
   "name": "서산",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 5680.0,
   "changePct": -0.7,
   "value": 54,
   "close": 5640.0,
   "ma240": 2602.15,
   "ma480": 1989.35,
   "matched": [
    "L2"
   ],
   "note": "급등 +729.4% 후 고점 대비 -30.5% 조정, 60일선 대비 +5.4%"
  },
  {
   "code": "035890",
   "name": "서희건설",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 2200.0,
   "changePct": 1.36,
   "value": 5,
   "close": 2230.0,
   "ma240": 2834.41,
   "ma480": 2798.89,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.8% 후 고점 대비 -16.6% 조정, 60일선 대비 +3.9%"
  },
  {
   "code": "037350",
   "name": "성도이엔지",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 8350.0,
   "changePct": 1.44,
   "value": 22,
   "close": 8470.0,
   "ma240": 8136.65,
   "ma480": 6325.1,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 3.0배"
  },
  {
   "code": "061090",
   "name": "세나테크놀로지",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 40550.0,
   "changePct": 2.1,
   "value": 12,
   "close": 41400.0,
   "ma240": null,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +66.0% 후 고점 대비 -12.9% 조정, 60일선 대비 +1.2%"
  },
  {
   "code": "108860",
   "name": "셀바스AI",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 8960.0,
   "changePct": 0.33,
   "value": 10,
   "close": 8990.0,
   "ma240": 11182.25,
   "ma480": 12248.58,
   "matched": [
    "L2"
   ],
   "note": "급등 +75.8% 후 고점 대비 -17.9% 조정, 60일선 대비 +3.1%"
  },
  {
   "code": "248070",
   "name": "솔루엠",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 15380.0,
   "changePct": 8.65,
   "value": 207,
   "close": 16710.0,
   "ma240": 16687.21,
   "ma480": 17127.73,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 9.7배"
  },
  {
   "code": "304100",
   "name": "솔트룩스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 15180.0,
   "changePct": 1.71,
   "value": 12,
   "close": 15440.0,
   "ma240": 22147.12,
   "ma480": 26347.98,
   "matched": [
    "L2"
   ],
   "note": "급등 +81.5% 후 고점 대비 -17.0% 조정, 60일선 대비 +5.8%"
  },
  {
   "code": "099440",
   "name": "스맥",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3840.0,
   "changePct": 2.73,
   "value": 6,
   "close": 3945.0,
   "ma240": 4628.73,
   "ma480": 3820.79,
   "matched": [
    "L2"
   ],
   "note": "급등 +65.1% 후 고점 대비 -13.5% 조정, 60일선 대비 +5.3%"
  },
  {
   "code": "340810",
   "name": "시선AI",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3580.0,
   "changePct": -3.63,
   "value": 6,
   "close": 3450.0,
   "ma240": 3063.54,
   "ma480": 3370.02,
   "matched": [
    "L2"
   ],
   "note": "급등 +66.8% 후 고점 대비 -25.2% 조정, 60일선 대비 +2.2%"
  },
  {
   "code": "019170",
   "name": "신풍제약",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 9300.0,
   "changePct": 0.11,
   "value": 10,
   "close": 9310.0,
   "ma240": 11243.46,
   "ma480": 11087.1,
   "matched": [
    "L2"
   ],
   "note": "급등 +46.3% 후 고점 대비 -11.8% 조정, 60일선 대비 +5.7%"
  },
  {
   "code": "004770",
   "name": "써니전자",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 1955.0,
   "changePct": -5.17,
   "value": 26,
   "close": 1854.0,
   "ma240": 1674.02,
   "ma480": 1787.24,
   "matched": [
    "L2"
   ],
   "note": "급등 +46.6% 후 고점 대비 -21.9% 조정, 60일선 대비 +1.1%"
  },
  {
   "code": "050890",
   "name": "쏠리드",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 10060.0,
   "changePct": 6.26,
   "value": 453,
   "close": 10690.0,
   "ma240": 10449.58,
   "ma480": 8427.04,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 3.1배"
  },
  {
   "code": "090430",
   "name": "아모레퍼시픽",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 136500.0,
   "changePct": -2.93,
   "value": 256,
   "close": 132500.0,
   "ma240": 128650.83,
   "ma480": 124757.08,
   "matched": [
    "L2"
   ],
   "note": "급등 +31.5% 후 고점 대비 -12.0% 조정, 60일선 대비 -1.5%"
  },
  {
   "code": "159010",
   "name": "아스플로",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 32250.0,
   "changePct": -0.47,
   "value": 28,
   "close": 32100.0,
   "ma240": 11272.15,
   "ma480": 7896.91,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "214430",
   "name": "아이쓰리시스템",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 83800.0,
   "changePct": -7.04,
   "value": 66,
   "close": 77900.0,
   "ma240": 80704.58,
   "ma480": 73326.35,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(1일 전), 거래량 평균의 7.3배"
  },
  {
   "code": "119830",
   "name": "아이텍",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 6910.0,
   "changePct": -3.47,
   "value": 14,
   "close": 6670.0,
   "ma240": 6483.98,
   "ma480": 6130.27,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 2.2배"
  },
  {
   "code": "161000",
   "name": "애경케미칼",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 10270.0,
   "changePct": 7.5,
   "value": 55,
   "close": 11040.0,
   "ma240": 10807.12,
   "ma480": 10033.23,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 3.8배"
  },
  {
   "code": "174900",
   "name": "앱클론",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 26500.0,
   "changePct": 6.6,
   "value": 93,
   "close": 28250.0,
   "ma240": 39635.33,
   "ma480": 26042.96,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(1일 전), 거래량 평균의 4.2배"
  },
  {
   "code": "039440",
   "name": "에스티아이",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 25900.0,
   "changePct": 0.19,
   "value": 43,
   "close": 25950.0,
   "ma240": 28089.62,
   "ma480": 23852.04,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(1일 전), 거래량 평균의 5.9배"
  },
  {
   "code": "078520",
   "name": "에이블씨엔씨",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 11250.0,
   "changePct": -2.31,
   "value": 7,
   "close": 10990.0,
   "ma240": 11096.42,
   "ma480": 9612.15,
   "matched": [
    "L2"
   ],
   "note": "급등 +41.7% 후 고점 대비 -18.2% 조정, 60일선 대비 +0.7%"
  },
  {
   "code": "036810",
   "name": "에프에스티",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 35050.0,
   "changePct": 1.85,
   "value": 111,
   "close": 35700.0,
   "ma240": 32645.14,
   "ma480": 26191.39,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 2.6배"
  },
  {
   "code": "265740",
   "name": "엔에프씨",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7520.0,
   "changePct": -1.33,
   "value": 16,
   "close": 7420.0,
   "ma240": 6102.02,
   "ma480": 4877.2,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "083310",
   "name": "엘오티베큠",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 11930.0,
   "changePct": 7.8,
   "value": 41,
   "close": 12860.0,
   "ma240": 12037.75,
   "ma480": 10946.9,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 4.5배"
  },
  {
   "code": "373170",
   "name": "엠아이큐브솔루션",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 1769.0,
   "changePct": 4.3,
   "value": 0,
   "close": 1845.0,
   "ma240": 2434.39,
   "ma480": 2548.03,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.2% 후 고점 대비 -20.0% 조정, 60일선 대비 +4.1%"
  },
  {
   "code": "000670",
   "name": "영풍",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 40300.0,
   "changePct": 0.74,
   "value": 8,
   "close": 40600.0,
   "ma240": 51003.04,
   "ma480": 45418.94,
   "matched": [
    "L2"
   ],
   "note": "급등 +33.9% 후 고점 대비 -18.7% 조정, 60일선 대비 +4.3%"
  },
  {
   "code": "900300",
   "name": "오가닉티코스메틱",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 2655.0,
   "changePct": 12.99,
   "value": 40,
   "close": 3000.0,
   "ma240": 9049.12,
   "ma480": 17142.79,
   "matched": [
    "L2"
   ],
   "note": "급등 +155.6% 후 고점 대비 -76.3% 조정, 60일선 대비 +11.7%"
  },
  {
   "code": "112290",
   "name": "와이씨켐",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 12830.0,
   "changePct": -2.73,
   "value": 44,
   "close": 12480.0,
   "ma240": 11417.01,
   "ma480": 10758.54,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 12.1배"
  },
  {
   "code": "011690",
   "name": "와이투솔루션",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 3650.0,
   "changePct": 1.78,
   "value": 12,
   "close": 3715.0,
   "ma240": 4643.71,
   "ma480": 3679.75,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(오늘), 거래량 평균의 2.4배"
  },
  {
   "code": "101160",
   "name": "월덱스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 33150.0,
   "changePct": -0.15,
   "value": 16,
   "close": 33100.0,
   "ma240": 27376.25,
   "ma480": 23458.79,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "330350",
   "name": "위더스제약",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7270.0,
   "changePct": -0.69,
   "value": 2,
   "close": 7220.0,
   "ma240": 7682.21,
   "ma480": 7326.83,
   "matched": [
    "L2"
   ],
   "note": "급등 +49.8% 후 고점 대비 -19.8% 조정, 60일선 대비 +0.5%"
  },
  {
   "code": "097800",
   "name": "윈팩",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3835.0,
   "changePct": 4.95,
   "value": 328,
   "close": 4025.0,
   "ma240": 2396.38,
   "ma480": 2981.0,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(2일 전), 거래량 평균의 8.9배"
  },
  {
   "code": "264450",
   "name": "유비쿼스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 11390.0,
   "changePct": 3.16,
   "value": 19,
   "close": 11750.0,
   "ma240": 11452.46,
   "ma480": 9763.87,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 2.4배"
  },
  {
   "code": "264850",
   "name": "이랜시스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 5800.0,
   "changePct": 2.41,
   "value": 23,
   "close": 5940.0,
   "ma240": 6075.06,
   "ma480": 5498.82,
   "matched": [
    "L2"
   ],
   "note": "급등 +90.6% 후 고점 대비 -13.9% 조정, 60일선 대비 +9.6%"
  },
  {
   "code": "457190",
   "name": "이수스페셜티케미컬",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 79400.0,
   "changePct": 3.15,
   "value": 303,
   "close": 81900.0,
   "ma240": 76901.88,
   "ma480": 59598.96,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 8.3배"
  },
  {
   "code": "119610",
   "name": "인터로조",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 15630.0,
   "changePct": 9.21,
   "value": 28,
   "close": 17070.0,
   "ma240": 17045.71,
   "ma480": 18857.35,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 5.8배"
  },
  {
   "code": "064290",
   "name": "인텍플러스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 58000.0,
   "changePct": 1.9,
   "value": 276,
   "close": 59100.0,
   "ma240": 26088.0,
   "ma480": 18617.38,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 60일선 지지 확인"
  },
  {
   "code": "333430",
   "name": "일승",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3940.0,
   "changePct": -0.63,
   "value": 6,
   "close": 3915.0,
   "ma240": 5279.92,
   "ma480": 5013.92,
   "matched": [
    "L2"
   ],
   "note": "급등 +49.1% 후 고점 대비 -11.4% 조정, 60일선 대비 +5.8%"
  },
  {
   "code": "003200",
   "name": "일신방직",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 10660.0,
   "changePct": 1.31,
   "value": 2,
   "close": 10800.0,
   "ma240": 11761.33,
   "ma480": 10382.96,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.7% 후 고점 대비 -15.6% 조정, 60일선 대비 +1.7%"
  },
  {
   "code": "049630",
   "name": "재영솔루텍",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7290.0,
   "changePct": 0.27,
   "value": 15,
   "close": 7310.0,
   "ma240": 11739.79,
   "ma480": 7730.07,
   "matched": [
    "L2"
   ],
   "note": "급등 +87.9% 후 고점 대비 -19.0% 조정, 60일선 대비 +8.8%"
  },
  {
   "code": "095700",
   "name": "제넥신",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 2790.0,
   "changePct": 0.9,
   "value": 2,
   "close": 2815.0,
   "ma240": 4130.19,
   "ma480": 4678.73,
   "matched": [
    "L2"
   ],
   "note": "급등 +42.1% 후 고점 대비 -15.3% 조정, 60일선 대비 +5.2%"
  },
  {
   "code": "147830",
   "name": "제룡산업",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7110.0,
   "changePct": 3.38,
   "value": 15,
   "close": 7350.0,
   "ma240": 7275.88,
   "ma480": 6719.19,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 2.0배"
  },
  {
   "code": "026040",
   "name": "제이에스티나",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 2185.0,
   "changePct": 1.6,
   "value": 1,
   "close": 2220.0,
   "ma240": 2686.4,
   "ma480": 2611.04,
   "matched": [
    "L2"
   ],
   "note": "급등 +52.6% 후 고점 대비 -15.6% 조정, 60일선 대비 +9.5%"
  },
  {
   "code": "420570",
   "name": "제이투케이바이오",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 9490.0,
   "changePct": -4.43,
   "value": 3,
   "close": 9070.0,
   "ma240": 8511.17,
   "ma480": 9544.52,
   "matched": [
    "L2"
   ],
   "note": "급등 +53.1% 후 고점 대비 -24.4% 조정, 60일선 대비 -1.9%"
  },
  {
   "code": "228760",
   "name": "지노믹트리",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 12600.0,
   "changePct": -3.33,
   "value": 7,
   "close": 12180.0,
   "ma240": 18039.38,
   "ma480": 17447.4,
   "matched": [
    "L2"
   ],
   "note": "급등 +43.9% 후 고점 대비 -18.0% 조정, 60일선 대비 +5.0%"
  },
  {
   "code": "119850",
   "name": "지엔씨에너지",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 54800.0,
   "changePct": -2.55,
   "value": 301,
   "close": 53400.0,
   "ma240": 35820.92,
   "ma480": 28242.43,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "029460",
   "name": "케이씨",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 45300.0,
   "changePct": -2.65,
   "value": 15,
   "close": 44100.0,
   "ma240": 31642.29,
   "ma480": 25935.58,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "032500",
   "name": "케이엠더블유",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 19420.0,
   "changePct": 8.14,
   "value": 116,
   "close": 21000.0,
   "ma240": 20198.62,
   "ma480": 15055.58,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 2.1배"
  },
  {
   "code": "220260",
   "name": "켐트로스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 4740.0,
   "changePct": 2.11,
   "value": 11,
   "close": 4840.0,
   "ma240": 4979.06,
   "ma480": 4674.34,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(1일 전), 거래량 평균의 3.0배"
  },
  {
   "code": "391710",
   "name": "코닉오토메이션",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 1263.0,
   "changePct": 0.08,
   "value": 2,
   "close": 1264.0,
   "ma240": 1917.02,
   "ma480": 1845.96,
   "matched": [
    "L2"
   ],
   "note": "급등 +37.5% 후 고점 대비 -14.1% 조정, 60일선 대비 +5.6%"
  },
  {
   "code": "041960",
   "name": "코미팜",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 9820.0,
   "changePct": 0.71,
   "value": 9,
   "close": 9890.0,
   "ma240": 7914.71,
   "ma480": 6398.36,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "044820",
   "name": "코스맥스비티아이",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 25050.0,
   "changePct": -0.2,
   "value": 8,
   "close": 25000.0,
   "ma240": 17358.75,
   "ma480": 15189.52,
   "matched": [
    "L2"
   ],
   "note": "급등 +48.1% 후 고점 대비 -10.7% 조정, 60일선 대비 +9.3%"
  },
  {
   "code": "355150",
   "name": "코스텍시스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 23200.0,
   "changePct": 1.94,
   "value": 46,
   "close": 23650.0,
   "ma240": 21378.25,
   "ma480": 14732.29,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 2.1배"
  },
  {
   "code": "405100",
   "name": "큐알티",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 16400.0,
   "changePct": 0.85,
   "value": 14,
   "close": 16540.0,
   "ma240": 15540.71,
   "ma480": 14368.19,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(1일 전), 거래량 평균의 6.5배"
  },
  {
   "code": "237880",
   "name": "클리오",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 12170.0,
   "changePct": -0.9,
   "value": 2,
   "close": 12060.0,
   "ma240": 12377.88,
   "ma480": 14958.77,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.2% 후 고점 대비 -15.2% 조정, 60일선 대비 +2.4%"
  },
  {
   "code": "020120",
   "name": "키다리스튜디오",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 8430.0,
   "changePct": -2.37,
   "value": 22,
   "close": 8230.0,
   "ma240": 3994.06,
   "ma480": 3821.26,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "219130",
   "name": "타이거일렉",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 91700.0,
   "changePct": 0.65,
   "value": 28,
   "close": 92300.0,
   "ma240": 44784.04,
   "ma480": 29954.25,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "131290",
   "name": "티에스이",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 301500.0,
   "changePct": -2.99,
   "value": 347,
   "close": 292500.0,
   "ma240": 147713.33,
   "ma480": 95370.0,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "037030",
   "name": "파워넷",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 3750.0,
   "changePct": 10.67,
   "value": 47,
   "close": 4150.0,
   "ma240": 3978.27,
   "ma480": 3248.8,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 3.4배"
  },
  {
   "code": "368770",
   "name": "파이버프로",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 13710.0,
   "changePct": 7.37,
   "value": 72,
   "close": 14720.0,
   "ma240": 13957.96,
   "ma480": 9937.69,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 3.2배"
  },
  {
   "code": "168360",
   "name": "펨트론",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 14940.0,
   "changePct": 7.36,
   "value": 129,
   "close": 16040.0,
   "ma240": 18442.88,
   "ma480": 14434.0,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(1일 전), 거래량 평균의 2.8배"
  },
  {
   "code": "039980",
   "name": "폴라리스AI",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 5050.0,
   "changePct": 0.59,
   "value": 2,
   "close": 5080.0,
   "ma240": 8126.38,
   "ma480": 10818.08,
   "matched": [
    "L2"
   ],
   "note": "급등 +67.2% 후 고점 대비 -21.5% 조정, 60일선 대비 -0.9%"
  },
  {
   "code": "032580",
   "name": "피델릭스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 7780.0,
   "changePct": -2.96,
   "value": 63,
   "close": 7550.0,
   "ma240": 2728.0,
   "ma480": 2000.47,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "031980",
   "name": "피에스케이홀딩스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 194000.0,
   "changePct": -0.21,
   "value": 394,
   "close": 193600.0,
   "ma240": 96683.75,
   "ma480": 67751.77,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 60일선 지지 확인"
  },
  {
   "code": "006140",
   "name": "피제이전자",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 4360.0,
   "changePct": 30.5,
   "value": 96,
   "close": 5690.0,
   "ma240": 5926.6,
   "ma480": 5684.11,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(오늘), 거래량 평균의 69.0배"
  },
  {
   "code": "017890",
   "name": "한국알콜",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 16050.0,
   "changePct": -1.62,
   "value": 14,
   "close": 15790.0,
   "ma240": 11984.04,
   "ma480": 10540.27,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "000240",
   "name": "한국앤컴퍼니",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 25150.0,
   "changePct": 1.19,
   "value": 8,
   "close": 25450.0,
   "ma240": 25597.92,
   "ma480": 22075.04,
   "matched": [
    "L2"
   ],
   "note": "급등 +36.8% 후 고점 대비 -17.0% 조정, 60일선 대비 +2.4%"
  },
  {
   "code": "452280",
   "name": "한선엔지니어링",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 14080.0,
   "changePct": 1.99,
   "value": 159,
   "close": 14360.0,
   "ma240": 13166.04,
   "ma480": 10441.88,
   "matched": [
    "L3a"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 2.8배"
  },
  {
   "code": "018880",
   "name": "한온시스템",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 3645.0,
   "changePct": 5.35,
   "value": 727,
   "close": 3840.0,
   "ma240": 3848.47,
   "ma480": 3642.28,
   "matched": [
    "L3b"
   ],
   "note": "480일선 돌파(1일 전), 거래량 평균의 5.7배"
  },
  {
   "code": "091440",
   "name": "한울소재과학",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 2910.0,
   "changePct": -3.95,
   "value": 9,
   "close": 2795.0,
   "ma240": 2836.64,
   "ma480": 3267.8,
   "matched": [
    "L2"
   ],
   "note": "급등 +64.1% 후 고점 대비 -19.2% 조정, 60일선 대비 -2.8%"
  },
  {
   "code": "180640",
   "name": "한진칼",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 132300.0,
   "changePct": 0.38,
   "value": 71,
   "close": 132800.0,
   "ma240": 118453.75,
   "ma480": 107680.42,
   "matched": [
    "L2"
   ],
   "note": "급등 +30.0% 후 고점 대비 -10.8% 조정, 60일선 대비 +5.5%"
  },
  {
   "code": "088350",
   "name": "한화생명",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 5300.0,
   "changePct": 0.38,
   "value": 113,
   "close": 5320.0,
   "ma240": 4374.62,
   "ma480": 3634.26,
   "matched": [
    "L2"
   ],
   "note": "급등 +41.5% 후 고점 대비 -12.9% 조정, 60일선 대비 +3.4%"
  },
  {
   "code": "000370",
   "name": "한화손해보험",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 7280.0,
   "changePct": 1.37,
   "value": 20,
   "close": 7380.0,
   "ma240": 6388.33,
   "ma480": 5607.44,
   "matched": [
    "L2"
   ],
   "note": "급등 +58.5% 후 고점 대비 -17.5% 조정, 60일선 대비 +5.7%"
  },
  {
   "code": "000720",
   "name": "현대건설",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 117300.0,
   "changePct": -2.22,
   "value": 809,
   "close": 114700.0,
   "ma240": 114476.25,
   "ma480": 79938.23,
   "matched": [
    "L2"
   ],
   "note": "급등 +59.6% 후 고점 대비 -15.0% 조정, 60일선 대비 +1.4%"
  },
  {
   "code": "453340",
   "name": "현대그린푸드",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 18820.0,
   "changePct": 0.43,
   "value": 4,
   "close": 18900.0,
   "ma240": 16763.08,
   "ma480": 15942.96,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "004020",
   "name": "현대제철",
   "market": "KOSPI",
   "sector": "",
   "marcap": 0,
   "prevClose": 30200.0,
   "changePct": -0.33,
   "value": 139,
   "close": 30100.0,
   "ma240": 33215.0,
   "ma480": 30348.85,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.8% 후 고점 대비 -16.0% 조정, 60일선 대비 +2.2%"
  },
  {
   "code": "024060",
   "name": "흥구석유",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 0,
   "prevClose": 12150.0,
   "changePct": -0.08,
   "value": 127,
   "close": 12140.0,
   "ma240": 14027.92,
   "ma480": 13414.17,
   "matched": [
    "L2"
   ],
   "note": "급등 +56.4% 후 고점 대비 -20.4% 조정, 60일선 대비 +4.6%"
  }
 ],
 "us": [
  {
   "code": "PTC",
   "name": "PTC Inc.",
   "close": 192.26,
   "ma240": 151.39,
   "ma480": 167.24,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(오늘), 거래량 평균의 16.9배 / 480일선 돌파(오늘), 거래량 평균의 16.9배"
  },
  {
   "code": "SNPS",
   "name": "Synopsys",
   "close": 488.47,
   "ma240": 442.75,
   "ma480": 475.26,
   "matched": [
    "L3a",
    "L3b"
   ],
   "note": "240일선 돌파(2일 전), 거래량 평균의 3.3배 / 480일선 돌파(2일 전), 거래량 평균의 3.3배"
  },
  {
   "code": "AES",
   "name": "AES Corporation",
   "close": 14.9,
   "ma240": 14.29,
   "ma480": 12.82,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "AME",
   "name": "Ametek",
   "close": 251.92,
   "ma240": 223.96,
   "ma480": 201.78,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "APH",
   "name": "Amphenol",
   "close": 87.27,
   "ma240": 73.01,
   "ma480": 57.98,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "CTSH",
   "name": "Cognizant",
   "close": 58.17,
   "ma240": 62.45,
   "ma480": 68.42,
   "matched": [
    "L2"
   ],
   "note": "급등 +44.5% 후 고점 대비 -10.0% 조정, 60일선 대비 +3.0%"
  },
  {
   "code": "CRWD",
   "name": "CrowdStrike",
   "close": 272.67,
   "ma240": 150.33,
   "ma480": 127.17,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "DDOG",
   "name": "Datadog",
   "close": 276.42,
   "ma240": 181.79,
   "ma480": 155.99,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "EMR",
   "name": "Emerson Electric",
   "close": 162.33,
   "ma240": 141.84,
   "ma480": 132.09,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "P",
   "name": "Everpure",
   "close": 143.88,
   "ma240": 80.0,
   "ma480": 70.25,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "FFIV",
   "name": "F5, Inc.",
   "close": 458.53,
   "ma240": 330.32,
   "ma480": 307.85,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "FDS",
   "name": "FactSet",
   "close": 276.44,
   "ma240": 251.58,
   "ma480": 334.0,
   "matched": [
    "L2"
   ],
   "note": "급등 +36.2% 후 고점 대비 -11.8% 조정, 60일선 대비 -0.4%"
  },
  {
   "code": "FTNT",
   "name": "Fortinet",
   "close": 184.13,
   "ma240": 113.05,
   "ma480": 104.46,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "HPE",
   "name": "Hewlett Packard Enterprise",
   "close": 68.36,
   "ma240": 34.56,
   "ma480": 27.09,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "ILMN",
   "name": "Illumina, Inc.",
   "close": 293.69,
   "ma240": 156.33,
   "ma480": 130.07,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "JCI",
   "name": "Johnson Controls",
   "close": 156.85,
   "ma240": 133.38,
   "ma480": 112.54,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "MRVL",
   "name": "Marvell Technology",
   "close": 271.25,
   "ma240": 154.49,
   "ma480": 118.13,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "MRNA",
   "name": "Moderna",
   "close": 203.21,
   "ma240": 62.04,
   "ma480": 46.91,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "NTAP",
   "name": "NetApp",
   "close": 223.77,
   "ma240": 134.38,
   "ma480": 120.5,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "NEM",
   "name": "Newmont",
   "close": 115.82,
   "ma240": 107.16,
   "ma480": 80.86,
   "matched": [
    "L2"
   ],
   "note": "급등 +48.0% 후 고점 대비 -14.1% 조정, 60일선 대비 +1.7%"
  },
  {
   "code": "NDSN",
   "name": "Nordson Corporation",
   "close": 334.43,
   "ma240": 277.0,
   "ma480": 244.94,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "NVDA",
   "name": "Nvidia",
   "close": 238.9,
   "ma240": 198.32,
   "ma480": 171.38,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "PANW",
   "name": "Palo Alto Networks",
   "close": 406.76,
   "ma240": 243.3,
   "ma480": 216.56,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "PSKY",
   "name": "Paramount Skydance Corporation",
   "close": 9.77,
   "ma240": 11.22,
   "ma480": 11.74,
   "matched": [
    "L2"
   ],
   "note": "급등 +38.3% 후 고점 대비 -12.3% 조정, 60일선 대비 +0.6%"
  },
  {
   "code": "RVTY",
   "name": "Revvity",
   "close": 157.36,
   "ma240": 104.89,
   "ma480": 103.27,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "STX",
   "name": "Seagate Technology",
   "close": 887.09,
   "ma240": 587.7,
   "ma480": 355.65,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.4% 후 고점 대비 -18.8% 조정, 60일선 대비 +3.9%"
  },
  {
   "code": "VTRS",
   "name": "Viatris",
   "close": 17.62,
   "ma240": 14.37,
   "ma480": 11.96,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "WBD",
   "name": "Warner Bros. Discovery",
   "close": 30.95,
   "ma240": 27.04,
   "ma480": 19.24,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "WAT",
   "name": "Waters Corporation",
   "close": 440.12,
   "ma240": 366.17,
   "ma480": 357.19,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  }
 ]
};
