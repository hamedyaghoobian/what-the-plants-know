# What the Plants Know

Readings, Otherwise, No. 5. *Kalila wa Dimna* (Nasrollah Monshi), Attar's *Conference of the Birds*,
Ferdowsi's *Shahnameh*, Rumi's *Masnavi*, Varavini's *Marzban-nameh*, Parvin E'tesami's *Divan*, and
Saadi's *Golestan* and *Bustan*, with every word taken out but the plants, each lit by how high up
the ladder of souls the text lifts it. With an atlas that counts it all. The companion to No. 4,
[What the Animals Know](https://github.com/hamedyaghoobian/what-the-animals-know), and built from its code.

## The frame

There is no book that does for plants what Steven Wagschal's *Minding Animals* (2018) does for
animals, so the frame is the tradition's own: Avicenna's division of the soul (after Aristotle) into
the vegetative soul (feeding, growing, bearing seed), the animal soul (adding sense, feeling,
desire) and the rational soul (adding speech and reason), and Rumi's poem of the ladder, *Masnavi*
III, section 187 (از جمادی مردم و نامی شدم). Each plant is placed on it:

| rung (field value) | on the page | |
|---|---|---|
| a thing (`anthropectomy`) | faintest | wood, fuel, fodder, scent, dye, tribute |
| plant life only (`species-typical`) | half | it grows, blooms, fruits, withers |
| a sense true to the plant (`constructive`) | yellow | it thirsts, turns to the sun, is drunk beside water |
| the animal soul (`gratuitous`, rung `animal`) | strong | it laughs, weeps, longs, is proud |
| the human soul (`gratuitous`, rung `human`) | full | it speaks, argues, prays, knows |

The yellow rung is the one modern plant science (Paco Calvo, *Planta Sapiens*, 2022) adds and the
old ladder lacks. The field names are kept from the animal scheme so the two pieces can be compared.
Behind it: Michael Marder, *Plant-Thinking* (2013); Wandersee and Schussler on "plant blindness"
(1999); Annemarie Schimmel, *A Two-Colored Brocade* (1992), for the conventions of Persian imagery.

## The pipeline

- `tools/fetch.py`: downloads a book from the Ganjoor API, now with the poems at a book's own level (the *Golestan*'s preface). `/saadi/golestan` and `/saadi/boostan` are fetched here; the other six are read from `../animals-persian-lit/data/`.
- `tools/corpus.py`: one list of units, `data/units.jsonl` (not committed; rebuilt from the dumps), couplets for verse and sentences for prose. The first six books number their units as in No. 4.
- `data/plants.tsv`: the plant words looked for, 113 forms, by hand, with homographs marked and an `exact` flag for words that must not lose an ending (نیست is not نی). A plant's part counts (leaf, thorn, grain, wood); a made product (wine, bread, rosewater) and a place (garden, meadow) do not.
- `tools/mentions.py`: every plant word in the units into `data/mentions.jsonl` (6,628), with a stop list of whole words an ending would turn into a plant (نخست, گلیم, رزم, بخارا).
- `data/scheme.md`: the instructions every judgement was made under.
- `tools/annotate.py`: each mention with its passage and neighbours to the Claude API (Message Batches, structured output, the scheme cached), into `data/annotations.jsonl`. All 6,628 by Claude Sonnet 5.5 at medium effort, in one batch.
- `data/corrections.json`: four judgements changed by hand, with the reason. `data/hand-check.tsv`: 60 drawn at random (seed 2029) and read against their passages: 56 agree, 1 wrong (corrected), 3 arguable.
- `tools/shape.py`, `tools/atlas.py`: the page's data and the atlas's. `tools/stats.py`: the numbers below.
- `tools/naardoon.py`: 17 drawings from [NaarDoon](https://library.eranshahr.com)'s Plant category (`data/naardoon-catalogue.json`, 132 elements), chosen by eye, cut into silhouettes with `credits.json`.
- `site/`: the piece and the atlas, in the site's faceplate; meant to be served from the website (`readings-otherwise/what-the-plants-know/`).

```
ln -s ../animals-persian-lit/.venv .venv     # or: uv venv .venv && uv pip install anthropic uharfbuzz fonttools brotli pillow
python3 -I tools/corpus.py data/units.jsonl
python3 -I tools/mentions.py data/units.jsonl data/mentions.jsonl
.venv/bin/python tools/annotate.py dry 50 claude-sonnet-5-5
.venv/bin/python tools/annotate.py submit claude-sonnet-5-5     # ANTHROPIC_API_KEY in .env
.venv/bin/python tools/annotate.py collect <batch id>
.venv/bin/python -I tools/shape.py && python3 -I tools/atlas.py && python3 -I tools/stats.py
```

## What it found

Of 6,628 matches, 5,202 are plants; 2,887 of those (55%) are figures of speech.

| | plants | figures of speech | human soul | animal soul | a sense true to it | plant life only | a thing |
|---|---|---|---|---|---|---|---|
| Kalila wa Dimna | 207 | 50% | 1% | 1% | 0% | 52% | 46% |
| Conference of the Birds | 130 | 49% | 2% | 10% | 0% | 19% | 70% |
| Shahnameh | 1,489 | 60% | 3% | 1% | 0% | 48% | 48% |
| Masnavi | 1,734 | 61% | 6% | 2% | 1% | 47% | 44% |
| Marzban-nameh | 262 | 57% | 5% | 5% | 0% | 53% | 38% |
| Parvin E'tesami, Divan | 933 | 36% | 19% | 4% | 0% | 57% | 19% |
| Golestan | 169 | 49% | 5% | 1% | 0% | 54% | 40% |
| Bustan | 278 | 68% | 0% | 0% | 2% | 40% | 57% |

(The rung shares are of the plants that are not figures of speech.) Only 12 plants in eight books
are given a sense true to plants. Of the 178 given speech or reason, 113 are Parvin's; the
*Shahnameh*'s 16 are nearly all Alexander's talking tree. Plants eaten, used or given are things 92
to 95 per cent of the time; plants in a garden are given a human soul 18 per cent of the time, wild
ones 5.

## Licences

The eight texts are in the public domain (Parvin E'tesami died in 1941); the text and headings are
Ganjoor's. The judgements were produced with the Claude API. Amiri is by Khaled Hosny, under the SIL
Open Font License 1.1 (`fonts/OFL.txt`); `site/data/hand.woff2` is a subset of it. The drawings in
`site/data/naardoon/` are from NaarDoon, which offers them to download and build with freely; each is
the work of the contributor named in `credits.json`, traced from an object whose own rights rest with
its collection.
