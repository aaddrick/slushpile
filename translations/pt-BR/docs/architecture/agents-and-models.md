# Agentes e modelos

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/agents-and-models.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/agents-and-models.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/agents-and-models.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/agents-and-models.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

## Uma habilidade orquestra. Um agente tem um único trabalho.

São dois tipos diferentes de arquivo e a fronteira entre eles é estrutural.

Uma habilidade sabe do pipeline: em que estágio está, o que rodou antes dela,
para quem ela entrega. Um agente sabe apenas do próprio trabalho. **Um agente que
sabe em que estágio está vai otimizar para o estágio em vez de fazer seu
trabalho**: um triador informado de que é o primeiro de cinco começa a fazer
ressalvas, porque percebe que outra pessoa vai conferir o trabalho dele.

O corolário é a regra que mantém a saída da revisão comparável:

**As restrições vinculantes ficam na definição do agente, não no prompt de
despacho.** Um orquestrador que improvisa restrições extras a cada execução
produz achados que não podem ser comparados entre candidaturas, o que destrói os
dados de calibração de que o sistema inteiro depende. Os limites de escopo do
contrarian estão em `agents/slushpile-contrarian.md` por esse motivo, e a
habilidade de revisão é explicitamente instruída a não repeti-los nem
estendê-los.

Os dados são a exceção, e a distinção vale ser dita com precisão.
`calibration_priors` vai no prompt de despacho porque muda *o que o agente sabe*.
Os limites de escopo ficam na definição porque mudam *o que o agente pode dizer*.
O primeiro varia por execução por projeto; o segundo não pode variar.

## Todo agente declara um modelo

<!-- BEGIN GENERATED agent-table: scripts/sync_docs.py -->

| # | Agent | Model | Simulates |
|---|---|---|---|
| 1 | `slushpile-triage-screener` | sonnet | 11 seconds, F-pattern, 347 resumes already read today |
| 2 | `slushpile-requirements-analyst` | sonnet | 30 seconds, methodical, checks every qualification against evidence |
| 3 | `slushpile-ats-simulator` | sonnet | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| 4 | `slushpile-fatigued-reader` | sonnet | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| 5 | `slushpile-pool-analyst` | opus | A recruiter who knows what the queue actually looks like |
| 6 | `slushpile-hiring-manager` | opus | The person who has to justify the interview slot to their skip-level |
| 7 | `slushpile-contrarian` | opus | Whoever should have asked whether any of this was worth doing |

Plus the voice agent, `aaddrick-voice`, which the review never dispatches and
which is named in `preferences.yaml` rather than here. The first five run in
parallel and are blind to each other; the last two run in order.

<!-- END GENERATED agent-table -->

O modelo está no frontmatter de cada agente, e a tabela de despacho em
`skills/adversarial-review/SKILL.md` também nomeia um por agente. Os dois são
conferidos um contra o outro por `tests/test_structure.py`: o frontmatter é
aquilo sobre o que um harness de fato despacha, e a coluna da tabela é a
documentação disso.

Um agente sem modelo declarado assume o que quer que a sessão esteja rodando.
Isso achata em silêncio uma revisão que mistura níveis de propósito, e é por isso
que o campo é obrigatório e não opcional.

A divisão não é arbitrária. Cada uma das personas mais baratas simula uma leitura
**limitada e mecânica**: onze segundos passando o olho, um checklist de
qualificações, um parser, a irritação de um leitor cansado. São tarefas bem
especificadas nas quais um modelo maior sobretudo acrescenta custo.

Cada uma das caras exige **estimar algo que não está no documento**. O analista
do pool de candidatos precisa caracterizar candidatos que não estão diante dele.
O gestor da vaga precisa pesar cinco relatórios uns contra os outros e
produzir probabilidades. O contrarian precisa construir o argumento mais forte de
que tudo isso está errado. Essas se degradam de forma visível em um modelo menor,
e são as três cuja saída o usuário de fato usa para agir.

## Espaço de nomes

Todo agente do pipeline recebe o prefixo `slushpile-` para não poder colidir com
um agente que o usuário já tenha. Um usuário com seu próprio `contrarian` fica
com ele; o deste pipeline é `slushpile-contrarian` e os dois nunca se encontram.

## Os agentes de voz são a exceção deliberada

O agente de voz é o único agente deste repositório que não se chama
`slushpile-*`, e o único cujo nome é o de uma pessoa.

Isso porque ele é gerado por pessoa pelo
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
e leva o nome de seu autor. Um usuário que troque pelo seu próprio precisa poder
manter esse nome, então o nome é lido de `preferences.yaml` em tempo de execução
em vez de ficar embutido em algum lugar:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`agents/aaddrick-voice.md` vem como o exemplo prático público daquele projeto,
para que o slushpile rode de imediato antes de o usuário ter gerado um. É a voz
do autor do plugin, não a do usuário, e enquanto `is_mine` for falso toda
habilidade que escreve prosa avisa antes de rodar. Esse aviso é a única coisa
entre um usuário e doze candidaturas enviadas na voz de um estranho.

Ele é isento dos padrões de identidade em `scripts/check_no_pii.py`, mas nunca do
padrão de dados de contato. Veja [personal-data.md](personal-data.md).

**Não adicione um segundo agente de voz a este repositório.** Um exemplo é uma
demonstração; dois são uma biblioteca de vozes alheias que ninguém pediu.
