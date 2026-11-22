# Análisis diario de reels (tarea de cada mañana, 10:17)

Objetivo: cada día ver reels que funcionan, detectar los virales, desmontar los mejores y pasar lo aprendido
a los reels de norte.local **antes** de que la tarea del reel diario (13:40/16:40/20:40) cree el de hoy.
Escribe todo en español.

## 1. Buscar reels (mínimo 40 revisados al día)
Fuentes, por este orden; usa todas las que funcionen:
- **Make** (si `datos/config.json` tiene `make_descubridor_webhook`): POST {"usuario": ...} por cada cuenta de
  `datos/referentes.json`. Si sigue en null, intentar montarlo como dice PLAN_DIARIO.md §2b (una vez).
- **TikTok y YouTube Shorts** con `python3 generador/descubrir.py <perfiles> --n 30 --salida datos/rondas/AAAA-MM-DD.json`.
  Muchos creadores de Instagram publican lo mismo ahí. Guarda en `datos/referentes.json` (campos `tiktok`, `youtube`)
  los perfiles que encuentres de cada referente; si una cuenta no existe o falla, anótalo y no lo repitas cada día.
- **Reels sueltos de Instagram**: búsqueda web (p. ej. `site:instagram.com/reel automatización IA negocio`,
  "reel viral recepcionista IA", "reels más vistos negocios locales") y enlaces que Hugo deje en `referencias/`.
  Se descargan con `python3 generador/descubrir.py --bajar <url> /tmp/vid/<id>` (no hace falta sesión).
- **Ampliar referentes** (2–3 cuentas nuevas por semana como máximo): cuentas en español del nicho (IA para negocios,
  automatización, marketing local, dueños de negocios, reformas/talleres/clínicas que hacen reels) con vídeos que
  superen claramente su media. Añadirlas a `datos/referentes.json` con el motivo. Quitar las que no aporten en 2 semanas.

**Cuidado con los nombres:** antes de usar un perfil de TikTok/YouTube comprueba que es el mismo creador (idioma,
tema, enlace de la bio, mismos vídeos). Ej.: youtube.com/@curiosfer es un canal francés que NO es nuestro referente.
**Instagram limita** las descargas desde la nube (error 429 tras 3–4 seguidas): máximo 5 reels de Instagram al día,
dejando ~1 minuto entre cada uno; Instagram no da visualizaciones sin sesión, solo me gusta (usarlos para comparar).
El grueso de los revisados sale de TikTok y YouTube Shorts, que sí dan visualizaciones fiables.

Viral = 3x la mediana de visualizaciones (o de me gusta+comentarios con Make) de su propio creador.
Guardar la ronda del día en `datos/virales.json` (añadir, sin duplicar por id).

## 2. Desmontar los 3 mejores del día
Los 3 virales más fuertes que no estén ya en `datos/desmontajes/` (prioridad: nicho parecido > formato que podamos
hacer con nuestro generador > más veces la mediana):
1. Descargar solo para analizar → `python3 generador/desmontar.py video.mp4 <cuenta>-<id> ` (transcripción, cortes,
   palabras/segundo, hojas de fotogramas).
2. Mirar las hojas y el primer fotograma y rellenar `ficha.md`: gancho (texto, imagen, tipo según `datos/ganchos.md`,
   cuánto tarda en enganchar), estructura por segundos, frases puente, ritmo (cortes/s, palabras/s), duración,
   CTA, por qué crees que funcionó y **qué copiamos** (solo estructura, nunca vídeo, música ni texto literal).
3. Borrar el vídeo descargado (no subirlo al repo).

Prioriza para desmontar los virales que se puedan clonar sin grabar a una persona hablando (texto en pantalla, objetos, animaciones,
pantallas de móvil, vídeos de stock), porque esos los podemos rehacer igual.
Si no aparece ningún viral nuevo, desmontar igualmente los 2 vídeos con más vistas revisados hoy.

## 2b. CLONAR el mejor viral (lo más importante del día — Hugo, 22-nov)
Hugo quiere que **no nos ciñamos a nuestro diseño**: si un reel se ha viralizado una vez, puede volver a hacerlo.
Cada día se elige el viral más fuerte que se pueda rehacer y se **copia tal cual, cambiando solo la información**
(el negocio, el problema y la oferta de norte.local):
- Mismo gancho (misma frase o misma estructura de frase, traducida y adaptada), mismo orden de escenas y misma duración.
- Mismo estilo visual: colores, tipografía (o la más parecida), tamaño y posición de los textos, estilo de subtítulos,
  transiciones, ritmo de cortes (cortes/s) y de voz (palabras/s) medidos en el desmontaje.
- Mismo tipo de imagen: si el viral usa un vídeo de algo (un objeto, una persona, un paisaje), buscar uno igual o muy
  parecido en Mixkit (gratis, uso comercial). Si es texto animado o animación, rehacerlo con palabras.py, Remotion
  (remotion/src: se pueden crear composiciones nuevas para cada clon) o ffmpeg/PIL.
- Mismo audio: si no tiene voz, el nuestro tampoco; si la tiene, voz con el mismo tono y ritmo. Música del mismo estilo
  (Mixkit). Si lleva voz y la nuestra suena peor que la suya, priorizar texto en pantalla.
- Lo que NO se copia: el vídeo, la música y la voz de otros creadores (el algoritmo de Instagram detecta contenido
  duplicado y lo hunde, y pueden denunciarlo). Solo se usan trozos literales de otros cuando Hugo lo pide para una prueba concreta.
**Herramienta principal para clonar: HyperFrames** (habilidades en `.claude/skills/`, instaladas con permiso de Hugo el
22-nov). OJO: el comando automático `reverse` es de pago (HeyGen Pro) y Hugo no lo tiene: NO iniciar sesión ni pagar.
Se clona a mano con el motor gratuito siguiendo el método de `reverse-any-video`: `measure cuts <video>` para los cortes
exactos, fotogramas de cada plano, y una composición en HTML con los mismos tiempos, colores, tipografía (las incluidas:
Oswald, League Gothic, Archivo Black, Inter…) y tamaños; luego `check` y `render`. Ejemplo completo:
`clones/asadwebsites-balon/` (LEEME.md). Para animaciones con Remotion, seguir la
habilidad `remotion-best-practices`. Exportar antes `DO_NOT_TRACK=1 HYPERFRAMES_TELEMETRY=0` y
`PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome`. HyperFrames no se instala: se ejecuta con
`node .claude/skills/hyperframes/scripts/plugin-cli.mjs <comando>` (init --non-interactive --skip-skills, render --output …).
Renderizar el clon con eso, con `generador/hacer_reel.sh` o el script que haga falta, revisarlo (hoja de fotogramas: que se lea,
que no haya textos cortados, que el gancho se entienda en 1–2 s), subirlo a `videos/<fecha>-M.mp4` y dejar
`historias/<fecha>-M-clon-<cuenta>.json` con `"tipo":"video_listo"`, `"clon_de":"<url del viral>"`, su caption
(adaptada del original) y el tipo de gancho. <fecha> = el primer día cuya franja M (13:40) esté libre, empezando por HOY (la tarea de las 13:25 lo publicará).
Antes de dejarlo listo, pasa tú también el control de `CONTROL.md`.
Ritmo de la semana: clones casi todos los días; 1–2 días a la semana una historia propia (formato PRO) para comparar.

## 3. Pasar lo aprendido a los reels
- Ganchos nuevos o confirmados → `datos/ganchos.md` (con ejemplo y fuente). Formatos → `datos/formatos.md`.
- Escribir en `datos/diario.md` una entrada "Análisis AAAA-MM-DD": cuántos revisados, virales, desmontados y las
  2–3 ideas concretas para los próximos reels.
- Si una idea es clara y se puede hacer con el generador, preparar la historia de mañana en
  `historias/<fecha de mañana>-<negocio>.json` aplicándola (respetando las reglas de `historias/banco.md`:
  no repetir tipo de negocio dos días seguidos). La tarea del reel diario usa la historia preparada si existe.
- Comparar con nuestros reels (Windsor, conector instagram, cuenta 17841476774457077): ¿lo que funciona fuera
  coincide con lo que mejor nos ha ido? Anotar la conclusión.

## 4. Contador y guardado
- Sumar en `datos/contador_analisis.json` (total + historial con la fecha): revisados, virales, desmontados.
- Commit y push ("Análisis diario AAAA-MM-DD").
- No avisar a Hugo cada día salvo que algo falle o se encuentre algo muy bueno (el resumen va en el informe del lunes).
