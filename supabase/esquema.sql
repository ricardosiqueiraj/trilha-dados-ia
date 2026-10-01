-- Trilha Dados e IA: banco do site.
-- Rode uma vez no Supabase: SQL Editor > New query > cole tudo > Run.
-- Cada pessoa só lê e grava as próprias linhas (Row Level Security).

create table if not exists public.docs (
  owner      uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  collection text        not null check (collection in ('progress', 'log', 'settings', 'accounts', 'sync', 'scores')),
  id         text        not null check (char_length(id) between 1 and 200),
  data       jsonb       not null,
  updated_at timestamptz not null default now(),
  primary key (owner, collection, id)
);

alter table public.docs enable row level security;
alter table public.docs replica identity full;

drop policy if exists "ler as proprias linhas"    on public.docs;
drop policy if exists "criar as proprias linhas"  on public.docs;
drop policy if exists "mudar as proprias linhas"  on public.docs;
drop policy if exists "apagar as proprias linhas" on public.docs;

create policy "ler as proprias linhas"    on public.docs for select using (auth.uid() = owner);
create policy "criar as proprias linhas"  on public.docs for insert with check (auth.uid() = owner);
create policy "mudar as proprias linhas"  on public.docs for update using (auth.uid() = owner) with check (auth.uid() = owner);
create policy "apagar as proprias linhas" on public.docs for delete using (auth.uid() = owner);

-- Atualização em tempo real entre celular e computador.
do $$
begin
  alter publication supabase_realtime add table public.docs;
exception when duplicate_object then null;
end $$;
