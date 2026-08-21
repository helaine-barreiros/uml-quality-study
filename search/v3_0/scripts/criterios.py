# -*- coding: utf-8 -*-
"""Le os criterios de elegibilidade e a estrutura de portoes DO PROTOCOLO.

Existe porque os geradores de portao traziam a redacao dos criterios escrita no
proprio codigo, com a pagina afirmando ao revisor que aquilo era "a redacao
literal do protocolo" -- uma afirmacao que nada verificava. Se o protocolo
mudasse um criterio, a pagina seguiria mostrando o antigo em silencio.

Agora a redacao vem do .tex e a estrutura e travada: exige() quebra se o
conjunto de filtros ou de codigos que um gerador usa deixar de bater com o que
o protocolo define. Quebrar e o ponto.
"""
import os
import re

_AQUI = os.path.abspath(__file__)                       # <raiz>/search/<versao>/scripts/criterios.py
VERSAO = os.path.basename(os.path.dirname(os.path.dirname(_AQUI)))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_AQUI))))
TEX = os.path.join(RAIZ, 'protocol', VERSAO,
                   'appendix_two_layer_mapping_protocol_%s.tex' % VERSAO)


def _limpa(s):
    s = re.sub(r'\\(?:textit|textbf|emph|texttt)\{([^}]*)\}', r'\1', s)
    s = s.replace('\\&', '&').replace('\\%', '%').replace('~', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def _tabela(txt, legenda):
    i = txt.index(legenda)
    return txt[i:txt.index('\\end{longtable}', i)]


def carrega(tex=None):
    txt = open(tex or TEX, encoding='utf-8').read()
    inc, exc, portoes = {}, {}, []

    for ln in _tabela(txt, 'Inclusion criteria}').split('\n'):
        m = re.match(r'^(I\d) & (.+?) & (.+?) & (.+?) \\\\', ln)
        if m:
            inc[m.group(1)] = {'criterio': _limpa(m.group(2)),
                               'filtro': _limpa(m.group(3)),
                               'par': _limpa(m.group(4))}

    for ln in _tabela(txt, 'Exclusion criteria}').split('\n'):
        m = re.match(r'^(E\d+b?) & (.+?) & (.+?) \\\\', ln)
        if m:
            exc[m.group(1)] = {'criterio': _limpa(m.group(2)),
                               'filtro': _limpa(m.group(3))}

    for ln in _tabela(txt, 'Screening gate structure').split('\n'):
        m = re.match(r'^(---|[A-C]) & (\S+) & (.+?) & (.+?) & (.+?) \\\\', ln)
        if m:
            portoes.append({'portao': m.group(1), 'filtro': m.group(2),
                            'pergunta': _limpa(m.group(3)),
                            'inclusao': _limpa(m.group(4)),
                            'exclusao': _limpa(m.group(5))})
    if not (inc and exc and portoes):
        raise SystemExit('ERRO: %s nao expos as tres tabelas de criterios' % TEX)
    return {'inclusao': inc, 'exclusao': exc, 'portoes': portoes, 'tex': tex or TEX}


def exige(C, filtros=None, codigos=None):
    """Trava. Quebra se o gerador e o protocolo discordarem sobre o que existe."""
    if filtros is not None:
        tem = {p['filtro'] for p in C['portoes']}
        falta = set(filtros) - tem
        if falta:
            raise SystemExit('ERRO: filtros %s nao existem no protocolo (%s)'
                             % (sorted(falta), sorted(tem)))
    if codigos is not None:
        falta = set(codigos) - set(C['exclusao'])
        if falta:
            raise SystemExit('ERRO: codigos de exclusao %s nao existem no protocolo (%s)'
                             % (sorted(falta), sorted(C['exclusao'])))


def texto(C, codigo):
    """A redacao literal do criterio, como o protocolo a escreve."""
    d = C['exclusao'].get(codigo) or C['inclusao'].get(codigo)
    if d is None:
        raise SystemExit('ERRO: o protocolo nao define o criterio %s' % codigo)
    return d['criterio']


def pergunta(C, filtro):
    for p in C['portoes']:
        if p['filtro'] == filtro:
            return p['pergunta']
    raise SystemExit('ERRO: o protocolo nao define o filtro %s' % filtro)


def fracao_segundo_revisor(C=None):
    """A fracao da amostra do segundo revisor, lida da prosa do protocolo.

    Estava escrita no gerador como 0.20 com um comentario apontando para um
    numero de linha da v1.8 -- o mesmo modo de falha das 24 referencias que o
    codebook carregava.
    """
    txt = open((C or {}).get('tex', TEX), encoding='utf-8').read()
    m = re.search(r'independently screens a stratified random sample of at least\s+(\d+)\s+percent', txt)
    if not m:
        raise SystemExit('ERRO: o protocolo nao declara a fracao do segundo revisor')
    return int(m.group(1)) / 100.0


if __name__ == '__main__':
    C = carrega()
    print('protocolo:', os.path.relpath(C['tex'], RAIZ))
    print('inclusao :', ' '.join(sorted(C['inclusao'])))
    print('exclusao :', ' '.join(sorted(C['exclusao'], key=lambda s: (len(s), s))))
    print('portoes  :', ' '.join(p['filtro'] for p in C['portoes']))
    print('fracao 2o revisor:', fracao_segundo_revisor(C))
    for p in C['portoes']:
        print('  %-3s %-3s %-62s inc=%-8s exc=%s'
              % (p['portao'], p['filtro'], p['pergunta'][:62], p['inclusao'], p['exclusao']))
