# -*- coding: utf-8 -*-
"""Pagina de busca manual (opcao 4): links prontos de Google Scholar e busca de PDF
para os 63 registros retidos sem texto completo. Somente leitura sobre o CSV."""
import csv, re, html, os
from urllib.parse import quote

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSV = os.path.join(BASE, 'search/v3_0/automated/records/custom_automated_search_collection.csv')
OUT = os.path.join(BASE, 'search/v3_0/gate_c_busca_manual.html')
CSS = open(os.path.join(BASE, 'search/v3_0/scripts/css_gate.css'), encoding='utf-8').read()

rows = list(csv.reader(open(CSV, encoding='utf-8')))
i = {c: n for n, c in enumerate(rows[0])}
ret = [r for r in rows[1:] if r[i['excluded']] != 'true']
falta = [r for r in ret if r[i['pdf_status']] in
         ('PENDENTE_CAPES_IEEE', 'SEM_ASSINATURA_CAPES', 'SEM_DOI')]

NUCLEO = {'925_SCOPUS', '949_SCOPUS', '956_SCOPUS', '983_SCOPUS', '976_SCOPUS',
          '898_SCOPUS', '924_SCOPUS', '939_SCOPUS', '942_SCOPUS', '948_SCOPUS',
          '958_SCOPUS', '970_SCOPUS', '985_SCOPUS'}
# achado do sweep por titulo no arXiv
ARXIV = {'900_SCOPUS': 'http://arxiv.org/abs/2311.07605v1'}
# veiculos com arquivo aberto proprio
VENUE = {
 '900_SCOPUS': ('CEUR-WS', 'https://ceur-ws.org/'),
 '935_SCOPUS': ('CEUR-WS', 'https://ceur-ws.org/'),
 '390_ACM':    ('arquivo da WSC', 'https://informs-sim.org/'),
 '100_ACM':    ('anais da CCSC', 'https://ccsc.org/publications/'),
}


def limpa(s):
    return ' '.join((s or '').split())


def autor1(s):
    a = (s or '').split(';')[0].strip()
    return a or 's/ autor'


def grupo_de(r):
    lid = r[i['logical_id']]
    if lid in VENUE:
        return 'g1'
    if r[i['DO']].startswith('10.1007'):
        return 'g2'
    if r[i['pdf_status']] == 'PENDENTE_CAPES_IEEE':
        return 'g3'
    return 'g4'


GRUPOS = [
 ('g1', 'Rota aberta ja identificada',
  'O veiculo publica em aberto e nao emite DOI, por isso o Unpaywall passou batido. '
  'Aqui a busca manual e quase formalidade: va direto ao arquivo do veiculo.'),
 ('g2', 'Springer - series de livro (LNCS e afins)',
  'Nao sao 19 paywalls independentes: todos estao em serie de LIVRO da Springer, colecao que o '
  'portal CAPES nao cobre. Se a busca manual nao render, esta e a hipotese a confirmar com a '
  'biblioteca da UPE antes de declarar perda.'),
 ('g3', 'IEEE - contrato CAPES suspenso',
  'Bloqueio institucional, nao paywall individual. O proxy nao contorna e o arXiv ja foi varrido '
  'por titulo sem resultado. A busca manual e a ultima via que nao depende de terceiros.'),
 ('g4', 'Demais editoras',
  'Elsevier, Wiley, Taylor & Francis e outros, sem assinatura CAPES para o titulo.'),
]


def links(r):
    ti = limpa(r[i['TI']])
    frase = quote('"%s"' % ti)
    out = [('Google Scholar', 'https://scholar.google.com/scholar?hl=pt-BR&q=%s' % frase, 'pri'),
           ('PDF na web', 'https://duckduckgo.com/?q=%s+filetype%%3Apdf' % frase, ''),
           ('Semantic Scholar', 'https://www.semanticscholar.org/search?q=%s' % quote(ti), '')]
    lid = r[i['logical_id']]
    if lid in ARXIV:
        out.insert(0, ('arXiv (achado)', ARXIV[lid], 'ok'))
    if lid in VENUE:
        nome, url = VENUE[lid]
        out.insert(0, (nome, url, 'ok'))
    if r[i['DO']]:
        out.append(('DOI', 'https://doi.org/%s' % r[i['DO']], 'dim'))
    return out


blocos = []
resumo = []
for chave, titulo, sub in GRUPOS:
    g = [r for r in falta if grupo_de(r) == chave]
    if not g:
        continue
    g.sort(key=lambda r: (r[i['logical_id']] not in NUCLEO, limpa(r[i['TI']])))
    resumo.append((chave, titulo, len(g)))
    cards = []
    for r in g:
        lid = r[i['logical_id']]
        ti = limpa(r[i['TI']])
        chips = ''.join('<a class="lk %s" href="%s" target="_blank" rel="noopener">%s</a>'
                        % (c, html.escape(u, True), html.escape(n)) for n, u, c in links(r))
        nuc = '<span class="tag nucleo">nucleo da revisao</span>' if lid in NUCLEO else ''
        fl = ''.join('<span class="tag fl">%s</span>' % html.escape(f)
                     for f in r[i['gate_c_flags']].split(';') if f)
        cards.append(
            '<article class="card">'
            '<label class="done"><input type="checkbox" data-k="%s"><span></span></label>'
            '<div class="body">'
            '<div class="hd"><span class="lid">%s</span>%s%s<span class="yr">%s</span></div>'
            '<h4>%s</h4>'
            '<div class="meta">%s &middot; <span class="veic">%s</span></div>'
            '<div class="lks">%s<button class="cp" data-cp="%s">copiar titulo</button></div>'
            '</div></article>'
            % (html.escape(lid, True), html.escape(lid), nuc, fl, html.escape(r[i['PY']]),
               html.escape(ti), html.escape(autor1(r[i['AU']])),
               html.escape(limpa(r[i['T2']]) or limpa(r[i['J2']]) or 's/ veiculo'),
               chips, html.escape(ti, True)))
    blocos.append('<section id="%s" class="onda"><div class="oh"><h2>%s</h2>'
                  '<span class="ct">%d artigos</span></div><p class="sub">%s</p>'
                  '<div class="cards">%s</div></section>'
                  % (chave, html.escape(titulo), len(g), html.escape(sub), ''.join(cards)))

nav = ''.join('<a href="#%s">%s</a>' % (c, html.escape(t.split(' - ')[0])) for c, t, _ in resumo)
tab = ''.join('<tr><td><a href="#%s">%s</a></td><td class="n">%d</td></tr>'
              % (c, html.escape(t), n) for c, t, n in resumo)

JS = """
var K='gatec.manual.v1';
function ld(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(e){return {}}}
function sv(o){localStorage.setItem(K,JSON.stringify(o))}
function prog(){var t=document.querySelectorAll('input[data-k]').length,
d=document.querySelectorAll('input[data-k]:checked').length;
document.getElementById('prog').textContent=d+' de '+t+' resolvidos';}
document.addEventListener('DOMContentLoaded',function(){
 var st=ld();
 document.querySelectorAll('input[data-k]').forEach(function(c){
  if(st[c.dataset.k]){c.checked=true;c.closest('.card').classList.add('feito');}
  c.addEventListener('change',function(){
   var s=ld(); if(c.checked){s[c.dataset.k]=1;c.closest('.card').classList.add('feito');}
   else{delete s[c.dataset.k];c.closest('.card').classList.remove('feito');}
   sv(s);prog();});
 });
 document.querySelectorAll('.cp').forEach(function(b){
  b.addEventListener('click',function(){navigator.clipboard.writeText(b.dataset.cp);
   var o=b.textContent;b.textContent='copiado';setTimeout(function(){b.textContent=o},1200);});
 });
 prog();
});
"""

EXTRA = """
.card.feito{opacity:.42}
.lk.ok{border-color:#4ade80;color:#4ade80}
.lk.pri{border-color:#60a5fa;color:#60a5fa;font-weight:600}
.lk.dim{opacity:.55}
.aviso{border:1px solid #f59e0b;background:rgba(245,158,11,.07);border-radius:10px;
padding:16px 20px;margin:22px 0}
.aviso b{color:#f59e0b}
"""

DOC = """<!doctype html><meta charset="utf-8">
<title>Portao C - busca manual</title>
<style>__CSS__
__EXTRA__</style><body>
<header>
<h1>Portao C &mdash; busca manual das versoes livres</h1>
<p>Os <b>%(n)d</b> artigos retidos ainda sem texto completo, com os links de busca ja montados.
O Google Scholar indexa pagina pessoal de autor e repositorio que as APIs de acesso aberto nao
alcancam &mdash; por isso esta via ainda vale depois de Unpaywall, OpenAlex, Semantic Scholar,
arXiv por titulo e OpenAIRE terem se esgotado.</p>
</header>
<nav class="nav"><a href="#topo">Resumo</a>%(nav)s<span class="prog" id="prog"></span></nav>
<main id="topo">

<div class="aviso">
<b>Como usar.</b> Clique em <b>Google Scholar</b>: se houver mais de uma copia, o resultado traz
&ldquo;Todas as N versoes&rdquo; logo abaixo do titulo &mdash; e ali que aparecem as copias de
repositorio e de pagina de autor. O link <b>PDF na web</b> faz a mesma busca restrita a arquivos
PDF. Marque a caixa quando resolver; o progresso fica salvo neste navegador.
</div>

<div class="aviso">
<b>Se nao render.</b> Para o grupo da Springer, a hipotese a confirmar antes de declarar perda e
institucional, nao bibliografica: as 19 referencias estao em series de <b>livro</b> (LNCS, LNNS,
CCIS, LNBIP, LNEE, LNDECT, LNICST), colecao distinta dos periodicos que o portal CAPES assina.
Confirmando com a biblioteca da UPE que nao ha assinatura dessa colecao, a exclusao por
indisponibilidade passa a ter justificativa documentada em vez de ficar como tentativa frustrada.
</div>

<table class="tb"><thead><tr><th>Grupo</th><th class="n">Artigos</th></tr></thead>
<tbody>%(tab)s</tbody></table>

%(blocos)s
</main>
<footer>Gerado a partir de custom_automated_search_collection.csv. Somente leitura: nada nesta
pagina altera a planilha. Links abrem em nova aba.</footer>
<script>__JS__</script>
"""

doc = (DOC % {'n': len(falta), 'nav': nav, 'tab': tab, 'blocos': ''.join(blocos)}
       ).replace('__CSS__', CSS).replace('__EXTRA__', EXTRA).replace('__JS__', JS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(doc)
print('gerado: %s | %d KB' % (OUT, len(doc) // 1024))
for c, t, n in resumo:
    print('  %-4s %-46s %d' % (c, t, n))
print('  total %d' % len(falta))
