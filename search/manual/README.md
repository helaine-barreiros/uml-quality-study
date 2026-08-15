# Busca manual

As unidades de busca manual registram o universo documental, suas fontes e a classificação de discovery separadamente do screening formal. O log consolida o estado e as contagens de cada unidade quando forem realizadas.

Em `source_manifest.csv`, `SourceRole` aceitará, no mínimo, `PRIMARY_TOC`, `VENUE_CROSSCHECK`, `METADATA_SOURCE` e `AUXILIARY_NAVIGATION`.

Os três registros globais têm funções distintas:

- [manual_venue_plan.csv](manual_venue_plan.csv) representa o plano global de venues core e condicionais;
- [manual_search_unit_registry.csv](manual_search_unit_registry.csv) representa somente unidades concretamente instanciadas;
- [manual_venue_search_log.csv](manual_venue_search_log.csv) preserva resultados e contagens de execução quando produzidos.
- [manual_collection_phase_log.csv](manual_collection_phase_log.csv) registra a fase global e os marcos de fechamento das duas ondas;
- [manual_conditional_venue_trigger_log.csv](manual_conditional_venue_trigger_log.csv) preserva separadamente as revisões pré-discovery e pós-screening dos triggers condicionais.
- [final_search_update_iteration_log.csv](final_search_update_iteration_log.csv) registra cada iteração da atualização final e as métricas do ponto fixo.

Os critérios gerais de promoção de venues condicionais permanecem os do protocolo v1.7: (1) seed relevante não recuperado por fonte automatizada core; (2) pelo menos dois candidatos elegíveis identificados durante busca automatizada, pilot screening ou snowballing; ou (3) decisão conjunta baseada em risco documentado de cobertura. Nenhum trigger é avaliado neste registro.

A002-R2 organiza a sequência como `initial screening -> snowballing -> screening of snowballing records -> conditional trigger review -> final update iterations -> fixed-point closure`. Venues ativados na segunda onda percorrem o mesmo pipeline documental e seletivo; novos estudos podem reabrir snowballing e trigger review antes da síntese.

O batch offline da família IEEE Requirements Engineering é documentado em [venues/re/](venues/re/). Os TOCs e exports controlados não são redistribuídos; os registros públicos preservam apenas proveniência, hashes, contagens, lacunas e estados de execução.

O batch offline da família NLBSE é documentado em [venues/nlbse/](venues/nlbse/). BibTeX e pacotes PDF permanecem controlados; apenas TOCs completos do publisher podem definir membership.
