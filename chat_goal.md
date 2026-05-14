# Stage 2 Chatbot Goal: LlamaIndex Text-to-SQL sobre sihrd5.duckdb

> Plano de implementacao para transformar os artefatos da Stage 1 em um chatbot funcional, auditavel e seguro para responder perguntas em portugues sobre o banco `sihrd5.duckdb`.

## Objetivo

Implementar um chatbot Text-to-SQL baseado em LlamaIndex que:

- receba perguntas em linguagem natural sobre dados hospitalares SIH/SUS;
- decida se a pergunta e respondivel, ambigua ou insegura;
- recupere contexto tecnico e semantico a partir dos artefatos da Stage 1;
- gere SQL DuckDB read-only;
- valide SQL, joins, metricas, escopo territorial e caveats antes de executar;
- execute a consulta contra `sihrd5.duckdb` em modo read-only;
- sintetize uma resposta em portugues com numeros, escopo, caveats e evidencia;
- seja avaliado contra o benchmark v2 de 100 perguntas ja existente.

A primeira versao so e considerada funcional quando responder um conjunto de perguntas reais do banco com SQL executado, validado e explicavel. Nao basta fazer uma demo que chama o LLM e retorna texto.

## Pesquisa LlamaIndex: decisoes para este projeto

### O que o LlamaIndex oferece

LlamaIndex e adequado para este caso porque combina:

- conectores e indices para contexto aumentado;
- query engines e retrievers para acesso natural a dados;
- agentes com ferramentas quando for necessario expor uma interface conversacional;
- Workflows para criar pipelines multi-etapa com eventos, validacao e observabilidade;
- integracoes com OpenAI para LLM e embeddings;
- mecanismos de observabilidade e avaliacao.

### Componentes relevantes

- `SQLDatabase`: wrapper do LlamaIndex sobre SQLAlchemy para expor bancos SQL.
- `NLSQLTableQueryEngine`: baseline pronto para Text-to-SQL quando as tabelas sao conhecidas.
- `SQLTableRetrieverQueryEngine`: consulta Text-to-SQL com recuperacao dinamica de tabelas, util quando o schema inteiro nao cabe no prompt.
- `SQLTableSchema`, `SQLTableNodeMapping`, `ObjectIndex`, `VectorStoreIndex`: caminho recomendado para indexar schemas com contexto adicional.
- `NLSQLRetriever`: opcao para separar geracao/execucao SQL da sintese de resposta.
- `Workflow`: melhor opcao para o nosso caso porque permite etapas explicitas de classificacao, recuperacao, geracao SQL, validacao, execucao e sintese.
- `FunctionAgent`: util depois, para uma camada de chat com ferramentas, mas nao deve ser o nucleo inicial do Text-to-SQL.
- `as_structured_llm` ou Pydantic Programs: devem ser usados para forcar saidas estruturadas, como plano SQL, justificativa, tabelas usadas e caveats.

### Decisao arquitetural

Usar LlamaIndex principalmente como framework de contexto, LLM, embeddings e Workflows, mas manter as regras criticas em codigo deterministico.

Nao usar `NLSQLTableQueryEngine` diretamente como nucleo final, porque ele executa o ciclo Text-to-SQL com pouca visibilidade sobre as regras especificas do projeto. Ele pode ser usado como baseline de comparacao ou smoke inicial.

O pipeline final deve ser um `Workflow` customizado:

1. Classificar a pergunta.
2. Recuperar tabelas, colunas, regras de join e exemplos relevantes.
3. Gerar um plano SQL estruturado.
4. Validar o plano e o SQL com regras deterministicas.
5. Executar em DuckDB read-only.
6. Sintetizar resposta baseada somente no resultado executado.
7. Registrar trace, SQL, resultado compacto, caveats e metrica de avaliacao.

## Estado local observado

- `.env` existe e contem `OPENAI_API_KEY`.
- `duckdb` esta instalado na `.venv` local.
- `llama_index`, `sqlalchemy`, `python-dotenv`, `sqlglot` e `pytest` ainda nao estao instalados na `.venv`.
- O benchmark v2 existe em `evaluation/ground_truth/stage1_questions_v2.jsonl` com 100 perguntas.
- `docs/stage2_readiness.md` define regras obrigatorias para o chatbot.
- `docs/generated/join_policy.csv` define quais joins sao seguros, restritos ou apenas para auditoria.
- A `.env` aparece como arquivo local nao versionado; o primeiro checkpoint de seguranca deve garantir que `.env` esteja no `.gitignore` antes de qualquer commit/push.

## Principios nao negociaveis

- Abrir `sihrd5.duckdb` somente em modo read-only.
- Nunca executar SQL mutante: `CREATE`, `ALTER`, `DROP`, `INSERT`, `UPDATE`, `DELETE`, `COPY`, `EXPORT`, `VACUUM`, `CHECKPOINT`, `ATTACH`, `INSTALL`, `LOAD`.
- Nao consultar tabelas de auditoria dbt como fonte de resposta de negocio, exceto em comandos explicitamente tecnicos.
- Nao usar relacoes rejeitadas como dimensoes descritivas.
- Nao esconder perda de populacao em joins com cobertura menor que `99.5%`.
- Diferenciar sempre municipio de residencia (`internacoes.MUNIC_RES`) de municipio do hospital (`hospital.MUNIC_MOV`).
- Declarar a base de metricas financeiras, por exemplo `VAL_TOT`, `VAL_SH`, `VAL_SP` ou `VAL_UTI`.
- Evitar multiplicar internacoes ao juntar `internacao_procedimento`; quando contar procedimentos, dizer que a unidade e ocorrencia de procedimento, nao internacao.
- Pedir esclarecimento para termos ambiguos como "custo", "producao", "mortalidade" e "local" sem denominador, periodo ou geografia.
- Validar UFs usando apenas codigos brasileiros validos; nao contar valores numericos invalidos de `municipios.SG_UF`.
- Toda resposta numerica deve vir de SQL executado, nao de conhecimento do modelo.

## Stack proposta

Dependencias minimas:

```text
duckdb
duckdb-engine
sqlalchemy
llama-index-core
llama-index-llms-openai
llama-index-embeddings-openai
python-dotenv
pydantic
sqlglot
pytest
```

Dependencias opcionais para uma etapa posterior:

```text
llama-index-callbacks-arize-phoenix
opentelemetry-distro
opentelemetry-exporter-otlp
```

Modelos iniciais:

- LLM de geracao SQL e sintese: configurar por `.env`, com default conservador no codigo.
- Embeddings de schema/contexto: `text-embedding-3-small`, salvo se custo/latencia indicar outro modelo.
- Temperatura: `0` ou valor muito baixo para geracao SQL.

Variaveis de ambiente esperadas:

```text
OPENAI_API_KEY=...
CHATBOT_DB_PATH=sihrd5.duckdb
CHATBOT_LLM_MODEL=...
CHATBOT_EMBED_MODEL=text-embedding-3-small
CHATBOT_MAX_ROWS=200
CHATBOT_QUERY_TIMEOUT_SECONDS=60
```

## Arquitetura de pacotes

Criar uma estrutura simples em `src/health_system_chatbot/`:

```text
src/health_system_chatbot/
|-- __init__.py
|-- config.py
|-- artifacts.py
|-- llm.py
|-- schema_context.py
|-- prompts.py
|-- models.py
|-- intent.py
|-- sql_generator.py
|-- sql_validator.py
|-- duckdb_executor.py
|-- answer_synthesizer.py
|-- workflow.py
|-- evaluation.py
`-- cli.py
```

Scripts de apoio:

```text
scripts/chat_smoke.py
scripts/evaluate_chatbot.py
```

Testes:

```text
tests/
|-- test_artifacts.py
|-- test_intent.py
|-- test_sql_validator.py
|-- test_duckdb_executor.py
|-- test_answer_synthesizer.py
|-- test_evaluation.py
`-- fixtures/
```

Resultados de avaliacao:

```text
evaluation/chatbot/
|-- results/
|-- traces/
`-- error_analysis/
```

## Contratos internos

### `QuestionIntent`

Campos minimos:

```text
status: answerable | needs_clarification | refused
reason: string
normalized_question: string
ambiguities: list[string]
required_caveats: list[string]
```

### `RetrievedContext`

Campos minimos:

```text
tables: list[string]
columns: list[string]
table_context: list[string]
join_policies: list[object]
data_quality_caveats: list[string]
ground_truth_examples: list[object]
```

### `SqlPlan`

Campos minimos:

```text
question: string
sql: string
tables_used: list[string]
columns_used: list[string]
metric_basis: list[string]
grain: hospitalization | procedure_occurrence | municipality_year | hospital | other
date_basis: string
geography_basis: residence | hospital | none | mixed
join_assumptions: list[string]
caveats: list[string]
```

### `ValidationResult`

Campos minimos:

```text
is_valid: bool
severity: info | warning | error
errors: list[string]
warnings: list[string]
required_clarification: string | null
safe_sql: string | null
```

### `ExecutionResult`

Campos minimos:

```text
sql: string
columns: list[string]
rows: list[object]
row_count: int
elapsed_seconds: float
result_hash: string
truncated: bool
```

### `ChatbotAnswer`

Campos minimos:

```text
answer_pt: string
sql: string
result_summary: string
caveats: list[string]
evidence: object
status: answered | clarified | refused | failed
```

## Checkpoints de implementacao

### Checkpoint 0: Seguranca e baseline do ambiente

- [ ] Confirmar branch e worktree antes de editar.

```bash
git status --short --branch
```

- [ ] Garantir que `.env` esta ignorado pelo Git.
- [ ] Confirmar que `OPENAI_API_KEY` esta setada sem imprimir o segredo.
- [ ] Confirmar que `sihrd5.duckdb` existe e abre em read-only.
- [ ] Confirmar dependencias presentes e ausentes.
- [ ] Criar arquivo de dependencias do chatbot sem remover dependencias existentes.

Validacao:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import duckdb
db = Path("sihrd5.duckdb")
print("db_exists", db.exists())
con = duckdb.connect(str(db), read_only=True)
print(con.execute("SELECT 1").fetchone()[0])
con.close()
PY
```

Aceite:

- `.env` nao aparece como arquivo a ser commitado.
- o banco abre em read-only.
- dependencias do chatbot estao instalaveis por comando reproduzivel.

### Checkpoint 1: Esqueleto do pacote e configuracao

- [ ] Criar pacote `src/health_system_chatbot/`.
- [ ] Criar `config.py` com carregamento de `.env`.
- [ ] Definir defaults para caminho do banco, modelos, limites de linhas e timeout.
- [ ] Criar `models.py` com os contratos Pydantic.
- [ ] Criar CLI minima que imprime configuracao segura sem segredos.

Validacao:

```bash
.venv/bin/python -m health_system_chatbot.cli --help
.venv/bin/python -m py_compile $(find src scripts -name '*.py')
```

Aceite:

- import do pacote funciona.
- nenhum segredo e exibido.
- configuracao falha de forma clara se faltar banco ou chave.

### Checkpoint 2: Loader dos artefatos da Stage 1

- [ ] Implementar `artifacts.py`.
- [ ] Ler `docs/stage2_readiness.md`.
- [ ] Ler `docs/generated/join_policy.csv`.
- [ ] Ler `docs/generated/table_metadata.csv`.
- [ ] Ler `docs/generated/column_profiles_exact.csv` e `column_profiles_approx.csv`.
- [ ] Ler `docs/business_dictionary.md`, `schema_catalog.md`, `relationship_map.md` e `data_quality_report.md`.
- [ ] Ler `evaluation/ground_truth/stage1_questions_v2.jsonl` para exemplos e avaliacao.
- [ ] Criar um resumo estruturado por tabela com: grao, colunas-chave, metricas, joins permitidos, joins restritos e caveats.

Validacao:

```bash
.venv/bin/python - <<'PY'
from health_system_chatbot.artifacts import load_stage1_context
ctx = load_stage1_context()
print(len(ctx.tables), len(ctx.join_policies), len(ctx.ground_truth))
PY
```

Aceite:

- loader encontra 100 itens de ground truth v2.
- loader reconhece relacoes `confirmed`, `likely` e `rejected`.
- loader expoe as regras de Stage 2 para o restante do pipeline.

### Checkpoint 3: Indice de contexto com LlamaIndex

- [ ] Criar `schema_context.py`.
- [ ] Construir documentos de contexto por tabela, usando os artefatos locais.
- [ ] Criar indice LlamaIndex para recuperar tabelas, colunas, caveats e exemplos.
- [ ] Usar `ObjectIndex`/`VectorStoreIndex` ou um `VectorStoreIndex` simples sobre documentos de schema.
- [ ] Persistir o indice em diretorio local ignoravel, por exemplo `.chatbot_index/`.
- [ ] Criar comando para rebuild do indice.

Validacao:

```bash
.venv/bin/python -m health_system_chatbot.cli index rebuild
.venv/bin/python -m health_system_chatbot.cli context "valor total por UF de residencia em 2020"
```

Aceite:

- perguntas sobre `VAL_TOT`, `MUNIC_RES`, `CNES`, CID e procedimento recuperam tabelas corretas.
- o contexto recuperado inclui join policy e caveats relevantes.
- o indice nao depende de consultar a internet em runtime.

### Checkpoint 4: Classificador de intencao e ambiguidades

- [ ] Criar `intent.py`.
- [ ] Implementar regras deterministicas antes do LLM para ambiguidades conhecidas.
- [ ] Usar LLM estruturado apenas quando a regra deterministica nao for suficiente.
- [ ] Classificar como `needs_clarification` perguntas com "custo", "producao", "mortalidade" ou "local" sem definicao suficiente.
- [ ] Recusar perguntas fora do escopo do banco.
- [ ] Permitir perguntas tecnicas sobre schema, qualidade dos dados e benchmark.

Casos minimos:

```text
"Qual foi o custo em SP?" -> needs_clarification
"Qual a mortalidade por UF?" -> needs_clarification se faltar denominador/date basis
"Quantas internacoes existem?" -> answerable
"Quantos pacientes unicos existem?" -> refused ou needs_clarification se nao houver identificador confiavel
```

Validacao:

```bash
.venv/bin/python -m pytest tests/test_intent.py
```

Aceite:

- ambiguidades da Stage 2 sao tratadas antes da geracao SQL.
- perguntas fora do escopo nao chegam ao executor.

### Checkpoint 5: Geracao SQL estruturada

- [ ] Criar `sql_generator.py`.
- [ ] Usar LlamaIndex LLM OpenAI com saida Pydantic `SqlPlan`.
- [ ] Promptar com:
  - pergunta normalizada;
  - contexto recuperado;
  - join policy relevante;
  - exemplos do ground truth v2 similares;
  - regras de DuckDB;
  - formato esperado de saida.
- [ ] Exigir que o modelo declare grao, metric basis, date basis e geography basis.
- [ ] Exigir que perguntas sobre residencia usem `MUNIC_RES`.
- [ ] Exigir que perguntas sobre hospital/local de atendimento usem `hospital.MUNIC_MOV`.
- [ ] Exigir que uso de `internacao_procedimento` declare unidade de procedimento.

Validacao:

```bash
.venv/bin/python -m health_system_chatbot.cli draft-sql "Qual foi o valor total por ano de entrada?"
```

Aceite:

- saida e parseada como `SqlPlan`.
- o SQL nao e executado nessa etapa.
- o plano declara bases semanticas suficientes para validacao.

### Checkpoint 6: Validador SQL deterministico

- [ ] Criar `sql_validator.py`.
- [ ] Usar `sqlglot` ou parser equivalente para validar AST.
- [ ] Bloquear multiplas statements.
- [ ] Permitir somente `SELECT` e `WITH`.
- [ ] Bloquear comandos mutantes e comandos com acesso a arquivos/extensoes.
- [ ] Validar tabelas contra allowlist dos artefatos Stage 1.
- [ ] Bloquear tabelas de auditoria como fonte de resposta de negocio.
- [ ] Validar que joins rejeitados sejam recusados, exceto em pergunta de auditoria.
- [ ] Exigir `LEFT JOIN` ou escopo explicito quando join policy exigir universo mapeado.
- [ ] Alertar quando `internacao_procedimento` aparece com `COUNT(*)` junto de metricas de internacao.
- [ ] Alertar quando `SG_UF` aparece sem filtro ou CTE de UFs validas.
- [ ] Exigir `LIMIT` para consultas exploratorias que retornam linhas detalhadas.
- [ ] Executar `EXPLAIN` antes da consulta real quando possivel.

Validacao:

```bash
.venv/bin/python -m pytest tests/test_sql_validator.py
```

Aceite:

- SQL inseguro e bloqueado.
- SQL com joins rejeitados e bloqueado.
- SQL com join restrito sem caveat gera erro ou clarificacao.
- SQL seguro retorna `safe_sql`.

### Checkpoint 7: Executor DuckDB read-only

- [ ] Criar `duckdb_executor.py`.
- [ ] Abrir conexao com `duckdb.connect(path, read_only=True)`.
- [ ] Executar apenas SQL validado.
- [ ] Medir latencia.
- [ ] Limitar linhas retornadas.
- [ ] Calcular hash compacto do resultado.
- [ ] Retornar colunas, amostra, row count, truncamento e erro estruturado.
- [ ] Fechar conexao apos execucao.

Validacao:

```bash
.venv/bin/python -m pytest tests/test_duckdb_executor.py
.venv/bin/python -m health_system_chatbot.cli run-sql "SELECT COUNT(*) AS total_internacoes FROM internacoes"
```

Aceite:

- executor nao aceita SQL sem `ValidationResult.is_valid=True`.
- executor nao muta o banco.
- resultado inclui `elapsed_seconds` e `result_hash`.

### Checkpoint 8: Sintese de resposta

- [ ] Criar `answer_synthesizer.py`.
- [ ] Gerar resposta em portugues baseada somente em `ExecutionResult`.
- [ ] Incluir valor principal, unidade, periodo, geografia e caveats.
- [ ] Incluir nota de escopo quando resultado usa registros mapeados.
- [ ] Incluir nota de `VAL_TOT` ou metricas financeiras usadas.
- [ ] Incluir nota de unidade quando usa procedimento.
- [ ] Nao inventar explicacoes clinicas alem do que o resultado suporta.
- [ ] Opcionalmente expor SQL com flag `--show-sql`.

Validacao:

```bash
.venv/bin/python -m pytest tests/test_answer_synthesizer.py
```

Aceite:

- resposta final cita caveats obrigatorios.
- resposta nao fala de dados nao consultados.
- resposta e legivel para usuario de saude, mas auditavel para desenvolvedor.

### Checkpoint 9: Workflow LlamaIndex ponta a ponta

- [ ] Criar `workflow.py`.
- [ ] Implementar eventos do pipeline:
  - `UserQuestionEvent`
  - `IntentEvent`
  - `ContextEvent`
  - `SqlDraftEvent`
  - `ValidationEvent`
  - `ExecutionEvent`
  - `AnswerEvent`
  - `FailureEvent`
- [ ] Usar uma entrada async unica, conforme recomendacao de Workflows.
- [ ] Registrar trace local de cada etapa.
- [ ] Fazer fallback controlado quando a validacao falhar:
  - uma tentativa de reparo SQL com erro estruturado;
  - se falhar novamente, resposta de clarificacao ou falha segura.

Validacao:

```bash
.venv/bin/python -m health_system_chatbot.cli ask "Quantas internacoes existem na tabela principal?" --show-sql
```

Aceite:

- pergunta simples passa de ponta a ponta.
- pergunta ambigua nao executa SQL.
- pergunta com join restrito inclui caveat ou pede clarificacao.

### Checkpoint 10: CLI funcional

- [ ] Implementar comandos:
  - `ask`
  - `draft-sql`
  - `validate-sql`
  - `run-sql`
  - `context`
  - `index rebuild`
  - `eval`
- [ ] Permitir `--show-sql`.
- [ ] Permitir `--json` para uso em avaliacao.
- [ ] Permitir `--limit` nos comandos de avaliacao.

Validacao:

```bash
.venv/bin/python -m health_system_chatbot.cli ask "Qual foi o valor total aprovado registrado em VAL_TOT?" --show-sql
.venv/bin/python -m health_system_chatbot.cli ask "Qual foi o custo por local?"
.venv/bin/python -m health_system_chatbot.cli ask "Qual foi a taxa bruta de mortalidade hospitalar por ano?" --show-sql
```

Aceite:

- CLI responde, clarifica ou recusa de forma estruturada.
- nenhum comando imprime segredo.
- erros sao legiveis e retornam exit code adequado.

## Checkpoints de teste

### Testes unitarios obrigatorios

- [ ] `test_artifacts.py`: loaders retornam contagens esperadas e regras criticas.
- [ ] `test_intent.py`: ambiguidades Stage 2.
- [ ] `test_sql_validator.py`: bloqueios de SQL perigoso e joins rejeitados.
- [ ] `test_duckdb_executor.py`: read-only, hash, limite de linhas.
- [ ] `test_answer_synthesizer.py`: caveats obrigatorios.
- [ ] `test_evaluation.py`: metricas de avaliacao e parsing do ground truth.

Comando:

```bash
.venv/bin/python -m pytest
```

### Testes sem OpenAI

Os testes unitarios devem rodar sem chamada externa. Usar fixtures e mocks para:

- LLM estruturado;
- embeddings;
- recuperador de contexto;
- executor em banco DuckDB temporario pequeno.

### Testes com OpenAI

Criar testes live marcados explicitamente, nunca como default:

```bash
.venv/bin/python -m pytest -m live_openai
```

Aceite:

- testes default nao gastam tokens.
- testes live exigem `OPENAI_API_KEY`.

## Checkpoints de avaliacao

### Dataset

Usar como dataset principal:

```text
evaluation/ground_truth/stage1_questions_v2.jsonl
```

Cada item tem pergunta, SQL esperado, tipo de resultado, dificuldade, resultado esperado e evidencia compacta.

### Avaliacao inicial

- [ ] Criar `scripts/evaluate_chatbot.py`.
- [ ] Rodar primeiro em 10 perguntas balanceadas por dificuldade.
- [ ] Rodar depois nas 100 perguntas.
- [ ] Salvar resultados em `evaluation/chatbot/results/`.

Comandos:

```bash
.venv/bin/python scripts/evaluate_chatbot.py --dataset evaluation/ground_truth/stage1_questions_v2.jsonl --limit 10
.venv/bin/python scripts/evaluate_chatbot.py --dataset evaluation/ground_truth/stage1_questions_v2.jsonl
```

Metricas minimas:

- `intent_accuracy`: classificacao correta entre resposta, clarificacao e recusa.
- `sql_valid_rate`: SQL passou no validador deterministico.
- `sql_execution_rate`: SQL executou sem erro.
- `result_match_rate`: resultado bate com evidencia quando comparacao deterministica for possivel.
- `caveat_recall`: caveats obrigatorios presentes.
- `latency_p50`, `latency_p95`, `cost_estimate`.
- `failure_by_difficulty`: falhas por L1-L5.

Comparacao de resultado:

- Para escalares: igualdade exata ou tolerancia numerica definida.
- Para rankings: comparar top N, chaves e metricas principais.
- Para series temporais: comparar dimensao temporal e valores agregados.
- Para respostas com SQL equivalente mas ordem diferente: normalizar ordenacao quando o ground truth nao depender da ordem.
- Nao usar LLM-as-judge como criterio principal da primeira versao. Ele pode ser um diagnostico auxiliar depois.

Aceite da primeira versao funcional:

- 10 perguntas smoke passam de ponta a ponta.
- 100 perguntas geram relatorio completo, mesmo que a acuracia inicial ainda nao seja alta.
- Nenhuma pergunta ambigua executa SQL sem clarificacao.
- Nenhum SQL inseguro passa no validador.
- Cada resposta executada registra SQL, caveats, hash e latencia.

## Primeira iteracao de melhoria

Depois do primeiro baseline nas 100 perguntas:

### 1. Classificar falhas

Salvar `evaluation/chatbot/error_analysis/iteration_001.md` com categorias:

- recuperacao de tabela errada;
- coluna errada;
- join sem caveat;
- uso incorreto de `MUNIC_RES` vs `MUNIC_MOV`;
- multiplicacao por `internacao_procedimento`;
- metrica financeira ambigua;
- SQL DuckDB invalido;
- consulta lenta;
- resposta sem caveat;
- falha de parsing estruturado;
- pergunta deveria ser clarificacao ou recusa.

### 2. Corrigir na ordem certa

Prioridade de correcao:

1. Regras deterministicas de seguranca e semantica.
2. Contexto de schema e join policy.
3. Exemplos few-shot do ground truth v2.
4. Prompt de geracao SQL.
5. Prompt de sintese.
6. Otimizacao de performance.

Nao ajustar prompts antes de confirmar se a falha era uma regra codificavel.

### 3. Rodar novamente

Comandos:

```bash
.venv/bin/python scripts/evaluate_chatbot.py --dataset evaluation/ground_truth/stage1_questions_v2.jsonl --output evaluation/chatbot/results/iteration_002.json
```

Aceite da iteracao:

- melhora mensuravel em relacao a `iteration_001`;
- nenhuma regressao em bloqueios de seguranca;
- pelo menos um subconjunto de perguntas L1-L3 fica confiavel para uso interativo;
- principais falhas restantes ficam documentadas com proximo passo claro.

## Marcos de entrega

### Marco A: Chatbot minimo seguro

- Configuracao, artifacts loader, validador e executor prontos.
- CLI consegue responder perguntas com SQL manual validado.
- Testes unitarios de seguranca passam.

### Marco B: LlamaIndex gerando SQL

- Indice de contexto criado.
- LLM gera `SqlPlan` estruturado.
- Workflow executa pergunta simples de ponta a ponta.
- Perguntas ambiguas sao clarificadas antes de SQL.

### Marco C: Benchmark automatizado

- Avaliador roda contra ground truth v2.
- Resultados ficam salvos em `evaluation/chatbot/results/`.
- Falhas ficam classificadas em `error_analysis`.

### Marco D: Primeira melhoria

- Uma iteracao de melhoria e aplicada com base nas falhas.
- Smoke set passa de ponta a ponta.
- O chatbot ja responde perguntas reais sobre o banco com caveats e SQL auditavel.

## Perguntas smoke iniciais

Usar estas perguntas para validar a primeira versao:

```text
Quantas internacoes existem na tabela principal?
Qual e o valor total aprovado registrado em VAL_TOT?
Quantas internacoes ocorreram por ano de entrada?
Qual foi a taxa bruta de mortalidade hospitalar por ano?
Quais UFs tiveram maior valor total por municipio de residencia mapeado?
Qual hospital teve maior volume em cada UF do estabelecimento?
Quais procedimentos tiveram maior valor medio por ocorrencia entre os com pelo menos 10 mil ocorrencias?
Qual foi a taxa de internacoes por 1.000 habitantes por UF e ano?
Qual foi o custo por local?
Quantos pacientes unicos existem na base?
```

Resultados esperados:

- As 8 primeiras devem responder com SQL executado e caveats quando aplicavel.
- "Qual foi o custo por local?" deve pedir esclarecimento.
- "Quantos pacientes unicos existem na base?" deve recusar ou pedir esclarecimento se nao existir identificador confiavel de paciente.

## Fontes consultadas

- LlamaIndex Framework: `https://developers.llamaindex.ai/python/framework/`
- LlamaIndex Installation and OpenAI setup: `https://developers.llamaindex.ai/python/framework/getting_started/installation/`
- LlamaIndex Structured Data guide: `https://developers.llamaindex.ai/python/framework/understanding/putting_it_all_together/structured_data/`
- LlamaIndex Text-to-SQL guide: `https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/`
- LlamaIndex SQL Query Engine with DuckDB: `https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/duckdb_sql_query/`
- LlamaIndex Advanced Text-to-SQL Workflows: `https://developers.llamaindex.ai/python/examples/workflow/advanced_text_to_sql/`
- LlamaIndex Workflows introduction: `https://developers.llamaindex.ai/python/llamaagents/workflows/`
- LlamaIndex FunctionAgent/AgentWorkflow basics: `https://developers.llamaindex.ai/python/examples/agent/agent_workflow_basic/`
- LlamaIndex Observability: `https://developers.llamaindex.ai/python/framework/module_guides/observability/`
- LlamaIndex Structured Outputs: `https://docs.llamaindex.ai/en/stable/examples/structured_outputs/structured_outputs/`
