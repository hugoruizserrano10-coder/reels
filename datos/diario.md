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
