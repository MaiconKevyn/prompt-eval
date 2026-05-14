# Business Dictionary

Generated at: 2026-05-13T19:23:25

## Reading Rules

- **Observed:** supported by executed SQL and schema inspection.
- **Inferred:** likely from names/descriptions, not externally verified in this run.
- **Externally verified:** confirmed by an official external source. No SIH/DATASUS field definition was promoted to this status in this run because no official field dictionary was cited in the generated artifacts.
- **Unknown:** do not rely on without more evidence.

## Table Meanings

### car_int

**Inferred:** Carater da internacao: eletivo, urgencia e categorias de acidente/lesao.

### cbor

**Inferred:** Dicionario de ocupacao CBO-R.

### cid

**Inferred:** Dicionario de diagnosticos CID com descricao, categoria, grupo e capitulo. Usado para interpretar `DIAG_PRINC`, `DIAG_SECUN`, `CID_MORTE`, `CID_NOTIF` e diagnosticos secundarios.

### complexidade

**Inferred:** Nivel de complexidade: atencao basica, media complexidade e alta complexidade.

### contraceptivos

**Inferred:** Dicionario de metodos contraceptivos.

### especialidade

**Inferred:** Especialidade/leito/linha assistencial associada a internacao.

### etnia

**Inferred:** Dimensao de etnia.

### hospital

**Inferred:** Cadastro de estabelecimentos por CNES, com nome, municipio de movimento/atendimento e codigos administrativos.

### instrucao

**Inferred:** Dimensao de instrucao/escolaridade.

### internacao_procedimento

**Inferred:** Tabela de detalhe/ponte entre internacao (`N_AIH`) e procedimento realizado (`PROC_REA`). Permite analisar mix de procedimentos, mas pode multiplicar linhas ao juntar com `internacoes`.

### internacoes

**Inferred:** Fato principal. Uma linha parece representar uma internacao/AIH com datas, permanencia, hospital, diagnosticos, valores, demografia, municipio de residencia e marcadores assistenciais.

### marca_uti

**Inferred:** Marcador/tipo de UTI usado na internacao.

### municipios

**Inferred:** Dimensao territorial com codigos municipais de 6 e 7 digitos, UF, regiao de saude e coordenadas.

### nacionalidade

**Inferred:** Dimensao de nacionalidade.

### procedimentos

**Inferred:** Dicionario de procedimentos realizados. `PROC_REA` e o codigo e `NOME_PROC` e a descricao.

### raca_cor

**Inferred:** Dimensao de raca/cor.

### sexo

**Inferred:** Dimensao de sexo. Observacao importante: ha descricoes duplicadas para `Feminino`. A duplicidade de descricao citada e observada por SQL no data quality report.

### socioeconomico

**Inferred:** Indicadores municipais anuais: populacao, PIB per capita, obitos infantis, nascidos vivos, leitos SUS e medicos.

### stg_hospital

**Inferred:** Tabela staging do cadastro hospitalar.

### stg_internacoes

**Inferred:** Tabela staging da internacao; usada para conferir carga final.

### stg_sexo

**Inferred:** Tabela staging de sexo.

### tempo

**Inferred:** Calendario diario com ano, mes, trimestre e dia da semana.

### vincprev

**Inferred:** Dimensao de vinculo previdenciario.

## Key Business Fields

| field | evidence_status | business_meaning | evidence_basis |
| --- | --- | --- | --- |
| N_AIH | Observed + Inferred | Identificador da AIH/internacao. A unicidade e observada por PRIMARY KEY e candidate-key checks; o significado AIH/internacao ainda depende de dicionario oficial para ficar externamente verificado. | duckdb_constraints(), candidate_keys.csv, nomes de colunas/tabelas |
| CNES | Inferred | Codigo nacional do estabelecimento de saude; liga `internacoes` a `hospital` com cobertura observada, mas a definicao oficial do campo ainda precisa ser citada. | relationship_coverage.csv, nomes de colunas/tabelas |
| DT_INTER | Inferred | Data de entrada/internacao. | nome da coluna, perfil temporal e uso nos SQLs validados |
| DT_SAIDA | Inferred | Data de saida/alta. | nome da coluna, checks DQ001-DQ004 |
| DIAS_PERM | Observed + Inferred | Dias de permanencia. A relacao com `DT_SAIDA - DT_INTER` precisa de caveat porque DQ004 mostra divergencia massiva em relacao a diferenca simples de datas. | DQ004, perfil de coluna |
| VAL_SH | Inferred | Valor de servicos hospitalares. | nome da coluna e checks financeiros |
| VAL_SP | Inferred | Valor de servicos profissionais. | nome da coluna e checks financeiros |
| VAL_UTI | Inferred | Valor associado a UTI. | nome da coluna e checks financeiros |
| VAL_TOT | Observed + Inferred | Valor total registrado. Nao assumir soma direta de VAL_SH + VAL_SP + VAL_UTI sem verificar; DQ015 apenas confirma que nao ha casos em que VAL_TOT seja menor que a soma dos componentes testados. | DQ015, nome da coluna |
| MORTE | Inferred | Marcador booleano de morte/desfecho obito. Perguntas de mortalidade ainda precisam explicitar denominador e data de referencia. | tipo booleano, nomes de colunas e checks relacionados a CID_MORTE |
| MUNIC_RES | Observed + Inferred | Municipio de residencia do usuario. A cobertura contra `municipios` e incompleta; perguntas territoriais devem declarar se usam apenas municipios mapeados ou preservar bucket sem correspondencia. | relationship_coverage.csv, DQ010, join_policy.csv |
| PROC_REA | Observed + Inferred | Procedimento realizado. Pode aparecer no fato principal e na tabela de detalhe; joins com `internacao_procedimento` podem multiplicar internacoes. | relationship_coverage.csv, nomes de tabelas/colunas |
| DIAG_PRINC | Observed + Inferred | Diagnostico principal CID. A cobertura contra `cid` e quase completa, mas DQ011 registra diagnosticos sem correspondencia. | relationship_coverage.csv, DQ011 |

## External Dictionaries Still Needed Before Stage 2 Promotion

- Official SIH/SUS AIH layout and field dictionary for `internacoes` and `stg_internacoes`.
- Official SIGTAP/procedure dictionary validation for `PROC_REA` and `procedimentos`.
- Official CID version/source confirmation for `cid` and all diagnosis columns.
- Official CNES dictionary/source confirmation for `hospital` and establishment fields.
- Official IBGE/DATASUS municipality code source for `municipios`, including the invalid `SG_UF` values found in DQ016.
- Official definitions for demographic/social fields such as `RACA_COR`, `ETNIA`, `INSTRU`, `VINCPREV`, `CBOR`, `NACIONAL`, and `CONTRACEP*`.


## Important Business Caveats

- Joining `internacoes` to `internacao_procedimento` can multiply admissions because one admission can have more than one procedure.
- Analyses by hospital use CNES and may lose interpretability when `NO_HOSPITAL` is missing.
- Analyses by CID should prefer joins to `cid` and should document whether `DIAG_PRINC`, `DIAG_SECUN`, or another diagnosis field is being used.
- Analyses by geography must state whether they use residence municipality (`MUNIC_RES`) or hospital movement municipality (`hospital.MUNIC_MOV`).
- Analyses by value must state whether they use `VAL_TOT`, components, or derived averages.
