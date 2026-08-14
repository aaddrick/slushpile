# Instalação

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../INSTALL.md">English</a> ·
  <a href="../zh-CN/INSTALL.md">简体中文</a> ·
  <a href="../es/INSTALL.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../vi/INSTALL.md">Tiếng Việt</a> ·
  <a href="../en-x-aibro/INSTALL.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

O slushpile é 10 habilidades e 8 definições de agente, tudo em Markdown. Todo
caminho abaixo coloca os mesmos arquivos em algum lugar onde seu agente vá lê-los.

**Uma coisa para decidir antes de instalar qualquer coisa:** onde fica o seu
espaço de trabalho.

O plugin é código. Seu espaço de trabalho é seu histórico profissional, seu
salário e suas restrições. São coisas diferentes e pertencem a diretórios
diferentes. Instale o plugin onde quer que seu agente guarde plugins; rode
`/slushpile:onboard` em um diretório separado que você mantenha privado.

---

## Claude Code

O pipeline completo. As habilidades viram comandos de barra, os 8 agentes são
despachados como subagentes, e os 5 revisores em paralelo de fato rodam ao mesmo
tempo.

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Verifique:

```bash
claude plugin list
```

Você deve ver `slushpile@slushpile` e `enabled`.

Então comece:

```
/slushpile:onboard
```

Rode-o no diretório onde você quer que sua busca de emprego fique.

### Atualizando

```bash
claude plugin marketplace update slushpile
```

```bash
claude plugin install slushpile@slushpile
```

### Desinstalando

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

Nenhum dos dois comandos toca nos arquivos do seu espaço de trabalho.

---

## Codex

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Dentro do Codex, `/plugins` abre o navegador de plugins.

O Codex prefixa as habilidades do plugin com o nome do plugin:

```
$slushpile:onboard
```

**O que muda.** O Codex não tem despacho de subagentes. O pipeline de revisão
roda seus 7 revisores em sequência, em um único contexto: leia cada definição de
agente no diretório `agents/` do plugin, assuma essa persona, escreva o
relatório, e então passe para a próxima.

A saída tem o mesmo formato. Duas coisas pioram, e vale saber quais:

1. É mais lento. Sete passagens sequenciais em vez de 5 revisores em paralelo
   mais dois.
2. Os 5 revisores em paralelo deveriam ser cegos entre si. Em um único contexto
   eles não são, e um especialista que já viu o veredito da triagem vai derivar
   para concordar com ele. Escreva cada relatório por completo antes de começar
   o próximo, que é o que a habilidade manda.

---

## Gemini CLI

```bash
gemini extensions install https://github.com/VonTerraProject501c3/slushpile
```

A extensão nomeia `GEMINI.md` como seu arquivo de contexto, que importa toda
habilidade e toda definição de agente.

Depois, no diretório do seu espaço de trabalho:

```
Set up a slushpile workspace here.
```

O Gemini também não tem despacho de subagentes, então vale a mesma ressalva
sobre execução sequencial.

### Manual

Clone no diretório de extensões:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.gemini/extensions/slushpile
```

---

## Cursor

O Cursor lê `.cursor/skills/` e `.cursor/rules/` do espaço de trabalho que
estiver aberto. Três coisas entram: o roteador de habilidades, o arquivo de
regras e o próprio pipeline. Aponte `WORKSPACE` para o diretório que o Cursor
tem aberto e rode o bloco como uma unidade só:

```bash
WORKSPACE="/path/to/your/workspace"
rm -rf /tmp/slushpile
git clone https://github.com/VonTerraProject501c3/slushpile /tmp/slushpile
mkdir -p "$WORKSPACE/.cursor/skills" "$WORKSPACE/.cursor/rules" "$WORKSPACE/.slushpile"
cp -r /tmp/slushpile/.cursor/skills/slushpile "$WORKSPACE/.cursor/skills/"
cp /tmp/slushpile/.cursor/rules/slushpile.mdc "$WORKSPACE/.cursor/rules/"
cp -r /tmp/slushpile/skills /tmp/slushpile/agents /tmp/slushpile/templates "$WORKSPACE/.slushpile/"
```

Confira se as três chegaram:

```bash
ls "$WORKSPACE/.cursor/skills/slushpile/SKILL.md" "$WORKSPACE/.cursor/rules/slushpile.mdc" "$WORKSPACE/.slushpile/skills"
```

O arquivo de regras é o que vale conferir. Ele carrega as duas regras
permanentes — ler `preferences.yaml` antes de afirmar qualquer coisa sobre o
usuário, e nunca enviar nada — e o Cursor é o único harness onde ele chega
copiado à mão em vez de junto com o plugin. Um espaço de trabalho sem ele é
idêntico a um que funciona.

`rm -rf /tmp/slushpile` está ali para o bloco poder ser repetido; `git clone`
recusa um destino que já existe.

A habilidade do Cursor é um roteador: ela aponta para os arquivos de habilidade
reais em `.slushpile/`. Isso mantém uma cópia do pipeline em vez de quatro.

Então digite `/slushpile` no Cursor e diga o que você quer fazer.

---

## Qualquer outro harness

O pipeline é Markdown puro com frontmatter YAML. Qualquer agente que saiba ler
arquivos consegue rodá-lo.

Clone o repositório em algum lugar que seu agente alcance:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.slushpile
```

Depois coloque isto no seu `AGENTS.md`, no seu prompt de sistema, ou no que quer
que seu harness use como instruções permanentes:

<!-- BEGIN GENERATED harness-snippet: scripts/sync_docs.py -->

```markdown
## slushpile

A job application pipeline lives at `~/.slushpile`. When the user asks to set up
a job search, search a careers board, build an application, or review one, read
the matching skill and follow it:

- `~/.slushpile/skills/onboard/SKILL.md` — set up the workspace, once
- `~/.slushpile/skills/job-board-search/SKILL.md` — search and score roles
- `~/.slushpile/skills/outreach/SKILL.md` — find a referrer and draft the ask
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

## O resto do manual

Tudo o que vem depois da instalação vive em [docs/](docs/index.md):

- [Primeiros passos](docs/getting-started.md): o que reunir antes do onboarding,
  e o que o pipeline precisa ter instalado — `pdftotext` e, opcionalmente, uma
  toolchain LaTeX e as fontes de documento que acompanham o repositório.
- [Habilidades](docs/skills.md): todo comando `/slushpile:*` e quando rodar cada um.
- [O espaço de trabalho](docs/workspace.md): os arquivos que o onboarding
  escreve no seu diretório, e o que lê cada um deles.
- [Seu agente de voz](docs/voice.md): por que cartas de apresentação precisam de
  um e como gerar o seu.
- [Solução de problemas](docs/troubleshooting.md).
- [Arquitetura](docs/architecture/index.md): por que o pipeline tem o formato
  que tem.
