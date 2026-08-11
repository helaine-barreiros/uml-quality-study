# Validação ACM

Fonte: ACM Full-Text Collection.

Resultados de validação registrados em `acm_fulltext_search_validation_log_v1_0.csv`:

- A1 = 1,854
- A2 = 454
- A3 = 104
- A4 = not executed

Source-specific seed denominator = 1.

Configuração aceita: A2 / ACM Full-Text Collection search strategy v1.0.

Conceitualmente:

```text
LLM_{Title OR Abstract OR AuthorKeyword}
AND
UML_{Anywhere}
AND
Generation_{Anywhere}
```

A3 foi rejeitada por evidência diagnóstica de falso negativo. A4 não foi executada porque herdaria a restrição problemática de A3. O arquivo EndNote disponível de A1 continha somente 1.000 dos 1.854 resultados e, portanto, é tratado no protocolo como partial diagnostic export, não como corpus bruto completo. Não adicione arquivos `.enw` ao repositório público nesta tarefa.

## Reproducibility and licensing

A query, decisões, contagens e validation log são publicáveis no replication package. Exports brutos obtidos de plataformas licenciadas não são adicionados automaticamente ao repositório público; os arquivos originais devem ser preservados no armazenamento controlado do projeto quando necessário para auditoria. Qualquer redistribuição futura depende das condições de uso da fonte correspondente.
