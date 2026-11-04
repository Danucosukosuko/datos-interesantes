# Feedback de los vídeos

Fuente: Metricool (Instagram Reels, @explica.exe). Métricas tomadas en cada ejecución programada.
Redes enlazadas: solo Instagram (sin TikTok ni YouTube).

## Vídeos y métricas (actualizado 2026-11-04)

### Instagram
| Fecha | Tema | Categoría | Voz | Gancho (fotograma 0) | Views | Alcance | Likes | Coment. | Guard. | Compart. | T. medio (s) | View rate (>3 s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-27 | ¿Cómo funciona un ordenador? | tecnología | no | título animado | 199 | 161 | 10 | 0 | 4 | 1 | 11,7 | 41,7 % |
| 2026-10-28 | ¿Cómo funciona el WiFi? | tecnología | no | título animado | 175 | 150 | 4 | 2 | 0 | 0 | 9,3 | 34,0 % |
| 2026-11-01 | ¿Cómo viaja un mensaje por internet? | tecnología | no | título animado (fotograma 0 casi negro) | 157 | 141 | 2 | 1 | 0 | 0 | 4,3 | 13,9 % |
| 2026-11-02 | ¿Por qué el cielo es azul? | física | sí | «EL CIELO DEBERÍA SER VIOLETA» fijo | 189 | 165 | 8 | 1 | 0 | 0 | **14,4** | **57,5 %** |

Media Instagram (4): 180 views · 154 alcance · 9,9 s · 36,8 % view rate. Seguidores: 3.

### TikTok
| Fecha | Tema | Voz | Views | Likes | Compart. |
|---|---|---|---|---|---|
| 2026-11-02 | ¿Por qué el cielo es azul? (cruzado) | sí | 1 | 1 | 1 |
| 2026-11-04 | ¿Cómo sabe el GPS dónde estás? | no | — (programado 18:00) | | |

### Créditos de voz (ElevenLabs)
Noviembre: 3.681 / 9.500 (todo de pruebas del 2-nov). Reserva de 900 para la Luna (11-nov).

## Conclusiones y decisiones

### 2026-11-04
- Instagram: el cielo (gancho fijo en fotograma 0 + voz) es el mejor vídeo del canal: 57,5 % pasa de 3 s (antes máx. 41,7 %) y 14,4 s de media (antes máx. 11,7). Un solo vídeo: buena señal, no conclusión. Mantener gancho fijo y voz en temas de explicación.
- TikTok: ALERTA — el cielo lleva ~40 h con 1 visualización. Cuenta nueva, probablemente en revisión o frenada. Si a las 48 h sigue igual y el GPS de hoy también se queda en ~0, proponer a Pablo dar más peso a Instagram.
- Opinión de 1 de 3 personas consultadas por Pablo: «interesantes y bien hechos». Faltan 2.
- Hoy: GPS en TikTok, SIN voz (regla: vídeos solo de TikTok sin voz; además TikTok aún no reparte). Gancho «TU MÓVIL SABE DÓNDE ESTÁS SIN INTERNET».
- Publicaciones de noviembre: 4/20.

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
