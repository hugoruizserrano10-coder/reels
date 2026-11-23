"""Subtítulos palabra a palabra (estilo del viral): trozos de 1-3 palabras; los que empiezan por * van en grande a dos tonos."""
import json, re, difflib, unicodedata
T = json.load(open('trabajo/timing.json'))
W = json.load(open('trabajo/palabras.json'))
TROZOS = {
 "s1": "",
 "s2": "Hay una herramienta|que se está haciendo|*muy viral|entre los negocios|*del norte de Madrid",
 "s3": "*Una recepcionista|con inteligencia artificial|que contesta|*cualquier mensaje|*a cualquier hora",
 "s4": "Desde aquí vas a poder|ver todo lo que pasa|en tu negocio|*en tiempo real",
 "s5": "", "s6": "",
 "s7": "No solo eso:|también le recuerda|*la cita|al cliente el día antes|*para que no falte",
 "s8": "Y todo eso|*mientras tú duermes",
 "s9": "",
}
def norm(w): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode())
lines = {l["scene"]: l for l in T["lines"]}
voz = {k: v for k, v in json.load(open('voz.json'))["voz"]}
out = []
for sc, spec in TROZOS.items():
    if not spec: continue
    L = lines[sc]
    ww = [w for w in W if w["s"] >= L["start"] - 0.3 and w["s"] < L["end"] + 0.1]
    chunks = spec.split("|")
    words = [(i, x) for i, c in enumerate(chunks) for x in c.lstrip("*").split()]
    a = [norm(x) for _, x in words]; b = [norm(w["w"]) for w in ww]
    t = [None] * len(words)
    for blk in difflib.SequenceMatcher(None, a, b).get_matching_blocks():
        for k in range(blk.size): t[blk.a + k] = ww[blk.b + k]["s"]
    # interpolar huecos
    known = [(i, x) for i, x in enumerate(t) if x is not None]
    for i in range(len(t)):
        if t[i] is None:
            prev = max([k for k in known if k[0] < i], default=(-1, L["start"]), key=lambda k: k[0])
            nxt = min([k for k in known if k[0] > i], default=(len(t), L["end"]), key=lambda k: k[0])
            t[i] = prev[1] + (nxt[1] - prev[1]) * (i - prev[0]) / (nxt[0] - prev[0])
    starts = {}
    for (ci, _), ti in zip(words, t): starts.setdefault(ci, ti)
    for ci, c in enumerate(chunks):
        s = max(starts[ci] - 0.05, L["start"] - 0.05)
        e = starts.get(ci + 1, L["end"] + 0.2) - 0.03
        out.append({"scene": sc, "txt": c.lstrip("*"), "big": c.startswith("*"), "s": round(s, 2), "e": round(e, 2)})
json.dump(out, open('trabajo/subtitulos.json', 'w'), ensure_ascii=False, indent=0)
for o in out: print(o["scene"], o["s"], o["e"], ("*" if o["big"] else " ") + o["txt"])
