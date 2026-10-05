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
print(f"\n{sum(ok)}/{len(ok)} 통과"); raise SystemExit(0 if all(ok) else 1)
