# -*- coding: utf-8 -*-
"""Tres linhas de 2026-08-20: fechamento dos pedidos a autores, versionamento dos
renderizados do protocolo e abertura do piloto de extracao.

Simula por padrao; escreve so com --apply. Nunca reescreve linha historica."""
import csv, sys

LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')

r1 = [
    'GLOBAL',
    '2026-08-20T10:00:00-03:00',
    'HB',
    'DECISAO_DESENHO',
    'C',
    '',
    '',
    'PEDIDOS DE TEXTO COMPLETO A AUTORES: FILA ENCERRADA, so aguardando retorno. '
    'METODO: registro de declaracao da revisora primaria, feita em 2026-08-20, corrigindo '
    'o que a nota de trabalho do projeto afirmava. '
    'EVIDENCIA: a nota de correspondencia registrava o despacho de 2026-08-16 (20 '
    'mensagens, 20:46 a 20:52) e afirmava que os 31 retidos em PENDENTE_CAPES_IEEE ainda '
    'nao tinham pedido, sendo a via do autor "hoje a unica via alem do COMUT". A revisora '
    'primaria declara que os pedidos JA FORAM TODOS DESPACHADOS, inclusive os desses 31, e '
    'que nao havera novos disparos. '
    'DISCUSSAO: a afirmacao anterior era minha inferencia a partir do unico despacho que eu '
    'tinha visto processar, e nao de um registro de envio; ela e quem despacha, entao a '
    'declaracao dela e a fonte. A consequencia e sobre o ESTRATO DE ATRICAO, nao sobre '
    'elegibilidade: se todo retido sem texto ja recebeu pedido, entao "identificado, nao '
    'recuperado" passa a significar pedido feito e sem resposta ate o prazo, e nao pedido '
    'nao tentado. Isso e o que o relato de atricao precisa poder afirmar. As capturas dos '
    'e-mails de pedido ficam em .local-evidence/, a que eu nao tenho acesso; esta linha '
    'registra a declaracao, nao a verificacao mensagem a mensagem. '
    'DECISAO: nenhum novo pedido sera disparado. Ate 2026-09-01 o unico evento que muda '
    'um registro sem texto e a chegada de resposta de autor. Os 47 retidos sem texto '
    '(PENDENTE_CAPES_IEEE 31, SEM_ASSINATURA_CAPES 12, SEM_ACESSO_DEFINITIVO 3, SEM_DOI 1) '
    'que nao responderem ate la fecham como atricao declarada. Nenhum pdf_status, nenhum '
    'gate_c_outcome e nenhuma decisao de triagem foi alterado por esta linha.',
    '',
]

r2 = [
    'GLOBAL',
    '2026-08-20T10:05:00-03:00',
    'HB',
    'DECISAO_DESENHO',
    '',
    '',
    '',
    'RENDERIZADOS DO PROTOCOLO PASSAM A SER VERSIONADOS. '
    'METODO: decisao pendente desde 2026-08-18, quando o gerador foi criado (d8fd7b0) e o '
    'PDF, o HTML e o CSS ficaram deliberadamente fora do controle de versao a espera desta '
    'decisao; resolvida pela revisora primaria em 2026-08-20. '
    'EVIDENCIA: protocol/appendix_two_layer_mapping_protocol_v1_7.{pdf,html,css} estavam '
    'como nao rastreados no git status, gerados em 2026-08-19 08:54 a partir do .tex de '
    '08:53, portanto posteriores a ultima alteracao da fonte. '
    'DISCUSSAO: sao artefatos DERIVADOS, e versionar derivado normalmente duplica a fonte e '
    'convida a divergencia. O que pesa a favor aqui e que o protocolo e o documento que a '
    'banca e os validadores leem, e que eles nao rodam LaTeX: sem o PDF versionado, a '
    'versao lida por terceiros nao tem carimbo no historico. O risco de divergencia fica '
    'controlado pela regra ja em vigor de regerar a cada alteracao do .tex, que agora '
    'passa a ter efeito visivel: se o .tex mudar e os gerados nao, o diff denuncia. Os '
    'intermediarios de build seguem no .gitignore; so os tres arquivos finais entram. '
    'DECISAO: os tres arquivos entram no repositorio. A regra de regerar a cada alteracao '
    'do .tex continua valendo e passa a ser condicao do commit, nao so higiene.',
    'protocol/appendix_two_layer_mapping_protocol_v1_7.pdf',
]

r3 = [
    'GLOBAL',
    '2026-08-20T10:10:00-03:00',
    'HB',
    'DECISAO_DESENHO',
    'C',
    '',
    '',
    'PILOTO DE EXTRACAO ABERTO, primeiro estudo 018_ACM. '
    'METODO: o piloto foi desenhado e sorteado em 2026-08-18 (4e37668) e ficou PAUSADO por '
    'escolha da revisora primaria ate que o refino de seis passos fechasse, para nao '
    'extrair contra um codebook que ainda ia mudar. O refino fechou com a A008 (e908ba0) e '
    'ela autorizou a abertura em 2026-08-20. '
    'EVIDENCIA de que o instrumento esta coerente: verifica_protocolo.py e '
    'verifica_ficha.py em ZERO falhas; analysis/ficha_extracao.html regerada em 2026-08-19 '
    '09:56, posterior ao codebook (07:38) e ao CSV mestre (09:32); a amostra segue nos '
    'MESMOS DEZ estudos apos a entrada do 933_SCOPUS. Amostra: 018_ACM, 521_IEEE, '
    '751_SCOPUS, 762_SCOPUS, 801_SCOPUS, 859_SCOPUS, 892_SCOPUS, 909_SCOPUS, 958_SCOPUS, '
    '976_SCOPUS. O 018_ACM tem PDF em disco (pdfs/018_ACM.pdf, OK_ACERVO_LOCAL), '
    'gate_b_outcome PASSOU e gate_c_outcome VAZIO. '
    'DISCUSSAO: a ficha e instrumento UNICO, entao a decisao de C1 e a extracao dos 64 '
    'campos acontecem na mesma passagem, com o texto aberto — e e aqui que o C1 dos 55 '
    'retidos com texto comeca a ser decidido, nao antes. O 018_ACM nao e um caso facil de '
    'proposito nem por acaso: ele e um dos NOVE casos-teste do B5 e o titulo anuncia '
    'modelos de comportamento SysML, entao a pergunta de fronteira "e UML separavel de '
    'outra notacao?" cai logo no primeiro estudo. Isso e bom para estressar o formulario, '
    'que e o proposito do piloto, mas o registro do que for decidido ali precisa nomear a '
    'leitura adotada sobre SysML, porque ela vale para os outros casos de fronteira. Os '
    'DOIS DESVIOS declarados seguem valendo e estao escritos na secao 2.2 da propria ficha: '
    'extrator unico onde a l. 1558 exige dois nos campos interpretativos, o que mantem o '
    'V10 preso; e tempo medido fora da ficha, unica das cinco medidas do piloto que nao se '
    'reconstroi do export. '
    'DECISAO: piloto aberto, 018_ACM primeiro. Ao final: conferir cobertura de tipo de '
    'diagrama e de referencial (circularidade ja declarada), medir as cinco grandezas, '
    'revisar o codebook — revisao material dispara revisao retrospectiva, l. 1558 — e '
    'cobrir as subsecoes de sintese de MQ5 e SQ5 que a A008 adiou, cujo diferimento esta '
    'preso pela trava de igualdade em verifica_protocolo.py.',
    'analysis/ficha_extracao.html',
]

novas = [r1, r2, r3]

antes = list(csv.reader(open(LOG, encoding='utf-8')))
assert antes[0][3] == 'event_type' and len(antes[0]) == 9
assert all(len(x) == 9 for x in antes), 'log com largura irregular ANTES de escrever'
for r in novas:
    assert len(r) == 9, r[:4]

print('log antes: %d linhas (com header)' % len(antes))
for r in novas:
    print('  + %-8s %s %-16s %d chars' % (r[0], r[1][:10], r[3], len(r[7])))
print('log depois: %d linhas' % (len(antes) + len(novas)))

if '--apply' not in sys.argv:
    print('\nSIMULACAO. Rode com --apply para escrever.')
    sys.exit(0)

with open(LOG, 'a', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(novas)

depois = list(csv.reader(open(LOG, encoding='utf-8')))
assert len(depois) == len(antes) + 3
assert all(len(x) == 9 for x in depois), 'largura irregular DEPOIS de escrever'
assert depois[:len(antes)] == antes, 'linha historica foi alterada'
print('\nAPLICADO. log: %d linhas, todas com 9 colunas.' % len(depois))
