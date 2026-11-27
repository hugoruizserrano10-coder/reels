"""Reel "Telediario: el fontanero en la antena" (27-nov). Estructura clonada del viral de Duolingo
«the capital of italy is what??» (5,7 M vistas): plató de noticias + corte al lugar del disparate.
Guion, dibujo y voz propios, montado con GUIA_REEL.md (gancho in medias res, segundo gancho, regla de tres,
giro con golpe y pausa, final en bucle). Uso: python3 gen.py carpeta (con voz.json y p/ dentro)."""
import json, sys, re
BASE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tele"
v = json.load(open(f"{BASE}/voz.json")); T = v["T"]; TR = v["trozos"]; W = v["words"]
INK = "#1d1b19"
src_f = open("/home/claude/reels/propios/fontanero-empanao/gen.py").read()
exec(src_f[src_f.index("def paco"):src_f.index("tienda = ")])
src_l = open("/home/claude/reels/propios/panadero-loros/gen.py").read()
exec(src_l[src_l.index("def loro"):src_l.index("def panadero")])

def ini(esc): return min(t["t0"] for t in TR if t["esc"] == esc)
def tw(frag, n=0, tr=None):
    hits = [w for w in W if frag.lower() in w["w"].lower() and (tr is None or w["tr"] == tr)]
    return hits[n]["t0"]
ST = [0] + [ini(e) - 0.22 for e in range(1, 8)] + [T]
SC = {e: (round(ST[e], 3), round(ST[e + 1], 3)) for e in range(8)}
def clip(e, inner, extra=""):
    a, b = SC[e]
    return f'<div id="s{e}" class="esc clip" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="0"{extra}>{inner}</div>'

# ---------------- subtítulos: 1-3 palabras, palabra activa en naranja, tercio central ----------------
pages = []
for tr in TR:
    if tr["esc"] == 2 or tr["fx"] == "loro" or tr["i"] == 12: continue  # 12: lo cuenta el móvil de la recepcionista
    ws = [w for w in W if w["tr"] == tr["i"]]; cur = []
    for i, w in enumerate(ws):
        cur.append(w)
        largo = len(" ".join(x["w"] for x in cur)); sig = len(ws[i + 1]["w"]) + 1 if i + 1 < len(ws) else 0
        if len(cur) == 3 or largo + sig > 14 or (w["w"][-1] in ".,?:" and (len(cur) > 1 or len(w["w"]) > 5)) or i == len(ws) - 1:
            pages.append(cur); cur = []
caps_html, caps_js = [], []
for k, p in enumerate(pages):
    t0 = p[0]["t0"] - 0.05
    sig = pages[k + 1][0]["t0"] - 0.05 if k + 1 < len(pages) else T
    t1 = min(sig, p[-1]["t1"] + 0.35)
    spans = "".join(f'<b id="c{k}w{j}">{re.sub(r"[.,:;]$", "", w["w"]).upper()}</b> ' for j, w in enumerate(p))
    caps_html.append(f'<div id="cap{k}" class="cap clip" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="9"><span>{spans.strip()}</span></div>')
    caps_js.append(f'tl.fromTo("#cap{k} span", {{ scale: 0.78, y: 14 }}, {{ scale: 1, y: 0, duration: 0.16, ease: "back.out(2.6)" }}, {t0:.3f});')
    for j, w in enumerate(p):
        caps_js.append(f'tl.set("#c{k}w{j}", {{ color: "#ff8a3d" }}, {w["t0"]:.3f});')
        if j: caps_js.append(f'tl.set("#c{k}w{j-1}", {{ color: "#ffffff" }}, {w["t0"]:.3f});')

# ---------------- dibujos ----------------
def cielo(id_):
    return f'''<g class="mano"><rect width="1080" height="1920" fill="url(#gcielo)"/>
      <g id="{id_}nubes"><path d="M80 520 Q90 450 170 460 Q210 400 280 440 Q350 430 345 500 Q350 540 290 545 L120 545 Q70 545 80 520 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>
      <path d="M700 330 Q705 270 775 280 Q810 230 870 265 Q935 260 930 320 Q935 355 880 358 L730 358 Q690 355 700 330 Z" fill="#fff" stroke="{INK}" stroke-width="7"/></g>
      <path d="M0 1700 Q270 1610 540 1690 Q810 1600 1080 1680 L1080 1920 L0 1920 Z" fill="#8fbf7f" stroke="{INK}" stroke-width="8"/>
      <path d="M0 1790 Q300 1730 600 1800 Q850 1740 1080 1790 L1080 1920 L0 1920 Z" fill="#7aab6b"/></g>'''

torre = f'''<g class="mano">
      <path d="M470 760 L380 1720 M610 760 L700 1720" stroke="#c0392b" stroke-width="22" stroke-linecap="round"/>
      <path d="M470 760 L380 1720 M610 760 L700 1720" stroke="{INK}" stroke-width="5" opacity="0.5"/>
      {''.join(f'<path d="M{470-(y-760)*0.094:.0f} {y} L{610+(y-760)*0.094:.0f} {y+120} M{610+(y-760)*0.094:.0f} {y} L{470-(y-760)*0.094:.0f} {y+120}" stroke="#e5e0d6" stroke-width="10"/><path d="M{470-(y-760)*0.094:.0f} {y} L{610+(y-760)*0.094:.0f} {y}" stroke="{INK}" stroke-width="7"/>' for y in range(760, 1700, 120))}
      <rect x="440" y="700" width="200" height="70" rx="10" fill="#e5e0d6" stroke="{INK}" stroke-width="8"/>
      <path d="M540 700 L540 520" stroke="{INK}" stroke-width="10"/><circle cx="540" cy="510" r="16" fill="#c0392b" stroke="{INK}" stroke-width="6"/>
      <path d="M470 600 Q540 560 610 600 M445 560 Q540 505 635 560" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
    </g>'''

def paco_antena(id_):
    return f'''<g transform="translate(400 330) scale(0.62)"><g id="{id_}">{paco(id_ + "p", "tonta")}
      <g transform="translate(395 250) rotate(18)"><rect x="-38" y="-70" width="76" height="140" rx="16" fill="{INK}"/><rect x="-28" y="-58" width="56" height="116" rx="10" fill="#6fd08c"/></g>
      <path d="M440 120 Q470 90 500 120 M455 85 Q480 60 510 85" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g></g>'''

viento = f'''<g id="VIENTO" class="mano" opacity="0.8">
      <path d="M60 900 Q220 880 300 905 M90 960 Q200 950 260 965 M760 820 Q900 800 1020 825 M800 880 Q930 870 1000 885" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/></g>'''

def antena(e):
    return f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam{e}">{cielo(f"a{e}")}<g transform="translate(0 150)">{torre}{paco_antena(f"pa{e}")}{viento.replace("VIENTO", f"vi{e}")}
      <g id="esc{e}" opacity="0" class="mano"><g transform="translate(720 1640) rotate(-8)"><path d="M0 0 L230 -20 M0 60 L230 40" stroke="#9b6b48" stroke-width="16" stroke-linecap="round"/>{''.join(f'<path d="M{x} {-2-x*0.087:.0f} L{x} {58-x*0.087:.0f}" stroke="#9b6b48" stroke-width="12"/>' for x in (30, 90, 150, 210))}</g></g></g></g></svg>'''

def directo(txt):
    return f'''<div class="directo"><i></i>EN DIRECTO</div>
      <div class="rotulo"><div class="r1">ÚLTIMA HORA</div><div class="r2">{txt}</div></div>'''

presentadora = f'''<g class="mano">
      <path d="M330 1180 Q330 900 540 880 Q750 900 750 1180 Z" fill="#c0392b" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
      <path d="M490 890 L540 980 L590 890 Z" fill="#fffaf2" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M395 620 Q380 430 540 420 Q700 430 685 620 L700 820 Q640 840 620 760 L460 760 Q440 840 380 820 Z" fill="#3b2a20" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <ellipse cx="540" cy="660" rx="125" ry="145" fill="#f2c39b" stroke="{INK}" stroke-width="9"/>
      <path d="M420 600 Q470 500 600 520 Q650 540 665 610 Q600 560 520 575 Q460 585 420 600 Z" fill="#3b2a20" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
      <g id="ojosP"><circle cx="490" cy="650" r="12" fill="{INK}"/><circle cx="590" cy="650" r="12" fill="{INK}"/></g>
      <path d="M465 618 L512 626 M568 626 L615 618" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
      <path id="bocaP" d="M500 730 Q540 750 580 730" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
      <circle cx="470" cy="705" r="14" fill="#f29a8a" opacity="0.6"/><circle cx="610" cy="705" r="14" fill="#f29a8a" opacity="0.6"/>
    </g>'''

def plato(e, pantalla):
    return f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam{e}"><g class="mano"><rect width="1080" height="1920" fill="#1f3a6b"/>
      {''.join(f'<path d="M0 {y} L1080 {y}" stroke="#2b4d86" stroke-width="22"/>' for y in range(140, 1300, 110))}
      <circle cx="880" cy="1050" r="260" fill="none" stroke="#3a63a8" stroke-width="10"/><path d="M620 1050 L1140 1050 M880 790 L880 1310 M700 870 Q880 960 1060 870 M700 1230 Q880 1140 1060 1230" fill="none" stroke="#3a63a8" stroke-width="8"/>
      <rect x="90" y="300" width="560" height="420" rx="16" fill="#0f1d36" stroke="{INK}" stroke-width="9"/></g>
      <g id="pant{e}">{pantalla}</g>
      <g id="pres{e}" transform="translate(220 260)"><g id="presi{e}">{presentadora}</g></g>
      <g class="mano"><path d="M40 1400 L1040 1400 L1000 1560 L80 1560 Z" fill="#e8692e" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
      <path d="M40 1400 L1040 1400 L1040 1440 L40 1440 Z" fill="#f2a066" stroke="{INK}" stroke-width="7"/>
      <rect x="0" y="1560" width="1080" height="360" fill="#16294d"/></g></g></svg>'''

pant1 = f'''<g class="mano"><rect x="100" y="310" width="540" height="400" rx="10" fill="#cfe3e8"/>
      <g transform="translate(180 330) scale(0.85)">{paco("pacoT", "tonta")}</g>
      <g id="contador" opacity="0"><rect x="420" y="360" width="200" height="110" rx="16" fill="#c0392b" stroke="{INK}" stroke-width="7"/>
      <text x="520" y="440" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="74" fill="#fff">-12</text></g>
      <text x="370" y="690" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="40" fill="{INK}">PACO · FONTANERO</text></g>'''

vecino = paco("pacoV", "normal").replace("#e8692e", "#f2c230").replace("#5b7fa6", "#7c9a7e").replace("#4f6e93", "#5d7f60")
pant6 = f'''<g class="mano"><rect x="100" y="310" width="540" height="400" rx="10" fill="#f6e7c8"/>
      <circle cx="560" cy="380" r="45" fill="#ffd24a" stroke="{INK}" stroke-width="6"/>
      <g transform="translate(250 340) scale(0.52)">{vecino}</g>
      <path d="M150 600 Q370 700 590 600 L590 640 Q370 740 150 640 Z" fill="#e8692e" stroke="{INK}" stroke-width="7"/>
      <text x="420" y="470" font-family="Oswald" font-weight="700" font-size="46" fill="{INK}">z z z</text></g>'''

movilIA = f'''<div id="movilIA"><div class="mtop">Recepcionista IA <i>● en línea</i></div>
      <div class="mi" id="mi0"><s>📞</s>Llamada atendida</div>
      <div class="mi" id="mi1"><s>💬</s>WhatsApp contestado</div>
      <div class="mi" id="mi2"><s>📅</s>Cita agendada</div>
      <div class="mi24" id="mi3">24 h · 7 días</div></div>'''

frente = f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam3"><g class="mano"><rect width="1080" height="1920" fill="#e9e1d3"/>
      <g opacity="0.5" stroke="#d6cbb8" stroke-width="4">{''.join(f'<path d="M{x} 0 L{x} 1400"/>' for x in range(0,1081,120))}{''.join(f'<path d="M0 {y} L1080 {y}"/>' for y in range(0,1401,120))}</g>
      <rect x="0" y="1400" width="1080" height="520" fill="#d9cdb9"/><path d="M0 1400 L1080 1400" stroke="{INK}" stroke-width="9"/>
      <path d="M820 300 L820 520 Q820 560 780 560 L700 560" fill="none" stroke="#8a8f96" stroke-width="30"/>
      <g id="chorro" opacity="0"><path d="M690 560 Q560 600 520 760" fill="none" stroke="#5aa9e6" stroke-width="26" stroke-linecap="round"/></g></g>
      <g transform="translate(330 720) scale(1.3)"><g id="paco3">{paco("pacoF", "normal")}
        <g id="movilFrente" transform="translate(205 150)"><rect x="-46" y="-80" width="92" height="160" rx="18" fill="{INK}"/><rect x="-35" y="-66" width="70" height="132" rx="12" fill="#6fd08c"/>
        <path d="M-80 -30 L80 30 M-80 30 L80 -30" stroke="#b9b2a5" stroke-width="30" stroke-linecap="round" opacity="0.92"/></g></g></g></g></svg>'''

vater = f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="camV"><g class="mano"><rect width="1080" height="1920" fill="#d7e7ea"/>
      {''.join(f'<path d="M{x} 0 L{x} 1920" stroke="#c4d8dc" stroke-width="5"/>' for x in range(0,1081,135))}
      <rect x="0" y="1450" width="1080" height="470" fill="#b9cdd2"/><path d="M0 1450 L1080 1450" stroke="{INK}" stroke-width="9"/>
      <rect x="310" y="560" width="460" height="380" rx="30" fill="#fff" stroke="{INK}" stroke-width="10"/>
      <path d="M220 960 Q220 900 540 900 Q860 900 860 960 Q860 1180 680 1260 L700 1460 L380 1460 L400 1260 Q220 1180 220 960 Z" fill="#fff" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>
      <ellipse cx="540" cy="975" rx="270" ry="70" fill="#9fd3e8" stroke="{INK}" stroke-width="9"/></g>
      <g id="movilV" class="mano"><g transform="translate(560 940) rotate(24)"><rect x="-50" y="-100" width="100" height="170" rx="18" fill="{INK}"/><rect x="-38" y="-86" width="76" height="140" rx="12" fill="#6fd08c"/></g></g>
      <g id="burbujas" class="mano">{''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="5"/>' for x, y, r in ((470, 880, 16), (640, 860, 12), (520, 820, 10), (610, 790, 14)))}</g>
      <g class="mano"><path d="M540 975 m-270 0 a270 70 0 0 0 540 0" fill="#9fd3e8" opacity="0.85"/></g>
      <text id="glu" x="540" y="460" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="120" fill="{INK}" opacity="0">GLU GLU</text></g></svg>'''

loros = f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam4"><g class="mano"><rect width="1080" height="1920" fill="#efe4d4"/>
      <rect x="110" y="400" width="860" height="130" rx="18" fill="#e8692e" stroke="{INK}" stroke-width="9"/>
      <text x="540" y="495" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="80" fill="#fffaf2">FONTANERÍA PACO</text>
      <rect x="90" y="1150" width="900" height="120" rx="12" fill="#9b6b48" stroke="{INK}" stroke-width="9"/>
      <rect x="130" y="1270" width="820" height="420" fill="#8a5d3d" stroke="{INK}" stroke-width="9"/>
      <path d="M560 1150 L560 760 M440 760 L680 760" stroke="#6b4a33" stroke-width="22" stroke-linecap="round"/>
      <g transform="translate(220 1000) rotate(-8)"><rect x="-80" y="-150" width="160" height="290" rx="30" fill="{INK}"/><rect x="-64" y="-130" width="128" height="250" rx="20" fill="#6fd08c"/>
      <path d="M-120 -60 Q-145 0 -120 60 M120 -60 Q145 0 120 60" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" id="ondas"/></g></g>
      <g id="perd4" class="mano" opacity="0"><circle cx="300" cy="860" r="56" fill="#c0392b" stroke="{INK}" stroke-width="7"/><text id="nperd" x="300" y="884" text-anchor="middle" font-family="Inter" font-weight="900" font-size="58" fill="#fff">13</text></g>
      <g transform="translate(450 410)"><g id="loroG">{loro("loroA")}</g></g>
      <g id="bocadillo" opacity="0"><g transform="translate(500 470)"><path d="M0 0 L470 0 Q500 0 500 30 L500 170 Q500 200 470 200 L120 200 L40 270 L70 200 L0 200 Q-30 200 -30 170 L-30 30 Q-30 0 0 0 Z" fill="#fff" stroke="{INK}" stroke-width="9" class="mano"/>
      <text x="235" y="125" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="56" fill="{INK}">¡LUEGO TE LLAMO!</text></g></g></g></svg>'''

hook = '<div class="pregunta" id="preg0">¿Qué hace un fontanero en lo alto de una <em>antena</em>?</div>'
fin = '<div class="pregunta" id="preg7">Envíaselo a quien nunca coge el <em>teléfono</em></div><div id="marca"><img src="assets/logo.svg" alt="" />norte.local</div>'

E = {}
E[0] = clip(0, antena(0) + directo("FONTANERO, 3 DÍAS SUBIDO A UNA ANTENA") + hook)
E[1] = clip(1, plato(1, pant1) + '<div class="tag">EL FONTANERO MÁS EMPANAO · EP. 2</div>')
E[2] = clip(2, plato(2, pant1.replace('PACO · FONTANERO', '')) + '<div id="grande">Y lo peor… todavía <em>no había pasado</em></div>')
E[3] = clip(3, f'<div id="s3a">{frente}</div><div id="s3b" style="opacity:0">{vater}</div><div class="intento">INTENTO 1</div>')
E[4] = clip(4, loros + '<div class="intento">INTENTO 2</div>')
E[5] = clip(5, antena(5) + '<div class="intento">INTENTO 3</div><div class="pegat" id="peg1">COBERTURA ✓</div><div class="pegat rojo" id="peg2">ESCALERA ✗</div>')
E[6] = clip(6, plato(6, pant6) + movilIA + '<div class="tag">MIENTRAS TANTO, SU VECINO…</div>')
E[7] = clip(7, antena(7) + directo("SIGUE EN LA ANTENA") + fin)

# tiempos clave
t_doce = tw("doce"); t_tel1 = tw("teléfono"); t_pasado = tw("pasado")
t_cinta = tw("cinta"); t_vater = tw("váter"); t_movil2 = tw("móvil", tr=4)
t_loro1 = tw("loro"); t_luego = tw("luego"); t_cob = tw("cobertura", tr=8); t_esc = tw("escalera")
t_secreto = tw("secreto"); t_coge = tw("coge", tr=12); t_cont = tw("contesta"); t_agenda = tw("agenda"); t_24 = tw("veinticuatro")
s5, s6, s7 = SC[5][0], SC[6][0], SC[7][0]

sfx = []
def fx(nombre, t, vol=0.6, dur=1.0):
    sfx.append(f'<audio id="fx{len(sfx)}" class="clip" src="assets/{nombre}" data-start="{max(0,t):.3f}" data-duration="{dur}" data-volume="{vol}" data-track-index="{12+len(sfx)}"></audio>')
for e in range(1, 8):
    if e != 2: fx("whoosh.mp3", SC[e][0] - 0.12, 0.45, 0.6)
fx("whoosh.mp3", t_vater - 0.15, 0.45, 0.6)
fx("ring.wav", SC[1][0] + 0.6, 0.25, 1.4); fx("pop.mp3", t_doce, 0.5, 0.4)
fx("impact-bass-1.mp3", SC[2][0] + 0.05, 0.75, 1.2); fx("impact-bass-2.mp3", t_pasado, 0.55, 1.2)
fx("pop.mp3", t_cinta, 0.5, 0.4); fx("boing.wav", t_vater + 0.25, 0.6, 0.6)
fx("pop.mp3", t_loro1, 0.5, 0.4); fx("ring.wav", SC[4][0] + 0.3, 0.22, 1.4); fx("ring.wav", t_luego - 1.6, 0.22, 1.4); fx("impact-bass-1.mp3", t_luego, 0.5, 0.8)
fx("chime.mp3", t_cob, 0.5, 0.8); fx("error.mp3", t_esc + 0.3, 0.55, 0.8)
fx("riser.mp3", s6 - 2.2, 0.45, 2.3)
fx("impact-bass-2.mp3", t_secreto, 0.8, 1.2)
for t in (t_coge, t_cont, t_agenda, t_24): fx("pop.mp3", t, 0.5, 0.4)
fx("sparkle.mp3", t_24 + 0.2, 0.4, 1.0)

js = []
J = js.append
# punch-in genérico: un "golpe" de cámara 100→112 % con muelle
def punch(sel, t, s=1.12, o="50% 45%", d=0.22):
    J(f'tl.fromTo("{sel}", {{ scale: 1 }}, {{ scale: {s}, transformOrigin: "{o}", duration: {d}, ease: "back.out(2)" }}, {t:.3f});')
def shake(sel, t, n=5, a=12):
    J(f'tl.fromTo("{sel}", {{ x: 0 }}, {{ x: {a}, duration: 0.04, yoyo: true, repeat: {n}, ease: "none" }}, {t:.3f});')
# 0. Gancho: ya en movimiento desde el fotograma 0
J('tl.fromTo("#cam0", { scale: 1.18, transformOrigin: "50% 25%" }, { scale: 1.05, duration: 1.6, ease: "power2.out" }, 0);')
J('tl.to("#pa0", { rotation: 6, transformOrigin: "205px 680px", duration: 0.32, yoyo: true, repeat: 11, ease: "sine.inOut" }, 0);')
J('tl.fromTo("#vi0", { x: -120 }, { x: 160, duration: 1.2, repeat: 3, ease: "none" }, 0);')
J('tl.fromTo("#preg0", { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.4)" }, 0.05);')
J('tl.fromTo("#s0 .rotulo", { x: -1080 }, { x: 0, duration: 0.35, ease: "power3.out" }, 0.9);')
punch("#cam0", 2.3, 1.16, "50% 22%", 0.3)
J('tl.to("#a0nubes", { x: 60, duration: 4, ease: "none" }, 0);')
# 1. Plató
J(f'tl.fromTo("#cam1", {{ scale: 1.1, transformOrigin: "40% 40%" }}, {{ scale: 1, duration: 0.5, ease: "power2.out" }}, {SC[1][0]:.3f});')
J(f'tl.fromTo("#s1 .tag", {{ x: -700 }}, {{ x: 0, duration: 0.3, ease: "power3.out" }}, {SC[1][0]+0.2:.3f});')
J(f'tl.to("#bocaP", {{ attr: {{ d: "M500 725 Q540 775 580 725" }}, duration: 0.12, yoyo: true, repeat: 15 }}, {SC[1][0]+0.2:.3f});')
J(f'tl.fromTo("#contador", {{ opacity: 0, scale: 0.4, transformOrigin: "520px 415px" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }}, {t_doce:.3f});')
punch("#cam1", t_tel1 - 0.05, 1.12, "30% 35%")
# 2. Segundo gancho: congelado, desaturado, golpe
J(f'tl.fromTo("#s2 svg", {{ filter: "saturate(1)" }}, {{ filter: "saturate(0.15) brightness(0.7)", duration: 0.15 }}, {SC[2][0]:.3f});')
J(f'tl.fromTo("#grande", {{ scale: 1.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "power4.out" }}, {SC[2][0]+0.05:.3f});')
shake("#s2", SC[2][0] + 0.05, 7, 16); J(f'tl.fromTo("#grande em", {{ scale: 0.8 }}, {{ scale: 1.08, duration: 0.25, ease: "back.out(3)" }}, {t_pasado:.3f});'); shake("#s2", t_pasado, 5, 10)
# 3. Intento 1
J(f'tl.fromTo("#cam3", {{ scale: 1.15, transformOrigin: "50% 55%" }}, {{ scale: 1, duration: 0.6, ease: "power2.out" }}, {SC[3][0]:.3f});')
J(f'tl.fromTo("#s3 .intento", {{ y: -200 }}, {{ y: 0, duration: 0.3, ease: "back.out(2)" }}, {SC[3][0]+0.1:.3f});')
J(f'tl.to("#paco3", {{ rotation: 3, transformOrigin: "205px 660px", duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }}, {SC[3][0]:.3f});')
punch("#cam3", t_cinta - 0.05, 1.14, "48% 48%")
J(f'tl.set("#chorro", {{ opacity: 1 }}, {t_cinta + 0.8:.3f}); tl.fromTo("#chorro path", {{ scaleY: 0.2, transformOrigin: "690px 560px" }}, {{ scaleY: 1, duration: 0.2 }}, {t_cinta + 0.8:.3f});')
J(f'tl.set("#s3a", {{ opacity: 0 }}, {t_vater - 0.1:.3f}); tl.set("#s3b", {{ opacity: 1 }}, {t_vater - 0.1:.3f});')
J(f'tl.fromTo("#movilV", {{ y: -900, rotation: -40 }}, {{ y: 0, rotation: 0, duration: 0.35, ease: "power2.in" }}, {t_vater - 0.1:.3f});')
J(f'tl.fromTo("#movilV", {{ y: 0 }}, {{ y: 60, duration: 1.2, ease: "power1.out" }}, {t_vater + 0.25:.3f});')
J(f'tl.fromTo("#burbujas circle", {{ y: 0, opacity: 0 }}, {{ y: -140, opacity: 1, duration: 0.9, stagger: 0.15, repeat: 1 }}, {t_vater + 0.3:.3f});')
J(f'tl.fromTo("#glu", {{ opacity: 0, scale: 0.6, transformOrigin: "540px 420px" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }}, {t_vater + 0.5:.3f});')
shake("#camV", t_vater + 0.25, 5, 10)
# 4. Intento 2: el loro
J(f'tl.fromTo("#cam4", {{ scale: 1.12, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.6, ease: "power2.out" }}, {SC[4][0]:.3f});')
J(f'tl.fromTo("#s4 .intento", {{ y: -200 }}, {{ y: 0, duration: 0.3, ease: "back.out(2)" }}, {SC[4][0]+0.1:.3f});')
J(f'tl.fromTo("#loroG", {{ y: -700 }}, {{ y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {t_loro1 - 0.1:.3f});')
J(f'tl.to("#loroG", {{ rotation: -5, transformOrigin: "125px 340px", duration: 0.25, yoyo: true, repeat: 9 }}, {t_loro1 + 0.4:.3f});')
J(f'tl.to("#ondas", {{ opacity: 0.2, duration: 0.1, yoyo: true, repeat: 19 }}, {SC[4][0]+0.3:.3f});')
J(f'tl.set("#perd4", {{ opacity: 1 }}, {SC[4][0]+0.8:.3f});')
J(f'const pr = {{ n: 13 }}; tl.to(pr, {{ n: 31, duration: {t_luego - SC[4][0] - 0.8:.2f}, ease: "power1.in", onUpdate: () => {{ document.querySelector("#nperd").textContent = Math.round(pr.n); }} }}, {SC[4][0]+0.8:.3f});')
J(f'tl.fromTo("#bocadillo", {{ opacity: 0, scale: 0.4, transformOrigin: "560px 740px" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }}, {t_luego - 0.05:.3f});')
punch("#cam4", t_luego - 0.05, 1.14, "60% 35%"); shake("#cam4", t_luego, 5, 8)
# 5. Intento 3: la antena (plano abierto que revela la escalera en el suelo)
J(f'tl.fromTo("#cam5", {{ scale: 1.5, transformOrigin: "50% 28%" }}, {{ scale: 1, duration: 1.4, ease: "power2.inOut" }}, {s5:.3f});')
J(f'tl.fromTo("#s5 .intento", {{ y: -200 }}, {{ y: 0, duration: 0.3, ease: "back.out(2)" }}, {s5+0.1:.3f});')
J(f'tl.to("#pa5", {{ rotation: 6, transformOrigin: "205px 680px", duration: 0.32, yoyo: true, repeat: 17, ease: "sine.inOut" }}, {s5:.3f});')
J(f'tl.fromTo("#vi5", {{ x: -120 }}, {{ x: 160, duration: 1.2, repeat: 5, ease: "none" }}, {s5:.3f});')
J(f'tl.fromTo("#peg1", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: -6, duration: 0.3, ease: "back.out(3)" }}, {t_cob:.3f});')
J(f'tl.set("#esc5", {{ opacity: 1 }}, {s5:.3f});')
J(f'tl.fromTo("#peg2", {{ scale: 0, rotation: 20 }}, {{ scale: 1, rotation: 5, duration: 0.3, ease: "back.out(3)" }}, {t_esc:.3f});')
punch("#cam5", t_esc + 0.9, 1.25, "88% 88%", 0.3)
# 6. Giro: la recepcionista IA
J(f'tl.fromTo("#cam6", {{ scale: 1.1, transformOrigin: "40% 40%" }}, {{ scale: 1, duration: 0.5, ease: "power2.out" }}, {s6:.3f});')
J(f'tl.fromTo("#s6 .tag", {{ x: -700 }}, {{ x: 0, duration: 0.3, ease: "power3.out" }}, {s6+0.2:.3f});')
J(f'tl.to("#bocaP", {{ attr: {{ d: "M500 725 Q540 775 580 725" }}, duration: 0.12, yoyo: true, repeat: 11 }}, {s6+0.2:.3f});')
punch("#cam6", t_secreto - 0.05, 1.16, "35% 35%", 0.25); shake("#cam6", t_secreto, 5, 10)
J(f'tl.fromTo("#movilIA", {{ y: 1300, rotation: 8 }}, {{ y: 0, rotation: -3, duration: 0.45, ease: "back.out(1.4)" }}, {t_secreto + 0.55:.3f});')
J(f'tl.to("#cam6", {{ scale: 1, duration: 0.3 }}, {t_secreto + 0.55:.3f});')
for i, t in enumerate((t_coge, t_cont, t_agenda, t_24)):
    J(f'tl.fromTo("#mi{i}", {{ x: -60, opacity: 0, scale: 0.9 }}, {{ x: 0, opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.2)" }}, {t - 0.05:.3f});')
# 7. Bucle: misma antena que el fotograma 0
J(f'tl.fromTo("#cam7", {{ scale: 1.3, transformOrigin: "50% 25%" }}, {{ scale: 1.18, duration: {T - s7:.2f}, ease: "power1.inOut" }}, {s7:.3f});')
J(f'tl.to("#pa7", {{ rotation: 6, transformOrigin: "205px 680px", duration: 0.32, yoyo: true, repeat: 13, ease: "sine.inOut" }}, {s7:.3f});')
J(f'tl.fromTo("#vi7", {{ x: -120 }}, {{ x: 160, duration: 1.2, repeat: 4, ease: "none" }}, {s7:.3f});')
J(f'tl.fromTo("#preg7", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {tw("Envíaselo"):.3f});')
J(f'tl.fromTo("#marca", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {tw("Envíaselo")+0.4:.3f});')
# grano vivo
J(f'tl.to("#grano", {{ backgroundPosition: "137px 91px", duration: 0.08, repeat: {int(T/0.08)}, ease: "steps(1)" }}, 0);')

html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --tinta: {INK}; --naranja: #e8692e; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #f0eee6; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter"; }}
      .esc {{ position: absolute; inset: 0; overflow: hidden; }}
      .esc > div[id^="s3"] {{ position: absolute; inset: 0; }}
      svg.lienzo {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .mano {{ filter: url(#lapiz); }}
      .cap {{ position: absolute; left: 0; right: 0; top: 1115px; display: flex; justify-content: center; z-index: 5; }}
      .cap span {{ display: inline-block; background: var(--tinta); color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 76px; letter-spacing: 1px; padding: 4px 28px 12px; border-radius: 18px; transform-origin: 50% 60%; }}
      .cap b {{ font-weight: 700; }}
      .pregunta {{ position: absolute; top: 310px; left: 100px; right: 100px; text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 74px; line-height: 1.04; color: #fff; text-shadow: 0 6px 0 var(--tinta), 0 0 24px rgba(0,0,0,.35); -webkit-text-stroke: 3px var(--tinta); }}
      .pregunta em {{ font-style: normal; color: #ffb02e; }}
      .directo {{ position: absolute; top: 600px; left: 110px; background: #c0392b; color: #fff; font-weight: 900; font-size: 38px; padding: 8px 20px; border-radius: 8px; display: flex; align-items: center; gap: 12px; border: 4px solid var(--tinta); }}
      .directo i {{ width: 18px; height: 18px; border-radius: 9px; background: #fff; }}
      .rotulo {{ position: absolute; left: 100px; right: 100px; top: 950px; border: 6px solid var(--tinta); border-radius: 14px; overflow: hidden; }}
      .rotulo .r1 {{ background: #c0392b; color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 44px; padding: 4px 22px; }}
      .rotulo .r2 {{ background: #fffaf2; color: var(--tinta); font-family: "Oswald"; font-weight: 700; font-size: 44px; padding: 8px 22px; }}
      .tag {{ position: absolute; top: 280px; left: 100px; background: #ffb02e; color: var(--tinta); font-family: "Oswald"; font-weight: 700; font-size: 50px; padding: 6px 24px; border: 5px solid var(--tinta); border-radius: 12px; }}
      .intento {{ position: absolute; top: 310px; left: 100px; background: var(--tinta); color: #ffb02e; font-family: "Oswald"; font-weight: 700; font-size: 54px; padding: 2px 24px 6px; border-radius: 12px; }}
      .intento::before {{ content: ""; }}
      #grande {{ position: absolute; top: 520px; left: 70px; right: 70px; text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 136px; line-height: 1.02; color: #fff; -webkit-text-stroke: 4px var(--tinta); text-shadow: 0 8px 0 var(--tinta); }}
      #grande em {{ font-style: normal; color: #ffb02e; display: inline-block; }}
      .pegat {{ position: absolute; right: 150px; top: 760px; background: #2e9e57; color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 66px; padding: 6px 26px; border: 6px solid var(--tinta); border-radius: 16px; }}
      .pegat.rojo {{ background: #c0392b; top: 920px; left: 120px; right: auto; }}
      #movilIA {{ position: absolute; left: 160px; right: 200px; top: 640px; height: 760px; background: #fffaf2; border: 12px solid var(--tinta); border-radius: 64px; padding: 50px 40px; box-shadow: 0 18px 0 rgba(0,0,0,.25); z-index: 4; }}
      .mtop {{ font-weight: 900; font-size: 46px; color: var(--tinta); margin-bottom: 30px; }}
      .mtop i {{ display: block; font-style: normal; font-size: 30px; color: #2e9e57; }}
      .mi {{ display: flex; align-items: center; gap: 20px; background: #e9f5ec; border: 5px solid var(--tinta); border-radius: 26px; height: 120px; margin-bottom: 22px; padding: 0 26px; font-weight: 800; font-size: 40px; color: var(--tinta); }}
      .mi s {{ text-decoration: none; font-size: 50px; }}
      .mi24 {{ text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 70px; color: var(--naranja); }}
      #marca {{ position: absolute; top: 1270px; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 18px; font-weight: 900; font-size: 60px; color: var(--tinta); }}
      #marca img {{ width: 84px; height: 84px; }}
      #grano {{ position: absolute; inset: -40px; pointer-events: none; z-index: 20; opacity: 0.09; mix-blend-mode: multiply; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }}
      #vineta {{ position: absolute; inset: 0; pointer-events: none; z-index: 19; background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 60%, rgba(0,0,0,.22) 100%); }}
    </style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><defs>
      <filter id="lapiz" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="r"/><feDisplacementMap in="SourceGraphic" in2="r" scale="5"/></filter>
      <linearGradient id="gcielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fc4e8"/><stop offset="1" stop-color="#d4eef7"/></linearGradient>
    </defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
      {chr(10).join(E[e] for e in range(8))}
      {chr(10).join(caps_html)}
      <div id="vineta"></div><div id="grano"></div>
      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{T}" data-volume="1" data-track-index="10"></audio>
      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{T}" data-media-start="0" data-volume="0.12" data-fade-out="1" data-track-index="11"></audio>
      {chr(10).join(sfx)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in js)}
      {chr(10).join("      " + x for x in caps_js)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(f"{BASE}/p/index.html", "w").write(html)
print("ok", T, "escenas", SC, "subtítulos", len(pages), "efectos", len(sfx))
