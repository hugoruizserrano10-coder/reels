# Aprendizajes de los reels de norte.local

Este archivo lo actualiza la tarea diaria. Arriba lo más reciente y lo que se aplica ya.

## Reglas que aplicamos ahora
- (22-nov) Calidad: efectos de sonido (ding en notificaciones, whoosh entre escenas) y volumen normalizado a -14 LUFS en todos los reels. Voz: Piper "davefx" por defecto; alternativa gratis con licencia comercial clara: Kokoro (Apache 2.0), voces em_alex, em_santa, ef_dora (`"voz_motor": "kokoro", "voz_id": "em_alex"` en la historia). Pendiente de que Hugo elija.
- (22-nov) Ganchos: ver `datos/ganchos.md`. Resultado o número concreto en el primer segundo; el gancho tipo "Son las diez de la noche…" (historia sin resultado) es de los que peor funcionan en 2026.
- (22-nov) Hugo abre la agencia a cualquier negocio local: cada reel, un tipo de negocio y una historia distinta. Medir qué tipo de negocio funciona mejor.
- Instagram reparte los reels sobre todo por **tiempo de visualización / % visto**, luego **envíos por DM por alcance** y **me gusta por alcance**. El % de gente que pasa en los 3 primeros segundos (skip rate) es la señal de alarma. (Fuentes: Buffer, SocialPilot, Later — oct/2026.)
- Lo más concreto (número, dinero, hora, lugar) va en los **3 primeros segundos**: en el título de arriba y en la primera frase.
- Más corto suele ganar en % visto: un reel de 15–30 s visto entero puntúa mejor que uno de 60 s a medias.
- El 65 % de las visualizaciones llega en los 3 primeros días (Metricool 2026): medimos a las 24 h y a las 72 h.
- Estructura que usamos: gancho con tensión (cliente que se pierde) → giro ("pero esta empresa tiene…") → pasos rápidos → resultado concreto → CTA "Comenta RECEPCIÓN".

## Investigación del 22-nov-2026 (crecimiento, visitas y DMs)
- Las 3 señales que más pesan siguen siendo: tiempo de visualización/% visto, envíos por DM por alcance y me gusta por alcance. Para llegar a gente nueva pesan más los **envíos** que los me gusta → probar CTA de "envíaselo a…".
- **Trial reels** (se enseñan solo a no seguidores): requieren cuenta profesional y, según varias fuentes, unos 1.000 seguidores (algunas dicen 200). Windsor los admite (`trial_params`). Activarlos cuando `followers_count` llegue al umbral.
- Para negocio local: ganchos con la ciudad concreta ("en Alcobendas…") y palabras clave locales en el texto; Instagram muestra reels públicos en Google, así que la descripción debe llevar servicio + municipio.
- El carrusel es el formato con más interacción en Instagram (Metricool 2026) → probar 1–2 carruseles por semana además del reel.
- Política de originalidad (abr-2026): penaliza contenido duplicado. Nunca resubir vídeos de otros: copiar estructuras, no vídeos.
- Comentario → DM automático: ManyChat gratis solo 25 contactos/mes (se agota con un reel); alternativas gratis con más margen: Inrō (100 contactos/mes), CreatorFlow (500 DMs/mes), ReplyRush. Es legal porque el usuario pide el mensaje al comentar. Requiere que Hugo conecte la cuenta (Meta).

## Hora de publicación
- Estudios generales para España: picos a las 14–16 h y sobre las 20 h; varían mucho entre fuentes, así que lo decidimos con nuestros datos (ver datos/horarios.json).

## Experimentos
| Fecha | Variable que cambia | Respecto a | Resultado |
|---|---|---|---|
| 2026-11-22 | (base, 47 s) | — | pendiente |
| 2026-11-23 | versión nueva: ~30 s + gancho "resultado primero" (escena g0) + taller en vez de reformas (historia ya preparada: historias/2026-11-23-taller-frenos.json) | base (47 s, gancho de historia) | pendiente |

## Ideas pendientes de probar (una cada vez)
- Gancho con pregunta directa al dueño ("¿Cuántos clientes pierdes los domingos?").
- Empezar sin título grande, directamente con el chat del cliente.
- Otros negocios locales del norte de Madrid (fontanero, electricista, pintor, clínica, academia).
- Velocidad de voz 0.80 (más rápida).
- Gancho con municipio concreto ("Esto pasó en Tres Cantos…").
- Formato "error que te cuesta obras" (lista de 3 errores, ~20 s).
- Loop: que el final enlace con el principio para que se vuelva a ver.
- CTA de compartir ("Envíaselo a alguien que tenga un taller / una academia…", según el negocio del reel) para subir envíos por DM.
