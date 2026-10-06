import json, os, re
import collect_youtube as cy
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
res = {}
for name, cid in [("sosu", "UCC3yfxS5qC6PCwDzetUuEWg"), ("orlando", "UCwSSqi-s0wcH6pJbH3YPZqQ")]:
    for tab in ("videos", "streams"):
        try:
            s = cy._get(f"https://www.youtube.com/channel/{cid}/{tab}")
            items = []
            for chunk in s.split('"lockupViewModel":{')[1:8]:
                mid = re.search(r'"contentId":"([\w-]{11})"', chunk)
                mt = re.search(r'"lockupMetadataViewModel":\{"title":\{"content":"((?:[^"\\]|\\.)*)"', chunk)
                pos_t = mt.start() if mt else -1
                meta = re.findall(r'"content":"((?:[^"\\]|\\.)*)"', chunk[pos_t:pos_t + 3000]) if mt else []
                items.append({"id": mid.group(1) if mid else None, "id_pos": mid.start() if mid else -1, "title_pos": pos_t,
                              "title": cy._unesc(mt.group(1))[:50] if mt else None, "meta": [cy._unesc(x)[:40] for x in meta[:8]], "chunk_len": len(chunk)})
            res[f"{name}_{tab}"] = {"len": len(s), "n_lockup": s.count('"lockupViewModel":{'), "n_videoRenderer": s.count('"videoRenderer":{'), "items": items}
        except Exception as e:
            res[f"{name}_{tab}"] = f"ERR {type(e).__name__}: {e}"
json.dump(res, open(os.path.join(OUT, "yt_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
