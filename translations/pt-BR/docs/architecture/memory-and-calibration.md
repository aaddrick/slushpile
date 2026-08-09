# Memória e calibração

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/memory-and-calibration.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/memory-and-calibration.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/memory-and-calibration.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/memory-and-calibration.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/memory-and-calibration.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Uma busca de emprego são quarenta candidaturas ao longo de três meses. Uma
ferramenta sem memória cobra o preço cheio por cada uma delas: você cola um
currículo, recebe um número de volta, fecha a aba, e a ferramenta encerra a
sessão sabendo exatamente o que sabia no começo.

A memória do slushpile é um diretório de arquivos que pertencem ao usuário. Não
há banco de dados, não há conta e não há estado dentro do plugin: o plugin é
código público e o espaço de trabalho é o histórico profissional do usuário,
então são coisas diferentes guardadas em lugares diferentes. Veja
[personal-data.md](personal-data.md).

## O que é duradouro

| Arquivo | Escrito por | Lido por |
| --- | --- | --- |
| `profile.md` | `onboard`, estendido por `explore-experience` e `application-builder` | todo estágio que escreve prosa |
| `preferences.yaml` | `onboard`, corrigido por `status` | a pontuação, os critérios de descarte, o despacho da revisão |
| `stories.md` | `onboard` | o construtor, quando escolhe a única história a contar |
| `job_search.md` | `job-board-search`, `application-builder`, `status` | o analista do pool de candidatos, o contrarian, a fila |
| `companies.md` | `job-board-search` | buscas posteriores na mesma empresa |
| `applications/<company>/<role>/` | `job-board-search`, depois o construtor | a revisão, e o `status` |

`profile.md` não é um currículo. É o material de onde um currículo é recortado,
várias vezes mais longo do que qualquer coisa que alguém enviaria, e seu valor é
que nada nunca faz ao usuário aquelas perguntas duas vezes.

## Os caminhos de reescrita

São três, e cada um existe porque algo aprendido em um estágio é inútil se ficar
ali.

**Achado da revisão → perfil.** Quando uma revisão diz que uma seção está rala, a
entrevista que vem em seguida costuma descobrir que a experiência era real e que
o usuário nunca a tinha escrito. O `explore-experience` traz isso à tona e vai
para `profile.md` de forma permanente, onde toda candidatura posterior pode se
apoiar nisso. Este é o caminho que faz a vigésima candidatura começar de um lugar
melhor do que a primeira.

**Resultado → rastreador.** O usuário registra o que aconteceu: sem resposta,
triagem, entrevista, oferta, rejeição, e em que estágio. Nada mais no pipeline
pode produzir isso, porque o pipeline nunca submete nada e nunca vê uma resposta.

**Rastreador → priors.** O `status` faz a regressão das próprias previsões do
pipeline contra esses resultados e escreve a correção em `preferences.yaml`.

## Por que a correção vai para os dados do usuário

O lugar óbvio para registrar “este pipeline é 12 pontos otimista sobre
candidaturas frias a laboratórios de fronteira” é o agente que fez a estimativa.
Esse é o lugar errado, e de um jeito silencioso: as definições de agente vêm com
o plugin, então uma edição ali é revertida pela próxima atualização sem aviso,
deixando um pipeline que *estava* afinado e não está mais.

Por isso a correção vai para `preferences.yaml`, que pertence ao usuário e
nenhuma atualização toca. O `job-board-search` lê `calibration_priors` no momento
da pontuação, e o `adversarial-review` passa o bloco ao analista do pool e ao
contrarian no despacho.

## As regras que mantêm a calibração honesta

**Cinco candidaturas resolvidas é o piso.** Abaixo disso, o `status` imprime as
contagens e diz que a amostra é pequena demais para regredir, em vez de produzir
uma tabela. Uma taxa calculada a partir de dois resultados é ruído fantasiado de
calibração, e uma vez que ela está numa tabela ninguém lembra do denominador.

**O silêncio conta como rejeição.** Uma candidatura enviada há mais de 30 dias
sem resposta é registrada como `no_response`, e não deixada pendente. Excluí-las
é a maior fonte isolada de otimismo disponível para uma tabela como esta. A
contagem inferida desse jeito é reportada.

**Avalie contra o canal de fato usado.** Os vereditos são agrupados pelo veredito
do canal pelo qual a candidatura de fato passou, nunca pelo do melhor caso.
Avaliar uma candidatura fria contra o veredito de indicação quente é como um
pipeline se convence de que estava certo.

**Os dois sentidos do erro são reportados.** Um veredito INTERVIEW que foi
auto-rejeitado em menos de 72 horas significa que a revisão deixou passar algo
que um filtro pegou em segundos. Um REJECT que converteu significa que a revisão
foi dura demais, e cada vaga da qual ela dissuadiu o usuário desde então é um
custo que não aparece em nenhum outro lugar. Só um desses dois é confortável de
reportar, e é por isso que a regra nomeia os dois.

**O achado nomeia um segmento, uma direção e um tamanho.** “O pipeline está mal
calibrado” não é acionável e nenhum agente consegue consumir isso. “Vereditos
INTERVIEW em candidaturas frias a laboratórios de fronteira converteram 0 de 7,
contra 12% estimados” pode ser escrito em um prior e usado para agir.

**Um prior nulo é uma resposta válida.** Só são escritas taxas apoiadas em cinco
ou mais candidaturas resolvidas naquele canal. Todo o resto fica nulo, os agentes
usam os padrões com que vêm, e rotulam a estimativa como não calibrada. Um prior
calculado a partir de dois resultados afasta a pontuação da realidade mais do que
nenhum prior afasta, e chega vestindo a autoridade de um número empírico.

**O diff é mostrado antes de `preferences.yaml` ser escrito.** É o arquivo de
restrições do usuário e a mudança altera como toda avaliação futura pontua. Uma
mudança de pontuação sobre a qual ninguém foi avisado é indistinguível de o
pipeline derivar por conta própria.
