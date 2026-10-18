# Consultas de auditoria (todas somente leitura)

Troque `'public'` pela lista de schemas expostos na Data API do projeto (Configurações → Data API).

## 1. Tabelas sem RLS em schema exposto

```sql
select n.nspname as schema, c.relname as tabela,
       c.relrowsecurity as rls_ligada, c.relforcerowsecurity as rls_forcada
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where c.relkind in ('r', 'p')
  and n.nspname in ('public')
order by c.relrowsecurity, n.nspname, c.relname;
```

## 2. Grants a anon / authenticated

```sql
select table_schema, table_name, grantee, string_agg(privilege_type, ', ' order by privilege_type) as privs
from information_schema.role_table_grants
where grantee in ('anon', 'authenticated', 'PUBLIC')
  and table_schema in ('public')
group by 1, 2, 3
order by 1, 2, 3;
```

Cruze com a consulta 1: grant + RLS desligada = **crítico**.

## 3. Políticas e seus predicados

```sql
select schemaname, tablename, policyname, permissive, roles, cmd,
       qual as using_expr, with_check
from pg_policies
where schemaname in ('public', 'storage')
order by schemaname, tablename, cmd;
```

Sinais a marcar:
- `using_expr = 'true'` ou ausente em `SELECT`/`DELETE`;
- `cmd = 'UPDATE'` com `with_check` nulo;
- `roles` contendo `{public}` ou `{anon}` em tabela com dado pessoal;
- expressões com `user_metadata` / `raw_user_meta_data` (editável pelo próprio usuário);
- `auth.role()` (obsoleto; use `TO authenticated`);
- `auth.uid()` sem `(select auth.uid())` (reavaliado por linha).

## 4. Tabelas com RLS e nenhuma política

```sql
select n.nspname, c.relname
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where c.relkind in ('r', 'p') and c.relrowsecurity
  and n.nspname in ('public')
  and not exists (select 1 from pg_policies p
                  where p.schemaname = n.nspname and p.tablename = c.relname);
```

## 5. Views que podem furar RLS

```sql
select n.nspname, c.relname, c.reloptions
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where c.relkind in ('v', 'm') and n.nspname in ('public');
```

View sem `security_invoker=true` em `reloptions` roda com o dono e ignora a RLS de quem consulta.
Views materializadas (`m`) não têm RLS nenhuma.

## 6. Funções SECURITY DEFINER expostas

```sql
select n.nspname, p.proname, pg_get_function_identity_arguments(p.oid) as args,
       has_function_privilege('anon', p.oid, 'execute') as anon_exec,
       p.proconfig as config
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where p.prosecdef and n.nspname in ('public');
```

Para cada linha: o corpo checa `auth.uid()`? Fixa `search_path` (`config` contém `search_path=`)?
Leia o corpo com `select pg_get_functiondef('<schema>.<nome>(<args>)'::regprocedure);`.

## 7. Storage

```sql
select id, name, public from storage.buckets order by public desc, name;
```

Bucket `public = true` serve qualquer objeto por URL, sem RLS. As políticas de `storage.objects`
aparecem na consulta 3.

## Prova sem escrita

Simula um usuário específico dentro de uma transação que é sempre desfeita:

```sql
begin;
set local role authenticated;
select set_config('request.jwt.claims',
  json_build_object('sub', '<uuid-do-usuario-A>', 'role', 'authenticated')::text, true);
select count(*) from public.<tabela> where user_id <> '<uuid-do-usuario-A>';  -- deve ser 0
rollback;
```

Só `select`/`count` dentro da prova. Se o resultado precisar de um `update` para demonstrar, descreva o
cenário no relatório em vez de executá-lo.
