# Dados pessoais

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/personal-data.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/personal-data.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/personal-data.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../../vi/docs/architecture/personal-data.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/personal-data.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## A fronteira

O plugin é código público. O espaço de trabalho é o histórico profissional de uma
pessoa, seus números de remuneração e suas restrições. São coisas diferentes e
moram em diretórios diferentes, e quase toda regra desta página decorre dessa
única frase.

O `/slushpile:onboard` roda no diretório do próprio usuário, não no checkout do
plugin. Ele escreve `profile.md`, `preferences.yaml` e `stories.md` ali. O
onboarding diz claramente que o diretório deve ser um repositório **privado** ou
nenhum repositório, e ele não vai inicializar um nem adicionar um remoto: essa é
uma decisão a se tomar deliberadamente, não um efeito colateral de montar um
espaço de trabalho.

## Nada em `skills/` ou `agents/` pode embutir um fato sobre nenhum usuário

Nenhum piso de remuneração. Nenhuma tabela de aluguel por região metropolitana.
Nenhuma cidadania, nenhum status de credenciamento de segurança, nenhum
empregador nomeado como sendo do usuário, nenhuma história nomeada, nenhum “o
candidato está aberto a mudar de cidade”. Uma habilidade que precise de um desses
lê o dado de `preferences.yaml` em tempo de execução.

A falha que isso evita é específica e silenciosa. Um piso de remuneração embutido
não dá erro; ele descarta vagas, com cara de correto, por um motivo que o usuário
nunca escolheu e não consegue ver. Um “aberto a mudar de cidade” embutido também
não dá erro; ele produz doze candidaturas afirmando algo sobre alguém que pode
não ser verdade.

Exemplos ilustrativos que nomeiam empresas reais são aceitáveis, e úteis, porque
ensinam o padrão. *“A maioria dos candidatos a planejamento de capacidade vem de
um lado só”* como exemplo de uma tese dependente da empresa é ensino. *“O
candidato tem dez anos em sistemas de controle industrial”* é um vazamento.

Note que o segundo exemplo teve de ser parafraseado para aparecer nesta página. O
real nomeia um domínio que o `check_no_pii.py` casa, e este arquivo é um dos que
ele varre, o que é a barreira funcionando como pretendido, na página que a
documenta.

## A barreira

```bash
python3 scripts/check_no_pii.py
```

Ele varre `skills/`, `agents/`, `templates/` e `docs/` em busca dos padrões que
vazaram da última vez, cada um com a razão pela qual conta como vazamento:
identidade do autor, um empregador anterior declarado como sendo do usuário, uma
localização de residência embutida, uma linha de base de remuneração embutida,
uma cidadania ou um status de credenciamento de segurança declarados como fato,
uma credencial declarada como fato, dados de contato reais, e referências a
arquivos que existem apenas no repositório privado do qual este plugin foi
produtizado.

Os padrões são deliberadamente estreitos. Um padrão amplo que dispara em prosa
legítima é suprimido em uma semana, e uma checagem suprimida é pior do que
nenhuma checagem porque parece cobertura.

Um novo padrão de vazamento que passe pertence àquele script, não a um comentário
de revisão.

## A única isenção, e seu limite

Os agentes de voz são isentos dos padrões de **identidade**, e apenas desses. Um
agente de voz *é* a identidade de uma pessoa por construção: ele é gerado a
partir de um corpus da escrita dela, leva o nome dela, e seus exemplos few-shot
são frases reais dela. Arrancar a identidade destruiria o artefato.

Dados de contato são proibidos em todo lugar, agentes de voz inclusive. Um número
de telefone em um agente distribuído é um vazamento sob qualquer teoria.

A lista de isenções é por arquivo e por padrão, em `check_no_pii.VOICE_AGENTS`.
Há uma segunda lista, `ALLOWED`, para qualquer outra coisa, e ela está vazia de
propósito. Toda entrada nela seria um buraco, e um buraco nesta barreira é
invisível até que a candidatura de outra pessoa diga que ela está aberta a se
mudar para uma cidade que nunca viu.

## O pipeline nunca submete nada

Nenhuma habilidade toca um portal de candidatura, um e-mail ou um formulário.
Todo estágio escreve arquivos. O usuário os lê e os envia.

Isso é uma propriedade de privacidade antes de ser de segurança: um pipeline que
submete é um pipeline que precisa guardar credenciais, e não há neste desenho
lugar para colocá-las que não seja a máquina do próprio usuário fazendo algo que
ele não viu.
