# Agentes y modelos

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/agents-and-models.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/agents-and-models.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/agents-and-models.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/agents-and-models.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/agents-and-models.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## Una habilidad orquesta. Un agente tiene un solo trabajo.

Son dos tipos distintos de archivo y la frontera entre ellos sostiene la
estructura.

Una habilidad sabe del pipeline: en qué etapa está, qué corrió antes, a quién le
entrega. Un agente sabe solamente su propio trabajo. **Un agente que sabe en qué
etapa está va a optimizar para la etapa en lugar de hacer su trabajo**: a un
filtro de triaje al que se le dice que es el primero de cinco empieza a matizar,
porque se da cuenta de que alguien más va a revisar su trabajo.

El corolario es la regla que mantiene comparable la salida de la revisión:

**Las restricciones vinculantes viven en la definición del agente, no en el
prompt que lo despacha.** Un orquestador que improvisa restricciones extra en
cada corrida produce hallazgos que no se pueden comparar entre postulaciones, lo
que destruye los datos de calibración de los que depende todo el sistema. Por
esta razón los límites de alcance del contrarian están en
`agents/slushpile-contrarian.md`, y a la habilidad de revisión se le dice
explícitamente que no los reformule ni los amplíe.

Los datos son la excepción, y la distinción vale la pena enunciarla con
precisión. `calibration_priors` va en el prompt de despacho porque cambia *lo
que el agente sabe*. Los límites de alcance se quedan en la definición porque
cambian *lo que el agente tiene permitido decir*. Lo primero varía por corrida a
propósito; lo segundo no debe variar.

## Cada agente declara un modelo

<!-- BEGIN GENERATED agent-table: scripts/sync_docs.py -->

| # | Agent | Model | Simulates |
|---|---|---|---|
| 1 | `slushpile-triage-screener` | sonnet | 11 seconds, F-pattern, 347 resumes already read today |
| 2 | `slushpile-requirements-analyst` | sonnet | 30 seconds, methodical, checks every qualification against evidence |
| 3 | `slushpile-ats-simulator` | sonnet | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| 4 | `slushpile-fatigued-reader` | sonnet | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| 5 | `slushpile-pool-analyst` | opus | A recruiter who knows what the queue actually looks like |
| 6 | `slushpile-hiring-manager` | opus | The person who has to justify the interview slot to their skip-level |
| 7 | `slushpile-contrarian` | opus | Whoever should have asked whether any of this was worth doing |

Plus the voice agent, `aaddrick-voice`, which the review never dispatches and
which is named in `preferences.yaml` rather than here. The first five run in
parallel and are blind to each other; the last two run in order.

<!-- END GENERATED agent-table -->

El modelo está en el frontmatter de cada agente, y la tabla de despacho en
`skills/adversarial-review/SKILL.md` también nombra uno por agente. Los dos se
contrastan entre sí con `tests/test_structure.py`: el frontmatter es sobre lo
que un harness despacha de verdad, y la columna de la tabla es su documentación.

Un agente sin modelo declarado toma el que esté corriendo la sesión. Eso aplana
en silencio una revisión que mezcla niveles a propósito, y por eso el campo es
obligatorio y no opcional.

La división no es arbitraria. Cada una de las personas baratas simula una
lectura **acotada y mecánica**: once segundos de vistazo, una lista de
verificación de calificaciones, un analizador sintáctico, la irritación de un
lector cansado. Esas son tareas bien especificadas donde un modelo más grande
sobre todo agrega costo.

Cada una de las caras requiere **estimar algo que no está en el documento**. El
analista del pool de postulantes tiene que caracterizar a candidatos que no
tiene enfrente. El hiring manager tiene que pesar cinco informes entre
sí y producir probabilidades. El contrarian tiene que construir el argumento más
fuerte de que todo lo anterior está mal. Esas se degradan de manera visible en
un modelo más chico, y son las tres cuya salida tú realmente accionas.

## Espacios de nombres

Cada agente del pipeline lleva el prefijo `slushpile-` para que no pueda chocar
con un agente que tú ya tengas. Un usuario con su propio `contrarian` se lo
queda; el de este pipeline es `slushpile-contrarian` y los dos nunca se cruzan.

## Los agentes de voz son la excepción deliberada

El agente de voz es el único agente de este repositorio que no se llama
`slushpile-*`, y el único cuyo nombre es el de una persona.

Eso es porque se genera por persona con
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
y lleva el nombre de su autor. Alguien que ponga el suyo propio tiene que poder
conservar ese nombre, así que el nombre se lee de `preferences.yaml` en tiempo
de ejecución en lugar de estar fijo en algún lado:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`agents/aaddrick-voice.md` se distribuye como el ejemplo público y trabajado de
ese pipeline, para que slushpile corra de entrada antes de que hayas generado el
tuyo. Es la voz del autor del plugin, no la tuya, y mientras `is_mine` sea
falso, cada habilidad que redacta prosa avisa antes de correr. Ese aviso es lo
único que hay entre tú y doce postulaciones enviadas con la voz de un
desconocido.

Está exento de los patrones de identidad en `scripts/check_no_pii.py`, pero
nunca del patrón de datos de contacto. Ve
[personal-data.md](personal-data.md).

**No agregues un segundo agente de voz a este repositorio.** Un ejemplo es una
demostración; dos son una biblioteca de voces ajenas que nadie pidió.
