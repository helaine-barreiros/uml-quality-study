# Cadeia de proveniência planejada

```text
Official publisher/proceedings TOC
-> immutable source evidence
-> raw documentary inventory
-> venue cross-check
-> bibliographic metadata enrichment
-> normalized inventory
-> manual discovery classification
-> Layer 1 screening
-> Layer 2 extraction when applicable
```

```text
PRIMARY_TOC / source snapshot
-> raw/inventory_raw.csv
-> reconciliation
-> normalized/inventory.csv
-> DOCUMENTARY COLLECTION GATE
-> screening/discovery.csv
-> formal Layer 1 screening
```

O publisher/proceedings TOC estabelece a membership documental de cada unidade de busca manual. A membership documental nasce no `PRIMARY_TOC`, e `raw/inventory_raw.csv` materializa todos os itens observados nesse universo. `normalized/inventory.csv` não pode criar silenciosamente novos membros do universo documental: todo registro normalizado deve ser rastreável a um `ManualSearchID` existente no inventário bruto. Registros adicionais descobertos durante a reconciliação entre fontes devem ser documentados como `InventoryConflict` e só podem ser incorporados após reconciliação explícita da membership.

Crossref e outras APIs são usadas apenas para metadata enrichment de registros já identificados; elas não definem, sozinhas, o universo documental de um venue-year. Quando disponível, a fonte oficial do venue é um cross-check independente.

Divergências entre fontes devem gerar `InventoryConflict` e impedem que a unidade seja marcada `COMPLETE` até a reconciliação. A estrutura permite auditar: (1) por que um artigo foi considerado; (2) de onde vieram seus metadados; e (3) se todos os itens do proceedings foram efetivamente inspecionados.

O gate é um controle operacional introduzido pelo Amendment A002 e revisado por A002-R1; ele não altera a membership documental. `DocumentaryCollectionStatus=COMPLETE` não promove uma unidade a `UnitStatus=COMPLETE`. As camadas raw e normalized permanecem separadas, e nenhum registro pode ser classificado enquanto `DiscoveryPhaseStatus=DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`.

A cadeia global é:

```text
PRE-DISCOVERY DOCUMENTARY COLLECTION WAVE
-> PRE_DISCOVERY_COLLECTION_CLOSED
-> manual discovery classification
-> candidate consolidation and deduplication
-> formal Layer 1 screening
-> post-screening conditional trigger review
-> snowballing
-> FINAL SEARCH UPDATE WAVE
-> discovery and screening of newly identified records
-> FINAL_SEARCH_UPDATE_COMPLETE
-> final synthesis
```

A primeira onda estabelece o conjunto documental necessário para iniciar discovery, mas seu fechamento não encerra definitivamente todas as rotas de identificação. A segunda onda é obrigatória para a atualização final. Venues ativados nessa segunda onda seguem o mesmo pipeline de proveniência, inventário raw, reconciliação, normalização, discovery e screening. Nenhuma síntese final ocorre antes de `FINAL_SEARCH_UPDATE_COMPLETE`.
