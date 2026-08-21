# -*- coding: utf-8 -*-
"""C1 do 018_ACM: ELEGIVEL. Primeira decisao do piloto de extracao."""
import csv, sys, shutil, datetime

CSV = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/custom_automated_search_collection.csv')
BKP = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/backups/'
       'custom_automated_search_collection_%s_pre-c1-018.csv'
       % datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

r = list(csv.DictReader(open(CSV, encoding='utf-8')))
cols = list(r[0].keys())
alvo = [x for x in r if x['logical_id'] == '018_ACM']
assert len(alvo) == 1
v = alvo[0]
assert v['excluded'] != 'true' and v['gate_b_outcome'] == 'PASSOU'
assert v['pdf_status'] == 'OK_ACERVO_LOCAL'
assert v['gate_c_outcome'] == '', 'o C1 do 018 ja estava decidido: %r' % v['gate_c_outcome']

print('018_ACM: gate_c_outcome %r -> %r' % (v['gate_c_outcome'], 'ELEGIVEL'))
antes = sum(1 for x in r if x['excluded'] != 'true'
            and x['pdf_status'].startswith('OK_') and x['gate_c_outcome'])
print('com C1 decidido: %d -> %d (de 58 com texto)' % (antes, antes + 1))

if '--apply' not in sys.argv:
    print('\nSIMULACAO. Rode com --apply para escrever.')
    sys.exit(0)

shutil.copy(CSV, BKP)
v['gate_c_outcome'] = 'ELEGIVEL'
with open(CSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(r)

d = {x['logical_id']: x for x in csv.DictReader(open(CSV, encoding='utf-8'))}
assert d['018_ACM']['gate_c_outcome'] == 'ELEGIVEL'
assert d['018_ACM']['exclusion_criteria'] == '' and d['018_ACM']['excluded'] != 'true'
assert len(d) == 986
print('\nAPLICADO. backup em %s' % BKP.rsplit('/', 1)[-1])
