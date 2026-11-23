Clon (23-nov) del viral de @alejavirivera «¿Cómo puede ser LEGAL tener acceso a todo esto?» (God's Eye View,
https://www.tiktok.com/@alejavirivera/video/7688762956502355233 · 511.500 vistas, 58x su mediana). Desmontaje en
datos/desmontajes/alejavirivera-7688762956502355233/.
Copiado: pregunta de incredulidad en el segundo 0 sobre un globo con paneles HUD → tarjeta-logo de la "herramienta"
(ojo + letras espaciadas + "conectando…") → "permite que…" → "desde aquí vas a poder ver…" (vista aérea nocturna con
etiquetas tipo matrícula) → lo que ves → "No solo eso…" (líneas amarillas como las rutas de vuelos) → CTA. Subtítulos de
1–4 palabras, las clave en grande a dos tonos (degradado naranja + cursiva blanca), como el original.
Cambios: sin persona (no grabamos a nadie): todo b-roll; 36 s en vez de 65 s (su cierre de 10 s era "búscalo en YouTube");
en las escenas de ficha y chat no hay subtítulos (regla de no leer dos cosas a la vez).
Material: Mixkit 29351 (Tierra), 27122 (ciudad de noche cenital), 50996 (rotonda), 42346 (edificio), música Mixkit 140
"Cyberpunk City"; voz Piper davefx (voz.json, velocidad 0.92).
Rehacer: preparar assets (ver comandos ffmpeg en el diario del 23-nov / recortes 9:16), luego
`HISTORIA=voz.json WORK=trabajo python3 ../../generador/voz.py && cp trabajo/voz.wav assets/` (+ palabras.json con
faster-whisper word_timestamps), `python3 subtitulos.py && python3 generar.py`, render con
`node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs render --fps 30 --quality high -o salida.mp4` y loudnorm a -14 LUFS.
