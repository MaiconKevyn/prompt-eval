# Stage 1 Ground Truth Questions

Accepted validated questions: `100`

## Difficulty Distribution

| difficulty | count |
| --- | --- |
| L1 | 15 |
| L2 | 25 |
| L3 | 25 |
| L4 | 20 |
| L5 | 15 |

## Questions

### SIHRD5_Q001 (L1)

- Persona: Analista DATASUS/SIH
- Question: Quantas internacoes existem na tabela principal?
- Intent: Medir o volume total de registros de internacao disponiveis.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q001.json`
- Rows returned: `1`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS total_internacoes FROM internacoes
```

### SIHRD5_Q002 (L1)

- Persona: Analista DATASUS/SIH
- Question: Quantos registros de procedimentos realizados existem?
- Intent: Medir o volume da tabela de procedimentos por internacao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q002.json`
- Rows returned: `1`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS total_procedimentos_realizados FROM internacao_procedimento
```

### SIHRD5_Q003 (L1)

- Persona: Analista DATASUS/SIH
- Question: Qual e o periodo minimo e maximo de entrada e saida das internacoes?
- Intent: Entender a cobertura temporal bruta da base.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q003.json`
- Rows returned: `1`
- Duration seconds: `0.091`
- Performance class: `fast`

```sql
SELECT MIN(DT_INTER) AS primeira_internacao, MAX(DT_INTER) AS ultima_internacao, MIN(DT_SAIDA) AS primeira_saida, MAX(DT_SAIDA) AS ultima_saida FROM internacoes
```

### SIHRD5_Q004 (L1)

- Persona: Coordenador hospitalar
- Question: Quantos hospitais existem no cadastro de estabelecimentos?
- Intent: Medir a cobertura cadastral de CNES/hospitais.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q004.json`
- Rows returned: `1`
- Duration seconds: `0.0`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS total_hospitais FROM hospital
```

### SIHRD5_Q005 (L1)

- Persona: Gestor municipal do SUS
- Question: Quantos municipios e quantas UFs aparecem na dimensao territorial?
- Intent: Medir a cobertura geografica da dimensao de municipios.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q005.json`
- Rows returned: `1`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS total_municipios, COUNT(DISTINCT SG_UF) AS total_ufs FROM municipios
```

### SIHRD5_Q006 (L1)

- Persona: Analista DATASUS/SIH
- Question: Quantos procedimentos distintos existem no cadastro de procedimentos?
- Intent: Medir a abrangencia do dicionario de procedimentos.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q006.json`
- Rows returned: `1`
- Duration seconds: `0.0`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS total_procedimentos_cadastrados FROM procedimentos
```

### SIHRD5_Q007 (L1)

- Persona: Pesquisador em saude publica
- Question: Quantos codigos CID existem na tabela de diagnosticos?
- Intent: Medir a abrangencia do dicionario de diagnosticos CID.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q007.json`
- Rows returned: `1`
- Duration seconds: `0.0`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS total_cids FROM cid
```

### SIHRD5_Q008 (L1)

- Persona: Pesquisador em saude publica
- Question: Qual e o intervalo de anos dos indicadores socioeconomicos?
- Intent: Entender cobertura temporal dos indicadores municipais auxiliares.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q008.json`
- Rows returned: `1`
- Duration seconds: `0.0`
- Performance class: `fast`

```sql
SELECT MIN(NU_ANO) AS primeiro_ano, MAX(NU_ANO) AS ultimo_ano, COUNT(*) AS registros FROM socioeconomico
```

### SIHRD5_Q009 (L1)

- Persona: Epidemiologista
- Question: Quantas internacoes tiveram morte registrada?
- Intent: Medir o volume bruto de obitos hospitalares marcados.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q009.json`
- Rows returned: `1`
- Duration seconds: `0.149`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS internacoes_com_morte FROM internacoes WHERE MORTE = TRUE
```

### SIHRD5_Q010 (L1)

- Persona: Planejador de rede assistencial
- Question: Quantas internacoes indicam uso de UTI pelo marcador de UTI?
- Intent: Medir volume bruto de uso de UTI.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q010.json`
- Rows returned: `1`
- Duration seconds: `0.114`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS internacoes_com_uti FROM internacoes WHERE MARCA_UTI <> 0 OR UTI_INT_TO > 0
```

### SIHRD5_Q011 (L1)

- Persona: Auditor de contas hospitalares
- Question: Qual e a menor e a maior idade registradas nas internacoes?
- Intent: Avaliar limites demograficos antes de analises por idade.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q011.json`
- Rows returned: `1`
- Duration seconds: `0.045`
- Performance class: `fast`

```sql
SELECT MIN(IDADE) AS idade_minima, MAX(IDADE) AS idade_maxima FROM internacoes
```

### SIHRD5_Q012 (L1)

- Persona: Analista financeiro da saude
- Question: Qual e o valor total aprovado registrado em VAL_TOT?
- Intent: Medir o total financeiro bruto da tabela principal.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q012.json`
- Rows returned: `1`
- Duration seconds: `0.886`
- Performance class: `fast`

```sql
SELECT ROUND(SUM(CAST(VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total FROM internacoes
```

### SIHRD5_Q013 (L1)

- Persona: Analista DATASUS/SIH
- Question: Quantos CNES distintos aparecem nas internacoes?
- Intent: Medir quantos estabelecimentos sao efetivamente usados nos fatos.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q013.json`
- Rows returned: `1`
- Duration seconds: `0.253`
- Performance class: `fast`

```sql
SELECT COUNT(DISTINCT CNES) AS cnes_distintos FROM internacoes
```

### SIHRD5_Q014 (L1)

- Persona: Analista DATASUS/SIH
- Question: Quantos municipios de residencia distintos aparecem nas internacoes?
- Intent: Medir cobertura territorial efetiva dos fatos.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q014.json`
- Rows returned: `1`
- Duration seconds: `0.231`
- Performance class: `fast`

```sql
SELECT COUNT(DISTINCT MUNIC_RES) AS municipios_residencia_distintos FROM internacoes
```

### SIHRD5_Q015 (L1)

- Persona: Analista DATASUS/SIH
- Question: Quantos dias existem na dimensao tempo?
- Intent: Medir cobertura do calendario analitico.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q015.json`
- Rows returned: `1`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS dias_calendario, MIN(data) AS data_inicial, MAX(data) AS data_final FROM tempo
```

### SIHRD5_Q016 (L2)

- Persona: Gestor estadual do SUS
- Question: Quantas internacoes ocorreram por ano de entrada?
- Intent: Acompanhar volume anual de internacoes.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q016.json`
- Rows returned: `23`
- Duration seconds: `0.184`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q017 (L2)

- Persona: Gestor estadual do SUS
- Question: Qual foi o valor total por ano de entrada?
- Intent: Acompanhar gasto/reembolso anual.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q017.json`
- Rows returned: `23`
- Duration seconds: `1.038`
- Performance class: `moderate`

```sql
SELECT year(DT_INTER) AS ano, ROUND(SUM(CAST(VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q018 (L2)

- Persona: Epidemiologista
- Question: Quantas mortes hospitalares foram registradas por ano?
- Intent: Acompanhar desfechos de obito ao longo do tempo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q018.json`
- Rows returned: `23`
- Duration seconds: `0.232`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, COUNT(*) FILTER (WHERE MORTE) AS mortes FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q019 (L2)

- Persona: Epidemiologista
- Question: Qual foi a taxa bruta de mortalidade hospitalar por ano?
- Intent: Comparar desfecho de morte usando internacoes como denominador.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q019.json`
- Rows returned: `23`
- Duration seconds: `0.264`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE MORTE) AS mortes, ROUND(100.0 * COUNT(*) FILTER (WHERE MORTE) / COUNT(*), 4) AS taxa_morte_pct FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q020 (L2)

- Persona: Analista financeiro da saude
- Question: Qual foi o valor medio por internacao em cada ano?
- Intent: Monitorar custo medio bruto anual.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q020.json`
- Rows returned: `23`
- Duration seconds: `1.061`
- Performance class: `moderate`

```sql
SELECT year(DT_INTER) AS ano, ROUND((SUM(CAST(VAL_TOT AS DECIMAL(20,2)))::DOUBLE / COUNT(VAL_TOT)), 2) AS valor_medio FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q021 (L2)

- Persona: Coordenador hospitalar
- Question: Quais CNES concentraram mais internacoes?
- Intent: Identificar estabelecimentos com maior volume usando codigo CNES.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q021.json`
- Rows returned: `20`
- Duration seconds: `0.284`
- Performance class: `fast`

```sql
SELECT CNES, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q022 (L2)

- Persona: Epidemiologista
- Question: Quais codigos de diagnostico principal foram mais frequentes?
- Intent: Identificar principais CIDs em volume bruto.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q022.json`
- Rows returned: `20`
- Duration seconds: `0.269`
- Performance class: `fast`

```sql
SELECT DIAG_PRINC, COUNT(*) AS internacoes FROM internacoes WHERE DIAG_PRINC IS NOT NULL GROUP BY 1 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q023 (L2)

- Persona: Tecnico de regulacao
- Question: Como as internacoes se distribuem por carater de internacao?
- Intent: Avaliar mix entre eletivo, urgencia e acidentes usando codigo bruto.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q023.json`
- Rows returned: `6`
- Duration seconds: `0.182`
- Performance class: `fast`

```sql
SELECT CAR_INT, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q024 (L2)

- Persona: Epidemiologista
- Question: Como as internacoes se distribuem por codigo de sexo?
- Intent: Avaliar distribuicao demografica basica por codigo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q024.json`
- Rows returned: `2`
- Duration seconds: `0.193`
- Performance class: `fast`

```sql
SELECT SEXO, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY SEXO
```

### SIHRD5_Q025 (L2)

- Persona: Epidemiologista
- Question: Como as internacoes se distribuem por codigo de raca/cor?
- Intent: Avaliar distribuicao demografica basica por raca/cor.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q025.json`
- Rows returned: `6`
- Duration seconds: `0.215`
- Performance class: `fast`

```sql
SELECT RACA_COR, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY RACA_COR
```

### SIHRD5_Q026 (L2)

- Persona: Epidemiologista
- Question: Qual e a distribuicao das internacoes por faixa etaria?
- Intent: Preparar analise populacional por grupos de idade.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q026.json`
- Rows returned: `6`
- Duration seconds: `1.278`
- Performance class: `moderate`

```sql
SELECT CASE WHEN IDADE < 1 THEN '00_<1' WHEN IDADE BETWEEN 1 AND 4 THEN '01_1_4' WHEN IDADE BETWEEN 5 AND 14 THEN '02_5_14' WHEN IDADE BETWEEN 15 AND 24 THEN '03_15_24' WHEN IDADE BETWEEN 25 AND 44 THEN '04_25_44' WHEN IDADE BETWEEN 45 AND 64 THEN '05_45_64' WHEN IDADE >= 65 THEN '06_65_plus' ELSE '99_ignorado' END AS faixa_etaria, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q027 (L2)

- Persona: Planejador de rede assistencial
- Question: Como as internacoes se distribuem por complexidade do atendimento?
- Intent: Avaliar mix de atencao basica, media e alta complexidade no codigo bruto.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q027.json`
- Rows returned: `3`
- Duration seconds: `1.063`
- Performance class: `moderate`

```sql
SELECT COMPLEX, COUNT(*) AS internacoes, ROUND(SUM(CAST(VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total FROM internacoes GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q028 (L2)

- Persona: Planejador de rede assistencial
- Question: Como as internacoes se distribuem pelo marcador de UTI?
- Intent: Entender uso de UTI por codigo bruto.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q028.json`
- Rows returned: `17`
- Duration seconds: `0.172`
- Performance class: `fast`

```sql
SELECT MARCA_UTI, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q029 (L2)

- Persona: Planejador de rede assistencial
- Question: Qual foi a media de dias de permanencia por ano?
- Intent: Acompanhar permanencia hospitalar media no tempo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q029.json`
- Rows returned: `23`
- Duration seconds: `0.375`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, ROUND((SUM(CAST(DIAS_PERM AS DECIMAL(20,2)))::DOUBLE / COUNT(DIAS_PERM)), 2) AS media_dias_permanencia FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q030 (L2)

- Persona: Planejador de rede assistencial
- Question: Qual e a distribuicao de permanencia em faixas de dias?
- Intent: Entender concentracao de internacoes curtas e longas.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q030.json`
- Rows returned: `4`
- Duration seconds: `0.067`
- Performance class: `fast`

```sql
SELECT CASE WHEN DIAS_PERM = 0 THEN '00_0' WHEN DIAS_PERM BETWEEN 1 AND 3 THEN '01_1_3' WHEN DIAS_PERM BETWEEN 4 AND 7 THEN '02_4_7' WHEN DIAS_PERM BETWEEN 8 AND 14 THEN '03_8_14' WHEN DIAS_PERM BETWEEN 15 AND 30 THEN '04_15_30' WHEN DIAS_PERM > 30 THEN '05_31_plus' ELSE '99_ignorado' END AS faixa_dias, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q031 (L2)

- Persona: Analista financeiro da saude
- Question: Qual foi o valor total por codigo de complexidade?
- Intent: Comparar volume financeiro por nivel de complexidade.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q031.json`
- Rows returned: `3`
- Duration seconds: `1.059`
- Performance class: `moderate`

```sql
SELECT COMPLEX, ROUND(SUM(CAST(VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY valor_total DESC
```

### SIHRD5_Q032 (L2)

- Persona: Epidemiologista
- Question: Quantas internacoes com gestacao de risco foram registradas por ano?
- Intent: Monitorar marcador de gestacao de risco no tempo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q032.json`
- Rows returned: `23`
- Duration seconds: `0.268`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, COUNT(*) FILTER (WHERE GESTRISCO) AS gestacao_risco FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q033 (L2)

- Persona: Planejador de rede assistencial
- Question: Quantos dias de UTI foram registrados por ano?
- Intent: Acompanhar intensidade anual de uso de UTI.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q033.json`
- Rows returned: `23`
- Duration seconds: `0.214`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, SUM(UTI_INT_TO) AS dias_uti FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q034 (L2)

- Persona: Gestor estadual do SUS
- Question: Quantas internacoes ocorreram por mes calendario?
- Intent: Avaliar sazonalidade mensal bruta.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q034.json`
- Rows returned: `225`
- Duration seconds: `0.233`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, month(DT_INTER) AS mes, COUNT(*) AS internacoes FROM internacoes GROUP BY 1, 2 ORDER BY 1, 2
```

### SIHRD5_Q035 (L2)

- Persona: Gestor estadual do SUS
- Question: Quantas saidas hospitalares ocorreram por ano?
- Intent: Comparar series por data de saida.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q035.json`
- Rows returned: `17`
- Duration seconds: `0.186`
- Performance class: `fast`

```sql
SELECT year(DT_SAIDA) AS ano_saida, COUNT(*) AS saidas FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q036 (L2)

- Persona: Analista DATASUS/SIH
- Question: Quais codigos PROC_REA aparecem mais na tabela de procedimentos realizados?
- Intent: Identificar procedimentos mais frequentes por codigo bruto.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q036.json`
- Rows returned: `20`
- Duration seconds: `0.277`
- Performance class: `fast`

```sql
SELECT PROC_REA, COUNT(*) AS ocorrencias FROM internacao_procedimento GROUP BY 1 ORDER BY ocorrencias DESC LIMIT 20
```

### SIHRD5_Q037 (L2)

- Persona: Gestor estadual do SUS
- Question: Qual e a populacao total registrada por ano nos indicadores socioeconomicos?
- Intent: Entender denominadores populacionais disponiveis.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q037.json`
- Rows returned: `13`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT NU_ANO AS ano, SUM(QT_POPULACAO) AS populacao_total FROM socioeconomico GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q038 (L2)

- Persona: Planejador de rede assistencial
- Question: Quantos leitos SUS estao registrados por ano nos indicadores socioeconomicos?
- Intent: Acompanhar capacidade assistencial agregada.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q038.json`
- Rows returned: `13`
- Duration seconds: `0.002`
- Performance class: `fast`

```sql
SELECT NU_ANO AS ano, SUM(QT_LEITOS_SUS) AS leitos_sus FROM socioeconomico GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q039 (L2)

- Persona: Gestor municipal do SUS
- Question: Quantos municipios existem por UF no cadastro territorial?
- Intent: Medir cobertura territorial por estado.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q039.json`
- Rows returned: `38`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT SG_UF, COUNT(*) AS municipios FROM municipios GROUP BY 1 ORDER BY municipios DESC, SG_UF
```

### SIHRD5_Q040 (L2)

- Persona: Coordenador hospitalar
- Question: Quantos hospitais existem por tipo de gestao cadastral?
- Intent: Entender distribuicao dos estabelecimentos por codigo de gestao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q040.json`
- Rows returned: `2`
- Duration seconds: `0.0`
- Performance class: `fast`

```sql
SELECT GESTAO, COUNT(*) AS hospitais FROM hospital GROUP BY 1 ORDER BY hospitais DESC
```

### SIHRD5_Q041 (L3)

- Persona: Gestor estadual do SUS
- Question: Quantas internacoes e qual valor total por UF de residencia?
- Intent: Comparar volume e valor financeiro por estado de residencia.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q041.json`
- Rows returned: `27`
- Duration seconds: `1.401`
- Performance class: `moderate`

```sql
SELECT m.SG_UF, COUNT(*) AS internacoes, ROUND(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q042 (L3)

- Persona: Gestor estadual do SUS
- Question: Quantas internacoes ocorreram por UF do hospital?
- Intent: Comparar producao assistencial por estado do estabelecimento.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q042.json`
- Rows returned: `27`
- Duration seconds: `0.768`
- Performance class: `fast`

```sql
SELECT mh.SG_UF, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q043 (L3)

- Persona: Epidemiologista
- Question: Como as internacoes se distribuem por sexo descrito?
- Intent: Usar a dimensao de sexo para resultado interpretavel.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q043.json`
- Rows returned: `2`
- Duration seconds: `0.271`
- Performance class: `fast`

```sql
SELECT s.DESCRICAO AS sexo, COUNT(*) AS internacoes FROM internacoes i JOIN sexo s ON i.SEXO = s.SEXO GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q044 (L3)

- Persona: Epidemiologista
- Question: Como as internacoes se distribuem por raca/cor descrita?
- Intent: Usar a dimensao de raca/cor para resultado interpretavel.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q044.json`
- Rows returned: `5`
- Duration seconds: `0.272`
- Performance class: `fast`

```sql
SELECT r.DESCRICAO AS raca_cor, COUNT(*) AS internacoes FROM internacoes i JOIN raca_cor r ON i.RACA_COR = r.RACA_COR GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q045 (L3)

- Persona: Tecnico de regulacao
- Question: Quantas internacoes ocorreram por descricao do carater de internacao?
- Intent: Interpretar eletivo, urgencia e acidentes com descricao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q045.json`
- Rows returned: `6`
- Duration seconds: `0.257`
- Performance class: `fast`

```sql
SELECT c.DESCRICAO AS carater_internacao, COUNT(*) AS internacoes FROM internacoes i JOIN car_int c ON i.CAR_INT = c.CAR_INT GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q046 (L3)

- Persona: Planejador de rede assistencial
- Question: Quais especialidades tiveram maior volume de internacoes?
- Intent: Identificar especialidades/leitos mais demandados.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q046.json`
- Rows returned: `15`
- Duration seconds: `0.286`
- Performance class: `fast`

```sql
SELECT e.DESCRICAO AS especialidade, COUNT(*) AS internacoes FROM internacoes i JOIN especialidade e ON i.ESPEC = e.ESPEC GROUP BY 1 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q047 (L3)

- Persona: Planejador de rede assistencial
- Question: Quantas internacoes existem por descricao de complexidade?
- Intent: Interpretar o mix de complexidade com descricao oficial da dimensao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q047.json`
- Rows returned: `2`
- Duration seconds: `1.828`
- Performance class: `moderate`

```sql
SELECT c.DESCRICAO AS complexidade, COUNT(*) AS internacoes, ROUND(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total FROM internacoes i JOIN complexidade c ON i.COMPLEX = c.COMPLEX GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q048 (L3)

- Persona: Planejador de rede assistencial
- Question: Quais tipos de UTI aparecem mais nas internacoes?
- Intent: Interpretar o marcador de UTI por descricao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q048.json`
- Rows returned: `17`
- Duration seconds: `0.284`
- Performance class: `fast`

```sql
SELECT mu.DESCRICAO AS marca_uti, COUNT(*) AS internacoes FROM internacoes i JOIN marca_uti mu ON i.MARCA_UTI = mu.MARCA_UTI GROUP BY 1 ORDER BY internacoes DESC
```

### SIHRD5_Q049 (L3)

- Persona: Analista DATASUS/SIH
- Question: Quais procedimentos realizados foram mais frequentes por descricao?
- Intent: Identificar procedimentos principais em linguagem de negocio.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q049.json`
- Rows returned: `20`
- Duration seconds: `1.313`
- Performance class: `moderate`

```sql
SELECT p.NOME_PROC, COUNT(*) AS ocorrencias FROM internacao_procedimento ip JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1 ORDER BY ocorrencias DESC LIMIT 20
```

### SIHRD5_Q050 (L3)

- Persona: Epidemiologista
- Question: Quais diagnosticos principais foram mais frequentes por descricao CID?
- Intent: Interpretar diagnosticos principais com descricao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q050.json`
- Rows returned: `20`
- Duration seconds: `1.88`
- Performance class: `moderate`

```sql
SELECT c.CID, c.DESCRICAO, COUNT(*) AS internacoes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q051 (L3)

- Persona: Epidemiologista
- Question: Quais capitulos CID concentraram mais internacoes?
- Intent: Analisar perfil clinico agregado por capitulo CID.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q051.json`
- Rows returned: `20`
- Duration seconds: `1.625`
- Performance class: `moderate`

```sql
SELECT c.DS_CAPITULO, COUNT(*) AS internacoes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID GROUP BY 1 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q052 (L3)

- Persona: Coordenador hospitalar
- Question: Quais hospitais tiveram maior volume de internacoes?
- Intent: Criar ranking nominal de hospitais por volume.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q052.json`
- Rows returned: `20`
- Duration seconds: `1.485`
- Performance class: `moderate`

```sql
SELECT i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q053 (L3)

- Persona: Gestor municipal do SUS
- Question: Quais municipios de residencia tiveram mais internacoes?
- Intent: Identificar municipios de maior demanda por residencia.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q053.json`
- Rows returned: `20`
- Duration seconds: `0.736`
- Performance class: `fast`

```sql
SELECT m.SG_UF, m.NO_MUNICIPIO, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q054 (L3)

- Persona: Gestor estadual do SUS
- Question: Quais regioes de saude tiveram mais internacoes por residencia?
- Intent: Apoiar planejamento regional de rede assistencial.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q054.json`
- Rows returned: `20`
- Duration seconds: `0.731`
- Performance class: `fast`

```sql
SELECT m.SG_UF, m.NO_REGIAO_SAUDE, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q055 (L3)

- Persona: Epidemiologista
- Question: Qual e a taxa de mortalidade hospitalar por UF de residencia?
- Intent: Comparar desfecho de morte usando UF de residencia.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q055.json`
- Rows returned: `27`
- Duration seconds: `0.558`
- Performance class: `fast`

```sql
SELECT m.SG_UF, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE i.MORTE) AS mortes, ROUND(100.0 * COUNT(*) FILTER (WHERE i.MORTE) / COUNT(*), 4) AS taxa_morte_pct FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY taxa_morte_pct DESC
```

### SIHRD5_Q056 (L3)

- Persona: Planejador de rede assistencial
- Question: Qual e a media de permanencia por UF de residencia?
- Intent: Comparar permanencia media entre estados.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q056.json`
- Rows returned: `27`
- Duration seconds: `0.629`
- Performance class: `fast`

```sql
SELECT m.SG_UF, ROUND((SUM(CAST(i.DIAS_PERM AS DECIMAL(20,2)))::DOUBLE / COUNT(i.DIAS_PERM)), 2) AS media_dias_permanencia, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY media_dias_permanencia DESC, SG_UF
```

### SIHRD5_Q057 (L3)

- Persona: Analista financeiro da saude
- Question: Qual e o valor medio por internacao em cada UF de residencia?
- Intent: Comparar custo medio bruto entre estados.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q057.json`
- Rows returned: `27`
- Duration seconds: `1.413`
- Performance class: `moderate`

```sql
SELECT m.SG_UF, ROUND((SUM(CAST(i.VAL_TOT AS DECIMAL(20,2)))::DOUBLE / COUNT(i.VAL_TOT)), 2) AS valor_medio, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY valor_medio DESC
```

### SIHRD5_Q058 (L3)

- Persona: Gestor estadual do SUS
- Question: Quais procedimentos por descricao tiveram maior valor total?
- Intent: Identificar procedimentos que mais concentram valor aprovado.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q058.json`
- Rows returned: `20`
- Duration seconds: `10.661`
- Performance class: `slow`

```sql
SELECT p.NOME_PROC, COUNT(*) AS ocorrencias, ROUND(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1 ORDER BY valor_total DESC LIMIT 20
```

### SIHRD5_Q059 (L3)

- Persona: Gestor estadual do SUS
- Question: Quais municipios dos hospitais tiveram mais internacoes?
- Intent: Analisar producao por municipio de atendimento.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q059.json`
- Rows returned: `20`
- Duration seconds: `1.771`
- Performance class: `moderate`

```sql
SELECT mh.SG_UF, mh.NO_MUNICIPIO, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q060 (L3)

- Persona: Coordenador hospitalar
- Question: Quais hospitais tiveram maior valor total registrado?
- Intent: Rankear estabelecimentos por valor aprovado.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q060.json`
- Rows returned: `20`
- Duration seconds: `3.095`
- Performance class: `moderate`

```sql
SELECT i.CNES, h.NO_HOSPITAL, ROUND(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES GROUP BY 1, 2 ORDER BY valor_total DESC LIMIT 20
```

### SIHRD5_Q061 (L3)

- Persona: Epidemiologista
- Question: Como as internacoes por sexo se distribuem em cada UF?
- Intent: Cruzar sexo e territorio para analise demografica regional.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q061.json`
- Rows returned: `54`
- Duration seconds: `1.311`
- Performance class: `moderate`

```sql
SELECT m.SG_UF, s.DESCRICAO AS sexo, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D JOIN sexo s ON i.SEXO = s.SEXO GROUP BY 1, 2 ORDER BY 1, internacoes DESC
```

### SIHRD5_Q062 (L3)

- Persona: Gestor estadual do SUS
- Question: Como a complexidade das internacoes se distribui em cada UF?
- Intent: Comparar mix assistencial por estado.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q062.json`
- Rows returned: `54`
- Duration seconds: `1.371`
- Performance class: `moderate`

```sql
SELECT m.SG_UF, c.DESCRICAO AS complexidade, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D JOIN complexidade c ON i.COMPLEX = c.COMPLEX GROUP BY 1, 2 ORDER BY 1, internacoes DESC
```

### SIHRD5_Q063 (L3)

- Persona: Epidemiologista
- Question: Quais grupos CID foram mais frequentes entre internacoes femininas?
- Intent: Analisar perfil clinico de internacoes femininas.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q063.json`
- Rows returned: `20`
- Duration seconds: `1.511`
- Performance class: `moderate`

```sql
SELECT c.DS_GRUPO, COUNT(*) AS internacoes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID JOIN sexo s ON i.SEXO = s.SEXO WHERE s.DESCRICAO = 'Feminino' GROUP BY 1 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q064 (L3)

- Persona: Pesquisador em saude publica
- Question: Qual e a populacao e o total de internacoes por UF e ano quando ha denominador socioeconomico?
- Intent: Conectar fatos assistenciais a denominadores populacionais agregados.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q064.json`
- Rows returned: `351`
- Duration seconds: `1.778`
- Performance class: `moderate`

```sql
SELECT m.SG_UF, se.NU_ANO AS ano, SUM(se.QT_POPULACAO) AS populacao, COUNT(i.N_AIH) AS internacoes FROM socioeconomico se JOIN municipios m ON se.CO_MUNICIPIO_6D = m.CO_MUNICIPIO_6D LEFT JOIN internacoes i ON i.MUNIC_RES = se.CO_MUNICIPIO_6D AND year(i.DT_INTER) = se.NU_ANO GROUP BY 1, 2 ORDER BY 1, 2
```

### SIHRD5_Q065 (L3)

- Persona: Gestor municipal do SUS
- Question: Quais municipios tiveram maior valor total por residencia?
- Intent: Identificar territorios de residencia com maior concentracao financeira.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q065.json`
- Rows returned: `20`
- Duration seconds: `1.711`
- Performance class: `moderate`

```sql
SELECT m.SG_UF, m.NO_MUNICIPIO, ROUND(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY valor_total DESC LIMIT 20
```

### SIHRD5_Q066 (L4)

- Persona: Gestor estadual do SUS
- Question: Qual foi a variacao ano contra ano no volume de internacoes?
- Intent: Medir crescimento ou queda anual em internacoes.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q066.json`
- Rows returned: `23`
- Duration seconds: `0.192`
- Performance class: `fast`

```sql
WITH anual AS (SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes GROUP BY 1) SELECT ano, internacoes, internacoes - LAG(internacoes) OVER (ORDER BY ano) AS diff_abs, ROUND(100.0 * (internacoes - LAG(internacoes) OVER (ORDER BY ano)) / NULLIF(LAG(internacoes) OVER (ORDER BY ano), 0), 4) AS diff_pct FROM anual ORDER BY ano
```

### SIHRD5_Q067 (L4)

- Persona: Analista financeiro da saude
- Question: Qual foi a variacao ano contra ano do valor total?
- Intent: Medir crescimento financeiro anual.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q067.json`
- Rows returned: `23`
- Duration seconds: `1.049`
- Performance class: `moderate`

```sql
WITH anual AS (SELECT year(DT_INTER) AS ano, SUM(CAST(VAL_TOT AS DECIMAL(20,2))) AS valor_total FROM internacoes GROUP BY 1) SELECT ano, ROUND(valor_total, 2) AS valor_total, ROUND(valor_total - LAG(valor_total) OVER (ORDER BY ano), 2) AS diff_abs, ROUND(100.0 * (valor_total - LAG(valor_total) OVER (ORDER BY ano)) / NULLIF(LAG(valor_total) OVER (ORDER BY ano), 0), 4) AS diff_pct FROM anual ORDER BY ano
```

### SIHRD5_Q068 (L4)

- Persona: Gestor estadual do SUS
- Question: Qual e a media movel de 3 meses das internacoes?
- Intent: Suavizar sazonalidade mensal para monitoramento.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q068.json`
- Rows returned: `225`
- Duration seconds: `1.437`
- Performance class: `moderate`

```sql
WITH mensal AS (SELECT date_trunc('month', DT_INTER) AS mes_ref, COUNT(*) AS internacoes FROM internacoes GROUP BY 1) SELECT mes_ref, internacoes, ROUND(AVG(internacoes) OVER (ORDER BY mes_ref ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS media_movel_3m FROM mensal ORDER BY mes_ref
```

### SIHRD5_Q069 (L4)

- Persona: Epidemiologista
- Question: Quais UFs tiveram maior taxa de mortalidade entre UFs com pelo menos 100 mil internacoes?
- Intent: Evitar rankings instaveis por baixo denominador.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q069.json`
- Rows returned: `27`
- Duration seconds: `0.653`
- Performance class: `fast`

```sql
WITH uf AS (SELECT m.SG_UF, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE i.MORTE) AS mortes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1) SELECT SG_UF, internacoes, mortes, ROUND(100.0 * mortes / internacoes, 4) AS taxa_morte_pct FROM uf WHERE internacoes >= 100000 ORDER BY taxa_morte_pct DESC
```

### SIHRD5_Q070 (L4)

- Persona: Analista financeiro da saude
- Question: Quais procedimentos tiveram maior valor medio por ocorrencia entre os com pelo menos 10 mil ocorrencias?
- Intent: Identificar procedimentos de alto custo medio com volume relevante.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q070.json`
- Rows returned: `20`
- Duration seconds: `9.592`
- Performance class: `slow`

```sql
WITH proc AS (SELECT p.NOME_PROC, COUNT(*) AS ocorrencias, (SUM(CAST(i.VAL_TOT AS DECIMAL(20,2)))::DOUBLE / COUNT(i.VAL_TOT)) AS valor_medio FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1) SELECT NOME_PROC, ocorrencias, ROUND(valor_medio, 2) AS valor_medio FROM proc WHERE ocorrencias >= 10000 ORDER BY valor_medio DESC LIMIT 20
```

### SIHRD5_Q071 (L4)

- Persona: Auditor de contas hospitalares
- Question: Quais hospitais estao acima do percentil 95 de volume de internacoes?
- Intent: Identificar estabelecimentos extremamente concentradores de volume.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q071.json`
- Rows returned: `344`
- Duration seconds: `1.864`
- Performance class: `moderate`

```sql
WITH hosp AS (SELECT i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES GROUP BY 1, 2), limiar AS (SELECT quantile_cont(internacoes, 0.95) AS p95 FROM hosp) SELECT hosp.CNES, hosp.NO_HOSPITAL, hosp.internacoes, limiar.p95 FROM hosp, limiar WHERE hosp.internacoes >= limiar.p95 ORDER BY hosp.internacoes DESC, hosp.CNES
```

### SIHRD5_Q072 (L4)

- Persona: Planejador de rede assistencial
- Question: Quais especialidades tiveram maior permanencia media entre as com pelo menos 100 mil internacoes?
- Intent: Comparar permanencia evitando especialidades raras.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q072.json`
- Rows returned: `12`
- Duration seconds: `0.65`
- Performance class: `fast`

```sql
WITH esp AS (SELECT e.DESCRICAO AS especialidade, COUNT(*) AS internacoes, (SUM(CAST(i.DIAS_PERM AS DECIMAL(20,2)))::DOUBLE / COUNT(i.DIAS_PERM)) AS media_dias FROM internacoes i JOIN especialidade e ON i.ESPEC = e.ESPEC GROUP BY 1) SELECT especialidade, internacoes, ROUND(media_dias, 2) AS media_dias FROM esp WHERE internacoes >= 100000 ORDER BY media_dias DESC, especialidade LIMIT 20
```

### SIHRD5_Q073 (L4)

- Persona: Epidemiologista
- Question: Qual proporcao das mortes vem de cada capitulo CID?
- Intent: Entender concentracao de obitos por grupo clinico amplo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q073.json`
- Rows returned: `22`
- Duration seconds: `0.684`
- Performance class: `fast`

```sql
WITH mortes AS (SELECT c.DS_CAPITULO, COUNT(*) AS mortes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.MORTE GROUP BY 1), total AS (SELECT SUM(mortes) AS total_mortes FROM mortes) SELECT DS_CAPITULO, mortes, ROUND(100.0 * mortes / total_mortes, 4) AS proporcao_mortes_pct FROM mortes, total ORDER BY mortes DESC
```

### SIHRD5_Q074 (L4)

- Persona: Planejador de rede assistencial
- Question: Quais foram os percentis de permanencia por ano?
- Intent: Entender distribuicao da permanencia alem da media.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q074.json`
- Rows returned: `23`
- Duration seconds: `2.699`
- Performance class: `moderate`

```sql
SELECT year(DT_INTER) AS ano, quantile_cont(DIAS_PERM, 0.5) AS p50_dias, quantile_cont(DIAS_PERM, 0.9) AS p90_dias, quantile_cont(DIAS_PERM, 0.99) AS p99_dias FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q075 (L4)

- Persona: Gestor estadual do SUS
- Question: Qual foi a taxa de internacoes por 1.000 habitantes por UF e ano?
- Intent: Usar denominador populacional para comparacao territorial.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q075.json`
- Rows returned: `351`
- Duration seconds: `0.957`
- Performance class: `fast`

```sql
WITH internacoes_uf AS (SELECT m.SG_UF, year(i.DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2), pop_uf AS (SELECT m.SG_UF, se.NU_ANO AS ano, SUM(se.QT_POPULACAO) AS populacao FROM socioeconomico se JOIN municipios m ON se.CO_MUNICIPIO_6D = m.CO_MUNICIPIO_6D GROUP BY 1, 2) SELECT p.SG_UF, p.ano, p.populacao, COALESCE(i.internacoes, 0) AS internacoes, ROUND(1000.0 * COALESCE(i.internacoes, 0) / NULLIF(p.populacao, 0), 4) AS internacoes_por_1000 FROM pop_uf p LEFT JOIN internacoes_uf i ON p.SG_UF = i.SG_UF AND p.ano = i.ano ORDER BY p.SG_UF, p.ano
```

### SIHRD5_Q076 (L4)

- Persona: Analista financeiro da saude
- Question: Qual foi o valor total por habitante por UF e ano?
- Intent: Comparar intensidade financeira com denominador populacional.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q076.json`
- Rows returned: `351`
- Duration seconds: `2.051`
- Performance class: `moderate`

```sql
WITH valor_uf AS (SELECT m.SG_UF, year(i.DT_INTER) AS ano, SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))) AS valor_total FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2), pop_uf AS (SELECT m.SG_UF, se.NU_ANO AS ano, SUM(se.QT_POPULACAO) AS populacao FROM socioeconomico se JOIN municipios m ON se.CO_MUNICIPIO_6D = m.CO_MUNICIPIO_6D GROUP BY 1, 2) SELECT p.SG_UF, p.ano, ROUND(COALESCE(v.valor_total, 0), 2) AS valor_total, p.populacao, ROUND(COALESCE(v.valor_total, 0) / NULLIF(p.populacao, 0), 4) AS valor_por_habitante FROM pop_uf p LEFT JOIN valor_uf v ON p.SG_UF = v.SG_UF AND p.ano = v.ano ORDER BY p.SG_UF, p.ano
```

### SIHRD5_Q077 (L4)

- Persona: Epidemiologista
- Question: Quais capitulos CID tiveram maior taxa de mortalidade com pelo menos 100 mil internacoes?
- Intent: Comparar risco de morte por capitulo com denominador minimo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q077.json`
- Rows returned: `20`
- Duration seconds: `1.701`
- Performance class: `moderate`

```sql
WITH cap AS (SELECT c.DS_CAPITULO, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE i.MORTE) AS mortes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID GROUP BY 1) SELECT DS_CAPITULO, internacoes, mortes, ROUND(100.0 * mortes / internacoes, 4) AS taxa_morte_pct FROM cap WHERE internacoes >= 100000 ORDER BY taxa_morte_pct DESC
```

### SIHRD5_Q078 (L4)

- Persona: Gestor estadual do SUS
- Question: Qual foi o procedimento mais frequente em cada UF de residencia?
- Intent: Identificar o procedimento dominante por estado.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q078.json`
- Rows returned: `27`
- Duration seconds: `10.273`
- Performance class: `slow`

```sql
WITH proc_uf AS (SELECT m.SG_UF, p.NOME_PROC, COUNT(*) AS ocorrencias, ROW_NUMBER() OVER (PARTITION BY m.SG_UF ORDER BY COUNT(*) DESC) AS rn FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1, 2) SELECT SG_UF, NOME_PROC, ocorrencias FROM proc_uf WHERE rn = 1 ORDER BY SG_UF
```

### SIHRD5_Q079 (L4)

- Persona: Gestor estadual do SUS
- Question: Qual hospital teve maior volume em cada UF do estabelecimento?
- Intent: Identificar lideres de producao por estado de atendimento.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q079.json`
- Rows returned: `27`
- Duration seconds: `1.781`
- Performance class: `moderate`

```sql
WITH hosp_uf AS (SELECT mh.SG_UF, i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes, ROW_NUMBER() OVER (PARTITION BY mh.SG_UF ORDER BY COUNT(*) DESC) AS rn FROM internacoes i JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1, 2, 3) SELECT SG_UF, CNES, NO_HOSPITAL, internacoes FROM hosp_uf WHERE rn = 1 ORDER BY SG_UF
```

### SIHRD5_Q080 (L4)

- Persona: Analista financeiro da saude
- Question: Como variou ano a ano o valor total por complexidade?
- Intent: Acompanhar crescimento financeiro por nivel de complexidade.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q080.json`
- Rows returned: `40`
- Duration seconds: `2.414`
- Performance class: `moderate`

```sql
WITH anual AS (SELECT c.DESCRICAO AS complexidade, year(i.DT_INTER) AS ano, SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))) AS valor_total FROM internacoes i JOIN complexidade c ON i.COMPLEX = c.COMPLEX GROUP BY 1, 2) SELECT complexidade, ano, ROUND(valor_total, 2) AS valor_total, ROUND(valor_total - LAG(valor_total) OVER (PARTITION BY complexidade ORDER BY ano), 2) AS diff_abs FROM anual ORDER BY complexidade, ano
```

### SIHRD5_Q081 (L4)

- Persona: Planejador de rede assistencial
- Question: Qual foi a taxa de uso de UTI por ano?
- Intent: Medir proporcao anual de internacoes com marcador de UTI.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q081.json`
- Rows returned: `23`
- Duration seconds: `0.343`
- Performance class: `fast`

```sql
SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE MARCA_UTI <> 0 OR UTI_INT_TO > 0) AS com_uti, ROUND(100.0 * COUNT(*) FILTER (WHERE MARCA_UTI <> 0 OR UTI_INT_TO > 0) / COUNT(*), 4) AS taxa_uti_pct FROM internacoes GROUP BY 1 ORDER BY 1
```

### SIHRD5_Q082 (L4)

- Persona: Tecnico de regulacao
- Question: Qual foi o mix percentual de carater de internacao por ano?
- Intent: Comparar eletivo/urgencia/acidentes no tempo.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q082.json`
- Rows returned: `111`
- Duration seconds: `0.519`
- Performance class: `fast`

```sql
WITH base AS (SELECT year(i.DT_INTER) AS ano, c.DESCRICAO AS carater, COUNT(*) AS internacoes FROM internacoes i JOIN car_int c ON i.CAR_INT = c.CAR_INT GROUP BY 1, 2), total AS (SELECT ano, SUM(internacoes) AS total_ano FROM base GROUP BY 1) SELECT b.ano, b.carater, b.internacoes, ROUND(100.0 * b.internacoes / t.total_ano, 4) AS percentual_ano FROM base b JOIN total t ON b.ano = t.ano ORDER BY b.ano, percentual_ano DESC
```

### SIHRD5_Q083 (L4)

- Persona: Epidemiologista
- Question: Como evoluiram as internacoes obstetricas por ano?
- Intent: Monitorar linhas de cuidado obstetricas pela especialidade.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q083.json`
- Rows returned: `17`
- Duration seconds: `0.12`
- Performance class: `fast`

```sql
SELECT year(i.DT_INTER) AS ano, e.DESCRICAO AS especialidade, COUNT(*) AS internacoes FROM internacoes i JOIN especialidade e ON i.ESPEC = e.ESPEC WHERE e.DESCRICAO ILIKE '%OBSTETRICIA%' GROUP BY 1, 2 ORDER BY 1, 2
```

### SIHRD5_Q084 (L4)

- Persona: Gestor estadual do SUS
- Question: Quantas internacoes ocorreram em UF de residencia diferente da UF do hospital?
- Intent: Medir deslocamento interestadual entre residencia e atendimento.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q084.json`
- Rows returned: `30`
- Duration seconds: `2.814`
- Performance class: `moderate`

```sql
WITH fluxo AS (SELECT mr.SG_UF AS uf_residencia, mh.SG_UF AS uf_hospital, COUNT(*) AS internacoes FROM internacoes i JOIN municipios mr ON i.MUNIC_RES = mr.CO_MUNICIPIO_6D JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1, 2) SELECT uf_residencia, uf_hospital, internacoes FROM fluxo WHERE uf_residencia <> uf_hospital ORDER BY internacoes DESC LIMIT 30
```

### SIHRD5_Q085 (L4)

- Persona: Analista DATASUS/SIH
- Question: Quais anos tem meses faltantes na serie de internacoes por entrada?
- Intent: Auditar completude mensal da serie temporal.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q085.json`
- Rows returned: `23`
- Duration seconds: `0.383`
- Performance class: `fast`

```sql
WITH meses AS (SELECT year(DT_INTER) AS ano, COUNT(DISTINCT month(DT_INTER)) AS meses_com_dados FROM internacoes GROUP BY 1) SELECT ano, meses_com_dados, 12 - meses_com_dados AS meses_faltantes FROM meses ORDER BY ano
```

### SIHRD5_Q086 (L5)

- Persona: Auditor de contas hospitalares
- Question: Existem internacoes com data de saida anterior a data de entrada?
- Intent: Detectar erro temporal critico.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q086.json`
- Rows returned: `1`
- Duration seconds: `0.113`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS registros_invalidos FROM internacoes WHERE DT_SAIDA < DT_INTER
```

### SIHRD5_Q087 (L5)

- Persona: Auditor de contas hospitalares
- Question: Quantas internacoes tem DIAS_PERM diferente da diferenca simples entre saida e entrada?
- Intent: Avaliar se DIAS_PERM pode ser usado como permanencia sem regra adicional.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q087.json`
- Rows returned: `1`
- Duration seconds: `0.358`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS divergencias FROM internacoes WHERE DT_INTER IS NOT NULL AND DT_SAIDA IS NOT NULL AND DIAS_PERM <> date_diff('day', DT_INTER, DT_SAIDA)
```

### SIHRD5_Q088 (L5)

- Persona: Auditor de contas hospitalares
- Question: Existem valores financeiros negativos nos campos de valor?
- Intent: Detectar problemas financeiros criticos.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q088.json`
- Rows returned: `1`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS registros_com_valor_negativo FROM internacoes WHERE VAL_SH < 0 OR VAL_SP < 0 OR VAL_UTI < 0 OR VAL_TOT < 0
```

### SIHRD5_Q089 (L5)

- Persona: Epidemiologista
- Question: Existem idades fora do intervalo aceito de 0 a 150 anos?
- Intent: Validar campo etario antes de analises demograficas.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q089.json`
- Rows returned: `1`
- Duration seconds: `0.0`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS idades_invalidas FROM internacoes WHERE IDADE < 0 OR IDADE > 150
```

### SIHRD5_Q090 (L5)

- Persona: Analista DATASUS/SIH
- Question: Quantos CNES das internacoes nao existem no cadastro hospitalar?
- Intent: Medir orfandade do relacionamento internacao-hospital.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q090.json`
- Rows returned: `1`
- Duration seconds: `0.537`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS internacoes_cnes_orfao FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES WHERE i.CNES IS NOT NULL AND h.CNES IS NULL
```

### SIHRD5_Q091 (L5)

- Persona: Gestor municipal do SUS
- Question: Quantas internacoes tem municipio de residencia sem cadastro territorial?
- Intent: Medir orfandade territorial.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q091.json`
- Rows returned: `1`
- Duration seconds: `0.476`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS internacoes_municipio_orfao FROM internacoes i LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D WHERE i.MUNIC_RES IS NOT NULL AND m.CO_MUNICIPIO_6D IS NULL
```

### SIHRD5_Q092 (L5)

- Persona: Epidemiologista
- Question: Quantos diagnosticos principais nao existem na tabela CID?
- Intent: Medir perda de interpretabilidade clinica.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q092.json`
- Rows returned: `1`
- Duration seconds: `0.861`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS diagnosticos_principais_orfaos FROM internacoes i LEFT JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.DIAG_PRINC IS NOT NULL AND c.CID IS NULL
```

### SIHRD5_Q093 (L5)

- Persona: Analista DATASUS/SIH
- Question: Quantos procedimentos realizados nao existem no cadastro de procedimentos?
- Intent: Medir orfandade de procedimentos.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q093.json`
- Rows returned: `1`
- Duration seconds: `0.801`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS procedimentos_orfaos FROM internacao_procedimento ip LEFT JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA WHERE ip.PROC_REA IS NOT NULL AND p.PROC_REA IS NULL
```

### SIHRD5_Q094 (L5)

- Persona: Epidemiologista
- Question: A dimensao sexo possui descricoes duplicadas entre codigos?
- Intent: Identificar risco de agrupamento errado por descricao.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q094.json`
- Rows returned: `1`
- Duration seconds: `0.001`
- Performance class: `fast`

```sql
SELECT DESCRICAO, COUNT(*) AS quantidade_codigos FROM sexo GROUP BY DESCRICAO HAVING COUNT(*) > 1
```

### SIHRD5_Q095 (L5)

- Persona: Analista financeiro da saude
- Question: Quantas internacoes tem VAL_TOT menor que VAL_SH + VAL_SP + VAL_UTI?
- Intent: Testar consistencia financeira entre total e componentes.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q095.json`
- Rows returned: `1`
- Duration seconds: `1.471`
- Performance class: `moderate`

```sql
SELECT COUNT(*) AS divergencias_financeiras FROM internacoes WHERE VAL_TOT + 0.01 < COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0)
```

### SIHRD5_Q096 (L5)

- Persona: Analista DATASUS/SIH
- Question: Quantas internacoes tem data de entrada fora da dimensao tempo?
- Intent: Verificar cobertura do calendario para DT_INTER.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q096.json`
- Rows returned: `1`
- Duration seconds: `0.543`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS dt_inter_sem_tempo FROM internacoes i LEFT JOIN tempo t ON i.DT_INTER = t.data WHERE i.DT_INTER IS NOT NULL AND t.data IS NULL
```

### SIHRD5_Q097 (L5)

- Persona: Analista DATASUS/SIH
- Question: Quantas internacoes tem data de saida fora da dimensao tempo?
- Intent: Verificar cobertura do calendario para DT_SAIDA.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q097.json`
- Rows returned: `1`
- Duration seconds: `0.53`
- Performance class: `fast`

```sql
SELECT COUNT(*) AS dt_saida_sem_tempo FROM internacoes i LEFT JOIN tempo t ON i.DT_SAIDA = t.data WHERE i.DT_SAIDA IS NOT NULL AND t.data IS NULL
```

### SIHRD5_Q098 (L5)

- Persona: Coordenador hospitalar
- Question: Quais CNES sem nome cadastrado concentram mais internacoes?
- Intent: Avaliar impacto pratico de hospitais sem nome.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q098.json`
- Rows returned: `20`
- Duration seconds: `0.399`
- Performance class: `fast`

```sql
SELECT i.CNES, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES WHERE h.NO_HOSPITAL IS NULL OR h.NO_HOSPITAL = '' GROUP BY 1 ORDER BY internacoes DESC LIMIT 20
```

### SIHRD5_Q099 (L5)

- Persona: Analista DATASUS/SIH
- Question: A tabela final de internacoes tem o mesmo volume da staging?
- Intent: Comparar carga final contra staging.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q099.json`
- Rows returned: `1`
- Duration seconds: `0.002`
- Performance class: `fast`

```sql
SELECT (SELECT COUNT(*) FROM stg_internacoes) AS stg_internacoes, (SELECT COUNT(*) FROM internacoes) AS internacoes, (SELECT COUNT(*) FROM stg_internacoes) - (SELECT COUNT(*) FROM internacoes) AS diferenca
```

### SIHRD5_Q100 (L5)

- Persona: Auditor de contas hospitalares
- Question: Quais anos tiveram volume extremamente baixo de internacoes e podem indicar cobertura parcial?
- Intent: Encontrar anos anomalo-baixos na serie.
- Evidence: `evaluation/ground_truth/query_results/SIHRD5_Q100.json`
- Rows returned: `0`
- Duration seconds: `0.186`
- Performance class: `fast`

```sql
WITH anual AS (SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes GROUP BY 1), stats AS (SELECT quantile_cont(internacoes, 0.25) AS q1, quantile_cont(internacoes, 0.75) AS q3 FROM anual) SELECT a.ano, a.internacoes, s.q1, s.q3, s.q1 - 1.5 * (s.q3 - s.q1) AS limite_inferior_iqr FROM anual a, stats s WHERE a.internacoes < s.q1 - 1.5 * (s.q3 - s.q1) ORDER BY a.ano
```
