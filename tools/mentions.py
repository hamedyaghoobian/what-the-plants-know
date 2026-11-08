"""Find every plant word in the six books.

Each token of each unit is looked up in data/plants.tsv as written, then with Persian endings
and an attached preposition taken off (tools/tag.py), and two-word names (ابن آوی, سنگ پشت) are
joined first. Writes data/mentions.jsonl: one line per mention, with its unit, the half-line it
is in, its word index there, the form matched and the species.

  python3 -I tools/mentions.py data/units.jsonl data/mentions.jsonl
"""
import json, sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from tag import norm, candidates

PAIRS = {}
# whole words that an ending taken off would turn into a plant: wine, Sorush, a rug, battle, return...
STOP = set("نیست نیستند نیستی نیستم نیز نبید سروش سروشی گلیم گلیمی رزم رزمی رزمگاه عودت تاکی خسرو موش خرمای نشاخت کاهش کاهد بکاهی بکاهم بکاهد نکاهم نکاهد میکاهی می‌کاهی میکاهد بکاه بخار بخاری بخارا بخارای خارا خارای ببیخت میبیخت می‌بیخت نسیب بکنجد بخارید نخارید نخارم بخارست بخارش می‌خارید".split())
STOP_AFTER = {"خرما": {"موش"}}   # موش خرما is a weasel

def lexicon(path):
    lex = {}
    for row in open(path):
        if row.startswith("#") or not row.strip(): continue
        form, species, cls, homo, exact, *note = row.rstrip("\n").split("\t")
        lex[norm(form)] = {"form": form, "species": species, "class": cls, "homograph": homo == "1", "exact": exact == "1"}
    return lex

def find(words, lex):
    """(word index, how many words, lexicon entry) for the animals in a half-line or sentence"""
    out, i = [], 0
    while i < len(words):
        w = words[i].strip("،؛:.!؟?«»\"'()")
        nxt = words[i + 1].strip("،؛:.!؟?«»\"'()") if i + 1 < len(words) else ""
        pair = PAIRS.get((norm(w), norm(nxt)))
        if pair:
            out.append((i, 2, lex[norm(pair)])); i += 2; continue
        hit = None
        if norm(w) not in STOP:
            for form, rule in candidates(norm(w)):
                for f in (form, form.replace("‌", "")):
                    if f in lex and (rule == "as written" or not lex[f]["exact"]): hit = lex[f]; break
                if hit: break
        prev = norm(words[i - 1].strip("،؛:.!؟?«»\"'()")) if i else ""
        if hit and prev in STOP_AFTER.get(hit["form"], ()): hit = None
        if hit: out.append((i, 1, hit))
        i += 1
    return out

if __name__ == "__main__":
    lex = lexicon("data/plants.tsv")
    # a mention keeps its number from one run to the next (the labels are keyed by it): known
    # mentions are found by where they are, new ones are numbered after the last
    old = {}
    if os.path.exists(sys.argv[2]):
        for line in open(sys.argv[2]):
            m = json.loads(line); old[(m["unit"], m["half"], m["w"])] = m["id"]
    nxt = max(old.values(), default=-1) + 1
    n, by = 0, Counter()
    found = []
    if True:
        for line in open(sys.argv[1]):
            u = json.loads(line)
            for half, text in ((0, u["text"]), (1, u.get("text2", ""))):
                if not text: continue
                words = text.split(" ")
                for wi, span, e in find(words, lex):
                    i = old.get((u["id"], half, wi))
                    if i is None: i = nxt; nxt += 1
                    found.append({"id": i, "unit": u["id"], "book": u["book"], "half": half, "w": wi, "span": span,
                                  "token": " ".join(words[wi:wi + span]), "form": e["form"], "species": e["species"],
                                  "class": e["class"], "homograph": e["homograph"]})
                    n += 1; by[(u["book"], e["form"])] += 1
    with open(sys.argv[2], "w") as f:
        for m in sorted(found, key=lambda m: m["id"]): f.write(json.dumps(m, ensure_ascii=False) + "\n")
    print(n, "mentions,", sum(1 for m in found if m["id"] not in set(old.values())), "new")
    for book in ("kalila", "attar", "shahnameh", "masnavi", "marzban", "parvin"):
        items = sorted(((c, form) for (b, form), c in by.items() if b == book), reverse=True)
        print(book, sum(c for c, _ in items), " ".join(f"{form}:{c}" for c, form in items[:45]))
