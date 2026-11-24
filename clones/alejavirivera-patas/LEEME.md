Clon (24-nov) del viral de @alejavirivera «DeepSeek acaba de hacer otra LOCURA… y ha puesto patas arriba todo el mercado»
(https://www.tiktok.com/@alejavirivera/video/7708818254814383393 · 52.200 vistas, 5,8x su mediana). Desmontaje en
datos/desmontajes/alejavirivera-7708818254814383393/.
Copiado: noticia en el s 0 → destello de cielo → tipografía cinética verde neón (Playfair cursiva con brillo, «arriba» boca
abajo, cruces verdes 3D, «IA» de marca de agua, cinta tipo cotizaciones) → escalada «No solamente… ni… sino que además ahora…
Y no hablo de A, hablo de B» → «Ya que ahora, desde aquí…» con la app en oscuro (entrada inclinada) → kanban por estados →
«De igual forma…» (aviso) → recordatorio → «Incluso…» mapa con pines → CTA caja escribiéndose «RECEPCIÓN». Subtítulos: línea
pequeña blanca + palabra clave grande (Inter 900 o Playfair cursiva).
Cambios: sin persona (b-roll Mixkit 14669 móvil, 1442 obra, 20874 ladrillo, 24217 noche, 43033 cocina, 26112 cielo); 41 s en
vez de 81 s; música Mixkit 175; voz Piper davefx (voz.json, velocidad 0.97).
Rehacer: bajar los clips (https://assets.mixkit.co/videos/<id>/<id>-720.mp4) y recortarlos a 1080x1920 (scale=3413:1920,crop),
música https://assets.mixkit.co/music/175/175.mp3 → assets/musica.mp3; `HISTORIA=voz.json WORK=trabajo python3 ../../generador/voz.py
&& cp trabajo/voz.wav assets/` + palabras.json (faster-whisper word_timestamps); `python3 subtitulos.py && python3 generar.py`;
render `node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs render --fps 30 --quality high -o salida.mp4` (~3 min)
y loudnorm a -14 LUFS.
