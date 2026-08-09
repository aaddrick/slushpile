<p align="center">
  <img src="../../.github/assets/hero-pt-BR.png" alt="Slushpile: uma busca de emprego adversarial com memória. 7 agentes tentam rejeitar você antes que um recrutador consiga, e o que encontram, fica com você. O que fica com você: profile.md, cada afirmação factual; preferences.yaml, remuneração, localização e restrições; stories.md, de quatro a oito histórias contáveis; job_search.md, resultados para calibração. Escrito uma vez, lido por toda etapa, atualizado por toda revisão. Os 7 revisores: triador, analista de requisitos, simulador de ATS, leitor cansado, analista do pool, gestor da vaga, contrarian. 5 revisores em paralelo, cegos uns aos outros, depois a síntese, depois um agente cuja função é derrubá-la." width="100%">
</p>

<p align="center">
  <strong>Slushpile</strong><br>
  <em>7 agentes tentam rejeitar você antes que um recrutador tenha a chance.</em><br>
  <em>O que eles encontram, fica com você.</em>
</p>

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/aaddrick/slushpile?style=flat" alt="Licença"></a>
  <a href="../../.github/workflows/plugin-load-check.yml"><img src="https://img.shields.io/github/actions/workflow/status/aaddrick/slushpile/plugin-load-check.yml?label=plugin%20loads&style=flat" alt="Verificação de carregamento do plugin"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/aaddrick/">Conecte-se no LinkedIn!</a>
</p>

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../README.md">English</a> ·
  <a href="../zh-CN/README.md">简体中文</a> ·
  <a href="../es/README.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../vi/README.md">Tiếng Việt</a> ·
  <a href="../en-x-aibro/README.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

<!-- BEGIN GENERATED market-note: scripts/sync_docs.py -->

> **Escopo**: este pipeline modela convenções de contratação anglófonas, principalmente dos EUA: uma página, sem foto, sem data de nascimento, ordem cronológica inversa e uma linha de autorização de trabalho. Se você se candidata em um mercado local com outras convenções, os conselhos de formatação não valem e a revisão vai apontar como defeito o que lá é normal. Acompanhe no [issue #2](https://github.com/aaddrick/slushpile/issues/2).

<!-- END GENERATED market-note -->

## Instalação

<details open>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add aaddrick/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Depois, no diretório onde você mantém sua busca de emprego:

```
/slushpile:onboard
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add aaddrick/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

O Codex prefixa as habilidades do plugin com o nome do plugin:

```
$slushpile:onboard
```

O Codex não despacha subagentes, então o pipeline de revisão roda seus 7
revisores em sequência num único contexto, em vez de 5 revisores em paralelo.
Mesma saída, mais lenta, e um pouco mais sujeita a que o raciocínio de uma
persona vaze para a próxima.

</details>

<details>
<summary><strong>Cursor, Gemini CLI e instalação manual</strong></summary>

Veja [INSTALL.md](./INSTALL.md).

</details>

## O problema

Você não está sendo avaliado contra a descrição da vaga. Você está sendo
avaliado contra as outras setenta pessoas que se candidataram à mesma vaga nesta
semana.

Quase toda ferramenta desse mercado inverte isso. Jogue um currículo e um
anúncio num otimizador de currículo e ele vai dizer que sua compatibilidade de
palavras-chave subiu de 68% para 91%, o que é um número real sobre a pergunta
errada. Se o candidato no percentil 75 daquela fila bate 94%, seus 91% são uma
rejeição, e nada na ferramenta vai te dizer isso.

A segunda coisa que erram: devolvem um veredito só. Mas o mesmo currículo e a
mesma carta convertem talvez 2% por um envio frio no portal e 30% por uma
indicação. Essas não são a mesma decisão, e colapsá-las num único "forte
compatibilidade" não é uma simplificação. É um erro com uma interface confiante
por cima.

A terceira é a que ninguém nomeia. Essas ferramentas não têm memória. Você cola
um currículo, recebe um número de volta, fecha a aba, e a ferramenta encerra a
sessão sabendo exatamente o que sabia no começo. Uma busca são quarenta
candidaturas em três meses. Cada uma delas custa o preço cheio.

## O que isto faz no lugar disso

**Ele constrói um modelo de você, uma vez.** `/slushpile:onboard` entrevista você
e escreve três arquivos: um perfil, um arquivo de preferências e um conjunto de
histórias. O perfil não é um currículo — é o material de onde um currículo é
recortado, várias vezes mais longo do que qualquer coisa que você enviaria. Toda
etapa posterior lê esse arquivo, e nada te pergunta aquilo duas vezes.

**Ele tenta te convencer a desistir da vaga antes de você escrever qualquer
coisa.** A etapa de busca pontua cada anúncio contra o pool estimado de
candidatos, roda os critérios de descarte, monta uma matriz de valor esperado
por canal de candidatura e coloca um contrarian na frente da lista de níveis.
Toda outra ferramenta começa a trabalhar depois que você já decidiu se
candidatar. O erro caro acontece antes disso, e esta é a única etapa que ainda
consegue pegá-lo de graça.

**Ele ataca o que acabou de escrever.** Um modelo a quem se pergunta se o próprio
rascunho é bom vai dizer que sim, longamente. Então o construtor não pergunta.
Ele entrega o currículo e a carta a 7 revisores, cada um recebendo apenas o que
o seu papel teria de verdade — o triador de onze segundos nunca vê a carta de
apresentação, porque um triador que leu a carta não é um triador. São 5
revisores em paralelo, cegos aos achados uns dos outros. O construtor corrige o
que volta e manda tudo de novo. A segunda rodada tem que se sustentar antes de
ele deixar você enviar, e ele para em três rodadas, porque depois disso as
lacunas são estruturais e mais edição é só movimento.

**Ele escreve de volta em você o que aprende.** Quando uma revisão diz que uma
seção está fraca, a entrevista que vem em seguida quase sempre descobre que a
experiência era real e você nunca a escreveu. Isso entra no perfil em
definitivo. As estimativas de conversão são corrigidas contra os resultados que
você registra. Sua vigésima candidatura começa de um lugar melhor que a
primeira, o que em qualquer outra ferramenta simplesmente não é verdade.

O que sai é um veredito por canal — envio frio, indicação quente, contato frio,
procura espontânea a partir do seu trabalho público — cada um com uma faixa de
probabilidade em vez de uma palavra de veredito, e com a qualidade do material
pontuada separadamente do valor esperado. "1-3% de entrevista" é informação.
"MAYBE" não é. Material excelente enviado para uma vaga de encaixe errado
continua tendo valor esperado baixo, e esses dois números discordam com
frequência.

## O que muda

Mesmo currículo, mesmo anúncio, mesma tarde.

### O que um otimizador de currículo te diz

> **Pontuação de compatibilidade: 91%** ✅
>
> Ótimas notícias — seu currículo é altamente compatível com esta vaga!
>
> ✅ 14 de 16 palavras-chave obrigatórias encontradas
> ✅ Formatação amigável a ATS detectada
> ⚠️ Considere adicionar: "stakeholder alignment", "OKRs"
>
> Você está pronto para se candidatar!

### O que o Slushpile te diz

> **Posição no pool: p55.** O candidato mediano aqui já entregou em escala
> comparável numa empresa que o gestor da vaga reconhece. Seu trabalho
> open-source é real e não é raro neste pool — mais ou menos um terço da coorte
> p75 tem algo equivalente.
>
> **Envio frio: REJECT, 1-3%.** O campo de anos de experiência no formulário
> barra abaixo de 8. Você tem 6 na função com esse título.
>
> **Indicação quente: MAYBE, 20-30%.** Este é o único canal com um caminho real.
>
> **Qualidade do material: 8/10.** O material não é o problema.
>
> **Contrarian:** SUBMIT_AS_PORTFOLIO_ONLY. Enviar isto a frio gasta uma hora por
> uma chance de 2%. Duas horas atrás de uma indicação valem mais que dez
> candidaturas frias a mais.

Um destes é um número sobre o seu documento. O outro é uma decisão sobre a sua
tarde.

## O pipeline

<!-- BEGIN GENERATED pipeline: scripts/sync_docs.py -->

### The main pipeline

Three commands, in order. A search runs on these alone.

```
/slushpile:onboard              once per workspace — builds your profile,
                                preferences, and stories

/slushpile:job-board-search     search a careers board, extract postings,
                                score pool-anchored fit, contrarian gate,
                                create role folders

/slushpile:application-builder  build the resume and cover letter, then
                                iterate them against the review until they
                                stabilize
```

### The three it runs for you

`/slushpile:application-builder` dispatches all three of these itself, in the
course of building an application. Run one directly only to work on materials
this pipeline did not build — a resume written elsewhere, a letter drafted by
hand.

```
/slushpile:explore-experience   interview to surface experience you have
                                but never wrote down

/slushpile:adversarial-review   seven agents, five in parallel, verdict
                                per channel

/slushpile:removing-ai-tells    strip AI-authorship signals from prose,
                                with a gatekeeper on every change
```

### Any time

```
/slushpile:redesign-templates   restyle the resume and letter templates,
                                holding the ATS constraints fixed

/slushpile:status               the queue, what is waiting on you, and whether
                                the pipeline's predictions are holding up

/slushpile:help                 what to run next, and how to read the output
```

<!-- END GENERATED pipeline -->

<!-- BEGIN GENERATED reviewers: scripts/sync_docs.py -->

### The seven reviewers

| Agent | Simulates |
|---|---|
| **Triage screener** | 11 seconds, F-pattern, 347 resumes already read today |
| **Requirements analyst** | 30 seconds, methodical, checks every qualification against evidence |
| **ATS simulator** | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| **Fatigued reader** | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| **Pool analyst** | A recruiter who knows what the queue actually looks like |
| **Hiring manager** | The person who has to justify the interview slot to their skip-level |
| **Contrarian** | Whoever should have asked whether any of this was worth doing |

The first five run in parallel and cannot see each other's work. The hiring
manager sees all five. The contrarian sees everything, including the hiring
manager, and can overrule it.

<!-- END GENERATED reviewers -->

## O manual

O resto está em [docs/](docs/index.md):

- [Primeiros passos](docs/getting-started.md): o que reunir antes do onboarding,
  e o que instalar.
- [Habilidades](docs/skills.md): cada comando, e quando rodá-lo.
- [O espaço de trabalho](docs/workspace.md): os arquivos que isto escreve no seu
  diretório.
- [Seu agente de voz](docs/voice.md), [Solução de
  problemas](docs/troubleshooting.md).
- [Arquitetura](docs/architecture/index.md): os diagramas, por que a revisão tem
  essa forma, e como a pontuação e a calibração funcionam.

## Suas cartas de apresentação precisam da sua voz

Um oitavo agente escreve a carta de apresentação. Ele escreve no estilo de uma
pessoa específica, construído a partir de um corpus da escrita dela.

O slushpile já vem com **`aaddrick-voice`** como exemplo funcional, para o
pipeline rodar de cara. É a voz do autor do plugin, não a sua. Cartas escritas
com ele vão soar como um estranho específico — bom para ver o pipeline
funcionando, errado para qualquer coisa que você realmente envie.

Gere a sua com
**[written-voice-replication](https://github.com/aaddrick/written-voice-replication)**.
Ele analisa um corpus da sua escrita em 25 dimensões e produz um agente de voz,
uma habilidade de voz e um perfil numérico com metas mensuráveis.
`aaddrick-voice` é o exemplo trabalhado desse próprio pipeline.

Depois aponte o `preferences.yaml` para ele:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

Enquanto `is_mine` for falso, toda habilidade que redige texto avisa você antes
de rodar. Esse aviso é a única coisa entre você e doze candidaturas enviadas na
voz de um estranho.

## Seus dados continuam seus

`/slushpile:onboard` escreve três arquivos no *seu* diretório: `profile.md`,
`preferences.yaml` e `stories.md`. Todo dado pessoal que o pipeline usa mora
ali. Nada fica embutido no plugin, e o repositório tem uma barreira de CI que
falha se um dado pessoal vazar para dentro de uma habilidade.

Esse espaço de trabalho vai conter seu histórico completo de empregos, seus
números de remuneração e suas restrições. Mantenha-o em um repositório
**privado**, ou em repositório nenhum. A habilidade de onboarding vai te dizer
isso e não vai inicializar um repositório para você.

**O pipeline nunca envia nada.** Nenhuma habilidade toca um portal de
candidatura, um e-mail ou um formulário. Ele escreve arquivos. Você lê e você
envia.

## A honestidade é o recurso

Esta ferramenta vai te dizer que um diferencial do qual você se orgulha é
mediano. Vai te dizer que uma vaga que você quer tem 2% de taxa de conversão. De
vez em quando, vai te dizer para não se candidatar.

Esse é o produto. Um pipeline que classifica a maioria das candidaturas como
INTERVIEW e converte 5% delas não está produzindo sinal, está produzindo
otimismo, e vai continuar fazendo isso indefinidamente porque nada dentro dele
empurra de volta. A passada do contrarian, a ancoragem no pool e as
probabilidades por canal existem para tornar a saída útil justamente quando ela
diz não.

Existe uma tabela `Calibration` no rastreador do espaço de trabalho exatamente
por isso: você registra o que o pipeline previu e o que de fato aconteceu, e as
probabilidades a priori são corrigidas pelo seu próprio histórico, e não pela
confiança de ninguém.

## Ajuste

As 9 habilidades e os 8 agentes são Markdown. Faça um fork, edite, instale a sua
cópia:

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

```bash
claude plugin marketplace add <your-username>/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Se você mudar uma habilidade, rode as barreiras antes de dar push. Veja
[CONTRIBUTING.md](../../CONTRIBUTING.md).

## Licença

MIT. Veja [LICENSE](../../LICENSE).
