"""Música de fondo propia (sin derechos): pad suave + pulso, duración = timing.json."""
import numpy as np, wave, json, os, sys
WORK = os.environ.get("WORK", os.getcwd())
SR = 44100; T = json.load(open(os.path.join(WORK, "timing.json")))["total"]; n = int(T * SR); t = np.arange(n) / SR
bpm = float(os.environ.get("BPM", 96)); beat = 60 / bpm
rng = np.random.default_rng(int(os.environ.get("SEED", 1)))
progs = [[[57,60,64],[53,57,60],[48,52,55],[55,59,62]], [[50,53,57],[46,50,53],[53,57,60],[48,52,55]], [[52,55,59],[48,52,55],[55,59,62],[50,54,57]]]
chords = progs[int(os.environ.get("SEED", 1)) % len(progs)]
out = np.zeros(n); f = lambda m: 440 * 2 ** ((m - 69) / 12); bar = beat * 4
for i in range(int(T / bar) + 1):
    s = int(i * bar * SR); e = min(n, int((i + 1) * bar * SR))
    if s >= n: break
    tt = np.arange(e - s) / SR; env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.4)
    for m in chords[i % 4]: out[s:e] += 0.05 * env * (np.sin(2 * np.pi * f(m) * tt) + 0.3 * np.sin(2 * np.pi * f(m + 12) * tt))
for k in range(int(T / beat) + 1):
    s = int(k * beat * SR)
    if s >= n: break
    L = min(n - s, int(0.25 * SR)); tt = np.arange(L) / SR
    out[s:s + L] += 0.35 * np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
    if k % 2 == 1:
        h = min(n - s, int(0.05 * SR)); out[s:s + h] += 0.06 * rng.standard_normal(h) * np.exp(-np.arange(h) / SR * 80)
out /= np.abs(out).max(); out *= np.minimum(1, np.minimum(t / 1.0, (T - t) / 1.5))
w = wave.open(os.path.join(WORK, "musica.wav"), "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 0.9 * 32767).astype(np.int16).tobytes()); w.close()

# --- efectos de sonido (archivo aparte para mezclarlo más alto que la música) ---
L_ = json.load(open(os.path.join(WORK, "timing.json")))["lines"]
sfx = np.zeros(n)
def add(t0, sig):
    i = int(t0 * SR)
    if i >= n: return
    j = min(n, i + len(sig)); sfx[i:j] += sig[:j - i]
def ding(f0=1320):
    tt = np.arange(int(0.35 * SR)) / SR
    return (0.5 * np.sin(2 * np.pi * f0 * tt) + 0.25 * np.sin(2 * np.pi * f0 * 1.5 * tt)) * np.exp(-tt * 11)
def whoosh():
    L = int(0.32 * SR); tt = np.arange(L) / SR
    noise = rng.standard_normal(L)
    # ruido filtrado con barrido (media móvil variable)
    out_ = np.zeros(L); acc = 0.0
    for i in range(L):
        a = 0.02 + 0.25 * (i / L); acc = acc + a * (noise[i] - acc); out_[i] = acc
    env = np.sin(np.pi * np.minimum(1, tt / 0.32)) ** 2
    return out_ * env * 0.9
escenas = []
for l in L_:
    if not escenas or escenas[-1][0] != l["scene"]: escenas.append((l["scene"], l["start"]))
if escenas and escenas[0][0] == "g0":
    for k_, t0 in enumerate([0.05, 0.55, 0.95]): add(t0, ding(1320 + 110 * k_))
for k_, (sc, t0) in enumerate(escenas):
    if k_ == 0: continue
    add(max(0, t0 - 0.42), whoosh())
if escenas and escenas[-1][0] == "cta": add(escenas[-1][1] + 1.9, ding(990))
sfx /= max(1e-6, np.abs(sfx).max())
w = wave.open(os.path.join(WORK, "sfx.wav"), "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((sfx * 0.8 * 32767).astype(np.int16).tobytes()); w.close()
