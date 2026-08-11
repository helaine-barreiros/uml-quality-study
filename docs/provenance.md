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
-> normalized/inventory.csv
-> screening/discovery.csv
```

O publisher/proceedings TOC estabelece a membership documental de cada unidade de busca manual. A membership documental nasce no `PRIMARY_TOC`, e `raw/inventory_raw.csv` materializa todos os itens observados nesse universo. `normalized/inventory.csv` não pode criar silenciosamente novos membros do universo documental: todo registro normalizado deve ser rastreável a um `ManualSearchID` existente no inventário bruto. Registros adicionais descobertos durante a reconciliação entre fontes devem ser documentados como `InventoryConflict` e só podem ser incorporados após reconciliação explícita da membership.

Crossref e outras APIs são usadas apenas para metadata enrichment de registros já identificados; elas não definem, sozinhas, o universo documental de um venue-year. Quando disponível, a fonte oficial do venue é um cross-check independente.

Divergências entre fontes devem gerar `InventoryConflict` e impedem que a unidade seja marcada `COMPLETE` até a reconciliação. A estrutura permite auditar: (1) por que um artigo foi considerado; (2) de onde vieram seus metadados; e (3) se todos os itens do proceedings foram efetivamente inspecionados.
