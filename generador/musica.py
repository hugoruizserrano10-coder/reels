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
