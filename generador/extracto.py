#!/usr/bin/env python3
"""Reel "extracto + final nuestro": usa el inicio de un vídeo de referencia (lo decide Hugo), lo recorta a vertical,
quita el audio original, pone la voz de Dave en español y tapa los subtítulos originales con los nuestros en el mismo
estilo. Al final: ventana de "Abriendo enlace… norte.local", la web en un móvil y la CTA.

Uso: python3 generador/extracto.py historia.json salida.mp4
"""
import json, os, sys, subprocess, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)
MODEL = os.environ.get("VOZ_MODELO", os.path.expanduser("~/voces/es_ES-davefx-medium.onnx"))
NAR = (255, 98, 20); OSC = (22, 22, 24); CREMA = (246, 240, 231); VERDE = (90, 220, 120)
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def voz(texto, path, ls):
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", str(ls), "-f", path],
                   input=texto.encode(), check=True, capture_output=True)
    w = wave.open(path); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.01)[0]
    return (a[max(0, nz[0] - 600): nz[-1] + 600] if len(nz) else a), sr

def trozos(texto):
    pal = [p.strip(",.¿?¡!…") for p in texto.upper().split()]
    pal = [p for p in pal if p]; out, cur = [], []
    for p in pal:
        cur.append(p)
        if len(cur) == 3 or len(" ".join(cur)) > 13: out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def caja(im, texto, y, minw=0):
    d = ImageDraw.Draw(im); f = F("InterDisplay-Black.otf", 60); tw = max(d.textlength(texto, font=f), minw)
    d.rounded_rectangle((540 - tw / 2 - 34, y - 62, 540 + tw / 2 + 34, y + 62), 14, fill=(26, 20, 16))
    d.text((540, y), texto, font=f, fill="white", anchor="mm")

def main(hist, salida):
    H_ = json.load(open(hist)); ls = H_.get("voz_velocidad", 0.95); tmp = tempfile.mkdtemp()
    # 1) extracto
    vf = f"crop={H_['recorte']},fps={FPS},scale={W}:{H}:flags=lanczos"
    nf = int(H_["hasta"] * FPS); t_clip = nf / FPS
    lector = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", H_["archivo"], "-t", str(H_["hasta"] + 0.2), "-vf", vf,
                               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    ultimo = [None]
    def leer():
        b = lector.stdout.read(W * H * 3)
        if len(b) == W * H * 3: ultimo[0] = Image.frombytes("RGB", (W, H), b)
        return ultimo[0]
    # 2) voces: las del extracto en su tiempo; las del final, seguidas
    SR = 22050; pista = []; subs = []
    for i, (t0, txt) in enumerate(H_["voz_intro"]):
        a, SR = voz(txt, f"{tmp}/i{i}.wav", ls); pista.append((t0, a)); subs.append((t0, len(a) / SR, txt))
    escenas = []; t = t_clip
    for i, e in enumerate(H_["final"]):
        a, SR = voz(e["voz"], f"{tmp}/f{i}.wav", ls); d = len(a) / SR
        pista.append((t + 0.1, a)); subs.append((t + 0.1, d, e["voz"])) if e["tipo"] != "cta" else None
        dur = d + e.get("pausa", 0.35) + 0.1; escenas.append((t, dur, e)); t += dur
    T = t
    chunks = []
    for t0, d, txt in subs:
        cs = trozos(txt)
        for k, c in enumerate(cs): chunks.append((t0 + d * k / len(cs), c))
    web = Image.open(H_["web"]).convert("RGB") if H_.get("web") else None
    if web: web = web.resize((780, int(web.height * 780 / web.width)), Image.LANCZOS)
    tap = H_.get("tapar_subtitulos", {"y": 1642, "w": 760})
    # 3) vídeo
    vid = f"{tmp}/v.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", vid], stdin=subprocess.PIPE)
    for fi in range(int(T * FPS)):
        tt = fi / FPS
        sub = None
        for t0, c in chunks:
            if t0 <= tt: sub = c
        if tt < t_clip:
            im = leer().copy()
            caja(im, sub or H_.get("primer_subtitulo", ""), tap["y"], tap["w"])
        else:
            k = max(i for i, (s, _, _) in enumerate(escenas) if s <= tt); s0, dur, e = escenas[k]; lt = tt - s0
            if e["tipo"] == "enlace":
                im = ImageEnhance.Brightness(ultimo[0]).enhance(0.55); d = ImageDraw.Draw(im)
                p = ease(lt / 0.25); y = 760 + int((1 - p) * 60)
                d.rounded_rectangle((110, y, 970, y + 300), 34, fill=(18, 18, 20), outline=(60, 60, 64), width=3)
                d.text((160, y + 70), "Abriendo enlace…", font=F("Inter-Medium.otf", 40), fill=(160, 160, 166))
                d.text((160, y + 150), e.get("url", "https://norte.local"), font=F("Inter-Bold.otf", 58), fill="white")
                d.rounded_rectangle((160, y + 235, 920, y + 249), 7, fill=(50, 50, 54))
                d.rounded_rectangle((160, y + 235, 160 + int(760 * ease(lt / max(0.3, dur - 0.2))), y + 249), 7, fill=VERDE)
                if sub: caja(im, sub, tap["y"], tap["w"])
            elif e["tipo"] == "web":
                im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
                x0, y0, pw, ph = 130, 170, 820, 1380
                d.rounded_rectangle((x0 - 14, y0 - 14, x0 + pw + 14, y0 + ph + 14), 70, fill=OSC)
                desp = int(min(web.height - ph, H_.get("web_desplazar", 520)) * ease((lt - 0.6) / max(0.5, dur - 0.9)))
                vista = web.crop((0, desp, 780, desp + ph - 40))
                scr = Image.new("RGB", (pw, ph), "white"); scr.paste(vista, (20, 40))
                m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), 58, fill=255)
                im.paste(scr, (x0, y0), m)
                d.rounded_rectangle((x0 + pw / 2 - 90, y0 + 14, x0 + pw / 2 + 90, y0 + 48), 17, fill=OSC)
                sc = 0.92 + 0.08 * ease(lt / 0.3)
                if sc < 1: im = im.resize((int(W * sc), int(H * sc))).crop((0, 0, W, H)) if False else im
                if sub: caja(im, sub, 1720)
            else:  # cta
                im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im); sc = 1.15 - 0.15 * ease(lt / 0.2)
                a_, b_ = H_.get("cta", ["Comenta", "RECEPCIÓN"])
                d.text((540, 720), a_, font=F("InterDisplay-Black.otf", int(110 * sc)), fill=OSC, anchor="mm")
                d.text((540, 860), b_, font=F("InterDisplay-Black.otf", int(130 * sc)), fill=NAR, anchor="mm")
                d.text((540, 1060), H_.get("cta_sub", "y te la monto en tu negocio"), font=F("Inter-SemiBold.otf", 46), fill=(90, 86, 80), anchor="mm")
                d.text((540, 1590), "norte.local", font=F("Inter-ExtraBold.otf", 56), fill=NAR, anchor="mm")
            if lt < 0.1 and k > 0:
                im = Image.blend(im, Image.new("RGB", (W, H), "white"), 0.3 * (1 - lt / 0.1))
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait(); lector.kill()
    # 4) audio: voz + música suave (sin el audio original)
    n = int(T * SR); vo = np.zeros(n); mu = np.zeros(n); rng = np.random.default_rng(5)
    for s, a in pista:
        i = int(s * SR); j = min(n, i + len(a)); vo[i:j] += a[:j - i]
    def add(t0, sig, g=1.0):
        i = int(t0 * SR); j = min(n, i + len(sig))
        if 0 <= i < n: mu[i:j] += g * sig[:j - i]
    fq = lambda m: 440 * 2 ** ((m - 69) / 12); beat = 60 / H_.get("bpm", 104); bar = 4 * beat
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]; tb = 0.0; k = 0
    while tb < T:
        L = int(min(bar, T - tb) * SR); tt = np.arange(L) / SR; ch = prog[k % 4]
        add(tb, sum(np.sin(2 * np.pi * fq(m) * tt) * 0.06 + np.sin(2 * np.pi * fq(m + 12) * tt) * 0.03 for m in ch) * np.minimum(1, tt / 0.3), 1)
        for q in range(4):
            Lk = int(0.25 * SR); t2 = np.arange(Lk) / SR
            add(tb + q * beat, np.sin(2 * np.pi * (50 + 70 * np.exp(-t2 * 35)) * t2) * np.exp(-t2 * 12), 0.5)
            Lh = int(0.03 * SR); add(tb + q * beat + beat / 2, rng.standard_normal(Lh) * np.exp(-np.arange(Lh) / SR * 150), 0.08)
        tb += bar; k += 1
    for s0, _, _ in escenas:
        Lw = int(0.3 * SR); add(s0, rng.standard_normal(Lw) * np.exp(-np.arange(Lw) / SR * 14) * 0.3, 1)
    mix = vo / max(1e-9, np.abs(vo).max()) * 0.9 + mu / max(1e-9, np.abs(mu).max()) * H_.get("musica_vol", 0.24)
    aud = f"{tmp}/a.wav"; w = wave.open(aud, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", aud, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest", salida], check=True)
    print(f"{salida}  ({T:.1f} s)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
