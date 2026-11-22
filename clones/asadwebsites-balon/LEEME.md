Clon de prueba (22-nov; v2: Hugo cambió el inicio por el gancho del móvil que se llena de mensajes a las 21:47, el resto igual) del reel de @asadwebsites, hecho con HyperFrames (motor gratuito) copiando sus tiempos medidos
con `measure cuts`: chut 1,73 s → tarjetas de ~1 s alternando claro/oscuro con texto condensado en cursiva → CTA →
marca → cierre con el logo. Cambios: información de norte.local, vídeo del chut de Mixkit 43494 (s 1,25–3,05),
música de Mixkit 623 desde el corte, CTA y marca más largas para que se lean (pedido de Hugo: que se entienda).
Antes de renderizar: copiar assets/chut.mp4 (ffmpeg desde Mixkit) y assets/musica.mp3 (Mixkit 623).
Render: `node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs render --fps 30 --quality high -o salida.mp4`.
