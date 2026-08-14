# Arquitetura do Slushpile

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/index.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/index.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/index.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/index.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile não é um programa. É um conjunto de arquivos Markdown que um agente de
codificação lê e sobre os quais age: 10 habilidades que orquestram, 8 definições
de agente que fazem cada uma um único trabalho, e um punhado de templates. Não há
motor, não há runtime e não há estado fora do diretório de trabalho do próprio
usuário.

Isso condiciona cada decisão documentada aqui. Uma regra que este pipeline queira
ver cumprida precisa sobreviver a ser parafraseada por um modelo sob carga,
porque não há interpretador que a imponha. Um fato de que o pipeline precisa tem
que morar em um arquivo que o modelo realmente vá ler, porque não há banco de
dados a consultar.

| Arquivo | Conteúdo |
| --- | --- |
| [pipeline.md](pipeline.md) | Os cinco diagramas, a legenda e o que cada estágio faz. |
| [the-review.md](the-review.md) | Por que a revisão tem a forma que tem: o estágio cego, a ordem de despacho, o guardião e o teto de três rodadas. |
| [scoring.md](scoring.md) | Ancoragem no pool de candidatos, vereditos condicionados ao canal, níveis e critérios de descarte. |
| [memory-and-calibration.md](memory-and-calibration.md) | O espaço de trabalho como memória duradoura, os caminhos de reescrita e como os resultados corrigem as previsões. |
| [agents-and-models.md](agents-and-models.md) | A fronteira entre habilidade e agente, o nível de modelo de cada persona e os agentes de voz. |
| [personal-data.md](personal-data.md) | Por que nenhum dado pessoal pode morar no plugin, e a barreira que faz isso valer. |
| [generated-surfaces.md](../../../../docs/architecture/generated-surfaces.md) | Por que seis superfícies descrevem este pipeline e nenhuma delas é dona de um fato. |
| [AGENTS.md](../../../../docs/architecture/AGENTS.md) | Gêmeo idêntico byte a byte do `CLAUDE.md` deste diretório, restringindo edições a estas convenções. |
