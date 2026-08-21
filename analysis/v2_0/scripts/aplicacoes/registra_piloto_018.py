# -*- coding: utf-8 -*-
"""Tres linhas: C1 do 018_ACM, o B5 que se dissolve, e o achado 1 do piloto."""
import csv, sys
LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')

r1 = ['018_ACM','2026-08-21T05:40:00-03:00','HB','DECISAO_GATE','C','','',
 'C1 = ELEGIVEL. Primeira decisao do piloto de extracao. '
 'METODO: leitura integral do texto na ficha unica, com o C1 respondido antes dos campos. '
 'Wang, Ge, Liu, Cao, Chen e Hu, "Generating SysML Behavior Models via Large Language '
 'Models: an Empirical Study", Internetware 2025, 12 paginas. '
 'EVIDENCIA da instancia de geracao: 107 modelos gerados, 36 de atividade, 34 de maquina de '
 'estados e 35 de sequencia, com metrica por tipo. Sintaxe medida em DOIS niveis separados '
 'pelo proprio estudo, Acc_P para formato PlantUML e Acc_S para gramatica SysML, e semantica '
 'checada a mao contra 55 regras da norma. Resultado atribuivel ao UML gerado, e nao a um '
 'artefato agregado: mais de 90 por cento de acuracia gramatical contra F1 de 95 por cento em '
 'atividade e 50 por cento em sequencia. '
 'EVIDENCIA de que o objeto e UML, por tres caminhos independentes: a linguagem declarada e '
 'SysML v1.6, que e PERFIL de UML 2; os tres diagramas gerados sao comportamentais do UML, e '
 'sequencia e maquina de estados sao reusados do UML sem alteracao em SysML v1.6; e a '
 'representacao concreta emitida e PlantUML, que os proprios autores registram nao ter '
 'gramatica SysML ("Because PlantUML lacks a SysML grammar checker") nem validacao semantica '
 '("As PlantUML does not support semantic validation"). '
 'EVIDENCIA EM CONTRARIO, registrada e nao apagada: o artigo NUNCA chama de UML o que gera, '
 'diz "SysML behavior model" o tempo todo, e a conformidade e aferida contra a especificacao '
 'SysML v1.6 e nao contra o metamodelo UML. '
 'DISCUSSAO: o vocabulario nativo e SysML e fica registrado assim, antes de qualquer '
 'normalizacao. Ele nao derruba a elegibilidade porque o criterio e sobre o OBJETO e nao '
 'sobre o rotulo que o estudo escolhe. '
 'DECISAO: ELEGIVEL. gate_c_outcome de vazio para ELEGIVEL; nenhum outro campo alterado. '
 'Com C1 decidido passa de 3 para 4, de 58 com texto.',
 'search/automated/pdfs/018_ACM.pdf']

r2 = ['GLOBAL','2026-08-21T05:45:00-03:00','HB','INTERPRETACAO_PROTOCOLO','B','','',
 'B5/E7b NAO SE APLICA a perfil de UML. Leitura fixada no primeiro caso-teste lido por inteiro. '
 'METODO: o 018_ACM e um dos NOVE casos-teste do B5 e o primeiro a chegar ao texto completo. '
 'EVIDENCIA: o estudo gera SysML v1.6, que e um PERFIL de UML 2, emitido como PlantUML. '
 'DISCUSSAO: o E7b pergunta se o resultado gerado mistura UML com OUTRA notacao sem '
 'contribuicao UML separavel, e cita C4, ER, BPMN, SysML, Mermaid e esboco de arquitetura. '
 'Perfil nao e outra notacao: e UML com estereotipos, definido sobre o mesmo metamodelo. Nao '
 'ha duas notacoes a separar, ha UMA. A pergunta do B5 nao se aplica, e o caso-teste resolve '
 'PARA DENTRO. O que muda entre UML puro e UML com perfil nao e a elegibilidade e sim CONTRA '
 'QUE DEFINICAO DE LINGUAGEM a conformidade foi aferida, e isso e o campo 65 NotationFamily, '
 'nao o portao. '
 'DECISAO: leitura fixada e valida para os outros oito casos-teste do B5. SysML v1.6 e perfil '
 'e resolve para dentro; SysML v2 NAO e perfil e exige a leitura caso a caso. Nenhuma decisao '
 'de triagem registrada foi alterada: o 018 ja constava com gate_b_outcome PASSOU.',
 '']

r3 = ['GLOBAL','2026-08-21T05:50:00-03:00','HB','DECISAO_DESENHO','C','','',
 'ACHADO 1 DO PILOTO: a pergunta do C1 orientava para o artefato e nao para a atribuicao do '
 'resultado. Instrumento corrigido. '
 'METODO: achado da revisora primaria durante a primeira extracao do piloto, que e o proposito '
 'declarado do piloto: estressar o formulario. '
 'EVIDENCIA: a ficha dizia "Se da para dizer o que o modelo gerou e avalia-lo, ELEGIVEL". A '
 'formulacao convida a varrer o artigo atras de "gerou PlantUML?", que e a pergunta do B1 e ja '
 'foi respondida na triagem. O 018_ACM expoe o custo do erro: e um estudo que se apresenta '
 'como SysML o tempo todo e que, decidido por essa varredura, seria descartado, sendo que '
 'traz dissonancia sintatico-semantica DIRETA, que e o fenomeno central da revisao. '
 'DISCUSSAO: o C1 nao pergunta O QUE foi gerado, pergunta se um resultado relatado e '
 'ATRIBUIVEL a geracao do UML e nao a outros artefatos da mesma execucao. A atividade e longa '
 'e repetitiva, 58 registros, e formulacao ambigua em tarefa repetitiva vira erro sistematico, '
 'nao erro ocasional. '
 'DECISAO: gera_ficha_extracao.py alterado em dois pontos. O cabecalho do C1 passa a dizer que '
 'a pergunta NAO e "o estudo gerou UML?" e a mandar procurar a unidade medida. O passo 1 do '
 '"Como usar" nomeia a falha comum e manda voltar ao fenomeno, a dissonancia entre '
 'conformidade sintatica e adequacao semantica no UML gerado. Ficha regerada, verificador em '
 'zero falhas, 65 campos, piloto nos MESMOS DEZ. Custo retrospectivo NULO: 0 de 58 extraidos. '
 'REGISTRO TECNICO relacionado, para o resto do piloto: conferir citacao por grep literal no '
 'texto extraido do PDF produz FALSO NEGATIVO. Subscrito matematico vira U+1D443 e U+1D446 '
 'dentro do proprio PDF, e a extracao quebra a frase no meio da linha. Normalizar com NFKC e '
 'colapsar espacos antes de comparar: no 018 a busca por AccS passou de 0 para 7 e a frase '
 'quebrada de 0 para 1. Trocar de extrator nao resolve, porque nenhuma das duas coisas e '
 'defeito do extrator.',
 'analysis/scripts/gera_ficha_extracao.py']

novas=[r1,r2,r3]
antes=list(csv.reader(open(LOG,encoding='utf-8')))
assert antes[0][3]=='event_type' and all(len(x)==9 for x in antes)
for x in novas: assert len(x)==9
print('log antes: %d' % len(antes))
for x in novas: print('  + %-10s %-24s %d chars' % (x[0], x[3], len(x[7])))
if '--apply' not in sys.argv:
    print('SIMULACAO.'); sys.exit(0)
with open(LOG,'a',encoding='utf-8',newline='') as f: csv.writer(f).writerows(novas)
d=list(csv.reader(open(LOG,encoding='utf-8')))
assert len(d)==len(antes)+3 and all(len(x)==9 for x in d) and d[:len(antes)]==antes
print('APLICADO. log: %d linhas.' % len(d))
