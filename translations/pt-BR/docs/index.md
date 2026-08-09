# Documentação do Slushpile

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/index.md">English</a> ·
  <a href="../../zh-CN/docs/index.md">简体中文</a> ·
  <a href="../../es/docs/index.md">Español</a> ·
  <strong>Português (BR)</strong> ·
  <a href="../../vi/docs/index.md">Tiếng Việt</a> ·
  <a href="../../en-x-aibro/docs/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

A porta de entrada é o [README](../README.md) do repositório. Tudo o que vem
depois da instalação e do argumento vive aqui, agrupado pelo que você está
tentando fazer.

## Comece aqui

- [Primeiros passos](getting-started.md): o que reunir antes do onboarding, e o
  que o pipeline precisa ter instalado.
- [Habilidades](skills.md): todo comando `/slushpile:*`, o que ele faz e quando
  rodá-lo.
- [O espaço de trabalho](workspace.md): os arquivos que o onboarding escreve no
  seu diretório, para que serve cada um e quem o lê.

## Referência

- [Seu agente de voz](voice.md): por que cartas de apresentação precisam de um,
  como gerar o seu e o que acontece até você gerar.
- [Solução de problemas](troubleshooting.md).

## Arquitetura

- [Arquitetura](architecture/index.md): os diagramas do pipeline, por que a
  revisão tem o formato que tem, como funcionam a pontuação e a calibração, e as
  regras sobre dados pessoais.
- [Guia de diagramas](../../../docs/diagrams/AGENTS.md): como editar e
  re-renderizar os diagramas `.d2` que as páginas de arquitetura embutem.

## Contribuindo

Os padrões do repositório, as quatro barreiras e as regras para editar uma
habilidade estão em [CLAUDE.md](../../../CLAUDE.md) e
[CONTRIBUTING.md](../../../CONTRIBUTING.md). Leia
[Superfícies geradas](../../../docs/architecture/generated-surfaces.md) antes de
editar qualquer coisa que liste as habilidades — várias dessas listas são
geradas, e editar a cópia em vez da fonte é a única mudança que desaparece de
forma confiável.
