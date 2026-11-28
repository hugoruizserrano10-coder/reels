"""Clon (28-nov) del viral de @scrubdaddy «SCRUB BABY IS HERE» (6,1 M vistas, 91x su mediana):
alguien pide un producto en los comentarios → «os dijimos que estábamos trabajando en ello» → «¡Aquí está!» con el blíster
→ repaso del producto por partes (primeros planos) → «¡hemos pensado en todo!» → dónde conseguirlo → despedida.
Aquí: Paco (serie del fontanero, ep. 3, sigue en la antena) pide un invento y le presentamos «la recepcionista de bolsillo»
en blíster (la jefa en miniatura). Dibujo, guion y voz propios. Uso: python3 gen.py carpeta (con voz.json y p/ dentro)."""
import json, sys, re
BASE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/blis"
v = json.load(open(f"{BASE}/voz.json")); T = v["T"]; TR = v["trozos"]; W = v["words"]
INK = "#1d1b19"
R = "/home/claude/reels/"
s = open(R + "propios/fontanero-empanao/gen.py").read(); exec(s[s.index("def paco"):s.index("tienda = ")])
s = open(R + "propios/fontanero-empanao/gen.py").read(); exec(s[s.index("cocina = "):s.index("movil = ")])
s = open(R + "propios/telediario-antena/gen.py").read(); exec(s[s.index("def cielo"):s.index("def antena")])
s = open(R + "clones/zachking-mensaje/generar.py").read(); exec(s[s.index("def jefa"):s.index("def despacho")])

def ini(esc): return min(t["t0"] for t in TR if t["esc"] == esc)
def tw(frag, n=0, tr=None):
    hits = [w for w in W if frag.lower() in w["w"].lower() and (tr is None or w["tr"] == tr)]
    return hits[n]["t0"]
NE = 8
ST = [0] + [ini(e) - 0.22 for e in range(1, NE)] + [T]
SC = {e: (round(ST[e], 3), round(ST[e + 1], 3)) for e in range(NE)}
def clip(e, inner):
    a, b = SC[e]
    return f'<div id="s{e}" class="esc clip" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="0">{inner}</div>'

# ---------------- subtítulos (1-3 palabras, palabra activa en naranja, tercio central) ----------------
SIN_CAP = {2, 7, 11}  # «¡Aquí está!» y «¡Hemos pensado en todo!» van en grande
pages = []
for tr in TR:
    if tr["i"] in SIN_CAP: continue
    ws = [w for w in W if w["tr"] == tr["i"]]; cur = []
    for i, w in enumerate(ws):
        cur.append(w)
        largo = len(" ".join(x["w"] for x in cur)); sig = len(ws[i + 1]["w"]) + 1 if i + 1 < len(ws) else 0
        if len(cur) == 3 or largo + sig > 14 or (w["w"][-1] in ".,?:!" and (len(cur) > 1 or len(w["w"]) > 5)) or i == len(ws) - 1:
            pages.append((tr, cur)); cur = []
caps_html, caps_js = [], []
for k, (tr, p) in enumerate(pages):
    t0 = p[0]["t0"] - 0.05
    sig = pages[k + 1][1][0]["t0"] - 0.05 if k + 1 < len(pages) else T
    t1 = min(sig, p[-1]["t1"] + 0.35)
    cls = "cap paco" if tr["fx"] == "paco" else "cap"
    spans = "".join(f'<b id="c{k}w{j}">{re.sub(r"[.,:;]$", "", w["w"]).upper()}</b> ' for j, w in enumerate(p))
    caps_html.append(f'<div id="cap{k}" class="{cls} clip" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="9"><span>{spans.strip()}</span></div>')
    caps_js.append(f'tl.fromTo("#cap{k} span", {{ scale: 0.78, y: 14 }}, {{ scale: 1, y: 0, duration: 0.16, ease: "back.out(2.6)" }}, {t0:.3f});')
    for j, w in enumerate(p):
        caps_js.append(f'tl.set("#c{k}w{j}", {{ color: "#ff8a3d" }}, {w["t0"]:.3f});')
        if j: caps_js.append(f'tl.set("#c{k}w{j-1}", {{ color: "#ffffff" }}, {w["t0"]:.3f});')

# ---------------- el blíster (colores y composición del de Scrub Baby: naranja arriba, verde abajo) ----------------
AZ = "#2c3e8f"
def blister(id_):
    bul = ["Coge llamadas", "Contesta WhatsApp", "Agenda citas", "Recuerda citas · 24 h"]
    bl = "".join(f'<g id="{id_}b{i}"><rect x="232" y="{1296+i*50}" width="430" height="46" rx="10" fill="#ffd23f" opacity="0" class="hl"/>'
                 f'<text x="250" y="{1330+i*50}" font-family="Inter" font-weight="900" font-size="34" fill="{INK}">✓ {b}</text></g>' for i, b in enumerate(bul))
    return f'''<g id="{id_}">
      <g class="mano"><path d="M220 300 L860 300 Q890 300 890 330 L890 1480 Q890 1510 860 1510 L220 1510 Q190 1510 190 1480 L190 330 Q190 300 220 300 Z" fill="#f07a2a" stroke="{INK}" stroke-width="10"/>
      <path d="M190 1090 Q400 1030 600 1080 Q760 1120 890 1060 L890 1480 Q890 1510 860 1510 L220 1510 Q190 1510 190 1480 Z" fill="#8fd6a4" stroke="{INK}" stroke-width="8"/>
      <rect x="470" y="322" width="140" height="36" rx="18" fill="#f0eee6" stroke="{INK}" stroke-width="7"/></g>
      <image href="assets/logo.svg" x="228" y="330" width="46" height="46"/>
      <text x="282" y="366" font-family="Inter" font-weight="900" font-size="30" fill="#fff">norte.local</text>
      <text x="230" y="480" font-family="Archivo Black" font-size="92" fill="#ffd23f" stroke="{AZ}" stroke-width="7" paint-order="stroke" transform="rotate(-4 230 480)">Recepcionista</text>
      <text x="250" y="590" font-family="Archivo Black" font-size="94" fill="#ffd23f" stroke="{AZ}" stroke-width="7" paint-order="stroke" transform="rotate(-4 250 590)">de BOLSILLO</text>
      <text x="250" y="660" font-family="Inter" font-weight="900" font-size="36" fill="#fff" stroke="{AZ}" stroke-width="5" paint-order="stroke">Edición: manos ocupadas</text>
      <g class="mano"><path d="M330 700 L760 700 Q800 700 800 740 L800 1220 Q800 1260 760 1260 L330 1260 Q290 1260 290 1220 L290 740 Q290 700 330 700 Z" fill="#fff" opacity="0.28" stroke="#fff" stroke-width="10"/></g>
      <g transform="translate(305 640) scale(0.82)">{jefa(id_ + "j")}</g>
      <g class="mano"><path d="M330 720 Q320 900 340 1000" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity="0.7"/></g>
      <g id="{id_}badge"><circle cx="770" cy="760" r="98" fill="#6fd08c" stroke="{INK}" stroke-width="7"/>
      <text text-anchor="middle" font-family="Inter" font-weight="900" font-size="27" fill="{INK}"><tspan x="770" y="738">¡Coge el</tspan><tspan x="770" y="772">teléfono</tspan><tspan x="770" y="806">por ti!</tspan></text></g>
      <circle cx="250" cy="840" r="52" fill="#fff" stroke="{INK}" stroke-width="6"/>
      <text text-anchor="middle" font-family="Inter" font-weight="900" font-size="22" fill="{INK}"><tspan x="250" y="834">100 %</tspan><tspan x="250" y="862">SIN PACO</tspan></text>
      {bl}
    </g>'''

def encimera(id_):
    return f'''<g class="mano"><rect width="1080" height="1920" fill="#e9e3d8"/>
      <rect x="0" y="0" width="1080" height="700" fill="#d8d2c6"/>
      {''.join(f'<path d="M{x} {y} q40 -14 80 6" fill="none" stroke="#c9c1b3" stroke-width="5"/>' for x, y in ((120,900),(700,1100),(300,1500),(820,1650),(90,1750),(520,820)))}</g>'''

def escena_blister(e, extra=""):
    return f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam{e}">{encimera(e)}<g id="bw{e}">{blister(f"bl{e}")}</g>{extra}</g></svg>'''

# ---------------- escenas ----------------
def antena_paco(e, con_blister=False):
    extra = ""
    if con_blister:
        extra = f'<g id="mini{e}" transform="translate(640 600) rotate(12) scale(0.17)">{blister(f"mb{e}")}</g>'
    return f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam{e}">{cielo(f"a{e}")}<g transform="translate(0 150)">{torre}{paco_antena(f"pa{e}")}{extra}{viento.replace("VIENTO", f"vi{e}")}</g></g></svg>'''

respuesta = '''<div class="resp"><div class="av">🔧</div><div><small>Responder al comentario de <b>paco_fontanero</b></small>
      Que alguien invente algo para no perder llamadas 🙏</div></div>'''

laboratorio = f'''<svg data-layout-allow-overflow class="lienzo" viewBox="0 0 1080 1920"><g id="cam1"><g class="mano"><rect width="1080" height="1920" fill="#efe4d4"/>
      <rect x="0" y="1250" width="1080" height="670" fill="#d9cdb9"/><path d="M0 1250 L1080 1250" stroke="{INK}" stroke-width="9"/>
      <rect x="120" y="260" width="840" height="120" rx="16" fill="#e8692e" stroke="{INK}" stroke-width="9"/>
      <text x="540" y="345" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="70" fill="#fffaf2">LABORATORIO NORTE.LOCAL</text></g>
      <g transform="translate(250 450) scale(0.95)"><g id="jefa1">{jefa("jf1")}</g></g>
      <g id="caja1" class="mano"><path d="M300 1080 Q540 1010 780 1080 L800 1300 Q540 1340 280 1300 Z" fill="#7c9a7e" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
      <path d="M380 1140 Q420 1200 400 1290 M700 1130 Q660 1200 690 1290" fill="none" stroke="{INK}" stroke-width="6" opacity="0.5"/>
      <text x="540" y="1230" text-anchor="middle" font-family="Archivo Black" font-size="110" fill="#ffd23f" stroke="{INK}" stroke-width="6" paint-order="stroke">?</text></g>
      <rect x="0" y="1300" width="1080" height="620" fill="#d9cdb9"/></g></svg>'''

def circulo(e, inner):
    return f'<div class="burbuja" id="bur{e}"><svg viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">{inner}</svg></div>'

fregadero = f'''<g class="mano">{cocina}{piernas}</g>
      <g transform="translate(330 700)"><g class="mano"><rect x="-60" y="-110" width="120" height="220" rx="24" fill="{INK}"/><rect x="-47" y="-95" width="94" height="190" rx="16" fill="#6fd08c"/></g>
      <text x="0" y="20" text-anchor="middle" font-size="80">📞</text></g>
      <g id="ok3"><rect x="150" y="380" width="520" height="110" rx="22" fill="#2e9e57" stroke="{INK}" stroke-width="7"/>
      <text x="410" y="455" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="58" fill="#fff">LLAMADA COGIDA ✓</text></g>'''

escalera = f'''<g class="mano"><rect width="1080" height="1920" fill="#d7e7ea"/><rect y="1500" width="1080" height="420" fill="#b9cdd2"/><path d="M0 1500 L1080 1500" stroke="{INK}" stroke-width="9"/>
      <path d="M380 1500 L470 420 M700 1500 L610 420" stroke="#c49a3a" stroke-width="22" stroke-linecap="round"/>
      {''.join(f'<path d="M{380+(1500-y)*0.0833:.0f} {y} L{700-(1500-y)*0.0833:.0f} {y}" stroke="#c49a3a" stroke-width="16"/>' for y in range(1420, 430, -120))}
      <path d="M380 1500 L470 420 M700 1500 L610 420" stroke="{INK}" stroke-width="5" opacity="0.5"/></g>
      <g transform="translate(360 420) scale(0.8)"><g id="pacoE">{paco("pacoE", "tonta")}</g></g>
      <g id="ok4"><path d="M560 560 L960 560 Q990 560 990 590 L990 700 Q990 730 960 730 L640 730 L600 790 L610 730 L560 730 Q530 730 530 700 L530 590 Q530 560 560 560 Z" fill="#dcf8c6" stroke="{INK}" stroke-width="7"/>
      <text x="760" y="665" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="{INK}">¡Contestado! ✓✓</text></g>'''

bomberos = f'''{cielo("ab")}<g transform="translate(0 150)">{torre}{paco_antena("pab")}</g>
      <g id="esc5" class="mano"><path d="M1180 1900 L700 760 M1290 1860 L800 720" stroke="#c0392b" stroke-width="26" stroke-linecap="round"/>
      {''.join(f'<path d="M{1180-k*48:.0f} {1900-k*114:.0f} L{1290-k*49:.0f} {1860-k*114:.0f}" stroke="#c0392b" stroke-width="16"/>' for k in range(1, 11))}
      <circle cx="850" cy="760" r="44" fill="#ffd23f" stroke="{INK}" stroke-width="7"/><path d="M800 760 Q850 690 900 760 Z" fill="#c0392b" stroke="{INK}" stroke-width="7"/></g>
      <g id="ok5"><rect x="130" y="330" width="560" height="120" rx="22" fill="#fff" stroke="{INK}" stroke-width="7"/>
      <text x="410" y="410" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="58" fill="{INK}">📅 CITA AGENDADA ✓</text></g>'''

hook = '<div class="pregunta" id="preg0">¿Qué le regalas a un fontanero atrapado en una <em>antena</em>?</div>'
fin = '<div class="pregunta abajo" id="preg7">Comenta <em>RECEPCIÓN</em></div><div id="marca"><img src="assets/logo.svg" alt="" />norte.local</div>'
pegs = ''.join(f'<div class="peg" id="pg{i}">{t}</div>' for i, t in enumerate(["TE AVISA ✓", "RECUERDA LA CITA ✓", "24 H ✓"]))

E = {}
E[0] = clip(0, antena_paco(0) + respuesta + hook)
E[1] = clip(1, laboratorio + '<div class="tag">PACO, EP. 3 · EL INVENTO</div>')
E[2] = clip(2, escena_blister(2) + '<div id="grande">¡AQUÍ <em>ESTÁ!</em></div>')
E[3] = clip(3, escena_blister(3) + circulo(3, fregadero) + '<div class="intento">DEBAJO DEL FREGADERO</div>')
E[4] = clip(4, escena_blister(4) + circulo(4, escalera) + '<div class="intento">EN LA ESCALERA</div>')
E[5] = clip(5, escena_blister(5) + circulo(5, bomberos) + '<div class="intento">EN LA ANTENA 🚒</div>')
E[6] = clip(6, escena_blister(6) + '<div id="grande6">¡Hemos pensado <em>en todo!</em></div>' + pegs)
E[7] = clip(7, antena_paco(7, True) + fin)

# ---------------- tiempos clave ----------------
t_aqui = tw("Aquí", tr=2); t_bols = tw("bolsillo"); t_edic = tw("Edición")
t_coge = tw("Coge", tr=4); t_freg = tw("fregadero"); t_cont = tw("Contesta", tr=5); t_esc4 = tw("escalera", tr=5)
t_agen = tw("agenda", tr=6); t_bomb = tw("bomberos"); t_ant5 = tw("antena", tr=6)
t_pens = tw("pensado"); t_avisa = tw("avisa"); t_rec = tw("recuerda"); t_24 = tw("veinticuatro")
t_tiene = tw("tiene", tr=10); t_coment = tw("Comenta"); t_esc7 = tw("escalera", tr=12)
s = {e: SC[e][0] for e in range(NE)}

sfx = []
def fx(nombre, t, vol=0.6, dur=1.0):
    sfx.append(f'<audio id="fx{len(sfx)}" class="clip" src="assets/{nombre}" data-start="{max(0,t):.3f}" data-duration="{dur}" data-volume="{vol}" data-track-index="{12+len(sfx)}"></audio>')
for e in (1, 3, 4, 5, 7): fx("whoosh.mp3", s[e] - 0.12, 0.45, 0.6)
fx("notification.mp3", 0.9, 0.35, 0.8)
fx("riser.mp3", t_aqui - 1.9, 0.4, 1.9)
fx("impact-bass-1.mp3", t_aqui, 0.8, 1.2); fx("sparkle.mp3", t_aqui + 0.15, 0.4, 1.0)
fx("pop.mp3", t_bols, 0.5, 0.4); fx("pop.mp3", t_edic, 0.45, 0.4)
fx("ring.wav", s[3] + 0.1, 0.22, 1.2); fx("chime.mp3", t_freg, 0.45, 0.8)
fx("notification.mp3", t_cont, 0.4, 0.8); fx("boing.wav", t_esc4, 0.5, 0.6)
fx("riser.mp3", t_bomb - 1.4, 0.35, 1.4); fx("impact-bass-2.mp3", t_ant5, 0.6, 1.0)
fx("impact-bass-1.mp3", t_pens, 0.75, 1.2)
for t in (t_avisa, t_rec, t_24): fx("pop.mp3", t, 0.5, 0.4)
fx("sparkle.mp3", t_24 + 0.3, 0.35, 1.0)
fx("pop.mp3", t_coment, 0.5, 0.4); fx("boing.wav", t_esc7 + 0.2, 0.5, 0.6)

js = []
J = js.append
def punch(sel, t, sc=1.12, o="50% 45%", d=0.22):
    J(f'tl.fromTo("{sel}", {{ scale: 1 }}, {{ scale: {sc}, transformOrigin: "{o}", duration: {d}, ease: "back.out(2)" }}, {t:.3f});')
def shake(sel, t, n=5, a=12):
    J(f'tl.fromTo("{sel}", {{ x: 0 }}, {{ x: {a}, duration: 0.04, yoyo: true, repeat: {n}, ease: "none" }}, {t:.3f});')
def balanceo(sel, t0, dur):
    J(f'tl.to("{sel}", {{ rotation: 6, transformOrigin: "205px 680px", duration: 0.32, yoyo: true, repeat: {max(1, int(dur/0.32)) | 1}, ease: "sine.inOut" }}, {t0:.3f});')
# 0. Gancho: Paco ya balanceándose en la antena desde el fotograma 0
J('tl.fromTo("#cam0", { scale: 1.2, transformOrigin: "50% 28%" }, { scale: 1.06, duration: 1.8, ease: "power2.out" }, 0);')
balanceo("#pa0", 0, s[1]); J(f'tl.fromTo("#vi0", {{ x: -120 }}, {{ x: 160, duration: 1.2, repeat: 3, ease: "none" }}, 0);')
J('tl.fromTo("#preg0", { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.4)" }, 0.05);')
J('tl.fromTo("#s0 .resp", { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)" }, 0.7);')
punch("#cam0", tw("antena", tr=0) - 0.05, 1.14, "50% 30%", 0.3)
J('tl.to("#a0nubes", { x: 60, duration: 4, ease: "none" }, 0);')
# 1. Laboratorio: la jefa con la caja tapada
J(f'tl.fromTo("#cam1", {{ scale: 1.12, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.5, ease: "power2.out" }}, {s[1]:.3f});')
J(f'tl.fromTo("#s1 .tag", {{ x: -900 }}, {{ x: 0, duration: 0.3, ease: "power3.out" }}, {s[1]+0.2:.3f});')
J(f'tl.to("#jefa1", {{ y: -18, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {s[1]:.3f});')
J(f'tl.to("#caja1", {{ rotation: 2, transformOrigin: "540px 1200px", duration: 0.08, yoyo: true, repeat: 13 }}, {s[2]-1.2:.3f});')
# 2. ¡Aquí está! (segundo gancho): el blíster cae sobre la encimera
J(f'tl.fromTo("#bw2", {{ y: -1500, rotation: -10, transformOrigin: "540px 900px" }}, {{ y: 0, rotation: 0, duration: 0.32, ease: "power3.in" }}, {s[2]:.3f});')
shake("#cam2", s[2] + 0.32, 7, 16)
J(f'tl.fromTo("#grande", {{ scale: 1.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: "power4.out" }}, {t_aqui:.3f});')
J(f'tl.to("#grande", {{ opacity: 0, y: -80, duration: 0.25 }}, {t_bols - 0.6:.3f});')
punch("#cam2", t_bols - 0.05, 1.16, "50% 28%", 0.3)
J(f'tl.to("#cam2", {{ scale: 1.05, duration: 0.4 }}, {t_edic:.3f});')
J(f'tl.fromTo("#bl2badge", {{ scale: 1 }}, {{ scale: 1.15, svgOrigin: "770 760", duration: 0.2, yoyo: true, repeat: 3 }}, {t_edic + 0.3:.3f});')
# 3-5. Regla de tres: primer plano de cada línea del blíster + burbuja con la situación
for e, t_kw, t_ok, b in ((3, t_coge, t_freg, 0), (4, t_cont, t_esc4, 1), (5, t_agen, t_ant5, 2)):
    J(f'tl.fromTo("#cam{e}", {{ scale: 1.25, transformOrigin: "50% 60%" }}, {{ scale: 1.6, duration: {SC[e][1]-s[e]:.2f}, ease: "power1.inOut" }}, {s[e]:.3f});')
    J(f'tl.set("#bl{e}b{b} .hl", {{ opacity: 1 }}, {t_kw:.3f}); tl.fromTo("#bl{e}b{b}", {{ scale: 1 }}, {{ scale: 1.06, svgOrigin: "250 {1320+b*50}", duration: 0.2, ease: "back.out(3)" }}, {t_kw:.3f});')
    J(f'tl.fromTo("#bur{e}", {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(1.8)" }}, {s[e]+0.05:.3f});')
    J(f'tl.fromTo("#s{e} .intento", {{ y: -200 }}, {{ y: 0, duration: 0.3, ease: "back.out(2)" }}, {s[e]+0.15:.3f});')
    J(f'tl.fromTo("#ok{e}", {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.28, ease: "back.out(3)" }}, {t_ok:.3f});')
J(f'tl.fromTo("#piernas #pierna1", {{ rotation: 0 }}, {{ rotation: -6, transformOrigin: "600px 1175px", duration: 0.2, yoyo: true, repeat: 11 }}, {s[3]:.3f});')
J(f'tl.to("#pacoE", {{ rotation: 5, transformOrigin: "205px 660px", duration: 0.2, yoyo: true, repeat: 13, ease: "sine.inOut" }}, {s[4]:.3f});')
J(f'tl.fromTo("#esc5", {{ x: 500, y: 600 }}, {{ x: 0, y: 0, duration: 1.3, ease: "power2.out" }}, {t_bomb - 0.3:.3f});')
balanceo("#pab", s[5], SC[5][1] - s[5])
shake("#bur5", t_ant5, 5, 10)
# 6. ¡Hemos pensado en todo!
J(f'tl.fromTo("#cam6", {{ scale: 1.35, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.45, ease: "power3.out" }}, {s[6]:.3f});')
J(f'tl.fromTo("#grande6", {{ scale: 1.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: "power4.out" }}, {t_pens - 0.25:.3f});')
shake("#cam6", t_pens, 5, 12)
J(f'tl.to("#grande6", {{ opacity: 0, scale: 0.8, duration: 0.25 }}, {t_avisa - 0.3:.3f});')
for i, t in enumerate((t_avisa, t_rec, t_24)):
    J(f'tl.fromTo("#pg{i}", {{ scale: 0, rotation: {(-1)**i*25} }}, {{ scale: 1, rotation: {(-1)**i*-5}, duration: 0.3, ease: "back.out(3)" }}, {t - 0.05:.3f});')
    J(f'tl.set("#bl6b{3 if i else 2} .hl", {{ opacity: 1 }}, {t:.3f});')
# 7. Paco en la antena con su blíster (bucle con el fotograma 0)
J(f'tl.fromTo("#cam7", {{ scale: 1.3, transformOrigin: "50% 28%" }}, {{ scale: 1.2, duration: {T - s[7]:.2f}, ease: "power1.inOut" }}, {s[7]:.3f});')
balanceo("#pa7", s[7], T - s[7]); J(f'tl.fromTo("#vi7", {{ x: -120 }}, {{ x: 160, duration: 1.2, repeat: 6, ease: "none" }}, {s[7]:.3f});')
J(f'tl.fromTo("#mini7", {{ scale: 0.05 }}, {{ scale: 0.17, duration: 0.35, ease: "back.out(2)" }}, {s[7]+0.2:.3f});')
J(f'tl.fromTo("#preg7", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {t_coment:.3f});')
J(f'tl.fromTo("#marca", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {t_coment + 0.4:.3f});')
punch("#cam7", t_esc7, 1.3, "50% 30%", 0.3)
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
      svg.lienzo {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .mano {{ filter: url(#lapiz); }}
      .cap {{ position: absolute; left: 0; right: 0; top: 1115px; display: flex; justify-content: center; z-index: 5; }}
      .cap span {{ display: inline-block; background: var(--tinta); color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 76px; letter-spacing: 1px; padding: 4px 28px 12px; border-radius: 18px; transform-origin: 50% 60%; }}
      .cap.paco span {{ background: #e8692e; }}
      .cap b {{ font-weight: 700; }}
      .pregunta {{ position: absolute; top: 300px; left: 90px; right: 90px; text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 74px; line-height: 1.04; color: #fff; text-shadow: 0 6px 0 var(--tinta), 0 0 24px rgba(0,0,0,.35); -webkit-text-stroke: 3px var(--tinta); z-index: 4; }}
      .pregunta.abajo {{ top: 1290px; font-size: 96px; }}
      .pregunta em {{ font-style: normal; color: #ffb02e; }}
      .resp {{ position: absolute; top: 1290px; left: 90px; right: 90px; display: flex; gap: 20px; align-items: center; background: #fff; border: 5px solid var(--tinta); border-radius: 26px; padding: 18px 24px; font-weight: 800; font-size: 36px; line-height: 1.15; color: var(--tinta); z-index: 4; }}
      .resp small {{ display: block; font-size: 26px; font-weight: 600; color: #6b665f; margin-bottom: 4px; }}
      .resp .av {{ flex: none; width: 78px; height: 78px; border-radius: 39px; background: #e8692e; border: 4px solid var(--tinta); display: flex; align-items: center; justify-content: center; font-size: 40px; }}
      .tag {{ position: absolute; top: 420px; left: 90px; background: #ffb02e; color: var(--tinta); font-family: "Oswald"; font-weight: 700; font-size: 50px; padding: 6px 24px; border: 5px solid var(--tinta); border-radius: 12px; }}
      .intento {{ position: absolute; top: 230px; left: 0; right: 0; margin: 0 auto; width: fit-content; background: var(--tinta); color: #ffb02e; font-family: "Oswald"; font-weight: 700; font-size: 54px; padding: 2px 26px 6px; border-radius: 12px; z-index: 4; }}
      .burbuja {{ position: absolute; left: 140px; top: 280px; width: 800px; height: 800px; border-radius: 50%; overflow: hidden; border: 12px solid var(--tinta); box-shadow: 0 16px 0 rgba(0,0,0,.25); background: #fff; z-index: 3; }}
      .burbuja svg {{ width: 100%; height: 100%; }}
      #grande, #grande6 {{ position: absolute; top: 760px; left: 60px; right: 60px; text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 170px; line-height: 1.0; color: #fff; -webkit-text-stroke: 5px var(--tinta); text-shadow: 0 10px 0 var(--tinta); z-index: 4; }}
      #grande6 {{ font-size: 130px; top: 700px; }}
      #grande em, #grande6 em {{ font-style: normal; color: #ffb02e; display: inline-block; }}
      .peg {{ position: absolute; background: #2e9e57; color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 62px; padding: 6px 26px; border: 6px solid var(--tinta); border-radius: 16px; z-index: 4; }}
      #pg0 {{ top: 250px; left: 80px; }} #pg1 {{ top: 820px; right: 60px; background: #2c3e8f; }} #pg2 {{ top: 1560px; left: 120px; background: #e8692e; }}
      #marca {{ position: absolute; top: 1440px; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 18px; font-weight: 900; font-size: 60px; color: var(--tinta); z-index: 4; }}
      #marca img {{ width: 84px; height: 84px; }}
      #grano {{ position: absolute; inset: -40px; pointer-events: none; z-index: 20; opacity: 0.08; mix-blend-mode: multiply; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }}
      #vineta {{ position: absolute; inset: 0; pointer-events: none; z-index: 19; background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 60%, rgba(0,0,0,.2) 100%); }}
    </style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><defs>
      <filter id="lapiz" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="r"/><feDisplacementMap in="SourceGraphic" in2="r" scale="5"/></filter>
      <linearGradient id="gcielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fc4e8"/><stop offset="1" stop-color="#d4eef7"/></linearGradient>
    </defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
      {chr(10).join(E[e] for e in range(NE))}
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
