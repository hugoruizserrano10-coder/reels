#!/usr/bin/env python3
"""Formato G "analogía absurda con giro" (estructura de reels tipo @trytaskless): historia ilustrada en plano
que no parece un anuncio → giro → lista de tareas que se tachan con ✓ "lo hace sola" → CTA.
Ilustración plana dibujada con PIL, voz de Dave (Piper) y subtítulos en cajas negras de 2–3 palabras.

Uso: python3 generador/cuento.py historias/<id>.json salida.mp4
JSON: {"tipo":"cuento", "oficio":"fontanero", "color_mono":[40,90,170], "escenas":[{"dibujo":..., "voz":...}, ...],
       "lista":[...], "herramientas":[...], "cta":["Comenta","RECEPCIÓN"], "caption":"..."}
Dibujos: pegar_moviles · fuga · perdidas · se_van · lista · herramientas · cta
"""
import json, os, sys, subprocess, tempfile, wave, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, S = 1080, 1920, 30, 2
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, int(s * S))
MODEL = os.environ.get("VOZ_MODELO", os.path.expanduser("~/voces/es_ES-davefx-medium.onnx"))
NAR = (255, 98, 20); OSC = (22, 22, 24); CREMA = (246, 240, 231); VERDE = (60, 190, 110)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def P(*v): return [int(a * S) for a in v]

# ---------- piezas ----------
def fondo(d, t):
    d.rectangle(P(0, 0, W, H), fill=(196, 226, 238))           # pared
    for i in range(0, W, 120):                                  # azulejos
        d.line(P(i, 0, i, 1180), fill=(181, 214, 228), width=3 * S)
    for j in range(0, 1180, 120):
        d.line(P(0, j, W, j), fill=(181, 214, 228), width=3 * S)
    d.rectangle(P(0, 1180, W, H), fill=(214, 196, 170))         # suelo
    d.rectangle(P(0, 1170, W, 1192), fill=(170, 150, 128))

PHONE_POS = [(470, 760), (600, 760), (420, 870), (540, 880), (650, 870), (470, 990), (600, 995),
             (380, 700), (700, 690), (540, 650), (360, 950), (720, 960)]

def movil(d, x, y, t, sonando=False, perdida=0, esc=1.0):
    ang = math.sin(t * 40) * 0.12 if sonando else 0.0
    w, h = 64 * esc, 112 * esc
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    rot = [(x + px * math.cos(ang) - py * math.sin(ang), y + px * math.sin(ang) + py * math.cos(ang)) for px, py in pts]
    d.polygon([tuple(v * S for v in p) for p in rot], fill=(30, 30, 34))
    ins = [(x + px * 0.8 * math.cos(ang) - py * 0.82 * math.sin(ang), y + px * 0.8 * math.sin(ang) + py * 0.82 * math.cos(ang)) for px, py in pts]
    d.polygon([tuple(v * S for v in p) for p in ins], fill=(120, 200, 255) if sonando else (70, 90, 110))
    if sonando:
        for r in (52, 74):
            a0 = (t * 6) % 1
            d.arc(P(x - r * esc, y - r * esc, x + r * esc, y + r * esc), 300, 360, fill=(255, 255, 255), width=5 * S)
            d.arc(P(x - r * esc, y - r * esc, x + r * esc, y + r * esc), 180, 240, fill=(255, 255, 255), width=5 * S)
    if perdida:
        d.ellipse(P(x + 18 * esc, y - 74 * esc, x + 62 * esc, y - 30 * esc), fill=(230, 40, 40))
        d.text(P(x + 40 * esc, y - 52 * esc), str(perdida), font=F("Inter-Bold.otf", 26 * esc), fill="white", anchor="mm")

def persona(d, mono, t, mojado=0.0, cara="normal"):
    cx = 540
    d.rounded_rectangle(P(cx - 150, 640, cx + 150, 1060), 60 * S, fill=mono)            # mono
    d.rectangle(P(cx - 130, 1040, cx - 30, 1180), fill=tuple(int(c * 0.8) for c in mono))  # piernas
    d.rectangle(P(cx + 30, 1040, cx + 130, 1180), fill=tuple(int(c * 0.8) for c in mono))
    d.rounded_rectangle(P(cx - 145, 1160, cx - 20, 1195), 15 * S, fill=(40, 30, 25))
    d.rounded_rectangle(P(cx + 20, 1160, cx + 145, 1195), 15 * S, fill=(40, 30, 25))
    sway = math.sin(t * 3) * 6
    d.rounded_rectangle(P(cx - 215, 660 + sway, cx - 150, 940), 32 * S, fill=mono)       # brazos
    d.rounded_rectangle(P(cx + 150, 660 - sway, cx + 215, 940), 32 * S, fill=mono)
    d.ellipse(P(cx - 225, 910, cx - 140, 990), fill=(236, 190, 150))
    d.ellipse(P(cx + 140, 910, cx + 225, 990), fill=(236, 190, 150))
    d.ellipse(P(cx - 95, 450, cx + 95, 640), fill=(236, 190, 150))                      # cabeza
    d.chord(P(cx - 100, 430, cx + 100, 600), 180, 360, fill=NAR)                          # gorra
    d.rounded_rectangle(P(cx - 10, 505, cx + 140, 530), 12 * S, fill=NAR)
    if cara == "agobio":
        d.line(P(cx - 50, 548, cx - 22, 558), fill=OSC, width=7 * S); d.line(P(cx + 22, 558, cx + 50, 548), fill=OSC, width=7 * S)
        d.ellipse(P(cx - 22, 590, cx + 22, 622), fill=OSC)
    else:
        d.ellipse(P(cx - 45, 550, cx - 27, 570), fill=OSC); d.ellipse(P(cx + 27, 550, cx + 45, 570), fill=OSC)
        d.arc(P(cx - 30, 575, cx + 30, 612), 20, 160, fill=OSC, width=6 * S)
    if mojado > 0:                                                                        # gotas
        rnd = random.Random(4)
        for k in range(26):
            x = rnd.uniform(330, 760); sp = rnd.uniform(500, 800); ph = rnd.uniform(0, 1)
            y = 330 + ((t * sp / 900 + ph) % 1) * 800
            if rnd.random() < mojado:
                d.ellipse(P(x - 9, y - 16, x + 9, y + 12), fill=(80, 160, 235))

def tuberia(d, t):
    d.rectangle(P(0, 260, W, 320), fill=(150, 156, 164)); d.rectangle(P(500, 250, 580, 330), fill=(120, 126, 134))
    for k in range(4):
        y = 330 + ((t * 1.6 + k / 4) % 1) * 140
        d.ellipse(P(530, y, 552, y + 30), fill=(80, 160, 235))

def caption(im, texto, y=1450):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FD + "InterDisplay-Black.otf", 62)
    tw = d.textlength(texto, font=f)
    d.rounded_rectangle((540 - tw / 2 - 30, y - 52, 540 + tw / 2 + 30, y + 52), 18, fill=OSC)
    d.text((540, y), texto, font=f, fill="white", anchor="mm")

# ---------- escenas ----------
def esc_pegar(d, t, dur, H_):
    fondo(d, t); persona(d, H_["mono"], t)
    n = int(ease(t / max(0.1, dur * 0.85)) * len(PHONE_POS)) + 1
    for i, (x, y) in enumerate(PHONE_POS[:n]): movil(d, x, y, t)

def esc_fuga(d, t, dur, H_):
    fondo(d, t); tuberia(d, t); persona(d, H_["mono"], t, mojado=ease(t / 1.2), cara="agobio")
    for i, (x, y) in enumerate(PHONE_POS): movil(d, x, y, t + i * 0.3, sonando=(i + int(t * 4)) % 3 == 0)

def esc_perdidas(d, t, dur, H_):
    fondo(d, t); tuberia(d, t); persona(d, H_["mono"], t, mojado=1.0, cara="agobio")
    for i, (x, y) in enumerate(PHONE_POS):
        movil(d, x, y, t + i * 0.3, sonando=True, perdida=1 + int(t * 2.2 + i) % 9)

def esc_se_van(d, t, dur, H_):
    fondo(d, t); persona(d, H_["mono"], t, mojado=1.0, cara="agobio")
    d.rounded_rectangle(P(700, 300, 1040, 460), 24 * S, fill="white")
    d.text(P(870, 350), H_.get("competencia", "Otro fontanero"), font=F("Inter-Bold.otf", 34), fill=OSC, anchor="mm")
    d.text(P(870, 410), "★★★★★", font=F("Inter-Bold.otf", 36), fill=(245, 180, 0), anchor="mm")
    for i, (x, y) in enumerate(PHONE_POS):
        p = ease((t - i * 0.12) / 0.9)
        movil(d, x + (870 - x) * p, y + (380 - y) * p - math.sin(p * math.pi) * 200, t, sonando=p < 1, esc=1 - 0.6 * p)

def esc_lista(d, t, dur, H_):
    d.rectangle(P(0, 0, W, H), fill=OSC)
    d.text(P(540, 300), "TU RECEPCIONISTA CON IA", font=F("Inter-Bold.otf", 34), fill=(150, 150, 156), anchor="mm")
    items = H_["lista"]
    for i, it in enumerate(items):
        y = 420 + i * 150; tc = dur * 0.32 + i * dur * 0.15; ok = t > tc
        d.rounded_rectangle(P(140, y, 940, y + 120), 26 * S, fill=(34, 34, 38), outline=VERDE if ok else (200, 60, 60), width=3 * S)
        d.text(P(190, y + 60), it, font=F("Inter-Bold.otf", 46), fill="white", anchor="lm")
        if ok:
            r = 34 * ease((t - tc) / 0.2); d.ellipse(P(860 - r, y + 60 - r, 860 + r, y + 60 + r), fill=VERDE)
            if r > 20: d.line(P(844, y + 60, 856, y + 74, 878, y + 46), fill=OSC, width=8 * S)
        else:
            d.text(P(870, y + 60), "A MANO", font=F("Inter-Bold.otf", 22), fill=(200, 60, 60), anchor="mm")
    tc = dur * 0.32 + len(items) * dur * 0.15 + 0.1
    if t > tc:
        p = ease((t - tc) / 0.25); y = 440 + len(items) * 150
        d.rounded_rectangle(P(540 - 220 * p, y, 540 + 220 * p, y + 96), 48 * S, fill=NAR)
        if p > 0.8: d.text(P(540, y + 48), "Lo hace sola", font=F("InterDisplay-Black.otf", 46), fill="white", anchor="mm")

def esc_herr(d, t, dur, H_):
    d.rectangle(P(0, 0, W, H), fill=OSC)
    d.text(P(540, 420), "FUNCIONA CON", font=F("Inter-Bold.otf", 34), fill=(150, 150, 156), anchor="mm")
    for i, it in enumerate(H_["herramientas"]):
        p = ease((t - i * 0.35) / 0.25)
        if p <= 0: continue
        y = 520 + i * 130; f = F("Inter-Bold.otf", 44); tw = d.textlength(it, font=f) / S + 120
        d.rounded_rectangle(P(540 - tw / 2, y, 540 + tw / 2, y + 96), 48 * S, fill=(34, 34, 38))
        d.ellipse(P(540 - tw / 2 + 26, y + 30, 540 - tw / 2 + 62, y + 66), fill=VERDE)
        d.text(P(540 + 25, y + 48), it, font=f, fill="white", anchor="mm")

def esc_cta(d, t, dur, H_):
    d.rectangle(P(0, 0, W, H), fill=CREMA)
    a, b = H_.get("cta", ["Comenta", "RECEPCIÓN"]); sc = 1.15 - 0.15 * ease(t / 0.2)
    d.text(P(540, 720), a, font=F("InterDisplay-Black.otf", 110 * sc), fill=OSC, anchor="mm")
    d.text(P(540, 860), b, font=F("InterDisplay-Black.otf", 130 * sc), fill=NAR, anchor="mm")
    d.text(P(540, 1060), H_.get("cta_sub", "y te lo monto en tu negocio"), font=F("Inter-SemiBold.otf", 46), fill=(90, 86, 80), anchor="mm")
    d.text(P(540, 1590), H_.get("marca", "norte.local"), font=F("Inter-ExtraBold.otf", 56), fill=NAR, anchor="mm")

DIB = {"pegar_moviles": esc_pegar, "fuga": esc_fuga, "perdidas": esc_perdidas, "se_van": esc_se_van,
       "lista": esc_lista, "herramientas": esc_herr, "cta": esc_cta}

# ---------- voz ----------
def voz(texto, path, ls):
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", str(ls), "-f", path],
                   input=texto.encode(), check=True, capture_output=True)
    w = wave.open(path); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.01)[0]
    return (a[max(0, nz[0] - 800): nz[-1] + 800] if len(nz) else a), sr

def trozos(texto, n=3):
    pal = texto.replace(",", "").replace(".", "").replace("¿", "").replace("?", "").upper().split()
    out, cur = [], []
    for p in pal:
        cur.append(p)
        if len(cur) == n or (len(cur) == 2 and len(" ".join(cur)) > 14): out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def main(hist, salida):
    H_ = json.load(open(hist)); H_["mono"] = tuple(H_.get("color_mono", [40, 90, 170]))
    tmp = tempfile.mkdtemp(); ls = H_.get("voz_velocidad", 0.95)
    SR = 22050; pista = []; tl = []; t = 0.0
    for i, e in enumerate(H_["escenas"]):
        a, SR = voz(e["voz"], os.path.join(tmp, f"v{i}.wav"), ls)
        dv = len(a) / SR; dur = dv + e.get("pausa", 0.3)
        tl.append((t, dur, dv)); pista.append((t, a)); t += dur
    T = t + 0.3
    vid = os.path.join(tmp, "v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", vid],
                          stdin=subprocess.PIPE)
    caps = [trozos(e["voz"]) for e in H_["escenas"]]
    for fi in range(int(T * FPS)):
        tt = fi / FPS
        k = max([i for i, (s, _, _) in enumerate(tl) if s <= tt] or [0])
        s0, dur, dv = tl[k]; lt = tt - s0; e = H_["escenas"][k]
        big = Image.new("RGB", (W * S, H * S)); d = ImageDraw.Draw(big)
        DIB[e["dibujo"]](d, lt, dur, H_)
        if e["dibujo"] in ("pegar_moviles", "fuga", "perdidas", "se_van"):
            z = 1.38 + 0.05 * lt / dur; cy = 800 if e["dibujo"] != "se_van" else 720
            cw, ch = W * S / z, H * S / z; cxp = (540 if e["dibujo"] != "se_van" else 640) * S
            cxp = min(max(cxp, cw / 2), W * S - cw / 2)
            big = big.crop((int(cxp - cw / 2), int(cy * S - ch / 2), int(cxp + cw / 2), int(cy * S + ch / 2))).resize((W, H), Image.LANCZOS)
            im = big
        else:
            im = big.reduce(S)
        if e["dibujo"] != "cta":
            cs = caps[k]; ci = min(len(cs) - 1, int(lt / max(0.1, dv) * len(cs)))
            if lt < dv + 0.1: caption(im, cs[ci])
        if lt < 0.12 and k > 0:
            im = Image.blend(im, Image.new("RGB", (W, H), "white"), 0.35 * (1 - lt / 0.12))
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait()
    # audio: voz + pulso suave + golpe en cada cambio de escena
    n = int(T * SR); vo = np.zeros(n); mu = np.zeros(n); rng = np.random.default_rng(2)
    for s, a in pista:
        i = int(s * SR); j = min(n, i + len(a)); vo[i:j] += a[:j - i]
    beat = 60 / H_.get("bpm", 100); b = 0.0
    while b < T:
        i = int(b * SR); L = min(n - i, int(0.3 * SR)); tt = np.arange(L) / SR
        mu[i:i + L] += 0.5 * np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 12); b += beat
    for s, _, _ in tl[1:]:
        i = int(s * SR); L = min(n - i, int(0.3 * SR)); tt = np.arange(L) / SR
        mu[i:i + L] += 0.4 * rng.standard_normal(L) * np.exp(-tt * 18)
    mix = vo / max(1e-9, np.abs(vo).max()) * 0.9 + mu / max(1e-9, np.abs(mu).max()) * 0.14
    aud = os.path.join(tmp, "a.wav"); w = wave.open(aud, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", aud, "-c:v", "copy", "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest", salida], check=True)
    print(f"{salida}  ({T:.1f} s, {len(tl)} escenas)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
