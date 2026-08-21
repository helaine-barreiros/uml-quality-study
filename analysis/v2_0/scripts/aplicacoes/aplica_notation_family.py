# -*- coding: utf-8 -*-
"""Acrescenta o campo NotationFamily ao codebook de extracao.

Entra como ordinal 65, o proximo livre: numerar 66 deixaria um buraco no 65 sem
explicacao. Nada renumera, e o gerador da ficha deriva do codebook POR NOME, entao
nenhuma trava nem prosa depende deste numero.

Simula por padrao; escreve so com --apply."""
import csv, sys

CB = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
      'uml-quality-study/analysis/extraction/codebook_extracao.csv')

NOVO = {
    'ordem': '65',
    'secao': 'MAPEAMENTO',
    'faceta': 'Output',
    'campo': 'NotationFamily',
    'tipo': 'fechado',
    'repetivel': 'NAO',
    'grupo_repeticao': '',
    'valores_admitidos': ('UML only; UML with a standard profile; a UML-derived language that '
                          'is not a UML profile; UML alongside a separable non-UML notation; '
                          'unclear'),
    'questoes': 'MQ2',
    'define_subconjunto': '',
    'origem': 'lido',
    'regra_extracao': ('Contra QUE definicao de linguagem a conformidade sintatica foi aferida. '
                       'O portao B5 ja decidiu que existe contribuicao UML separavel e depois '
                       'descarta qual era a outra notacao; este campo guarda o que o portao joga '
                       'fora. Importa ao eixo L: conformidade contra o metamodelo UML nao e '
                       'conformidade contra um perfil, e registrar uma pela outra falsifica o '
                       'eixo que alimenta a SQ4. Exemplos: SysML 1.x e perfil; SysML v2 nao e. '
                       'Nao repetivel porque a lista ja oferece o caso misto.'),
}

antes = list(csv.DictReader(open(CB, encoding='utf-8')))
cols = list(antes[0].keys())
assert len(antes) == 64, 'esperava 64 campos, achei %d' % len(antes)
assert set(NOVO) == set(cols), 'colunas divergem do codebook'
assert NOVO['campo'] not in {x['campo'] for x in antes}, 'nome ja usado'
assert max(int(x['ordem']) for x in antes) == 64
assert NOVO['questoes'] in {q for x in antes for q in x['questoes'].split(';') if q}, \
    'MQ2 tem de ja existir como dono'

depois = antes + [NOVO]
print('campos: %d -> %d' % (len(antes), len(depois)))
print('novo: %s (ordem %s, %s, dono %s)'
      % (NOVO['campo'], NOVO['ordem'], NOVO['tipo'], NOVO['questoes']))
print('valores: %s' % NOVO['valores_admitidos'])

if '--apply' not in sys.argv:
    print('\nSIMULACAO. Rode com --apply para escrever.')
    sys.exit(0)

with open(CB, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(depois)

conf = list(csv.DictReader(open(CB, encoding='utf-8')))
assert len(conf) == 65
assert conf[:64] == antes, 'linha existente foi alterada'
assert conf[64]['campo'] == 'NotationFamily'
print('\nAPLICADO. codebook: %d campos.' % len(conf))
