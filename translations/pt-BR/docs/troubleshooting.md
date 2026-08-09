# Solução de problemas

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/troubleshooting.md">English</a> ·
  <a href="../../zh-CN/docs/troubleshooting.md">简体中文</a> ·
  <a href="../../es/docs/troubleshooting.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../vi/docs/troubleshooting.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/troubleshooting.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

**`plugin install` conclui, mas as habilidades não aparecem.** Rode `claude plugin
list` e procure por `enabled`. As habilidades carregam no início da sessão,
então abra uma sessão nova ou rode `/clear`.

**Uma habilidade diz que não encontra `preferences.yaml`.** Você está em um
diretório diferente daquele em que rodou o onboarding. Toda habilidade lê o
workspace a partir do diretório de trabalho atual. Veja
[O workspace](workspace.md).

**Os agentes da revisão reportam um currículo quase vazio.** Eles estão lendo o
texto extraído, não o seu PDF como ele é renderizado. Rode
`pdftotext yourresume.pdf -` e olhe a saída. Se ela estiver vazia ou
embaralhada, o currículo tem um problema de layout (uma grade de várias colunas,
uma caixa de texto, dados de contato dentro do cabeçalho) e isso é um achado
real, não uma falha de ferramenta. Um ATS enxerga o que o `pdftotext` enxerga.

**A carta de apresentação soa genérica, ou soa como outra pessoa.** Confira
`voice.is_mine` em `preferences.yaml`. Se estiver false, você está usando a voz
de exemplo que vem junto, que é do autor do plugin. Gere a sua com
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
e aponte `voice.agent` para ela. Se já estiver true, o corpus provavelmente era
ralo demais: alguns milhares de palavras é o piso. Veja
[Seu agente de voz](voice.md).

**Toda vaga volta eliminada pela remuneração.** Abra `preferences.yaml` e
confira `compensation`. Com `net_qol`, a causa mais comum é um
`current_baseline` informado como valor bruto em vez de líquido depois de
impostos e moradia, o que faz toda proposta parecer pior do que é.

**Toda vaga volta como Nível 1.** Alguma coisa está pontuando contra o anúncio em
vez de contra o pool de candidatos. Confira se `role_analysis.md` de fato contém
arquétipos por percentil para a vaga, e não só uma comparação de palavras-chave:
uma nota de encaixe sem estimativa de pool por trás é uma nota de
correspondência usando o nome de um percentil. Veja
[Pontuação](architecture/scoring.md).

**A revisão nunca diz não.** Confira se o contrarian chegou a rodar: a decisão
líquida dele deve aparecer no resumo do pipeline e em `application.yaml`, no
campo `contrarian_net`. Ele é para ser automático, não condicional, e uma
revisão sem ele é uma revisão sem etapa de falsificação.

**A calibração diz que não há dados suficientes, e claramente há.** O piso é
cinco candidaturas *resolvidas*, e uma candidatura só conta como resolvida
quando `outcome.stage_reached` está preenchido, ou quando foi enviada há mais de
30 dias sem resposta. Candidaturas paradas em `application.yaml` com resultado
vazio contam como em andamento, não como rejeições. `/slushpile:status` informa
quais registros estão incompletos.

**Uma rodada de revisão produz os mesmos achados da anterior.** Isso é o sinal,
não um defeito. Um problema apontado em mais de uma rodada é real; um problema
apontado uma vez só é ruído. Se nada mudou até a terceira rodada, as lacunas são
estruturais, e o pipeline deve dizer isso em vez de rodar uma quarta rodada.

**O pipeline não vai enviar a candidatura por você.** E nunca vai. Nenhuma
habilidade toca em um portal, em um e-mail ou em um formulário. Ele escreve
arquivos; você os lê e você os envia.
