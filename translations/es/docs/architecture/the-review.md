# La revisión

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/the-review.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/the-review.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/the-review.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/the-review.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:adversarial-review` despacha 7 revisores contra un currículum y una
carta de presentación. Esta página explica por qué tiene esa forma. La imagen
está en [pipeline.md](pipeline.md); las definiciones por agente están en
`agents/`.

## Cuatro modos de falla, cuatro etapas

La forma no es un comité arbitrario. Cada etapa responde a una manera concreta
en que un pipeline de revisión ingenuo produce disparates con seguridad.

**Adulación de perspectiva única.** En un pipeline ingenuo, todos los revisores
trabajan para el candidato. Ninguno modela la fila. El analista del pool de
postulantes existe para forzar el razonamiento comparativo: no "¿son buenos
estos materiales?" sino "¿son mejores que las otras setenta postulaciones que
recibió esta vacante esta semana?".

**Colapso del veredicto.** Una sola respuesta ENTREVISTA / QUIZÁ / DESCARTE
esconde que los mismos materiales convierten a tasas muy distintas en frío que a
través de un referido. Esas son decisiones diferentes sobre tu tarde. El hiring
manager produce un veredicto por canal, con un rango de probabilidad en lugar de
una palabra.

**Preocupación sintética por detección de IA.** Una persona detectora de IA
marca patrones basándose en la duda hipotética de un lector, y va a pasar por
encima del juicio fundamentado sobre lo que un lector real nota. Se la
reemplazó por el lector fatigado, que hace la pregunta contestable: ¿esto
molestaría a alguien en su sexagésima primera postulación del día?

**Sin paso de falsación.** Nada en una revisión normal pregunta qué tendría que
ser cierto para que el ejercicio entero fuera un desperdicio de ciclos. El
contrarian lo pregunta, al final, con permiso para revocar todo lo anterior.

## La etapa ciega

Los primeros 5 revisores en paralelo se despachan en un solo mensaje. A ninguno
se le entrega la salida de otro.

Esta es la propiedad que sostiene toda la revisión, y es la que se degrada en
silencio. La contaminación no produce un error; produce acuerdo. Un especialista
que ya leyó el veredicto de triaje deriva hacia confirmarlo, y cinco informes
que coinciden parecen un consenso fuerte y no una sola opinión repetida cinco
veces. El consenso a lo largo de la etapa ciega es la señal más confiable que
produce el pipeline, y vale algo solamente porque los cinco no pudieron hablar
entre sí.

A cada persona se le entrega únicamente lo que su rol tendría de verdad:

| Persona | Recibe | Se le oculta, y por qué |
| --- | --- | --- |
| Filtro de triaje | Texto del currículum, título, empresa, nivel | La carta de presentación. Está simulando once segundos, y un filtro que leyó la carta no lo es. |
| Analista de requisitos | Currículum, carta de presentación, publicación completa, nivel | Nada. Su trabajo es contrastar cada calificación contra la evidencia. |
| Simulador de ATS | Texto del currículum, publicación completa y la fuente `.tex` o `.docx` si existe | Nada, pero nota que recibe la *fuente* a propósito: las tablas, las columnas y la ubicación de los encabezados son invisibles en el texto extraído y son exactamente lo que existe para detectar. |
| Lector fatigado | Currículum, carta de presentación | Cualquier instrucción de juzgar autoría por IA. Esa es otra pregunta y no es la suya. |
| Analista del pool | Todo, más el historial previo de postulaciones y las tasas de conversión observadas | Nada. Necesita más contexto que los otros cuatro. |

El currículum que lee cada persona es la salida de `pdftotext`, no la fuente en
LaTeX o Markdown. Revisar la fuente es revisar un documento que nadie va a ver
nunca. Si el texto extraído sale vacío o revuelto, eso es un hallazgo y no una
falla de herramientas: un ATS ve lo que ve `pdftotext`.

## Por qué los dos últimos son secuenciales

El hiring manager corre después de que vuelven los cinco, y los ve a los cinco.
El contrarian corre después del hiring manager, y ve todo, incluido eso.

Ordenarlos así cuesta tiempo de reloj y compra lo único que la etapa ciega no
puede dar: alguien que pueda pesar a los cinco entre sí, y después alguien que
pueda atacar ese pesaje. Un contrarian que corriera en paralelo con el hiring
manager estaría discutiendo con una síntesis que nunca leyó.

El contrarian es **automático, no condicional**. Un paso de falsación que corre
solo cuando el orquestador se siente inseguro se va a saltar a sí mismo justo en
los casos donde la seguridad estaba mal puesta.

## Los priors se pasan textualmente, incluso cuando están vacíos

Tanto el analista del pool como el contrarian reciben el bloque
`calibration_priors` de `preferences.yaml` tal como está escrito.

Resumirlo a "el candidato convierte mal" le quita el tamaño de muestra, que es
lo único que dice cuánto peso merece el número. Y omitir el bloque cuando no
está definido se lee, para el agente, como una corrida ordinaria y no como una
sin calibrar: una estimación no calibrada que no está etiquetada como tal es
peor que ninguna estimación, porque aguas abajo es indistinguible de una
calibrada.

Cuando una tasa observada tiene un tamaño de muestra de cinco o más, el analista
del pool tiene instrucciones de usarla en lugar de su propio prior para ese
canal, y de decir que lo hizo.

## El guardián

La habilidad orquestadora es el guardián. No es una de las personas, y eso es
deliberado: las personas están afinadas para ser duras, parte de lo que producen
está mal, y nada afinado para ser duro puede además ser lo que decide qué se
descarta.

Contrasta a cada persona contra su propia carta constitutiva: ¿el filtro de
triaje se quedó dentro de los once segundos, o citó algo de la tercera página?
¿El simulador de ATS marcó un formato que los analizadores modernos manejan sin
problema? ¿El lector fatigado marcó como defecto un marcador de voz
deliberado, documentado en tu propio agente de voz?

Dos clases de argumento del contrarian se **eliminan** en vez de pesarse:

1. **Términos contractuales de la etapa de oferta.** Financiamiento de mudanza,
   bono de firma, equity, fecha de inicio, recomprar una cláusula de devolución.
   Eso se negocia después de que existe una oferta. Matar una postulación por
   dinero que todavía es negociable, en la etapa donde el candidato tiene menos
   poder, es un error de categoría.
2. **Una vacante vecina sin evaluar.** Un puesto que se ve mejor en otra parte
   de la misma empresa no es una entrada a menos que se haya evaluado por
   completo y tú hayas pedido que se pese. La secuenciación entre vacantes es
   decisión tuya.

Todo lo demás que levante el contrarian está en alcance: probabilidad de
conversión, estructura de canal, posición en el pool, brechas de calificación,
exageraciones, fallas en las pruebas de intercambio, densidad de los materiales,
señales de ajuste de nivel e historial adverso de postulaciones en la empresa
objetivo.

Tanto las patas eliminadas como las que sobreviven quedan registradas en
`role_analysis.md`. Registrar solo el resultado hace imposible mejorar la
compuerta, porque los falsos positivos que atrapó se vuelven invisibles en el
momento en que los atrapa.

## El tope de tres rondas

Las rondas se comparan, no solo se vuelven a correr. Un problema marcado en más
de una ronda es real; un problema marcado una sola vez es ruido. Esa señal
existe únicamente si la revisión corre más de una vez, y por eso el constructor
la corre dos veces por defecto.

Cada ronda usa **instancias nuevas del agente**. Una persona que ya vio su
propio veredicto no puede volver a derivarlo de forma independiente, así que
reutilizar un informe entre rondas convierte una segunda opinión en un eco.

Tres rondas es el techo. Más allá de eso, las brechas restantes son
estructurales, y la salida honesta es decirlo en vez de correr una cuarta ronda
y producir más ediciones.

## En un harness sin despacho de subagentes

Codex y Gemini CLI no tienen despacho de subagentes. La revisión igual corre:
las personas se adoptan por turnos, en un solo contexto, y cada informe se
escribe completo antes de que empiece el siguiente.

Dos cosas se degradan, y vale la pena saber cuáles. Es más lenta, lo que no
importa mucho. Y la etapa ciega deja de ser ciega, lo que sí importa: la
contaminación descrita arriba es exactamente lo que reintroduce un contexto
compartido. La habilidad le indica al modelo que escriba cada informe por
completo antes de empezar el siguiente, lo que limita la deriva sin eliminarla.
