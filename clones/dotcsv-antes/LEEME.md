Clon (25-nov) del viral de @dotcsv «Hace tres años, este era el resultado de generar a Will Smith comiendo pasta… pero tres
años más tarde, esto es lo que podemos lograr» (https://www.tiktok.com/@dotcsv/video/7606027425373228310 · 619.900 vistas,
50,8x su mediana). Desmontaje en datos/desmontajes/dotcsv-7606027425373228310/.
Copiado: ANTES feo (teléfono y contestador de cinta con grano, look VHS, REC/PLAY) con «Hace tres años, esto era…» →
plano limpio en «Impresionante…» → vuelta a lo viejo con «2023» → destello y «2026» en «Pero tres años más tarde» → el
AHORA nítido (WhatsApp que contesta, ofrece hueco y deja la cita) → «Resultado que viene de… un terremoto» (sacudida) →
lo que hace (agenda, aviso, recordatorio) → split ANTES/AHORA → fondo coral del set con la enumeración «talleres, clínicas,
peluquerías, reformas, academias… TODO» → CTA. Subtítulos: una línea blanca en negrita, 2–4 palabras.
Cambios: sin presentador (b-roll Mixkit), 47 s en vez de 57 s, CTA «Comenta RECEPCIÓN».
Rehacer: bajar https://assets.mixkit.co/videos/<id>/<id>-720.mp4 (234, 48532, 46291 → look viejo; 13270, 4716, 13260,
14669, 41165 → nítido; recortes y filtros en el historial: scale=3413:1920,crop=1080:1920 y para lo viejo
scale=270:480,scale=1080:1920:flags=neighbor,eq=saturation=0.45:contrast=1.15,noise=alls=28:allf=t,gblur=sigma=1.2) con los
nombres de assets/ (viejo_tel, viejo_tel2 = 234 recortado, viejo_cinta, estatica, taller1/2/3, noche, whatsapp);
música https://assets.mixkit.co/music/140/140.mp3 → assets/musica.mp3; voz: `HISTORIA=voz.json WORK=trabajo python3
../../generador/voz.py && cp trabajo/voz.wav assets/` (modelo Piper davefx en ~/voces) + trabajo/palabras.json
(faster-whisper word_timestamps); `python3 generar.py`; render `node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs
render --fps 30 --quality high -o salida.mp4` (~4,5 min) y loudnorm a -14 LUFS.
