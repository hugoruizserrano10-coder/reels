"""Voz Dave (Piper) por trozos con pausas antes de los remates y tiempos por palabra (faster-whisper, español forzado).
Uso: python3 voz.py carpeta_salida"""
import json, os, subprocess, sys, wave
import numpy as np
OUT = sys.argv[1]
MODEL = os.path.expanduser("~/voces/es_ES-davefx-medium.onnx")
LS = 1.07  # algo más lenta que la normal (Hugo: "va muy rápido")
# (escena, texto, pausa_antes, efecto)
TROZOS = [
 (0, "Última hora: un fontanero lleva tres días subido a una antena.", 0.25, None),
 (1, "Se llama Paco, y esta semana ha perdido doce clientes por no coger el teléfono.", 0.35, None),
 (2, "Y lo peor… todavía no había pasado.", 0.35, None),
 (3, "Primero, se pegó el móvil a la frente con cinta americana.", 0.35, None),
 (3, "El móvil acabó dentro del váter.", 0.45, None),
 (4, "Después, contrató a un loro de secretario. El loro solo sabe decir:", 0.4, None),
 (4, "¡Luego te llamo!", 0.3, "loro"),
 (5, "Y hoy, se ha subido a una antena para tener más cobertura.", 0.4, None),
 (5, "Cobertura tiene.", 0.3, None),
 (5, "Escalera para bajar… no.", 0.45, None),
 (6, "Mientras tanto, su vecino electricista no ha perdido ni una llamada.", 0.55, None),
 (6, "¿Su secreto?", 0.25, None),
 (6, "Una recepcionista con inteligencia artificial: coge llamadas, contesta WhatsApps y agenda citas. Las veinticuatro horas.", 0.45, None),
 (7, "Paco sigue en la antena. Envíaselo a quien nunca coge el teléfono.", 0.45, None),
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
    if fx == "loro":  # voz de loro: más aguda y rápida
        p = f"{OUT}/t{i}.wav"; q = f"{OUT}/t{i}l.wav"
        with wave.open(p, "w") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-af", f"asetrate={SR}*1.45,aresample={SR},atempo=0.9,volume=1.1", q], check=True)
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
