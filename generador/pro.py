#!/usr/bin/env python3
"""Reels "pro" con Remotion (animaciones motion con muelles, desenfoques, contadores, subtítulos palabra a palabra).
Prepara voz (Dave/Piper), tiempos por palabra (faster-whisper), música libre (Mixkit) y efectos, y renderiza.

Uso: python3 generador/pro.py historias/<id>.json salida.mp4
Historia: {"tipo":"pro", "marca":"norte.local", "musica_mixkit":623, "escenas":[{"type":"hook", "voz":"...", ...}, ...]}
Tipos de escena (remotion/src/ReelPro.tsx): hook · notifs · chat · agenda · lista · cta
En chat/agenda/lista, "t" de cada elemento = segundos desde el inicio de la escena; si falta, se reparten solos.
"""
import json, os, sys, subprocess, wave, shutil
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REM = os.path.join(RAIZ, "remotion"); PUB = os.path.join(REM, "public")
MODEL = os.environ.get("VOZ_MODELO", os.path.expanduser("~/voces/es_ES-davefx-medium.onnx"))
FPS = 30; SR = 22050

def voz(texto, ls):
    r = subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", str(ls), "--output-raw"],
                       input=texto.encode(), capture_output=True, check=True)
    a = np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 500): nz[-1] + 900] if len(nz) else a

def wav(path, a, sr=SR):
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def sfx():
    os.makedirs(f"{PUB}/sfx", exist_ok=True); rng = np.random.default_rng(1); sr = 44100
    L = int(0.45 * sr); t = np.arange(L) / sr
    n = rng.standard_normal(L); n = np.convolve(n, np.ones(30) / 30, "same")
    wav(f"{PUB}/sfx/whoosh.wav", n * np.sin(np.pi * t / t[-1]) ** 2 * 1.6, sr)
    L = int(0.12 * sr); t = np.arange(L) / sr
    wav(f"{PUB}/sfx/pop.wav", np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-t * 35) * 0.8, sr)
    L = int(0.5 * sr); t = np.arange(L) / sr
    wav(f"{PUB}/sfx/ding.wav", (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t * 7) * 0.5, sr)

def main(hist, salida):
    H_ = json.load(open(hist)); ls = H_.get("voz_velocidad", 0.95)
    tmp = os.path.join(PUB, "tmp"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    sfx()
    from faster_whisper import WhisperModel
    wm = WhisperModel("small", compute_type="int8")
    escenas, words, pista, sonidos = [], [], [], []
    t = 0.0
    for i, e in enumerate(H_["escenas"]):
        a = voz(e["voz"], ls) if e.get("voz") else np.zeros(int(0.8 * SR))
        dv = len(a) / SR
        lead = e.get("antes", 0.25 if i else 0.1)
        dur = lead + dv + e.get("pausa", 0.35)
        pista.append((t + lead, a))
        if e.get("voz") and e["type"] != "cta":
            a16 = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
            segs, _ = wm.transcribe(a16, language="es", word_timestamps=True, initial_prompt=e["voz"])
            for s in segs:
                for w in s.words:
                    words.append({"t0": round(t + lead + w.start, 3), "t1": round(t + lead + w.end, 3), "w": w.word.strip()})
        sc = {k: v for k, v in e.items() if k not in ("voz", "pausa", "antes")}
        for key in ("mensajes", "huecos", "items"):
            if key in sc:
                n = len(sc[key])
                for j, it in enumerate(sc[key]):
                    it.setdefault("t", round(lead + 0.15 + dv * 0.85 * (j + 0.15) / max(1, n), 2))
                    sonidos.append({"t": round(t + it["t"], 2), "s": "sfx/pop.wav" if key != "huecos" else "sfx/ding.wav", "v": 0.35})
        sc["from"] = int(round(t * FPS)); sc["dur"] = int(round(dur * FPS))
        escenas.append(sc)
        if i: sonidos.append({"t": round(max(0, t - 0.15), 2), "s": "sfx/whoosh.wav", "v": 0.25})
        t += dur
    T = t + 0.2
    out = np.zeros(int(T * SR) + SR)
    for s, a in pista:
        k = int(s * SR); out[k:k + len(a)] += a
    out = out / max(1e-9, np.abs(out).max()) * 0.95
    wav(f"{tmp}/voz.wav", out)
    musica = None
    if H_.get("musica_mixkit"):
        mid = H_["musica_mixkit"]; cache = os.path.expanduser(f"~/musica/{mid}.mp3"); os.makedirs(os.path.dirname(cache), exist_ok=True)
        if not os.path.exists(cache):
            subprocess.run(["curl", "-sL", "--max-time", "120", "-o", cache, f"https://assets.mixkit.co/music/{mid}/{mid}.mp3"], check=True)
        shutil.copy(cache, f"{tmp}/musica.mp3"); musica = "tmp/musica.mp3"
    props = {"scenes": escenas, "words": words, "voice": "tmp/voz.wav", "music": musica, "musicVol": H_.get("musica_vol", 0.13),
             "totalFrames": int(T * FPS), "brand": H_.get("marca", "norte.local"), "sfx": sonidos}
    pj = os.path.join(tmp, "props.json"); json.dump(props, open(pj, "w"), ensure_ascii=False)
    crudo = os.path.join(tmp, "crudo.mp4")
    subprocess.run(["npx", "remotion", "render", "src/index.ts", "ReelPro", crudo, f"--props={pj}",
                    "--browser-executable=/usr/bin/google-chrome", "--concurrency=2", "--log=error", "--crf=18"], cwd=REM, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", crudo, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "44100", "-c:a", "aac", "-b:a", "192k", salida], check=True)
    print(f"{salida}  ({T:.1f} s, {len(escenas)} escenas, {len(words)} palabras)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
