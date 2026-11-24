"""Subtítulos al estilo del viral: una línea pequeña blanca y, debajo, la palabra clave en grande.
Formato de cada trozo: "pequeño/#Grande" (negrita sans) o "pequeño/*Grande" (serif cursiva) o solo "pequeño".
"""
import json, re, difflib, unicodedata
T = json.load(open('trabajo/timing.json'))
W = json.load(open('trabajo/palabras.json'))
TROZOS = {
 "s1": "La/#inteligencia artificial|acaba de hacer/*otra locura",
 "s3": "No solamente/#contesta|a tus clientes/*a cualquier hora",
 "s4": "ni se queda solo|con lo que/#necesitan",
 "s5": "sino que además ahora|les ofrece una hora/#de tu agenda|y les crea/*la visita",
 "s6": "Y no hablo de/#un contestador|Hablo de una/*recepcionista",
 "s7": "Ya que ahora|desde aquí vas a poder ver/#cada visita",
 "s8": "qué quería/#cada cliente|y en qué/*estado está",
 "s9": "De igual forma/#te avisa a ti|en el/*momento",
 "s10": "y le recuerda/#la cita|el día antes/*para que no falte",
 "s11": "Incluso puedes ver/#de dónde te escriben",
}
def norm(w): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode())
lines = {l["scene"]: l for l in T["lines"]}
out = []
for sc, spec in TROZOS.items():
    L = lines[sc]
    ww = [w for w in W if w["s"] >= L["start"] - 0.3 and w["s"] < L["end"] + 0.1]
    chunks = spec.split("|")
    words = [(i, x) for i, c in enumerate(chunks) for x in c.replace("/#", " ").replace("/*", " ").split()]
    a = [norm(x) for _, x in words]; b = [norm(w["w"]) for w in ww]
    t = [None] * len(words)
    for blk in difflib.SequenceMatcher(None, a, b).get_matching_blocks():
        for k in range(blk.size): t[blk.a + k] = ww[blk.b + k]["s"]
    known = [(i, x) for i, x in enumerate(t) if x is not None]
    for i in range(len(t)):
        if t[i] is None:
            prev = max([k for k in known if k[0] < i], default=(-1, L["start"]), key=lambda k: k[0])
            nxt = min([k for k in known if k[0] > i], default=(len(t), L["end"]), key=lambda k: k[0])
            t[i] = prev[1] + (nxt[1] - prev[1]) * (i - prev[0]) / (nxt[0] - prev[0])
    # inicio de cada trozo y de su palabra grande
    pos = 0; starts = []
    for ci, c in enumerate(chunks):
        if "/" in c:
            peq, gr = c.split("/", 1); estilo = gr[0]; gr = gr[1:]
        else:
            peq, gr, estilo = c, "", ""
        n_peq = len(peq.split())
        starts.append((t[pos], t[pos + n_peq] if gr else None, peq, gr, estilo))
        pos += n_peq + len(gr.split())
    for ci, (s, sg, peq, gr, estilo) in enumerate(starts):
        s = max(s - 0.05, L["start"] - 0.05)
        e = (starts[ci + 1][0] if ci + 1 < len(starts) else L["end"] + 0.25) - 0.03
        out.append({"scene": sc, "peq": peq, "gr": gr, "estilo": estilo, "s": round(s, 2),
                    "sg": round(sg - 0.04, 2) if sg else None, "e": round(e, 2)})
json.dump(out, open('trabajo/subtitulos.json', 'w'), ensure_ascii=False, indent=0)
for o in out: print(o["scene"], o["s"], o["sg"], o["e"], o["peq"], "/", o["estilo"], o["gr"])
