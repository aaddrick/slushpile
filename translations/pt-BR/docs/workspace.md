# O workspace

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/workspace.md">English</a> ·
  <a href="../../zh-CN/docs/workspace.md">简体中文</a> ·
  <a href="../../es/docs/workspace.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../vi/docs/workspace.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:onboard` roda no **seu** diretório, não no checkout do plugin, e
tudo o que o pipeline sabe sobre você mora ali.

Esse diretório vai conter seu histórico completo de emprego, seus números de
remuneração e suas restrições. Mantenha-o em um repositório **privado**, ou em
repositório nenhum. O onboarding vai dizer isso a você e não vai inicializar um
repositório por você, nem adicionar um remoto: essa é uma decisão para se tomar
de propósito, não para herdar de um passo de configuração.

## O que o onboarding escreve

```
profile.md          every factual claim about you
preferences.yaml    compensation, location, constraints, calibration priors
stories.md          four to eight tellable stories, with the numbers attached
job_search.md       the tracker: applications, outcomes, calibration
companies.md        one line per company ever looked at
applications/       one folder per role, created by job-board-search
```

### `profile.md`

**Não é um currículo.** É o material de onde um currículo é recortado: várias
vezes mais longo do que qualquer coisa que você mandaria, porque um currículo é
uma seleção e isto é aquilo de onde se seleciona.

Todo número ali carrega uma linha de base ou está explicitamente marcado como
dispensando uma. "Cortei a latência em 40%" é inútil até o leitor saber 40% de
quê, e um número sem origem é justamente aquele sobre o qual você vai ser
perguntado em uma entrevista e não vai saber responder. Números cuja fonte não
foi verificada são marcados como `UNVERIFIED` em vez de descartados.

Ele cresce. Quando uma revisão diz que uma seção está rala,
`/slushpile:explore-experience` entrevista você e escreve aqui o que encontrar,
para que a próxima candidatura já parta disso.

### `preferences.yaml`

A metade legível por máquina. Método e linha de base de remuneração, restrições
de localização e de mudança, situação de credenciamento de segurança e de
diploma, os diferenciais que você reivindica, seu agente de voz e
`calibration_priors`.

Dois campos trabalham mais que todos os outros:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

Enquanto `is_mine` for false, toda habilidade que redige texto avisa você antes
de rodar. Veja [Seu agente de voz](voice.md).

`calibration_priors` começa vazio e continua vazio até você ter cinco ou mais
candidaturas resolvidas em um canal. Um prior vazio significa que os agentes
usam os padrões que vieram com o plugin e rotulam suas estimativas como não
calibradas, que é o comportamento correto: um prior calculado a partir de dois
resultados afasta a pontuação da realidade mais do que prior nenhum, e ainda
chega com cara de empírico.

### `stories.md`

De quatro a oito histórias que você consegue de fato contar, com os números
junto. O builder escolhe uma por candidatura; a entrevista que você acabar
conseguindo roda em cima delas.

### `job_search.md`

O rastreador, e a memória de longo prazo do pipeline. Candidaturas, seus
resultados, candidaturas anteriores por empresa, e uma seção `Calibration` que
`/slushpile:status` reescreve a partir dos seus próprios resultados.

O histórico de candidaturas anteriores em uma empresa é lido pelo analista do
pool de candidatos e pelo contrarian durante uma revisão. Uma rejeição anterior
em um nível **mais alto** pesa de verdade: o recrutador vê todo o histórico no
sistema de recrutamento, e uma candidatura posterior em um nível mais baixo é
lida como uma queda de vários níveis.

### `companies.md`

Uma linha por empresa que você já olhou, para que uma segunda busca na mesma
empresa comece do que a primeira encontrou.

## Pastas de vaga

`/slushpile:job-board-search` cria uma pasta por vaga que sobrevive à
classificação em níveis:

```
applications/<Company>/<Function>/<Role>/
  job_description.md    the posting, captured verbatim
  role_analysis.md      pool position, channel EV, kill criteria, contrarian notes
  application.yaml      the record: verdicts, scores, channel used, outcome
  resume.tex            copied per role by the builder
  cover_letter.tex      copied per role by the builder
```

O anúncio é guardado **na íntegra**, não resumido. 3 agentes leem esse texto
diretamente durante uma revisão, e uma paráfrase remove em silêncio a redação
exata dos requisitos que eles existem para conferir.

`application.yaml` é o arquivo que `/slushpile:status` lê para montar a fila e
para regredir as previsões contra os resultados. É também o arquivo a atualizar
quando algo acontece: uma rejeição, uma triagem, uma entrevista, uma proposta.
Nada mais no pipeline consegue ficar sabendo, porque o pipeline nunca envia nada
e nunca vê uma resposta.

Os templates são copiados **para dentro de cada pasta de vaga** em vez de
ficarem na raiz do workspace. Uma cópia intocada na raiz vira uma cópia
desatualizada no instante em que a primeira candidatura diverge dela.

## O que o plugin nunca guarda

Nada em `skills/` ou `agents/` fixa no código um fato sobre você. Nenhum piso de
remuneração, nenhuma localização, nenhuma situação de credenciamento de
segurança, nenhum empregador. Uma habilidade que precise de um desses lê o valor
de `preferences.yaml` em tempo de execução, e um gate de CI quebra o build se um
dado pessoal vazar para dentro do plugin.

É isso que torna o workspace portátil e o plugin atualizável: você pode
reinstalar, forkar ou atualizar o slushpile sem tocar em nada que seja sobre
você. Veja [Dados pessoais](architecture/personal-data.md).
