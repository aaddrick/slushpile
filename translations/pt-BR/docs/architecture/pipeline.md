# O pipeline, estágio por estágio

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/pipeline.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/pipeline.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/pipeline.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/pipeline.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/pipeline.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## O laço inteiro

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/pipeline-overview-dark.svg">
  <img alt="Slushpile de ponta a ponta. Primeira linha, da esquerda para a direita: onboard, que entrevista e ingere um currículo para escrever perfil, preferências e histórias; busca em quadro de vagas, que extrai anúncios literalmente e pontua o encaixe ancorado no pool de candidatos e o valor esperado por canal; construtor de candidatura, que produz o ângulo, o currículo, a carta, a passagem de voz e a etapa de humanização; e revisão adversarial, 7 revisores no total, 5 revisores em paralelo e cegos entre si, devolvendo um veredito por canal. Construtor e revisão são ligados por uma seta bidirecional rotulada até três rodadas. O fluxo desce da revisão para uma caixa azul, você envia, observando que nenhuma habilidade toca um portal, um e-mail ou um formulário. A segunda linha se lê de volta, da direita para a esquerda: resultado registrado, depois status, que compara as previsões do pipeline com os resultados, depois uma seta tracejada rotulada priors entrando na caixa do espaço de trabalho que guarda profile.md, preferences.yaml, stories.md e job_search.md. Uma seta tracejada liga o espaço de trabalho de volta ao onboard, rotulada escrito pelo onboarding, lido por todo estágio." src="../../../../docs/diagrams/pipeline-overview-light.svg">
</picture>

Três comandos formam a espinha dorsal: `onboard` uma vez por espaço de trabalho,
depois `job-board-search` e `application-builder` por empresa e por vaga. O
construtor despacha `explore-experience`, `adversarial-review` e
`removing-ai-tells` por conta própria.

O laço no rodapé é a parte que não tem equivalente em um otimizador de currículo.
Os resultados são registrados, o `status` faz a regressão do que o pipeline
previu contra o que aconteceu, e os priors corrigidos voltam para
`preferences.yaml`, onde a próxima busca os lê. Veja
[memory-and-calibration.md](memory-and-calibration.md).

## Legenda

Todo diagrama desta página desenha a partir de um único vocabulário de classes,
definido em `docs/diagrams/theme-light.d2` e `theme-dark.d2`. Os dois arquivos de
tema e esta tabela são conferidos um contra o outro por `tests/test_docs.py`.

| Classe | Significa |
| --- | --- |
| `stage` | Um passo comum que a própria habilidade orquestradora executa |
| `agent` | Uma persona despachada: um subagente com definição própria em `agents/` |
| `gate` | Uma barreira ou um laço com teto: um ponto onde a execução pode iterar, travar ou parar |
| `memory` | Um arquivo duradouro do espaço de trabalho, escrito uma vez e lido por todo estágio posterior |
| `human` | O único lugar onde o usuário é obrigatório |
| `terminal` | Um estado terminal para aquele diagrama |
| `phase` | Um contêiner agrupando células que rodam juntas |
| `flow` | Uma aresta normal para a frente |
| `loop` | Uma aresta para trás: retrabalho, nova revisão, outra rodada |
| `writeback` | Uma aresta que escreve na memória do espaço de trabalho |

A distinção entre `stage` e `agent` é a que vale ler com atenção. Uma caixa
`agent` é um subagente com definição própria e contexto próprio. Em um harness
que não sabe despachar subagentes, são elas que colapsam em um único contexto, e
esse colapso é toda a diferença entre uma execução completa e uma degradada.

## `/slushpile:onboard`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-onboard-dark.svg">
  <img alt="As fases do onboarding. Primeira linha: ingerir um currículo em qualquer formato ou uma exportação do LinkedIn; entrevistar para as lacunas que um documento não preenche, com números recebendo linhas de base; profile.md, descrito como o material de onde um currículo é recortado, e não como um currículo; preferences.yaml, guardando o método de remuneração e as restrições, com calibration_priors deixado vazio. A segunda linha se lê de volta, da direita para a esquerda: stories.md, de quatro a oito histórias contáveis com os números anexados; uma barreira de agente de voz que aponta o usuário para o seu próprio e deixa is_mine falso até que ele tenha um; scaffold, escrevendo job_search.md e companies.md e rodando a checagem da toolchain; e verificar e entregar, onde toda checagem é reportada, inclusive as que passaram." src="../../../../docs/diagrams/phase-onboard-light.svg">
</picture>

O onboarding é uma entrevista, não um formulário. Ele roda uma vez e tudo que vem
depois lê o que ele escreveu.

Dois de seus passos são barreiras, não trabalho. O passo do agente de voz se
recusa a construir um perfil de voz por conta própria: um perfil improvisado a
partir de algumas amostras de escrita soa como o padrão do modelo usando o nome
do usuário, e o usuário vai confiar nele porque parece pronto. Em vez disso, ele
define `voice.is_mine: false` e aponta para
[written-voice-replication](https://github.com/aaddrick/written-voice-replication).
O passo de verificação declara quais checagens *passaram*, não apenas quais
falharam, porque uma checagem que reporta só as falhas é indistinguível de uma
que nunca rodou.

`calibration_priors` é deixado vazio de propósito. Um prior inventado é uma
restrição que o usuário nunca escolheu, matando vagas em silêncio por um motivo
que ele não consegue ver. Ele se preenche a partir de resultados reais mais
tarde, ou fica vazio e toda estimativa rio abaixo é rotulada como não calibrada.

## `/slushpile:job-board-search`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-search-dark.svg">
  <img alt="As fases da busca em quadro de vagas. Primeira linha: descoberta, encontrando a URL de carreiras e rodando várias consultas antes de triar pelos títulos; captura literal, tomando o anúncio como escrito e não resumido; estimativa do pool de candidatos, caracterizando quem mais se candidata como arquétipos p50, p75 e p90; e a nota de encaixe, onde o número é o percentil no pool e não a correspondência de palavras-chave. A segunda linha se lê de volta, da direita para a esquerda: a matriz de valor esperado por canal, cobrindo candidatura fria, indicação, abordagem direta e entrada por trabalho público, onde o nível é o melhor canal de fato disponível; critérios de descarte sobre remuneração, localização e credenciamento de segurança, checados e declarados de todo jeito; uma barreira do contrarian que roda antes de os níveis serem finais e pode rebaixar um nível ou descartar uma vaga; e pastas de vaga, uma por vaga com a descrição da vaga e a análise, mais o rastreador e o arquivo de empresas atualizados." src="../../../../docs/diagrams/phase-search-light.svg">
</picture>

Este é o estágio de maior retorno, e é o que a maioria das ferramentas não tem.
Tudo rio abaixo custa ao usuário uma tarde por candidatura. Este estágio custa
minutos e pode terminar com “não se candidate a nenhuma destas”.

O anúncio é capturado **literalmente**. 3 agentes mais adiante analisam esse
texto diretamente, o analista de requisitos, o simulador de ATS e o analista do
pool, e um anúncio resumido remove em silêncio a redação exata das qualificações
que esses três existem para conferir.

A barreira do contrarian roda *antes* de os níveis serem finalizados, e não
depois, porque uma lista de níveis que o usuário já leu é uma lista com a qual
ele já se comprometeu. Veja [scoring.md](scoring.md) para o que os níveis
significam e o que os critérios de descarte checam.

## `/slushpile:application-builder`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-build-dark.svg">
  <img alt="As fases do construtor de candidatura. Primeira linha: ângulo, escolhendo o currículo-base, a tese, o gancho e a única história que vale contar; currículo, adaptado e depois compilado, lendo o texto extraído em vez do fonte; carta de apresentação, escrita pelo agente de voz nomeado em preferences.yaml; e humanizar, rodando removing-ai-tells com o orquestrador barrando cada mudança. A segunda linha se lê de volta, da direita para a esquerda: revisão adversarial rodada um, produzindo uma nota de ATS, testes de troca e valor esperado por canal; corrigir, primeiro as correções mecânicas e depois a profundidade tirada de profile.md; revisão adversarial rodada dois, cuja barreira de decisão lê o veredito do canal de maior valor esperado, ligada a corrigir por um laço tracejado rotulado três rodadas no máximo; e finalizar, a compilação final com application.yaml, o perfil e o rastreador atualizados." src="../../../../docs/diagrams/phase-build-light.svg">
</picture>

O construtor escreve e depois ataca o que escreveu. Um modelo a quem se pergunta
se o próprio rascunho é bom vai dizer que sim, longamente, então o construtor
nunca pergunta: ele entrega os materiais a uma revisão que não tem nada
investido neles.

A ordem das correções importa. As mecânicas vêm primeiro porque são baratas e não
ambíguas: palavras-chave faltando, datas só com o ano, um marcador copiado quase
literalmente do anúncio. Só então ele tenta as caras, onde uma seção rala precisa
ser preenchida a partir de `profile.md`, e onde, se o material genuinamente não
estiver no perfil, ele roda `/slushpile:explore-experience` em vez de inventá-lo.

**Três rodadas é o teto.** Se o veredito não se moveu até a terceira rodada, a
lacuna é estrutural, e continuar editando é movimento, não progresso. O teto
existe porque a alternativa é um laço que sempre acha alguma coisa, e uma revisão
que sempre acha alguma coisa é indistinguível de uma que não acha nada.

## `/slushpile:adversarial-review`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-review-dark.svg">
  <img alt="A revisão adversarial. Primeiro, reunir os materiais: rodar pdftotext no PDF compilado, mais a descrição da vaga, a análise da vaga, preferences.yaml e job_search.md. Isso alimenta um contêiner com 5 revisores em paralelo, especialistas cegos despachados em uma única mensagem, nenhum vendo o relatório do outro: o triador em onze segundos, só com o currículo; o analista de requisitos em trinta segundos, conferindo cada qualificação; o simulador de ATS como um parser e não como um leitor; o leitor cansado na candidatura sessenta e um de oitenta; e o analista do pool perguntando quem mais está na fila. Uma aresta rotulada todos os cinco retornam leva ao gestor da vaga, que vê os cinco relatórios e produz um veredito por canal, com a qualidade pontuada separadamente do valor esperado. Depois o contrarian, que vê tudo, inclusive o gestor da vaga, pode derrubá-lo e nunca é opcional. Depois o guardião, o orquestrador e não um agente, que risca falsos positivos e descartes fora de escopo, re-deriva a decisão líquida e roda o pipeline inteiro de novo com instâncias novas quando os materiais mudam. Por último, apresentar e registrar, priorizado pelo impacto sobre o canal de maior valor esperado e não por qual agente gritou mais alto." src="../../../../docs/diagrams/phase-review-light.svg">
</picture>

Os 5 revisores em paralelo do contêiner são despachados em uma única mensagem e
não conseguem ver os achados uns dos outros. Cada um recebe apenas o que seu
papel genuinamente teria: o triador nunca vê a carta de apresentação, porque um
triador que leu a carta não é um triador.

O guardião é a habilidade orquestradora, não um agente. As personas são
deliberadamente duras e parte do que produzem está errado, então algo precisa
aplicar julgamento à saída delas, e esse algo não pode ser uma delas.

[the-review.md](the-review.md) cobre a ordem de despacho, o que é sonegado a cada
persona e quais achados o guardião pode riscar.
