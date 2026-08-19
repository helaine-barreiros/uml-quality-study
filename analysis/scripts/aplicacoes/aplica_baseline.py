#!/usr/bin/env python3
"""Passo 5, movimento 2: o campo 26 VIRA BaselineCondition.

Nao entra campo novo, entao nada e renumerado. A metade "dimensoes de qualidade"
sai porque e derivada: os eixos L/D/U dizem quais dimensoes o estudo avaliou, e o
campo 34 particiona o vocabulario por dimensao. A metade "baseline" fica, fechada
e repetivel, porque e a UNICA portadora da entrega 5 (baselines e medidas de
efeito) e um estudo compara contra mais de um baseline.
Muta por NOME, nunca por numero de ordem.
"""
import csv, shutil, datetime, sys

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CB = BASE + '/analysis/extraction/codebook_extracao.csv'
TEX = BASE + '/protocol/appendix_two_layer_mapping_protocol_v1_7.tex'

VELHO = 'Dimensions and baselines'
NOVO = 'BaselineCondition'

VALS = ('no baseline; human-authored model; rule-based or deterministic tool; '
        'another LLM; another version or configuration of the same LLM; '
        'ablation of the generation context; published benchmark or gold standard; other')

REGRA = (
    'Condicao de comparacao contra a qual o estudo avalia a saida do LLM. REPETIVEL: '
    'uma ocorrencia por baseline, porque um estudo compara contra mais de um. '
    '"no baseline" e o estudo que declara nao comparar; NAO_REPORTADO e o estudo que '
    'nao diz — nao colapsar os dois. '
    'A metade "dimensoes de qualidade reportadas" do campo antigo SAIU por ser DERIVADA '
    '(A006 passo 5): os eixos L, D e U dizem quais dimensoes o estudo avaliou, e o campo '
    'NormalizedConstruct particiona o vocabulario nas tres dimensoes. Mante-la seria a '
    'sexta ocorrencia do mesmo objeto especificado duas vezes. '
    'Portador UNICO da entrega 5 da revisao para a tese (baselines e medidas de efeito): '
    'sem este campo nao ha como dizer contra o que a literatura mede.')

LINHA_VELHA = ('Evaluation & Dimensions and baselines & Reported quality dimensions, '
               'comparison conditions, human baseline, rule based baseline, or no baseline \\\\')
LINHA_NOVA = ('Evaluation & BaselineCondition & No baseline; human-authored model; rule based or '
              'deterministic tool; another LLM; another version or configuration of the same LLM; '
              'ablation of the generation context; published benchmark or gold standard; other. '
              'Repeatable. Reported quality dimensions are not recorded here: they are given by the '
              'three axes and by the dimension partition of the normalized construct field. \\\\')

rows = list(csv.DictReader(open(CB, encoding='utf-8')))
cols = list(rows[0].keys())
idx = {r['campo']: r for r in rows}
if NOVO in idx:
    sys.exit('ABORTA: %s ja existe' % NOVO)
if VELHO not in idx:
    sys.exit('ABORTA: %s nao existe' % VELHO)
r26 = idx[VELHO]
if (r26['tipo'], r26['repetivel'], r26['questoes'], r26['valores_admitidos']) != \
        ('composto', 'NAO', 'MQ4', ''):
    sys.exit('ABORTA: campo 26 nao esta no estado esperado: %r' % r26)
ordem_antes = r26['ordem']

tex = open(TEX, encoding='utf-8').read()
n_antes = tex.count('\n')
if tex.count(LINHA_VELHA) != 1:
    sys.exit('ABORTA: a linha do .tex nao aparece exatamente uma vez')

if '--aplica' not in sys.argv:
    print('campo %s: %r -> %r' % (ordem_antes, VELHO, NOVO))
    print('  tipo     composto -> fechado')
    print('  repetivel     NAO -> SIM')
    print('  valores  (vazio) -> %d valores' % len(VALS.split(';')))
    print('  .tex l. do row substituida NO LUGAR, %d linhas antes e depois' % n_antes)
    print('SIMULACAO.')
    sys.exit(0)

hoje = datetime.date.today().isoformat()
shutil.copy(CB, CB + '.bak-baseline-' + hoje)
shutil.copy(TEX, TEX + '.bak-baseline-' + hoje)

r26['campo'] = NOVO
r26['tipo'] = 'fechado'
r26['repetivel'] = 'SIM'
r26['valores_admitidos'] = VALS
r26['regra_extracao'] = REGRA
with open(CB, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

open(TEX, 'w', encoding='utf-8').write(tex.replace(LINHA_VELHA, LINHA_NOVA))

# releitura de verdade
rel = list(csv.DictReader(open(CB, encoding='utf-8')))
ridx = {r['campo']: r for r in rel}
falhas = 0
if len(rel) != 64:
    print('FALHA numero de campos', len(rel)); falhas += 1
if VELHO in ridx:
    print('FALHA: o campo velho sobreviveu'); falhas += 1
n = ridx.get(NOVO)
if not n:
    print('FALHA: o campo novo nao esta la'); falhas += 1
else:
    if n['ordem'] != ordem_antes:
        print('FALHA: a ordem mudou', n['ordem']); falhas += 1
    if (n['tipo'], n['repetivel'], n['questoes'], n['grupo_repeticao']) != \
            ('fechado', 'SIM', 'MQ4', ''):
        print('FALHA: estado inesperado', n); falhas += 1
    if n['valores_admitidos'] != VALS:
        print('FALHA: valores'); falhas += 1
    if 'not reported' in n['valores_admitidos'].lower():
        print('FALHA: "not reported" na lista apagaria a distincao com "no baseline"'); falhas += 1
if [r['ordem'] for r in rel] != [str(i) for i in range(1, 65)]:
    print('FALHA: a ordem 1..64 deixou de ser contigua'); falhas += 1
tex2 = open(TEX, encoding='utf-8').read()
if tex2.count('\n') != n_antes:
    print('FALHA: o .tex mudou de tamanho', tex2.count('\n'), n_antes); falhas += 1
if LINHA_VELHA in tex2 or LINHA_NOVA not in tex2:
    print('FALHA: a substituicao no .tex nao pegou'); falhas += 1
print('campo %s = %s, %d valores, .tex com %d linhas'
      % (ordem_antes, NOVO, len(VALS.split(';')), tex2.count('\n')))
print('FALHAS:', falhas)
