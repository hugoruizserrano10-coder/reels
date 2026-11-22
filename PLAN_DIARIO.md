# Plan diario de reels — norte.local

Instrucciones para la tarea programada. Se ejecuta 3 veces al día (13:40, 16:40 y 20:40, hora de Madrid),
pero **solo publica una vez al día**: la ejecución de la franja que toca según `datos/horarios.json`.
Las demás ejecuciones del día terminan sin hacer nada.

## 0. Preparación
- Leer `datos/diario.md` (lecciones de ejecuciones anteriores: errores y cómo se arreglaron) y aplicarlas.
- Conectar el repositorio `hugoruizserrano10-coder/reels` (add_repo con push) y clonarlo en /home/claude/reels.
- Fecha y hora de Madrid. Si hoy ya hay un reel en `datos/registro.json` con `fecha` = hoy y `hora_publicacion` no nula → terminar.
- Calcular la franja de hoy: si `franja_fija` no es null, usarla (salvo 1 de cada 5 días, que se prueba otra);
  si no, `orden[(días desde inicio) % 3]`. Si la hora actual no corresponde a esa franja (±30 min) → terminar sin hacer nada.

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
  o "Cuestionario rellenado"). Resumir cada uno para Hugo (empresa, municipio, teléfono, cuándo llamar). No contestar por él.

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
- **Formato PRO (desde el 23-nov, el de por defecto para las historias):** `"tipo":"pro"` → animaciones motion con
  Remotion (remotion/src/ReelPro.tsx): títulos que entran palabra a palabra, contadores, avisos del móvil, chat con
  "escribiendo…", agenda que se llena, subtítulos palabra a palabra sincronizados con la voz (faster-whisper), música
  libre de Mixkit (`musica_mixkit`, cambiar de pista cada semana: 623, 1167, 744, 729, 471…) y efectos. Ejemplo:
  `historias/ejemplo-pro-peluqueria.json`. Escenas: hook · notifs · chat · agenda · lista · cta. Tarda ~4 min en
  renderizar. Si falla el render, rehacer la misma historia con el formato A antiguo y apuntarlo en diario.md.
  Ritmo: seguir "Ritmo y claridad" de datos/aprendizajes.md (voz 1.05, pausas, campo "en", sin subtítulos sobre chats).
  Cuando haga falta una escena nueva (p. ej. llamada entrante, mapa, gráfico), añadirla en ReelPro.tsx.
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
- Descripción: servicio + municipio concretos (Instagram muestra reels en Google), 3–6 hashtags locales y de oficio.
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

## 4. Publicar
- `git add historias videos/*.mp4 datos` → commit → `git push` (con push.negotiate=true).
- URL pública: `https://raw.githubusercontent.com/hugoruizserrano10-coder/reels/main/videos/AAAA-MM-DD.mp4`
  (comprobar con curl -I que da 200).
- Windsor execute_action: connector instagram, action create_video_post, account 17841476774457077,
  params {video_url, caption (del JSON), share_to_feed: true}.
- Si el vídeo dura entre 3 y 60 s, publicarlo también como historia (create_story con el mismo video_url) para que lo vean los seguidores.
- Apuntar en el registro: fecha, hora_publicacion, franja, historia, video, media_id, duracion_s, variante, cta. Commit y push.

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
