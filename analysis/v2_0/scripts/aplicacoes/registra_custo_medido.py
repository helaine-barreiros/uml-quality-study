# -*- coding: utf-8 -*-
"""Uma linha: campo de custo de geracao MEDIDO e NAO incluido."""
import csv, sys

LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')

r1 = [
    'GLOBAL',
    '2026-08-20T20:10:00-03:00',
    'HB',
    'DECISAO_DESENHO',
    '',
    '',
    '',
    'CUSTO DE GERACAO: campo MEDIDO e NAO INCLUIDO no codebook. '
    'METODO: a comparacao do instrumento de extracao contra tres estudos secundarios '
    'proximos mostrou que nenhum dos 64 campos registra o custo de PRODUZIR a saida; o '
    'campo 60 Correction measure registra o custo de CORRIGI-LA, que e outra coisa. Em vez '
    'de decidir por plausibilidade, a taxa de preenchimento foi medida numa fonte externa '
    'antes de qualquer alteracao. '
    'EVIDENCIA: pacote de replicacao de "LLMs for Model-driven Engineering: A Survey" '
    '(github.com/WSE-Lab/LLM4MDE, data/final_selection.csv, 236 estudos extraidos, 34 '
    'colunas), que traz duas colunas dedicadas, RQ14 TimeCostMetric e RQ14 '
    'ResourceCostMetric, com a sentinela [No] para nao reportado. Reportam algum custo: '
    '42 de 236, 17,8 por cento no corpus inteiro; 9 de 83, 10,8 por cento entre os que '
    'manipulam UML; 4 de 59, 6,8 por cento entre os que manipulam UML em tarefa de geracao. '
    'Este ultimo estrato e o analogo mais proximo do corpus desta revisao. Os rotulos '
    'nativos sao seis no total: Total task duration, Inference/generation time, Training '
    'effort, Token consumption, Monetary cost, API overhead. '
    'DISCUSSAO: extrapolado para os 58 registros com texto, o campo devolveria nao '
    'reportado em cerca de 93 por cento dos casos, para colher da ordem de quatro dados. O '
    'argumento de que o silencio sistematico seria achado da MQ5 nao se sustenta aqui, '
    'porque o silencio JA esta medido e publicado e pode ser citado na discussao sem custar '
    'uma decisao por estudo em 58 estudos. Pesa contra tambem o fato de os seis rotulos '
    'nativos ja convergirem sozinhos: um campo cuja funcao seria tornar comensuravel algo '
    'que ja e comensuravel nao faz trabalho. E a inclusao exigiria emendar o texto da MQ4, '
    'que hoje enumera dimensoes de avaliacao, baselines, papeis humanos, procedimentos '
    'automatizados e praticas de ciencia aberta, e nao custo; sem isso o campo entraria com '
    'a projecao faltante, o modo de falha que ja custou uma revisao inteira. '
    'DECISAO: o campo NAO entra. A medicao fica registrada para que a ausencia de custo na '
    'extracao seja uma decisao com numero e nao uma omissao. Se um estudo do piloto reportar '
    'custo, o campo 23 Sampling and repetition, que e composto e aberto, acomoda a mencao '
    'sem campo novo e sem tocar na MQ4. Nenhum campo do codebook foi alterado por esta '
    'linha. A decisao gemea, o campo NotationFamily, foi aplicada e consta em linha propria.',
    'https://github.com/WSE-Lab/LLM4MDE',
]

antes = list(csv.reader(open(LOG, encoding='utf-8')))
assert antes[0][3] == 'event_type' and all(len(x) == 9 for x in antes)
assert len(r1) == 9
print('log antes: %d | + %s %s %d chars' % (len(antes), r1[0], r1[3], len(r1[7])))
if '--apply' not in sys.argv:
    print('SIMULACAO. Rode com --apply para escrever.'); sys.exit(0)
with open(LOG, 'a', encoding='utf-8', newline='') as f:
    csv.writer(f).writerow(r1)
d = list(csv.reader(open(LOG, encoding='utf-8')))
assert len(d) == len(antes)+1 and all(len(x) == 9 for x in d) and d[:len(antes)] == antes
print('APLICADO. log: %d linhas.' % len(d))
