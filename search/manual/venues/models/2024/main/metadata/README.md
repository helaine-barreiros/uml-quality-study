# Metadados

O normalized inventory usa o schema versão 1. O raw inventory é imutável e a membership permanece definida pelo ACM PRIMARY_TOC. O publisher-generated ACM BibTeX é exclusivamente `METADATA_SOURCE`; o matching é por DOI e ele não define membership.

`normalize_acm_bibtex.pl` é determinístico, local e reprodutível. Ele usa `BibTeX::Parser` e `Text::CSV`, sem acesso à rede. Hashes são calculados e verificados em runtime contra o source manifest; as versões dos módulos são obtidas dinamicamente; `parse_ok` é obrigatório para cada entrada BibTeX; o CSV gerado é relido e validado; e o raw inventory é verificado por SHA-256 antes e depois. Abstracts e author keywords permanecem em evidência controlada: o CSV público registra a disponibilidade, mas não redistribui seus textos. Nenhuma fonte Crossref ou externa é usada.

Para `Series`, o normalizador usa `field()` seguido de normalização NFC e whitespace. Esta exceção técnica preserva a aspa ASCII literalmente fornecida pelo publisher (`MODELS '24`): nesta biblioteca, `cleaned_field('series')` a converteria para uma aspa tipográfica, sem decodificação TeX necessária.

O resultado da execução é documentado em [normalization_audit.md](normalization_audit.md).
