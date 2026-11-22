"""Genera la locución línea a línea con Piper (voz davefx) y guarda los tiempos."""
import json, subprocess, wave, os, sys
import numpy as np

MODEL = os.environ.get("VOZ_MODELO", os.path.expanduser("~/voces/es_ES-davefx-medium.onnx"))

H_ = json.load(open(os.environ["HISTORIA"]))
OUT = os.environ.get("WORK", os.getcwd())
LS = H_.get("voz_velocidad", 0.88)
LINES = [tuple(l) + (None,) * (3 - len(l)) for l in H_["voz"]]  # (escena, texto hablado, subtítulo opcional)
GAP = 0.18   # silencio entre frases
LEAD = 0.35  # silencio inicial
SR = 22050

MOTOR = H_.get("voz_motor", "piper")  # "piper" (davefx) o "kokoro" (em_alex, em_santa, ef_dora)
_KOK = None
def synth_kokoro(text):
    global _KOK
    import numpy as _np
    from kokoro_onnx import Kokoro
    if _KOK is None:
        base = os.path.expanduser("~/voces/kokoro/")
        _KOK = Kokoro(base + "kokoro-v1.0.onnx", base + "voices-v1.0.bin")
    a, sr = _KOK.create(text, voice=H_.get("voz_id", "em_alex"), speed=H_.get("voz_velocidad_kokoro", 1.05), lang="es")
    # a 22050 Hz mono int16-like float
    import math
    n = int(len(a) * SR / sr)
    a = _np.interp(_np.linspace(0, len(a) - 1, n), _np.arange(len(a)), a).astype(_np.float32) * 32767
    thr = 300
    idx = _np.where(_np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 400): idx[-1] + 800]

def synth(text, path):
    if MOTOR == "kokoro":
        return synth_kokoro(text)
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", str(LS), "-f", path],
                   input=text.encode(), check=True, capture_output=True)
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    # recorta silencios de los extremos
    thr = 300
    idx = np.where(np.abs(a) > thr)[0]
    a = a[max(0, idx[0] - 400): idx[-1] + 800]
    return a

audio = [np.zeros(int(LEAD * SR), np.float32)]
t = LEAD
timing = []
os.makedirs(os.path.join(OUT, "lines"), exist_ok=True)
for i, (scene, text, cap) in enumerate(LINES):
    a = synth(text, os.path.join(OUT, "lines", f"l{i:02d}.wav"))
    d = len(a) / SR
    timing.append({"scene": scene, "text": cap or text, "start": round(t, 3), "end": round(t + d, 3)})
    audio.append(a)
    gap = GAP + (0.25 if i + 1 < len(LINES) and LINES[i + 1][0] != scene else 0)
    audio.append(np.zeros(int(gap * SR), np.float32))
    t += d + gap
audio.append(np.zeros(int(1.6 * SR), np.float32))
full = np.concatenate(audio)
full = full / max(1, np.abs(full).max()) * 0.92 * 32767
with wave.open(os.path.join(OUT, "voz.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(full.astype(np.int16).tobytes())
json.dump({"lines": timing, "total": round(len(full) / SR, 3)}, open(os.path.join(OUT, "timing.json"), "w"),
          ensure_ascii=False, indent=1)
print(json.dumps(timing, ensure_ascii=False, indent=0)[:3000]); print("total", len(full) / SR)
