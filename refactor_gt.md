# Refactor Ground Truth V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refatorar `ground_truth_v2.json` ate que todas as perguntas finais sejam coerentes com o contexto documentado, tenham SQL correto para o schema real do `sihrd5.duckdb`, executem com sucesso e possuam evidencia reprodutivel de validacao.

**Architecture:** Tratar `ground_truth_v2.json` como fonte editavel, mas sincronizar o formato final com o contrato usado pelo chatbot (`GroundTruthItem` em `src/health_system_chatbot/models.py`). A validacao deve ser automatizada em duas camadas: checks estaticos de schema/semantica e reexecucao completa no DuckDB read-only com hashes de resultado.

**Tech Stack:** Python 3, DuckDB, Pydantic, JSON/JSONL, `pytest`, scripts existentes `scripts/verify_stage1.py` e artefatos em `docs/generated/`.

---

## Success Criteria

- `ground_truth_v2.json` fica em formato canonico e validavel, sem campos legados ambiguos como `question`/`query` como unica fonte.
- Toda pergunta final tem `question_pt`, `sql`, `difficulty`, `tables_used`, `columns_used`, `expected_result_type`, `assumptions`, `data_quality_notes`, `semantic_disposition` e `validation_evidence`.
- Toda SQL final e read-only, comeca com `SELECT` ou `WITH`, nao usa tabela/coluna inexistente e executa contra `sihrd5.duckdb`.
- Toda pergunta final esta alinhada com a granularidade real do banco: internacao/AIH, ocorrencia de procedimento, hospital, municipio-ano ou auditoria.
- Perguntas que dizem "pacientes" sao reescritas para "internacoes de pacientes" quando nao houver chave real de paciente.
- Perguntas territoriais usam `CO_MUNICIPIO_6D`, `NO_MUNICIPIO` e `SG_UF`.
- Perguntas com UF filtram as 27 UFs brasileiras validas ou declaram que estao auditando valores invalidos.
- Perguntas que usam `MUNIC_RES -> municipios` declaram "considerando apenas municipios de residencia mapeados" ou usam `LEFT JOIN` com bucket sem correspondencia.
- Perguntas de `RACA_COR`, `INSTRU`, `VINCPREV`, `CBOR`, `ETNIA`, `DIAG_SECUN` e `CID_MORTE` respeitam `docs/generated/join_policy.csv`.
- Perguntas sobre UTI declaram se medem marcador assistencial (`MARCA_UTI`) ou valor/cobranca (`VAL_UTI`).
- Perguntas de permanencia nao usam `DIAS_PERM` como verdade sem caveat; quando o objetivo for permanencia real, usar `date_diff('day', DT_INTER, DT_SAIDA)` e documentar a premissa.
- Perguntas sobre indicadores socioeconomicos usam somente colunas existentes em `socioeconomico`: `QT_POPULACAO`, `VL_PIB_PERCAPITA`, `QT_OBITOS_INFANTIS`, `QT_NASCIDOS_VIVOS`, `VL_MORT_INFANTIL`, `QT_LEITOS_SUS`, `VL_LEITOS_SUS_1000`, `QT_MEDICOS`, `VL_MEDICOS_1000`.
- Todos os itens finais possuem evidencia em `evaluation/ground_truth/query_results_v2/`.
- `scripts/verify_stage1.py --version v2` passa.
- Um novo verificador especifico para `ground_truth_v2.json` passa e reexecuta todas as queries finais.

## Non-Goals

- Nao alterar o conteudo do `sihrd5.duckdb`.
- Nao criar metricas dependentes de fontes ausentes, como Bolsa Familia, IDHM ou esgotamento sanitario, sem antes adicionar essas fontes ao banco.
- Nao usar o ground truth como rota deterministica do chatbot em runtime. Ele serve para avaliacao.
- Nao aceitar uma query apenas porque executa; a semantica precisa bater com a pergunta e com a documentacao.

## Current Evidence

Relatorio base: `evaluation/ground_truth/ground_truth_v2_review.md`.

Resumo atual do arquivo raiz:

| classe | quantidade |
| --- | ---: |
| perguntas em `ground_truth_v2.json` | 132 |
| executam no DuckDB | 76 |
| falham no DuckDB | 56 |
| executam sem ressalva imediata | 46 |
| executam com ressalva semantica | 30 |

Categorias de correcao ja identificadas:

| categoria | IDs |
| --- | --- |
| Colunas antigas de municipio/geografia | `GT006`, `GT018`, `GT019`, `GT028`, `GT031`, `GT032`, `GT038`, `GT049`, `GT051`, `GT072`, `GT073`, `GT074`, `GT075`, `GT076`, `GT077`, `GT080`, `GT083`, `GT086`, `GT087`, `GT088`, `GT093`, `GT102`, `GT103`, `GT112`, `GT113`, `GT120`, `GT121`, `GT123`, `GT124`, `GT128`, `GT130`, `GT132`, `GT134`, `GT135` |
| Coluna CID antiga `CD_DESCRICAO` | `GT014`, `GT015`, `GT035`, `GT039`, `GT048`, `GT069`, `GT070`, `GT078`, `GT082`, `GT090`, `GT092`, `GT116`, `GT127`, `GT129` |
| Tabela inexistente `atendimentos` | `GT021`, `GT068`, `GT079`, `GT081`, `GT084`, `GT122`, `GT131` |
| Modelo socioeconomico antigo ou indicador ausente | `GT040`, `GT073`, `GT074`, `GT123`, `GT135` |
| `ESPEC` hard-coded com significado errado | `GT010`, `GT019`, `GT027`, `GT089`, `GT114`, `GT130`, `GT107`, `GT117` |
| UTI definida por `VAL_UTI > 0` sem deixar isso claro | `GT007`, `GT023`, `GT027`, `GT041`, `GT088`, `GT117`, `GT118`, `GT125`, `GT128`, `GT133` |
| Pergunta fala "pacientes", mas SQL conta internacoes/AIHs | `GT011`, `GT012`, `GT013`, `GT033`, `GT037`, `GT042`, `GT044`, `GT062`, `GT065`, `GT070`, `GT076`, `GT078`, `GT082`, `GT109`, `GT114`, `GT119`, `GT131` |
| Joins rejeitados pela politica atual | `GT065`, `GT071`, `GT083`, `GT108` |
| Problemas pontuais | `GT017`, `GT024`, `GT030`, `GT055`, `GT091`, `GT133` |

## Target Format

`ground_truth_v2.json` deve ser um JSON array. Cada item final deve usar esta estrutura:

```json
{
  "id": "GT001",
  "persona": "Analista DATASUS/SIH",
  "question_pt": "Quantas internacoes foram registradas no total?",
  "business_intent": "Medir o volume total de internacoes/AIHs no fato principal.",
  "difficulty": "L1",
  "difficulty_rationale": "L1: uma tabela, contagem simples, sem join.",
  "sql": "SELECT COUNT(*) AS total_internacoes FROM internacoes",
  "tables_used": ["internacoes"],
  "columns_used": ["internacoes.N_AIH"],
  "expected_result_type": "scalar",
  "execution_status": "passed",
  "row_count": 1,
  "result_summary": "Resultado unico: total_internacoes=183877219.",
  "validation_evidence": "evaluation/ground_truth/query_results_v2/GT001.json",
  "assumptions": "Uma linha em internacoes representa uma internacao/AIH.",
  "data_quality_notes": "Sem caveat bloqueante para contagem total.",
  "semantic_disposition": "accepted"
}
```

Campos legados podem existir apenas durante a migracao, mas o estado final nao deve depender de:

- `question` no lugar de `question_pt`;
- `query` no lugar de `sql`;
- `tables` no lugar de `tables_used`;
- `difficulty` com valores `easy`, `medium`, `hard`.

Mapeamento de dificuldade:

| legado | canonico inicial |
| --- | --- |
| `easy` | `L1` ou `L2`, decidido por complexidade real |
| `medium` | `L2` ou `L3`, decidido por joins/agregacao |
| `hard` | `L4` ou `L5`, decidido por janelas, CTEs, taxas, auditoria ou caveats |

## Files

- Modify: `ground_truth_v2.json`
  - Fonte revisada em formato JSON array canonico.
- Create: `evaluation/ground_truth/ground_truth_v2_refactor_audit.csv`
  - Uma linha por ID original com decisao `keep`, `rewrite`, `replace`, `drop`, motivo e ID final.
- Create: `evaluation/ground_truth/query_results_v2/GT*.json`
  - Evidencia de execucao das queries finais do arquivo raiz.
- Modify: `evaluation/ground_truth/stage1_questions_v2.jsonl`
  - Espelho JSONL do ground truth final para o avaliador do chatbot.
- Modify: `evaluation/ground_truth/stage1_questions_v2.md`
  - Versao legivel do ground truth final.
- Modify: `evaluation/ground_truth/manifest.json`
  - Contagens, distribuicao de dificuldade e paths de evidencia.
- Modify: `docs/generated/ground_truth_semantic_audit.csv`
  - Auditoria semantica final.
- Create: `scripts/validate_ground_truth_v2_json.py`
  - Validador especifico para `ground_truth_v2.json`.
- Create: `scripts/sync_ground_truth_v2.py`
  - Sincroniza `ground_truth_v2.json` para JSONL, Markdown, evidencias e manifest.
- Modify: `scripts/verify_stage1.py`
  - Incluir verificacao de consistencia entre `ground_truth_v2.json` e `stage1_questions_v2.jsonl`.
- Create: `tests/test_ground_truth_v2_contract.py`
  - Testes unitarios leves do formato e dos gates estaticos.

## Canonical Schema Reminders

Use estes nomes reais no refactor:

| conceito | tabela/coluna correta |
| --- | --- |
| Internacoes | `internacoes` |
| Procedimentos por internacao | `internacao_procedimento` |
| Cadastro de procedimentos | `procedimentos` |
| Municipio | `municipios.CO_MUNICIPIO_6D`, `municipios.NO_MUNICIPIO`, `municipios.SG_UF` |
| Diagnostico CID | `cid.CID`, `cid.DESCRICAO`, `cid.DS_CATEGORIA`, `cid.DS_GRUPO`, `cid.DS_CAPITULO` |
| Hospital | `hospital.CNES`, `hospital.NO_HOSPITAL`, `hospital.MUNIC_MOV` |
| Socioeconomico | `socioeconomico.CO_MUNICIPIO_6D`, `socioeconomico.NU_ANO`, indicadores em colunas largas |
| Sexo | `sexo.SEXO`, `sexo.DESCRICAO` |
| Especialidade | `especialidade.ESPEC`, `especialidade.DESCRICAO` |
| UTI assistencial | `internacoes.MARCA_UTI <> 0`, quando a pergunta for uso/marcador |
| Custo/valor de UTI | `internacoes.VAL_UTI`, quando a pergunta for valor/cobranca |
| Permanencia calculada | `date_diff('day', DT_INTER, DT_SAIDA)`, salvo pergunta explicitamente sobre `DIAS_PERM` |

## Task 1: Baseline e Backup

**Files:**
- Read: `ground_truth_v2.json`
- Read: `evaluation/ground_truth/ground_truth_v2_review.md`
- Create: `evaluation/ground_truth/ground_truth_v2_refactor_audit.csv`

- [ ] **Step 1: Registrar estado inicial**

Run:

```bash
./.venv/bin/python - <<'PY'
import json
from pathlib import Path
items = json.loads(Path("ground_truth_v2.json").read_text(encoding="utf-8"))
ids = [item["id"] for item in items]
print({"items": len(items), "first": ids[0], "last": ids[-1]})
print("missing", [f"GT{i:03d}" for i in range(1, 136) if f"GT{i:03d}" not in ids])
PY
```

Expected:

```text
{'items': 132, 'first': 'GT001', 'last': 'GT135'}
missing ['GT016', 'GT020', 'GT045']
```

- [ ] **Step 2: Criar auditoria de decisao por ID**

Create `evaluation/ground_truth/ground_truth_v2_refactor_audit.csv` with this header:

```csv
original_id,final_id,decision,execution_status_before,semantic_status_before,decision_reason,question_action,sql_action,validation_status_after,evidence_path
```

Decision values allowed:

```text
keep
rewrite
replace
drop
```

- [ ] **Step 3: Preencher a coluna `execution_status_before`**

Use the results from `evaluation/ground_truth/ground_truth_v2_review.md`:

```text
ok
error
```

Expected completion evidence:

```bash
./.venv/bin/python - <<'PY'
import csv
rows = list(csv.DictReader(open("evaluation/ground_truth/ground_truth_v2_refactor_audit.csv", encoding="utf-8")))
assert len(rows) == 132
assert set(rows[0]) == {
    "original_id", "final_id", "decision", "execution_status_before",
    "semantic_status_before", "decision_reason", "question_action",
    "sql_action", "validation_status_after", "evidence_path"
}
print("audit_rows=132")
PY
```

## Task 2: Implementar Validador Estatico do JSON

**Files:**
- Create: `scripts/validate_ground_truth_v2_json.py`
- Create: `tests/test_ground_truth_v2_contract.py`

- [ ] **Step 1: Definir contrato de item**

The validator must require exactly these semantic fields for every final item:

```python
REQUIRED_FIELDS = {
    "id",
    "persona",
    "question_pt",
    "business_intent",
    "difficulty",
    "difficulty_rationale",
    "sql",
    "tables_used",
    "columns_used",
    "expected_result_type",
    "execution_status",
    "row_count",
    "result_summary",
    "validation_evidence",
    "assumptions",
    "data_quality_notes",
    "semantic_disposition",
}
```

Allowed difficulties:

```python
ALLOWED_DIFFICULTIES = {"L1", "L2", "L3", "L4", "L5"}
```

Allowed result types:

```python
ALLOWED_RESULT_TYPES = {
    "scalar",
    "distribution",
    "ranking",
    "time_series",
    "comparison",
    "data_quality_finding",
}
```

Allowed semantic dispositions:

```python
ALLOWED_DISPOSITIONS = {
    "accepted",
    "accepted_with_explicit_scope",
    "valid_with_caveats",
}
```

- [ ] **Step 2: Implement static SQL guardrails**

The validator must fail on these patterns:

```python
FORBIDDEN_SQL = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|EXPORT|IMPORT|ATTACH|DETACH|VACUUM|CALL)\b"
LEGACY_PATTERNS = [
    " atendimentos ",
    "codigo_6d",
    ".nome",
    ".estado",
    "CD_DESCRICAO",
    " metrica ",
    " valor ",
    "bolsa_familia",
    "idhm",
    "esgotamento_sanitario",
]
```

Normalize SQL before checking by lowercasing and collapsing whitespace.

- [ ] **Step 3: Add tests for the validator**

Run:

```bash
./.venv/bin/python -m pytest tests/test_ground_truth_v2_contract.py -q
```

Expected after implementation:

```text
passed
```

Minimum test cases:

```python
def test_rejects_legacy_municipio_columns():
    sql = "SELECT m.nome FROM municipios m WHERE m.estado = 'RS'"
    assert "m.nome" in collect_static_sql_errors(sql)
    assert "m.estado" in collect_static_sql_errors(sql)


def test_rejects_missing_atendimentos_table():
    sql = "SELECT COUNT(*) FROM atendimentos"
    assert "atendimentos" in collect_static_sql_errors(sql)


def test_accepts_current_municipio_columns():
    sql = "SELECT m.NO_MUNICIPIO FROM municipios m WHERE m.SG_UF = 'RS'"
    assert collect_static_sql_errors(sql) == []
```

## Task 3: Corrigir Formato do `ground_truth_v2.json`

**Files:**
- Modify: `ground_truth_v2.json`

- [ ] **Step 1: Converter campos legados**

For each item:

| legacy | canonical |
| --- | --- |
| `question` | `question_pt` |
| `query` | `sql` |
| `tables` | `tables_used` |
| `notes` | split into `assumptions` and `data_quality_notes` |

- [ ] **Step 2: Converter dificuldade**

Use this rule as first pass:

```text
easy + one table + scalar -> L1
easy + grouping/order -> L2
medium + one table aggregation/filter/grouping -> L2
medium + confirmed joins -> L3
hard + CTE/window/rate/temporal comparison -> L4
hard + audit/data-quality/caveated metric -> L5
```

- [ ] **Step 3: Populate missing fields**

Each item must include a concrete `business_intent`, `difficulty_rationale`, `expected_result_type`, `assumptions`, `data_quality_notes`, and `semantic_disposition`.

Example for a simple scalar:

```json
{
  "business_intent": "Medir o volume total de internacoes/AIHs no fato principal.",
  "difficulty_rationale": "L1: uma tabela, contagem simples, sem join.",
  "expected_result_type": "scalar",
  "assumptions": "Uma linha em internacoes representa uma internacao/AIH.",
  "data_quality_notes": "Sem caveat bloqueante para contagem total.",
  "semantic_disposition": "accepted"
}
```

Validation:

```bash
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --static-only
```

Expected:

```text
PASS static_format
```

## Task 4: Corrigir Erros de Schema

**Files:**
- Modify: `ground_truth_v2.json`
- Modify: `evaluation/ground_truth/ground_truth_v2_refactor_audit.csv`

- [ ] **Step 1: Replace municipio columns**

Use:

```sql
m.CO_MUNICIPIO_6D
m.NO_MUNICIPIO
m.SG_UF
```

Do not use:

```sql
m.codigo_6d
m.nome
m.estado
```

- [ ] **Step 2: Replace CID description column**

Use:

```sql
c.DESCRICAO
```

Do not use:

```sql
c.CD_DESCRICAO
```

- [ ] **Step 3: Replace `atendimentos`**

Use:

```sql
internacao_procedimento ip
```

Join pattern:

```sql
FROM internacao_procedimento ip
JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA
```

If the question also needs admission attributes:

```sql
FROM internacao_procedimento ip
JOIN internacoes i ON ip.N_AIH = i.N_AIH
JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA
```

- [ ] **Step 4: Replace unsupported socioeconomics**

Drop or replace questions that require unavailable columns:

| unsupported concept | allowed replacement |
| --- | --- |
| Bolsa Familia | `VL_PIB_PERCAPITA`, `QT_POPULACAO`, `VL_MORT_INFANTIL`, `QT_LEITOS_SUS`, `QT_MEDICOS` |
| IDHM | `VL_PIB_PERCAPITA` or remove question |
| esgotamento sanitario | remove question or replace with available health infrastructure metric |

Validation:

```bash
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --static-only
```

Expected:

```text
PASS static_sql_schema_names
```

## Task 5: Corrigir Semantica das Perguntas

**Files:**
- Modify: `ground_truth_v2.json`
- Modify: `evaluation/ground_truth/ground_truth_v2_refactor_audit.csv`

- [ ] **Step 1: Rewrite patient wording**

If the SQL counts rows in `internacoes`, rewrite:

```text
pacientes
```

to:

```text
internacoes de pacientes
```

Example:

```text
Antes: Quantos pacientes do sexo masculino foram internados?
Depois: Quantas internacoes de pacientes do sexo masculino foram registradas?
```

- [ ] **Step 2: Replace wrong `ESPEC` assumptions**

Use joins to `especialidade` when the question names the specialty.

Obstetric example:

```sql
JOIN especialidade e ON i.ESPEC = e.ESPEC
WHERE e.DESCRICAO ILIKE '%OBSTETRIC%'
```

Psychiatry: only keep the question if the current `especialidade` table has a psychiatry category. If not, replace it with a procedure/CID-based psychiatry question using documented fields:

```sql
WHERE i.DIAG_PRINC LIKE 'F%'
```

and phrase the question as:

```text
Quantas internacoes com diagnostico principal do capitulo de transtornos mentais e comportamentais resultaram em obito?
```

- [ ] **Step 3: Separate UTI usage from UTI value**

For use/marcador:

```sql
WHERE i.MARCA_UTI <> 0
```

For financial value:

```sql
WHERE i.VAL_UTI > 0
```

The question must say either:

```text
com marcador de UTI
```

or:

```text
com valor de UTI registrado
```

- [ ] **Step 4: Fix permanence metrics**

For real length of stay:

```sql
date_diff('day', i.DT_INTER, i.DT_SAIDA)
```

For explicit field audit:

```sql
i.DIAS_PERM
```

Question wording must say:

```text
segundo a diferenca entre data de entrada e data de saida
```

or:

```text
segundo o campo DIAS_PERM
```

- [ ] **Step 5: Enforce join policy**

For `MUNIC_RES -> municipios`, either:

```sql
LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D
```

with bucket:

```sql
COALESCE(m.SG_UF, 'SEM_MUNICIPIO_MAPEADO')
```

or inner join with question text:

```text
considerando apenas internacoes com municipio de residencia mapeado
```

For `RACA_COR` and `INSTRU`, prefer `LEFT JOIN` with bucket. If using inner join, classify as audit or explicit mapped-scope question.

Validation:

```bash
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --semantic-only
```

Expected:

```text
PASS semantic_policy
```

## Task 6: Executar Todas as Queries e Gerar Evidencia

**Files:**
- Create/Modify: `evaluation/ground_truth/query_results_v2/GT*.json`
- Modify: `ground_truth_v2.json`

- [ ] **Step 1: Run execution validator**

Run:

```bash
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --execute --db sihrd5.duckdb
```

Expected:

```text
PASS executed=<final_count>
errors=0
semantic_failures=0
hash_mismatches=0
```

- [ ] **Step 2: Evidence file contract**

Each evidence file must include:

```json
{
  "id": "GT001",
  "question_pt": "Quantas internacoes foram registradas no total?",
  "sql": "SELECT COUNT(*) AS total_internacoes FROM internacoes",
  "executed_at": "2026-05-14T00:00:00Z",
  "duration_seconds": 0.01,
  "performance_class": "fast",
  "row_count": 1,
  "columns": ["total_internacoes"],
  "preview_rows": [{"total_internacoes": 183877219}],
  "result_hash": "<sha256>",
  "semantic_disposition": "accepted"
}
```

- [ ] **Step 3: Update item evidence references**

Each item in `ground_truth_v2.json` must point to:

```text
evaluation/ground_truth/query_results_v2/<ID>.json
```

Validation:

```bash
./.venv/bin/python - <<'PY'
import json
from pathlib import Path
items = json.loads(Path("ground_truth_v2.json").read_text(encoding="utf-8"))
missing = [item["id"] for item in items if not Path(item["validation_evidence"]).exists()]
assert not missing, missing
print(f"evidence_files_ok={len(items)}")
PY
```

## Task 7: Sincronizar JSON Canonico com JSONL do Avaliador

**Files:**
- Create: `scripts/sync_ground_truth_v2.py`
- Modify: `evaluation/ground_truth/stage1_questions_v2.jsonl`
- Modify: `evaluation/ground_truth/stage1_questions_v2.md`
- Modify: `evaluation/ground_truth/manifest.json`

- [ ] **Step 1: Generate JSONL from root JSON**

Run:

```bash
./.venv/bin/python scripts/sync_ground_truth_v2.py
```

Expected outputs:

```text
wrote ground_truth_v2.json
wrote evaluation/ground_truth/stage1_questions_v2.jsonl
wrote evaluation/ground_truth/stage1_questions_v2.md
wrote evaluation/ground_truth/manifest.json
```

- [ ] **Step 2: Validate app loader compatibility**

Run:

```bash
./.venv/bin/python - <<'PY'
from pathlib import Path
from health_system_chatbot.artifacts import load_stage1_context
ctx = load_stage1_context(Path("."))
assert ctx.ground_truth
assert all(item.question_pt and item.sql for item in ctx.ground_truth)
print(f"loaded_ground_truth={len(ctx.ground_truth)}")
PY
```

Expected:

```text
loaded_ground_truth=<final_count>
```

## Task 8: Integrar com `verify_stage1.py`

**Files:**
- Modify: `scripts/verify_stage1.py`

- [ ] **Step 1: Add root JSON consistency check**

`verify_v2()` must verify:

- `ground_truth_v2.json` exists.
- It has the same count as `evaluation/ground_truth/stage1_questions_v2.jsonl`.
- IDs match in the same order.
- `question_pt`, `sql`, `difficulty`, `tables_used`, `columns_used`, `validation_evidence`, `result_summary` match between JSON and JSONL.
- Every evidence file hash matches a fresh DuckDB execution.

- [ ] **Step 2: Run v2 verifier**

Run:

```bash
./.venv/bin/python scripts/verify_stage1.py --version v2
```

Expected:

```text
PASS: Stage 1 v2 artifacts verified
semantic_failures=0
hash_mismatches=0
```

## Task 9: Rodar Smoke do Chatbot Contra o Ground Truth Corrigido

**Files:**
- Read: `evaluation/ground_truth/stage1_questions_v2.jsonl`
- Create: `evaluation/chatbot/results/ground_truth_v2_refactor_smoke.json`

- [ ] **Step 1: Run no-LLM negative smoke**

This project intentionally does not use ground truth as a deterministic runtime shortcut. With `--no-llm`, the evaluator should classify questions as answerable but should not generate SQL.

Run:

```bash
./.venv/bin/python scripts/evaluate_chatbot.py \
  --dataset evaluation/ground_truth/stage1_questions_v2.jsonl \
  --output evaluation/chatbot/results/ground_truth_v2_refactor_smoke.json \
  --limit 20 \
  --no-llm
```

Expected:

```json
{
  "total": 20,
  "intent_accuracy": 1.0,
  "sql_valid_rate": 0.0,
  "sql_execution_rate": 0.0
}
```

- [ ] **Step 2: Run full execution validator for ground-truth correctness**

Run:

```bash
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --execute --db sihrd5.duckdb
```

Expected:

```text
errors=0
semantic_failures=0
```

## Task 10: Final Review and Commit-Ready Gate

**Files:**
- Read all changed files from this plan.

- [ ] **Step 1: Run formatting and whitespace checks**

Run:

```bash
git diff --check
```

Expected:

```text
<no output>
```

- [ ] **Step 2: Run unit tests**

Run:

```bash
./.venv/bin/python -m pytest -q
```

Expected:

```text
passed
```

- [ ] **Step 3: Run all ground truth verifiers**

Run:

```bash
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --static-only
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --semantic-only
./.venv/bin/python scripts/validate_ground_truth_v2_json.py --execute --db sihrd5.duckdb
./.venv/bin/python scripts/verify_stage1.py --version v2
```

Expected:

```text
PASS static_format
PASS semantic_policy
errors=0
PASS: Stage 1 v2 artifacts verified
```

- [ ] **Step 4: Inspect final diff scope**

Run:

```bash
git status --short
git diff --stat
```

Expected changed areas:

```text
ground_truth_v2.json
refactor_gt.md
scripts/validate_ground_truth_v2_json.py
scripts/sync_ground_truth_v2.py
scripts/verify_stage1.py
tests/test_ground_truth_v2_contract.py
evaluation/ground_truth/
docs/generated/ground_truth_semantic_audit.csv
```

## Completion Checklist

- [ ] Every original `GT...` ID has a row in `evaluation/ground_truth/ground_truth_v2_refactor_audit.csv`.
- [ ] Every final item in `ground_truth_v2.json` is either preserved, rewritten, or replaced with a reason.
- [ ] No final SQL references `atendimentos`, `codigo_6d`, `.nome`, `.estado`, `CD_DESCRICAO`, `metrica`, `valor`, `bolsa_familia`, `idhm`, or `esgotamento_sanitario`.
- [ ] Every final SQL executes in DuckDB read-only.
- [ ] Every final query has evidence with row count, preview rows and result hash.
- [ ] Every final evidence hash matches fresh execution.
- [ ] Every final question is aligned with the documented schema, grain, join policy and data-quality caveats.
- [ ] `ground_truth_v2.json` and `evaluation/ground_truth/stage1_questions_v2.jsonl` are synchronized.
- [ ] `scripts/verify_stage1.py --version v2` passes.
- [ ] `./.venv/bin/python -m pytest -q` passes.

## Execution Notes

Prefer repairing questions in this order:

1. Static schema errors first, because they block execution.
2. Semantic wording and grain errors second, because they can silently corrupt evaluation.
3. Join policy and caveat errors third, because they decide whether a query is accepted, accepted with explicit scope, or invalid.
4. Evidence generation last, because result hashes are useful only after SQL and semantics stabilize.

Do not mark the refactor complete while any query is only "probably correct". The final acceptance condition is executable SQL plus documented semantic alignment for every item that remains in the ground truth.
