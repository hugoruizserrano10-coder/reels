> **Antes de crear cualquier reel, leer `GUIA_REEL.md`** (estructura por segundos, edición, ganchos; investigación del 27-nov).

# Plan diario de reels — norte.local

Instrucciones para la tarea programada. Desde el 23-nov **se publican 2 reels al día** (prueba de 2 semanas pedida por
Hugo; en el informe se compara con la etapa de 1 al día). La tarea arranca a las 13:25, 16:25 y 20:25 (Madrid) para tener
el reel listo y revisado y **publicar a las :40**. Franjas en `datos/horarios.json`:
- **Franja M (mediodía, 13:40)** → el clon del viral preparado por la tarea de análisis (o una historia PRO si no hay).
- **Franja N (noche, 20:40)** → **historia absurda con giro, todos los días** (banco: `historias/absurdas.md`; es lo que
  mejor funciona en Instagram y TikTok desde el 24-nov). Si hay un extracto aprobado por Hugo en la cola, va aquí.
- Desde el 26-nov la franja M (13:40) es el **clon de una historia absurda viral** (ANALISIS_DIARIO.md §2a). Los clones de
  anuncios/texto ya no se publican (datos: <3 s de media). Los que ya estén en la cola se publican a las 20:40 como prueba.
- 1 de cada 5 días la franja M se mueve a las 16:40 para seguir probando horas (lo marca `horarios.json`).
Las ejecuciones que no tocan terminan sin hacer nada.

## 0. Preparación
- Leer `datos/diario.md` (lecciones de ejecuciones anteriores: errores y cómo se arreglaron) y aplicarlas.
- Conectar el repositorio `hugoruizserrano10-coder/reels` (add_repo con push) y clonarlo en /home/claude/reels.
- Fecha y hora de Madrid. Saber qué franja es esta ejecución (M o N) según `datos/horarios.json`: a las 13:25 toca M
  salvo los días de prueba de 16:40 (días desde inicio % 5 == 4), en los que M se hace a las 16:25; a las 20:25 toca N.
  Si esta ejecución no corresponde a ninguna franja de hoy → terminar sin hacer nada.
- Si en `datos/registro.json` ya hay un reel con `fecha` = hoy y `franja` = esta franja → terminar.
- Historia de esta franja: `historias/AAAA-MM-DD-M-*.json` o `historias/AAAA-MM-DD-N-*.json`. Si no existe: en M, el
  primer clon libre (`"clon_de"`) de `historias/`; si no hay clon, crear una historia PRO; en N, crear una historia PRO
  o de palabras gigantes (alternando). Vídeo: `videos/AAAA-MM-DD-M.mp4` / `videos/AAAA-MM-DD-N.mp4`.

## 1. Medir (Windsor, conector instagram, cuenta 17841476774457077)
- Para cada reel del registro con >24 h y sin `metricas_24h`, o >72 h y sin `metricas_72h`, leer con get_data:
  media_id, media_views, media_reach, media_reel_avg_watch_time, media_reel_skip_rate, media_like_count,
  media_comments_count, media_saved, media_shares, timestamp (rango amplio, p. ej. last_30d; filtrar por media_id).
- Guardar en el registro. Calcular `pct_visto` = avg_watch_time / (duracion_s*1000).
- Leer comentarios nuevos (comment_text, comment_username, comment_timestamp). Si alguien comenta RECEPCIÓN o pregunta algo,
  **no contestar automáticamente**: incluirlo en el resumen para Hugo.
- Leer `followers_count`. Si llega a 1.000 (umbral de los trial reels), empezar a usar `trial_params` para los experimentos arriesgados
  (graduation_strategy SS_PERFORMANCE) y apuntarlo en aprendizajes.
- Contactos de la web: buscar en Gmail `subject:"norte.local ·" newer_than:2d` (correos de FormSubmit con "Nueva petición de demo"
  o "Cuestionario rellenado"). Resumir cada uno para Hugo (empresa, ciudad, teléfono, cuándo llamar). No contestar por él.

## 2. Aprender
- Comparar el último experimento con la base (vistas, % visto, skip rate, envíos y me gusta por alcance).
  Con pocos datos, no sacar conclusiones fuertes: hacen falta al menos 2–3 reels por variante.
- Actualizar `datos/aprendizajes.md`: tabla de experimentos, reglas (añadir/quitar según los datos).
- Las preguntas repetidas de comentarios y formularios son ideas de reel y de FAQ para la web: apuntarlas.
- Los lunes: buscar en la web (WebSearch) novedades sobre reels que funcionan (estructura, ganchos, duración, algoritmo)
  y apuntar lo útil con su fuente. Si hay vídeos en la carpeta `referencias/` que no estén analizados, sacar fotogramas
  con ffmpeg, estudiar la estructura y apuntarla.
- Los lunes, además: revisar la web (index.html, cuestionario.html): sacar capturas con Playwright y Chrome
  (/usr/bin/google-chrome, escritorio y móvil), comprobar enlaces, y mejorar textos o preguntas frecuentes con lo aprendido
  en comentarios y formularios. Commit y push. Mantener la estética y no inventar testimonios ni resultados.
- Horarios: cuando haya ≥4 reels por franja, elegir la ganadora y escribirla en `franja_fija`.

## 2b. Descubridor, virales y desmontaje
> Desde el 22-nov lo hace cada mañana la tarea "Análisis diario de reels" (ver ANALISIS_DIARIO.md). Aquí solo: leer la
> entrada "Análisis" de hoy en datos/diario.md y aplicar sus ideas. Si esa tarea no ha corrido hoy, hacer lo de abajo.
Copia del sistema "content-os" de @curiosfer, con la API oficial de Instagram (sin scraping).
- **Montaje automático del Descubridor** (una sola vez): si `make_descubridor_webhook` es null, mirar en Make (organización 9494560,
  equipo 3444695, plan gratuito: máx. 2 escenarios y 1.000 operaciones/mes) si ya hay una conexión de tipo Instagram for Business
  (connections_list). Si la hay: crear el escenario "Descubridor norte.local" = webhook (recibe {"usuario"}) → Instagram for Business
  "List public user posts" (GetUserDataMedia, 25 publicaciones, con like_count, comments_count, timestamp, permalink, caption,
  media_type, media_url) → agregador → "Webhook response" con el JSON. Validarlo, activarlo, probarlo con una cuenta de referentes,
  guardar la URL del webhook en `datos/config.json`, commit, y avisar a Hugo de que ya funciona. Si no hay conexión, seguir sin él.
- **Descubridor**: si `datos/config.json` tiene `make_descubridor_webhook`, llamarlo (POST {"usuario": ...}) para cada cuenta de
  `datos/referentes.json`. Devuelve sus últimas publicaciones con me gusta, comentarios, fecha, enlace, descripción y media_url.
- **Virales**: para cada cuenta, mediana de me gusta + comentarios de sus últimas 25 publicaciones; un reel es viral si supera
  `umbral_viral` veces esa mediana (es lo que hace content-os: "por encima de lo normal de su creador"). Guardar en `datos/virales.json`.
- **Desmontar** los 2 virales más fuertes que no estén ya en `datos/desmontajes/`: descargar el vídeo (media_url) solo para analizarlo,
  `python3 generador/desmontar.py video.mp4 <usuario>-<fecha>`, mirar las hojas de fotogramas y escribir el análisis en su `ficha.md`.
  Nunca resubir ni copiar el vídeo, la música o el texto: solo la estructura, el tipo de gancho, las frases puente y el ritmo.
- Pasar lo aprendido a `datos/ganchos.md` y `datos/formatos.md`, y usarlo en los siguientes reels.
- **Contador**: después de cada ronda, sumar en `datos/contador_analisis.json` (total e historial con la fecha) cuántos reels se han
  revisado, cuántos eran virales y cuántos se han desmontado. Al medir nuestros reels, sumar también `propios_medidos`.
- Si no hay webhook todavía: desmontar los vídeos nuevos de `referencias/` con el mismo programa.

## 2c. Pruebas (cuando uno funciona)
- Si un reel nuestro tiene a las 72 h el doble o más de visualizaciones que la mediana de nuestros reels, al día siguiente hacer una
  variante: la misma historia con otro tipo de gancho (y otro color de acento o arranque visual). Apuntar `variante_de` en la historia.
- Cuando la cuenta llegue a ~1.000 seguidores, publicar esas variantes como trial reels (`trial_params`, graduation_strategy SS_PERFORMANCE),
  que solo ven los que aún no nos siguen.

## 3. Crear el reel de hoy
- Si ya existe `historias/AAAA-MM-DD-*.json` para hoy (preparada de antemano), usar esa. Si su "tipo" es "video_listo",
  el vídeo ya está hecho y revisado (Hugo lo aprobó): NO generar nada, publicar directamente el archivo de "video_listo"
  con su caption (paso 4) y apuntar `formato` y `variante` en el registro.
- Escribir `historias/AAAA-MM-DD-<tema>.json` (mismo formato que las anteriores). Elegir un caso de `historias/banco.md`
  (no repetir oficio + problema en 7 días), marcarlo como usado y añadir 1–2 casos nuevos al banco. Nombres y empresas inventados.
- **Variar el tipo de negocio cada día** entre los clientes potenciales (talleres, reformas, academias, inmobiliarias, estética y peluquería,
  fontanería y climatización, gimnasios, tiendas…): nunca el mismo tipo dos días seguidos, y cada historia distinta. Adaptar al negocio
  el título, la escena, la agenda, el resumen, el estado de "cerrado", la etiqueta y los hashtags. Apuntar el tipo en el registro
  (`tipo_negocio`) para ver qué negocios dan más visualizaciones y comentarios.
- **Gancho**: elegirlo de `datos/ganchos.md` siguiendo sus reglas (resultado o dato concreto en el primer segundo, nunca empezar
  contando la historia sin resultado). Apuntar `tipo_gancho` en la historia y en el registro. Por defecto usar la escena `g0`
  (resultado primero) hasta que los datos digan otra cosa; ir probando los otros tipos de uno en uno.
- **Clones de virales (prioridad, Hugo 22-nov):** si hay en `historias/` un clon preparado por la tarea de análisis
  ("tipo":"video_listo" con "clon_de"), se publica ese. En el registro apuntar `clon_de` para comparar clones con
  historias propias en el informe.
- **Formato PRO (historias propias, 1–2 días por semana como control):** `"tipo":"pro"` → animaciones motion con
  Remotion (remotion/src/ReelPro.tsx): títulos que entran palabra a palabra, contadores, avisos del móvil, chat con
  "escribiendo…", agenda que se llena, subtítulos palabra a palabra sincronizados con la voz (faster-whisper), música
  libre de Mixkit (`musica_mixkit`, cambiar de pista cada semana: 623, 1167, 744, 729, 471…) y efectos. Ejemplo:
  `historias/ejemplo-pro-peluqueria.json`. Escenas: hook · notifs · chat · agenda · lista · cta. Tarda ~4 min en
  renderizar. Si falla el render, rehacer la misma historia con el formato A antiguo y apuntarlo en diario.md.
  Ritmo: seguir "Ritmo y claridad" de datos/aprendizajes.md (voz 1.05, pausas, campo "en", sin subtítulos sobre chats).
  Cuando haga falta una escena nueva (p. ej. llamada entrante, mapa, gráfico), añadirla en ReelPro.tsx siguiendo la
  habilidad `remotion-best-practices` (.claude/skills). Para piezas de motion graphics cortas y pulidas también se puede
  usar HyperFrames (habilidad `hyperframes`, ver ANALISIS_DIARIO.md para cómo ejecutarlo).
- **Formatos — rotación semanal:** 5 días historias (formato PRO; el A antiguo solo como respaldo) y 2 días formato F (`"tipo":"palabras"`).
  Hugo (22-nov) quiere el F **con un inicio de vídeo real, gracioso o raro, como los reels de referencia** (chut de fútbol,
  gato con gafas…), y después corte seco a nuestras palabras y la CTA. Ese inicio sale SIEMPRE de un vídeo de stock gratuito
  con licencia comercial (Mixkit: `"intro":{"tipo":"clip","mixkit":<id>,...}`; se descarga al generar y no se sube al
  repo). Buscar clips en mixkit.co/free-stock-video/<tema>/ (graciosos, satisfactorios o de tensión de 2–4 s) y no repetir
  clip. **Nunca usar el vídeo de otro creador de Instagram/TikTok** (derechos de autor y la norma de originalidad de
  Instagram penaliza la cuenta). `"encuadre":"marco"` + `"texto_arriba"` para el estilo meme (texto blanco arriba).
  El formato G (cuento dibujado, `borrador-cuento-fontanero.json`) está en pausa: a Hugo no le convenció el dibujo.
  Todos se generan con `generador/hacer_reel.sh historias/<id>.json …` (el script mira "tipo"). Todo gancho pasa el test
  PCD de `datos/ganchos.md`. Apuntar `formato` en el registro para comparar formatos.
- Consultar `datos/formatos.md`: si los datos dicen que el formato A se agota (vistas y % visto bajando 5 reels seguidos),
  construir el siguiente formato ampliando el generador.
- Descripción: servicio y oficio concretos (sin municipios: trabajamos en remoto), 3–6 hashtags de oficio y generales.
- CTA: alternar "Comenta RECEPCIÓN" con "Envíaselo a alguien que tenga un <tipo de negocio del reel>" (los envíos pesan mucho)
  y medir cuál da más comentarios/envíos.
- Mantener lo que funciona y **cambiar una sola cosa** respecto a la mejor versión (la siguiente de "Ideas pendientes"
  o lo que sugieran los datos). Apuntar en el JSON `"variante"` qué cambia.
- Si los datos piden cambiar la estructura o la estética, se puede editar `generador/render.py`, pero sin romper
  las historias anteriores y revisando el resultado.
- No prometer cosas falsas: la recepcionista contesta, entiende, ofrece horas de la agenda, crea la visita, avisa al dueño y recuerda la cita.
- Generar: `generador/hacer_reel.sh historias/<id>.json videos/AAAA-MM-DD.mp4`.
- **Revisar** la hoja `videos/AAAA-MM-DD_revision.jpg` (y fotogramas sueltos si hace falta): textos que no se corten,
  horas y nombres coherentes entre escenas, logo al final. Si algo falla, corregir y volver a generar. No subir la hoja de revisión.

## 3b. Música (Hugo, 25-nov: "aplica la música de fondo")
- **Todos los reels llevan música de fondo** que se oiga (no un pulso flojo): bajo la voz a volumen ~0,2–0,25 de la voz;
  sin voz, protagonista. Siempre libre de derechos con uso comercial: Mixkit (https://mixkit.co/free-stock-music/,
  descargar `https://assets.mixkit.co/music/<id>/<id>.mp3`) o Pixabay Music. Elegir estilos que suenan en tendencia en
  reels (phonk, funk, hip-hop suave, lo-fi, electrónica con ritmo marcado) y cambiar de pista cada pocos días; apuntar el
  id en el registro (`musica`) para ver cuál funciona mejor. Nunca canciones comerciales (Instagram/TikTok las silencian o
  penalizan en contenido de empresa).
- Lunes: mirar en TikTok Creative Center → Biblioteca de música comercial → "Top Music" (o búsqueda web de "canciones
  tendencia TikTok España esta semana") y apuntar en `datos/musica.md` 3–5 sonidos en tendencia que estén en la biblioteca
  comercial. En el mensaje a Hugo para TikTok, sugerirle uno de esos para que lo añada al subir (a volumen bajo, encima del nuestro).

## 3c. CONTROL DE CALIDAD (obligatorio, ~10 min antes de publicar — Hugo, 22-nov)
Antes de publicar, repasar `CONTROL.md` punto por punto con el vídeo y la historia de esta franja, y guardar el resultado
en el registro como `"control": {"punto": "ok" | "corregido: …" | "fallo: …"}`. Si algún punto obligatorio falla:
corregirlo y volver a generar; si no da tiempo, publicar la siguiente historia preparada que sí pase el control y avisar a
Hugo. Nunca publicar algo que no haya pasado el control.

## 4. Publicar
- `git add historias videos/*.mp4 datos` → commit → `git push` (con push.negotiate=true).
- URL pública: `https://raw.githubusercontent.com/hugoruizserrano10-coder/reels/main/videos/AAAA-MM-DD-<franja>.mp4`
  (comprobar con curl -I que da 200).
- Windsor execute_action: connector instagram, action create_video_post, account 17841476774457077,
  params {video_url, caption (del JSON), share_to_feed: true}.
- Si el vídeo dura entre 3 y 60 s, publicarlo también como historia (create_story con el mismo video_url) para que lo vean los seguidores.
- Publicar a las :40 (esperar si el control termina antes). Apuntar en el registro: fecha, hora_publicacion, franja (M/N),
  historia, video, media_id, duracion_s, formato, clon_de, variante, cta y control. Commit y push.

## 4a. TikTok — 1 al día, la historia graciosa (Hugo, 27-nov)
- **Solo un TikTok al día: el de la franja N (20:40), que es la historia graciosa/absurda** (lo que funciona en TikTok).
  Si un día la N no es graciosa y la M sí, subir la M. Nunca los dos.
- Metricool gratis = 20 publicaciones/mes → calendario en `datos/tiktok.json`:
  - **Automático (lunes, martes, jueves y sábado)**: en la ejecución de las 20:25, tras publicar en Instagram, programarlo
    con Metricool `createScheduledPost` (blogId **8407772**, Europe/Madrid) para las **20:45**: `media` = enlace raw de
    GitHub, `providers` [{"network":"tiktok"}], `text` = texto TikTok (corto + 3–5 hashtags sin lugares), `tiktokData`
    {"privacyOption":"PUBLIC_TO_EVERYONE","title":"<primera frase, obligatorio>","commercialContentOwnBrand":true,
    "isAigc":true,"autoAddMusic":false}. Añadirlo a `publicados_metricool[<AAAA-MM>]` en datos/tiktok.json.
  - **Manual (miércoles, viernes y domingo)**, o cuando en el mes ya haya 19 automáticos, o si Metricool falla: NO usar
    Metricool. El mensaje a Hugo tiene que empezar por **"📲 HOY TOCA SUBIR A TIKTOK A MANO"** con el enlace
    https://raw.githubusercontent.com/hugoruizserrano10-coder/reels/main/videos/<archivo>.mp4, el texto listo para copiar
    y un sonido en tendencia sugerido.
- Las ejecuciones de las 13:25/16:25 no tocan TikTok.
- Métricas de TikTok: Windsor (tiktok_organic) o Metricool (getAnalyticsDataByMetrics).

## 4b. Retroalimentación de la propia tarea
- Añadir al final de `datos/diario.md` una línea: fecha, qué se hizo, qué falló y cómo se resolvió, y qué cambiar la próxima vez.
- Si un mismo problema aparece 2 veces, cambiar este plan o el generador para que no vuelva a pasar (y apuntarlo).

## 4c. Analíticas que hay que mirar SIEMPRE (Hugo lo pidió: todo automático)
- De cada reel: visualizaciones, alcance, % visto (tiempo medio / duración), % que lo pasa en 3 s, me gusta, comentarios, guardados,
  envíos, y desglose por `tipo_negocio`, `tipo_gancho`, `cta` y franja horaria.
- De la cuenta: seguidores, visitas al perfil, toques en el enlace de la bio.
- Una vez por semana (lunes), una tabla resumen en `datos/semanal.md`: qué tipo de negocio, gancho, CTA, duración y hora funcionan mejor,
  y qué se cambia esa semana por esos datos.

## 5. Avisar a Hugo
Mensaje corto en español: qué se ha publicado y a qué hora, qué se probaba, cómo fueron los reels anteriores
(vistas, % visto, skip rate) y qué se ha aprendido, y comentarios de posibles clientes para que los conteste él.
Si algo falla (publicación, push, render), decirlo claramente y no reintentar en bucle.

## Zona (Hugo, 26-nov)
**Ya no decimos "norte de Madrid" ni nombres de municipios** (ni en el vídeo, ni en la voz, ni en la descripción, ni en los
hashtags): trabajamos en remoto y por llamada con negocios de cualquier sitio. Si hace falta decirlo: "lo montamos todo en
remoto, estés donde estés". Hashtags sin lugares (#negocioslocales #autonomos #pymes #inteligenciaartificial + oficio).
