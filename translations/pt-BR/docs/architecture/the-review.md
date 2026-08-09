# A revisão

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/the-review.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/the-review.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/the-review.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/the-review.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:adversarial-review` despacha 7 revisores contra um currículo e uma
carta de apresentação. Esta página é o porquê dessa forma. O desenho está em
[pipeline.md](pipeline.md); as definições por agente estão em `agents/`.

## Quatro modos de falha, quatro estágios

A forma não é um comitê arbitrário. Cada estágio responde a um jeito específico
pelo qual um pipeline de revisão ingênuo produz besteira com confiança.

**Bajulação de perspectiva única.** Todo revisor em um pipeline ingênuo trabalha
para o candidato. Nenhum deles modela a fila. O analista do pool de candidatos
existe para forçar raciocínio comparativo: não “estes materiais são bons”, mas
“eles são melhores do que as outras setenta candidaturas que esta requisição
recebeu esta semana”.

**Colapso do veredito.** Uma única resposta INTERVIEW / MAYBE / PASS esconde que
os mesmos materiais convertem a taxas muito diferentes a frio e por indicação.
São decisões diferentes sobre a tarde do usuário. O gestor da vaga produz um
veredito por canal, com uma faixa de probabilidade em vez de uma palavra.

**Preocupação sintética com detecção de IA.** Uma persona detectora de IA marca
padrões com base na dúvida hipotética de um leitor, e vai atropelar o julgamento
fundamentado sobre o que um leitor real percebe. Ela é substituída pelo leitor
cansado, que faz a pergunta respondível: isto irritaria alguém na sexagésima
primeira candidatura do dia?

**Nenhuma etapa de falseamento.** Nada em uma revisão normal pergunta o que teria
de ser verdade para o exercício inteiro ser um desperdício de ciclos. O
contrarian pergunta isso, por último, com permissão para derrubar tudo que veio
antes.

## O estágio cego

Os primeiros 5 revisores em paralelo são despachados em uma única mensagem.
Nenhum recebe a saída de outro.

Esta é a propriedade estrutural de toda a revisão, e é a que se degrada em
silêncio. Contaminação não produz um erro; produz concordância. Um especialista
que já leu o veredito da triagem tende a confirmá-lo, e cinco relatórios que
concordam parecem consenso forte em vez de uma única opinião repetida cinco
vezes. O consenso no estágio cego é o sinal mais confiável que o pipeline produz,
e ele só vale alguma coisa porque os cinco não puderam conversar.

Cada persona recebe apenas o que seu papel genuinamente teria:

| Persona | Recebe | Sonegado, e por quê |
| --- | --- | --- |
| Triador | Texto do currículo, título, empresa, senioridade | A carta de apresentação. Ele está simulando onze segundos, e um triador que leu a carta não é um triador. |
| Analista de requisitos | Currículo, carta de apresentação, anúncio completo, senioridade | Nada. Seu trabalho é conferir cada qualificação contra as evidências. |
| Simulador de ATS | Texto do currículo, anúncio completo, e o fonte `.tex` ou `.docx` se houver um | Nada, mas note que ele recebe o *fonte* de propósito: tabelas, colunas e posicionamento de cabeçalho são invisíveis no texto extraído e são exatamente o que ele existe para pegar. |
| Leitor cansado | Currículo, carta de apresentação | Qualquer instrução para julgar autoria de IA. Essa é outra pergunta, e não é a dele. |
| Analista do pool | Tudo, mais o histórico de candidaturas anteriores e as taxas de conversão observadas | Nada. Ele precisa do maior contexto entre os cinco. |

O currículo que toda persona lê é a saída do `pdftotext`, não o fonte LaTeX ou
Markdown. Revisar o fonte é revisar um documento que ninguém jamais verá. Se o
texto extraído sair vazio ou embaralhado, isso é um achado e não uma falha de
ferramenta: um ATS enxerga o que o `pdftotext` enxerga.

## Por que os dois últimos são sequenciais

O gestor da vaga roda depois que todos os cinco retornam, e vê os cinco. O
contrarian roda depois do gestor da vaga, e vê tudo, inclusive ele.

Ordená-los assim custa tempo de relógio e compra a única coisa que o estágio cego
não pode dar: alguém capaz de pesar os cinco uns contra os outros, e depois
alguém capaz de atacar essa pesagem. Um contrarian que rodasse em paralelo com o
gestor da vaga estaria discutindo com uma síntese que nunca leu.

O contrarian é **automático, não condicional**. Uma etapa de falseamento que só
roda quando o orquestrador se sente incerto vai se pular exatamente nos casos em
que a certeza era infundada.

## Os priors são passados literalmente, inclusive quando estão vazios

Tanto o analista do pool quanto o contrarian recebem o bloco
`calibration_priors` de `preferences.yaml` como está escrito.

Resumi-lo para “o candidato converte mal” tira o tamanho da amostra, que é a
única coisa que diz quanto peso o número merece. E omitir o bloco quando ele não
está definido soa para o agente como uma execução comum e não como uma execução
não calibrada: uma estimativa não calibrada que não é rotulada como tal é pior do
que nenhuma estimativa, porque rio abaixo ela é indistinguível de uma calibrada.

Quando uma taxa observada tem amostra de cinco ou mais, o analista do pool é
instruído a usá-la no lugar do próprio prior para aquele canal, e a dizer que
fez isso.

## O guardião

A habilidade orquestradora é o guardião. Ela não é uma das personas, e isso é
deliberado: as personas são afinadas para serem duras, parte do que produzem está
errado, e nada afinado para ser duro pode ao mesmo tempo ser aquilo que decide o
que descartar.

Ela confere cada persona contra a própria carta de atribuições: o triador ficou
dentro dos onze segundos, ou citou algo da terceira página? O simulador de ATS
marcou uma formatação que os parsers modernos tratam bem? O leitor cansado
marcou como defeito uma marca de voz deliberada, documentada no agente de voz do
próprio usuário?

Duas classes de argumento do contrarian são **riscadas** em vez de pesadas:

1. **Termos contratuais da fase de oferta.** Verba de mudança, bônus de
   contratação, participação acionária, data de início, compra de uma cláusula de
   devolução. Isso é negociado depois que existe uma oferta. Descartar uma
   candidatura por causa de dinheiro que ainda é negociável, no estágio em que o
   candidato tem a menor alavancagem, é um erro de categoria.
2. **Uma requisição vizinha não avaliada.** Uma cadeira mais bonita em outro
   lugar da mesma empresa não é uma entrada, a menos que tenha sido avaliada por
   completo e o usuário tenha pedido que fosse pesada. O sequenciamento entre
   requisições é decisão do usuário.

Todo o resto que o contrarian levanta está no escopo: probabilidade de conversão,
estrutura de canal, posição no pool, lacunas de qualificação, exageros, falhas
no teste de troca, densidade dos materiais, sinalização de encaixe no nível e
histórico adverso de candidaturas na empresa-alvo.

Tanto as pernas riscadas quanto as que sobreviveram são registradas em
`role_analysis.md`. Registrar só o resultado torna a barreira impossível de
melhorar, porque os falsos positivos que ela pegou ficam invisíveis no instante
em que ela os pega.

## O teto de três rodadas

As rodadas são comparadas, não apenas repetidas. Um problema apontado em mais de
uma rodada é real; um problema apontado uma vez é ruído. Esse sinal só existe se
a revisão rodar mais de uma vez, e é por isso que o construtor a roda duas vezes
por padrão.

Toda rodada usa **instâncias novas de agente**. Uma persona que já viu o próprio
veredito não consegue re-derivá-lo de forma independente, então reaproveitar um
relatório entre rodadas converte uma segunda opinião em eco.

Três rodadas é o teto. Além disso, as lacunas restantes são estruturais, e a
saída honesta é dizer isso em vez de rodar uma quarta rodada e produzir mais
edições.

## Em um harness sem despacho de subagentes

Codex e Gemini CLI não têm despacho de subagentes. A revisão ainda roda: as
personas são assumidas uma por vez, em um único contexto, com cada relatório
escrito por inteiro antes de o próximo começar.

Duas coisas se degradam, e vale saber quais. Fica mais lento, o que não importa
muito. E o estágio cego deixa de ser cego, o que importa: a contaminação descrita
acima é exatamente o que um contexto compartilhado reintroduz. A habilidade
instrui o modelo a escrever cada relatório por completo antes de começar o
próximo, o que limita a deriva sem eliminá-la.
