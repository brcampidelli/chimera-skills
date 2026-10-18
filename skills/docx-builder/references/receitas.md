# Receitas python-docx

## Criar um relatório

```python
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

doc = Document()

section = doc.sections[0]
section.top_margin = section.bottom_margin = Cm(2.5)
section.left_margin = section.right_margin = Cm(2.5)

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)

doc.add_heading("Relatório mensal", level=0)          # título do documento
p = doc.add_paragraph("Período: outubro de 2026")
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

doc.add_heading("1. Resumo", level=1)
doc.add_paragraph("Receita cresceu 12,5% sobre setembro.")
doc.add_paragraph("Novos clientes: 48", style="List Bullet")
doc.add_paragraph("Cancelamentos: 7", style="List Bullet")

doc.add_page_break()
doc.save("relatorio.docx")
```

## Tabela

```python
rows = [("Produto", "Vendas", "Receita"), ("Plano mensal", "120", "R$ 5.880,00")]
table = doc.add_table(rows=0, cols=3)
table.style = "Table Grid"
for i, values in enumerate(rows):
    cells = table.add_row().cells
    for cell, value in zip(cells, values):
        cell.text = value
        if i == 0:
            cell.paragraphs[0].runs[0].bold = True
```

## Imagem e legenda

```python
doc.add_picture("grafico.png", width=Cm(15))
doc.add_paragraph("Figura 1 — Receita por mês", style="Caption")
```

## Cabeçalho e rodapé

```python
header = doc.sections[0].header
header.paragraphs[0].text = "Empresa X — Confidencial"
footer = doc.sections[0].footer
footer.paragraphs[0].text = "Gerado automaticamente"
```

## Paisagem numa seção nova

```python
from docx.enum.section import WD_SECTION
new = doc.add_section(WD_SECTION.NEW_PAGE)
new.orientation = WD_ORIENT.LANDSCAPE
new.page_width, new.page_height = new.page_height, new.page_width
```

## Ler

```python
doc = Document("entrada.docx")
for para in doc.paragraphs:
    print(para.style.name, "|", para.text)
for t in doc.tables:
    for row in t.rows:
        print([c.text for c in row.cells])
```

`doc.paragraphs` não inclui texto de tabelas, cabeçalhos e rodapés; percorra cada um.

## Trocar texto que atravessa runs

```python
def replace_in_paragraph(paragraph, old: str, new: str) -> bool:
    """Troca no texto do parágrafo inteiro; mantém a formatação do primeiro run."""
    full = "".join(run.text for run in paragraph.runs)
    if old not in full:
        return False
    first, *rest = paragraph.runs
    first.text = full.replace(old, new)
    for run in rest:
        run.text = ""
    return True
```

Aplique também em células de tabela (`cell.paragraphs`) e em cabeçalhos/rodapés. Avise o usuário se o
parágrafo tinha formatação mista (negrito numa parte), porque ela é simplificada.
