# Query Design Methodology

Generated at: 2026-05-13T19:23:25

## Goal

The ground truth evaluates whether a future chatbot can convert realistic Brazilian health-system questions into executable SQL over `sihrd5.duckdb`.

## Acceptance Gate

Each accepted question must:

- be written as a natural Portuguese question from a realistic SUS/DATASUS persona;
- contain read-only SQL starting with `SELECT` or `WITH`;
- execute successfully against `sihrd5.duckdb`;
- return compact evidence stored under `evaluation/ground_truth/query_results/`;
- include tables, columns, difficulty, business intent, assumptions, and data quality notes.

## Difficulty Criteria

- `L1`: one table, basic retrieval/count/min/max, no joins.
- `L2`: one table aggregation, filtering, grouping, ordering, or simple ranking.
- `L3`: joins between fact and dimensions with business interpretation.
- `L4`: CTEs, windows, denominators, rates, temporal comparisons, percentiles, or multiple aggregation stages.
- `L5`: expert audit/data-quality question with inconsistency detection, orphan checks, or caveated metric definitions.

The criteria follow the same spirit as component-complexity evaluation in Text-to-SQL benchmarks such as Spider/BIRD: tables, joins, aggregation, nesting, windows, ordering, and domain ambiguity increase difficulty.

## Evidence Format

For each accepted item, the validator writes one JSON evidence file with:

- query id;
- question text;
- executed SQL;
- execution timestamp;
- duration;
- performance class;
- `EXPLAIN` output for queries slower than 5 seconds;
- row count;
- result columns;
- preview rows;
- SHA-256 hash of the full returned result.
- semantic audit fields for v2, including relationship risk, dropped-row count, and final disposition.

## V2 Semantic Acceptance Gate

V2 accepts a query only when it executes and the SQL semantics match the Portuguese question.

- Relationships with `confirmed` confidence can use inner joins for business questions.
- Relationships with `likely` confidence must use `LEFT JOIN` plus an unmatched bucket, or the question must explicitly say it is restricted to mapped records.
- Relationships with `weak` confidence are allowed only for audit questions unless externally validated.
- Relationships with `rejected` confidence are allowed only for audit/data-quality questions, except when the SQL explicitly preserves unmapped codes and the wording says labels are shown only when mapped.
- Questions about UFs must filter to the 27 valid Brazilian UF codes or explicitly discuss invalid `SG_UF` codes.
- Rate questions must make denominator scope clear.

## Performance Policy

- `fast`: <= 1 second.
- `moderate`: > 1 and <= 5 seconds.
- `slow`: > 5 and <= 15 seconds.
- `too_slow_for_default_eval`: > 15 seconds.

Slow queries should be inspected with `EXPLAIN`. Use `EXPLAIN ANALYZE` selectively because it executes the query.

## Rejection Rules

A question is rejected or left pending when the SQL fails, is too ambiguous, requires unavailable external data, exposes unnecessary row-level personal detail, mutates the database, or depends on unsupported business assumptions.
