# Documentación de Slushpile

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/index.md">English</a> ·
  <a href="../../zh-CN/docs/index.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../pt-BR/docs/index.md">Português (BR)</a> ·
  <a href="../../vi/docs/index.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

La puerta de entrada es el [README](../README.md) del repositorio. Todo lo que
va más allá de la instalación y del argumento vive acá, agrupado por lo que
estás tratando de hacer.

## Empieza acá

- [Primeros pasos](getting-started.md): qué reunir antes del onboarding y qué
  necesita tener instalado el pipeline.
- [Habilidades](skills.md): cada comando `/slushpile:*`, qué hace y cuándo
  ejecutarlo.
- [El espacio de trabajo](workspace.md): los archivos que el onboarding escribe
  en tu directorio, para qué sirve cada uno y quién los lee.

## Referencia

- [Tu agente de voz](voice.md): por qué las cartas de presentación necesitan
  uno, cómo generar el tuyo y qué pasa hasta que lo hagas.
- [Solución de problemas](troubleshooting.md).

## Arquitectura

- [Arquitectura](architecture/index.md): los diagramas del pipeline, por qué la
  revisión tiene la forma que tiene, cómo funcionan el puntaje y la calibración,
  y las reglas sobre datos personales.
- [Guía de diagramas](../../../docs/diagrams/AGENTS.md): cómo editar y volver a
  renderizar los diagramas `.d2` que incrustan las páginas de arquitectura.

## Contribuir

Los estándares del repositorio, las cuatro compuertas y las reglas para editar
una habilidad están en [CLAUDE.md](../../../CLAUDE.md) y
[CONTRIBUTING.md](../../../CONTRIBUTING.md). Lee
[Superficies generadas](../../../docs/architecture/generated-surfaces.md) antes
de editar cualquier cosa que liste las habilidades: varias de esas listas son
generadas, y editar la copia en vez de la fuente es el cambio que desaparece de
manera más confiable.
