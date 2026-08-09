# Pontuação

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/scoring.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/scoring.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/scoring.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/scoring.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/scoring.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Todo número que este pipeline produz é resposta a uma de duas perguntas: onde o
candidato está na fila para esta vaga específica, e quanto vale de fato uma
candidatura por um dado canal. Nada aqui pontua um documento contra um anúncio
isoladamente, porque isso é um número real sobre a pergunta errada.

## Ancoragem no pool

Uma nota de correspondência de palavras-chave compara um currículo a uma
descrição de vaga. Ninguém é contratado por uma descrição de vaga. A comparação
que decide o resultado é contra os outros candidatos na fila, e uma nota de
correspondência não consegue vê-los.

Por isso o estágio de busca estima o pool de candidatos primeiro: quem mais se
candidata a esta requisição, e com o que se parecem o candidato mediano, o do
75º percentil e o do 90º percentil. O candidato é então localizado nessa
distribuição, e **o percentil no pool é registrado como o número canônico de
encaixe.** A correspondência de palavras-chave, se for desejada, vai em um campo
separado. Fundir as duas coisas é exatamente a falha que a rubrica existe para
evitar.

| Posição no pool | Nível | Significado |
| --- | --- | --- |
| p75+ | Nível 1 | Acima da barra de candidato forte para esta vaga específica |
| p55–p74 | Nível 2 | Competitivo, não diferenciado. Precisa de uma vantagem de canal. |
| p35–p54 | Nível 3 | Abaixo da mediana. Perseguir apenas por um canal forte. |
| abaixo de p35 | Pass | O pool supera o candidato. Uma candidatura fria é um lugar na fila desperdiçado. |

As entradas são ordenadas. Duas ou mais qualificações mínimas críticas não
atendidas derrubam a posição em um a dois níveis, independentemente de todo o
resto. Depois a comparação com o pool: a alegação mais forte de fato se
destaca aqui, ou é mediana? Depois a divergência em relação ao ritmo real de
operação da vaga, depois os fatores de risco a mais ou menos cinco a dez pontos
percentuais cada, depois o prior de calibração para a empresa.

A saída mais útil deste estágio é um diferencial alegado voltando marcado como
mediano no pool. Essa é uma informação que o candidato não obtém de um
escaneador de documentos, e costuma ser o que muda o que ele escreve.

## Vereditos condicionados ao canal

Os mesmos materiais convertem a taxas muito diferentes conforme a forma como
chegam. Um veredito único faz a média dessa diferença e reporta a média como se
fosse um fato sobre a candidatura.

Por isso toda vaga de Nível 1 a 3 recebe uma matriz em vez de um veredito:

| Canal | Barreira | Faixa aproximada de aprovação na triagem |
| --- | --- | --- |
| Candidatura fria | nenhuma | 5–15%, varia com a posição no pool |
| Indicação quente | precisa existir quem indique | 25–50%, depende do pool |
| Abordagem fria a um funcionário nomeado | um alvo identificável | 5–15% |
| Entrada por trabalho público | um artefato existente, semeado | 20–40% se pegar |
| Contato de recrutador | fora do controle do candidato | não estimado |

Duas regras impedem que isso seja decorativo.

**O nível da vaga é o nível mais alto entre os canais *disponíveis***, e a matriz
registra qual canal o destrava e que barreira precisa ser vencida. Se hoje não
existe quem indique, a linha da indicação quente é apenas informativa e não
destrava o Nível 1. Inflar um nível apoiando-se em um canal indisponível é a
forma mais comum de burlar esta matriz, e ela é autoinfligida.

**O histórico do próprio usuário ganha de qualquer prior.** Onde `job_search.md`
registra uma taxa real de indicação quente nesta empresa, esse número é usado no
lugar do genérico. Veja
[memory-and-calibration.md](memory-and-calibration.md).

## Qualidade dos materiais não é valor esperado

A revisão reporta os dois como números separados porque eles discordam com
frequência. Materiais excelentes enviados para uma vaga mal alinhada continuam
tendo valor esperado baixo; materiais adequados enviados por indicação para uma
vaga bem alinhada têm valor esperado alto.

Fundir os dois manda o usuário gastar mais uma hora editando quando a
recomendação honesta é gastar essa hora procurando quem o indique. Uma nota de
materiais de 8/10 ao lado de uma conversão fria de 1–3% não é uma contradição: é
o achado inteiro.

## Critérios de descarte

Os critérios de descarte rodam no momento da varredura e são checados contra
`preferences.yaml`: remuneração, localização, credenciamento de segurança e o que
mais o usuário tiver registrado como restrição.

Duas propriedades importam mais do que a lista em si.

**As aprovações são declaradas, não só as falhas.** Uma checagem que reporta só o
que falhou é indistinguível de uma checagem que não rodou, e aqui não há
interpretador para provar que ela rodou.

**Um Pass nomeia seu único bloqueador principal.** Se nenhum bloqueador isolado
justifica, por si só, dar Pass na vaga, a vaga recebe uma nota em vez de um Pass.
Um Pass justificado por um acúmulo de pequenas dúvidas é um estado de humor, e
não vai sobreviver à releitura do próprio usuário uma semana depois.

A remuneração é avaliada pela **faixa publicada**, usando o método registrado em
`preferences.yaml`. Os termos da fase de oferta estão explicitamente fora de
escopo aqui pelo mesmo motivo pelo qual são riscados na revisão: veja
[the-review.md](the-review.md#the-gatekeeper).

## Faixas de probabilidade, não palavras de veredito

A saída é “1–3% de entrevista” em vez de “MAYBE”. Uma faixa carrega a própria
incerteza e pode ser conferida contra o que de fato aconteceu; uma palavra de
veredito não carrega nenhuma das duas coisas e não pode.

É isso também que torna possível o laço de calibração. “MAYBE” não pode ser
regredido contra resultados. Uma porcentagem pode, e é em
[memory-and-calibration.md](memory-and-calibration.md) que essa regressão
acontece.
