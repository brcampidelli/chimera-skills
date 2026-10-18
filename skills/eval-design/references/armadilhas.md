# Armadilhas de avaliação (com o sintoma de cada uma)

| Armadilha | Sintoma típico | Guarda |
|---|---|---|
| Régua escrita para o modelo base, aplicada ao modelo ajustado | modelo "0%" que, lido à mão, acerta | ler 3 saídas cruas antes de confiar; medir no formato em que treinou; token de parada ligado |
| Configuração diferente entre braços | diferença grande sem mecanismo | config lida no artefato da rodada (JSON salvo), não nos defaults |
| Configuração errada igual nos dois braços | "inalterado" com número absurdo nos dois | controle reproduz número conhecido |
| Gabarito impossível | taxa baixa concentrada em poucas categorias | executar gabaritos antes; checar derivabilidade |
| Métrica "funcional" que é igualdade de string | ferramentas de texto livre com acerto muito menor | perguntar "o que no resultado discrimina?"; rotular eco |
| Holdout com duplicatas | intervalo estreito demais | contar itens distintos |
| Vazamento treino/teste | desempenho alto que some em dado novo | separação por componente conexo + verificação final |
| Atalho de construção (classes geradas por processos diferentes) | regra trivial (tamanho, posição) separa as classes | medir o melhor classificador trivial antes de treinar |
| Comparar pontos de regimes diferentes (ex.: schedules de LR) | tendência que inverte ao final | comparar só pontos do mesmo regime |
| Ruído de semente maior que o limiar | vencedor muda ao trocar a semente | três sementes, limiar acima do piso |
| Lote/hardware diferente em inferência determinística | poucos casos trocam sem padrão | mesmo lote e mesma GPU dos dois lados; remedir referências |
| Verificador que aceita quase tudo | laço de retentativa que não melhora | medir a taxa de rejeição antes de projetar o laço |
| Medir o destino em vez do caminho | intervenção na geração piora o que a análise prévia dizia ser seguro | medir com a intervenção ligada num subconjunto |
| Consolidador que reaproveita relatório | célula "inalterada" que não foi medida | procedência no JSON; nome de saída derivado do artefato |
| Veredito que o ruído confirma | "confirmado" com deltas dentro do piso | testar o consolidador com deltas nulos |
| Censo por amostra para pares (duplicatas, vazamento) | "corpus limpo" | censo completo, ou corrigir por 1/f e reportar os dois |

## Checklist de leitura de um resultado alheio

- [ ] O n é de itens distintos? Há intervalo?
- [ ] Os braços usaram a mesma régua, config, lote e hardware?
- [ ] Algum braço reproduz um número conhecido?
- [ ] Quantas sementes? Qual a dispersão?
- [ ] O que piorou está na tabela?
- [ ] A previsão foi registrada antes?
- [ ] O que este holdout não conseguiria mostrar?
