# Modelo de dados sugerido (Postgres/Supabase)

```sql
create table questions (
  id uuid primary key default gen_random_uuid(),
  statement text not null,
  options jsonb not null,            -- [{"key":"A","text":"..."}]
  answer_key text not null,          -- "C"
  explanation text,
  subject_path text[] not null,      -- {"Direito Constitucional","Direitos Fundamentais","Art. 5º"}
  board text, exam_year int, agency text,
  source_ref text not null,          -- de onde veio
  source_license text,               -- licença/termos da origem
  dedup_group uuid,                  -- componente conexo de duplicatas
  status text not null default 'active' check (status in ('active','annulled','outdated','draft')),
  status_reason text,
  created_at timestamptz not null default now()
);

create table cards (                 -- estado FSRS por aluno e questão
  user_id uuid not null references auth.users(id) on delete cascade,
  question_id uuid not null references questions(id),
  state jsonb not null,              -- estado devolvido pela biblioteca FSRS
  due_at timestamptz not null,
  suspended boolean not null default false,
  primary key (user_id, question_id)
);

create table review_logs (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  question_id uuid not null references questions(id),
  rating smallint not null check (rating between 1 and 4),
  answered_option text,
  response_ms int,
  state_before jsonb, state_after jsonb,
  reviewed_at timestamptz not null default now()
);

create index on cards (user_id, due_at) where not suspended;
create index on review_logs (user_id, reviewed_at);

alter table questions enable row level security;
alter table cards enable row level security;
alter table review_logs enable row level security;
-- políticas: questions leitura para authenticated; cards/review_logs só do próprio usuário,
-- com (select auth.uid()) = user_id em USING e WITH CHECK.
```

Validações na importação (falham a carga, não só avisam):
- `answer_key` existe em `options`;
- enunciado + alternativas não vazios e sem marcação de gabarito embutida no texto;
- `source_ref` preenchido;
- duplicata detectada recebe o `dedup_group` existente.
