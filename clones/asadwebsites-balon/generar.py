import json
D=2.1
cards=[("t1","claro",1.0,'<div id="t1x" class="txt s">¿necesitas<br />recepcionista?</div>'),
("t2","oscuro",1.033333,'<div id="t2x" class="txt g">24/7.</div>'),
("t3","claro",1.033333,'<div id="t3x" class="txt g">rápida.</div>'),
("t4","oscuro",1.033333,'<div id="t4x" class="txt g">agenda sola.</div>'),
("t5","claro",1.8,'<div id="t5x" class="txt m">Comenta "<span class="acento">RECEPCIÓN</span>"<br />para una demo gratis</div>'),
("t6","oscuro",1.7,'<img id="t6logo" class="logo" src="assets/logo.svg" alt="" />\n        <div id="t6x" class="txt m">Recepcionista con IA<br />para negocios locales</div>'),
("t7","oscuro",2.4,'<div id="cierre-caja">\n          <img id="t7logo" class="logo" src="assets/logo.svg" alt="" style="margin-bottom: 0" />\n          <div id="t7marca" class="marca">norte.local</div>\n        </div>')]
t=D; html=[]; starts={}
for cid,est,dur,inner in cards:
    starts[cid]=round(t,6)
    html.append(f'      <div id="{cid}" class="tarjeta {est} clip" data-start="{t:.6f}" data-duration="{dur}" data-track-index="1">\n        {inner}\n      </div>')
    t+=dur
T=t
jg=json.dumps([["#t%dx"%i, starts["t%d"%i]] for i in range(1,7)])
notifs=[("Marta","¿Tenéis hueco mañana?"),("Pedro","¿Me podéis mirar los frenos?"),("Lucía","Hola!! ¿Abrís el sábado?"),("Cliente nuevo","¿Precio de una revisión?"),("Carmen","¿Me llamáis cuando podáis?"),("+34 6•• ••• 218","Llamada perdida")]
nhtml="\n".join(f'              <div id="n{i}" class="notif"><div class="napp">{"☎" if i==5 else "✆"}</div><div class="ntxt"><b>{a}</b><span>{b}</span></div><div class="nh">ahora</div></div>' for i,(a,b) in enumerate(notifs))
s=open('index.html').read()
head=s[:s.index('<body>')]
css="""      #gancho { position: absolute; inset: 0; background: radial-gradient(circle at 50% 38%, #3a2c24 0%, #171210 55%, #0b0908 100%); }
      #movil { position: absolute; left: 190px; top: 250px; width: 700px; height: 1420px; border-radius: 96px; background: #0c0c0d; padding: 22px; box-shadow: 0 60px 120px rgba(0,0,0,0.6), 0 0 0 3px #2e2e30; }
      #pantalla { position: relative; width: 100%; height: 100%; border-radius: 76px; overflow: hidden; background: linear-gradient(165deg, #ff8a3d 0%, #e25434 45%, #7a2a1c 100%); }
      #isla { position: absolute; top: 26px; left: 50%; width: 200px; height: 56px; margin-left: -100px; border-radius: 30px; background: #000; }
      #hora { position: absolute; top: 150px; width: 100%; text-align: center; font-family: "Inter"; font-weight: 700; font-size: 190px; color: #fff; letter-spacing: -6px; }
      #fecha { position: absolute; top: 120px; width: 100%; text-align: center; font-family: "Inter"; font-weight: 700; font-size: 38px; color: rgba(255,255,255,0.9); }
      #lista { position: absolute; top: 430px; left: 28px; right: 28px; }
      .notif { display: flex; align-items: center; gap: 22px; height: 128px; margin-bottom: 14px; padding: 0 26px; border-radius: 40px; background: rgba(255,255,255,0.9); font-family: "Inter"; }
      .napp { width: 74px; height: 74px; border-radius: 20px; background: #25d366; color: #fff; font-size: 40px; display: flex; align-items: center; justify-content: center; flex: none; }
      #n5 .napp { background: #e5342b; }
      .ntxt { display: flex; flex-direction: column; min-width: 0; flex: 1; }
      .ntxt b { font-size: 33px; color: #111; }
      .ntxt span { font-size: 30px; color: #444; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .nh { font-size: 26px; color: #666; align-self: flex-start; margin-top: 26px; }
      #contador { position: absolute; top: 210px; right: 150px; min-width: 130px; height: 130px; padding: 0 30px; border-radius: 65px; background: #e5342b; color: #fff; font-family: "Inter"; font-weight: 900; font-size: 68px; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px rgba(229,52,43,0.45); }
      #titulo-g { position: absolute; top: 110px; width: 100%; text-align: center; font-family: "Oswald"; font-weight: 700; font-style: italic; font-size: 84px; color: #fff; }
"""
head=head.replace("      #chut { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }\n",css)
aud=[("vibra","vibra.wav",0.15,0.75,0.8),("ding1","ding.wav",0.35,0.35,0.5),("ding2","ding.wav",0.6,0.35,0.5),("ding3","ding.wav",0.85,0.35,0.5),
("ding4","ding.wav",1.1,0.35,0.5),("vibra2","vibra.wav",1.15,0.75,0.8),("ding5","ding.wav",1.35,0.35,0.5),("golpe","golpe.wav",D-0.03,0.4,1)]
ah="\n".join(f'      <audio id="{i}" class="clip" src="assets/{f}" data-start="{st:.2f}" data-duration="{du}" data-volume="{v}" data-track-index="{2+k}"></audio>' for k,(i,f,st,du,v) in enumerate(aud))
body=f'''<body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T:.6f}" data-width="1080" data-height="1920">
      <div id="gancho" class="clip" data-start="0" data-duration="{D}" data-track-index="0">
        <div id="titulo-g">Viernes, 21:47…</div>
        <div id="movil">
          <div id="pantalla">
            <div id="isla"></div>
            <div id="fecha">viernes 22 de noviembre</div>
            <div id="hora">21:47</div>
            <div id="lista">
{nhtml}
            </div>
          </div>
        </div>
        <div id="contador">0</div>
      </div>

{chr(10).join(html)}

{ah}
      <audio id="musica" class="clip" src="assets/musica.mp3" data-start="{D}" data-duration="{T-D:.6f}" data-media-start="0" data-volume="0.9" data-fade-out="0.5" data-track-index="12"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#movil", {{ y: 80, scale: 0.94 }}, {{ y: 0, scale: 1, duration: 0.35, ease: "power3.out" }}, 0);
      tl.fromTo("#titulo-g", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, 0.05);
      [0.35, 0.6, 0.85, 1.1, 1.35, 1.6].forEach((t, i) => {{
        tl.fromTo("#n" + i, {{ y: -120, opacity: 0, scale: 0.9 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.22, ease: "back.out(1.6)" }}, t);
      }});
      const cont = {{ v: 0 }};
      tl.to(cont, {{ v: 37, duration: 1.5, ease: "power2.in", onUpdate: () => {{ document.querySelector("#contador").textContent = Math.round(cont.v); }} }}, 0.35);
      tl.fromTo("#contador", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, 0.35);
      [0.15, 1.15].forEach((t0) => {{
        tl.to("#movil", {{ x: 10, rotation: 0.8, duration: 0.04, ease: "none", yoyo: true, repeat: 15 }}, t0);
        tl.set("#movil", {{ x: 0, rotation: 0 }}, t0 + 0.66);
      }});
      tl.to("#movil", {{ scale: 1.18, duration: 0.3, ease: "power2.in" }}, {D-0.3:.2f});
      const golpes = {jg};
      golpes.forEach(([sel, t]) => {{
        tl.fromTo(sel, {{ scale: 1.08, skewX: -6 }}, {{ scale: 1, skewX: -6, duration: 0.133, ease: "power3.out" }}, t);
      }});
      tl.fromTo("#t6logo", {{ scale: 0.9 }}, {{ scale: 1, duration: 0.2, ease: "power3.out" }}, {starts["t6"]});
      tl.fromTo("#cierre-caja", {{ scale: 1.9 }}, {{ scale: 1, duration: 0.233, ease: "power2.out" }}, {starts["t7"]});
      tl.fromTo("#t7marca", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "power1.out" }}, {starts["t7"]+0.233:.6f});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open('index.html','w').write(head+body)
print(T)
