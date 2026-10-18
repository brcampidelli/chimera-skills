# Receitas openpyxl

## Criar com fórmulas e formatos

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Receita"

ws.append(["Mês", "Receita", "Custo", "Margem"])
data = [("2026-01", 12000, 7000), ("2026-02", 13500, 7200)]
for i, (month, revenue, cost) in enumerate(data, start=2):
    ws.append([month, revenue, cost, f"=(B{i}-C{i})/B{i}"])

last = ws.max_row
ws.append(["Total", f"=SUM(B2:B{last})", f"=SUM(C2:C{last})", f"=(B{last+1}-C{last+1})/B{last+1}"])

for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="DDEBF7")
for row in ws.iter_rows(min_row=2, min_col=2, max_col=3):
    for cell in row:
        cell.number_format = '"R$" #,##0.00'
for row in ws.iter_rows(min_row=2, min_col=4, max_col=4):
    for cell in row:
        cell.number_format = "0.0%"

ws.freeze_panes = "A2"
for col in range(1, ws.max_column + 1):
    ws.column_dimensions[get_column_letter(col)].width = 16

wb.save("receita.xlsx")
```

## Validação de dados e formatação condicional

```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

dv = DataValidation(type="list", formula1='"Aberto,Pago,Cancelado"', allow_blank=False)
ws.add_data_validation(dv)
dv.add("E2:E500")

red = PatternFill("solid", fgColor="F8CBAD")
ws.conditional_formatting.add("D2:D500", CellIsRule(operator="lessThan", formula=["0"], fill=red))
```

## Gráfico de linhas

```python
from openpyxl.chart import LineChart, Reference

chart = LineChart()
chart.title = "Receita por mês"
values = Reference(ws, min_col=2, min_row=1, max_row=last)
cats = Reference(ws, min_col=1, min_row=2, max_row=last)
chart.add_data(values, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "F2")
```

## Ler

```python
from openpyxl import load_workbook

wb = load_workbook("entrada.xlsx")                    # fórmulas como texto
wb_values = load_workbook("entrada.xlsx", data_only=True)  # últimos valores salvos (podem ser None)
for row in wb["Receita"].iter_rows(min_row=2, values_only=True):
    print(row)
```

## pandas (dados tabulares)

```python
import pandas as pd

df = pd.read_excel("entrada.xlsx", sheet_name="Receita")
with pd.ExcelWriter("saida.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Dados", index=False)
```

pandas escreve valores, não fórmulas: use-o para dados e o openpyxl para a camada de fórmulas e formato.

## Arquivos grandes

`Workbook(write_only=True)` para escrever muitas linhas com pouca memória; `load_workbook(...,
read_only=True)` para ler. Nos dois modos, várias operações de formatação não estão disponíveis.
