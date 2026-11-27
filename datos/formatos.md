# Formatos de reel (biblioteca)

Estructuras que funcionan, para variar sin perder lo que da resultado. El generador actual hace el formato A;
los demás se pueden construir ampliando `generador/render.py` (escenas nuevas) cuando los datos digan que el A se agota.

## A. Historia de un cliente perdido → flujo por pasos (el actual)
Basado en el reel de referencia de @marketingconlaurita ("VÉNDELE ESTO A UN DENTISTA POR 3.000 €", 41 s):
- Título fijo arriba en 3 líneas, el número/dinero en naranja. Bajo él: píldora "PASO n · Nombre" + reloj que avanza.
- 0–6 s: escena concreta con hora (23:47, "Lucía manda un audio a su dentista"), la clínica cerrada.
- Giro: "Normalmente ese audio se queda sin respuesta" → mensaje de rechazo ("Ya encontré otro dentista").
- Pasos: Escucha (transcribe) → Entiende (agente con Cerebro/Memoria/Agenda, etiqueta "Urgente") → Agenda (responde con 2 horas,
  crea cita, guarda ficha, manda ubicación) → Reporta (resumen a las 08:00 con 3 pacientes) → Recordatorios.
- Cierre: "Todo en 41 segundos" + "¿Quieres este agente? Comenta AGENDA y te envío el flujo completo".
- Ojo: su público eran **otros vendedores/agencias** ("véndele esto"); el nuestro son los **dueños**. Por eso nuestro gancho habla de obras perdidas.

## B. Error que te cuesta obras (lista, ~20 s)
"3 cosas que hacen que pierdas presupuestos" → 1 contestar al día siguiente, 2 no preguntar zona y plazo, 3 no recordar la visita → "la tercera la arreglamos en 1 minuto".

## C. Antes / después en pantalla partida (~15 s)
Izquierda: el móvil del reformista con 6 mensajes sin leer a las 22:00. Derecha: los mismos, contestados y con 3 visitas en la agenda.

## D. Pregunta directa al dueño (~10–15 s, para enviar)
"¿Cuántos mensajes te llegan mientras estás en obra?" + contador que sube + "Envíaselo a alguien con empresa de reformas".

## E. Demo real grabada (cuando haya cliente o demo en n8n)
Grabación del móvil escribiendo al asistente y su respuesta en tiempo real. Es lo más creíble; necesita a Hugo 1 minuto.

## Cómo analizar reels nuevos
- Hugo sube grabaciones de pantalla a `referencias/`. La tarea de los lunes saca fotogramas cada 1 s con ffmpeg,
  apunta: duración, gancho (qué se ve y se dice en 0–3 s), cuándo cambia la imagen, estructura, CTA, y lo añade aquí como formato nuevo.
- Copiamos estructura, ritmo y tipo de gancho; nunca el vídeo, la música ni los textos.

## F. Palabras gigantes (8–15 s) — `python3 generador/palabras.py historias/<id>.json salida.mp4`
Una palabra o frase enorme por golpe de ritmo, cortes secos, fondos alternos crema/oscuro/naranja, efectos zoom/sube/
sacude/tachar y la palabra clave en naranja con *asteriscos*. Opcional: intro de interrupción con avisos de "Llamada
perdida" cayendo. Sin voz (el ritmo es la música). Al ser tan corto se ve entero y se repite → mucho % visto.
Ejemplo: `historias/ejemplo-palabras-llamadas.json`. Usarlo 1–2 veces por semana alternando con el formato A.

## G. Analogía absurda con giro (25–35 s) — pendiente de generador
Historia ilustrada que no parece anuncio → giro que conecta con el problema del negocio → lista de tareas que se tachan
con ✓ "lo hace sola" → CTA. Se puede hacer con render.py usando tarjetas grandes; pendiente: escenas ilustradas planas.

## H. Lista numerada "N cosas que hace tu recepcionista" (20–30 s)
Números gigantes 01…N, una idea por golpe, pensado para que lo guarden ("guarda este vídeo"). Se puede con palabras.py
(una tarjeta por número) o con render.py.

## Efectos para dar profundidad (vídeo de @annderrey) — ideas para el generador
Zoom rápido de entrada en cada escena (ya: efecto "zoom"), la cámara atraviesa un objeto al cambiar de escena,
pantalla de móvil que se mueve, gráfico que crece con datos, titulares pegados en la pared, garabatos alrededor.

## I. "God's Eye" / HUD de película (clon del 23-nov, @alejavirivera 58x)
Pregunta de incredulidad sobre un globo con paneles HUD → tarjeta-logo (ojo + letras espaciadas + "conectando…") →
vista aérea nocturna con etiquetas y pins por municipio "en directo" → ficha/chat que se rellena → "No solo eso…" con
líneas amarillas tipo rutas de vuelo → CTA. Subtítulos de 1–4 palabras, los clave a dos tonos (Archivo Black en degradado
naranja + Playfair cursiva blanca). Todo b-roll de Mixkit + HyperFrames, sin persona. Plantilla: `clones/alejavirivera-ojo/`
(generar.py + subtitulos.py; se cambian textos de voz.json y se regenera). ~36 s.

## J. "La mayoría hace A / los que saben hacen B" (@marketingconlaurita, 9,7x)
Autoridad → error de la mayoría → qué es B (diagrama dibujado) → pausa "un segundo" en blanco y negro → antes/ahora
("¿quién estaba detrás? Tú") → CTA comenta palabra. Hacerlo con el estilo dibujo (cuento.py/HyperFrames).

## K. "Noticia + patas arriba" con tipografía cinética (clon del 24-nov, @alejavirivera 5,8x)
Noticia en el s 0 sobre b-roll → destello (cielo) → fondo gris oscuro con palabras gigantes en Playfair cursiva verde neón,
una palabra boca abajo, cruces verdes 3D, marca de agua «IA» y cinta tipo cotizaciones → escalada «No solamente… ni… sino
que además ahora…» sobre b-roll de obra → «Y no hablo de A, hablo de B» → la app en oscuro (agenda, tablero por estados,
aviso, recordatorio, mapa con pines por municipio) → CTA con caja de búsqueda que escribe «RECEPCIÓN». Subtítulos: línea
pequeña + palabra clave grande (Inter 900 / Playfair cursiva). Plantilla: `clones/alejavirivera-patas/` (generar.py +
subtitulos.py; cambiar voz.json y regenerar). ~41 s, render HyperFrames ~3 min.

## L. "Antes/ahora" con imagen vieja (clon del 25-nov, @dotcsv 50,8x)
ANTES con look VHS (grano, baja resolución, REC/PLAY, «2023» gigante) y voz «Hace tres años, esto era…» → plano limpio →
destello + «2026» en «Pero tres años más tarde, esto es lo que podemos lograr» → el AHORA nítido (chat que contesta y agenda)
→ «Resultado que viene de… un terremoto» con sacudida → agenda / aviso / recordatorio en tarjetas → pantalla partida
ANTES/AHORA → fondo coral con la enumeración de negocios palabra a palabra y «TODO.» → CTA en coral → marca. Subtítulos de una
línea blanca en negrita. Plantilla: `clones/dotcsv-antes/` (generar.py; cambiar voz.json, el chat y los planos). ~47 s,
render HyperFrames ~4,5 min. Sirve para cualquier negocio: cambiar el ANTES (contestador, agenda de papel, «pulse 1»).

## M. "Acompáñame a…" proceso de oficio en clave absurda (clon del 26-nov, @soyfranciscorivas 734x)
Voz en off pausada de técnico (2,5 palabras/s) sobre planos de trabajo (Mixkit: banco de taller, placa, soldador,
hidrolimpiadora, esponja con jabón, mecánico con tablet, móvil con WhatsApp) y un móvil en HTML que es «el aparato» al que se
le hace el mantenimiento: lleno de llamadas perdidas → ficha técnica en pegatina → buzón lleno y «luego te llamo» → las
notificaciones salen volando con el agua → los mensajes sin contestar explotan como burbujas de jabón → pieza nueva (la
recepcionista, destello verde) → chat que contesta y agenda → «ya no grabé lo demás…» → CTA coral. Subtítulos blancos con
borde negro (estilo CapCut). Plantilla: `clones/franciscorivas-minisplit/` (generar.py; cambiar voz.json, el oficio y los chats).
~56 s, render HyperFrames ~6–7 min. Sirve para cualquier oficio: «la ITV al WhatsApp de un taller», «la revisión del gas al
buzón de un fontanero»…

## N. "Mensaje solemne de villano" en dibujo (clon del 27-nov, @zachking 5,7x / 68,5 M)
Despacho a oscuras con contraluz (monitor azul, estantes con bombillas), personaje con jersey de cuello alto y gorra naranja
con las manos en pico; subtítulo rojo (Inter 900) que se acumula palabra a palabra en el gancho; después, cortes secos y UNA
palabra clave gigante en serif roja (Playfair Display 700, arriba) por golpe, cada una con golpe de graves; plano en silueta
sobre fondo gris con foco para «me llamo…»; giro «mi jefa» = móvil con gorra y corona que se ilumina; montaje rápido de lo que
hace (llamadas / WhatsApps / visitas / 24 horas) y «Síguela» + CTA. Voz davefx lenta (voz_velocidad 1,08), música Mixkit 671
(cinematic thriller) a 0,4. Plantilla: `clones/zachking-mensaje/` (generar.py; cambiar voz.json y PAL). ~28 s, render ~6 min.
Ojo: el tamaño de las palabras se calcula por longitud (min(210, 900/(0,74·letras))) para que no se corten.
