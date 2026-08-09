# Habilidades

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/skills.md">English</a> ·
  <a href="../../zh-CN/docs/skills.md">简体中文</a> ·
  <a href="../../es/docs/skills.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../vi/docs/skills.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/skills.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

O slushpile se instala como 9 habilidades. O Claude Code expõe cada uma como
`/slushpile:<name>`; o Codex usa `$slushpile:<name>`; o Gemini CLI e outros
harnesses leem os mesmos arquivos, e você pede a etapa em palavras.

Três delas são a espinha dorsal. Outras três são acionadas para você ao longo
da construção de uma candidatura, e você só as roda à mão em material que este
pipeline não produziu. As três últimas são consultivas e podem ser rodadas a
qualquer momento.

## A espinha dorsal

### `/slushpile:onboard`

Monta o workspace. Ingere um currículo existente ou uma exportação do LinkedIn,
entrevista você para cobrir as lacunas e escreve `profile.md`,
`preferences.yaml` e `stories.md`. Confere a toolchain de documentos, cria o
esqueleto do rastreador e passa o bastão.

Rode uma vez por workspace, antes de qualquer outra coisa. Veja
[Primeiros passos](getting-started.md) para o que ter em mãos e
[O workspace](workspace.md) para o que ela escreve.

### `/slushpile:job-board-search`

Vasculha a página de vagas de uma empresa, extrai cada anúncio na íntegra,
estima o pool realista de candidatos, pontua o encaixe ancorado no pool e
condicionado ao canal, roda os critérios de descarte, põe um contrarian na
frente da lista de níveis e cria uma pasta de vaga para cada vaga que sobrevive.

**Argumento:** o nome de uma empresa.

Esta é a etapa de maior retorno do pipeline e a que a maioria das ferramentas
não tem. Tudo o que vem depois dela custa uma tarde por candidatura; esta custa
minutos e pode terminar com "nenhuma delas". Veja
[Pontuação](architecture/scoring.md).

### `/slushpile:application-builder`

Constrói o currículo e a carta de apresentação direcionados para uma pasta de
vaga que já tem uma descrição da vaga e uma análise da vaga, e depois os itera
contra a revisão até que estabilizem ou batam no teto de três rodadas.

**Argumento:** o caminho de uma pasta de vaga.

Ela mesma aciona `explore-experience`, `adversarial-review` e
`removing-ai-tells`. Nunca envia nada; entrega os arquivos prontos na sua mão.

## As três que ela roda por você

Rode uma destas diretamente só para trabalhar em material que este pipeline não
produziu: um currículo escrito em outro lugar, uma carta rascunhada à mão.

### `/slushpile:adversarial-review`

Roda 7 revisores contra um currículo e uma carta de apresentação. Devolve um
veredito e uma faixa de probabilidade por canal de envio, a qualidade do
material pontuada separadamente do valor esperado, e uma passada do contrarian
que pode derrubar todo o resto.

**Argumento:** o caminho de uma pasta de vaga contendo, no mínimo, um currículo
e `job_description.md`.

Veja [A revisão](architecture/the-review.md) para o que cada revisor recebe e o
que é deliberadamente escondido dele.

### `/slushpile:explore-experience`

Entrevista você para trazer à tona experiência que é real mas não está
documentada, mapeada contra os requisitos de uma vaga específica, e depois a
escreve em `profile.md` em definitivo.

Use quando uma avaliação de encaixe ou uma revisão apontar uma seção como rala.
Na maioria das vezes a experiência é real e simplesmente nunca foi escrita, e é
por isso que isto é uma entrevista, não uma reescrita.

### `/slushpile:removing-ai-tells`

Tira construções, estrutura e escolhas de palavras que denunciam autoria de IA,
rodando passadas iterativas por instâncias novas do agente de voz, com o
orquestrador filtrando cada mudança individual.

Use em uma carta de apresentação antes do envio, ou em qualquer texto que
precise ser lido como escrito por uma pessoa.

## A qualquer momento

### `/slushpile:redesign-templates`

Reestiliza `resume.tex` e `cover_letter.tex` no seu próprio padrão visual
(tipografia, paleta, layout) mantendo fixas as restrições de ATS, e depois prova
que o resultado ainda compila e ainda é extraído.

Rode isto em vez de editar o checkout do plugin, que a próxima atualização
substitui.

### `/slushpile:status`

Lê cada `application.yaml` do workspace e reporta o estado da busca: a fila
ranqueada, o que está esperando por você, o que ficou em silêncio, e a regressão
das previsões do próprio pipeline contra o que de fato aconteceu. Escreve as
conclusões da calibração de volta em `job_search.md` e `preferences.yaml`.

Rode depois que os resultados chegarem. Veja
[Memória e calibração](architecture/memory-and-calibration.md).

### `/slushpile:help`

Explica o que é o slushpile, o que cada habilidade faz, em que ordem rodá-las,
onde ficam os arquivos do workspace e como configurar um agente de voz.

Rode quando você não souber o que rodar.
