# Plano de estudos: Trilha Dados e IA

De Analista de Integração a Engenheiro de Dados e, depois, a Engenheiro de IA. São 39 etapas em 6 fases, de outubro de 2026 a dezembro de 2027, só com cursos gratuitos. As etapas marcadas já foram concluídas.

## Engenharia de Dados (Trilha 1 · Fases 0 a 3)

Você já extrai, trata e carrega dados de ERP no trabalho. Estas fases dão ferramentas, projetos e certificação a essa experiência. Meta: vagas de Engenheiro de Dados a partir de junho de 2027.

### Fase 0 · Preparar o terreno

**Período:** 5 a 11 de outubro de 2026 · ≈ 6,5 h de estudo · **Situação:** Em andamento (1/5)

**Objetivo:** Deixar ambiente, contas e rotina prontos para não perder tempo depois.

- [x] **F0.1 · Defina sua rotina de estudo** (≈ 1 h) · concluída em 29/09/2026\
  Reserve três blocos fixos por semana, como os que já estão na sua agenda: terças e quintas à noite e sábado de manhã. Registre cada sessão na aba Horas.
- [ ] **F0.2 · Ligue seu GitHub ao projeto** (≈ 1 h)\
  Você já tem conta. Crie o repositório trilha-dados-ia e conecte o GitHub ao Claude, como mostra a aba Contas e integrações: o repositório passa a receber seu progresso toda semana. Os projetos do plano também vão para o GitHub, cada um no seu repositório, com um README que explica o problema, a arquitetura e como rodar.\
  Links: [GitHub](https://github.com/) (EN)
- [ ] **F0.3 · Monte o ambiente no seu computador** (≈ 3 h)\
  Instale VS Code, Python 3 e Git. No Windows, ative o WSL2 para ter um terminal Linux, o padrão no dia a dia de dados.\
  Links: [Instalar o WSL](https://learn.microsoft.com/pt-br/windows/wsl/install) (PT) · [VS Code](https://code.visualstudio.com/) (EN)
- [ ] **F0.4 · Crie as contas gratuitas de estudo** (≈ 1 h)\
  Databricks Free Edition (sem cartão de crédito), conta Microsoft para o Microsoft Learn, Kaggle e DataTalks.Club. É nelas que você vai praticar e fazer os cursos. A aba Contas e integrações mostra quais deixam entrar com o GitHub e quais salvam o trabalho nele.\
  Links: [Databricks Free Edition](https://www.databricks.com/learn/free-edition) (EN) · [Microsoft Learn](https://learn.microsoft.com/pt-br/training/) (PT) · [Kaggle Learn](https://www.kaggle.com/learn) (EN)
- [ ] **F0.5 · Inscreva-se no Data Engineering Zoomcamp** (≈ 0,5 h)\
  O curso é gratuito e a turma ao vivo costuma começar em janeiro. Só quem acompanha a turma recebe certificado. Entre também no Slack da DataTalks.Club.\
  Links: [Inscrição no Data Engineering Zoomcamp](https://courses.datatalks.club/register/de-zoomcamp/) (EN) · [Slack da DataTalks.Club](https://datatalks.club/slack.html) (EN)

### Fase 1 · Python e ferramentas de engenheiro

**Período:** 12 de outubro a 20 de dezembro de 2026 · ≈ 93 h de estudo · **Situação:** Na fila (0/8)

**Objetivo:** Fazer com código o que você já faz no trabalho: extrair, tratar, validar e carregar dados.

_Use as disciplinas de programação e banco de dados do ADS para reforçar esta fase._

- [ ] **F1.1 · Python do zero ao intermediário** (≈ 25 h)\
  Variáveis, listas e dicionários, funções, leitura de arquivos e tratamento de erros. Faça os exercícios, não só as aulas.\
  Links: [Curso em Vídeo: Python 3, Mundo 1](https://www.youtube.com/playlist?list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6) (PT) · [Kaggle Learn: Python](https://www.kaggle.com/learn/python) (EN)
- [ ] **F1.2 · pandas para tratar dados** (≈ 15 h)\
  Ler CSV, Excel e SQL; limpar, juntar e agrupar tabelas; gravar em Parquet. É a versão em código das suas validações de migração.\
  Links: [Kaggle Learn: Pandas](https://www.kaggle.com/learn/pandas) (EN) · [Livro Python for Data Analysis](https://wesmckinney.com/book/) (EN)
- [ ] **F1.3 · Conecte o Python aos bancos que você já usa** (≈ 8 h)\
  SQLAlchemy com SQL Server, PostgreSQL, MySQL e Firebird. Aprenda a ler em lotes, para tabelas grandes, e a gravar sem duplicar registros.\
  Links: [Tutorial oficial do SQLAlchemy](https://docs.sqlalchemy.org/en/20/tutorial/index.html) (EN)
- [ ] **F1.4 · Git e GitHub no dia a dia** (≈ 5 h)\
  Commit, branch, pull request e .gitignore. Regra de ouro: nunca subir senha nem dado de cliente.\
  Links: [Livro Pro Git em português](https://git-scm.com/book/pt-br/v2) (PT)
- [ ] **F1.5 · Terminal Linux e Docker** (≈ 10 h)\
  Comandos básicos de terminal, containers e docker compose para subir PostgreSQL, SQL Server e Firebird na sua máquina em minutos.\
  Links: [Docker: primeiros passos](https://docs.docker.com/get-started/) (EN)
- [ ] **F1.6 · SQL avançado** (≈ 10 h)\
  Window functions, CTEs, índices e plano de execução. Resolva os 50 exercícios: esse tipo de questão aparece em quase toda entrevista de dados.\
  Links: [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/) (EN)
- [ ] **F1.7 · Automatize uma rotina no seu trabalho** (no trabalho)\
  Escolha uma extração ou validação de migração que você repete e faça em Python, com autorização do seu líder e sem tirar dados de clientes da empresa. Isso vira experiência real no currículo.
- [ ] **F1.8 · Projeto 1: Migrador de dados de ERP** (≈ 20 h)\
  Pipeline em Python que extrai de um banco legado (Firebird ou MySQL com dados fictícios), limpa, valida e carrega no PostgreSQL, gerando um relatório de divergências. Tudo sobe com docker compose e tem README com diagrama.\
  Links: [Faker, para gerar dados fictícios](https://faker.readthedocs.io/) (EN)

### Fase 2 · Engenharia de dados de ponta a ponta

**Período:** janeiro a março de 2027 · ≈ 91 h de estudo · **Situação:** Na fila (0/8)

**Objetivo:** Fazer o Data Engineering Zoomcamp com a turma: nuvem, orquestração, data warehouse, dbt, Spark e streaming.

_Se perder a turma de janeiro, siga pelo repositório no seu ritmo. Você aprende o mesmo, só não recebe o certificado._

- [ ] **F2.1 · Conceitos que caem em entrevista** (≈ 8 h)\
  ETL e ELT, data lake, data warehouse e lakehouse, batch e streaming, modelagem dimensional (fatos e dimensões), Parquet e particionamento.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.2 · Módulo 1: Docker, PostgreSQL, Terraform e Google Cloud** (≈ 10 h)\
  Infraestrutura como código e o primeiro contato com a nuvem.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.3 · Módulo 2: orquestração e data lake** (≈ 10 h)\
  Agendar, reprocessar e monitorar pipelines com Kestra, gravando no Cloud Storage.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.4 · Módulo 3: data warehouse no BigQuery** (≈ 8 h)\
  Particionamento, clusterização e boas práticas para gastar pouco.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.5 · Módulo 4: dbt** (≈ 10 h)\
  Transformar dados brutos em modelos prontos para análise, com testes e documentação. O dbt aparece com frequência nas vagas.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.6 · Módulos 5 e 6: plataforma de dados e Spark** (≈ 12 h)\
  Pipelines de ponta a ponta e processamento em lote com DataFrames e Spark SQL.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.7 · Módulo 7: streaming com Kafka** (≈ 8 h)\
  Eventos em tempo real, Kafka Streams e controle de esquemas.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **F2.8 · Projeto 2: projeto final do Zoomcamp** (≈ 25 h)\
  Pipeline completo com dados de varejo, por exemplo a base pública de e-commerce da Olist: ingestão, data lake, warehouse, dbt e painel. Passar na revisão por pares dá o certificado.\
  Links: [Base pública da Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (EN)

### Fase 3 · Databricks, Azure e certificação

**Período:** abril a início de junho de 2027 · ≈ 77 h de estudo · **Situação:** Na fila (0/6)

**Objetivo:** Dominar a combinação que mais aparece nas vagas brasileiras (SQL, Python, Spark e Databricks na Azure) e tirar a DP-750.

- [ ] **F3.1 · Databricks na prática** (≈ 22 h)\
  Spark e PySpark, Delta Lake, arquitetura medalhão (bronze, prata e ouro), Unity Catalog e jobs, tudo na Free Edition. Os cursos da Databricks Academy são gratuitos, vários em português, e alguns dão credenciais para o LinkedIn.\
  Links: [Databricks Academy](https://www.databricks.com/learn/training/home) (EN) · [Databricks Free Edition](https://www.databricks.com/learn/free-edition) (EN)
- [ ] **F3.2 · Azure para dados** (≈ 10 h)\
  Data Lake Storage, Data Factory, Key Vault e Entra ID, que a DP-750 cobra. Use a conta gratuita e apague os recursos ao fim de cada estudo para não gerar cobrança.\
  Links: [Conta gratuita da Azure](https://azure.microsoft.com/pt-br/free/) (PT)
- [ ] **F3.3 · Airflow básico** (≈ 8 h)\
  DAGs, agendamento e reprocessamento. Reescreva a orquestração do Projeto 1 em Airflow, que aparece com frequência nas vagas.\
  Links: [Astronomer Academy](https://academy.astronomer.io/) (EN) · [Documentação do Airflow](https://airflow.apache.org/docs/) (EN)
- [ ] **F3.4 · Projeto 3: Lakehouse de varejo no Databricks** (≈ 22 h)\
  Camadas bronze, prata e ouro em Delta Lake, job agendado, testes de qualidade e um painel com vendas por período, ticket médio e curva ABC de produtos. É o mundo comercial e de retaguarda que você conhece, sem a parte fiscal.\
  Links: [Base pública da Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (EN)
- [ ] **F3.5 · Certificação DP-750** (≈ 15 h)\
  Azure Databricks Data Engineer Associate: prova de 120 minutos, disponível em português. Antes de marcar, faça a avaliação prática gratuita da Microsoft.\
  Links: [Página da DP-750](https://learn.microsoft.com/pt-br/credentials/certifications/implementing-data-engineering-solutions-using-azure-databricks/) (PT) · [Avaliações práticas gratuitas](https://learn.microsoft.com/pt-br/credentials/certifications/practice-assessments-for-microsoft-certifications) (PT)
- [ ] **F3.6 · Marco: comece a se candidatar** (contínuo)\
  Com três projetos no GitHub e a DP-750, mire em Engenheiro de Dados júnior ou pleno e em Analista de Dados ou de Integração. Converse também no seu trabalho sobre assumir os pipelines de dados.

## Engenharia de IA (Trilha 2 · Fases 4 e 5)

Engenheiro de IA costuma ser o segundo passo: quem é contratado chega com 3,6 anos de experiência, em média, vindo de engenharia de software, ciência de dados ou engenharia de dados (LinkedIn, 2026). Estas fases preparam você enquanto já trabalha com dados.

### Fase 4 · Fundamentos de IA aplicada

**Período:** junho a setembro de 2027 · ≈ 107 h de estudo · **Situação:** Na fila (0/6)

**Objetivo:** Construir aplicações com LLMs: RAG, busca vetorial e avaliação, com o LLM Zoomcamp.

_O LLM Zoomcamp costuma começar em junho e dura cerca de 10 semanas. Confira a data na página de inscrição._

- [ ] **F4.1 · Como a IA generativa funciona** (≈ 10 h)\
  Tokens, janela de contexto, embeddings, temperatura, alucinação e custo por token. A trilha de fundamentos da Microsoft é gratuita e em português.\
  Links: [Fundamentos de IA do Azure](https://learn.microsoft.com/pt-br/credentials/certifications/azure-ai-fundamentals/) (PT) · [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) (EN)
- [ ] **F4.2 · Modelos no seu computador, sem pagar API** (≈ 6 h)\
  Rode modelos abertos pequenos com o Ollama e chame por Python. Assim você pratica sem cartão de crédito.\
  Links: [Ollama](https://ollama.com/) (EN)
- [ ] **F4.3 · APIs com FastAPI** (≈ 8 h)\
  Exponha seus pipelines e modelos como serviço: rotas, validação de dados e documentação automática.\
  Links: [FastAPI em português](https://fastapi.tiangolo.com/pt/) (PT)
- [ ] **F4.4 · LLM Zoomcamp** (≈ 50 h)\
  RAG, busca vetorial e híbrida, agentes, function calling, avaliação e monitoramento. Gratuito, com certificado para quem acompanha a turma.\
  Links: [Inscrição no LLM Zoomcamp](https://courses.datatalks.club/register/llm-zoomcamp/) (EN) · [Repositório do LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) (EN)
- [ ] **F4.5 · Machine learning básico** (≈ 8 h)\
  Regressão, classificação, treino e teste, métricas. O suficiente para conversar com cientistas de dados e entender o que as vagas chamam de ML.\
  Links: [Kaggle Learn: Intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning) (EN)
- [ ] **F4.6 · Projeto 4: Assistente de suporte de ERP com RAG** (≈ 25 h)\
  Responde dúvidas de usuários a partir de manuais e procedimentos, sempre citando a fonte, com um conjunto de perguntas de teste para medir o acerto. Use documentos públicos ou escritos por você, nunca material interno sem autorização.

### Fase 5 · Agentes, avaliação e produção

**Período:** outubro a dezembro de 2027 · ≈ 97 h de estudo · **Situação:** Na fila (0/6)

**Objetivo:** O que separa uma demonstração de um produto: agentes com ferramentas, dados para IA, avaliação e custo.

- [ ] **F5.1 · Agentes com ferramentas** (≈ 20 h)\
  Function calling, orquestração de várias etapas e MCP para conectar o agente a outros sistemas.\
  Links: [Hugging Face Agents Course](https://huggingface.co/learn/agents-course) (EN)
- [ ] **F5.2 · Dados para IA** (≈ 12 h)\
  Pipelines que alimentam a IA: ingestão de documentos, divisão em trechos, embeddings e busca vetorial no PostgreSQL com pgvector.\
  Links: [pgvector](https://github.com/pgvector/pgvector) (EN)
- [ ] **F5.3 · Avaliação e LLMOps** (≈ 15 h)\
  Conjunto de perguntas de teste versionado, métricas separadas para a busca e para a resposta, LLM como juiz calibrado contra avaliação humana, custo por resposta e latência.\
  Links: [Repositório do LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) (EN)
- [ ] **F5.4 · Projeto 5: Agente de mapeamento de dados** (≈ 30 h)\
  Recebe as estruturas de origem e de destino, como no seu trabalho, sugere o de-para das colunas, gera o SQL de transformação e valida a carga com testes. Junta dados e IA num problema que poucos candidatos conhecem por dentro.
- [ ] **F5.5 · Certificação AI-103** (≈ 20 h)\
  Azure AI App and Agent Developer Associate: agentes e IA generativa no Microsoft Foundry. Substituiu a AI-102 em 2026, tem 120 minutos e está disponível em português.\
  Links: [Página da AI-103](https://learn.microsoft.com/pt-br/credentials/certifications/exams/ai-103/) (PT) · [Avaliações práticas gratuitas](https://learn.microsoft.com/pt-br/credentials/certifications/practice-assessments-for-microsoft-certifications) (PT)
- [ ] **F5.6 · Marco: vagas de Engenheiro de IA** (contínuo)\
  Mire em vagas que juntam dados e IA: Engenheiro de IA, Engenheiro de ML e Engenheiro de Dados com foco em IA. Leve os projetos 4 e 5 para as entrevistas.

## Inglês do básico ao avançado (Trilha paralela · 20 a 30 minutos por dia)

Cinco níveis, um depois do outro, do A1 ao C1, só com material gratuito. Cada nível termina com um teste gratuito para medir sua evolução, e o conteúdo usa o que você já estuda na trilha técnica: aulas, documentação e projetos. Esta faixa não entra na porcentagem da trilha técnica; ela tem o próprio progresso.

### Nível 1 · Básico (A1 a A2)

**Período:** outubro a dezembro de 2026 · ≈ 33,5 h de estudo · **Situação:** Na fila (0/7)

**Objetivo:** Montar e entender frases simples, com a pronúncia certa desde o começo, e reconhecer as palavras que aparecem na tela do computador.

_Se o teste de nível der B1 ou mais, marque o que você já domina neste nível e siga para o próximo._

- [ ] **I1.1 · Descubra seu nível com um teste gratuito** (≈ 1 h)\
  Faça o EF SET de 50 minutos: é gratuito, corrige leitura e escuta e mostra seu nível no Quadro Europeu (de A1 a C2). Anote o resultado: você vai refazer o teste no fim de cada nível para medir a evolução.\
  Links: [EF SET, teste de nível gratuito](https://www.efset.org/) (EN)
- [ ] **I1.2 · Crie o hábito de 20 a 30 minutos por dia** (≈ 0,5 h)\
  De segunda a sexta, das 21h30 às 22h, como está na sua agenda. Pouco todo dia rende mais do que muito uma vez por semana. Deixe o celular e o VS Code em inglês: você aprende vocabulário sem perceber.
- [ ] **I1.3 · Gramática básica, explicada em português** (≈ 15 h)\
  Verbo to be, presente e passado simples, perguntas e negativas, artigos e preposições. Veja a explicação em português no canal da Carina Fragozo e faça os exercícios do British Council do nível A1 a A2.\
  Links: [English in Brazil, com Carina Fragozo](https://www.youtube.com/@carinafragozo) (PT) · [British Council: gramática A1 a A2](https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2) (EN)
- [ ] **I1.4 · Pronúncia desde o início** (≈ 5 h)\
  Os sons do inglês que não existem em português, como o th e as vogais curtas. Use o YouGlish para ouvir palavras da área em vídeos reais: data, query, schema, cache, deploy.\
  Links: [BBC Learning English: pronúncia](https://www.bbc.co.uk/learningenglish/english/features/pronunciation) (EN) · [YouGlish](https://youglish.com/) (EN)
- [ ] **I1.5 · Vocabulário de TI do dia a dia** (≈ 6 h)\
  Monte um baralho no Anki com as palavras que você vê no trabalho e nos cursos: file, folder, run, install, error, warning, table, column, row, query, load, merge. Revise 5 minutos por dia; o Anki mostra cada palavra na hora certa para você não esquecer.\
  Links: [Anki, flashcards gratuitos](https://apps.ankiweb.net/) (EN)
- [ ] **I1.6 · Primeiras leituras e escutas** (≈ 5 h)\
  Textos e áudios curtos com exercícios, no seu nível. Comece pelo A1 e passe para o A2 quando acertar quase tudo.\
  Links: [British Council: leitura A1](https://learnenglish.britishcouncil.org/free-resources/reading/a1) (EN) · [British Council: escuta A2](https://learnenglish.britishcouncil.org/free-resources/listening/a2) (EN)
- [ ] **I1.7 · Teste de fim de nível: meta A2** (≈ 1 h)\
  Refaça o EF SET e compare com o primeiro resultado. Chegou ao A2? Siga para o Nível 2. Se ainda não, repita as etapas em que sentiu mais dificuldade por mais algumas semanas.\
  Links: [EF SET, teste de nível gratuito](https://www.efset.org/) (EN)

### Nível 2 · Pré-intermediário (A2 a B1)

**Período:** janeiro a março de 2027 · ≈ 36 h de estudo · **Situação:** Na fila (0/6)

**Objetivo:** Acompanhar aulas técnicas com legenda em inglês e ler documentação com a ajuda do dicionário. Coincide com o Zoomcamp, que é todo em inglês.

- [ ] **I2.1 · Os tempos verbais que mais aparecem em TI** (≈ 12 h)\
  Present perfect ("the job has failed"), futuro com will e going to, comparativos, verbos modais (can, should, must) e a voz passiva simples ("the file is generated"). Comece pelas lições de nível B1.\
  Links: [British Council: gramática B1 a B2](https://learnenglish.britishcouncil.org/free-resources/grammar/b1-b2) (EN) · [English in Brazil, com Carina Fragozo](https://www.youtube.com/@carinafragozo) (PT)
- [ ] **I2.2 · 6 Minute English, duas vezes por semana** (≈ 8 h)\
  Episódios curtos sobre temas do dia a dia, com transcrição e vocabulário. Ouça uma vez sem ler, depois com a transcrição, e anote três palavras novas no Anki.\
  Links: [BBC Learning English: 6 Minute English](https://www.bbc.co.uk/learningenglish/english/features/6-minute-english) (EN)
- [ ] **I2.3 · Aulas do Zoomcamp com legenda em inglês** (≈ 6 h)\
  Assista com a legenda em inglês, não em português. Pause quando travar e anote os termos técnicos. É o mesmo tempo de estudo da trilha principal, agora servindo para as duas coisas.\
  Links: [Repositório do Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (EN)
- [ ] **I2.4 · Leia documentação de verdade** (≈ 6 h)\
  Uma seção por semana do tutorial oficial do Python, em inglês. Tente entender pelo contexto e pelo código; traduza só a frase que travar.\
  Links: [Tutorial oficial do Python](https://docs.python.org/3/tutorial/) (EN)
- [ ] **I2.5 · Commits e README em inglês** (≈ 3 h)\
  Mensagens de commit curtas, com o verbo no início ("Add data validation", "Fix date parsing"), e o README do Projeto 1 em inglês. O Write & Improve, da Cambridge, corrige textos curtos de graça.\
  Links: [Write & Improve, da Cambridge](https://writeandimprove.com/) (EN)
- [ ] **I2.6 · Teste de fim de nível: meta B1** (≈ 1 h)\
  Refaça o EF SET. Com B1 você já entende a maior parte das aulas técnicas e consegue escrever sobre seus projetos.\
  Links: [EF SET, teste de nível gratuito](https://www.efset.org/) (EN)

### Nível 3 · Intermediário (B1 a B2)

**Período:** abril a junho de 2027 · ≈ 33 h de estudo · **Situação:** Na fila (0/6)

**Objetivo:** Entender podcasts de tecnologia e começar a falar: explicar seu trabalho e seus projetos, devagar mas sem travar.

- [ ] **I3.1 · Gramática para conversar melhor** (≈ 10 h)\
  Condicionais ("if the load fails, we roll back"), orações relativas, discurso indireto e os phrasal verbs mais comuns em TI: set up, roll back, log in, figure out, run into.\
  Links: [British Council: gramática B1 a B2](https://learnenglish.britishcouncil.org/free-resources/grammar/b1-b2) (EN)
- [ ] **I3.2 · Podcasts de tecnologia** (≈ 8 h)\
  Escolha episódios sobre o que você estuda no momento e use a transcrição quando precisar. Se ficar rápido demais, reduza a velocidade para 0,9.\
  Links: [Talk Python To Me](https://talkpython.fm/) (EN) · [Data Engineering Podcast](https://www.dataengineeringpodcast.com/) (EN)
- [ ] **I3.3 · Comece a falar: repetição e gravação** (≈ 8 h)\
  Repita em voz alta, junto com o áudio, trechos do 6 Minute English (a técnica se chama shadowing). Uma vez por semana, grave 1 minuto explicando o que estudou e ouça de novo para notar os erros.\
  Links: [British Council: fala B1](https://learnenglish.britishcouncil.org/free-resources/speaking/b1) (EN) · [BBC Learning English: 6 Minute English](https://www.bbc.co.uk/learningenglish/english/features/6-minute-english) (EN)
- [ ] **I3.4 · Sua apresentação de 1 minuto** (≈ 4 h)\
  Quem você é, o que faz (integração e migração de dados de ERP) e o que está estudando. Escreva, corrija no Write & Improve, treine em voz alta e grave. Ela abre toda entrevista em inglês.\
  Links: [Write & Improve, da Cambridge](https://writeandimprove.com/) (EN)
- [ ] **I3.5 · LinkedIn também em inglês** (≈ 2 h)\
  O LinkedIn deixa criar o perfil em um segundo idioma. Faça a versão em inglês e publique o Projeto 3 com um texto curto em inglês.
- [ ] **I3.6 · Teste de fim de nível: meta B1 alto** (≈ 1 h)\
  Refaça o EF SET. A meta é estar perto do B2, que é o nível que muitas vagas pedem.\
  Links: [EF SET, teste de nível gratuito](https://www.efset.org/) (EN)

### Nível 4 · Intermediário superior (B2)

**Período:** julho a setembro de 2027 · ≈ 36 h de estudo · **Situação:** Na fila (0/5)

**Objetivo:** Conversar sobre tecnologia sem travar, fazer cursos inteiros em inglês e escrever e-mails e documentação com segurança.

- [ ] **I4.1 · Curso: falar inglês no trabalho** (≈ 15 h)\
  Speak English Professionally, do Georgia Tech: reuniões, chamadas de vídeo e telefone. Na inscrição, escolha a opção de assistir de graça, se aparecer; o certificado é pago e não é necessário.\
  Links: [Speak English Professionally (Coursera)](https://www.coursera.org/learn/speak-english-professionally) (EN)
- [ ] **I4.2 · Escuta sem legenda** (≈ 8 h)\
  Exercícios de escuta do nível B2 e trechos do LLM Zoomcamp sem legenda, nos assuntos que você já conhece.\
  Links: [British Council: escuta B2](https://learnenglish.britishcouncil.org/free-resources/listening/b2) (EN) · [Repositório do LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) (EN)
- [ ] **I4.3 · Conversa de verdade** (≈ 8 h)\
  Faça e responda perguntas em inglês no Slack da DataTalks.Club. Para falar, treine com um assistente de IA no modo de voz, pedindo que ele corrija seus erros no fim de cada conversa.\
  Links: [Slack da DataTalks.Club](https://datatalks.club/slack.html) (EN)
- [ ] **I4.4 · E-mails e documentação técnica** (≈ 4 h)\
  Pratique e-mails formais e textos de opinião do nível B2. Escreva a documentação do Projeto 4 em inglês.\
  Links: [British Council: escrita B2](https://learnenglish.britishcouncil.org/free-resources/writing/b2) (EN)
- [ ] **I4.5 · Teste de fim de nível: meta B2** (≈ 1 h)\
  Refaça o EF SET. Com B2 você já pode se candidatar a vagas que pedem inglês avançado.\
  Links: [EF SET, teste de nível gratuito](https://www.efset.org/) (EN)

### Nível 5 · Avançado (B2 a C1)

**Período:** outubro a dezembro de 2027 · ≈ 40 h de estudo · **Situação:** Na fila (0/6)

**Objetivo:** Fazer entrevistas de emprego em inglês, técnicas e comportamentais, e trabalhar com equipes de fora do Brasil.

- [ ] **I5.1 · Gramática avançada** (≈ 8 h)\
  Passivas avançadas, orações com particípio e formas de dar ênfase: o que deixa sua fala e sua escrita mais naturais.\
  Links: [British Council: gramática C1](https://learnenglish.britishcouncil.org/free-resources/grammar/c1) (EN)
- [ ] **I5.2 · Curso: inglês para a carreira** (≈ 12 h)\
  English for Career Development, da Universidade da Pensilvânia: busca de vagas, currículo, carta de apresentação e entrevista. Escolha a opção de assistir de graça, se aparecer.\
  Links: [English for Career Development (Coursera)](https://www.coursera.org/learn/careerdevelopment) (EN)
- [ ] **I5.3 · Entrevista comportamental com o método STAR** (≈ 8 h)\
  Prepare seis histórias reais do seu trabalho contadas em Situação, Tarefa, Ação e Resultado: uma migração difícil, um cliente exigente, um erro que você corrigiu, uma rotina que você automatizou. Treine em voz alta até contar cada uma em 2 minutos.\
  Links: [Tech Interview Handbook: entrevista comportamental](https://www.techinterviewhandbook.org/behavioral-interview/) (EN)
- [ ] **I5.4 · Entrevista técnica falando em inglês** (≈ 8 h)\
  Explique em voz alta a arquitetura dos projetos 3, 4 e 5 e resolva exercícios de SQL narrando o raciocínio em inglês, como se pede nas entrevistas. Grave e reveja.\
  Links: [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/) (EN)
- [ ] **I5.5 · Currículo e LinkedIn prontos em inglês** (≈ 3 h)\
  Revise a versão em inglês do LinkedIn e prepare o currículo em inglês para as vagas de Engenheiro de IA.
- [ ] **I5.6 · Teste final: meta C1** (≈ 1 h)\
  Refaça o EF SET. O resultado vem com um certificado gratuito que você pode colocar no LinkedIn.\
  Links: [EF SET, teste de nível gratuito](https://www.efset.org/) (EN)

## Certificações

| Certificação | Prova | Quando | Observação |
|---|---|---|---|
| [Azure Databricks Data Engineer Associate](https://learn.microsoft.com/pt-br/credentials/certifications/implementing-data-engineering-solutions-using-azure-databricks/) | DP-750 | Fase 3, até junho de 2027 | Lançada em 2026. 120 minutos, em português. É a principal da trilha de dados. |
| [Azure AI App and Agent Developer Associate](https://learn.microsoft.com/pt-br/credentials/certifications/exams/ai-103/) | AI-103 | Fase 5, dezembro de 2027 | Substituiu a AI-102 em 30/06/2026. 120 minutos, em português. |
| [Fabric Data Engineer Associate](https://learn.microsoft.com/pt-br/credentials/certifications/fabric-data-engineer-associate/) | DP-700 | Alternativa à DP-750 | Vale a pena se as vagas que você mirar pedirem Microsoft Fabric. Em agosto de 2026, cerca de 230 vagas no Brasil citavam a plataforma. |
| [Databricks Certified Data Engineer Associate](https://www.databricks.com/learn/certification/data-engineer-associate) | Databricks | Alternativa à DP-750 | Programa atualizado em maio de 2026. A Databricks costuma dar vouchers de 50% no Learning Festival; em 2026 foi em janeiro. |
| [Azure Data Fundamentals](https://learn.microsoft.com/pt-br/credentials/certifications/azure-data-fundamentals/) | DP-900 | Opcional, antes da Fase 3 | Prova de fundamentos. Serve como primeira certificação, mas não é pré-requisito da DP-750. |
| Azure Data Engineer Associate | DP-203 | Não faça | Aposentada desde 31/03/2025. Ainda aparece em roteiros antigos. |
| Azure AI Engineer Associate | AI-102 | Não faça | Aposentada desde 30/06/2026. Substituída pela AI-103. |
