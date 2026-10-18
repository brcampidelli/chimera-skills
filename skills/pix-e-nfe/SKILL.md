---
name: pix-e-nfe
description: >-
  Notas de engenharia para cobrar com Pix e emitir documento fiscal no Brasil: Pix via PSP (QR
  dinâmico, txid, webhook, conciliação, devolução), e qual documento fiscal emitir (NF-e, NFC-e ou
  NFS-e), por meio de um emissor homologado, com ambientes de homologação e produção, cancelamento e
  guarda do XML. Use ao integrar checkout com Pix, conciliar pagamentos ou planejar emissão de nota em
  e-commerce ou SaaS. Não é consultoria contábil ou tributária.
license: Apache-2.0
metadata:
  category: finance-payments
  categories_secondary: apis-integrations, operations
  tags: pix, nf-e, nfs-e, nfc-e, pagamentos, fiscal, brasil
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: build
topic: software-dev
---

# Pix e nota fiscal — notas de engenharia

> Não substitui contador. Regras fiscais variam por estado, município e regime tributário, e a reforma
> tributária (IBS/CBS) está mudando os leiautes por etapas. Confirme com o contador e com a
> documentação do emissor antes de ir para produção, e marque o que não foi confirmado.

## Pix

1. **Integre por um PSP** (banco ou intermediador com API Pix: Mercado Pago, Stripe no Brasil, bancos
   com API de cobrança). Não monte a infraestrutura do Banco Central na mão.
2. **Cobrança dinâmica por pedido** (QR dinâmico / "copia e cola" com `txid` único por cobrança).
   QR estático serve para doação e valor livre, não para conciliar pedido.
3. **A verdade vem do servidor:** o pedido só vira "pago" com o **webhook do PSP** validado *e/ou*
   consulta da cobrança pela API. Tela do cliente dizendo "paguei" não conta.
4. **Idempotência:** o webhook pode chegar repetido ou fora de ordem; use o identificador fim a fim
   (`endToEndId`) e o `txid` para não dar baixa duas vezes.
5. **Expiração:** cobrança tem validade; pedido não pago expira e libera estoque.
6. **Devolução:** feita pela API do PSP referenciando o pagamento original; registre motivo e valor.
7. **Segurança:** credenciais e certificados do PSP (muitos exigem mTLS) só no servidor; webhook
   autenticado conforme o PSP.

Detalhes e checklist de conciliação: [references/pix.md](references/pix.md).

## Qual documento fiscal

| Situação | Documento | Esfera |
|---|---|---|
| Venda de mercadoria (B2B ou B2C, com transporte) | NF-e (modelo 55) | estadual (ICMS) |
| Venda de mercadoria ao consumidor no varejo presencial | NFC-e (modelo 65) | estadual |
| Prestação de serviço (SaaS, assinatura, curso online) | NFS-e | municipal / padrão nacional |

SaaS e plataforma de estudo **vendem serviço** → NFS-e, não NF-e. A classificação exata (código de
serviço, alíquota, retenções) é decisão do contador.

Fluxo de emissão e cuidados: [references/nota-fiscal.md](references/nota-fiscal.md).
