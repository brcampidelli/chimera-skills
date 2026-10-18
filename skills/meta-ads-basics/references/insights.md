# Marketing API — insights (somente leitura)

Fixe a versão da Graph API (`vNN.N`) e confira os campos na documentação dessa versão.

```http
GET https://graph.facebook.com/vNN.N/act_{AD_ACCOUNT_ID}/insights
  ?level=campaign
  &date_preset=last_7d
  &fields=campaign_name,spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,actions,cost_per_action_type,purchase_roas
  &time_increment=1
Authorization: Bearer {TOKEN}
```

- `level`: `account`, `campaign`, `adset`, `ad`.
- `actions` e `cost_per_action_type` vêm como listas de `{action_type, value}`; filtre pelo evento de
  otimização (por exemplo `purchase`, `lead`, `offsite_conversion.fb_pixel_purchase`).
- `breakdowns` (idade, gênero, posicionamento) multiplicam linhas e podem esconder métricas; peça
  um de cada vez.
- Contas grandes: use relatório assíncrono (`/insights` com `POST` gera um job) e pagine por `paging.next`.
- Respeite o rate limit da conta (cabeçalhos de uso na resposta); em erro de limite, espere e reduza o lote.

## Contas que devem bater

| Métrica | Fórmula |
|---|---|
| CTR | cliques / impressões |
| CPC | gasto / cliques |
| CPM | gasto / impressões × 1000 |
| CPA | gasto / conversões do evento |
| ROAS | receita atribuída / gasto |
| Frequência | impressões / alcance |

Calcule as contas com código a partir dos números brutos e confira com o que a API devolve;
divergência indica filtro de evento ou atribuição diferente.

## Formato sugerido do relatório

1. Resumo em 3 linhas (o que mudou e por quê, com n).
2. Tabela por campanha: gasto, conversões, CPA, ROAS, frequência, variação contra o período anterior.
3. Hipóteses marcadas como hipóteses, com o dado que confirmaria cada uma.
4. Ações propostas, cada uma com custo e risco, aguardando aprovação.
