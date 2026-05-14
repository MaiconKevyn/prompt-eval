# Revisao do `ground_truth_v2.json`

Gerado em: 2026-05-14

## Escopo

Arquivo revisado: `ground_truth_v2.json` na raiz do repositorio.

Banco executado: `sihrd5.duckdb`, aberto em modo read-only via DuckDB Python.

Documentacao usada como referencia:

- `docs/database_overview.md`
- `docs/schema_catalog.md`
- `docs/business_dictionary.md`
- `docs/relationship_map.md`
- `docs/data_quality_report.md`
- `docs/query_design_methodology.md`
- `docs/generated/join_policy.csv`
- `docs/generated/relationship_coverage.csv`

Observacao importante: este arquivo da raiz nao e o mesmo artefato que `evaluation/ground_truth/stage1_questions_v2.jsonl`. O pipeline documentado em `docs/query_design_methodology.md` aponta para 100 perguntas v2 validadas em `evaluation/ground_truth/`, enquanto o arquivo da raiz contem 132 itens com IDs `GT001` a `GT135`, faltando `GT016`, `GT020` e `GT045`.

## Metodologia

1. Li a documentacao de schema, dicionario de negocio, qualidade de dados e politica de joins.
2. Executei todas as 132 queries do `ground_truth_v2.json` contra `sihrd5.duckdb`.
3. Registrei sucesso ou erro de execucao, quantidade de linhas retornadas e amostras de resultados.
4. Comparei a semantica das queries com o contexto documentado: nomes reais de tabelas/colunas, granularidade de internacao/AIH, dimensoes, caveats de qualidade e politica de joins.

Comando equivalente usado para a execucao:

```bash
.venv/bin/python -u - <<'PY'
import json, duckdb
items = json.load(open("ground_truth_v2.json"))
con = duckdb.connect("sihrd5.duckdb", read_only=True)
for item in items:
    con.execute(item["query"]).fetchall()
PY
```

## Resultado executivo

O `ground_truth_v2.json` da raiz nao esta pronto para ser usado como ground truth do chatbot.

Resumo da execucao:

| classe | quantidade |
| --- | ---: |
| Total de perguntas | 132 |
| Executam no DuckDB | 76 |
| Falham no DuckDB | 56 |
| Executam sem ressalva imediata identificada | 46 |
| Executam, mas com ressalva semantica ou de qualidade | 30 |

As falhas nao sao pontuais. O arquivo mistura premissas de um schema antigo com o schema real atual:

- usa `atendimentos`, mas a tabela real de detalhe de procedimentos e `internacao_procedimento`;
- usa `municipios.codigo_6d`, `municipios.nome` e `municipios.estado`, mas o schema real usa `CO_MUNICIPIO_6D`, `NO_MUNICIPIO` e `SG_UF`;
- usa `cid.CD_DESCRICAO`, mas a coluna real e `cid.DESCRICAO`;
- assume `socioeconomico` no modelo longo `metrica`/`valor`, mas a tabela real e larga, com colunas como `QT_POPULACAO`, `VL_PIB_PERCAPITA`, `VL_MORT_INFANTIL`, `QT_LEITOS_SUS` e `QT_MEDICOS`;
- codifica significados errados para `ESPEC`, por exemplo `ESPEC = 2` como obstetricia, quando a dimensao mostra `2 = CARDIOLOGIA`.

## Evidencias de schema e contexto

Principais fatos usados na revisao:

| objeto | evidencia |
| --- | --- |
| `internacoes` | fato principal, 183.877.219 linhas; uma linha representa uma internacao/AIH, nao um paciente unico. |
| `internacao_procedimento` | tabela de detalhe/ponte entre `N_AIH` e `PROC_REA`; substitui a tabela inexistente `atendimentos`. |
| `municipios` | colunas reais: `CO_MUNICIPIO_6D`, `CO_MUNICIPIO_7D`, `NO_MUNICIPIO`, `SG_UF`, `NO_REGIAO_SAUDE`, `latitude`, `longitude`. |
| `cid` | colunas reais: `CID`, `DESCRICAO`, `TP_NIVEL`, `RESTRSEXO`, `DS_CATEGORIA`, `DS_GRUPO`, `DS_CAPITULO`. |
| `socioeconomico` | modelo largo por municipio/ano; nao possui `metrica`, `valor`, `bolsa_familia_total`, `idhm` ou `esgotamento_sanitario_domicilio`. |
| `especialidade` | `ESPEC = 1` e `BUCO MAXILO FACIAL`; `2` e `CARDIOLOGIA`; `5` e `GASTROENTEROLOGIA`; `10` e `OBSTETRICIA CIRURGICA`. |
| `sexo` | dimensao contem `1 = Masculino`, `2 = Feminino`, `3 = Feminino`; no fato executado apareceram registros em `1` e `3`. |
| `DIAS_PERM` | tem caveat forte: apenas 421 linhas possuem `DIAS_PERM > 0`; a media de `DIAS_PERM` executada foi `0,0000448669`, enquanto a media por diferenca de datas foi `5,109691` dias. |
| `MUNIC_RES -> municipios` | relacao classificada como `likely`; perde 1.270.397 internacoes em inner join e exige `LEFT JOIN` ou escopo explicito de registros mapeados. |
| `RACA_COR -> raca_cor` | relacao classificada como `rejected/audit_only`; inner join perde 48.760.813 internacoes. |
| `INSTRU -> instrucao` | relacao classificada como `rejected/audit_only`; inner join preserva apenas 1.757.501 de 183.877.219 internacoes. |

## Falhas de execucao

Foram 56 queries com erro de execucao. As categorias abaixo se sobrepoem em alguns itens, mas explicam a raiz tecnica.

### Colunas antigas de municipio/geografia

IDs afetados:

`GT006`, `GT018`, `GT019`, `GT028`, `GT031`, `GT032`, `GT038`, `GT049`, `GT051`, `GT072`, `GT073`, `GT074`, `GT075`, `GT076`, `GT077`, `GT080`, `GT083`, `GT086`, `GT087`, `GT088`, `GT093`, `GT102`, `GT103`, `GT112`, `GT113`, `GT120`, `GT121`, `GT123`, `GT124`, `GT128`, `GT130`, `GT132`, `GT134`, `GT135`.

Causa: usam `codigo_6d`, `nome` ou `estado`. No banco atual, usar `CO_MUNICIPIO_6D`, `NO_MUNICIPIO` e `SG_UF`.

Exemplo:

```sql
-- incorreto no schema atual
JOIN municipios mu ON i."MUNIC_RES" = mu.codigo_6d
WHERE mu.estado = 'RS'

-- forma alinhada ao schema
JOIN municipios mu ON i."MUNIC_RES" = mu.CO_MUNICIPIO_6D
WHERE mu.SG_UF = 'RS'
```

### Coluna antiga de CID

IDs afetados:

`GT014`, `GT015`, `GT035`, `GT039`, `GT048`, `GT069`, `GT070`, `GT078`, `GT082`, `GT090`, `GT092`, `GT116`, `GT127`, `GT129`.

Causa: usam `cid.CD_DESCRICAO`. No banco atual, a coluna e `cid.DESCRICAO`.

### Tabela inexistente `atendimentos`

IDs afetados:

`GT021`, `GT068`, `GT079`, `GT081`, `GT084`, `GT122`, `GT131`.

Causa: a tabela `atendimentos` nao existe. O modelo atual usa `internacao_procedimento` para relacionar internacoes a procedimentos.

### Modelo socioeconomico antigo ou fora de escopo

IDs afetados:

`GT040`, `GT073`, `GT074`, `GT123`, `GT135`.

Causa: estas queries assumem modelo `metrica`/`valor` ou indicadores nao presentes (`bolsa_familia_total`, `esgotamento_sanitario_domicilio`, `IDHM`). A tabela real tem indicadores fixos por coluna: populacao, PIB per capita, mortalidade infantil, leitos SUS e medicos.

## Queries que executam, mas nao devem ser aceitas sem correcao

### Especialidade (`ESPEC`) hard-coded com significado errado

| ID | problema |
| --- | --- |
| `GT010` | Pergunta casos obstetricos, mas usa `ESPEC = 2`; no schema atual `2 = CARDIOLOGIA`. |
| `GT027` | Pergunta obstetricia em UTI, mas usa `ESPEC = 2`; retorna cardiologia com `VAL_UTI > 0`. |
| `GT089` | Pergunta mortalidade obstetrica, mas usa `ESPEC = 2`; mede mortalidade em cardiologia. |
| `GT114` | Pergunta metodos contraceptivos em internacoes obstetricas, mas filtra `ESPEC = 2`; mede cardiologia. |
| `GT107` | Pergunta internacoes psiquiatricas, mas usa `ESPEC = 5`; no schema atual `5 = GASTROENTEROLOGIA`. |
| `GT117` | Pergunta internacoes cirurgicas, mas usa `ESPEC = 1`; no schema atual `1 = BUCO MAXILO FACIAL`. |

Evidencia executada:

| ESPEC | DESCRICAO | internacoes |
| ---: | --- | ---: |
| 1 | BUCO MAXILO FACIAL | 57.484.340 |
| 2 | CARDIOLOGIA | 34.051.416 |
| 5 | GASTROENTEROLOGIA | 2.847.736 |
| 10 | OBSTETRICIA CIRURGICA | 116.261 |

### UTI definida por valor financeiro

IDs afetados:

`GT007`, `GT023`, `GT027`, `GT041`, `GT088`, `GT117`, `GT118`, `GT125`, `GT128`, `GT133`.

Essas perguntas falam de internacao/uso de UTI, mas a query usa `VAL_UTI > 0`. Isso mede cobranca/valor de UTI, nao necessariamente o marcador assistencial de uso de UTI. Para perguntas de uso, a documentacao sugere explicitar o criterio e considerar `MARCA_UTI`.

Evidencia executada:

| criterio | total |
| --- | ---: |
| `VAL_UTI > 0` | 12.349.838 |
| `MARCA_UTI <> 0` | 12.254.045 |
| `UTI_INT_TO > 0` | 77 |

Esses numeros sao proximos entre `VAL_UTI` e `MARCA_UTI`, mas nao identicos. O ground truth precisa escolher uma definicao e escrever isso na pergunta.

### `DIAS_PERM` tem caveat forte

IDs que dependem de `DIAS_PERM`:

`GT017`, `GT034`, `GT058`, `GT063`, `GT077`, `GT091`, `GT101`, `GT134`.

O campo executa, mas a qualidade documentada impede tratar isso como permanencia media confiavel sem ressalva. Evidencia:

| metrica | valor |
| --- | ---: |
| `AVG(DIAS_PERM)` | 0,0000448669 |
| linhas com `DIAS_PERM > 0` | 421 |
| `AVG(date_diff('day', DT_INTER, DT_SAIDA))` | 5,109691 |
| linhas com divergencia `DIAS_PERM` vs diferenca simples de datas | 172.581.441 |

`GT091` e especialmente problematica: executa, mas retorna 0 linhas para uma pergunta que pede "os 5 hospitais".

### Inner joins rejeitados pela politica de joins

| ID | problema |
| --- | --- |
| `GT065` | Usa inner join `internacoes.INSTRU -> instrucao.INSTRU`, relacao `rejected/audit_only`; preserva apenas 1.757.501 de 183.877.219 internacoes. |
| `GT071` | Usa inner join `internacoes.RACA_COR -> raca_cor.RACA_COR`, relacao `rejected/audit_only`; perde 48.760.813 internacoes. |
| `GT108` | Mesmo problema de `RACA_COR`; pergunta nao declara escopo "apenas codigos mapeados". |

Para perguntas de negocio, estas queries devem usar `LEFT JOIN` com bucket sem correspondencia, ou a pergunta deve declarar explicitamente que considera apenas registros mapeados.

### Perguntas falam "pacientes", SQL conta internacoes

IDs afetados:

`GT011`, `GT012`, `GT013`, `GT033`, `GT037`, `GT042`, `GT044`, `GT062`, `GT065`, `GT070`, `GT076`, `GT078`, `GT082`, `GT109`, `GT114`, `GT119`, `GT131`.

O banco documentado nao tem identificador de paciente unico. A granularidade operacional e internacao/AIH. Essas perguntas devem ser reescritas para "internacoes de pacientes..." ou o SQL deve usar uma chave real de paciente, se ela existir em outra versao do modelo.

### Outros problemas pontuais

| ID | achado |
| --- | --- |
| `GT024` | Executa, mas retorna 5.654 linhas; nao e compacto para ground truth de avaliacao. |
| `GT030` | Usa `SEXO = 3` para mulheres. No fato atual isso retorna as internacoes femininas observadas, mas a dimensao possui `2` e `3` como `Feminino`; melhor juntar por descricao ou documentar o codigo usado. |
| `GT055` | Pergunta "registros de raca/cor cadastrados", mas conta linhas de internacao com `RACA_COR` nao nulo. Para categorias cadastradas, a query correta e sobre `raca_cor`. |
| `GT091` | Executa e retorna 0 linhas; nao atende uma pergunta top-5. |
| `GT133` | Pergunta anos 2008-2023, mas a SQL nao filtra esse intervalo e retorna 2007. |

## Itens que parecem aproveitaveis

Os seguintes IDs executaram e nao tiveram ressalva imediata identificada nesta revisao:

`GT001`, `GT002`, `GT003`, `GT004`, `GT005`, `GT008`, `GT009`, `GT022`, `GT025`, `GT026`, `GT029`, `GT036`, `GT043`, `GT046`, `GT047`, `GT050`, `GT052`, `GT053`, `GT054`, `GT056`, `GT057`, `GT059`, `GT060`, `GT061`, `GT064`, `GT066`, `GT067`, `GT085`, `GT094`, `GT095`, `GT096`, `GT097`, `GT098`, `GT099`, `GT100`, `GT104`, `GT105`, `GT106`, `GT110`, `GT111`, `GT115`, `GT126`.

Com ressalva leve de `DIAS_PERM`, tambem executam:

`GT034`, `GT058`, `GT063`, `GT101`.

Mesmo para estes itens, a recomendacao e padronizar metadados no formato usado pelo pipeline v2 oficial: dificuldade `L1`-`L5`, intencao de negocio, premissas, notas de qualidade e evidencia de execucao.

## Exemplos de resultados executados

| ID | pergunta | resultado observado |
| --- | --- | --- |
| `GT001` | Total de internacoes | `183.877.219` |
| `GT002` | Total de mortes | `7.907.788` |
| `GT003` | Procedimentos cadastrados | `5.394` |
| `GT004` | Codigos CID | `14.253` |
| `GT005` | Hospitais cadastrados | `6.873` |
| `GT007` | Registros de UTI via `VAL_UTI > 0` | `12.349.838`, mas a definicao de UTI esta ambigua. |
| `GT010` | Casos obstetricos | `34.051.416`, mas isso e cardiologia (`ESPEC = 2`), nao obstetricia. |
| `GT017` | Media de permanencia por `DIAS_PERM` | `0,0000448669` dias; resultado nao e confiavel como permanencia hospitalar media. |
| `GT024` | Hospitais com mais de 1000 internacoes | `5.654` linhas; resultado grande demais para evidencia compacta. |
| `GT091` | Top-5 hospitais por custo/dia | `0` linhas; nao responde ao formato pedido. |
| `GT133` | Mes com mais UTI por ano | retorna `2007`, embora a pergunta peca `2008-2023`. |

## Recomendacao

Nao usar o `ground_truth_v2.json` da raiz como fonte de avaliacao do chatbot no estado atual.

O caminho recomendado e:

1. Promover `evaluation/ground_truth/stage1_questions_v2.jsonl` como base canonica, porque ja segue a metodologia documentada e possui 100 perguntas com auditoria semantica.
2. Se for necessario manter um JSON na raiz, gerar esse JSON a partir do artefato canonico, nao manter uma lista paralela.
3. Corrigir ou remover as 56 queries que nao executam.
4. Reescrever as perguntas que contam internacoes como se fossem pacientes.
5. Substituir hard-codes de `ESPEC` por joins com `especialidade` ou filtros por descricao verificada.
6. Padronizar perguntas de UTI: separar "uso/marcador de UTI" de "valor/custo/cobranca de UTI".
7. Para `MUNIC_RES`, usar `LEFT JOIN` ou declarar "apenas municipios de residencia mapeados".
8. Para `RACA_COR`, `INSTRU`, `VINCPREV` e `CBOR`, tratar como auditoria ou declarar explicitamente a perda de cobertura.
9. Remover perguntas sobre Bolsa Familia, IDHM e esgotamento sanitario, a menos que novas fontes sejam adicionadas ao banco.
10. Executar novamente todas as queries e salvar evidencia por ID antes de usar o arquivo em avaliacao automatica.

## Veredito

O arquivo tem valor como rascunho de perguntas, mas nao como ground truth confiavel. A maioria das perguntas faz sentido para um chatbot SUS/DATASUS em abstrato, porem muitas nao fazem sentido para o schema atual ou usam premissas que contradizem a documentacao gerada em `docs`.

Para avaliacao do modelo, usar este arquivo hoje contaminaria as metricas: o chatbot poderia ser penalizado por gerar SQL correto no schema atual, enquanto o "ground truth" esperado usa tabelas/colunas antigas ou definicoes semanticas erradas.
