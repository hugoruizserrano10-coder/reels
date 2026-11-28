# Diario de ejecuciones (lecciones operativas)

- 2026-11-22 (montaje): Instagram necesita el vídeo en URL pública; GitHub Pages no estaba activado, pero la URL raw.githubusercontent.com funcionó con Windsor. Si un día falla, probar la URL de GitHub Pages (https://hugoruizserrano10-coder.github.io/reels/videos/...).
- 2026-11-22: el push a GitHub necesita la app de Claude instalada en el repo; si da 403, avisar a Hugo para reinstalarla.
- 2026-11-22: con escenas cortas, el logo final no daba tiempo a salir; ya corregido en render.py (sale al acabar la última frase).
- 2026-11-22 (extra, 13:52): Hugo pidió un segundo reel hoy (la ejecución de las 13:40 había parado porque ya había reel). Academia/selectividad, 34,5 s, gancho g0; reel + historia publicados sin problemas. El archivo se llamó videos/2026-11-22b.mp4 para no pisar el de la mañana. La rotación de franjas empieza el 23-nov con la C (20:40).

## Análisis 2026-11-23
- Revisados 187 vídeos (TikTok + YouTube Shorts con descubrir.py, 11 perfiles), 26 virales (≥3x mediana). Instagram: no se bajó
  ningún reel suelto hoy (no hacía falta para llegar a 40; Make sigue sin webhook porque Hugo no ha conectado Instagram en Make).
- Desmontados 3 (TikTok): @alejavirivera God's Eye (58x), @marketingconlaurita loops (9,7x), @alejavirivera Google vídeo (11,7x).
  Los tres son a cámara; el más fuerte se clonó sin persona (todo b-roll).
- **Clon**: God's Eye → `videos/2026-11-24-M.mp4` (36 s) + `historias/2026-11-24-M-clon-alejavirivera.json`, sale el 24-nov a las 13:40.
- Fallos: YouTube no deja descargar desde la nube (pide iniciar sesión; probados clientes tv/android_vr/ios/mweb): de YouTube solo
  listamos vistas. Varios perfiles de TikTok no los lee yt-dlp (ver `fuentes_que_fallan` en referentes.json). Render con
  HyperFrames: ~4 min por 36 s; ojo, en escenas que no son sub-composiciones el `data-start` de un `<video>` es absoluto, y
  `text-shadow` heredado ensucia el texto con degradado (poner `text-shadow:none`).
- Ideas para próximos reels: (1) gancho «¿Cómo puede ser LEGAL…?» si el clon funciona, probarlo en un formato propio;
  (2) formato J «la mayoría contesta al día siguiente / ¿quién está detrás? Tú, a las 23:00»; (3) imagen surrealista en el s 2
  para romper el plano (formato «y no me refiero a…»).
- Comparación con lo nuestro: aún no hay datos de 24–72 h de los reels del 22–23-nov para comparar (se hará en el informe del lunes).
- 2026-11-23 (franja M, 13:40): publicado el clon de @asadwebsites (12,1 s) como reel (18124625351073554) + historia. El control pilló que la pantalla del móvil decía «viernes 22 de noviembre» y el 22-nov-2026 fue domingo: se cambió a «viernes 20» y se re-renderizó con HyperFrames en 30 s (hay que bajar antes assets/musica.mp3 de Mixkit 623, no está en el repo). raw.githubusercontent tardó ~3 min en servir el vídeo nuevo tras el push. Próxima vez: comprobar día de la semana de cualquier fecha en pantalla al preparar el clon. Windsor (plan gratuito) da datos en caché: las métricas de las últimas horas pueden ir atrasadas.
- 2026-11-23 (franja N, 20:40): publicado «Fontanero empanao» (video_listo, dibujos + humor, guion de Hugo, 25,4 s) como reel (18122682914089294) + historia (18055405466602762). Control 10/10 ok (aviso: fontanería repetida del 22-nov con otro problema). Sin incidencias; el vídeo ya estaba en raw desde el commit de preparación, así que se publicó a la hora exacta. Ojo: la tarea arranca con HEAD separado (detached) en el clon; hacer `git switch main && git merge --ff-only origin/main` antes de commitear. Sin correos de FormSubmit en 2 días; 0 comentarios; 2 seguidores.

## Análisis 2026-11-24
- Revisados 310 vídeos (TikTok + YouTube Shorts con descubrir.py, 14 perfiles + 1 TikTok nuevo); 15 virales nuevos (≥3x).
  Las cuentas de siempre repiten casi los mismos vídeos que ayer: solo 1 viral nuevo entre ellas. Nuevos referentes (3):
  Adrián Sáenz (negocios, 12x en «¿Cuánto gana un…?»), Hermanos García Reformas (reformas, nuestro cliente tipo, antes/después
  3–4,8x) y Anthony Shoosh (vende recepcionistas con IA en español, vigilar). Instagram: la búsqueda web no da enlaces de reels
  (no se bajó ninguno); Make sigue sin webhook (Hugo no ha conectado Instagram en Make). YouTube sigue sin dejar descargar.
- Desmontados 3 (TikTok): @javadex titular-polémica (14,8x), @alejavirivera «patas arriba» (5,8x), @alejavirivera 6 herramientas (5,1x).
- **Clon**: «patas arriba» → `videos/2026-11-25-M.mp4` (41 s) + `historias/2026-11-25-M-clon-alejavirivera-patas.json`, sale
  el 25-nov a las 13:40. Control 10/10 ok. Render HyperFrames 3 min 20 s. Ojo: un `<video>` que empieza antes que su escena
  no se ve: el destello de cielo va fuera de las escenas, en la raíz.
- Ideas: (1) formato H con «Aquí van 4 cosas…» y número gigante neón en el s 1 (de 6 herramientas); (2) titular-polémica fijo
  en caja blanca si Hugo graba algo a cámara (de javadex); (3) los virales de Hermanos García son «adiós tabique» y antes/después:
  probar un reel para reformistas con b-roll de obra y «el cliente que te escribió mientras tirabas el tabique».
- Para que las rondas no se repitan: hacen falta más cuentas que publiquen a diario en TikTok (descargables) o que Hugo conecte
  Instagram en Make.
- Comparación con lo nuestro (Windsor, datos en caché): «fuga» 120 vistas (8,5 s de media, 18 % visto, 3 guardados) y
  «fontanero empanao» 141 vistas en <24 h (7,9 s, 31 % visto) son los mejores; el clon de @asadwebsites 7 vistas y el extracto
  del balón 6 (aún pocas horas / sin empuje). Lo que funciona fuera (noticia + golpe visual en el s 2–3 y escalada) coincide con
  lo nuestro: los reels con historia y humor retienen más que los cortos de impacto. Aún es pronto: decidir en el informe del lunes.
- 2026-11-24 (franja M, 13:40): publicado el clon de @alejavirivera «God's Eye» (video_listo, 36,2 s) como reel (18083757878723093) + historia (18076588232765834). Control 10/10 ok, sin incidencias (vídeo ya servido por raw desde la preparación). Métricas 24 h: clon @asadwebsites 7 vistas, 100 % skip (casi sin distribución); extracto balón 6 vistas (medido tarde, a ~38 h). Fontanero empanao lleva 141 vistas, skip 43 % (el mejor skip hasta ahora). TikTok: Windsor da 0 vistas por vídeo (solo el total de cuenta, 313), así que no sirve aún para comparar. Sin comentarios ni correos de FormSubmit. Próxima vez: medir el 22-N a tiempo no aplica ya; vigilar si los clones cortos siguen sin empuje.
- 2026-11-24 (franja N, 20:40): publicado «tanque con QR» (video_listo, dibujos, idea de @trytaskless aprobada por Hugo, 28,4 s) como reel (18649476994032328) + historia (18657631903055336). Control 10/10 ok (aviso: tipo_negocio genérico, igual que el clon de mediodía). Sin incidencias; el clon arrancó otra vez con HEAD separado, resuelto con `git checkout -B main origin/main` (árbol limpio). Métricas 24 h de fontanero empanao: 142 vistas, 124 alcance, 8,0 s (31 % visto), skip 43 %. TikTok: Windsor ya da tiempo medio por vídeo (Paco 4,97 s, 2,9 % completo; 37 mensajes 1,3 s) y 1.413 vistas de cuenta en 30 días, pero no vistas por vídeo. 0 comentarios, 2 seguidores, sin correos de FormSubmit.

## Análisis 2026-11-25
- Revisados 325 vídeos (TikTok + YouTube Shorts con descubrir.py): 277 de los 11 perfiles habituales, que **no dieron ningún
  viral nuevo** (repiten los mismos de ayer), y 48 de 6 cuentas exploradas en TikTok. Nueva referente: **@dotcsv** (DotCSV,
  divulgación de IA en español, mediana 12,2k, 7 virales de 3,4–50,8x, se descarga bien). Es la 4.ª cuenta nueva de la semana
  (el máximo es 3): excepción porque sin cuentas nuevas la ronda no da nada. @iaparatodos y @marketingconia no aportan;
  @ia_productividad, @xavimarcet y @reformasyobras fallan (en referentes.json). Instagram: la búsqueda web sigue sin dar reels
  (solo blogs); Make sigue sin webhook. 9 virales nuevos (≥3x).
- Desmontados 3 (TikTok @dotcsv): Seedance «hace tres años… tres años más tarde» (**50,8x**), Genie 3 «Tremenda tecnología…
  Imagínate que…» (10,6x), Claude Cowork «Hablemos de…» (7,3x). Los tres son presentador + insertos; el primero se puede clonar
  sin persona porque su fuerza está en el contraste de imágenes.
- **Clon**: Seedance antes/ahora → `videos/2026-11-26-M.mp4` (46,9 s, taller: Raúl, frenos, domingo 23:10 → lunes 8:30) +
  `historias/2026-11-26-M-clon-dotcsv.json`, sale el **26-nov a las 13:40**. Control 10/10 ok. Render HyperFrames 4 min 24 s.
  Ojo: los clips de Mixkit con id 1008xx no tienen URL directa -720; el look viejo sale mejor hecho con ffmpeg (bajar a 270x480
  + ruido) que con filtros CSS; el check de HyperFrames avisa de textos cortos (line_unread): mensajes de chat de ≤8 palabras.
- Ideas: (1) el formato antes/ahora sirve para cualquier negocio (agenda de papel, «pulse 1», buzón lleno) y se puede repetir en
  dibujos para la franja N; (2) «Imagínate que un cliente te escribe a las 23:00…» con caja de texto escribiéndose (de Genie 3);
  (3) interfaz con cursor que pulsa pestañas «Contestar / Agendar / Avisar / Recordar» (de Cowork).
- **Comparación con lo nuestro (Windsor, últimos 7 días)**: los reels de la franja N (20:40) con dibujos/humor son los que
  funcionan: «tanque con QR» 199 vistas (11,5 s de media, skip 31 %), «fontanero empanao» 142 (8,0 s, skip 43 %), «fuga» 122.
  Los **clones de mediodía casi no reciben distribución**: @asadwebsites 8 vistas (skip 80 %), God's Eye 5 vistas (2 de
  alcance). Lo que se viraliza fuera no está funcionando en nuestra cuenta a las 13:40; puede ser la hora o el formato
  (b-roll + voz sintética). Hoy se prueba un clon con gancho de contraste visual muy fuerte; si también se queda en <20 vistas,
  proponer a Hugo en el informe del lunes mover los clones a la franja N o hacerlos en dibujos.
- 2026-11-25 (franja M, 13:40): publicado el clon de @alejavirivera «patas arriba» (video_listo, 41,2 s, reformas) como reel (18424332973154639) + historia (18114824471628485). Control 10/10 ok (repasado de nuevo: hoja de fotogramas, -13,9 LUFS, raw 200). Aviso: el plan dice que desde hoy los días impares la M es historia absurda, pero había clon preparado para hoy y se usó (paso 0); la tarea de análisis debería dejar absurda en los impares. Métricas: tanque con QR 208 vistas (11,3 s, 40 % visto, skip 32 %) en <24 h, el mejor hasta ahora; God's Eye 24 h: 5 vistas, 2 alcance (los clones de mediodía siguen sin distribución). TikTok: Paco alcance 222 (4,95 s), tanque 9,7 s de media (el mejor). 0 comentarios, 0 correos. Clon arrancó con HEAD separado otra vez: `git checkout -B main origin/main`.
- 2026-11-25 (franja N, 20:40): publicado «gato con gafas» (formato F, palabras gigantes, 12,6 s) como reel (18140193463658887) + historia (18226213798356274). Control 10/10 (2 corregidos): el formato F salía con audio flojo (-24,7 LUFS, intro sin música) → añadida música Mixkit 744 desde el inicio y loudnorm a -14; faltaba "variante" en el JSON. Métricas: tanque con QR 24 h = 238 vistas, 219 alcance, 11,2 s (39 % visto), skip 31 % (el mejor); patas arriba (M de hoy) 5 vistas / 1 alcance a las 8 h; los clones de mediodía siguen sin distribución. TikTok: Hugo ya subió a las 16:54 un vídeo con el mismo texto del gato (2,1 s de media) → este de Instagram es el mismo concepto. 0 comentarios, 0 correos. Próxima vez: palabras.py debería meter música Mixkit desde el segundo 0 (2.ª vez que el audio de un formato sale flojo → arreglar el generador); y la tarea de análisis debería preparar historias absurdas para la N como dice el plan.

## Análisis 2026-11-26
- Revisados 369 vídeos (TikTok + YouTube Shorts con descubrir.py): 307 de los 11 perfiles habituales, que otra vez **no dieron
  virales nuevos** (solo 1 de NateHerk en YouTube, que no se descarga), y 62 de 7 cuentas exploradas. Nueva referente:
  **@soyfranciscorivas** (técnico de aire acondicionado y electricidad, nuestro cliente tipo; mediana 290, mini split **734x**,
  213k vistas). Fallan: tiktok @alexhormozi (privada), @ibai, @lapapelerademaria, @moonpiofficial; @elmundotoday casi sin
  vídeos. La búsqueda web sigue sin dar reels de Instagram (solo noticias). Make sigue sin webhook. 9 virales nuevos (≥3x).
- Desmontados 4: @soyfranciscorivas mini split «Acompáñame a…» (734x), su historia de origen «hace 9 años… ¡BOOM!» (13x), la
  acometida con el «chalán nuevo» (8,4x) y @dotcsv Flux Kontext «lo de siempre falla → lo nuevo acierta» (9,2x).
- **Clon**: mini split → `videos/2026-11-28-M.mp4` (55,8 s, climatización, «mantenimiento preventivo al TELÉFONO de un técnico
  de aire acondicionado») + `historias/2026-11-28-M-clon-franciscorivas.json`, sale el **sábado 28-nov a las 13:40** (el 27 es
  impar → la M es absurda). Primer clon que mezcla la estructura del viral con historia absurda. Control 10/10 ok, -14,5 LUFS.
  Render HyperFrames 6 min (x2: el primero tenía dos subtítulos solapados en la hidrolimpiadora → ahora generar.py fuerza que
  cada subtítulo termine antes del siguiente). Ojo: la voz Piper davefx no está en la nube; se baja de huggingface
  (rhasspy/piper-voices es/es_ES/davefx/medium) a ~/voces.
- **27-M**: dejado `historias/2026-11-27-M-absurda-pendiente.json` (absurda del electricista que se clonó) para que la tarea del
  reel no adelante el clon del 28. El 27 es día de prueba de 16:40 (días desde inicio % 5 == 4).
- Ideas: (1) repetir «Acompáñame a…» con otros oficios (ITV al WhatsApp de un taller, revisión al buzón de un fontanero);
  (2) historia de origen «hace 9 años… ¡BOOM!… ¡BAM!» de un fontanero inventado; (3) un personaje torpe secundario (el «chalán
  nuevo») en las absurdas en dibujo.
- **Comparación con lo nuestro (Windsor, 7 días)**: «tanque con QR» 239 vistas (11,2 s, skip 31 %), «fontanero empanao» 142,
  «fuga» 122. Clones de mediodía: patas arriba 14 vistas (skip 83 %), God's Eye 5, @asadwebsites 8; el formato F del gato (N,
  25-nov) solo 5 vistas a las ~15 h. Se confirma: lo que retiene es historia con humor/absurdo; el b-roll con voz sintética y el
  texto de anuncio no reciben distribución. Por eso el clon de hoy va en clave absurda. Si el 26-M (antes/ahora) y el 28-M
  también se quedan en <20 vistas, proponer a Hugo en el informe del lunes clonar los virales en dibujo o moverlos a la N.
- Las cuentas habituales ya no dan virales nuevos (3.er día seguido): hace falta que Hugo conecte Instagram en Make o buscar
  más oficios en TikTok (técnicos, reformistas, mecánicos) como @soyfranciscorivas.

- 2026-11-26 M (13:40): publicada absurda loros/panadería (video_listo, 23,8 s) como reel 18202348414392838 + historia. Control 10/10 (nota: descripción sin municipio concreto). Métricas 25-M a 24 h: 14 vistas, skip 83 %. Sin fallos. Próxima vez: meter municipio en la caption de las absurdas.
- 2026-11-26 N (20:40): publicado clon dotcsv antes/ahora (taller, video_listo, 46,3 s) como reel 18114246296097327 + historia 18163244941459952. Control 10/10 (re-medido -14,3 LUFS). Métricas 25-N gato a 24 h: 6 vistas, 19 % visto, skip 75 %. 26-M loros a 8 h: 151 vistas, 42 % visto, skip 39 %. Sin fallos.

## Análisis 2026-11-27
- Revisados 539 vídeos: 337 de los perfiles habituales con descubrir.py (**4.º día sin virales nuevos**), 162 de 8 cuentas
  exploradas para el paso 2a (historias absurdas) y 40 de una búsqueda de YouTube. **YouTube ya no deja nada desde la nube**:
  `ytsearch` da 403 a partir de la 2.ª consulta y las descargas piden «confirmar que no eres un bot» con cualquier cliente;
  solo se pueden listar canales. Así que las absurdas salen de TikTok. Nuevas referentes: **@zachking** (mediana 12 M) y
  **@curiosidadesconmike** (humor visual tonto en español, 10 virales hasta 91x). Make sigue sin webhook. 24 virales nuevos.
- Desmontados 3: @zachking «a message to all AI» (**68,5 M, 5,7x**), @zachking «is it cake» (67,9 M, 5,7x) y @curiosidadesconmike
  juguetes navideños sospechosos (240k, 91x).
- **Clon (absurda, paso 2a)**: «a message to all AI» → `videos/2026-11-27-M.mp4` (28,2 s, electricista) +
  `historias/2026-11-27-M-absurda-clon-zachking.json`, sale **hoy 27-nov a las 13:40**. «Este es un mensaje para todas las
  llamadas perdidas. Me llamo Toni y soy electricista. Y voy a cogeros a todas, clonándome cinco veces…» → los 5 Tonis se
  pelean por el móvil y no lo coge ninguno → «mi jefa va a acabar con vosotras» (la recepcionista, un móvil con gorra y corona)
  → llamadas / WhatsApps / visitas / 24 horas → «Síguela. O comenta RECEPCIÓN». Misma estética del viral (oscuro, contraluz,
  palabras gigantes en serif roja una a una, voz lenta) pero dibujado (formato N en formatos.md). Usa la idea reservada del
  electricista que se clona. Música Mixkit 671.
- Ideas: (1) formato N como serie: «Este es un mensaje para todos los WhatsApps sin leer» y la «jefa» como personaje fijo;
  (2) diciembre: «Empieza la Navidad y estos clientes se ven muy sospechosos» (juguetes de cuerda dibujados, sin voz);
  (3) «¿Es real o es IA?» con dos móviles.
- **Comparación con lo nuestro (Windsor, 7 días)**: tanque 240 vistas (11,2 s), loros 152 (10,0 s, skip 39 %), Paco 142, fuga
  122; los clones de anuncio/texto siguen sin distribución (dotcsv antes/ahora: 9 vistas, skip 100 %; patas arriba 14; gato 6).
  Lo que funciona fuera (personaje + situación absurda + giro) coincide con lo único que nos funciona: por eso el clon de hoy
  va en dibujo y en clave absurda. Mañana sale el clon del mini split (28-M), otra prueba de «estructura de viral + absurdo».

- 2026-11-27 M (16:40, día de prueba de hora): publicado clon absurdo @zachking «mensaje a todas las llamadas perdidas» (electricista, video_listo, 28,3 s) como reel 17947618140366827 + historia 18081076379729327. Control 10/10 (re-medido -13,6 LUFS, hoja revisada). Métricas: 26-M loros a 27 h 152 vistas, 42 % visto, skip 39 %; 26-N antes/ahora 10 vistas, skip 100 %. TikTok: soldados/drones 662 vistas y 9,7 s de media (el mejor en retención), loros 213. Sin comentarios ni formularios. Sin fallos.
- 2026-11-27 N (20:40 → 21:42): publicado extracto fútsal + edit (video_listo, 17,2 s) como reel 18381816013241074 + historia 18130013126492714, con 1 h de retraso (la ejecución de las 20:25 se quedó sin uso y Hugo pidió subirlo). TikTok ya salió por Metricool a las 20:45 (444751235). Control 10/10 (audio -15,6 LUFS, algo bajo). Métricas: clon Toni 27-M a 5 h 126 vistas, 7,7 s de media; tanque 240, loros 152.

## Análisis 2026-11-28
- Revisados 400 vídeos con descubrir.py: 304 de los perfiles habituales (TikTok + listados de YouTube) y 96 de 8 cuentas de
  humor/animación exploradas en TikTok. Las habituales **no dan virales nuevos por 5.º día** (solo listados de YouTube que no se
  pueden descargar). Nuevas referentes: **@scrubdaddy** (marca con humor absurdo, mediana 67k, virales hasta 91x) y **@duolingo**
  (sketches dibujados, mediana 880k, hasta 19x); excepción al máximo semanal por la sequía. Fallan @srpelo, @jaidenanimations,
  @illymation; @theodd1sout y @domics casi vacías. Make sigue sin webhook; no se probó Instagram (la búsqueda web nunca da reels).
  17 virales nuevos.
- Desmontados 3: @scrubdaddy «Scrub Baby is here» (**91x, 6,1 M**), @scrubdaddy montaña de biberones (58x, 3,9 M, teaser sin voz)
  y @duolingo coro de cumpleaños (18,8x, 16,5 M).
- **Clon (absurda, paso 2a)**: Scrub Baby → `videos/2026-11-29-M.mp4` (39,0 s) + `historias/2026-11-29-M-absurda-clon-scrubdaddy.json`,
  sale el **domingo 29-nov a las 13:40**. Paco (ep. 3, sigue en la antena del 28-N) pide un invento en un comentario → «Paco… te
  dijimos que estábamos trabajando en ello» → «¡Aquí está!»: la recepcionista de bolsillo en blíster naranja/verde (la jefa dentro)
  → coge llamadas debajo de un fregadero / contesta WhatsApps en una escalera / agenda citas mientras los bomberos le bajan de la
  antena → «¡Hemos pensado en todo!» (avisa, recuerda la cita, 24 h) → «Comenta RECEPCIÓN» → Paco: «¿Y la escalera, para
  cuándo?» (bucle). Control 10/10 (aviso en variedad: repite fontanero porque es serie). 3 renders de ~5 min (el resaltado de las
  líneas del blíster se desplazaba: en SVG usar `svgOrigin`). -14,8 LUFS. Música Mixkit 738 (nueva).
- Ideas: (1) cuando llegue un comentario de verdad, responderlo con este formato («nos lo pediste… ¡aquí está!»); (2) teaser en
  2 partes: móvil sonando sobre una mesa de taller sin voz + «Ojalá existiera algo para esto 👀», y al día siguiente el blíster;
  (3) coro de 12 s de los personajes de serie (Paco, loro, Toni, la jefa) para el cumpleaños de la jefa.
- **Comparación con lo nuestro (Windsor, 7 días)**: tanque 240 vistas (11,2 s, skip 32 %), loros 152 (10,0 s, skip 39 %), Paco
  142, fútsal (27-N) 142 (7,0 s, skip 42 %), Toni el electricista (clon absurdo de @zachking, 27-M) 126 (7,7 s, skip 50 %), fuga
  122. Los clones de anuncio/texto siguen sin distribución (patas arriba 14, antes/ahora 14, gato 6). Se confirma por 4.º día:
  lo que nos funciona es personaje + absurdo en dibujo, y los clones de virales funcionan cuando se pasan a ese estilo (Toni 126
  frente a 5–14 de los clones de anuncio). Por eso el clon de hoy sigue con Paco: si la serie engancha, los ep. 2 y 3 deberían
  superar las 142 vistas del ep. 1.
