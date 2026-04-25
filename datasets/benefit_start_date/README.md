# Benefit Start Date Dataset

This dataset supports the `benefit_start_date` benchmark task.

## Files

- `eval-cases.yaml`: canonical promptfoo cases used in the benchmark
- `vars.csv`: tabular version of representative examples for larger runs or auxiliary analysis

## Dataset rules

- Keep the task fixed: extract the primary benefit start date only
- Add new bad cases as soon as they are discovered
- Prefer small, interpretable cases over large noisy corpora
- Use metadata fields to keep cases filterable by category
