#!/usr/bin/env python3
# A006 secao 6 (eixo L): regra de projecao e de escada no campo 28, mais duas
# celulas de prosa velha nos campos 29 e 30. Muta por NOME, nunca por numero.
import csv, shutil, datetime, sys

CB = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/analysis/extraction/codebook_extracao.csv'

R28 = ('Relacao modelo-linguagem (Krogstie). Espelha a coluna eixo_L do CSV mestre. '
       'Nunca colapsar L, D e U numa escala unica. Campo INSTRUMENTO da revisao: nao e '
       'dado de resposta de pergunta nenhuma, e por isso a coluna questoes fica vazia. '
       'Define o subconjunto da SQ4 junto com o eixo D. '
       'PROJECAO do campo SyntacticQualityConstruct sobre dois NIVEIS (l. 182-183 e '
       'l. 1360): textual validity, rendering validity, PlantUML parseability e '
       'notation-level validity -> "textual validity"; UML syntactic conformity, '
       'metamodel conformance e well-formedness -> "UML conformity". Rodada de '
       'renderizador ou de parser NAO e "absent". '
       'ESCADA: o eixo carrega UM valor por estudo e o construto e repetivel, entao o '
       'eixo registra o NIVEL MAIS EXIGENTE avaliado — afirma o que foi avaliado, nao '
       'que um nivel implica o outro; o inventario fica no campo do construto.')

R29 = ('Relacao modelo-dominio. Espelha eixo_D. Define o subconjunto da SQ4 junto com o '
       'eixo L. A006 secao 4: SQ1 a SQ3 foram para o CORPUS INTEIRO e este eixo NAO as '
       'condiciona mais. Campo INSTRUMENTO da revisao: nao e dado de resposta de '
       'pergunta nenhuma, e por isso a coluna questoes fica vazia.')

R30 = ('Relacao modelo-interprete e uso. Espelha eixo_U. Define o subconjunto da SQ7 '
       '(era da SQ6 antes da divisao da A006 secao 10). Campo INSTRUMENTO da revisao: '
       'nao e dado de resposta de pergunta nenhuma, e por isso a coluna questoes fica '
       'vazia.')

ANTES = {
    'QualityAxisL': 'Relacao modelo-linguagem (Krogstie). Espelha a coluna eixo_L do CSV mestre. Nunca colapsar L, D e U numa escala unica. Campo INSTRUMENTO da revisao: nao e dado de resposta de pergunta nenhuma, e por isso a coluna questoes fica vazia.',
    'QualityAxisD': 'Relacao modelo-dominio. Espelha eixo_D. Define os subconjuntos de SQ1 a SQ3. Campo INSTRUMENTO da revisao: nao e dado de resposta de pergunta nenhuma, e por isso a coluna questoes fica vazia.',
    'QualityAxisU': 'Relacao modelo-interprete e uso. Espelha eixo_U. Define o subconjunto da SQ6. Campo INSTRUMENTO da revisao: nao e dado de resposta de pergunta nenhuma, e por isso a coluna questoes fica vazia.',
}
DEPOIS = {'QualityAxisL': R28, 'QualityAxisD': R29, 'QualityAxisU': R30}

rows = list(csv.DictReader(open(CB, encoding='utf-8')))
cols = list(rows[0].keys())
idx = {r['campo']: r for r in rows}

for campo, v in ANTES.items():
    if idx[campo]['regra_extracao'] != v:
        sys.exit('ABORTA: %s.regra_extracao inesperada:\n  %r' % (campo, idx[campo]['regra_extracao']))
    if idx[campo]['valores_admitidos'].count(';') < 1:
        sys.exit('ABORTA: %s sem valores' % campo)

# o eixo L nao ganha valor novo: a rejeicao do movimento 1 e verificavel aqui
if idx['QualityAxisL']['valores_admitidos'] != 'absent; textual validity; UML conformity':
    sys.exit('ABORTA: o eixo L nao deve mudar de valores')

if '--aplica' not in sys.argv:
    for campo, v in DEPOIS.items():
        print('%s.regra_extracao\n  antes : %s\n  depois: %s\n' % (campo, ANTES[campo], v))
    sys.exit(0)

shutil.copy(CB, CB + '.bak-eixoL-' + datetime.date.today().isoformat())
for campo, v in DEPOIS.items():
    idx[campo]['regra_extracao'] = v
with open(CB, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

rel = {r['campo']: r for r in csv.DictReader(open(CB, encoding='utf-8'))}
falhas = 0
for campo, v in DEPOIS.items():
    if rel[campo]['regra_extracao'] != v:
        print('FALHA', campo); falhas += 1
if rel['QualityAxisL']['valores_admitidos'] != 'absent; textual validity; UML conformity':
    print('FALHA: o eixo L mudou de valores'); falhas += 1
# a projecao tem de cobrir os 7 valores substantivos do campo 37
sint = [v.strip() for v in rel['SyntacticQualityConstruct']['valores_admitidos'].split(';')]
subs = [v for v in sint if v not in ('other', 'not reported')]
regra = rel['QualityAxisL']['regra_extracao'].lower()
for v in subs:
    if v.lower() not in regra:
        print('FALHA projecao nao cobre:', v); falhas += 1
print('valores substantivos do campo 37 cobertos pela projecao:', len(subs))
print('FALHAS:', falhas)
