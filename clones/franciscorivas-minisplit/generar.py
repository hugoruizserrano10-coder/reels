"""Genera index.html del clon de @soyfranciscorivas «Acompáñame a darle mantenimiento preventivo a este mini split»
(https://www.tiktok.com/@soyfranciscorivas/video/7649129985223019783 · 213.200 vistas, 734x su mediana).
Desmontaje en datos/desmontajes/soyfranciscorivas-7649129985223019783/.
Estructura copiada: «Acompáñame a darle mantenimiento preventivo a…» → ficha técnica → «a mí en lo particular me gusta
desmontarlo» → «no es por hablar mal del anterior técnico, pero…» → «posteriormente» hidrolimpiadora arriba y abajo → tallar
con agua y jabón → «le pregunté al cliente y me dijo: sí, es verdad» → armar con la pieza nueva → «ya no grabé lo demás porque
se me hacía tarde, jajaja, pero este es el proceso». Voz en off pausada de oficio (2,5 palabras/s), planos de trabajo y
subtítulos blancos con borde negro (los de sus otros vídeos). Cambio: el mantenimiento se le hace al TELÉFONO de un técnico
de aire acondicionado (absurdo), 55 s en vez de 162 s, música de fondo y CTA.
Uso: python3 generar.py (necesita trabajo/timing.json y trabajo/palabras.json)
"""
import json, html, re, unicodedata, difflib

T = json.load(open("trabajo/timing.json"))
W = json.load(open("trabajo/palabras.json"))
L = {l["scene"]: l for l in T["lines"]}
TOTAL = round(T["total"] + 1.6, 3)

def norm(w): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", w.lower()).encode("ascii", "ignore").decode())
def t_de(palabra, desde):
    for w in W:
        if w["s"] >= desde - 0.3 and norm(palabra) in norm(w["w"]): return w["s"]
    raise SystemExit(f"no encuentro {palabra}")
def ini(sc): return round(L[sc]["start"] - 0.08, 3) if sc != "s1" else 0.0

B = {s: ini(s) for s in ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11"]}
B["marca"] = round(L["s11"]["end"] + 0.25, 3)
orden = list(B)
def dur(sc):
    i = orden.index(sc)
    return round((B[orden[i + 1]] if i + 1 < len(orden) else TOTAL) - B[sc], 3)

# ---------- subtítulos (blancos, borde negro, 1-2 líneas, como CapCut) ----------
TROZOS = {
    "s1": "Acompáñame a darle|mantenimiento preventivo|al teléfono de este técnico|de aire acondicionado.",
    "s2": "Móvil de tres años.|47 llamadas perdidas.",
    "s3": "A mí, en lo particular,|me gusta desmontarlo entero,|para que quede bien limpio|cada rincón.",
    "s4": "No es por hablar mal|del anterior técnico,|pero le dejó el buzón de voz lleno,|y un «luego te llamo»|pegado en cada WhatsApp.",
    "s5": "Posteriormente le metemos|la hidrolimpiadora,|arriba y abajo,|para quitar todas|las llamadas perdidas.",
    "s6": "Ahora toca tallar|con agua y jabón|los mensajes sin contestar.",
    "s7": "Le pregunté al dueño,|y me dijo: sí, es verdad.|Esta semana perdí|tres instalaciones.",
    "s8": "Armamos de nuevo,|y le ponemos la pieza nueva:|una recepcionista|con inteligencia artificial.",
    "s9": "Coge las llamadas,|contesta los WhatsApps,|te apunta la cita,|y te avisa a ti.",
    "s10": "Ya no grabé lo demás|porque se me hacía tarde,|jajaja.|Pero este es el proceso.",
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
    pos = 0; starts = []
    for c in chunks:
        starts.append((t[pos], c)); pos += len(c.split())
    for ci, (s, c) in enumerate(starts):
        e = (starts[ci + 1][0] if ci + 1 < len(starts) else Ls["end"] + 0.3) - 0.03
        SUB.append({"s": round(max(0, s - 0.05), 2), "e": round(e, 2), "txt": c, "sc": sc})
SUB[0]["s"] = 0.0
for a_, b_ in zip(SUB, SUB[1:]):
    if b_["s"] <= a_["s"] + 0.3: b_["s"] = round(a_["s"] + 0.6, 2)
    a_["e"] = min(a_["e"], round(b_["s"] - 0.02, 2))
def cap_html():
    out = []
    for i, c in enumerate(SUB):
        d = round(max(0.25, c["e"] - c["s"]), 3)
        cls = "cap alto" if c["sc"] in ("s1", "s2", "s4", "s8", "s9") else "cap"
        out.append(f'      <div id="c{i}" class="{cls} clip" data-start="{c["s"]:.3f}" data-duration="{d}" data-track-index="20">{html.escape(c["txt"])}</div>')
    return "\n".join(out)

# ---------- tiempos clave ----------
t_47 = t_de("47", B["s2"]); t_buzon = t_de("buzon", B["s4"]); t_luego = t_de("luego", B["s4"])
t_arriba = t_de("arriba", B["s5"]); t_quitar = t_de("quitar", B["s5"])
t_tallar = t_de("tallar", B["s6"]); t_mens = t_de("mensajes", B["s6"])
t_pieza = t_de("pieza", B["s8"]); t_recep = t_de("recepcionista", B["s8"])
t_coge = t_de("coge", B["s9"]); t_cont = t_de("contesta", B["s9"]); t_apunta = t_de("apunta", B["s9"]); t_avisa = t_de("avisa", B["s9"])
t_comenta = t_de("comenta", B["s11"]); t_rec2 = t_de("recepcion", B["s11"])
t_soldar = round(B["s3"] + dur("s3") * 0.5, 2)
t_esponja = round(B["s6"] + 1.5, 2)

css = """
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #111; }
      #root { width: 100%; height: 100%; position: relative; font-family: "Inter"; color: #fff; }
      .escena { position: absolute; inset: 0; overflow: hidden; background: #111; }
      .vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .borroso { filter: blur(10px) brightness(0.6); transform: scale(1.08); }
      .velo { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.0) 50%, rgba(0,0,0,0.35) 100%); }
      /* subtítulos estilo CapCut: blanco, borde negro */
      .cap { position: absolute; left: 70px; right: 70px; top: 1250px; text-align: center; font-weight: 800; font-size: 66px; line-height: 1.15;
             color: #fff; -webkit-text-stroke: 12px #000; paint-order: stroke fill; text-shadow: 0 4px 12px rgba(0,0,0,0.5); }
      .cap.alto { top: 1560px; }
      /* móvil */
      .movil { position: absolute; left: 230px; top: 170px; width: 620px; height: 1300px; border-radius: 74px; background: #0b0b0c; padding: 20px;
               box-shadow: 0 50px 120px rgba(0,0,0,0.75), 0 0 0 5px #3a3a3c; }
      .pant { position: relative; width: 100%; height: 100%; border-radius: 56px; overflow: hidden; }
      .isla { position: absolute; left: 50%; top: 22px; width: 170px; height: 46px; margin-left: -85px; border-radius: 24px; background: #000; z-index: 5; }
      .bloq { background: linear-gradient(160deg, #3b4a6b, #1c2333 60%, #111522); }
      .hora { position: absolute; left: 0; right: 0; top: 120px; text-align: center; font-size: 150px; font-weight: 300; letter-spacing: -4px; }
      .notis { position: absolute; left: 22px; right: 22px; top: 340px; }
      .noti { display: flex; gap: 18px; align-items: center; padding: 20px 22px; margin-bottom: 14px; border-radius: 30px; background: rgba(245,245,247,0.82); color: #111; }
      .noti .ic { width: 64px; height: 64px; flex: none; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 36px; }
      .noti b { display: block; font-size: 27px; } .noti span { display: block; font-size: 25px; color: #333; margin-top: 2px; }
      .tel { background: #34c759; } .wa { background: #25d366; } .buz { background: #ff3b30; }
      .badge { position: absolute; right: -36px; top: -36px; width: 150px; height: 150px; border-radius: 50%; background: #ff3b30; color: #fff; font-size: 72px; font-weight: 900;
               display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 40px rgba(255,59,48,0.6); border: 8px solid #fff; z-index: 6; }
      /* ficha técnica (pegatina) */
      #ficha { position: absolute; left: 90px; top: 1040px; width: 560px; padding: 26px 30px; background: #f4efe2; color: #1b1b1b; border-radius: 10px; transform: rotate(-4deg);
               box-shadow: 0 20px 50px rgba(0,0,0,0.6); font-family: "JetBrains Mono"; font-weight: 700; font-size: 31px; line-height: 1.45; border-top: 16px solid #e25434; }
      #ficha i { font-style: normal; color: #e25434; }
      /* whatsapp */
      .wapp { background: #0b141a; }
      .wtop { height: 150px; background: #1f2c34; display: flex; align-items: flex-end; gap: 18px; padding: 0 26px 22px; }
      .wtop .av { width: 70px; height: 70px; border-radius: 50%; background: #6b7c85; display: flex; align-items: center; justify-content: center; font-size: 36px; }
      .wtop b { display: block; font-size: 31px; } .wtop span { display: block; font-size: 22px; color: #8696a0; margin-top: 2px; }
      .lista .fila { display: flex; gap: 18px; align-items: center; padding: 20px 24px; border-bottom: 1px solid #1f2c34; }
      .lista .av { width: 78px; height: 78px; flex: none; border-radius: 50%; background: #45535c; display: flex; align-items: center; justify-content: center; font-size: 38px; }
      .lista .tx { flex: 1; } .lista b { display: block; font-size: 29px; } .lista span { display: block; font-size: 25px; color: #8696a0; margin-top: 4px; }
      .lista span em { font-style: normal; color: #53bdeb; }
      .lista .n { width: 46px; height: 46px; border-radius: 50%; background: #25d366; color: #0b141a; font-size: 24px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
      #buzon { position: absolute; left: 18px; right: 18px; top: 18px; padding: 22px 24px; border-radius: 28px; background: #ff3b30; color: #fff; display: flex; gap: 16px; align-items: center; z-index: 7;
               box-shadow: 0 16px 40px rgba(0,0,0,0.5); }
      #buzon b { display: block; font-size: 30px; } #buzon span { display: block; font-size: 24px; opacity: 0.9; }
      .chat { padding: 26px 22px; }
      .msg { max-width: 470px; padding: 18px 22px; border-radius: 22px; font-size: 30px; line-height: 1.28; margin-bottom: 16px; }
      .msg small { display: block; font-size: 19px; color: rgba(255,255,255,0.55); margin-top: 4px; text-align: right; }
      .cli { background: #202c33; border-top-left-radius: 6px; }
      .bot { background: #005c4b; border-top-right-radius: 6px; margin-left: auto; }
      /* notificaciones que salen volando con el agua / burbujas de jabón */
      .vuela { position: absolute; left: 110px; width: 860px; display: flex; gap: 20px; align-items: center; padding: 24px 26px; border-radius: 32px; background: rgba(245,245,247,0.9); color: #111;
               box-shadow: 0 20px 50px rgba(0,0,0,0.45); }
      .vuela .ic { width: 72px; height: 72px; flex: none; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 40px; }
      .vuela b { display: block; font-size: 32px; } .vuela span { display: block; font-size: 28px; color: #333; }
      .burbuja { position: absolute; padding: 22px 28px; border-radius: 34px; background: rgba(32,44,51,0.92); color: #fff; font-size: 36px; max-width: 640px;
                 box-shadow: 0 0 0 4px rgba(255,255,255,0.55), inset 0 0 30px rgba(255,255,255,0.18); }
      /* pieza nueva */
      .nueva { background: radial-gradient(circle at 50% 35%, #17402f, #0a1712 70%); }
      #brillo { position: absolute; left: 140px; top: 80px; width: 800px; height: 1480px; border-radius: 120px; background: radial-gradient(ellipse, rgba(61,220,132,0.55), rgba(61,220,132,0) 70%); }
      .activa { position: absolute; left: 40px; right: 40px; top: 300px; text-align: center; }
      .activa img { width: 170px; height: 170px; }
      .activa h2 { font-size: 50px; font-weight: 900; margin-top: 26px; line-height: 1.15; }
      .activa .pill { display: inline-block; margin-top: 30px; padding: 16px 34px; border-radius: 40px; background: #3ddc84; color: #06281a; font-size: 32px; font-weight: 800; }
      .activa .cero { margin-top: 70px; font-size: 30px; color: #b9e8cf; line-height: 1.6; }
      #flash { position: absolute; inset: 0; background: #fff; }
      #okcita { position: absolute; left: 30px; right: 30px; bottom: 40px; padding: 24px 26px; border-radius: 28px; background: #f4f5f6; color: #111; display: flex; gap: 20px; align-items: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.6); }
      #okcita .ic { width: 78px; height: 78px; flex: none; border-radius: 20px; background: #3ddc84; display: flex; align-items: center; justify-content: center; font-size: 44px; }
      #okcita b { display: block; font-size: 30px; } #okcita span { display: block; font-size: 26px; color: #333; margin-top: 2px; }
      #llamada { position: absolute; left: 30px; right: 30px; top: 175px; padding: 20px 24px; border-radius: 28px; background: rgba(30,30,32,0.96); display: flex; gap: 18px; align-items: center; z-index: 7; }
      #llamada .ic { width: 70px; height: 70px; border-radius: 50%; background: #34c759; display: flex; align-items: center; justify-content: center; font-size: 36px; }
      #llamada b { display: block; font-size: 28px; } #llamada span { display: block; font-size: 24px; color: #3ddc84; }
      /* CTA */
      .cta { background: #e25434; }
      #ctab { position: absolute; left: 0; right: 0; top: 560px; text-align: center; }
      #ctab .p { font-size: 70px; font-weight: 800; }
      #ctab .g { display: inline-block; margin-top: 30px; padding: 26px 50px; border-radius: 30px; background: #fff; color: #e25434; font-family: "Archivo Black"; font-size: 120px; }
      #ctab .s { margin-top: 40px; font-size: 40px; font-weight: 600; opacity: 0.95; }
      .marca { background: #111; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px; }
      .marca img { width: 220px; height: 220px; } .marca b { font-size: 84px; font-weight: 900; } .marca span { font-size: 38px; color: #ccc; }
"""

def esc(sc, inner, cls="", d=None, pista=1):
    return f'      <div id="{sc}" class="escena clip {cls}" data-start="{B[sc]:.3f}" data-duration="{d or dur(sc)}" data-track-index="{pista}">\n{inner}\n      </div>'

def vid(id_, src, start, d, ms=0, cls=""):
    return f'        <video id="{id_}" class="clip vid {cls}" src="assets/{src}.mp4" data-start="{start:.3f}" data-duration="{d:.3f}" data-media-start="{ms}" muted playsinline data-track-index="2"></video>'

VELO = '        <div class="velo"></div>'

def movil(id_, clase, cuerpo, extra=""):
    return f'        <div id="{id_}" class="movil"><div class="pant {clase}"><div class="isla"></div>{cuerpo}</div>{extra}</div>'

perdidas = [("tel", "📞", "Llamada perdida", "Cliente · Alcobendas"), ("wa", "💬", "WhatsApp · 4 mensajes", "«¿Me podéis llamar? No enfría»"),
            ("tel", "📞", "Llamada perdida (3)", "Número desconocido"), ("wa", "💬", "WhatsApp · Lucía", "«Hola?? 😡»"),
            ("tel", "📞", "Llamada perdida", "Comunidad Las Lomas")]
notis = "".join(f'<div id="n{i}" class="noti"><div class="ic {k}">{e}</div><div><b>{t}</b><span>{s}</span></div></div>' for i, (k, e, t, s) in enumerate(perdidas))
s1 = (vid("v1", "banco", B["s1"], dur("s1") + dur("s2"), cls="borroso") + "\n" +
      movil("m1", "bloq", f'<div class="hora">08:47</div><div class="notis">{notis}</div>', '<div id="badge" class="badge">47</div>'))
s2 = ('        <div id="ficha">MODELO: <i>móvil de técnico</i><br />ANTIGÜEDAD: <i>3 años</i><br />LLAMADAS PERDIDAS: <i>47</i><br />ESTADO: <i>no lo coge</i></div>')
s3 = vid("v3a", "placa", B["s3"], t_soldar - B["s3"]) + "\n" + vid("v3b", "soldar", t_soldar, B["s4"] - t_soldar) + "\n" + VELO
chats = [("👷", "Instalación Tres Cantos", "<em>✓✓</em> Luego te llamo", "3"), ("🏠", "Lucía · split salón", "<em>✓✓</em> Luego te llamo", "5"),
         ("🔧", "Comunidad Las Lomas", "<em>✓✓</em> Luego te llamo", "2"), ("📞", "Marcos · Sanse", "<em>✓✓</em> Luego te llamo", "4"),
         ("🏢", "Oficina Alcobendas", "<em>✓✓</em> Luego te llamo", "7")]
lista = "".join(f'<div id="f{i}" class="fila"><div class="av">{a}</div><div class="tx"><b>{n}</b><span>{m}</span></div><div class="n">{c}</div></div>' for i, (a, n, m, c) in enumerate(chats))
s4 = (vid("v4", "banco", B["s4"], dur("s4"), ms=3, cls="borroso") + "\n" +
      movil("m4", "wapp", f'<div class="wtop"><div><b>WhatsApp</b><span>21 chats sin leer</span></div></div><div class="lista">{lista}</div>'
            '<div id="buzon"><div style="font-size:44px">📭</div><div><b>Buzón de voz lleno</b><span>No se pueden dejar más mensajes</span></div></div>'))
vuelan = [("tel", "📞", "Llamada perdida", "Cliente · Alcobendas", 330), ("tel", "📞", "Llamada perdida (3)", "Número desconocido", 520),
          ("wa", "💬", "WhatsApp · 4 mensajes", "«¿Me podéis llamar?»", 710), ("tel", "📞", "Llamada perdida", "Comunidad Las Lomas", 900)]
s5 = (vid("v5", "hidro", B["s5"], dur("s5")) + "\n" + VELO + "\n" +
      "\n".join(f'        <div id="vu{i}" class="vuela" style="top:{y}px"><div class="ic {k}">{e}</div><div><b>{t}</b><span>{s}</span></div></div>' for i, (k, e, t, s, y) in enumerate(vuelan)))
burbujas = [("¿Tenéis hueco esta semana?", 120, 300), ("Hola?? 😡", 520, 520), ("¿Cuánto cuesta revisar el split?", 90, 720), ("Bueno, llamo a otro", 380, 920)]
s6 = (vid("v6a", "jabon", B["s6"], t_esponja - B["s6"]) + "\n" + vid("v6b", "esponja", t_esponja, B["s7"] - t_esponja) + "\n" + VELO + "\n" +
      "\n".join(f'        <div id="bu{i}" class="burbuja" style="left:{x}px;top:{y}px">{html.escape(t)}</div>' for i, (t, x, y) in enumerate(burbujas)))
s7 = vid("v7", "dueno", B["s7"], dur("s7")) + "\n" + VELO
s8 = ('        <div id="brillo"></div>\n' +
      movil("m8", "nueva", '<div class="activa"><img src="assets/logo.svg" alt="" /><h2>Recepcionista<br />con IA</h2><div class="pill">● Activa 24/7</div>'
            '<div class="cero">Llamadas perdidas: 0<br />WhatsApps sin contestar: 0</div></div>') +
      '\n        <div id="flash"></div>')
s9 = (vid("v9", "banco", B["s9"], dur("s9"), ms=1, cls="borroso") + "\n" +
      movil("m9", "wapp", '<div class="wtop"><div class="av">🏠</div><div><b>Lucía · split salón</b><span>Recepción de Climas Robledo</span></div></div><div class="chat">'
            '<div id="w1" class="msg cli">Hola, el split no calienta 🥶 ¿Podéis venir a mirarlo?<small>20:14</small></div>'
            '<div id="w2" class="msg bot">¡Hola Lucía! Sí 🙂 El lunes tengo hueco a las 10:00 o a las 12:30. ¿Cuál te viene mejor?<small>20:14 ✓✓</small></div>'
            '<div id="w3" class="msg cli">A las 10 👍<small>20:15</small></div></div>'
            '<div id="llamada"><div class="ic">📞</div><div><b>Llamada de Marcos · Sanse</b><span>Atendida por la recepcionista</span></div></div>'
            '<div id="okcita"><div class="ic">✓</div><div><b>Visita agendada · lunes 10:00</b><span>Lucía · el split no calienta</span></div></div>'))
s10 = vid("v10", "whatsapp", B["s10"], dur("s10")) + "\n" + VELO
s11 = ('        <div id="ctab"><div class="p">Comenta</div><div class="g">RECEPCIÓN</div><div class="s">y te monto la pieza nueva<br />en tu negocio</div></div>')
marca = ('        <img id="logo" src="assets/logo.svg" alt="" />\n        <b>norte.local</b>\n        <span>Recepcionista con IA para negocios locales</span>')

js = f"""
      const tl = gsap.timeline({{ paused: true }});
      // s1-s2: móvil lleno de avisos, zoom lento como el plano de la unidad en el suelo
      tl.fromTo("#m1", {{ scale: 0.92, rotation: -3 }}, {{ scale: 1.0, rotation: 0, duration: {dur('s1') + dur('s2'):.2f}, ease: "power1.out" }}, 0);
      for (let i = 0; i < 5; i++) tl.fromTo("#n" + i, {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, 0.15 + i * 0.5);
      tl.fromTo("#badge", {{ scale: 0 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_47 - 0.1:.2f});
      tl.fromTo("#ficha", {{ opacity: 0, y: 40, rotation: -10 }}, {{ opacity: 1, y: 0, rotation: -4, duration: 0.3, ease: "back.out(1.6)" }}, {B['s2'] + 0.05:.2f});
      // s3: desmontar
      tl.fromTo("#v3a", {{ scale: 1.08 }}, {{ scale: 1.0, duration: {t_soldar - B['s3']:.2f}, ease: "none" }}, {B['s3']});
      tl.fromTo("#v3b", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {B['s4'] - t_soldar:.2f}, ease: "none" }}, {t_soldar});
      // s4: buzón lleno y "luego te llamo"
      tl.fromTo("#m4", {{ y: 80, opacity: 0.4 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }}, {B['s4']});
      tl.fromTo("#buzon", {{ y: -140, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }}, {t_buzon - 0.1:.2f});
      for (let i = 0; i < 5; i++) tl.fromTo("#f" + i + " span", {{ color: "#8696a0" }}, {{ color: "#ffd166", duration: 0.12 }}, {t_luego:.2f} + i * 0.12);
      // s5: hidrolimpiadora: las notificaciones salen volando arriba y abajo
      tl.fromTo("#v5", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {dur('s5')}, ease: "none" }}, {B['s5']});
      for (let i = 0; i < 4; i++) {{
        tl.fromTo("#vu" + i, {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.15 }}, {B['s5'] + 0.1:.2f} + i * 0.12);
        tl.to("#vu" + i, {{ x: (i % 2 ? 1300 : -1300), rotation: (i % 2 ? 25 : -25), opacity: 0, duration: 0.45, ease: "power2.in" }}, {t_arriba - 0.2:.2f} + i * 0.45);
      }}
      // s6: agua y jabón: los mensajes sin contestar son burbujas que explotan
      for (let i = 0; i < 4; i++) {{
        tl.fromTo("#bu" + i, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {B['s6'] + 0.1:.2f} + i * 0.15);
        tl.to("#bu" + i, {{ scale: 1.35, opacity: 0, duration: 0.18, ease: "power2.out" }}, {t_mens - 0.1:.2f} + i * 0.3);
      }}
      // s7: el dueño
      tl.fromTo("#v7", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {dur('s7')}, ease: "none" }}, {B['s7']});
      // s8: pieza nueva, destello
      tl.fromTo("#m8", {{ scale: 0.8, opacity: 0, rotation: 6 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(1.4)" }}, {B['s8']});
      tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.06 }}, {t_pieza - 0.05:.2f});
      tl.to("#flash", {{ opacity: 0, duration: 0.35 }}, {t_pieza + 0.02:.2f});
      tl.fromTo("#brillo", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.6 }}, {t_pieza:.2f});
      tl.fromTo("#m8 .pill", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {t_recep - 0.1:.2f});
      // s9: lo que hace
      tl.fromTo("#m9", {{ y: 60, opacity: 0.5 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, {B['s9']});
      tl.fromTo("#llamada", {{ y: -120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, {t_coge - 0.1:.2f});
      tl.to("#llamada", {{ opacity: 0, y: -120, duration: 0.25 }}, {t_cont - 0.15:.2f});
      tl.fromTo("#w1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {t_cont - 0.3:.2f});
      tl.fromTo("#w2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {t_cont + 0.25:.2f});
      tl.fromTo("#w3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {t_apunta - 0.25:.2f});
      tl.fromTo("#okcita", {{ opacity: 0, y: 120 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, {t_apunta + 0.35:.2f});
      // s10
      tl.fromTo("#v10", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {dur('s10')}, ease: "none" }}, {B['s10']});
      // s11: CTA
      tl.fromTo("#ctab .p", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {B['s11'] + 0.05:.2f});
      tl.fromTo("#ctab .g", {{ scale: 1.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {B['s11'] + 0.25:.2f});
      tl.fromTo("#ctab .s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {B['s11'] + 0.6:.2f});
      tl.to("#ctab .g", {{ scale: 1.1, duration: 0.15, yoyo: true, repeat: 1 }}, {t_rec2 - 0.05:.2f});
      tl.fromTo("#logo", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {B['marca']});
      document.querySelectorAll(".cap").forEach((c) => {{
        const s = parseFloat(c.dataset.start);
        tl.fromTo(c, {{ scale: 0.85 }}, {{ scale: 1, duration: 0.12, ease: "power2.out" }}, s);
      }});
      window.__timelines["main"] = tl;
      tl.seek(0);
"""

golpes = [B["s3"], t_soldar, B["s5"], B["s6"], B["s7"], t_pieza - 0.05, B["s10"], B["s11"]]
pips = [t_47 - 0.1, t_buzon - 0.1, t_coge - 0.1, t_apunta + 0.35] + [B["s1"] + 0.15 + i * 0.5 for i in range(5)]
aud = [f'      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="30"></audio>',
       f'      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{TOTAL}" data-media-start="0" data-volume="0.22" data-fade-out="1.2" data-track-index="31"></audio>']
aud += [f'      <audio id="g{i}" class="clip" src="assets/golpe.wav" data-start="{max(0, t - 0.03):.2f}" data-duration="0.4" data-volume="0.4" data-track-index="{32 + i}"></audio>' for i, t in enumerate(golpes)]
aud += [f'      <audio id="p{i}" class="clip" src="assets/{"ding" if i < 4 else "pip"}.wav" data-start="{max(0, t):.2f}" data-duration="0.35" data-volume="0.28" data-track-index="{44 + i}"></audio>' for i, t in enumerate(pips)]

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
{esc('s1', s1, d=round(dur('s1') + dur('s2'), 3))}
{esc('s2', s2, cls='', pista=3).replace('class="escena clip "', 'class="clip" style="position:absolute;inset:0"')}
{esc('s3', s3)}
{esc('s4', s4)}
{esc('s5', s5)}
{esc('s6', s6)}
{esc('s7', s7)}
{esc('s8', s8, 'nueva')}
{esc('s9', s9)}
{esc('s10', s10)}
{esc('s11', s11, 'cta')}
{esc('marca', marca, 'marca')}
{cap_html()}
{chr(10).join(aud)}
    </div>
    <script>{js}    </script>
  </body>
</html>
"""
open("index.html", "w").write(doc)
print("ok", TOTAL, B)
