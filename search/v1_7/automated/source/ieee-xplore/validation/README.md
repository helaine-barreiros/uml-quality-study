# Validação IEEE Xplore

Resultados de validação registrados em `ieee_xplore_search_validation_log_v1_0.csv`:

- I0 = invalid implementation produced by Structured Advanced Search
- I1 = 327
- I2 = 104
- I3 = 283

Source-specific seed denominator = 4.

Configuração aceita: I3 / IEEE Xplore search strategy v1.0.

Conceitualmente:

```text
LLM_{Title,Abstract,AuthorKeywords}
AND
UML_{AllMetadata}
AND
Generation_{AllMetadata}
```

I2 foi rejeitada porque a restrição do bloco UML introduziu risco de falsos negativos. Não publique os raw CSV exports da plataforma nesta tarefa.

## Reproducibility and licensing

A query, decisões, contagens e validation log são publicáveis no replication package. Exports brutos obtidos de plataformas licenciadas não são adicionados automaticamente ao repositório público; os arquivos originais devem ser preservados no armazenamento controlado do projeto quando necessário para auditoria. Qualquer redistribuição futura depende das condições de uso da fonte correspondente.
