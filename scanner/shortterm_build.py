"""단기 탭 화면 파일(data/shortterm.js)을 만듭니다.
  유형 A 종가배팅주  ← out/closing_kr.json  (collect_closing.py, 장 마감 직전·마감 후)
  유형 B 전고점 돌파 ← out/breakout_kr.json (run_scan.py, 장 마감 후 일봉 기준)
  유형 C 480분선 지지 ← out/m480_kr.json    (collect_m480.py, 10:00~12:00 30분 간격, 1분봉 기준)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_JS = os.path.join(HERE, "..", "data", "shortterm.js")


def _load(name):
    try:
        with open(os.path.join(OUT, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def merge(closing, breakout, m480=None):
    payload = dict(closing or {"asOf": "", "window": "15:20~15:40", "status": "아직 실행 전입니다.", "types": []})
    types = [t for t in payload.get("types", []) if t.get("id") != "B"]
    if breakout:
        types.append({"id": "B", "name": "전고점 돌파", "timeframe": "일봉",
                      "desc": "52주 신고가(또는 3년 내 최고가)를 찍고 하락했던 전고점을 다시 넘어서는 종목. 장 마감 후 종가 기준으로 하루 한 번 갱신됩니다.",
                      "asOf": breakout.get("asOf", ""), "subtypes": breakout.get("subtypes", [])})
    types = [t for t in types if t.get("id") != "C"]
    if m480:
        types.append({"id": "C", "name": "480분선 지지", "timeframe": "1분봉",
                      "desc": ("오늘 장중 +15% 이상 올랐던 종목이 1분봉 480분선 근처까지 내려왔지만 이탈하지 않고 옆으로 기는(횡보) 상태. "
                               "10:00~12:00 사이 30분마다 그 시점의 모습을 한 번씩 찍어 보여주며 실시간은 아닙니다."),
                      "asOf": m480.get("asOf", ""), "window": "10:00~12:00 · 30분 간격", "status": m480.get("status", ""),
                      "kr": m480.get("kr", [])})
    payload["types"] = types
    return payload


def build(target=None):
    target = target or DATA_JS
    payload = merge(_load("closing_kr.json"), _load("breakout_kr.json"), _load("m480_kr.json"))
    with open(target, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/shortterm_build.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.shortterm = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    return payload
