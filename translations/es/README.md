<p align="center">
  <img src="../../.github/assets/hero-es.png" alt="Slushpile: una búsqueda de empleo adversarial con memoria. 7 agentes intentan rechazarte antes de que lo haga un reclutador, y lo que encuentran, te lo quedas. Lo que te quedas: profile.md, cada afirmación factual; preferences.yaml, sueldo, ubicación y límites; stories.md, de cuatro a ocho historias contables; job_search.md, resultados para calibrar. Se escribe una vez, lo lee cada etapa, lo actualiza cada revisión. Los 7 revisores: filtro de triaje, analista de requisitos, simulador ATS, lector fatigado, analista del pool, hiring manager, contrarian. 5 revisores en paralelo, ciegos entre sí, luego la síntesis, y luego un agente cuyo trabajo es revocarla." width="100%">
</p>

<p align="center">
  <strong>Slushpile</strong><br>
  <em>7 agentes intentan rechazarte antes de que un reclutador tenga la oportunidad.</em><br>
  <em>Lo que encuentran, te lo quedas.</em>
</p>

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/VonTerraProject501c3/slushpile?style=flat" alt="Licencia"></a>
  <a href="../../.github/workflows/plugin-load-check.yml"><img src="https://img.shields.io/github/actions/workflow/status/VonTerraProject501c3/slushpile/plugin-load-check.yml?label=plugin%20loads&style=flat" alt="Comprobación de carga del plugin"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/aaddrick/">¡Conecta conmigo en LinkedIn!</a>
</p>

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../README.md">English</a> ·
  <a href="../zh-CN/README.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../pt-BR/README.md">Português (BR)</a> ·
  <a href="../vi/README.md">Tiếng Việt</a> ·
  <a href="../en-x-aibro/README.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

<!-- BEGIN GENERATED market-note: scripts/sync_docs.py -->

> **Alcance**: este pipeline modela convenciones de contratación anglófonas, sobre todo estadounidenses: una página, sin foto, sin fecha de nacimiento, orden cronológico inverso y una línea de autorización de trabajo. Si postulas en un mercado local con otras convenciones, los consejos de formato no aplican y la revisión marcará como defectos cosas que allí son normales. Seguimiento en el [issue #2](https://github.com/VonTerraProject501c3/slushpile/issues/2).

<!-- END GENERATED market-note -->

## Instalación

<details open>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Luego, en el directorio donde llevas tu búsqueda de empleo:

```
/slushpile:onboard
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Codex antepone el nombre del plugin a las habilidades que este trae:

```
$slushpile:onboard
```

Codex no despacha subagentes, así que el pipeline de revisión corre sus 7
revisores de forma secuencial en un solo contexto, en vez de tener
5 revisores en paralelo. La misma salida, más lenta y algo más propensa a que
el razonamiento de un revisor se filtre al siguiente.

</details>

<details>
<summary><strong>Cursor, Gemini CLI e instalación manual</strong></summary>

Consulta [INSTALL.md](./INSTALL.md).

</details>

## El problema

No te están evaluando contra la descripción del puesto. Te están evaluando
contra las otras setenta personas que postularon a la misma vacante esta semana.

Casi toda herramienta de este rubro lo entiende al revés. Mete un currículum y
una publicación en un optimizador de currículums y te dirá que tu coincidencia
de palabras clave subió de 68% a 91%, que es un número real sobre la pregunta
equivocada. Si el postulante del percentil 75 de esa fila coincide al 94%, tu
91% es un rechazo, y nada en la herramienta te lo va a decir nunca.

Lo segundo que hacen mal: devuelven un solo veredicto. Pero el mismo currículum
y la misma carta convierten quizá al 2% por un envío en frío al portal y al 30%
por un referido. Esas no son la misma decisión, y colapsarlas en un único
«coincidencia fuerte» no es una simplificación. Es un error con una interfaz
segura de sí misma encima.

El tercero es el que nadie nombra. Estas herramientas no tienen memoria. Pegas
un currículum, recibes un número, cierras la pestaña, y la herramienta termina
la sesión sabiendo exactamente lo que sabía al empezar. Una búsqueda son
cuarenta postulaciones en tres meses. Cada una cuesta precio completo.

## Qué hace esto en cambio

**Construye un modelo de ti, una sola vez.** `/slushpile:onboard` te entrevista y
escribe tres archivos: un perfil, un archivo de preferencias y un conjunto de
historias. El perfil no es un currículum: es el material del que se recorta un
currículum, varias veces más largo que cualquier cosa que llegues a enviar.
Todas las etapas posteriores lo leen, y nada te vuelve a hacer esas preguntas.

**Intenta disuadirte del puesto antes de que escribas nada.** La etapa de
búsqueda puntúa cada publicación contra el pool de postulantes estimado, aplica
los criterios de descarte, arma una matriz de valor esperado por canal de
postulación y pone un contrarian delante de la lista de niveles. Cualquier otra
herramienta empieza a trabajar después de que ya decidiste postular. El error
caro ocurre antes de eso, y esta es la única etapa que todavía puede atraparlo
gratis.

**Va y abre el canal que él mismo dice que es el mejor.** Una matriz que valora
un referido varias veces por encima de un envío en frío no sirve de nada si
nadie actúa sobre ella. `/slushpile:outreach` lee tu propio historial buscando a
alguien que ya conoces ahí, te hace la única pregunta que ningún archivo puede
responder, investiga contactos con nombre a partir de presencia profesional
pública solo cuando no conoces a nadie, y redacta el pedido con tu voz. Califica
cada vía por lo que esa persona podría decir de verdad sobre tu trabajo, y lo
registra en `job_search.md`, que es de donde cada revisión posterior lee si ese
canal está abierto. Nunca envía nada.

**Ataca lo que acaba de escribir.** Un modelo al que le preguntas si su propio
borrador es bueno te va a decir que sí, y largamente. Así que el constructor no
pregunta. Le entrega el currículum y la carta a 7 revisores, con
5 revisores en paralelo que no pueden ver los hallazgos de los demás, y a cada
uno le da solo lo que su rol tendría de verdad: al filtro de once segundos nunca
se le muestra la carta de presentación, porque un filtro que leyó la carta ya no
es un filtro.
El constructor corrige lo que vuelve y lo manda de nuevo. La segunda ronda tiene
que aguantar antes de que te deje enviar, y se detiene a las tres rondas, porque
más allá de eso las brechas son estructurales y seguir editando es puro
movimiento.

**Escribe de vuelta en ti lo que aprende.** Cuando una revisión dice que una
sección está floja, la entrevista que sigue casi siempre descubre que la
experiencia era real y que nunca la escribiste. Eso entra en el perfil de forma
permanente. Las estimaciones de conversión se corrigen contra los resultados que
registras. Tu vigésima postulación arranca desde un lugar mejor que la primera,
algo que en cualquier otra herramienta simplemente no es cierto.

Lo que sale es un veredicto por canal (envío en frío, referido tibio, contacto
en frío, entrantes desde tu trabajo público), cada uno con un rango de
probabilidad en vez de una palabra de veredicto, y con la calidad de los
materiales puntuada aparte del valor esperado. «1-3% de entrevista» es
información. «MAYBE» no lo es. Materiales excelentes enviados a un puesto que no
encaja siguen teniendo un valor esperado bajo, y esos dos números discrepan de
forma rutinaria.

## Qué cambia

El mismo currículum, la misma publicación, la misma tarde.

### Lo que te dice un optimizador de currículums

> **Puntaje de coincidencia: 91%** ✅
>
> ¡Buenas noticias! Tu currículum encaja fuerte con este puesto.
>
> ✅ 14 de 16 palabras clave requeridas encontradas
> ✅ Formato compatible con ATS detectado
> ⚠️ Considera agregar: "stakeholder alignment", "OKRs"
>
> ¡Ya estás listo para postular!

### Lo que te dice Slushpile

> **Posición en el pool: p55.** El postulante mediano de aquí ya entregó a
> escala comparable en una empresa que el hiring manager reconoce. Tu trabajo
> open source es real y no es raro en este pool: cerca de un tercio de la
> cohorte p75 tiene algo equivalente.
>
> **Envío en frío: REJECT, 1-3%.** El desplegable de años de experiencia del
> formulario corta en 8. Tienes 6 en la función con ese título.
>
> **Referido tibio: MAYBE, 20-30%.** Es el único canal con un camino real.
>
> **Calidad de los materiales: 8/10.** Los materiales no son el problema.
>
> **Contrarian:** SUBMIT_AS_PORTFOLIO_ONLY. Enviar esto en frío gasta una hora
> por una chance del 2%. Dos horas buscando un referido valen más que diez
> postulaciones en frío adicionales.

Uno de los dos es un número sobre tu documento. El otro es una decisión sobre tu
tarde.

## El pipeline

<!-- BEGIN GENERATED pipeline: scripts/sync_docs.py -->

### The main pipeline

Three commands, in order. A search runs on these alone.

```
/slushpile:onboard              once per workspace — builds your profile,
                                preferences, and stories

/slushpile:job-board-search     search a careers board, extract postings,
                                score pool-anchored fit, contrarian gate,
                                create role folders

/slushpile:application-builder  build the resume and cover letter, then
                                iterate them against the review until they
                                stabilize
```

### The three dispatched for you

`/slushpile:application-builder` and `/slushpile:outreach` dispatch these in the
course of a run. Run one directly only to work on materials this pipeline did
not build — a resume written elsewhere, a letter drafted by hand.

```
/slushpile:explore-experience   interview to surface experience you have
                                but never wrote down

/slushpile:adversarial-review   seven agents, five in parallel, verdict
                                per channel

/slushpile:removing-ai-tells    strip AI-authorship signals from prose,
                                with a gatekeeper on every change
```

### Any time

```
/slushpile:outreach             find who they already know at the company,
                                grade the path, and draft the ask

/slushpile:redesign-templates   restyle the resume and letter templates,
                                holding the ATS constraints fixed

/slushpile:status               the queue, what is waiting on you, and whether
                                the pipeline's predictions are holding up

/slushpile:help                 what to run next, and how to read the output
```

<!-- END GENERATED pipeline -->

<!-- BEGIN GENERATED reviewers: scripts/sync_docs.py -->

### The seven reviewers

| Agent | Simulates |
|---|---|
| **Triage screener** | 11 seconds, F-pattern, 347 resumes already read today |
| **Requirements analyst** | 30 seconds, methodical, checks every qualification against evidence |
| **ATS simulator** | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| **Fatigued reader** | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| **Pool analyst** | A recruiter who knows what the queue actually looks like |
| **Hiring manager** | The person who has to justify the interview slot to their skip-level |
| **Contrarian** | Whoever should have asked whether any of this was worth doing |

The first five run in parallel and cannot see each other's work. The hiring
manager sees all five. The contrarian sees everything, including the hiring
manager, and can overrule it.

<!-- END GENERATED reviewers -->

## El manual

El resto vive en [docs/](docs/index.md):

- [Primeros pasos](docs/getting-started.md): qué reunir antes del onboarding, y
  qué instalar.
- [Habilidades](docs/skills.md): cada comando, y cuándo ejecutarlo.
- [El espacio de trabajo](docs/workspace.md): los archivos que esto escribe en
  tu directorio.
- [Tu agente de voz](docs/voice.md), [Resolución de
  problemas](docs/troubleshooting.md).
- [Arquitectura](docs/architecture/index.md): los diagramas, por qué la revisión
  tiene esta forma, y cómo funcionan la puntuación y la calibración.

## Tus cartas de presentación necesitan tu voz

Un octavo agente escribe la carta de presentación. Escribe en el estilo de una
persona específica, construido a partir de un corpus de su propia escritura.

slushpile incluye **`aaddrick-voice`** como ejemplo funcional para que el
pipeline corra de entrada. Es la voz del autor del plugin, no la tuya. Las
cartas escritas con ella van a sonar como un desconocido específico: sirve para
ver el pipeline funcionando, y está mal para cualquier cosa que envíes de
verdad.

Genera la tuya con
**[written-voice-replication](https://github.com/aaddrick/written-voice-replication)**.
Analiza un corpus de tu escritura en 25 dimensiones y produce un agente de voz,
una habilidad de voz y un perfil numérico con objetivos medibles.
`aaddrick-voice` es el ejemplo trabajado de ese mismo pipeline.

Luego apunta `preferences.yaml` a ella:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

Mientras `is_mine` sea false, cada habilidad que redacta prosa te avisa antes de
correr. Esa advertencia es lo único que hay entre tú y doce postulaciones
enviadas con la voz de un desconocido.

## Tus datos siguen siendo tuyos

`/slushpile:onboard` escribe tres archivos en *tu* directorio: `profile.md`,
`preferences.yaml` y `stories.md`. Cada dato personal que usa el pipeline vive
ahí. Nada está fijo dentro del plugin, y el repositorio tiene un gate de CI que
falla si un dato personal se filtra a una habilidad.

Ese espacio de trabajo va a contener tu historial laboral completo, tus cifras
de compensación y tus restricciones. Mantenlo en un repositorio **privado**, o
en ningún repositorio. La habilidad de onboarding te lo va a decir y no va a
inicializar uno por ti.

**El pipeline nunca envía nada.** Ninguna habilidad toca un portal de
postulación, un correo ni un formulario. Escribe archivos. Tú los lees y tú los
envías.

## La honestidad es la función

Esta herramienta te va a decir que un diferenciador del que estás orgulloso es
mediano. Te va a decir que un puesto que quieres tiene una tasa de conversión
del 2%. De vez en cuando te va a decir que no postules.

Ese es el producto. Un pipeline que califica la mayoría de las postulaciones
como INTERVIEW y convierte el 5% no está produciendo señal, está produciendo
optimismo, y va a seguir haciéndolo indefinidamente porque nada dentro de él
contradice nunca. El paso del contrarian, el anclaje al pool y las
probabilidades por canal existen para que la salida sirva justamente cuando dice
que no.

Hay una tabla `Calibration` en el tracker del espacio de trabajo exactamente por
esto: registras qué predijo el pipeline y qué pasó de verdad, y las
probabilidades previas se corrigen con tu propio historial en vez de con la
confianza de nadie.

## Ajústalo

Las 10 habilidades y los 8 agentes son Markdown. Haz un fork, edita, instala tu
copia:

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

```bash
claude plugin marketplace add <your-username>/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Si cambias una habilidad, corre los gates antes de hacer push. Consulta
[CONTRIBUTING.md](../../CONTRIBUTING.md).

## Licencia

MIT. Consulta [LICENSE](../../LICENSE).
