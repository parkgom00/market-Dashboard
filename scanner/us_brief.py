"""미국장 AI 브리핑: 이슈 요약 · 섹터 흐름 · 국장 영향 · 미국 특징주↔국내 연관주 연결 · 오늘 체크리스트.

숫자(지수·업종 등락률)는 실제 시세만 넣고, 원인과 연결은 제미나이가 구글 검색으로 찾은 근거로 씁니다.
검색을 못 쓰는 경우에는 수치 기반 해석만 하고 화면에 '원인 미확인'임을 표시합니다.
미국 종목 등락률은 모델이 쓴 값을 버리고 실제 시세로 다시 채웁니다 (fill_changes).
"""
import json

SYSTEM = ("너는 한국 개인투자자를 위한 미국장 마감 브리핑 작성자다. 사실과 해석을 구분하고, 확인되지 않은 원인·수치·종목 관계를 지어내지 않는다. "
          "매수·매도를 권유하지 않고 '점검 포인트' 형태로 쓴다. 한국 종목은 실제 코스피/코스닥 상장사만 쓴다.")

SCHEMA_TEXT = """다음 JSON 하나로만 답해라 (설명·코드블록 금지):
{
 "us_market": "간밤 미국 증시 요약 3~4문장 (지수 움직임과 그 원인)",
 "sector_flow": "강했던/약했던 업종과 이유 2~3문장",
 "korea_impact": "금리·환율·유가·반도체 등을 근거로 오늘 국내 증시에 미칠 영향 2~4문장",
 "news": [{"title": "", "fact": "핵심 사실 2문장", "korea_impact": "국내 파급"}],
 "connections": [{"sector": "업종/테마", "direction": "up|down", "us_name": "미국 종목명", "us_ticker": "티커",
   "cause": "주가가 움직인 구체적 원인", "logic": "미국 기업 이벤트 -> 산업 영향 -> 국내 기업 연결 고리",
   "korea_picks": [{"name": "한국 종목명", "strength": 3, "reason": "연결 이유 한 줄"}]}],
 "caution": [{"theme": "", "us": "근거가 된 미국 종목/지표", "cause": "", "action": "오늘 점검할 포인트"}],
 "watch": [{"theme": "", "us": "", "cause": "", "action": ""}]
}
strength: 3=직접 수혜/피해, 2=간접, 1=동조 가능성. connections 는 4~8개, news 는 3~6개, caution 은 1~3개, watch 는 2~4개."""


def build_prompt(for_date, indices, sectors, kr_hints):
    lines = [f"기준: 미국 정규장 {for_date} 마감. 아래 시세는 실제 값이다.", "", "[지수·금리·원자재]"]
    for i in indices:
        lines.append(f"- {i['name']}: {i['changeText']}")
    lines += ["", "[업종 ETF 등락률 (강한 순)]"]
    for s in sorted(sectors, key=lambda s: -s["changePct"]):
        lines.append(f"- {s['name']}({s['symbol']}): {s['changePct']:+.2f}%")
    if kr_hints:
        lines += ["", "[참고: 사용자가 정리한 미국-국내 연결 후보 (맞을 때만 활용)]"]
        lines += [f"- {h}" for h in kr_hints]
    lines += ["", "구글 검색으로 이 날짜 미국 증시 마감 시황, 지수 움직임의 원인, 실적·뉴스로 크게 움직인 개별 종목을 확인해서 작성해라.", SCHEMA_TEXT]
    return "\n".join(lines)


def _s(v):
    return str(v).strip() if v is not None else ""


def _items(v, keys):
    out = []
    for x in v if isinstance(v, list) else []:
        if isinstance(x, dict):
            row = {k: _s(x.get(k)) for k in keys}
            if row[keys[0]]:
                out.append(row)
    return out


def clean_brief(obj):
    """모델 응답을 화면용 구조로 정리. 필수(us_market)가 없으면 None."""
    if not isinstance(obj, dict) or not _s(obj.get("us_market")):
        return None
    conns = []
    for c in obj.get("connections") if isinstance(obj.get("connections"), list) else []:
        if not isinstance(c, dict) or not _s(c.get("us_ticker")) or not _s(c.get("us_name")):
            continue
        picks = []
        for p in c.get("korea_picks") if isinstance(c.get("korea_picks"), list) else []:
            if isinstance(p, dict) and _s(p.get("name")):
                try:
                    st = max(1, min(3, int(p.get("strength", 1))))
                except (TypeError, ValueError):
                    st = 1
                picks.append({"name": _s(p["name"]), "strength": st, "reason": _s(p.get("reason"))})
        conns.append({"sector": _s(c.get("sector")), "direction": "down" if _s(c.get("direction")) == "down" else "up",
                      "usName": _s(c["us_name"]), "usTicker": _s(c["us_ticker"]).upper(), "usChange": None,
                      "cause": _s(c.get("cause")), "logic": _s(c.get("logic")), "koreaPicks": picks})
    return {
        "usMarket": _s(obj["us_market"]), "sectorFlow": _s(obj.get("sector_flow")), "koreaImpact": _s(obj.get("korea_impact")),
        "news": _items(obj.get("news"), ["title", "fact", "korea_impact"]),
        "connections": conns,
        "caution": _items(obj.get("caution"), ["theme", "us", "cause", "action"]),
        "watch": _items(obj.get("watch"), ["theme", "us", "cause", "action"]),
    }


def fill_changes(brief, pct_by_ticker):
    """연결 항목의 미국 종목 등락률을 실제 시세로 채움 (모르면 None → 화면에서 뱃지 없이 표시)."""
    for c in brief["connections"]:
        v = pct_by_ticker.get(c["usTicker"])
        c["usChange"] = None if v is None else round(float(v), 2)
    return brief


def generate_brief(for_date, indices, sectors, kr_hints, gen):
    """gen(prompt, system, search, want_json) → 객체/문자열. 검색 실패 시 검색 없이 한 번 더."""
    prompt = build_prompt(for_date, indices, sectors, kr_hints)
    grounded = True
    try:
        obj = gen(prompt, SYSTEM, True)
    except Exception as e:
        if e.__class__.__name__ == "GeminiBusy":
            raise
        grounded = False
        obj = gen(prompt + "\n(검색을 쓸 수 없다. 위 시세만 근거로 해석하고, 원인을 확인할 수 없는 부분은 '원인 미확인'이라고 써라.)", SYSTEM, False)
    brief = clean_brief(obj)
    if brief is None:
        raise ValueError("브리핑 응답 형식이 올바르지 않음")
    brief["grounded"] = grounded
    return brief
