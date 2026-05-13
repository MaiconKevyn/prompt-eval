# Relationship Map

Generated at: 2026-05-13T09:42:16

## Candidate Keys

Candidate-key confidence is **observed** from null checks and exact distinct-key counts. A key is `confirmed` only when it has zero null-key rows and zero duplicate-key rows.

| table | candidate_key | row_count | null_key_rows | distinct_key_count | duplicate_key_rows | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| car_int | CAR_INT | 6 | 0 | 6 | 0 | confirmed |
| cbor | CBOR | 2812 | 0 | 2812 | 0 | confirmed |
| cid | CID | 14253 | 0 | 14253 | 0 | confirmed |
| complexidade | COMPLEX | 3 | 0 | 3 | 0 | confirmed |
| contraceptivos | CONTRACEPTIVO | 12 | 0 | 12 | 0 | confirmed |
| especialidade | ESPEC | 70 | 0 | 70 | 0 | confirmed |
| etnia | ETNIA | 264 | 0 | 264 | 0 | confirmed |
| hospital | CNES | 6873 | 0 | 6873 | 0 | confirmed |
| instrucao | INSTRU | 4 | 0 | 4 | 0 | confirmed |
| internacao_procedimento | id_atendimento | 187957888 | 0 | 187957888 | 0 | confirmed |
| internacoes | N_AIH | 183877219 | 0 | 183877219 | 0 | confirmed |
| marca_uti | MARCA_UTI | 17 | 0 | 17 | 0 | confirmed |
| municipios | CO_MUNICIPIO_6D | 5589 | 0 | 5589 | 0 | confirmed |
| nacionalidade | NACIONAL | 332 | 0 | 332 | 0 | confirmed |
| procedimentos | PROC_REA | 5394 | 0 | 5394 | 0 | confirmed |
| raca_cor | RACA_COR | 5 | 0 | 5 | 0 | confirmed |
| sexo | SEXO | 3 | 0 | 3 | 0 | confirmed |
| socioeconomico | CO_MUNICIPIO_6D, NU_ANO | 72395 | 0 | 72395 | 0 | confirmed |
| stg_hospital | CNES | 6873 | 0 | 6873 | 0 | confirmed |
| stg_internacoes | N_AIH | 183877219 | 0 | 183877219 | 0 | confirmed |
| stg_sexo | SEXO | 2 | 0 | 2 | 0 | confirmed |
| tempo | data | 6210 | 0 | 6210 | 0 | confirmed |
| vincprev | VINCPREV | 6 | 0 | 6 | 0 | confirmed |

Relationship confidence is based on non-null match coverage:

- `confirmed`: >= 99.5%
- `likely`: >= 95%
- `weak`: >= 80%
- `rejected`: < 80% or unavailable

| left | right | meaning | left_rows | matched_rows | unmatched_rows | match_rate_non_null | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| internacoes.CNES | hospital.CNES | Hospital de atendimento pela chave CNES | 183877219 | 183877219 | 0 | 1.0 | confirmed |
| hospital.MUNIC_MOV | municipios.CO_MUNICIPIO_6D | Municipio de movimento/estabelecimento | 6873 | 6851 | 22 | 0.9967990688200203 | confirmed |
| internacoes.MUNIC_RES | municipios.CO_MUNICIPIO_6D | Municipio de residencia do usuario | 183877219 | 182606822 | 1270397 | 0.9930910582240207 | likely |
| internacoes.SEXO | sexo.SEXO | Sexo do usuario | 183877219 | 183877219 | 0 | 1.0 | confirmed |
| internacoes.RACA_COR | raca_cor.RACA_COR | Raca/cor informada | 183877219 | 135116406 | 48760813 | 0.7348186291636268 | rejected |
| internacoes.ETNIA | etnia.ETNIA | Etnia informada | 183877219 | 375040 | 183502179 | 0.0020396218848622027 | rejected |
| internacoes.NACIONAL | nacionalidade.NACIONAL | Nacionalidade | 183877219 | 183877185 | 34 | 0.9999998150940057 | confirmed |
| internacoes.INSTRU | instrucao.INSTRU | Instrucao/escolaridade | 183877219 | 1757501 | 182119718 | 0.009558013817905305 | rejected |
| internacoes.VINCPREV | vincprev.VINCPREV | Vinculo previdenciario | 183877219 | 18864 | 183858355 | 0.00010259019634183177 | rejected |
| internacoes.CAR_INT | car_int.CAR_INT | Carater da internacao | 183877219 | 183877219 | 0 | 1.0 | confirmed |
| internacoes.ESPEC | especialidade.ESPEC | Especialidade/leito | 183877219 | 183874401 | 2818 | 0.9999846745561233 | confirmed |
| internacoes.COMPLEX | complexidade.COMPLEX | Complexidade do atendimento | 183877219 | 183877207 | 12 | 0.9999999347390609 | confirmed |
| internacoes.MARCA_UTI | marca_uti.MARCA_UTI | Marcador/tipo de UTI | 183877219 | 183877219 | 0 | 1.0 | confirmed |
| internacoes.CBOR | cbor.CBOR | Ocupacao CBO-R | 183877219 | 18864 | 183858355 | 0.00010259019634183177 | rejected |
| internacoes.DIAG_PRINC | cid.CID | Diagnostico principal CID | 183877219 | 183876175 | 1044 | 0.9999943222982941 | confirmed |
| internacoes.DIAG_SECUN | cid.CID | Diagnostico secundario CID | 183877219 | 10543926 | 173333293 | 0.05734220942290845 | rejected |
| internacoes.CID_MORTE | cid.CID | CID da morte | 183877219 | 2871985 | 181005234 | 0.01561903652675974 | rejected |
| internacao_procedimento.N_AIH | internacoes.N_AIH | Procedimentos vinculados a AIH/internacao | 187957888 | 187957888 | 0 | 1.0 | confirmed |
| internacao_procedimento.PROC_REA | procedimentos.PROC_REA | Procedimento realizado | 187957888 | 187957261 | 627 | 0.9999966641463858 | confirmed |
| socioeconomico.CO_MUNICIPIO_6D | municipios.CO_MUNICIPIO_6D | Indicadores socioeconomicos por municipio | 72395 | 72395 | 0 | 1.0 | confirmed |

## SQL Evidence

### Candidate Key Checks

#### car_int (CAR_INT)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CAR_INT" IS NULL) AS null_key_rows, COUNT(DISTINCT "CAR_INT") AS distinct_key_count FROM "car_int"
```

#### cbor (CBOR)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CBOR" IS NULL) AS null_key_rows, COUNT(DISTINCT "CBOR") AS distinct_key_count FROM "cbor"
```

#### cid (CID)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CID" IS NULL) AS null_key_rows, COUNT(DISTINCT "CID") AS distinct_key_count FROM "cid"
```

#### complexidade (COMPLEX)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "COMPLEX" IS NULL) AS null_key_rows, COUNT(DISTINCT "COMPLEX") AS distinct_key_count FROM "complexidade"
```

#### contraceptivos (CONTRACEPTIVO)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CONTRACEPTIVO" IS NULL) AS null_key_rows, COUNT(DISTINCT "CONTRACEPTIVO") AS distinct_key_count FROM "contraceptivos"
```

#### especialidade (ESPEC)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "ESPEC" IS NULL) AS null_key_rows, COUNT(DISTINCT "ESPEC") AS distinct_key_count FROM "especialidade"
```

#### etnia (ETNIA)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "ETNIA" IS NULL) AS null_key_rows, COUNT(DISTINCT "ETNIA") AS distinct_key_count FROM "etnia"
```

#### hospital (CNES)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CNES" IS NULL) AS null_key_rows, COUNT(DISTINCT "CNES") AS distinct_key_count FROM "hospital"
```

#### instrucao (INSTRU)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "INSTRU" IS NULL) AS null_key_rows, COUNT(DISTINCT "INSTRU") AS distinct_key_count FROM "instrucao"
```

#### internacao_procedimento (id_atendimento)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "id_atendimento" IS NULL) AS null_key_rows, COUNT(DISTINCT "id_atendimento") AS distinct_key_count FROM "internacao_procedimento"
```

#### internacoes (N_AIH)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "N_AIH" IS NULL) AS null_key_rows, COUNT(DISTINCT "N_AIH") AS distinct_key_count FROM "internacoes"
```

#### marca_uti (MARCA_UTI)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "MARCA_UTI" IS NULL) AS null_key_rows, COUNT(DISTINCT "MARCA_UTI") AS distinct_key_count FROM "marca_uti"
```

#### municipios (CO_MUNICIPIO_6D)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CO_MUNICIPIO_6D" IS NULL) AS null_key_rows, COUNT(DISTINCT "CO_MUNICIPIO_6D") AS distinct_key_count FROM "municipios"
```

#### nacionalidade (NACIONAL)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "NACIONAL" IS NULL) AS null_key_rows, COUNT(DISTINCT "NACIONAL") AS distinct_key_count FROM "nacionalidade"
```

#### procedimentos (PROC_REA)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "PROC_REA" IS NULL) AS null_key_rows, COUNT(DISTINCT "PROC_REA") AS distinct_key_count FROM "procedimentos"
```

#### raca_cor (RACA_COR)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "RACA_COR" IS NULL) AS null_key_rows, COUNT(DISTINCT "RACA_COR") AS distinct_key_count FROM "raca_cor"
```

#### sexo (SEXO)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "SEXO" IS NULL) AS null_key_rows, COUNT(DISTINCT "SEXO") AS distinct_key_count FROM "sexo"
```

#### socioeconomico (CO_MUNICIPIO_6D, NU_ANO)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CO_MUNICIPIO_6D" IS NULL OR "NU_ANO" IS NULL) AS null_key_rows, (SELECT COUNT(*) FROM (SELECT "CO_MUNICIPIO_6D", "NU_ANO" FROM "socioeconomico" WHERE NOT ("CO_MUNICIPIO_6D" IS NULL OR "NU_ANO" IS NULL) GROUP BY "CO_MUNICIPIO_6D", "NU_ANO") keys) AS distinct_key_count FROM "socioeconomico"
```

#### stg_hospital (CNES)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "CNES" IS NULL) AS null_key_rows, COUNT(DISTINCT "CNES") AS distinct_key_count FROM "stg_hospital"
```

#### stg_internacoes (N_AIH)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "N_AIH" IS NULL) AS null_key_rows, COUNT(DISTINCT "N_AIH") AS distinct_key_count FROM "stg_internacoes"
```

#### stg_sexo (SEXO)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "SEXO" IS NULL) AS null_key_rows, COUNT(DISTINCT "SEXO") AS distinct_key_count FROM "stg_sexo"
```

#### tempo (data)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "data" IS NULL) AS null_key_rows, COUNT(DISTINCT "data") AS distinct_key_count FROM "tempo"
```

#### vincprev (VINCPREV)

```sql
SELECT COUNT(*) AS row_count, COUNT(*) FILTER (WHERE "VINCPREV" IS NULL) AS null_key_rows, COUNT(DISTINCT "VINCPREV") AS distinct_key_count FROM "vincprev"
```

### Relationship Coverage Checks

#### internacoes.CNES -> hospital.CNES

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."CNES") AS non_null_left_key, COUNT(r."CNES") AS matched_rows, COUNT(*) - COUNT(r."CNES") AS unmatched_rows, COUNT(r."CNES")::DOUBLE / NULLIF(COUNT(l."CNES"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "hospital" r ON l."CNES" = r."CNES" WHERE l."CNES" IS NOT NULL
```

#### hospital.MUNIC_MOV -> municipios.CO_MUNICIPIO_6D

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."MUNIC_MOV") AS non_null_left_key, COUNT(r."CO_MUNICIPIO_6D") AS matched_rows, COUNT(*) - COUNT(r."CO_MUNICIPIO_6D") AS unmatched_rows, COUNT(r."CO_MUNICIPIO_6D")::DOUBLE / NULLIF(COUNT(l."MUNIC_MOV"), 0) AS match_rate_non_null FROM "hospital" l LEFT JOIN "municipios" r ON l."MUNIC_MOV" = r."CO_MUNICIPIO_6D" WHERE l."MUNIC_MOV" IS NOT NULL
```

#### internacoes.MUNIC_RES -> municipios.CO_MUNICIPIO_6D

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."MUNIC_RES") AS non_null_left_key, COUNT(r."CO_MUNICIPIO_6D") AS matched_rows, COUNT(*) - COUNT(r."CO_MUNICIPIO_6D") AS unmatched_rows, COUNT(r."CO_MUNICIPIO_6D")::DOUBLE / NULLIF(COUNT(l."MUNIC_RES"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "municipios" r ON l."MUNIC_RES" = r."CO_MUNICIPIO_6D" WHERE l."MUNIC_RES" IS NOT NULL
```

#### internacoes.SEXO -> sexo.SEXO

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."SEXO") AS non_null_left_key, COUNT(r."SEXO") AS matched_rows, COUNT(*) - COUNT(r."SEXO") AS unmatched_rows, COUNT(r."SEXO")::DOUBLE / NULLIF(COUNT(l."SEXO"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "sexo" r ON l."SEXO" = r."SEXO" WHERE l."SEXO" IS NOT NULL
```

#### internacoes.RACA_COR -> raca_cor.RACA_COR

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."RACA_COR") AS non_null_left_key, COUNT(r."RACA_COR") AS matched_rows, COUNT(*) - COUNT(r."RACA_COR") AS unmatched_rows, COUNT(r."RACA_COR")::DOUBLE / NULLIF(COUNT(l."RACA_COR"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "raca_cor" r ON l."RACA_COR" = r."RACA_COR" WHERE l."RACA_COR" IS NOT NULL
```

#### internacoes.ETNIA -> etnia.ETNIA

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."ETNIA") AS non_null_left_key, COUNT(r."ETNIA") AS matched_rows, COUNT(*) - COUNT(r."ETNIA") AS unmatched_rows, COUNT(r."ETNIA")::DOUBLE / NULLIF(COUNT(l."ETNIA"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "etnia" r ON l."ETNIA" = r."ETNIA" WHERE l."ETNIA" IS NOT NULL
```

#### internacoes.NACIONAL -> nacionalidade.NACIONAL

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."NACIONAL") AS non_null_left_key, COUNT(r."NACIONAL") AS matched_rows, COUNT(*) - COUNT(r."NACIONAL") AS unmatched_rows, COUNT(r."NACIONAL")::DOUBLE / NULLIF(COUNT(l."NACIONAL"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "nacionalidade" r ON l."NACIONAL" = r."NACIONAL" WHERE l."NACIONAL" IS NOT NULL
```

#### internacoes.INSTRU -> instrucao.INSTRU

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."INSTRU") AS non_null_left_key, COUNT(r."INSTRU") AS matched_rows, COUNT(*) - COUNT(r."INSTRU") AS unmatched_rows, COUNT(r."INSTRU")::DOUBLE / NULLIF(COUNT(l."INSTRU"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "instrucao" r ON l."INSTRU" = r."INSTRU" WHERE l."INSTRU" IS NOT NULL
```

#### internacoes.VINCPREV -> vincprev.VINCPREV

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."VINCPREV") AS non_null_left_key, COUNT(r."VINCPREV") AS matched_rows, COUNT(*) - COUNT(r."VINCPREV") AS unmatched_rows, COUNT(r."VINCPREV")::DOUBLE / NULLIF(COUNT(l."VINCPREV"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "vincprev" r ON l."VINCPREV" = r."VINCPREV" WHERE l."VINCPREV" IS NOT NULL
```

#### internacoes.CAR_INT -> car_int.CAR_INT

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."CAR_INT") AS non_null_left_key, COUNT(r."CAR_INT") AS matched_rows, COUNT(*) - COUNT(r."CAR_INT") AS unmatched_rows, COUNT(r."CAR_INT")::DOUBLE / NULLIF(COUNT(l."CAR_INT"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "car_int" r ON l."CAR_INT" = r."CAR_INT" WHERE l."CAR_INT" IS NOT NULL
```

#### internacoes.ESPEC -> especialidade.ESPEC

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."ESPEC") AS non_null_left_key, COUNT(r."ESPEC") AS matched_rows, COUNT(*) - COUNT(r."ESPEC") AS unmatched_rows, COUNT(r."ESPEC")::DOUBLE / NULLIF(COUNT(l."ESPEC"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "especialidade" r ON l."ESPEC" = r."ESPEC" WHERE l."ESPEC" IS NOT NULL
```

#### internacoes.COMPLEX -> complexidade.COMPLEX

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."COMPLEX") AS non_null_left_key, COUNT(r."COMPLEX") AS matched_rows, COUNT(*) - COUNT(r."COMPLEX") AS unmatched_rows, COUNT(r."COMPLEX")::DOUBLE / NULLIF(COUNT(l."COMPLEX"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "complexidade" r ON l."COMPLEX" = r."COMPLEX" WHERE l."COMPLEX" IS NOT NULL
```

#### internacoes.MARCA_UTI -> marca_uti.MARCA_UTI

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."MARCA_UTI") AS non_null_left_key, COUNT(r."MARCA_UTI") AS matched_rows, COUNT(*) - COUNT(r."MARCA_UTI") AS unmatched_rows, COUNT(r."MARCA_UTI")::DOUBLE / NULLIF(COUNT(l."MARCA_UTI"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "marca_uti" r ON l."MARCA_UTI" = r."MARCA_UTI" WHERE l."MARCA_UTI" IS NOT NULL
```

#### internacoes.CBOR -> cbor.CBOR

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."CBOR") AS non_null_left_key, COUNT(r."CBOR") AS matched_rows, COUNT(*) - COUNT(r."CBOR") AS unmatched_rows, COUNT(r."CBOR")::DOUBLE / NULLIF(COUNT(l."CBOR"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "cbor" r ON l."CBOR" = r."CBOR" WHERE l."CBOR" IS NOT NULL
```

#### internacoes.DIAG_PRINC -> cid.CID

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."DIAG_PRINC") AS non_null_left_key, COUNT(r."CID") AS matched_rows, COUNT(*) - COUNT(r."CID") AS unmatched_rows, COUNT(r."CID")::DOUBLE / NULLIF(COUNT(l."DIAG_PRINC"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "cid" r ON l."DIAG_PRINC" = r."CID" WHERE l."DIAG_PRINC" IS NOT NULL
```

#### internacoes.DIAG_SECUN -> cid.CID

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."DIAG_SECUN") AS non_null_left_key, COUNT(r."CID") AS matched_rows, COUNT(*) - COUNT(r."CID") AS unmatched_rows, COUNT(r."CID")::DOUBLE / NULLIF(COUNT(l."DIAG_SECUN"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "cid" r ON l."DIAG_SECUN" = r."CID" WHERE l."DIAG_SECUN" IS NOT NULL
```

#### internacoes.CID_MORTE -> cid.CID

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."CID_MORTE") AS non_null_left_key, COUNT(r."CID") AS matched_rows, COUNT(*) - COUNT(r."CID") AS unmatched_rows, COUNT(r."CID")::DOUBLE / NULLIF(COUNT(l."CID_MORTE"), 0) AS match_rate_non_null FROM "internacoes" l LEFT JOIN "cid" r ON l."CID_MORTE" = r."CID" WHERE l."CID_MORTE" IS NOT NULL
```

#### internacao_procedimento.N_AIH -> internacoes.N_AIH

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."N_AIH") AS non_null_left_key, COUNT(r."N_AIH") AS matched_rows, COUNT(*) - COUNT(r."N_AIH") AS unmatched_rows, COUNT(r."N_AIH")::DOUBLE / NULLIF(COUNT(l."N_AIH"), 0) AS match_rate_non_null FROM "internacao_procedimento" l LEFT JOIN "internacoes" r ON l."N_AIH" = r."N_AIH" WHERE l."N_AIH" IS NOT NULL
```

#### internacao_procedimento.PROC_REA -> procedimentos.PROC_REA

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."PROC_REA") AS non_null_left_key, COUNT(r."PROC_REA") AS matched_rows, COUNT(*) - COUNT(r."PROC_REA") AS unmatched_rows, COUNT(r."PROC_REA")::DOUBLE / NULLIF(COUNT(l."PROC_REA"), 0) AS match_rate_non_null FROM "internacao_procedimento" l LEFT JOIN "procedimentos" r ON l."PROC_REA" = r."PROC_REA" WHERE l."PROC_REA" IS NOT NULL
```

#### socioeconomico.CO_MUNICIPIO_6D -> municipios.CO_MUNICIPIO_6D

```sql
SELECT COUNT(*) AS left_rows, COUNT(l."CO_MUNICIPIO_6D") AS non_null_left_key, COUNT(r."CO_MUNICIPIO_6D") AS matched_rows, COUNT(*) - COUNT(r."CO_MUNICIPIO_6D") AS unmatched_rows, COUNT(r."CO_MUNICIPIO_6D")::DOUBLE / NULLIF(COUNT(l."CO_MUNICIPIO_6D"), 0) AS match_rate_non_null FROM "socioeconomico" l LEFT JOIN "municipios" r ON l."CO_MUNICIPIO_6D" = r."CO_MUNICIPIO_6D" WHERE l."CO_MUNICIPIO_6D" IS NOT NULL
```
