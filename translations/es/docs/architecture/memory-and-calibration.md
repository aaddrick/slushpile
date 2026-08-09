# Memoria y calibración

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/memory-and-calibration.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/memory-and-calibration.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/memory-and-calibration.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/memory-and-calibration.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/memory-and-calibration.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Una búsqueda de trabajo son cuarenta postulaciones en tres meses. Una
herramienta sin memoria te cobra el precio completo por cada una: pegas un
currículum, recibes un número, cierras la pestaña, y la herramienta termina la
sesión sabiendo exactamente lo que sabía al empezar.

La memoria de Slushpile es un directorio de archivos que son tuyos. No hay base
de datos, no hay cuenta y no hay estado dentro del plugin: el plugin es código
público y el espacio de trabajo es tu historial laboral, así que son cosas
distintas guardadas en lugares distintos. Ve
[personal-data.md](personal-data.md).

## Qué es duradero

| Archivo | Escrito por | Leído por |
| --- | --- | --- |
| `profile.md` | `onboard`, extendido por `explore-experience` y `application-builder` | cada etapa que escribe prosa |
| `preferences.yaml` | `onboard`, corregido por `status` | la puntuación, los criterios de descarte, el despacho de la revisión |
| `stories.md` | `onboard` | el constructor, cuando elige la única historia que va a contar |
| `job_search.md` | `job-board-search`, `application-builder`, `status` | el analista del pool de postulantes, el contrarian, la fila |
| `companies.md` | `job-board-search` | búsquedas posteriores en la misma empresa |
| `applications/<company>/<role>/` | `job-board-search`, y después el constructor | la revisión, y `status` |

`profile.md` no es un currículum. Es el material del que se recorta un
currículum, varias veces más largo que cualquier cosa que alguien enviaría, y su
valor está en que nada vuelve a hacerte esas preguntas dos veces.

## Las rutas de reescritura

Son tres, y cada una existe porque algo aprendido en una etapa es inútil si se
queda ahí.

**Hallazgo de la revisión → perfil.** Cuando una revisión dice que una sección
está delgada, la entrevista que sigue casi siempre descubre que la experiencia
era real y que nunca la habías escrito. `explore-experience` la saca a la
superficie y entra permanentemente en `profile.md`, donde cada postulación
posterior puede apoyarse en ella. Esta es la ruta que hace que la vigésima
postulación arranque desde un mejor lugar que la primera.

**Resultado → tracker.** Tú registras lo que pasó: sin respuesta, filtro
telefónico, entrevista, oferta, rechazo, y en qué etapa. Nada más en el pipeline
puede producir esto, porque el pipeline nunca envía nada y nunca ve una
respuesta.

**Tracker → priors.** `status` regresa las propias predicciones del pipeline
contra esos resultados y escribe la corrección en `preferences.yaml`.

## Por qué la corrección va a los datos del usuario

El lugar obvio para registrar "este pipeline es 12 puntos optimista sobre los
envíos en frío a laboratorios de frontera" es el agente que hizo la estimación.
Ese es el lugar equivocado, y de forma silenciosa: las definiciones de agente se
distribuyen con el plugin, así que una edición ahí queda revertida por la
siguiente actualización sin aviso, dejando un pipeline que *estaba* afinado y ya
no lo está.

Así que la corrección va a `preferences.yaml`, que es tuyo y que ninguna
actualización toca. `job-board-search` lee `calibration_priors` al momento de
puntuar, y `adversarial-review` le pasa el bloque al analista del pool y al
contrarian en el despacho.

## Las reglas que mantienen honesta la calibración

**Cinco postulaciones resueltas es el piso.** Por debajo de eso, `status`
imprime los conteos y dice que la muestra es demasiado pequeña para regresar, en
lugar de producir una tabla. Una tasa calculada a partir de dos resultados es
ruido disfrazado de calibración, y una vez que está en una tabla nadie se
acuerda del denominador.

**El silencio cuenta como rechazo.** Una postulación enviada hace más de 30 días
sin respuesta se registra como `no_response`, no se deja pendiente. Excluirlas
es la mayor fuente de optimismo disponible para una tabla así. El conteo
inferido de esa manera se reporta.

**Se califica contra el canal realmente usado.** Los veredictos se agrupan por
el veredicto del canal por el que la postulación efectivamente salió, nunca por
el del mejor caso. Calificar un envío en frío contra su veredicto de referido
tibio es como un pipeline se convence de que tenía razón.

**Se reportan las dos direcciones del error.** Un veredicto de ENTREVISTA que
recibió un rechazo automático en menos de 72 horas significa que la revisión se
perdió algo que un filtro atrapó en segundos. Un DESCARTE que convirtió
significa que la revisión fue demasiado dura, y cada puesto del que te disuadió
desde entonces es un costo que no aparece en ningún otro lado. Solo una de esas
dos es cómoda de reportar, y por eso la regla nombra las dos.

**El hallazgo nombra un segmento, una dirección y un tamaño.** "El pipeline está
mal calibrado" es inaccionable y ningún agente puede consumirlo. "Los veredictos
de ENTREVISTA en envíos en frío a laboratorios de frontera convirtieron 0 de 7,
contra un 12% estimado" se puede escribir en un prior y se puede accionar.

**Un prior nulo es una respuesta válida.** Solo se escriben las tasas
respaldadas por cinco o más postulaciones resueltas en ese canal. Todo lo demás
queda nulo, los agentes usan los valores por defecto con los que se distribuyen,
y etiquetan la estimación como no calibrada. Un prior calculado a partir de dos
resultados aleja la puntuación de la realidad más de lo que la aleja no tener
prior, y llega vestido con la autoridad de un número empírico.

**Se muestra el diff antes de escribir `preferences.yaml`.** Es tu archivo de
restricciones y el cambio altera cómo se puntúa cada evaluación futura. Un
cambio de puntuación del que nadie te avisó es indistinguible de que el pipeline
esté derivando por su cuenta.
