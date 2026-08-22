# -*- coding: utf-8 -*-
"""Gera a pagina de trabalho do Portao C: recuperacao de texto completo.
Somente leitura sobre o CSV. Escreve search/v3_0/gate_c_recuperacao.html."""
import criterios as crit
CRIT = crit.carrega()
crit.exige(CRIT, filtros={'C1'}, codigos={'E12'})

import csv, re, html, json, os
from urllib.parse import quote
from collections import Counter

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSV = os.path.join(BASE, 'search/v3_0/automated/records/custom_automated_search_collection.csv')
OUT = os.path.join(BASE, 'search/v3_0/gate_c_recuperacao.html')

rows = list(csv.reader(open(CSV, encoding='utf-8')))
i = {c: n for n, c in enumerate(rows[0])}
ret = [r for r in rows[1:] if r[i['excluded']] != 'true']

EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
CORRESP = re.compile(r'Correspondence Address:\s*([^;]+)')

# nucleo tematico: registros que a triagem apontou como centrais para a extracao
NUCLEO = {'925_SCOPUS', '949_SCOPUS', '956_SCOPUS', '983_SCOPUS', '976_SCOPUS',
          '898_SCOPUS', '924_SCOPUS', '939_SCOPUS', '942_SCOPUS', '948_SCOPUS',
          '958_SCOPUS', '970_SCOPUS', '985_SCOPUS'}

# ondas de despacho: (chave, titulo, subtitulo, acao, statuses)
ONDAS = [
    ('w1', 'Onda 1 - Aberto, ja baixada',
     'CONCLUIDA. Os 3 registros eram legalmente abertos e o Unpaywall so nao entregava o link '
     'direto do PDF. A pesquisadora baixou os tres e nenhum registro permanece neste status.',
     'Nada a fazer.',
     ['ABERTO_SEM_PDF_DIRETO']),
    ('w2', 'Onda 2 - No acervo local, ja conferida',
     'CONCLUIDA. Os 18 arquivos foram abertos e conferidos um a um contra o registro; '
     'todos corretos. Ficam em OK_ACERVO_LOCAL por decisao: o status descreve a procedencia '
     'do arquivo, e a conferencia esta registrada no log e no campo de observacao.',
     'Nada a fazer. Disponivel para leitura de texto completo.',
     ['OK_ACERVO_LOCAL']),
    ('w3', 'Onda 3 - Versao de repositorio',
     'Copia do arXiv, do HAL ou de repositorio institucional. Duas situacoes convivem aqui: '
     'as aceitas como definitivas pela pesquisadora (397 e 439) e as que ainda valeria trocar '
     'pela versao da editora. Em todas, a paginacao pode divergir da publicada. '
     'Entraram aqui na busca manual: 743 (sem carimbo de editora) e 539 (camera-ready '
     'certificado pelo IEEE PDFeXpress, nao a versao paginada do Xplore).',
     'Ler por esta versao. Ao citar trecho com numero de pagina, conferir na versao publicada.',
     ['OK_REPOSITORY_SUBSTITUIR']),
    ('w4', 'Onda 4 - Sem DOI, praticamente encerrada',
     'RESIDUO DE UM. Dos 21 registros originais, 18 tiveram o texto completo recuperado e 2 '
     'foram declarados sem acesso. Sobra 791, cuja busca ainda nao teve exito. Lembrete: em '
     '100, 390, 801, 867, 900, 918 e 935 nao existe DOI a procurar, e caracteristica do '
     'veiculo (CCSC, WSC, CEUR, ICAS, repositorio institucional), e todos ja estao lidos.',
     'A ausencia de DOI nao impede a inclusao. Falta apenas o texto completo, por titulo e autor.',
     ['SEM_DOI', 'NAO_INDEXADO']),
    ('w5', 'Onda 5 - Fora da assinatura CAPES',
     'Verificado com sessao autenticada no proxy ez371: a pagina so oferece compra. '
     'Nao e falha de autenticacao, a CAPES nao assina este titulo. Insistir no proxy nao resolve. '
     'Os 20 e-mails desta onda foram despachados em 2026-08-16 e ja produziram resultado: '
     '829 voltou com a versao publicada e 986 com o manuscrito de autor, ambos em menos de duas '
     'horas; 832 teve o endereco devolvido pelo servidor e foi encerrado sem acesso. '
     'O grupo caiu de 20 para 17.',
     'Aguardar as respostas pendentes. Buscar versao de autor em repositorio ou COMUT. '
     'Persistindo, candidato a E5 com tentativas documentadas.',
     ['SEM_ASSINATURA_CAPES']),
    ('w6', 'Onda 6 - Bloqueio IEEE (contrato CAPES nao renovado)',
     'Nao e paywall comum e nao depende de voce: o acesso da CAPES ao IEEE Xplore esta '
     'suspenso, e a tentativa pelo proxy responde HTTP 420 gerado no CloudFront, atrelado ao IP '
     'de saida da CAPES e nao a sua conta. O proxy nao contorna. Parte do grupo ja foi recuperada '
     'por arXiv e busca manual, de 34 para 32. Atencao ao 521: o PDF que chegou traz o carimbo '
     '"Authorized licensed use limited to: Linkoping University Library", ou seja, e copia '
     'redistribuida por terceiro e nao evidencia de que o acesso CAPES/IEEE funcione.',
     'Procurar copia em arXiv ou repositorio, pedir ao autor, ou aguardar a CAPES. '
     'Registrar a tentativa de qualquer forma.',
     ['PENDENTE_CAPES_IEEE']),
    ('w7', 'Onda 7 - Perda declarada de texto completo',
     'ENCERRADA SEM EXITO. Esgotadas as vias disponiveis, sem rota de acesso automatizada a '
     'editoras. Entram no PRISMA como perda documentada, nao como pendencia. O 832 entrou aqui '
     'em 2026-08-16: o e-mail do autor correspondente foi devolvido pelo servidor de destino, '
     'o que fecha a ultima via aberta.',
     'Nada a fazer, a menos que apareca uma via nova.',
     ['SEM_ACESSO_DEFINITIVO']),
]

STATUS_ROTULO = {
    'ABERTO_SEM_PDF_DIRETO': 'aberto, sem link direto',
    'OK_ACERVO_LOCAL': 'no acervo local',
    'OK_REPOSITORY_SUBSTITUIR': 'preprint, substituir',
    'SEM_DOI': 'sem DOI',
    'NAO_INDEXADO': 'fora do Unpaywall',
    'SEM_ASSINATURA_CAPES': 'sem assinatura CAPES',
    'PENDENTE_CAPES_IEEE': 'bloqueio IEEE',
    'OK_PUBLISHER': 'pronto',
    'SEM_ACESSO_DEFINITIVO': 'sem acesso, encerrado',
}


def limpa(s):
    return ' '.join((s or '').split())


def primeiro_autor(au):
    a = limpa(au).split(';')[0].strip()
    return a or '(autor nao registrado)'


INFERIDO = re.compile(r'EMAIL_INFERIDO=([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})')


def dados_contato(r):
    """Email e nome do autor correspondente.

    Primeiro o campo N1 (endereco declarado pela fonte). Se o registro nao traz
    correspondencia, cai no endereco reconstruido por coautoria e gravado como
    EMAIL_INFERIDO no campo de orientacao. O terceiro retorno diz qual dos dois
    e, porque um endereco inferido e atribuicao provavel e nao dado de origem.
    """
    n1 = r[i['N1']] or ''
    em = EMAIL.search(n1)
    nome = ''
    m = CORRESP.search(n1)
    if m:
        nome = limpa(m.group(1))
        nome = re.sub(r'\s*email:.*$', '', nome, flags=re.I).strip()
        if EMAIL.search(nome):
            nome = ''
    if em:
        return em.group(0), nome, False
    mi = INFERIDO.search(r[i['pdf_status_orientacao']] or '')
    if mi:
        return mi.group(1), '', True
    return '', nome, False


CONTATO = re.compile(r'TENTATIVA DE ACESSO em (\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})')


def contatado_em(r):
    """Data do e-mail ja despachado, lida do campo de observacao. Vazio se nunca contactado."""
    m = CONTATO.search(r[i['pdf_status_orientacao']] or '')
    return '%s %s' % (m.group(1), m.group(2)) if m else ''


def referencia(r):
    veic = limpa(r[i['T2']]) or limpa(r[i['J2']])
    ano = limpa(r[i['PY']])
    # nomes de anais quase sempre ja carregam o ano; nao repetir
    sufixo = ', %s' % ano if ano and ano not in veic else ''
    return '%s\n  %s%s' % (limpa(r[i['TI']]), veic, sufixo)


def assunto_curto(ti, limite=115):
    """Corta o titulo em fronteira de palavra, sem deixar pontuacao solta no fim."""
    t = limpa(ti)
    if len(t) <= limite:
        return t
    corte = t[:limite].rsplit(' ', 1)[0]
    return corte.rstrip(' ,;:-') + '...'


def tratamento(nome):
    """'Q. Su' -> 'Dr. Su'. O campo Correspondence Address do Scopus vem como inicial + sobrenome."""
    n = limpa(nome)
    if not n:
        return 'Authors'
    sobren = n.split()[-1]
    if len(sobren) < 2 or sobren.endswith('.'):
        return n or 'Authors'
    return 'Dr. %s' % sobren


def motivo(recs):
    """Justificativa honesta da falta de acesso, conforme o status real do registro."""
    sts = {r[i['pdf_status']] for r in recs}
    if sts == {'PENDENTE_CAPES_IEEE'}:
        return ("Unfortunately I have not been able to obtain the full text through my institution: "
                "access to IEEE Xplore under our national consortium is currently unavailable, and "
                "no open access version is indexed.")
    if 'PENDENTE_CAPES_IEEE' in sts:
        return ("Unfortunately I have not been able to obtain the full text through my institution: "
                "part of this material is not covered by our national subscription, access to IEEE "
                "Xplore under our consortium is currently unavailable, and no open access version "
                "is indexed.")
    return ("Unfortunately I could not obtain the full text through my institution: the publisher "
            "copy is not covered by our national subscription and no open access version is indexed.")


FECHO = ("Best regards,\n"
         "Helaine Barreiros\n"
         "PhD candidate, University of Pernambuco (UPE), Brazil\n")

ESCOPO = ("a systematic literature review on the quality of UML models generated by large language "
          "models from textual specifications")


def mensagem(recs, nome, ja=()):
    """Assunto e corpo de um unico e-mail cobrindo todos os artigos pendentes do destinatario.
    'ja' sao os artigos que essa mesma pessoa ja recebeu pedido, para nao repetir o pedido."""
    trat = tratamento(nome)
    if ja:
        anterior = ja[0]
        assunto = ('Follow-up: request for a copy of a second paper' if len(recs) == 1
                   else 'Follow-up: request for copies of %d further papers' % len(recs))
        # Se o pedido anterior ja foi atendido, agradecer em vez de pedir desculpa por insistir.
        atendido = anterior[i['pdf_status']] in COM_ARQUIVO
        preambulo = (
            'You very kindly sent me a copy of "%s" (%s%s), for which I am most grateful.\n\n'
            if atendido else
            'I wrote to you recently asking for a copy of "%s" (%s%s), and I apologise for coming '
            'back so soon.\n\n')
        abertura = (
            preambulo +
            "While reviewing my corpus I found %s of yours that also %s within the scope of my "
            "PhD research at the University of Pernambuco (UPE), Brazil, %s:\n"
            ) % (limpa(anterior[i['TI']]),
                 limpa(anterior[i['T2']]) or limpa(anterior[i['J2']]),
                 (', %s' % anterior[i['PY']]) if anterior[i['PY']] else '',
                 'a second paper' if len(recs) == 1 else '%d further papers' % len(recs),
                 'falls' if len(recs) == 1 else 'fall', ESCOPO)
        pedido = (
            "If it is convenient, a copy of both in the same reply would be more than enough, and "
            "would save you a second message."
            if len(recs) == 1 else
            "If it is convenient, copies of all of them in the same reply would be more than "
            "enough, and would save you further messages.")
        gratidao = "Thank you very much for your time and patience.\n\n"
    else:
        assunto = ('Request for a copy of your paper: %s' % assunto_curto(recs[0][i['TI']])
                   if len(recs) == 1 else
                   'Request for copies of %d of your papers' % len(recs))
        abertura = (
            "I am a PhD candidate at the University of Pernambuco (UPE), Brazil, conducting %s.\n\n"
            "%s selected for full-text analysis in my review:\n"
            % (ESCOPO,
               'Your paper was' if len(recs) == 1
               else 'The following %d papers of yours were' % len(recs)))
        pedido = (
            "Would you be willing to share a copy of the manuscript for academic research purposes?"
            if len(recs) == 1 else
            "Would you be willing to share copies of these manuscripts for academic research "
            "purposes?")
        gratidao = "Thank you very much for your time.\n\n"

    if len(recs) == 1:
        lista = '\n  %s\n' % referencia(recs[0])
    else:
        lista = '\n' + ''.join('  %d. %s\n\n' % (n, referencia(r)) for n, r in enumerate(recs, 1))

    corpo = (
        "Dear %s,\n\n%s%s\n%s\n\n"
        "%s %s would be cited and analysed within the review, and as soon as the findings are "
        "consolidated it would be a pleasure to share the synthesis with you.\n\n%s%s"
        % (trat, abertura, lista, motivo(recs), pedido,
           'The paper' if len(recs) + len(ja) == 1 else 'They',
           gratidao, FECHO))
    return assunto, corpo


def link_mailto(email, assunto, corpo):
    return 'mailto:%s?subject=%s&body=%s' % (email, quote(assunto), quote(corpo))


def link_gmail(email, assunto, corpo):
    """Abre a janela de composicao do Gmail no navegador, sem depender de cliente local."""
    return ('https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=%s&su=%s&body=%s'
            % (quote(email), quote(assunto), quote(corpo)))


MSGS = {}   # chave -> texto integral, para o botao "copiar mensagem"


def botoes_envio(chave, recs, email, nome, ja=(), rotulo='Abrir no Gmail'):
    """Tres vias para o mesmo e-mail: Gmail no navegador, cliente local, copiar texto."""
    assunto, corpo = mensagem(recs, nome, ja)
    MSGS[chave] = 'Para: %s\nAssunto: %s\n\n%s' % (email, assunto, corpo)
    return ('<a class="lk gmail" href="%s" target="_blank" rel="noopener">%s</a>'
            '<a class="lk local" href="%s" title="usa o programa de e-mail instalado no computador">'
            'cliente local</a>'
            '<button class="cp" data-msg="%s">copiar mensagem</button>'
            '<button class="cp" data-cp="%s">copiar endereco</button>'
            % (html.escape(link_gmail(email, assunto, corpo), True), html.escape(rotulo),
               html.escape(link_mailto(email, assunto, corpo), True),
               html.escape(chave, True), html.escape(email, True)))


def links(r):
    out = []
    ti = limpa(r[i['TI']])
    doi = limpa(r[i['DO']])
    if doi:
        out.append(('DOI', 'https://doi.org/%s' % doi, 'principal'))
    if r[i['oa_pdf_url']]:
        out.append(('PDF aberto', r[i['oa_pdf_url']], 'principal'))
    if r[i['oa_landing_url']]:
        out.append(('Pagina OA', r[i['oa_landing_url']], 'principal'))
    ur = limpa(r[i['UR']]).split(';')[0].strip()
    if ur and ur not in [u for _, u, _ in out]:
        out.append(('Editora', ur, ''))
    if ti:
        q = quote(ti)
        out.append(('Scholar', 'https://scholar.google.com/scholar?q=%s' % q, 'busca'))
        out.append(('arXiv', 'https://arxiv.org/search/?searchtype=all&query=%s' % q, 'busca'))
        out.append(('Semantic Scholar', 'https://www.semanticscholar.org/search?q=%s' % q, 'busca'))
        out.append(('OpenAlex', 'https://openalex.org/works?search=%s' % q, 'busca'))
    return out


def orientacao_curta(r):
    o = limpa(r[i['pdf_status_orientacao']])
    m = re.search(r'ACAO:\s*(.+)$', o)
    return m.group(1).strip() if m else o


# ---------------------------------------------------------------- montagem
por_status = Counter(r[i['pdf_status']] or '(vazio)' for r in ret)
COM_ARQUIVO = ('OK_PUBLISHER', 'OK_ACERVO_LOCAL', 'OK_REPOSITORY_SUBSTITUIR')
prontos = sum(por_status.get(s, 0) for s in COM_ARQUIVO)
perdidos = por_status.get('SEM_ACESSO_DEFINITIVO', 0)
faltam = len(ret) - prontos - perdidos
assert prontos == sum(1 for r in ret if r[i['pdf_file']].strip()), 'prontos != registros com arquivo'

# --------------------------------------------------- indice por destinatario
# So entram os registros que ainda nao tem texto completo e nao foram encerrados.
# O que ja foi contactado sai do proprio CSV, nao de lista digitada a mao.
pendentes = [r for r in ret
             if r[i['pdf_status']] not in COM_ARQUIVO
             and r[i['pdf_status']] != 'SEM_ACESSO_DEFINITIVO']

DEST = {}   # email -> {'nome':..., 'recs':[...]}
SEM_EMAIL = []
for r in pendentes:
    email, nome, inf = dados_contato(r)
    if not email:
        SEM_EMAIL.append(r)
        continue
    d = DEST.setdefault(email.lower(), {'nome': '', 'recs': [], 'inferidos': set()})
    d['recs'].append(r)
    if inf:
        d['inferidos'].add(r[i['logical_id']])
    if nome and not d['nome']:
        d['nome'] = nome

# Historico de contato varrido sobre o CORPUS INTEIRO, nao so sobre os pendentes.
# Um autor que ja respondeu sai da lista de pendentes junto com o artigo dele; se a
# checagem olhasse so os pendentes, esse endereco reapareceria como se fosse primeiro
# contato. Foi o que aconteceu com kim2@oakland.edu, que respondeu pelo 829_SCOPUS.
CONTATO_GLOBAL = {}
for r in rows[1:]:
    q = contatado_em(r)
    if not q:
        continue
    em, _, _ = dados_contato(r)
    if em and (em.lower() not in CONTATO_GLOBAL or q < CONTATO_GLOBAL[em.lower()][0]):
        CONTATO_GLOBAL[em.lower()] = (q, r)

# classifica cada destinatario: quantos artigos ja foram pedidos e quantos faltam
for e, d in DEST.items():
    d['ja'] = [r for r in d['recs'] if contatado_em(r)]
    d['falta'] = [r for r in d['recs'] if not contatado_em(r)]
    d['antes'] = CONTATO_GLOBAL.get(e)   # contato anterior fora da lista de pendentes
    if not d['falta']:
        d['classe'] = 'fechado'      # tudo ja pedido, nao escrever de novo
    elif d['ja'] or d['antes']:
        d['classe'] = 'parcial'      # ja recebeu e-mail meu sobre algum artigo
    else:
        d['classe'] = 'novo'
CONTATADOS_EMAIL = {e for e, d in DEST.items() if d['ja']}
ORDEM_CLASSE = {'novo': 0, 'parcial': 1, 'fechado': 2}

blocos = []
resumo_ondas = []
total_emails = 0
emails_por_onda = {}

for chave, titulo, sub, acao, sts in ONDAS:
    grupo = [r for r in ret if r[i['pdf_status']] in sts]
    grupo.sort(key=lambda r: (r[i['logical_id']] not in NUCLEO, -int(r[i['PY']] or 0),
                              limpa(r[i['TI']])))
    if not grupo:
        continue
    mails = []
    cards = []
    for r in grupo:
        lid = r[i['logical_id']]
        email, nome, inf = dados_contato(r)
        # so entra na copia em massa quem ainda nao recebeu e-mail sobre este corpus
        if email and email.lower() in DEST and not DEST[email.lower()]['ja']:
            mails.append(email)
        ls = links(r)
        chips = ''.join(
            '<a class="lk %s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, html.escape(u, True), html.escape(n))
            for n, u, cls in ls)
        quando = contatado_em(r)
        d_email = DEST.get(email.lower()) if email else None
        if email and d_email is None:
            # registro ja resolvido (tem arquivo) ou encerrado: nada a pedir
            contato = ('<div class="contato feito"><span class="ct-lab">Autor correspondente</span>'
                       '<code>%s</code><span class="hint">%s</span></div>'
                       % (html.escape(email),
                          'Pedido atendido em %s.' % html.escape(quando) if quando
                          else 'Nada a pedir neste registro.'))
        elif not email:
            contato = ('<div class="contato sem"><span class="ct-lab">Sem e-mail no registro</span>'
                       '<span class="hint">buscar na pagina do artigo ou no site do grupo de pesquisa</span></div>')
        elif quando:
            contato = ('<div class="contato feito"><span class="ct-lab">Ja pedido</span>'
                       '<code>%s</code><span class="hint">e-mail enviado em %s. '
                       'Nao escrever de novo sobre este artigo.</span></div>'
                       % (html.escape(email), html.escape(quando)))
        elif email.lower() in CONTATADOS_EMAIL:
            outros = ', '.join(x[i['logical_id']] for x in d_email['ja'])
            contato = ('<div class="contato alerta"><span class="ct-lab">Endereco ja contactado</span>'
                       '<code>%s</code><span class="hint">este autor ja recebeu e-mail seu sobre '
                       '%s. Nao use um pedido avulso: escreva pela secao '
                       '<a href="#dest">Por destinatario</a>, que junta os artigos em uma mensagem '
                       'so e reconhece o contato anterior.</span></div>'
                       % (html.escape(email), html.escape(outros)))
        elif len(d_email['falta']) > 1:
            irmaos = ', '.join(x[i['logical_id']] for x in d_email['falta']
                               if x[i['logical_id']] != lid)
            contato = ('<div class="contato alerta"><span class="ct-lab">Mesmo destinatario</span>'
                       '<code>%s</code><span class="hint">este endereco tambem responde por %s. '
                       'Peca tudo de uma vez pela secao <a href="#dest">Por destinatario</a>.</span></div>'
                       % (html.escape(email), html.escape(irmaos)))
        else:
            contato = ('<div class="contato"><span class="ct-lab">Autor correspondente</span>'
                       '<code>%s</code><div class="envio">%s</div></div>'
                       % (html.escape(email),
                          botoes_envio('card:' + lid, [r], email, nome)))
        nuc = '<span class="tag nucleo">nucleo da revisao</span>' if lid in NUCLEO else ''
        flags = ''.join('<span class="tag fl">%s</span>' % html.escape(f)
                        for f in r[i['gate_c_flags']].split(';') if f)
        arq = ''
        if r[i['pdf_file']]:
            arq = '<div class="arq">arquivo: <code>%s</code></div>' % html.escape(limpa(r[i['pdf_file']]))
        cards.append(
            '<article class="card" data-id="%s">'
            '<label class="done"><input type="checkbox" data-k="%s"><span></span></label>'
            '<div class="body">'
            '<div class="hd"><span class="lid">%s</span>%s%s'
            '<span class="tag st">%s</span><span class="yr">%s</span></div>'
            '<h4>%s</h4>'
            '<div class="meta">%s &middot; <span class="veic">%s</span></div>'
            '%s'
            '<div class="acao"><strong>Acao</strong> %s</div>'
            '<div class="lks">%s</div>'
            '%s</div></article>'
            % (html.escape(lid), html.escape(lid), html.escape(lid), nuc, flags,
               html.escape(STATUS_ROTULO.get(r[i['pdf_status']], r[i['pdf_status']])),
               html.escape(r[i['PY']]),
               html.escape(limpa(r[i['TI']])),
               html.escape(primeiro_autor(r[i['AU']])),
               html.escape(limpa(r[i['T2']]) or limpa(r[i['J2']]) or 's/ veiculo'),
               arq,
               html.escape(orientacao_curta(r)),
               chips, contato))

    emails_por_onda[chave] = sorted(set(mails))
    total_emails += len(set(mails))
    resumo_ondas.append((chave, titulo, len(grupo), len(set(mails))))
    barra = ''
    if mails:
        barra = ('<button class="bulk" data-onda="%s">Copiar os %d e-mails ainda nao contactados desta onda</button>'
                 % (chave, len(set(mails))))
    blocos.append(
        '<section id="%s" class="onda">'
        '<div class="onda-hd"><h3>%s</h3><span class="cnt">%d artigos</span></div>'
        '<p class="sub">%s</p>'
        '<p class="acao-g"><strong>O que fazer</strong> %s</p>'
        '%s'
        '<div class="grid">%s</div></section>'
        % (chave, html.escape(titulo), len(grupo), html.escape(sub), html.escape(acao),
           barra, ''.join(cards)))

# ------------------------------------------------------ bloco por destinatario
ROT_CLASSE = {
    'novo': ('a enviar', 'novo'),
    'parcial': ('endereco ja contactado', 'parcial'),
    'fechado': ('tudo ja pedido', 'fechado'),
}
dcards = []
for e in sorted(DEST, key=lambda e: (ORDEM_CLASSE[DEST[e]['classe']], e)):
    d = DEST[e]
    rot, cls = ROT_CLASSE[d['classe']]
    itens = []
    for r in sorted(d['recs'], key=lambda r: r[i['logical_id']]):
        q = contatado_em(r)
        marca = ('<span class="jd">pedido em %s</span>' % html.escape(q) if q
                 else '<span class="pd">pendente</span>')
        itens.append('<li><span class="lid">%s</span> %s %s</li>'
                     % (html.escape(r[i['logical_id']]),
                        html.escape(limpa(r[i['TI']])), marca))
    if d['falta']:
        n = len(d['falta'])
        if d['classe'] == 'parcial':
            rotulo = 'Abrir no Gmail: retomada do contato'
        elif n > 1:
            rotulo = 'Abrir no Gmail: um e-mail com os %d artigos' % n
        else:
            rotulo = 'Abrir no Gmail'
        anteriores = d['ja'] or ([d['antes'][1]] if d['antes'] else [])
        acao = botoes_envio('dest:' + e, d['falta'], e, d['nome'],
                            ja=anteriores, rotulo=rotulo)
    else:
        acao = '<span class="hint">Nada a enviar. Aguardar resposta.</span>'
    aviso = ''
    if d['classe'] == 'parcial':
        if d['ja']:
            quando_ant, ref_ant = contatado_em(d['ja'][0]), d['ja'][0][i['logical_id']]
        else:
            quando_ant, ref_ant = d['antes'][0], d['antes'][1][i['logical_id']]
        aviso = ('<p class="dwarn">Este endereco ja recebeu um pedido seu em %s, pelo registro '
                 '%s. A mensagem abaixo reconhece o contato anterior e pede apenas o que ainda '
                 'falta, para nao repetir o mesmo pedido.</p>'
                 % (html.escape(quando_ant), html.escape(ref_ant)))
    if d.get('inferidos'):
        aviso += ('<p class="dwarn">Endereco <b>inferido</b>, nao declarado, para %s. Foi '
                  'reconstruido pelo cruzamento de coautoria com outros registros do corpus e '
                  'confirmado pela afiliacao no ORCID. E atribuicao provavel, nao certa: confira o '
                  'nome antes de enviar.</p>'
                  % html.escape(', '.join(sorted(d['inferidos']))))
    marcar = ''
    if d['falta']:
        marcar = ('<label class="enviei"><input type="checkbox" data-env="%s">'
                  '<span>Ja enviei este. Marcar so depois de ver a mensagem na caixa de '
                  'enviados.</span></label>' % html.escape(e, True))
    dcards.append(
        '<article class="dcard %s" data-dest="%s"><div class="dhd"><code>%s</code>'
        '<span class="tag dc">%s</span></div>'
        '<div class="dnome">%s</div><ul class="dlist">%s</ul>%s'
        '<div class="dacao">%s</div>%s</article>'
        % (cls, html.escape(e, True), html.escape(e), html.escape(rot),
           html.escape(d['nome'] or '(nome nao registrado)'), ''.join(itens), aviso,
           acao, marcar))

n_novo = sum(1 for d in DEST.values() if d['classe'] == 'novo')
n_parc = sum(1 for d in DEST.values() if d['classe'] == 'parcial')
n_fech = sum(1 for d in DEST.values() if d['classe'] == 'fechado')

bloco_dest = (
    '<section id="dest" class="onda">'
    '<div class="onda-hd"><h3>Por destinatario</h3>'
    '<span class="cnt">%d enderecos &middot; %d artigos pendentes</span></div>'
    '<p class="sub">Esta secao inverte a leitura: em vez de um pedido por artigo, um pedido por '
    'pessoa. Serve para nao pedir duas vezes ao mesmo autor. O que ja foi enviado nao esta digitado '
    'aqui, e lido do campo de observacao do proprio CSV, entao a pagina nao pode discordar dos '
    'dados. Hoje sao <b>%d enderecos a enviar</b>, <b>%d que ja receberam e-mail seu</b> sobre '
    'outro artigo e <b>%d ja integralmente pedidos</b>.</p>'
    '<p class="acao-g"><strong>O que fazer</strong> Enviar pelos botoes desta secao, nao pelos '
    'cartoes das ondas. Onde o mesmo endereco responde por mais de um artigo, o botao gera '
    'uma unica mensagem cobrindo todos.</p>'
    '<div class="dgrid">%s</div></section>'
    % (len(DEST), sum(len(d['falta']) for d in DEST.values()),
       n_novo, n_parc, n_fech, ''.join(dcards)))

# ------------------------------------------------------------ sem e-mail
linhas_sem = ''.join(
    '<tr><td><span class="lid">%s</span></td><td>%s</td><td class="dim">%s</td>'
    '<td><a href="https://scholar.google.com/scholar?q=%s" target="_blank" rel="noopener">Scholar</a></td></tr>'
    % (html.escape(r[i['logical_id']]), html.escape(limpa(r[i['TI']])),
       html.escape(STATUS_ROTULO.get(r[i['pdf_status']], r[i['pdf_status']])),
       quote(limpa(r[i['TI']])))
    for r in sorted(SEM_EMAIL, key=lambda r: r[i['logical_id']]))

bloco_sem = (
    '<section id="semmail" class="onda">'
    '<div class="onda-hd"><h3>Sem e-mail no registro</h3><span class="cnt">%d artigos</span></div>'
    '<p class="sub">Nestes registros nao ha endereco a extrair: o campo <code>Correspondence '
    'Address</code> so existe no export do Scopus, e a exportacao do IEEE nao o traz. Por isso a '
    'lista e quase toda IEEE. Nao e falha da triagem nem do registro, e limite da fonte.</p>'
    '<p class="acao-g"><strong>O que fazer</strong> Abrir a pagina do artigo na editora e copiar o '
    'endereco de la, ou procurar a pagina pessoal do autor. Se nada aparecer, o registro segue '
    'para E5 com as tentativas ja documentadas.</p>'
    '<table class="res"><thead><tr><th>Registro</th><th>Titulo</th><th>Situacao</th>'
    '<th>Buscar</th></tr></thead><tbody>%s</tbody></table></section>'
    % (len(SEM_EMAIL), linhas_sem))

linhas_resumo = ''.join(
    '<tr><td><a href="#%s">%s</a></td><td class="n">%d</td><td class="n">%d</td></tr>'
    % (c, html.escape(t), n, e) for c, t, n, e in resumo_ondas)

HTML = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portao C - painel de recuperacao de texto completo</title>
<style>
:root{--bg:#0f1115;--pan:#171a21;--pan2:#1d212a;--ln:#2a2f3a;--tx:#e6e9ef;--dim:#9aa3b2;
--ac:#6ea8fe;--ok:#4ade80;--wr:#fbbf24;--bad:#f87171;--nuc:#c084fc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
font:15px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--ac)}
header{padding:36px 28px 24px;border-bottom:1px solid var(--ln);background:linear-gradient(180deg,#161a22,#0f1115)}
header h1{margin:0 0 6px;font-size:26px;letter-spacing:-.02em}
header p{margin:0;color:var(--dim);max-width:76ch}
main{padding:24px 28px 80px;max-width:1500px;margin:0 auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:22px 0 8px}
.kpi{background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:14px 16px}
.kpi b{display:block;font-size:30px;line-height:1.1;letter-spacing:-.02em}
.kpi span{color:var(--dim);font-size:12.5px;text-transform:uppercase;letter-spacing:.06em}
.kpi.ok b{color:var(--ok)}.kpi.wr b{color:var(--wr)}.kpi.ac b{color:var(--ac)}
table.res{width:100%%;border-collapse:collapse;margin:18px 0 30px;background:var(--pan);
border:1px solid var(--ln);border-radius:12px;overflow:hidden}
table.res th,table.res td{padding:9px 14px;border-bottom:1px solid var(--ln);text-align:left}
table.res th{background:var(--pan2);font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim)}
table.res td.n{text-align:right;font-variant-numeric:tabular-nums}
table.res tr:last-child td{border-bottom:0}
.onda{margin:36px 0 0;scroll-margin-top:16px}
.onda-hd{display:flex;align-items:baseline;gap:12px;border-bottom:2px solid var(--ln);padding-bottom:8px}
.onda-hd h3{margin:0;font-size:19px;letter-spacing:-.01em}
.cnt{color:var(--dim);font-size:13px}
.sub{color:var(--dim);margin:10px 0 4px;max-width:92ch}
.acao-g{margin:4px 0 12px;max-width:92ch;font-size:14px}
.acao-g strong,.acao strong{color:var(--wr);font-weight:600;margin-right:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:12px}
.card{display:flex;gap:10px;background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:13px 15px}
.card.feito{opacity:.42}
.card.feito h4{text-decoration:line-through}
.body{min-width:0;flex:1}
.hd{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:5px}
.lid{font:600 12px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--ac);
background:#1b2331;padding:2px 7px;border-radius:5px}
.yr{color:var(--dim);font-size:12px;margin-left:auto}
.tag{font-size:11px;padding:2px 7px;border-radius:5px;border:1px solid var(--ln);color:var(--dim)}
.tag.nucleo{color:var(--nuc);border-color:#4c2f6b;background:#241a33}
.tag.st{color:var(--wr);border-color:#4a3b16;background:#2a2313}
.tag.fl{font-family:ui-monospace,monospace;font-size:10px}
h4{margin:2px 0 4px;font-size:14.5px;font-weight:600;line-height:1.35}
.meta{color:var(--dim);font-size:12.5px;margin-bottom:8px}
.veic{font-style:italic}
.arq{font-size:11.5px;color:var(--dim);margin-bottom:6px;word-break:break-all}
.acao{font-size:12.5px;color:var(--dim);margin:6px 0 9px;padding-left:9px;border-left:2px solid var(--ln)}
.lks{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:8px}
.lk{font-size:11.5px;padding:3px 9px;border:1px solid var(--ln);border-radius:999px;
text-decoration:none;color:var(--dim);background:var(--pan2)}
.lk:hover{border-color:var(--ac);color:var(--ac)}
.lk.principal{color:var(--tx);border-color:#38506f}
.lk.busca{opacity:.72}
.lk.mail{color:#0f1115;background:var(--ok);border-color:var(--ok);font-weight:600}
.contato{display:flex;flex-wrap:wrap;gap:7px;align-items:center;font-size:12px;
border-top:1px dashed var(--ln);padding-top:8px}
.contato code{font-size:11.5px;color:var(--tx);background:var(--pan2);padding:2px 6px;border-radius:4px}
.ct-lab{color:var(--dim);text-transform:uppercase;font-size:10px;letter-spacing:.06em}
.contato.sem .hint{color:#6b7385;font-size:11.5px}
button{font:inherit;cursor:pointer}
.cp,.bulk{background:var(--pan2);color:var(--dim);border:1px solid var(--ln);
border-radius:6px;padding:3px 9px;font-size:11.5px}
.cp:hover,.bulk:hover{border-color:var(--ac);color:var(--ac)}
.bulk{margin-bottom:14px;padding:6px 13px;font-size:13px}
.done{display:flex;align-items:flex-start;padding-top:2px}
.done input{position:absolute;opacity:0;width:0;height:0}
.done span{display:block;width:19px;height:19px;border:1.5px solid var(--ln);border-radius:5px;background:var(--pan2)}
.done input:checked+span{background:var(--ok);border-color:var(--ok);
box-shadow:inset 0 0 0 3px var(--pan)}
.contato.feito{border-top-color:#2a4a32}
.contato.feito .ct-lab{color:var(--ok)}
.contato.alerta{border-top:1px solid #4a3b16}
.contato.alerta .ct-lab{color:var(--wr)}
.contato .hint{color:#8892a4;font-size:11.5px;flex-basis:100%%;line-height:1.45}
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:12px}
.dcard{background:var(--pan);border:1px solid var(--ln);border-left:3px solid var(--ln);
border-radius:12px;padding:13px 15px}
.dcard.novo{border-left-color:var(--ok)}
.dcard.parcial{border-left-color:var(--wr)}
.dcard.fechado{border-left-color:#3a4150;opacity:.62}
.dhd{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:3px}
.dhd code{font-size:12.5px;color:var(--tx);background:var(--pan2);padding:2px 7px;border-radius:5px}
.tag.dc{margin-left:auto}
.dcard.novo .tag.dc{color:var(--ok);border-color:#2a4a32}
.dcard.parcial .tag.dc{color:var(--wr);border-color:#4a3b16}
.dnome{color:var(--dim);font-size:12.5px;margin-bottom:8px}
.dlist{list-style:none;margin:0 0 10px;padding:0;font-size:12.5px}
.dlist li{padding:5px 0;border-top:1px dashed var(--ln);line-height:1.45}
.dlist .lid{margin-right:5px}
.dlist .jd{color:var(--ok);font-size:11px;white-space:nowrap}
.dlist .pd{color:var(--wr);font-size:11px;white-space:nowrap}
.dwarn{margin:0 0 10px;font-size:12px;color:var(--wr);background:#1e1a10;border:1px solid #4a3b16;
border-radius:7px;padding:8px 11px;line-height:1.5}
.dacao{display:flex;flex-wrap:wrap;gap:7px;align-items:center}
.dacao .hint{color:#6b7385;font-size:12px}
.envio{display:flex;flex-wrap:wrap;gap:6px;align-items:center;flex-basis:100%%;margin-top:7px}
.lk.gmail{color:#0f1115;background:var(--ok);border-color:var(--ok);font-weight:600;padding:5px 13px}
.lk.gmail:hover{background:#6ee79a;color:#0f1115}
.lk.local{font-size:11px;opacity:.8}
.enviei{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--dim);
margin-top:10px;padding-top:9px;border-top:1px dashed var(--ln);cursor:pointer;flex-basis:100%%}
.enviei input{width:16px;height:16px;accent-color:var(--ok);cursor:pointer}
.dcard.marcado{border-left-color:var(--ac)}
.dcard.marcado .dacao .lk.gmail{background:var(--pan2);color:var(--dim);border-color:var(--ln);font-weight:400}
.dim{color:var(--dim)}
.aviso{background:#1e1a10;border:1px solid #4a3b16;border-left:3px solid var(--wr);
border-radius:8px;padding:13px 16px;margin:20px 0;font-size:13.5px;max-width:96ch}
.aviso b{color:var(--wr)}
.nav{position:sticky;top:0;z-index:9;background:rgba(15,17,21,.94);backdrop-filter:blur(8px);
border-bottom:1px solid var(--ln);padding:9px 28px;display:flex;gap:14px;flex-wrap:wrap;font-size:13px}
.nav a{text-decoration:none;color:var(--dim)}.nav a:hover{color:var(--ac)}
.prog{margin-left:auto;color:var(--dim);font-variant-numeric:tabular-nums}
footer{color:#6b7385;font-size:12px;padding:0 28px 40px;max-width:1500px;margin:0 auto}
</style></head><body>
<header>
<h1>Portao C &mdash; painel de recuperacao de texto completo</h1>
<p>Situacao da recuperacao de texto completo dos %(total)d artigos retidos, organizada em ondas de
despacho. <b>%(prontos)d ja tem arquivo em maos</b>, %(faltam)d ainda faltam e %(perdidos)d foram
encerrados sem acesso. Dos que faltam, %(japed)d ja foram pedidos por e-mail ao autor e aguardam
resposta. A ordem das ondas vai do concluido ao que depende de terceiros.
Marque o que for concluindo: o progresso fica salvo neste navegador.</p>
</header>
<nav class="nav">
<a href="#topo">Resumo</a><a href="#dest">Por destinatario</a>%(navlinks)s<a href="#semmail">Sem e-mail</a>
<span class="prog" id="prog"></span>
</nav>
<main id="topo">

<div class="kpis">
<div class="kpi ok"><b>%(prontos)d</b><span>com arquivo em maos</span></div>
<div class="kpi wr"><b>%(faltam)d</b><span>a recuperar</span></div>
<div class="kpi"><b>%(japed)d</b><span>ja pedidos, aguardando</span></div>
<div class="kpi ac"><b>%(aenviar)d</b><span>enderecos a enviar</span></div>
<div class="kpi"><b>%(perdidos)d</b><span>sem acesso, encerrados</span></div>
<div class="kpi"><b>%(total)d</b><span>retidos no total</span></div>
</div>

<table class="res">
<thead><tr><th>Onda</th><th class="n">Artigos</th><th class="n">E-mails a enviar</th></tr></thead>
<tbody>%(resumo)s</tbody></table>

<div class="aviso">
<b>Como enviar por esta pagina.</b> Cada pedido tem tres vias para a mesma mensagem, ja pronta em
ingles com destinatario, assunto e corpo. <b>Nada e enviado automaticamente</b>: voce le, edita e
decide se envia.
<br><b>1. Abrir no Gmail</b> &mdash; abre a janela de composicao do Gmail numa aba nova, tudo
preenchido. <b>Use esta.</b>
<br><b>2. Cliente local</b> &mdash; link <code>mailto:</code> tradicional. So funciona se houver um
programa de e-mail registrado no sistema. Se nao houver, <b>o clique nao faz nada e nao avisa</b>,
e foi isso que ja aconteceu uma vez aqui: tres pedidos foram dados como enviados sem terem saido.
<br><b>3. Copiar mensagem</b> &mdash; poe destinatario, assunto e corpo na area de transferencia
para colar onde voce quiser.
<br><b>Confira sempre na caixa de enviados antes de marcar como enviado.</b> A caixa de selecao de
cada destinatario e so um lembrete no seu navegador; o registro oficial no CSV so e lancado
mediante evidencia.
</div>

<div class="aviso">
<b>Sobre nao pedir duas vezes.</b> Os enderecos vieram do campo <code>Correspondence Address</code>
do registro exportado do Scopus, ou seja, sao o contato que os autores publicaram junto do artigo.
Como um mesmo autor pode assinar mais de um artigo do corpus, <b>envie pela secao
<a href="#dest">Por destinatario</a></b>, que agrupa por pessoa, junta os artigos em uma mensagem
so e desliga o botao de quem ja foi contactado. Nos cartoes das ondas, quem ja recebeu e-mail
aparece marcado e sem botao de envio. O tratamento (<code>Dear Dr. Sobrenome</code>) e derivado
desse mesmo campo, que ocasionalmente inverte nome e sobrenome &mdash; vale bater os olhos antes de
enviar. Vale tambem espacar os envios e conferir se o endereco ainda esta ativo: enderecos
academicos expiram quando o autor troca de instituicao.
</div>

%(dest)s

%(blocos)s

%(semmail)s
</main>
<footer>
Gerado a partir de <code>search/v3_0/automated/records/custom_automated_search_collection.csv</code>.
Cada numero desta pagina sai do CSV; nada foi digitado a mao. O estado das caixas de selecao fica
apenas no seu navegador (localStorage) e nao altera o CSV.
</footer>
<script>
var MAILS=%(mails_json)s;
var MSGS=%(msgs_json)s;
var K='gatec.done.v1';
var st=JSON.parse(localStorage.getItem(K)||'{}');
function prog(){
  var tot=document.querySelectorAll('.done input').length;
  var f=document.querySelectorAll('.done input:checked').length;
  document.getElementById('prog').textContent=f+' de '+tot+' despachados';
}
document.querySelectorAll('.done input').forEach(function(cb){
  var k=cb.dataset.k;
  if(st[k]){cb.checked=true;cb.closest('.card').classList.add('feito');}
  cb.addEventListener('change',function(){
    st[k]=cb.checked; if(!cb.checked) delete st[k];
    localStorage.setItem(K,JSON.stringify(st));
    cb.closest('.card').classList.toggle('feito',cb.checked);
    prog();
  });
});
prog();
function copia(txt,btn){
  navigator.clipboard.writeText(txt).then(function(){
    var o=btn.textContent; btn.textContent='copiado'; setTimeout(function(){btn.textContent=o;},1200);
  });
}
document.querySelectorAll('.cp').forEach(function(b){
  b.addEventListener('click',function(){
    copia(b.dataset.msg?(MSGS[b.dataset.msg]||''):b.dataset.cp,b);
  });
});
var KE='gatec.enviei.v1';
var se=JSON.parse(localStorage.getItem(KE)||'{}');
document.querySelectorAll('.enviei input').forEach(function(cb){
  var k=cb.dataset.env;
  if(se[k]){cb.checked=true;cb.closest('.dcard').classList.add('marcado');}
  cb.addEventListener('change',function(){
    se[k]=cb.checked; if(!cb.checked) delete se[k];
    localStorage.setItem(KE,JSON.stringify(se));
    cb.closest('.dcard').classList.toggle('marcado',cb.checked);
  });
});
document.querySelectorAll('.bulk').forEach(function(b){
  b.addEventListener('click',function(){copia((MAILS[b.dataset.onda]||[]).join(', '),b);});
});
</script>
</body></html>"""

navlinks = ''.join('<a href="#%s">%s</a>' % (c, html.escape(t.split(' - ')[0]))
                   for c, t, _, _ in resumo_ondas)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(HTML % {
        'faltam': faltam, 'prontos': prontos, 'perdidos': perdidos, 'total': len(ret),
        'emails': total_emails, 'resumo': linhas_resumo, 'blocos': ''.join(blocos),
        'mails_json': json.dumps(emails_por_onda), 'navlinks': navlinks,
        'msgs_json': json.dumps(MSGS, ensure_ascii=False),
        'dest': bloco_dest, 'semmail': bloco_sem,
        'japed': sum(1 for r in pendentes if contatado_em(r)),
        'aenviar': n_novo + n_parc,
    })

print('gerado:', OUT)
print('retidos %d | prontos %d | a recuperar %d | com e-mail %d' % (len(ret), prontos, faltam, total_emails))
for c, t, n, e in resumo_ondas:
    print('  %-6s %-52s %3d artigos, %3d e-mails' % (c, t[:52], n, e))
print('destinatarios %d (novos %d, parciais %d, fechados %d) | sem e-mail %d | ja pedidos %d'
      % (len(DEST), n_novo, n_parc, n_fech, len(SEM_EMAIL),
         sum(1 for r in pendentes if contatado_em(r))))
