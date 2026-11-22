#!/usr/bin/env python3
"""Formato "palabras gigantes" (formato F): reel corto de 8–15 s con una palabra o frase enorme por golpe de ritmo,
cortes secos y colores alternos. Inspirado en la estructura de anuncios virales tipo "need a website? / clean. /
modern. / DM me" (solo la estructura). Sin voz por defecto: el ritmo lo marca la música.

Uso: python3 generador/palabras.py historias/<id>.json salida.mp4
JSON: {"tipo":"palabras", "bpm":120, "marca":"norte.local",
       "escenas":[{"texto":"¿Se te escapan|clientes?", "estilo":"crema", "golpes":2, "efecto":"zoom"}, ...],
       "caption": "..."}
  texto: "|" = salto de línea. estilo: crema | naranja | oscuro | blanco. golpes: duración en golpes de ritmo.
  efecto: zoom (entra grande), sube (entra desde abajo), sacude (temblor), tachar (raya la última línea), nada.
  Opcional "intro": {"tipo":"notificaciones","n":6} = abre con avisos de llamadas perdidas cayendo (interrupción visual).
"""
import json, os, sys, subprocess, tempfile, wave, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)
EST = {  # fondo, texto, acento
    "crema":   ((246, 240, 231), (24, 22, 20), (255, 98, 20)),
    "naranja": ((255, 98, 20), (255, 250, 244), (24, 22, 20)),
    "oscuro":  ((22, 22, 24), (255, 250, 244), (255, 98, 20)),
    "blanco":  ((255, 255, 255), (255, 98, 20), (24, 22, 20)),
}

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def texto_img(texto, color, acento, ancho=960):
    lineas = texto.split("|")
    size = 260
    while size > 70:
        f = F("InterDisplay-Black.otf", size)
        if all(f.getlength(l) <= ancho for l in lineas): break
        size -= 6
    f = F("InterDisplay-Black.otf", size)
    lh = int(size * 1.02)
    im = Image.new("RGBA", (W, lh * len(lineas) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lineas):
        # la palabra entre *asteriscos* va en color de acento
        x = (W - f.getlength(l.replace("*", ""))) / 2; y = 10 + i * lh
        acc = False
        for trozo in l.split("*"):
            d.text((x, y), trozo, font=f, fill=acento if acc else color)
            x += f.getlength(trozo); acc = not acc
    return im, size, len(lineas), lh

def notif(t_local, n, est):
    """Intro de interrupción: avisos de 'Llamada perdida' cayendo uno tras otro."""
    bg, fg, ac = EST["oscuro"]
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    for k in range(n):
        t0 = k * 0.16; p = ease((t_local - t0) / 0.22)
        if p <= 0: continue
        y = 300 + k * 205 - int((1 - p) * 120)
        a = int(255 * p)
        card = Image.new("RGBA", (920, 175), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, 919, 174), 40, fill=(44, 44, 48, a))
        cd.ellipse((34, 42, 124, 132), fill=(255, 98, 20, a))
        cd.text((79, 87), "!", font=F("InterDisplay-Black.otf", 56), fill=(255, 255, 255, a), anchor="mm")
        cd.text((154, 40), "Llamada perdida", font=F("Inter-Bold.otf", 46), fill=(255, 255, 255, a))
        cd.text((154, 100), f"Cliente · hace {k + 1} min", font=F("Inter-Medium.otf", 38), fill=(170, 170, 176, a))
        im.paste(card, (80, y), card)
    return im

def balon(d, cx, cy, r, rot):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(250, 250, 250), outline=(30, 30, 30), width=max(2, int(r * 0.04)))
    def pent(px, py, pr, a0):
        pts = [(px + pr * math.cos(a0 + k * 2 * math.pi / 5), py + pr * math.sin(a0 + k * 2 * math.pi / 5)) for k in range(5)]
        d.polygon(pts, fill=(30, 30, 30))
    pent(cx + r * 0.12 * math.cos(rot), cy + r * 0.12 * math.sin(rot), r * 0.3, rot)
    for k in range(5):
        a = rot + k * 2 * math.pi / 5 + math.pi / 5; rr = r * 0.78
        px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
        if math.hypot(px - cx, py - cy) < r * 0.95: pent(px, py, r * 0.2, a)

def pelota(t_local, dur):
    """Intro de interrupción: un balón rebota por el suelo acercándose a cámara hasta tapar la pantalla."""
    im = Image.new("RGB", (W, H), (120, 170, 90)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 760), fill=(40, 52, 80))                      # cielo de noche
    for x in (160, 920):                                                 # focos
        d.rectangle((x - 6, 180, x + 6, 760), fill=(70, 70, 80)); d.ellipse((x - 40, 150, x + 40, 210), fill=(255, 250, 220))
    for k in range(9): d.rectangle((0, 760 + k * 130, W, 760 + k * 130 + 65), fill=(110, 160, 82))  # franjas de césped
    d.rectangle((330, 520, 750, 760), outline=(255, 255, 255), width=8)  # portería al fondo
    p = min(1.0, t_local / dur)
    r = 40 + (p ** 2.2) * 1500
    cx = 540 + math.sin(p * 3) * 80 * (1 - p)
    rebote = abs(math.sin(p * math.pi * 3.2)) * 260 * (1 - p)
    cy = 900 + p * 500 - rebote
    d.ellipse((cx - r * 0.9, cy + r * 0.85, cx + r * 0.9, cy + r * 1.05), fill=(80, 120, 60))   # sombra
    balon(d, cx, cy, r, p * 9)
    return im

def cargar_clip(intro):
    """Vídeo de stock gratuito (Mixkit, licencia libre para uso comercial) recortado a vertical. Se descarga al vuelo
    por su id y no se guarda en el repositorio (la licencia no permite redistribuir el archivo suelto)."""
    mid = intro["mixkit"]; cache = os.path.expanduser(f"~/clips/{mid}.mp4"); os.makedirs(os.path.dirname(cache), exist_ok=True)
    if not os.path.exists(cache):
        subprocess.run(["curl", "-sL", "--max-time", "120", "-o", cache, f"https://assets.mixkit.co/videos/{mid}/{mid}-720.mp4"], check=True)
    cx = intro.get("centro_x", 0.5); vel = intro.get("velocidad", 1.0)
    marco = intro.get("encuadre") == "marco"
    MW, MH = (W, 1000) if marco else (W, H)
    escala = f"scale=-2:{MH}:flags=lanczos" if not marco else f"scale={int(MH * 16 / 9)}:{MH}:flags=lanczos"
    vf = (f"setpts=PTS/{vel},fps={FPS},{escala},crop={MW}:{MH}:(iw-{MW})*{cx}:0"
          + (",eq=saturation=1.15:contrast=1.05" if intro.get("realzar", True) else ""))
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(intro.get("desde", 0)), "-t", str(intro["dur"] * vel + 0.2),
                        "-i", cache, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    n = len(r.stdout) // (MW * MH * 3); out = []
    for i in range(n):
        fr = Image.frombytes("RGB", (MW, MH), r.stdout[i * MW * MH * 3:(i + 1) * MW * MH * 3])
        if marco:
            im = Image.new("RGB", (W, H), (255, 255, 255)); im.paste(fr, (0, 520)); fr = im
        out.append(fr)
    return out

def texto_arriba(im, texto):
    d = ImageDraw.Draw(im); f = F("Inter-Bold.otf", 58); lineas = texto.split("|")
    h = 90 + 72 * len(lineas)
    d.rectangle((0, 0, W, 170 + h), fill=(255, 255, 255))
    for i, l in enumerate(lineas):
        d.text((W // 2, 230 + i * 72), l, font=f, fill=(20, 20, 20), anchor="mm")
    return im

def main(hist, salida):
    H_ = json.load(open(hist)); bpm = float(H_.get("bpm", 120)); beat = 60 / bpm
    marca = H_.get("marca", "norte.local")
    esc = H_["escenas"]; intro = H_.get("intro")
    t_intro = ((0.16 * intro.get("n", 6) + 0.9) if intro.get("tipo") == "notificaciones" else intro.get("dur", 1.8)) if intro else 0.0
    clip = cargar_clip(intro) if intro and intro.get("tipo") == "clip" else None
    t_intro = round(t_intro / beat) * beat if intro else 0.0
    tiempos = []; t = t_intro
    for e in esc:
        d = e.get("golpes", 2) * beat; tiempos.append((t, d)); t += d
    T = t + 0.4
    cache = {}
    tmp = tempfile.mkdtemp()
    vid = os.path.join(tmp, "v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", vid],
                          stdin=subprocess.PIPE)
    for fi in range(int(T * FPS)):
        tt = fi / FPS
        if tt < t_intro:
            if clip:
                im = clip[min(len(clip) - 1, fi)].copy()
                if intro.get("texto_arriba"): im = texto_arriba(im, intro["texto_arriba"])
            else:
                im = notif(tt, intro.get("n", 6), None) if intro.get("tipo") == "notificaciones" else pelota(tt, t_intro)
        else:
            k = max(i for i, (s, _) in enumerate(tiempos) if s <= tt or i == 0)
            e = esc[min(k, len(esc) - 1)]; s0, dur = tiempos[min(k, len(esc) - 1)]; tl = tt - s0
            bg, fg, ac = EST[e.get("estilo", "crema")]
            if k not in cache: cache[k] = texto_img(e["texto"], fg, ac)
            ti, size, nl, lh = cache[k]
            im = Image.new("RGB", (W, H), bg)
            ef = e.get("efecto", "zoom"); p = ease(tl / 0.16)
            sc, dx, dy = 1.0, 0, 0
            if ef == "zoom": sc = 1.22 - 0.22 * p + 0.03 * tl / dur
            elif ef == "sube": dy = int((1 - p) * 260); sc = 1.0 + 0.03 * tl / dur
            elif ef == "sacude":
                amp = 18 * max(0.0, 1 - tl / 0.35); dx = int(amp * math.sin(tl * 90)); dy = int(amp * math.cos(tl * 70))
            else: sc = 1.0 + 0.02 * tl / dur
            tw, th = int(ti.width * sc), int(ti.height * sc)
            t2 = ti.resize((tw, th), Image.LANCZOS) if sc != 1.0 else ti
            im.paste(t2, ((W - tw) // 2 + dx, (H - th) // 2 + dy - 60), t2)
            if ef == "tachar":
                pr = ease((tl - 0.25) / 0.25)
                if pr > 0:
                    dd = ImageDraw.Draw(im); y = (H - th) // 2 - 60 + 10 + (nl - 1) * lh + int(size * 0.66)
                    dd.rounded_rectangle((90, y - 12, 90 + int(900 * pr), y + 12), 12, fill=ac)
            if k == len(esc) - 1:  # marca en la última tarjeta
                dd = ImageDraw.Draw(im); fm = F("Inter-ExtraBold.otf", 56)
                dd.text((W // 2, H - 330), marca, font=fm, fill=ac, anchor="mm")
            if p < 1 and k > 0:  # destello corto en el corte
                a = int(70 * (1 - p)); im = Image.blend(im, Image.new("RGB", (W, H), (255, 255, 255)), a / 255)
        ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait()

    # audio: pulso + golpe en cada corte + subida antes de la marca
    SR = 44100; n = int(T * SR); out = np.zeros(n); rng = np.random.default_rng(3)
    def add(t0, sig, g=1.0):
        i = int(t0 * SR); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += g * sig[:j - i]
    def kick():
        tt = np.arange(int(0.3 * SR)) / SR
        return np.sin(2 * np.pi * (48 + 90 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 12)
    def hit():
        L = int(0.25 * SR); tt = np.arange(L) / SR
        return 0.5 * rng.standard_normal(L) * np.exp(-tt * 28) + 0.6 * np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 20)
    def tic():
        tt = np.arange(int(0.12 * SR)) / SR
        return np.sin(2 * np.pi * 1760 * tt) * np.exp(-tt * 40)
    b = t_intro if (intro and intro.get("tipo") == "clip") else 0.0
    while b < T - 0.3:
        add(b, kick(), 0.8)
        if int(round(b / beat)) % 2: add(b, 0.15 * rng.standard_normal(int(0.04 * SR)) * np.exp(-np.arange(int(0.04 * SR)) / SR * 90))
        b += beat
    if intro and intro.get("tipo") == "notificaciones":
        for k in range(intro.get("n", 6)): add(k * 0.16, tic(), 0.5)
    elif intro and intro.get("tipo") == "clip":
        for g in intro.get("golpes_audio", []): add(g, kick(), 1.0)
    elif intro:  # botes del balón
        for b_ in (0.0, 0.31, 0.62): add(b_ * t_intro, kick(), 0.9)
    for s, _ in tiempos: add(s, hit(), 0.9)
    out /= max(1e-9, np.abs(out).max())
    aud = os.path.join(tmp, "a.wav"); w = wave.open(aud, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 0.9 * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", aud, "-c:v", "copy", "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-shortest", salida], check=True)
    print(f"{salida}  ({T:.1f} s, {len(esc)} tarjetas)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
