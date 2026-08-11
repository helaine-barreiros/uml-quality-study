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

O publisher/proceedings TOC estabelece a membership documental de cada unidade de busca manual. Crossref e outras APIs são usadas apenas para metadata enrichment de registros já identificados; elas não definem, sozinhas, o universo documental de um venue-year. Quando disponível, a fonte oficial do venue é um cross-check independente.

Divergências entre fontes devem gerar `InventoryConflict` e impedem que a unidade seja marcada `COMPLETE` até a reconciliação. A estrutura permite auditar: (1) por que um artigo foi considerado; (2) de onde vieram seus metadados; e (3) se todos os itens do proceedings foram efetivamente inspecionados.
