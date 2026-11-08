"""Put the eight books into one list of units, in reading order, for finding and reading animals.

A unit is a couplet (verse) or a sentence (prose), with where it sits: the book, the chapter,
the section heading and its Ganjoor address. Kalila wa Dimna is prose with verse set into it;
the Conference of the Birds and the Shahnameh are verse.

  python3 -I tools/corpus.py data/units.jsonl
"""
import json, re, sys

BOOKS = [  # key, file, title
    ("kalila", "../animals-persian-lit/data/kalila-ganjoor.json", "کلیله و دمنه"),
    ("attar", "../attar-conference-of-birds/data/manteq-ganjoor.json", "منطق‌الطیر"),
    ("shahnameh", "../ferdowsi-shahnameh/data/shahnameh-ganjoor.json", "شاهنامه"),
    ("masnavi", "../animals-persian-lit/data/masnavi-ganjoor.json", "مثنوی معنوی"),     # books added later go last, so earlier units keep their numbers
    ("marzban", "../animals-persian-lit/data/marzban-ganjoor.json", "مرزبان‌نامه"),
    ("parvin", "../animals-persian-lit/data/parvin-ganjoor.json", "دیوان پروین اعتصامی"),
    ("golestan", "data/golestan-ganjoor.json", "گلستان"),       # Saadi's two garden books, added for the plants
    ("bustan", "data/bustan-ganjoor.json", "بوستان"),
]

def clean(t):
    t = t.replace("ي", "ی").replace("ك", "ک").replace("‏", "").replace("‎", "")
    return re.sub(r"\s+", " ", t).strip()

# a sentence ends at . ! ? ؟ followed by a space; Ganjoor's prose has few other marks
SENTENCE = re.compile(r"(?<=[.!?؟])\s+")

def ganjoor_chapters(path):
    """(chapter title, [poems]) from a Ganjoor dump made by tools/fetch.py, or the Attar one"""
    d = json.load(open(path))
    if isinstance(d, list):   # Attar: sections with poems whose verses carry an order
        for s in d:
            yield s["section"], [{"title": p["title"], "url": p["url"], "verses": sorted(p["verses"], key=lambda v: v["o"])} for p in s["poems"]]
        return
    def poems(n):
        out = list(n["poems"])
        for ch in n["children"]: out += poems(ch)
        return out
    for b in d["books"]:
        yield b["title"], [{"title": p["title"], "url": p["url"], "verses": p["verses"]} for p in poems(b)]

if __name__ == "__main__":
    n = 0
    with open(sys.argv[1], "w") as f:
        for key, path, book_title in BOOKS:
            for ci, (chapter, poems) in enumerate(ganjoor_chapters(path)):
                for pi, p in enumerate(poems):
                    vs = p["verses"]
                    i = 0
                    while i < len(vs):
                        v = vs[i]
                        if v["p"] == -1:   # a prose paragraph: one unit per sentence
                            para = clean(v["t"])
                            for si, s in enumerate(x for x in SENTENCE.split(para) if x):
                                f.write(json.dumps({"id": n, "book": key, "ch": ci, "chapter": clean(chapter), "sec": pi,
                                                    "title": clean(p["title"]), "url": p["url"], "kind": "prose",
                                                    "para": i, "s": si, "text": s}, ensure_ascii=False) + "\n"); n += 1
                            i += 1
                        else:              # a couplet: the two half-lines together
                            a = clean(v["t"]); b = clean(vs[i + 1]["t"]) if i + 1 < len(vs) and vs[i + 1]["p"] == 1 else ""
                            f.write(json.dumps({"id": n, "book": key, "ch": ci, "chapter": clean(chapter), "sec": pi,
                                                "title": clean(p["title"]), "url": p["url"], "kind": "verse",
                                                "para": i, "s": 0, "text": a, "text2": b}, ensure_ascii=False) + "\n"); n += 1
                            i += 2 if b else 1
    print(n, "units")
