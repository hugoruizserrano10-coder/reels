"""Voz Dave (Piper) por trozos con pausas antes de los remates y tiempos por palabra (faster-whisper, español forzado).
Uso: python3 voz.py carpeta_salida"""
import json, os, subprocess, sys, wave
import numpy as np
OUT = sys.argv[1]
MODEL = os.path.expanduser("~/voces/es_ES-davefx-medium.onnx")
LS = 1.07  # algo más lenta que la normal (Hugo: "va muy rápido")
# (escena, texto, pausa_antes, efecto)
TROZOS = [
 (0, "¡Que alguien invente algo para coger el teléfono sin subirme a una antena!", 0.15, "paco"),
 (1, "Paco… te dijimos que estábamos trabajando en ello.", 0.4, None),
 (2, "¡Aquí está!", 0.3, None),
 (2, "La recepcionista de bolsillo. Edición: manos ocupadas.", 0.45, None),
 (3, "Coge las llamadas mientras estás debajo de un fregadero.", 0.45, None),
 (4, "Contesta los WhatsApps mientras estás subido a una escalera.", 0.4, None),
 (5, "Y agenda las citas… mientras los bomberos te bajan de la antena.", 0.45, None),
 (6, "¡Hemos pensado en todo!", 0.45, None),
 (6, "Te avisa de cada cita al momento.", 0.3, None),
 (6, "Y hasta le recuerda la cita al cliente el día antes. Las veinticuatro horas.", 0.3, None),
 (7, "Paco ya la tiene. Ahora solo le falta bajar.", 0.5, None),
 (7, "Comenta RECEPCIÓN y te la montamos en tu negocio.", 0.45, None),
 (7, "¿Y la escalera, para cuándo?", 0.4, "paco"),
]
SR = 22050
def tts(txt, path):
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", str(LS), "-f", path], input=txt.encode(), check=True, capture_output=True)
    with wave.open(path) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    nz = np.where(np.abs(a) > 300)[0]
    return a[max(0, nz[0] - 200): nz[-1] + 600]
audio = []; t = 0.0; trozos = []; crudos = []
for i, (esc, txt, pausa, fx) in enumerate(TROZOS):
    a = tts(txt, f"{OUT}/t{i}.wav"); orig = a.copy()
    if fx == "paco":  # voz de Paco: más grave y con prisa
        p = f"{OUT}/t{i}.wav"; q = f"{OUT}/t{i}p.wav"
        with wave.open(p, "w") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-af", f"asetrate={SR}*0.86,aresample={SR},atempo=1.22,volume=1.15", q], check=True)
        with wave.open(q) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    t += pausa; audio.append(np.zeros(int(pausa * SR))); trozos.append({"i": i, "esc": esc, "txt": txt, "t0": round(t, 3), "t1": round(t + len(a) / SR, 3), "fx": fx, "ratio": len(a) / len(orig)}); crudos.append(orig)
    audio.append(a); t += len(a) / SR
audio.append(np.zeros(int(1.2 * SR))); T = t + 1.2
full = np.concatenate(audio).clip(-32768, 32767).astype(np.int16)
with wave.open(f"{OUT}/voz.wav", "w") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(full.tobytes())
from faster_whisper import WhisperModel
m = WhisperModel("small", compute_type="int8")
words = []
for tr in trozos:
    o = crudos[tr["i"]] / 32768.0
    o16 = np.interp(np.arange(0, len(o), SR / 16000), np.arange(len(o)), o).astype(np.float32)
    segs, _ = m.transcribe(o16, language="es", word_timestamps=True)
    ws = [w for s in segs for w in s.words]
    guion = tr["txt"].replace("…", " ").split()
    escala = tr["ratio"]
    if len(ws) == len(guion):
        tiempos = [(w.start, w.end) for w in ws]
    else:  # no cuadra: reparte las palabras del guion por longitud entre el inicio y el final reales
        a0, a1 = ws[0].start, ws[-1].end; L = sum(len(g) + 1 for g in guion); acc = 0; tiempos = []
        for g in guion:
            ini = a0 + (a1 - a0) * acc / L; acc += len(g) + 1; tiempos.append((ini, a0 + (a1 - a0) * acc / L - 0.03))
    for k, g in enumerate(guion):
        words.append({"tr": tr["i"], "esc": tr["esc"], "w": g, "t0": round(tr["t0"] + tiempos[k][0] * escala, 3), "t1": round(tr["t0"] + tiempos[k][1] * escala, 3)})
json.dump({"T": round(T, 3), "trozos": trozos, "words": words}, open(f"{OUT}/voz.json", "w"), ensure_ascii=False, indent=0)
print("T", round(T, 2), "palabras", len(words))
for tr in trozos: print(tr["esc"], tr["t0"], tr["t1"], tr["txt"][:50])
