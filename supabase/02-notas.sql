-- Trilha Dados e IA: libera a coleção "scores" (provas, testes e notas do Painel).
-- Rode uma vez no Supabase: SQL Editor > New query > cole tudo > Run.
alter table public.docs drop constraint if exists docs_collection_check;
alter table public.docs add constraint docs_collection_check
  check (collection in ('progress', 'log', 'settings', 'accounts', 'sync', 'scores'));
