# Validação Scopus

Contagens de validação registradas em `scopus_search_validation_log_v1_0.csv`:

- S1 = 376
- S2 = 371
- S3 = 250
- S4 = 249

Configuração aceita: S4 / Scopus search strategy v1.0.

Conceitualmente:

```text
LLM_{TITLE-ABS-KEY}
AND
UML_{TITLE-ABS OR AUTHKEY}
AND
Generation_{TITLE-ABS-KEY}
```

`foundation model*` foi removido durante a validação. Não inclua raw RIS exports no repositório público.

## Reproducibility and licensing

A query, decisões, contagens e validation log são publicáveis no replication package. Exports brutos obtidos de plataformas licenciadas não são adicionados automaticamente ao repositório público; os arquivos originais devem ser preservados no armazenamento controlado do projeto quando necessário para auditoria. Qualquer redistribuição futura depende das condições de uso da fonte correspondente.
