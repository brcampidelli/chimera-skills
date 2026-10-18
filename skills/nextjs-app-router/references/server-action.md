# Server Action com Zod + Supabase

## Cliente de servidor (`@/lib/supabase/server.ts`)

```ts
import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";

export async function createClient() {
  const cookieStore = await cookies(); // assíncrono no Next 15+
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!, // justificativa: validado na inicialização (env.ts)
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (list) => {
          try {
            list.forEach(({ name, value, options }) => cookieStore.set(name, value, options));
          } catch {
            // chamado de um Server Component: o middleware/proxy renova a sessão
          }
        },
      },
    },
  );
}
```

Confira na documentação do `@supabase/ssr` instalado o nome da variável da chave pública usada pelo
projeto (projetos antigos usam a chave `anon`).

## Action (`@/actions/plan-actions.ts`)

```ts
"use server";

import { revalidatePath } from "next/cache";
import { z } from "zod";
import { createClient } from "@/lib/supabase/server";

type ActionResult<T> = { success: boolean; data: T | null; error: string | null };

const RenamePlanSchema = z.object({
  planId: z.string().uuid(),
  title: z.string().trim().min(1).max(200),
});

export async function renamePlan(input: unknown): Promise<ActionResult<{ id: string }>> {
  const parsed = RenamePlanSchema.safeParse(input);
  if (!parsed.success) return { success: false, data: null, error: "Dados inválidos." };

  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { success: false, data: null, error: "Não autorizado." };

  const { data, error } = await supabase
    .from("plans")
    .update({ title: parsed.data.title })
    .eq("id", parsed.data.planId)
    .eq("user_id", user.id) // dono derivado do servidor, não do cliente
    .select("id")
    .single();

  if (error || !data) return { success: false, data: null, error: "Não foi possível salvar." };
  revalidatePath("/plans");
  return { success: true, data, error: null };
}
```

## Teste mínimo (Vitest)

Mocke o módulo `@/lib/supabase/server` na fronteira e cubra: entrada inválida, usuário ausente, erro do
banco e caminho feliz. Um teste por comportamento.
