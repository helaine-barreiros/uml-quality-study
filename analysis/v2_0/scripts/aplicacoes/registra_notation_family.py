# -*- coding: utf-8 -*-
"""Uma linha: campo NotationFamily acrescentado ao codebook."""
import csv, sys
LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')
r1 = [
    'GLOBAL', '2026-08-20T20:05:00-03:00', 'HB', 'DECISAO_DESENHO', '', '', '',
    'CODEBOOK DE EXTRACAO: campo 65 NotationFamily acrescentado. '
    'METODO: comparacao do instrumento contra tres estudos secundarios proximos, um deles '
    'com pacote de replicacao de 236 estudos. A comparacao mostrou que quase todos os campos '
    'deles ja estao cobertos pelos 64, e isolou duas ausencias reais; esta e a que foi '
    'aplicada. '
    'EVIDENCIA: nenhum dos 64 campos registra se o conteudo gerado e UML, um perfil de UML, '
    'ou uma linguagem derivada. O Portao B5 decide SEPARABILIDADE e depois descarta qual era '
    'a outra notacao. Entre os 58 registros com texto, 3 citam outra notacao no titulo ou '
    'resumo: 018_ACM (SysML), 769_SCOPUS (DEVS) e 918_SCOPUS; 018_ACM e o PRIMEIRO estudo do '
    'piloto e um dos nove casos-teste do B5. '
    'DISCUSSAO: o volume e baixo mas a alavancagem nao. O eixo L registra o nivel mais '
    'exigente de evidencia de linguagem, e UML syntactic conformity e um de seus valores; um '
    'estudo que afere conformidade contra um PERFIL seria registrado como conformidade UML, e '
    'o eixo L alimenta a SQ4, que e a pergunta da dissonancia. O erro nao apareceria em lugar '
    'nenhum depois. Sem o campo, o extrator escreve a notacao numa nota livre ou perde. '
    'Momento: com 0 de 58 extraidos, a clausula de revisao retrospectiva do protocolo nao '
    'cobra nada; depois do piloto cobraria 10 registros e depois da extracao, 58. '
    'DECISAO: entra como ordinal 65, o proximo livre, e NAO como 66, porque numerar 66 '
    'deixaria um buraco no 65 sem explicacao. Fechado, nao repetivel, dono MQ2, origem lido. '
    'Valores: UML only; UML with a standard profile; a UML-derived language that is not a UML '
    'profile; UML alongside a separable non-UML notation; unclear. Nada renumera e o gerador '
    'da ficha deriva do codebook POR NOME, entao nenhuma trava nem prosa depende deste '
    'numero. Codebook de 64 para 65 campos; verifica_ficha.py teve as duas travas de contagem '
    'atualizadas de 64 para 65 e segue em zero falhas; ficha regerada, piloto conferido nos '
    'MESMOS DEZ. A MQ2 ja pergunta pelos tipos de diagrama e representacoes de saida, entao o '
    'campo entra com dono declarado e o texto do protocolo NAO precisou mudar.',
    'analysis/extraction/codebook_extracao.csv',
]
antes = list(csv.reader(open(LOG, encoding='utf-8')))
assert antes[0][3] == 'event_type' and all(len(x) == 9 for x in antes) and len(r1) == 9
print('log antes: %d | + %s %d chars' % (len(antes), r1[3], len(r1[7])))
if '--apply' not in sys.argv:
    print('SIMULACAO.'); sys.exit(0)
with open(LOG, 'a', encoding='utf-8', newline='') as f: csv.writer(f).writerow(r1)
d = list(csv.reader(open(LOG, encoding='utf-8')))
assert len(d) == len(antes)+1 and all(len(x) == 9 for x in d) and d[:len(antes)] == antes
print('APLICADO. log: %d linhas.' % len(d))
