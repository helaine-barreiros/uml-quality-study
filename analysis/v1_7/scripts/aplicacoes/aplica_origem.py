#!/usr/bin/env python3
"""Passo 5, movimento 1: coluna `origem` no codebook e `procedencia` no extracao.csv.

Nenhum campo e removido. Oito deixam de ser BUSCA no artigo: quatro sao
conferencia de dado ja registrado e quatro sao funcao de outro campo.
Muta por NOME, nunca por numero de ordem.
"""
import csv, shutil, datetime, sys

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CB = BASE + '/analysis/extraction/codebook_extracao.csv'
EX = BASE + '/analysis/extraction/extracao.csv'

CONFERIDO = {
    'Year, venue, publication type, status':
        'CONFERIDO, nao buscado: PY, T2, TY e M3 do CSV mestre (fill rate nos 57 com '
        'texto: PY/T2/TY 57/57, M3 48/57).',
    'Authors and affiliations':
        'CONFERIDO, nao buscado: AU, AD e C1 do CSV mestre (AU 57/57, AD 50/57, C1 3/57 '
        '— so o C1 exige leitura).',
    'SubstantiveLLMUseDecision':
        'CONFERIDO: e a decisao do Portao B, ja registrada em gate_b_outcome, 57/57.',
    'BoundaryDecisionRationale':
        'CONFERIDO: ja registrado em gate_b_notes, 57/57.',
}

DERIVADO = {
    'PlantUMLGenerated':
        'DERIVADO de OutputRepresentation: "PlantUML code" -> yes; outra representacao '
        'explicita -> no; "mixed representation" ou "unclear" -> decidir a mao.',
    'SyntacticEvidenceAvailable':
        'DERIVADO do eixo L: diferente de absent -> yes; absent -> no. "unclear" e o '
        'UNICO valor que o extrator poe a mao.',
    'SemanticEvidenceAvailable':
        'DERIVADO do eixo D: diferente de absent -> yes; absent -> no. "unclear" e o '
        'UNICO valor que o extrator poe a mao.',
    'CorrectionOrReworkEvidence':
        'DERIVADO: alguma Correction measure registrada, ou eixo U = rework -> yes; '
        'nenhuma das duas -> no. "unclear" e o unico valor posto a mao.',
}

rows = list(csv.DictReader(open(CB, encoding='utf-8')))
cols = list(rows[0].keys())
if 'origem' in cols:
    sys.exit('ABORTA: a coluna origem ja existe')
idx = {r['campo']: r for r in rows}
for campo in list(CONFERIDO) + list(DERIVADO):
    if campo not in idx:
        sys.exit('ABORTA: campo ausente no codebook: ' + campo)

if '--aplica' not in sys.argv:
    print('coluna origem: conferido %d, derivado %d, lido %d'
          % (len(CONFERIDO), len(DERIVADO), len(rows) - len(CONFERIDO) - len(DERIVADO)))
    for campo, t in list(CONFERIDO.items()) + list(DERIVADO.items()):
        print(' %2s %-34s %s' % (idx[campo]['ordem'], campo, t[:60]))
    print('extracao.csv: cabecalho ganha "procedencia"')
    print('SIMULACAO.')
    sys.exit(0)

hoje = datetime.date.today().isoformat()
shutil.copy(CB, CB + '.bak-origem-' + hoje)
shutil.copy(EX, EX + '.bak-origem-' + hoje)

cols.insert(cols.index('regra_extracao'), 'origem')
for r in rows:
    campo = r['campo']
    if campo in CONFERIDO:
        r['origem'] = 'conferido'
        extra = CONFERIDO[campo]
    elif campo in DERIVADO:
        r['origem'] = 'derivado'
        extra = DERIVADO[campo]
    else:
        r['origem'] = 'lido'
        extra = ''
    if extra:
        r['regra_extracao'] = (r['regra_extracao'] + ' ' + extra).strip()
with open(CB, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

cab = next(csv.reader(open(EX, encoding='utf-8')))
resto = list(csv.reader(open(EX, encoding='utf-8')))[1:]
if 'procedencia' not in cab:
    cab.append('procedencia')
with open(EX, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(cab)
    w.writerows(resto)

# releitura de verdade
rel = list(csv.DictReader(open(CB, encoding='utf-8')))
falhas = 0
cont = {'lido': 0, 'conferido': 0, 'derivado': 0}
for r in rel:
    if r['origem'] not in cont:
        print('FALHA origem invalida', r['campo'], repr(r['origem'])); falhas += 1
    else:
        cont[r['origem']] += 1
    if r['campo'] in DERIVADO and 'DERIVADO' not in r['regra_extracao']:
        print('FALHA regra sem derivacao', r['campo']); falhas += 1
    if r['campo'] in CONFERIDO and 'CONFERIDO' not in r['regra_extracao']:
        print('FALHA regra sem conferencia', r['campo']); falhas += 1
if len(rel) != 64:
    print('FALHA numero de campos', len(rel)); falhas += 1
cab2 = next(csv.reader(open(EX, encoding='utf-8')))
if cab2[-1] != 'procedencia' or len(cab2) != 12:
    print('FALHA cabecalho de extracao.csv', cab2); falhas += 1
print(cont, '| cabecalho extracao.csv:', len(cab2), 'colunas')
print('FALHAS:', falhas)
