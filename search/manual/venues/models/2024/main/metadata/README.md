# Metadados

O normalized inventory usa o schema versão 1. O raw inventory é imutável e a membership permanece definida pelo ACM PRIMARY_TOC. O publisher-generated ACM BibTeX é exclusivamente `METADATA_SOURCE`; o matching é por DOI e ele não define membership.

`normalize_acm_bibtex.pl` é determinístico, local e reprodutível. Ele usa `BibTeX::Parser` versão `1.05` (e `Text::CSV` para I/O de CSV), sem acesso à rede. Abstracts e author keywords permanecem em evidência controlada: o CSV público registra a disponibilidade, mas não redistribui seus textos. Nenhuma fonte Crossref ou externa é usada.

O resultado da execução é documentado em [normalization_audit.md](normalization_audit.md).
