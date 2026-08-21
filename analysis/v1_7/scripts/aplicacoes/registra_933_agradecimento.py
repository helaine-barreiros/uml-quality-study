# -*- coding: utf-8 -*-
"""Uma linha: fechamento da correspondencia do 933_SCOPUS (agradecimento enviado)."""
import csv, sys

LOG = ('/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/'
       'uml-quality-study/search/automated/screening_decision_log.csv')

r1 = [
    '933_SCOPUS',
    '2026-08-20T10:30:00-03:00',
    'HB',
    'RESPOSTA_AUTOR',
    'C',
    '',
    '',
    'CORRESPONDENCIA ENCERRADA: agradecimento enviado ao autor. '
    'METODO: a linha de 2026-08-19 (commit f1cd3a6) deixou registrado como PENDENTE COM A '
    'REVISORA PRIMARIA o envio da resposta, redigida por mim, e o arquivamento da captura, '
    'a que eu nao tenho acesso. Esta linha fecha essa pendencia contra a captura entregue. '
    'EVIDENCIA: captura do fio no Gmail, arquivada em '
    '.local-evidence/correspondencia/2026-08-20_1028_agradecimento-enviado-933.png, '
    'md5 653ec9a29ed4f87c1037062dd2dcdcf6, copiada de ~/Pictures/Screenshots sem alterar o '
    'original. A captura mostra a mensagem recebida de MINH TRUONG THI THAI recolhida no '
    'topo, com a primeira linha "Dear Helaine, Thank you for your interest in our work, '
    '\'An LLM-Based Multi-agent Framework for Automatic Use Case Diagrams and Scenarios '
    'Generation.\'", e abaixo dela a resposta enviada por helaine.lins@upe.br para MINH, '
    'assinada "PhD candidate, University of Pernambuco (UPE), Brazil". '
    'RESSALVA 1, para nao ser lida errado depois: o corpo enviado agradece "for sending the '
    'manuscript", mas o arquivo recebido e a VERSAO PUBLICADA (IEA/AIE 2026, LNAI 16614, '
    'p. 116-127), diagnosticada nas tres frentes na linha de 2026-08-19. A palavra e '
    'cortesia de e-mail e NAO reabre o pdf_status: o registro segue OK_PUBLISHER, e nao '
    'OK_REPOSITORY_SUBSTITUIR. Fica escrito aqui porque a captura e evidencia arquivada e '
    'alguem que a leia isolada poderia inferir manuscrito. '
    'RESSALVA 2, lacuna real e nao mascarada: continua SEM captura propria da mensagem '
    'RECEBIDA de 2026-08-19 06:14. O passo 3 do procedimento de correspondencia pede essa '
    'captura, e o que existe hoje e apenas a linha recolhida dentro deste fio, que '
    'corrobora remetente e assunto mas NAO exibe data, hora nem o anexo. A identidade e a '
    'versao do texto nao dependem dela: estao ancoradas na folha de rosto do PDF, no md5 e '
    'nas tres frentes ja registradas. O que fica sem lastro visual e apenas o CARIMBO DE '
    'TEMPO da chegada. '
    'DECISAO: pendencia de envio encerrada; nenhum campo do CSV mestre alterado; '
    'pdf_status, pdf_file, pdf_local_source e gate_c_outcome intactos. O C1 do 933 segue '
    'por decidir na ficha, com o texto aberto. Compromisso de compartilhar a sintese NAO '
    'foi assumido com este autor: a lista de compromissos segue com 932, 986 e 939.',
    '.local-evidence/correspondencia/2026-08-20_1028_agradecimento-enviado-933.png',
]

antes = list(csv.reader(open(LOG, encoding='utf-8')))
assert antes[0][3] == 'event_type' and all(len(x) == 9 for x in antes)
assert len(r1) == 9

print('log antes: %d | + %s %s %d chars' % (len(antes), r1[0], r1[3], len(r1[7])))

if '--apply' not in sys.argv:
    print('SIMULACAO. Rode com --apply para escrever.')
    sys.exit(0)

with open(LOG, 'a', encoding='utf-8', newline='') as f:
    csv.writer(f).writerow(r1)

depois = list(csv.reader(open(LOG, encoding='utf-8')))
assert len(depois) == len(antes) + 1
assert all(len(x) == 9 for x in depois)
assert depois[:len(antes)] == antes, 'linha historica alterada'
print('APLICADO. log: %d linhas, todas com 9 colunas.' % len(depois))
