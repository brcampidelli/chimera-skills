---
name: chimera-skill-authoring
description: >-
  Escrever uma skill no formato SKILL.md que o Chimera lê e que outros agentes também aceitam:
  frontmatter (name, description, license, metadata, stage, topic), divulgação progressiva (metadados,
  instruções, referências), corpo no formato cartão (Trigger, Do, Avoid, Check, Risk), regras de
  segurança deste catálogo e o que acontece na importação (pendente e não confiável). Use ao criar,
  revisar ou portar uma skill para o Chimera ou para o repositório chimera-skills.
license: Apache-2.0
metadata:
  category: ai-models-agents
  categories_secondary: reference-docs
  tags: skills, skill-md, chimera, agentes, progressive-disclosure
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: build
topic: ai-agents
---

# Como escrever uma skill para o Chimera

## Estrutura

```
skills/<id>/
├── SKILL.md          # frontmatter + instruções curtas (até ~100 linhas; o CI corta em 500)
└── references/       # detalhe, carregado só quando a instrução manda ler
```

Sem `scripts/`: código de exemplo vai dentro do markdown, para o agente escrever e executar sob a
governança do Chimera. Arquivo executável num pacote de skill é o que o CI deste catálogo recusa.

## Frontmatter

| Campo | Regra |
|---|---|
| `name` | igual ao nome da pasta, kebab-case, até 64 caracteres |
| `description` | até 1024 caracteres: **o que faz + "Use quando…"**. É o que a busca lê para decidir relevância |
| `license` | SPDX; conteúdo próprio = `Apache-2.0` |
| `metadata` | `category` (uma das 26 de `categories.yaml`), `categories_secondary` (até 3), `tags`, `mode` (`own`/`include`/`adapt`) |
| `stage` | `define`, `build`, `verify`, `review` ou `ship` |
| `topic` | um dos tópicos do Chimera (`software-dev`, `ai-agents`, `research`, `devops`, `security`, `data-science`, `productivity`, `mlops`, `networking`, `vision-ai`, `translation`) |

Campos desconhecidos são ignorados pelo leitor do Chimera; valores fora do vocabulário em
`stage`/`topic` viram vazio. `provenance` e `status` escritos no arquivo **não valem**: a importação
marca toda skill de fora como `tainted` e `pending` até uma pessoa aprovar.

## Corpo

Divulgação progressiva: o agente vê primeiro só nome e descrição; o corpo carrega quando a skill é
escolhida; as referências, só quando o corpo mandar. Então:
- o corpo diz **o procedimento** e aponta para `references/` com link relativo;
- tabelas e listas curtas no corpo, exemplos longos nas referências;
- seções `## Trigger`, `## Do`, `## Avoid`, `## Check`, `## Risk` são lidas pelo importador do
  Chimera como os campos do cartão (opcional, mas recomendado para skills curtas).

## Regras de segurança do catálogo

- Gatilho descreve **quando** a skill serve; nunca exige ser usada em todo turno ou antes de qualquer
  resposta, nem proíbe o agente de usar outras ferramentas.
- Nada de instalar pacote sem versão, instalar globalmente, pedir privilégio de administrador ou
  baixar e executar código da rede numa linha só.
- Nenhuma frase dirigida a quem revisa ou ao agente para pular revisão, esconder algo do usuário ou
  desconsiderar instruções anteriores.
- Ação que mexe com dinheiro, produção, dados de terceiros ou acesso fica com aprovação humana, e a
  skill diz isso explicitamente.
- Número que importa (dinheiro, risco, métrica) sai de código determinístico, não de cálculo do modelo.

## Antes de abrir o PR

`python scripts/check.py` passa; `catalog/<id>.json` e `reviews/<id>.md` existem; a revisão registra o
`Content sha256` impresso por `python scripts/check.py --print-tree-hash skills/<id>`.
