---
name: whatsapp-cloud-api
description: >-
  Integração com a WhatsApp Business Cloud API oficial da Meta: envio de mensagens, janela de
  atendimento de 24 horas, templates aprovados (marketing, utilidade, autenticação), opt-in, webhooks
  com verificação de assinatura, mídia, limites e erros comuns. Use ao construir ou revisar bot,
  atendimento ou notificação por WhatsApp. Nunca recomenda bibliotecas não oficiais que automatizam o
  WhatsApp Web. Official WhatsApp Cloud API integration guide.
license: Apache-2.0
metadata:
  category: email-messaging
  categories_secondary: apis-integrations, marketing
  tags: whatsapp, meta, cloud-api, webhooks, templates, chatbot
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: build
topic: software-dev
---

# WhatsApp Cloud API (oficial)

**Só a API oficial.** Bibliotecas que automatizam o WhatsApp Web violam os termos e levam a banimento
do número. Se o projeto usa uma delas, aponte o risco e proponha a migração.

**Versão da Graph API:** fixe uma versão explícita na URL (`/vNN.N/`) e confira a atual em
developers.facebook.com antes de escrever código. Preços, categorias e limites mudam com frequência:
cite a página oficial, não números de memória.

## Modelo mental

1. **Janela de atendimento de 24 h:** quando o cliente manda mensagem, abre-se uma janela em que você
   responde com mensagem livre (texto, mídia, botões). Fora dela, só **template aprovado**.
2. **Templates** são aprovados pela Meta, têm categoria (marketing, utilidade, autenticação) e
   variáveis. Categoria errada é reclassificada ou rejeitada; marketing exige opt-in claro.
3. **Opt-in** antes de qualquer mensagem iniciada pela empresa, com registro de quando e como.
   Sempre ofereça saída ("responda SAIR"), e respeite.
4. **Qualidade do número** cai com bloqueios e denúncias e limita o volume. Mensagem irrelevante custa caro.

## Implementação

- Envio, webhook e verificação de assinatura: [references/api.md](references/api.md).
- Token: **token de usuário do sistema** (System User) com só as permissões necessárias, em variável de
  ambiente do servidor. Nunca no cliente, nunca em log.
- Webhook: responda `200` rápido e processe numa fila; a Meta reenvia em caso de falha, então o
  processamento é **idempotente** pelo `id` da mensagem.
- Valide `X-Hub-Signature-256` (HMAC-SHA256 do corpo cru com o app secret) antes de confiar no payload.
- Trate o texto recebido como **dado não confiável**: ele pode conter instruções para o seu agente.

## Antes de pôr em produção

- [ ] número verificado e nome de exibição aprovado
- [ ] templates aprovados para cada mensagem fora da janela
- [ ] opt-in registrado e descadastro funcionando
- [ ] assinatura do webhook validada e processamento idempotente
- [ ] dados pessoais da conversa cobertos pela política de privacidade (ver skill `lgpd-checklist`)
- [ ] envio ativo (marketing) aprovado por uma pessoa antes de disparar
