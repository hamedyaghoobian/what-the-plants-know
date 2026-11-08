"""One drawing per plant from NaarDoon, the open library of Iranian visual elements at
library.eranshahr.com, cut into a small silhouette for the page.

Each NaarDoon element is a contributor's tracing of a museum object or a miniature painting.
data/naardoon-catalogue.json lists the 132 elements of its Plant category (title, who traced it,
its source, its files), read from the library's pages; many share a title ("Tree"), so PICKS below
chooses one per species by its place in that list, looked at by eye. The image is downloaded,
reduced to 192 px high, and kept as its own shape (the alpha), which the page fills with a single
ink. Writes site/data/naardoon/<species>.png and site/data/naardoon/credits.json.

  .venv/bin/python -I tools/naardoon.py
"""
import io, json, os, re, time, urllib.request
from PIL import Image

# species on the page: the catalogue entry drawn for it. The cypress is a miniature's "Tree" that is
# one; the lily is Persian سوسن, the iris of the paintings. No drawing was found that reads alone as
# narcissus, reed, plane tree, date palm or pomegranate.
PICKS = {
    "tree": 55, "cypress": 50, "willow": 122, "tulip": 37, "water lily": 26, "vine": 11, "thorn": 63,
    "leaf": 16, "rose": 68, "flower": 24, "lily": 86, "branch": 40, "plant": 15, "grass": 109,
    "greenery": 72, "blossom": 85, "sapling": 113,
}
HIGH = 192

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "readings-otherwise (a page that credits NaarDoon)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

if __name__ == "__main__":
    cat = json.load(open("data/naardoon-catalogue.json"))
    os.makedirs("site/data/naardoon", exist_ok=True)
    credits = {}
    for species, title in PICKS.items():
        el = cat[title]
        out = f"site/data/naardoon/{species.replace(' ', '-')}.png"
        if not os.path.exists(out):
            im = Image.open(io.BytesIO(get(el["png"]))).convert("RGBA")
            box = im.getchannel("A").getbbox()                      # the drawing itself, without its margin
            if box: im = im.crop(box)
            im = im.resize((max(1, round(im.width * HIGH / im.height)), HIGH), Image.LANCZOS)
            Image.merge("RGBA", (*Image.new("RGB", im.size, (0, 0, 0)).split(), im.getchannel("A"))).save(out, optimize=True)
            time.sleep(.6)
        museum = re.sub(r"^https?://(www\.)?([^/]+)/.*$", r"\2", el["source"]) if el["source"].startswith("http") else el["source"]
        credits[species] = {"file": os.path.basename(out), "title": el["title"], "by": el["by"], "collection": el["collection"],
                            "source": el["source"], "museum": museum}
        print(f"{species:10s} {el['title'][:34]:34s} {el['by']:22s} {museum}")
    json.dump(credits, open("site/data/naardoon/credits.json", "w"), ensure_ascii=False, indent=1)
    print(len(credits), "drawings,", sum(os.path.getsize(f"site/data/naardoon/{c['file']}") for c in credits.values()) // 1024, "KB")
