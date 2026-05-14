# Data Quality Report

Generated at: 2026-05-13T19:23:25

## Summary

| id | title | severity | affected_rows | blocks_ground_truth |
| --- | --- | --- | --- | --- |
| DQ001 | Altas anteriores a internacao | critical | 0 | False |
| DQ002 | DT_INTER fora do periodo 2007-2023 | high | 27 | True |
| DQ003 | DT_SAIDA fora do periodo 2007-2023 | high | 0 | False |
| DQ004 | DIAS_PERM diferente da diferenca simples entre saida e entrada | medium | 172581441 | False |
| DQ005 | Valores financeiros negativos | critical | 0 | False |
| DQ006 | Idades fora do intervalo 0-150 | critical | 0 | False |
| DQ007 | Internacoes sem CNES | high | 0 | False |
| DQ008 | Internacoes sem diagnostico principal | high | 0 | False |
| DQ009 | Internacoes com CNES sem correspondencia em hospital | high | 0 | False |
| DQ010 | Internacoes com municipio de residencia sem correspondencia | high | 1270397 | True |
| DQ011 | Diagnosticos principais sem correspondencia na tabela CID | high | 1044 | True |
| DQ012 | Procedimentos realizados sem descricao | high | 627 | True |
| DQ013 | Hospitais referenciados sem nome cadastrado | medium | 59346551 | False |
| DQ014 | Tabela sexo possui descricoes duplicadas | medium | 1 | False |
| DQ015 | VAL_TOT menor que a soma VAL_SH + VAL_SP + VAL_UTI | medium | 0 | False |
| DQ016 | municipios.SG_UF contem valores que nao sao UFs brasileiras | high | 18 | True |
| DQ017 | CO_MUNICIPIO_6D com formato diferente de seis digitos | high | 0 | False |
| DQ018 | CO_MUNICIPIO_7D nao nulo com formato diferente de sete digitos | medium | 0 | False |

## DQ001: Altas anteriores a internacao

- Severity: `critical`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Datas de saida anteriores a entrada quebram analises de permanencia e desfecho.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_SAIDA < DT_INTER
```

Sample SQL:

```sql
SELECT N_AIH, DT_INTER, DT_SAIDA, DIAS_PERM FROM internacoes WHERE DT_SAIDA < DT_INTER LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ002: DT_INTER fora do periodo 2007-2023

- Severity: `high`
- Affected rows: `27`
- Blocks ground truth: `True`

Why it matters: O calendario `tempo` cobre 2007-2023; registros fora desse intervalo podem indicar carga historica residual ou erro.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_INTER < DATE '2007-01-01' OR DT_INTER > DATE '2023-12-31'
```

Sample SQL:

```sql
SELECT N_AIH, DT_INTER, DT_SAIDA FROM internacoes WHERE DT_INTER < DATE '2007-01-01' OR DT_INTER > DATE '2023-12-31' ORDER BY DT_INTER LIMIT 10
```

Sample rows:

| N_AIH | DT_INTER | DT_SAIDA |
| --- | --- | --- |
| 2607104890841 | 2000-01-01 | 2008-07-31 |
| 4108100249957 | 2000-03-01 | 2008-03-25 |
| 4108104837177 | 2000-03-20 | 2008-05-30 |
| 3508111513797 | 2000-06-11 | 2008-07-25 |
| 3509113569401 | 2000-06-24 | 2009-08-22 |
| 5208102827290 | 2000-06-27 | 2008-08-31 |
| 3508110556566 | 2000-07-18 | 2008-08-06 |
| 3108102537716 | 2000-11-01 | 2008-11-30 |
| 2308101989523 | 2000-11-17 | 2009-03-31 |
| 2910100451126 | 2001-04-01 | 2010-04-03 |

## DQ003: DT_SAIDA fora do periodo 2007-2023

- Severity: `high`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Saidas fora do calendario esperado afetam series temporais por competencia/alta.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_SAIDA < DATE '2007-01-01' OR DT_SAIDA > DATE '2023-12-31'
```

Sample SQL:

```sql
SELECT N_AIH, DT_INTER, DT_SAIDA FROM internacoes WHERE DT_SAIDA < DATE '2007-01-01' OR DT_SAIDA > DATE '2023-12-31' ORDER BY DT_SAIDA LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ004: DIAS_PERM diferente da diferenca simples entre saida e entrada

- Severity: `medium`
- Affected rows: `172581441`
- Blocks ground truth: `False`

Why it matters: Pode ser regra de negocio inclusiva ou divergencia de calculo; deve ser documentado antes de usar como permanencia exata.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_INTER IS NOT NULL AND DT_SAIDA IS NOT NULL AND DIAS_PERM <> date_diff('day', DT_INTER, DT_SAIDA)
```

Sample SQL:

```sql
SELECT N_AIH, DT_INTER, DT_SAIDA, DIAS_PERM, date_diff('day', DT_INTER, DT_SAIDA) AS diff_dias FROM internacoes WHERE DT_INTER IS NOT NULL AND DT_SAIDA IS NOT NULL AND DIAS_PERM <> date_diff('day', DT_INTER, DT_SAIDA) LIMIT 10
```

Sample rows:

| N_AIH | DT_INTER | DT_SAIDA | DIAS_PERM | diff_dias |
| --- | --- | --- | --- | --- |
| 1222100640134 | 2022-12-30 | 2023-01-01 | 0 | 2 |
| 1222100530332 | 2022-11-04 | 2022-12-01 | 0 | 27 |
| 1223100031681 | 2023-02-03 | 2023-02-06 | 0 | 3 |
| 1222100689084 | 2022-11-21 | 2022-11-23 | 0 | 2 |
| 1223100033463 | 2023-01-16 | 2023-01-18 | 0 | 2 |
| 1223100032858 | 2023-02-07 | 2023-02-09 | 0 | 2 |
| 1223100033628 | 2023-02-08 | 2023-02-13 | 0 | 5 |
| 1222100655996 | 2023-01-19 | 2023-01-22 | 0 | 3 |
| 1223100064780 | 2023-02-22 | 2023-02-25 | 0 | 3 |
| 1223100065210 | 2023-02-22 | 2023-02-26 | 0 | 4 |

## DQ005: Valores financeiros negativos

- Severity: `critical`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Valores negativos em VAL_SH, VAL_SP, VAL_UTI ou VAL_TOT podem distorcer totais financeiros.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE VAL_SH < 0 OR VAL_SP < 0 OR VAL_UTI < 0 OR VAL_TOT < 0
```

Sample SQL:

```sql
SELECT N_AIH, VAL_SH, VAL_SP, VAL_UTI, VAL_TOT FROM internacoes WHERE VAL_SH < 0 OR VAL_SP < 0 OR VAL_UTI < 0 OR VAL_TOT < 0 LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ006: Idades fora do intervalo 0-150

- Severity: `critical`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Idades impossiveis invalidam analises demograficas e coortes.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE IDADE < 0 OR IDADE > 150
```

Sample SQL:

```sql
SELECT N_AIH, NASC, IDADE, DT_INTER FROM internacoes WHERE IDADE < 0 OR IDADE > 150 LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ007: Internacoes sem CNES

- Severity: `high`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: CNES ausente impede analise por estabelecimento hospitalar.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE CNES IS NULL
```
## DQ008: Internacoes sem diagnostico principal

- Severity: `high`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Diagnostico principal ausente limita analises clinicas por CID.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DIAG_PRINC IS NULL OR DIAG_PRINC = ''
```
## DQ009: Internacoes com CNES sem correspondencia em hospital

- Severity: `high`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Orfaos de CNES reduzem confianca em rankings e agregacoes por hospital.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES WHERE i.CNES IS NOT NULL AND h.CNES IS NULL
```

Sample SQL:

```sql
SELECT i.CNES, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES WHERE i.CNES IS NOT NULL AND h.CNES IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ010: Internacoes com municipio de residencia sem correspondencia

- Severity: `high`
- Affected rows: `1270397`
- Blocks ground truth: `True`

Why it matters: Municipios orfaos prejudicam analises territoriais.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes i LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D WHERE i.MUNIC_RES IS NOT NULL AND m.CO_MUNICIPIO_6D IS NULL
```

Sample SQL:

```sql
SELECT i.MUNIC_RES, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D WHERE i.MUNIC_RES IS NOT NULL AND m.CO_MUNICIPIO_6D IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10
```

Sample rows:

| MUNIC_RES | internacoes |
| --- | --- |
| 530040 | 255165 |
| 530180 | 136543 |
| 530120 | 127226 |
| 530140 | 111526 |
| 530060 | 100550 |
| 530170 | 95189 |
| 530110 | 84318 |
| 530150 | 81120 |
| 530130 | 59376 |
| 530070 | 56689 |

## DQ011: Diagnosticos principais sem correspondencia na tabela CID

- Severity: `high`
- Affected rows: `1044`
- Blocks ground truth: `True`

Why it matters: CIDs orfaos impedem interpretacao clinica por descricao, grupo e capitulo.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes i LEFT JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.DIAG_PRINC IS NOT NULL AND c.CID IS NULL
```

Sample SQL:

```sql
SELECT i.DIAG_PRINC, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.DIAG_PRINC IS NOT NULL AND c.CID IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10
```

Sample rows:

| DIAG_PRINC | internacoes |
| --- | --- |
| U04 | 727 |
| N185 | 101 |
| U109 | 75 |
| N184 | 38 |
| U10 | 26 |
| N182 | 20 |
| U099 | 18 |
| N183 | 15 |
| U09 | 15 |
| U89 | 6 |

## DQ012: Procedimentos realizados sem descricao

- Severity: `high`
- Affected rows: `627`
- Blocks ground truth: `True`

Why it matters: Procedimentos orfaos impedem interpretacao assistencial do codigo PROC_REA.

```sql
SELECT COUNT(*) AS affected_rows FROM internacao_procedimento ip LEFT JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA WHERE ip.PROC_REA IS NOT NULL AND p.PROC_REA IS NULL
```

Sample SQL:

```sql
SELECT ip.PROC_REA, COUNT(*) AS ocorrencias FROM internacao_procedimento ip LEFT JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA WHERE ip.PROC_REA IS NOT NULL AND p.PROC_REA IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10
```

Sample rows:

| PROC_REA | ocorrencias |
| --- | --- |
| 410010219 | 607 |
| 506020134 | 16 |
| 403070171 | 3 |
| 404020798 | 1 |

## DQ013: Hospitais referenciados sem nome cadastrado

- Severity: `medium`
- Affected rows: `59346551`
- Blocks ground truth: `False`

Why it matters: CNES com nome ausente dificulta comunicacao com gestores e auditoria nominal.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes i JOIN hospital h ON i.CNES = h.CNES WHERE h.NO_HOSPITAL IS NULL OR h.NO_HOSPITAL = ''
```

Sample SQL:

```sql
SELECT i.CNES, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES WHERE h.NO_HOSPITAL IS NULL OR h.NO_HOSPITAL = '' GROUP BY 1 ORDER BY 2 DESC LIMIT 10
```

Sample rows:

| CNES | internacoes |
| --- | --- |
| 2078015 | 761959 |
| 2237571 | 587240 |
| 2077396 | 582168 |
| 655 | 522136 |
| 2688689 | 467320 |
| 2079798 | 442815 |
| 9717 | 424481 |
| 2755130 | 385833 |
| 2077485 | 371173 |
| 2748223 | 359852 |

## DQ014: Tabela sexo possui descricoes duplicadas

- Severity: `medium`
- Affected rows: `1`
- Blocks ground truth: `False`

Why it matters: Codigos distintos com mesma descricao podem distorcer agrupamentos se o usuario agrupar por descricao sem entender os codigos.

```sql
SELECT COUNT(*) AS affected_rows FROM (SELECT DESCRICAO FROM sexo GROUP BY DESCRICAO HAVING COUNT(*) > 1) t
```

Sample SQL:

```sql
SELECT DESCRICAO, COUNT(*) AS codigos FROM sexo GROUP BY DESCRICAO HAVING COUNT(*) > 1
```

Sample rows:

| DESCRICAO | codigos |
| --- | --- |
| Feminino | 2 |

## DQ015: VAL_TOT menor que a soma VAL_SH + VAL_SP + VAL_UTI

- Severity: `medium`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Divergencia pode indicar que VAL_TOT nao e soma direta dos componentes ou que ha inconsistencia financeira.

```sql
SELECT COUNT(*) AS affected_rows FROM internacoes WHERE VAL_TOT + 0.01 < COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0)
```

Sample SQL:

```sql
SELECT N_AIH, VAL_SH, VAL_SP, VAL_UTI, VAL_TOT, COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0) AS soma_componentes FROM internacoes WHERE VAL_TOT + 0.01 < COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0) LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ016: municipios.SG_UF contem valores que nao sao UFs brasileiras

- Severity: `high`
- Affected rows: `18`
- Blocks ground truth: `True`

Why it matters: Valores numericos em SG_UF fazem perguntas sobre UFs retornarem 38 categorias em vez das 27 UFs validas.

```sql
WITH valid_uf(sg_uf) AS (VALUES ('AC'), ('AL'), ('AP'), ('AM'), ('BA'), ('CE'), ('DF'), ('ES'), ('GO'), ('MA'), ('MT'), ('MS'), ('MG'), ('PA'), ('PB'), ('PR'), ('PE'), ('PI'), ('RJ'), ('RN'), ('RS'), ('RO'), ('RR'), ('SC'), ('SP'), ('SE'), ('TO')) SELECT COUNT(*) AS affected_rows FROM municipios m LEFT JOIN valid_uf v ON m.SG_UF = v.sg_uf WHERE v.sg_uf IS NULL
```

Sample SQL:

```sql
WITH valid_uf(sg_uf) AS (VALUES ('AC'), ('AL'), ('AP'), ('AM'), ('BA'), ('CE'), ('DF'), ('ES'), ('GO'), ('MA'), ('MT'), ('MS'), ('MG'), ('PA'), ('PB'), ('PR'), ('PE'), ('PI'), ('RJ'), ('RN'), ('RS'), ('RO'), ('RR'), ('SC'), ('SP'), ('SE'), ('TO')) SELECT m.SG_UF, COUNT(*) AS municipios FROM municipios m LEFT JOIN valid_uf v ON m.SG_UF = v.sg_uf WHERE v.sg_uf IS NULL GROUP BY 1 ORDER BY 1
```

Sample rows:

| SG_UF | municipios |
| --- | --- |
| 13 | 3 |
| 14 | 1 |
| 20 | 1 |
| 21 | 2 |
| 25 | 4 |
| 29 | 1 |
| 33 | 1 |
| 42 | 1 |
| 43 | 2 |
| 51 | 1 |

## DQ017: CO_MUNICIPIO_6D com formato diferente de seis digitos

- Severity: `high`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Codigos municipais fora do formato esperado prejudicam joins territoriais e validacao IBGE/DATASUS.

```sql
SELECT COUNT(*) AS affected_rows FROM municipios WHERE NOT regexp_full_match(CAST(CO_MUNICIPIO_6D AS VARCHAR), '^[0-9]{6}$')
```

Sample SQL:

```sql
SELECT CO_MUNICIPIO_6D, NO_MUNICIPIO, SG_UF FROM municipios WHERE NOT regexp_full_match(CAST(CO_MUNICIPIO_6D AS VARCHAR), '^[0-9]{6}$') LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._

## DQ018: CO_MUNICIPIO_7D nao nulo com formato diferente de sete digitos

- Severity: `medium`
- Affected rows: `0`
- Blocks ground truth: `False`

Why it matters: Codigos municipais de sete digitos fora do formato esperado indicam problema cadastral ou campo com significado distinto.

```sql
SELECT COUNT(*) AS affected_rows FROM municipios WHERE CO_MUNICIPIO_7D IS NOT NULL AND NOT regexp_full_match(CAST(CO_MUNICIPIO_7D AS VARCHAR), '^[0-9]{7}$')
```

Sample SQL:

```sql
SELECT CO_MUNICIPIO_7D, NO_MUNICIPIO, SG_UF FROM municipios WHERE CO_MUNICIPIO_7D IS NOT NULL AND NOT regexp_full_match(CAST(CO_MUNICIPIO_7D AS VARCHAR), '^[0-9]{7}$') LIMIT 10
```

Sample rows:

_Nenhuma linha retornada._
