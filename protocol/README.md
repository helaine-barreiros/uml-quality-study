# Protocolo

A versão metodológica corrente é a 1.7. A v1.7 incorpora a validação já realizada das buscas Scopus, IEEE Xplore e ACM, e formaliza a cadeia de proveniência da busca manual:

```text
PRIMARY_TOC / source evidence
-> source_manifest.csv
-> raw/inventory_raw.csv
-> normalized/inventory.csv
-> screening/discovery.csv
```

A versão 1.7 não altera as research questions, eligibility criteria, analytical layers ou review interval. Futuras alterações após eventual registro formal devem ser tratadas como amendments, conforme o próprio protocolo.

O [Amendment A001](amendments/A001-normalized-inventory-schema.md) define prospectivamente o schema da camada normalized, sem alterar a versão metodológica corrente 1.7.

O [Amendment A002](amendments/A002-documentary-collection-before-discovery.md), revisado por A002-R1, formaliza uma arquitetura de coleta documental em duas ondas, com fechamento pré-discovery auditável e atualização final obrigatória, sem alterar a versão metodológica corrente 1.7.
