---
name: xlsx-builder
description: >-
  Criar, ler e editar planilhas Excel (.xlsx) com a biblioteca aberta openpyxl (e pandas para dados
  tabulares): fórmulas vivas em vez de números colados, formatos de moeda e data brasileiros, larguras,
  congelar painéis, validação de dados, formatação condicional e gráficos, mais a diferença entre
  fórmula e valor calculado. Use quando o entregável for um .xlsx ou para limpar e reorganizar uma
  planilha existente. Create and edit Excel workbooks with openpyxl.
license: Apache-2.0
metadata:
  category: files-documents
  categories_secondary: finance-payments
  tags: xlsx, excel, openpyxl, pandas, planilha
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: build
topic: data-science
---

# Planilhas com openpyxl

Escrito do zero sobre a documentação pública do `openpyxl` (licença MIT). Fixe a versão no projeto.

## Regras

1. **Fórmula, não número colado.** Totais, médias e percentuais ficam como fórmula (`"=SUM(B2:B13)"`)
   para a planilha continuar certa quando alguém editar uma célula.
2. **Fórmulas no arquivo usam a sintaxe em inglês** (`SUM`, `IF`, separador `,`), mesmo que o Excel do
   usuário mostre `SOMA` e `;`. O Excel traduz ao abrir.
3. **openpyxl não calcula fórmulas.** Ao ler com `data_only=True`, você recebe o último valor salvo por
   um programa de planilha — ou `None` se o arquivo nunca foi aberto e salvo nele. Para conferir
   números, calcule em Python a partir dos dados e compare.
4. **Formato é apresentação; o valor continua número.** Moeda: `'"R$" #,##0.00'`; data: `'DD/MM/YYYY'`;
   porcentagem: `'0.0%'`. O Excel aplica separadores do idioma do usuário.
5. **Uma tabela por aba, cabeçalho na linha 1**, sem células mescladas em área de dados.
6. **Abra o arquivo de novo e verifique** por código: dimensões, cabeçalhos, fórmulas presentes, nenhum
   `#REF!`/`#DIV/0!` nos valores calculados quando disponíveis.

Receitas (criar, formatar, validar, gráfico, ler, pandas, arquivos grandes): [references/receitas.md](references/receitas.md).

## Armadilhas

- `.xls` antigo não é lido pelo openpyxl; converta ou use outra biblioteca.
- Macros (`.xlsm`): preserve só com `keep_vba=True`, nunca execute; trate como não confiável.
- Datas: o Excel guarda número de série; openpyxl converte para `datetime` quando a célula tem formato
  de data. Sem formato, você verá um número.
- Salvar por cima do arquivo original apaga gráficos e recursos que o openpyxl não entende; salve em
  arquivo novo e avise.
