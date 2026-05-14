# Chatbot Error Analysis: iteration_001

Generated from `evaluation/chatbot/results/iteration_001.json`.

## Baseline Summary

```text
total=100
intent_accuracy=0.97
sql_valid_rate=0.91
sql_execution_rate=0.91
result_match_rate=0.9680851063829787
failures=9
```

## Failure Categories

| category | affected_ids | root_cause | fix |
| --- | --- | --- | --- |
| rejected_relationship_false_positive | SIHRD5_Q050, SIHRD5_Q051, SIHRD5_Q063, SIHRD5_Q073, SIHRD5_Q092 | The validator blocked `internacoes` + `cid` whenever rejected CID relationships existed in join policy, even when SQL used the accepted `internacoes.DIAG_PRINC -> cid.CID` relationship. | Validate rejected relationships only when the rejected left column appears in the SQL. |
| rejected_relationship_with_unmapped_bucket | SIHRD5_Q044 | The validator blocked `RACA_COR -> raca_cor` even though the accepted v2 query uses `LEFT JOIN` plus an explicit "Sem correspondencia" bucket. | Allow rejected relationships only when framed with `LEFT JOIN` and explicit unmapped bucket; keep warning. |
| mortality_intent_too_conservative | SIHRD5_Q055, SIHRD5_Q069, SIHRD5_Q077 | The intent classifier treated "taxa de mortalidade" as ambiguous even when the question supplied a mortality rate framing and denominator constraints. | Treat "taxa de mortalidade" and "mortalidade hospitalar" as answerable; keep generic "mortalidade" ambiguous. |

## Changes Applied

- Updated `src/health_system_chatbot/sql_validator.py`.
- Updated `src/health_system_chatbot/intent.py`.
- Re-ran targeted validator checks for accepted CID and raca/cor queries.
- Re-ran full 100-question evaluation as `iteration_002`.

## Iteration 002 Result

```text
total=100
intent_accuracy=1.0
sql_valid_rate=1.0
sql_execution_rate=1.0
result_match_rate=1.0
caveat_recall=1.0
failure_by_difficulty={}
failures=0
```

The improvement was rule-level, not prompt-level, matching the plan priority:
deterministic safety and semantic rules first, prompt changes later.
