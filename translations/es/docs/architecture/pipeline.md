# El pipeline, etapa por etapa

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/pipeline.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/pipeline.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/pipeline.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/pipeline.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

## El ciclo completo

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/pipeline-overview-dark.svg">
  <img alt="Slushpile de principio a fin. Fila uno, de izquierda a derecha: onboard, que te entrevista e ingiere un currículum para escribir el perfil, las preferencias y las historias; búsqueda en bolsas de trabajo, que extrae las publicaciones textualmente y puntúa el ajuste anclado al pool de postulantes y el valor esperado por canal; constructor de postulaciones, que produce el ángulo, el currículum, la carta, la pasada de voz y el paso de humanización; y revisión adversarial, 7 revisores entre los que hay 5 revisores en paralelo a ciegas, que devuelve un veredicto por canal. El constructor y la revisión están unidos por una flecha bidireccional rotulada hasta tres rondas. El flujo baja desde la revisión hacia una caja azul, tú la envías, que hace notar que ninguna habilidad toca un portal, un correo ni un formulario. La fila dos se lee de regreso, de derecha a izquierda: resultado registrado, luego status, que compara las predicciones del pipeline contra los resultados, y luego una flecha punteada rotulada priors que entra a la caja del espacio de trabajo, la que contiene profile.md, preferences.yaml, stories.md y job_search.md. Una flecha punteada une el espacio de trabajo de vuelta con onboard, rotulada escrita por el onboarding, leída por cada etapa." src="../../../../docs/diagrams/pipeline-overview-light.svg">
</picture>

La espina dorsal son tres comandos: `onboard` una vez por espacio de trabajo, y
después `job-board-search` y `application-builder` por empresa y por puesto. El
constructor despacha `explore-experience`, `adversarial-review` y
`removing-ai-tells` por su cuenta.

El ciclo de abajo es la parte que no tiene equivalente en un optimizador de
currículums. Los resultados se registran, `status` regresa lo que el pipeline
predijo contra lo que pasó, y los priors corregidos vuelven a
`preferences.yaml`, donde la siguiente búsqueda los lee. Ve
[memory-and-calibration.md](memory-and-calibration.md).

## Leyenda

Cada diagrama de esta página se dibuja con un solo vocabulario de clases,
definido en `docs/diagrams/theme-light.d2` y `theme-dark.d2`. Los dos archivos de
tema y esta tabla se verifican entre sí con `tests/test_docs.py`.

| Clase | Significa |
| --- | --- |
| `stage` | Un paso ordinario que la habilidad orquestadora ejecuta ella misma |
| `agent` | Una persona despachada: un subagente con su propia definición en `agents/` |
| `gate` | Una compuerta o un bucle con tope: algún punto donde la corrida puede iterar, atascarse o detenerse |
| `memory` | Un archivo duradero del espacio de trabajo, escrito una vez y leído por cada etapa posterior |
| `human` | El único lugar donde tú eres indispensable |
| `terminal` | Un estado terminal para ese diagrama |
| `phase` | Un contenedor que agrupa celdas que corren juntas |
| `flow` | Una arista normal hacia adelante |
| `loop` | Una arista hacia atrás: retrabajo, nueva revisión, otra ronda |
| `writeback` | Una arista que escribe en la memoria del espacio de trabajo |

La distinción entre `stage` y `agent` es la que vale la pena leer con cuidado.
Una caja `agent` es un subagente con su propia definición y su propio contexto.
En un harness que no puede despachar subagentes, esas son las que colapsan en un
solo contexto, y ese colapso es toda la diferencia entre una corrida completa y
una degradada.

## `/slushpile:onboard`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-onboard-dark.svg">
  <img alt="Las fases del onboarding. Fila uno: ingerir un currículum en cualquier formato o una exportación de LinkedIn; entrevistar para cubrir los huecos que un documento no puede llenar, con líneas base dadas para los números; profile.md, descrito como el material del que se recorta un currículum y no como un currículum; preferences.yaml, que guarda el método de compensación y las restricciones, con calibration_priors dejado vacío. La fila dos se lee de regreso, de derecha a izquierda: stories.md, de cuatro a ocho historias contables con los números adjuntos; una compuerta de agente de voz que te apunta hacia el tuyo propio y deja is_mine en false hasta que lo tengas; scaffold, que escribe job_search.md y companies.md y corre la verificación de la cadena de herramientas; y verificar y entregar, donde se reporta cada chequeo, incluidos los que pasaron." src="../../../../docs/diagrams/phase-onboard-light.svg">
</picture>

El onboarding es una entrevista, no un formulario. Corre una sola vez y todo lo
que viene después lee lo que él escribió.

Dos de sus pasos son compuertas y no trabajo. El paso del agente de voz se niega
a construir un perfil de voz él mismo: un perfil improvisado a partir de unas
cuantas muestras de escritura se lee como el estilo por defecto del modelo
llevando tu nombre, y tú vas a confiar en él porque se ve terminado. Deja
`voice.is_mine: false` y te apunta a
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
en su lugar. El paso de verificación declara qué chequeos *pasaron*, no
solamente cuáles fallaron, porque un chequeo que reporta únicamente las fallas
es indistinguible de uno que nunca corrió.

`calibration_priors` se deja vacío deliberadamente. Un prior inventado es una
restricción que tú nunca elegiste, y mata puestos en silencio por una razón que
no puedes ver. Se llena más tarde con resultados reales, o se queda vacío y cada
estimación aguas abajo queda etiquetada como no calibrada.

## `/slushpile:job-board-search`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-search-dark.svg">
  <img alt="Las fases de la búsqueda en bolsas de trabajo. Fila uno: descubrimiento, encontrar la URL de carreras y correr varias consultas antes de triar por títulos; captura textual, tomar la publicación tal como está escrita en lugar de resumida; estimación del pool de postulantes, caracterizar quién más se postula mediante arquetipos p50, p75 y p90; y el puntaje de ajuste, donde el número es el percentil dentro del pool y no la coincidencia de palabras clave. La fila dos se lee de regreso, de derecha a izquierda: la matriz de valor esperado por canal a través de frío, referido, contacto directo y entrante, donde el nivel es el mejor canal realmente disponible; criterios de descarte sobre compensación, ubicación y habilitación de seguridad, verificados y declarados en cualquiera de los dos sentidos; una compuerta contrarian que corre antes de que los niveles queden definitivos y puede bajar un nivel o descartar un puesto; y carpetas de puesto, una por puesto con una descripción del trabajo y un análisis, más el tracker y el archivo de empresas actualizados." src="../../../../docs/diagrams/phase-search-light.svg">
</picture>

Esta es la etapa con el mayor retorno, y es la que la mayoría de las
herramientas no tienen. Todo lo que viene después te cuesta una tarde por
postulación. Esta etapa cuesta minutos y puede terminar con "no te postules a
ninguno de estos".

La publicación se captura **textualmente**. 3 agentes leen después ese texto
directamente (el analista de requisitos, el simulador de ATS y el analista del
pool), y una publicación resumida elimina en silencio la redacción exacta de
las calificaciones que esos tres existen para revisar.

La compuerta contrarian corre *antes* de que los niveles queden definitivos y no
después, porque una lista de niveles que ya leíste es una lista de niveles con
la que ya te comprometiste. Ve [scoring.md](scoring.md) para saber qué
significan los niveles y qué revisan los criterios de descarte.

## `/slushpile:application-builder`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-build-dark.svg">
  <img alt="Las fases del constructor de postulaciones. Fila uno: ángulo, elegir el currículum base, la tesis, el gancho y la única historia que vale la pena contar; currículum, adaptado y luego compilado, leyendo el texto extraído y no la fuente; carta de presentación, escrita por el agente de voz nombrado en preferences.yaml; y humanizar, que corre removing-ai-tells con el orquestador aprobando cada cambio. La fila dos se lee de regreso, de derecha a izquierda: revisión adversarial ronda uno, que produce un puntaje ATS, pruebas de intercambio y valor esperado por canal; corregir, primero las correcciones mecánicas y después la profundidad tomada de profile.md; revisión adversarial ronda dos, cuya compuerta de decisión lee el veredicto del canal de mayor valor esperado, unida a corregir por un bucle punteado rotulado tres rondas como máximo; y terminar, la compilación final con application.yaml, el perfil y el tracker actualizados." src="../../../../docs/diagrams/phase-build-light.svg">
</picture>

El constructor escribe, y después ataca lo que escribió. Un modelo al que le
preguntas si su propio borrador es bueno va a decir que sí y con muchas
palabras, así que el constructor nunca pregunta: entrega los materiales a una
revisión que no tiene nada invertido en ellos.

El orden de las correcciones importa. Las correcciones mecánicas van primero
porque son baratas e inequívocas: palabras clave faltantes, fechas con solo el
año, una viñeta copiada casi textualmente de la publicación. Recién entonces
intenta las caras, donde una sección delgada tiene que llenarse desde
`profile.md`, y donde, si el material genuinamente no está en el perfil, corre
`/slushpile:explore-experience` en vez de inventarlo.

**Tres rondas es el techo.** Si el veredicto no se movió para la tercera ronda,
la brecha es estructural y seguir editando es movimiento, no progreso. El tope
existe porque la alternativa es un bucle que siempre encuentra algo, y una
revisión que siempre encuentra algo es indistinguible de una que no encuentra
nada.

## `/slushpile:adversarial-review`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-review-dark.svg">
  <img alt="La revisión adversarial. Primero reunir los materiales: pdftotext sobre el PDF compilado, más la descripción del puesto, el análisis del puesto, preferences.yaml y job_search.md. Eso alimenta un contenedor con 5 revisores en paralelo a ciegas, especialistas despachados en un solo mensaje, sin que ninguno vea el informe de otro: el filtro de triaje a los once segundos con el currículum solamente, el analista de requisitos a los treinta segundos revisando cada calificación, el simulador de ATS como analizador sintáctico y no como lector, el lector fatigado en la postulación sesenta y uno de ochenta, y el analista del pool preguntando quién más está en la fila. Una arista rotulada los cinco devuelven lleva al hiring manager, que ve los cinco informes y produce un veredicto por canal, con la calidad puntuada aparte del valor esperado. Después el contrarian, que ve todo, incluido el hiring manager, y puede revocarlo, y que nunca es opcional. Después el guardián, que es el orquestador y no un agente, que elimina los falsos positivos y los descartes fuera de alcance, vuelve a derivar la decisión neta y reejecuta todo el pipeline con instancias nuevas cuando los materiales cambian. Por último, presentar y registrar, priorizando por impacto sobre el canal de mayor valor esperado y no por cuál agente gritó más fuerte." src="../../../../docs/diagrams/phase-review-light.svg">
</picture>

Los 5 revisores en paralelo del contenedor se despachan en un solo mensaje y no
pueden ver los hallazgos de los demás. A cada uno se le da únicamente lo que su
rol tendría de verdad: al filtro de triaje nunca se le muestra la carta de
presentación, porque un filtro que leyó la carta no es un filtro.

El guardián es la habilidad orquestadora, no un agente. Las personas están
deliberadamente afiladas y parte de lo que producen está mal, así que algo tiene
que aplicar criterio sobre su salida, y ese algo no puede ser una de ellas.

[the-review.md](the-review.md) cubre el orden de despacho, qué se le oculta a
cada persona y qué hallazgos puede eliminar el guardián.
