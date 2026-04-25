# Prompt Eval

[![Node.js](https://img.shields.io/badge/Node.js-runtime-5FA04E.svg)](https://nodejs.org/)
[![promptfoo](https://img.shields.io/badge/promptfoo-0.117.6-FF6B35.svg)](https://www.promptfoo.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-local-000000.svg)](https://ollama.com/)
[![Model](https://img.shields.io/badge/model-llama3.1%3A8b-4B8BBE.svg)](https://ollama.com/library/llama3.1)
[![Experiment](https://img.shields.io/badge/type-prompt%20benchmark-1f6feb.svg)](#scientific-intention)

> A prompt engineering benchmark designed to measure how different prompt formulations affect a closed structured extraction task: identifying the start date of a benefits plan from free text and returning only the date.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Evaluation](#running-the-evaluation)
- [Usage](#usage)
- [Experimental Design](#experimental-design)
- [Test Dataset](#test-dataset)
- [Scientific Intention](#scientific-intention)
- [Generated Artifacts](#generated-artifacts)
- [How To Read Results](#how-to-read-results)
- [Contributing Notes](#contributing-notes)

## Overview
**Prompt Eval** is not a chatbot and not a general-purpose extraction application. This repository was built as a controlled prompt evaluation experiment. The task stays fixed, the model stays fixed, and the dataset stays fixed; the main variable under study is the wording of the prompt.

### Key Capabilities
- **Controlled prompt comparison**: compares multiple prompt versions for the same task
- **Structured extraction benchmark**: measures whether the model returns only the correct date
- **Distractor resistance**: tests behavior when the input contains competing dates
- **Local reproducibility**: runs locally with `promptfoo` and `ollama`
- **Operational metrics**: measures accuracy, latency, and token usage in the same workflow
- **Report generation**: turns raw evaluation JSON into a readable HTML report

## Features
- **Prompt registry by file**: each prompt version lives in `prompts/benefit_start_date/`
- **Single-task evaluation**: all prompts solve exactly the same problem
- **File-based experiment wiring**: `configs/promptfoo.yaml` connects prompts, provider, and tests
- **Explicit expected-date assertions**: tests compare outputs against fixed expected values
- **Custom HTML summary**: `scripts/generate-html-report.js` produces a synthesized view of results
- **Scientific comparability**: the repository avoids changes that would break cross-run comparison

## Architecture
```text
Free-text benefit description
            |
            v
Prompt variant
(direct / roleplay / chain-of-thought / QA / emphasis)
            |
            v
promptfoo evaluation runner
            |
            v
ollama:chat:llama3.1:8b
            |
            v
Model output
"date only"
            |
            v
Assertions against expected date
            |
            v
Metrics: accuracy, latency, token usage
            |
            v
Artifacts: artifacts/generated/evaluation-results.json / promptfoo UI / artifacts/generated/evaluation-results.html
```

The core experimental architecture is intentionally simple: change the linguistic framing without changing the task. That reduces noise and makes it easier to observe whether prompt wording changes fidelity, cost, and stability.

## Technology Stack
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Evaluation framework** | `promptfoo` 0.117.6 | Runs prompts, providers, and assertions |
| **Inference provider** | `Ollama` | Serves the model locally |
| **Language model** | `llama3.1:8b` | Solves the extraction task |
| **Runtime** | `Node.js` | Scripts and evaluation commands |
| **Test cases** | YAML + CSV | Controlled cases and tabular examples |
| **Reporting** | Custom HTML generator | Summarizes score, tokens, and latency |

## Project Structure
```bash
prompt-eval/
├── CLAUDE.md                    # Experiment rules and repository hygiene
├── AGENTS.md                    # Instructions for future coding agents
├── configs/
│   └── promptfoo.yaml           # Connects prompts, provider, and tests
├── prompts/
│   └── benefit_start_date/
│       ├── 01_direct.txt        # Minimal direct instruction
│       ├── 02_roleplay.txt      # Persona framing to test adherence
│       ├── 03_chain_of_thought.txt
│       ├── 04_qa_format.txt
│       ├── 05_emphasis.txt
│       └── README.md            # Conventions for new prompt versions
├── datasets/
│   └── benefit_start_date/
│       ├── eval-cases.yaml      # Canonical promptfoo cases with metadata
│       └── vars.csv             # Tabular base for larger experiments
├── scripts/
│   └── generate-html-report.js  # Generates a custom HTML report
├── artifacts/
│   ├── fixtures/                # Reference outputs kept intentionally
│   └── generated/               # Fresh local outputs, ignored by git
├── docs/
│   └── evaluation-strategy.md   # Quality gates and benchmark policy
├── package.json                 # Project scripts
└── README.md                    # This file
```

## Getting Started
### Prerequisites
- **Node.js** installed locally
- **Ollama** installed and running
- **`llama3.1:8b`** available in Ollama

### Installation
1. **Enter the repository**
```bash
cd /home/maiconkevyn/PycharmProjects/prompt-eval
```

2. **Install dependencies**
```bash
npm install
```

3. **Pull the local model**
```bash
ollama pull llama3.1:8b
```

### Configuration
There is no large configuration layer in this project. The main experiment is defined in `configs/promptfoo.yaml`:

- prompts loaded from files in `prompts/benefit_start_date/`
- provider fixed to `ollama:chat:llama3.1:8b`
- tests loaded from `datasets/benefit_start_date/eval-cases.yaml`

If you want to change the model or provider, do it in that file. To preserve scientific comparability, do not change both the model and the prompt at the same time unless the change is explicitly documented.

### Running the Evaluation
1. **Run the benchmark**
```bash
npm run eval
```

2. **Open the default promptfoo visualization**
```bash
npm run view
```

3. **Generate the custom HTML report**
```bash
npm run report
```

Generated files are written to `artifacts/generated/`. Reference outputs that are intentionally kept in the repository live in `artifacts/fixtures/`.

## Usage
### What is being tested
Each prompt receives a `{{text_blob}}` and must respond with only the start date of the primary benefit.

### Example input
```text
Your coverage begins on March 15, 2024, but the premium dental plan benefits do not start until May 1, 2024. The vision plan starts at the same time as the main health coverage.
```

### Expected output
```text
March 15, 2024
```

### Prompt families currently included
- `01_direct.txt`: direct and minimal instruction
- `02_roleplay.txt`: extraction persona framing
- `03_chain_of_thought.txt`: more verbose analytical framing
- `04_qa_format.txt`: question and answer structure
- `05_emphasis.txt`: stronger output-only constraint

## Experimental Design
The experiment is built to answer one specific question: **does prompt wording change model behavior in a closed extraction task?**

### Controlled variables
- Same extraction problem
- Same model (`llama3.1:8b`)
- Same provider (`ollama`)
- Same variable name (`{{text_blob}}`)
- Same test set

### Independent variable
- Prompt wording

### Dependent variables
- **Accuracy**: whether the correct date is returned
- **Format adherence**: whether the model returns only the expected string
- **Latency**: response time per attempt
- **Token usage**: relative computational cost across prompts

### Why this matters
This kind of experiment is useful when a team wants to determine whether a more elaborate prompt actually improves extraction, or whether it only increases verbosity, cost, and behavioral variance.

## Test Dataset
The cases in `datasets/benefit_start_date/eval-cases.yaml` and `datasets/benefit_start_date/vars.csv` cover patterns that matter for robust extraction:

- explicit primary dates in simple sentences
- competing dates for secondary benefits
- wording variations such as "effective starting" and "commences on"
- different date formats, including ISO
- ordinal suffix dates such as `December 1st, 2023`
- relative-date language paired with the correct explicit date

The goal is not unlimited linguistic diversity. The goal is a small, controlled, interpretable dataset that supports prompt comparison without contaminating the experiment with unrelated variables.

## Scientific Intention
The real scientific intention of the project is not to "make the model think better." It is to test whether different instructions change:

- extraction fidelity
- the ability to ignore distractor dates
- obedience to a strict output format
- token cost for solving the same task
- the operational stability of a small local model

In other words, this repository functions as a micro-benchmark for prompt engineering. It is closer to a controlled evaluation experiment than to a production NLP application.

There is also an important methodological point: if two prompts solve the same cases equally well, the better prompt is not necessarily the one that looks more sophisticated. In a closed task, the better candidate may simply be the shorter, cheaper, and more predictable one.

## Generated Artifacts
After running the benchmark, the main artifacts are:

- `evaluation-results.json`: raw output with prompts, responses, score, latency, and tokens
- `results.html`: default `promptfoo` visualization
- `evaluation-results.html`: custom report generated by `generate-html-report.js`

These files make it possible to compare prompts by both quality and operational cost.

## How To Read Results
When interpreting results, use this order:

1. **Did it extract the correct date?**
2. **Did it return only the date, with no extra text?**
3. **Did it remain robust when competing dates were present?**
4. **Did it do that with lower latency and fewer tokens?**

If a more elaborate prompt does not improve the hard cases, it probably does not add scientific value in this benchmark. In closed extraction tasks, extra prompt sophistication can be noise.

## Contributing Notes
If you extend the experiment:

- keep the task fixed when comparing prompts
- document new versions in `prompts/benefit_start_date/README.md`
- add edge cases to the test set as soon as they are discovered
- do not mix structural refactoring with experiment changes without making that explicit
- keep `README.md`, prompts, and tests aligned whenever the benchmark changes
