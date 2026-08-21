#!/usr/bin/env bash
# Renderiza ESTA versao do protocolo em PDF e HTML, a partir do proprio .tex.
# O .tex e um APENDICE (comeca em \chapter), entao a renderizacao usa o embrulho
# ../../build/protocol_standalone.tex, que so reproduz o preambulo declarado no
# topo do apendice e o inclui com \input. Nada do protocolo e alterado para gerar.
set -euo pipefail
VER="v1_7"
BASE="appendix_two_layer_mapping_protocol_$VER"
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"   # protocol/$VER
cd "$RAIZ/build"
latexmk -pdf -interaction=nonstopmode -halt-on-error protocol_standalone.tex >/dev/null
# Falha ruidosa: referencia ou citacao nao resolvida invalida o artefato.
# Conferido AQUI porque o make4ht sobrescreve o .log com o dele.
if grep -qE "Undefined control sequence|Warning: Citation|Warning: Reference" protocol_standalone.log; then
  echo "ERRO: referencia ou citacao nao resolvida. Ver $RAIZ/build/protocol_standalone.log" >&2
  grep -nE "Undefined control sequence|Warning: Citation|Warning: Reference" protocol_standalone.log >&2
  exit 1
fi
PAGS=$(grep -oP 'Output written on protocol_standalone\.pdf \(\K[0-9]+' protocol_standalone.log | tail -1)
make4ht -u -m draft protocol_standalone.tex "0,fn-in" >/dev/null 2>&1
cp protocol_standalone.pdf "$RAIZ/$BASE.pdf"
cp protocol_standalone.css "$RAIZ/$BASE.css"
sed 's/protocol_standalone\.css/'"$BASE"'.css/g' protocol_standalone.html > "$RAIZ/$BASE.html"
echo "OK  $VER  $(wc -l < "$RAIZ/$BASE.tex") linhas  ->  $PAGS paginas"
echo "    $RAIZ/$BASE.pdf"
