"""Genera index.html del clon de @dotcsv «Hace tres años, este era el resultado de generar a Will Smith comiendo pasta…
pero tres años más tarde, esto es lo que podemos lograr» (https://www.tiktok.com/@dotcsv/video/7606027425373228310,
619.900 vistas, 50,8x su mediana). Desmontaje en datos/desmontajes/dotcsv-7606027425373228310/.
Estructura copiada: ANTES (imagen vieja, cutre, con grano) en el s 0 con «Hace tres años, esto era…» → plano limpio →
vuelta a lo viejo en «…la tecnología en 2023» → «Pero tres años más tarde, esto es lo que podemos lograr» y corte a imagen
nítida (el resultado) → «Resultado que viene de… que está suponiendo un terremoto» → lista de lo que hace → «un antes y un
después, un terremoto para … todo». Subtítulos: una línea blanca en negrita, centrada, 3-4 palabras, como el original.
Fondo coral (el del set del original) en los planos de texto. Cambios: sin persona (b-roll Mixkit), 47 s en vez de 57 s, CTA.
Uso: python3 generar.py  (necesita trabajo/timing.json y trabajo/palabras.json)
"""
import json, html, re, unicodedata, difflib

T = json.load(open("trabajo/timing.json"))
W = json.load(open("trabajo/palabras.json"))
L = {l["scene"]: l for l in T["lines"]}
TOTAL = round(T["total"] + 0.9, 3)

def norm(w): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", w.lower()).encode("ascii", "ignore").decode())
def t_de(palabra, desde):
    for w in W:
        if w["s"] >= desde - 0.3 and norm(palabra) in norm(w["w"]): return w["s"]
    raise SystemExit(f"no encuentro {palabra}")
def ini(sc): return round(L[sc]["start"] - 0.08, 3)

# ---------- planos (cortes) ----------
t_2023 = t_de("2023", ini("s3")); t_pero = ini("s4"); t_esc = t_de("escribe", ini("s5"))
t_resp = t_de("respuesta", ini("s5")); t_hueco = t_de("hueco", ini("s5")); t_cita = t_de("cita", ini("s5"))
t_rec = t_de("recepcionista", ini("s6")); t_terr = t_de("terremoto", ini("s6"))
t_cont = ini("s7"); t_ofr = t_de("ofrece", ini("s7")); t_avi = t_de("avisa", ini("s7")); t_recu = t_de("recuerda", ini("s7"))
t_antes = ini("s8"); t_terr2 = t_de("terremoto", ini("s8"))
pal8 = ["talleres", "clínicas", "peluquerías", "reformas", "academ", "todo"]
t8 = [t_de(p, t_terr2) for p in pal8]
t_cta = ini("s9"); t_com = t_de("comenta", t_cta); t_recep = t_de("recepci", t_cta)
t_marca = round(L["s9"]["end"] + 0.2, 3)
t_tres = t_de("tres", t_pero)  # «Pero tres años más tarde»
t_tarde = t_de("tarde", t_pero)

planos = [  # (id, inicio, tipo, contenido)
    ("p1", 0.0, "viejo", "viejo_tel"),
    ("p2", t_de("taller", 0) - 0.05, "viejo", "viejo_tel2"),
    ("p3", ini("s2"), "viejo", "viejo_cinta"),
    ("p4", L["s2"]["end"] + 0.5, "nuevo", "taller1"),
    ("p5", t_2023 - 0.25, "viejo", "estatica"),
    ("p6", t_tarde - 0.1, "nuevo", "noche"),
    ("p7", t_esc - 0.3, "chat", None),
    ("p8", ini("s6"), "nuevo", "taller2"),
    ("p9", t_rec - 0.1, "noti", None),
    ("p10", t_cont, "nuevo", "whatsapp"),
    ("p11", t_ofr - 0.1, "agenda", None),
    ("p12", t_avi - 0.15, "aviso", None),
    ("p14", t_antes, "split", None),
    ("p15", t_terr2 - 0.1, "lista", None),
    ("p16", t_cta, "cta", None),
    ("p17", t_marca, "marca", None),
]
B = {p[0]: round(p[1], 3) for p in planos}
orden = [p[0] for p in planos]
def dur(pid):
    i = orden.index(pid)
    return round((B[orden[i + 1]] if i + 1 < len(orden) else TOTAL) - B[pid], 3)

# ---------- subtítulos (una línea, 2-4 palabras) ----------
TROZOS = {
    "s1": "Hace tres años,|esto era lo que oías|al llamar a un taller|un domingo por la noche.",
    "s2": "«Deje su mensaje|después de la señal.»",
    "s3": "Impresionante,|para lo que permitía|la tecnología en 2023.",
    "s4": "Pero tres años|más tarde,|esto es lo que|podemos lograr.",
    "s6": "Resultado que viene|de una recepcionista|con inteligencia artificial,|que está suponiendo|un terremoto|para los negocios locales.",
    "s7": "Contesta a cualquier hora,|ofrece huecos de tu agenda,|te avisa a ti,|y le recuerda la cita|al cliente.",
    "s8": "Estamos ante|un antes y un después.",
}
SUB = []
for sc, spec in TROZOS.items():
    Ls = L[sc]
    ww = [w for w in W if w["s"] >= Ls["start"] - 0.3 and w["s"] < Ls["end"] + 0.1]
    chunks = spec.split("|")
    words = [(i, x) for i, c in enumerate(chunks) for x in c.split()]
    a = [norm(x) for _, x in words]; b = [norm(w["w"]) for w in ww]
    t = [None] * len(words)
    for blk in difflib.SequenceMatcher(None, a, b).get_matching_blocks():
        for k in range(blk.size): t[blk.a + k] = ww[blk.b + k]["s"]
    known = [(i, x) for i, x in enumerate(t) if x is not None]
    for i in range(len(t)):
        if t[i] is None:
            prev = max([k for k in known if k[0] < i], default=(-1, Ls["start"]), key=lambda k: k[0])
            nxt = min([k for k in known if k[0] > i], default=(len(t), Ls["end"]), key=lambda k: k[0])
            t[i] = prev[1] + (nxt[1] - prev[1]) * (i - prev[0]) / (nxt[0] - prev[0])
    pos = 0
    starts = []
    for c in chunks:
        starts.append((t[pos], c)); pos += len(c.split())
    for ci, (s, c) in enumerate(starts):
        e = (starts[ci + 1][0] if ci + 1 < len(starts) else Ls["end"] + 0.25) - 0.03
        SUB.append({"s": round(max(0, s - 0.05), 2), "e": round(e, 2), "txt": c, "sc": sc})
SUB[0]["s"] = 0.0
for c in SUB:
    if c["sc"] == "s8": c["e"] = min(c["e"], round(B["p15"] - 0.03, 2))
# en s7 los textos de pantalla y el subtítulo dicen lo mismo: el subtítulo va arriba de la tarjeta
def cap_html():
    out = []
    for i, c in enumerate(SUB):
        d = round(max(0.2, c["e"] - c["s"]), 3)
        cls = "cap alto" if c["sc"] == "s7" else "cap"
        out.append(f'      <div id="c{i}" class="{cls} clip" data-start="{c["s"]:.3f}" data-duration="{d}" data-track-index="20">{html.escape(c["txt"])}</div>')
    return "\n".join(out)

css = """
      :root { --coral: #e9605a; --coral2: #c9443f; --verde: #25d366; --wa: #0b141a; --gris: #8696a0; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #111; }
      #root { width: 100%; height: 100%; position: relative; font-family: "Inter"; color: #fff; }
      .escena { position: absolute; inset: 0; overflow: hidden; background: #111; }
      .vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .velo { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.05) 50%, rgba(0,0,0,0.55) 80%, rgba(0,0,0,0.3)); }
      /* look VHS para el ANTES */
      .vhs { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0 3px, rgba(0,0,0,0) 3px 7px); mix-blend-mode: multiply; }
      .vign { position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,0.65) 100%); }
      .osd { position: absolute; left: 70px; top: 110px; font-family: "JetBrains Mono"; font-weight: 700; font-size: 50px; color: #f2f2f2; text-shadow: 3px 3px 0 #000; letter-spacing: 2px; }
      .osd2 { position: absolute; right: 70px; top: 110px; font-family: "JetBrains Mono"; font-weight: 700; font-size: 50px; color: #f2f2f2; text-shadow: 3px 3px 0 #000; }
      .osd .rec { color: #ff3b30; }
      #lcd { position: absolute; left: 90px; right: 90px; top: 560px; padding: 40px 44px; background: #93a37a; border: 10px solid #3a3a36; border-radius: 18px; box-shadow: inset 0 0 40px rgba(0,0,0,0.45), 0 20px 50px rgba(0,0,0,0.6); font-family: "JetBrains Mono"; font-weight: 700; color: #20261a; font-size: 58px; line-height: 1.25; text-transform: uppercase; }
      #lcd small { display: block; font-size: 34px; opacity: 0.75; margin-bottom: 14px; }
      #piip { position: absolute; left: 0; right: 0; top: 1020px; text-align: center; font-family: "Archivo Black"; font-size: 150px; color: #fff; text-shadow: 0 6px 30px #000; }
      #ano { position: absolute; left: 0; right: 0; top: 640px; text-align: center; font-family: "Archivo Black"; font-size: 300px; line-height: 1; color: #fff; text-shadow: 0 10px 40px #000; }
      #ano2 { position: absolute; left: 0; right: 0; top: 240px; text-align: center; font-family: "Archivo Black"; font-size: 210px; line-height: 1; color: #fff; text-shadow: 0 10px 40px rgba(0,0,0,0.8); }
      #flash { position: absolute; inset: 0; background: #fff; }
      /* móvil con WhatsApp */
      .fondo-borroso { filter: blur(14px) brightness(0.55); transform: scale(1.1); }
      .movil { position: absolute; left: 140px; top: 150px; width: 800px; height: 1330px; border-radius: 70px; background: #000; padding: 22px; box-shadow: 0 50px 120px rgba(0,0,0,0.7), 0 0 0 4px #2a2a2a; }
      .pant { position: relative; width: 100%; height: 100%; border-radius: 52px; overflow: hidden; background: var(--wa); }
      .wa-top { height: 170px; background: #1f2c34; display: flex; align-items: flex-end; gap: 22px; padding: 0 30px 24px; }
      .wa-top .av { width: 86px; height: 86px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; }
      .wa-top .av img { width: 64px; height: 64px; }
      .wa-top b { display: block; font-size: 36px; } .wa-top span { display: block; font-size: 25px; color: var(--gris); margin-top: 4px; }
      .wa-body { padding: 30px 28px; }
      .dia { text-align: center; margin: 0 auto 26px; width: 320px; padding: 8px 0; border-radius: 14px; background: #182229; color: var(--gris); font-size: 24px; }
      .msg { max-width: 600px; padding: 20px 26px; border-radius: 24px; font-size: 35px; line-height: 1.28; margin-bottom: 20px; }
      .msg small { display: block; font-size: 21px; color: rgba(255,255,255,0.55); margin-top: 6px; text-align: right; }
      .cli { background: #202c33; border-top-left-radius: 6px; }
      .bot { background: #005c4b; border-top-right-radius: 6px; margin-left: auto; }
      .ok { position: absolute; left: 40px; right: 40px; bottom: 50px; padding: 26px 30px; border-radius: 26px; background: #f4f5f6; color: #111; display: flex; gap: 22px; align-items: center; box-shadow: 0 20px 60px rgba(0,0,0,0.6); }
      .ok .ic { width: 84px; height: 84px; flex: none; border-radius: 22px; background: var(--verde); display: flex; align-items: center; justify-content: center; font-size: 48px; }
      .ok b { display: block; font-size: 33px; } .ok span { display: block; font-size: 28px; color: #333; margin-top: 4px; }
      /* tarjetas */
      .tarj { position: absolute; left: 80px; right: 80px; top: 560px; padding: 40px 40px; border-radius: 36px; background: rgba(246,247,248,0.97); color: #111; box-shadow: 0 40px 100px rgba(0,0,0,0.6); }
      .tarj h3 { font-size: 40px; font-weight: 900; margin-bottom: 20px; }
      .tarj .noti { display: flex; gap: 24px; align-items: center; }
      .tarj .noti .ic { width: 110px; height: 110px; flex: none; border-radius: 28px; background: var(--coral); display: flex; align-items: center; justify-content: center; font-size: 60px; }
      .tarj .noti b { display: block; font-size: 40px; } .tarj .noti span { display: block; font-size: 34px; color: #333; margin-top: 6px; } .tarj .noti small { display: block; font-size: 26px; color: #777; margin-top: 6px; }
      .hora { display: flex; gap: 18px; align-items: center; padding: 22px 22px; border-radius: 18px; background: #eceef0; margin-bottom: 14px; font-size: 34px; }
      .hora b { width: 150px; font-family: "JetBrains Mono"; color: #555; }
      .hora.libre { background: #d9f7e5; border: 3px solid var(--verde); }
      .hora.libre b { color: #0d7a3c; }
      .hora em { font-style: normal; margin-left: auto; font-size: 28px; color: #0d7a3c; font-weight: 700; }
      /* split antes / después */
      .mitad { position: absolute; left: 0; width: 1080px; height: 960px; overflow: hidden; }
      .mitad .vid { height: 1920px; top: -480px; }
      .etq { position: absolute; left: 50px; font-family: "Archivo Black"; font-size: 96px; text-shadow: 0 6px 24px #000; }
      #raya { position: absolute; left: 0; right: 0; top: 954px; height: 12px; background: #fff; }
      /* lista en coral (el fondo del set del original) */
      .coral { background: radial-gradient(circle at 50% 35%, #f07a6f 0%, var(--coral) 45%, var(--coral2) 100%); }
      #terr { position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 60px; font-weight: 800; }
      .pal { position: absolute; left: 0; right: 0; top: 760px; text-align: center; font-family: "Archivo Black"; font-size: 150px; line-height: 1; text-shadow: 0 8px 30px rgba(0,0,0,0.25); }
      #todo { font-size: 300px; top: 690px; }
      /* CTA */
      #ctab { position: absolute; left: 0; right: 0; top: 560px; text-align: center; }
      #ctab .l1 { font-size: 60px; font-weight: 800; line-height: 1.2; }
      #ctab .pal2 { display: inline-block; margin-top: 50px; padding: 26px 56px; border-radius: 30px; background: #fff; color: var(--coral2); font-family: "Archivo Black"; font-size: 120px; box-shadow: 0 20px 60px rgba(0,0,0,0.25); }
      #ctab .l3 { margin-top: 50px; font-size: 52px; font-weight: 700; }
      #marca { background: #0f1012; display: flex; flex-direction: column; align-items: center; justify-content: center; }
      #marca img { width: 260px; height: 260px; }
      #marca b { font-weight: 900; font-size: 84px; margin-top: 40px; letter-spacing: -1px; }
      #marca span { font-size: 40px; margin-top: 14px; color: rgba(255,255,255,0.75); }
      /* subtítulos como el original: una línea blanca en negrita */
      .cap { position: absolute; left: 40px; right: 40px; top: 1470px; text-align: center; font-weight: 800; font-size: 66px; line-height: 1.1; text-shadow: 0 3px 14px rgba(0,0,0,0.95), 0 0 4px #000; }
      .cap.alto { top: 300px; }
"""

def esc(pid, inner, extra_cls=""):
    return f'      <div id="{pid}" class="escena clip {extra_cls}" data-start="{B[pid]:.3f}" data-duration="{dur(pid)}" data-track-index="1">\n{inner}\n      </div>'
def vid(vid_id, src, pid, ms=0, cls="vid"):
    return f'        <video id="{vid_id}" class="clip {cls}" src="assets/{src}.mp4" data-start="{B[pid]:.3f}" data-duration="{dur(pid)}" data-media-start="{ms}" muted playsinline data-track-index="2"></video>'
VHS = '        <div class="vhs"></div><div class="vign"></div>\n        <div class="osd"><span class="rec">●</span> PLAY</div><div class="osd2">DOM 23:47</div>'
VELO = '        <div class="velo"></div>'

def movil(cuerpo, extra=""):
    return ('        <div class="movil"><div class="pant"><div class="wa-top"><div class="av"><img src="assets/logo.svg" alt="" /></div>'
            '<div><b>Talleres Robledo</b><span>Asistente · en línea</span></div></div>'
            f'<div class="wa-body">{cuerpo}</div>{extra}</div></div>')

H = {}
H["p1"] = vid("v1", "viejo_tel", "p1") + "\n" + VHS
H["p2"] = vid("v2", "viejo_tel2", "p2") + "\n" + VHS
H["p3"] = (vid("v3", "viejo_cinta", "p3") + "\n" + VHS +
           '\n        <div id="lcd">Deje su mensaje después de la señal</div>\n        <div id="piip">PIIIP</div>')
H["p4"] = vid("v4", "taller1", "p4") + "\n" + VELO
H["p5"] = vid("v5", "estatica", "p5") + "\n" + VHS + '\n        <div id="ano">2023</div>'
H["p6"] = vid("v6", "noche", "p6") + "\n" + VELO + '\n        <div id="ano2">2026</div>\n        <div id="flash"></div>'
chat = ('<div class="dia">DOMINGO</div>'
        '<div id="m1" class="msg cli">Me chirrían los frenos 😬 ¿Podéis mirarlo?<small>23:10</small></div>'
        '<div id="m2" class="msg bot">¡Claro, Raúl! 🔧 Mañana lunes a las 8:30. ¿Te va bien?<small>23:10 ✓✓</small></div>'
        '<div id="m3" class="msg cli">Sí 👍<small>23:11</small></div>'
        '<div id="m4" class="msg bot">Hecho ✅ Lunes 8:30, frenos.<small>23:11 ✓✓</small></div>')
H["p7"] = (vid("v7", "noche", "p7", ms=2, cls="vid fondo-borroso") + "\n" +
           movil(chat, '<div id="ok7" class="ok"><div class="ic">📅</div><div><b>Cita creada</b><span>Raúl · frenos · lun 8:30</span></div></div>'))
H["p8"] = vid("v8", "taller2", "p8") + "\n" + VELO
H["p9"] = (vid("v9", "taller3", "p9") + "\n" + VELO +
           '\n        <div id="n9" class="tarj" style="top:420px"><div class="noti"><div class="ic">🔔</div><div><b>Nueva cita agendada</b><span>Raúl · ruido al frenar</span><small>Lunes 8:30 · por WhatsApp a las 23:10</small></div></div></div>')
H["p10"] = vid("v10", "whatsapp", "p10") + "\n" + VELO
H["p11"] = (vid("v11", "taller1", "p11", ms=2.5, cls="vid fondo-borroso") +
            '\n        <div id="ag" class="tarj"><h3>Agenda del lunes</h3>'
            '<div class="hora"><b>8:00</b>ITV</div><div class="hora libre"><b>8:30</b>Libre<em>ofrecida ✓</em></div>'
            '<div class="hora"><b>9:30</b>Cambio de aceite</div></div>')
H["p12"] = (vid("v12", "taller3", "p12", ms=3) + "\n" + VELO +
            '\n        <div id="n12" class="tarj" style="top:420px"><div class="noti"><div class="ic">🔔</div><div><b>Cita nueva</b><span>Raúl · frenos · lun 8:30</span></div></div></div>'
            '\n        <div id="n13" class="tarj" style="top:760px"><div class="noti"><div class="ic" style="background:#25d366">⏰</div><div><b>Recordatorio enviado</b><span>a Raúl · lunes 7:30</span></div></div></div>')
H["p14"] = (f'        <div class="mitad" style="top:0">' + vid("v14a", "viejo_tel", "p14", ms=2).strip() + '<div class="vhs"></div><div class="etq" style="top:760px">ANTES</div></div>\n'
            f'        <div class="mitad" style="top:960px">' + vid("v14b", "whatsapp", "p14", ms=1).strip() + '<div class="etq" style="top:60px">AHORA</div></div>\n'
            '        <div id="raya"></div>')
H["p15"] = ('        <div id="terr">Un terremoto para…</div>\n' +
            "\n".join(f'        <div id="w{i}" class="pal">{html.escape(p)}</div>' for i, p in enumerate(["talleres", "clínicas", "peluquerías", "reformas", "academias"])) +
            '\n        <div id="todo" class="pal">TODO.</div>')
H["p16"] = ('        <div id="ctab"><div class="l1">¿Tienes un negocio?</div>'
            '<div class="l3" id="l3">Comenta la palabra</div><div class="pal2" id="pal2">RECEPCIÓN</div>'
            '<div class="l3" id="l4">y te mando la demo</div></div>')
H["p17"] = ('        <img id="logo" src="assets/logo.svg" alt="" />\n        <b>norte.local</b>\n'
            '        <span>Recepcionista con IA para negocios locales</span>')
extra = {"p15": "coral", "p16": "coral"}
escenas = "\n".join(esc(pid, H[pid], extra.get(pid, "")) for pid in orden).replace('id="p17" class="escena clip ', 'id="marca" class="escena clip ')

js = f"""
      const tl = gsap.timeline({{ paused: true }});
      // ANTES: temblor de cinta y zoom lento
      ["#v1", "#v2", "#v3", "#v5"].forEach((v, i) => tl.fromTo(v, {{ scale: 1.08 }}, {{ scale: 1.0, duration: 2.6, ease: "none" }}, [{B['p1']}, {B['p2']}, {B['p3']}, {B['p5']}][i]));
      tl.fromTo("#lcd", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {B['p3'] + 0.05});
      tl.fromTo("#piip", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.15 }}, {L['s2']['end'] + 0.02:.2f});
      tl.fromTo("#ano", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power3.out" }}, {t_2023 - 0.05:.2f});
      // DESPUÉS: destello blanco y nitidez
      tl.fromTo("#flash", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35 }}, {B['p6']});
      tl.fromTo("#v6", {{ scale: 1.15 }}, {{ scale: 1.0, duration: {dur('p6')}, ease: "power1.out" }}, {B['p6']});
      tl.fromTo("#ano2", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "power3.out" }}, {B['p6'] + 0.05});
      // chat
      tl.fromTo("#p7 .movil", {{ opacity: 0, y: 140, rotation: -4 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "power3.out" }}, {B['p7']});
      tl.fromTo("#m1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {B['p7'] + 0.35:.2f});
      tl.fromTo("#m2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {t_resp - 0.6:.2f});
      tl.fromTo("#m3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {t_hueco + 0.2:.2f});
      tl.fromTo("#m4", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {t_cita - 0.7:.2f});
      tl.fromTo("#ok7", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {t_cita + 0.1:.2f});
      tl.fromTo("#v8", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {dur('p8')}, ease: "none" }}, {B['p8']});
      tl.fromTo("#n9", {{ opacity: 0, y: -160 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {B['p9'] + 0.15});
      // terremoto: sacudida
      tl.to("#p9", {{ x: 18, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }}, {t_terr - 0.03:.2f});
      tl.set("#p9", {{ x: 0 }}, {t_terr + 0.4:.2f});
      tl.fromTo("#v10", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {dur('p10')}, ease: "none" }}, {B['p10']});
      tl.fromTo("#ag", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {B['p11']});
      tl.fromTo("#ag .libre", {{ scale: 0.9 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {B['p11'] + 0.3});
      tl.fromTo("#n12", {{ opacity: 0, y: -160 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, {B['p12'] + 0.05});
      tl.fromTo("#n13", {{ opacity: 0, x: 200 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.6)" }}, {t_recu - 0.1:.2f});
      tl.fromTo("#raya", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3 }}, {B['p14']});
      // lista: cada palabra entra cuando se dice
      tl.fromTo("#terr", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {B['p15']});
      const tp = {json.dumps([round(x, 2) for x in t8])};
      for (let i = 0; i < 5; i++) {{
        tl.fromTo("#w" + i, {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "power3.out" }}, tp[i] - 0.04);
        tl.set("#w" + i, {{ opacity: 0 }}, tp[i + 1] - 0.05);
      }}
      tl.fromTo("#todo", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, tp[5] - 0.05);
      tl.to("#p15", {{ x: 16, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }}, tp[5]);
      tl.fromTo("#ctab .l1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {B['p16']});
      tl.fromTo("#l3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {t_com - 0.1:.2f});
      tl.fromTo("#pal2", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {t_recep - 0.08:.2f});
      tl.fromTo("#l4", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {t_recep + 0.6:.2f});
      tl.fromTo("#logo", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {B['p17']});
      document.querySelectorAll(".cap").forEach((c) => tl.fromTo(c, {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.08 }}, parseFloat(c.dataset.start)));
      window.__timelines["main"] = tl;
      tl.seek(0);
"""

golpes = [B["p4"], B["p6"], B["p8"], B["p14"], B["p15"], B["p16"], t_terr, t8[5]]
dings = [B["p7"] + 0.35, t_recu - 0.1, t_resp - 0.2, t_cita + 0.1, B["p9"] + 0.15, B["p12"] + 0.05]
aud = [f'      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="30"></audio>',
       f'      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="{t_tarde - 0.1:.2f}" data-duration="{round(TOTAL - t_tarde + 0.1, 2)}" data-media-start="0" data-volume="0.22" data-fade-out="1.2" data-track-index="31"></audio>',
       f'      <audio id="pip" class="clip" src="assets/pip.wav" data-start="{L["s2"]["end"] + 0.02:.2f}" data-duration="0.55" data-volume="0.35" data-track-index="50"></audio>']
aud += [f'      <audio id="g{i}" class="clip" src="assets/golpe.wav" data-start="{max(0, t - 0.03):.2f}" data-duration="0.4" data-volume="0.45" data-track-index="{32 + i}"></audio>' for i, t in enumerate(golpes)]
aud += [f'      <audio id="d{i}" class="clip" src="assets/ding.wav" data-start="{t:.2f}" data-duration="0.35" data-volume="0.3" data-track-index="{42 + i}"></audio>' for i, t in enumerate(dings)]

doc = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>{css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{escenas}
{cap_html()}
{chr(10).join(aud)}
    </div>
    <script>{js}    </script>
  </body>
</html>
"""
open("index.html", "w").write(doc)
print("ok", TOTAL, len(orden), "planos", {k: B[k] for k in orden})
