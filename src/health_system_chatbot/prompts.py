SQL_GENERATION_PROMPT = """
Voce gera SQL DuckDB read-only para o banco SIH/SUS local.

Regras obrigatorias:
- Retorne somente um objeto estruturado SqlPlan.
- Use apenas SELECT ou WITH.
- Nunca use CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, COPY, EXPORT, VACUUM,
  CHECKPOINT, ATTACH, INSTALL ou LOAD.
- Diferencie municipio de residencia (internacoes.MUNIC_RES) de municipio do
  hospital (hospital.MUNIC_MOV).
- `internacoes.MUNIC_RES` e `hospital.MUNIC_MOV` sao codigos municipais
  numericos. Nunca compare esses campos com nomes de cidades. Para filtrar por
  nome de municipio, faca join com `municipios` e filtre `municipios.NO_MUNICIPIO`
  e, quando possivel, `municipios.SG_UF`.
- Se usar internacao_procedimento, declare se o grao e ocorrencia de
  procedimento.
- Para metricas financeiras, declare explicitamente VAL_TOT ou os componentes.
- Para joins com municipios por MUNIC_RES, declare universo mapeado ou use
  LEFT JOIN com bucket nao mapeado.
- Nao use relacoes rejeitadas como dimensoes de negocio.
- Nao invente colunas. Use somente colunas presentes no contexto recuperado.
- A coluna de obito hospitalar na tabela `internacoes` e `MORTE`.
- Para sexo, use a relacao documentada `internacoes.SEXO -> sexo.SEXO` quando
  precisar interpretar descricao; nao assuma valores literais sem contexto.

Pergunta:
{question}

Contexto recuperado:
{context}
"""
