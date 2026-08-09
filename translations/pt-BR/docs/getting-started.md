# Primeiros passos

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/getting-started.md">English</a> ·
  <a href="../../zh-CN/docs/getting-started.md">简体中文</a> ·
  <a href="../../es/docs/getting-started.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../vi/docs/getting-started.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/getting-started.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Tudo o que você precisa antes da primeira execução: o que instalar, o que reunir
e onde rodar.

## Obtendo o plugin

O [INSTALL.md](../INSTALL.md) tem um caminho por harness — Claude Code, Codex,
Gemini CLI, Cursor, e um trecho para colar em qualquer outro. A versão curta
para o Claude Code:

```bash
claude plugin marketplace add aaddrick/slushpile
claude plugin install slushpile@slushpile
```

Depois, no diretório onde você quer que sua busca de emprego fique:

```
/slushpile:onboard
```

**Rode em outro lugar que não o checkout do plugin.** O plugin é código público.
O espaço de trabalho é seu histórico profissional, seus números de remuneração e
suas restrições. Veja [O espaço de trabalho](workspace.md).

## O que o onboarding vai pedir a você

Vale reunir antes de começar, porque dois destes itens demoram mais para você
achar do que a entrevista inteira demora para rodar.

**Um currículo**, em qualquer formato. PDF, `.tex`, `.docx`, Markdown. Troca uns
dez minutos de entrevista por trinta segundos de leitura. Uma exportação de
dados do LinkedIn também serve — `Positions.csv` e `Education.csv` carregam a
maior parte.

**Um corpus de escrita**, para o seu agente de voz. Vários milhares de palavras
da sua própria prosa, sem edição. O onboarding não analisa isso por conta
própria — ele aponta você para o
[written-voice-replication](https://github.com/aaddrick/written-voice-replication),
que é um pipeline separado, rodado uma vez. Reunir o corpus é a parte lenta,
então comece cedo. Veja [Seu agente de voz](voice.md).

Boas fontes: posts de fórum e do Reddit, posts de blog, mensagens longas no
Slack, e-mails para colegas, descrições de pull request, documentação que você
escreveu sozinho. Uma exportação de dados do Reddit ou do Twitter serve direto.

Fontes ruins: qualquer coisa escrita em conjunto, qualquer coisa editada por
outra pessoa, qualquer coisa que já passou por um LLM, qualquer coisa em voz
institucional. Textos de marketing e avaliações de desempenho são os dois
piores.

**Seus números.** Orçamentos, tamanhos de equipe, porcentagens, e o estado
*anterior* de cada um. “Reduzi a latência em 40%” é inutilizável até você saber
40% de quê, e o onboarding vai perguntar.

**Sua situação de remuneração**, se você quiser que a barreira de remuneração
funcione. Para o método recomendado, ela precisa do seu bruto atual, do seu
imposto e do seu custo de moradia. Ela faz a conta; você não precisa chegar com
um número pronto.

## Requisitos

**Obrigatório:** um agente que saiba ler arquivos locais e navegar na web.

**Recomendado:** `pdftotext` (do `poppler-utils`), para que os agentes de
revisão vejam o que um ATS vê, e não o que o seu visualizador de PDF mostra.

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

**Opcional:** uma toolchain LaTeX, se você usar `templates/resume.tex` e
`templates/cover_letter.tex`. Toda habilidade trabalha sobre texto extraído e
nenhuma delas exige LaTeX — só esses dois modelos exigem.

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

Compile com `latexmk -xelatex resume.tex && latexmk -c`. Dois comandos: o
primeiro compila, o segundo limpa. Nenhum dos dois faz as duas coisas.

Os modelos são compostos em Public Sans e IBM Plex Mono. Nenhuma das duas vem
com o TeX Live, então as duas acompanham este repositório e um comando as
instala:

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

Ele copia sete arquivos de fonte para o seu diretório de fontes de usuário e
atualiza o cache. Nada mais o executa, e pular esse passo não é problema: os
dois modelos caem para DejaVu quando uma família está ausente, então uma fonte
faltando muda a aparência dos documentos e nunca se eles compilam ou não.

Para reestilizá-los em algo seu, rode `/slushpile:redesign-templates` em vez de
editar o checkout do plugin, que a próxima atualização substitui.

## Sua primeira hora

```
/slushpile:onboard                    # once, in your workspace directory
/slushpile:job-board-search <company> # search, score, and create role folders
/slushpile:application-builder <path> # build and review one application
```

`onboard` é uma entrevista, não um formulário, e é a única etapa que faz
perguntas que não serão feitas de novo. Tudo depois dela lê o que ela escreveu.

Comece com `job-board-search` em uma empresa que realmente te interessa, e não
na primeira vaga que você encontrar. A etapa de busca é a única que ainda
consegue te convencer a desistir de uma candidatura de graça, e é onde o
pipeline devolve mais por minuto gasto.

[Habilidades](skills.md) é a referência completa dos comandos.
