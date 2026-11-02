# Feedback de los vídeos

Fuente: Metricool (Instagram Reels, @explica.exe). Métricas tomadas en cada ejecución programada.
Redes enlazadas: solo Instagram (sin TikTok ni YouTube).

## Vídeos y métricas (actualizado 2026-11-02)

| Fecha | Tema | Categoría | Views | Alcance | Likes | Coment. | Guard. | Compart. | T. medio (s) | Retención | View rate (>3 s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-27 | ¿Cómo funciona un ordenador? | tecnología | 199 | 161 | 10 | 0 | 4 | 1 | 11,8 | n/d | 41,7 % |
| 2026-10-28 | ¿Cómo funciona el WiFi? | tecnología | 175 | 150 | 4 | 2 | 0 | 0 | 9,2 | n/d | 34,0 % |
| 2026-11-01 | ¿Cómo viaja un mensaje por internet? | tecnología | 154 | 139 | 2 | 1 | 0 | 0 | 4,0 | n/d | 14,1 % |
| 2026-11-02 | ¿Por qué el cielo es azul? | física | — | — | — | — | — | — | — | — | — (programado 18:00) |

Media del canal (2 vídeos): 187 views · 156 alcance · (guardados+compartidos)/alcance = 1,6 % · view rate 37,9 % · 10,5 s de 60 s vistos de media. Metricool no devuelve retención (IGRE27) para esta cuenta.

## Ranking de categorías

| Categoría | Vídeos | View rate medio | T. medio | (Guard.+Comp.)/alcance |
|---|---|---|---|---|
| tecnología | 2 | 37,9 % | 10,5 s | 1,6 % |

## Conclusiones y decisiones

### 2026-11-02 (tarde, con Pablo)
- Voz en off: ElevenLabs (Eleven v3, voz elegida por Pablo), con etiquetas de entonación en todas las frases; cierre tranquilo «[cálido] Sígueme para más datos curiosos.» (el entusiasta sonaba forzado).
- Subtítulos generados desde los tiempos exactos de la voz; los dibujos de cada escena se ajustan al momento en que la voz los nombra (make.py --words). La música se mantiene, atenuada bajo la voz.
- Lista de temas reordenada por temporada/tendencias (GPS, otoño, gatos, contraseñas, estaciones, microondas, Leónidas, IA, bostezos…; contactless y precios en 9 la semana del Black Friday; Spotify antes del Wrapped). Cada ejecución mira tendencias de la semana.
- Texto: palabra clave en la 1.ª línea y dicha por la voz, 5 hashtags (límite de Instagram), texto alternativo, primer comentario con pregunta de SÍ/NO.

### 2026-11-02 (diagnóstico de alcance, a petición de Pablo)
- Situación: 3 seguidores. Cada Reel llega a ~140-160 cuentas el primer día y el alcance cae a 0 al día siguiente → Instagram enseña cada vídeo a un grupo de prueba y ninguno ha pasado la prueba.
- Tendencia mala: view rate 41,7 % → 34,0 % → 14,1 %; tiempo medio 11,8 s → 9,2 s → 4,0 s (de 60 s). Guardados+compartidos: 5 → 0 → 0.
- Causa principal encontrada: el fotograma 0 salía casi negro (el título entraba volando desde fuera y, por un fallo del motor, se transparentaba el cierre «09/09»). En el vídeo de internet empeoró porque todo el gancho estaba animado.
- Decisiones aplicadas hoy:
  1. Motor: corregido el fallo de t<0 en el fotograma 0.
  2. Gancho obligatorio en el fotograma 0: afirmación sorprendente, grande, sin animación de entrada (cielo: «EL CIELO DEBERÍA SER VIOLETA»). Vídeo de hoy re-renderizado y sustituido en Metricool.
  3. Texto: primera línea = gancho, línea para invitar a enviarlo por mensaje, 5 hashtags en vez de 16.
  4. Prompt de la tarea actualizado con estas reglas.
- Pendiente de Pablo: enlazar TikTok y YouTube en Metricool; decidir si se prueba voz en off y/o vídeos de ~30 s.

### 2026-11-02
- Métricas sin cambios (ordenador y WiFi idénticos a ayer); el vídeo de internet (1-nov) aún no aparece en Metricool. Siguen siendo 2 vídeos con datos → solo anotaciones.
- Tema de hoy: «¿Por qué el cielo es azul?» (física), primera categoría distinta de tecnología, para poder comparar.
- Formato aplicado: gancho de contradicción en el segundo 0 («la física dice que debería ser violeta»), título completo en 1,5 s y subtítulos desde el inicio; texto del post abre con la misma pregunta-gancho.
- Próximo: alternar (siguiente candidato de la lista: «¿Cómo funciona el GPS?», tecnología).

### 2026-11-01
- 2 vídeos con datos (menos de 4): solo anotaciones, sin conclusiones fuertes.
- El WiFi rindió por debajo del ordenador en todo: view rate 34,0 % vs 41,7 %, 9,2 s vs 11,8 s de visionado medio, 0 guardados/compartidos vs 5. Solo tuvo más comentarios (2). Con una sola categoría probada aún no se puede comparar entre categorías.
- El problema principal sigue siendo el arranque: ~6 de cada 10 personas se van antes de 3 s y de media se ven ~10 s. Se mantiene la decisión de gancho en los 2 primeros segundos (ya aplicada en el vídeo de internet de hoy); su view rate dirá si funciona.
- Planificación: el vídeo de hoy (internet, 18:00) es el 3.º de tecnología seguido; el próximo será OBLIGATORIAMENTE de otra categoría. Primer candidato: «¿Por qué el cielo es azul?» (física), así además se prueba una categoría nueva frente a tecnología.
- Hoy ya hay publicación programada → no se genera vídeo nuevo.

### 2026-10-28
- Solo hay 1 vídeo con datos (menos de 4): se anota, sin conclusiones fuertes.
- Señales a vigilar: tiempo medio de visualización ~10 s de 60 s (≈17 %) y view rate del 41,8 % → posible caída temprana. En los próximos vídeos: gancho visual y textual más fuerte en los 2 primeros segundos y portada/título más llamativos.
- Planificación: sin cambios en el orden de la lista base. Tras dos vídeos de tecnología seguidos (ordenador, WiFi), el siguiente tema debe ser de otra categoría (regla: nunca 3 seguidos de la misma).
- Hoy ya hay publicación programada (WiFi, 17:00) → no se genera vídeo nuevo.
- (añadido 2026-10-28, a petición de Pablo) Vídeo del 2026-11-01 preparado por adelantado: «¿Cómo viaja un mensaje por internet?» (tecnología), programado a las 18:00. Pablo pidió expresamente este tema aunque sea el 3.º de tecnología seguido; el siguiente debe ser de otra categoría. Formato: gancho desde el segundo 0 (título en 1,5 s, sobre cruzando la pantalla y subtítulos desde el inicio).
