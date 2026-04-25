# Benefit Start Date Prompts

This folder stores the prompt versions used by the `promptfoo` benchmark for the `benefit_start_date` extraction task.

## Conventions

- `01_`, `02_`, ... keeps execution order explicit.
- Each file should solve the same task with one controlled variation in framing.
- The variable name is `{{text_blob}}` across all prompt versions.
- Prompts must stay short and deterministic because the benchmark is about extraction fidelity, not generation quality.
- Keep output instructions explicit: the expected response is the date string only.

## Current versions

| File | Intent |
| --- | --- |
| `01_direct.txt` | Minimal instruction, direct extraction |
| `02_roleplay.txt` | Persona framing to test instruction adherence |
| `03_chain_of_thought.txt` | More verbose analytical framing to measure whether extra reasoning hurts extraction |
| `04_qa_format.txt` | Question/answer framing |
| `05_emphasis.txt` | Same task with stronger output constraint wording |

## Editing rule

When adding a new version, keep the same task, same variable, and same dataset. Otherwise the comparison stops being an apples-to-apples prompt experiment.

## Review checklist for new prompt versions

- Same task as existing prompts
- Same variable contract
- No hidden few-shot examples unless intentionally applied to all variants
- Output format still constrained to the date only
- Added to `configs/promptfoo.yaml`
