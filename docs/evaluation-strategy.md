# Evaluation Strategy

This document captures the minimum AI engineering controls that apply to this repository in its current early-stage form.

## Scope

- Single benchmark task: extract the primary benefit start date from free text
- Single default local model: `ollama:chat:llama3.1:8b`
- Single canonical dataset: `datasets/benefit_start_date/eval-cases.yaml`

## Quality gates

- Every prompt variant must use the same input variable: `{{text_blob}}`
- Every prompt variant must target the same output contract: date string only
- Every change to prompt behavior should be checked against the canonical dataset
- New failure cases should be added to the dataset as regression coverage
- Accuracy is necessary but not sufficient; latency and token usage also matter

## Artifact policy

- `artifacts/generated/` is for fresh local outputs and should stay untracked
- `artifacts/fixtures/` is for intentionally preserved reference outputs
- Reports are useful only if they can be tied back to a known prompt set and model

## Change policy

- Do not change prompt wording, model, and dataset in the same experiment iteration unless the comparison goal explicitly requires it
- Prefer one controlled variable per round of evaluation
- Keep prompt additions small and isolated so the benchmark remains interpretable

## Recommended workflow

1. Add or modify one prompt version
2. Run `npm run eval`
3. Run `npm run report`
4. Review accuracy, output discipline, latency, and token usage together
5. Add any discovered bad case to the canonical dataset
