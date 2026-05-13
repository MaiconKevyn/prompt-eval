# Stage 2 Readiness Notes

Generated at: 2026-05-13T09:42:16

## What Is Ready

- A validated Stage 1 Text-to-SQL benchmark exists with `100` executable question/SQL pairs.
- The schema, relationship map, business dictionary, and data-quality report are generated from the real DuckDB file.
- Query evidence exists for every accepted ground-truth item.

## Chatbot Requirements Derived From Stage 1

- The chatbot must always distinguish residence geography (`MUNIC_RES`) from hospital geography (`hospital.MUNIC_MOV`).
- The chatbot must warn users that joining procedures can multiply admissions unless the query intentionally counts procedure occurrences.
- The chatbot must cite whether a metric is based on `VAL_TOT` or component fields.
- The chatbot must use CID/procedure/hospital/municipality dimensions for human-readable answers.
- The chatbot should refuse or ask a clarification when the user asks for undefined terms such as "custo", "produção", "mortalidade" or "local" without specifying denominator/date/geography.

## Known Data Quality Caveats

| id | title | severity | affected_rows |
| --- | --- | --- | --- |
| DQ002 | DT_INTER fora do periodo 2007-2023 | high | 27 |
| DQ010 | Internacoes com municipio de residencia sem correspondencia | high | 1270397 |
| DQ011 | Diagnosticos principais sem correspondencia na tabela CID | high | 1044 |
| DQ012 | Procedimentos realizados sem descricao | high | 627 |

## Baseline Evaluation Metrics For Stage 2

- SQL execution accuracy.
- Answer correctness against query evidence.
- Correct use of denominator and date field.
- Correct handling of joins that multiply rows.
- Caveat/citation quality.
- Latency.
- Refusal or clarification accuracy for ambiguous questions.
