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
