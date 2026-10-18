---
name: meta-ads-basics
description: >-
  Fundamentos de Meta Ads (Facebook/Instagram) para ler e diagnosticar campanhas: estrutura
  campanha/conjunto/anúncio, objetivos, fase de aprendizado, métricas que importam (CPA, ROAS, CTR,
  CPM, frequência), atribuição, Pixel + Conversions API com deduplicação, e relatório pela Marketing
  API em modo somente leitura. Use ao analisar desempenho de anúncios, montar relatório ou revisar
  rastreamento. Mudanças de verba ou criação de anúncio ficam com uma pessoa.
license: Apache-2.0
metadata:
  category: marketing
  categories_secondary: apis-integrations
  tags: meta-ads, facebook-ads, instagram, marketing-api, capi, pixel
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: review
topic: data-science
---

# Meta Ads — fundamentos e leitura

**Modo padrão: leitura.** Esta skill lê e explica. Pausar, criar, mudar verba ou público mexe com
dinheiro: proponha a mudança com o motivo e deixe a pessoa executar ou aprovar.

## Estrutura

- **Campanha:** objetivo (vendas, leads, tráfego, engajamento, reconhecimento, app). O objetivo
  define o que o algoritmo otimiza; escolher "tráfego" para vender é o erro mais comum.
- **Conjunto de anúncios:** público, posicionamentos, orçamento (se não for orçamento de campanha),
  evento de otimização.
- **Anúncio:** criativo e texto.

## Leitura de desempenho

1. **Comece pelo resultado de negócio** (CPA ou ROAS do evento certo), não por CTR.
2. **Janela e atribuição:** compare períodos com a mesma configuração de atribuição; números da Meta e
   do seu backend nunca batem exatamente — explique a diferença, não a esconda.
3. **Fase de aprendizado:** conjunto com poucos eventos de otimização por semana fica instável.
   Mudanças grandes (orçamento, público, criativo, evento) reiniciam o aprendizado; agrupe mudanças.
4. **Fadiga:** frequência subindo + CTR caindo + CPM subindo no mesmo público = criativo cansado.
5. **Amostra:** com poucas conversões, diferenças entre anúncios são ruído. Diga o n ao lado de cada
   comparação e não declare vencedor com dezenas de eventos.

## Rastreamento

- **Pixel + Conversions API (CAPI)** juntos, com o mesmo `event_id` nos dois para deduplicar.
- Envie dados do cliente com hash (SHA-256) conforme a documentação, e só com base legal e aviso de
  privacidade (ver `lgpd-checklist`).
- Verifique o domínio e priorize os eventos no Gerenciador de Eventos.

## Relatório pela API

Consulta de insights, campos e cuidados em [references/insights.md](references/insights.md).
Token de **usuário do sistema** com permissão de leitura (`ads_read`); permissão de gestão só se a
pessoa pedir, e nunca usada sem aprovação a cada mudança.

## Categorias especiais

Anúncios de crédito, emprego, moradia e temas sociais/eleitorais têm regras e segmentação restritas.
Identifique antes de sugerir público.
