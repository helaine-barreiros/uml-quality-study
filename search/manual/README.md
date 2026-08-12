# Busca manual

As unidades de busca manual registram o universo documental, suas fontes e a classificação de discovery separadamente do screening formal. O log consolida o estado e as contagens de cada unidade quando forem realizadas.

Em `source_manifest.csv`, `SourceRole` aceitará, no mínimo, `PRIMARY_TOC`, `VENUE_CROSSCHECK`, `METADATA_SOURCE` e `AUXILIARY_NAVIGATION`.

Os três registros globais têm funções distintas:

- [manual_venue_plan.csv](manual_venue_plan.csv) representa o plano global de venues core e condicionais;
- [manual_search_unit_registry.csv](manual_search_unit_registry.csv) representa somente unidades concretamente instanciadas;
- [manual_venue_search_log.csv](manual_venue_search_log.csv) preserva resultados e contagens de execução quando produzidos.

Os critérios gerais de promoção de venues condicionais permanecem os do protocolo v1.7: (1) seed relevante não recuperado por fonte automatizada core; (2) pelo menos dois candidatos elegíveis identificados durante busca automatizada, pilot screening ou snowballing; ou (3) decisão conjunta baseada em risco documentado de cobertura. Nenhum trigger é avaliado neste registro.
