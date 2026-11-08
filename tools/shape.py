"""Shape the three books for the page: every line set in Amiri with HarfBuzz, every animal word placed.

Verse is set as couplets, two half-lines to a row; Kalila's prose is broken into lines the width
of a couplet. Each animal mention carries its labels from data/annotations.jsonl; words the
labels say are not animals (milk, a grave, "again") are dropped. Writes site/data/<book>.json
and site/data/hand.woff2.

  .venv/bin/python -I tools/shape.py
"""
import json, os
from collections import defaultdict
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools import subset

FONT = "fonts/Amiri-Regular.ttf"
BOOKS = ["kalila", "attar", "shahnameh", "masnavi", "marzban", "parvin"]
GUTTER = 1.4                      # em between the halves of a couplet, as on the page
FACULTIES = ["speech", "reasoning", "knowledge", "emotion", "deception", "perception", "desire", "memory", "moral", "devotion"]
SPECTRUM = ["none", "anthropectomy", "species-typical", "constructive", "gratuitous"]
FIGURE = ["none", "creature", "character", "figure"]

face = hb.Face(hb.Blob.from_file_path(FONT)); font = hb.Font(face)
upem = TTFont(FONT)["head"].unitsPerEm

def shape(text):
    """the width of a line, and each word's left and right edge by advance, in font units"""
    b = hb.Buffer(); b.add_str(text); b.direction, b.script, b.language = "rtl", "Arab", "fa"
    hb.shape(font, b)
    spans, i = [], 0
    for w in text.split(" "):
        spans.append((i, i + len(w))); i += len(w) + 1
    ext = [[1e9, -1e9] for _ in spans]
    x = 0
    for info, pos in zip(b.glyph_infos, b.glyph_positions):
        k = next((j for j, (a, z) in enumerate(spans) if a <= info.cluster < z), None)
        if k is not None:
            ext[k][0] = min(ext[k][0], x); ext[k][1] = max(ext[k][1], x + pos.x_advance)
        x += pos.x_advance
    return x, ext

SPACE = shape("ا ا")[0] - 2 * shape("ا")[0]

def build(book, us, by_unit, labels):
    verse = [t for u in us if u["kind"] == "verse" for t in (u["text"], u.get("text2", "")) if t]
    ws = sorted(shape(t)[0] for t in verse)
    col_w = round(ws[int(len(ws) * .99)] / upem + .4, 2) if len(ws) > 100 else 12.5
    prose_w = (2 * col_w + GUTTER - .4) * upem          # a prose line fills the couplet's width

    lines, widths, blocks, sections, marks, table, passages = [], [], [], [], [], [], []
    pass_ix = {}

    def add_line(text):
        w, ext = shape(text)
        lines.append(text); widths.append(w)
        return len(lines) - 1, ext

    def keep(m, line, word, ext, verse_lines=None):
        a = labels.get(m["id"])
        if a is not None and not a["is_animal"]:
            return
        u = unit_of[m["unit"]]
        if u["id"] not in pass_ix:
            pass_ix[u["id"]] = len(passages)
            # a couplet points at its two lines; a prose sentence keeps its own text
            passages.append(verse_lines if verse_lines else u["text"])
        a = a or {}
        fac = sum(1 << FACULTIES.index(f) for f in a.get("faculties", []) if f in FACULTIES)
        table.append([a.get("species") or m["species"], FIGURE.index(a.get("figure", "none")), a.get("mode", "none"), fac,
                      SPECTRUM.index(a.get("spectrum", "none")), a.get("evidence", ""), pass_ix[u["id"]],
                      1 if a.get("unsure") else 0, 0 if a else 1])
        x0, x1 = ext[word]
        marks.extend([line, word, round(x0), round(x1), len(table) - 1])

    unit_of = {u["id"]: u for u in us}
    last = (None, None)
    i = 0
    while i < len(us):
        u = us[i]
        if (u["ch"], u["sec"]) != last:
            if u["ch"] != last[0]:
                sections.append({"title": u["chapter"], "poems": []}); blocks.append([2, len(sections) - 1])
            sections[-1]["poems"].append({"title": u["title"], "url": u["url"]})
            blocks.append([1, len(sections) - 1, len(sections[-1]["poems"]) - 1])
            last = (u["ch"], u["sec"])
        if u["kind"] == "verse":
            row, exts = [0], []
            for half, t in ((0, u["text"]), (1, u.get("text2", ""))):
                if not t: continue
                li, ext = add_line(t); row.append(li); exts.append(ext)
            for m in by_unit[u["id"]]:
                keep(m, row[1 + m["half"]], m["w"], exts[m["half"]], row[1:])
            blocks.append(row); i += 1
            continue
        # a prose paragraph: its run of sentences, word by word, broken greedily into lines
        run = [u]
        while i + len(run) < len(us):
            v = us[i + len(run)]
            if v["kind"] != "prose" or (v["ch"], v["sec"], v["para"]) != (u["ch"], u["sec"], u["para"]): break
            run.append(v)
        words, owner = [], []
        for s in run:
            for wi, w in enumerate(s["text"].split(" ")):
                words.append(w); owner.append((s["id"], wi))
        start, acc = 0, 0
        breaks = []
        for k, w in enumerate(words):
            ww = shape(w)[0]
            if k > start and acc + SPACE + ww > prose_w:
                breaks.append((start, k)); start, acc = k, ww
            else:
                acc += (SPACE if k > start else 0) + ww
        breaks.append((start, len(words)))
        where = {}
        for a, z in breaks:
            li, ext = add_line(" ".join(words[a:z]))
            blocks.append([3, li])
            for k in range(a, z): where[owner[k]] = (li, k - a, ext)
        for s in run:
            for m in by_unit[s["id"]]:
                li, k, ext = where[(s["id"], m["w"])]
                if m["span"] == 2 and (s["id"], m["w"] + 1) in where and where[(s["id"], m["w"] + 1)][0] == li:
                    ext = [list(e) for e in ext]; ext[k] = [min(ext[k][0], ext[k + 1][0]), max(ext[k][1], ext[k + 1][1])]
                keep(m, li, k, ext)
        i += len(run)

    page = {"colW": col_w, "rowH": 1.95, "base": 1.19, "gutter": GUTTER}
    return {"book": book, "upem": upem, "page": page, "lines": lines, "widths": widths, "blocks": blocks,
            "sections": sections, "marks": marks, "table": table, "passages": passages,
            "labelled": sum(1 for r in table if not r[8]), "mentions": len(table)}

if __name__ == "__main__":
    units = [json.loads(l) for l in open("data/units.jsonl")]
    mentions = [json.loads(l) for l in open("data/mentions.jsonl")]
    labels = {}
    if os.path.exists("data/annotations.jsonl"):
        for l in open("data/annotations.jsonl"):
            a = json.loads(l); labels[a["id"]] = a
    # hand corrections over the labels, and one name for each species (tortoise and turtle, ox and cattle)
    for k, v in json.load(open("data/corrections.json")).items():
        if not k.startswith("_") and int(k) in labels:
            labels[int(k)].update({f: x for f, x in v.items() if f != "why"}); labels[int(k)]["model"] = "hand"
    merge = json.load(open("data/species-merge.json"))
    for a in labels.values():
        a["species"] = merge.get(a.get("species", ""), a.get("species", ""))
    by_unit = defaultdict(list)
    for m in mentions: by_unit[m["unit"]].append(m)
    os.makedirs("site/data", exist_ok=True)
    text = set()
    for book in BOOKS:
        d = build(book, [u for u in units if u["book"] == book], by_unit, labels)
        json.dump(d, open(f"site/data/{book}.json", "w"), ensure_ascii=False, separators=(",", ":"))
        text |= set("".join(d["lines"]) + "".join(s["title"] + "".join(p["title"] for p in s["poems"]) for s in d["sections"]))
        print(book, len(d["lines"]), "lines", d["mentions"], "animals kept,", d["labelled"], "labelled")
    opts = subset.Options(); opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    ft = TTFont(FONT); sub = subset.Subsetter(opts); sub.populate(text="".join(sorted(text | set(" ۰۱۲۳۴۵۶۷۸۹«»")))); sub.subset(ft)
    ft.flavor = "woff2"; ft.save("site/data/hand.woff2")
