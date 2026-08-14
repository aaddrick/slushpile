# Habilidades

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/skills.md">English</a> ·
  <a href="../../zh-CN/docs/skills.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../pt-BR/docs/skills.md">Português (BR)</a> ·
  <a href="../../vi/docs/skills.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/skills.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile se instala como 10 habilidades. Claude Code expone cada una como
`/slushpile:<name>`; Codex usa `$slushpile:<name>`; Gemini CLI y otros entornos
leen los mismos archivos y ahí pides la etapa con palabras.

Tres de ellas son la columna vertebral. Otras tres se despachan solas mientras
se construye una postulación, y solo las ejecutas a mano sobre materiales que
este pipeline no construyó. Las últimas cuatro las ejecutas cuando hacen falta
y no en secuencia, y una de ellas necesita una carpeta de puesto ya evaluada.

## La columna vertebral

### `/slushpile:onboard`

Prepara el espacio de trabajo. Ingiere un currículum existente o una exportación
de LinkedIn, te entrevista para llenar los huecos y escribe `profile.md`,
`preferences.yaml` y `stories.md`. Verifica la cadena de herramientas de
documentos, arma el tracker y entrega el control.

Ejecútala una vez por espacio de trabajo, antes que cualquier otra cosa.
Consulta [Primeros pasos](getting-started.md) para saber qué tener listo y
[El espacio de trabajo](workspace.md) para saber qué escribe.

### `/slushpile:job-board-search`

Busca en un portal de empleo, extrae cada publicación textualmente, estima el
pool real de postulantes, califica el ajuste anclado al pool y condicionado al
canal, corre los criterios de descarte, pone a un contrarian frente a la lista
de niveles y crea una carpeta de puesto por cada puesto que sobrevive.

**Argumento:** el nombre de una empresa, o una consulta que describa el trabajo
y dónde lo quieres. Dada una consulta, la Fase 0 la resuelve en una lista de
empresas (leyendo tus restricciones desde `preferences.yaml` y tu historial
desde `companies.md`), te muestra esa lista y la busca en cuanto la confirmas.
Todo lo que viene después de la Fase 0 es igual en ambos casos, así que una
evaluación de una corrida por consulta es comparable con una de una corrida por
empresa nombrada y la tabla de calibración puede juntarlas.

Es la etapa de mayor retorno del pipeline y la que la mayoría de las
herramientas no tiene. Todo lo que viene después cuesta una tarde por
postulación; esto cuesta minutos y puede terminar en «ninguno de estos».
Consulta [Puntuación](architecture/scoring.md).

### `/slushpile:application-builder`

Construye el currículum y la carta de presentación dirigidos a una carpeta de
puesto que ya tiene una descripción del puesto y un análisis del puesto, y
después los itera contra la revisión hasta que se estabilizan o llegan al tope
de tres rondas.

**Argumento:** la ruta de una carpeta de puesto.

Despacha `explore-experience`, `adversarial-review` y `removing-ai-tells` por su
cuenta. Nunca envía nada; te entrega archivos terminados.

## Las tres que se despachan por ti

Ejecuta una de estas directamente solo para trabajar sobre materiales que este
pipeline no construyó: un currículum escrito en otro lado, una carta redactada a
mano.

### `/slushpile:adversarial-review`

Corre 7 revisores contra un currículum y una carta de presentación. Devuelve un
veredicto y un rango de probabilidad por canal de envío, la calidad de los
materiales calificada por separado del valor esperado, y una pasada del
contrarian que puede revertir todo lo demás.

**Argumento:** la ruta de una carpeta de puesto que contenga como mínimo un
currículum y `job_description.md`.

Consulta [La revisión](architecture/the-review.md) para saber qué se le muestra
a cada revisor y qué se le oculta a propósito.

### `/slushpile:explore-experience`

Te entrevista para sacar a la luz experiencia que es real pero no está
documentada, mapeada contra los requisitos de un puesto específico, y después la
escribe en `profile.md` de forma permanente.

Úsala cuando una evaluación de ajuste o una revisión marca una sección como
floja. La mayoría de las veces la experiencia resulta ser real y simplemente
nunca se escribió, y por eso esto es una entrevista y no una reescritura.

### `/slushpile:removing-ai-tells`

Elimina giros, estructuras y elecciones de palabras que delatan autoría de IA,
corriendo pasadas iterativas por instancias nuevas del agente de voz mientras el
orquestador filtra cada cambio individual.

Úsala en una carta de presentación antes de enviarla, o en cualquier prosa que
tenga que leerse como escrita por una persona.

## En cualquier momento

### `/slushpile:outreach`

Abre el canal cálido para un puesto. Lee la tabla de referencias y tu perfil
buscando gente que ya conoces en la empresa, te hace la pregunta que ningún
archivo puede responder, investiga contactos con nombre a partir de presencia
profesional pública solo cuando no conoces a nadie, califica cada vía por lo que
esa persona podría decir de verdad sobre tu trabajo, y redacta el pedido de
referencia o la nota en frío con tu agente de voz.

**Argumento:** la ruta de una carpeta de puesto.

Ejecútala cuando la evaluación diga que la referencia convierte varias veces
mejor que el envío en frío y no tengas a nadie que te refiera. Sin esto el
pipeline calcula que tu mejor canal es una referencia, te lo dice, y después
construye materiales de portal en frío igual. Escribe los contactos en
`job_search.md`, que es de donde la búsqueda arma su matriz de canales y de
donde `status` decide si ordenar un puesto por su número cálido o por el frío.
Hasta que ahí haya un contacto real, las dos valoran ese canal como cerrado, con
razón.

Nunca envía nada. Los mensajes son tuyos, desde tu propia cuenta.

### `/slushpile:redesign-templates`

Reestiliza `resume.tex` y `cover_letter.tex` con tu propio estilo de casa
(tipografía, paleta, disposición) manteniendo fijas las restricciones de ATS, y
después demuestra que el resultado sigue compilando y sigue siendo extraíble.

Ejecuta esto en lugar de editar la copia del plugin, que la próxima
actualización reemplaza.

### `/slushpile:status`

Lee cada `application.yaml` del espacio de trabajo e informa el estado de la
búsqueda: la fila ordenada, qué está esperando por ti, qué se quedó en silencio
y la regresión de las predicciones del propio pipeline contra lo que de verdad
pasó. Escribe los hallazgos de calibración de vuelta en `job_search.md` y
`preferences.yaml`.

Ejecútala cuando lleguen los resultados. Consulta
[Memoria y calibración](architecture/memory-and-calibration.md).

### `/slushpile:help`

Explica qué es slushpile, qué hace cada habilidad, en qué orden ejecutarlas,
dónde viven los archivos del espacio de trabajo y cómo configurar un agente de
voz.

Ejecútala cuando no sepas qué ejecutar.
