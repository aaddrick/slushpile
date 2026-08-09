# Tu agente de voz

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/voice.md">English</a> ·
  <a href="../../zh-CN/docs/voice.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../pt-BR/docs/voice.md">Português (BR)</a> ·
  <a href="../../vi/docs/voice.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

Un octavo agente escribe la carta de presentación, y escribe en el estilo de una
persona específica, construido a partir de un corpus de la escritura de esa
misma persona.

Esa es la única parte de este pipeline que tienes que traer tú.

## Por qué un agente aparte

La carta de presentación es el único documento de una postulación que se supone
que debe sonar como una persona. Un modelo que escribe «con tu voz» a partir de
un currículum produce el registro por defecto del modelo con tus datos adentro:
competente, uniforme y reconocible como tal para el lector número sesenta y uno
del día.

Por eso la voz no es una instrucción del prompt. Es una definición de agente
generada a partir de varios miles de palabras de tu prosa real, medida sobre un
conjunto de dimensiones estilísticas, con objetivos numéricos contra los que una
pasada posterior puede verificar.

## Cómo generar el tuyo

[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
es un pipeline aparte que ejecutas una sola vez. Analiza un corpus de tu
escritura en 25 dimensiones y produce un agente de voz, una habilidad de voz y
un perfil numérico con objetivos medibles.

Reunir el corpus es la parte lenta, así que empieza antes de necesitarlo.

**Buenas fuentes:** publicaciones en foros y en Reddit, entradas de blog,
mensajes largos de Slack, correos a colegas, descripciones de pull requests,
documentación que escribiste tú solo. Una exportación de datos de Reddit o de
Twitter sirve directamente.

**Malas fuentes:** cualquier cosa escrita entre varios, cualquier cosa editada
por otra persona, cualquier cosa que ya pasó por un LLM, cualquier cosa en voz
institucional. Los textos de marketing y las evaluaciones de desempeño son las
dos peores: ambas están escritas en un registro que nadie usa por voluntad
propia.

Unos pocos miles de palabras son el piso. Por debajo de eso el resultado se lee
genérico, que es el modo de falla más difícil de notar porque parece terminado.

## Cómo apuntar slushpile hacia él

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`voice.agent` nombra al agente por su nombre y nada lo deja fijo en el código,
que es lo que te permite poner el tuyo sin editar el plugin.

## Mientras tanto

`aaddrick-voice` viene incluido como ejemplo funcional para que el pipeline
corra apenas se instala. Es la voz del autor del plugin, no la tuya. Las cartas
escritas con él van a sonar como un desconocido concreto: sirve para ver el
pipeline funcionando, no sirve para nada que envíes de verdad.

Mientras `is_mine` sea falso, cada habilidad que redacta prosa te avisa antes de
ejecutarse. Esa advertencia es lo único que se interpone entre tú y doce
postulaciones enviadas con la voz de un desconocido, así que no la silencies
poniendo la bandera en verdadero antes de que el agente sea de verdad tuyo.

## Cómo se usa la voz, y cómo se la defiende

`/slushpile:removing-ai-tells` pasa la carta por instancias nuevas del agente de
voz, con la habilidad orquestadora actuando como guardián sobre cada cambio
individual. Una pasada que aceptara todas las sugerencias lijaría la carta de
vuelta hacia el promedio, que es justo lo que el agente de voz existe para
evitar.

El lector fatigado de la revisión se contrasta con tu agente de voz por la misma
razón. Un hábito distintivo documentado ahí no es un defecto por el hecho de que
un revisor lo haya marcado, y quitarlo es exactamente la forma en que una carta
se desliza de vuelta hacia lo genérico.

Ten en cuenta que un agente de voz es, por construcción, la identidad de una
persona: generado a partir de su escritura, nombrado con su nombre, y sus
ejemplos son sus oraciones reales. Por eso es el único agente de este
repositorio exento de las reglas de datos personales que atan a todo lo demás, y
por eso la excepción se detiene en los datos de contacto. Consulta
[Agentes y modelos](architecture/agents-and-models.md).
