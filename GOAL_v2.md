# sihrd5.duckdb Stage 1 Recovery And Deep Exploration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `database-reviewer` plus `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Repair the current Stage 1 exploration gaps, deepen the DuckDB/database analysis, and produce a trustworthy Text-to-SQL benchmark whose SQL execution and business semantics are both validated.

**Architecture:** Stage 1 remains read-only and evidence-driven. The work starts by auditing the already generated artifacts, then iterates through database metadata, schema profiling, relationship coverage, data quality, business meaning, query performance, and ground-truth validation. A question is accepted only when its SQL executes, preserves the intended population, records evidence, and is not contradicted by known data-quality or join-coverage caveats.

**Tech Stack:** `sihrd5.duckdb`, DuckDB Python package in `./.venv`, SQL, reproducible Python scripts, Markdown documentation, CSV/JSON/JSONL evidence artifacts, and official DuckDB/DATASUS/SIH documentation where external meaning is claimed.

---

## Current Review Findings To Fix First

The existing implementation is a strong first pass, but it is not yet acceptable as final Stage 1 ground truth.

- `evaluation/ground_truth/stage1_questions.jsonl` contains queries that execute but silently drop known orphan records through `INNER JOIN`.
- `internacoes.RACA_COR -> raca_cor` is marked `rejected` in `docs/relationship_map.md`, but `SIHRD5_Q044` still uses an inner join and discards `48,760,813` rows.
- `internacoes.MUNIC_RES -> municipios` is only `likely`, with `1,270,397` unmatched rows, but many UF/municipality questions use inner joins without exposing the dropped population.
- `municipios.SG_UF` contains non-UF numeric values (`13`, `14`, `20`, `21`, `25`, `29`, `33`, `42`, `43`, `51`, `52`), so `COUNT(DISTINCT SG_UF)=38` is not a valid answer to "quantas UFs".
- `docs/generated/column_profiles.csv` uses `approx_count_distinct`, but the current `GOAL.md` asks for distinct counts. This produced impossible-looking values such as `approx_distinct > row_count`.
- Physical DuckDB constraints exist but are not documented as physical metadata. Current local inspection found `20 PRIMARY KEY` and `21 NOT NULL` constraints through `duckdb_constraints()`.
- `scripts/verify_stage1.py` validates artifact structure but does not reexecute SQL, recompute hashes, or reject semantically unsafe accepted questions.

## Non-Negotiable Rules

- Keep `sihrd5.duckdb` read-only. Do not run `CREATE`, `ALTER`, `DROP`, `INSERT`, `UPDATE`, `DELETE`, `COPY`, `EXPORT`, `VACUUM`, `CHECKPOINT`, or compaction against the source database.
- Use `duckdb.connect(str(DB_PATH), read_only=True)` for all scripted access.
- Do not commit `sihrd5.duckdb`, `*.duckdb.wal`, `*.duckdb.tmp`, full row-level exports, or large sensitive result dumps.
- Every important number must be traceable to SQL, execution timestamp, database file, DuckDB version, and filters.
- Distinguish `Observed`, `Inferred`, `Externally verified`, and `Unknown` in all docs.
- Never accept a query just because it executes. It must answer the natural-language question over the intended population.
- If a join has less than `99.5%` coverage, the question must either use `LEFT JOIN` plus an explicit unmatched bucket, or the natural-language question must say it is restricted to mapped records.
- If a relationship is `rejected`, do not use it for descriptive business labels in accepted non-audit questions.
- If a data-quality issue blocks a business interpretation, the related question must be rejected, rewritten, or marked as an audit/data-quality item.

## Source Anchors

Use official documentation for DBMS-specific claims.

- DuckDB metadata table functions: `https://duckdb.org/docs/current/sql/meta/duckdb_table_functions.html`
- DuckDB concurrency model: `https://duckdb.org/docs/stable/connect/concurrency`
- DuckDB pragmas/profiling: `https://duckdb.org/docs/current/configuration/pragmas.html`
- DuckDB limits and settings: `https://duckdb.org/docs/current/operations_manual/limits.html`
- DuckDB constraints: `https://duckdb.org/docs/current/sql/constraints.html`
- DuckDB indexing: `https://duckdb.org/docs/current/guides/performance/indexing.html`

## File Ownership Map

### Existing files to modify

- `scripts/sihrd5_stage1.py`: generation pipeline for metadata, profiling, relationships, data quality, and ground truth.
- `scripts/verify_stage1.py`: validation gate. Must become a real semantic and execution verifier.
- `docs/database_overview.md`: regenerated overview after corrected profiling and metadata capture.
- `docs/schema_catalog.md`: regenerated schema catalog with exact/approx distinct fields clearly separated.
- `docs/business_dictionary.md`: regenerated business meaning with official-source status.
- `docs/relationship_map.md`: regenerated physical constraints, inferred relationships, coverage, and accepted join policy.
- `docs/data_quality_report.md`: regenerated and expanded data-quality findings.
- `docs/query_design_methodology.md`: regenerated acceptance/rejection policy.
- `docs/stage2_readiness.md`: regenerated readiness and known caveats.
- `evaluation/ground_truth/stage1_questions.jsonl`: regenerated accepted benchmark.
- `evaluation/ground_truth/stage1_questions.md`: regenerated human-readable benchmark.
- `evaluation/ground_truth/rejected_questions.md`: regenerated rejected/pending questions with reasons.
- `evaluation/ground_truth/query_results/*.json`: regenerated compact evidence.

### New files to create

- `docs/generated/duckdb_runtime_metadata.json`: DuckDB version, settings, database size, access mode, memory/temp settings.
- `docs/generated/physical_constraints.csv`: output from `duckdb_constraints()`.
- `docs/generated/secondary_indexes.csv`: output from `duckdb_indexes()`.
- `docs/generated/table_metadata.csv`: output from `duckdb_tables()` and selected `information_schema` fields.
- `docs/generated/column_profiles_exact.csv`: exact distinct profiles for small and dimension tables.
- `docs/generated/column_profiles_approx.csv`: approximate distinct profiles for very large fact columns.
- `docs/generated/join_policy.csv`: one row per known join with confidence, unmatched count, accepted usage policy, and ground-truth impact.
- `docs/generated/uf_code_quality.csv`: valid and invalid `SG_UF` values with counts.
- `docs/generated/ground_truth_semantic_audit.csv`: per-question semantic checks, lost-row checks, relationship-risk flags, and final disposition.
- `evaluation/ground_truth/stage1_questions_v2.jsonl`: canonical regenerated v2 benchmark.
- `evaluation/ground_truth/stage1_questions_v2.md`: human-readable regenerated v2 benchmark.
- `evaluation/ground_truth/query_results_v2/`: evidence for regenerated v2 questions.
- `evaluation/ground_truth/rejected_questions_v2.md`: rejected/pending questions from v2.

## Starting Protocol

- [x] Confirm worktree state before touching files.

```bash
git status --short
```

Expected: understand whether existing Stage 1 files are untracked or modified. Do not revert unrelated user work.

- [x] Confirm local DuckDB package and source DB access.

```bash
./.venv/bin/python - <<'PY'
import duckdb
from pathlib import Path
db = Path("sihrd5.duckdb")
print("duckdb_version", duckdb.__version__)
print("db_exists", db.exists())
print("db_size_bytes", db.stat().st_size if db.exists() else None)
con = duckdb.connect(str(db), read_only=True)
print(con.execute("PRAGMA version").fetchall())
print(con.execute("SELECT name, value FROM duckdb_settings() WHERE name IN ('access_mode','threads','memory_limit','temp_directory','max_temp_directory_size') ORDER BY name").fetchall())
PY
```

Expected: DuckDB opens in `read_only` mode and reports settings without mutating the file.

- [x] Run the current validator to establish baseline.

```bash
./.venv/bin/python scripts/verify_stage1.py
```

Expected now: structural pass is allowed, but record that this is not sufficient for final completion.

- [x] Run the known regression probes from the review.

```bash
./.venv/bin/python - <<'PY'
import csv, json
from pathlib import Path
root = Path(".")
profiles = list(csv.DictReader((root / "docs/generated/column_profiles.csv").open()))
bad = [r for r in profiles if r["row_count"] and r["approx_distinct"] and float(r["approx_distinct"]) > float(r["row_count"])]
print("profiles_over_row_count", len(bad))
for r in bad[:20]:
    print(r["table_name"], r["column_name"], "rows", r["row_count"], "approx", r["approx_distinct"])
PY
```

Expected now: nonzero bad count until profiling is fixed or relabeled.

## Iteration Model

Run the work in cycles. Each cycle must end with regenerated artifacts plus validation.

1. **Inspect:** read current generated evidence and identify one class of failure.
2. **Codify:** add or update deterministic SQL/script logic that detects the failure.
3. **Regenerate:** run the Stage 1 generator against `sihrd5.duckdb` in read-only mode.
4. **Validate:** run structural, execution, semantic, and regression checks.
5. **Classify:** accept, rewrite, reject, or mark questions pending.
6. **Document:** update docs with observed evidence and caveats.
7. **Checkpoint:** commit only when a coherent slice is passing and the source DB remains untracked.

## Phase 1: Make DuckDB Metadata Complete

### Task 1.1: Capture runtime and database settings

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `docs/generated/duckdb_runtime_metadata.json`
- Modify: `docs/database_overview.md`

- [x] Add a function that captures `PRAGMA version`, `PRAGMA database_size`, and selected `duckdb_settings()`.

Required SQL:

```sql
PRAGMA version;
PRAGMA database_size;
SELECT name, value, description, input_type, scope
FROM duckdb_settings()
WHERE name IN (
  'access_mode',
  'threads',
  'memory_limit',
  'temp_directory',
  'max_temp_directory_size'
)
ORDER BY name;
```

- [x] Write the JSON artifact with generated timestamp and `database_file`.
- [x] Document the runtime in `docs/database_overview.md`, including `access_mode=read_only`.
- [x] Reject completion if runtime metadata is missing.

### Task 1.2: Document physical constraints and indexes

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `docs/generated/physical_constraints.csv`
- Create: `docs/generated/secondary_indexes.csv`
- Create: `docs/generated/table_metadata.csv`
- Modify: `docs/relationship_map.md`

- [x] Export physical constraints.

Required SQL:

```sql
SELECT
  schema_name,
  table_name,
  constraint_type,
  constraint_column_names,
  constraint_name,
  referenced_table,
  referenced_column_names,
  constraint_text
FROM duckdb_constraints()
ORDER BY schema_name, table_name, constraint_type, constraint_column_names;
```

- [x] Export secondary indexes.

Required SQL:

```sql
SELECT
  schema_name,
  table_name,
  index_name,
  is_unique,
  is_primary,
  expressions,
  sql
FROM duckdb_indexes()
ORDER BY schema_name, table_name, index_name;
```

- [x] Export table metadata.

Required SQL:

```sql
SELECT
  schema_name,
  table_name,
  has_primary_key,
  estimated_size,
  column_count,
  index_count,
  check_constraint_count,
  sql
FROM duckdb_tables()
WHERE NOT internal
ORDER BY schema_name, table_name;
```

- [x] In `relationship_map.md`, separate:
  - Physical DuckDB constraints.
  - Inferred candidate keys.
  - Inferred relationships.
  - Join policy for question generation.

Acceptance: the docs must not imply that `duckdb_indexes()` includes primary-key indexes. Per DuckDB docs, `duckdb_indexes()` reports secondary indexes, while PK/unique/foreign-key metadata belongs in `duckdb_constraints()`.

## Phase 2: Correct Profiling Semantics

### Task 2.1: Split exact and approximate distinct counts

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `docs/generated/column_profiles_exact.csv`
- Create: `docs/generated/column_profiles_approx.csv`
- Modify: `docs/schema_catalog.md`
- Modify: `scripts/verify_stage1.py`

- [x] For dimension/reference tables and low-cardinality columns, compute exact distinct counts.

Required SQL pattern:

```sql
SELECT
  COUNT(*) AS row_count,
  COUNT(*) FILTER (WHERE "{column}" IS NULL) AS null_count,
  COUNT(DISTINCT "{column}") AS exact_distinct_count,
  MIN("{column}") AS min_value,
  MAX("{column}") AS max_value
FROM "{schema}"."{table}";
```

- [x] For large fact columns where exact distinct is too expensive, compute approximate distinct but label it as approximate.

Required output fields:

```text
profile_mode = exact|approx
exact_distinct_count = integer or null
approx_distinct_count = integer or null
distinct_count_for_catalog = integer or null
distinct_is_exact = true|false
```

- [x] Add validation: exact distinct can never exceed row count.
- [x] Add validation: approximate distinct values may exceed row count, but docs must label them approximate and must not call them exact.
- [x] Update `GOAL.md` references only if this v2 plan is promoted later. For now, keep `GOAL_v2.md` as the controlling plan.

### Task 2.2: Add safe profiling tiers

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Modify: `docs/schema_catalog.md`

- [x] Define table-size tiers.

Required policy:

```text
small: <= 100,000 rows, exact profile every column
medium: > 100,000 and <= 5,000,000 rows, exact profile identifiers and dimensions, approximate for broad text
large: > 5,000,000 rows, exact for keys and critical business columns, approximate for exploratory cardinality
```

- [x] For every profile row, record `profile_sql`, `profile_seconds`, and `profile_mode`.
- [x] For large fact tables, add selected exact checks for business-critical keys: `N_AIH`, `id_atendimento`, `PROC_REA`, `CNES`, `MUNIC_RES`, `DIAG_PRINC`, `DT_INTER`, `DT_SAIDA`, `VAL_TOT`, `MORTE`.

## Phase 3: Fix Relationship And Join Policy

### Task 3.1: Generate explicit join policy

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `docs/generated/join_policy.csv`
- Modify: `docs/relationship_map.md`
- Modify: `docs/query_design_methodology.md`

- [x] For every relationship, calculate:
  - `left_rows`
  - `non_null_left_key`
  - `matched_rows`
  - `unmatched_rows`
  - `match_rate_non_null`
  - `confidence`
  - `accepted_usage_policy`

Required policy:

```text
confirmed: can be used in inner joins for business questions
likely: use left join with unmatched bucket, or make the question explicitly scoped to mapped records
weak: audit questions only unless externally validated
rejected: audit/data-quality questions only
```

- [x] Generate a list of current questions that violate join policy.
- [x] Reject or rewrite every violating question before v2 acceptance.

### Task 3.2: Fix known join-loss questions

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Modify: `evaluation/ground_truth/stage1_questions_v2.jsonl`
- Modify: `evaluation/ground_truth/rejected_questions_v2.md`

- [x] Rewrite `RACA_COR` descriptive questions to preserve unmapped values.

Required SQL pattern:

```sql
SELECT
  COALESCE(r.DESCRICAO, 'Sem correspondencia na dimensao raca_cor') AS raca_cor,
  i.RACA_COR AS codigo_raca_cor,
  COUNT(*) AS internacoes
FROM internacoes i
LEFT JOIN raca_cor r
  ON i.RACA_COR = r.RACA_COR
GROUP BY 1, 2
ORDER BY internacoes DESC;
```

- [x] Rewrite UF/municipality residence questions to either:
  - use `LEFT JOIN` and include `Sem municipio mapeado`, or
  - state "entre internações com município de residência mapeado" in the natural-language question.

Required SQL pattern for complete-population answers:

```sql
SELECT
  COALESCE(m.SG_UF, 'UF_nao_mapeada') AS sg_uf_residencia,
  COUNT(*) AS internacoes,
  COUNT(*) FILTER (WHERE m.CO_MUNICIPIO_6D IS NULL) AS internacoes_sem_municipio_mapeado
FROM internacoes i
LEFT JOIN municipios m
  ON i.MUNIC_RES = m.CO_MUNICIPIO_6D
GROUP BY 1
ORDER BY internacoes DESC;
```

- [x] Move questions that depend on `ETNIA`, `INSTRU`, `VINCPREV`, `CBOR`, `DIAG_SECUN`, or `CID_MORTE` as descriptive dimensions to rejected/pending unless the SQL is explicitly an audit/data-quality query.

## Phase 4: Expand Data Quality Beyond The Current Report

### Task 4.1: Add code-domain validation

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `docs/generated/uf_code_quality.csv`
- Modify: `docs/data_quality_report.md`

- [x] Add a DQ item for invalid `municipios.SG_UF`.

Required SQL:

```sql
WITH valid_uf(sg_uf) AS (
  VALUES
    ('AC'), ('AL'), ('AP'), ('AM'), ('BA'), ('CE'), ('DF'), ('ES'), ('GO'),
    ('MA'), ('MT'), ('MS'), ('MG'), ('PA'), ('PB'), ('PR'), ('PE'), ('PI'),
    ('RJ'), ('RN'), ('RS'), ('RO'), ('RR'), ('SC'), ('SP'), ('SE'), ('TO')
)
SELECT m.SG_UF, COUNT(*) AS municipios
FROM municipios m
LEFT JOIN valid_uf v ON m.SG_UF = v.sg_uf
WHERE v.sg_uf IS NULL
GROUP BY 1
ORDER BY 1;
```

- [x] Add a DQ item for all ground-truth questions that count UFs without filtering valid UF codes.
- [x] Add DQ checks for code format:
  - `CO_MUNICIPIO_6D`: six digits.
  - `CO_MUNICIPIO_7D`: seven digits when non-null.
  - `CNES`: expected code shape from observed data and official source if verified.
  - `CID`: valid enough for joining to `cid`, with unknown format caveats.
  - `PROC_REA`: valid enough for joining to `procedimentos`.

### Task 4.2: Add population-loss and denominator checks

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Modify: `docs/data_quality_report.md`
- Modify: `docs/query_design_methodology.md`

- [x] For each accepted question, compute the intended base population if possible.
- [x] When the result uses a join, compute dropped-row count.
- [x] For rate questions, record numerator, denominator, and excluded records.
- [x] Reject questions where a denominator is implicit or silently changed by joins.

Required evidence fields per question:

```json
{
  "base_population_sql": "SELECT COUNT(*) ...",
  "base_population_count": 0,
  "result_population_count": 0,
  "dropped_by_join_count": 0,
  "dropped_by_join_rate": 0.0,
  "denominator_definition": "..."
}
```

## Phase 5: Rebuild The Ground Truth As V2

### Task 5.1: Create semantic audit before accepting questions

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `docs/generated/ground_truth_semantic_audit.csv`
- Modify: `scripts/verify_stage1.py`

- [x] Add a per-question semantic audit with these fields:

```text
id
question_pt
execution_status
read_only_status
tables_used
relationships_used
worst_relationship_confidence
uses_rejected_relationship
uses_likely_relationship_without_caveat
dropped_by_join_count
dropped_by_join_rate
invalid_domain_dependency
business_semantics_status
final_disposition
disposition_reason
```

- [x] Final disposition values must be:

```text
accepted
accepted_with_explicit_scope
rejected_join_loss
rejected_domain_invalid
rejected_ambiguous
rejected_too_slow
pending_external_dictionary
```

- [x] `scripts/verify_stage1.py` must fail if any item in the canonical v2 JSONL has final disposition other than `accepted` or `accepted_with_explicit_scope`.

### Task 5.2: Regenerate accepted and rejected v2 artifacts

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Create: `evaluation/ground_truth/stage1_questions_v2.jsonl`
- Create: `evaluation/ground_truth/stage1_questions_v2.md`
- Create: `evaluation/ground_truth/query_results_v2/`
- Create: `evaluation/ground_truth/rejected_questions_v2.md`
- Modify: `evaluation/ground_truth/manifest.json`

- [x] Keep 100 accepted v2 questions only if 100 survive semantic validation.
- [x] If fewer than 100 survive, keep at least 50 high-quality accepted questions and document the gap.
- [x] Preserve difficulty balance, but do not keep a flawed question just to satisfy a quota.
- [x] For every rejected question, store:
  - question text.
  - original SQL.
  - rejection reason.
  - relationship or data-quality evidence.
  - whether it can be fixed.

Acceptance: `stage1_questions_v2.jsonl` is the canonical v2 file. The old `stage1_questions.jsonl` remains historical until explicitly replaced.

## Phase 6: Add Query Performance And DuckDB Execution Evidence

### Task 6.1: Add performance metadata for benchmark SQL

**Files:**
- Modify: `scripts/sihrd5_stage1.py`
- Modify: `evaluation/ground_truth/query_results_v2/*.json`
- Modify: `docs/query_design_methodology.md`

- [x] Record duration for every query.
- [x] Add warning thresholds:

```text
fast: <= 1 second
moderate: > 1 and <= 5 seconds
slow: > 5 and <= 15 seconds
too_slow_for_default_eval: > 15 seconds
```

- [x] For slow queries, capture `EXPLAIN` text.

Required SQL pattern:

```sql
EXPLAIN <query>;
```

- [x] Do not use `EXPLAIN ANALYZE` automatically for every query because it executes the query and can materially increase runtime. Use it selectively for slow queries during optimization.

### Task 6.2: Add safe DuckDB settings guidance

**Files:**
- Modify: `docs/query_design_methodology.md`
- Modify: `docs/stage2_readiness.md`

- [x] Document the runtime settings used for generation.
- [x] Explain that DuckDB is embedded and analytical; Stage 2 should use controlled query execution, read-only connections, timeouts, and concurrency limits.
- [x] Include the official concurrency caveat: multiple processes can read in read-only mode, while multi-process writing is not automatic and is not needed for this project.

## Phase 7: External Business Meaning Validation

### Task 7.1: Separate observed database facts from official DATASUS/SIH definitions

**Files:**
- Modify: `docs/business_dictionary.md`
- Modify: `docs/database_overview.md`
- Modify: `docs/query_design_methodology.md`

- [x] For every table and key field, mark one of:

```text
Observed in database
Inferred from names/values
Externally verified against official source
Unknown
```

- [x] Do not label any field meaning as official unless an official source is cited.
- [x] Add a section listing external dictionaries still needed before Stage 2:
  - SIH/SUS AIH field dictionary.
  - CNES field dictionary.
  - SIGTAP/procedure dictionary if not fully trusted from `procedimentos`.
  - CID source/version used by `cid`.
  - IBGE municipality code conventions.

### Task 7.2: Add unsafe or ambiguous user-intent catalog

**Files:**
- Modify: `docs/stage2_readiness.md`
- Modify: `evaluation/ground_truth/rejected_questions_v2.md`

- [x] Document questions Stage 2 must clarify before answering:
  - "custo" without specifying `VAL_TOT`, `VAL_SH`, `VAL_SP`, `VAL_UTI`, or derived definition.
  - "local" without residence vs hospital municipality.
  - "mortalidade" without denominator and date field.
  - "procedimento principal" without deciding between `internacoes` fields and `internacao_procedimento`.
  - race/color, ethnicity, instruction, CBO-R, and secondary diagnosis descriptions where relationship coverage is rejected.

## Phase 8: Verification Gates

### Task 8.1: Strengthen `verify_stage1.py`

**Files:**
- Modify: `scripts/verify_stage1.py`

- [x] Add `--version v1|v2` argument. Default to `v2`.
- [x] Verify all required v2 artifacts exist and are non-empty.
- [x] Reexecute every SQL in `stage1_questions_v2.jsonl` against `sihrd5.duckdb` in read-only mode.
- [x] Recompute result hash and compare with stored evidence.
- [x] Fail if canonical v2 questions use rejected relationships for business-label questions.
- [x] Fail if a likely relationship is used without explicit scope or unmatched bucket.
- [x] Fail if `COUNT(DISTINCT SG_UF)` is used to answer "quantas UFs" without valid-UF filtering.
- [x] Fail if exact distinct count exceeds row count.
- [x] Fail if `sihrd5.duckdb` is tracked by Git.

Required command:

```bash
./.venv/bin/python scripts/verify_stage1.py --version v2
```

Expected final output:

```text
PASS: Stage 1 v2 artifacts verified
questions=<accepted_count>
reexecuted=<accepted_count>
semantic_failures=0
hash_mismatches=0
```

### Task 8.2: Add focused regression probes

**Files:**
- Modify: `scripts/verify_stage1.py`

- [x] Hard-code these known regressions until they are covered by general logic:

```text
RACA_COR inner join must not be accepted for full-population race/color distribution.
MUNIC_RES inner join must not be accepted for full-population UF/municipality questions unless explicitly scoped.
Invalid numeric SG_UF values must be reported.
approx_count_distinct must not be labeled as exact distinct.
duckdb_constraints() output must be documented.
```

## Phase 9: Finalization Criteria

Do not mark Stage 1 v2 complete until all items below pass.

- [x] `./.venv/bin/python scripts/verify_stage1.py --version v2` passes.
- [x] All accepted v2 SQL queries are reexecuted against `sihrd5.duckdb`.
- [x] Every accepted query has evidence under `evaluation/ground_truth/query_results_v2/`.
- [x] Every accepted query has a semantic audit row with final disposition `accepted` or `accepted_with_explicit_scope`.
- [x] `docs/generated/physical_constraints.csv` documents DuckDB physical constraints.
- [x] `docs/generated/join_policy.csv` exists and is reflected in accepted/rejected questions.
- [x] `docs/generated/uf_code_quality.csv` exists and invalid `SG_UF` values are documented.
- [x] `docs/schema_catalog.md` clearly separates exact and approximate distinct counts.
- [x] `docs/data_quality_report.md` includes join-loss, invalid-code, denominator, and existing DQ issues.
- [x] `docs/query_design_methodology.md` explains semantic acceptance, join policy, denominator policy, and performance policy.
- [x] `docs/stage2_readiness.md` lists safe chatbot requirements, unsafe intents, caveats, and evaluation metrics.
- [x] `git status --short` confirms `sihrd5.duckdb` is not staged or tracked.

Final verification command sequence:

```bash
git status --short
./.venv/bin/python scripts/verify_stage1.py --version v2
./.venv/bin/python - <<'PY'
import json
from pathlib import Path
items = [json.loads(line) for line in Path("evaluation/ground_truth/stage1_questions_v2.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
print("accepted_v2", len(items))
print("difficulty_distribution", {d: sum(1 for item in items if item["difficulty"] == d) for d in ["L1", "L2", "L3", "L4", "L5"]})
PY
```

## Recommended Commit Slices

- [ ] Commit 1: `docs(goal): add stage 1 v2 recovery plan`
- [ ] Commit 2: `feat(stage1): capture duckdb metadata and physical constraints`
- [ ] Commit 3: `fix(stage1): separate exact and approximate profiling`
- [ ] Commit 4: `fix(stage1): enforce join policy and semantic audit`
- [ ] Commit 5: `feat(stage1): regenerate v2 ground truth evidence`
- [ ] Commit 6: `test(stage1): reexecute and semantically verify v2 benchmark`

Commit slices were not executed because the requested work was implementation/review, not commit/push.

## Completion Statement Template

When finishing implementation, report:

```text
Stage 1 v2 status: complete|partial|blocked
Accepted v2 questions: <n>
Rejected/pending v2 questions: <n>
Verification: <exact command and result>
Known residual risks: <list>
Files changed: <summary>
```

## Completion Record

Stage 1 v2 status: complete

Accepted v2 questions: `100`

Rejected/pending v2 questions: `0`

Verification:

```text
./.venv/bin/python scripts/verify_stage1.py --version v2
PASS: Stage 1 v2 artifacts verified
questions=100 distribution={'L1': 15, 'L2': 25, 'L3': 25, 'L4': 20, 'L5': 15}
reexecuted=100
semantic_failures=0
hash_mismatches=0
```

Additional verification:

```text
./.venv/bin/python scripts/verify_stage1.py --version v1
PASS: Stage 1 artifacts verified
questions=100 distribution={'L1': 15, 'L2': 25, 'L3': 25, 'L4': 20, 'L5': 15}
evidence_files=100

slow_v2 [('SIHRD5_Q058', 'slow', True), ('SIHRD5_Q070', 'slow', True), ('SIHRD5_Q078', 'slow', True)]
missing_explain []
```

Known residual risks:

- No SIH/DATASUS field definition was promoted to `Externally verified`; `docs/business_dictionary.md` lists the external dictionaries still needed before Stage 2 promotion.
- `stage1_questions_v2.jsonl` is the canonical v2 benchmark. The original `stage1_questions.jsonl` remains available for v1/backward compatibility.
