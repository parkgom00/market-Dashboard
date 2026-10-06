import json, os, re, urllib.parse, urllib.request
import collect_youtube as cy
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
res = {}
for h in ["@hkwowtv", "@hkglobalmarket", "@wowtv", "@한국경제TV"]:
    r = {}
    try:
        html = cy._get("https://www.youtube.com/" + urllib.parse.quote(h))
        cid = cy.find_channel_id(html)
        m = re.search(r'<title>(.*?)</title>', html)
        r["channelId"], r["title"] = cid, m.group(1) if m else ""
        if cid:
            r["rss"] = [(v.get("title"), v.get("published"), v.get("id") or v.get("videoId")) for v in cy.parse_feed(cy._get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"), limit=15)]
        for q in ["당잠사", "담장사"]:
            s = cy._get("https://www.youtube.com/" + urllib.parse.quote(h) + "/search?query=" + urllib.parse.quote(q))
            hits = re.findall(r'"videoRenderer":\{"videoId":"([\w-]{11})".{0,1500}?"title":\{"runs":\[\{"text":"(.*?)"\}.{0,2500}?"publishedTimeText":\{"simpleText":"(.*?)"', s)
            r["search_" + q] = hits[:12]
            r["len_" + q] = len(s)
    except Exception as e:
        r["err"] = f"{type(e).__name__}: {e}"
    res[h] = r
json.dump(res, open(os.path.join(OUT, "yt_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
