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

## 3. Crear el reel de hoy
- Si ya existe `historias/AAAA-MM-DD-*.json` para hoy (preparada de antemano), usar esa.
- Escribir `historias/AAAA-MM-DD-<tema>.json` (mismo formato que las anteriores). Elegir un caso de `historias/banco.md`
  (no repetir oficio + problema en 7 días), marcarlo como usado y añadir 1–2 casos nuevos al banco. Nombres y empresas inventados.
- **Variar el tipo de negocio cada día** entre los clientes potenciales (talleres, reformas, academias, inmobiliarias, estética y peluquería,
  fontanería y climatización, gimnasios, tiendas…): nunca el mismo tipo dos días seguidos, y cada historia distinta. Adaptar al negocio
  el título, la escena, la agenda, el resumen, el estado de "cerrado", la etiqueta y los hashtags. Apuntar el tipo en el registro
  (`tipo_negocio`) para ver qué negocios dan más visualizaciones y comentarios.
- **Gancho**: elegirlo de `datos/ganchos.md` siguiendo sus reglas (resultado o dato concreto en el primer segundo, nunca empezar
  contando la historia sin resultado). Apuntar `tipo_gancho` en la historia y en el registro. Por defecto usar la escena `g0`
  (resultado primero) hasta que los datos digan otra cosa; ir probando los otros tipos de uno en uno.
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

## 5. Avisar a Hugo
Mensaje corto en español: qué se ha publicado y a qué hora, qué se probaba, cómo fueron los reels anteriores
(vistas, % visto, skip rate) y qué se ha aprendido, y comentarios de posibles clientes para que los conteste él.
Si algo falla (publicación, push, render), decirlo claramente y no reintentar en bucle.
