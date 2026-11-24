"""Genera index.html del clon de @alejavirivera «DeepSeek acaba de hacer otra LOCURA… y ha puesto patas arriba todo el
mercado» (https://www.tiktok.com/@alejavirivera/video/7708818254814383393, 52.200 vistas, 5,8x su mediana).
Estructura copiada: noticia en 0 s («X acaba de hacer otra locura») → destello de cielo → tipografía cinética verde neón
sobre fondo oscuro («y ha puesto PATAS (arriba boca abajo) todo el MERCADO» con cinta de cotizaciones y cruces verdes 3D)
→ «No solamente… ni… sino que además ahora…» → «y no hablo de X, sino de Y» → «Ya que ahora, desde aquí…» (pantallas de
la app en oscuro) → «De igual forma…» → «crear incluso…» (mapa con datos reales) → CTA con caja de búsqueda escribiéndose.
Subtítulos: línea pequeña blanca + palabra clave grande (negrita o serif cursiva), como el original.
Uso: python3 subtitulos.py && python3 generar.py
"""
import json, html

T = json.load(open("trabajo/timing.json"))
SUB = json.load(open("trabajo/subtitulos.json"))
W = json.load(open("trabajo/palabras.json"))
L = {l["scene"]: l for l in T["lines"]}
TOTAL = round(T["total"] + 1.0, 3)

def ini(sc): return round(L[sc]["start"] - 0.06, 3)
def t_de(palabra, desde):
    for w in W:
        if w["s"] >= desde - 0.3 and palabra in w["w"].lower(): return w["s"]
    raise SystemExit(f"no encuentro {palabra}")

B = {"s1": 0.0, "s2": ini("s2")}
for s in ["s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12"]: B[s] = ini(s)
B["marca"] = round(L["s12"]["end"] + 0.15, 3)
orden = list(B)
def dur(sc):
    i = orden.index(sc)
    return round((B[orden[i + 1]] if i + 1 < len(orden) else TOTAL) - B[sc], 3)

CIELO = (round(B["s2"] - 0.42, 2), 0.42)  # destello de cielo antes de la tipografía (cortes rápidos del original)

# subtítulos
SUB[0]["s"] = 0.0; SUB[0]["sg"] = 0.0
for c in SUB:
    if c["scene"] == "s11": c["e"] = round(t_de("alcov", B["s11"]) - 0.1, 2)
def cap_html():
    out = []
    for i, c in enumerate(SUB):
        d = round(max(0.15, c["e"] - c["s"]), 3)
        gr = ""
        if c["gr"]:
            cls = "gi" if c["estilo"] == "*" else "gb"
            gr = f'<div class="{cls}" data-sg="{c["sg"]}">{html.escape(c["gr"])}</div>'
        peq = f'<div class="gp">{html.escape(c["peq"])}</div>' if c["peq"] else ""
        out.append(f'      <div id="c{i}" class="cap clip" data-start="{c["s"]:.3f}" data-duration="{d}" data-track-index="20">{peq}{gr}</div>')
    return "\n".join(out)

css = """
      :root { --verde: #3ddc84; --verde2: #1fae5b; --fondo: #121417; --panel: #1b1e22; --borde: #2a2e34; --gris: #8a9099; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--fondo); }
      #root { width: 100%; height: 100%; position: relative; font-family: "Inter"; color: #fff; }
      .escena { position: absolute; inset: 0; overflow: hidden; background: var(--fondo); }
      .vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .velo { position: absolute; inset: 0; }
      /* s2 tipografía cinética */
      #s2 { background: radial-gradient(circle at 50% 50%, #1a1d21 0%, #111316 70%, #0c0d0f 100%); }
      #marcaagua { position: absolute; left: 0; right: 0; top: 520px; text-align: center; font-family: "Playfair Display"; font-style: italic; font-weight: 700; font-size: 900px; line-height: 1; color: rgba(255,255,255,0.035); }
      .cruz { position: absolute; width: 230px; height: 230px; }
      .cruz::before, .cruz::after { content: ""; position: absolute; background: linear-gradient(135deg, #5df29a, #13a04e 60%, #0b6b33); border-radius: 22px; box-shadow: 0 18px 40px rgba(0,0,0,0.6), inset 0 6px 10px rgba(255,255,255,0.25); }
      .cruz::before { left: 80px; top: 0; width: 70px; height: 230px; }
      .cruz::after { left: 0; top: 80px; width: 230px; height: 70px; }
      .gris { position: absolute; font-size: 24px; color: rgba(255,255,255,0.32); line-height: 1.35; }
      .kin { position: absolute; left: 0; right: 0; text-align: center; }
      .neon { font-family: "Playfair Display"; font-style: italic; font-weight: 700; background: linear-gradient(180deg, #8dffbb, #2fd277 55%, #149a4b); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none; filter: drop-shadow(0 0 22px rgba(61,220,132,0.55)); }
      #k1 { top: 700px; font-size: 52px; font-weight: 400; color: #d8dbe0; }
      #k2 { top: 760px; font-size: 300px; line-height: 1; }
      #k3 { top: 1060px; font-size: 150px; line-height: 1; transform: rotate(180deg); }
      #k4 { top: 760px; font-size: 48px; color: #d8dbe0; }
      #k5 { top: 810px; font-size: 250px; line-height: 1; }
      #k6 { top: 1230px; font-size: 64px; font-weight: 900; }
      #cinta { position: absolute; left: -200px; top: 1090px; width: 1600px; font-family: "JetBrains Mono"; font-size: 30px; line-height: 1.7; color: rgba(255,255,255,0.75); white-space: nowrap; }
      #cinta .up { color: #3ddc84; } #cinta .dn { color: #ff5a5a; }
      #flash { position: absolute; inset: 0; background: #fff; }
      /* app (s7-s11) */
      .app { position: absolute; left: 50px; right: 50px; top: 230px; height: 1000px; border-radius: 28px; background: var(--panel); border: 2px solid var(--borde); box-shadow: 0 40px 90px rgba(0,0,0,0.6); overflow: hidden; }
      .barra { height: 76px; display: flex; align-items: center; gap: 14px; padding: 0 28px; border-bottom: 2px solid var(--borde); }
      .barra i { width: 20px; height: 20px; border-radius: 50%; display: inline-block; }
      .barra b { margin-left: 18px; font-size: 30px; font-weight: 700; }
      .barra b span { color: var(--verde); }
      .barra em { margin-left: auto; font-style: normal; font-family: "JetBrains Mono"; font-size: 24px; color: var(--verde); padding: 6px 16px; border: 2px solid rgba(61,220,132,0.4); border-radius: 30px; }
      .lado { position: absolute; left: 0; top: 76px; bottom: 0; width: 280px; border-right: 2px solid var(--borde); padding: 30px 22px; }
      .lado div { font-size: 28px; color: var(--gris); padding: 16px 18px; border-radius: 12px; margin-bottom: 6px; }
      .lado div.on { background: #262a30; color: #fff; }
      .cuerpo { position: absolute; left: 280px; right: 0; top: 76px; bottom: 0; padding: 34px 30px; }
      .cuerpo h3 { font-size: 46px; font-weight: 900; margin-bottom: 6px; }
      .cuerpo p.sub { font-size: 26px; color: var(--gris); margin-bottom: 26px; }
      .visita { display: flex; gap: 20px; align-items: center; padding: 22px 20px; border-radius: 16px; background: #23272c; margin-bottom: 16px; border: 2px solid transparent; }
      .visita .h { width: 128px; flex: none; font-family: "JetBrains Mono"; font-weight: 700; font-size: 30px; color: var(--verde); }
      .visita b { display: block; font-size: 32px; }
      .visita span { display: block; font-size: 25px; color: var(--gris); margin-top: 4px; }
      .cols { display: flex; gap: 16px; height: 820px; }
      .col { flex: 1; background: #202328; border-radius: 16px; padding: 18px 14px; }
      .col h4 { font-size: 24px; color: var(--gris); margin-bottom: 14px; letter-spacing: 1px; }
      .tj { background: #2b3036; border-radius: 12px; padding: 14px; margin-bottom: 12px; font-size: 23px; line-height: 1.3; }
      .tj b { display: block; font-size: 25px; }
      .tj em { display: inline-block; font-style: normal; margin-top: 8px; font-size: 20px; padding: 3px 10px; border-radius: 20px; background: rgba(61,220,132,0.18); color: var(--verde); }
      #cursor { position: absolute; width: 46px; height: 46px; }
      #noti { position: absolute; left: 70px; right: 70px; top: 300px; display: flex; gap: 26px; align-items: center; padding: 30px 34px; border-radius: 34px; background: rgba(245,246,248,0.97); color: #111; box-shadow: 0 30px 80px rgba(0,0,0,0.6); }
      #noti .ic { width: 100px; height: 100px; flex: none; border-radius: 24px; background: var(--verde2); display: flex; align-items: center; justify-content: center; font-size: 56px; }
      #noti b { display: block; font-size: 36px; } #noti span { display: block; font-size: 33px; color: #333; margin-top: 6px; } #noti small { display: block; font-size: 24px; color: #777; margin-top: 4px; }
      #chat { position: absolute; left: 70px; right: 70px; top: 260px; padding: 40px 34px; border-radius: 28px; background: #0b141a; border: 2px solid var(--borde); }
      #chat .top { font-size: 30px; font-weight: 700; padding-bottom: 24px; border-bottom: 1px solid #22313a; margin-bottom: 28px; }
      #chat .top span { display: block; font-size: 22px; font-weight: 400; color: var(--gris); margin-top: 4px; }
      .msg { max-width: 720px; padding: 24px 30px; border-radius: 26px; font-size: 38px; line-height: 1.28; margin-bottom: 24px; }
      .msg small { display: block; font-size: 22px; color: rgba(255,255,255,0.55); margin-top: 8px; text-align: right; }
      .bot { background: #005c4b; border-bottom-right-radius: 6px; margin-left: auto; }
      .cli { background: #202c33; border-bottom-left-radius: 6px; }
      /* s11 mapa */
      #s11 { background: #0d0f12; }
      #mapa { position: absolute; left: 0; top: 160px; width: 1080px; height: 1300px; }
      .pin { position: absolute; }
      .pin .pt { position: absolute; left: -15px; top: -15px; width: 30px; height: 30px; border-radius: 50%; background: var(--verde); box-shadow: 0 0 0 10px rgba(61,220,132,0.25), 0 0 30px var(--verde); }
      .pin .pn { position: absolute; left: 34px; top: -36px; white-space: nowrap; font-weight: 900; font-size: 50px; text-shadow: 0 3px 14px #000; }
      .pin .pm { position: absolute; left: 34px; top: 22px; white-space: nowrap; font-family: "JetBrains Mono"; font-size: 26px; color: var(--verde); }
      .pin.chico .pn { font-size: 30px; font-weight: 700; color: #cfd3d8; top: -22px; }
      .pin.chico .pt { left: -9px; top: -9px; width: 18px; height: 18px; box-shadow: 0 0 16px var(--verde); }
      #madrid { position: absolute; left: 470px; top: 1290px; font-family: "JetBrains Mono"; font-size: 26px; color: var(--gris); }
      /* s12 CTA buscador */
      #s12 { background: #0f1012; }
      #caja { position: absolute; left: 60px; right: 60px; top: 520px; height: 120px; border-radius: 60px; border: 3px solid #3a3f46; background: #1b1d21; display: flex; align-items: center; padding: 0 40px; gap: 24px; }
      #caja .lupa { font-size: 48px; color: var(--gris); }
      #escrito { font-size: 56px; font-weight: 700; letter-spacing: 1px; }
      #barrita { width: 4px; height: 62px; background: var(--verde); }
      #post { position: absolute; left: 60px; right: 60px; top: 700px; border-radius: 30px; background: #1b1d21; border: 2px solid var(--borde); padding: 34px; }
      #post .cab { display: flex; align-items: center; gap: 22px; }
      #post .cab img { width: 96px; height: 96px; border-radius: 50%; background: #fff; padding: 12px; }
      #post .cab b { font-size: 38px; } #post .cab span { display: block; font-size: 26px; color: var(--gris); }
      #post .txt { font-size: 38px; line-height: 1.3; margin-top: 26px; }
      #post .txt span { color: var(--verde); font-weight: 900; }
      #ctab { position: absolute; left: 0; right: 0; top: 1240px; text-align: center; }
      #ctab .gp { font-size: 54px; font-weight: 700; }
      #ctab .gi { font-size: 120px; text-shadow: none; }
      #marca { background: #0f1012; display: flex; flex-direction: column; align-items: center; justify-content: center; }
      #marca img { width: 260px; height: 260px; }
      #marca b { font-weight: 900; font-size: 84px; margin-top: 40px; letter-spacing: -1px; }
      #marca span { font-size: 40px; margin-top: 14px; color: rgba(255,255,255,0.75); }
      /* subtítulos como el original: línea pequeña + palabra clave grande */
      .cap { position: absolute; left: 50px; right: 50px; top: 1330px; text-align: center; }
      .gp { font-weight: 700; font-size: 54px; line-height: 1.1; text-shadow: 0 3px 16px rgba(0,0,0,0.95), 0 0 3px #000; }
      .gb { font-weight: 900; font-size: 92px; line-height: 1.05; margin-top: 4px; text-shadow: 0 4px 20px rgba(0,0,0,0.95), 0 0 3px #000; }
      .gi { font-family: "Playfair Display"; font-style: italic; font-weight: 700; font-size: 104px; line-height: 1.05; margin-top: 0; text-shadow: 0 4px 20px rgba(0,0,0,0.95), 0 0 3px #000; }
"""

def esc(sc, inner, extra="", d=None, pista=1):
    return f'      <div id="{sc}" class="escena clip" data-start="{B[sc]:.3f}" data-duration="{d or dur(sc)}" data-track-index="{pista}"{extra}>\n{inner}\n      </div>'

def vid(id_, src, sc, d=None, ms=0):
    return f'        <video id="{id_}" class="clip vid" src="assets/{src}.mp4" data-start="{B[sc]:.3f}" data-duration="{d or dur(sc)}" data-media-start="{ms}" muted playsinline data-track-index="2"></video>'

VELO = '        <div class="velo" style="background: linear-gradient(180deg, rgba(0,0,0,0.15), rgba(0,0,0,0.05) 45%, rgba(0,0,0,0.55) 75%, rgba(0,0,0,0.35))"></div>'

s1 = vid("v1", "movil", "s1") + "\n" + VELO
cruces = [(-60, 120, 20), (840, 1580, -15), (880, 260, 35)]
s2 = ('        <div id="marcaagua">IA</div>\n' +
      "\n".join(f'        <div id="x{i}" class="cruz" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"></div>' for i, (x, y, r) in enumerate(cruces)) +
      '\n        <div class="gris" style="right:60px;top:120px;text-align:right">Recepcionista con IA<br />para negocios de reformas</div>'
      '\n        <div class="gris" style="left:60px;bottom:110px">Contesta, agenda y recuerda<br />mientras tú trabajas</div>'
      '\n        <div id="k1" class="kin">y ha puesto</div>\n        <div id="k2" class="kin neon">Patas</div>\n        <div id="k3" class="kin neon">arriba</div>'
      '\n        <div id="k4" class="kin">todo el</div>\n        <div id="k5" class="kin neon">sector</div>'
      '\n        <div id="cinta"><div>WHATSAPP 23:47 <span class="up">▲ contestado</span> · BAÑO ALCOBENDAS <span class="up">▲ visita jue 10:00</span> · COCINA TRES CANTOS <span class="up">▲ agendada</span> · LLAMADAS SIN CONTESTAR <span class="dn">▼ 0</span></div>'
      '<div>RECORDATORIOS <span class="up">▲ enviados</span> · HUMEDAD SANSE <span class="up">▲ visita lun 9:00</span> · PRESUPUESTOS PERDIDOS <span class="dn">▼ 0</span> · WHATSAPP 07:12 <span class="up">▲ contestado</span></div></div>'
      '\n        <div id="k6" class="kin">de las reformas</div>')
CIELO_H = f'      <video id="cielo" class="clip vid" src="assets/cielo.mp4" data-start="{CIELO[0]}" data-duration="{CIELO[1]}" data-media-start="0" muted playsinline data-track-index="5"></video>'
s3 = vid("v3", "obra", "s3") + "\n" + VELO
s4 = vid("v4", "ladrillo", "s4") + "\n" + VELO
s5 = vid("v5", "noche", "s5") + "\n" + VELO
s6 = vid("v6", "cocina", "s6") + "\n" + VELO

def app(cuerpo, activo, aid):
    items = ["Agenda", "Conversaciones", "Avisos", "Mapa"]
    lado = "".join(f'<div class="{"on" if x == activo else ""}">{x}</div>' for x in items)
    return (f'        <div id="{aid}" class="app"><div class="barra"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>'
            f'<b>norte<span>.</span>local · Recepción</b><em>● conectada</em></div><div class="lado">{lado}</div><div class="cuerpo">{cuerpo}</div></div>')
visitas = [("JUE 10:00", "Marta · Alcobendas", "Reforma de baño · por WhatsApp a las 23:47"),
           ("VIE 17:30", "Javier · Tres Cantos", "Cocina completa · llamó a las 14:05"),
           ("LUN 09:00", "Lucía · Sanse", "Humedad en el salón · Instagram, domingo"),
           ("LUN 12:30", "Andrés · Algete", "Cambiar ventanas · web, 21:10")]
v_html = "".join(f'<div id="vi{i}" class="visita"><div class="h">{h}</div><div><b>{n}</b><span>{d}</span></div></div>' for i, (h, n, d) in enumerate(visitas))
s7 = ('        <div class="velo" style="background: radial-gradient(circle at 50% 30%, #1f2328, #0d0f12 70%)"></div>\n' +
      app(f'<h3>Visitas agendadas</h3><p class="sub">Las ha creado la recepcionista</p>{v_html}', "Agenda", "app7") +
      '\n        <svg id="cursor" viewBox="0 0 24 24" style="left:600px;top:900px"><path d="M3 2l7 19 2.5-7.5L20 11z" fill="#fff" stroke="#000" stroke-width="1.2"/></svg>')
cols = [("NUEVOS", [("Pedro · Colmenar", "¿Hacéis tejados?", "pidiendo dirección")]),
        ("VISITA AGENDADA", [("Marta · Alcobendas", "Baño completo, plato de ducha", "jue 10:00"), ("Javier · Tres Cantos", "Cocina, quitar tabique", "vie 17:30")]),
        ("RECORDADA", [("Lucía · Sanse", "Mancha de humedad", "confirmada ✓")])]
c_html = '<div class="cols">' + "".join(f'<div class="col"><h4>{t}</h4>' + "".join(f'<div class="tj kt"><b>{n}</b>{q}<br /><em>{e}</em></div>' for n, q, e in tj) + '</div>' for t, tj in cols) + '</div>'
s8 = ('        <div class="velo" style="background: radial-gradient(circle at 50% 30%, #1f2328, #0d0f12 70%)"></div>\n' +
      app(f'<h3>Clientes</h3><p class="sub">Qué quería cada uno</p>{c_html}', "Conversaciones", "app8"))
s9 = ('        <div class="velo" style="background: radial-gradient(circle at 50% 30%, #1f2328, #0d0f12 70%)"></div>\n' +
      app(f'<h3>Visitas agendadas</h3><p class="sub">Las ha creado la recepcionista</p>{v_html.replace('id="vi', 'id="wi')}', "Avisos", "app9") +
      '\n        <div id="noti"><div class="ic">🔔</div><div><b>Nueva visita agendada</b><span>Marta · Baño · jueves 10:00</span><small>Recepción norte.local · ahora</small></div></div>')
s10 = ('        <div class="velo" style="background: radial-gradient(circle at 50% 30%, #1f2328, #0d0f12 70%)"></div>\n'
       '        <div id="chat"><div class="top">Marta · Alcobendas<span>Asistente automático de Reformas Robledo</span></div>'
       '<div id="r1" class="msg bot">Hola Marta 👋 Te recordamos la visita de mañana jueves a las 10:00 para ver el baño. ¿Nos confirmas?<small>miércoles 19:00 ✓✓</small></div>'
       '<div id="r2" class="msg cli">Sí, allí estaré. ¡Gracias!<small>19:04</small></div>'
       '<div id="r3" class="msg bot">¡Perfecto! Te esperamos 🙌<small>19:04 ✓✓</small></div></div>')
pins = [("Alcobendas", 560, 760, "12 mensajes esta semana", ""), ("Tres Cantos", 170, 520, "7 mensajes", ""), ("Sanse", 600, 560, "9 mensajes", ""),
        ("Algete", 860, 640, "", "chico"), ("Colmenar Viejo", 120, 260, "", "chico"), ("Fuencarral", 330, 1080, "", "chico")]
pins_h = "\n".join(f'        <div id="pin{i}" class="pin {k}" style="left:{x}px;top:{y + 160}px"><div class="pt"></div><div class="pn">{n}</div>' + (f'<div class="pm">{m}</div>' if m else "") + '</div>' for i, (n, x, y, m, k) in enumerate(pins))
calles = "".join(f'<path d="{d}" fill="none" stroke="#2a3038" stroke-width="{w}"/>' for d, w in [
    ("M 540 1300 L 560 900 L 600 560 L 640 120", 10), ("M 540 1300 L 420 900 L 200 540 L 120 200", 8), ("M 560 900 L 860 650 L 1080 600", 6),
    ("M 0 1000 L 420 900 L 700 950 L 1080 1050", 5), ("M 330 1240 L 420 900", 5), ("M 600 560 L 200 540", 4), ("M 600 560 L 860 650", 4)])
rios = '<path d="M 980 0 C 900 300 1000 700 900 1300" fill="none" stroke="#173246" stroke-width="18"/>'
s11 = (f'        <svg id="mapa" viewBox="0 0 1080 1300">{rios}{calles}</svg>\n{pins_h}\n        <div id="madrid">↓ Madrid</div>')
s12 = ('        <div id="caja"><div class="lupa">⌕</div><div id="escrito"></div><div id="barrita"></div></div>\n'
       '        <div id="post"><div class="cab"><img src="assets/logo.svg" alt="" /><div><b>norte.local_</b><span>Recepcionista con IA · norte de Madrid</span></div></div>'
       '<div class="txt">Comenta <span>RECEPCIÓN</span> y te mando la demo funcionando con tu negocio.</div></div>\n'
       '        <div id="ctab"><div class="gp">comenta la palabra</div><div class="gi neon" style="font-size:130px">recepción</div></div>')
marca = ('        <img id="logo" src="assets/logo.svg" alt="" />\n        <b>norte.local</b>\n'
         '        <span>Recepcionista con IA para negocios locales</span>')

# tiempos por palabra para la tipografía cinética y los detalles
tpatas = t_de("patas", B["s2"]); tarr = t_de("arriba", B["s2"]); ttodo = t_de("todo", B["s2"]); tsec = t_de("sector", B["s2"]); tref = t_de("reformas", B["s2"])
tcada = t_de("cada", B["s7"]); tavisa = t_de("avisa", B["s9"]); trec = t_de("recuerda", B["s10"]); tfal = t_de("falte", B["s10"])
talc = t_de("alcov", B["s11"]); ttres = t_de("tres", B["s11"]); tsanse = t_de("sanse", B["s11"])
tcom = t_de("comenta", B["s12"]); trecep = t_de("recepci", B["s12"])

js = f"""
      const tl = gsap.timeline({{ paused: true }});
      // s1: vídeo con zoom lento
      tl.fromTo("#v1", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {dur('s1')}, ease: "power1.out" }}, 0);
      // s2: tipografía cinética
      tl.fromTo("#cielo", {{ scale: 1.4, rotation: -8 }}, {{ scale: 1.0, rotation: 0, duration: {CIELO[1]}, ease: "power2.out" }}, {CIELO[0]});
      tl.fromTo("#k1", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {B['s2'] + 0.02});
      tl.fromTo("#k2", {{ opacity: 0, scale: 1.5, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "power3.out" }}, {tpatas - 0.06:.2f});
      tl.fromTo("#k3", {{ opacity: 0, rotation: 0 }}, {{ opacity: 1, rotation: 180, duration: 0.4, ease: "back.out(1.5)" }}, {tarr - 0.08:.2f});
      // al llegar "todo el sector", Patas/arriba suben y encogen, como en el original
      tl.to("#k1", {{ y: -380, scale: 0.6, duration: 0.35, ease: "power2.inOut" }}, {ttodo - 0.12:.2f});
      tl.to("#k2", {{ y: -420, scale: 0.42, duration: 0.35, ease: "power2.inOut" }}, {ttodo - 0.12:.2f});
      tl.to("#k3", {{ y: -500, scale: 0.55, duration: 0.35, ease: "power2.inOut" }}, {ttodo - 0.12:.2f});
      tl.fromTo("#k4", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, {ttodo + 0.2:.2f});
      tl.fromTo("#k5", {{ opacity: 0, scale: 1.5, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "power3.out" }}, {tsec - 0.06:.2f});
      tl.fromTo("#cinta", {{ opacity: 0, x: 0 }}, {{ opacity: 1, x: -500, duration: {dur('s2'):.2f}, ease: "none" }}, {tsec:.2f});
      tl.fromTo("#k6", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tref - 0.2:.2f});
      for (let i = 0; i < 3; i++) tl.fromTo("#x" + i, {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }}, {B['s2']} + 0.1 + i * 0.15);
      for (let i = 0; i < 3; i++) tl.to("#x" + i, {{ rotation: "+=25", y: (i % 2 ? -30 : 30), duration: {dur('s2') - 0.6:.2f}, ease: "sine.inOut" }}, {B['s2']} + 0.6);
      tl.fromTo("#marcaagua", {{ scale: 1.15 }}, {{ scale: 1, duration: {dur('s2')}, ease: "none" }}, {B['s2']});
      // s3-s6: vídeos con zoom
      tl.fromTo("#v3", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {dur('s3')}, ease: "none" }}, {B['s3']});
      tl.fromTo("#v4", {{ scale: 1.15 }}, {{ scale: 1.0, duration: {dur('s4')}, ease: "none" }}, {B['s4']});
      tl.fromTo("#v5", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {dur('s5')}, ease: "none" }}, {B['s5']});
      tl.fromTo("#v6", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {dur('s6')}, ease: "none" }}, {B['s6']});
      // s7: la app se inclina y entra (como el "modo creador")
      tl.fromTo("#app7", {{ opacity: 0, rotationX: 28, rotationZ: -6, y: 120, transformPerspective: 1400 }}, {{ opacity: 1, rotationX: 0, rotationZ: 0, y: 0, duration: 0.6, ease: "power3.out" }}, {B['s7']});
      for (let i = 0; i < 4; i++) tl.fromTo("#vi" + i, {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {B['s7'] + 0.5} + i * 0.22);
      tl.fromTo("#cursor", {{ x: 0, y: 0 }}, {{ x: -40, y: -380, duration: 0.6, ease: "power2.inOut" }}, {tcada - 0.5:.2f});
      tl.to("#vi0", {{ borderColor: "#3ddc84", duration: 0.2 }}, {tcada:.2f});
      // s8: tablero por estados
      tl.fromTo("#app8", {{ opacity: 0.6, scale: 0.96 }}, {{ opacity: 1, scale: 1, duration: 0.3 }}, {B['s8']});
      document.querySelectorAll("#app8 .kt").forEach((k, i) => tl.fromTo(k, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.22 }}, {B['s8'] + 0.1} + i * 0.25));
      // s9: aviso al dueño
      tl.fromTo("#noti", {{ opacity: 0, y: -160 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {tavisa - 0.15:.2f});
      // s10: recordatorio
      tl.fromTo("#chat", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {B['s10']});
      tl.fromTo("#r1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {trec - 0.1:.2f});
      tl.fromTo("#r2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tfal - 0.6:.2f});
      tl.fromTo("#r3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25 }}, {tfal + 0.2:.2f});
      // s11: mapa con pines
      tl.fromTo("#mapa", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1.0, opacity: 1, duration: 1.2, ease: "power2.out" }}, {B['s11']});
      tl.fromTo("#pin3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {B['s11'] + 0.4});
      tl.fromTo("#pin4", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {B['s11'] + 0.6});
      tl.fromTo("#pin5", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {B['s11'] + 0.8});
      tl.fromTo("#pin0", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {talc - 0.1:.2f});
      tl.fromTo("#pin1", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {ttres - 0.1:.2f});
      tl.fromTo("#pin2", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {tsanse - 0.1:.2f});
      tl.fromTo("#madrid", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {B['s11'] + 0.8});
      // s12: CTA con la caja escribiéndose (como la búsqueda de YouTube del original)
      tl.fromTo("#caja", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {B['s12']});
      tl.fromTo("#post", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {B['s12'] + 0.25});
      const pal = "RECEPCIÓN"; const ty = {{ n: 0 }};
      tl.to(ty, {{ n: pal.length, duration: 0.7, ease: "none", onUpdate: () => {{ document.querySelector("#escrito").textContent = pal.slice(0, Math.round(ty.n)); }} }}, {tcom:.2f});
      tl.fromTo("#barrita", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.25, yoyo: true, repeat: 9 }}, {B['s12']});
      tl.fromTo("#ctab", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {tcom - 0.1:.2f});
      tl.fromTo("#ctab .gi", {{ scale: 1.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {trecep - 0.08:.2f});
      tl.fromTo("#logo", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {B['marca']});
      // subtítulos: la palabra grande entra con golpe cuando se dice
      document.querySelectorAll(".cap").forEach((c) => {{
        const s = parseFloat(c.dataset.start);
        const p = c.querySelector(".gp"); if (p) tl.fromTo(p, {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.1 }}, s);
        const g = c.querySelector(".gb, .gi"); if (g) tl.fromTo(g, {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power3.out" }}, Math.max(s, parseFloat(g.dataset.sg)));
      }});
      window.__timelines["main"] = tl;
      tl.seek(0);
"""

golpes = [CIELO[0], B["s2"], B["s3"], B["s5"], B["s7"], B["s11"], B["s12"]]
dings = [tavisa - 0.15, trec - 0.1, tfal + 0.2]
aud = [f'      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="30"></audio>',
       f'      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{TOTAL}" data-media-start="0" data-volume="0.2" data-fade-out="1.2" data-track-index="31"></audio>']
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
{esc('s1', s1)}
{esc('s2', s2)}
{esc('s3', s3)}
{esc('s4', s4)}
{esc('s5', s5)}
{esc('s6', s6)}
{esc('s7', s7)}
{esc('s8', s8)}
{esc('s9', s9)}
{esc('s10', s10)}
{esc('s11', s11)}
{esc('s12', s12)}
{esc('marca', marca)}
{CIELO_H}
{cap_html()}
{chr(10).join(aud)}
    </div>
    <script>{js}    </script>
  </body>
</html>
"""
open("index.html", "w").write(doc)
print("ok", TOTAL, B, "cielo", CIELO)
