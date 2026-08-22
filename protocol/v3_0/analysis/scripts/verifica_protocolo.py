# -*- coding: utf-8 -*-
"""Travas do protocolo v3.0. Somente leitura.

Nao substitui verifica_protocolo_v2.py, que continua verificando a v2.0. As travas
sao especificas de versao porque afirmam o conteudo, nao a forma.

Quatro travas novas nasceram de falhas reais encontradas em 2026-08-21:

  POLO      SQ1 guarda atributo, SQ2 guarda desvio, e os dois vocabularios nao
            compartilham rotulo. `unsupported addition` estava nos dois.
  POSSE     todo objeto nomeado no texto de uma pergunta tem campo com aquele dono
            no codebook. A MQ4 pedia cinco objetos e possuia um.
  TITULO    o titulo tem fonte unica. Existiam tres strings divergentes.
  PORTAO_C  o unico codigo de exclusao do Portao C e o E12, e o adiamento de um
            filtro nao o move de portao.
"""
import csv
import io
import os
import re
import sys

BASE = ('/home/helaine-barreiros/Development/doutorado-workspace/'
        'estudo_sistematico/uml-quality-study')
TEX = os.path.join(BASE, 'protocol/v3_0/appendix_two_layer_mapping_protocol_v3_0.tex')
CODEBOOK = os.path.join(BASE, 'analysis/v3_0/extraction/codebook_extracao.csv')

LINHAS_ESPERADAS = 1230
LACUNA_ESPERADA = {'MQ5', 'SQ5'}

MARCADOR = {
    'MQ1': 'publication year by venue',
    'MQ2': 'diagram type by generation task',
    'MQ3': 'model family and version',
    'MQ4': 'baseline',
    'MQ5': 'gap analysis',
    'SQ1': 'construct matrix',
    'SQ2': 'Taxonomy of reported UML inadequacies',
    'SQ3': 'Measure and evaluation-reference catalogue',
    'SQ4': 'Syntax-semantic dissonance synthesis',
    'SQ5': 'credibility',
    'SQ6': 'Generation context knowledge synthesis',
    'SQ7': 'Pragmatic adequacy and rework synthesis',
}

# Objeto nomeado no texto de uma pergunta -> campo do codebook que o carrega.
# So entram os objetos que JA custaram um erro; a trava cresce quando outro custar.
POSSE = {
    'MQ1': ['Year, venue, publication type, status', 'Data, prompts, code, models, and replication package'],
    'MQ4': ['BaselineCondition'],
    'SQ2': ['Violated reference', 'UML carrier', 'Normalized discrepancy operation'],
    'SQ3': ['EvaluationReference', 'AutomatedEvaluatorTool', 'Unit of assessment'],
    'SQ5': ['HumanEvaluatorRole'],
}

falhas = []


def ok(cond, msg):
    print(('  OK    ' if cond else '  FALHA ') + msg)
    if not cond:
        falhas.append(msg)


L = io.open(TEX, encoding='utf-8').read().splitlines()
TXT = '\n'.join(L)
CB = {r['campo']: r for r in csv.DictReader(io.open(CODEBOOK, encoding='utf-8'))}


def secao(nome):
    ini = next(i for i, l in enumerate(L) if l.startswith('\\section{%s}' % nome))
    fim = next((i for i in range(ini + 1, len(L)) if L[i].startswith('\\section{')), len(L))
    return '\n'.join(L[ini:fim])


def pergunta(codigo):
    m = re.search(r'\\item\[%s\.\](.*)' % codigo, TXT)
    return m.group(1) if m else ''


print('== tamanho ==')
ok(len(L) == LINHAS_ESPERADAS,
   'o .tex tem %d linhas (esperado %d)' % (len(L), LINHAS_ESPERADAS))

print()
print('== TITULO: fonte unica ==')
ok(TXT.count('\\newcommand{\\reviewtitle}') == 1, 'a macro reviewtitle e definida uma vez')
ok('\\chapter{Protocol for the systematic mapping study on \\reviewtitle}' in TXT,
   'o \\chapter deriva da macro em vez de repetir o titulo')
ok('Review title & \\reviewtitle: a systematic mapping study' in TXT,
   'a tabela de identificacao deriva da macro')
ok('Systematic Mapping Study on Quality of LLM Generated UML Diagrams' not in TXT,
   'o titulo antigo, em Title Case e com o objeto repetido, nao sobreviveu')

ok('Table~\\ref{tab:protocol_reviewers}' in TXT.split('\\section{Rationale')[0],
   'a tabela de identificacao aponta para a tabela de papeis em vez de repetir as pessoas')
ok('Methodological supervisor & \\protocolfield' not in TXT,
   'nao ha placeholder de pessoa: quem sao os pesquisadores esta escrito num lugar so')

print()
print('== POLO: SQ1 guarda atributo, SQ2 guarda desvio ==')
atr = set(v.strip().lower() for v in CB['Normalized construct']['valores_admitidos'].split(';'))
dsv = set(v.strip().lower() for v in CB['Normalized discrepancy operation']['valores_admitidos'].split(';'))
proj = set(v.strip().lower() for v in CB['SemanticQualityConstruct']['valores_admitidos'].split(';'))
ok(not (atr & dsv), 'nenhum rotulo compartilhado entre os dois polos (%s)' % (sorted(atr & dsv) or 'vazio'))
ok(not (proj - atr - {'other', 'not reported'}),
   'SemanticQualityConstruct nao admite valor ausente do construto normalizado')
ok('sec:protocol_attribute_deviation_measure' in TXT, 'a subsecao da espinha existe e e referenciavel')
ok('attribute} \\rightarrow \\text{deviation' in TXT, 'a espinha declara os dois primeiros elos')

print()
print('== POSSE: todo objeto do texto de uma pergunta tem campo daquele dono ==')
for q, campos in sorted(POSSE.items()):
    for c in campos:
        dono = CB.get(c, {}).get('questoes', '<campo inexistente>')
        ok(dono == q, '%s possui o campo "%s" (dono declarado: %s)' % (q, c, dono or 'vazio'))
ok('evaluation dimensions' not in pergunta('MQ4'),
   'a MQ4 nao pede mais "evaluation dimensions", que a A007 removeu e nenhum campo carrega')
ok('human roles' not in pergunta('MQ4'), 'a MQ4 nao pede mais o avaliador humano, que e da SQ5')
ok('open science' not in pergunta('MQ4'), 'a MQ4 nao pede mais artefato aberto, que e da MQ1')
ok('violated reference' in pergunta('SQ2').lower(),
   'a SQ2 pede a referencia violada, que e o campo onde a dissonancia se torna observavel')
ok('evaluators' not in pergunta('SQ3'), 'a SQ3 nao pede mais o avaliador humano, que e da SQ5')

print()
print('== PORTAO C: E12 e a unica saida, e adiar filtro nao muda de portao ==')
SEL = secao('Study selection process')
ok('C1 is the only exclusion available at Gate C' in SEL, 'a regra do Portao C esta escrita')
ok('A deferred filter remains a filter of its own gate' in TXT,
   'o filtro adiado continua sendo do proprio portao')
ok('recording the primary exclusion criterion and the gate outcome at the filter that owns' in SEL,
   'a triagem de texto completo grava o codigo no filtro que o possui')
ok('reached only by reports that passed Gate B' in SEL,
   'o C1 so e alcancado por quem passou o Portao B')
for c in ('E5', 'E10', 'E11'):
    ok(not re.search(r'\b%s\b' % c, TXT), 'o codigo retirado %s nao reapareceu' % c)

print()
print('== estrutura da sintese (herdado da v1.7) ==')
SP = secao('Synthesis plan')
subs = re.findall(r'\\subsection\{([^}]*)\}', SP)
ok(len(subs) == 8, 'o Synthesis plan tem %d subsecoes (esperado 8)' % len(subs))
ok('Generation context, pragmatic adequacy, and rework synthesis' not in SP,
   'o titulo FUNDIDO de SQ6 com SQ7 nao voltou')
CR = TXT[TXT.index('\\subsection{Coding reliability}'):TXT.index('\\section{Synthesis plan}')]
ok('unitization' in CR and CR.index('unitization') < CR.index('Cohen kappa'),
   'a regra de unidade vem ANTES do coeficiente')
ok('never absorbed into a coefficient' in CR,
   'o desacordo de enumeracao e reportado a parte')

print()
print('== LACUNA: perguntas sem subsecao no Synthesis plan ==')
sem = {q for q, m in MARCADOR.items() if m.lower() not in SP.lower()}
print('       sem subsecao: %s' % (sorted(sem) or 'nenhuma'))
ok(sem == LACUNA_ESPERADA,
   'as lacunas sao EXATAMENTE %s' % sorted(LACUNA_ESPERADA))

print()
print('FALHAS: %d' % len(falhas))
for f in falhas:
    print(' -', f)
sys.exit(1 if falhas else 0)
