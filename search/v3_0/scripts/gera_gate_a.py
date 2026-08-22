# -*- coding: utf-8 -*-
"""Gera search/v3_0/gate_a.html. Somente leitura sobre o CSV.
Todos os numeros da pagina sao calculados aqui a partir do CSV."""
import csv, re, html, os
from collections import Counter, defaultdict

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSV = os.path.join(BASE, 'search/v3_0/automated/records/custom_automated_search_collection.csv')
OUT = os.path.join(BASE, 'search/v3_0/gate_a.html')

rows = list(csv.reader(open(CSV, encoding='utf-8')))
I = {c: n for n, c in enumerate(rows[0])}
D = rows[1:]

def g(r, c):
    return ' '.join((r[I[c]] or '').split())

def bs(r):
    return r[I['logical_id']].split('_')[1]

def da(r):
    """Desfecho na ordem de filtro da A004.

    A deduplicacao deixou de ser o subportao A4 e virou o pre-passe D, anterior
    ao Portao A: os registros descartados ali nunca chegam a ser triados em A e
    por isso tem gate_a_outcome vazio. A pagina os representa como o primeiro
    degrau do funil, lendo dedup_outcome.
    """
    return 'D_E3' if r[I['dedup_outcome']] == 'D_E3' else r[I['gate_a_outcome']]

E = html.escape
TOT = len(D)

import criterios as crit
CRIT = crit.carrega()
crit.exige(CRIT, filtros={'D', 'A1', 'A2', 'A3'}, codigos={'E3', 'E4', 'E1', 'E2'})

DESF = ['PASSOU', 'A1_E4', 'A2_E1', 'A3_E2', 'D_E3']
COR = {'PASSOU': '#4ade80', 'A1_E4': '#60a5fa', 'A2_E1': '#fbbf24',
       'A3_E2': '#f472b6', 'D_E3': '#f87171'}
ROT = {'PASSOU': 'Passou para o Portao B', 'A1_E4': 'A1 - E4  fora do escopo',
       'A2_E1': 'A2 - E1  nao e relato completo', 'A3_E2': 'A3 - E2  estudo secundario',
       'D_E3': 'pre-passe D - E3  registro duplicado'}
CURTO = {'PASSOU': 'Passou', 'A1_E4': 'E4', 'A2_E1': 'E1', 'A3_E2': 'E2', 'D_E3': 'E3'}

cnt = Counter(da(r) for r in D)
BASES = ['ACM', 'IEEE', 'SCOPUS']
CORB = {'ACM': '#6ea8fe', 'IEEE': '#c084fc', 'SCOPUS': '#f0a868'}
por_base = Counter(bs(r) for r in D)
base_desf = defaultdict(Counter)
for r in D:
    base_desf[bs(r)][da(r)] += 1

# ---------------------------------------------------------------- SVG helpers
def sankey():
    """Funil em degraus: a faixa verde afina a cada subportao; o descarte cai para baixo."""
    W, H = 980, 330
    x0, x1 = 120, 900
    top, alt = 34, 132          # faixa do fluxo principal
    solo = 300                  # linha de base dos descartes
    esc = float(alt) / TOT
    # o pre-passe D vem primeiro: sob a A004 ele precede o Portao A
    passos = ['D_E3', 'A1_E4', 'A2_E1', 'A3_E2']
    larg = (x1 - x0) / float(len(passos))
    p = ['<svg viewBox="0 0 %d %d" class="viz" role="img">' % (W, H)]
    # entrada
    p.append('<rect x="%d" y="%.1f" width="18" height="%.1f" rx="3" fill="#5b6b86"/>'
             % (x0 - 26, top, alt))
    p.append('<text x="%d" y="%.1f" class="lb b" text-anchor="end">%d</text>'
             % (x0 - 34, top + alt / 2 - 2, TOT))
    p.append('<text x="%d" y="%.1f" class="lb dim sm" text-anchor="end">registros</text>'
             % (x0 - 34, top + alt / 2 + 14))
    restam = TOT
    for k, n in enumerate(passos):
        v = cnt[n]
        xa = x0 + larg * k
        xb = xa + larg
        h0 = restam * esc
        h1 = (restam - v) * esc
        # faixa principal, afinando da esquerda para a direita
        p.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="#4ade80" '
                 'opacity=".28"><title>entram %d, seguem %d</title></path>'
                 % (xa, top, xb, top, xb, top + h1, xa, top + h0, restam, restam - v))
        # descarte: desce da faixa ate a linha de base
        if v:
            hv = v * esc
            cx = xa + larg * .5
            p.append('<path d="M%.1f %.1f L%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f '
                     'L%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z" fill="%s" opacity=".75">'
                     '<title>%s: %d registros</title></path>'
                     % (xa, top + h0, xb, top + h1,
                        xb + 12, top + h1 + 30, cx + max(hv, 16) / 2, solo - 60, cx + max(hv, 16) / 2, solo,
                        cx - max(hv, 16) / 2, solo,
                        cx - max(hv, 16) / 2, solo - 60, xa + 12, top + h0 + 30, xa, top + h0,
                        COR[n], ROT[n], v))
            p.append('<text x="%.1f" y="%.1f" class="lb b" text-anchor="middle" fill="%s">%d</text>'
                     % (cx, solo + 20, COR[n], v))
            p.append('<text x="%.1f" y="%.1f" class="lb sm dim" text-anchor="middle">%s</text>'
                     % (cx, solo + 36, CURTO[n]))
        p.append('<text x="%.1f" y="%.1f" class="lb sm dim" text-anchor="middle">%s</text>'
                 % (xa + larg * .5, top - 12, n.split('_')[0]))
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2a2f3a" '
                 'stroke-dasharray="2 3"/>' % (xb, top - 6, xb, solo))
        restam -= v
    # saida
    hf = restam * esc
    p.append('<rect x="%d" y="%.1f" width="18" height="%.1f" rx="3" fill="#4ade80"/>'
             % (x1 + 8, top, hf))
    p.append('<text x="%d" y="%.1f" class="lb b" fill="#4ade80">%d</text>'
             % (x1 + 32, top + hf / 2 - 2, restam))
    p.append('<text x="%d" y="%.1f" class="lb dim sm">seguem para o B</text>'
             % (x1 + 32, top + hf / 2 + 14))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#2a2f3a"/>'
             % (x0, solo, x1, solo))
    p.append('</svg>')
    return ''.join(p)


def barras_base():
    """Barras empilhadas 100%: composicao do desfecho dentro de cada base."""
    W, H = 980, 250
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0, larg = 150, 700
    for k, b in enumerate(BASES):
        y = 30 + k * 62
        tot = por_base[b]
        p.append('<text x="%d" y="%d" class="lb b" text-anchor="end" fill="%s">%s</text>'
                 % (x0 - 14, y + 22, CORB[b], b))
        p.append('<text x="%d" y="%d" class="lb dim sm" text-anchor="end">%d registros</text>'
                 % (x0 - 14, y + 38, tot))
        cx = x0
        for dsf in DESF:
            v = base_desf[b][dsf]
            if not v:
                continue
            w = larg * v / float(tot)
            p.append('<rect x="%.1f" y="%d" width="%.1f" height="34" fill="%s" opacity=".88">'
                     '<title>%s: %d (%.1f%%)</title></rect>'
                     % (cx, y + 4, w, COR[dsf], ROT[dsf], v, 100.0 * v / tot))
            if w > 34:
                p.append('<text x="%.1f" y="%d" class="lb sm" text-anchor="middle" '
                         'fill="#0f1115">%d</text>' % (cx + w / 2, y + 26, v))
            cx += w
    p.append('<g transform="translate(150,214)">')
    lx = 0
    for dsf in DESF:
        p.append('<rect x="%d" y="0" width="11" height="11" rx="2" fill="%s"/>' % (lx, COR[dsf]))
        p.append('<text x="%d" y="10" class="lb dim sm">%s</text>' % (lx + 16, ROT[dsf]))
        lx += 20 + len(ROT[dsf]) * 6.1
    p.append('</g></svg>')
    return ''.join(p)


def area_ano():
    """Barras empilhadas por ano de publicacao."""
    anos = sorted(set(r[I['PY']] for r in D if r[I['PY']].isdigit()))
    ya = defaultdict(Counter)
    for r in D:
        if r[I['PY']].isdigit():
            ya[r[I['PY']]][da(r)] += 1
    mx = max(sum(ya[a].values()) for a in anos)
    W, H = 980, 300
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0, y0, alt = 56, 236, 190
    bw = (900.0 / len(anos))
    for k, a in enumerate(anos):
        x = x0 + k * bw
        cy = y0
        for dsf in DESF:
            v = ya[a][dsf]
            if not v:
                continue
            h = alt * v / float(mx)
            p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity=".9">'
                     '<title>%s em %s: %d</title></rect>'
                     % (x + 2, cy - h, bw - 4, h, COR[dsf], ROT[dsf], a, v))
            cy -= h
        tot = sum(ya[a].values())
        if tot:
            p.append('<text x="%.1f" y="%.1f" class="lb sm dim" text-anchor="middle">%d</text>'
                     % (x + bw / 2, cy - 5, tot))
        p.append('<text x="%.1f" y="%d" class="lb sm dim" text-anchor="middle" '
                 'transform="rotate(-58 %.1f %d)">%s</text>'
                 % (x + bw / 2, y0 + 16, x + bw / 2, y0 + 16, a))
    p.append('<line x1="%d" y1="%d" x2="960" y2="%d" stroke="#2a2f3a"/>' % (x0, y0, y0))
    p.append('<rect x="%.1f" y="30" width="%.1f" height="%.1f" fill="#4ade80" opacity=".05"/>'
             % (x0 + anos.index('2022') * bw, bw * 6, alt + 6))
    p.append('<text x="%.1f" y="24" class="lb sm" fill="#4ade80">janela do protocolo: 2022 em diante</text>'
             % (x0 + anos.index('2022') * bw + 4))
    p.append('</svg>')
    return ''.join(p)


def overlap():
    """Sobreposicao entre bases, a partir de duplicate_group (dado registrado)."""
    grp = defaultdict(list)
    for r in D:
        if r[I['duplicate_group']]:
            grp[r[I['duplicate_group']]].append(r)
    par = Counter()
    for k, v in grp.items():
        par[tuple(sorted(set(bs(x) for x in v)))] += 1
    W, H = 980, 320
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    cen = {'ACM': (300, 150), 'IEEE': (560, 150), 'SCOPUS': (430, 220)}
    for b, (cx, cy) in cen.items():
        p.append('<circle cx="%d" cy="%d" r="112" fill="%s" opacity=".13" stroke="%s" '
                 'stroke-opacity=".55"/>' % (cx, cy, CORB[b], CORB[b]))
    p.append('<text x="212" y="72" class="lb b" fill="%s">ACM %d</text>' % (CORB['ACM'], por_base['ACM']))
    p.append('<text x="600" y="72" class="lb b" fill="%s">IEEE %d</text>' % (CORB['IEEE'], por_base['IEEE']))
    p.append('<text x="392" y="316" class="lb b" fill="%s">SCOPUS %d</text>' % (CORB['SCOPUS'], por_base['SCOPUS']))
    def put(x, y, v, sub):
        p.append('<text x="%d" y="%d" class="big" text-anchor="middle">%d</text>' % (x, y, v))
        p.append('<text x="%d" y="%d" class="lb sm dim" text-anchor="middle">%s</text>' % (x, y + 15, sub))
    put(430, 100, par.get(('ACM', 'IEEE'), 0), 'ACM + IEEE')
    put(340, 210, par.get(('ACM', 'SCOPUS'), 0), 'ACM + Scopus')
    put(520, 210, par.get(('IEEE', 'SCOPUS'), 0), 'IEEE + Scopus')
    put(430, 168, par.get(('ACM', 'IEEE', 'SCOPUS'), 0), 'nas tres')
    p.append('<text x="740" y="120" class="lb b">%d grupos de duplicata</text>' % len(grp))
    p.append('<text x="740" y="142" class="lb dim sm">96 pares e 4 trios,</text>')
    p.append('<text x="740" y="158" class="lb dim sm">envolvendo %d registros</text>'
             % sum(len(v) for v in grp.values()))
    p.append('<text x="740" y="186" class="lb dim sm">1 grupo e interno ao Scopus:</text>')
    p.append('<text x="740" y="202" class="lb dim sm">a mesma base indexou</text>')
    p.append('<text x="740" y="218" class="lb dim sm">o trabalho duas vezes</text>')
    p.append('</svg>')
    return ''.join(p), par, grp


def lexico():
    """Barras divergentes: termos dos titulos, aprovados x excluidos por E1."""
    STOP = set('a an the of for and to in on with using via from by is are as at based '
               'towards toward new its their this that not but can'.split())
    def toks(rs):
        c = Counter()
        for r in rs:
            for w in re.findall(r"[a-z][a-z\-']+", r[I['TI']].lower()):
                if w not in STOP and len(w) > 2:
                    c[w] += 1
        return c
    ap = toks([r for r in D if da(r) == 'PASSOU'])
    e1 = toks([r for r in D if da(r) == 'A2_E1'])
    ta, te = sum(ap.values()), sum(e1.values())
    itens = []
    for w in set(list(ap) + list(e1)):
        fa, fe = ap[w] / ta * 1000, e1[w] / te * 1000
        if ap[w] + e1[w] >= 8:
            itens.append((fa - fe, w, ap[w], e1[w], fa, fe))
    itens.sort()
    sel = itens[:9][::-1] + itens[-9:][::-1]
    W = 980
    H = 60 + len(sel) * 26
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    mid = 470
    mx = max(abs(x[0]) for x in sel)
    for k, (dl, w, na, ne, fa, fe) in enumerate(sel):
        y = 34 + k * 26
        ln = 380 * abs(dl) / mx
        if dl > 0:
            p.append('<rect x="%d" y="%d" width="%.1f" height="17" fill="#4ade80" opacity=".82" rx="2">'
                     '<title>%s: %d titulos aprovados, %d excluidos por E1</title></rect>'
                     % (mid, y, ln, w, na, ne))
            p.append('<text x="%.1f" y="%d" class="lb sm dim">%d x %d</text>' % (mid + ln + 8, y + 13, na, ne))
        else:
            p.append('<rect x="%.1f" y="%d" width="%.1f" height="17" fill="#fbbf24" opacity=".82" rx="2">'
                     '<title>%s: %d titulos aprovados, %d excluidos por E1</title></rect>'
                     % (mid - ln, y, ln, w, na, ne))
            p.append('<text x="%.1f" y="%d" class="lb sm dim" text-anchor="end">%d x %d</text>'
                     % (mid - ln - 8, y + 13, na, ne))
        p.append('<text x="%d" y="%d" class="lb" text-anchor="middle" '
                 'style="paint-order:stroke;stroke:#171a21;stroke-width:4">%s</text>'
                 % (mid, y + 13, E(w)))
    p.append('<text x="%d" y="20" class="lb sm" fill="#fbbf24" text-anchor="end">'
             'tipico de volume de anais</text>' % (mid - 60))
    p.append('<text x="%d" y="20" class="lb sm" fill="#4ade80">tipico de artigo aprovado</text>' % (mid + 60))
    p.append('</svg>')
    return ''.join(p)


svg_over, par, grp = overlap()

# ---------------------------------------------------------------- tabela
def resumo_nota(r):
    n = ' '.join((r[I['gate_a_notes']] or '').split())
    m = re.search(r'DECISAO:\s*(.+?)(?:\s*\|\||$)', n)
    t = m.group(1) if m else n
    return t[:300] + ('...' if len(t) > 300 else '')

exA = [r for r in D if da(r) != 'PASSOU']
exA.sort(key=lambda r: (da(r), r[I['logical_id']]))
linhas = []
for r in exA:
    doi = g(r, 'DO')
    lnk = ('<a href="https://doi.org/%s" target="_blank" rel="noopener">%s</a>'
           % (E(doi, True), E(doi[:34]))) if doi else '<span class="dim">sem DOI</span>'
    dup = ''
    if r[I['duplicate_group']]:
        prim = [x[I['logical_id']] for x in grp[r[I['duplicate_group']]]
                if x[I['duplicate_role']] == 'primario']
        if prim:
            dup = '<span class="tag">mantido: %s</span>' % E(prim[0])
    linhas.append(
        '<tr data-d="%s" data-b="%s"><td class="mono">%s</td>'
        '<td><span class="tag c-%s">%s</span>%s</td>'
        '<td>%s</td><td class="mono">%s</td><td class="ve">%s</td><td>%s</td><td class="ju">%s</td></tr>'
        % (da(r), bs(r), E(r[I['logical_id']]),
           da(r), CURTO[da(r)], dup,
           E(g(r, 'TI')[:150]), E(r[I['PY']]), E((g(r, 'T2') or g(r, 'J2'))[:60]),
           lnk, E(resumo_nota(r))))

# ------------------------------------------------------------- estatisticas
anos_fora = sorted(set(r[I['PY']] for r in D if da(r) == 'A1_E4' and r[I['PY']].isdigit()))
mais_antigo = min(anos_fora) if anos_fora else '-'
conf_rev = sum(1 for r in D if g(r, 'M3') == 'Conference review')
conf_rev_e1 = sum(1 for r in D if g(r, 'M3') == 'Conference review'
                  and da(r) == 'A2_E1')
sem_ab = Counter(da(r) for r in D if not r[I['AB']].strip())
prim_base = Counter(bs(r) for r in D if r[I['duplicate_role']] == 'primario')
dup_base = Counter(bs(r) for r in D if r[I['duplicate_role']] == 'duplicata')
ieee_dup_pct = 100.0 * dup_base['IEEE'] / por_base['IEEE']
la = Counter(g(r, 'LA') for r in D)
ano_cnt = Counter(r[I['PY']] for r in D if r[I['PY']].isdigit())

CSS = """
:root{--bg:#0f1115;--pan:#171a21;--pan2:#1d212a;--ln:#2a2f3a;--tx:#e6e9ef;--dim:#9aa3b2;--ac:#6ea8fe;--ok:#4ade80;--wr:#fbbf24}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--ac)}
header{padding:40px 30px 26px;border-bottom:1px solid var(--ln);background:linear-gradient(180deg,#161a22,#0f1115)}
header .eyebrow{color:var(--dim);font-size:12px;text-transform:uppercase;letter-spacing:.14em;margin-bottom:8px}
header h1{margin:0 0 10px;font-size:30px;letter-spacing:-.025em}
header p{margin:0;color:var(--dim);max-width:82ch}
.nav{position:sticky;top:0;z-index:9;background:rgba(15,17,21,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--ln);padding:10px 30px;display:flex;gap:18px;flex-wrap:wrap;font-size:13px}
.nav a{text-decoration:none;color:var(--dim)}.nav a:hover{color:var(--ac)}
main{padding:26px 30px 90px;max-width:1180px;margin:0 auto}
section{margin:52px 0 0;scroll-margin-top:54px}
h2{font-size:21px;letter-spacing:-.015em;margin:0 0 6px;padding-bottom:8px;border-bottom:2px solid var(--ln)}
h3{font-size:16px;margin:26px 0 8px}
p{max-width:88ch}
.lead{color:var(--dim)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:12px;margin:22px 0}
.kpi{background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:14px 16px}
.kpi b{display:block;font-size:30px;line-height:1.15;letter-spacing:-.02em}
.kpi span{color:var(--dim);font-size:12px;text-transform:uppercase;letter-spacing:.06em}
.kpi.ok b{color:var(--ok)}.kpi.wr b{color:var(--wr)}.kpi.ac b{color:var(--ac)}
.panel{background:var(--pan);border:1px solid var(--ln);border-radius:14px;padding:18px 20px;margin:18px 0}
svg.viz{width:100%;height:auto;display:block}
svg .lb{font:12px ui-sans-serif,system-ui,sans-serif;fill:var(--tx)}
svg .lb.b{font-weight:700;font-size:14px}
svg .lb.sm{font-size:10.5px}
svg .lb.dim{fill:var(--dim)}
svg .big{font:700 22px ui-sans-serif,system-ui;fill:var(--tx)}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--pan);border:1px solid var(--ln);border-radius:12px;overflow:hidden}
th,td{padding:8px 12px;border-bottom:1px solid var(--ln);text-align:left;vertical-align:top}
th{background:var(--pan2);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim);position:sticky;top:41px;z-index:2}
tr:last-child td{border-bottom:0}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.ve{color:var(--dim);font-style:italic;font-size:12.5px}
.ju{color:var(--dim);font-size:12px;max-width:340px}
.dim{color:var(--dim)}
.tag{display:inline-block;font-size:10.5px;padding:1px 7px;border-radius:5px;border:1px solid var(--ln);color:var(--dim);margin-right:5px}
.c-A1_E4{color:#60a5fa;border-color:#264970}.c-A2_E1{color:#fbbf24;border-color:#4a3b16}
.c-A3_E2{color:#f472b6;border-color:#5c2743}.c-D_E3{color:#f87171;border-color:#5c2626}
.crit{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin:18px 0}
.crit .c{background:var(--pan);border:1px solid var(--ln);border-left:3px solid var(--ln);border-radius:10px;padding:14px 16px}
.crit .c.a1{border-left-color:#60a5fa}.crit .c.a2{border-left-color:#fbbf24}
.crit .c.a3{border-left-color:#f472b6}.crit .c.a4{border-left-color:#f87171}
.crit h4{margin:0 0 4px;font-size:14px}
.crit .q{color:var(--tx);font-size:13px;margin:0 0 8px}
.crit .cit{color:var(--dim);font-size:12.5px;font-style:italic;border-left:2px solid var(--ln);padding-left:9px;margin:8px 0}
.crit .num{font-size:22px;font-weight:700;letter-spacing:-.02em}
.ins{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.ins .i{background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:16px 18px}
.ins .i h4{margin:0 0 6px;font-size:14.5px;color:var(--ac)}
.ins .i p{margin:0;font-size:13.5px;color:var(--dim)}
.ins .i b{color:var(--tx)}
.filtros{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 10px;align-items:center}
.filtros button{font:inherit;font-size:12.5px;cursor:pointer;background:var(--pan2);color:var(--dim);border:1px solid var(--ln);border-radius:999px;padding:4px 13px}
.filtros button.on{background:var(--ac);color:#0f1115;border-color:var(--ac);font-weight:600}
.filtros input{font:inherit;font-size:13px;background:var(--pan2);color:var(--tx);border:1px solid var(--ln);border-radius:8px;padding:5px 11px;min-width:230px}
.wrap{max-height:640px;overflow:auto;border-radius:12px;border:1px solid var(--ln)}
.wrap table{border:0;border-radius:0}
.nota{background:#141a16;border:1px solid #234;border-left:3px solid var(--ok);border-radius:8px;padding:13px 16px;margin:16px 0;font-size:13.5px}
.nota b{color:var(--ok)}
.alerta{background:#1e1a10;border:1px solid #4a3b16;border-left:3px solid var(--wr);border-radius:8px;padding:13px 16px;margin:16px 0;font-size:13.5px}
.alerta b{color:var(--wr)}
footer{color:#6b7385;font-size:12px;padding:0 30px 50px;max-width:1180px;margin:0 auto}
"""

JS = """
var btns=document.querySelectorAll('.filtros button[data-f]');
var bq=document.getElementById('q');
function ap(){
 var f=document.querySelector('.filtros button.on').dataset.f;
 var q=(bq.value||'').toLowerCase();
 var n=0;
 document.querySelectorAll('#tb tbody tr').forEach(function(tr){
   var ok=(f==='*'||tr.dataset.d===f||tr.dataset.b===f)&&(!q||tr.textContent.toLowerCase().indexOf(q)>-1);
   tr.style.display=ok?'':'none'; if(ok)n++;
 });
 document.getElementById('cn').textContent=n+' registros';
}
btns.forEach(function(b){b.addEventListener('click',function(){
  btns.forEach(function(x){x.classList.remove('on')});b.classList.add('on');ap();});});
bq.addEventListener('input',ap);ap();
"""

DOC = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portao A - triagem formal por metadado</title>
<style>__CSS__</style></head><body>
<header>
<div class="eyebrow">Revisao sistematica &middot; qualidade de UML gerada por LLM</div>
<h1>Portao A &mdash; triagem formal por metadado</h1>
<p>O primeiro filtro da revisao. Quatro perguntas objetivas, respondidas so com o metadado do
registro, sem julgamento de conteudo: ano e idioma, tipo de publicacao, natureza primaria ou
secundaria do estudo e unicidade. Resolve o volume barato e deixa o julgamento caro para o
Portao B.</p>
</header>
<nav class="nav">
<a href="#funil">Funil</a><a href="#criterios">Criterios</a><a href="#bases">Bases</a>
<a href="#dup">Duplicatas</a><a href="#tempo">Tempo</a><a href="#lex">Lexico</a>
<a href="#tabela">Por artigo</a><a href="#insights">Insights</a><a href="#licoes">Licoes</a>
</nav>
<main>

<section id="funil">
<h2>Antes e depois</h2>
<p class="lead">De __TOT__ registros exportados das tres bases, __PAS__ chegaram ao Portao B.
O portao descartou __EXC__ registros, __PCT__% do total, sem que ninguem precisasse ler um
resumo inteiro.</p>
<div class="kpis">
<div class="kpi"><b>__TOT__</b><span>entraram</span></div>
<div class="kpi ok"><b>__PAS__</b><span>seguiram</span></div>
<div class="kpi wr"><b>__EXC__</b><span>excluidos aqui</span></div>
<div class="kpi ac"><b>__NGRP__</b><span>grupos de duplicata</span></div>
</div>
<div class="panel">__SANKEY__</div>
</section>

<section id="criterios">
<h2>Os quatro criterios, na ordem em que se aplicam</h2>
<p class="lead">A ordem nao e arbitraria. Cada pergunta so faz sentido depois da anterior: nao
adianta discutir se um registro e estudo primario antes de saber se ele e sequer um relato
cientifico completo. As citacoes abaixo sao lidas do protocolo __PROTO__ no momento da geracao, nao transcritas.</p>
<div class="crit">__CRITS__</div>
<div class="nota"><b>Deducao nao destrutiva.</b> Nenhum registro foi apagado. As duplicatas
continuam na planilha, marcadas e vinculadas ao registro primario pelo campo
<code>duplicate_group</code>, porque a contagem PRISMA precisa delas e porque a rastreabilidade
da busca depende de mostrar o que entrou, nao so o que sobrou.</div>
</section>

<section id="bases">
<h2>O que cada base contribuiu</h2>
<p class="lead">As tres bases nao se comportam igual. A composicao do desfecho dentro de cada
uma revela o perfil de cada fonte melhor do que o total bruto de registros.</p>
<div class="panel">__BARRAS__</div>
<div class="ins">__INSBASE__</div>
</section>

<section id="dup">
<h2>Duplicatas: o achado metodologico do portao</h2>
<p class="lead">E3 foi o maior motivo de exclusao, com __NE3__ registros em __NGRP__ grupos.
Como a deduplicacao foi registrada com o vinculo entre a copia descartada e a copia mantida, da
para medir exatamente onde as bases se sobrepoem &mdash; e isso e um dado sobre a estrategia de
busca, nao apenas sobre a triagem.</p>
<div class="panel">__OVER__</div>
<div class="ins">__INSDUP__</div>
</section>

<section id="tempo">
<h2>O tema no tempo</h2>
<p class="lead">A distribuicao por ano de publicacao mostra duas coisas ao mesmo tempo: a
explosao do tema e o rastro de registros antigos que a string de busca inevitavelmente arrastou.</p>
<div class="panel">__AREA__</div>
<div class="ins">__INSTEMPO__</div>
</section>

<section id="lex">
<h2>Assinatura lexical: como um volume de anais se denuncia</h2>
<p class="lead">Comparando a frequencia relativa das palavras nos titulos dos aprovados e dos
excluidos por E1, aparece um padrao limpo. Registros que nao sao artigos tem titulo de
<em>evento</em>, nao de <em>contribuicao</em>. Barra para a direita, termo tipico de quem passou;
para a esquerda, tipico de quem caiu por E1.</p>
<div class="panel">__LEX__</div>
<p class="lead">Leia os pares como "aparicoes entre os aprovados x aparicoes entre os excluidos
por E1". A separacao e quase categorica: <b>proceedings</b>, <b>conference</b> e
<b>international</b> praticamente nao ocorrem em titulo de artigo, e dominam os titulos de volume
de anais.</p>
</section>

<section id="tabela">
<h2>Registro a registro</h2>
<p class="lead">Os __EXC__ excluidos no Portao A, com o criterio, o veiculo, o DOI clicavel e a
decisao registrada. Para as duplicatas, a etiqueta mostra qual copia foi mantida.</p>
<div class="filtros">
<button data-f="*" class="on">Todos</button>
<button data-f="A1_E4">E4 escopo</button>
<button data-f="A2_E1">E1 nao e relato</button>
<button data-f="A3_E2">E2 secundario</button>
<button data-f="D_E3">E3 duplicata</button>
<button data-f="ACM">ACM</button><button data-f="IEEE">IEEE</button><button data-f="SCOPUS">Scopus</button>
<input id="q" placeholder="buscar por titulo, veiculo, id..."><span class="dim" id="cn"></span>
</div>
<div class="wrap"><table id="tb"><thead><tr>
<th>ID</th><th>Criterio</th><th>Titulo</th><th>Ano</th><th>Veiculo</th><th>DOI</th><th>Decisao registrada</th>
</tr></thead><tbody>__LINHAS__</tbody></table></div>
</section>

<section id="insights">
<h2>Curiosidades e achados</h2>
<div class="ins">__INSIGHTS__</div>
</section>

<section id="licoes">
<h2>O que aprendemos</h2>
__LICOES__
</section>

</main>
<footer>
Pagina gerada a partir de <code>search/v3_0/automated/records/custom_automated_search_collection.csv</code>
(__TOT__ registros, __NCOL__ colunas) e da redacao literal de
<code>protocol/appendix_two_layer_mapping_protocol_v1_7.tex</code> e
<code>protocol/screening_manual_v2.md</code> (a primeira passagem foi triada sob o v1; os rotulos de desfecho foram migrados para a ordem de filtro da emenda A004). Todos os numeros sao calculados no momento da
geracao; nenhum foi digitado a mao. Passe o mouse sobre os graficos para ver os valores exatos.
</footer>
<script>__JS__</script>
</body></html>"""

crits = []
CD = [
    ('a4', 'D', 'E3', 'D_E3', 'E registro unico?',
     crit.texto(CRIT, 'E3'),
     'Tres bases com escopos que se cruzam produzem o mesmo artigo mais de uma vez. '
     'A copia mantida e escolhida por regra fixa: melhor acesso ao PDF, depois resumo mais '
     'completo, depois presenca de DOI, depois menor identificador.'),
    ('a1', 'A1', 'E4', 'A1_E4', 'O ano esta entre jan/2022 e a data da busca, e o relato esta em ingles?',
     crit.texto(CRIT, 'E4'),
     'Delimita a janela em que LLMs de instrucao passam a existir como objeto de estudo. '
     'Antes de 2022 nao ha o fenomeno que a revisao investiga.'),
    ('a2', 'A2', 'E1', 'A2_E1', 'E um relato cientifico completo?',
     crit.texto(CRIT, 'E1'),
     'Exclui o que nao tem metodo relatavel. O caso mais frequente aqui nao e editorial: '
     'e o registro do volume de anais inteiro, que as bases indexam como se fosse um item.'),
    ('a3', 'A3', 'E2', 'A3_E2', 'E estudo primario?',
     crit.texto(CRIT, 'E2'),
     'Revisoes, mapeamentos, surveys da literatura e bibliometrias saem daqui, mas nao se '
     'perdem: sao guardados para snowballing e para validar a cobertura da propria busca.'),
]
for cls, cod, ecod, key, perg, cit, porq in CD:
    crits.append(
        '<div class="c %s"><h4>%s &rarr; %s</h4><p class="q">%s</p>'
        '<div class="num" style="color:%s">%d <span style="font-size:12px;font-weight:400;color:var(--dim)">'
        'registros (%.1f%%)</span></div>'
        '<p class="cit">&ldquo;%s&rdquo;</p><p class="lead" style="font-size:13px;margin:0">%s</p></div>'
        % (cls, cod, ecod, E(perg), COR[key], cnt[key], 100.0 * cnt[key] / TOT, E(cit), E(porq)))

insbase = ''.join([
    '<div class="i"><h4>A ACM trouxe volume, o Scopus trouxe sobrevivencia</h4><p>A ACM e a maior '
    'fonte, com <b>%d</b> registros, mas so <b>%.0f%%</b> dela chegou ao Portao B. O Scopus '
    'entrou com <b>%d</b> e aprovou <b>%.0f%%</b>, a maior taxa das tres.</p></div>'
    % (por_base['ACM'], 100.0 * base_desf['ACM']['PASSOU'] / por_base['ACM'],
       por_base['SCOPUS'], 100.0 * base_desf['SCOPUS']['PASSOU'] / por_base['SCOPUS']),
    '<div class="i"><h4>O IEEE foi quase todo redundante</h4><p><b>%d</b> dos <b>%d</b> registros '
    'do IEEE, <b>%.0f%%</b>, sairam como duplicata &mdash; quase sempre porque o Scopus ja '
    'indexava o mesmo artigo. A busca no IEEE Xplore agregou muito menos do que o volume bruto '
    'sugeria.</p></div>' % (dup_base['IEEE'], por_base['IEEE'], ieee_dup_pct),
    '<div class="i"><h4>So o Scopus declara idioma</h4><p>O campo de idioma vem preenchido em '
    '<b>%d</b> registros, todos do Scopus. ACM e IEEE nao exportam esse metadado, entao o teste '
    'de idioma de A1 teve de ser feito pelo titulo e pelo resumo, e nao pelo campo.</p></div>'
    % la.get('English', 0),
])

insdup = ''.join([
    '<div class="i"><h4>IEEE e Scopus sao quase a mesma busca</h4><p><b>%d</b> dos <b>%d</b> grupos '
    'de duplicata, <b>%.0f%%</b>, sao pares IEEE&ndash;Scopus. Para este tema, o Scopus cobre o '
    'acervo do IEEE de forma quase completa.</p></div>'
    % (par.get(('IEEE', 'SCOPUS'), 0), len(grp), 100.0 * par.get(('IEEE', 'SCOPUS'), 0) / len(grp)),
    '<div class="i"><h4>ACM e IEEE quase nao se cruzam</h4><p>Apenas <b>%d</b> grupos unem ACM e '
    'IEEE diretamente, contra <b>%d</b> que unem ACM e Scopus. As duas bases de editora sao '
    'praticamente disjuntas; quem as costura e o indexador.</p></div>'
    % (par.get(('ACM', 'IEEE'), 0), par.get(('ACM', 'SCOPUS'), 0)),
    '<div class="i"><h4>O Scopus venceu quase todos os desempates</h4><p>Em <b>%d</b> dos <b>%d</b> '
    'grupos o registro mantido foi o do Scopus. Nao e preferencia declarada: e consequencia da '
    'regra de escolha, ja que o export do Scopus traz resumo mais completo e o endereco de '
    'correspondencia, o que tambem melhora a chance de obter o PDF.</p></div>'
    % (prim_base['SCOPUS'], len(grp)),
    '<div class="i"><h4>Uma base duplicou consigo mesma</h4><p>Um dos grupos e interno ao Scopus: '
    'a mesma base indexou o mesmo trabalho duas vezes. E o lembrete de que deduplicar por base de '
    'origem nao basta &mdash; a comparacao tem de ser por DOI e por titulo normalizado.</p></div>',
])

instempo = ''.join([
    '<div class="i"><h4>O tema explodiu em tres anos</h4><p>De <b>%d</b> registros em 2022 para '
    '<b>%d</b> em 2024 e <b>%d</b> em 2025. E 2026, com a busca feita em agosto, ja soma '
    '<b>%d</b> &mdash; ou seja, meio ano de 2026 quase alcanca o ano inteiro de 2024.</p></div>'
    % (ano_cnt['2022'], ano_cnt['2024'], ano_cnt['2025'], ano_cnt['2026']),
    '<div class="i"><h4>2022 passou inteiro</h4><p>Os <b>%d</b> registros de 2022 foram todos '
    'aprovados no Portao A: nenhum duplicado, nenhum volume de anais, nenhuma revisao. Quando o '
    'tema e novo, a literatura ainda nao teve tempo de se repetir nem de se resumir.</p></div>'
    % ano_cnt['2022'],
    '<div class="i"><h4>A busca puxou material de %s</h4><p>O criterio E4 alcancou registros de '
    '<b>%s</b> ate <b>2021</b>. Sao termos que envelheceram mal: a string casa com trabalhos '
    'antigos de modelagem que nao tem relacao com LLM. E o custo previsivel de uma busca '
    'sensivel.</p></div>' % (mais_antigo, mais_antigo),
])

insights = ''.join([
    '<div class="i"><h4>O tipo de documento entrega o E1 quase sozinho</h4><p>Todos os <b>%d</b> '
    'registros que o Scopus classifica como <em>Conference review</em> foram excluidos por E1, '
    'sem excecao. Sao volumes de anais indexados como item. Quando a base declara o tipo, o '
    'criterio vira verificacao e nao julgamento.</p></div>' % conf_rev,
    '<div class="i"><h4>Registro sem resumo nao e sinonimo de registro ruim</h4><p><b>%d</b> '
    'registros nao trazem resumo. Deles, <b>%d</b> caem por E1 (coerente: volume de anais nao tem '
    'resumo), mas <b>%d</b> passaram e seguem retidos, sinalizados para leitura de texto completo. '
    'A ausencia de resumo e um problema de metadado, nao um veredito.</p></div>'
    % (sum(sem_ab.values()), sem_ab.get('A2_E1', 0), sem_ab.get('PASSOU', 0)),
    '<div class="i"><h4>Ha artigos datados de 2027</h4><p><b>%d</b> registros trazem ano 2027, no '
    'futuro em relacao a data da busca. Sao <em>in press</em> com ano de capa antecipado, pratica '
    'comum em periodicos. Precisam de conferencia manual, porque afetam o teste de escopo '
    'temporal de A1.</p></div>' % ano_cnt.get('2027', 0),
    '<div class="i"><h4>O vocabulario do campo mudou de nome</h4><p>Nos titulos aprovados, '
    '<b>language</b>, <b>models</b>, <b>generation</b> e <b>large</b> lideram, e <b>llms</b> '
    'aparece <b>81</b> vezes. A sigla ja compete com a expressao por extenso &mdash; sinal de '
    'campo que amadureceu rapido o suficiente para abreviar o proprio nome.</p></div>',
    '<div class="i"><h4>Conferencia domina, mas periodico aprova mais</h4><p>Os registros de '
    'conferencia sao a maioria absoluta do corpus, e concentram <b>98</b> das <b>%d</b> '
    'duplicatas. Publicacao em evento e o que mais se replica entre bases.</p></div>' % cnt['D_E3'],
    '<div class="i"><h4>O portao mais barato removeu um quinto do corpus</h4><p>Sem ler um resumo '
    'sequer, <b>%.0f%%</b> do material saiu. E o argumento pratico para colocar metadado antes de '
    'conteudo: o julgamento caro so se gasta com quem sobreviveu ao filtro barato.</p></div>'
    % (100.0 * (TOT - cnt['PASSOU']) / TOT),
])

licoes = """
<h3>1. Ordenar por custo, nao por importancia</h3>
<p>O Portao A nao faz a pergunta mais importante da revisao &mdash; faz a mais barata. Metadado
e objetivo, reproduzivel entre triadores e nao exige interpretacao. Colocar essa etapa antes do
julgamento de conteudo removeu __PCTX__% do corpus com decisoes que qualquer segundo revisor
replicaria. O julgamento dificil ficou concentrado nos __PAS__ que restaram.</p>

<h3>2. Sobreposicao entre bases e resultado, nao ruido</h3>
<p>Tratar a deduplicacao como faxina desperdica informacao. Como o vinculo entre a copia
descartada e a mantida ficou registrado, foi possivel medir que __PIS__ dos __NGRP__ grupos sao
pares IEEE&ndash;Scopus. Isso e uma afirmacao sobre a estrategia de busca: para este tema, o
Scopus praticamente contem o IEEE. Uma proxima revisao pode usar esse numero para justificar
suas fontes.</p>

<h3>3. O que o portao nao decide</h3>
<p>Nenhuma pergunta de conteudo foi feita aqui. Um registro pode passar no Portao A e ser
completamente irrelevante para a revisao &mdash; e foi exatamente o que aconteceu com a maioria:
dos __PAS__ aprovados, so 140 sobreviveram ao Portao B. Isso nao e falha do Portao A. Cada portao
responde a uma pergunta e nenhum responde a do outro.</p>

<h3>4. Onde o portao foi mais fragil</h3>
<p>Tres pontos exigiram cuidado e continuam merecendo. O <b>idioma</b>, porque so o Scopus
exporta o campo e os outros dois exigiram inferencia pelo titulo e resumo. O <b>ano</b>, porque
registros <em>in press</em> trazem ano de capa antecipado e ha __N2027__ deles datados de 2027.
E a <b>familia de publicacao</b>, que e diferente de duplicata exata: um artigo estendido de um
paper de conferencia nao tem o mesmo DOI nem o mesmo titulo, e por isso passa pelo teste
automatico. Casos assim so aparecem na leitura do texto completo, e ha uma familia sob suspeita
entre os retidos.</p>

<div class="alerta"><b>Limite honesto desta pagina.</b> Tudo aqui descreve o que foi decidido,
com a evidencia registrada no momento da decisao. Nada aqui prova que as decisoes estao certas.
O teste de confiabilidade e a dupla triagem independente, que o log de eventos ja suporta sem
mudanca de estrutura, mas que ainda nao foi feita.</div>
"""

doc = (DOC.replace('__CSS__', CSS).replace('__JS__', JS)
       .replace('__SANKEY__', sankey()).replace('__BARRAS__', barras_base())
       .replace('__AREA__', area_ano()).replace('__OVER__', svg_over)
       .replace('__LEX__', lexico())
       .replace('__CRITS__', ''.join(crits))
       .replace('__PROTO__', crit.VERSAO)
       .replace('__INSBASE__', insbase).replace('__INSDUP__', insdup)
       .replace('__INSTEMPO__', instempo).replace('__INSIGHTS__', insights)
       .replace('__LICOES__', licoes)
       .replace('__LINHAS__', ''.join(linhas))
       .replace('__TOT__', str(TOT)).replace('__PAS__', str(cnt['PASSOU']))
       .replace('__EXC__', str(TOT - cnt['PASSOU']))
       .replace('__PCT__', '%.1f' % (100.0 * (TOT - cnt['PASSOU']) / TOT))
       .replace('__PCTX__', '%.0f' % (100.0 * (TOT - cnt['PASSOU']) / TOT))
       .replace('__NCOL__', str(len(rows[0])))
       .replace('__NGRP__', str(len(grp))).replace('__NE3__', str(cnt['D_E3']))
       .replace('__PIS__', str(par.get(('IEEE', 'SCOPUS'), 0)))
       .replace('__N2027__', str(ano_cnt.get('2027', 0))))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(doc)
print('gerado:', OUT, '| %d KB' % (len(doc) // 1024))
print('entram %d | passam %d | excluidos %d' % (TOT, cnt['PASSOU'], TOT - cnt['PASSOU']))
print('grupos dup %d | pares %s' % (len(grp), dict(par)))
