# Receitas python-pptx

## Criar em 16:9 com título e tópicos

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


def layout(prs, name: str):
    for lay in prs.slide_layouts:
        if lay.name == name:
            return lay
    raise KeyError(f"layout {name!r} não existe neste modelo")


title_slide = prs.slides.add_slide(layout(prs, "Title Slide"))
title_slide.shapes.title.text = "Resultados de outubro"
title_slide.placeholders[1].text = "Equipe de produto — 17/10/2026"

s = prs.slides.add_slide(layout(prs, "Title and Content"))
s.shapes.title.text = "Receita cresceu 12,5% em outubro"
body = s.placeholders[1].text_frame
body.text = "48 novos clientes"
for line in ("7 cancelamentos", "Ticket médio estável"):
    p = body.add_paragraph()
    p.text = line
    p.font.size = Pt(20)
s.notes_slide.notes_text_frame.text = "Explicar a campanha de setembro que puxou os novos clientes."

prs.save("resultados.pptx")
```

Os nomes de layout acima são os do modelo padrão em inglês; num modelo da empresa, liste
`[l.name for l in prs.slide_layouts]` primeiro.

## Gráfico nativo

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

data = CategoryChartData()
data.categories = ["Jul", "Ago", "Set", "Out"]
data.add_series("Receita (R$ mil)", (10.2, 11.0, 11.6, 13.05))

s = prs.slides.add_slide(layout(prs, "Title Only"))
s.shapes.title.text = "Outubro foi o melhor mês do ano"
s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1), Inches(1.6), Inches(11), Inches(5.4), data)
```

## Tabela

```python
rows, cols = 3, 3
shape = s.shapes.add_table(rows, cols, Inches(1), Inches(1.6), Inches(8), Inches(2))
table = shape.table
for c, h in enumerate(("Plano", "Clientes", "Receita")):
    table.cell(0, c).text = h
```

## Imagem

```python
s.shapes.add_picture("logo.png", Inches(11.5), Inches(0.3), height=Inches(0.8))
```

## Extrair texto

```python
prs = Presentation("entrada.pptx")
for i, slide in enumerate(prs.slides, start=1):
    texts = [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame]
    notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
    print(i, texts, notes)
```
