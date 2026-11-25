import json
v = json.load(open("/tmp/fonta/voz.json"))
T = 25.4
SC = {"s1": (0, 4.6), "s2": (4.6, 6.45), "s3": (6.45, 11.6), "s4": (11.6, 14.4), "s5": (14.4, 22.35), "s6": (22.35, T)}

# ---------- subtítulos (solo en las escenas sin texto grande: frases 0, 2 y 3) ----------
pages = []
for li in (0, 2, 3):
    ws = [w for w in v["words"] if w["l"] == li]
    cur = []
    for i, w in enumerate(ws):
        cur.append(w)
        largo = len(" ".join(x["w"] for x in cur))
        sig = len(ws[i + 1]["w"]) + 1 if i + 1 < len(ws) else 0
        if len(cur) == 3 or largo + sig > 16 or w["w"][-1] in ".,?…" or i == len(ws) - 1:
            pages.append(cur); cur = []
caps = []
for k, p in enumerate(pages):
    t0 = p[0]["t0"] - 0.04
    t1 = pages[k + 1][0]["t0"] - 0.04 if k + 1 < len(pages) and pages[k + 1][0]["l"] == p[0]["l"] else p[-1]["t1"] + 0.25
    txt = " ".join(w["w"] for w in p).strip(".,…").upper()
    caps.append((k, t0, t1 - t0, txt))
caps_html = "\n".join(
    f'      <div id="cap{k}" class="cap clip" data-start="{t0:.3f}" data-duration="{d:.3f}" data-track-index="9"><span>{txt}</span></div>'
    for k, t0, d, txt in caps)
caps_js = "\n".join(f'      tl.fromTo("#cap{k} span", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.14, ease: "back.out(2.5)" }}, {t0:.3f});' for k, t0, d, txt in caps)

def word_t(li, frag, default):
    for w in v["words"]:
        if w["l"] == li and frag.lower() in w["w"].lower():
            return w["t0"]
    return default

t_llam = word_t(4, "llamadas", 19.0); t_whats = word_t(4, "whatsapp", 19.8); t_insta = word_t(4, "instagram", 20.6)
t_demo = word_t(4, "demo", 16.0); t_telef = word_t(2, "teléfono", 10.8); t_imp = word_t(3, "impuestos", 13.3)

# ---------- dibujos (línea negra a mano, colores planos, estilo ilustración cálida) ----------
INK = "#1d1b19"
def paco(id_, cara="tonta"):
    ojos = ('<circle cx="170" cy="215" r="13" fill="%s"/><circle cx="238" cy="210" r="7" fill="%s"/>' % (INK, INK)) if cara == "tonta" else \
           ('<circle cx="172" cy="212" r="9" fill="%s"/><circle cx="232" cy="212" r="9" fill="%s"/>' % (INK, INK))
    return f'''<g id="{id_}" class="mano">
      <path d="M150 520 L140 660 L205 660 L208 540 Z M250 520 L262 660 L320 660 L300 520 Z" fill="#4f6e93" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M118 662 Q120 640 145 640 L210 640 Q222 664 210 680 L120 680 Q110 674 118 662 Z M250 662 Q252 640 277 640 L330 640 Q345 664 335 680 L252 680 Q240 674 250 662 Z" fill="{INK}"/>
      <path d="M125 300 Q200 270 280 300 L310 540 Q205 575 110 540 Z" fill="#5b7fa6" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M160 300 L165 420 L250 420 L255 300" fill="none" stroke="{INK}" stroke-width="7"/>
      <rect x="175" y="345" width="62" height="50" rx="8" fill="#4f6e93" stroke="{INK}" stroke-width="6"/>
      <path d="M128 310 Q80 380 92 470" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>
      <path d="M128 310 Q80 380 92 470" fill="none" stroke="#5b7fa6" stroke-width="30" stroke-linecap="round"/>
      <path d="M282 310 Q330 370 340 440" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>
      <path d="M282 310 Q330 370 340 440" fill="none" stroke="#5b7fa6" stroke-width="30" stroke-linecap="round"/>
      <circle cx="92" cy="478" r="24" fill="#f2c39b" stroke="{INK}" stroke-width="7"/>
      <circle cx="340" cy="450" r="24" fill="#f2c39b" stroke="{INK}" stroke-width="7"/>
      <path d="M335 445 L395 360 M380 340 Q400 330 412 350 Q420 368 400 378 L385 372" fill="none" stroke="#8a8f96" stroke-width="16" stroke-linecap="round"/>
      <path d="M335 445 L395 360" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity="0.5"/>
      <ellipse cx="205" cy="215" rx="98" ry="104" fill="#f2c39b" stroke="{INK}" stroke-width="8"/>
      <path d="M108 180 Q110 95 205 92 Q300 95 302 180 Z" fill="#e8692e" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M285 172 Q340 170 352 188 Q330 198 290 192" fill="#e8692e" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      {ojos}
      <path d="M150 255 Q178 238 205 252 Q232 238 262 255 Q250 285 205 272 Q160 285 150 255 Z" fill="#6b4a33" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M185 285 Q205 300 228 284" fill="#7a2f22" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
      <path d="M198 222 Q192 245 210 246" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
    </g>'''

tienda = f'''<g class="mano">
      <rect x="70" y="420" width="940" height="900" fill="#efe4d4" stroke="{INK}" stroke-width="9"/>
      <rect x="110" y="470" width="860" height="170" rx="18" fill="#e8692e" stroke="{INK}" stroke-width="9"/>
      <text x="540" y="580" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="92" fill="#fffaf2">FONTANERÍA PACO</text>
      <path d="M95 690 L985 690 L950 760 L130 760 Z" fill="#7c9a7e" stroke="{INK}" stroke-width="8"/>
      <path d="M130 760 Q175 790 220 760 Q265 790 310 760 Q355 790 400 760 Q445 790 490 760 Q535 790 580 760 Q625 790 670 760 Q715 790 760 760 Q805 790 850 760 Q895 790 950 760" fill="none" stroke="{INK}" stroke-width="7"/>
      <rect x="150" y="830" width="420" height="330" rx="10" fill="#bcd6dc" stroke="{INK}" stroke-width="9"/>
      <path d="M300 950 L300 900 Q300 880 330 880 L420 880 M420 865 L420 900 M300 950 Q300 990 330 990" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>
      <path d="M335 1010 Q335 1040 345 1040 Q355 1040 355 1010 Q345 990 335 1010 Z" fill="#5aa9e6" stroke="{INK}" stroke-width="5"/>
      <rect x="650" y="830" width="260" height="490" rx="8" fill="#9b6b48" stroke="{INK}" stroke-width="9"/>
      <circle cx="875" cy="1080" r="13" fill="{INK}"/>
      <rect x="0" y="1320" width="1080" height="600" fill="#d8cfc2"/>
      <path d="M0 1320 L1080 1320" stroke="{INK}" stroke-width="9"/>
    </g>'''

cocina = f'''<g class="mano">
      <rect x="0" y="0" width="1080" height="1920" fill="#f0eee6"/>
      <rect x="0" y="0" width="1080" height="1120" fill="#e9e1d3"/>
      <g opacity="0.5" stroke="#d6cbb8" stroke-width="4">{''.join(f'<path d="M{x} 0 L{x} 1120"/>' for x in range(0,1081,120))}{''.join(f'<path d="M0 {y} L1080 {y}"/>' for y in range(0,1121,120))}</g>
      <rect x="140" y="700" width="800" height="70" rx="12" fill="#cfc4b4" stroke="{INK}" stroke-width="9"/>
      <rect x="170" y="770" width="740" height="420" fill="#f7f2ea" stroke="{INK}" stroke-width="9"/>
      <rect x="200" y="800" width="680" height="360" fill="#3b3631" stroke="{INK}" stroke-width="7"/>
      <path d="M470 700 L470 610 Q470 570 520 570 L640 570 L640 620" fill="none" stroke="#8a8f96" stroke-width="26" stroke-linecap="round"/>
      <path d="M470 700 L470 610 Q470 570 520 570 L640 570 L640 620" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" opacity="0.6"/>
      <path d="M540 800 L540 980 Q540 1010 570 1010 L650 1010" fill="none" stroke="#9aa0a6" stroke-width="22"/>
      <rect x="0" y="1190" width="1080" height="730" fill="#d9cdb9"/>
      <path d="M0 1190 L1080 1190" stroke="{INK}" stroke-width="9"/>
    </g>'''

piernas = f'''<g id="piernas" class="mano">
      <path d="M380 1120 Q520 1080 640 1130 L640 1215 Q510 1250 380 1210 Z" fill="#5b7fa6" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <g id="pierna1"><path d="M600 1140 L860 1150 L860 1210 L600 1210 Z" fill="#4f6e93" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M850 1120 Q900 1120 905 1160 L905 1215 L850 1215 Z" fill="{INK}"/></g>
      <g id="pierna2"><path d="M560 1175 L820 1235 L808 1290 L550 1235 Z" fill="#4f6e93" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M812 1215 Q860 1220 860 1262 L850 1305 L800 1295 Z" fill="{INK}"/></g>
    </g>'''

movil = f'''<g id="movil" class="mano">
      <rect x="-70" y="-130" width="140" height="260" rx="28" fill="{INK}"/>
      <rect x="-56" y="-112" width="112" height="224" rx="18" fill="#6fd08c"/>
      <path d="M-26 -10 Q-20 -40 0 -40 L10 -40 M-30 0 L-30 20 Q-30 35 -15 35 L20 35" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>
      <path d="M-105 -60 Q-130 0 -105 60 M105 -60 Q130 0 105 60 M-135 -90 Q-170 0 -135 90 M135 -90 Q170 0 135 90" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
    </g>'''

oficina = f'''<g class="mano">
      <rect x="0" y="0" width="1080" height="1920" fill="#e7e1d6"/>
      <rect x="300" y="250" width="480" height="300" rx="10" fill="#f7f2ea" stroke="{INK}" stroke-width="8"/>
      <text x="540" y="380" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="64" fill="{INK}">AGENCIA</text>
      <text x="540" y="460" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="64" fill="#c0392b">TRIBUTARIA</text>
      <g id="perro">
        <path d="M330 1180 Q330 960 540 940 Q750 960 750 1180 Z" fill="#2f3440" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
        <path d="M470 950 L540 1060 L610 950 Z" fill="#fffaf2" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
        <path d="M525 980 L555 980 L565 1090 L540 1120 L515 1090 Z" fill="#c0392b" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
        <path d="M420 640 Q340 650 345 800 Q360 860 410 840 Z" fill="#7a5233" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M660 640 Q740 650 735 800 Q720 860 670 840 Z" fill="#7a5233" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        <ellipse cx="540" cy="760" rx="150" ry="170" fill="#c99566" stroke="{INK}" stroke-width="9"/>
        <ellipse cx="540" cy="850" rx="85" ry="65" fill="#ead2b5" stroke="{INK}" stroke-width="7"/>
        <ellipse cx="540" cy="815" rx="34" ry="24" fill="{INK}"/>
        <path d="M540 840 L540 870 Q515 895 495 878 M540 870 Q565 895 585 878" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
        <circle cx="485" cy="730" r="15" fill="{INK}"/><circle cx="595" cy="730" r="15" fill="{INK}"/>
        <path d="M455 690 L510 705 M625 690 L570 705" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>
        <rect x="440" y="610" width="200" height="22" rx="4" fill="{INK}"/><rect x="470" y="560" width="140" height="60" rx="6" fill="{INK}"/>
      </g>
      <rect x="120" y="1150" width="840" height="90" rx="10" fill="#9b6b48" stroke="{INK}" stroke-width="9"/>
      <rect x="160" y="1240" width="60" height="500" fill="#8a5d3d" stroke="{INK}" stroke-width="8"/><rect x="860" y="1240" width="60" height="500" fill="#8a5d3d" stroke="{INK}" stroke-width="8"/>
      <rect x="380" y="1090" width="320" height="70" rx="8" fill="#e8692e" stroke="{INK}" stroke-width="7"/>
      <text x="540" y="1140" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="44" fill="#fffaf2">HACIENDA</text>
      <rect x="170" y="1070" width="180" height="80" fill="#fffaf2" stroke="{INK}" stroke-width="6" transform="rotate(-6 260 1110)"/>
      <rect x="740" y="1060" width="200" height="90" fill="#fffaf2" stroke="{INK}" stroke-width="6" transform="rotate(5 840 1105)"/>
      <g id="sellado" opacity="0"><rect x="730" y="1050" width="220" height="100" rx="8" fill="none" stroke="#c0392b" stroke-width="10" transform="rotate(5 840 1100)"/>
      <text x="840" y="1128" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="62" fill="#c0392b" transform="rotate(5 840 1100)">PAGAR</text></g>
      <g id="sello"><rect x="805" y="780" width="70" height="140" rx="14" fill="#9b6b48" stroke="{INK}" stroke-width="7"/><rect x="770" y="910" width="140" height="50" rx="8" fill="#c0392b" stroke="{INK}" stroke-width="7"/>
      <circle cx="840" cy="770" r="40" fill="#c99566" stroke="{INK}" stroke-width="7"/></g>
    </g>'''

items = [("Responde llamadas", t_llam), ("Contesta WhatsApps", t_whats), ("Y los MD's de Instagram", t_insta)]
items_html = "\n".join(f'''        <div id="it{i}" class="item"><div class="chk">✓</div><span>{txt}</span></div>''' for i, (txt, _) in enumerate(items))
items_js = "\n".join(f'      tl.fromTo("#it{i}", {{ x: -80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }}, {t-0.05:.2f});\n      tl.fromTo("#it{i} .chk", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, ease: "back.out(3)" }}, {t+0.12:.2f});' for i, (txt, t) in enumerate(items))

html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      /* Reel de humor "el fontanero más imbécil" (guion de Hugo, 23-nov). Ilustración cálida a mano: tinta negra,
         colores planos, fondo crema; subtítulos en caja; marca norte.local. */
      :root {{ --crema: #f0eee6; --tinta: #1d1b19; --naranja: #e8692e; --font-display: "Oswald"; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--crema); }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter"; }}
      .esc {{ position: absolute; inset: 0; overflow: hidden; background: var(--crema); }}
      svg.lienzo {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .mano {{ filter: url(#lapiz); }}
      .cap {{ position: absolute; left: 0; right: 0; top: 1500px; display: flex; justify-content: center; }}
      .cap span {{ display: inline-block; background: var(--tinta); color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 82px; letter-spacing: 1px; padding: 6px 30px 12px; border-radius: 18px; transform-origin: 50% 60%; }}
      #s2t {{ position: absolute; top: 640px; left: 80px; right: 80px; text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 150px; line-height: 1.02; color: var(--tinta); }}
      #s2t em {{ font-style: normal; color: var(--naranja); }}
      #s5t {{ position: absolute; top: 300px; left: 80px; right: 80px; font-family: "Oswald"; font-weight: 700; font-size: 118px; line-height: 1.02; color: var(--tinta); }}
      #s5t em {{ font-style: normal; color: var(--naranja); }}
      #lista {{ position: absolute; top: 760px; left: 80px; right: 80px; }}
      .item {{ display: flex; align-items: center; gap: 30px; height: 150px; margin-bottom: 30px; padding: 0 40px; border: 7px solid var(--tinta); border-radius: 34px; background: #fffaf2; font-weight: 800; font-size: 58px; color: var(--tinta); }}
      .chk {{ width: 84px; height: 84px; border-radius: 42px; background: var(--naranja); color: #fff; font-size: 54px; font-weight: 900; display: flex; align-items: center; justify-content: center; border: 6px solid var(--tinta); flex: none; }}
      #marca5 {{ position: absolute; bottom: 230px; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 24px; font-weight: 900; font-size: 64px; color: var(--tinta); }}
      #marca5 img {{ width: 96px; height: 96px; }}
      #s6t {{ position: absolute; top: 330px; left: 70px; right: 70px; text-align: center; font-family: "Oswald"; font-weight: 700; font-size: 136px; line-height: 1.02; color: var(--tinta); }}
      #s6t em {{ font-style: normal; color: var(--naranja); }}
      #marca6 {{ position: absolute; top: 760px; left: 0; right: 0; text-align: center; font-weight: 900; font-size: 60px; color: var(--naranja); }}
    </style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><defs>
      <filter id="lapiz" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="r"/><feDisplacementMap in="SourceGraphic" in2="r" scale="5"/></filter>
    </defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">

      <div id="s1" class="esc clip" data-start="{SC['s1'][0]}" data-duration="{SC['s1'][1]-SC['s1'][0]:.2f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#cfe3e8"/>{tienda}
          <g transform="translate(330 760)"><g id="paco1">{paco("pacoA")}</g></g></svg>
      </div>

      <div id="s2" class="esc clip" data-start="{SC['s2'][0]}" data-duration="{SC['s2'][1]-SC['s2'][0]:.2f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><g id="paco2" opacity="0.13" transform="translate(140 300) scale(2)">{paco("pacoB")}</g></svg>
        <div id="s2t">Y te preguntarás… <em>¿por qué?</em></div>
      </div>

      <div id="s3" class="esc clip" data-start="{SC['s3'][0]}" data-duration="{SC['s3'][1]-SC['s3'][0]:.2f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920">{cocina}{piernas}<g transform="translate(250 1290) rotate(-12)"><g id="movil3">{movil}</g></g>
          <g id="perdidas" opacity="0"><circle cx="330" cy="1150" r="52" fill="#c0392b" stroke="{INK}" stroke-width="7"/><text id="nperd" x="330" y="1172" text-anchor="middle" font-family="Inter" font-weight="900" font-size="60" fill="#fff">1</text></g></svg>
      </div>

      <div id="s4" class="esc clip" data-start="{SC['s4'][0]}" data-duration="{SC['s4'][1]-SC['s4'][0]:.2f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920">{oficina}</svg>
      </div>

      <div id="s5" class="esc clip" data-start="{SC['s5'][0]}" data-duration="{SC['s5'][1]-SC['s5'][0]:.2f}" data-track-index="0">
        <div id="s5t">No seas como él.<br />Pide tu <em>demo gratis</em></div>
        <div id="lista">
{items_html}
        </div>
        <div id="marca5"><img src="assets/logo.svg" alt="" />norte.local</div>
      </div>

      <div id="s6" class="esc clip" data-start="{SC['s6'][0]}" data-duration="{SC['s6'][1]-SC['s6'][0]:.2f}" data-track-index="0">
        <div id="s6t">No seas tan <em>tonto</em><br />como él</div>
        <div id="marca6">norte.local</div>
        <svg class="lienzo" viewBox="0 0 1080 1920"><g transform="translate(240 980) scale(1.5)"><g id="paco6">{paco("pacoC")}</g></g></svg>
      </div>

{caps_html}

      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{T}" data-volume="1" data-track-index="10"></audio>
      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{T}" data-media-start="0" data-volume="0.25" data-fade-out="0.8" data-track-index="11"></audio>
      <audio id="ring" class="clip" src="assets/ring.wav" data-start="{SC['s3'][0]+0.3:.2f}" data-duration="1.6" data-volume="0.35" data-track-index="12"></audio>
      <audio id="ring2" class="clip" src="assets/ring.wav" data-start="{SC['s3'][0]+2.2:.2f}" data-duration="1.6" data-volume="0.35" data-track-index="13"></audio>
      <audio id="whoosh" class="clip" src="assets/whoosh.wav" data-start="{SC['s4'][0]-0.12:.2f}" data-duration="0.45" data-volume="0.6" data-track-index="14"></audio>
      <audio id="sello" class="clip" src="assets/sello.wav" data-start="{t_imp+0.25:.2f}" data-duration="0.35" data-volume="0.9" data-track-index="15"></audio>
      <audio id="boing" class="clip" src="assets/boing.wav" data-start="{SC['s6'][0]+0.05:.2f}" data-duration="0.5" data-volume="0.7" data-track-index="16"></audio>
      <audio id="pop0" class="clip" src="assets/pop.wav" data-start="{t_llam:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="17"></audio>
      <audio id="pop1" class="clip" src="assets/pop.wav" data-start="{t_whats:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="18"></audio>
      <audio id="pop2" class="clip" src="assets/pop.wav" data-start="{t_insta:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="19"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // 1. Delante de su local, se balancea... y se larga.
      tl.fromTo("#s1 svg", {{ scale: 1.08, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 4.0, ease: "power1.out" }}, 0);
      tl.to("#paco1", {{ y: -12, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 7 }}, 0.2);
      tl.to("#paco1", {{ x: 1150, duration: 0.75, ease: "power2.in" }}, 3.8);
      // 2. ¿Por qué?
      tl.fromTo("#s2t", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {SC['s2'][0]+0.1});
      tl.fromTo("#s2t em", {{ rotation: -6 }}, {{ rotation: 0, duration: 0.3, ease: "back.out(3)" }}, {word_t(1,'por',5.5):.2f});
      // 3. Trabajando bajo el fregadero mientras el móvil no para.
      tl.fromTo("#s3 svg", {{ scale: 1.15, transformOrigin: "40% 65%" }}, {{ scale: 1, duration: 0.6, ease: "power2.out" }}, {SC['s3'][0]});
      tl.to("#pierna1", {{ rotation: 4, transformOrigin: "600px 1175px", duration: 0.25, yoyo: true, repeat: 15, ease: "sine.inOut" }}, {SC['s3'][0]+0.2});
      tl.to("#movil3", {{ rotation: -4, duration: 0.05, yoyo: true, repeat: 31, ease: "none" }}, {SC['s3'][0]+0.3});
      tl.to("#movil3", {{ rotation: -20, duration: 0.05, yoyo: true, repeat: 31, ease: "none" }}, {SC['s3'][0]+2.2});
      tl.to("#perdidas", {{ opacity: 1, duration: 0.15 }}, {SC['s3'][0]+1.9});
      const perd = {{ n: 1 }};
      tl.to(perd, {{ n: 14, duration: 2.6, ease: "power2.in", onUpdate: () => {{ document.querySelector("#nperd").textContent = Math.round(perd.n); }} }}, {SC['s3'][0]+1.9});
      tl.fromTo("#movil3", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.25, ease: "back.out(2)" }}, {t_telef:.2f});
      // 4. Giro de cámara: el perro con traje (Hacienda) sella "PAGAR".
      tl.fromTo("#s4 svg", {{ x: 1080, filter: "blur(18px)" }}, {{ x: 0, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }}, {SC['s4'][0]});
      tl.to("#perro", {{ rotation: 2, transformOrigin: "540px 1180px", duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {SC['s4'][0]+0.4});
      tl.to("#sello", {{ y: 160, duration: 0.15, ease: "power3.in" }}, {t_imp+0.12:.2f});
      tl.set("#sellado", {{ opacity: 1 }}, {t_imp+0.27:.2f});
      tl.to("#sello", {{ y: 0, duration: 0.3, ease: "power2.out" }}, {t_imp+0.3:.2f});
      tl.fromTo("#s4 svg", {{ y: 0 }}, {{ y: 10, duration: 0.05, yoyo: true, repeat: 3 }}, {t_imp+0.27:.2f});
      // 5. CTA
      tl.fromTo("#s5t", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {SC['s5'][0]+0.05});
      tl.fromTo("#s5t em", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2.5)" }}, {t_demo:.2f});
{items_js}
      tl.fromTo("#marca5", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {SC['s5'][0]+0.6});
      // 6. Vuelve el fontanero
      tl.fromTo("#paco6", {{ y: 900 }}, {{ y: 0, duration: 0.45, ease: "back.out(1.6)" }}, {SC['s6'][0]+0.05});
      tl.fromTo("#s6t", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {SC['s6'][0]+0.1});
      tl.to("#paco6", {{ rotation: 3, transformOrigin: "50% 100%", duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {SC['s6'][0]+0.6});
{caps_js}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open("/tmp/fonta/p/index.html", "w").write(html)
print(len(caps), "subtítulos")
