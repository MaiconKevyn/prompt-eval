# sihrd5.duckdb Exploration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Explore `sihrd5.duckdb` as deeply as possible, produce complete technical and business documentation, and create a validated Text-to-SQL ground truth with at least 50 to 100 important healthcare questions for Stage 1.

**Architecture:** Stage 1 is a read-only data understanding and evaluation-preparation phase. Every claim about schema, business meaning, data quality, and SQL behavior must be backed by executed queries against `sihrd5.duckdb` or explicitly labeled as an inference that still needs validation. The output must prepare the project for Stage 2, where a chatbot will answer Brazilian healthcare-system questions using this database as source of truth.

**Tech Stack:** DuckDB database file (`sihrd5.duckdb`), SQL, reproducible profiling queries, Markdown documentation, CSV/JSONL/YAML artifacts for validated ground truth, and optional Python scripts for repeatable extraction.

---

## Non-Negotiable Objective

The current project objective is not to build the chatbot yet. The objective is to understand the database, document it, identify business meaning and inconsistencies, and create a reliable validated benchmark for future chatbot development.

The work is only complete when:

- The database schema is documented with tables, columns, types, row counts, candidate keys, inferred relationships, and profiling statistics.
- The business meaning of the data is documented in language understandable to a Brazilian healthcare professional.
- Data quality issues, inconsistencies, gaps, suspicious values, duplicates, and join problems are reported with evidence.
- At least 50 validated question/SQL pairs exist, with a strong target of 100.
- Every ground-truth SQL query was executed against `sihrd5.duckdb` and confirmed to run correctly.
- Each query result has enough recorded evidence to prove that the query answers the question.
- Questions are organized by scientifically grounded difficulty levels inspired by Text-to-SQL evaluation literature such as Spider/BIRD-style component complexity: number of tables, joins, filters, aggregations, grouping, ordering, nesting, set operations, temporal reasoning, and domain ambiguity.

## Source Database

- Primary file: `sihrd5.duckdb`
- Current observed local size: approximately 26 GB
- Access mode: read-only by default
- Do not mutate, compact, overwrite, export full sensitive data, or rewrite the database unless explicitly requested.
- Do not commit the database file to Git.

Recommended connection pattern:

```bash
duckdb sihrd5.duckdb
```

If the DuckDB CLI is unavailable, use a local Python environment with `duckdb` installed and connect in read-only mode when possible.

## Stage 1 Deliverables

Create or maintain the following artifacts as the exploration progresses:

- `docs/database_overview.md`: high-level description of the database, scope, size, temporal coverage, main entities, and likely SIH/SUS domain context.
- `docs/schema_catalog.md`: table-by-table schema catalog with columns, types, row counts, null rates, distinct counts, example values, min/max values, and notes.
- `docs/business_dictionary.md`: business meaning of tables and fields, written for healthcare users in Brazil.
- `docs/relationship_map.md`: inferred relationships, candidate primary keys, join keys, join coverage, and relationship confidence.
- `docs/data_quality_report.md`: inconsistencies, missing values, duplicate patterns, impossible values, orphan codes, temporal gaps, and distribution anomalies.
- `docs/query_design_methodology.md`: how questions are selected, how difficulty is assigned, how SQL is validated, and what makes a query accepted or rejected.
- `evaluation/ground_truth/stage1_questions.jsonl`: canonical machine-readable ground truth.
- `evaluation/ground_truth/stage1_questions.md`: human-readable version of the validated questions.
- `evaluation/ground_truth/query_results/`: compact result evidence for each accepted SQL query, such as row count, sample rows, checksums, or aggregate totals.
- `evaluation/ground_truth/rejected_questions.md`: questions rejected because they are ambiguous, impossible with the available data, too slow, unsupported by schema, or semantically unsafe.

## Exploration Method

Follow an iterative loop. Do not jump straight to question generation before understanding the tables.

### Task 1: Inventory The Database

- [ ] List all schemas and tables.
- [ ] Count rows per table.
- [ ] Estimate table sizes if DuckDB metadata permits.
- [ ] Identify empty or near-empty tables.
- [ ] Identify very large tables requiring sampled profiling before full scans.
- [ ] Record all executed inventory SQL in `docs/database_overview.md`.

Minimum SQL patterns:

```sql
SELECT * FROM information_schema.tables ORDER BY table_schema, table_name;
SELECT table_schema, table_name, column_name, data_type, is_nullable
FROM information_schema.columns
ORDER BY table_schema, table_name, ordinal_position;
```

### Task 2: Profile Columns

For every table and important column:

- [ ] Compute null counts and null rates.
- [ ] Compute distinct counts and distinct rates.
- [ ] Record min/max for numeric, date, and timestamp fields.
- [ ] Record top frequent values for categorical fields.
- [ ] Detect likely IDs, codes, dates, monetary values, counts, quantities, geography fields, patient attributes, provider attributes, procedure fields, diagnosis fields, and outcome fields.
- [ ] Add examples only when they do not expose sensitive personal information.

### Task 3: Infer Relationships

- [ ] Identify candidate primary keys from uniqueness and null checks.
- [ ] Identify candidate foreign keys by column names, value overlap, and join coverage.
- [ ] Quantify join coverage in both directions.
- [ ] Identify orphan records and many-to-many surprises.
- [ ] Create a relationship confidence level: confirmed, likely, weak, rejected.

Relationship evidence must include SQL. Example pattern:

```sql
SELECT
  COUNT(*) AS left_rows,
  COUNT(right_table.key_col) AS matched_rows,
  COUNT(right_table.key_col)::DOUBLE / NULLIF(COUNT(*), 0) AS match_rate
FROM left_table
LEFT JOIN right_table
  ON left_table.key_col = right_table.key_col;
```

### Task 4: Build The Business Dictionary

Document the business layer, not only the technical schema.

For each important table:

- [ ] What real-world entity or process does one row represent?
- [ ] Is the grain one hospitalization, AIH, patient event, procedure line, monthly aggregate, provider, municipality, diagnosis, payment record, or another unit?
- [ ] What period does the data cover?
- [ ] What geography exists: Brazil, state, municipality, health region, establishment, or other?
- [ ] What actors are represented: patient, hospital, SUS manager, provider, municipality, procedure, diagnosis, authorization, payment?
- [ ] Which metrics look like cost, reimbursement, length of stay, quantity, mortality, procedure count, admission count, or discharge outcome?
- [ ] Which codes require an external dictionary before they can be interpreted safely?
- [ ] Which meanings are directly proven by column names and values, and which are inferred?

When official DATASUS/SIH/SUS terminology is used, mark whether it was verified against a source or inferred from the database.

### Task 5: Find Inconsistencies

Act as both data engineer and health-system analyst. Look for:

- Impossible dates, such as discharge before admission.
- Future dates or dates outside the documented coverage.
- Negative costs, quantities, days, ages, or counts where they should not exist.
- Age outliers and impossible patient demographics.
- Missing mandatory business fields.
- Duplicate identifiers or duplicate event rows.
- Procedure, diagnosis, municipality, UF, CNES, or provider codes with invalid formats.
- Orphan codes not found in dimension/reference tables.
- Distribution shifts by month, year, UF, provider, procedure, or diagnosis.
- Large spikes or drops that may indicate extraction gaps.
- Monetary totals that disagree across levels of aggregation.
- Rows that cannot be joined to expected dimensions.
- Ambiguous fields whose meaning cannot be trusted without more evidence.

Every reported issue must include:

- A short title.
- Why it matters for healthcare/business interpretation.
- SQL evidence.
- Count of affected rows.
- Example rows or aggregate evidence.
- Severity: low, medium, high, critical.
- Whether it blocks ground-truth questions.

## Ground Truth Requirements

The ground truth is the most important Stage 1 output. It will be used later to evaluate the chatbot.

Each accepted item must include:

```yaml
id: "SIHRD5_Q001"
persona: "Gestor estadual do SUS"
question_pt: "Pergunta natural em portugues"
business_intent: "O que o usuario esta tentando decidir ou entender"
difficulty: "L1|L2|L3|L4|L5"
difficulty_rationale: "Criterios objetivos usados para classificar"
sql: "SELECT ..."
tables_used: ["table_a", "table_b"]
columns_used: ["table_a.col1", "table_b.col2"]
expected_result_type: "scalar|table|time_series|ranking|distribution|data_quality_finding"
execution_status: "passed"
row_count: 0
result_summary: "Resumo curto do resultado observado"
validation_evidence: "Caminho para CSV/MD com amostra, checksum ou agregados"
assumptions: "Premissas semanticas usadas"
data_quality_notes: "Riscos ou inconsistencias relevantes"
created_at: "YYYY-MM-DD"
```

Acceptance rules:

- The SQL must run successfully against `sihrd5.duckdb`.
- The SQL must be read-only.
- The result must answer the natural-language question directly.
- The query must not depend on hidden state, manual post-processing, or undefined aliases.
- If the question is ambiguous, rewrite the question or reject it.
- If a business concept cannot be mapped confidently to columns, reject or mark as pending.
- If a query is too slow, first optimize it; if still too slow, document why and move it to rejected/pending.
- Store enough result evidence to validate future regressions without saving unnecessarily large outputs.

## Difficulty Levels

Use the following objective criteria. A query can move to a higher level if it combines multiple lower-level elements with strong domain reasoning.

### L1: Basic Retrieval

Characteristics:

- One table.
- Simple filters or direct counts.
- No joins.
- No grouping beyond a global aggregate.
- Minimal domain ambiguity.

Examples:

- Count total rows in a table.
- Find the temporal min/max of a date column.
- List top values of a categorical field.

### L2: Aggregation And Filtering

Characteristics:

- One table or one clearly documented relationship.
- `GROUP BY`, `ORDER BY`, `LIMIT`, `SUM`, `AVG`, `MIN`, `MAX`, `COUNT`.
- Simple business metric such as total admissions, total value, average stay, or count by UF/month/procedure.

Examples:

- Total hospitalizations by year.
- Top procedures by total approved value.
- Average length of stay by state, if the column exists.

### L3: Multi-Table Business Query

Characteristics:

- Two or more tables.
- Explicit joins with validated join coverage.
- Business interpretation depends on dimensions, code descriptions, geography, provider, diagnosis, procedure, or time.
- May include grouped metrics and rankings.

Examples:

- Total value by procedure description and state.
- Hospitalizations by diagnosis group and year.
- Providers with the highest count of selected procedures.

### L4: Advanced Analytical Query

Characteristics:

- Multiple joins and multiple aggregation stages.
- CTEs or subqueries.
- Cohort-like filtering, temporal comparisons, rates, percentages, ranking within groups, or year-over-year/month-over-month change.
- Requires careful denominator definition.

Examples:

- Monthly mortality rate by UF with numerator and denominator documented.
- Year-over-year growth in total approved value by procedure group.
- Providers above the 95th percentile for a selected metric.

### L5: Expert / Extra-Hard Query

Characteristics:

- Nested logic, window functions, set operations, anomaly detection, or multi-step validation.
- Explicit handling of data quality limitations.
- Requires healthcare-domain reasoning and precise metric definitions.
- Often answers audit, inconsistency, or policy-monitoring questions.

Examples:

- Detect municipalities with large reimbursement spikes unexplained by admission volume.
- Identify procedure/provider combinations with abnormal cost per hospitalization.
- Find temporal gaps by geography and quantify affected metrics.
- Compare two alternative metric definitions and explain the difference.

## Question Personas

Generate questions as if they came from real users of the Brazilian health system. Include at least these personas:

- Gestor municipal do SUS.
- Gestor estadual do SUS.
- Analista DATASUS/SIH.
- Auditor de contas hospitalares.
- Coordenador hospitalar.
- Epidemiologista.
- Planejador de rede assistencial.
- Pesquisador em saude publica.
- Tecnico de regulacao.
- Analista financeiro da saude.

Questions should sound natural, but the accepted SQL must be precise and reproducible.

## Minimum Question Distribution

For 50 questions:

- L1: 8 to 10
- L2: 12 to 15
- L3: 12 to 15
- L4: 8 to 10
- L5: 5 to 8

For 100 questions:

- L1: 15
- L2: 25
- L3: 25
- L4: 20
- L5: 15

Include both business-answer questions and data-quality/audit questions. Do not create only descriptive statistics.

## Candidate Question Themes

Convert these into validated question/SQL pairs only after the schema is understood:

- Volume of hospitalizations/events over time.
- Temporal coverage of the database.
- Coverage by UF, municipality, region, provider, or establishment.
- Top procedures by count.
- Top procedures by total value.
- Average value per hospitalization/event.
- Total value by year and month.
- Distribution of length of stay, if available.
- Mortality or outcome rates, if available.
- Diagnoses or CID groups, if available.
- Procedure groups and subgroups, if available.
- Provider-level concentration.
- Municipality-level concentration.
- State-level comparisons.
- Seasonal patterns.
- Year-over-year variation.
- Month-over-month variation.
- High-cost outliers.
- Low-volume/high-cost combinations.
- Duplicate or suspicious AIH/event identifiers.
- Missing diagnosis, procedure, provider, geography, or date fields.
- Invalid code formats.
- Orphan dimension codes.
- Join coverage between fact and dimension tables.
- Inconsistent monetary totals.
- Age/demographic outliers, if available.
- Admission/discharge date inconsistencies, if available.
- Length-of-stay inconsistencies.
- Procedure mix by provider.
- Diagnosis mix by geography.
- Payment/reimbursement concentration.
- Municipalities or providers with abrupt metric changes.
- Ranking shifts over time.
- Data completeness by year/month.
- Data completeness by geography.
- Business definitions with alternative denominators.

## Documentation Standards

All documentation must distinguish four types of statements:

- **Observed:** directly proven by SQL result.
- **Inferred:** likely based on names, values, or relationships, but not externally verified.
- **Externally verified:** confirmed through an official data dictionary or documentation.
- **Unknown:** cannot be safely concluded from the current evidence.

Every important number in documentation must be traceable to:

- The SQL query that produced it.
- The date of execution.
- The database file used.
- Any filters applied.

## Validation And Iteration Loop

Repeat this loop until the documentation and ground truth are strong enough:

1. Explore schema and profile data.
2. Write technical notes.
3. Infer business meaning.
4. Test the inference with SQL.
5. Draft candidate questions.
6. Write SQL for each question.
7. Execute SQL against `sihrd5.duckdb`.
8. Inspect whether the result makes business sense.
9. Record evidence.
10. Accept, revise, or reject the question.
11. Add discovered issues to the data-quality report.
12. Update the business dictionary and relationship map.

Do not count a question as ground truth until steps 6 through 10 pass.

## Stage 1 Completion Checklist

- [ ] Database inventory completed.
- [ ] Schema catalog completed.
- [ ] Table and column profiling completed.
- [ ] Relationship map completed.
- [ ] Business dictionary completed.
- [ ] Data quality report completed.
- [ ] Query design methodology documented.
- [ ] At least 50 validated question/SQL pairs accepted.
- [ ] Stretch goal: 100 validated question/SQL pairs accepted.
- [ ] All accepted queries executed successfully.
- [ ] All accepted queries have result evidence.
- [ ] Rejected and pending questions documented.
- [ ] Stage 2 chatbot requirements and risks summarized from Stage 1 findings.

## Stage 2 Readiness Criteria

Only start chatbot implementation after Stage 1 produces:

- A trusted schema/business dictionary.
- A validated ground-truth benchmark.
- Clear known limitations of the database.
- A list of high-value user intents.
- A list of unsafe or unsupported question types.
- Baseline SQL examples for common tasks.
- Data-quality caveats the chatbot must disclose.
- Evaluation metrics for chatbot answers: SQL execution accuracy, answer correctness, citation/evidence quality, latency, refusal accuracy, and robustness to ambiguous questions.
