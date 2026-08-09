# Arquitectura de Slushpile

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/index.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/index.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../../pt-BR/docs/architecture/index.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/index.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile no es un programa. Es un conjunto de archivos Markdown que un agente de
codificación lee y sobre los que actúa: 9 habilidades que orquestan, 8
definiciones de agente que hacen una sola cosa cada una, y un puñado de
plantillas. No hay motor, no hay runtime y no hay estado fuera del directorio de
trabajo del propio usuario.

Eso condiciona cada decisión documentada aquí. Una regla que este pipeline quiera
hacer cumplir tiene que sobrevivir a que un modelo bajo carga la parafrasee,
porque no hay intérprete que la imponga. Un dato que el pipeline necesita tiene
que vivir en un archivo que el modelo vaya a leer de verdad, porque no hay base
de datos que consultar.

| Archivo | Contenido |
| --- | --- |
| [pipeline.md](pipeline.md) | Los cinco diagramas, la leyenda y qué hace cada etapa. |
| [the-review.md](the-review.md) | Por qué la revisión tiene la forma que tiene: la etapa ciega, el orden de despacho, el guardián y el tope de tres rondas. |
| [scoring.md](scoring.md) | Anclaje al pool, veredictos condicionados por canal, niveles y criterios de descarte. |
| [memory-and-calibration.md](memory-and-calibration.md) | El espacio de trabajo como memoria duradera, las rutas de reescritura y cómo los resultados corrigen las predicciones. |
| [agents-and-models.md](agents-and-models.md) | La frontera entre habilidad y agente, el nivel de modelo por persona y los agentes de voz. |
| [personal-data.md](personal-data.md) | Por qué ningún dato personal puede vivir en el plugin, y la barrera que lo hace cumplir. |
| [generated-surfaces.md](../../../../docs/architecture/generated-surfaces.md) | Por qué seis superficies describen este pipeline y ninguna es dueña de un dato. |
| [AGENTS.md](../../../../docs/architecture/AGENTS.md) | Gemelo idéntico byte a byte del `CLAUDE.md` de este directorio, que restringe las ediciones a estas convenciones. |
