---
name: eval-design
description: >-
  Desenhar e ler avaliações de modelos, agentes e prompts sem enganar a si mesmo: comparação pareada
  (mesmos itens, mesma régua, mesmo n), piso de ruído, três sementes, controle que reproduz um número
  conhecido, gabarito executável e derivável do prompt, itens distintos, intervalo de confiança,
  política realizável em vez de pass@k, e pré-registro da previsão. Use ao criar um benchmark ou
  holdout, comparar dois checkpoints, prompts ou modelos, ou revisar uma afirmação de melhora.
license: Apache-2.0
metadata:
  category: ai-models-agents
  categories_secondary: research, testing-quality
  tags: evals, benchmark, holdout, estatistica, llm, agentes
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: verify
topic: mlops
---

# Desenho de avaliação

Quase todo erro de avaliação tem a mesma cara: **nada dá erro, o número sai plausível**. A pergunta que
abre cada item abaixo é: *o que este aparato NÃO conseguiria mostrar?*

## Antes de rodar

1. **Pré-registre** a previsão e o critério de decisão (folga **absoluta**, por exemplo ≥ 5 pontos,
   nunca multiplicativa) num arquivo commitado antes do resultado.
2. **Gabarito:** todo gabarito executa **e** é derivável do que o modelo recebe. Rode os gabaritos
   antes de carregar qualquer modelo; referência impossível derruba a métrica em silêncio.
3. **Itens distintos:** conte itens únicos, não linhas; calcule o intervalo (Wilson) sobre o n efetivo.
4. **Separação treino/teste** por componente conexo de tudo que é compartilhado (prompt, tupla,
   fonte), com verificação posterior sobre os arquivos finais.
5. **Poder:** escreva o que a métrica mostraria se a hipótese fosse verdadeira. Se o efeito esperado é
   menor que o piso de ruído, o experimento não decide nada.

## Ao comparar

- **Três perguntas:** mesmos itens? mesma régua (config, formato do prompt, lote, hardware)? mesmo n?
  Algum "não" → a diferença é do aparato até prova em contrário.
- **Pareado** sempre que possível: os dois braços nos mesmos itens, contando o que melhorou **e o que piorou**.
- **Controle:** pelo menos um braço reproduz um número já publicado; se não reproduz, não há comparação.
- **Sementes:** duas alertam, três decidem. Compare a dispersão ao erro amostral da diferença (EP·√2).
- **Agregado** se decompõe por componente antes de virar afirmação; sinais opostos indicam efeito de
  formato, não de capacidade.

## Ao reportar

- Mostre o piso de ruído ao lado do efeito.
- `pass@k` olha a referência; reporte junto a **política realizável** (o que dá para entregar sem gabarito).
- Invariante obrigatório: **previsão idêntica à referência não pode reprovar**. Se reprova, a régua está quebrada.
- Refutação registra o que o holdout era incapaz de mostrar.
- Resultado nulo é resultado: publique com o mesmo destaque.

Checklist completo e exemplos de cada armadilha: [references/armadilhas.md](references/armadilhas.md).
