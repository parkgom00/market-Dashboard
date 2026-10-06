import json, os, re, urllib.parse, urllib.request
import collect_youtube as cy
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
res = {}
cid = "UCF8AeLlUbEpKju6v1H6p8Eg"
def tryit(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        res[name] = f"ERR {type(e).__name__}: {e}"
feed = lambda q: [(v["title"], v["publishedAt"], v["url"][-11:]) for v in cy.parse_feed(cy._get("https://www.youtube.com/feeds/videos.xml?" + q), limit=15)]
tryit("rss_channel", lambda: feed("channel_id=" + cid))
tryit("rss_uploads", lambda: feed("playlist_id=UU" + cid[2:]))
tryit("rss_uulf", lambda: feed("playlist_id=UULF" + cid[2:]))
def search(q):
    s = cy._get("https://www.youtube.com/@hkwowtv/search?query=" + urllib.parse.quote(q))
    hits = re.findall(r'"videoRenderer":\{"videoId":"([\w-]{11})".{0,1500}?"title":\{"runs":\[\{"text":"(.*?)"\}.{0,2500}?"publishedTimeText":\{"simpleText":"(.*?)"', s)
    return {"len": len(s), "hits": hits[:12], "consent": "consent.youtube" in s}
tryit("search_당잠사", lambda: search("당잠사"))
tryit("search_담장사", lambda: search("담장사"))
def videos_tab():
    s = cy._get("https://www.youtube.com/@hkwowtv/videos")
    hits = re.findall(r'"videoRenderer":\{"videoId":"([\w-]{11})".{0,1500}?"title":\{"runs":\[\{"text":"(.*?)"\}.{0,2500}?"publishedTimeText":\{"simpleText":"(.*?)"', s)
    return {"len": len(s), "hits": hits[:30]}
tryit("videos_tab", videos_tab)
def playlists():
    s = cy._get("https://www.youtube.com/@hkwowtv/playlists")
    return re.findall(r'"playlistId":"(PL[\w-]+)".{0,800}?"title":\{"(?:simpleText|runs)":(?:\[\{"text":)?"(.*?)"', s)[:40]
tryit("playlists", playlists)
for h in ["@sosumonkey"]:
    tryit("cid_" + h, lambda: cy.find_channel_id(cy._get("https://www.youtube.com/" + h)))
tryit("rss_dante", lambda: feed("channel_id=UCKTMvIu9a4VGSrpWy-8bUrQ")[:3])
json.dump(res, open(os.path.join(OUT, "yt_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
