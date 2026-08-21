#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registra as recuperacoes das Ondas 1, 2 e 4 do Portao C.
Decisoes da pesquisadora (2026-08-16): (a) extrair os artigos dos volumes de anais;
(b) manter OK_ACERVO_LOCAL e registrar a conferencia; (c) aceitar versao de
repositorio como definitiva para 397 e 439."""
import csv, os, datetime

CSV = 'custom_automated_search_collection.csv'
LOG = 'screening_decision_log.csv'
AGORA = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
REV = 'HB'


def nota(metodo, evidencia, discussao, decisao):
    return ('METODO: %s | EVIDENCIA: %s | DISCUSSAO: %s | DECISAO: %s'
            % (metodo, evidencia, discussao, decisao))


# ---------------------------------------------------------------- ONDA 1
M1 = 'Download direto no site do editor; validacao por extracao da 1a pagina e conferencia do DOI impresso.'
D1 = ('IEEE Access e ouro: a versao de registro esta aberta no proprio editor, '
      'sem necessidade de proxy CAPES nem de copia de repositorio.')
ONDA1 = {
 '806_SCOPUS': ('LLM-Driven_MDA_Pipeline_for_Generating_UML_Class_Diagrams_and_Code.pdf',
                'DOI impresso na capa 10.1109/ACCESS.2025.3615828, identico ao do registro.'),
 '810_SCOPUS': ('VeriGen_An_LLM-Augmented_Framework_for_End-to-End_Automation_of_Software_Development_LifecycleFrom_Requirements_Specifications_to_Code_Generation.pdf',
                'DOI impresso na capa 10.1109/ACCESS.2026.3686308, identico ao do registro.'),
 '948_SCOPUS': ('Fine-Tuned_LLMs_Versus_Rule-Based_NLP_for_UML_Diagram_Generation_An_Educational_Evaluation.pdf',
                'DOI impresso na capa 10.1109/ACCESS.2025.3638372, identico ao do registro.'),
}

# ---------------------------------------------------------------- ONDA 4
MW = ('DOI localizado manualmente pela pesquisadora no IEEE Xplore; PDF obtido do arquivo '
      'oficial da Winter Simulation Conference; validacao por extracao da 1a pagina.')
DW = ('O registro chegou do ACM DL sem DOI e sem resumo. O DOI real e do IEEE (prefixo 10.1109), '
      'porque os anais da WSC sao publicados pelo IEEE e apenas indexados pela ACM. '
      'O PDF traz o cabecalho "Proceedings of the ... Winter Simulation Conference": e a versao de registro.')
WSC = {
 '422_ACM': ('2024-mustafee-harper-viana-monks.pdf', '10.1109/WSC63780.2024.10838785',
             'Titulo do PDF "A MATURITY MODEL FOR DIGITAL TWINS IN HEALTHCARE" (Mustafee, Harper, Viana, Monks) confere com o registro.'),
 '307_ACM': ('2024-sarjoughian-mohite.pdf', '10.1109/WSC63780.2024.10838715',
             'Titulo do PDF "CONSTRUCTING HIERARCHICAL MODULAR MODELS IN ALTERNATIVE AND INTERCHANGEABLE REPRESENTATIONS" (Sarjoughian, Mohite) confere.'),
 '427_ACM': ('2024-ragazzini-mcginnis-negri-macchi.pdf', '10.1109/WSC63780.2024.10838758',
             'Titulo do PDF "MODELING OPERATIONAL CONTROL IN DISCRETE-EVENT LOGISTICS SYSTEMS AND THEIR DIGITAL TWINS" confere.'),
 '399_ACM': ('2024-winstanley-wainer.pdf', '10.1109/WSC63780.2024.10838817',
             'Titulo do PDF "TESTING METHODOLOGY FOR DEVS MODELS IN CADMIUM" (Winstanley, Wainer) confere.'),
 '386_ACM': ('2024-oukassi-jaoua-yacout-negri-jaoua.pdf', '10.1109/WSC63780.2024.10838930',
             'Titulo do PDF "TOWARDS STANDARDIZING THE INTEGRATION OF DIGITAL TWINS IN MANUFACTURING SYSTEMS" confere.'),
 '383_ACM': ('2023-matta-lugaresi.pdf', '10.1109/WSC60868.2023.10407260',
             'Titulo do PDF "DIGITAL TWINS: FEATURES, MODELS, AND SERVICES" (Matta, Lugaresi) confere.'),
 '324_ACM': ('2023-giabbanelli-1.pdf', '10.1109/WSC60868.2023.10408017',
             'Titulo do PDF "GPT-BASED MODELS MEET SIMULATION..." (Giabbanelli) confere.'),
}

MR = 'PDF obtido em repositorio; validacao por extracao da 1a pagina, que declara o DOI da versao publicada.'
DR = ('Decisao (c) da pesquisadora em %s: a copia de repositorio e aceita como definitiva. '
      'O conteudo e o do artigo aceito; a paginacao pode divergir da versao do editor, '
      'o que so importa para citacao de trecho, nao para extracao de dados.' % AGORA)
REPO = {
 '397_ACM': ('2408.10763v2.pdf', '10.1109/WSC63780.2024.10838852',
             'A capa do arXiv declara "Accepted version of the paper presented at the 2024 Winter Simulation Conference" e imprime o DOI 10.1109/WSC63780.2024.10838852, confirmando o DOI informado.'),
 '439_ACM': ('439.pdf', '',
             'Deposito HAL (hal-03968479) da versao do autor; a folha de rosto cita a publicacao em MODELS 2022, pp. 497-502, com o DOI 10.1145/3550356.3561606 ja registrado.'),
}

MA = 'PDF obtido do proprio canal de distribuicao aberta da conferencia; validacao por extracao da 1a pagina.'
ABERTO = {
 '801_SCOPUS': ('ER25_PAD_Divljan.pdf',
                'Titulo do PDF "Towards an LLM-based Tool for Automated Database Design" (Divljan, Brdjanin) confere.',
                'CEUR-WS (vol. 4099) publica os anais em acesso aberto com URL persistente, mas nao registra DOI comercial por artigo. A ausencia de DOI e do modelo editorial, nao falha de recuperacao. O arquivo obtido e a versao de registro.'),
 '918_SCOPUS': ('Integrating Generative Artificial Intelligence with Systems Archi.pdf',
                'Apos a folha de rosto do DigitalCommons@ODU, a pagina 2 traz "Proceedings of the American Society for Engineering Management 2024 International Annual Conference" com o titulo do registro.',
                'Anais distribuidos por repositorio institucional (ODU), sem DOI por artigo. O deposito embrulha a versao publicada, nao um preprint: por isso vale como versao de registro.'),
 '867_SCOPUS': ('icas2024_0514_paper.pdf',
                'Titulo do PDF "LARGE LANGUAGE MODEL IN AIRCRAFT SYSTEM DESIGN" (Petter Krus, Linkoping) confere.',
                'A ICAS distribui os anais pelo seu proprio arquivo historico e nao atribui DOI por artigo. Ausencia de DOI por modelo editorial.'),
}

MV = ('Artigo extraido do volume completo dos anais com pypdf, apos localizar a faixa de paginas '
      'pelo sumario e confirmar o inicio e o fim pela leitura das paginas de fronteira.')
DV = ('Decisao (a) da pesquisadora em %s. O arquivo baixado era o volume inteiro do periodico, '
      'nao o artigo. Guardar o volume inviabilizaria a extracao por registro. '
      'ATENCAO: o codigo 10.5555 e o prefixo que a ACM DL atribui a itens SEM DOI registrado e '
      'NAO resolve em doi.org; serve como identificador ACM, nao como link.' % AGORA)
VOLUME = {
 '108_ACM': ('CCSCNW2024Final (1).pdf', '10.5555/3715602.3715614', 70, 80,
             'Sumario do volume (26th Annual CCSC Northwestern, 158p) aponta o artigo na pagina 70; a pagina 70 abre com o titulo do registro e a pagina 81 ja inicia o artigo seguinte.'),
 '170_ACM': ('CCSCSE2024Final.pdf', '10.5555/3717781.3717790', 44, 53,
             'Volume 38th Annual CCSC Southeastern (171p); pagina 44 abre com o titulo do registro e a pagina 54 ja inicia o artigo seguinte.'),
}

MS = 'Busca manual de DOI pela pesquisadora nas bases e no canal de publicacao.'
SEMDOI = {
 '791_SCOPUS': 'Busca sem resultado ate esta data. Permanece sem DOI; a recuperacao do texto completo segue em aberto.',
 '935_SCOPUS': 'Busca sem resultado ate esta data. Permanece sem DOI; a recuperacao do texto completo segue em aberto.',
 '390_ACM':    'Item de anais sem DOI atribuido. Confirmado em definitivo: nao existe DOI a recuperar.',
 '100_ACM':    'Periodico distribuido pela CCSC: o sumario e o texto completo estao na ACM DL, mas a CCSC costuma registrar apenas o codigo interno e a URL da base, sem prefixo DOI proprio. Confirmado: nao ha DOI.',
 '900_SCOPUS': 'Item de anais sem DOI atribuido. Confirmado em definitivo: nao existe DOI a recuperar.',
}

MN = 'Tentativa de acesso pela pesquisadora por DOI, editor e proxy CAPES.'
SEMACESSO = {
 '866_SCOPUS': ('', 'O DOI 10.12305/j.issn.1001-506X.2025.12.17 nao resolve e nao houve via de acesso ao texto.',
                'Esgotadas as vias disponiveis sem rota de acesso automatizada a editoras. Marcado como sem acesso em definitivo, para que o PRISMA registre a perda em vez de deixar o item em pendencia indefinida.'),
 '380_ACM': ('10.5555/3615924.3623629', 'Codigo ACM localizado, mas sem acesso ao texto completo.',
             'O codigo 10.5555 e o prefixo de itens SEM DOI registrado na ACM DL e nao resolve em doi.org, logo nao abre rota de acesso. Marcado como sem acesso em definitivo.'),
}

# ---------------------------------------------------------------- carga
with open(CSV, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
h = rows[0]
i = {c: n for n, c in enumerate(h)}
by = {r[i['logical_id']]: r for r in rows[1:]}

NOVO_ST = 'SEM_ACESSO_DEFINITIVO'
tocados = set()


def marca(lid, arquivo, status, doi, texto, origem):
    r = by[lid]
    assert r[i['excluded']] != 'true', lid
    if doi:
        r[i['DO']] = doi
    if arquivo:
        r[i['pdf_file']] = 'pdfs/%s.pdf' % lid
        r[i['pdf_local_source']] = origem
        assert os.path.exists('pdfs/%s.pdf' % lid), lid
    r[i['pdf_status']] = status
    ant = r[i['pdf_status_orientacao']]
    r[i['pdf_status_orientacao']] = (ant + ' || ' if ant else '') + texto
    tocados.add(lid)


for lid, (arq, ev) in ONDA1.items():
    marca(lid, arq, 'OK_PUBLISHER', '', nota(M1, ev, D1, 'Texto completo recuperado do editor. Status ABERTO_SEM_PDF_DIRETO -> OK_PUBLISHER.'), 'Downloads/' + arq)

for lid, (arq, doi, ev) in WSC.items():
    marca(lid, arq, 'OK_PUBLISHER', doi, nota(MW, ev, DW, 'DOI %s registrado e texto completo recuperado. Status SEM_DOI -> OK_PUBLISHER.' % doi), 'Downloads/' + arq)

for lid, (arq, doi, ev) in REPO.items():
    marca(lid, arq, 'OK_REPOSITORY_SUBSTITUIR', doi, nota(MR, ev, DR, 'Copia de repositorio aceita como definitiva. Status -> OK_REPOSITORY_SUBSTITUIR.'), 'Downloads/' + arq)

for lid, (arq, ev, di) in ABERTO.items():
    marca(lid, arq, 'OK_PUBLISHER', '', nota(MA, ev, di, 'Ausencia de DOI confirmada como caracteristica do canal editorial. Texto completo recuperado. Status SEM_DOI -> OK_PUBLISHER.'), 'Downloads/' + arq)

for lid, (arq, doi, ini, fim, ev) in VOLUME.items():
    marca(lid, arq, 'OK_PUBLISHER', doi, nota(MV, ev, DV, 'Extraidas as paginas %d-%d do volume para pdfs/%s.pdf. Codigo ACM %s registrado no campo DO com a ressalva de que nao resolve. Status SEM_DOI -> OK_PUBLISHER.' % (ini, fim, lid, doi)), 'Downloads/%s pp.%d-%d' % (arq, ini, fim))

for lid, ev in SEMDOI.items():
    marca(lid, '', 'SEM_DOI', '', nota(MS, ev, 'A ausencia de DOI nao impede a inclusao: o registro segue identificado por titulo, autores e veiculo.', 'Confirmado sem DOI. Status SEM_DOI mantido; texto completo ainda a recuperar.'), '')

for lid, (doi, ev, di) in SEMACESSO.items():
    marca(lid, '', NOVO_ST, doi, nota(MN, ev, di, 'Marcado como %s. Entra no PRISMA como perda declarada de texto completo.' % NOVO_ST), '')

# ---------------------------------------------------------------- ONDA 2
onda2 = [r[i['logical_id']] for r in rows[1:]
         if r[i['excluded']] != 'true' and r[i['pdf_status']] == 'OK_ACERVO_LOCAL']
assert len(onda2) == 18, len(onda2)
NOTA2 = nota('Conferencia individual dos arquivos ja presentes no acervo local, feita pela pesquisadora.',
             'Os 18 arquivos foram abertos e conferidos contra o registro; todos corretos.',
             'A Onda 2 existia porque o arquivo estava no acervo sem verificacao de correspondencia com o registro. A conferencia fecha essa duvida.',
             'Decisao (b) da pesquisadora em %s: manter o status OK_ACERVO_LOCAL e registrar a conferencia aqui e no log, sem criar valor novo de status.' % AGORA)
for lid in onda2:
    r = by[lid]
    ant = r[i['pdf_status_orientacao']]
    r[i['pdf_status_orientacao']] = (ant + ' || ' if ant else '') + NOTA2
    tocados.add(lid)

# ---------------------------------------------------------------- grava
with open(CSV, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(rows)

EVENTOS = [
 (';'.join(sorted(ONDA1)), 'RECUPERACAO_PDF', 'C', 'ABERTO_SEM_PDF_DIRETO', 'OK_PUBLISHER',
  'Onda 1 do Portao C. ' + nota(M1, 'DOI impresso na capa dos 3 PDFs identico ao do registro.', D1, 'Os 3 recuperados do editor.')),
 (';'.join(onda2), 'CONFERENCIA_ACERVO', 'C', 'OK_ACERVO_LOCAL', 'OK_ACERVO_LOCAL', 'Onda 2 do Portao C. ' + NOTA2),
 (';'.join(sorted(WSC)), 'RECUPERACAO_PDF', 'C', 'SEM_DOI', 'OK_PUBLISHER',
  'Onda 4 do Portao C. ' + nota(MW, 'Titulo da 1a pagina confere nos 7; cabecalho dos anais da WSC presente.', DW, '7 DOIs do IEEE registrados e 7 textos completos recuperados.')),
 (';'.join(sorted(REPO)), 'RECUPERACAO_PDF', 'C', 'SEM_DOI/NAO_INDEXADO', 'OK_REPOSITORY_SUBSTITUIR',
  'Onda 4 do Portao C. ' + nota(MR, '397 pelo arXiv (versao aceita), 439 pelo HAL (versao do autor).', DR, 'Aceitas como definitivas por decisao (c).')),
 (';'.join(sorted(ABERTO)), 'RECUPERACAO_PDF', 'C', 'SEM_DOI', 'OK_PUBLISHER',
  'Onda 4 do Portao C. ' + nota(MA, 'CEUR-WS vol.4099 (801), ASEM 2024 via DigitalCommons@ODU (918), arquivo da ICAS (867).',
     'Nos tres o veiculo publica em aberto sem atribuir DOI por artigo. A ausencia de DOI e do modelo editorial, nao falha de recuperacao.',
     '3 textos completos recuperados; permanecem sem DOI por natureza.')),
 (';'.join(sorted(VOLUME)), 'RECUPERACAO_PDF', 'C', 'SEM_DOI', 'OK_PUBLISHER',
  'Onda 4 do Portao C. ' + nota(MV, '108 nas pp.70-80 do volume CCSC NW; 170 nas pp.44-53 do volume CCSC SE.', DV,
     'Artigos extraidos dos volumes. Codigos 10.5555 registrados COM a ressalva de que nao resolvem em doi.org.')),
 (';'.join(sorted(SEMDOI)), 'CORRECAO', 'C', 'SEM_DOI', 'SEM_DOI',
  'Onda 4 do Portao C. ' + nota(MS, '390, 100 e 900 confirmados sem DOI por caracteristica do veiculo; 791 e 935 sem resultado ate esta data.',
     'Distincao registrada: em 390/100/900 nao ha DOI a procurar; em 791/935 a busca apenas nao teve exito ainda.',
     'Status SEM_DOI mantido nos 5; texto completo ainda a recuperar.')),
 (';'.join(sorted(SEMACESSO)), 'PERDA_TEXTO_COMPLETO', 'C', 'NAO_INDEXADO/SEM_DOI', NOVO_ST,
  'Onda 4 do Portao C. ' + nota(MN, '866: DOI 10.12305 nao resolve. 380: codigo ACM 10.5555 nao resolve e nao abre rota de acesso.',
     'Novo valor de pdf_status introduzido aqui, para separar "ainda nao recuperado" de "nao sera recuperado".',
     'Ambos marcados como %s por decisao da pesquisadora; entram no PRISMA como perda declarada.' % NOVO_ST)),
]

with open(LOG, 'a', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    for lids, tipo, gate, antes, depois, txt in EVENTOS:
        w.writerow([lids, AGORA, REV, tipo, gate, antes, depois, txt, ''])

print('registros tocados:', len(tocados))
print('eventos gravados no log:', len(EVENTOS))
