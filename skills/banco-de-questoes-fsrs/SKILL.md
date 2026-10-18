---
name: banco-de-questoes-fsrs
description: >-
  Construir e manter um banco de questões para estudo (concursos, vestibular, certificações) e agendar
  revisões com FSRS (repetição espaçada): modelo de dados, gabarito derivável do enunciado,
  deduplicação, classificação por assunto e banca, qualidade de distratores, e uso correto do FSRS
  (notas 1–4, retenção desejada, otimização de parâmetros). Use ao criar, importar ou revisar questões,
  ou ao implementar ou depurar o agendador de revisões de uma plataforma de estudo.
license: Apache-2.0
metadata:
  category: education
  categories_secondary: product, databases
  tags: edtech, questoes, concursos, fsrs, repeticao-espacada, quiz
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: build
topic: data-science
---

# Banco de questões + FSRS

## Banco de questões — regras de qualidade

1. **O gabarito tem de ser derivável do enunciado** (mais o material citado). Questão cuja resposta
   depende de informação ausente é defeito, não "questão difícil". Verifique isso em toda importação.
2. **Uma questão, uma ideia testada.** Marque o assunto pelo edital (disciplina → tópico → subtópico),
   a banca, o ano e o órgão quando houver.
3. **Distratores plausíveis:** cada alternativa errada representa um erro real de raciocínio, com o
   mesmo tamanho e registro das outras. "Todas as anteriores" e pegadinhas de forma enfraquecem a medida.
4. **Questão anulada ou desatualizada** (lei mudou) não some: fica marcada com motivo e data, fora das
   revisões.
5. **Deduplicação por componente conexo:** a mesma questão aparece com pequenas variações em várias
   fontes. Agrupe por enunciado normalizado **ou** por gabarito + alternativas; separar treino e teste
   (ou "simulado inédito") por questão individual vaza.
6. **Conte itens distintos**, não linhas, ao anunciar o tamanho do banco.
7. **Direitos autorais:** registre a origem e a licença de cada questão; prova pública não significa
   comentário ou explicação livres para copiar.

Modelo de dados sugerido: [references/modelo-dados.md](references/modelo-dados.md).

## FSRS — como usar sem reinventar

- **Use uma biblioteca mantida** (`ts-fsrs`, `py-fsrs` ou a da sua linguagem, versão fixada) em vez de
  reimplementar as fórmulas. Guarde o estado do cartão que ela devolve.
- **Notas:** 1 = Errei (Again), 2 = Difícil, 3 = Bom, 4 = Fácil. Numa questão objetiva, mapeie de forma
  simples e estável (errou = 1, acertou com hesitação = 2, acertou = 3) e documente o mapeamento.
- **Retenção desejada** (tipicamente perto de 0,9) é a alavanca de carga: subir aumenta revisões
  diárias. Mude com cuidado e mostre o impacto estimado ao aluno.
- **Otimize os parâmetros** com o histórico real de revisões quando houver volume suficiente; antes
  disso, use os padrões da biblioteca.
- **Registre cada revisão** (cartão, data, nota, tempo de resposta, estado antes e depois). Sem o
  log, não há otimização nem auditoria.

Fundamentos do modelo e armadilhas: [references/fsrs.md](references/fsrs.md).
