D = 8.366667
E = {"e1": (0, 0.7), "e2": (0.7, 1.6), "e3": (1.6, 3.4), "e4a": (3.4, 4.0), "e4b": (4.0, 4.6), "e4c": (4.6, 5.2), "e5": (5.2, 6.4), "e6": (6.4, 8.8)}
T = D + 8.8
def st(k): return D + E[k][0]
def du(k): return E[k][1] - E[k][0]

ICON = {
 "tel": '<svg viewBox="0 0 100 100" width="210" height="210"><path d="M30 15 L42 15 L50 35 L40 42 Q48 60 60 66 L66 56 L86 64 L86 76 Q84 88 70 88 Q20 82 14 30 Q14 15 30 15 Z" fill="currentColor"/></svg>',
 "chat": '<svg viewBox="0 0 100 100" width="210" height="210"><path d="M50 12 Q88 12 88 46 Q88 80 50 80 Q42 80 34 78 L16 88 L22 70 Q12 60 12 46 Q12 12 50 12 Z" fill="currentColor"/></svg>',
 "cal": '<svg viewBox="0 0 100 100" width="210" height="210"><rect x="12" y="20" width="76" height="68" rx="10" fill="currentColor"/><rect x="12" y="34" width="76" height="8" fill="#121110" opacity="0.35"/><rect x="26" y="10" width="10" height="20" rx="4" fill="currentColor"/><rect x="64" y="10" width="10" height="20" rx="4" fill="currentColor"/><path d="M32 62 L45 74 L70 50" fill="none" stroke="#121110" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      /* Extracto literal (Hugo, 24-nov) hasta que la bola choca con la cámara + edit propio de norte.local. */
      :root {{ --negro: #121110; --naranja: #ff5a14; --crema: #f6f0e7; --font-display: "Oswald"; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--negro); }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter"; }}
      #extracto {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .esc {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: var(--negro); color: #fff; overflow: hidden; }}
      .naranja {{ background: var(--naranja); }}
      .crema {{ background: var(--crema); color: var(--negro); }}
      .k {{ font-family: "Oswald"; font-weight: 700; font-style: italic; text-transform: uppercase; line-height: 0.95; text-align: center; }}
      #e1 img {{ width: 300px; height: 300px; }}
      #e1 .marca {{ margin-top: 40px; font-weight: 900; font-size: 92px; letter-spacing: -2px; }}
      #e2 .k {{ font-size: 132px; }}
      #e2 .k em {{ font-style: italic; color: var(--naranja); }}
      #movil {{ width: 820px; height: 1340px; border-radius: 90px; background: #1d1c1b; border: 14px solid #2b2a28; box-shadow: 0 50px 120px rgba(255,90,20,0.25); padding: 60px 40px; display: flex; flex-direction: column; gap: 28px; }}
      #movil .cab {{ display: flex; align-items: center; gap: 22px; padding-bottom: 26px; border-bottom: 2px solid #333; }}
      #movil .av {{ width: 84px; height: 84px; border-radius: 42px; background: var(--naranja); display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 40px; }}
      #movil .nom {{ font-weight: 800; font-size: 40px; }}
      #movil .on {{ font-size: 28px; color: #5fd47f; font-weight: 600; }}
      .bur {{ max-width: 88%; padding: 30px 38px; border-radius: 40px; font-size: 52px; font-weight: 600; line-height: 1.3; }}
      .cli {{ background: #2e2d2b; align-self: flex-start; }}
      .ia {{ background: var(--naranja); align-self: flex-end; }}
      #esc3t {{ position: absolute; top: 120px; font-size: 64px; }}
      .card .k {{ font-size: 150px; margin-top: 40px; }}
      .card svg {{ color: currentColor; }}
      #e5 .k {{ font-size: 400px; color: var(--naranja); }}
      #e5 .sub {{ font-family: "Oswald"; font-style: italic; font-weight: 700; font-size: 90px; text-transform: uppercase; margin-top: 20px; }}
      #e6 .a {{ font-size: 130px; }}
      #e6 .pill {{ margin-top: 30px; padding: 20px 60px 30px; border-radius: 40px; background: var(--naranja); color: #fff; font-family: "Oswald"; font-weight: 700; font-style: italic; font-size: 150px; }}
      #e6 .b {{ margin-top: 40px; font-size: 64px; font-weight: 800; }}
      #e6 .m {{ position: absolute; bottom: 260px; display: flex; align-items: center; gap: 22px; font-weight: 900; font-size: 64px; }}
      #e6 .m img {{ width: 96px; height: 96px; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T:.4f}" data-width="1080" data-height="1920">
      <video id="extracto" class="clip" src="assets/extracto.mp4" muted playsinline data-start="0" data-duration="{D}" data-track-index="0"></video>
      <audio id="extracto-audio" class="clip" src="assets/extracto.mp4" data-start="0" data-duration="{D}" data-volume="1" data-track-index="5"></audio>

      <div id="e1" class="esc clip" data-start="{st('e1'):.4f}" data-duration="{du('e1')}" data-track-index="1"><img id="logo1" src="assets/logo.svg" alt="" /><div class="marca">norte.local</div></div>
      <div id="e2" class="esc clip" data-start="{st('e2'):.4f}" data-duration="{du('e2')}" data-track-index="1"><div class="k"><span id="w1">Tu</span><br /><span id="w2">recepcionista</span><br /><em id="w3">con IA</em></div></div>
      <div id="e3" class="esc crema clip" data-start="{st('e3'):.4f}" data-duration="{du('e3'):.2f}" data-track-index="1">
        <div id="movil">
          <div class="cab"><div class="av">N</div><div><div class="nom" style="color:#fff">Tu negocio</div><div class="on">responde al momento</div></div></div>
          <div id="b1" class="bur cli" style="color:#fff">¿Tenéis hueco mañana?</div>
          <div id="b2" class="bur ia" style="color:#fff">¡Claro! Mañana a las 10:00 o a las 12:30. ¿Cuál te viene mejor?</div>
          <div id="b3" class="bur cli" style="color:#fff">A las 10 perfecto</div>
          <div id="b4" class="bur ia" style="color:#fff">Hecho. Te he reservado a las 10:00</div>
        </div>
      </div>
      <div id="e4a" class="esc naranja card clip" data-start="{st('e4a'):.4f}" data-duration="{du('e4a'):.2f}" data-track-index="1">{ICON["tel"]}<div class="k">Coge<br />llamadas</div></div>
      <div id="e4b" class="esc card clip" data-start="{st('e4b'):.4f}" data-duration="{du('e4b'):.2f}" data-track-index="1"><span style="color:var(--naranja)">{ICON["chat"]}</span><div class="k">Contesta<br />WhatsApp</div></div>
      <div id="e4c" class="esc naranja card clip" data-start="{st('e4c'):.4f}" data-duration="{du('e4c'):.2f}" data-track-index="1">{ICON["cal"]}<div class="k">Agenda<br />citas</div></div>
      <div id="e5" class="esc clip" data-start="{st('e5'):.4f}" data-duration="{du('e5'):.2f}" data-track-index="1"><div class="k">24/7</div><div class="sub">aunque estés currando</div></div>
      <div id="e6" class="esc crema clip" data-start="{st('e6'):.4f}" data-duration="{du('e6'):.2f}" data-track-index="1">
        <div class="k a">Comenta</div><div class="pill">RECEPCIÓN</div><div class="b">y te enseño una demo gratis</div>
        <div class="m"><img src="assets/logo.svg" alt="" />norte.local</div>
      </div>
      <div id="flash" class="clip" data-start="{D-0.02:.4f}" data-duration="0.3" data-track-index="2"></div>

      <audio id="golpe" class="clip" src="assets/golpe.wav" data-start="{D-0.03:.3f}" data-duration="0.4" data-volume="1" data-track-index="6"></audio>
      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="{D:.4f}" data-duration="{T-D:.4f}" data-media-start="0" data-volume="0.85" data-fade-out="0.6" data-track-index="7"></audio>
      <audio id="wh1" class="clip" src="assets/whoosh.wav" data-start="{st('e2')-0.1:.3f}" data-duration="0.3" data-volume="0.6" data-track-index="8"></audio>
      <audio id="wh2" class="clip" src="assets/whoosh.wav" data-start="{st('e3')-0.1:.3f}" data-duration="0.3" data-volume="0.6" data-track-index="9"></audio>
      <audio id="p1" class="clip" src="assets/pop.wav" data-start="{st('e3')+0.35:.3f}" data-duration="0.25" data-volume="0.5" data-track-index="10"></audio>
      <audio id="p2" class="clip" src="assets/ding.wav" data-start="{st('e3')+0.8:.3f}" data-duration="0.35" data-volume="0.45" data-track-index="11"></audio>
      <audio id="g1" class="clip" src="assets/golpe.wav" data-start="{st('e4a'):.3f}" data-duration="0.4" data-volume="0.45" data-track-index="12"></audio>
      <audio id="g2" class="clip" src="assets/golpe.wav" data-start="{st('e4b'):.3f}" data-duration="0.4" data-volume="0.45" data-track-index="13"></audio>
      <audio id="g3" class="clip" src="assets/golpe.wav" data-start="{st('e4c'):.3f}" data-duration="0.4" data-volume="0.45" data-track-index="14"></audio>
      <audio id="g4" class="clip" src="assets/golpe.wav" data-start="{st('e5'):.3f}" data-duration="0.4" data-volume="0.6" data-track-index="15"></audio>
      <audio id="wh3" class="clip" src="assets/whoosh.wav" data-start="{st('e6')-0.1:.3f}" data-duration="0.3" data-volume="0.6" data-track-index="16"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#flash", {{ opacity: 0.95 }}, {{ opacity: 0, duration: 0.28, ease: "power2.out" }}, {D-0.02:.4f});
      // logo que entra de golpe con temblor
      tl.fromTo("#logo1", {{ scale: 3.2, rotation: -25 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "back.out(1.4)" }}, {st('e1'):.4f});
      tl.fromTo("#e1 .marca", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {st('e1')+0.15:.4f});
      tl.fromTo("#e1", {{ x: 0 }}, {{ x: 14, duration: 0.04, yoyo: true, repeat: 5 }}, {st('e1')+0.28:.4f});
      // texto cinético
      ["#w1", "#w2", "#w3"].forEach((s, i) => tl.fromTo(s, {{ y: 140, opacity: 0, skewX: -12 }}, {{ y: 0, opacity: 1, skewX: 0, duration: 0.22, ease: "back.out(1.8)" }}, {st('e2'):.4f} + i * 0.12));
      tl.fromTo("#e2 .k", {{ scale: 1 }}, {{ scale: 1.08, duration: {du('e2')}, ease: "none" }}, {st('e2'):.4f});
      // chat
      tl.fromTo("#movil", {{ y: 900, rotation: 8 }}, {{ y: 0, rotation: 0, duration: 0.4, ease: "power3.out" }}, {st('e3'):.4f});
      [["#b1", 0.35], ["#b2", 0.8], ["#b3", 1.25], ["#b4", 1.5]].forEach(([s, t]) => tl.fromTo(s, {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.2, ease: "back.out(2)" }}, {st('e3'):.4f} + t));
      // tarjetas de golpe
      ["#e4a", "#e4b", "#e4c"].forEach((s, i) => {{
        tl.fromTo(s + " .k", {{ scale: 1.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.18, ease: "power4.out" }}, {st('e4a'):.4f} + i * 0.6);
        tl.fromTo(s + " svg", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.25, ease: "back.out(2.5)" }}, {st('e4a'):.4f} + i * 0.6 + 0.05);
      }});
      tl.fromTo("#e5 .k", {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "power4.out" }}, {st('e5'):.4f});
      tl.fromTo("#e5 .sub", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {st('e5')+0.3:.4f});
      tl.fromTo("#e5", {{ x: 0 }}, {{ x: 12, duration: 0.04, yoyo: true, repeat: 5 }}, {st('e5')+0.2:.4f});
      // CTA
      tl.fromTo("#e6 .a", {{ y: -80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {st('e6'):.4f});
      tl.fromTo("#e6 .pill", {{ scale: 0.3, rotation: -8 }}, {{ scale: 1, rotation: -3, duration: 0.35, ease: "back.out(2.2)" }}, {st('e6')+0.15:.4f});
      tl.to("#e6 .pill", {{ scale: 1.06, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {st('e6')+0.6:.4f});
      tl.fromTo("#e6 .b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {st('e6')+0.4:.4f});
      tl.fromTo("#e6 .m", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {st('e6')+0.6:.4f});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open("/tmp/r3/p/index.html", "w").write(html)
print(round(T, 2))
