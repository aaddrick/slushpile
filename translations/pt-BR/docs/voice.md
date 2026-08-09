# Seu agente de voz

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/voice.md">English</a> ·
  <a href="../../zh-CN/docs/voice.md">简体中文</a> ·
  <a href="../../es/docs/voice.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../vi/docs/voice.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/voice.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Um oitavo agente escreve a carta de apresentação, e ele escreve no estilo de uma
pessoa específica, construído a partir de um corpus de textos escritos por ela.

Essa é a única parte deste pipeline que você tem que trazer por conta própria.

## Por que um agente separado

A carta de apresentação é o único documento de uma candidatura que deveria soar
como uma pessoa. Um modelo escrevendo "na sua voz" a partir de um currículo
produz o registro padrão do modelo com os seus fatos dentro: competente,
uniforme e reconhecível como tal pelo sexagésimo primeiro leitor do dia.

Por isso a voz não é uma instrução de prompt. É uma definição de agente gerada a
partir de vários milhares de palavras da sua prosa real, medida em um conjunto
de dimensões estilísticas, com alvos numéricos contra os quais uma passada
posterior pode conferir.

## Gerando o seu

[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
é um pipeline separado que você roda uma vez. Ele analisa um corpus dos seus
textos em 25 dimensões e produz um agente de voz, uma habilidade de voz e um
perfil numérico com alvos mensuráveis.

Juntar o corpus é a parte lenta, então comece antes de precisar dele.

**Boas fontes:** posts de fórum e do Reddit, posts de blog, mensagens longas no
Slack, e-mails para colegas, descrições de pull request, documentação que você
escreveu sozinho. Uma exportação de dados do Reddit ou do Twitter funciona
direto.

**Fontes ruins:** qualquer coisa escrita a quatro mãos, qualquer coisa editada
por outra pessoa, qualquer coisa que já passou por um LLM, qualquer coisa em voz
institucional. Texto de marketing e avaliação de desempenho são os dois piores:
ambos são escritos em um registro que ninguém usa por vontade própria.

Alguns milhares de palavras é o piso. Abaixo disso a saída soa genérica, que é o
modo de falha mais difícil de notar porque ela parece pronta.

## Apontando o slushpile para ele

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`voice.agent` nomeia o agente pelo nome e nada o fixa no código, que é o que
deixa você trocar pelo seu sem editar o plugin.

## Até lá

`aaddrick-voice` vem junto como exemplo funcional para o pipeline rodar de
fábrica. É a voz do autor do plugin, não a sua. Cartas escritas com ele vão soar
como um estranho específico: serve para ver o pipeline funcionando, e está
errado para qualquer coisa que você realmente envie.

Enquanto `is_mine` for false, toda habilidade que redige texto avisa você antes
de rodar. Esse aviso é a única coisa entre você e doze candidaturas enviadas na
voz de um estranho, então não o silencie marcando a flag como true antes de o
agente ser de fato seu.

## Como a voz é usada, e defendida

`/slushpile:removing-ai-tells` passa a carta por instâncias novas do agente de
voz, com a habilidade orquestradora atuando como filtro em cada mudança
individual. Uma passada que aceitasse toda sugestão lixaria a carta de volta na
direção da média, que é exatamente o que o agente de voz existe para impedir.

O leitor cansado da revisão é conferido contra o seu agente de voz pela mesma
razão. Um hábito distintivo documentado ali não vira defeito porque um revisor o
apontou, e remover esse hábito é exatamente como uma carta escorrega de volta
para o genérico.

Note que um agente de voz é, por construção, a identidade de uma pessoa: gerado
a partir dos textos dela, batizado com o nome dela, e seus exemplos são frases
reais dela. É por isso que ele é o único agente deste repositório isento das
regras de dados pessoais que prendem todo o resto, e é por isso que a isenção
termina nos dados de contato. Veja
[Agentes e modelos](architecture/agents-and-models.md).
