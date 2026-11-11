-- Move as datas de conclusão das etapas da Fase 0 de setembro/2026 para novembro/2026.
-- Rode uma vez no SQL Editor do Supabase. Só altera o campo doneAt das etapas listadas.
update public.docs
set data = jsonb_set(data, '{doneAt}', to_jsonb(novo.data_nova::text))
from (values
  ('f0-rotina',   '2026-11-11'::date),
  ('f0-github',   '2026-11-12'::date),
  ('f0-ambiente', '2026-11-14'::date),
  ('f0-contas',   '2026-11-16'::date),
  ('f0-zoomcamp', '2026-11-17'::date)
) as novo(etapa, data_nova)
where public.docs.collection = 'progress'
  and public.docs.id = novo.etapa
  and public.docs.data ? 'doneAt';
