"""Write site/atlas/data.json: every plant mention with its labels, for the atlas page.

  python3 -I tools/atlas.py
"""
import json, os

BOOKS = ["kalila", "attar", "shahnameh", "masnavi", "marzban", "parvin", "golestan", "bustan"]
FACULTIES = ["speech", "reasoning", "knowledge", "emotion", "deception", "perception", "desire", "memory", "moral", "devotion"]
units = {u["id"]: u for u in map(json.loads, open("data/units.jsonl"))}
mentions = {m["id"]: m for m in map(json.loads, open("data/mentions.jsonl"))}
labels = {a["id"]: a for a in map(json.loads, open("data/annotations.jsonl"))}
for k, v in json.load(open("data/corrections.json")).items():
    if not k.startswith("_"): labels[int(k)].update({f: x for f, x in v.items() if f != "why"})
merge = json.load(open("data/species-merge.json"))

passages, pix, rows = [], {}, []
for i, a in sorted(labels.items()):
    if not a["is_plant"]: continue
    m = mentions[i]; u = units[m["unit"]]
    if u["id"] not in pix:
        pix[u["id"]] = len(passages)
        t = u["text"] + (" / " + u["text2"] if u.get("text2") else "")
        passages.append([t if len(t) <= 260 else t[:257] + "…", u["url"], u["title"]])
    rows.append([BOOKS.index(m["book"]), merge.get(a["species"], a["species"]), m["class"], a["figure"], a["mode"],
                 sum(1 << FACULTIES.index(f) for f in a["faculties"] if f in FACULTIES), ("rational" if a["spectrum"] == "gratuitous" and a.get("rung") == "human" else a["spectrum"]),
                 1 if a["unsure"] else 0, pix[u["id"]], m["token"], a["evidence"]])
os.makedirs("site/atlas", exist_ok=True)
json.dump({"books": BOOKS, "faculties": FACULTIES, "rows": rows, "passages": passages},
          open("site/atlas/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(rows), "plant mentions,", len(passages), "passages", os.path.getsize("site/atlas/data.json") // 1024, "KB")
