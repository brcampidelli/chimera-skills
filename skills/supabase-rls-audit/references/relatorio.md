# Formato do relatório

```markdown
# Auditoria de RLS — <projeto> (<ambiente>) — <data>

**Escopo:** schemas <lista>. **Meio de leitura:** <MCP/psql/CLI, papel>. **Nada foi alterado.**

## Resumo
| Severidade | Quantidade |
|---|---|
| Crítica | n |
| Alta | n |
| Média | n |
| Baixa | n |

## Achados
### [CRÍTICA] public.<tabela>: exposta sem RLS
- **Evidência:** consulta 1 (rls_ligada = false) + consulta 2 (anon: SELECT, INSERT).
- **Impacto:** qualquer visitante lê e grava pela Data API.
- **Prova:** <resultado da transação desfeita, ou "não provado: <motivo>">.
- **Correção proposta:** ver migração, bloco 1.

## Migração proposta (NÃO APLICADA)
-- revisar e aplicar manualmente, em branch/local primeiro
-- bloco 1
alter table public.<tabela> enable row level security;
create policy "<tabela>_select_own" on public.<tabela>
  for select to authenticated using ((select auth.uid()) = user_id);
```

Regras do relatório:
- toda afirmação aponta para a consulta que a sustenta;
- conte linhas afetadas, nunca liste dados pessoais;
- o que não foi possível verificar entra numa seção "Não verificado", com o motivo.
