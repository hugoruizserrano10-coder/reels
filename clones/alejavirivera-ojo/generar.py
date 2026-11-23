"""Genera index.html del clon de @alejavirivera ("¿Cómo puede ser LEGAL tener acceso a todo esto?", God's Eye View).
Estructura copiada: pregunta de incredulidad sobre un globo con paneles HUD → tarjeta-logo de la herramienta →
"permite que…" → "desde aquí vas a poder ver…" (vista aérea con etiquetas) → lista de cosas que ve →
"No solo eso…" (líneas amarillas tipo vuelos) → cierre con CTA. Subtítulos de 1-3 palabras, los clave en grande a dos tonos.
Uso: python3 subtitulos.py && python3 generar.py
"""
import json, html

T = json.load(open("trabajo/timing.json"))
SUB = json.load(open("trabajo/subtitulos.json"))
L = {l["scene"]: l for l in T["lines"]}
TOTAL = round(T["total"] + 0.9, 3)

# límites de escena: cada escena empieza un poco antes de su frase
def ini(sc): return round(L[sc]["start"] - 0.06, 3)
B = {"s1": 0.0, "s2": ini("s2"), "s3": ini("s3"), "s4": ini("s4"), "s5": ini("s5"), "s6": ini("s6"),
     "s7": ini("s7"), "s8": ini("s8"), "s9": ini("s9")}
FIN_CTA = round(L["s9"]["end"] + 0.15, 3)
orden = list(B) + ["marca"]
B["marca"] = FIN_CTA
def dur(sc):
    i = orden.index(sc)
    return round((B[orden[i + 1]] if i + 1 < len(orden) else TOTAL) - B[sc], 3)

paneles = [("LLAMADAS HOY", "37", 50, 150, -14), ("WHATSAPP", "24/7", 730, 150, 12), ("CITAS HOY", "+12", 60, 390, -10),
           ("RESPUESTA", "4 s", 720, 390, 10), ("SIN LEER", "0", 60, 1330, -8), ("RECORDATORIOS", "18", 720, 1330, 8),
           ("ALCOBENDAS", "ACTIVO", 210, 1570, -6), ("TRES CANTOS", "ACTIVO", 570, 1570, 6)]
def panel(i, t, v, x, y, r):
    barras = "".join(f'<i style="height:{h}px"></i>' for h in [(17 * (i + 3) * (k + 2)) % 46 + 8 for k in range(9)])
    return (f'<div id="p{i}" class="panel" style="left:{x}px;top:{y}px;--r:{r}deg"><b>{t}</b><em>{v}</em>'
            f'<div class="barras">{barras}</div></div>')

pins = [("Alcobendas", 560, 650, "MSG-2104 · 21:47"), ("San Sebastián de los Reyes", 90, 440, "MSG-2105 · 21:52"),
        ("Tres Cantos", 140, 1440, "MSG-2106 · 22:10"), ("Algete", 640, 960, "MSG-2107 · 22:31"), ("Colmenar Viejo", 560, 1620, "MSG-2108 · 23:04")]
etiquetas = [(x, y) for x, y in [(120, 300), (800, 290), (130, 800), (860, 820), (300, 1000), (60, 1640), (820, 1400), (400, 1750), (430, 560), (60, 1050)]]
pings = [(150, 420), (860, 520), (480, 760), (260, 1040), (720, 1180), (520, 1460), (880, 1520), (180, 1360), (640, 360), (380, 600)]

def cap_html():
    out = []
    for i, c in enumerate(SUB):
        nxt = SUB[i + 1]["s"] if i + 1 < len(SUB) and SUB[i + 1]["scene"] == c["scene"] else c["e"]
        d = round(max(0.12, nxt - c["s"]), 3)
        if c["big"]:
            w = c["txt"].split()
            if len(w) >= 2:
                a, b = " ".join(w[:-1]), w[-1]
                inner = f'<span class="g1">{html.escape(a)}</span><span class="g2">{html.escape(b)}</span>'
            else:
                inner = f'<span class="g1">{html.escape(c["txt"])}</span>'
            cls = "cap big"
        else:
            inner = html.escape(c["txt"]); cls = "cap"
        out.append(f'      <div id="c{i}" class="{cls} clip" data-start="{c["s"]:.3f}" data-duration="{d}" data-track-index="20"><div class="ci">{inner}</div></div>')
    return "\n".join(out)

css = """
      :root { --cian: #4fe3ff; --cian2: rgba(79,227,255,0.55); --naranja: #ff7a2f; --amarillo: #ffc845; --fondo: #04080d; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--fondo); }
      #root { width: 100%; height: 100%; position: relative; font-family: "Inter"; color: #fff; }
      .escena { position: absolute; inset: 0; overflow: hidden; background: var(--fondo); }
      .vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .velo { position: absolute; inset: 0; }
      .scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0 2px, transparent 2px 5px); mix-blend-mode: multiply; }
      /* s1 globo + paneles */
      #globo { position: absolute; left: 0; top: 420px; width: 1080px; height: 1080px; object-fit: cover; }
      #halo { position: absolute; left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 50%; border: 3px solid var(--cian2); box-shadow: 0 0 80px rgba(79,227,255,0.35), inset 0 0 80px rgba(79,227,255,0.25); }
      .panel { position: absolute; width: 300px; height: 190px; padding: 18px 20px; border: 2px solid var(--cian2); border-radius: 10px; background: rgba(6,30,44,0.72); box-shadow: 0 0 24px rgba(79,227,255,0.25); transform: perspective(900px) rotateY(var(--r)); }
      .panel b { display: block; font-family: "JetBrains Mono"; font-weight: 700; font-size: 22px; letter-spacing: 2px; color: var(--cian); }
      .panel em { display: block; font-style: normal; font-weight: 900; font-size: 46px; margin-top: 4px; }
      .barras { position: absolute; left: 20px; right: 20px; bottom: 14px; height: 46px; display: flex; align-items: flex-end; gap: 6px; }
      .barras i { flex: 1; background: linear-gradient(0deg, rgba(79,227,255,0.3), var(--cian)); border-radius: 2px; }
      #gancho { position: absolute; left: 70px; right: 70px; top: 640px; text-align: center; font-family: "Inter"; font-weight: 900; font-size: 96px; line-height: 1.08; letter-spacing: -2px; text-shadow: 0 6px 30px rgba(0,0,0,0.9), 0 0 4px #000; }
      #gancho .leg { font-family: "Archivo Black"; color: var(--naranja); background: linear-gradient(180deg, var(--amarillo), var(--naranja)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none; filter: drop-shadow(0 0 18px rgba(255,122,47,0.6)); font-size: 150px; display: inline-block; }
      /* s2 logo */
      #s2 { background: radial-gradient(circle at 50% 45%, #0b1f2e 0%, #050b12 60%, #020407 100%); }
      #ojo { position: absolute; left: 340px; top: 540px; width: 400px; height: 400px; }
      #nombre { position: absolute; left: 0; right: 0; top: 990px; text-align: center; font-family: "JetBrains Mono"; font-weight: 700; font-size: 58px; letter-spacing: 14px; }
      #nombre span { color: var(--cian); }
      #carga { position: absolute; left: 0; right: 0; top: 1080px; text-align: center; font-family: "JetBrains Mono"; font-size: 30px; letter-spacing: 3px; color: rgba(255,255,255,0.45); }
      /* s3/s4 ciudad */
      .ping { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; border: 4px solid var(--cian); }
      .burbuja { position: absolute; width: 74px; height: 60px; margin: -30px 0 0 -37px; border-radius: 18px 18px 18px 4px; background: #25d366; box-shadow: 0 0 20px rgba(37,211,102,0.7); }
      .burbuja::after { content: "✓✓"; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 26px; color: #fff; }
      #reloj { position: absolute; left: 60px; top: 150px; padding: 14px 26px; border: 2px solid var(--cian2); border-radius: 10px; background: rgba(6,30,44,0.75); font-family: "JetBrains Mono"; font-weight: 700; font-size: 44px; color: var(--cian); }
      #directo { position: absolute; right: 60px; top: 150px; padding: 14px 26px; border-radius: 10px; background: rgba(229,52,43,0.9); font-family: "JetBrains Mono"; font-weight: 700; font-size: 36px; }
      .etq { position: absolute; padding: 4px 10px; border: 1.5px solid var(--cian2); background: rgba(4,20,30,0.7); font-family: "JetBrains Mono"; font-size: 26px; color: var(--cian); }
      .pin { position: absolute; }
      .pin .pt { position: absolute; left: -16px; top: -16px; width: 32px; height: 32px; border-radius: 50%; background: var(--naranja); box-shadow: 0 0 0 8px rgba(255,122,47,0.3), 0 0 30px var(--naranja); }
      .pin .pn { position: absolute; left: 30px; top: -40px; white-space: nowrap; font-weight: 900; font-size: 38px; text-shadow: 0 2px 12px #000; }
      .pin .pm { position: absolute; left: 30px; top: 4px; white-space: nowrap; font-family: "JetBrains Mono"; font-size: 24px; color: var(--cian); text-shadow: 0 2px 8px #000; }
      /* s5 ficha */
      .tarjeta { position: absolute; left: 80px; right: 80px; border: 2px solid var(--cian2); border-radius: 26px; background: rgba(5,18,28,0.9); box-shadow: 0 0 60px rgba(79,227,255,0.25); padding: 44px 50px; }
      .fila { display: flex; align-items: center; gap: 28px; padding: 26px 0; border-bottom: 1px solid rgba(79,227,255,0.2); }
      .fila:last-child { border-bottom: 0; }
      .fila .k { width: 210px; flex: none; font-family: "JetBrains Mono"; font-weight: 700; font-size: 30px; letter-spacing: 2px; color: var(--cian); }
      .fila .v { font-weight: 900; font-size: 50px; line-height: 1.15; }
      .ok { color: #3ee07a; }
      /* s6 chat */
      #hora23 { position: absolute; left: 0; right: 0; top: 250px; text-align: center; font-family: "JetBrains Mono"; font-weight: 700; font-size: 150px; color: var(--cian); text-shadow: 0 0 40px rgba(79,227,255,0.6); }
      #chat { top: 560px; padding: 40px; }
      .msg { max-width: 760px; padding: 26px 32px; border-radius: 28px; font-size: 42px; line-height: 1.25; margin-bottom: 26px; }
      .cli { background: #fff; color: #111; border-bottom-left-radius: 6px; }
      .bot { margin-left: auto; background: #d9fdd3; color: #111; border-bottom-right-radius: 6px; }
      .msg small { display: block; font-size: 26px; color: #667; margin-top: 8px; text-align: right; }
      /* s7 */
      #lineas { position: absolute; inset: 0; }
      #aviso { top: 300px; display: flex; gap: 30px; align-items: center; padding: 36px 40px; border-radius: 34px; background: rgba(255,255,255,0.95); color: #111; border: 0; }
      #aviso .ic { width: 110px; height: 110px; flex: none; border-radius: 26px; background: #25d366; display: flex; align-items: center; justify-content: center; font-size: 62px; color: #fff; }
      #aviso b { display: block; font-size: 38px; }
      #aviso span { display: block; font-size: 36px; color: #333; margin-top: 6px; }
      #confirmado { position: absolute; left: 0; right: 0; top: 640px; text-align: center; }
      #confirmado div { display: inline-block; padding: 18px 44px; border-radius: 60px; background: #3ee07a; color: #052; font-weight: 900; font-size: 50px; }
      /* s9 CTA */
      #s9 { background: radial-gradient(circle at 50% 45%, #0b1f2e 0%, #050b12 65%, #020407 100%); }
      .cta { position: absolute; left: 0; right: 0; text-align: center; }
      #cta1 { top: 640px; font-weight: 900; font-size: 92px; }
      #cta2 { top: 760px; font-family: "Archivo Black"; font-size: 150px; background: linear-gradient(180deg, var(--amarillo), var(--naranja)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 22px rgba(255,122,47,0.55)); }
      #cta3 { top: 980px; font-family: "Playfair Display"; font-style: italic; font-weight: 700; font-size: 84px; }
      #cta0 { top: 330px; left: 60px; right: 60px; font-weight: 900; font-size: 76px; line-height: 1.1; } #cta0 span { color: var(--cian); }
      #marca { background: #050b12; display: flex; flex-direction: column; align-items: center; justify-content: center; }
      #marca img { width: 260px; height: 260px; }
      #marca b { font-weight: 900; font-size: 84px; margin-top: 40px; letter-spacing: -1px; }
      #marca span { font-size: 40px; margin-top: 14px; color: rgba(255,255,255,0.75); }
      /* subtítulos */
      .cap { position: absolute; left: 60px; right: 60px; top: 1180px; text-align: center; }
      .cap .ci { display: inline-block; font-weight: 900; font-size: 78px; line-height: 1.05; text-shadow: 0 4px 22px rgba(0,0,0,0.95), 0 0 3px #000; }
      .cap.big { top: 1120px; }
      .cap.big .g1 { display: block; text-shadow: none; font-family: "Archivo Black"; font-size: 104px; background: linear-gradient(180deg, var(--amarillo), var(--naranja)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 16px rgba(255,122,47,0.65)) drop-shadow(0 4px 10px rgba(0,0,0,0.9)); }
      .cap.big .g2 { display: block; font-family: "Playfair Display"; font-style: italic; font-weight: 700; font-size: 112px; margin-top: -10px; text-shadow: 0 4px 22px rgba(0,0,0,0.95), 0 0 3px #000; }
"""

def esc(sc, inner, extra="", d=None, pista=1):
    return f'      <div id="{sc}" class="escena clip" data-start="{B[sc]:.3f}" data-duration="{d or dur(sc)}" data-track-index="{pista}"{extra}>\n{inner}\n      </div>'

s1 = (f'        <video id="globo" class="clip" src="assets/globo.mp4" data-start="0" data-duration="{dur("s1")}" data-media-start="0" muted playsinline data-track-index="2"></video>\n'
      '        <div id="halo"></div>\n' + "\n".join("        " + panel(i, *p) for i, p in enumerate(paneles)) +
      '\n        <div class="scan"></div>\n'
      '        <div id="gancho">¿Cómo puede ser<br /><span class="leg">LEGAL</span><br />que cualquier negocio<br />tenga esto?</div>')
ojo = ('<svg id="ojo" viewBox="0 0 200 200"><path id="parpado" d="M10 100 Q100 20 190 100 Q100 180 10 100Z" fill="none" stroke="#4fe3ff" stroke-width="5"/>'
       '<circle cx="100" cy="100" r="46" fill="#0d3a4a" stroke="#4fe3ff" stroke-width="5"/>'
       '<path d="M84 80c3-3 7-2 9 1l5 8c2 3 1 6-1 8l-4 3c3 7 8 12 15 15l3-4c2-2 5-3 8-1l8 5c3 2 4 6 1 9l-4 4c-4 4-11 4-17 1-13-7-22-16-28-29-3-6-3-13 1-17z" fill="#ff7a2f"/>'
       '<circle cx="100" cy="100" r="62" fill="none" stroke="#4fe3ff" stroke-width="2" stroke-dasharray="6 8" id="anillo"/></svg>')
s2 = (f'        {ojo}\n        <div id="nombre">RECEPCIONISTA <span>IA</span></div>\n'
      '        <div id="carga">conectando negocios del norte de Madrid…</div>')
pings_h = "\n".join(f'        <div id="pg{i}" class="ping" style="left:{x}px;top:{y}px"></div><div id="bb{i}" class="burbuja" style="left:{x}px;top:{y}px"></div>' for i, (x, y) in enumerate(pings))
s3 = (f'        <video id="ciudad1" class="clip vid" src="assets/ciudad.mp4" data-start="{B["s3"]:.3f}" data-duration="{dur("s3")}" data-media-start="0" muted playsinline data-track-index="2"></video>\n'
      '        <div class="velo" style="background: linear-gradient(180deg, rgba(4,8,13,0.55), rgba(10,60,80,0.25) 50%, rgba(4,8,13,0.7))"></div>\n'
      f'{pings_h}\n        <div id="reloj">03:12</div>\n        <div class="scan"></div>')
etq_h = "\n".join(f'        <div id="e{i}" class="etq" style="left:{x}px;top:{y}px">MSG-{2090 + i}</div>' for i, (x, y) in enumerate(etiquetas))
pins_h = "\n".join(f'        <div id="pin{i}" class="pin" style="left:{x}px;top:{y}px"><div class="pt"></div><div class="pn">{n}</div><div class="pm">{m}</div></div>' for i, (n, x, y, m) in enumerate(pins))
s4 = (f'        <video id="ciudad2" class="clip vid" src="assets/ciudad.mp4" data-start="{B["s4"]:.3f}" data-duration="{round(dur("s4") + dur("s5") + dur("s6"), 3)}" data-media-start="{dur("s3"):.3f}" muted playsinline data-track-index="2"></video>\n'
      '        <div class="velo" style="background: linear-gradient(180deg, rgba(4,8,13,0.5), rgba(10,60,80,0.2) 50%, rgba(4,8,13,0.65))"></div>\n'
      f'{etq_h}\n{pins_h}\n        <div id="directo">● EN DIRECTO</div>\n        <div class="scan"></div>')
s5 = ('        <div class="velo" style="background: rgba(3,8,12,0.78)"></div>\n'
      '        <div id="ficha" class="tarjeta" style="top: 560px">\n'
      '          <div id="f1" class="fila"><div class="k">QUIÉN</div><div class="v">Lucía · Alcobendas</div></div>\n'
      '          <div id="f2" class="fila"><div class="k">QUÉ QUERÍA</div><div class="v">“¿Tenéis hueco el sábado?”</div></div>\n'
      '          <div id="f3" class="fila"><div class="k">CITA</div><div class="v ok">✓ Sábado, 10:00</div></div>\n'
      '        </div>')
s6 = ('        <div class="velo" style="background: rgba(3,8,12,0.82)"></div>\n        <div id="hora23">23:04</div>\n'
      '        <div id="chat" class="tarjeta">\n'
      '          <div id="m1" class="msg cli">¿Mañana me podéis mirar el coche?<small>23:04</small></div>\n'
      '          <div id="m2" class="msg bot">¡Hola! Soy el asistente automático del taller. Mañana a las 9:30, ¿te va bien?<small>23:04 ✓✓</small></div>\n'
      '        </div>')
arcos = "".join(f'<path id="a{i}" d="{d}" fill="none" stroke="#ffc845" stroke-width="4" stroke-linecap="round" opacity="0.85"/>' for i, d in enumerate([
    "M-40 1500 Q 400 900 1120 1200", "M-40 1200 Q 500 1700 1120 1000", "M 100 1950 Q 300 1000 1120 900", "M -40 900 Q 600 1500 900 1950",
    "M 300 1950 Q 700 1100 1120 1600", "M -40 1700 Q 500 1100 1120 1450", "M 600 1950 Q 200 1200 -40 1000", "M -40 1350 Q 540 800 1120 1350"]))
s7 = (f'        <video id="rotonda" class="clip vid" src="assets/rotonda.mp4" data-start="{B["s7"]:.3f}" data-duration="{dur("s7")}" data-media-start="0" muted playsinline data-track-index="2"></video>\n'
      '        <div class="velo" style="background: linear-gradient(180deg, rgba(4,8,13,0.7), rgba(4,8,13,0.2) 45%, rgba(4,8,13,0.45))"></div>\n'
      f'        <svg id="lineas" viewBox="0 0 1080 1920">{arcos}</svg>\n'
      '        <div id="aviso" class="tarjeta"><div class="ic">🔔</div><div><b>Recordatorio de tu cita</b><span>Mañana a las 9:30 en el taller. ¿Vienes?</span></div></div>\n'
      '        <div id="confirmado"><div id="conf">✓ Confirmada</div></div>')
s8 = (f'        <video id="edificio" class="clip vid" src="assets/edificio.mp4" data-start="{B["s8"]:.3f}" data-duration="{dur("s8")}" data-media-start="0" muted playsinline data-track-index="2"></video>\n'
      '        <div class="velo" style="background: linear-gradient(180deg, rgba(4,8,13,0.35), rgba(4,8,13,0.15) 40%, rgba(4,8,13,0.6))"></div>')
s9 = ('        <div id="cta0" class="cta">¿Lo quieres<br /><span>en tu negocio?</span></div>\n        <div id="cta1" class="cta">Comenta</div>\n'
      '        <div id="cta2" class="cta">RECEPCIÓN</div>\n        <div id="cta3" class="cta">y te mando la demo</div>')
marca = ('        <img id="logo" src="assets/logo.svg" alt="" />\n        <b>norte.local</b>\n'
         '        <span>Recepcionista con IA para negocios locales</span>')

W = json.load(open("trabajo/palabras.json"))
def t_de(palabra, desde):
    for w in W:
        if w["s"] >= desde - 0.3 and palabra in w["w"].lower(): return w["s"]
    raise SystemExit(f"no encuentro {palabra}")
tq = t_de("quién", B["s5"]); tqq = t_de("quería", B["s5"]); tc = t_de("cita", B["s5"])
tleer = t_de("leer", B["s6"]); t11 = t_de("11", B["s6"])
trec = t_de("recuerda", B["s7"]); tfal = t_de("falte", B["s7"])
tcom = t_de("comenta", B["s9"]); trecep = t_de("recepción", B["s9"]); tdemo = t_de("mando", B["s9"])

js = f"""
      const tl = gsap.timeline({{ paused: true }});
      // s1: globo que gira despacio y paneles que flotan
      tl.fromTo("#globo", {{ scale: 1.25 }}, {{ scale: 1.0, duration: {dur('s1')}, ease: "power1.out" }}, 0);
      tl.fromTo("#halo", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.6, ease: "power2.out" }}, 0);
      for (let i = 0; i < {len(paneles)}; i++) tl.fromTo("#p" + i, {{ opacity: 0, y: 40, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.6)" }}, 0.05 + i * 0.07);
      for (let i = 0; i < {len(paneles)}; i++) tl.to("#p" + i, {{ y: (i % 2 ? -18 : 18), duration: {dur('s1') - 0.7:.2f}, ease: "sine.inOut" }}, 0.7);
      tl.fromTo("#gancho", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power3.out" }}, 0.0);
      tl.fromTo("#gancho .leg", {{ scale: 1.4 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, 0.55);
      // s2: tarjeta-logo con ojo
      tl.fromTo("#ojo", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {B['s2'] + 0.05});
      tl.fromTo("#anillo", {{ rotation: 0, svgOrigin: "100 100" }}, {{ rotation: 120, svgOrigin: "100 100", duration: {dur('s2')}, ease: "none" }}, {B['s2']});
      tl.fromTo("#nombre", {{ opacity: 0, letterSpacing: "40px" }}, {{ opacity: 1, letterSpacing: "14px", duration: 0.6, ease: "power3.out" }}, {B['s2'] + 0.3});
      tl.fromTo("#carga", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {B['s2'] + 0.9});
      tl.to("#ojo", {{ scale: 1.08, duration: {dur('s2') - 1:.2f}, ease: "sine.inOut" }}, {B['s2'] + 0.6});
      // s3: mensajes que llegan por toda la ciudad y se contestan
      tl.fromTo("#ciudad1", {{ scale: 1.35 }}, {{ scale: 1.05, duration: {dur('s3')}, ease: "power1.out" }}, {B['s3']});
      for (let i = 0; i < {len(pings)}; i++) {{
        const t0 = {B['s3'] + 0.35} + i * 0.42;
        tl.fromTo("#pg" + i, {{ scale: 0.2, opacity: 1 }}, {{ scale: 1.8, opacity: 0, duration: 0.7, ease: "power2.out" }}, t0);
        tl.fromTo("#bb" + i, {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }}, t0 + 0.12);
      }}
      const reloj = {{ m: 3 * 60 + 12 }};
      tl.to(reloj, {{ m: 23 * 60 + 58, duration: {dur('s3') - 0.4:.2f}, ease: "power1.in", onUpdate: () => {{
        const m = Math.round(reloj.m); document.querySelector("#reloj").textContent = String(Math.floor(m / 60) % 24).padStart(2, "0") + ":" + String(m % 60).padStart(2, "0"); }} }}, {B['s3'] + 0.2});
      // s4: vista en directo con etiquetas y municipios
      tl.fromTo("#ciudad2", {{ scale: 1.05 }}, {{ scale: 1.3, duration: {dur('s4') + dur('s5') + dur('s6'):.2f}, ease: "none" }}, {B['s4']});
      for (let i = 0; i < {len(etiquetas)}; i++) tl.fromTo("#e" + i, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {B['s4'] + 0.1} + i * 0.08);
      for (let i = 0; i < {len(pins)}; i++) tl.fromTo("#pin" + i, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }}, {B['s4'] + 0.5} + i * 0.45);
      tl.fromTo("#directo", {{ opacity: 0.4 }}, {{ opacity: 1, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {B['s4']});
      // s5: ficha que se rellena cuando la voz lo nombra
      tl.fromTo("#ficha", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {B['s5']});
      tl.fromTo("#f1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {tq - 0.05:.2f});
      tl.fromTo("#f2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {tqq - 0.15:.2f});
      tl.fromTo("#f3", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {tc - 0.15:.2f});
      tl.fromTo("#f3 .v", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {tc - 0.1:.2f});
      // s6: conversación de las 23:04
      tl.fromTo("#hora23", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }}, {B['s6'] + 0.05});
      tl.fromTo("#chat", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {tleer - 0.2:.2f});
      tl.fromTo("#m1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tleer - 0.1:.2f});
      tl.fromTo("#m2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tleer + 0.5:.2f});
      tl.fromTo("#hora23", {{ textShadow: "0 0 40px rgba(79,227,255,0.6)" }}, {{ textShadow: "0 0 90px rgba(79,227,255,1)", duration: 0.3, yoyo: true, repeat: 1 }}, {t11 - 0.1:.2f});
      // s7: líneas amarillas (como las rutas de vuelos) y el recordatorio
      document.querySelectorAll("#lineas path").forEach((p, i) => {{ const L = p.getTotalLength(); p.style.strokeDasharray = L; tl.fromTo(p, {{ strokeDashoffset: L }}, {{ strokeDashoffset: 0, duration: 1.6, ease: "power1.inOut" }}, {B['s7'] + 0.05} + i * 0.18); }});
      tl.fromTo("#rotonda", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {dur('s7')}, ease: "none" }}, {B['s7']});
      tl.fromTo("#aviso", {{ opacity: 0, y: -120 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, {trec - 0.1:.2f});
      tl.fromTo("#conf", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {tfal - 0.35:.2f});
      // s8
      tl.fromTo("#edificio", {{ scale: 1.15 }}, {{ scale: 1.0, duration: {dur('s8')}, ease: "power1.out" }}, {B['s8']});
      // s9 CTA y marca
      tl.fromTo("#cta0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {B['s9'] + 0.1});
      tl.fromTo("#cta1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tcom - 0.1:.2f});
      tl.fromTo("#cta2", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {trecep - 0.1:.2f});
      tl.fromTo("#cta3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tdemo - 0.2:.2f});
      tl.fromTo("#logo", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {B['marca']});
      // subtítulos: golpe de escala al entrar
      document.querySelectorAll(".cap").forEach((c) => {{ tl.fromTo(c.querySelector(".ci"), {{ scale: 1.18, opacity: 0.4 }}, {{ scale: 1, opacity: 1, duration: 0.12, ease: "power3.out" }}, parseFloat(c.dataset.start)); }});
      window.__timelines["main"] = tl;
      tl.seek(0);
"""

golpes = [B[s] for s in ["s2", "s3", "s4", "s7", "s8", "s9"]]
dings = [B["s3"] + 0.47 + i * 0.42 for i in range(0, len(pings), 2)] + [tleer + 0.5, trec, tfal - 0.35]
aud = [f'      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="30"></audio>',
       f'      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{TOTAL}" data-media-start="0" data-volume="0.22" data-fade-out="1.2" data-track-index="31"></audio>']
aud += [f'      <audio id="g{i}" class="clip" src="assets/golpe.wav" data-start="{t - 0.03:.2f}" data-duration="0.4" data-volume="0.45" data-track-index="{32 + i}"></audio>' for i, t in enumerate(golpes)]
aud += [f'      <audio id="d{i}" class="clip" src="assets/ding.wav" data-start="{t:.2f}" data-duration="0.35" data-volume="0.3" data-track-index="{40 + i}"></audio>' for i, t in enumerate(dings)]

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
{esc('s1', s1)}
{esc('s2', s2)}
{esc('s3', s3)}
{esc('s4', s4, d=round(dur('s4') + dur('s5') + dur('s6'), 3))}
{esc('s5', s5, ' style="background: transparent"', pista=3)}
{esc('s6', s6, ' style="background: transparent"', pista=4)}
{esc('s7', s7)}
{esc('s8', s8)}
{esc('s9', s9)}
{esc('marca', marca)}
{cap_html()}
{chr(10).join(aud)}
    </div>
    <script>{js}    </script>
  </body>
</html>
"""
open("index.html", "w").write(doc)
print("ok", TOTAL, B)
