"""Clon (27-nov) del viral de @zachking «a message to all AI» (TikTok, 68,5 M vistas, 5,7x su mediana).
Misma estructura: mensaje solemne → «me llamo X y soy Y» en silueta → plan absurdo → «mi jefe/a…» → «síguela».
Mismo estilo: escenas oscuras con contraluz, palabras clave gigantes en serif roja arriba (una cada vez), subtítulos
rojos que se acumulan en el gancho, cortes secos. Cambio: dibujado a mano (Toni, electricista inventado) y el giro
lleva a la recepcionista con IA de norte.local. Uso: python3 generar.py  (lee voz.json/trabajo/*.json, escribe index.html)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
tim = json.load(open(f"{D}/trabajo/timing.json")); W = json.load(open(f"{D}/trabajo/palabras.json"))
T = round(tim["total"], 2)
L = {l["scene"]: l for l in tim["lines"]}
INK = "#141212"; ROJO = "#d8141c"


def st(s):  # inicio de escena: un poco antes de su frase
    return 0 if s == "s1" else round(L[s]["start"] - 0.2, 3)


ORD = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
def fin(s):
    i = ORD.index(s)
    return T if i == len(ORD) - 1 else st(ORD[i + 1])
def du(s): return round(fin(s) - st(s), 3)


def wt(frag, n=0, d=None):
    hits = [w for w in W if frag.lower() in w["w"].lower()]
    return round(hits[n]["s"] + 0.05, 2) if len(hits) > n else d


# ---------- personajes ----------
def toni(id_, sil=False, brazos="manos"):
    piel = INK if sil else "#e2b48f"; ropa = INK if sil else "#1d1a19"; borde = "#000" if sil else "#5b514c"
    gorra = INK if sil else "#e8692e"; tinta = INK
    cara = "" if sil else f'''
      <path d="M232 238 L282 252 M368 238 L318 252" stroke="{tinta}" stroke-width="11" stroke-linecap="round"/>
      <ellipse cx="262" cy="272" rx="10" ry="8" fill="{tinta}"/><ellipse cx="338" cy="272" rx="10" ry="8" fill="{tinta}"/>
      <path d="M300 278 Q292 305 308 310" fill="none" stroke="{tinta}" stroke-width="6" stroke-linecap="round"/>
      <path d="M268 340 L332 338" stroke="{tinta}" stroke-width="8" stroke-linecap="round"/>
      <path d="M210 330 Q300 372 390 330 Q385 362 300 380 Q215 362 210 330 Z" fill="#5a3b28" opacity="0.55"/>'''
    if brazos == "manos":   # manos juntas en pico, como en el original
        br = f'''<path d="M95 690 Q140 560 250 640 L300 560 L350 640 Q460 560 505 690 Z" fill="{ropa}" stroke="{borde}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M262 650 L300 548 L338 650 Q300 668 262 650 Z" fill="{piel}" stroke="{tinta}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M300 560 L300 655" stroke="{tinta}" stroke-width="5"/>'''
    elif brazos == "barbilla":  # mano en la barbilla (plano en silueta)
        br = f'''<path d="M150 700 Q170 560 260 520 Q300 470 330 420" fill="none" stroke="{ropa}" stroke-width="70" stroke-linecap="round"/>
      <ellipse cx="325" cy="405" rx="40" ry="34" fill="{piel}" stroke="{tinta}" stroke-width="6"/>'''
    else:  # cruzados
        br = f'''<path d="M120 640 Q300 560 480 640 L470 690 Q300 620 130 690 Z" fill="{ropa}" stroke="{borde}" stroke-width="7" stroke-linejoin="round"/>'''
    return f'''<g id="{id_}" class="mano">
      <path d="M40 760 Q40 470 300 440 Q560 470 560 760 Z" fill="{ropa}" stroke="{borde}" stroke-width="7" stroke-linejoin="round"/>
      <rect x="235" y="370" width="130" height="95" rx="30" fill="{ropa}" stroke="{borde}" stroke-width="7"/>
      <ellipse cx="300" cy="275" rx="105" ry="118" fill="{piel}" stroke="{tinta}" stroke-width="8"/>
      <path d="M192 250 Q190 150 300 145 Q410 150 408 250 Q380 215 300 212 Q220 215 192 250 Z" fill="{gorra}" stroke="{tinta}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M262 214 Q300 196 338 214 L332 232 Q300 220 268 232 Z" fill="{INK}"/>
      {cara}
      {br}
    </g>'''


def jefa(id_, sil=False):
    cuerpo = INK if sil else "#1f2430"; pant = INK if sil else "#2c3e8f"; borde = "#000" if sil else INK
    cara = "" if sil else f'''
      <path d="M215 330 L265 345 M385 330 L335 345" stroke="#fff" stroke-width="10" stroke-linecap="round"/>
      <ellipse cx="245" cy="372" rx="16" ry="12" fill="#fff"/><ellipse cx="355" cy="372" rx="16" ry="12" fill="#fff"/>
      <path d="M262 445 Q300 465 338 445" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>
      <image href="assets/logo.svg" x="268" y="560" width="64" height="64"/>'''
    gorra = INK if sil else "#e8692e"
    return f'''<g id="{id_}" class="mano">
      <path d="M120 700 Q60 560 150 470 M480 700 Q540 560 450 470" fill="none" stroke="{cuerpo}" stroke-width="44" stroke-linecap="round"/>
      <rect x="150" y="215" width="300" height="560" rx="54" fill="{cuerpo}" stroke="{borde}" stroke-width="9"/>
      <rect x="175" y="255" width="250" height="470" rx="30" fill="{pant}"/>
      <path d="M150 600 Q300 520 450 600 L450 660 Q300 585 150 660 Z" fill="{cuerpo}" stroke="{borde}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M168 240 Q170 120 300 115 Q430 120 432 240 Q380 205 300 205 Q220 205 168 240 Z" fill="{gorra}" stroke="{INK}" stroke-width="8"/>
      <path d="M300 118 L300 205" stroke="{INK}" stroke-width="4" opacity="0.5"/>
      <path d="M262 150 L278 128 L300 150 L322 128 L338 150 L338 172 L262 172 Z" fill="{'#f2c230' if not sil else INK}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
      {cara}
    </g>'''


def despacho(fondo="#2b2524"):
    return f'''<rect width="1080" height="1920" fill="{fondo}"/>
      <g class="mano">
      <rect x="60" y="330" width="560" height="330" rx="12" fill="#101418" stroke="#000" stroke-width="8"/>
      <rect x="85" y="355" width="510" height="280" fill="#1e3a55"/>
      <rect x="110" y="380" width="200" height="120" fill="#2f5d86"/><path d="M110 560 L570 560 M110 590 L470 590" stroke="#4d86b8" stroke-width="12"/>
      <rect x="700" y="300" width="300" height="20" fill="#3b302c"/><rect x="700" y="520" width="300" height="20" fill="#3b302c"/>
      <path d="M760 300 Q735 250 760 205 Q790 175 820 205 Q845 250 820 300 Z" fill="#f4d35e" opacity="0.85"/><rect x="772" y="300" width="36" height="10" fill="#777"/>
      <path d="M890 520 Q865 470 890 425 Q920 395 950 425 Q975 470 950 520 Z" fill="#f4d35e" opacity="0.6"/><rect x="902" y="520" width="36" height="10" fill="#777"/>
      <rect x="720" y="395" width="110" height="120" rx="6" fill="#d9d4cc"/><circle cx="775" cy="440" r="22" fill="#555"/>
      </g>
      <rect y="1400" width="1080" height="520" fill="#0c0a0a"/>'''


movil = f'''<g class="mano">
      <rect x="-95" y="-170" width="190" height="340" rx="34" fill="{INK}"/><rect x="-78" y="-148" width="156" height="296" rx="22" fill="#6fd08c"/>
      <path d="M-30 -10 Q-24 -46 0 -46 L12 -46 M-35 2 L-35 24 Q-35 42 -17 42 L24 42" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/>
    </g>'''
movil_perdida = f'''<g class="mano">
      <rect x="-95" y="-170" width="190" height="340" rx="34" fill="{INK}"/><rect x="-78" y="-148" width="156" height="296" rx="22" fill="#e23b3b"/>
      <path d="M-40 -40 L40 40 M40 -40 L-40 40" stroke="#fff" stroke-width="22" stroke-linecap="round"/>
    </g>'''


def nube():
    circ = [(540, 900, 260), (330, 960, 190), (750, 960, 200), (420, 780, 170), (660, 770, 180), (540, 1100, 200), (300, 1120, 140), (790, 1130, 150)]
    c = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in circ)
    asoma = f'''
      <path d="M180 870 L60 800" stroke="#1d1a19" stroke-width="46" stroke-linecap="round"/><circle cx="55" cy="797" r="30" fill="#e2b48f" stroke="{INK}" stroke-width="7"/>
      <path d="M900 860 L1020 780" stroke="#1d1a19" stroke-width="46" stroke-linecap="round"/><circle cx="1025" cy="777" r="30" fill="#e2b48f" stroke="{INK}" stroke-width="7"/>
      <path d="M380 1250 L330 1380" stroke="#2c2f3a" stroke-width="50" stroke-linecap="round"/><ellipse cx="318" cy="1395" rx="55" ry="26" fill="{INK}"/>
      <path d="M700 1250 L760 1370" stroke="#2c2f3a" stroke-width="50" stroke-linecap="round"/><ellipse cx="775" cy="1385" rx="55" ry="26" fill="{INK}"/>
      <path d="M470 620 Q470 540 540 538 Q610 540 612 620 Z" fill="#e8692e" stroke="{INK}" stroke-width="7"/>
      <path d="M640 1200 Q650 1140 700 1150 Q740 1160 730 1210 Z" fill="#e8692e" stroke="{INK}" stroke-width="7"/>'''
    estrellas = "".join(f'<path transform="translate({x} {y})" d="M0 -40 L11 -12 L40 -12 L17 6 L26 36 L0 18 L-26 36 L-17 6 L-40 -12 L-11 -12 Z" fill="#f2c230" stroke="{INK}" stroke-width="5"/>' for x, y in [(250, 720), (850, 700), (180, 1050), (900, 1080), (540, 640)])
    return f'''<g class="mano">{asoma}<g fill="#e9e4dc" stroke="{INK}" stroke-width="9">{c}</g>
      <g fill="#e9e4dc">{c.replace('r="', 'r="0').replace('r="0', 'r="')}</g>
      <path d="M360 870 L400 840 L440 880 L480 845 M610 890 L650 860 L690 900 L730 865 M450 1020 L500 990 L550 1025 L600 990 L640 1020" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
      {estrellas}</g>'''


# ---------- palabras gigantes (serif roja, una cada vez, arriba) ----------
PAL = [("TONI", wt("tony", 0, 3.8), None), ("ELECTRICISTA", wt("electricista"), None),
       ("COGEROS", wt("cogeros"), None), ("A TODAS", wt("todas", 1), None), ("CLONÁNDOME", wt("clonándome"), None),
       ("CINCO TONIS", wt("5", 1, 10.0), None), ("UN SOLO", wt("un", 1, 11.4), None), ("MÓVIL", wt("móvil", 0), None),
       ("SE PELEAN", wt("pelean"), None), ("NINGUNO", wt("bono", 0, 15.4), None),
       ("MI JEFA", wt("jefa"), None), ("VOSOTRAS", wt("vosotras"), None),
       ("LLAMADAS", wt("llamadas", 1), None), ("WHATSAPPS", wt("whatsapp"), None), ("VISITAS", wt("visitas"), None), ("24 HORAS", wt("24"), None),
       ("SÍGUELA", wt("hiela", 0, 24.3), None)]
pal = []
for i, (txt, t0, _) in enumerate(PAL):
    t1 = PAL[i + 1][1] if i + 1 < len(PAL) else wt("comenta", 0, t0 + 0.9) - 0.1
    # que no cruce un corte de escena
    for s in ORD:
        if st(s) > t0 and st(s) < t1: t1 = st(s)
    pal.append((i, txt, t0, round(t1 - t0, 3)))
pal_html = "\n".join(f'      <div id="pw{i}" class="pw clip" data-start="{t0:.2f}" data-duration="{d:.2f}" data-track-index="8"><span style="font-size:{min(210, int(900 / (0.74 * len(txt))))}px">{txt}</span></div>' for i, txt, t0, d in pal)
pal_js = "\n".join(f'      tl.fromTo("#pw{i} span", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.12, ease: "power3.out" }}, {t0:.2f});' for i, txt, t0, d in pal)

# subtítulos rojos que se acumulan (gancho, como el original)
g_words = [w for w in W if w["s"] < L["s2"]["start"] - 0.3]
g_html = " ".join(f'<span id="gw{k}">{w["w"].strip(",.")}</span>' for k, w in enumerate(g_words))
g_js = "\n".join(f'      tl.fromTo("#gw{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {max(0.0, w["s"] + 0.25):.2f});' for k, w in enumerate(g_words))

# efectos
golpes = [t0 for i, txt, t0, d in pal]
sfx = [("boom", "boom.mp3", t, 0.9, 0.55) for t in golpes]
sfx += [("ring", "ring.wav", st("s4") + 0.05, 2.2, 0.35), ("wc", "wcine.mp3", st("s3") + 1.7, 1.0, 0.5),
        ("wh", "whoosh.wav", st("s5") + 0.05, 0.45, 0.6), ("se", "sello.wav", wt("bono", 0, 15.4), 0.5, 0.7),
        ("ri", "riser.mp3", st("s6") - 1.2, 1.2, 0.35), ("po", "pop.wav", wt("recepción", 0, 25.7), 0.3, 0.5)]
sfx_html = "\n".join(f'      <audio id="fx{k}" class="clip" src="assets/{f}" data-start="{max(0.01, t):.2f}" data-duration="{d}" data-volume="{v}" data-track-index="{12 + k}"></audio>' for k, (n, f, t, d, v) in enumerate(sfx))

clon_pos = [(-40, 760), (180, 700), (400, 680), (620, 700), (840, 760)]
clones_svg = "".join(f'<g transform="translate({x} {y}) scale(0.48)"><g id="cl{k}">{toni(f"tc{k}", brazos="cruz")}</g></g>' for k, (x, y) in enumerate(clon_pos))

html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter"; }}
      .esc {{ position: absolute; inset: 0; overflow: hidden; background: #2b2524; }}
      svg.lienzo {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .mano {{ filter: url(#lapiz); }}
      .pw {{ position: absolute; left: 0; right: 0; top: 150px; height: 300px; display: flex; align-items: center; justify-content: center; }}
      .pw span {{ display: inline-block; font-family: "Playfair Display"; font-weight: 700; color: {ROJO}; line-height: 1; transform-origin: 50% 50%; letter-spacing: -2px; text-shadow: 0 6px 24px rgba(0,0,0,.45); white-space: nowrap; }}
      #gancho {{ position: absolute; left: 110px; right: 110px; top: 1470px; text-align: center; font-family: "Inter"; font-weight: 900; font-size: 88px; line-height: 1.05; color: {ROJO}; text-shadow: 0 4px 0 #000, 0 0 18px rgba(0,0,0,.8); }}
      #gancho span {{ display: inline; }}
      .marca {{ position: absolute; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 24px; font-weight: 900; font-size: 70px; color: #fff; }}
      .marca img {{ width: 100px; height: 100px; }}
      #pill {{ position: absolute; top: 1020px; left: 0; right: 0; display: flex; justify-content: center; }}
      #pill span {{ padding: 18px 56px 28px; border-radius: 36px; background: #e8692e; color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 140px; border: 8px solid #fff; }}
      #comenta {{ position: absolute; top: 860px; left: 0; right: 0; text-align: center; font-family: "Playfair Display"; font-weight: 700; font-size: 130px; color: #fff; }}
    </style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><defs>
      <filter id="lapiz" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="r"/><feDisplacementMap in="SourceGraphic" in2="r" scale="5"/></filter>
      <radialGradient id="foco" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#efece8"/><stop offset="1" stop-color="#a9a29c"/></radialGradient>
      <radialGradient id="vin" cx="50%" cy="45%" r="75%"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.75"/></radialGradient>
    </defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">

      <div id="s1" class="esc clip" data-start="0" data-duration="{du('s1')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920">{despacho()}
          <g transform="translate(240 700)"><g id="t1">{toni("ta1")}</g></g>
          <rect x="0" y="1440" width="1080" height="90" fill="#1a1818" class="mano"/><rect x="250" y="1458" width="580" height="50" rx="6" fill="#0d0d0d"/>
          <rect width="1080" height="1920" fill="url(#vin)"/></svg>
        <div id="gancho">{g_html}</div>
      </div>

      <div id="s2" class="esc clip" data-start="{st('s2')}" data-duration="{du('s2')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="url(#foco)"/>
          <g transform="translate(150 650) scale(1.3)"><g id="t2">{toni("ts2", sil=True, brazos="barbilla")}</g></g></svg>
      </div>

      <div id="s3" class="esc clip" data-start="{st('s3')}" data-duration="{du('s3')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><g id="s3a">{despacho("#241f1e")}
          <g transform="translate(140 520) scale(1.35)"><g id="t3">{toni("ta3")}</g></g>
          <rect width="1080" height="1920" fill="url(#vin)"/></g>
          <g id="s3b" opacity="0"><rect width="1080" height="1920" fill="url(#foco)"/>{clones_svg}
          <rect y="1180" width="1080" height="740" fill="#8f8780" class="mano"/></g>
          <rect id="flash" width="1080" height="1920" fill="#fff" opacity="0"/></svg>
      </div>

      <div id="s4" class="esc clip" data-start="{st('s4')}" data-duration="{du('s4')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#2b2524"/>
          {"".join(f'<g transform="translate({x} {y}) scale(0.5)"><g id="c4{k}">{toni(f"t4{k}", brazos="cruz")}</g></g>' for k, (x, y) in enumerate([(-30, 560), (170, 500), (390, 470), (610, 500), (810, 560)]))}
          <rect y="1050" width="1080" height="870" fill="#5a3f2c" class="mano"/><path d="M0 1050 L1080 1050" stroke="#000" stroke-width="9"/>
          <g transform="translate(540 1380)"><g id="mv4">{movil}</g></g>
          <rect width="1080" height="1920" fill="url(#vin)"/></svg>
      </div>

      <div id="s5" class="esc clip" data-start="{st('s5')}" data-duration="{du('s5')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#2b2524"/>
          <rect y="1300" width="1080" height="620" fill="#5a3f2c" class="mano"/>
          <g id="nb">{nube()}</g>
          <g transform="translate(860 1560)"><g id="mv5"><g transform="rotate(-18)">{movil}</g></g></g>
          <g transform="translate(860 1560)"><g id="mv5b" opacity="0"><g transform="rotate(-18)">{movil_perdida}</g></g></g>
          <rect width="1080" height="1920" fill="url(#vin)"/></svg>
      </div>

      <div id="s6" class="esc clip" data-start="{st('s6')}" data-duration="{du('s6')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="url(#foco)"/>
          <g transform="translate(240 620) scale(1.0)"><g id="j6">{jefa("js6", sil=True)}</g></g>
          <g transform="translate(240 620) scale(1.0)"><g id="j6b" opacity="0">{jefa("jc6")}</g></g></svg>
      </div>

      <div id="s7" class="esc clip" data-start="{st('s7')}" data-duration="{du('s7')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#1b1716"/>
          <g id="p1"><g transform="translate(540 1050) scale(2)"><g id="p1m">{movil}</g></g></g>
          <g id="p2" opacity="0"><g class="mano">
            <rect x="200" y="620" width="680" height="900" rx="40" fill="#ece5dd" stroke="#000" stroke-width="9"/>
            <rect x="240" y="680" width="430" height="120" rx="26" fill="#fff" stroke="#000" stroke-width="6"/>
            <rect x="420" y="850" width="420" height="120" rx="26" fill="#d9fdd3" stroke="#000" stroke-width="6"/>
            <rect x="240" y="1020" width="380" height="120" rx="26" fill="#fff" stroke="#000" stroke-width="6"/>
            <rect x="420" y="1190" width="420" height="120" rx="26" fill="#d9fdd3" stroke="#000" stroke-width="6"/>
            <path d="M740 940 L760 958 L800 918 M770 940 L790 958 L830 918" fill="none" stroke="#34b7f1" stroke-width="9" stroke-linecap="round"/>
            <path d="M740 1280 L760 1298 L800 1258 M770 1280 L790 1298 L830 1258" fill="none" stroke="#34b7f1" stroke-width="9" stroke-linecap="round"/>
            <path d="M280 730 L600 730 M280 765 L520 765 M460 900 L780 900 M280 1070 L560 1070 M460 1240 L760 1240" stroke="#777" stroke-width="12" stroke-linecap="round"/></g></g>
          <g id="p3" opacity="0"><g class="mano">
            <rect x="190" y="640" width="700" height="820" rx="30" fill="#fffaf2" stroke="#000" stroke-width="9"/>
            <rect x="190" y="640" width="700" height="160" rx="30" fill="#e8692e" stroke="#000" stroke-width="9"/>
            <circle cx="330" cy="640" r="22" fill="#000"/><circle cx="750" cy="640" r="22" fill="#000"/>
            {"".join(f'<rect x="{240 + c * 125}" y="{850 + r * 140}" width="95" height="100" rx="12" fill="#ece5dd"/>' for r in range(4) for c in range(5))}
            <ellipse id="circ" cx="537" cy="1040" rx="80" ry="72" fill="none" stroke="{ROJO}" stroke-width="12"/>
            <path d="M505 1040 L530 1065 L575 1012" fill="none" stroke="#2c9a4a" stroke-width="16" stroke-linecap="round"/></g></g>
          <g id="p4" opacity="0"><g class="mano"><circle cx="540" cy="1050" r="330" fill="#fffaf2" stroke="#000" stroke-width="10"/>
            <path d="M540 1050 L540 820 M540 1050 L690 1120" stroke="#000" stroke-width="22" stroke-linecap="round"/>
            <path d="M540 720 L540 760 M870 1050 L830 1050 M540 1380 L540 1340 M210 1050 L250 1050" stroke="#000" stroke-width="14"/></g></g>
          <rect width="1080" height="1920" fill="url(#vin)"/></svg>
      </div>

      <div id="s8" class="esc clip" data-start="{st('s8')}" data-duration="{du('s8')}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="url(#foco)"/>
          <g id="j8w"><g transform="translate(240 600)"><g id="j8">{jefa("jc8")}</g></g></g></svg>
        <div id="cta" style="position:absolute;inset:0;opacity:0;background:#141212">
          <div id="comenta">Comenta</div>
          <div id="pill"><span>RECEPCIÓN</span></div>
          <div class="marca" style="bottom:300px"><img src="assets/logo.svg" alt="" />norte.local</div>
        </div>
      </div>

{pal_html}

      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{T}" data-volume="1" data-track-index="10"></audio>
      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{T}" data-media-start="0" data-volume="0.4" data-fade-out="0.8" data-track-index="11"></audio>
{sfx_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#s1 svg", {{ scale: 1.0, transformOrigin: "50% 50%" }}, {{ scale: 1.06, duration: {du('s1')}, ease: "none" }}, 0);
{g_js}
      tl.fromTo("#t2", {{ x: -30 }}, {{ x: 10, duration: {du('s2')}, ease: "none" }}, {st('s2')});
      tl.fromTo("#s3a", {{ scale: 1.0, transformOrigin: "50% 50%" }}, {{ scale: 1.08, duration: 1.8, ease: "none" }}, {st('s3')});
      tl.to("#flash", {{ opacity: 1, duration: 0.08 }}, {wt('clonándome', 0, 8.1) - 0.08:.2f});
      tl.set("#s3a", {{ opacity: 0 }}, {wt('clonándome', 0, 8.1):.2f});
      tl.set("#s3b", {{ opacity: 1 }}, {wt('clonándome', 0, 8.1):.2f});
      tl.to("#flash", {{ opacity: 0, duration: 0.3 }}, {wt('clonándome', 0, 8.1):.2f});
      [0, 1, 2, 3, 4].forEach(k => tl.fromTo("#cl" + k, {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.16, ease: "back.out(2)" }}, {wt('clonándome', 0, 8.1):.2f} + Math.abs(k - 2) * 0.12));
      tl.to("#mv4", {{ rotation: 7, duration: 0.05, yoyo: true, repeat: 41, ease: "none" }}, {st('s4') + 0.05:.2f});
      [0, 1, 2, 3, 4].forEach(k => tl.to("#c4" + k, {{ y: 40, duration: 0.25, ease: "power2.out" }}, {wt('móvil', 0, 11.9) - 0.1:.2f} + k * 0.03));
      tl.fromTo("#nb", {{ scale: 0.6, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.2, ease: "back.out(2)" }}, {st('s5'):.2f});
      tl.to("#nb", {{ x: 14, y: -10, rotation: 1.5, duration: 0.06, yoyo: true, repeat: 40, ease: "none" }}, {st('s5') + 0.2:.2f});
      tl.fromTo("#mv5", {{ x: -420, y: -900, rotation: -200 }}, {{ x: 0, y: 0, rotation: 0, duration: 0.5, ease: "power2.in" }}, {wt('móvil', 1, 13.8):.2f});
      tl.set("#mv5", {{ opacity: 0 }}, {wt('bono', 0, 15.4):.2f});
      tl.set("#mv5b", {{ opacity: 1 }}, {wt('bono', 0, 15.4):.2f});
      tl.fromTo("#mv5b", {{ scale: 1.4 }}, {{ scale: 1, duration: 0.18, ease: "back.out(3)" }}, {wt('bono', 0, 15.4):.2f});
      tl.fromTo("#j6", {{ x: 60 }}, {{ x: 0, duration: 1.2, ease: "power2.out" }}, {st('s6'):.2f});
      tl.to("#j6", {{ opacity: 0, duration: 0.25 }}, {wt('vosotras', 0, 17.6) - 0.1:.2f});
      tl.to("#j6b", {{ opacity: 1, duration: 0.25 }}, {wt('vosotras', 0, 17.6) - 0.1:.2f});
      tl.set("#p1", {{ opacity: 0 }}, {wt('whatsapp', 0, 20.3):.2f}); tl.set("#p2", {{ opacity: 1 }}, {wt('whatsapp', 0, 20.3):.2f});
      tl.set("#p2", {{ opacity: 0 }}, {wt('visitas', 0, 21.3):.2f}); tl.set("#p3", {{ opacity: 1 }}, {wt('visitas', 0, 21.3):.2f});
      tl.set("#p3", {{ opacity: 0 }}, {wt('24', 0, 22.6):.2f}); tl.set("#p4", {{ opacity: 1 }}, {wt('24', 0, 22.6):.2f});
      tl.fromTo("#p1m", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {st('s7'):.2f});
      tl.fromTo("#circ", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {wt('visitas', 0, 21.3) + 0.2:.2f});
      tl.fromTo("#j8", {{ scale: 1, transformOrigin: "50% 40%" }}, {{ scale: 1.12, duration: 1.2, ease: "power1.out" }}, {st('s8'):.2f});
      tl.to("#cta", {{ opacity: 1, duration: 0.15 }}, {wt('comenta', 0, 25.3) - 0.1:.2f});
      tl.fromTo("#pill span", {{ scale: 0.3, rotation: -8 }}, {{ scale: 1, rotation: -3, duration: 0.35, ease: "back.out(2.2)" }}, {wt('recepción', 0, 25.7):.2f});
{pal_js}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(f"{D}/index.html", "w").write(html)
print("ok T=", T, [(s, st(s)) for s in ORD])
print([(t, round(a, 2)) for _, t, a, _ in pal])
