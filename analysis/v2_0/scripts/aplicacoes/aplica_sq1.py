#!/usr/bin/env python3
# A006 secao 4 (SQ1): vocabulario unico no campo 34 e denominador de SQ1-SQ3.
# Muta SEMPRE por NOME de campo, nunca por numero de ordem.
import csv, shutil, datetime, sys

CB = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/analysis/extraction/codebook_extracao.csv'

VOCAB = ('textual validity; rendering validity; PlantUML parseability; '
         'UML syntactic conformity; metamodel conformance; well-formedness; '
         'notation-level validity; semantic correctness; semantic completeness; '
         'requirements coverage; domain fidelity; consistency; '
         'consistency with source requirements; omitted element; '
         'unsupported addition; incorrect relation; incorrect actor; '
         'incorrect behavior; pragmatic adequacy; understandability; readability; '
         'clarity; correction effort; inspection effort; other')

REGRA = ('So preencher DEPOIS de registrado o termo nativo. VOCABULARIO UNICO: '
         'SyntacticQualityConstruct e SemanticQualityConstruct sao as projecoes '
         'sintatica e semantica deste campo e nao admitem valor ausente daqui.')

ANTES = {
    'Normalized construct': {
        'valores_admitidos': ('textual validity; UML conformity; semantic correctness; '
                              'semantic completeness; consistency; pragmatic adequacy; '
                              'understandability; readability; clarity; other'),
        'regra_extracao': 'So preencher DEPOIS de registrado o termo nativo.',
    },
    'QualityAxisD': {'define_subconjunto': 'SQ1;SQ2;SQ3;SQ4'},
}
DEPOIS = {
    'Normalized construct': {'valores_admitidos': VOCAB, 'regra_extracao': REGRA},
    'QualityAxisD': {'define_subconjunto': 'SQ4'},
}

rows = list(csv.DictReader(open(CB, encoding='utf-8')))
cols = list(rows[0].keys())
idx = {r['campo']: r for r in rows}

for campo, esperado in ANTES.items():
    if campo not in idx:
        sys.exit('ABORTA: campo ausente ' + campo)
    for k, v in esperado.items():
        if idx[campo][k] != v:
            sys.exit('ABORTA: %s.%s inesperado:\n  %r' % (campo, k, idx[campo][k]))

if '--aplica' not in sys.argv:
    for campo, novo in DEPOIS.items():
        for k, v in novo.items():
            print('%s.%s\n  antes : %s\n  depois: %s\n' % (campo, k, idx[campo][k], v))
    sys.exit(0)

shutil.copy(CB, CB + '.bak-' + datetime.date.today().isoformat())
for campo, novo in DEPOIS.items():
    idx[campo].update(novo)
with open(CB, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# releitura de verdade
rel = {r['campo']: r for r in csv.DictReader(open(CB, encoding='utf-8'))}
falhas = 0
for campo, novo in DEPOIS.items():
    for k, v in novo.items():
        if rel[campo][k] != v:
            print('FALHA', campo, k); falhas += 1
# nenhuma projecao pode ter valor fora do vocabulario
uni = {v.strip() for v in VOCAB.split(';')}
for proj in ('SyntacticQualityConstruct', 'SemanticQualityConstruct'):
    for v in rel[proj]['valores_admitidos'].split(';'):
        v = v.strip()
        if v and v not in uni and v != 'not reported':
            print('FALHA projecao fora do vocabulario:', proj, repr(v)); falhas += 1
print('FALHAS:', falhas)
