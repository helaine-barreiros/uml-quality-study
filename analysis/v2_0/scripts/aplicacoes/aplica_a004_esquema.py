# -*- coding: utf-8 -*-
"""Aplica o esquema da emenda A004 ao CSV mestre.

Fonte normativa: protocol/screening_manual_v2.md, secoes 5 (atributos do Portao B),
7.1 (registro por portao) e 9 (o que o Portao C classifica sem excluir).

Colunas criadas
  dedup_outcome          secao 7.1  UNICO | D_E3
  attr_saida             secao 5    B1 e B5
  attr_tarefa            secao 5    B2
  attr_entrada           secao 5    B3
  attr_modelo            secao 5    B4
  eixo_L                 secao 9    ausente | validade_textual | conformidade_uml
  eixo_D                 secao 9    ausente | alegada | requisitos_fonte |
                                    modelo_referencia | julgamento_especialista | rubrica
  eixo_U                 secao 9    ausente | alegada | compreensao |
                                    atividade_engenharia | retrabalho
  atribuicao_resultado   secao 9    atribuivel_ao_uml | agregado_com_outros_artefatos |
                                    nao_reportado

gate_c_outcome ja existia desde 2026-08-17.

Preenchimento
  Apenas dedup_outcome e derivavel do que ja esta registrado. Todo o resto nasce
  vazio, porque vazio significa "nao triado / nao extraido" e inventar valor aqui
  seria fabricar dado.
"""
import csv, os, collections

CSV = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/custom_automated_search_collection.csv')

NOVAS_ANTES_DE = [
    ('dedup_outcome', 'gate_a_outcome'),
    ('attr_saida', 'gate_c_outcome'),
    ('attr_tarefa', 'gate_c_outcome'),
    ('attr_entrada', 'gate_c_outcome'),
    ('attr_modelo', 'gate_c_outcome'),
]
NOVAS_NO_FIM = ['eixo_L', 'eixo_D', 'eixo_U', 'atribuicao_resultado']


def main(apply=False):
    with open(CSV, encoding='utf-8') as fh:
        rd = csv.DictReader(fh)
        campos = list(rd.fieldnames)
        linhas = list(rd)

    criadas = []
    for nome, ancora in NOVAS_ANTES_DE:
        if nome not in campos:
            campos.insert(campos.index(ancora), nome)
            criadas.append(nome)
    for nome in NOVAS_NO_FIM:
        if nome not in campos:
            campos.append(nome)
            criadas.append(nome)

    for x in linhas:
        for nome in criadas:
            x[nome] = ''

    # dedup_outcome: unico campo derivavel sem julgamento.
    # D_E3 <=> a exclusao por duplicata foi decidida NO PRE-PASSE D, o que no
    # esquema antigo se registrava como gate_a_outcome == 'A4_E3'.
    # Os membros de familia descobertos no texto completo (868, 877, 963, 623,
    # 842, 051) receberam E3 no PORTAO C e passaram o pre-passe D como unicos:
    # para eles UNICO e o registro correto do que o pre-passe produziu, e o E3
    # vive em exclusion_criteria e em gate_c_notes.
    cont = collections.Counter()
    for x in linhas:
        v = 'D_E3' if x['gate_a_outcome'] == 'A4_E3' else 'UNICO'
        x['dedup_outcome'] = v
        cont[v] += 1

    print('colunas criadas:', ', '.join(criadas) if criadas else '(nenhuma)')
    print('total de colunas:', len(campos))
    print('dedup_outcome:', dict(cont))

    tardios = [x['logical_id'] for x in linhas
               if x['exclusion_criteria'] == 'E3' and x['dedup_outcome'] == 'UNICO']
    print('E3 com dedup_outcome=UNICO (familia decidida no Portao C):', tardios)

    if apply:
        tmp = CSV + '.tmp'
        with open(tmp, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=campos)
            w.writeheader()
            w.writerows(linhas)
        os.replace(tmp, CSV)
        print('APLICADO.')
    else:
        print('SIMULACAO.')


if __name__ == '__main__':
    import sys
    main(apply='--apply' in sys.argv)
