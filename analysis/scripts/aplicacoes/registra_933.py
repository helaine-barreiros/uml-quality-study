# -*- coding: utf-8 -*-
"""Uma linha: RESPOSTA_AUTOR do 933_SCOPUS."""
import csv, collections, sys

LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')

r1 = [
    '933_SCOPUS',
    '2026-08-19T09:35:00-03:00',
    'HB',
    'RESPOSTA_AUTOR',
    'C',
    '',
    '',
    'TEXTO COMPLETO RECEBIDO por resposta do autor correspondente. O autor Thai-Minh '
    'Truong (thaiminh@hcmut.edu.vn, HCMUT / VNU-HCM) respondeu em 2026-08-19 06:14 ao '
    'pedido despachado em 2026-08-16 20:52, 63 horas depois, e anexou o artigo. '
    'METODO: a regra do projeto manda conferir a folha de rosto contra o registro ANTES '
    'de aceitar o arquivo, nunca pelo nome do arquivo, e diagnosticar a versao em TRES '
    'FRENTES que precisam concordar. As duas coisas foram feitas antes de qualquer '
    'escrita. '
    'EVIDENCIA DE IDENTIDADE, sem divergencia: titulo "An LLM-Based Multi-agent Framework '
    'for Automatic Use Case Diagrams and Scenarios Generation" identico ao TI; autores Nhi '
    'Tran, Anh Nguyen, Ky Vu e Thai-Minh Truong identicos ao AU; afiliacao HCMUT e '
    'VNU-HCM; DOI 10.1007/978-981-92-2885-0_10 identico ao DO; IEA/AIE 2026, LNAI 16614, '
    'p. 116-127, identicos a T2, VL, SP e EP; o arquivo tem 12 paginas, que e exatamente '
    '116 a 127. '
    'EVIDENCIA DE VERSAO, as tres frentes concordando: (1) metadado, Creator "Springer" e '
    'campo Title com o titulo DO VOLUME, "Advances and Trends in Artificial Intelligence", '
    'com Producer macOS Quartz, ou seja, o autor extraiu o capitulo do volume ja '
    'diagramado; (2) tamanho de pagina 439,37 x 666,14 pt, isto e 155 x 235 mm, o formato '
    'de corte da LNCS, e NAO letter 612x792 nem A4 595x842, que sao o que sai de um '
    'manuscrito de autor; (3) o texto da p. 1 traz 10.1007/978-981-92-2885-0_10, LNAI, '
    'Springer e IEA/AIE, marcas que num manuscrito dao zero. '
    'DISCUSSAO: pdf_status diz QUE VERSAO e o texto e pdf_local_source diz POR ONDE ele '
    'chegou. Sao dimensoes distintas e por isso NAO EXISTE o rotulo OK_AUTOR, que ja foi '
    'proposto, aprovado e retirado por fundir as duas. Aqui a via foi o autor e a versao e '
    'a publicada, entao OK_PUBLISHER com a via anotada ao lado, como nos 907_SCOPUS e '
    '829_SCOPUS, e nao OK_REPOSITORY_SUBSTITUIR, que e reservado a manuscrito de autor '
    '(986_SCOPUS, 932_SCOPUS). O PY nominal de 2027 diverge do evento de 2026, mas a '
    'divergencia ja fora decidida no Portao A e NAO e reaberta: o PDF apenas confirma que '
    'a decisao registrada e coerente com a folha de rosto, que traz "Springer Nature '
    'Singapore Pte Ltd. 2027". '
    'DIREITO AUTORAL: copia sob licenca exclusiva da Springer, cedida pelo autor para uso '
    'academico. Guardada em search/automated/pdfs/, que esta no .gitignore; NAO entra no '
    'repositorio nem no pacote de replicacao. md5 d67980912ad57bd38da2b0243be4ab36, '
    'conferido contra o original, que permanece intacto em ~/Downloads/IEA_AIE2026.pdf. '
    'DECISAO: pdf_status de SEM_ASSINATURA_CAPES para OK_PUBLISHER; pdf_file '
    'pdfs/933_SCOPUS.pdf; pdf_local_source "(anexo de e-mail do autor)". O registro DEIXA '
    'de ser candidato a atricao. O gate_c_outcome permanece VAZIO DE PROPOSITO: o C1 nao '
    'se decide por metadado nem por resumo, decide-se na ficha com o texto aberto, e o '
    'resumo sugerir geracao de casos de uso a partir de requisitos em linguagem natural '
    'nao antecipa a decisao. Corpus retido de 105 inalterado; com texto passa de 57 para '
    '58, sem texto de 48 para 47. Ficha regerada e piloto conferido: segue nos MESMOS DEZ '
    'estudos, e o 933 entra na fila geral, fora do piloto. '
    'PENDENTE COM A REVISORA PRIMARIA: a resposta de agradecimento ao autor foi redigida '
    'por mim e e ENVIADA POR ELA, e a captura do e-mail vai por ela para '
    '.local-evidence/correspondencia/, a que eu nao tenho acesso.',
    'search/automated/pdfs/933_SCOPUS.pdf',
]


def main(apply=False):
    assert len(r1) == 9, len(r1)
    print('%-12s %-16s %6d chars' % (r1[0], r1[3], len(r1[7])))
    if not apply:
        print('SIMULACAO.')
        return
    with open(LOG, 'a', newline='', encoding='utf-8') as fh:
        csv.writer(fh).writerow(r1)
    rows = list(csv.reader(open(LOG, encoding='utf-8')))
    print('linhas:', len(rows), collections.Counter(len(x) for x in rows))
    print('APLICADO.')


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
