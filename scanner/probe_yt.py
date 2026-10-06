import json, os, re, urllib.parse, urllib.request
import collect_youtube as cy
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
res = {}
def tryit(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        res[name] = f"ERR {type(e).__name__}: {e}"
feed = lambda cid: [(v["title"][:40], v["publishedAt"]) for v in cy.parse_feed(cy._get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid), limit=3)]
for n, cid in [("815", "UCCG6BEYjfQMGzypJw2EJCDQ"), ("dante", "UCKTMvIu9a4VGSrpWy-8bUrQ"), ("sosu", "UCC3yfxS5qC6PCwDzetUuEWg"), ("hk", "UCF8AeLlUbEpKju6v1H6p8Eg")]:
    tryit("rss_" + n, lambda: feed(cid))
def vt():
    s = cy._get("https://www.youtube.com/channel/UCKTMvIu9a4VGSrpWy-8bUrQ/videos")
    i = s.find('"videoId"'); j = s.find('"contentId"'); k = s.find("lockupViewModel")
    return {"len": len(s), "videoId_at": i, "contentId_at": j, "lockup_at": k,
            "snip_videoId": s[max(0, i - 300): i + 1500] if i > 0 else "", "snip_lockup": s[max(0, k - 100): k + 2500] if k > 0 else ""}
tryit("videos_tab", vt)
def watch():
    s = cy._get("https://www.youtube.com/watch?v=8s4kFJ6eXs4")
    return {"len": len(s), "lengthSeconds": re.findall(r'"lengthSeconds":"(\d+)"', s)[:2], "isLive": re.findall(r'"isLiveContent":(\w+)', s)[:1],
            "isLiveNow": re.findall(r'"isLiveNow":(\w+)', s)[:1], "start": re.findall(r'"startTimestamp":"([^"]+)"', s)[:1], "end": re.findall(r'"endTimestamp":"([^"]+)"', s)[:1],
            "captions": "captionTracks" in s, "title": re.findall(r'<title>(.*?)</title>', s)[:1]}
tryit("watch", watch)
json.dump(res, open(os.path.join(OUT, "yt_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
