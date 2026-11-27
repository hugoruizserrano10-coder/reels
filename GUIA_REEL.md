# Guía para cada reel (de la investigación del 27-nov: docs/investigacion-reels-virales.md)

**Idea central: el producto es el chiste.** La recepcionista con IA es el remate que resuelve el desastre, nunca una pausa
publicitaria a mitad. Lo que más empuja: tiempo visto, likes y **reenvíos** (estos pesan más para llegar a no seguidores).

## Estructura por segundos (historia absurda de ~40–50 s, ~100–110 palabras; mínimo aceptable 25 s)
| Tiempo | Función | Qué pasa |
|---|---|---|
| 0–1,5 s | Gancho *in medias res* | Fotograma 0 ya en movimiento, el momento MÁS absurdo; texto grande con una pregunta concreta que el vídeo responde. Nada de logo, saludo ni "IA". |
| 1,5–6 s | Contexto mínimo | "3 horas antes…" + personaje/serie ("El empleado más empanao, ep. 3") |
| 6–10 s | Segundo gancho | "Y lo peor todavía no había pasado" + corte, punch-in y efecto |
| 10–32 s | Regla de tres | Intento 1 → intento 2 (peor, fija el patrón) → intento 3 (el más exagerado, riser antes) |
| 32–40 s | Giro | La recepcionista IA lo resuelve en un segundo; golpe + pausa 0,4 s antes de la frase |
| 40–45 s | Callback + CTA | Chiste final encima + UNA línea de CTA ("Envíaselo a quien nunca coge el teléfono" / "Comenta RECEPCIÓN"); el último fotograma enlaza con el primero (bucle) |

Humor = **violación benigna**: algo va mal pero es inofensivo (dibujo, exageración, personaje inventado). Series con
personajes que vuelven (Paco el fontanero, los loros, el perro de Hacienda) para que la gente repita.

## Edición (todo ya instalado: HyperFrames / Remotion / skills media-use y hyperframes-registry)
- Subtítulos animados de 1–3 palabras, palabra activa en naranja, en el tercio central, **nunca en el 15 % inferior**.
- Un cambio visual cada 2–4 s con duraciones variadas (2,1 / 3,4 / 2,7 s…), nunca fijas. Punch-in 100→112 % con muelle en
  palabras clave; temblor solo en impactos (bloques `cinematic-zoom`, `camera-shake`, `beat-freeze-cut`).
- Textura: `grain-overlay` ligero + LUT `film-fade` al 0,3–0,5 + viñeta suave (en vídeo real; en dibujos solo grano muy suave).
- Sonido: efecto en cada transición (whoosh), pop en elementos, riser antes del giro, impacto en el remate; música a ~0,12
  (≈ −18 dB) bajo la voz; máster a −14 LUFS (`npx hyperframes normalize-audio --lufs=-14`).
- Imagen ágil pero voz pausada (Hugo: "va muy rápido"): pausa antes de cada remate.
- `hyperframes transcribe` traduce si no se fuerza el idioma: forzar español (o usar faster-whisper language="es").
- Música de media-use con MusicGen: NO (pesos no comerciales). BBC SFX: NO. Usar SFX de media-use (Pixabay), Mixkit, Pexels.

## Originalidad
Guion, voz y montaje propios. Instagram solo recomienda el original cuando hay copias; pegar metraje viral ajeno resta
alcance. Los extractos literales solo cuando Hugo lo pida expresamente para una prueba.

## Descripción
Palabras clave del oficio y del problema (mejor que solo hashtags), 2–3 hashtags al final, CTA de reenvío. Sin municipios
(trabajamos en remoto). Sin cebo de interacción ("comenta SÍ si…").

## Medir
Diario: tipo de gancho, historia, hora, duración; a las 48 h reenvíos/alcance, likes/alcance y tiempo medio visto.
Cada variable (gancho, voz, duración, hora) como prueba A/B en el informe semanal.
