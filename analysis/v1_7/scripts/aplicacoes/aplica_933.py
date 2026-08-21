# -*- coding: utf-8 -*-
"""933_SCOPUS: o texto completo chegou por resposta do autor correspondente.

Grava a VERSAO em pdf_status e a VIA em pdf_local_source, que sao duas dimensoes
distintas (nao existe OK_AUTOR). Nao decide o C1: gate_c_outcome fica VAZIO, e a
decisao pertence a leitura integral na ficha.
"""
import csv, os, shutil, sys

BASE = ('/home/helaine-barreiros/Development/doutorado-workspace/'
        'estudo_sistematico/uml-quality-study')
CSV = os.path.join(BASE, 'search/automated/custom_automated_search_collection.csv')

ID = '933_SCOPUS'
MD5 = 'd67980912ad57bd38da2b0243be4ab36'

ANTES = {'pdf_status': 'SEM_ASSINATURA_CAPES', 'pdf_file': '', 'pdf_local_source': '',
         'excluded': '', 'exclusion_criteria': '', 'gate_b_outcome': 'PASSOU',
         'gate_c_outcome': ''}

DEPOIS = {'pdf_status': 'OK_PUBLISHER',
          'pdf_file': 'pdfs/933_SCOPUS.pdf',
          'pdf_local_source': '(anexo de e-mail do autor)'}

BLOCO = (
    ' || TEXTO COMPLETO RECEBIDO em 2026-08-19, por resposta do autor correspondente '
    'Thai-Minh Truong (thaiminh@hcmut.edu.vn), 63 horas apos o pedido de 2026-08-16 20:52. '
    'METODO: conferencia da folha de rosto contra o registro ANTES de aceitar o arquivo, '
    'nunca pelo nome do arquivo; e diagnostico de versao em TRES FRENTES que precisam '
    'concordar. '
    'EVIDENCIA DE IDENTIDADE, sem divergencia: titulo identico ao TI; autores Nhi Tran, '
    'Anh Nguyen, Ky Vu, Thai-Minh Truong identicos ao AU; afiliacao HCMUT e VNU-HCM; DOI '
    '10.1007/978-981-92-2885-0_10 identico ao DO; IEA/AIE 2026, LNAI 16614, p. 116-127, '
    'identicos a T2, VL, SP e EP; 12 paginas, que e exatamente 116 a 127. '
    'EVIDENCIA DE VERSAO, as tres frentes concordando: (1) metadado, Creator "Springer" e '
    'campo Title com o titulo DO VOLUME ("Advances and Trends in Artificial Intelligence"), '
    'Producer macOS Quartz, ou seja, o autor extraiu do volume ja diagramado; (2) tamanho '
    'de pagina 439,37 x 666,14 pt, isto e 155 x 235 mm, o formato de corte da LNCS, e NAO '
    'letter 612x792 nem A4 595x842; (3) texto da p. 1 traz 10.1007/978-981-92-2885-0_10, '
    'LNAI, Springer e IEA/AIE, marcas que num manuscrito de autor dao zero. '
    'DISCUSSAO: pdf_status diz QUE VERSAO e o texto e pdf_local_source diz POR ONDE ele '
    'chegou; sao dimensoes distintas e nao se fundem num rotulo unico. A via foi o autor, '
    'mas a versao e a publicada, logo OK_PUBLISHER com a via anotada ao lado, como nos '
    '907_SCOPUS e 829_SCOPUS, e nao OK_REPOSITORY_SUBSTITUIR, que e para manuscrito de '
    'autor. O PY nominal de 2027 diverge do evento de 2026 e da data de recebimento, mas a '
    'divergencia ja fora decidida no Portao A e NAO e reaberta aqui; o PDF apenas confirma '
    'que a decisao registrada esta coerente com a folha de rosto, que traz "Springer Nature '
    'Singapore Pte Ltd. 2027". '
    'DIREITO AUTORAL: copia sob licenca exclusiva da Springer, cedida pelo autor para uso '
    'academico. Fica em search/automated/pdfs/, diretorio no .gitignore; NAO entra no repo '
    'nem na replicacao. md5 d67980912ad57bd38da2b0243be4ab36, conferido contra o original, '
    'que permanece intacto em ~/Downloads/IEA_AIE2026.pdf. '
    'DECISAO: pdf_status OK_PUBLISHER, pdf_file pdfs/933_SCOPUS.pdf, pdf_local_source '
    '(anexo de e-mail do autor). O registro DEIXA de ser candidato a atricao. O '
    'gate_c_outcome permanece VAZIO de proposito: o C1 nao se decide por metadado nem por '
    'resumo, decide-se na ficha com o texto aberto. Corpus com texto passa de 57 para 58, '
    'sem texto de 48 para 47.'
)


def main(apply=False):
    with open(CSV, encoding='utf-8', newline='') as fh:
        rd = csv.DictReader(fh)
        campos = rd.fieldnames
        rows = list(rd)

    alvo = [r for r in rows if r['logical_id'] == ID]
    assert len(alvo) == 1, 'esperava 1 registro %s, achei %d' % (ID, len(alvo))
    r = alvo[0]
    for k, v in ANTES.items():
        assert r[k] == v, 'estado inesperado em %s: %r (esperado %r)' % (k, r[k], v)

    pdf = os.path.join(BASE, 'search/automated', DEPOIS['pdf_file'])
    assert os.path.exists(pdf), 'PDF ausente em %s' % pdf

    print('%-22s %-24s -> %s' % ('campo', 'antes', 'depois'))
    for k, v in DEPOIS.items():
        print('%-22s %-24r -> %r' % (k, r[k], v))
    print('%-22s %-24s -> %s' % ('pdf_status_orientacao', '%d chars' % len(r['pdf_status_orientacao']),
                                 '%d chars' % (len(r['pdf_status_orientacao']) + len(BLOCO))))
    print('%-22s %-24r -> %r  (o C1 e decidido na ficha)' % ('gate_c_outcome', r['gate_c_outcome'], r['gate_c_outcome']))

    if not apply:
        print('SIMULACAO.')
        return

    r.update(DEPOIS)
    r['pdf_status_orientacao'] += BLOCO

    tmp = CSV + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(rows)
    shutil.move(tmp, CSV)

    novo = list(csv.DictReader(open(CSV, encoding='utf-8')))
    assert len(novo) == len(rows), 'contagem de linhas mudou'
    v = [x for x in novo if x['logical_id'] == ID][0]
    for k, val in DEPOIS.items():
        assert v[k] == val, k
    assert v['gate_c_outcome'] == '', 'o C1 nao pode ter sido decidido aqui'
    assert v['excluded'] == '' and v['exclusion_criteria'] == ''
    # "com texto" so faz sentido ENTRE OS RETIDOS. Contar OK_* no corpus inteiro
    # inclui excluidos que tinham PDF e devolve um numero sem significado.
    ret = [x for x in novo if x['excluded'] != 'true']
    com = [x for x in ret if x['pdf_status'].startswith('OK_')]
    print('registros: %d | retidos: %d | com texto: %d | sem texto: %d'
          % (len(novo), len(ret), len(com), len(ret) - len(com)))
    print('APLICADO.')


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
