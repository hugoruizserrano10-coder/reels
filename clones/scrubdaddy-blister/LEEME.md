Clon (28-nov) del viral de @scrubdaddy «SCRUB BABY IS HERE» (https://www.tiktok.com/@scrubdaddy/video/7688381219578334494 ·
6,1 M vistas, 91x su mediana) en clave de historia absurda dibujada. Desmontaje en datos/desmontajes/scrubdaddy-7688381219578334494/.
Copiado: petición de un usuario → «te dijimos que estábamos trabajando en ello» → «¡Aquí está!» con el blíster naranja/verde →
repaso del producto por partes en primeros planos → «¡hemos pensado en todo!» → CTA → despedida. Cambiado: Paco (serie del
fontanero, ep. 3, sigue en la antena del 28-N) pide un invento; el producto es «la recepcionista de bolsillo» (la jefa en blíster).
Rehacer: `python3 voz.py /tmp/blis` (voz davefx de ~/voces); crear /tmp/blis/p con hyperframes.json/meta.json/package.json de
clones/zachking-mensaje y assets: voz.wav, ring/boing/logo de propios/fontanero-empanao/assets, SFX de
.claude/skills/media-use/audio/assets/sfx (whoosh, pop, impact-bass-1/2, riser, sparkle, chime, error, notification) y
https://assets.mixkit.co/music/738/738.mp3 recortada a 41 s como musica.mp3; `python3 gen.py /tmp/blis`; render
`node .claude/skills/hyperframes/scripts/plugin-cli.mjs render --fps 30 --quality high -o salida.mp4` (~5 min) y loudnorm a -14.
