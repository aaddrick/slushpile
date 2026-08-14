# Instalación

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../INSTALL.md">English</a> ·
  <a href="../zh-CN/INSTALL.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../pt-BR/INSTALL.md">Português (BR)</a> ·
  <a href="../vi/INSTALL.md">Tiếng Việt</a> ·
  <a href="../en-x-aibro/INSTALL.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

slushpile son 9 habilidades y 8 definiciones de agente, todo en Markdown. Cada
ruta de abajo deja los mismos archivos en algún lugar donde tu agente los va a
leer.

**Una cosa que decidir antes de instalar nada:** dónde va tu espacio de trabajo.

El plugin es código. Tu espacio de trabajo es tu historial laboral, tu salario y
tus restricciones. Son cosas distintas y van en directorios distintos. Instala
el plugin donde tu agente guarde sus plugins; ejecuta `/slushpile:onboard` en un
directorio aparte que mantengas privado.

---

## Claude Code

El pipeline completo. Las habilidades quedan como slash commands, los 8 agentes
se despachan como subagentes, y los 5 revisores en paralelo corren de verdad al
mismo tiempo.

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Verifica:

```bash
claude plugin list
```

Deberías ver `slushpile@slushpile` y `enabled`.

Después arranca:

```
/slushpile:onboard
```

Ejecútalo en el directorio donde quieres que viva tu búsqueda de trabajo.

### Actualizar

```bash
claude plugin marketplace update slushpile
```

```bash
claude plugin install slushpile@slushpile
```

### Desinstalar

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

Ninguno de los dos comandos toca los archivos de tu espacio de trabajo.

---

## Codex

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Dentro de Codex, `/plugins` abre el explorador de plugins.

Codex antepone el nombre del plugin a las habilidades:

```
$slushpile:onboard
```

**Qué cambia.** Codex no despacha subagentes. El pipeline de revisión corre sus
7 revisores de forma secuencial en un solo contexto: lee cada definición de
agente del directorio `agents/` del plugin, la adopta, escribe el informe y pasa
a la siguiente.

La salida tiene la misma forma. Dos cosas se degradan, y vale la pena saber
cuáles:

1. Es más lento. 7 pasadas secuenciales en lugar de 5 revisores en paralelo más
   dos.
2. Los 5 revisores en paralelo deberían ser ciegos entre sí. En un solo contexto
   no lo son, y un especialista que ya vio el veredicto del triaje va a derivar
   hacia darle la razón. Escribe cada informe completo antes de empezar el
   siguiente, que es lo que indica la habilidad.

---

## Gemini CLI

```bash
gemini extensions install https://github.com/VonTerraProject501c3/slushpile
```

La extensión declara `GEMINI.md` como su archivo de contexto, que importa cada
habilidad y cada definición de agente.

Después, en el directorio de tu espacio de trabajo:

```
Set up a slushpile workspace here.
```

Gemini tampoco despacha subagentes, así que aplica la misma advertencia sobre lo
secuencial.

### Manual

Clona dentro del directorio de extensiones:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.gemini/extensions/slushpile
```

---

## Cursor

Cursor lee `.cursor/skills/` y `.cursor/rules/` del espacio de trabajo que tenga
abierto. Clona el repositorio y cópialos a tu espacio de trabajo:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile /tmp/slushpile
```

```bash
cp -r /tmp/slushpile/.cursor/skills/slushpile <your-workspace>/.cursor/skills/
```

```bash
cp -r /tmp/slushpile/skills /tmp/slushpile/agents /tmp/slushpile/templates <your-workspace>/.slushpile/
```

La habilidad de Cursor es un enrutador: apunta a los archivos reales de las
habilidades bajo `.slushpile/`. Así queda una sola copia del pipeline en vez de
cuatro.

Después escribe `/slushpile` en Cursor y di qué quieres hacer.

---

## Cualquier otro entorno

El pipeline es Markdown plano con frontmatter YAML. Cualquier agente que sepa
leer archivos puede ejecutarlo.

Clona el repositorio en algún lugar al que tu agente llegue:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.slushpile
```

Después pon esto en tu `AGENTS.md`, en tu system prompt, o en lo que sea que tu
entorno use para instrucciones permanentes:

<!-- BEGIN GENERATED harness-snippet: scripts/sync_docs.py -->

```markdown
## slushpile

A job application pipeline lives at `~/.slushpile`. When the user asks to set up
a job search, search a careers board, build an application, or review one, read
the matching skill and follow it:

- `~/.slushpile/skills/onboard/SKILL.md` — set up the workspace, once
- `~/.slushpile/skills/job-board-search/SKILL.md` — search and score roles
- `~/.slushpile/skills/explore-experience/SKILL.md` — interview for undocumented experience
- `~/.slushpile/skills/application-builder/SKILL.md` — build the resume and cover letter
- `~/.slushpile/skills/adversarial-review/SKILL.md` — run the seven-agent review
- `~/.slushpile/skills/removing-ai-tells/SKILL.md` — strip AI-authorship signals from prose
- `~/.slushpile/skills/redesign-templates/SKILL.md` — restyle the document templates
- `~/.slushpile/skills/status/SKILL.md` — report the queue and check pipeline calibration
- `~/.slushpile/skills/help/SKILL.md` — what to run next, and how to read the output

The review dispatches personas defined in `~/.slushpile/agents/`. If you cannot
dispatch subagents, adopt each definition in turn and run them sequentially,
writing each report out before starting the next.

Cover letters are written by the voice agent named in `preferences.yaml` under
`voice.agent`. A working example ships as `aaddrick-voice`; it is the plugin
author's voice, and users generate their own with
https://github.com/aaddrick/written-voice-replication

Workspace templates are in `~/.slushpile/templates/`.
```

<!-- END GENERATED harness-snippet -->

---

## El resto del manual

Todo lo que viene después de instalar vive en [docs/](docs/index.md):

- [Primeros pasos](docs/getting-started.md): qué reunir antes del onboarding y
  qué necesita tener instalado el pipeline: `pdftotext` y, opcionalmente, un
  toolchain de LaTeX y las tipografías de documento que vienen incluidas.
- [Habilidades](docs/skills.md): cada comando `/slushpile:*` y cuándo ejecutarlo.
- [El espacio de trabajo](docs/workspace.md): los archivos que el onboarding
  escribe en tu directorio, y qué lee cada uno.
- [Tu agente de voz](docs/voice.md): por qué las cartas de presentación
  necesitan uno y cómo generar el tuyo.
- [Solución de problemas](docs/troubleshooting.md).
- [Arquitectura](docs/architecture/index.md): por qué el pipeline tiene la forma
  que tiene.
