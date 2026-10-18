---
name: nextjs-app-router
description: >-
  Padrões do Next.js App Router (15+) com Supabase: Server Components por padrão, "use client" só nas
  folhas, Server Actions com validação Zod e autenticação por getUser(), revalidação de cache, rotas
  de API, metadata, loading/error, imports absolutos. Use ao criar ou revisar páginas, layouts, server
  actions, route handlers ou integração @supabase/ssr num projeto Next.js com App Router.
license: Apache-2.0
metadata:
  category: sites-frontend
  categories_secondary: code, security
  tags: nextjs, react, app-router, server-actions, zod, supabase-ssr
  mode: own
  lang: pt-BR
  scripts: "false"
  network: "false"
stage: build
topic: software-dev
---

# Next.js App Router

**Primeiro passo sempre:** leia `package.json` e confirme a versão do `next`. Várias APIs mudaram entre
14, 15 e 16 (veja [references/versoes.md](references/versoes.md)). Siga o padrão que o projeto já usa
antes de introduzir outro.

## Regras

1. **Server Component é o padrão.** `"use client"` só no menor componente que precisa de estado,
   efeito ou evento do navegador. Dado é buscado no servidor e passado como prop.
2. **Toda Server Action e todo Route Handler** fazem, nesta ordem: validar entrada com Zod
   (`safeParse`) → autenticar com `supabase.auth.getUser()` (nunca `getSession()` para decidir acesso
   no servidor) → autorizar (o recurso é do usuário?) → executar → revalidar.
3. **Nunca confie em id vindo do cliente** para dono do recurso; derive de `user.id`. A RLS do banco
   é a segunda trava, não a única.
4. **Erros:** devolva mensagem genérica ao cliente e registre o detalhe no servidor. Formato:
   `{ success, data, error }`.
5. **Segredos** só em variáveis sem `NEXT_PUBLIC_`. Tudo com esse prefixo vai para o navegador.
6. **Cache:** depois de mutação, `revalidatePath` ou `revalidateTag` do que mudou.
7. **Imports absolutos** (`@/lib/...`), `next/image` para imagem, `next/font` para fonte.
8. **Estados de rota:** `loading.tsx` para carregamento, `error.tsx` (client) para falha,
   `not-found.tsx` com `notFound()`.

## Esqueleto de Server Action

Veja [references/server-action.md](references/server-action.md) — inclui o cliente Supabase de servidor
com `@supabase/ssr` e um teste mínimo.

## Revisão rápida (antes de entregar)

- [ ] nenhuma action/handler sem Zod + `getUser()`
- [ ] nenhum `"use client"` em página inteira sem necessidade
- [ ] nenhum segredo com `NEXT_PUBLIC_`
- [ ] nenhum `select('*')` em consulta de produção
- [ ] mutação revalida o que exibe
- [ ] `params`/`searchParams`/`cookies()` tratados conforme a versão (assíncronos a partir da 15)
