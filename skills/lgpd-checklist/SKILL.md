---
name: lgpd-checklist
description: >-
  Checklist prático de LGPD (Lei 13.709/2018) para produto digital: mapear dados pessoais, escolher a
  base legal, tratar dados sensíveis e de crianças, retenção e exclusão, direitos do titular, operadores
  e transferência internacional, incidentes e encarregado. Use ao desenhar uma feature que coleta dado
  pessoal, ao revisar política de privacidade, cadastro, analytics, pixel/cookies ou fornecedor novo.
  Brazilian data protection (LGPD) review. Não é parecer jurídico.
license: Apache-2.0
metadata:
  category: security
  categories_secondary: product, operations
  tags: lgpd, privacidade, dados-pessoais, anpd, compliance
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: define
topic: security
---

# Checklist de LGPD

> Orientação de engenharia e produto, não parecer jurídico. Normas da ANPD mudam: confira a versão
> vigente no site da ANPD antes de decidir algo com efeito legal e marque o que não foi conferido.

## Para cada feature que toca dado pessoal

1. **Mapeie** quais dados, de quem, para quê, onde ficam, quem acessa, por quanto tempo.
   Use o modelo de [references/mapeamento.md](references/mapeamento.md).
2. **Finalidade e necessidade:** cada campo tem uma finalidade escrita? Dá para coletar menos?
3. **Base legal** (art. 7º) escolhida e registrada — ver tabela em [references/bases-legais.md](references/bases-legais.md).
   Consentimento não é o padrão: em produto pago, "execução de contrato" costuma cobrir o essencial.
4. **Sensível?** Saúde, biometria, origem racial, religião, opinião política, vida sexual, dado
   genético, filiação sindical (art. 5º, II) → bases do art. 11, mais restritas.
5. **Criança ou adolescente?** Tratamento no melhor interesse (art. 14); para criança, consentimento
   específico de um dos pais ou responsável, com as exceções do próprio artigo.
6. **Retenção:** prazo definido e rotina de exclusão ou anonimização ao fim (art. 16).
7. **Operadores:** cada fornecedor que recebe o dado (e-mail, analytics, IA, hospedagem) tem contrato e
   está listado. Fora do Brasil → regras de transferência internacional (arts. 33–36 e regulamento da ANPD).
8. **Segurança:** acesso mínimo, RLS no banco, criptografia em trânsito e repouso, logs sem dado pessoal.
9. **Transparência:** a política de privacidade cita esta finalidade, a base e os operadores.

## Direitos do titular (art. 18) — o produto precisa conseguir

confirmar tratamento · dar acesso · corrigir · anonimizar/bloquear/eliminar o desnecessário ·
portabilidade · eliminar dados tratados com consentimento · informar com quem compartilha ·
informar sobre não consentir · revogar consentimento. Tenha um canal e um prazo interno de resposta.

## Incidente de segurança

Avalie risco ou dano relevante aos titulares; se houver, comunique ANPD e titulares no prazo do
regulamento de comunicação de incidentes (hoje, dias úteis contados do conhecimento — confira o texto
vigente). Registre todo incidente, mesmo o não comunicado.

## Sinais de alerta numa revisão

- "Vamos guardar tudo, depois vemos" (sem finalidade).
- Pixel/analytics de terceiros carregado antes de qualquer aviso, em página com dado sensível.
- Dado pessoal enviado a API de IA sem estar no contrato nem na política.
- Exportação de base inteira para planilha pessoal.
- Logs de aplicação com CPF, e-mail ou token.
