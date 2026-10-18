# WhatsApp Cloud API — referência rápida

Troque `vNN.N` pela versão fixada no projeto e confira os campos na documentação oficial da versão.

## Enviar texto (dentro da janela de 24 h)

```http
POST https://graph.facebook.com/vNN.N/{PHONE_NUMBER_ID}/messages
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "text",
  "text": { "body": "Olá! Seu pedido saiu para entrega." }
}
```

## Enviar template (fora da janela)

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "pedido_enviado",
    "language": { "code": "pt_BR" },
    "components": [
      { "type": "body", "parameters": [ { "type": "text", "text": "#1234" } ] }
    ]
  }
}
```

## Webhook

**Verificação (GET)** — a Meta chama com `hub.mode=subscribe`, `hub.verify_token` e `hub.challenge`.
Se o token bater com o seu, responda o `hub.challenge` com status 200.

**Eventos (POST)** — mensagens recebidas e status (`sent`, `delivered`, `read`, `failed`) chegam em
`entry[].changes[].value`. Mensagens em `value.messages[]`, status em `value.statuses[]`.

### Validar a assinatura (TypeScript, Route Handler)

```ts
import { createHmac, timingSafeEqual } from "node:crypto";

export async function POST(req: Request) {
  const raw = await req.text(); // corpo CRU: não reserializar o JSON
  const header = req.headers.get("x-hub-signature-256") ?? "";
  const expected = "sha256=" + createHmac("sha256", process.env.META_APP_SECRET ?? "").update(raw).digest("hex");
  const ok = header.length === expected.length && timingSafeEqual(Buffer.from(header), Buffer.from(expected));
  if (!ok) return new Response("invalid signature", { status: 401 });
  await enqueue(JSON.parse(raw)); // processar fora da requisição, idempotente por message.id
  return new Response("ok", { status: 200 });
}
```

## Erros que aparecem cedo

| Sintoma | Causa provável |
|---|---|
| Mensagem livre recusada | fora da janela de 24 h → use template |
| Template rejeitado | categoria errada, variável no começo/fim, conteúdo promocional em "utilidade" |
| Webhook não chega | app não inscrito no WABA, campo `messages` não assinado, URL sem HTTPS válido |
| Número com qualidade baixa | muitos bloqueios: revise frequência, relevância e opt-in |
| Limite de envio atingido | o número está num nível de limite de conversas por 24 h; cresce com qualidade e volume |

## Mídia

Envie por `link` (URL HTTPS pública) ou por `id` após upload em `/{PHONE_NUMBER_ID}/media`. Mídia
recebida chega como `id`; baixe pela Graph API com o token e trate como arquivo não confiável.
