# Primeros pasos

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/getting-started.md">English</a> ·
  <a href="../../zh-CN/docs/getting-started.md">简体中文</a> ·
  <strong>Español</strong> ·
  <a href="../../pt-BR/docs/getting-started.md">Português (BR)</a> ·
  <a href="../../vi/docs/getting-started.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/getting-started.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Todo lo que necesitas antes de tu primera corrida: qué instalar, qué reunir y
dónde ejecutarlo.

## Conseguir el plugin

[INSTALL.md](../INSTALL.md) tiene una ruta por entorno: Claude Code, Codex,
Gemini CLI, Cursor y un fragmento para pegar en cualquier otro. La versión corta
para Claude Code:

```bash
claude plugin marketplace add aaddrick/slushpile
claude plugin install slushpile@slushpile
```

Después, en el directorio donde quieres que viva tu búsqueda de trabajo:

```
/slushpile:onboard
```

**Ejecútalo en un lugar distinto del checkout del plugin.** El plugin es código
público. El espacio de trabajo es tu historial laboral, tus cifras de
compensación y tus restricciones. Mira [El espacio de trabajo](workspace.md).

## Qué te va a pedir el onboarding

Vale la pena reunir esto antes de empezar, porque dos de estas cosas te toman
más tiempo de encontrar que lo que tarda la entrevista en correr.

**Un currículum**, en cualquier formato. PDF, `.tex`, `.docx`, Markdown.
Reemplaza unos diez minutos de entrevista por treinta segundos de lectura. Una
exportación de datos de LinkedIn también sirve: `Positions.csv` y
`Education.csv` traen casi todo.

**Un corpus de escritura**, para tu agente de voz. Varios miles de palabras de
tu propia prosa sin editar. El onboarding no lo analiza él mismo: te apunta a
[written-voice-replication](https://github.com/aaddrick/written-voice-replication),
que es un pipeline aparte que corres una sola vez. Reunir el corpus es la parte
lenta, así que empieza temprano. Mira [Tu agente de voz](voice.md).

Buenas fuentes: publicaciones en foros y en Reddit, entradas de blog, mensajes
largos de Slack, correos a colegas, descripciones de pull requests,
documentación que escribiste solo. Una exportación de datos de Reddit o de
Twitter sirve directamente.

Malas fuentes: cualquier cosa escrita entre varias personas, cualquier cosa que
editó alguien más, cualquier cosa que ya pasó por un LLM, cualquier cosa en voz
institucional. El material de marketing y las evaluaciones de desempeño son las
dos peores.

**Tus números.** Presupuestos, tamaños de equipo, porcentajes y el estado
*anterior* de cada uno. "Bajé la latencia 40%" es inservible hasta que se sepa
40% de qué, y el onboarding te lo va a preguntar.

**Tu situación de compensación**, si quieres que la compuerta de compensación
funcione. Para el método recomendado necesita tu bruto actual, tus impuestos y
tu costo de vivienda. Ella hace la aritmética; no tienes que llegar con un
número.

## Requisitos

**Obligatorio:** un agente que pueda leer archivos locales y navegar la web.

**Recomendado:** `pdftotext` (de `poppler-utils`), para que los agentes de
revisión vean lo que ve un ATS y no lo que muestra tu visor de PDF.

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

**Opcional:** un toolchain de LaTeX, si usas `templates/resume.tex` y
`templates/cover_letter.tex`. Todas las habilidades trabajan sobre texto
extraído y ninguna necesita LaTeX; solo esas dos plantillas.

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

Compila con `latexmk -xelatex resume.tex && latexmk -c`. Dos comandos: el
primero compila, el segundo limpia. Ninguno hace las dos cosas.

Las plantillas están compuestas en Public Sans e IBM Plex Mono. Ninguna de las
dos viene con TeX Live, así que ambas están incluidas en este repositorio y un
solo comando las instala:

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

Copia siete archivos de fuente en tu directorio de fuentes de usuario y refresca
el caché. Nada más lo ejecuta, y saltárselo está bien: ambas plantillas caen de
vuelta a DejaVu cuando falta una familia, así que una fuente ausente cambia cómo
se ven los documentos y nunca si compilan.

Para rediseñarlas a algo tuyo, ejecuta `/slushpile:redesign-templates` en vez de
editar el checkout del plugin, que la próxima actualización reemplaza.

## Tu primera hora

```
/slushpile:onboard                          # once, in your workspace directory
/slushpile:job-board-search <company|query> # search, score, and create role folders
/slushpile:application-builder <path>       # build and review one application
```

`onboard` es una entrevista, no un formulario, y es la única etapa que te hace
preguntas que no te van a volver a hacer. Todo lo que viene después lee lo que
esa etapa escribió.

Empieza con `job-board-search` en una empresa que te interese de verdad, no en
el primer puesto que encuentres. La etapa de búsqueda es la única que todavía
puede convencerte de no postular sin costo alguno, y es donde el pipeline
devuelve más por minuto invertido.

Si no tienes una empresa en mente, describe en su lugar lo que estás buscando y
el mismo comando lo resuelve en una lista: `applied AI roles within 50 miles of
Martinsville, VA that fit my profile` sirve como argumento. Te muestra las
empresas que eligió antes de buscar en ninguna de ellas, así que una lista
construida sobre una lectura equivocada de tu consulta te cuesta una corrección
y no una hora.

[Habilidades](skills.md) es la referencia completa de comandos.
