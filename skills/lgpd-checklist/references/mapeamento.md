# Modelo de mapeamento de dados (registro das operações)

Uma linha por finalidade. Guarde no repositório do produto (por exemplo `docs/privacidade/mapa.md`).

| Finalidade | Dados | Titulares | Base legal | Origem | Onde fica | Quem acessa | Operadores | Fora do Brasil? | Retenção | Exclusão |
|---|---|---|---|---|---|---|---|---|---|---|
| Criar conta | nome, e-mail, senha (hash) | usuários | execução de contrato | formulário | Supabase (auth) | suporte (leitura) | Supabase | sim (região do projeto) | enquanto a conta existir | rotina de exclusão de conta |
| Newsletter | e-mail | inscritos | consentimento | formulário com opt-in | provedor de e-mail | marketing | provedor de e-mail | sim | até descadastro | descadastro remove o contato |

Perguntas que o mapa precisa responder:
- Se o titular pedir "apaguem meus dados", em quantos sistemas a gente mexe? Estão todos aqui?
- Algum dado chega a um operador sem contrato?
- Algum campo não tem finalidade escrita? Corte-o.
