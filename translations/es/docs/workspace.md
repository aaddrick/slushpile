# El espacio de trabajo

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/workspace.md">English</a> ·
  <a href="../../zh-CN/docs/workspace.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../pt-BR/docs/workspace.md">Português (BR)</a> ·
  <a href="../../vi/docs/workspace.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/workspace.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:onboard` se ejecuta en **tu** directorio, no en la copia del plugin,
y todo lo que el pipeline sabe de ti vive ahí.

Ese directorio va a contener todo tu historial laboral, tus cifras de
compensación y tus restricciones. Manténlo en un repositorio **privado**, o en
ningún repositorio. El onboarding te lo va a decir y no va a inicializar uno por
ti, ni agregar un remoto: esa es una decisión que se toma a propósito, no una
que se hereda de un paso de configuración.

## Qué escribe el onboarding

```
profile.md          every factual claim about you
preferences.yaml    compensation, location, constraints, calibration priors
stories.md          four to eight tellable stories, with the numbers attached
job_search.md       the tracker: applications, outcomes, calibration
companies.md        one line per company ever looked at
applications/       one folder per role, created by job-board-search
```

### `profile.md`

**No es un currículum.** Es el material del que se recorta un currículum: varias
veces más largo que cualquier cosa que llegarías a enviar, porque un currículum
es una selección y esto es aquello de lo que se selecciona.

Cada número que hay ahí lleva una línea base o está marcado explícitamente como
que no necesita una. «Reduje la latencia 40%» es inservible hasta que el lector
sabe 40% de qué, y un número sin atribución es justo el que te van a preguntar
en una entrevista y no vas a poder responder. Los números cuya fuente no está
verificada se marcan `UNVERIFIED` en vez de eliminarse.

Crece. Cuando una revisión dice que una sección está floja,
`/slushpile:explore-experience` te entrevista y escribe aquí lo que encuentra,
para que la siguiente postulación arranque desde eso.

### `preferences.yaml`

La mitad legible por máquina. Método y línea base de compensación, restricciones
de ubicación y de reubicación, estado de habilitación de seguridad y de
estudios, los diferenciadores que reclamas, tu agente de voz y
`calibration_priors`.

Dos campos hacen más trabajo que el resto:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

Mientras `is_mine` sea falso, cada habilidad que redacta prosa te avisa antes de
ejecutarse. Consulta [Tu agente de voz](voice.md).

`calibration_priors` empieza vacío y sigue vacío hasta que tengas cinco o más
postulaciones resueltas en un canal. Un prior vacío significa que los agentes
usan los valores por defecto con los que vienen y etiquetan sus estimaciones
como no calibradas, que es el comportamiento correcto: un prior calculado a
partir de dos resultados aleja la puntuación de la realidad más que no tener
ninguno, y encima llega con aspecto de dato empírico.

### `stories.md`

De cuatro a ocho historias que de verdad puedes contar, con los números
incluidos. El constructor elige una por postulación; la entrevista que llegues a
conseguir se apoya en estas.

### `job_search.md`

El tracker, y la memoria de largo plazo del pipeline. Postulaciones, sus
resultados, postulaciones previas por empresa y una sección `Calibration` que
`/slushpile:status` reescribe a partir de tus propios resultados.

El historial de postulaciones previas en una empresa lo leen el analista del
pool de postulantes y el contrarian durante una revisión. Un rechazo previo
en un nivel **más alto** importa de forma material: el reclutador ve todo el
historial del sistema de seguimiento de candidatos, y una postulación posterior
a un nivel más bajo se lee como una caída de varios niveles.

### `companies.md`

Una línea por cada empresa que hayas mirado alguna vez, para que una segunda
búsqueda en la misma empresa arranque desde lo que encontró la primera.

## Carpetas de puesto

`/slushpile:job-board-search` crea una carpeta por cada puesto que sobrevive a
la clasificación por niveles:

```
applications/<Company>/<Function>/<Role>/
  job_description.md    the posting, captured verbatim
  role_analysis.md      pool position, channel EV, kill criteria, contrarian notes
  application.yaml      the record: verdicts, scores, channel used, outcome
  resume.tex            copied per role by the builder
  cover_letter.tex      copied per role by the builder
```

La publicación se guarda **textualmente**, no resumida. 3 agentes analizan ese
texto directamente durante una revisión, y una paráfrasis elimina en silencio la
redacción exacta de los requisitos que ellos existen para verificar.

`application.yaml` es el archivo que `/slushpile:status` lee para armar la fila
y para regresar las predicciones contra los resultados. También es el archivo
que hay que actualizar cuando pasa algo: un rechazo, una preselección, una
entrevista, una oferta. Nada más en el pipeline puede enterarse de eso, porque
el pipeline nunca envía nada y nunca ve una respuesta.

Las plantillas se copian **dentro de cada carpeta de puesto** en lugar de
quedarse en la raíz del espacio de trabajo. Una copia impecable en la raíz se
vuelve una copia desactualizada en el momento en que la primera postulación se
desvía de ella.

## Lo que el plugin nunca guarda

Nada en `skills/` ni en `agents/` deja fijo un dato tuyo. Ningún piso de
compensación, ninguna ubicación, ningún estado de habilitación de seguridad,
ningún empleador. Una habilidad que necesita alguno de esos lo lee de
`preferences.yaml` en tiempo de ejecución, y una compuerta de CI hace fallar la
compilación si un dato personal se filtra al plugin.

Eso es lo que hace que el espacio de trabajo sea portátil y el plugin
actualizable: puedes reinstalar, bifurcar o actualizar slushpile sin tocar nada
sobre ti. Consulta [Datos personales](architecture/personal-data.md).
