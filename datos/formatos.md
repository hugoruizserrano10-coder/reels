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
