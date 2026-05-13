# Query Design Methodology

Generated at: 2026-05-13T09:42:16

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
- row count;
- result columns;
- preview rows;
- SHA-256 hash of the full returned result.

## Rejection Rules

A question is rejected or left pending when the SQL fails, is too ambiguous, requires unavailable external data, exposes unnecessary row-level personal detail, mutates the database, or depends on unsupported business assumptions.
