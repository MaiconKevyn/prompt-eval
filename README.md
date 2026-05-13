# Health System Chatbot

Projeto para preparar um chatbot Text-to-SQL sobre dados hospitalares do
SIH/SUS a partir do banco local `sihrd5.duckdb`.

## Status Atual

Stage 1 esta concluida como fase de entendimento de dados e preparacao de
avaliacao. O chatbot ainda nao foi implementado nesta etapa.

Artefatos gerados:

- catalogo tecnico do banco, tabelas, colunas e perfis;
- dicionario de negocio para usuarios de saude no Brasil;
- mapa de relacionamentos e chaves candidatas;
- relatorio de qualidade de dados;
- metodologia de desenho das consultas;
- ground truth Text-to-SQL validado com 100 perguntas;
- evidencias de resultado para todas as queries aceitas;
- notas de prontidao para Stage 2.

## Banco de Dados

O banco principal e `sihrd5.duckdb`, com cerca de 25 GiB no ambiente local. Ele
nao deve ser versionado no Git.

O `.gitignore` bloqueia:

- `*.duckdb`
- `*.duckdb.wal`
- `*.duckdb.tmp`

## Estrutura

```text
.
|-- GOAL.md
|-- docs/
|   |-- database_overview.md
|   |-- schema_catalog.md
|   |-- business_dictionary.md
|   |-- relationship_map.md
|   |-- data_quality_report.md
|   |-- query_design_methodology.md
|   |-- stage2_readiness.md
|   `-- generated/
|-- evaluation/
|   `-- ground_truth/
|       |-- manifest.json
|       |-- stage1_questions.jsonl
|       |-- stage1_questions.md
|       |-- rejected_questions.md
|       `-- query_results/
`-- scripts/
    |-- sihrd5_stage1.py
    `-- verify_stage1.py
```

## Stage 1

O plano executado esta em `GOAL.md`.

Resultados principais:

- 234 tabelas inventariadas.
- 23 tabelas no schema analitico `main`.
- 211 tabelas de auditoria dbt em `main_dbt_test__audit`.
- 2.415 colunas catalogadas.
- 166 colunas do schema `main` perfiladas.
- 23 estimativas de armazenamento de tabelas.
- 23 chaves candidatas confirmadas.
- 20 relacionamentos avaliados.
- 15 checagens de qualidade de dados.
- 100 perguntas Text-to-SQL validadas.

Distribuicao do ground truth:

| Dificuldade | Quantidade |
| --- | ---: |
| L1 | 15 |
| L2 | 25 |
| L3 | 25 |
| L4 | 20 |
| L5 | 15 |

## Gerar Artefatos

Requer um ambiente Python com `duckdb` instalado e o arquivo `sihrd5.duckdb` na
raiz do projeto.

```bash
.venv/bin/python scripts/sihrd5_stage1.py
```

O script abre o banco em modo read-only, executa consultas de inventario,
perfilamento, qualidade e validacao, e escreve os artefatos em `docs/` e
`evaluation/ground_truth/`.

## Verificar

```bash
.venv/bin/python scripts/verify_stage1.py
```

Ultima verificacao executada:

```text
PASS: Stage 1 artifacts verified
questions=100 distribution={'L1': 15, 'L2': 25, 'L3': 25, 'L4': 20, 'L5': 15}
evidence_files=100
```

Tambem foi feita uma reexecucao independente das 100 queries salvas contra
`sihrd5.duckdb`, comparando row counts e hashes dos resultados com as evidencias
armazenadas:

```text
reexecuted=100 seconds=92.039 failures=0
```

## Stage 2

A implementacao do chatbot deve comecar somente depois de consumir os achados da
Stage 1, especialmente:

- diferenciar municipio de residencia (`MUNIC_RES`) de municipio do hospital
  (`hospital.MUNIC_MOV`);
- evitar multiplicacao acidental de internacoes ao juntar procedimentos;
- declarar se metricas financeiras usam `VAL_TOT` ou componentes;
- usar dimensoes de CID, procedimento, hospital e municipio para respostas
  legiveis;
- pedir esclarecimento ou recusar perguntas ambiguas sobre custo, producao,
  mortalidade ou local sem denominador e recorte definidos.
