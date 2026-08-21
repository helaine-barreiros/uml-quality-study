# Evidência bruta

`inventory_raw.csv` constitui o inventário documental bruto da unidade. Ele deve conter todos os itens pertencentes ao universo estabelecido pelo `PRIMARY_TOC`, não apenas candidatos. Nenhuma decisão de relevância ocorre nesta etapa.

Os valores são preservados exatamente como observados. Depois que a unidade de inventário bruto for registrada e versionada, correções posteriores devem ocorrer na camada `normalized`, sem sobrescrever silenciosamente os valores raw. `InventorySourceID` liga cada linha ao `source/source_manifest.csv`, e `ManualSearchID` é preservado nas camadas `normalized` e `screening`.
