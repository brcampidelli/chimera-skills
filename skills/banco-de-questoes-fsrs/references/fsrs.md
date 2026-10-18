# FSRS — fundamentos e armadilhas

## O modelo em uma tela

Cada cartão tem três variáveis:
- **Estabilidade (S):** quantos dias até a probabilidade de lembrar cair para o nível de referência.
- **Dificuldade (D):** quanto a estabilidade cresce a cada acerto (cartões difíceis crescem menos).
- **Recuperabilidade (R):** probabilidade de lembrar agora, que cai com o tempo desde a última revisão.

Nas versões FSRS-4.5/5, a curva de esquecimento é uma potência:

```
R(t, S) = (1 + F · t / S) ^ C,   com C = -0,5 e F = 19/81
```

e o intervalo para uma retenção desejada `r` sai invertendo a curva:

```
I(r, S) = (S / F) · (r^(1/C) - 1)
```

Com `r = 0,9`, `I = S`: por isso a estabilidade é "o intervalo a 90%". Versões mais novas tornam o
expoente treinável; use as fórmulas da versão da biblioteca instalada, não as daqui.

## Armadilhas

| Armadilha | Consequência | Como evitar |
|---|---|---|
| Reimplementar fórmulas "de cabeça" | agendamento silenciosamente errado | biblioteca com versão fixa + teste com casos da própria biblioteca |
| Mapear nota de forma diferente entre telas | parâmetros otimizados sobre dado incoerente | uma função única de mapeamento |
| Guardar só a próxima data | impossível otimizar ou corrigir depois | log completo de revisões |
| Fuso horário | revisão "atrasada" ou duplicada à meia-noite | datas em UTC no banco, "dia" calculado no fuso do aluno |
| Revisar questão anulada | aluno aprende errado | estado `suspenso` fora da fila |
| Comparar retenção entre grupos com n pequeno | conclusão por ruído | mesmo período, mesmos itens, intervalo de confiança |

## Medir se está funcionando

Compare a retenção prevista com a observada (acerto real nas revisões) em faixas de R prevista; uma
curva de calibração bem alinhada é o sinal de saúde. Desvios sistemáticos indicam parâmetros
desatualizados ou mapeamento de nota inconsistente.
