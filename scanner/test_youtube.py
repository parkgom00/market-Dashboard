"""유튜브 수집 로직을 가짜 응답으로 검증합니다. 실행: python test_youtube.py"""
import os
import tempfile
import collect_youtube as cy

ok = []
def check(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

FEED = """<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
<entry><yt:videoId>AAA</yt:videoId><title>첫 영상</title><published>2026-10-05T12:30:00+00:00</published></entry>
<entry><yt:videoId>BBB</yt:videoId><title>둘째</title><published>2026-10-04T01:00:00+00:00</published></entry></feed>"""
v = cy.parse_feed(FEED)
check("RSS 파싱: 제목·링크·한국시간", v[0] == {"title": "첫 영상", "publishedAt": "2026-10-05 21:30", "url": "https://www.youtube.com/watch?v=AAA"})
check("채널 ID 추출", cy.find_channel_id('x"externalId":"UC' + "a" * 22 + '"y') == "UC" + "a" * 22)

chs = [{"name": "A", "handle": "@a"}, {"name": "B", "handle": "@b"}]
def fake(url):
    if "feeds" in url:
        if "UC" + "b" * 22 in url:
            raise OSError("boom")
        return FEED
    return '"externalId":"UC' + ("a" if "%40a" in url or "@a" in url else "b") * 22 + '"'
prev = {"B": {"name": "B", "channelId": "UC" + "b" * 22, "videos": [{"title": "old"}]}}
res, errs = cy.build(chs, prev, fake)
check("성공 채널은 갱신", len(res[0]["videos"]) == 2 and res[0]["channelId"] == "UC" + "a" * 22)
check("실패 채널은 이전 목록 유지 + 오류 기록", res[1]["videos"] == [{"title": "old"}] and len(errs) == 1)
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "y.js"); cy.write(res, p)
    check("저장 후 다시 읽기", cy.load_previous(p)["A"]["videos"][0]["title"] == "첫 영상")

raw = {"skip": False, "key_summary": "요약", "market": ["a", ""], "sectors": [{"name": "반도체", "point": "p", "stocks": [{"name": "SK하이닉스", "note": "n"}, {"name": ""}]}, "이상한값"], "checkpoints": "문자열"}
c = cy.clean_summary(raw)
check("요약 정리: 빈 항목·이상한 타입 제거", c["market"] == ["a"] and len(c["sectors"]) == 1 and len(c["sectors"][0]["stocks"]) == 1 and c["checkpoints"] == [])
check("skip/빈 응답은 None", cy.clean_summary({"skip": True}) is None and cy.clean_summary("x") is None)
vids = [{"title": "t", "publishedAt": "2026-10-05 10:00", "url": "u1"}]
cy.carry_summaries(vids, [{"url": "u1", "ai": {"keySummary": "k"}}])
check("이전 요약 이어붙임", vids[0]["ai"]["keySummary"] == "k")
class GeminiBusy(Exception): pass
chs2 = [{"name": "A", "videos": [{"url": "a1", "publishedAt": "2026-10-05 10:00"}, {"url": "a2", "publishedAt": "2026-10-04 10:00"}]}]
calls = []
def fake_sum(url):
    calls.append(url)
    if url == "a2": raise GeminiBusy("busy")
    return {"key_summary": "ok"}
n, notes = cy.summarize_new(chs2, fake_sum)
check("채널별 최신 영상 1개만 요약 (두 번째 영상은 호출조차 안 함)", n == 1 and calls == ["a1"] and "ai" in chs2[0]["videos"][0] and "ai" not in chs2[0]["videos"][1])
calls.clear()
chs4 = [{"name": "A", "videos": [{"url": "a2", "publishedAt": "2026-10-05"}]}]
n4, notes4 = cy.summarize_new(chs4, fake_sum)
check("혼잡이면 중단하고 다음에 재시도 (실패 횟수 올리지 않음)", n4 == 0 and "aiFail" not in chs4[0]["videos"][0] and "ai" not in chs4[0]["videos"][0])
def bad(url): raise ValueError("파싱")
chs3 = [{"name": "A", "videos": [{"url": "a1", "publishedAt": "2026-10-05"}]}]
cy.summarize_new(chs3, bad); cy.summarize_new(chs3, bad); n3, _ = cy.summarize_new(chs3, bad)
check("두 번 실패한 영상은 더 시도하지 않음", chs3[0]["videos"][0]["aiFail"] == 2 and n3 == 0)
print(f"\n{sum(ok)}/{len(ok)} 통과"); raise SystemExit(0 if all(ok) else 1)
