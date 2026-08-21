# Extração do PRIMARY_TOC

`extract_acm_proceedings_toc.pl` extrai a ordem documental de um HTML salvo da página oficial ACM de proceedings. O parser usa apenas a estrutura genérica da página (`issue-downloads__item` e `issue-item-container`); ele não contém títulos, autores, DOI ou regras de relevância.

Dependências: Perl e os módulos `Getopt::Long`, `Encode` e `HTML::TreeBuilder`. O HTML de entrada é mantido em armazenamento controlado e não é versionado neste repositório. A execução deve registrar no manifest o caminho controlado, quando permitido, ou seu SHA-256 e o método de extração.
