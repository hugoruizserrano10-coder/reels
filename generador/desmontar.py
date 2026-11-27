"""Desmonta un reel de referencia para estudiar su estructura (nunca para resubirlo).

Uso: python3 generador/desmontar.py <video.mp4> <id> [carpeta_salida]
Saca: duración, transcripción con tiempos (Whisper), cortes de plano, hojas de fotogramas
y una ficha.md con los datos para que Claude escriba el análisis (gancho, estructura, CTA).
"""
import json, os, re, subprocess, sys

video, rid = sys.argv[1], sys.argv[2]
base = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datos", "desmontajes")
out = os.path.join(base, rid); os.makedirs(out, exist_ok=True)

def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)

dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]).stdout.strip())

# 1) transcripción con tiempos
wav = os.path.join(out, "audio.wav")
run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav])
segs = []
try:
    import soundfile as sf
    from faster_whisper import WhisperModel
    a, _ = sf.read(wav, dtype="float32")
    m = WhisperModel(os.environ.get("WHISPER_MODELO", "small"), device="cpu", compute_type="int8")
    for s in m.transcribe(a, language=os.environ.get("WHISPER_IDIOMA", "es"), vad_filter=True)[0]:
        segs.append({"ini": round(s.start, 1), "fin": round(s.end, 1), "texto": s.text.strip()})
except Exception as e:
    segs.append({"ini": 0, "fin": 0, "texto": f"(sin transcripción: {e})"})
os.remove(wav)

# 2) cortes de plano (cambios de escena)
r = run(["ffmpeg", "-v", "info", "-i", video, "-vf", "select='gt(scene,0.2)',showinfo", "-f", "null", "-"])
cortes = [round(float(x), 2) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]

# 3) hojas de fotogramas: una imagen cada segundo, 10 por hoja
run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=1,scale=300:-1,tile=5x2", os.path.join(out, "hoja_%02d.jpg")])
# fotograma del primer segundo en grande (el gancho visual)
run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", video, "-frames:v", "1", "-vf", "scale=540:-1", os.path.join(out, "primer_fotograma.jpg")])

datos = {"id": rid, "duracion_s": round(dur, 1), "cortes_s": cortes,
         "cortes_por_10s": round(len(cortes) / max(dur, 1) * 10, 1),
         "palabras_por_s": round(sum(len(s["texto"].split()) for s in segs) / max(dur, 1), 2),
         "transcripcion": segs}
json.dump(datos, open(os.path.join(out, "datos.json"), "w"), ensure_ascii=False, indent=1)

gancho = " ".join(s["texto"] for s in segs if s["ini"] < 3.5)
with open(os.path.join(out, "ficha.md"), "w") as f:
    f.write(f"# Desmontaje: {rid}\n\n")
    f.write(f"- Duración: {dur:.1f} s · cortes de plano: {len(cortes)} ({datos['cortes_por_10s']} cada 10 s) · ritmo de voz: {datos['palabras_por_s']} palabras/s\n")
    f.write(f"- Gancho hablado (0–3 s): «{gancho}»\n\n## Transcripción\n")
    for s in segs: f.write(f"- [{s['ini']:.1f}–{s['fin']:.1f}] {s['texto']}\n")
    f.write("\n## Análisis (lo escribe Claude mirando las hojas de fotogramas)\n")
    f.write("- Gancho visual (primer fotograma):\n- Tipo de gancho (ver datos/ganchos.md):\n- Estructura por bloques:\n- Frases puente que retienen:\n- Cierre / CTA:\n- Qué copiamos (estructura, no contenido):\n")
print(out)
