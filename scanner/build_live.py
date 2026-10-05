"""scanner/out/ 의 조각 파일들을 합쳐 data/live.js 를 만듭니다.

조각 파일 (있는 것만 사용, 없으면 그 항목은 화면에서 숨겨짐):
  live_news.json        {"asOf", "items"}            국내 [특징주] 뉴스      ← fetch_news.py
  live_kr_rank.json     {"asOf", "gainers", "value"} 국내 등락률·거래대금 상위 ← collect_kr.py
  live_themes_kr.json   {"asOf", "themes"}           국내 테마 강약          ← collect_kr.py
  live_themes_us.json   {"asOf", "themes"}           미국 테마 강약          ← collect_us.py
화면의 '데이터 기준' 시각은 조각들 중 가장 최근 시각입니다.
"""
import json
import os
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DEFAULT_TARGET = os.path.join(HERE, "..", "data", "live.js")
KST = timezone(timedelta(hours=9))


def _load(name, out_dir):
    path = os.path.join(out_dir, name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def build(out_dir=OUT, target=DEFAULT_TARGET):
    news = _load("live_news.json", out_dir)
    rank = _load("live_kr_rank.json", out_dir)
    th_kr = _load("live_themes_kr.json", out_dir)
    th_us = _load("live_themes_us.json", out_dir)

    kr, us = {}, {}
    if news is not None:
        kr["news"] = news["items"]
    if rank is not None:
        kr["gainers"] = rank.get("gainers", [])
        kr["value"] = rank.get("value", [])
    if th_kr is not None:
        kr["themes"] = th_kr["themes"]
    if th_us is not None:
        us["themes"] = th_us["themes"]

    stamps = [p["asOf"] for p in (news, rank, th_kr, th_us) if p and p.get("asOf")]
    as_of = max(stamps) if stamps else datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    payload = {"asOf": as_of, "kr": kr, "us": us}
    with open(target, "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 (scanner/build_live.py). 직접 고치지 마세요.\n")
        f.write("window.DASH = window.DASH || {};\nwindow.DASH.live = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    return payload


if __name__ == "__main__":
    build()
    print("data/live.js 갱신 완료")
