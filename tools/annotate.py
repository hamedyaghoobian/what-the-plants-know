"""Label every plant mention on the ladder of souls, through the Claude API.

Each plant mention is sent with its passage (the couplet or sentence, the marked word in ⟦ ⟧), the
section heading, and the passages before and after it. The instructions are data/scheme.md,
the same for every request and cached. The answer is JSON in a fixed schema.

  .venv/bin/python tools/annotate.py dry 50 claude-haiku-5-5       # a sample, one by one, to read
  .venv/bin/python tools/annotate.py submit claude-haiku-5-5       # every mention not yet labelled, as a batch
  .venv/bin/python tools/annotate.py collect <batch id>            # write the results to data/annotations.jsonl
  .venv/bin/python tools/annotate.py sample 300 claude-sonnet-5-5  # the check sample, as a batch
"""
import json, os, random, sys, time
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = {"kalila": "Kalila wa Dimna", "attar": "Attar, Manteq al-Tayr", "shahnameh": "Ferdowsi, Shahnameh", "masnavi": "Rumi, Masnavi", "marzban": "Varavini, Marzban-nameh", "parvin": "Parvin E'tesami, Divan", "golestan": "Saadi, Golestan", "bustan": "Saadi, Bustan"}
FACULTIES = ["speech", "reasoning", "knowledge", "emotion", "deception", "perception", "desire", "memory", "moral", "devotion"]
SCHEMA = {
    "type": "object",
    "properties": {
        "is_plant": {"type": "boolean"},
        "species": {"type": "string"},
        "figure": {"type": "string", "enum": ["plant", "character", "figure", "none"]},
        "mode": {"type": "string", "enum": ["garden", "harvest", "eaten", "cut", "used", "gift", "wild", "emblem", "none"]},
        "faculties": {"type": "array", "items": {"type": "string", "enum": FACULTIES}},
        "spectrum": {"type": "string", "enum": ["anthropectomy", "species-typical", "constructive", "gratuitous", "none"]},
        "rung": {"type": "string", "enum": ["animal", "human", ""]},
        "evidence": {"type": "string"},
        "unsure": {"type": "boolean"},
    },
    "required": ["is_plant", "species", "figure", "mode", "faculties", "spectrum", "rung", "evidence", "unsure"],
    "additionalProperties": False,
}

def load_env():
    """ANTHROPIC_API_KEY from the project's .env, if it is not already set"""
    path = os.path.join(HERE, ".env")
    if os.environ.get("ANTHROPIC_API_KEY") or not os.path.exists(path):
        return
    for line in open(path):
        k, _, v = line.partition("=")
        if k.strip() and v.strip():
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def load():
    units = {}
    for line in open(os.path.join(HERE, "data/units.jsonl")):
        u = json.loads(line); units[u["id"]] = u
    mentions = [json.loads(l) for l in open(os.path.join(HERE, "data/mentions.jsonl"))]
    return units, mentions

def unit_text(u, mark=None):
    """the passage, with one word marked: mark = (half, word index, span)"""
    halves = [u["text"]] + ([u["text2"]] if u.get("text2") else [])
    if mark:
        half, w, span = mark
        ws = halves[half].split(" ")
        ws[w] = "⟦" + ws[w]; ws[w + span - 1] += "⟧"
        halves[half] = " ".join(ws)
    return " / ".join(halves)

def prompt(m, units):
    u = units[m["unit"]]
    near = lambda i: units.get(i) if units.get(i) and units[i]["book"] == u["book"] and units[i]["sec"] == u["sec"] and units[i]["ch"] == u["ch"] else None
    before, after = near(u["id"] - 1), near(u["id"] + 1)
    return (f"Book: {BOOKS[u['book']]}\nSection: {u['chapter']} · {u['title']}\n"
            f"Dictionary guess for the marked word: {m['species']}\n\n"
            + (f"Before: «{unit_text(before)}»\n" if before else "")
            + f"Passage: «{unit_text(u, (m['half'], m['w'], m['span']))}»\n"
            + (f"After: «{unit_text(after)}»\n" if after else ""))

def params(m, units, model, system):
    return {
        "model": model,
        "max_tokens": 4000,
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": prompt(m, units)}],
        "output_config": {"effort": "low" if "haiku" in model else "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
    }

def answer(message):
    if message.stop_reason == "refusal":
        return None
    text = next((b.text for b in message.content if b.type == "text"), "")
    return json.loads(text) if text else None

def done_ids(path):
    if not os.path.exists(path): return set()
    return {json.loads(l)["id"] for l in open(path)}

if __name__ == "__main__":
    load_env()
    client = anthropic.Anthropic()
    system = open(os.path.join(HERE, "data/scheme.md")).read()
    units, mentions = load()
    cmd = sys.argv[1]
    os.makedirs(os.path.join(HERE, "data/cache"), exist_ok=True)

    if cmd == "dry":
        n, model = int(sys.argv[2]), sys.argv[3]
        rnd = random.Random(11)
        pick = rnd.sample(mentions, n)
        out = os.path.join(HERE, f"data/cache/dry-{model}.jsonl")
        usage = {"in": 0, "cache_read": 0, "cache_write": 0, "out": 0}
        with open(out, "w") as f:
            for m in pick:
                msg = client.messages.create(**params(m, units, model, system))
                u = msg.usage
                usage["in"] += u.input_tokens; usage["out"] += u.output_tokens
                usage["cache_read"] += u.cache_read_input_tokens or 0; usage["cache_write"] += u.cache_creation_input_tokens or 0
                f.write(json.dumps({"id": m["id"], "model": model, "passage": prompt(m, units), "label": answer(msg)}, ensure_ascii=False) + "\n")
        print(json.dumps(usage), "for", n)

    elif cmd in ("submit", "sample"):
        if cmd == "submit":
            model = sys.argv[2]
            todo = [m for m in mentions if m["id"] not in done_ids(os.path.join(HERE, "data/annotations.jsonl"))]
        else:
            n, model = int(sys.argv[2]), sys.argv[3]
            todo = random.Random(5).sample(mentions, n)
            json.dump([m["id"] for m in todo], open(os.path.join(HERE, "data/check-ids.json"), "w"))
        batch = client.messages.batches.create(requests=[
            Request(custom_id=f"m{m['id']}", params=MessageCreateParamsNonStreaming(**params(m, units, model, system)))
            for m in todo])
        print(batch.id, len(todo), "requests", model)
        with open(os.path.join(HERE, "data/cache/batches.txt"), "a") as f:
            f.write(f"{batch.id}\t{cmd}\t{model}\t{len(todo)}\t{time.strftime('%Y-%m-%d %H:%M')}\n")

    elif cmd == "redo":   # label again, one by one, the mentions a file of ids names; replaces their labels
        ids, model = set(json.load(open(sys.argv[2]))), sys.argv[3]
        path = os.path.join(HERE, "data/annotations.jsonl")
        old = [json.loads(l) for l in open(path)]
        by_id = {m["id"]: m for m in mentions}
        new = {}
        for i in sorted(ids):
            lab = answer(client.messages.create(**params(by_id[i], units, model, system)))
            if lab is not None: new[i] = {"id": i, "model": model, **lab}
        with open(path, "w") as f:
            for a in old: f.write(json.dumps(new.get(a["id"], a), ensure_ascii=False) + "\n")
        print(len(new), "labelled again")

    elif cmd == "collect":
        bid = sys.argv[2]
        dest = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "data/annotations.jsonl")
        b = client.messages.batches.retrieve(bid)
        if b.processing_status != "ended":
            print(b.processing_status, b.request_counts); sys.exit(1)
        model = next(l.split("\t")[2] for l in open(os.path.join(HERE, "data/cache/batches.txt")) if l.startswith(bid))
        have = done_ids(dest); ok = bad = 0
        with open(dest, "a") as f:
            for r in client.messages.batches.results(bid):
                i = int(r.custom_id[1:])
                if i in have: continue
                lab = answer(r.result.message) if r.result.type == "succeeded" else None
                if lab is None: bad += 1; continue
                f.write(json.dumps({"id": i, "model": model, **lab}, ensure_ascii=False) + "\n"); ok += 1
        print(ok, "written,", bad, "failed or refused (run submit again for them)")
