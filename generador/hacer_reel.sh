#!/usr/bin/env bash
# Uso: generador/hacer_reel.sh historias/<id>.json salida.mp4
# Genera voz (Piper, voz davefx), vídeo (render.py) y música, y lo mezcla todo.
set -euo pipefail
GEN="$(cd "$(dirname "$0")" && pwd)"
export HISTORIA="$(realpath "$1")"; OUTF="$(realpath -m "$2")"
export WORK="$(mktemp -d)"
VOCES="$HOME/voces"; mkdir -p "$VOCES"
export VOZ_MODELO="$VOCES/es_ES-davefx-medium.onnx"
python3 -c "import piper" 2>/dev/null || pip install -q --break-system-packages piper-tts
if [ ! -s "$VOZ_MODELO" ]; then
  base=https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium
  curl -sSL -o "$VOZ_MODELO" "$base.onnx"; curl -sSL -o "$VOZ_MODELO.json" "$base.onnx.json"
fi
cd "$WORK"
python3 "$GEN/voz.py" > /dev/null
python3 "$GEN/musica.py"
T=$(python3 -c "import json;print(json.load(open('timing.json'))['total'])"); H=$(python3 -c "print($T/2)")
python3 "$GEN/render.py" full 0 "$H" part1.mp4 & P1=$!
python3 "$GEN/render.py" full "$H" "$T" part2.mp4
wait $P1
printf "file part1.mp4\nfile part2.mp4\n" > list.txt
ffmpeg -v error -y -f concat -i list.txt -c copy vid.mp4
ffmpeg -v error -y -i vid.mp4 -i voz.wav -i musica.wav -filter_complex \
  "[1:a]aresample=44100[v];[2:a]volume=${MUSICA_VOL:-0.13}[m];[v][m]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -shortest "$OUTF"
# hoja de contacto para revisar el vídeo
ffmpeg -v error -y -i "$OUTF" -vf "fps=1/2.5,scale=216:-1,tile=10x2" -frames:v 1 "${OUTF%.mp4}_revision.jpg"
echo "OK $OUTF ($T s)  trabajo: $WORK"
