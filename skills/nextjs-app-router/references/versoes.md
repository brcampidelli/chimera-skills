# Diferenças de versão que mais quebram código

Confirme sempre na documentação da versão instalada; esta lista é um mapa, não a fonte.

| Tema | Next 14 | Next 15 | Next 16 |
|---|---|---|---|
| `params` / `searchParams` em páginas | objeto | **Promise** (`await props.params`) | Promise |
| `cookies()`, `headers()`, `draftMode()` | síncronos | **assíncronos** | assíncronos |
| `fetch` no servidor | cacheado por padrão | **não cacheado** por padrão | modelo de cache explícito (`"use cache"` / cache components) |
| Interceptação de requisição | `middleware.ts` | `middleware.ts` | renomeado para `proxy.ts` (confira o codemod da versão) |
| React | 18 | 19 | 19.x |

Ao atualizar: rode o codemod oficial da versão (`npx @next/codemod@<versão> ...`, com versão fixa) num
branch, leia o diff inteiro e rode build + testes antes de abrir PR.
