#!/usr/bin/env bash
# Renderiza o protocolo em PDF e em HTML a partir do proprio .tex, sem editar o .tex.
#
# O .tex e um APENDICE (comeca em \chapter, nao tem \documentclass), entao a
# renderizacao usa o embrulho protocol/build/protocol_standalone.tex, que so
# reproduz o preambulo declarado nas linhas 1-4 do proprio apendice e o inclui
# com \input. Nada do protocolo e alterado para gerar a saida.
#
# Uso: bash analysis/scripts/gera_pdf_protocolo.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROTO="$RAIZ/protocol"
BUILD="$PROTO/build"
BASE="appendix_two_layer_mapping_protocol_v1_7"

cd "$BUILD"

latexmk -pdf -interaction=nonstopmode -halt-on-error protocol_standalone.tex >/dev/null

# Falha ruidosa: referencia ou citacao nao resolvida invalida o artefato.
# Tem de ser conferido AQUI: o make4ht sobrescreve o .log com o log dele.
if grep -qE "Undefined control sequence|Warning: Citation|Warning: Reference" protocol_standalone.log; then
  echo "ERRO: referencia ou citacao nao resolvida. Ver $BUILD/protocol_standalone.log" >&2
  grep -nE "Undefined control sequence|Warning: Citation|Warning: Reference" protocol_standalone.log >&2
  exit 1
fi
PAGS=$(grep -oP 'Output written on protocol_standalone\.pdf \(\K[0-9]+' protocol_standalone.log | tail -1)

make4ht -u -m draft protocol_standalone.tex "0,fn-in" >/dev/null 2>&1

cp protocol_standalone.pdf "$PROTO/$BASE.pdf"
cp protocol_standalone.css "$PROTO/$BASE.css"
sed 's/protocol_standalone\.css/'"$BASE"'.css/g' protocol_standalone.html > "$PROTO/$BASE.html"

LINHAS=$(wc -l < "$PROTO/$BASE.tex")
echo "OK  $LINHAS linhas do .tex  ->  $PAGS paginas"
echo "    $PROTO/$BASE.pdf"
echo "    $PROTO/$BASE.html"
