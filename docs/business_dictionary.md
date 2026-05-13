# Business Dictionary

Generated at: 2026-05-13T09:42:16

## Reading Rules

- **Observed:** supported by executed SQL and schema inspection.
- **Inferred:** likely from names/descriptions, not externally verified in this run.
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

| field | business_meaning |
| --- | --- |
| N_AIH | Identificador da AIH/internacao. Deve ser tratado como chave candidata somente apos validar unicidade. |
| CNES | Codigo nacional do estabelecimento de saude; liga `internacoes` a `hospital`. |
| DT_INTER | Data de entrada/internacao. |
| DT_SAIDA | Data de saida/alta. |
| DIAS_PERM | Dias de permanencia. A relacao com `DT_SAIDA - DT_INTER` precisa de caveat porque pode seguir regra inclusiva ou ter divergencias. |
| VAL_SH | Valor de servicos hospitalares. |
| VAL_SP | Valor de servicos profissionais. |
| VAL_UTI | Valor associado a UTI. |
| VAL_TOT | Valor total registrado. Nao assumir soma direta de VAL_SH + VAL_SP + VAL_UTI sem verificar. |
| MORTE | Marcador booleano de morte/desfecho obito. |
| MUNIC_RES | Municipio de residencia do usuario. |
| PROC_REA | Procedimento realizado. |
| DIAG_PRINC | Diagnostico principal CID. |

## Important Business Caveats

- Joining `internacoes` to `internacao_procedimento` can multiply admissions because one admission can have more than one procedure.
- Analyses by hospital use CNES and may lose interpretability when `NO_HOSPITAL` is missing.
- Analyses by CID should prefer joins to `cid` and should document whether `DIAG_PRINC`, `DIAG_SECUN`, or another diagnosis field is being used.
- Analyses by geography must state whether they use residence municipality (`MUNIC_RES`) or hospital movement municipality (`hospital.MUNIC_MOV`).
- Analyses by value must state whether they use `VAL_TOT`, components, or derived averages.
