#!/usr/bin/env bash
# Despachante. Cada versao do protocolo tem a sua propria pasta autocontida, com
# .tex, .bib, embrulho de render e verificador:
#
#   protocol/<versao>/appendix_two_layer_mapping_protocol_<versao>.{tex,bib,pdf,html,css}
#   protocol/<versao>/build/protocol_standalone.tex
#   protocol/<versao>/analysis/scripts/{gera_pdf_protocolo.sh,verifica_protocolo.py}
#
# Este arquivo existe para que o comando memorizado continue valendo. Ele so
# encaminha para o script da versao pedida, que e quem de fato renderiza.
#
# Uso: bash analysis/scripts/gera_pdf_protocolo.sh [versao]   (default: v3_0)
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VER="${1:-v3_0}"
VER="${VER#appendix_two_layer_mapping_protocol_}"   # aceita a base antiga como argumento
ALVO="$RAIZ/protocol/$VER/analysis/scripts/gera_pdf_protocolo.sh"
if [ ! -x "$ALVO" ]; then
  echo "ERRO: versao '$VER' nao existe. Disponiveis:" >&2
  ls -1 "$RAIZ/protocol" | grep -E '^v[0-9]' >&2
  exit 1
fi
exec bash "$ALVO"
