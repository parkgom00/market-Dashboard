// 자동 생성 파일 (scanner/run_scan.py). 직접 고치지 마세요.
window.DASH = window.DASH || {};
window.DASH.longterm = {
 "swingRules": [
  {
   "id": "S1",
   "label": "상한가 후 조정 → 20일선 반등",
   "desc": "최근 40거래일 안에 상한가, 고점 대비 -10% 이상 조정 후 최근 5일 안에 20일선까지 내려왔다가 오늘 20일선 위에서 상승 마감 (국내만)"
  },
  {
   "id": "S2",
   "label": "상한가 후 조정 → 60일선 반등",
   "desc": "최근 120거래일 안에 상한가, 고점 대비 -10% 이상 조정 후 최근 5일 안에 60일선까지 내려왔다가 오늘 60일선 위에서 상승 마감 (국내만)"
  },
  {
   "id": "S3",
   "label": "급등 후 10일 이상 조정, 10일선 지지",
   "desc": "20일 안에 +30% 이상 급등, 고점 이후 10거래일 이상 조정, 종가가 10일선 ±3% 이내에서 지지"
  },
  {
   "id": "S4",
   "label": "급등 후 거래량 감소, 20일선 지지",
   "desc": "급등 후 최근 5일 평균 거래량이 급등 막바지의 50% 이하로 줄고, 상승 중인 20일선에서 지지"
  },
  {
   "id": "S5",
   "label": "외국인·기관 지속 유입 + 10일선 위 상승",
   "desc": "최근 10거래일 종가가 10일선을 이탈하지 않고 +3% 이상 상승, 최근 5거래일 중 4일 이상 외국인+기관 합계 순매수 (국내만, 수급은 네이버 공개분까지)"
  }
 ],
 "swing": {
  "kr": [],
  "us": [
   {
    "code": "ARM",
    "name": "Arm Holdings plc American Depositary Shares",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 302.56,
    "changePct": -1.48,
    "value": null,
    "close": 298.08,
    "ma10": 298.67,
    "ma20": 287.98,
    "ma60": 268.75,
    "ma240": 206.29,
    "ma480": 172.33,
    "matched": [
     "S3",
     "S4"
    ],
    "note": "급등 +41.9% 후 11일째 조정(-10.5%), 10일선 대비 -0.2% / 급등 +41.9% 후 거래량이 급등 때의 47%로 감소, 20일선 대비 +3.5%"
   },
   {
    "code": "BAX",
    "name": "Baxter International",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 24.36,
    "changePct": -0.1,
    "value": null,
    "close": 24.33,
    "ma10": 23.79,
    "ma20": 23.64,
    "ma60": 24.85,
    "ma240": 20.58,
    "ma480": 24.76,
    "matched": [
     "S3"
    ],
    "note": "급등 +30.8% 후 45일째 조정(-14.1%), 10일선 대비 +2.3%"
   },
   {
    "code": "DASH",
    "name": "DoorDash",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 193.62,
    "changePct": -1.33,
    "value": null,
    "close": 191.04,
    "ma10": 187.77,
    "ma20": 192.1,
    "ma60": 202.55,
    "ma240": 192.02,
    "ma480": 201.63,
    "matched": [
     "S3"
    ],
    "note": "급등 +31.0% 후 29일째 조정(-19.4%), 10일선 대비 +1.7%"
   },
   {
    "code": "IT",
    "name": "Gartner",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 184.92,
    "changePct": 1.2,
    "value": null,
    "close": 187.14,
    "ma10": 186.28,
    "ma20": 185.57,
    "ma60": 177.18,
    "ma240": 182.8,
    "ma480": 294.88,
    "matched": [
     "S3"
    ],
    "note": "급등 +46.2% 후 31일째 조정(-7.7%), 10일선 대비 +0.5%"
   },
   {
    "code": "PYPL",
    "name": "PayPal",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 54.61,
    "changePct": 0.43,
    "value": null,
    "close": 54.85,
    "ma10": 53.81,
    "ma20": 53.45,
    "ma60": 56.28,
    "ma240": 52.17,
    "ma480": 62.87,
    "matched": [
     "S3"
    ],
    "note": "급등 +36.3% 후 33일째 조정(-11.7%), 10일선 대비 +1.9%"
   },
   {
    "code": "NOW",
    "name": "ServiceNow",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 137.97,
    "changePct": 0.93,
    "value": null,
    "close": 139.25,
    "ma10": 135.42,
    "ma20": 136.57,
    "ma60": 126.32,
    "ma240": 124.68,
    "ma480": 158.74,
    "matched": [
     "S3"
    ],
    "note": "급등 +41.1% 후 26일째 조정(-5.9%), 10일선 대비 +2.8%"
   },
   {
    "code": "TRI",
    "name": "Thomson Reuters Corporation Common Shares",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 98.09,
    "changePct": 0.59,
    "value": null,
    "close": 98.67,
    "ma10": 98.1,
    "ma20": 98.36,
    "ma60": 100.06,
    "ma240": 102.58,
    "ma480": 135.43,
    "matched": [
     "S3"
    ],
    "note": "급등 +30.2% 후 23일째 조정(-11.7%), 10일선 대비 +0.6%"
   },
   {
    "code": "WDAY",
    "name": "Workday, Inc.",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [],
    "krRank": "",
    "prevClose": 186.55,
    "changePct": 0.01,
    "value": null,
    "close": 186.57,
    "ma10": 188.36,
    "ma20": 189.64,
    "ma60": 180.62,
    "ma240": 168.25,
    "ma480": 207.24,
    "matched": [
     "S3"
    ],
    "note": "급등 +61.5% 후 23일째 조정(-9.8%), 10일선 대비 -1.0%"
   },
   {
    "code": "RBLX",
    "name": "로블록스",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "게임"
    ],
    "krRank": "",
    "prevClose": 45.56,
    "changePct": 0.26,
    "value": null,
    "close": 45.68,
    "ma10": 44.36,
    "ma20": 46.42,
    "ma60": 43.72,
    "ma240": 62.58,
    "ma480": 74.58,
    "matched": [
     "S3"
    ],
    "note": "급등 +36.6% 후 17일째 조정(-10.9%), 10일선 대비 +3.0%"
   },
   {
    "code": "ABNB",
    "name": "에어비앤비",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "항공·여행"
    ],
    "krRank": "",
    "prevClose": 160.39,
    "changePct": 0.31,
    "value": null,
    "close": 160.88,
    "ma10": 159.08,
    "ma20": 162.27,
    "ma60": 166.3,
    "ma240": 140.42,
    "ma480": 135.37,
    "matched": [
     "S3"
    ],
    "note": "급등 +35.5% 후 30일째 조정(-15.5%), 10일선 대비 +1.1%"
   },
   {
    "code": "CRWV",
    "name": "코어위브",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "네오클라우드"
    ],
    "krRank": "",
    "prevClose": 91.72,
    "changePct": -4.06,
    "value": null,
    "close": 88.0,
    "ma10": 88.11,
    "ma20": 86.34,
    "ma60": 85.69,
    "ma240": 92.6,
    "ma480": null,
    "matched": [
     "S3"
    ],
    "note": "급등 +77.1% 후 39일째 조정(-18.3%), 10일선 대비 -0.1%"
   },
   {
    "code": "CLF",
    "name": "클리블랜드클리프스",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "철강"
    ],
    "krRank": "",
    "prevClose": 12.25,
    "changePct": -2.69,
    "value": null,
    "close": 11.92,
    "ma10": 11.71,
    "ma20": 11.96,
    "ma60": 11.65,
    "ma240": 11.49,
    "ma480": 10.72,
    "matched": [
     "S3"
    ],
    "note": "급등 +40.9% 후 10일째 조정(-7.4%), 10일선 대비 +1.8%"
   },
   {
    "code": "FCX",
    "name": "프리포트맥모란",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "구리·전선"
    ],
    "krRank": "",
    "prevClose": 72.56,
    "changePct": -1.58,
    "value": null,
    "close": 71.41,
    "ma10": 71.5,
    "ma20": 71.34,
    "ma60": 69.52,
    "ma240": 60.23,
    "ma480": 50.01,
    "matched": [
     "S3"
    ],
    "note": "급등 +33.2% 후 30일째 조정(-10.6%), 10일선 대비 -0.1%"
   },
   {
    "code": "NBIS",
    "name": "네비우스",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "네오클라우드"
    ],
    "krRank": "서학개미 보관 47위",
    "prevClose": 249.87,
    "changePct": -6.2,
    "value": null,
    "close": 234.38,
    "ma10": 237.78,
    "ma20": 229.82,
    "ma60": 217.45,
    "ma240": 158.43,
    "ma480": 103.09,
    "matched": [
     "S4"
    ],
    "note": "급등 +87.3% 후 거래량이 급등 때의 42%로 감소, 20일선 대비 +2.0%"
   },
   {
    "code": "META",
    "name": "메타",
    "market": "",
    "sector": "",
    "marcap": 0,
    "themes": [
     "빅테크·AI 소프트웨어"
    ],
    "krRank": "서학개미 보관 26위",
    "prevClose": 738.88,
    "changePct": -1.81,
    "value": null,
    "close": 725.54,
    "ma10": 736.92,
    "ma20": 711.85,
    "ma60": 632.51,
    "ma240": 631.49,
    "ma480": 644.7,
    "matched": [
     "S4"
    ],
    "note": "급등 +36.3% 후 거래량이 급등 때의 35%로 감소, 20일선 대비 +1.9%"
   }
  ]
 },
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
   "id": "L3",
   "label": "240·480일선 동시 거래량 돌파",
   "desc": "최근 3일 안에 240일선과 480일선을 모두 아래→위로 돌파, 각 돌파일 거래량이 직전 20일 평균의 2배 이상"
  },
  {
   "id": "L4",
   "label": "신고가 후 240일선 지지 → 전고점 향해 반등",
   "desc": "52주(또는 역사적) 신고가를 찍고 -15% 이상 조정, 조정 중 240일선 지지, 저점 대비 +8% 이상 반등해 전고점 아래에서 상승 중이며 최근 5일 종가가 20일선을 이탈하지 않음"
  }
 ],
 "scanInfo": {
  "kr": {
   "asOf": "2026-10-07",
   "scanned": 2710
  },
  "us": {
   "asOf": "2026-10-07",
   "scanned": 556
  }
 },
 "kr": [
  {
   "code": "236200",
   "name": "슈프리마",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 3892,
   "themes": [],
   "krRank": "",
   "prevClose": 60200.0,
   "changePct": -8.64,
   "value": 25,
   "close": 55000.0,
   "ma240": 44963.75,
   "ma480": 37323.96,
   "matched": [
    "L1",
    "L2"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인 / 급등 +41.2% 후 고점 대비 -13.7% 조정, 60일선 대비 +3.5%"
  },
  {
   "code": "375500",
   "name": "DL이앤씨",
   "market": "KOSPI",
   "sector": "",
   "marcap": 28053,
   "themes": [],
   "krRank": "",
   "prevClose": 74200.0,
   "changePct": -2.56,
   "value": 133,
   "close": 72300.0,
   "ma240": 61772.71,
   "ma480": 51101.46,
   "matched": [
    "L2"
   ],
   "note": "급등 +41.8% 후 고점 대비 -18.3% 조정, 60일선 대비 +1.0%"
  },
  {
   "code": "007340",
   "name": "DN오토모티브",
   "market": "KOSPI",
   "sector": "",
   "marcap": 28817,
   "themes": [],
   "krRank": "",
   "prevClose": 49700.0,
   "changePct": -1.11,
   "value": 47,
   "close": 49150.0,
   "ma240": 35545.42,
   "ma480": 28708.81,
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
   "marcap": 3121,
   "themes": [],
   "krRank": "",
   "prevClose": 3335.0,
   "changePct": 1.65,
   "value": 4,
   "close": 3390.0,
   "ma240": 3705.9,
   "ma480": 3535.67,
   "matched": [
    "L2"
   ],
   "note": "급등 +79.2% 후 고점 대비 -19.5% 조정, 60일선 대비 -0.6%"
  },
  {
   "code": "078930",
   "name": "GS",
   "market": "KOSPI",
   "sector": "",
   "marcap": 103021,
   "themes": [],
   "krRank": "",
   "prevClose": 106100.0,
   "changePct": 3.02,
   "value": 496,
   "close": 109300.0,
   "ma240": 74954.58,
   "ma480": 58650.62,
   "matched": [
    "L2"
   ],
   "note": "급등 +52.7% 후 고점 대비 -15.4% 조정, 60일선 대비 +3.9%"
  },
  {
   "code": "006360",
   "name": "GS건설",
   "market": "KOSPI",
   "sector": "",
   "marcap": 28327,
   "themes": [],
   "krRank": "",
   "prevClose": 33050.0,
   "changePct": -0.61,
   "value": 221,
   "close": 32850.0,
   "ma240": 26711.83,
   "ma480": 22765.25,
   "matched": [
    "L2"
   ],
   "note": "급등 +70.3% 후 고점 대비 -14.7% 조정, 60일선 대비 +0.2%"
  },
  {
   "code": "012630",
   "name": "HDC",
   "market": "KOSPI",
   "sector": "",
   "marcap": 13531,
   "themes": [],
   "krRank": "",
   "prevClose": 23250.0,
   "changePct": -2.37,
   "value": 10,
   "close": 22700.0,
   "ma240": 21702.88,
   "ma480": 19238.9,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.5% 후 고점 대비 -20.2% 조정, 60일선 대비 -0.5%"
  },
  {
   "code": "322000",
   "name": "HD현대에너지솔루션",
   "market": "KOSPI",
   "sector": "",
   "marcap": 16598,
   "themes": [],
   "krRank": "",
   "prevClose": 151400.0,
   "changePct": -3.17,
   "value": 327,
   "close": 146600.0,
   "ma240": 112688.33,
   "ma480": 73091.81,
   "matched": [
    "L2"
   ],
   "note": "급등 +62.7% 후 고점 대비 -14.5% 조정, 60일선 대비 +14.3%"
  },
  {
   "code": "294870",
   "name": "IPARK현대산업개발",
   "market": "KOSPI",
   "sector": "",
   "marcap": 14664,
   "themes": [],
   "krRank": "",
   "prevClose": 21750.0,
   "changePct": 1.61,
   "value": 16,
   "close": 22100.0,
   "ma240": 21118.08,
   "ma480": 21100.79,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.2% 후 고점 대비 -11.1% 조정, 60일선 대비 +1.4%"
  },
  {
   "code": "024840",
   "name": "KBI메탈",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2682,
   "themes": [],
   "krRank": "",
   "prevClose": 6420.0,
   "changePct": -5.3,
   "value": 158,
   "close": 6080.0,
   "ma240": 3468.92,
   "ma480": 2762.02,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "003550",
   "name": "LG",
   "market": "KOSPI",
   "sector": "",
   "marcap": 169637,
   "themes": [],
   "krRank": "",
   "prevClose": 114900.0,
   "changePct": -3.48,
   "value": 122,
   "close": 110900.0,
   "ma240": 97343.33,
   "ma480": 85244.17,
   "matched": [
    "L2"
   ],
   "note": "급등 +68.7% 후 고점 대비 -33.1% 조정, 60일선 대비 +1.7%"
  },
  {
   "code": "060250",
   "name": "NHN KCP",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 5422,
   "themes": [],
   "krRank": "",
   "prevClose": 13710.0,
   "changePct": -1.39,
   "value": 20,
   "close": 13520.0,
   "ma240": 16360.46,
   "ma480": 13171.44,
   "matched": [
    "L2"
   ],
   "note": "급등 +43.2% 후 고점 대비 -16.3% 조정, 60일선 대비 -1.0%"
  },
  {
   "code": "010060",
   "name": "OCI홀딩스",
   "market": "KOSPI",
   "sector": "",
   "marcap": 45742,
   "themes": [],
   "krRank": "",
   "prevClose": 245000.0,
   "changePct": -2.45,
   "value": 379,
   "close": 239000.0,
   "ma240": 194437.08,
   "ma480": 135510.83,
   "matched": [
    "L2"
   ],
   "note": "급등 +70.5% 후 고점 대비 -17.6% 조정, 60일선 대비 +4.2%"
  },
  {
   "code": "010950",
   "name": "S-Oil",
   "market": "KOSPI",
   "sector": "",
   "marcap": 191728,
   "themes": [],
   "krRank": "",
   "prevClose": 165000.0,
   "changePct": 2.79,
   "value": 637,
   "close": 169600.0,
   "ma240": 111509.17,
   "ma480": 84971.67,
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
   "marcap": 3571,
   "themes": [],
   "krRank": "",
   "prevClose": 86900.0,
   "changePct": 3.91,
   "value": 21,
   "close": 90300.0,
   "ma240": 56989.17,
   "ma480": 48021.88,
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
   "marcap": 268794,
   "themes": [],
   "krRank": "",
   "prevClose": 156700.0,
   "changePct": 1.4,
   "value": 1525,
   "close": 158900.0,
   "ma240": 119028.75,
   "ma480": 114741.25,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "089230",
   "name": "THE E&M",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 828,
   "themes": [],
   "krRank": "",
   "prevClose": 2020.0,
   "changePct": 1.24,
   "value": 25,
   "close": 2045.0,
   "ma240": 1853.18,
   "ma480": 1435.45,
   "matched": [
    "L2"
   ],
   "note": "급등 +114.4% 후 고점 대비 -16.2% 조정, 60일선 대비 +10.7%"
  },
  {
   "code": "002900",
   "name": "TYM",
   "market": "KOSPI",
   "sector": "",
   "marcap": 2745,
   "themes": [],
   "krRank": "",
   "prevClose": 6570.0,
   "changePct": 1.52,
   "value": 7,
   "close": 6670.0,
   "ma240": 6741.75,
   "ma480": 5838.93,
   "matched": [
    "L2"
   ],
   "note": "급등 +30.9% 후 고점 대비 -11.3% 조정, 60일선 대비 +0.1%"
  },
  {
   "code": "399720",
   "name": "가온칩스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 5574,
   "themes": [],
   "krRank": "",
   "prevClose": 48500.0,
   "changePct": -3.81,
   "value": 30,
   "close": 46650.0,
   "ma240": 54608.12,
   "ma480": 48948.12,
   "matched": [
    "L2"
   ],
   "note": "급등 +56.3% 후 고점 대비 -18.4% 조정, 60일선 대비 +2.2%"
  },
  {
   "code": "013580",
   "name": "계룡건설",
   "market": "KOSPI",
   "sector": "",
   "marcap": 1920,
   "themes": [],
   "krRank": "",
   "prevClose": 21550.0,
   "changePct": -0.7,
   "value": 4,
   "close": 21400.0,
   "ma240": 22131.58,
   "ma480": 19655.98,
   "matched": [
    "L2"
   ],
   "note": "급등 +40.6% 후 고점 대비 -17.1% 조정, 60일선 대비 +1.8%"
  },
  {
   "code": "950190",
   "name": "고스트스튜디오",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1267,
   "themes": [],
   "krRank": "",
   "prevClose": 9670.0,
   "changePct": -0.21,
   "value": 1,
   "close": 9650.0,
   "ma240": 8672.04,
   "ma480": 8827.04,
   "matched": [
    "L2"
   ],
   "note": "급등 +33.8% 후 고점 대비 -14.1% 조정, 60일선 대비 +1.5%"
  },
  {
   "code": "036800",
   "name": "나이스정보통신",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 3754,
   "themes": [],
   "krRank": "",
   "prevClose": 8340.0,
   "changePct": -1.44,
   "value": 6,
   "close": 8220.0,
   "ma240": 5527.12,
   "ma480": 4744.24,
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
   "marcap": 1446,
   "themes": [],
   "krRank": "",
   "prevClose": 11030.0,
   "changePct": -4.9,
   "value": 9,
   "close": 10490.0,
   "ma240": 9112.38,
   "ma480": 7339.42,
   "matched": [
    "L2"
   ],
   "note": "급등 +90.8% 후 고점 대비 -32.6% 조정, 60일선 대비 +0.4%"
  },
  {
   "code": "007390",
   "name": "네이처셀",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 16012,
   "themes": [],
   "krRank": "",
   "prevClose": 24850.0,
   "changePct": -0.6,
   "value": 26,
   "close": 24700.0,
   "ma240": 23038.79,
   "ma480": 22945.38,
   "matched": [
    "L2"
   ],
   "note": "급등 +99.6% 후 고점 대비 -28.5% 조정, 60일선 대비 +2.3%"
  },
  {
   "code": "144960",
   "name": "뉴파워프라즈마",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 5763,
   "themes": [],
   "krRank": "",
   "prevClose": 13800.0,
   "changePct": -4.2,
   "value": 164,
   "close": 13220.0,
   "ma240": 7430.31,
   "ma480": 6203.26,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "064260",
   "name": "다날",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 3461,
   "themes": [],
   "krRank": "",
   "prevClose": 4715.0,
   "changePct": -3.92,
   "value": 20,
   "close": 4530.0,
   "ma240": 6514.92,
   "ma480": 5691.56,
   "matched": [
    "L2"
   ],
   "note": "급등 +31.6% 후 고점 대비 -18.4% 조정, 60일선 대비 -3.3%"
  },
  {
   "code": "000490",
   "name": "대동",
   "market": "KOSPI",
   "sector": "",
   "marcap": 2194,
   "themes": [],
   "krRank": "",
   "prevClose": 7700.0,
   "changePct": -1.95,
   "value": 8,
   "close": 7550.0,
   "ma240": 9042.25,
   "ma480": 9749.77,
   "matched": [
    "L2"
   ],
   "note": "급등 +44.0% 후 고점 대비 -11.0% 조정, 60일선 대비 +1.6%"
  },
  {
   "code": "045390",
   "name": "대아티아이",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2125,
   "themes": [],
   "krRank": "",
   "prevClose": 3060.0,
   "changePct": -1.8,
   "value": 12,
   "close": 3005.0,
   "ma240": 3753.71,
   "ma480": 3824.56,
   "matched": [
    "L2"
   ],
   "note": "급등 +51.2% 후 고점 대비 -20.8% 조정, 60일선 대비 +2.4%"
  },
  {
   "code": "006340",
   "name": "대원전선",
   "market": "KOSPI",
   "sector": "",
   "marcap": 10327,
   "themes": [],
   "krRank": "",
   "prevClose": 13430.0,
   "changePct": -3.43,
   "value": 289,
   "close": 12970.0,
   "ma240": 8298.23,
   "ma480": 5640.8,
   "matched": [
    "L2"
   ],
   "note": "급등 +60.4% 후 고점 대비 -19.1% 조정, 60일선 대비 -2.1%"
  },
  {
   "code": "003490",
   "name": "대한항공",
   "market": "KOSPI",
   "sector": "",
   "marcap": 114148,
   "themes": [],
   "krRank": "",
   "prevClose": 31250.0,
   "changePct": -1.6,
   "value": 372,
   "close": 30750.0,
   "ma240": 25179.38,
   "ma480": 24261.25,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "028100",
   "name": "동아지질",
   "market": "KOSPI",
   "sector": "",
   "marcap": 2188,
   "themes": [],
   "krRank": "",
   "prevClose": 19820.0,
   "changePct": 0.4,
   "value": 3,
   "close": 19900.0,
   "ma240": 16916.21,
   "ma480": 15788.25,
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
   "marcap": 18590,
   "themes": [],
   "krRank": "",
   "prevClose": 50900.0,
   "changePct": 0.79,
   "value": 31,
   "close": 51300.0,
   "ma240": 34652.5,
   "ma480": 32415.52,
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
   "marcap": 6936,
   "themes": [],
   "krRank": "",
   "prevClose": 2180.0,
   "changePct": 2.98,
   "value": 15,
   "close": 2245.0,
   "ma240": 1982.0,
   "ma480": 1918.75,
   "matched": [
    "L2"
   ],
   "note": "급등 +58.3% 후 고점 대비 -15.3% 조정, 60일선 대비 +6.9%"
  },
  {
   "code": "280360",
   "name": "롯데웰푸드",
   "market": "KOSPI",
   "sector": "",
   "marcap": 11276,
   "themes": [],
   "krRank": "",
   "prevClose": 119900.0,
   "changePct": 2.34,
   "value": 13,
   "close": 122700.0,
   "ma240": 116842.92,
   "ma480": 116268.54,
   "matched": [
    "L2"
   ],
   "note": "급등 +46.0% 후 고점 대비 -17.4% 조정, 60일선 대비 +0.5%"
  },
  {
   "code": "377450",
   "name": "리파인",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2452,
   "themes": [],
   "krRank": "",
   "prevClose": 14100.0,
   "changePct": 0.0,
   "value": 1,
   "close": 14100.0,
   "ma240": 12363.29,
   "ma480": 13163.21,
   "matched": [
    "L2"
   ],
   "note": "급등 +59.6% 후 고점 대비 -18.0% 조정, 60일선 대비 -0.2%"
  },
  {
   "code": "446540",
   "name": "메가터치",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 3205,
   "themes": [],
   "krRank": "",
   "prevClose": 11650.0,
   "changePct": -5.41,
   "value": 46,
   "close": 11020.0,
   "ma240": 5583.25,
   "ma480": 4697.83,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "140410",
   "name": "메지온",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 21063,
   "themes": [],
   "krRank": "",
   "prevClose": 70800.0,
   "changePct": -4.66,
   "value": 49,
   "close": 67500.0,
   "ma240": 82547.08,
   "ma480": 59763.85,
   "matched": [
    "L2"
   ],
   "note": "급등 +35.7% 후 고점 대비 -17.9% 조정, 60일선 대비 +4.9%"
  },
  {
   "code": "083650",
   "name": "비에이치아이",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 17824,
   "themes": [],
   "krRank": "",
   "prevClose": 58700.0,
   "changePct": -2.73,
   "value": 141,
   "close": 57100.0,
   "ma240": 66484.17,
   "ma480": 47688.94,
   "matched": [
    "L2"
   ],
   "note": "급등 +89.0% 후 고점 대비 -16.5% 조정, 60일선 대비 +3.0%"
  },
  {
   "code": "018260",
   "name": "삼성에스디에스",
   "market": "KOSPI",
   "sector": "",
   "marcap": 162880,
   "themes": [],
   "krRank": "",
   "prevClose": 220000.0,
   "changePct": -5.45,
   "value": 368,
   "close": 208000.0,
   "ma240": 190197.92,
   "ma480": 165753.54,
   "matched": [
    "L2"
   ],
   "note": "급등 +119.7% 후 고점 대비 -42.5% 조정, 60일선 대비 -5.2%"
  },
  {
   "code": "0120G0",
   "name": "삼양바이오팜",
   "market": "KOSPI",
   "sector": "",
   "marcap": 3770,
   "themes": [],
   "krRank": "",
   "prevClose": 50900.0,
   "changePct": -1.77,
   "value": 19,
   "close": 50000.0,
   "ma240": null,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +83.2% 후 고점 대비 -19.5% 조정, 60일선 대비 +6.3%"
  },
  {
   "code": "252990",
   "name": "샘씨엔에스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 11514,
   "themes": [],
   "krRank": "",
   "prevClose": 19880.0,
   "changePct": -4.53,
   "value": 143,
   "close": 18980.0,
   "ma240": 11100.92,
   "ma480": 7985.49,
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
   "marcap": 938,
   "themes": [],
   "krRank": "",
   "prevClose": 46400.0,
   "changePct": 0.86,
   "value": 4,
   "close": 46800.0,
   "ma240": 48757.71,
   "ma480": 46346.35,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.2% 후 고점 대비 -18.6% 조정, 60일선 대비 +3.6%"
  },
  {
   "code": "079650",
   "name": "서산",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1084,
   "themes": [],
   "krRank": "",
   "prevClose": 5640.0,
   "changePct": -4.61,
   "value": 28,
   "close": 5380.0,
   "ma240": 2634.77,
   "ma480": 2007.14,
   "matched": [
    "L2"
   ],
   "note": "급등 +729.4% 후 고점 대비 -33.7% 조정, 60일선 대비 +0.3%"
  },
  {
   "code": "035890",
   "name": "서희건설",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 4515,
   "themes": [],
   "krRank": "",
   "prevClose": 2220.0,
   "changePct": -2.7,
   "value": 4,
   "close": 2160.0,
   "ma240": 2826.52,
   "ma480": 2797.87,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.8% 후 고점 대비 -19.3% 조정, 60일선 대비 +0.5%"
  },
  {
   "code": "108860",
   "name": "셀바스AI",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2455,
   "themes": [],
   "krRank": "",
   "prevClose": 9520.0,
   "changePct": -5.46,
   "value": 19,
   "close": 9000.0,
   "ma240": 11143.04,
   "ma480": 12242.08,
   "matched": [
    "L2"
   ],
   "note": "급등 +75.8% 후 고점 대비 -17.8% 조정, 60일선 대비 +2.4%"
  },
  {
   "code": "304100",
   "name": "솔트룩스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1898,
   "themes": [],
   "krRank": "",
   "prevClose": 15620.0,
   "changePct": -4.1,
   "value": 9,
   "close": 14980.0,
   "ma240": 22006.29,
   "ma480": 26330.31,
   "matched": [
    "L2"
   ],
   "note": "급등 +81.5% 후 고점 대비 -19.5% 조정, 60일선 대비 +1.8%"
  },
  {
   "code": "099440",
   "name": "스맥",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2638,
   "themes": [],
   "krRank": "",
   "prevClose": 3885.0,
   "changePct": -1.54,
   "value": 5,
   "close": 3825.0,
   "ma240": 4625.65,
   "ma480": 3824.91,
   "matched": [
    "L2"
   ],
   "note": "급등 +65.1% 후 고점 대비 -16.1% 조정, 60일선 대비 +1.1%"
  },
  {
   "code": "340810",
   "name": "시선AI",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 504,
   "themes": [],
   "krRank": "",
   "prevClose": 3620.0,
   "changePct": 0.83,
   "value": 3,
   "close": 3650.0,
   "ma240": 3064.52,
   "ma480": 3371.58,
   "matched": [
    "L2"
   ],
   "note": "급등 +66.8% 후 고점 대비 -20.8% 조정, 60일선 대비 +6.7%"
  },
  {
   "code": "004770",
   "name": "써니전자",
   "market": "KOSPI",
   "sector": "",
   "marcap": 632,
   "themes": [],
   "krRank": "",
   "prevClose": 1801.0,
   "changePct": -1.28,
   "value": 9,
   "close": 1778.0,
   "ma240": 1675.3,
   "ma480": 1788.04,
   "matched": [
    "L2"
   ],
   "note": "급등 +46.6% 후 고점 대비 -25.1% 조정, 60일선 대비 -3.3%"
  },
  {
   "code": "475400",
   "name": "씨메스로보틱스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2184,
   "themes": [],
   "krRank": "",
   "prevClose": 19340.0,
   "changePct": -5.07,
   "value": 6,
   "close": 18360.0,
   "ma240": 28489.0,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +51.9% 후 고점 대비 -14.8% 조정, 60일선 대비 +0.9%"
  },
  {
   "code": "159010",
   "name": "아스플로",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 4414,
   "themes": [],
   "krRank": "",
   "prevClose": 32150.0,
   "changePct": 1.4,
   "value": 37,
   "close": 32600.0,
   "ma240": 11504.54,
   "ma480": 8002.93,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "052860",
   "name": "아이앤씨",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1344,
   "themes": [],
   "krRank": "",
   "prevClose": 7680.0,
   "changePct": -1.56,
   "value": 3,
   "close": 7560.0,
   "ma240": 4239.29,
   "ma480": 3097.58,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "052460",
   "name": "아이크래프트",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 872,
   "themes": [],
   "krRank": "",
   "prevClose": 6250.0,
   "changePct": -5.6,
   "value": 10,
   "close": 5900.0,
   "ma240": 3657.52,
   "ma480": 3063.43,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "124500",
   "name": "아이티센글로벌",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 6660,
   "themes": [],
   "krRank": "",
   "prevClose": 30350.0,
   "changePct": -7.41,
   "value": 59,
   "close": 28100.0,
   "ma240": 36021.33,
   "ma480": 23601.66,
   "matched": [
    "L2"
   ],
   "note": "급등 +119.4% 후 고점 대비 -30.6% 조정, 60일선 대비 +1.1%"
  },
  {
   "code": "078520",
   "name": "에이블씨엔씨",
   "market": "KOSPI",
   "sector": "",
   "marcap": 2883,
   "themes": [],
   "krRank": "",
   "prevClose": 10950.0,
   "changePct": 7.85,
   "value": 18,
   "close": 11810.0,
   "ma240": 11103.29,
   "ma480": 9629.67,
   "matched": [
    "L2"
   ],
   "note": "급등 +41.7% 후 고점 대비 -12.1% 조정, 60일선 대비 +7.9%"
  },
  {
   "code": "000670",
   "name": "영풍",
   "market": "KOSPI",
   "sector": "",
   "marcap": 7420,
   "themes": [],
   "krRank": "",
   "prevClose": 41450.0,
   "changePct": -3.5,
   "value": 9,
   "close": 40000.0,
   "ma240": 50959.96,
   "ma480": 45446.1,
   "matched": [
    "L2"
   ],
   "note": "급등 +33.9% 후 고점 대비 -19.9% 조정, 60일선 대비 +2.5%"
  },
  {
   "code": "101160",
   "name": "월덱스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 5366,
   "themes": [],
   "krRank": "",
   "prevClose": 32950.0,
   "changePct": -1.67,
   "value": 11,
   "close": 32400.0,
   "ma240": 27434.17,
   "ma480": 23511.94,
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
   "marcap": 949,
   "themes": [],
   "krRank": "",
   "prevClose": 7210.0,
   "changePct": -1.53,
   "value": 4,
   "close": 7100.0,
   "ma240": 7683.96,
   "ma480": 7326.65,
   "matched": [
    "L2"
   ],
   "note": "급등 +49.8% 후 고점 대비 -21.1% 조정, 60일선 대비 -1.6%"
  },
  {
   "code": "333430",
   "name": "일승",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1172,
   "themes": [],
   "krRank": "",
   "prevClose": 3895.0,
   "changePct": -3.21,
   "value": 4,
   "close": 3770.0,
   "ma240": 5250.81,
   "ma480": 5017.46,
   "matched": [
    "L2"
   ],
   "note": "급등 +49.1% 후 고점 대비 -14.7% 조정, 60일선 대비 +1.2%"
  },
  {
   "code": "003200",
   "name": "일신방직",
   "market": "KOSPI",
   "sector": "",
   "marcap": 2537,
   "themes": [],
   "krRank": "",
   "prevClose": 10910.0,
   "changePct": 1.65,
   "value": 5,
   "close": 11090.0,
   "ma240": 11767.92,
   "ma480": 10394.83,
   "matched": [
    "L2"
   ],
   "note": "급등 +34.7% 후 고점 대비 -13.4% 조정, 60일선 대비 +4.4%"
  },
  {
   "code": "420570",
   "name": "제이투케이바이오",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 546,
   "themes": [],
   "krRank": "",
   "prevClose": 9190.0,
   "changePct": 7.83,
   "value": 6,
   "close": 9910.0,
   "ma240": 8518.0,
   "ma480": 9513.17,
   "matched": [
    "L2"
   ],
   "note": "급등 +53.1% 후 고점 대비 -17.4% 조정, 60일선 대비 +6.6%"
  },
  {
   "code": "228760",
   "name": "지노믹트리",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2981,
   "themes": [],
   "krRank": "",
   "prevClose": 12250.0,
   "changePct": -2.53,
   "value": 8,
   "close": 11940.0,
   "ma240": 17974.08,
   "ma480": 17427.71,
   "matched": [
    "L2"
   ],
   "note": "급등 +43.9% 후 고점 대비 -19.7% 조정, 60일선 대비 +2.6%"
  },
  {
   "code": "029460",
   "name": "케이씨",
   "market": "KOSPI",
   "sector": "",
   "marcap": 5196,
   "themes": [],
   "krRank": "",
   "prevClose": 45400.0,
   "changePct": 3.74,
   "value": 29,
   "close": 47100.0,
   "ma240": 31793.96,
   "ma480": 26041.94,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "391710",
   "name": "코닉오토메이션",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 531,
   "themes": [],
   "krRank": "",
   "prevClose": 1295.0,
   "changePct": -2.78,
   "value": 1,
   "close": 1259.0,
   "ma240": 1907.5,
   "ma480": 1842.06,
   "matched": [
    "L2"
   ],
   "note": "급등 +37.5% 후 고점 대비 -14.4% 조정, 60일선 대비 +4.8%"
  },
  {
   "code": "041960",
   "name": "코미팜",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 8186,
   "themes": [],
   "krRank": "",
   "prevClose": 10490.0,
   "changePct": 4.86,
   "value": 79,
   "close": 11000.0,
   "ma240": 7951.79,
   "ma480": 6425.49,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "021240",
   "name": "코웨이",
   "market": "KOSPI",
   "sector": "",
   "marcap": 72466,
   "themes": [],
   "krRank": "",
   "prevClose": 100300.0,
   "changePct": 1.89,
   "value": 118,
   "close": 102200.0,
   "ma240": 88130.83,
   "ma480": 86900.83,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "237880",
   "name": "클리오",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2226,
   "themes": [],
   "krRank": "",
   "prevClose": 11990.0,
   "changePct": 3.92,
   "value": 11,
   "close": 12460.0,
   "ma240": 12365.29,
   "ma480": 14897.94,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.2% 후 고점 대비 -12.4% 조정, 60일선 대비 +5.6%"
  },
  {
   "code": "219130",
   "name": "타이거일렉",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 6220,
   "themes": [],
   "krRank": "",
   "prevClose": 92200.0,
   "changePct": 7.05,
   "value": 123,
   "close": 98700.0,
   "ma240": 45356.12,
   "ma480": 30261.12,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "134580",
   "name": "탑코미디어",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1225,
   "themes": [],
   "krRank": "",
   "prevClose": 2530.0,
   "changePct": -6.52,
   "value": 15,
   "close": 2365.0,
   "ma240": 1924.59,
   "ma480": 1958.85,
   "matched": [
    "L2"
   ],
   "note": "급등 +335.4% 후 고점 대비 -44.2% 조정, 60일선 대비 +1.8%"
  },
  {
   "code": "131290",
   "name": "티에스이",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 33571,
   "themes": [],
   "krRank": "",
   "prevClose": 311000.0,
   "changePct": -0.32,
   "value": 799,
   "close": 310000.0,
   "ma240": 149856.67,
   "ma480": 96441.67,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "103140",
   "name": "풍산",
   "market": "KOSPI",
   "sector": "",
   "marcap": 19085,
   "themes": [],
   "krRank": "",
   "prevClose": 76700.0,
   "changePct": -11.08,
   "value": 307,
   "close": 68200.0,
   "ma240": 94224.17,
   "ma480": 88585.42,
   "matched": [
    "L2"
   ],
   "note": "급등 +51.8% 후 고점 대비 -22.1% 조정, 60일선 대비 -8.9%"
  },
  {
   "code": "300080",
   "name": "플리토",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1367,
   "themes": [],
   "krRank": "",
   "prevClose": 8470.0,
   "changePct": -4.13,
   "value": 9,
   "close": 8120.0,
   "ma240": 11937.88,
   "ma480": 10006.79,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.6% 후 고점 대비 -20.4% 조정, 60일선 대비 -2.8%"
  },
  {
   "code": "032580",
   "name": "피델릭스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 2492,
   "themes": [],
   "krRank": "",
   "prevClose": 7920.0,
   "changePct": -2.53,
   "value": 45,
   "close": 7720.0,
   "ma240": 2781.9,
   "ma480": 2027.11,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 60일선 지지 확인"
  },
  {
   "code": "005430",
   "name": "한국공항",
   "market": "KOSPI",
   "sector": "",
   "marcap": 3040,
   "themes": [],
   "krRank": "",
   "prevClose": 95900.0,
   "changePct": 0.83,
   "value": 3,
   "close": 96700.0,
   "ma240": 70307.08,
   "ma480": 63206.35,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "017890",
   "name": "한국알콜",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 3297,
   "themes": [],
   "krRank": "",
   "prevClose": 15810.0,
   "changePct": 1.83,
   "value": 13,
   "close": 16100.0,
   "ma240": 12036.08,
   "ma480": 10568.06,
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
   "marcap": 24161,
   "themes": [],
   "krRank": "",
   "prevClose": 25300.0,
   "changePct": 0.79,
   "value": 9,
   "close": 25500.0,
   "ma240": 25625.0,
   "ma480": 22109.85,
   "matched": [
    "L2"
   ],
   "note": "급등 +36.8% 후 고점 대비 -16.8% 조정, 60일선 대비 +2.7%"
  },
  {
   "code": "448900",
   "name": "한국피아이엠",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 3353,
   "themes": [],
   "krRank": "",
   "prevClose": 58200.0,
   "changePct": -6.19,
   "value": 18,
   "close": 54600.0,
   "ma240": 70275.62,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +81.3% 후 고점 대비 -24.8% 조정, 60일선 대비 +1.9%"
  },
  {
   "code": "053690",
   "name": "한미글로벌",
   "market": "KOSPI",
   "sector": "",
   "marcap": 2208,
   "themes": [],
   "krRank": "",
   "prevClose": 20850.0,
   "changePct": -2.64,
   "value": 22,
   "close": 20300.0,
   "ma240": 20705.42,
   "ma480": 19337.29,
   "matched": [
    "L2"
   ],
   "note": "급등 +60.7% 후 고점 대비 -16.1% 조정, 60일선 대비 +4.7%"
  },
  {
   "code": "008930",
   "name": "한미사이언스",
   "market": "KOSPI",
   "sector": "",
   "marcap": 39394,
   "themes": [],
   "krRank": "",
   "prevClose": 57700.0,
   "changePct": 1.91,
   "value": 79,
   "close": 58800.0,
   "ma240": 39125.62,
   "ma480": 37101.15,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "051600",
   "name": "한전KPS",
   "market": "KOSPI",
   "sector": "",
   "marcap": 20160,
   "themes": [],
   "krRank": "",
   "prevClose": 45600.0,
   "changePct": -2.63,
   "value": 41,
   "close": 44400.0,
   "ma240": 52293.54,
   "ma480": 49467.29,
   "matched": [
    "L2"
   ],
   "note": "급등 +39.2% 후 고점 대비 -30.5% 조정, 60일선 대비 -2.8%"
  },
  {
   "code": "130660",
   "name": "한전산업",
   "market": "KOSPI",
   "sector": "",
   "marcap": 4003,
   "themes": [],
   "krRank": "",
   "prevClose": 12450.0,
   "changePct": -2.65,
   "value": 20,
   "close": 12120.0,
   "ma240": 14238.29,
   "ma480": 13003.38,
   "matched": [
    "L2"
   ],
   "note": "급등 +44.2% 후 고점 대비 -10.7% 조정, 60일선 대비 +3.0%"
  },
  {
   "code": "180640",
   "name": "한진칼",
   "market": "KOSPI",
   "sector": "",
   "marcap": 89461,
   "themes": [],
   "krRank": "",
   "prevClose": 133900.0,
   "changePct": -0.6,
   "value": 40,
   "close": 133100.0,
   "ma240": 118759.58,
   "ma480": 107860.83,
   "matched": [
    "L2"
   ],
   "note": "급등 +30.0% 후 고점 대비 -10.6% 조정, 60일선 대비 +5.8%"
  },
  {
   "code": "088350",
   "name": "한화생명",
   "market": "KOSPI",
   "sector": "",
   "marcap": 46553,
   "themes": [],
   "krRank": "",
   "prevClose": 5280.0,
   "changePct": 0.95,
   "value": 84,
   "close": 5330.0,
   "ma240": 4392.79,
   "ma480": 3644.03,
   "matched": [
    "L2"
   ],
   "note": "급등 +41.5% 후 고점 대비 -12.8% 조정, 60일선 대비 +3.0%"
  },
  {
   "code": "000370",
   "name": "한화손해보험",
   "market": "KOSPI",
   "sector": "",
   "marcap": 8615,
   "themes": [],
   "krRank": "",
   "prevClose": 7240.0,
   "changePct": 1.1,
   "value": 19,
   "close": 7320.0,
   "ma240": 6403.58,
   "ma480": 5615.79,
   "matched": [
    "L2"
   ],
   "note": "급등 +58.5% 후 고점 대비 -18.2% 조정, 60일선 대비 +4.1%"
  },
  {
   "code": "076610",
   "name": "해성옵틱스",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 708,
   "themes": [],
   "krRank": "",
   "prevClose": 1179.0,
   "changePct": -1.78,
   "value": 7,
   "close": 1158.0,
   "ma240": 1162.57,
   "ma480": 951.95,
   "matched": [
    "L2"
   ],
   "note": "급등 +64.0% 후 고점 대비 -25.0% 조정, 60일선 대비 -2.3%"
  },
  {
   "code": "000720",
   "name": "현대건설",
   "market": "KOSPI",
   "sector": "",
   "marcap": 123828,
   "themes": [],
   "krRank": "",
   "prevClose": 113100.0,
   "changePct": -1.95,
   "value": 477,
   "close": 110900.0,
   "ma240": 114927.92,
   "ma480": 80280.83,
   "matched": [
    "L2"
   ],
   "note": "급등 +59.6% 후 고점 대비 -17.8% 조정, 60일선 대비 -2.2%"
  },
  {
   "code": "004020",
   "name": "현대제철",
   "market": "KOSPI",
   "sector": "",
   "marcap": 38032,
   "themes": [],
   "krRank": "",
   "prevClose": 30050.0,
   "changePct": -5.16,
   "value": 242,
   "close": 28500.0,
   "ma240": 33186.46,
   "ma480": 30357.29,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.8% 후 고점 대비 -20.5% 조정, 60일선 대비 -3.4%"
  },
  {
   "code": "024060",
   "name": "흥구석유",
   "market": "KOSDAQ",
   "sector": "",
   "marcap": 1826,
   "themes": [],
   "krRank": "",
   "prevClose": 12100.0,
   "changePct": 0.74,
   "value": 56,
   "close": 12190.0,
   "ma240": 14026.08,
   "ma480": 13392.4,
   "matched": [
    "L2"
   ],
   "note": "급등 +56.4% 후 고점 대비 -20.1% 조정, 60일선 대비 +4.4%"
  }
 ],
 "us": [
  {
   "code": "AES",
   "name": "AES Corporation",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 14.93,
   "changePct": -0.1,
   "value": null,
   "close": 14.91,
   "ma10": 14.89,
   "ma20": 14.85,
   "ma60": 14.76,
   "ma240": 14.3,
   "ma480": 12.83,
   "matched": [
    "L1",
    "L4"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인 / 02/27 52주 신고가 후 -20.7% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -13.4%)"
  },
  {
   "code": "APH",
   "name": "Amphenol",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 88.62,
   "changePct": -1.5,
   "value": null,
   "close": 87.29,
   "ma10": 85.62,
   "ma20": 82.73,
   "ma60": 80.95,
   "ma240": 73.22,
   "ma480": 58.2,
   "matched": [
    "L1",
    "L4"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인 / 06/30 역사적 신고가 후 -21.8% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -2.0%)"
  },
  {
   "code": "ETN",
   "name": "이튼",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "전력 인프라"
   ],
   "krRank": "",
   "prevClose": 445.09,
   "changePct": -3.36,
   "value": null,
   "close": 430.12,
   "ma10": 435.56,
   "ma20": 426.22,
   "ma60": 420.38,
   "ma240": 382.78,
   "ma480": 356.78,
   "matched": [
    "L1",
    "L4"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인 / 08/12 역사적 신고가 후 -19.5% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -10.0%)"
  },
  {
   "code": "AMD",
   "name": "AMD",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "반도체·AI 인프라"
   ],
   "krRank": "서학개미 보관 22위",
   "prevClose": 649.42,
   "changePct": -0.96,
   "value": null,
   "close": 643.19,
   "ma10": 626.11,
   "ma20": 587.49,
   "ma60": 521.12,
   "ma240": 356.12,
   "ma480": 245.35,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "ASML",
   "name": "ASML",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "반도체 장비"
   ],
   "krRank": "서학개미 보관 40위",
   "prevClose": 1834.1,
   "changePct": -1.68,
   "value": null,
   "close": 1803.36,
   "ma10": 1805.7,
   "ma20": 1736.25,
   "ma60": 1734.15,
   "ma240": 1467.66,
   "ma480": 1106.99,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "ABBV",
   "name": "AbbVie",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 266.69,
   "changePct": 2.97,
   "value": null,
   "close": 274.61,
   "ma10": 265.04,
   "ma20": 263.63,
   "ma60": 257.86,
   "ma240": 228.67,
   "ma480": 207.55,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "AME",
   "name": "Ametek",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 253.72,
   "changePct": -2.25,
   "value": null,
   "close": 248.0,
   "ma10": 250.33,
   "ma20": 244.19,
   "ma60": 243.15,
   "ma240": 224.51,
   "ma480": 202.08,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "BBY",
   "name": "Best Buy",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 84.85,
   "changePct": -0.04,
   "value": null,
   "close": 84.82,
   "ma10": 88.11,
   "ma20": 90.1,
   "ma60": 86.59,
   "ma240": 71.92,
   "ma480": 71.28,
   "matched": [
    "L2"
   ],
   "note": "급등 +39.5% 후 고점 대비 -10.5% 조정, 60일선 대비 -2.0%"
  },
  {
   "code": "CRL",
   "name": "Charles River Laboratories",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 304.96,
   "changePct": -0.75,
   "value": null,
   "close": 302.67,
   "ma10": 296.83,
   "ma20": 287.0,
   "ma60": 271.51,
   "ma240": 206.32,
   "ma480": 183.82,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "CTSH",
   "name": "Cognizant",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 57.22,
   "changePct": -0.42,
   "value": null,
   "close": 56.98,
   "ma10": 57.73,
   "ma20": 59.19,
   "ma60": 56.93,
   "ma240": 62.37,
   "ma480": 68.36,
   "matched": [
    "L2"
   ],
   "note": "급등 +44.5% 후 고점 대비 -11.9% 조정, 60일선 대비 +0.1%"
  },
  {
   "code": "CRWD",
   "name": "CrowdStrike",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 278.86,
   "changePct": -3.96,
   "value": null,
   "close": 267.83,
   "ma10": 265.4,
   "ma20": 251.71,
   "ma60": 219.74,
   "ma240": 151.56,
   "ma480": 127.99,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "DDOG",
   "name": "Datadog",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 278.24,
   "changePct": -1.19,
   "value": null,
   "close": 274.94,
   "ma10": 271.94,
   "ma20": 253.17,
   "ma60": 247.61,
   "ma240": 182.8,
   "ma480": 156.62,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "EMR",
   "name": "Emerson Electric",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 161.4,
   "changePct": -1.37,
   "value": null,
   "close": 159.19,
   "ma10": 158.92,
   "ma20": 154.44,
   "ma60": 152.99,
   "ma240": 142.1,
   "ma480": 132.3,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "P",
   "name": "Everpure",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 147.2,
   "changePct": 2.22,
   "value": null,
   "close": 150.47,
   "ma10": 135.39,
   "ma20": 118.85,
   "ma60": 100.77,
   "ma240": 80.49,
   "ma480": 70.66,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "FFIV",
   "name": "F5, Inc.",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 469.79,
   "changePct": 0.21,
   "value": null,
   "close": 470.77,
   "ma10": 450.52,
   "ma20": 440.37,
   "ma60": 413.55,
   "ma240": 331.75,
   "ma480": 308.84,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "FDS",
   "name": "FactSet",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 272.01,
   "changePct": 1.01,
   "value": null,
   "close": 274.76,
   "ma10": 270.87,
   "ma20": 273.22,
   "ma60": 278.05,
   "ma240": 251.47,
   "ma480": 333.25,
   "matched": [
    "L2"
   ],
   "note": "급등 +36.2% 후 고점 대비 -12.4% 조정, 60일선 대비 -1.2%"
  },
  {
   "code": "FAST",
   "name": "Fastenal",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 50.81,
   "changePct": -1.11,
   "value": null,
   "close": 50.24,
   "ma10": 50.39,
   "ma20": 49.95,
   "ma60": 49.37,
   "ma240": 45.1,
   "ma480": 42.85,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "FTNT",
   "name": "Fortinet",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 191.27,
   "changePct": -0.26,
   "value": null,
   "close": 190.77,
   "ma10": 180.9,
   "ma20": 175.45,
   "ma60": 164.34,
   "ma240": 113.94,
   "ma480": 104.93,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "GEV",
   "name": "GE베르노바",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "전력 인프라"
   ],
   "krRank": "",
   "prevClose": 1029.21,
   "changePct": -3.22,
   "value": null,
   "close": 996.05,
   "ma10": 976.68,
   "ma20": 952.21,
   "ma60": 976.51,
   "ma240": 868.3,
   "ma480": 658.57,
   "matched": [
    "L4"
   ],
   "note": "07/06 역사적 신고가 후 -27.4% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -16.7%)"
  },
  {
   "code": "GRMN",
   "name": "Garmin",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 279.21,
   "changePct": -1.31,
   "value": null,
   "close": 275.55,
   "ma10": 286.42,
   "ma20": 282.81,
   "ma60": 281.57,
   "ma240": 238.61,
   "ma480": 225.35,
   "matched": [
    "L2"
   ],
   "note": "급등 +32.3% 후 고점 대비 -11.7% 조정, 60일선 대비 -2.1%"
  },
  {
   "code": "ILMN",
   "name": "Illumina, Inc.",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 273.54,
   "changePct": -0.1,
   "value": null,
   "close": 273.26,
   "ma10": 274.07,
   "ma20": 251.72,
   "ma60": 218.57,
   "ma240": 157.79,
   "ma480": 130.57,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "JCI",
   "name": "Johnson Controls",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 158.76,
   "changePct": -2.03,
   "value": null,
   "close": 155.54,
   "ma10": 152.17,
   "ma20": 147.31,
   "ma60": 145.71,
   "ma240": 133.79,
   "ma480": 112.89,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "MPC",
   "name": "Marathon Petroleum",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 432.36,
   "changePct": 1.82,
   "value": null,
   "close": 440.22,
   "ma10": 410.99,
   "ma20": 407.34,
   "ma60": 362.29,
   "ma240": 251.88,
   "ma480": 203.3,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "MAR",
   "name": "Marriott International",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 361.28,
   "changePct": -1.23,
   "value": null,
   "close": 356.85,
   "ma10": 356.72,
   "ma20": 347.95,
   "ma60": 353.75,
   "ma240": 338.58,
   "ma480": 301.17,
   "matched": [
    "L4"
   ],
   "note": "06/15 역사적 신고가 후 -21.8% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -13.0%)"
  },
  {
   "code": "NTAP",
   "name": "NetApp",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 228.45,
   "changePct": 3.05,
   "value": null,
   "close": 235.42,
   "ma10": 215.1,
   "ma20": 204.28,
   "ma60": 190.8,
   "ma240": 135.35,
   "ma480": 121.0,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "NEM",
   "name": "Newmont",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 116.39,
   "changePct": -2.19,
   "value": null,
   "close": 113.84,
   "ma10": 116.75,
   "ma20": 120.56,
   "ma60": 114.62,
   "ma240": 107.4,
   "ma480": 81.16,
   "matched": [
    "L2"
   ],
   "note": "급등 +48.0% 후 고점 대비 -15.6% 조정, 60일선 대비 -0.7%"
  },
  {
   "code": "NDSN",
   "name": "Nordson Corporation",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 334.22,
   "changePct": -1.92,
   "value": null,
   "close": 327.8,
   "ma10": 329.67,
   "ma20": 321.2,
   "ma60": 312.66,
   "ma240": 277.81,
   "ma480": 245.31,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "PTC",
   "name": "PTC Inc.",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 193.0,
   "changePct": 0.38,
   "value": null,
   "close": 193.73,
   "ma10": 156.26,
   "ma20": 145.43,
   "ma60": 142.33,
   "ma240": 151.31,
   "ma480": 167.27,
   "matched": [
    "L3"
   ],
   "note": "240일선 돌파(2일 전, 거래량 16.9배) · 480일선 돌파(2일 전, 거래량 16.9배)"
  },
  {
   "code": "RVTY",
   "name": "Revvity",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 153.3,
   "changePct": 1.76,
   "value": null,
   "close": 155.99,
   "ma10": 152.57,
   "ma20": 145.23,
   "ma60": 127.19,
   "ma240": 105.37,
   "ma480": 103.39,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "SNOW",
   "name": "Snowflake Inc",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "서학개미 순매수 39위",
   "prevClose": 335.95,
   "changePct": 0.31,
   "value": null,
   "close": 336.99,
   "ma10": 336.29,
   "ma20": 334.48,
   "ma60": 318.11,
   "ma240": 232.99,
   "ma480": 210.2,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "TSM",
   "name": "TSMC",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "반도체·AI 인프라"
   ],
   "krRank": "서학개미 보관 23위",
   "prevClose": 482.3,
   "changePct": -1.93,
   "value": null,
   "close": 472.98,
   "ma10": 464.08,
   "ma20": 447.78,
   "ma60": 425.47,
   "ma240": 371.78,
   "ma480": 290.24,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "VLO",
   "name": "Valero Energy",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "",
   "prevClose": 419.22,
   "changePct": 0.71,
   "value": null,
   "close": 422.21,
   "ma10": 401.05,
   "ma20": 397.08,
   "ma60": 352.46,
   "ma240": 247.43,
   "ma480": 189.9,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "NBIS",
   "name": "네비우스",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "네오클라우드"
   ],
   "krRank": "서학개미 보관 47위",
   "prevClose": 249.87,
   "changePct": -6.2,
   "value": null,
   "close": 234.38,
   "ma10": 237.78,
   "ma20": 229.82,
   "ma60": 217.45,
   "ma240": 158.43,
   "ma480": 103.09,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "HOOD",
   "name": "로빈후드",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "증권"
   ],
   "krRank": "서학개미 순매수 44위",
   "prevClose": 112.0,
   "changePct": -2.73,
   "value": null,
   "close": 108.94,
   "ma10": 114.43,
   "ma20": 114.97,
   "ma60": 105.63,
   "ma240": 99.97,
   "ma480": 85.67,
   "matched": [
    "L2"
   ],
   "note": "급등 +46.9% 후 고점 대비 -12.7% 조정, 60일선 대비 +3.1%"
  },
  {
   "code": "ROK",
   "name": "로크웰오토메이션",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "로봇"
   ],
   "krRank": "",
   "prevClose": 450.74,
   "changePct": -2.28,
   "value": null,
   "close": 440.46,
   "ma10": 440.83,
   "ma20": 430.98,
   "ma60": 440.65,
   "ma240": 415.39,
   "ma480": 356.87,
   "matched": [
    "L4"
   ],
   "note": "06/30 역사적 신고가 후 -17.9% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -11.2%)"
  },
  {
   "code": "MRVL",
   "name": "마벨",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "서학개미 보관 31위",
   "prevClose": 287.01,
   "changePct": -1.93,
   "value": null,
   "close": 281.47,
   "ma10": 268.04,
   "ma20": 253.97,
   "ma60": 226.38,
   "ma240": 156.17,
   "ma480": 118.96,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "MU",
   "name": "마이크론",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "반도체·AI 인프라",
    "메모리·스토리지"
   ],
   "krRank": "서학개미 보관 9위",
   "prevClose": 1045.56,
   "changePct": 3.29,
   "value": null,
   "close": 1079.99,
   "ma10": 1070.88,
   "ma20": 1032.25,
   "ma60": 956.4,
   "ma240": 617.13,
   "ma480": 363.84,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "BE",
   "name": "블룸에너지",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "서학개미 보관 42위",
   "prevClose": 295.78,
   "changePct": -2.77,
   "value": null,
   "close": 287.6,
   "ma10": 282.32,
   "ma20": 275.74,
   "ma60": 236.63,
   "ma240": 193.92,
   "ma480": 113.71,
   "matched": [
    "L4"
   ],
   "note": "06/25 역사적 신고가 후 -55.2% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -18.1%)"
  },
  {
   "code": "CRCL",
   "name": "서클",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "서학개미 보관 38위",
   "prevClose": 84.13,
   "changePct": -3.95,
   "value": null,
   "close": 80.81,
   "ma10": 84.61,
   "ma20": 87.44,
   "ma60": 79.5,
   "ma240": 87.36,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +63.1% 후 고점 대비 -21.7% 조정, 60일선 대비 +1.6%"
  },
  {
   "code": "STX",
   "name": "씨게이트",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "메모리·스토리지"
   ],
   "krRank": "서학개미 순매수 15위",
   "prevClose": 805.63,
   "changePct": -0.65,
   "value": null,
   "close": 800.36,
   "ma10": 886.77,
   "ma20": 864.85,
   "ma60": 851.2,
   "ma240": 592.61,
   "ma480": 358.58,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.4% 후 고점 대비 -26.7% 조정, 60일선 대비 -6.0%"
  },
  {
   "code": "ANET",
   "name": "아리스타네트웍스",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "AI 서버·네트워크"
   ],
   "krRank": "",
   "prevClose": 215.36,
   "changePct": -0.37,
   "value": null,
   "close": 214.57,
   "ma10": 207.23,
   "ma20": 202.6,
   "ma60": 191.87,
   "ma240": 156.01,
   "ma480": 132.26,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선 지지 확인"
  },
  {
   "code": "IREN",
   "name": "아이렌",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "네오클라우드"
   ],
   "krRank": "서학개미 보관 32위",
   "prevClose": 41.28,
   "changePct": -6.6,
   "value": null,
   "close": 38.56,
   "ma10": 41.7,
   "ma20": 43.24,
   "ma60": 41.0,
   "ma240": 46.54,
   "ma480": 31.67,
   "matched": [
    "L2"
   ],
   "note": "급등 +53.2% 후 고점 대비 -20.6% 조정, 60일선 대비 -6.0%"
  },
  {
   "code": "XOM",
   "name": "엑슨모빌",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "정유·에너지"
   ],
   "krRank": "",
   "prevClose": 164.48,
   "changePct": -0.4,
   "value": null,
   "close": 163.83,
   "ma10": 162.95,
   "ma20": 163.17,
   "ma60": 159.09,
   "ma240": 142.66,
   "ma480": 124.26,
   "matched": [
    "L4"
   ],
   "note": "03/30 역사적 신고가 후 -23.0% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -5.9%)"
  },
  {
   "code": "NVDA",
   "name": "엔비디아",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "반도체·AI 인프라"
   ],
   "krRank": "서학개미 보관 2위",
   "prevClose": 239.24,
   "changePct": -0.92,
   "value": null,
   "close": 237.03,
   "ma10": 231.41,
   "ma20": 225.56,
   "ma60": 217.89,
   "ma240": 198.8,
   "ma480": 171.8,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "CRWV",
   "name": "코어위브",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "네오클라우드"
   ],
   "krRank": "",
   "prevClose": 91.72,
   "changePct": -4.06,
   "value": null,
   "close": 88.0,
   "ma10": 88.11,
   "ma20": 86.34,
   "ma60": 85.69,
   "ma240": 92.6,
   "ma480": null,
   "matched": [
    "L2"
   ],
   "note": "급등 +77.1% 후 고점 대비 -18.3% 조정, 60일선 대비 +2.7%"
  },
  {
   "code": "PWR",
   "name": "콴타서비스",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "전력 인프라"
   ],
   "krRank": "",
   "prevClose": 719.56,
   "changePct": -4.01,
   "value": null,
   "close": 690.7,
   "ma10": 666.36,
   "ma20": 647.99,
   "ma60": 645.28,
   "ma240": 582.12,
   "ma480": 460.74,
   "matched": [
    "L4"
   ],
   "note": "05/06 역사적 신고가 후 -29.7% 조정, 240일선 지지 → 20일선 위에서 반등 중 (전고점까지 -12.4%)"
  },
  {
   "code": "QCOM",
   "name": "퀄컴",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "스마트폰·애플"
   ],
   "krRank": "",
   "prevClose": 181.03,
   "changePct": -2.41,
   "value": null,
   "close": 176.66,
   "ma10": 185.73,
   "ma20": 186.25,
   "ma60": 171.5,
   "ma240": 168.31,
   "ma480": 160.44,
   "matched": [
    "L2"
   ],
   "note": "급등 +43.0% 후 고점 대비 -28.7% 조정, 60일선 대비 +3.0%"
  },
  {
   "code": "CLF",
   "name": "클리블랜드클리프스",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "철강"
   ],
   "krRank": "",
   "prevClose": 12.25,
   "changePct": -2.69,
   "value": null,
   "close": 11.92,
   "ma10": 11.71,
   "ma20": 11.96,
   "ma60": 11.65,
   "ma240": 11.49,
   "ma480": 10.72,
   "matched": [
    "L2"
   ],
   "note": "급등 +45.3% 후 고점 대비 -19.2% 조정, 60일선 대비 +2.3%"
  },
  {
   "code": "PANW",
   "name": "팔로알토네트웍스",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [],
   "krRank": "서학개미 순매수 19위",
   "prevClose": 419.91,
   "changePct": -3.14,
   "value": null,
   "close": 406.73,
   "ma10": 397.54,
   "ma20": 382.37,
   "ma60": 362.41,
   "ma240": 244.96,
   "ma480": 217.53,
   "matched": [
    "L1"
   ],
   "note": "정배열 상승 중, 최근 20일선·60일선 지지 확인"
  },
  {
   "code": "FCX",
   "name": "프리포트맥모란",
   "market": "",
   "sector": "",
   "marcap": 0,
   "themes": [
    "구리·전선"
   ],
   "krRank": "",
   "prevClose": 72.56,
   "changePct": -1.58,
   "value": null,
   "close": 71.41,
   "ma10": 71.5,
   "ma20": 71.34,
   "ma60": 69.52,
   "ma240": 60.23,
   "ma480": 50.01,
   "matched": [
    "L2"
   ],
   "note": "급등 +33.2% 후 고점 대비 -10.6% 조정, 60일선 대비 +2.7%"
  }
 ]
};
