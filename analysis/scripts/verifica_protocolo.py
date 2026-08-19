# -*- coding: utf-8 -*-
"""Travas do protocolo. Somente leitura.

A trava LACUNA e a razao de este arquivo existir: MQ5 e SQ5 nao tem subsecao no
Synthesis Plan, e a decisao de 2026-08-19 foi ADIAR as duas para o fim do piloto,
nao esquece-las. A trava afirma IGUALDADE, entao ela quebra dos dois lados: se
aparecer uma terceira lacuna, e se MQ5 ou SQ5 for coberta. Cobrir uma delas
OBRIGA a mexer aqui, e mexer aqui obriga a registrar a decisao.
"""
import os
import re
import sys

BASE = ('/home/helaine-barreiros/Development/doutorado-workspace/'
        'estudo_sistematico/uml-quality-study')
TEX = os.path.join(BASE, 'protocol/appendix_two_layer_mapping_protocol_v1_7.tex')

LINHAS_ESPERADAS = 1870          # A008; era 1862 antes do passo 6
LACUNA_ESPERADA = {'MQ5', 'SQ5'}  # adiadas para o fim do piloto

# Termo do PRODUTO de cada pergunta, tal como a tabela de rastreabilidade
# (l. 134-145) o nomeia, procurado dentro do Synthesis Plan.
MARCADOR = {
    'MQ1': 'publication year by venue',
    'MQ2': 'diagram type by generation task',
    'MQ3': 'model family and version',
    'MQ4': 'baseline and human involvement',
    'MQ5': 'gap analysis',
    'SQ1': 'construct matrix',
    'SQ2': 'Taxonomy of reported UML inadequacies',
    'SQ3': 'Metric and evaluation-reference catalogue',
    'SQ4': 'Syntax-semantic dissonance synthesis',
    'SQ5': 'credibility',
    'SQ6': 'Generation context knowledge synthesis',
    'SQ7': 'Pragmatic adequacy and rework synthesis',
}

falhas = []


def ok(cond, msg):
    print(('  OK    ' if cond else '  FALHA ') + msg)
    if not cond:
        falhas.append(msg)


L = open(TEX, encoding='utf-8').read().splitlines()  # mesma contagem de `wc -l`
TXT = '\n'.join(L)


def secao(nome):
    """Corpo de uma \\section, do titulo ate a proxima \\section."""
    ini = next(i for i, l in enumerate(L) if l.startswith('\\section{%s}' % nome))
    fim = next((i for i in range(ini + 1, len(L)) if L[i].startswith('\\section{')), len(L))
    return '\n'.join(L[ini:fim])


print('== tamanho ==')
ok(len(L) == LINHAS_ESPERADAS,
   'o .tex tem %d linhas (esperado %d; mudar exige chave de traducao e emenda)'
   % (len(L), LINHAS_ESPERADAS))

SP = secao('Synthesis Plan')
subs = re.findall(r'\\subsection\{([^}]*)\}', SP)

print()
print('== passo 6, achado 4: a subsecao fundida foi partida ==')
ok(len(subs) == 8, 'o Synthesis Plan tem %d subsecoes (eram 7)' % len(subs))
ok('Generation context, pragmatic adequacy, and rework synthesis' not in SP,
   'o titulo FUNDIDO de SQ6 com SQ7 nao voltou')
for t in ('Generation context knowledge synthesis', 'Pragmatic adequacy and rework synthesis'):
    ok(subs.count(t) == 1, 'existe exatamente uma subsecao "%s"' % t)
i6 = SP.index('\\subsection{Generation context knowledge synthesis}')
i7 = SP.index('\\subsection{Pragmatic adequacy and rework synthesis}')
ok('whole eligible corpus' in SP[i6:i7],
   'a subsecao da SQ6 declara o proprio denominador: corpus inteiro')
ok('axis U is not absent' in SP[i7:],
   'a subsecao da SQ7 declara o proprio denominador: eixo U nao-ausente')

print()
print('== passo 6, achado 1: unitizacao antes de classificacao ==')
CR = TXT[TXT.index('\\subsection{Coding reliability}'):TXT.index('\\section{Synthesis Plan}')]
ok('unitization' in CR, 'a unitizacao e nomeada')
ok('reconciled by discussion and adjudication before classification begins' in CR,
   'a lista enumerada e reconciliada ANTES de classificar')
ok(CR.index('unitization') < CR.index('Cohen kappa'),
   'a regra de unidade vem ANTES do coeficiente, nao depois')
ok('never absorbed into a coefficient' in CR,
   'o desacordo de enumeracao e reportado a parte, nao dissolvido no coeficiente')

print()
print('== passo 6, achado 5: o bullet nao aponta mais para o campo 26 velho ==')
ok('evaluation dimension by diagram type' not in SP,
   'o bullet do campo 26 fundido (removido pela A007) nao sobreviveu')
ok('as given by the three evidence axes' in SP,
   'a dimensao de qualidade e ancorada nos eixos e no construto normalizado')

print()
print('== LACUNA: perguntas sem subsecao no Synthesis Plan ==')
sem = {q for q, m in MARCADOR.items() if m.lower() not in SP.lower()}
print('       sem subsecao: %s' % (sorted(sem) or 'nenhuma'))
ok(sem == LACUNA_ESPERADA,
   'as lacunas sao EXATAMENTE %s. Quebrar aqui e o ponto: cobrir MQ5 ou SQ5 '
   'obriga a atualizar esta trava e a registrar a decisao'
   % sorted(LACUNA_ESPERADA))

print()
print('FALHAS: %d' % len(falhas))
for f in falhas:
    print(' -', f)
sys.exit(1 if falhas else 0)
