# Database Overview: sihrd5.duckdb

Generated at: 2026-05-13T09:42:16

## Scope

**Observed:** `sihrd5.duckdb` is a DuckDB database with `234` tables: `23` analytical tables in schema `main` and `211` dbt audit tables in schema `main_dbt_test__audit`.

**Observed:** the main fact table `internacoes` has `183,877,219` rows and the bridge/detail table `internacao_procedimento` has `187,957,888` rows. The database therefore appears to model SIH/SUS hospital admissions (AIH/internacoes), procedures, hospitals, municipalities, clinical diagnoses, and socioeconomic context.

**Observed:** `PRAGMA database_size` reports the database size as `25.0 GiB`. Main-schema table storage estimates are derived from `PRAGMA storage_info` persistent block ids, so they are approximate and intended for prioritizing exploration rather than billing or physical storage guarantees.

**Inferred:** one row in `internacoes` most likely represents one hospital admission/AIH-level event. `internacao_procedimento` links admissions to performed procedures and can contain multiple records per admission.

**Unknown:** official DATASUS field definitions were not fetched in this run. Field meanings below are inferred from table/column names, dimension descriptions, and executed SQL evidence.

## Table Inventory

| table_schema | table_name | table_type | classificacao | row_count |
| --- | --- | --- | --- | --- |
| main | car_int | BASE TABLE | dimensao/referencia | 6 |
| main | cbor | BASE TABLE | dimensao/referencia | 2812 |
| main | cid | BASE TABLE | dimensao/referencia | 14253 |
| main | complexidade | BASE TABLE | dimensao/referencia | 3 |
| main | contraceptivos | BASE TABLE | dimensao/referencia | 12 |
| main | especialidade | BASE TABLE | dimensao/referencia | 70 |
| main | etnia | BASE TABLE | dimensao/referencia | 264 |
| main | hospital | BASE TABLE | dimensao/referencia | 6873 |
| main | instrucao | BASE TABLE | dimensao/referencia | 4 |
| main | internacao_procedimento | BASE TABLE | fato/staging | 187957888 |
| main | internacoes | BASE TABLE | fato/staging | 183877219 |
| main | marca_uti | BASE TABLE | dimensao/referencia | 17 |
| main | municipios | BASE TABLE | dimensao/referencia | 5589 |
| main | nacionalidade | BASE TABLE | dimensao/referencia | 332 |
| main | procedimentos | BASE TABLE | dimensao/referencia | 5394 |
| main | raca_cor | BASE TABLE | dimensao/referencia | 5 |
| main | sexo | BASE TABLE | dimensao/referencia | 3 |
| main | socioeconomico | BASE TABLE | dimensao/referencia | 72395 |
| main | stg_hospital | BASE TABLE | outro | 6873 |
| main | stg_internacoes | BASE TABLE | fato/staging | 183877219 |
| main | stg_sexo | BASE TABLE | outro | 2 |
| main | tempo | BASE TABLE | dimensao/referencia | 6210 |
| main | vincprev | BASE TABLE | dimensao/referencia | 6 |

## Largest Main Tables By Estimated Storage

| table_schema | table_name | row_count | persistent_block_count | estimated_bytes | estimated_gib | database_size | sql | duration_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| main | internacoes | 183877219 | 33612 | 8811184128 | 8.2061 | 25.0 GiB | PRAGMA storage_info('internacoes') | 6.497 |
| main | stg_internacoes | 183877219 | 32005 | 8389918720 | 7.8137 | 25.0 GiB | PRAGMA storage_info('stg_internacoes') | 9.957 |
| main | internacao_procedimento | 187957888 | 5794 | 1518862336 | 1.4146 | 25.0 GiB | PRAGMA storage_info('internacao_procedimento') | 2.118 |
| main | socioeconomico | 72395 | 7 | 1835008 | 0.0017 | 25.0 GiB | PRAGMA storage_info('socioeconomico') | 0.002 |
| main | cid | 14253 | 2 | 524288 | 0.0005 | 25.0 GiB | PRAGMA storage_info('cid') | 0.001 |
| main | car_int | 6 | 1 | 262144 | 0.0002 | 25.0 GiB | PRAGMA storage_info('car_int') | 0.001 |
| main | cbor | 2812 | 1 | 262144 | 0.0002 | 25.0 GiB | PRAGMA storage_info('cbor') | 0.001 |
| main | complexidade | 3 | 1 | 262144 | 0.0002 | 25.0 GiB | PRAGMA storage_info('complexidade') | 0.0 |
| main | contraceptivos | 12 | 1 | 262144 | 0.0002 | 25.0 GiB | PRAGMA storage_info('contraceptivos') | 0.001 |
| main | especialidade | 70 | 1 | 262144 | 0.0002 | 25.0 GiB | PRAGMA storage_info('especialidade') | 0.001 |

## dbt Audit Tables

**Observed:** schema `main_dbt_test__audit` contains `211` tables, mostly named after accepted-value/range tests. These look like persisted dbt audit/failure tables and should be treated as quality evidence, not primary analytical facts.

## Temporal Coverage Snapshot

| ano | internacoes |
| --- | --- |
| 2000 | 9 |
| 2001 | 2 |
| 2002 | 2 |
| 2003 | 1 |
| 2005 | 6 |
| 2006 | 7 |
| 2007 | 602947 |
| 2008 | 10847458 |
| 2009 | 11114857 |
| 2010 | 11347880 |
| 2011 | 11267097 |
| 2012 | 11103250 |
| 2013 | 11179438 |
| 2014 | 11353704 |
| 2015 | 11325421 |
| 2016 | 11256224 |
| 2017 | 11522847 |
| 2018 | 11857648 |
| 2019 | 12185437 |
| 2020 | 10531843 |
| 2021 | 11566528 |
| 2022 | 12363889 |
| 2023 | 12450724 |

## UF Residence Snapshot

| SG_UF | internacoes | valor_total |
| --- | --- | --- |
| SP | 37750172 | 65999677549.54 |
| MG | 19403123 | 34899738095.24 |
| BA | 13289208 | 15655044149.59 |
| PR | 12700186 | 24007925832.21 |
| RS | 11834981 | 20292376586.16 |
| RJ | 10939273 | 17238517757.09 |
| PE | 8532465 | 13502252721.22 |
| PA | 7958966 | 7478331366.4 |
| CE | 7813316 | 10417216394.28 |
| SC | 7223756 | 12996451904.97 |
| MA | 6804713 | 6401860266.55 |
| GO | 6179099 | 8855861956.94 |
| ES | 3656717 | 5938445961.28 |
| PI | 3338399 | 3368022229.32 |
| PB | 3223339 | 4414466432.71 |
| MT | 3028008 | 3904079438.57 |
| AM | 2877882 | 3283628918.7 |
| AL | 2724676 | 3567420178.33 |
| RN | 2708573 | 4314434369.79 |
| MS | 2706080 | 4129896893.26 |
| RO | 1738501 | 1846169112.29 |
| SE | 1484587 | 2126006432.7 |
| TO | 1465583 | 1676243390.83 |
| DF | 1264585 | 1956743257.45 |
| AC | 772507 | 720567357.8 |
| RR | 601447 | 593208943.82 |
| AP | 586680 | 496805211.33 |

## Top Procedures

| PROC_REA | NOME_PROC | ocorrencias |
| --- | --- | --- |
| 310010039 | PARTO NORMAL | 16435256 |
| 303140151 | TRATAMENTO DE PNEUMONIAS OU INFLUENZA (GRIPE) | 10576911 |
| 411010034 | PARTO CESARIANO | 10309968 |
| 303010061 | TRATAMENTO DE DOENCAS INFECCIOSAS INTESTINAIS | 4507648 |
| 303170093 | TRATAMENTO EM PSIQUIATRIA (POR DIA) | 4214855 |
| 303140046 | TRATAMENTO DAS DOENCAS CRONICAS DAS VIAS AEREAS INFERIORES | 3735530 |
| 303010037 | TRATAMENTO DE OUTRAS DOENCAS BACTERIANAS | 3723552 |
| 303060212 | TRATAMENTO DE INSUFICIENCIA CARDIACA | 3636826 |
| 415010012 | TRATAMENTO C/ CIRURGIAS MULTIPLAS | 3353755 |
| 303100044 | TRATAMENTO DE INTERCORRENCIAS CLINICAS NA GRAVIDEZ | 3139159 |
| 301060088 | DIAGNOSTICO E/OU ATENDIMENTO DE URGENCIA EM CLINICA MEDICA | 3120396 |
| 303040149 | TRATAMENTO DE ACIDENTE VASCULAR CEREBRAL - AVC (ISQUEMICO OU HEMORRAGICO AGUDO) | 3017652 |
| 411020013 | CURETAGEM POS-ABORTAMENTO / PUERPERAL | 2839585 |
| 303150050 | TRATAMENTO DE OUTRAS DOENCAS DO APARELHO URINARIO | 2347762 |
| 411010026 | PARTO CESARIANO EM GESTACAO DE ALTO RISCO | 2068691 |
| 407030026 | COLECISTECTOMIA | 1998158 |
| 407040102 | HERNIOPLASTIA INGUINAL / CRURAL (UNILATERAL) | 1868884 |
| 304100021 | TRATAMENTO CLINICO DE PACIENTE ONCOLOGICO | 1813092 |
| 303010223 | TRATAMENTO DE INFECCAO PELO CORONAVIRUS ? COVID 19 | 1792677 |
| 305020013 | TRATAMENTO DA PIELONEFRITE | 1789419 |

## Top CID Chapters

| DS_CAPITULO | internacoes |
| --- | --- |
| XV. Gravidez, parto e puerpério | 37670769 |
| X. Doenças do aparelho respiratório | 19690732 |
| IX. Doenças do aparelho circulatório | 18158828 |
| XIX. Lesões, envenenamento e outras consequências de causas externas | 17789367 |
| XI. Doenças do aparelho digestivo | 17325707 |
| I. Algumas doenças infecciosas e parasitárias | 14907800 |
| XIV. Doenças do aparelho geniturinário | 12654302 |
| II. Neoplasias [tumores] | 11975513 |
| XVI. Algumas afecções originadas no período perinatal | 4192852 |
| IV. Doenças endócrinas, nutricionais e metabólicas | 4090558 |
| V. Transtornos mentais e comportamentais | 3926755 |
| XXI. Fatores que influenciam o estado de saúde | 3885467 |
| XII. Doenças da pele e do tecido subcutâneo | 3737369 |
| XIII. Doenças do sistema osteomuscular e do tecido conjuntivo | 3241585 |
| VI. Doenças do sistema nervoso | 2963099 |
| XVIII. Sintomas, sinais e achados anormais | 2871002 |
| VII. Doenças do olho e anexos | 1642482 |
| III. Doenças do sangue e dos órgãos hematopoéticos | 1536821 |
| XVII. Malformações congênitas, deformidades e anomalias cromossômicas | 1284877 |
| VIII. Doenças do ouvido e da apófise mastóide | 299473 |

## Executed Inventory SQL

```sql
SELECT * FROM information_schema.tables ORDER BY table_schema, table_name;
```

```sql
SELECT table_schema, table_name, column_name, data_type, is_nullable
FROM information_schema.columns
ORDER BY table_schema, table_name, ordinal_position;
```

```sql
SELECT COUNT(*) FROM <schema>.<table>;
```

```sql
PRAGMA database_size;
PRAGMA storage_info('<main_table_name>');
```
