---
name: trading-risk-rules
description: >-
  Regras de gestão de risco para revisar um plano de operação ANTES de qualquer ordem: no máximo 2% do
  patrimônio em risco por operação, no máximo 5% de perda no dia, stop loss sempre definido, e parada
  após 3 perdas seguidas. Calcula o tamanho da posição por código determinístico e devolve APROVADO ou
  BLOQUEADO com o motivo. Use ao planejar, revisar ou registrar uma operação, ou ao montar um diário de
  trades. Orientação, não execução: esta skill nunca envia ordens e não é recomendação de investimento.
license: Apache-2.0
metadata:
  category: finance-payments
  categories_secondary: operations
  tags: trading, risco, position-sizing, stop-loss, diario-de-trades
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: verify
topic: data-science
---

# Regras de risco em trading (orientação)

**Esta skill não opera.** Não envia, altera nem cancela ordens, não acessa corretora e não diz o que
comprar ou vender. Ela verifica se um plano **já decidido pela pessoa** cabe nas regras, e explica por
quê. Não é recomendação de investimento.

## As quatro regras (invioláveis)

| # | Regra | Bloqueia quando |
|---|---|---|
| 1 | Risco por operação ≤ **2%** do patrimônio | `perda_se_stop > 0,02 × patrimônio` |
| 2 | Perda do dia ≤ **5%** do patrimônio de abertura do dia | `perda_realizada_hoje + risco_desta_operação > 0,05 × patrimônio_abertura` |
| 3 | **Stop loss sempre**, definido antes da entrada | plano sem preço de stop, ou stop do lado errado |
| 4 | **3 perdas seguidas = parar** pelo resto do dia e revisar | as três últimas operações encerradas foram perdas |

Uma regra violada = **BLOQUEADO**. Não existe "só desta vez", nem arredondar para caber.

## Números só por código

Modelos de linguagem erram aritmética e trocam casas decimais. Todo número desta skill (tamanho de
posição, perda potencial, soma do dia) sai de **código determinístico** executado sobre os dados de
entrada, e o resultado é mostrado com as contas. Nunca estime de cabeça. Fórmulas e um exemplo em
[references/calculo.md](references/calculo.md).

## Procedimento

1. Peça (ou leia do diário) os dados: patrimônio atual, patrimônio na abertura do dia, perda realizada
   hoje, resultado das últimas operações, ativo, direção, preço de entrada, preço de stop, valor por
   ponto/tick e lote mínimo.
2. Se faltar o stop, **pare**: regra 3.
3. Calcule por código o tamanho máximo pela regra 1 e o risco somado do dia pela regra 2.
4. Verifique a regra 4 no histórico.
5. Responda no formato abaixo.

```
RESULTADO: APROVADO | BLOQUEADO
Regra 1 (2%/op):   risco R$ X de limite R$ Y — ok/violada
Regra 2 (5%/dia):  R$ X de limite R$ Y — ok/violada
Regra 3 (stop):    stop em P (lado correto) — ok/violada
Regra 4 (3 perdas): sequência atual N — ok/violada
Tamanho máximo permitido: Q contratos/ações (contas abaixo)
```

## Não faça

- Não sugira afrouxar o stop para "dar espaço" depois da entrada.
- Não some lucros do dia para liberar risco além de 5% do patrimônio de abertura.
- Não trate a sequência de perdas como zerada por uma operação aberta ainda sem resultado.
