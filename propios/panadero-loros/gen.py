import json, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/loros"
v = json.load(open(f"{BASE}/voz.json"))
T = v["T"]; S = v["starts"]
SC = {"s1": (0, S[1] - 0.15), "s2": (S[1] - 0.15, S[2] - 0.15), "s3": (S[2] - 0.15, S[3] - 0.15),
      "s4": (S[3] - 0.15, S[4] - 0.15), "s5": (S[4] - 0.15, S[5] - 0.15), "s6": (S[5] - 0.15, T)}
INK = "#1d1b19"

def word_t(li, frag, default, n=0):
    hits = [w for w in v["words"] if w["l"] == li and frag.lower() in w["w"].lower()]
    return hits[n]["t0"] if len(hits) > n else default

# subtítulos en las escenas sin texto grande (frases 0, 2 y 3)
pages = []
for li in (0, 2, 3):
    ws = [w for w in v["words"] if w["l"] == li]; cur = []
    for i, w in enumerate(ws):
        cur.append(w)
        largo = len(" ".join(x["w"] for x in cur)); sig = len(ws[i + 1]["w"]) + 1 if i + 1 < len(ws) else 0
        if len(cur) == 3 or largo + sig > 16 or w["w"][-1] in ".,?…:" or i == len(ws) - 1:
            pages.append(cur); cur = []
caps = []
for k, p in enumerate(pages):
    t0 = p[0]["t0"] - 0.04
    t1 = pages[k + 1][0]["t0"] - 0.04 if k + 1 < len(pages) and pages[k + 1][0]["l"] == p[0]["l"] else p[-1]["t1"] + 0.25
    caps.append((k, t0, t1 - t0, " ".join(w["w"] for w in p).strip(".,…:").upper()))
caps_html = "\n".join(f'      <div id="cap{k}" class="cap clip" data-start="{t0:.3f}" data-duration="{d:.3f}" data-track-index="9"><span>{txt}</span></div>' for k, t0, d, txt in caps)
caps_js = "\n".join(f'      tl.fromTo("#cap{k} span", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.14, ease: "back.out(2.5)" }}, {t0:.3f});' for k, t0, d, txt in caps)

def loro(id_, cuerpo="#3fae5a", cabeza="#e5463b", flip=False):
    tr = ' transform="scale(-1 1) translate(-240 0)"' if flip else ""
    return f'''<g id="{id_}" class="mano"><g{tr}>
      <path d="M95 300 Q70 380 85 430 L115 360 Z" fill="#2f7fd1" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
      <ellipse cx="125" cy="230" rx="62" ry="95" fill="{cuerpo}" stroke="{INK}" stroke-width="7"/>
      <path d="M90 200 Q60 260 95 320 Q120 280 110 210 Z" fill="#2c8c45" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
      <circle cx="135" cy="115" r="55" fill="{cabeza}" stroke="{INK}" stroke-width="7"/>
      <circle cx="150" cy="105" r="17" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="154" cy="106" r="8" fill="{INK}"/>
      <path d="M178 110 Q215 118 205 150 Q190 165 170 145 Z" fill="#f2c230" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M110 320 L105 345 M140 322 L145 347" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
    </g></g>'''

def panadero(id_):
    return f'''<g id="{id_}" class="mano">
      <path d="M150 520 L140 660 L205 660 L208 540 Z M250 520 L262 660 L320 660 L300 520 Z" fill="#6b5a4a" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M118 662 Q120 640 145 640 L210 640 Q222 664 210 680 L120 680 Q110 674 118 662 Z M250 662 Q252 640 277 640 L330 640 Q345 664 335 680 L252 680 Q240 674 250 662 Z" fill="{INK}"/>
      <path d="M125 300 Q200 270 280 300 L310 540 Q205 575 110 540 Z" fill="#f7f2ea" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M150 340 Q205 330 260 340 L270 520 Q205 540 140 520 Z" fill="#e9a35a" stroke="{INK}" stroke-width="6" stroke-linejoin="round" opacity="0.9"/>
      <path d="M128 310 Q80 380 92 470" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/><path d="M128 310 Q80 380 92 470" fill="none" stroke="#f7f2ea" stroke-width="30" stroke-linecap="round"/>
      <path d="M282 310 Q330 370 340 440" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/><path d="M282 310 Q330 370 340 440" fill="none" stroke="#f7f2ea" stroke-width="30" stroke-linecap="round"/>
      <circle cx="92" cy="478" r="24" fill="#f2c39b" stroke="{INK}" stroke-width="7"/><circle cx="340" cy="450" r="24" fill="#f2c39b" stroke="{INK}" stroke-width="7"/>
      <path d="M318 430 Q360 380 420 400 Q440 420 410 440 Q360 450 330 465 Z" fill="#d9954c" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M350 415 L360 435 M375 405 L385 428 M400 405 L405 425" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
      <ellipse cx="205" cy="215" rx="98" ry="104" fill="#f2c39b" stroke="{INK}" stroke-width="8"/>
      <path d="M115 150 Q95 70 150 60 Q170 10 215 40 Q260 10 280 60 Q330 70 300 150 Z" fill="#fff" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <rect x="118" y="140" width="180" height="34" rx="8" fill="#fff" stroke="{INK}" stroke-width="7"/>
      <circle cx="172" cy="215" r="10" fill="{INK}"/><circle cx="236" cy="215" r="10" fill="{INK}"/>
      <path d="M160 270 Q205 300 250 270" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
      <circle cx="150" cy="250" r="14" fill="#f29a8a" opacity="0.6"/><circle cx="262" cy="250" r="14" fill="#f29a8a" opacity="0.6"/>
    </g>'''

def tienda(nombre, color, toldo):
    return f'''<g class="mano">
      <rect x="70" y="420" width="940" height="900" fill="#efe4d4" stroke="{INK}" stroke-width="9"/>
      <rect x="110" y="470" width="860" height="170" rx="18" fill="{color}" stroke="{INK}" stroke-width="9"/>
      <text x="540" y="585" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="{96 if len(nombre) < 16 else 70}" fill="#fffaf2">{nombre}</text>
      <path d="M95 690 L985 690 L950 760 L130 760 Z" fill="{toldo}" stroke="{INK}" stroke-width="8"/>
      <rect x="150" y="830" width="420" height="330" rx="10" fill="#bcd6dc" stroke="{INK}" stroke-width="9"/>
      <path d="M200 1080 Q260 1000 330 1080 Z M350 1080 Q410 990 480 1080 Z" fill="#d9954c" stroke="{INK}" stroke-width="6"/>
      <rect x="650" y="830" width="260" height="490" rx="8" fill="#9b6b48" stroke="{INK}" stroke-width="9"/><circle cx="875" cy="1080" r="13" fill="{INK}"/>
      <rect x="0" y="1320" width="1080" height="600" fill="#d8cfc2"/><path d="M0 1320 L1080 1320" stroke="{INK}" stroke-width="9"/>
    </g>'''

movil = f'''<g class="mano">
      <rect x="-80" y="-145" width="160" height="290" rx="30" fill="{INK}"/><rect x="-64" y="-125" width="128" height="250" rx="20" fill="#6fd08c"/>
      <path d="M-26 -10 Q-20 -40 0 -40 L10 -40 M-30 0 L-30 20 Q-30 35 -15 35 L20 35" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>
      <path d="M-115 -60 Q-140 0 -115 60 M115 -60 Q140 0 115 60" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
    </g>'''

cliente = f'''<g class="mano">
      <path d="M130 760 Q130 560 300 540 Q470 560 470 760 Z" fill="#7c9a7e" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
      <ellipse cx="300" cy="420" rx="110" ry="120" fill="#e8846e" stroke="{INK}" stroke-width="8"/>
      <path d="M200 360 Q210 280 300 285 Q395 280 405 360 Q360 330 300 335 Q240 330 200 360 Z" fill="#3b2a20" stroke="{INK}" stroke-width="6"/>
      <path d="M245 395 L285 410 M355 395 L315 410" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>
      <circle cx="262" cy="425" r="9" fill="{INK}"/><circle cx="338" cy="425" r="9" fill="{INK}"/>
      <path d="M265 485 Q300 465 335 485" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
      <rect x="395" y="360" width="60" height="110" rx="14" fill="{INK}" transform="rotate(15 425 415)"/>
      <path d="M420 300 Q440 260 420 230 M460 300 Q480 255 455 220 M380 300 Q395 265 380 235" fill="none" stroke="#9aa0a6" stroke-width="10" stroke-linecap="round" id="humo"/>
    </g>'''

items = [("Coge las llamadas", word_t(4, "llamadas", 16.0)), ("Contesta los WhatsApps", word_t(4, "whatsapp", 17.0)), ("Apunta los encargos", word_t(4, "encargos", 18.5))]
items_html = "\n".join(f'        <div id="it{i}" class="item"><div class="chk">✓</div><span>{txt}</span></div>' for i, (txt, _) in enumerate(items))
items_js = "\n".join(f'      tl.fromTo("#it{i}", {{ x: -80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }}, {t-0.05:.2f});\n      tl.fromTo("#it{i} .chk", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, ease: "back.out(3)" }}, {t+0.12:.2f});' for i, (txt, t) in enumerate(items))
digas = [word_t(2, "diga", S[2] + 2.0 + 0.5 * k, k) for k in range(3)]
def st(k): return SC[k][0]
def du(k): return SC[k][1] - SC[k][0]

html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      /* Historia absurda: el panadero de los tres loros (banco historias/absurdas.md, 25-nov). Estilo de dibujo a mano. */
      :root {{ --crema: #f0eee6; --tinta: #1d1b19; --naranja: #e8692e; --font-display: "Oswald"; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--crema); }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter"; }}
      .esc {{ position: absolute; inset: 0; overflow: hidden; background: var(--crema); }}
      svg.lienzo {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .mano {{ filter: url(#lapiz); }}
      .cap {{ position: absolute; left: 0; right: 0; top: 1500px; display: flex; justify-content: center; }}
      .cap span {{ display: inline-block; background: var(--tinta); color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 82px; letter-spacing: 1px; padding: 6px 30px 12px; border-radius: 18px; }}
      .grande {{ position: absolute; left: 80px; right: 80px; text-align: center; font-family: "Oswald"; font-weight: 700; line-height: 1.02; color: var(--tinta); }}
      .grande em {{ font-style: normal; color: var(--naranja); }}
      .bocadillo {{ position: absolute; padding: 18px 34px 24px; border: 7px solid var(--tinta); border-radius: 40px; background: #fff; font-family: "Oswald"; font-weight: 700; font-size: 72px; color: var(--tinta); }}
      #lista {{ position: absolute; top: 760px; left: 80px; right: 80px; }}
      .item {{ display: flex; align-items: center; gap: 30px; height: 150px; margin-bottom: 30px; padding: 0 40px; border: 7px solid var(--tinta); border-radius: 34px; background: #fffaf2; font-weight: 800; font-size: 56px; color: var(--tinta); }}
      .chk {{ width: 84px; height: 84px; border-radius: 42px; background: var(--naranja); color: #fff; font-size: 54px; font-weight: 900; display: flex; align-items: center; justify-content: center; border: 6px solid var(--tinta); flex: none; }}
      .marca {{ position: absolute; left: 0; right: 0; display: flex; align-items: center; justify-content: center; gap: 24px; font-weight: 900; font-size: 64px; color: var(--tinta); }}
      .marca img {{ width: 96px; height: 96px; }}
      #pill {{ position: absolute; top: 560px; left: 0; right: 0; display: flex; justify-content: center; }}
      #pill span {{ padding: 20px 60px 30px; border-radius: 40px; background: var(--naranja); color: #fff; font-family: "Oswald"; font-weight: 700; font-size: 150px; border: 8px solid var(--tinta); }}
    </style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><defs>
      <filter id="lapiz" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="r"/><feDisplacementMap in="SourceGraphic" in2="r" scale="5"/></filter>
    </defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">

      <div id="s1" class="esc clip" data-start="{st('s1')}" data-duration="{du('s1'):.3f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#f6e1c4"/>{tienda("PANADERÍA LOLA", "#c9783a", "#e8692e")}
          <g transform="translate(150 780)"><g id="pan1">{panadero("panA")}</g></g>
          <rect x="560" y="1010" width="420" height="22" rx="10" fill="#8a5d3d" stroke="{INK}" stroke-width="7"/>
          <g transform="translate(540 690) scale(0.85)"><g id="l1a">{loro("la1")}</g></g>
          <g transform="translate(680 690) scale(0.85)"><g id="l1b">{loro("lb1", "#f2c230", "#3fae5a")}</g></g>
          <g transform="translate(820 690) scale(0.85)"><g id="l1c">{loro("lc1", "#2f7fd1", "#f2c230")}</g></g></svg>
      </div>

      <div id="s2" class="esc clip" data-start="{st('s2'):.3f}" data-duration="{du('s2'):.3f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><g opacity="0.14" transform="translate(140 1000) scale(1.6)">{loro("lfant")}</g></svg>
        <div id="s2t" class="grande" style="top:620px;font-size:170px">Y no,<br /><em>no es broma.</em></div>
      </div>

      <div id="s3" class="esc clip" data-start="{st('s3'):.3f}" data-duration="{du('s3'):.3f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#f6e1c4"/>
          <rect x="0" y="1150" width="1080" height="770" fill="#c9a27a" class="mano"/><path d="M0 1150 L1080 1150" stroke="{INK}" stroke-width="9"/>
          <g transform="translate(540 1040)"><g id="movil3">{movil}</g></g>
          <g transform="translate(-20 520) scale(1.45)"><g id="l3a">{loro("la3")}</g></g>
          <g transform="translate(370 440) scale(1.45)"><g id="l3b">{loro("lb3", "#f2c230", "#3fae5a")}</g></g>
          <g transform="translate(740 520) scale(1.45)"><g id="l3c">{loro("lc3", "#2f7fd1", "#f2c230", True)}</g></g></svg>
        <div id="d1" class="bocadillo" style="left:40px;top:330px">¿DIGA?</div>
        <div id="d2" class="bocadillo" style="left:390px;top:240px">¿DIGA?</div>
        <div id="d3" class="bocadillo" style="left:720px;top:330px">¿DIGA?</div>
      </div>

      <div id="s4" class="esc clip" data-start="{st('s4'):.3f}" data-duration="{du('s4'):.3f}" data-track-index="0">
        <svg class="lienzo" viewBox="0 0 1080 1920"><rect width="1080" height="1920" fill="#dfe8ea"/>
          <g transform="translate(240 260)"><g id="cli">{cliente}</g></g>
          <g transform="translate(0 520)"><g id="enfrente">{tienda("PANADERÍA DE ENFRENTE", "#3f7d5a", "#7c9a7e")}</g></g></svg>
      </div>

      <div id="s5" class="esc clip" data-start="{st('s5'):.3f}" data-duration="{du('s5'):.3f}" data-track-index="0">
        <div id="s5t" class="grande" style="top:300px;font-size:120px;text-align:left">No hacen falta<br /><em>loros.</em></div>
        <div id="lista">
{items_html}
        </div>
        <div id="badge" class="grande" style="top:560px;font-size:70px;font-family:Inter;font-weight:900;text-align:left;color:var(--naranja)">Tu recepcionista con IA:</div>
        <div id="m5" class="marca" style="bottom:230px"><img src="assets/logo.svg" alt="" />norte.local</div>
      </div>

      <div id="s6" class="esc clip" data-start="{st('s6'):.3f}" data-duration="{du('s6'):.3f}" data-track-index="0">
        <div class="grande" style="top:380px;font-size:130px">Comenta</div>
        <div id="pill"><span>RECEPCIÓN</span></div>
        <div class="grande" style="top:880px;font-size:64px;font-family:Inter;font-weight:800">y te la monto en tu negocio</div>
        <svg class="lienzo" viewBox="0 0 1080 1920">
          <g transform="translate(120 1080)"><g id="l6a">{loro("la6")}</g></g>
          <g transform="translate(420 1040)"><g id="l6b">{loro("lb6", "#f2c230", "#3fae5a")}</g></g>
          <g transform="translate(720 1080)"><g id="l6c">{loro("lc6", "#2f7fd1", "#f2c230", True)}</g></g></svg>
        <div class="marca" style="bottom:120px"><img src="assets/logo.svg" alt="" />norte.local</div>
      </div>

{caps_html}

      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-duration="{T}" data-volume="1" data-track-index="10"></audio>
      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="0" data-duration="{T}" data-media-start="0" data-volume="0.25" data-fade-out="0.8" data-track-index="11"></audio>
      <audio id="ring" class="clip" src="assets/ring.wav" data-start="{st('s3')+0.1:.2f}" data-duration="1.6" data-volume="0.3" data-track-index="12"></audio>
      <audio id="pi1" class="clip" src="assets/pop.wav" data-start="{digas[0]:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="13"></audio>
      <audio id="pi2" class="clip" src="assets/pop.wav" data-start="{digas[1]:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="14"></audio>
      <audio id="pi3" class="clip" src="assets/pop.wav" data-start="{digas[2]:.2f}" data-duration="0.3" data-volume="0.5" data-track-index="15"></audio>
      <audio id="wh" class="clip" src="assets/whoosh.wav" data-start="{st('s4')+1.4:.2f}" data-duration="0.45" data-volume="0.6" data-track-index="16"></audio>
      <audio id="boing" class="clip" src="assets/boing.wav" data-start="{st('s6')+0.1:.2f}" data-duration="0.5" data-volume="0.6" data-track-index="17"></audio>
      <audio id="po0" class="clip" src="assets/pop.wav" data-start="{items[0][1]:.2f}" data-duration="0.3" data-volume="0.45" data-track-index="18"></audio>
      <audio id="po1" class="clip" src="assets/pop.wav" data-start="{items[1][1]:.2f}" data-duration="0.3" data-volume="0.45" data-track-index="19"></audio>
      <audio id="po2" class="clip" src="assets/pop.wav" data-start="{items[2][1]:.2f}" data-duration="0.3" data-volume="0.45" data-track-index="20"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#s1 svg", {{ scale: 1.08, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 3.2, ease: "power1.out" }}, 0);
      ["#l1a", "#l1b", "#l1c"].forEach((s, i) => {{
        tl.fromTo(s, {{ y: -500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }}, {word_t(0, "loros", 1.6):.2f} - 0.3 + i * 0.12);
        tl.to(s, {{ rotation: 6, transformOrigin: "50% 100%", duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {word_t(0, "loros", 1.6):.2f} + 0.2 + i * 0.1);
      }});
      tl.to("#pan1", {{ y: -10, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 0.2);
      tl.fromTo("#s2t", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {st('s2')+0.05:.2f});
      tl.fromTo("#s3 svg", {{ scale: 1.12, transformOrigin: "50% 60%" }}, {{ scale: 1, duration: 0.5, ease: "power2.out" }}, {st('s3'):.2f});
      tl.to("#movil3", {{ rotation: 8, duration: 0.05, yoyo: true, repeat: 31, ease: "none" }}, {st('s3')+0.1:.2f});
      [["#d1", "#l3a"], ["#d2", "#l3b"], ["#d3", "#l3c"]].forEach(([d, l], i) => {{
        const t = [{digas[0]:.2f}, {digas[1]:.2f}, {digas[2]:.2f}][i];
        tl.fromTo(d, {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.2, ease: "back.out(3)" }}, t - 0.05);
        tl.fromTo(l, {{ y: 0 }}, {{ y: -40, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }}, t - 0.05);
      }});
      tl.set(["#d1", "#d2", "#d3"], {{ opacity: 0 }}, 0);
      tl.fromTo("#cli", {{ x: -500 }}, {{ x: 0, duration: 0.35, ease: "power3.out" }}, {st('s4'):.2f});
      tl.fromTo("#humo", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, yoyo: true, repeat: 3 }}, {st('s4')+0.4:.2f});
      tl.fromTo("#enfrente", {{ x: 1100 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, {word_t(3, "enfrente", st('s4') + 2.0) - 0.6:.2f});
      tl.fromTo("#s5t", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {st('s5')+0.05:.2f});
      tl.fromTo("#badge", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }}, {word_t(4, "recepcionista", st('s5') + 1.5) - 0.05:.2f});
{items_js}
      tl.fromTo("#m5", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {st('s5')+0.6:.2f});
      tl.fromTo("#pill span", {{ scale: 0.3, rotation: -8 }}, {{ scale: 1, rotation: -3, duration: 0.35, ease: "back.out(2.2)" }}, {st('s6')+0.1:.2f});
      ["#l6a", "#l6b", "#l6c"].forEach((s, i) => tl.fromTo(s, {{ y: 900 }}, {{ y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {st('s6')+0.15:.2f} + i * 0.1));
      ["#l6a", "#l6b", "#l6c"].forEach((s, i) => tl.to(s, {{ rotation: 5, transformOrigin: "50% 100%", duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {st('s6')+0.6:.2f} + i * 0.08));
{caps_js}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(f"{BASE}/p/index.html", "w").write(html)
print("ok", T, digas)
