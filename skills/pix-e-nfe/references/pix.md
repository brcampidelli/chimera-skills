# Pix — detalhes de integração

## Conceitos

- **Chave Pix:** CPF/CNPJ, e-mail, telefone ou chave aleatória. A empresa recebe numa chave da conta
  do PSP.
- **BR Code:** o payload do QR (padrão EMV) termina num CRC16; nunca edite o texto "copia e cola" à
  mão — gere pela API do PSP.
- **Cobrança imediata** vs **cobrança com vencimento** (com juros, multa, desconto): escolha pela
  natureza do pedido.
- **txid:** identificador da cobrança escolhido por você (ou pelo PSP), único; regras de tamanho e
  caracteres seguem a especificação da API Pix do BCB e do PSP — confira antes de gerar.
- **endToEndId:** identificador da transação liquidada; chave natural para idempotência.
- **Pix Automático** (recorrência autorizada pelo pagador) existe para assinaturas; verifique se o seu
  PSP oferece e quais as regras de autorização.

## Máquina de estados do pedido

```
criado → cobranca_gerada → pago → (faturado) → concluído
                       ↘ expirado
pago → devolvido_parcial | devolvido
```

Transições só no servidor. `pago` exige: assinatura/autenticação do webhook válida, valor recebido
igual ao esperado e `txid` pertencente ao pedido.

## Conciliação diária

- [ ] todo pagamento do extrato do PSP casa com um pedido (por `txid`/`endToEndId`)
- [ ] nenhum pedido "pago" sem pagamento correspondente
- [ ] valores iguais (centavos inteiros, nunca float)
- [ ] devoluções refletidas nos dois lados
- [ ] diferenças viram tarefa para uma pessoa, não ajuste automático

## Fraude e golpes

Pagamento contestado pode passar pelo Mecanismo Especial de Devolução (MED) do Banco Central; mantenha
evidências de entrega. Nunca libere pedido de alto valor só com comprovante enviado por imagem.
