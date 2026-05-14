# Schema Catalog

Generated at: 2026-05-13T19:23:25

## Tables

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
| main_dbt_test__audit | accepted_values_stg_internacoes_RACA_COR__0__1__2__3__4__5 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | accepted_values_stg_sexo_SEXO__0__1__3 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_1a18b2060f4c9f3544ea148aa02bd0ef | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_3102aa068aea89a943afb942e0556f12 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_3e54c8366885e58155d2f77835412cbe | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_6890d7ed6eb2ca06debd4047d5b3d939 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_777c86d82b14a00657691c6db817c463 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_86cab16768069715b1d6349bd3387189 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_92c019c1ee7790db14579fbb9093e5ec | BASE TABLE | dbt audit | 1 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_c2d40d6e54bd30fc3d6952faf9b46e1e | BASE TABLE | dbt audit | 366 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_c4b4734e30bb150d860146005c9ac02b | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_c6958574dbb3d45d1d2b833f5085e83d | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_cff276ae6c287df74a945008a6836741 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_d8dbd07a1add6fa4a10c4e2a59a5265a | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_e29b252a2897cb3cea258a2ea4e8cb7f | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_ed47cb877c740a6929e10d626e4263e4 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_rang_f23e37c5d4fdb7ffbad61bd94cc048cc | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_etnia_ETNIA__266__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_DIAS_PERM__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_IDADE__150__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_NUM_FILHOS__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_VAL_SH__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_VAL_SP__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_VAL_TOT__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_internacoes_VAL_UTI__0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_tempo_ano__2023__2007 | BASE TABLE | dbt audit | 366 |
| main_dbt_test__audit | dbt_utils_source_accepted_range_main_tempo_mes__12__1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | hospital_cnes_munic_mov | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | internacoes_contracep1_sexo | BASE TABLE | dbt audit | 83955 |
| main_dbt_test__audit | internacoes_diar_acom_dias_perm | BASE TABLE | dbt audit | 553 |
| main_dbt_test__audit | internacoes_dt_saida_dt_inter | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | internacoes_etnia_raca_cor | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | internacoes_gestrisco_sexo | BASE TABLE | dbt audit | 75730745 |
| main_dbt_test__audit | internacoes_idade | BASE TABLE | dbt audit | 15981798 |
| main_dbt_test__audit | internacoes_insc_pn_sexo | BASE TABLE | dbt audit | 3456 |
| main_dbt_test__audit | internacoes_morte_cid_morte | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | internacoes_morte_false_cid_morte | BASE TABLE | dbt audit | 928 |
| main_dbt_test__audit | internacoes_nasc_dt_inter | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | internacoes_raca_cor_etnia | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | internacoes_uti_int_to_marca_uti | BASE TABLE | dbt audit | 46 |
| main_dbt_test__audit | internacoes_val_uti_marca_uti | BASE TABLE | dbt audit | 95794 |
| main_dbt_test__audit | not_null_stg_sexo_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_hospital_754a726ab74be14d40cb0a09e04b4adf | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_2cbe6b3f20ef954f92638adc0d5722d4 | BASE TABLE | dbt audit | 182119635 |
| main_dbt_test__audit | relationships_stg_internacoes_58e51ce9b68822857f95bfdc62d16ef5 | BASE TABLE | dbt audit | 182732638 |
| main_dbt_test__audit | relationships_stg_internacoes_6774ac624f86bcbf606e9d38e92e3a71 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_9797541b51e3e77fbfaf1558436792d8 | BASE TABLE | dbt audit | 48760813 |
| main_dbt_test__audit | relationships_stg_internacoes_CID_MORTE__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_CID_NOTIF__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC1__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC2__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC3__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC4__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC5__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC6__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC7__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC8__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAGSEC9__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | relationships_stg_internacoes_DIAG_SECUN__CID__source_main_cid_ | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_cid_TP_NIVEL__CAT__SUBCAT | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_co_471c48ba2d676862c685ad110899f3c1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_co_fbdc93df62d4eb8921deb81c2d6e5b06 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_es_2a731c4d3897a6ae0db3b82980ccf379 | BASE TABLE | dbt audit | 33 |
| main_dbt_test__audit | source_accepted_values_main_in_11ad171b3535dd2529c0b671c4ad8f11 | BASE TABLE | dbt audit | 3 |
| main_dbt_test__audit | source_accepted_values_main_in_2d6a096fa84aa31a444ae08b50fe4c63 | BASE TABLE | dbt audit | 1 |
| main_dbt_test__audit | source_accepted_values_main_in_5b793e5d1d4e992d6117bd4a8e7664d8 | BASE TABLE | dbt audit | 1 |
| main_dbt_test__audit | source_accepted_values_main_in_ae8b94f76e4dddc1da5f96fdd84ed66e | BASE TABLE | dbt audit | 1 |
| main_dbt_test__audit | source_accepted_values_main_in_b5ffd551c812c717078223b9416c4bfa | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_instrucao_INSTRU__0__1__2__3__4__9 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_internacoes_GESTRISCO__0__1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_internacoes_IND_VDRL__0__1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_internacoes_MORTE__0__1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_internacoes_SEXO__1__2__3 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_ma_db39f4c3a7cbbe665734e2399082bae1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_mu_15630bdc87815a1cf3f85982670d4cf3 | BASE TABLE | dbt audit | 11 |
| main_dbt_test__audit | source_accepted_values_main_ra_3d04e48020300849b5b76e5242503dbc | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_sexo_SEXO__0__1__3 | BASE TABLE | dbt audit | 1 |
| main_dbt_test__audit | source_accepted_values_main_te_448012159218cefc26a5e0c42e98bf7b | BASE TABLE | dbt audit | 1 |
| main_dbt_test__audit | source_accepted_values_main_tempo_trimestre__1__2__3__4 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_accepted_values_main_vi_6f0b5d23ef30eb47c15e59b2cbaa6854 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_car_int_CAR_INT | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_car_int_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_cbor_CBOR | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_cbor_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_cid_CID | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_cid_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_cid_TP_NIVEL | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_complexidade_COMPLEX | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_complexidade_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_contraceptivos_CONTRACEPTIVO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_contraceptivos_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_especialidade_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_especialidade_ESPEC | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_etnia_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_etnia_ETNIA | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_hospital_CNES | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_hospital_MUNIC_MOV | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_instrucao_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_instrucao_INSTRU | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacao_procedimento_N_AIH | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacao_procedimento_PROC_REA | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacao_procedimento_id_atendimento | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_CAR_INT | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_CNES | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_COMPLEX | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_CONTRACEP1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_CONTRACEP2 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_DIAG_PRINC | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_DIAR_ACOM | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_DIAS_PERM | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_DT_INTER | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_DT_SAIDA | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_ESPEC | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_GESTRISCO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_IDADE | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_IND_VDRL | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_INSTRU | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_MARCA_UTI | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_MORTE | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_MUNIC_RES | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_NACIONAL | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_NUM_FILHOS | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_N_AIH | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_RACA_COR | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_SEXO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_UTI_INT_TO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_VAL_SH | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_VAL_SP | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_VAL_TOT | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_VAL_UTI | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_internacoes_VINCPREV | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_marca_uti_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_marca_uti_MARCA_UTI | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_municipios_CO_MUNICIPIO_6D | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_municipios_CO_MUNICIPIO_7D | BASE TABLE | dbt audit | 18 |
| main_dbt_test__audit | source_not_null_main_municipios_NO_MUNICIPIO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_municipios_SG_UF | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_nacionalidade_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_nacionalidade_NACIONAL | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_procedimentos_NOME_PROC | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_procedimentos_PROC_REA | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_raca_cor_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_raca_cor_RACA_COR | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_sexo_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_sexo_SEXO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_CO_MUNICIPIO_6D | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_NU_ANO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_QT_LEITOS_SUS | BASE TABLE | dbt audit | 26535 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_QT_MEDICOS | BASE TABLE | dbt audit | 685 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_QT_NASCIDOS_VIVOS | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_QT_OBITOS_INFANTIS | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_socioeconomico_QT_POPULACAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_tempo_ano | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_tempo_data | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_tempo_dia_semana | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_tempo_mes | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_tempo_trimestre | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_vincprev_DESCRICAO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_not_null_main_vincprev_VINCPREV | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_relationships_main_hosp_af9492e85d8ab80c0f30fec05b85012e | BASE TABLE | dbt audit | 22 |
| main_dbt_test__audit | source_relationships_main_inte_003bf65cd26dacabf3c106a55fe73dce | BASE TABLE | dbt audit | 2818 |
| main_dbt_test__audit | source_relationships_main_inte_01d6d98ba1ce6a1b15cd0aaa3ad2d03d | BASE TABLE | dbt audit | 114750667 |
| main_dbt_test__audit | source_relationships_main_inte_101823f556112fa23ddf3389526b63d1 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_relationships_main_inte_1d2f51b325a9ba82df75212c72cdb950 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_relationships_main_inte_1eca6ef348e13b408da8989c4cc97b5b | BASE TABLE | dbt audit | 183858355 |
| main_dbt_test__audit | source_relationships_main_inte_214665dc766c240f1798063cd2613723 | BASE TABLE | dbt audit | 116180756 |
| main_dbt_test__audit | source_relationships_main_inte_29256be1b4f85d65fc1280af0bb276b0 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_relationships_main_inte_2a1ac166274c275684c54257999133ce | BASE TABLE | dbt audit | 116710629 |
| main_dbt_test__audit | source_relationships_main_inte_3bf772a30f6ca9f86a5816c15d47d4c9 | BASE TABLE | dbt audit | 183502179 |
| main_dbt_test__audit | source_relationships_main_inte_4c19f1327477bcdde9cbf1b6f113a9dd | BASE TABLE | dbt audit | 117076265 |
| main_dbt_test__audit | source_relationships_main_inte_4feb2349c9aae6bc7827e77150823f16 | BASE TABLE | dbt audit | 117076265 |
| main_dbt_test__audit | source_relationships_main_inte_5ccb13b21da8915cf8a1a1707522d12c | BASE TABLE | dbt audit | 12 |
| main_dbt_test__audit | source_relationships_main_inte_7ac46c47dabb88d9c4185eeacdfc2769 | BASE TABLE | dbt audit | 173333293 |
| main_dbt_test__audit | source_relationships_main_inte_84fb54c151ea7aeb7967873423e83d08 | BASE TABLE | dbt audit | 181005234 |
| main_dbt_test__audit | source_relationships_main_inte_88bdc55ba5cf0dff52192c85210c70c1 | BASE TABLE | dbt audit | 34 |
| main_dbt_test__audit | source_relationships_main_inte_9a5ac789578c03d3878cf370cae2290c | BASE TABLE | dbt audit | 117058530 |
| main_dbt_test__audit | source_relationships_main_inte_a6ae8967bfcfd29d3c16da8e28a229c3 | BASE TABLE | dbt audit | 95448360 |
| main_dbt_test__audit | source_relationships_main_inte_aa57f2b929f7a5546015d28a82cbce59 | BASE TABLE | dbt audit | 182133421 |
| main_dbt_test__audit | source_relationships_main_inte_baa10a92a581828d095d0efdd752a8d8 | BASE TABLE | dbt audit | 182119718 |
| main_dbt_test__audit | source_relationships_main_inte_c4bd8260baa159b682c36cd225ce7c98 | BASE TABLE | dbt audit | 627 |
| main_dbt_test__audit | source_relationships_main_inte_c5ab0d270fe1518fa52bbf1bc63f5cd2 | BASE TABLE | dbt audit | 182732638 |
| main_dbt_test__audit | source_relationships_main_inte_ce103a8b59e28f4117f4f327c231800f | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_relationships_main_inte_ce48749eca09d747ff0cde52163216d2 | BASE TABLE | dbt audit | 116936986 |
| main_dbt_test__audit | source_relationships_main_inte_cf75d8c49752e7842e6dfa0cc07d59ec | BASE TABLE | dbt audit | 48760813 |
| main_dbt_test__audit | source_relationships_main_inte_d10d17c954eae75d0d71544e28f16249 | BASE TABLE | dbt audit | 117027259 |
| main_dbt_test__audit | source_relationships_main_inte_d36364804cdb6ec95ec38a629cc8c2c6 | BASE TABLE | dbt audit | 1270397 |
| main_dbt_test__audit | source_relationships_main_inte_d761c09c93c45b856a3f45046ff7eb34 | BASE TABLE | dbt audit | 182119635 |
| main_dbt_test__audit | source_relationships_main_inte_e24ecb984c6e2d587e01eadd9ab63b91 | BASE TABLE | dbt audit | 183858355 |
| main_dbt_test__audit | source_relationships_main_inte_ea730314920b831b4f6cac966a8cfb41 | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_relationships_main_inte_f24139773aa85d1a6a68992569ed12b6 | BASE TABLE | dbt audit | 1044 |
| main_dbt_test__audit | source_relationships_main_soci_79f2271162d3a7343632023bbd034bec | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_car_int_CAR_INT | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_cbor_CBOR | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_cid_CID | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_complexidade_COMPLEX | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_contraceptivos_CONTRACEPTIVO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_especialidade_ESPEC | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_etnia_ETNIA | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_hospital_CNES | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_instrucao_INSTRU | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_internacao_procedimento_id_atendimento | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_internacoes_N_AIH | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_marca_uti_MARCA_UTI | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_municipios_CO_MUNICIPIO_6D | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_municipios_CO_MUNICIPIO_7D | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_nacionalidade_NACIONAL | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_procedimentos_PROC_REA | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_raca_cor_RACA_COR | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_sexo_SEXO | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_tempo_data | BASE TABLE | dbt audit | 0 |
| main_dbt_test__audit | source_unique_main_vincprev_VINCPREV | BASE TABLE | dbt audit | 0 |

## Top Frequent Values For Selected Categorical Fields

These values are **observed** from executed `GROUP BY` queries and focus on important categorical/code fields used by the Stage 1 questions.

| table_name | column_name | business_meaning | rank | value | row_count | sql | duration_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| internacoes | CAR_INT | carater da internacao | 1 | 2 | 145586729 | SELECT "CAR_INT" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.216 |
| internacoes | CAR_INT | carater da internacao | 2 | 1 | 36515288 | SELECT "CAR_INT" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.216 |
| internacoes | CAR_INT | carater da internacao | 3 | 6 | 1138155 | SELECT "CAR_INT" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.216 |
| internacoes | CAR_INT | carater da internacao | 4 | 5 | 635768 | SELECT "CAR_INT" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.216 |
| internacoes | CAR_INT | carater da internacao | 5 | 3 | 1060 | SELECT "CAR_INT" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.216 |
| internacoes | CAR_INT | carater da internacao | 6 | 4 | 219 | SELECT "CAR_INT" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.216 |
| internacoes | ESPEC | especialidade | 1 | 3 | 66592564 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 2 | 1 | 57484340 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 3 | 2 | 34051416 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 4 | 7 | 19967078 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 5 | 5 | 2847736 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 6 | 9 | 1545414 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 7 | 4 | 339853 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 8 | 8 | 253952 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 9 | 14 | 235106 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | ESPEC | especialidade | 10 | 87 | 230078 | SELECT "ESPEC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | COMPLEX | complexidade | 1 | 02 | 171675245 | SELECT "COMPLEX" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.221 |
| internacoes | COMPLEX | complexidade | 2 | 03 | 12201962 | SELECT "COMPLEX" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.221 |
| internacoes | COMPLEX | complexidade | 3 | 00 | 12 | SELECT "COMPLEX" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.221 |
| internacoes | MARCA_UTI | marcador de UTI | 1 | 0 | 171623174 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.288 |
| internacoes | MARCA_UTI | marcador de UTI | 2 | 75 | 7273804 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 3 | 76 | 1503527 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 4 | 81 | 1231179 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 5 | 78 | 657578 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 6 | 51 | 477515 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 7 | 74 | 311251 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 8 | 79 | 252301 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 9 | 82 | 214056 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | MARCA_UTI | marcador de UTI | 10 | 85 | 149119 | SELECT "MARCA_UTI" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.289 |
| internacoes | SEXO | sexo | 1 | 3 | 107928385 | SELECT "SEXO" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.199 |
| internacoes | SEXO | sexo | 2 | 1 | 75948834 | SELECT "SEXO" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.199 |
| internacoes | RACA_COR | raca/cor | 1 | 3 | 65749749 | SELECT "RACA_COR" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | RACA_COR | raca/cor | 2 | 1 | 60081825 | SELECT "RACA_COR" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | RACA_COR | raca/cor | 3 | 99 | 48760813 | SELECT "RACA_COR" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.176 |
| internacoes | RACA_COR | raca/cor | 4 | 2 | 6541484 | SELECT "RACA_COR" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.177 |
| internacoes | RACA_COR | raca/cor | 5 | 4 | 2252044 | SELECT "RACA_COR" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.177 |
| internacoes | RACA_COR | raca/cor | 6 | 5 | 491304 | SELECT "RACA_COR" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.177 |
| internacoes | DIAG_PRINC | diagnostico principal | 1 | O800 | 12391391 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 2 | J189 | 4090969 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 3 | O809 | 3224114 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 4 | N390 | 2412074 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 5 | A09 | 2322889 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 6 | I64 | 2307576 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 7 | I500 | 1917483 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 8 | B342 | 1860545 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 9 | O821 | 1637991 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | DIAG_PRINC | diagnostico principal | 10 | O829 | 1630248 | SELECT "DIAG_PRINC" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.4 |
| internacoes | CNES | hospital | 1 | 2078015 | 761959 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 2 | 434 | 719254 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 3 | 27014 | 623140 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 4 | 2082187 | 592426 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 5 | 2237571 | 587240 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 6 | 2077396 | 582168 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 7 | 13846 | 569114 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 8 | 655 | 522136 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 9 | 2237601 | 521837 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | CNES | hospital | 10 | 2688689 | 467320 | SELECT "CNES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.409 |
| internacoes | MUNIC_RES | municipio de residencia | 1 | 355030 | 9179591 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 2 | 330455 | 3412931 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 3 | 292740 | 2249720 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 4 | 230440 | 2237047 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 5 | 310620 | 2148438 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 6 | 410690 | 1773231 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 7 | 130260 | 1691106 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 8 | 261160 | 1636126 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 9 | 431490 | 1581334 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacoes | MUNIC_RES | municipio de residencia | 10 | 520870 | 1285536 | SELECT "MUNIC_RES" AS value, COUNT(*) AS row_count FROM "internacoes" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.328 |
| internacao_procedimento | PROC_REA | procedimento realizado | 1 | 310010039 | 16435256 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 2 | 303140151 | 10576911 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 3 | 411010034 | 10309968 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 4 | 303010061 | 4507648 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 5 | 303170093 | 4214855 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 6 | 303140046 | 3735530 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 7 | 303010037 | 3723552 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 8 | 303060212 | 3636826 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 9 | 415010012 | 3353755 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| internacao_procedimento | PROC_REA | procedimento realizado | 10 | 303100044 | 3139159 | SELECT "PROC_REA" AS value, COUNT(*) AS row_count FROM "internacao_procedimento" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.358 |
| hospital | GESTAO | gestao hospitalar | 1 | 2 | 3891 | SELECT "GESTAO" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | GESTAO | gestao hospitalar | 2 | 1 | 2982 | SELECT "GESTAO" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 1 | 50 | 2130 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 2 | 61 | 1466 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 3 | 20 | 1150 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 4 | 00 | 904 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 5 | 40 | 658 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 6 | 60 | 402 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 7 | 22 | 99 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 8 | 30 | 62 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | NATUREZA | natureza hospitalar | 9 | 80 | 2 | SELECT "NATUREZA" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 1 | 355030 | 134 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 2 | 330455 | 110 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 3 | 230440 | 85 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 4 | 292740 | 81 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 5 | 520870 | 63 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 6 | 261160 | 55 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 7 | 410690 | 51 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 8 | 211130 | 46 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 9 | 270430 | 41 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| hospital | MUNIC_MOV | municipio do estabelecimento | 10 | 310620 | 41 | SELECT "MUNIC_MOV" AS value, COUNT(*) AS row_count FROM "hospital" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 1 | MG | 853 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 2 | SP | 645 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 3 | RS | 497 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 4 | BA | 417 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 5 | PR | 399 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 6 | SC | 295 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 7 | GO | 246 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 8 | PI | 224 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 9 | PB | 223 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| municipios | SG_UF | UF | 10 | MA | 217 | SELECT "SG_UF" AS value, COUNT(*) AS row_count FROM "municipios" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 1 | 2012 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 2 | 2013 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 3 | 2014 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 4 | 2015 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 5 | 2016 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 6 | 2017 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 7 | 2018 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 8 | 2019 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 9 | 2020 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |
| socioeconomico | NU_ANO | ano socioeconomico | 10 | 2021 | 5570 | SELECT "NU_ANO" AS value, COUNT(*) AS row_count FROM "socioeconomico" GROUP BY 1 ORDER BY row_count DESC, value LIMIT 10 | 0.001 |

## Main Schema Columns


### car_int


Rows: `6`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | car_int | 1 | CAR_INT | TINYINT | NO |
| main | car_int | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAR_INT | TINYINT | 0.0 | exact | 6 |  | 6 | True | 1 | 6 |
| DESCRICAO | VARCHAR | 0.0 | exact | 6 |  | 6 | True | Acidente no local trabalho ou a serv da empresa | Urgência |

### cbor


Rows: `2,812`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | cbor | 1 | CBOR | VARCHAR | NO |
| main | cbor | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CBOR | VARCHAR | 0.0 | exact | 2812 |  | 2812 | True | 010105 | 992225 |
| DESCRICAO | VARCHAR | 0.0 | exact | 2738 |  | 2738 | True | Abatedor | Zootecnista |

### cid


Rows: `14,253`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | cid | 1 | CID | VARCHAR | NO |
| main | cid | 2 | DESCRICAO | VARCHAR | YES |
| main | cid | 3 | TP_NIVEL | VARCHAR | YES |
| main | cid | 4 | RESTRSEXO | VARCHAR | YES |
| main | cid | 5 | DS_CATEGORIA | VARCHAR | YES |
| main | cid | 6 | DS_GRUPO | VARCHAR | YES |
| main | cid | 7 | DS_CAPITULO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CID | VARCHAR | 0.0 | exact | 14253 |  | 14253 | True | A00 | Z999 |
| DESCRICAO | VARCHAR | 0.0 | exact | 10856 |  | 10856 | True | 2-propanol | Zona cloacogenica |
| TP_NIVEL | VARCHAR | 0.0 | exact | 2 |  | 2 | True | CAT | SUBCAT |
| RESTRSEXO | VARCHAR | 0.0 | exact | 3 |  | 3 | True | 1 | 5 |
| DS_CATEGORIA | VARCHAR | 0.001263 | exact | 2039 |  | 2039 | True | Abortamento habitual | Zigomicose |
| DS_GRUPO | VARCHAR | 0.0 | exact | 226 |  | 226 | True | A00-A09 Doenças infecciosas intestinais | Z80-Z99 Pessoas com riscos relacionados com história pessoal e familiar |
| DS_CAPITULO | VARCHAR | 0.0 | exact | 22 |  | 22 | True | I. Algumas doenças infecciosas e parasitárias | XXII. Códigos para propósitos especiais |

### complexidade


Rows: `3`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | complexidade | 1 | COMPLEX | VARCHAR | NO |
| main | complexidade | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COMPLEX | VARCHAR | 0.0 | exact | 3 |  | 3 | True | 01 | 03 |
| DESCRICAO | VARCHAR | 0.0 | exact | 3 |  | 3 | True | Alta complexidade | Média complexidade |

### contraceptivos


Rows: `12`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | contraceptivos | 1 | CONTRACEPTIVO | TINYINT | NO |
| main | contraceptivos | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CONTRACEPTIVO | TINYINT | 0.0 | exact | 12 |  | 12 | True | 1 | 12 |
| DESCRICAO | VARCHAR | 0.0 | exact | 12 |  | 12 | True | Billings | Temperatura basal |

### especialidade


Rows: `70`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | especialidade | 1 | ESPEC | TINYINT | NO |
| main | especialidade | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESPEC | TINYINT | 0.0 | exact | 70 |  | 70 | True | 1 | 95 |
| DESCRICAO | VARCHAR | 0.0 | exact | 63 |  | 63 | True | ACOLHIMENTO NOTURNO | UTI PEDIATRICA - TIPO III |

### etnia


Rows: `264`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | etnia | 1 | ETNIA | SMALLINT | NO |
| main | etnia | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ETNIA | SMALLINT | 0.0 | exact | 264 |  | 264 | True | 1 | 264 |
| DESCRICAO | VARCHAR | 0.0 | exact | 264 |  | 264 | True | ACONA (WAKONAS, NACONAS, JAKONA, ACORA­NES) | ZURUAHA (SOROWAHA, SURUWAHA) |

### hospital


Rows: `6,873`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | hospital | 1 | CNES | INTEGER | NO |
| main | hospital | 2 | NO_HOSPITAL | VARCHAR | YES |
| main | hospital | 3 | MUNIC_MOV | INTEGER | YES |
| main | hospital | 4 | NATUREZA | VARCHAR | YES |
| main | hospital | 5 | GESTAO | VARCHAR | YES |
| main | hospital | 6 | NAT_JUR | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CNES | INTEGER | 0.0 | exact | 6873 |  | 6873 | True | 27 | 9997784 |
| NO_HOSPITAL | VARCHAR | 0.457733 | exact | 3196 |  | 3196 | True | ABIMED SERVICOS MEDICOS LTDA | Y A PENHA E CIA LTDA |
| MUNIC_MOV | INTEGER | 0.0 | exact | 3618 |  | 3618 | True | 110001 | 530180 |
| NATUREZA | VARCHAR | 0.0 | exact | 9 |  | 9 | True | 00 | 80 |
| GESTAO | VARCHAR | 0.0 | exact | 2 |  | 2 | True | 1 | 2 |
| NAT_JUR | VARCHAR | 0.811145 | exact | 25 |  | 25 | True |  | 3999 |

### instrucao


Rows: `4`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | instrucao | 1 | INSTRU | TINYINT | NO |
| main | instrucao | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INSTRU | TINYINT | 0.0 | exact | 4 |  | 4 | True | 1 | 4 |
| DESCRICAO | VARCHAR | 0.0 | exact | 4 |  | 4 | True | 1º grau | Analfabeto |

### internacao_procedimento


Rows: `187,957,888`. Classification: `fato/staging`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | internacao_procedimento | 1 | id_atendimento | UBIGINT | NO |
| main | internacao_procedimento | 2 | N_AIH | BIGINT | YES |
| main | internacao_procedimento | 3 | PROC_REA | BIGINT | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| id_atendimento | UBIGINT | 0.0 | exact | 187957888 |  | 187957888 | True | 0 | 187957887 |
| N_AIH | BIGINT | 0.0 | exact | 183877219 |  | 183877219 | True | 1107100903524 | 9923300006499 |
| PROC_REA | BIGINT | 0.0 | exact | 1930 |  | 1930 | True | 201010038 | 506020134 |

### internacoes


Rows: `183,877,219`. Classification: `fato/staging`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | internacoes | 1 | N_AIH | BIGINT | NO |
| main | internacoes | 2 | CNES | INTEGER | YES |
| main | internacoes | 3 | DT_INTER | DATE | YES |
| main | internacoes | 4 | DT_SAIDA | DATE | YES |
| main | internacoes | 5 | DIAS_PERM | SMALLINT | YES |
| main | internacoes | 6 | DIAR_ACOM | SMALLINT | YES |
| main | internacoes | 7 | CAR_INT | TINYINT | YES |
| main | internacoes | 8 | ESPEC | TINYINT | YES |
| main | internacoes | 9 | COMPLEX | VARCHAR | YES |
| main | internacoes | 10 | MARCA_UTI | TINYINT | YES |
| main | internacoes | 11 | UTI_INT_TO | TINYINT | YES |
| main | internacoes | 12 | IND_VDRL | BOOLEAN | YES |
| main | internacoes | 13 | MORTE | BOOLEAN | YES |
| main | internacoes | 14 | GESTRISCO | BOOLEAN | YES |
| main | internacoes | 15 | DIAG_PRINC | VARCHAR | YES |
| main | internacoes | 16 | DIAG_SECUN | VARCHAR | YES |
| main | internacoes | 17 | CID_MORTE | VARCHAR | YES |
| main | internacoes | 18 | CID_NOTIF | VARCHAR | YES |
| main | internacoes | 19 | DIAGSEC1 | VARCHAR | YES |
| main | internacoes | 20 | DIAGSEC2 | VARCHAR | YES |
| main | internacoes | 21 | DIAGSEC3 | VARCHAR | YES |
| main | internacoes | 22 | DIAGSEC4 | VARCHAR | YES |
| main | internacoes | 23 | DIAGSEC5 | VARCHAR | YES |
| main | internacoes | 24 | DIAGSEC6 | VARCHAR | YES |
| main | internacoes | 25 | DIAGSEC7 | VARCHAR | YES |
| main | internacoes | 26 | DIAGSEC8 | VARCHAR | YES |
| main | internacoes | 27 | DIAGSEC9 | VARCHAR | YES |
| main | internacoes | 28 | VAL_SH | DOUBLE | YES |
| main | internacoes | 29 | VAL_SP | DOUBLE | YES |
| main | internacoes | 30 | VAL_UTI | DOUBLE | YES |
| main | internacoes | 31 | VAL_TOT | DOUBLE | YES |
| main | internacoes | 32 | NASC | DATE | YES |
| main | internacoes | 33 | IDADE | SMALLINT | YES |
| main | internacoes | 34 | SEXO | TINYINT | YES |
| main | internacoes | 35 | RACA_COR | TINYINT | YES |
| main | internacoes | 36 | ETNIA | SMALLINT | YES |
| main | internacoes | 37 | NACIONAL | SMALLINT | YES |
| main | internacoes | 38 | INSTRU | TINYINT | YES |
| main | internacoes | 39 | VINCPREV | TINYINT | YES |
| main | internacoes | 40 | CBOR | VARCHAR | YES |
| main | internacoes | 41 | MUNIC_RES | INTEGER | YES |
| main | internacoes | 42 | CEP | VARCHAR | YES |
| main | internacoes | 43 | NUM_FILHOS | TINYINT | YES |
| main | internacoes | 44 | CONTRACEP1 | TINYINT | YES |
| main | internacoes | 45 | CONTRACEP2 | TINYINT | YES |
| main | internacoes | 46 | INSC_PN | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N_AIH | BIGINT | 0.0 | exact | 183877219 |  | 183877219 | True | 1107100903524 | 9923300006499 |
| CNES | INTEGER | 0.0 | exact | 6873 |  | 6873 | True | 27 | 9997784 |
| DT_INTER | DATE | 0.0 | exact | 6148 |  | 6148 | True | 2000-01-01 | 2023-12-31 |
| DT_SAIDA | DATE | 0.0 | exact | 5997 |  | 5997 | True | 2007-08-01 | 2023-12-31 |
| DIAS_PERM | SMALLINT | 0.0 | approx |  | 44 | 44 | False | 0 | 97 |
| DIAR_ACOM | SMALLINT | 0.0 | approx |  | 243 | 243 | False | 0 | 361 |
| CAR_INT | TINYINT | 0.0 | approx |  | 6 | 6 | False | 1 | 6 |
| ESPEC | TINYINT | 0.0 | approx |  | 17 | 17 | False | 1 | 87 |
| COMPLEX | VARCHAR | 0.0 | approx |  | 3 | 3 | False | 00 | 03 |
| MARCA_UTI | TINYINT | 0.0 | approx |  | 18 | 18 | False | 0 | 99 |
| UTI_INT_TO | TINYINT | 0.0 | approx |  | 28 | 28 | False | 0 | 125 |
| IND_VDRL | BOOLEAN | 0.0 | approx |  | 2 | 2 | False | False | True |
| MORTE | BOOLEAN | 0.0 | exact | 2 |  | 2 | True | False | True |
| GESTRISCO | BOOLEAN | 0.0 | approx |  | 2 | 2 | False | False | True |
| DIAG_PRINC | VARCHAR | 0.0 | exact | 11830 |  | 11830 | True | A00 | Z999 |
| DIAG_SECUN | VARCHAR | 0.0 | approx |  | 13216 | 13216 | False |  | Z999 |
| CID_MORTE | VARCHAR | 0.0 | approx |  | 6994 | 6994 | False |  | Z999 |
| CID_NOTIF | VARCHAR | 0.0 | approx |  | 67 | 67 | False |  | ZZ30 |
| DIAGSEC1 | VARCHAR | 0.363291 | approx |  | 14603 | 14603 | False |  | Z999 |
| DIAGSEC2 | VARCHAR | 0.363291 | approx |  | 10905 | 10905 | False |  | Z999 |
| DIAGSEC3 | VARCHAR | 0.363291 | approx |  | 6766 | 6766 | False |  | Z999 |
| DIAGSEC4 | VARCHAR | 0.363291 | approx |  | 6275 | 6275 | False |  | Z999 |
| DIAGSEC5 | VARCHAR | 0.363291 | approx |  | 4928 | 4928 | False |  | Z993 |
| DIAGSEC6 | VARCHAR | 0.363291 | approx |  | 3364 | 3364 | False |  | Z992 |
| DIAGSEC7 | VARCHAR | 0.363291 | approx |  | 1634 | 1634 | False |  | Z999 |
| DIAGSEC8 | VARCHAR | 0.363291 | approx |  | 1 | 1 | False |  |  |
| DIAGSEC9 | VARCHAR | 0.363291 | approx |  | 1 | 1 | False |  |  |
| VAL_SH | DOUBLE | 0.0 | approx |  | 2020322 | 2020322 | False | 0.0 | 450734.6699999999 |
| VAL_SP | DOUBLE | 0.0 | approx |  | 601585 | 601585 | False | 0.0 | 72642.67 |
| VAL_UTI | DOUBLE | 0.0 | approx |  | 42144 | 42144 | False | 0.0 | 272000.0 |
| VAL_TOT | DOUBLE | 0.0 | exact | 4560227 |  | 4560227 | True | 0.0 | 546207.48 |
| NASC | DATE | 0.0 | approx |  | 40851 | 40851 | False | 1887-10-10 | 2023-12-31 |
| IDADE | SMALLINT | 0.0 | approx |  | 83 | 83 | False | 0 | 99 |
| SEXO | TINYINT | 0.0 | approx |  | 2 | 2 | False | 1 | 3 |
| RACA_COR | TINYINT | 0.0 | approx |  | 6 | 6 | False | 1 | 99 |
| ETNIA | SMALLINT | 0.0 | approx |  | 292 | 292 | False | 0 | 264 |
| NACIONAL | SMALLINT | 0.0 | approx |  | 342 | 342 | False | 0 | 350 |
| INSTRU | TINYINT | 0.0 | approx |  | 10 | 10 | False | 0 | 9 |
| VINCPREV | TINYINT | 0.0 | approx |  | 7 | 7 | False | 0 | 6 |
| CBOR | VARCHAR | 0.0 | approx |  | 593 | 593 | False | 000000 | 992225 |
| MUNIC_RES | INTEGER | 0.0 | exact | 5588 |  | 5588 | True | 110001 | 530180 |
| CEP | VARCHAR | 0.0 | approx |  | 1331685 | 1331685 | False | 00411330 | 99990971 |
| NUM_FILHOS | TINYINT | 0.0 | approx |  | 65 | 65 | False | 0 | 99 |
| CONTRACEP1 | TINYINT | 0.0 | approx |  | 16 | 16 | False | 0 | 13 |
| CONTRACEP2 | TINYINT | 0.0 | approx |  | 16 | 16 | False | 0 | 13 |
| INSC_PN | VARCHAR | 0.0 | approx |  | 4097423 | 4097423 | False | -1838225210 | 999999999999 |

### marca_uti


Rows: `17`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | marca_uti | 1 | MARCA_UTI | TINYINT | NO |
| main | marca_uti | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MARCA_UTI | TINYINT | 0.0 | exact | 17 |  | 17 | True | 0 | 99 |
| DESCRICAO | VARCHAR | 0.0 | exact | 17 |  | 17 | True | Não utilizou UTI | Utilizou mais de um tipo de UTI |

### municipios


Rows: `5,589`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | municipios | 1 | CO_MUNICIPIO_6D | INTEGER | NO |
| main | municipios | 2 | CO_MUNICIPIO_7D | INTEGER | YES |
| main | municipios | 3 | NO_MUNICIPIO | VARCHAR | YES |
| main | municipios | 4 | SG_UF | VARCHAR | YES |
| main | municipios | 5 | NO_REGIAO_SAUDE | VARCHAR | YES |
| main | municipios | 6 | latitude | FLOAT | YES |
| main | municipios | 7 | longitude | FLOAT | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CO_MUNICIPIO_6D | INTEGER | 0.0 | exact | 5589 |  | 5589 | True | 110001 | 530010 |
| CO_MUNICIPIO_7D | INTEGER | 0.003221 | exact | 5571 |  | 5571 | True | 1100015 | 5300108 |
| NO_MUNICIPIO | VARCHAR | 0.0 | exact | 5315 |  | 5315 | True | 130002 Alvaraes | Óleo |
| SG_UF | VARCHAR | 0.0 | exact | 38 |  | 38 | True | 13 | TO |
| NO_REGIAO_SAUDE | VARCHAR | 0.003221 | exact | 425 |  | 425 | True | 10ª RS Cascavel | Área Sudoeste |
| latitude | FLOAT | 0.0034 | exact | 5513 |  | 5513 | True | -33.6593017578125 | 4.646299839019775 |
| longitude | FLOAT | 0.0034 | exact | 5485 |  | 5485 | True | -73.34529876708984 | -32.42679977416992 |

### nacionalidade


Rows: `332`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | nacionalidade | 1 | NACIONAL | SMALLINT | NO |
| main | nacionalidade | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NACIONAL | SMALLINT | 0.0 | exact | 332 |  | 332 | True | 10 | 350 |
| DESCRICAO | VARCHAR | 0.0 | exact | 329 |  | 329 | True | Abissinia | Zimbabwe |

### procedimentos


Rows: `5,394`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | procedimentos | 1 | PROC_REA | BIGINT | NO |
| main | procedimentos | 2 | NOME_PROC | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PROC_REA | BIGINT | 0.0 | exact | 5394 |  | 5394 | True | 101010010 | 803010141 |
| NOME_PROC | VARCHAR | 0.0 | exact | 5237 |  | 5237 | True | .QUIMIOTERAPIA DE LEUCEMIA LINFOIDE/LINFOBLASTICA AGUDA, LEUCEMIA MIELOIDE AGUDA E LEUCEMIA PROMIELO | ZIPRASIDONA 80 MG (POR CAPSULA) |

### raca_cor


Rows: `5`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | raca_cor | 1 | RACA_COR | TINYINT | NO |
| main | raca_cor | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RACA_COR | TINYINT | 0.0 | exact | 5 |  | 5 | True | 1 | 5 |
| DESCRICAO | VARCHAR | 0.0 | exact | 5 |  | 5 | True | Amarela | Preta |

### sexo


Rows: `3`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | sexo | 1 | SEXO | TINYINT | NO |
| main | sexo | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEXO | TINYINT | 0.0 | exact | 3 |  | 3 | True | 1 | 3 |
| DESCRICAO | VARCHAR | 0.0 | exact | 2 |  | 2 | True | Feminino | Masculino |

### socioeconomico


Rows: `72,395`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | socioeconomico | 1 | CO_MUNICIPIO_6D | INTEGER | NO |
| main | socioeconomico | 2 | NU_ANO | SMALLINT | NO |
| main | socioeconomico | 3 | QT_POPULACAO | BIGINT | YES |
| main | socioeconomico | 4 | VL_PIB_PERCAPITA | DOUBLE | YES |
| main | socioeconomico | 5 | QT_OBITOS_INFANTIS | INTEGER | YES |
| main | socioeconomico | 6 | QT_NASCIDOS_VIVOS | INTEGER | YES |
| main | socioeconomico | 7 | VL_MORT_INFANTIL | DOUBLE | YES |
| main | socioeconomico | 8 | QT_LEITOS_SUS | INTEGER | YES |
| main | socioeconomico | 9 | VL_LEITOS_SUS_1000 | DOUBLE | YES |
| main | socioeconomico | 10 | QT_MEDICOS | INTEGER | YES |
| main | socioeconomico | 11 | VL_MEDICOS_1000 | DOUBLE | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CO_MUNICIPIO_6D | INTEGER | 0.0 | exact | 5570 |  | 5570 | True | 110001 | 530010 |
| NU_ANO | SMALLINT | 0.0 | exact | 13 |  | 13 | True | 2008 | 2021 |
| QT_POPULACAO | BIGINT | 0.0 | exact | 35070 |  | 35070 | True | 771 | 12396372 |
| VL_PIB_PERCAPITA | DOUBLE | 8.3e-05 | exact | 66659 |  | 66659 | True | -19046.0 | 828980747.0 |
| QT_OBITOS_INFANTIS | INTEGER | 0.0 | exact | 336 |  | 336 | True | 0 | 2109 |
| QT_NASCIDOS_VIVOS | INTEGER | 0.0 | exact | 4128 |  | 4128 | True | 0 | 176487 |
| VL_MORT_INFANTIL | DOUBLE | 8.3e-05 | exact | 3260 |  | 3260 | True | 0.0 | 285.71 |
| QT_LEITOS_SUS | INTEGER | 0.366531 | exact | 1172 |  | 1172 | True | 0 | 16099 |
| VL_LEITOS_SUS_1000 | DOUBLE | 0.366531 | exact | 21652 |  | 21652 | True | 0.0 | 25.6731 |
| QT_MEDICOS | INTEGER | 0.009462 | exact | 1728 |  | 1728 | True | 1 | 58449 |
| VL_MEDICOS_1000 | DOUBLE | 0.009462 | exact | 26461 |  | 26461 | True | 0.0331 | 55.2304 |

### stg_hospital


Rows: `6,873`. Classification: `outro`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | stg_hospital | 1 | CNES | INTEGER | YES |
| main | stg_hospital | 2 | NO_HOSPITAL | VARCHAR | YES |
| main | stg_hospital | 3 | MUNIC_MOV | INTEGER | YES |
| main | stg_hospital | 4 | NATUREZA | VARCHAR | YES |
| main | stg_hospital | 5 | GESTAO | VARCHAR | YES |
| main | stg_hospital | 6 | NAT_JUR | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CNES | INTEGER | 0.0 | exact | 6873 |  | 6873 | True | 27 | 9997784 |
| NO_HOSPITAL | VARCHAR | 0.457733 | exact | 3196 |  | 3196 | True | ABIMED SERVICOS MEDICOS LTDA | Y A PENHA E CIA LTDA |
| MUNIC_MOV | INTEGER | 0.0 | exact | 3606 |  | 3606 | True | 110001 | 530010 |
| NATUREZA | VARCHAR | 0.0 | exact | 9 |  | 9 | True | 00 | 80 |
| GESTAO | VARCHAR | 0.0 | exact | 2 |  | 2 | True | 1 | 2 |
| NAT_JUR | VARCHAR | 0.811145 | exact | 25 |  | 25 | True |  | 3999 |

### stg_internacoes


Rows: `183,877,219`. Classification: `fato/staging`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | stg_internacoes | 1 | N_AIH | BIGINT | YES |
| main | stg_internacoes | 2 | CNES | INTEGER | YES |
| main | stg_internacoes | 3 | DT_INTER | DATE | YES |
| main | stg_internacoes | 4 | DT_SAIDA | DATE | YES |
| main | stg_internacoes | 5 | DIAS_PERM | BIGINT | YES |
| main | stg_internacoes | 6 | DIAR_ACOM | SMALLINT | YES |
| main | stg_internacoes | 7 | CAR_INT | TINYINT | YES |
| main | stg_internacoes | 8 | ESPEC | TINYINT | YES |
| main | stg_internacoes | 9 | COMPLEX | VARCHAR | YES |
| main | stg_internacoes | 10 | MARCA_UTI | TINYINT | YES |
| main | stg_internacoes | 11 | UTI_INT_TO | TINYINT | YES |
| main | stg_internacoes | 12 | IND_VDRL | BOOLEAN | YES |
| main | stg_internacoes | 13 | MORTE | BOOLEAN | YES |
| main | stg_internacoes | 14 | CID_MORTE | VARCHAR | YES |
| main | stg_internacoes | 15 | GESTRISCO | BOOLEAN | YES |
| main | stg_internacoes | 16 | DIAG_PRINC | VARCHAR | YES |
| main | stg_internacoes | 17 | DIAG_SECUN | VARCHAR | YES |
| main | stg_internacoes | 18 | CID_MORTE_1 | VARCHAR | YES |
| main | stg_internacoes | 19 | CID_NOTIF | VARCHAR | YES |
| main | stg_internacoes | 20 | DIAGSEC1 | VARCHAR | YES |
| main | stg_internacoes | 21 | DIAGSEC2 | VARCHAR | YES |
| main | stg_internacoes | 22 | DIAGSEC3 | VARCHAR | YES |
| main | stg_internacoes | 23 | DIAGSEC4 | VARCHAR | YES |
| main | stg_internacoes | 24 | DIAGSEC5 | VARCHAR | YES |
| main | stg_internacoes | 25 | DIAGSEC6 | VARCHAR | YES |
| main | stg_internacoes | 26 | DIAGSEC7 | VARCHAR | YES |
| main | stg_internacoes | 27 | DIAGSEC8 | VARCHAR | YES |
| main | stg_internacoes | 28 | DIAGSEC9 | VARCHAR | YES |
| main | stg_internacoes | 29 | VAL_SH | DOUBLE | YES |
| main | stg_internacoes | 30 | VAL_SP | DOUBLE | YES |
| main | stg_internacoes | 31 | VAL_UTI | DOUBLE | YES |
| main | stg_internacoes | 32 | VAL_TOT | DOUBLE | YES |
| main | stg_internacoes | 33 | NASC | DATE | YES |
| main | stg_internacoes | 34 | IDADE | SMALLINT | YES |
| main | stg_internacoes | 35 | SEXO | TINYINT | YES |
| main | stg_internacoes | 36 | RACA_COR | TINYINT | YES |
| main | stg_internacoes | 37 | ETNIA | SMALLINT | YES |
| main | stg_internacoes | 38 | NACIONAL | SMALLINT | YES |
| main | stg_internacoes | 39 | INSTRU | TINYINT | YES |
| main | stg_internacoes | 40 | VINCPREV | TINYINT | YES |
| main | stg_internacoes | 41 | CBOR | VARCHAR | YES |
| main | stg_internacoes | 42 | MUNIC_RES | INTEGER | YES |
| main | stg_internacoes | 43 | CEP | VARCHAR | YES |
| main | stg_internacoes | 44 | NUM_FILHOS | TINYINT | YES |
| main | stg_internacoes | 45 | CONTRACEP1 | TINYINT | YES |
| main | stg_internacoes | 46 | CONTRACEP2 | TINYINT | YES |
| main | stg_internacoes | 47 | INSC_PN | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N_AIH | BIGINT | 0.0 | exact | 183877219 |  | 183877219 | True | 1107100903524 | 9923300006499 |
| CNES | INTEGER | 0.0 | approx |  | 7137 | 7137 | False | 27 | 9997784 |
| DT_INTER | DATE | 0.0 | approx |  | 5779 | 5779 | False | 2000-01-01 | 2023-12-31 |
| DT_SAIDA | DATE | 0.0 | approx |  | 5779 | 5779 | False | 2007-08-01 | 2023-12-31 |
| DIAS_PERM | BIGINT | 0.0 | approx |  | 1624 | 1624 | False | 0 | 3406 |
| DIAR_ACOM | SMALLINT | 0.0 | approx |  | 243 | 243 | False | 0 | 361 |
| CAR_INT | TINYINT | 0.0 | approx |  | 6 | 6 | False | 1 | 6 |
| ESPEC | TINYINT | 0.0 | approx |  | 17 | 17 | False | 1 | 87 |
| COMPLEX | VARCHAR | 0.0 | approx |  | 3 | 3 | False | 00 | 03 |
| MARCA_UTI | TINYINT | 0.0 | approx |  | 18 | 18 | False | 0 | 99 |
| UTI_INT_TO | TINYINT | 0.0 | approx |  | 28 | 28 | False | 0 | 125 |
| IND_VDRL | BOOLEAN | 0.0 | approx |  | 2 | 2 | False | False | True |
| MORTE | BOOLEAN | 0.0 | approx |  | 2 | 2 | False | False | True |
| CID_MORTE | VARCHAR | 0.984381 | approx |  | 6994 | 6994 | False | A000 | Z999 |
| GESTRISCO | BOOLEAN | 0.0 | approx |  | 2 | 2 | False | False | True |
| DIAG_PRINC | VARCHAR | 0.0 | approx |  | 12057 | 12057 | False | A00 | Z999 |
| DIAG_SECUN | VARCHAR | 0.942658 | approx |  | 13216 | 13216 | False | A000 | Z999 |
| CID_MORTE_1 | VARCHAR | 0.984381 | approx |  | 6994 | 6994 | False | A000 | Z999 |
| CID_NOTIF | VARCHAR | 0.990517 | approx |  | 62 | 62 | False | A302 | Z320 |
| DIAGSEC1 | VARCHAR | 0.882379 | approx |  | 14603 | 14603 | False | A00 | Z999 |
| DIAGSEC2 | VARCHAR | 0.987352 | approx |  | 10905 | 10905 | False | A000 | Z999 |
| DIAGSEC3 | VARCHAR | 0.99513 | approx |  | 6766 | 6766 | False | A000 | Z999 |
| DIAGSEC4 | VARCHAR | 0.998012 | approx |  | 5977 | 5977 | False | A000 | Z999 |
| DIAGSEC5 | VARCHAR | 0.999243 | approx |  | 4743 | 4743 | False | A000 | Z993 |
| DIAGSEC6 | VARCHAR | 0.999733 | approx |  | 3364 | 3364 | False | A029 | Z992 |
| DIAGSEC7 | VARCHAR | 0.999904 | approx |  | 1634 | 1634 | False | A047 | Z999 |
| DIAGSEC8 | VARCHAR | 1.0 | approx |  | 0 | 0 | False |  |  |
| DIAGSEC9 | VARCHAR | 1.0 | approx |  | 0 | 0 | False |  |  |
| VAL_SH | DOUBLE | 0.0 | approx |  | 2020322 | 2020322 | False | 0.0 | 450734.6699999999 |
| VAL_SP | DOUBLE | 0.0 | approx |  | 601585 | 601585 | False | 0.0 | 72642.67 |
| VAL_UTI | DOUBLE | 0.0 | approx |  | 42144 | 42144 | False | 0.0 | 272000.0 |
| VAL_TOT | DOUBLE | 0.0 | approx |  | 4487654 | 4487654 | False | 0.0 | 546207.48 |
| NASC | DATE | 0.0 | approx |  | 40851 | 40851 | False | 1887-10-10 | 2023-12-31 |
| IDADE | SMALLINT | 0.0 | approx |  | 83 | 83 | False | 0 | 99 |
| SEXO | TINYINT | 0.0 | approx |  | 2 | 2 | False | 1 | 3 |
| RACA_COR | TINYINT | 0.0 | approx |  | 6 | 6 | False | 0 | 5 |
| ETNIA | SMALLINT | 0.0 | approx |  | 292 | 292 | False | 0 | 264 |
| NACIONAL | SMALLINT | 0.0 | approx |  | 342 | 342 | False | 0 | 350 |
| INSTRU | TINYINT | 0.0 | approx |  | 10 | 10 | False | 0 | 9 |
| VINCPREV | TINYINT | 0.0 | approx |  | 7 | 7 | False | 0 | 6 |
| CBOR | VARCHAR | 0.0 | approx |  | 593 | 593 | False | 000000 | 992225 |
| MUNIC_RES | INTEGER | 0.0 | approx |  | 6496 | 6496 | False | 110001 | 530010 |
| CEP | VARCHAR | 0.0 | approx |  | 1331685 | 1331685 | False | 00411330 | 99990971 |
| NUM_FILHOS | TINYINT | 0.0 | approx |  | 65 | 65 | False | 0 | 99 |
| CONTRACEP1 | TINYINT | 0.0 | approx |  | 14 | 14 | False | 0 | 12 |
| CONTRACEP2 | TINYINT | 0.0 | approx |  | 14 | 14 | False | 0 | 12 |
| INSC_PN | VARCHAR | 0.965703 | approx |  | 4033411 | 4033411 | False | -1838225210 | 999999999999 |

### stg_sexo


Rows: `2`. Classification: `outro`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | stg_sexo | 1 | SEXO | TINYINT | YES |
| main | stg_sexo | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEXO | TINYINT | 0.0 | exact | 2 |  | 2 | True | 1 | 3 |
| DESCRICAO | VARCHAR | 0.0 | exact | 2 |  | 2 | True | Feminino | Masculino |

### tempo


Rows: `6,210`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | tempo | 1 | data | DATE | NO |
| main | tempo | 2 | ano | SMALLINT | YES |
| main | tempo | 3 | mes | TINYINT | YES |
| main | tempo | 4 | trimestre | TINYINT | YES |
| main | tempo | 5 | dia_semana | TINYINT | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data | DATE | 0.0 | exact | 6210 |  | 6210 | True | 2008-01-01 | 2024-12-31 |
| ano | SMALLINT | 0.0 | exact | 17 |  | 17 | True | 2008 | 2024 |
| mes | TINYINT | 0.0 | exact | 12 |  | 12 | True | 1 | 12 |
| trimestre | TINYINT | 0.0 | exact | 4 |  | 4 | True | 1 | 4 |
| dia_semana | TINYINT | 0.0 | exact | 7 |  | 7 | True | 1 | 7 |

### vincprev


Rows: `6`. Classification: `dimensao/referencia`.

| table_schema | table_name | ordinal_position | column_name | data_type | is_nullable |
| --- | --- | --- | --- | --- | --- |
| main | vincprev | 1 | VINCPREV | TINYINT | NO |
| main | vincprev | 2 | DESCRICAO | VARCHAR | YES |


Column profile:

| column_name | data_type | null_rate | profile_mode | exact_distinct_count | approx_distinct_count | distinct_count_for_catalog | distinct_is_exact | min_value | max_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VINCPREV | TINYINT | 0.0 | exact | 6 |  | 6 | True | 1 | 6 |
| DESCRICAO | VARCHAR | 0.0 | exact | 6 |  | 6 | True | Aposentado | Não segurado |
