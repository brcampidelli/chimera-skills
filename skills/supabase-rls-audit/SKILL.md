---
name: supabase-rls-audit
description: >-
  Auditoria adversarial, somente leitura, das políticas RLS e dos privilégios de um projeto Supabase:
  tabelas expostas sem RLS, políticas permissivas (USING true, TO public), UPDATE sem WITH CHECK,
  views que furam RLS, funções SECURITY DEFINER expostas, grants a anon/authenticated, storage e uso de
  user_metadata. Produz um relatório com evidência e uma migração PROPOSTA, nunca aplicada. Use quando
  pedirem auditoria de RLS, revisão de segurança de banco Supabase, "quem consegue ler esta tabela?"
  ou antes de abrir uma tabela à Data API. Read-only Supabase RLS / privilege audit.
license: Apache-2.0
metadata:
  category: security
  categories_secondary: databases
  tags: supabase, postgres, rls, auditoria, idor, privilegios
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: review
topic: security
---

# Auditoria de RLS no Supabase (somente leitura)

**Princípio:** auditar é ler. Esta skill **nunca** executa `ALTER`, `GRANT`, `REVOKE`, `CREATE POLICY`,
`DROP` nem escreve em `auth.*`. Tudo o que muda o banco sai como **migração proposta** num arquivo, para
uma pessoa revisar e aplicar. Testar uma correção "contra produção contando que algo bloqueie" já causou
incidente real; não repita.

## Procedimento

1. **Confirme o alvo e o acesso.** Projeto (ref), ambiente (local, branch, produção) e o meio de leitura
   (MCP `execute_sql` em modo leitura, `psql` com papel de leitura, ou `supabase db query` local). Se a
   única credencial disponível escreve, diga isso ao usuário antes de continuar.
2. **Inventário.** Rode as consultas de [references/consultas.md](references/consultas.md), seção por
   seção. Guarde a saída crua; o relatório cita a linha.
3. **Classifique cada achado** pela tabela de severidade abaixo.
4. **Prove o impacto quando possível**, sempre dentro de `begin; ... rollback;` e com papel simulado
   (seção "Prova sem escrita" das consultas). Se o ambiente não permitir transação, não prove: descreva.
5. **Relatório** no formato de [references/relatorio.md](references/relatorio.md), com a migração
   proposta em bloco separado e marcada como **não aplicada**.

## Severidade

| Severidade | Exemplos |
|---|---|
| Crítica | tabela em schema exposto sem RLS e com grant a `anon`; política `USING (true)` em dado pessoal; `SECURITY DEFINER` em `public` sem checagem de `auth.uid()` |
| Alta | `UPDATE` sem `WITH CHECK` (dono reatribuível); view sem `security_invoker` sobre tabela com RLS; política baseada em `user_metadata` |
| Média | `TO authenticated` sem predicado de dono (IDOR entre usuários logados); bucket de storage público com dado não público |
| Baixa | `auth.role()` obsoleto; `auth.uid()` sem `(select ...)` (custo por linha) |

## Armadilhas que esta auditoria procura de propósito

- RLS ligada **sem nenhuma política** bloqueia tudo — parece seguro, mas costuma vir acompanhada de um
  atalho com `service_role` no cliente. Procure o atalho.
- Política certa no `SELECT` e ausente no `UPDATE`: o update "não dá erro", só não muda nada.
- `anon` herda de `PUBLIC`: função nova em `public` é executável por qualquer visitante.
- Dono da tabela ignora RLS a menos que exista `FORCE ROW LEVEL SECURITY`.

## Não faça

- Não "conserte" durante a auditoria, nem quando a correção parece óbvia.
- Não imprima linhas de dados pessoais no relatório: conte, não liste.
- Não confie em `NEXT_PUBLIC_*`/front-end para controle de acesso; a regra mora no banco.
