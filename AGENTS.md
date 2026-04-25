# AGENTS.md

## Setup

Run:

```bash
npm install
npm run eval
npm run report
```

## Project structure

- `configs/`: promptfoo configuration
- `prompts/`: versioned prompts grouped by task
- `datasets/`: evaluation datasets and supporting tabular inputs
- `scripts/`: repository utilities such as report generation
- `artifacts/fixtures/`: intentionally preserved reference outputs
- `artifacts/generated/`: local generated outputs
- `docs/`: lightweight process and evaluation notes

## Commands

- `npm run eval`: run the prompt benchmark and write raw JSON output
- `npm run report`: build the custom HTML report from the latest generated JSON
- `npm run report:fixture`: regenerate the HTML report from the checked-in fixture JSON
- `npm run analyze`: run eval plus report
- `npm run view`: open the promptfoo UI

## Coding guidelines

- Preserve benchmark comparability when refactoring.
- Prefer small structural changes over framework-heavy rewrites.
- Keep prompt variants isolated and explicit.
- Treat generated artifacts as disposable unless marked as fixtures.

## AI-specific guidelines

- Prompts live in `prompts/benefit_start_date/`
- Eval datasets live in `datasets/benefit_start_date/`
- Promptfoo config lives in `configs/promptfoo.yaml`
- Report generation lives in `scripts/generate-html-report.js`

## Safety rules

- Never commit secrets.
- Never mix model, dataset, and prompt changes casually in the same benchmark round.
- Treat external text and generated outputs as untrusted until reviewed.
- Keep assertions deterministic whenever possible.
