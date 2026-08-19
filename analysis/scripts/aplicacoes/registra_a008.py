# -*- coding: utf-8 -*-
"""Duas linhas: a A008 (passo 6, metodos) e a TERCEIRA chave de traducao."""
import csv, collections, sys

LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')

r1 = [
    'GLOBAL',
    '2026-08-19T15:10:00-03:00',
    'HB',
    'DECISAO_DESENHO',
    'DESENHO',
    '',
    '',
    'A008, PASSO 6 DO REFINO (metodos). FECHA a sequencia de seis passos pedida pela '
    'revisora primaria. '
    'METODO: o mesmo do passo 5, medir antes de propor. O metodo estava escrito DUAS '
    'VEZES — na coluna "Synthesis procedure" da tabela de rastreabilidade (l. 134-145, '
    'uma linha por pergunta) e no Synthesis Plan (l. 1645-1695, sete subsecoes). Doze '
    'perguntas contra sete subsecoes. Busquei o termo do PRODUTO de cada pergunta DENTRO '
    'do Synthesis Plan: "gap analysis"/"under investigated"/"concentration" AUSENTES; '
    '"credibility"/"adjudication"/"evaluator training" AUSENTES; "gap analysis" so ocorre '
    'em l. 138 e l. 1382; "credibility matrix" so em l. 143; "appraisal" dentro do '
    'Synthesis Plan so em l. 1695, e como ESTRATO de sensibilidade, uso diferente do que '
    'a SQ5 pede. Cinco achados; TRES aplicados, DOIS adiados. '
    'ACHADO 1 APLICADO, REGRA DE ALINHAMENTO DE UNIDADE (era o que travava a V09): a l. '
    '1640 mandava dois revisores codificarem TODA a inadequacao e calcular Cohen kappa e '
    'Krippendorff alpha sobre as dimensoes da tupla, mas inadequacao e CAMPO REPETIVEL DE '
    'ENUMERACAO LIVRE — o revisor A pode enumerar 5 e o B 7 no mesmo estudo, e sem regra '
    'de pareamento NAO EXISTE tabela de contingencia; o coeficiente reportaria quanto cada '
    'um achou, nao o quanto concordam sobre fronteira de categoria. E a l. 1560 tratava o '
    'assunto como pergunta de VIABILIDADE do piloto ("the feasibility of unit level '
    'extraction"), nao como PROCEDIMENTO. Aplicado: codificar inadequacao passa a ser DUAS '
    'operacoes e so a segunda carrega coeficiente. (1) UNITIZACAO: enumerar as '
    'inadequacoes no vocabulario NATIVO do estudo, os dois revisores, e RECONCILIAR por '
    'discussao e adjudicacao ANTES de classificar; o desacordo de enumeracao e reportado '
    'como contagem de itens somados, retirados e fundidos de cada lado, e NUNCA e '
    'dissolvido dentro do coeficiente. (2) CLASSIFICACAO: os dois independentes sobre a '
    'MESMA lista reconciliada, e ai sim kappa e alpha. A regra fica fixada ANTES das duas '
    'passagens porque alinhar unidade depois deixaria a classificacao de cada revisor '
    'decidir quais itens contam como relatados — exatamente a contaminacao que a '
    'independencia existia para evitar. '
    'ACHADO 4 APLICADO, UM DENOMINADOR POR SINTESE: uma unica subsecao carregava '
    '"Generation context, pragmatic adequacy, and rework", embora a A006 s.10 tenha '
    'SEPARADO a SQ6 da SQ7 e a tabela de subconjuntos (l. 1375-1378) lhes de denominadores '
    'DIFERENTES — SQ6 corpus inteiro, SQ7 so eixo U nao-ausente. Escrever as duas juntas '
    'instala a ARMADILHA DO DENOMINADOR dentro do proprio plano de sintese; 7a OCORRENCIA '
    'do padrao estrutural. Aplicado: duas subsecoes, cada uma declarando o proprio '
    'denominador NA PRIMEIRA FRASE e dizendo por que. A classificacao de status '
    'inferencial dos fatores de contexto foi para a SQ7, porque a tabela de rastreabilidade '
    'atribui "inferential status" a SQ7 e atribui a SQ6 so o que e SUPRIDO como '
    'conhecimento. '
    'ACHADO 5 APLICADO: o bullet "evaluation dimension by diagram type" (l. 1656) ainda '
    'falava o vocabulario do campo 26 fundido, que a A007 removeu ontem por DERIVADO. '
    'Reancorado nos tres eixos e na particao de dimensao do construto normalizado, no '
    'lugar, sem deslocar linha. '
    'ACHADOS 2 e 3 ADIADOS, E ADIADOS COM TRAVA, NAO COM PROMESSA: a MQ5 nao tem subsecao '
    'embora seu produto seja o mapa de lacuna, e a SQ5 nao tem subsecao embora seu produto '
    'seja a matriz de credibilidade. Ambas dependem de dado extraido — a MQ5 precisa saber '
    'QUAIS combinacoes de fato ocorrem (com 0 de 57 extraidos, escrever a subsecao seria '
    'escolher as celulas antes de ver a tabela) e as COLUNAS da matriz de credibilidade '
    'SAO os dominios de appraisal que a literatura de fato reporta. A revisora primaria '
    'levantou explicitamente o receio de as duas "passarem em branco e serem esquecidas". '
    'Resposta: criado analysis/scripts/verifica_protocolo.py, VERSIONADO (o verificador do '
    'instrumento vive em /tmp e nao serve de guarda duravel), que calcula o conjunto de '
    'perguntas cujo produto nao e nomeado em lugar nenhum do Synthesis Plan e afirma que o '
    'conjunto e EXATAMENTE {MQ5, SQ5}. E IGUALDADE, entao quebra dos DOIS lados: quebra se '
    'surgir uma terceira lacuna e quebra quando a MQ5 ou a SQ5 for coberta — cobrir uma '
    'delas OBRIGA a mexer na trava, e mexer na trava obriga a registrar a decisao. '
    'GATILHO: fim do piloto de 10, junto da conferencia de cobertura que ja esta agendada '
    'para la. '
    'SEXTO ACHADO, SURGIDO AO PREPARAR E RELATADO ANTES DE EXECUTAR: a lacuna da SQ5 tem '
    'DUAS metades. A de CONTEUDO (o que a matriz contem) depende do piloto; a PROCEDURAL '
    'nao — a l. 1711 deixa o adjudicador resolver "appraisal disagreements", o que '
    'PRESSUPOE dois appraisers, mas o A1-A13 nao aparece em NENHUMA linha da tabela de '
    'papeis, e decidir quem appraisa depois de appraisar contamina do mesmo jeito que o '
    'alinhamento de unidade. Propus incluir no passo 6; a revisora primaria REconfirmou o '
    'escopo original (1, 4 e 5), entao NAO foi aplicado. Fica escrito na A008 s.5 para ser '
    'reencontrado, sem trava propria. '
    'CUSTOS: .tex de 1862 para 1870 linhas, TERCEIRA chave de traducao (linha propria de '
    'CORRECAO_REFERENCIA nesta mesma data). PDF e HTML regerados, 57 paginas. Verificador '
    'do protocolo com 14 travas em zero falhas; verificador do instrumento inalterado e em '
    'zero falhas. ZERO retriagem e ZERO recodificacao: nenhum campo de extracao (seguem 64, '
    'ordinais intactos), nenhuma pergunta (seguem 12) e nenhum valor de decisao de triagem '
    'mudou. Com isto os SEIS passos do refino estao fechados.',
    'protocol/amendments/A008-unit-alignment-and-synthesis-denominators.md',
]

r2 = [
    'GLOBAL',
    '2026-08-19T15:11:00-03:00',
    'HB',
    'CORRECAO_REFERENCIA',
    'DESENHO',
    '',
    '',
    'TERCEIRA CHAVE DE TRADUCAO DE REFERENCIAS DE LINHA, .tex de 1862 para 1870 linhas, '
    'pela A008 (passo 6). Duas insercoes: a l. 1640 (Coding reliability) virou tres '
    'paragrafos, MAIS QUATRO linhas; e a subsecao fundida de SQ6 com SQ7 virou duas '
    'subsecoes, MAIS QUATRO linhas. A terceira mudanca, o bullet da l. 1656, foi '
    'substituicao no lugar e NAO desloca nada. '
    'REGRA: linhas ATE 1640 da numeracao antiga NAO MUDAM; linhas de 1641 a 1689 somam '
    'MAIS QUATRO; linhas de 1690 em diante somam MAIS OITO. '
    'CONTEUDO QUE CRESCEU: o texto da antiga l. 1640 hoje ocupa as l. 1640-1644; o texto '
    'das antigas l. 1689-1691 hoje ocupa as l. 1693-1699. '
    'ORDEM DE APLICACAO DAS TRES CHAVES, para quem le um registro antigo: primeiro a '
    'CORRECAO_REFERENCIA de 2026-08-17 (v1.7 para v1.8), depois a de 2026-08-18 (1860 '
    'para 1862), depois esta. '
    'REFERENCIAS CITADAS COM FREQUENCIA, JA TRADUZIDAS: tabela de subconjuntos analiticos '
    'l. 1375-1378 INALTERADA; regra do piloto de dez estudos l. 1560 INALTERADA; tupla de '
    'inadequacao l. 1601-1620 INALTERADA; l. 1354/1356 (pergunta fundida da codigo fundido) '
    'INALTERADAS; appraisal A1-A13 l. 1562-1594 INALTERADO. MUDARAM: Coding reliability '
    'mantem o titulo na l. 1638 e o corpo passa de l. 1640 para l. 1640-1644; Synthesis '
    'Plan de l. 1642-1695 para l. 1646-1703; tabela de papeis de revisor de l. 1697-1719 '
    'para l. 1705-1727; a linha da adjudicacao de appraisal de l. 1711 para l. 1719. '
    'NENHUMA chave de NUMERO DE CAMPO: os 64 campos e seus ordinais nao foram tocados.',
    'protocol/amendments/A008-unit-alignment-and-synthesis-denominators.md',
]


def main(apply=False):
    for r in (r1, r2):
        assert len(r) == 9, len(r)
        print('%-10s %-22s %6d chars' % (r[0], r[3], len(r[7])))
    if not apply:
        print('SIMULACAO.')
        return
    with open(LOG, 'a', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(r1)
        w.writerow(r2)
    rows = list(csv.reader(open(LOG, encoding='utf-8')))
    print('linhas:', len(rows), collections.Counter(len(x) for x in rows))
    print('APLICADO.')


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
