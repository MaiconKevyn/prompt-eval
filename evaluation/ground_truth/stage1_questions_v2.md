# Ground Truth V2

| id | difficulty | result_type | question |
| --- | --- | --- | --- |
| `SIHRD5_Q001` | `L1` | `scalar` | Quantas internacoes existem na tabela principal? |
| `SIHRD5_Q002` | `L1` | `scalar` | Quantos registros de procedimentos realizados existem? |
| `SIHRD5_Q003` | `L1` | `comparison` | Qual e o periodo minimo e maximo de entrada e saida das internacoes? |
| `SIHRD5_Q004` | `L1` | `scalar` | Quantos hospitais existem no cadastro de estabelecimentos? |
| `SIHRD5_Q005` | `L1` | `comparison` | Quantos municipios existem e quantas UFs brasileiras validas aparecem na dimensao territorial? |
| `SIHRD5_Q006` | `L1` | `scalar` | Quantos procedimentos distintos existem no cadastro de procedimentos? |
| `SIHRD5_Q007` | `L1` | `scalar` | Quantos codigos CID existem na tabela de diagnosticos? |
| `SIHRD5_Q008` | `L1` | `comparison` | Qual e o intervalo de anos dos indicadores socioeconomicos? |
| `SIHRD5_Q009` | `L1` | `scalar` | Quantas internacoes tiveram morte registrada? |
| `SIHRD5_Q010` | `L1` | `scalar` | Quantas internacoes indicam uso de UTI pelo marcador de UTI? |
| `SIHRD5_Q011` | `L1` | `comparison` | Qual e a menor e a maior idade registradas nas internacoes? |
| `SIHRD5_Q012` | `L1` | `scalar` | Qual e o valor total aprovado registrado em VAL_TOT? |
| `SIHRD5_Q013` | `L1` | `scalar` | Quantos CNES distintos aparecem nas internacoes? |
| `SIHRD5_Q014` | `L1` | `scalar` | Quantos municipios de residencia distintos aparecem nas internacoes? |
| `SIHRD5_Q015` | `L1` | `scalar` | Quantos dias existem na dimensao tempo? |
| `SIHRD5_Q016` | `L2` | `time_series` | Quantas internacoes ocorreram por ano de entrada? |
| `SIHRD5_Q017` | `L2` | `time_series` | Qual foi o valor total por ano de entrada? |
| `SIHRD5_Q018` | `L2` | `time_series` | Quantas mortes hospitalares foram registradas por ano? |
| `SIHRD5_Q019` | `L2` | `time_series` | Qual foi a taxa bruta de mortalidade hospitalar por ano? |
| `SIHRD5_Q020` | `L2` | `time_series` | Qual foi o valor medio por internacao em cada ano? |
| `SIHRD5_Q021` | `L2` | `ranking` | Quais CNES concentraram mais internacoes? |
| `SIHRD5_Q022` | `L2` | `ranking` | Quais codigos de diagnostico principal foram mais frequentes? |
| `SIHRD5_Q023` | `L2` | `distribution` | Como as internacoes se distribuem por carater de internacao? |
| `SIHRD5_Q024` | `L2` | `distribution` | Como as internacoes se distribuem por codigo de sexo? |
| `SIHRD5_Q025` | `L2` | `distribution` | Como as internacoes se distribuem por codigo de raca/cor? |
| `SIHRD5_Q026` | `L2` | `distribution` | Qual e a distribuicao das internacoes por faixa etaria? |
| `SIHRD5_Q027` | `L2` | `distribution` | Como as internacoes se distribuem por complexidade do atendimento? |
| `SIHRD5_Q028` | `L2` | `distribution` | Como as internacoes se distribuem pelo marcador de UTI? |
| `SIHRD5_Q029` | `L2` | `time_series` | Qual foi a media de dias de permanencia por ano segundo o campo DIAS_PERM? |
| `SIHRD5_Q030` | `L2` | `distribution` | Qual e a distribuicao de permanencia em faixas de dias segundo o campo DIAS_PERM? |
| `SIHRD5_Q031` | `L2` | `distribution` | Qual foi o valor total por codigo de complexidade? |
| `SIHRD5_Q032` | `L2` | `time_series` | Quantas internacoes com gestacao de risco foram registradas por ano? |
| `SIHRD5_Q033` | `L2` | `time_series` | Quantos dias de UTI foram registrados por ano? |
| `SIHRD5_Q034` | `L2` | `time_series` | Quantas internacoes ocorreram por mes calendario? |
| `SIHRD5_Q035` | `L2` | `time_series` | Quantas saidas hospitalares ocorreram por ano? |
| `SIHRD5_Q036` | `L2` | `ranking` | Quais codigos PROC_REA aparecem mais na tabela de procedimentos realizados? |
| `SIHRD5_Q037` | `L2` | `time_series` | Qual e a populacao total registrada por ano nos indicadores socioeconomicos? |
| `SIHRD5_Q038` | `L2` | `time_series` | Quantos leitos SUS estao registrados por ano nos indicadores socioeconomicos? |
| `SIHRD5_Q039` | `L2` | `distribution` | Quantos municipios existem por UF brasileira valida no cadastro territorial? |
| `SIHRD5_Q040` | `L2` | `distribution` | Quantos hospitais existem por tipo de gestao cadastral? |
| `SIHRD5_Q041` | `L3` | `distribution` | Quantas internacoes e qual valor total por UF de residencia? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q042` | `L3` | `distribution` | Quantas internacoes ocorreram por UF do hospital? |
| `SIHRD5_Q043` | `L3` | `distribution` | Como as internacoes se distribuem por sexo descrito? |
| `SIHRD5_Q044` | `L3` | `distribution` | Como as internacoes se distribuem por codigo de raca/cor, com descricao quando houver correspondencia na dimensao? |
| `SIHRD5_Q045` | `L3` | `distribution` | Quantas internacoes ocorreram por descricao do carater de internacao? |
| `SIHRD5_Q046` | `L3` | `ranking` | Quais especialidades tiveram maior volume de internacoes? |
| `SIHRD5_Q047` | `L3` | `distribution` | Quantas internacoes existem por descricao de complexidade? |
| `SIHRD5_Q048` | `L3` | `distribution` | Quais tipos de UTI aparecem mais nas internacoes? |
| `SIHRD5_Q049` | `L3` | `ranking` | Quais procedimentos realizados foram mais frequentes por descricao? |
| `SIHRD5_Q050` | `L3` | `ranking` | Quais diagnosticos principais foram mais frequentes por descricao CID? |
| `SIHRD5_Q051` | `L3` | `ranking` | Quais capitulos CID concentraram mais internacoes? |
| `SIHRD5_Q052` | `L3` | `ranking` | Quais hospitais tiveram maior volume de internacoes? |
| `SIHRD5_Q053` | `L3` | `ranking` | Quais municipios de residencia tiveram mais internacoes? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q054` | `L3` | `ranking` | Quais regioes de saude tiveram mais internacoes por residencia? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q055` | `L3` | `distribution` | Qual e a taxa de mortalidade hospitalar por UF de residencia? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q056` | `L3` | `distribution` | Qual e a media de permanencia por UF de residencia? (considerando apenas internacoes com municipio de residencia mapeado) segundo o campo DIAS_PERM |
| `SIHRD5_Q057` | `L3` | `distribution` | Qual e o valor medio por internacao em cada UF de residencia? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q058` | `L3` | `ranking` | Quais procedimentos por descricao tiveram maior valor total? |
| `SIHRD5_Q059` | `L3` | `ranking` | Quais municipios dos hospitais tiveram mais internacoes? |
| `SIHRD5_Q060` | `L3` | `ranking` | Quais hospitais tiveram maior valor total registrado? |
| `SIHRD5_Q061` | `L3` | `distribution` | Como as internacoes por sexo se distribuem em cada UF? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q062` | `L3` | `distribution` | Como a complexidade das internacoes se distribui em cada UF? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q063` | `L3` | `ranking` | Quais grupos CID foram mais frequentes entre internacoes femininas? |
| `SIHRD5_Q064` | `L3` | `time_series` | Qual e a populacao e o total de internacoes por UF e ano quando ha denominador socioeconomico? |
| `SIHRD5_Q065` | `L3` | `ranking` | Quais municipios tiveram maior valor total por residencia? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q066` | `L4` | `time_series` | Qual foi a variacao ano contra ano no volume de internacoes? |
| `SIHRD5_Q067` | `L4` | `time_series` | Qual foi a variacao ano contra ano do valor total? |
| `SIHRD5_Q068` | `L4` | `time_series` | Qual e a media movel de 3 meses das internacoes? |
| `SIHRD5_Q069` | `L4` | `ranking` | Quais UFs tiveram maior taxa de mortalidade entre UFs com pelo menos 100 mil internacoes? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q070` | `L4` | `ranking` | Quais procedimentos tiveram maior valor medio por ocorrencia entre os com pelo menos 10 mil ocorrencias? |
| `SIHRD5_Q071` | `L4` | `ranking` | Quais hospitais estao acima do percentil 95 de volume de internacoes? |
| `SIHRD5_Q072` | `L4` | `ranking` | Quais especialidades tiveram maior permanencia media entre as com pelo menos 100 mil internacoes segundo o campo DIAS_PERM? |
| `SIHRD5_Q073` | `L4` | `distribution` | Qual proporcao das mortes vem de cada capitulo CID? |
| `SIHRD5_Q074` | `L4` | `time_series` | Quais foram os percentis de permanencia por ano segundo o campo DIAS_PERM? |
| `SIHRD5_Q075` | `L4` | `time_series` | Qual foi a taxa de internacoes por 1.000 habitantes por UF e ano? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q076` | `L4` | `time_series` | Qual foi o valor total por habitante por UF e ano? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q077` | `L4` | `ranking` | Quais capitulos CID tiveram maior taxa de mortalidade com pelo menos 100 mil internacoes? |
| `SIHRD5_Q078` | `L4` | `ranking` | Qual foi o procedimento mais frequente em cada UF de residencia? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q079` | `L4` | `ranking` | Qual hospital teve maior volume em cada UF do estabelecimento? |
| `SIHRD5_Q080` | `L4` | `time_series` | Como variou ano a ano o valor total por complexidade? |
| `SIHRD5_Q081` | `L4` | `time_series` | Qual foi a taxa de uso de UTI por ano? |
| `SIHRD5_Q082` | `L4` | `time_series` | Qual foi o mix percentual de carater de internacao por ano? |
| `SIHRD5_Q083` | `L4` | `time_series` | Como evoluiram as internacoes obstetricas por ano? |
| `SIHRD5_Q084` | `L4` | `ranking` | Quantas internacoes ocorreram em UF de residencia diferente da UF do hospital? (considerando apenas internacoes com municipio de residencia mapeado) |
| `SIHRD5_Q085` | `L4` | `data_quality_finding` | Quais anos tem meses faltantes na serie de internacoes por entrada? |
| `SIHRD5_Q086` | `L5` | `data_quality_finding` | Existem internacoes com data de saida anterior a data de entrada? |
| `SIHRD5_Q087` | `L5` | `data_quality_finding` | Quantas internacoes tem DIAS_PERM diferente da diferenca simples entre saida e entrada? |
| `SIHRD5_Q088` | `L5` | `data_quality_finding` | Existem valores financeiros negativos nos campos de valor? |
| `SIHRD5_Q089` | `L5` | `data_quality_finding` | Existem idades fora do intervalo aceito de 0 a 150 anos? |
| `SIHRD5_Q090` | `L5` | `data_quality_finding` | Quantos CNES das internacoes nao existem no cadastro hospitalar? |
| `SIHRD5_Q091` | `L5` | `data_quality_finding` | Quantas internacoes tem municipio de residencia sem cadastro territorial? |
| `SIHRD5_Q092` | `L5` | `data_quality_finding` | Quantos diagnosticos principais nao existem na tabela CID? |
| `SIHRD5_Q093` | `L5` | `data_quality_finding` | Quantos procedimentos realizados nao existem no cadastro de procedimentos? |
| `SIHRD5_Q094` | `L5` | `data_quality_finding` | A dimensao sexo possui descricoes duplicadas entre codigos? |
| `SIHRD5_Q095` | `L5` | `data_quality_finding` | Quantas internacoes tem VAL_TOT menor que VAL_SH + VAL_SP + VAL_UTI? |
| `SIHRD5_Q096` | `L5` | `data_quality_finding` | Quantas internacoes tem data de entrada fora da dimensao tempo? |
| `SIHRD5_Q097` | `L5` | `data_quality_finding` | Quantas internacoes tem data de saida fora da dimensao tempo? |
| `SIHRD5_Q098` | `L5` | `data_quality_finding` | Quais CNES sem nome cadastrado concentram mais internacoes? |
| `SIHRD5_Q099` | `L5` | `data_quality_finding` | A tabela final de internacoes tem o mesmo volume da staging? |
| `SIHRD5_Q100` | `L5` | `data_quality_finding` | Quais anos tiveram volume extremamente baixo de internacoes e podem indicar cobertura parcial? |
