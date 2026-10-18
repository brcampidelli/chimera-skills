# Emissão de nota fiscal — fluxo e cuidados

## Use um emissor homologado

Assinar XML com certificado digital, falar com cada SEFAZ e com cada prefeitura (ou com o padrão
nacional da NFS-e) é trabalho de um serviço especializado. Integre por API de um emissor (há vários no
mercado) e deixe o certificado digital (A1) guardado nele ou num cofre de segredos — nunca no
repositório.

## Fluxo

1. Pagamento confirmado (ver `pix.md`) → evento "faturar pedido".
2. Monte os dados fiscais a partir do cadastro: tomador (CPF/CNPJ, endereço quando exigido), itens ou
   serviço, valores, códigos fiscais definidos pelo contador.
3. Envie ao emissor **em homologação** até passar em todos os cenários; só então troque para produção
   (são ambientes e credenciais diferentes).
4. Trate a resposta assíncrona: autorizada, rejeitada (com código e motivo) ou em processamento.
5. Guarde **XML autorizado e PDF (DANFE/DANFSe)**, número, série, chave e protocolo.
6. Envie ao cliente por e-mail.

## Cuidados

- **Rejeição** tem código: registre e mostre a uma pessoa; não reenvie em laço.
- **Cancelamento** tem prazo legal curto e regras por documento; depois dele, só por outros
  instrumentos. Confirme o prazo vigente para o seu caso.
- **Carta de correção** corrige alguns campos da NF-e, nunca valores nem destinatário.
- **Guarda:** mantenha os XMLs pelo prazo legal (anos, não meses), com backup.
- **Idempotência:** um pedido gera no máximo uma nota; use o id do pedido como referência externa no emissor.
- **Reforma tributária:** campos de IBS/CBS entram nos leiautes por fases; acompanhe as notas técnicas
  pelo emissor e não fixe alíquota no código.
