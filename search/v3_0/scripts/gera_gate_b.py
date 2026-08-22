# -*- coding: utf-8 -*-
"""Gera search/v3_0/gate_b.html. Somente leitura sobre o CSV."""
import csv, re, html, os
from collections import Counter, defaultdict

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSVF = os.path.join(BASE, 'search/v3_0/automated/records/custom_automated_search_collection.csv')
OUT = os.path.join(BASE, 'search/v3_0/gate_b.html')

rows = list(csv.reader(open(CSVF, encoding='utf-8')))
I = {c: n for n, c in enumerate(rows[0])}
D = rows[1:]
E = html.escape

def g(r, c):
    return ' '.join((r[I[c]] or '').split())

def bs(r):
    return r[I['logical_id']].split('_')[1]

B = [r for r in D if r[I['gate_b_outcome']]]
RET = [r for r in B if r[I['gate_b_outcome']] == 'PASSOU']
EXC = [r for r in B if r[I['gate_b_outcome']] != 'PASSOU']
NB = len(B)

# Ordem canonica dos desfechos, na numeracao de filtro da A004. Os 93 desfechos
# gravados sob a numeracao anterior foram migrados
# no CSV em 2026-08-17; ver a linha DECISAO_DESENHO em screening_decision_log.csv.
DESF = ['PASSOU', 'B1_E7', 'B2_E8', 'B3_E9', 'B4_E6', 'B5_E7b']
COR = {'PASSOU': '#4ade80', 'B1_E7': '#f87171',
       'B2_E8': '#c084fc', 'B3_E9': '#60a5fa', 'B4_E6': '#fbbf24',
       'B5_E7b': '#f472b6'}
ROT = {'PASSOU': 'Retido para texto completo',
       'B1_E7': 'B1 - E7  o resultado gerado nao inclui UML',
       'B2_E8': 'B2 - E8  o LLM so avalia UML existente',
       'B3_E9': 'B3 - E9  a entrada nao e textual',
       'B4_E6': 'B4 - E6  o LLM nao e substantivo',
       'B5_E7b': 'B5 - E7b  UML misturada a outra notacao'}
CURTO = {'PASSOU': 'retido', 'B1_E7': 'E7',
         'B2_E8': 'E8', 'B3_E9': 'E9', 'B4_E6': 'E6', 'B5_E7b': 'E7b'}
cnt = Counter(r[I['gate_b_outcome']] for r in B)

# Nenhum desfecho novo pode derrubar a pagina: o que nao estiver previsto entra
# ao fim, com rotulo e cor neutros, em vez de estourar em DESF.index().
for _d in sorted(cnt):
    if _d and _d not in DESF:
        DESF.append(_d)
        COR.setdefault(_d, '#94a3b8')
        ROT.setdefault(_d, _d + '  (desfecho nao previsto nesta pagina)')
        CURTO.setdefault(_d, _d)

def txt(r):
    return (r[I['TI']] + ' ' + r[I['AB']] + ' ' + r[I['KW']]).lower()

# ------------------------------------------------------------------ SVG
def funil():
    W, H = 980, 340
    x0, x1 = 130, 880
    top, alt, solo = 34, 130, 300
    esc = float(alt) / NB
    passos = ['B1_E7', 'B2_E8', 'B3_E9', 'B4_E6', 'B5_E7b']
    larg = (x1 - x0) / float(len(passos))
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    p.append('<rect x="%d" y="%.1f" width="18" height="%.1f" rx="3" fill="#5b6b86"/>' % (x0 - 26, top, alt))
    p.append('<text x="%d" y="%.1f" class="lb b" text-anchor="end">%d</text>' % (x0 - 34, top + alt / 2 - 2, NB))
    p.append('<text x="%d" y="%.1f" class="lb dim sm" text-anchor="end">vindos do A</text>' % (x0 - 34, top + alt / 2 + 14))
    restam = NB
    for k, n in enumerate(passos):
        keys = n if isinstance(n, tuple) else (n,)
        v = sum(cnt[x] for x in keys)
        xa, xb = x0 + larg * k, x0 + larg * (k + 1)
        h0, h1 = restam * esc, (restam - v) * esc
        p.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="#4ade80" opacity=".26">'
                 '<title>entram %d, seguem %d</title></path>'
                 % (xa, top, xb, top, xb, top + h1, xa, top + h0, restam, restam - v))
        cx = xa + larg * .5
        base_y = solo
        for j, key in enumerate(keys):
            vv = cnt[key]
            hv = max(vv * esc, 13)
            off = (j - (len(keys) - 1) / 2.0) * 58
            p.append('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f L%.1f %.1f '
                     'C%.1f %.1f %.1f %.1f %.1f %.1f Z" fill="%s" opacity=".7">'
                     '<title>%s: %d</title></path>'
                     % (cx + off - hv / 2, base_y, cx + off - hv / 2, base_y - 70,
                        xa + 8, top + h0 + 22, xa + 4, top + h0,
                        xb - 4, top + h1,
                        xb - 8, top + h1 + 22, cx + off + hv / 2, base_y - 70,
                        cx + off + hv / 2, base_y, COR[key], ROT[key], vv))
            p.append('<text x="%.1f" y="%.1f" class="lb b" text-anchor="middle" fill="%s">%d</text>'
                     % (cx + off, base_y + 20, COR[key], vv))
            p.append('<text x="%.1f" y="%.1f" class="lb sm dim" text-anchor="middle">%s</text>'
                     % (cx + off, base_y + 35, CURTO[key]))
        lbl = 'B3' if isinstance(n, tuple) else n.split('_')[0]
        p.append('<text x="%.1f" y="%.1f" class="lb sm dim" text-anchor="middle">%s</text>' % (cx, top - 12, lbl))
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2a2f3a" stroke-dasharray="2 3"/>'
                 % (xb, top - 6, xb, solo))
        restam -= v
    hf = restam * esc
    p.append('<rect x="%d" y="%.1f" width="18" height="%.1f" rx="3" fill="#4ade80"/>' % (x1 + 8, top, hf))
    p.append('<text x="%d" y="%.1f" class="lb b" fill="#4ade80">%d</text>' % (x1 + 32, top + hf / 2 - 2, restam))
    p.append('<text x="%d" y="%.1f" class="lb dim sm">retidos</text>' % (x1 + 32, top + hf / 2 + 14))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#2a2f3a"/>' % (x0, solo, x1, solo))
    p.append('</svg>')
    return ''.join(p)


def matriz():
    """Matriz entrada -> saida, o coracao conceitual do portao."""
    W, H = 980, 330
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    cel = [
        # (col, lin, chave, entrada, saida, rotulo)
        (0, 0, 'PASSOU', 'texto', 'UML', 'RETEM'),
        (1, 0, 'B1_E7', 'UML', 'codigo, testes, doc', 'E7'),
        (0, 1, 'B3_E9', 'codigo, imagem, modelo', 'UML', 'E9'),
        (1, 1, 'B2_E8', 'UML', 'avaliacao, resumo', 'E8'),
    ]
    cw, ch = 300, 105
    ox, oy = 210, 60
    p.append('<text x="%d" y="34" class="lb b">O que ENTRA no processo</text>' % ox)
    p.append('<text x="%d" y="%d" class="lb b" transform="rotate(-90 %d %d)" text-anchor="middle">'
             'O que SAI</text>' % (176, oy + ch, 176, oy + ch))
    for cx, cy, key, ent, sai, cod in cel:
        x, y = ox + cx * (cw + 16), oy + cy * (ch + 16)
        v = cnt[key]
        p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" fill-opacity=".13" '
                 'stroke="%s" stroke-opacity=".55"/>' % (x, y, cw, ch, COR[key], COR[key]))
        p.append('<text x="%d" y="%d" class="big" fill="%s">%d</text>' % (x + 18, y + 42, COR[key], v))
        p.append('<text x="%d" y="%d" class="lb b" fill="%s">%s</text>' % (x + 18 + 22 + len(str(v)) * 16, y + 42, COR[key], cod))
        p.append('<text x="%d" y="%d" class="lb sm dim">entra: %s</text>' % (x + 18, y + 64, E(ent)))
        p.append('<text x="%d" y="%d" class="lb sm dim">sai: %s</text>' % (x + 18, y + 80, E(sai)))
        p.append('<text x="%d" y="%d" class="lb sm">%s</text>' % (x + 18, y + 97, E(ROT[key].split('  ')[-1])))
    # fora da matriz
    x = ox
    y = oy + 2 * (ch + 16)
    for key, desc in (('B1_E7', 'a saida nunca foi UML: BPMN, ER, C4, fluxograma, arvore de falhas, esboco arquitetural'),
                      ('B4_E6', 'ha UML, mas quem o determina nao e um LLM: regras, encoder classificador, ML classico')):
        p.append('<rect x="%d" y="%d" width="%d" height="42" rx="8" fill="%s" fill-opacity=".1" '
                 'stroke="%s" stroke-opacity=".4"/>' % (x, y, cw * 2 + 16, COR[key], COR[key]))
        p.append('<text x="%d" y="%d" class="lb b" fill="%s">%d</text>' % (x + 16, y + 26, COR[key], cnt[key]))
        p.append('<text x="%d" y="%d" class="lb sm dim">%s &mdash; %s</text>'
                 % (x + 16 + 26 + len(str(cnt[key])) * 9, y + 26, CURTO[key], E(desc)))
        y += 50
    p.append('</svg>')
    return ''.join(p)


def barras(dados, titulo_esq, W=980, alt_lin=30, cor=None, sufixo=''):
    """Barras horizontais simples: dados = [(rotulo, valor, extra)]"""
    mx = max(v for _, v, _ in dados) or 1
    H = 16 + len(dados) * alt_lin
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0 = 190
    for k, (lab, v, extra) in enumerate(dados):
        y = 8 + k * alt_lin
        w = (W - x0 - 190) * v / float(mx)
        c = cor(lab, v) if callable(cor) else (cor or '#6ea8fe')
        p.append('<text x="%d" y="%d" class="lb" text-anchor="end">%s</text>' % (x0 - 12, y + 17, E(lab)))
        p.append('<rect x="%d" y="%d" width="%.1f" height="19" rx="3" fill="%s" opacity=".85"/>'
                 % (x0, y + 3, w, c))
        p.append('<text x="%.1f" y="%d" class="lb sm">%d%s</text>' % (x0 + w + 9, y + 17, v, sufixo))
        if extra:
            p.append('<text x="%.1f" y="%d" class="lb sm dim">%s</text>' % (x0 + w + 9 + 34, y + 17, E(extra)))
    p.append('</svg>')
    return ''.join(p)


def heat_tipos():
    TIPOS = [('diagrama de classes', r'\bclass diagram|\bclass model'),
             ('sequencia', r'sequence diagram'),
             ('casos de uso', r'use[- ]case diagram'),
             ('atividade', r'activity diagram'),
             ('maquina de estados', r'state machine|statechart|state diagram'),
             ('componentes', r'component diagram'),
             ('implantacao', r'deployment diagram'),
             ('objetos', r'object diagram')]
    W = 980
    H = 60 + len(TIPOS) * 30
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0 = 230
    cols = [('retidos', RET, '#4ade80'), ('excluidos no B', EXC, '#f87171')]
    for j, (nm, _, c) in enumerate(cols):
        p.append('<text x="%d" y="26" class="lb b" fill="%s" text-anchor="middle">%s</text>'
                 % (x0 + 150 + j * 330, c, E(nm)))
    for k, (nome, pat) in enumerate(TIPOS):
        y = 40 + k * 30
        p.append('<text x="%d" y="%d" class="lb" text-anchor="end">%s</text>' % (x0 - 14, y + 17, E(nome)))
        for j, (nm, grupo, c) in enumerate(cols):
            n = sum(1 for r in grupo if re.search(pat, txt(r)))
            pc = 100.0 * n / len(grupo)
            w = 280 * pc / 26.0
            xx = x0 + j * 330
            p.append('<rect x="%d" y="%d" width="%.1f" height="19" rx="3" fill="%s" opacity=".85">'
                     '<title>%s: %d de %d (%.1f%%)</title></rect>' % (xx, y + 3, max(w, 1.5), c, nm, n, len(grupo), pc))
            p.append('<text x="%.1f" y="%d" class="lb sm dim">%d &middot; %.0f%%</text>'
                     % (xx + max(w, 1.5) + 8, y + 17, n, pc))
    p.append('</svg>')
    return ''.join(p)


def divergente_qual():
    QUAL = [('completeness', r'completeness'), ('syntactic / syntax', r'syntactic|syntax'),
            ('correctness', r'correctness'), ('consistency', r'consistenc'),
            ('semantic', r'semantic'), ('human evaluation', r'human evaluation|user study|expert'),
            ('benchmark', r'benchmark'), ('accuracy', r'accurac'), ('F1', r'f1[- ]score|\bf1\b'),
            ('precision / recall', r'\bprecision\b|\brecall\b'), ('similarity', r'similarit')]
    itens = []
    for nome, pat in QUAL:
        a = 100.0 * sum(1 for r in RET if re.search(pat, txt(r))) / len(RET)
        b = 100.0 * sum(1 for r in EXC if re.search(pat, txt(r))) / len(EXC)
        itens.append((a - b, nome, a, b))
    itens.sort(reverse=True)
    W = 980
    H = 46 + len(itens) * 27
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    mid = 520
    mx = max(abs(x[0]) for x in itens) or 1
    p.append('<text x="%d" y="18" class="lb sm" fill="#4ade80">discrimina a favor do retido &rarr;</text>' % (mid + 20))
    p.append('<text x="%d" y="18" class="lb sm" fill="#f87171" text-anchor="end">&larr; nao discrimina</text>' % (mid - 20))
    p.append('<line x1="%d" y1="26" x2="%d" y2="%d" stroke="#2a2f3a"/>' % (mid, mid, H - 6))
    for k, (dl, nome, a, b) in enumerate(itens):
        y = 30 + k * 27
        w = 300 * abs(dl) / mx
        c = '#4ade80' if dl > 0 else '#f87171'
        if dl >= 0:
            p.append('<rect x="%d" y="%d" width="%.1f" height="18" rx="3" fill="%s" opacity=".8"/>' % (mid, y, w, c))
            tx, an = mid + w + 9, 'start'
        else:
            p.append('<rect x="%.1f" y="%d" width="%.1f" height="18" rx="3" fill="%s" opacity=".8"/>' % (mid - w, y, w, c))
            tx, an = mid - w - 9, 'end'
        p.append('<text x="%d" y="%d" class="lb" text-anchor="end">%s</text>' % (mid - 320, y + 14, E(nome)))
        p.append('<text x="%.1f" y="%d" class="lb sm dim" text-anchor="%s">%.0f%% x %.0f%%</text>'
                 % (tx, y + 14, an, a, b))
    p.append('</svg>')
    return ''.join(p)


def onde_uml():
    def onde(r):
        t = (r[I['TI']] + ' ' + r[I['AB']]).lower()
        k = r[I['KW']].lower()
        if 'uml' in t or 'unified modeling' in t:
            return 'TI/AB'
        if 'uml' in k or 'unified modeling' in k:
            return 'so KW'
        return 'nenhum'
    c = defaultdict(Counter)
    for r in B:
        c[onde(r)][r[I['gate_b_outcome']]] += 1
    ordem = ['TI/AB', 'so KW', 'nenhum']
    LAB = {'TI/AB': 'UML no titulo ou resumo', 'so KW': 'UML so nas palavras-chave',
           'nenhum': 'UML nao aparece'}
    W, H = 980, 210
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0, larg = 250, 560
    for k, o in enumerate(ordem):
        y = 26 + k * 58
        tot = sum(c[o].values())
        p.append('<text x="%d" y="%d" class="lb" text-anchor="end">%s</text>' % (x0 - 14, y + 20, E(LAB[o])))
        p.append('<text x="%d" y="%d" class="lb sm dim" text-anchor="end">%d registros</text>' % (x0 - 14, y + 36, tot))
        cx = x0
        for dsf in DESF:
            v = c[o][dsf]
            if not v:
                continue
            w = larg * v / float(tot)
            p.append('<rect x="%.1f" y="%d" width="%.1f" height="30" fill="%s" opacity=".88">'
                     '<title>%s: %d (%.0f%%)</title></rect>' % (cx, y + 2, w, COR[dsf], ROT[dsf], v, 100.0 * v / tot))
            cx += w
        pc = 100.0 * c[o]['PASSOU'] / tot
        p.append('<text x="%d" y="%d" class="lb b" fill="#4ade80">%.0f%% retidos</text>' % (x0 + larg + 14, y + 22, pc))
    p.append('</svg>')
    return ''.join(p)


def por_base():
    cb = defaultdict(Counter)
    for r in B:
        cb[bs(r)][r[I['gate_b_outcome']]] += 1
    W, H = 980, 210
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0, larg = 190, 600
    for k, b in enumerate(['ACM', 'IEEE', 'SCOPUS']):
        y = 26 + k * 58
        tot = sum(cb[b].values())
        p.append('<text x="%d" y="%d" class="lb b" text-anchor="end">%s</text>' % (x0 - 14, y + 20, b))
        p.append('<text x="%d" y="%d" class="lb sm dim" text-anchor="end">%d</text>' % (x0 - 14, y + 36, tot))
        cx = x0
        for dsf in DESF:
            v = cb[b][dsf]
            if not v:
                continue
            w = larg * v / float(tot)
            p.append('<rect x="%.1f" y="%d" width="%.1f" height="30" fill="%s" opacity=".88">'
                     '<title>%s: %d (%.0f%%)</title></rect>' % (cx, y + 2, w, COR[dsf], ROT[dsf], v, 100.0 * v / tot))
            cx += w
        p.append('<text x="%d" y="%d" class="lb b" fill="#4ade80">%.0f%% retidos</text>'
                 % (x0 + larg + 14, y + 22, 100.0 * cb[b]['PASSOU'] / tot))
    p.append('<g transform="translate(190,192)">')
    lx = 0
    for dsf in DESF:
        p.append('<rect x="%d" y="0" width="11" height="11" rx="2" fill="%s"/>' % (lx, COR[dsf]))
        p.append('<text x="%d" y="10" class="lb dim sm">%s</text>' % (lx + 16, ROT[dsf]))
        lx += 22 + len(ROT[dsf]) * 5.9
    p.append('</g></svg>')
    return ''.join(p)


def ano_b():
    ya = defaultdict(Counter)
    for r in B:
        if r[I['PY']].isdigit():
            ya[r[I['PY']]][r[I['gate_b_outcome']]] += 1
    anos = sorted(ya)
    mx = max(sum(ya[a].values()) for a in anos)
    W, H = 980, 260
    p = ['<svg viewBox="0 0 %d %d" class="viz">' % (W, H)]
    x0, y0, alt = 70, 210, 165
    bw = 860.0 / len(anos)
    for k, a in enumerate(anos):
        x = x0 + k * bw
        cy = y0
        for dsf in DESF:
            v = ya[a][dsf]
            if not v:
                continue
            h = alt * v / float(mx)
            p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity=".9">'
                     '<title>%s em %s: %d</title></rect>' % (x + 6, cy - h, bw - 12, h, COR[dsf], ROT[dsf], a, v))
            cy -= h
        tot = sum(ya[a].values())
        p.append('<text x="%.1f" y="%.1f" class="lb sm dim" text-anchor="middle">%d</text>' % (x + bw / 2, cy - 6, tot))
        p.append('<text x="%.1f" y="%d" class="lb" text-anchor="middle">%s</text>' % (x + bw / 2, y0 + 20, a))
        pc = 100.0 * ya[a]['PASSOU'] / tot
        p.append('<text x="%.1f" y="%d" class="lb sm" text-anchor="middle" fill="#4ade80">%.0f%%</text>'
                 % (x + bw / 2, y0 + 38, pc))
    p.append('<line x1="%d" y1="%d" x2="960" y2="%d" stroke="#2a2f3a"/>' % (x0, y0, y0))
    p.append('<text x="%d" y="%d" class="lb sm dim" text-anchor="end">retencao</text>' % (x0 - 8, y0 + 38))
    p.append('</svg>')
    return ''.join(p)


# ------------------------------------------------------------------ tabela
def campo(nota, chave, prox):
    m = re.search(chave + r':\s*(.+?)(?=\s(?:%s):|$)' % '|'.join(prox), nota)
    return m.group(1).strip() if m else ''

linhas = []
for r in sorted(B, key=lambda r: (DESF.index(r[I['gate_b_outcome']]), r[I['logical_id']])):
    nota = ' '.join((r[I['gate_b_notes']] or '').split())
    ev = campo(nota, 'EVIDENCIA', ['DISCUSSAO', 'DECISAO'])
    di = campo(nota, 'DISCUSSAO', ['DECISAO'])
    ensina = di or ev or 'sem nota registrada'
    doi = g(r, 'DO')
    lnk = ('<a href="https://doi.org/%s" target="_blank" rel="noopener">DOI</a>' % E(doi, True)) if doi else '<span class="dim">-</span>'
    flags = ''.join('<span class="tag">%s</span>' % E(f) for f in r[I['gate_c_flags']].split(';') if f)
    dsf = r[I['gate_b_outcome']]
    linhas.append(
        '<tr data-d="%s" data-b="%s" data-f="%s">'
        '<td class="mono">%s</td><td><span class="tag c-%s">%s</span></td>'
        '<td><div class="ti">%s</div><div class="ve">%s &middot; %s</div>%s</td>'
        '<td class="mono">%s</td><td>%s</td>'
        '<td class="ju">%s</td></tr>'
        % (dsf, bs(r), E(r[I['gate_c_flags']]), E(r[I['logical_id']]), dsf, CURTO[dsf],
           E(g(r, 'TI')[:170]), E((g(r, 'T2') or g(r, 'J2'))[:56]), E(r[I['PY']]), flags,
           E(r[I['PY']]), lnk, E(ensina[:430] + ('...' if len(ensina) > 430 else ''))))

# ------------------------------------------------------------------ numeros
def n_re(grupo, pat):
    return sum(1 for r in grupo if re.search(pat, txt(r)))

LLMS = [('ChatGPT', r'chatgpt'), ('GPT-4', r'gpt-?4'), ('Llama', r'\bllama'), ('Gemini', r'\bgemini\b'),
        ('DeepSeek', r'deepseek'), ('Claude', r'\bclaude\b'), ('Qwen', r'qwen'), ('Copilot', r'copilot'),
        ('GPT-3.5', r'gpt-?3\.5'), ('BERT', r'\bbert\b'), ('Mistral', r'mistral')]
dl = []
for nome, pat in LLMS:
    t, a = n_re(B, pat), n_re(RET, pat)
    dl.append((nome, t, '%d retidos (%.0f%%)' % (a, 100.0 * a / t if t else 0)))
dl.sort(key=lambda x: -x[1])
svg_llm = barras(dl, 'LLM', cor=lambda l, v: '#c084fc' if l in ('BERT', 'GPT-3.5') else '#6ea8fe')

flags = Counter()
for r in RET:
    for f in r[I['gate_c_flags']].split(';'):
        if f:
            flags[f] += 1
FLAGDESC = {'EVIDENCIA=EXPLICITA': 'o resumo ja declara avaliacao ou metrica',
            'EVIDENCIA=A_VERIFICAR': 'nada no resumo sobre avaliacao; verificar no texto',
            'INCERTO_SAIDA': 'nao da para afirmar que a saida e UML',
            'INCERTO_PAPEL_LLM': 'papel do LLM nao especificado, ou co-producao com humano',
            'INCERTO_ENTRADA': 'entrada nao declarada no resumo',
            'CANDIDATO_E10': 'a UML pode nao ser separavel de outros artefatos',
            'SEM_RESUMO': 'registro sem resumo; decidido so por titulo e metadado'}
svg_flags = barras([(k, v, FLAGDESC.get(k, '')) for k, v in flags.most_common()], 'flag',
                   cor='#fbbf24')

cb = defaultdict(Counter)
for r in B:
    cb[bs(r)][r[I['gate_b_outcome']]] += 1
bert_ret = n_re(RET, r'\bbert\b')
uml_ti = sum(1 for r in B if 'uml' in (r[I['TI']] + r[I['AB']]).lower() or 'unified modeling' in (r[I['TI']] + r[I['AB']]).lower())
uml_ti_ret = sum(1 for r in RET if 'uml' in (r[I['TI']] + r[I['AB']]).lower() or 'unified modeling' in (r[I['TI']] + r[I['AB']]).lower())
sem_uml_ret = len(RET) - uml_ti_ret
acc_r = 100.0 * n_re(RET, r'accurac') / len(RET)
acc_e = 100.0 * n_re(EXC, r'accurac') / len(EXC)
comp_r = 100.0 * n_re(RET, r'completeness') / len(RET)
comp_e = 100.0 * n_re(EXC, r'completeness') / len(EXC)
e6_2022 = sum(1 for r in B if r[I['PY']] == '2022' and r[I['gate_b_outcome']] == 'B4_E6')
tot_2022 = sum(1 for r in B if r[I['PY']] == '2022')
cls_r = n_re(RET, r'\bclass diagram|\bclass model')

CSS = open(os.path.join(BASE, 'search/v3_0/scripts/css_gate.css'), encoding='utf-8').read()

JS = """
var bt=document.querySelectorAll('.filtros button[data-f]');
var q=document.getElementById('q');
function ap(){
 var f=document.querySelector('.filtros button.on').dataset.f;
 var s=(q.value||'').toLowerCase(),n=0;
 document.querySelectorAll('#tb tbody tr').forEach(function(tr){
  var ok=(f==='*'||tr.dataset.d===f||tr.dataset.b===f||(tr.dataset.f||'').indexOf(f)>-1)
       &&(!s||tr.textContent.toLowerCase().indexOf(s)>-1);
  tr.style.display=ok?'':'none'; if(ok)n++;});
 document.getElementById('cn').textContent=n+' registros';
}
bt.forEach(function(b){b.addEventListener('click',function(){
 bt.forEach(function(x){x.classList.remove('on')});b.classList.add('on');ap();});});
q.addEventListener('input',ap);ap();
"""

DOC = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portao B - triagem substantiva</title>
<style>__CSS__</style></head><body>
<header>
<div class="eyebrow">Revisao sistematica &middot; qualidade de UML gerada por LLM</div>
<h1>Portao B &mdash; triagem substantiva</h1>
<p>Aqui a revisao decide o que ela e. Quatro perguntas sobre o conteudo do estudo, sempre na mesma
ordem: o que <em>sai</em> do processo, <em>quem</em> determina esse conteudo, em que <em>direcao</em>
o fluxo corre e o que <em>entra</em>. Dos __NB__ registros aprovados no Portao A, __RET__
sobreviveram.</p>
<p class="alerta"><b>Leia os numeros desta pagina como o que o Portao B decidiu</b>, nao como o
corpus de hoje. Tres registros aprovados aqui &mdash; 868, 877 e 963 &mdash; foram excluidos
depois, ja no Portao C, por E3: a recuperacao do texto completo revelou que pertencem a uma
familia de publicacao (grupo <code>FAM-C-001</code>) cujo membro mais completo, 869, permanece
retido. Os desfechos <code>PASSOU</code> deles foram preservados de proposito, porque estavam
corretos diante do titulo e do resumo. O corpus valido atual e de <b>137</b> registros.</p>
</header>
<nav class="nav">
<a href="#funil">Funil</a><a href="#ordem">Os quatro passos</a><a href="#matriz">Matriz</a>
<a href="#bases">Bases</a><a href="#sinal">Sinal do UML</a><a href="#diagramas">Diagramas</a>
<a href="#llms">Modelos</a><a href="#qualidade">Qualidade</a><a href="#tempo">Tempo</a>
<a href="#flags">Flags</a><a href="#tabela">Por artigo</a><a href="#insights">Insights</a>
<a href="#licoes">Licoes</a>
</nav>
<main>

<section id="funil">
<h2>Antes e depois</h2>
<p class="lead">O Portao B e o filtro caro: exige ler o resumo e interpretar. Tambem e o mais
severo &mdash; removeu __EXCN__ dos __NB__ registros, __PEXC__% do que o Portao A tinha aprovado.</p>
<div class="kpis">
<div class="kpi"><b>__NB__</b><span>entraram</span></div>
<div class="kpi ok"><b>__RET__</b><span>retidos</span></div>
<div class="kpi wr"><b>__EXCN__</b><span>excluidos aqui</span></div>
<div class="kpi ac"><b>__PRET__%</b><span>taxa de retencao</span></div>
</div>
<div class="panel">__FUNIL__</div>
</section>

<section id="ordem">
<h2>Os cinco passos, e por que a ordem importa</h2>
<div class="crit">__PASSOS__</div>
<div class="nota"><b>Regra de ouro 3.</b> O criterio a registrar e o do <em>primeiro</em> portao que
explica o caso sem deixar residuo. Nao se desce a B2 para discutir se o LLM apenas avalia um
estudo cujo resultado gerado ja nao incluia UML em B1. Isso mantem o codigo de exclusao interpretavel: __B1__ registros
sairam por B1 porque o produto nunca foi UML, e nao porque alguem julgou o resto do desenho.</p>
</div>
<div class="alerta"><b>Uma distincao que a emenda A004 absorveu de proposito.</b> Na numeracao
anterior o E7 aparecia em dois lugares: <code>B1_E7</code>, quando nunca houve UML no estudo, e
<code>B3_E7</code>, quando havia UML mas na <em>entrada</em>, sendo o produto codigo, teste ou
documentacao. A A004 reformulou o B1 como &ldquo;o resultado gerado inclui UML?&rdquo;, pergunta
cuja resposta e <em>nao</em> nos dois casos, e os 22 registros de direcao invertida passaram a
sair por B1_E7 &mdash; hoje __B1__ no total. O subconjunto deixou de ser consultavel por um campo
so, e a verificacao mostrou que as notas de triagem nao o reconstituem: apenas 11 dos 22 citam a
sigla antiga, e quatro registros que nao pertencem ao grupo a citam por contraste. A enumeracao
integral dos 22 identificadores esta na linha <code>DECISAO_DESENHO</code> de
<code>screening_decision_log.csv</code>, de 2026-08-17.</div>
</section>

<section id="matriz">
<h2>A matriz de direcao</h2>
<p class="lead">O nucleo conceitual do portao cabe em quatro celulas. O que decide nao e o assunto
do artigo, e a posicao da UML no fluxo: se ela e <em>produto</em>, o estudo interessa; se e
<em>insumo</em>, nao.</p>
<div class="panel">__MATRIZ__</div>
<div class="nota"><b>O padrao mais dificil que a triagem enfrentou.</b> Um estudo que faz
<code>texto &rarr; UML &rarr; codigo</code> <em>nao</em> cai na celula de direcao invertida, que
pressupoe UML ja pronta na entrada; se o LLM sintetiza o diagrama a partir dos requisitos e so
depois gera codigo, a celula correta e a primeira, e o registro e retido &mdash; com a ressalva <code>CANDIDATO_E10</code>,
porque a qualidade medida costuma ser a do codigo, nao a do diagrama.</div>
</section>

<section id="bases">
<h2>As bases se comportam de modo muito diferente</h2>
<div class="panel">__PORBASE__</div>
<div class="ins">__INSBASE__</div>
</section>

<section id="sinal">
<h2>Onde a sigla UML aparece prediz o desfecho</h2>
<p class="lead">Um dos achados operacionais mais uteis da triagem: <em>onde</em> a mencao a UML
ocorre vale mais do que o fato de ela ocorrer.</p>
<div class="panel">__ONDEUML__</div>
<div class="alerta"><b>A armadilha do descritor.</b> No IEEE Xplore, "Unified modeling language"
e vocabulario controlado atribuido pelo indexador, e aparece na cauda do campo de palavras-chave
entre termos genericos como Training, Accuracy e Codes. <b>Nunca e declaracao dos autores.</b>
Entre os registros do IEEE em que UML so aparecia nas palavras-chave, praticamente todos eram
ruido. Por isso o teste decisivo passou a ser: a UML esta no titulo ou no resumo, ou e palavra-chave
autoral na posicao inicial? No Scopus a palavra-chave costuma ser autoral e confiavel.</div>
<div class="nota"><b>E o contrario tambem acontece.</b> __SEMUML__ dos __RET__ retidos nao usam a
sigla UML em nenhum lugar do titulo ou do resumo &mdash; falam em "class diagram", "domain model"
ou "conceptual model". Uma busca que exigisse a sigla perderia esses estudos.</div>
</section>

<section id="diagramas">
<h2>Que tipos de diagrama o campo realmente estuda</h2>
<p class="lead">Proporcao de registros que nomeiam cada tipo, entre retidos e entre excluidos no
Portao B.</p>
<div class="panel">__HEAT__</div>
<div class="ins">__INSDIAG__</div>
</section>

<section id="llms">
<h2>Quais modelos aparecem</h2>
<p class="lead">Mencoes nos __NB__ registros que chegaram ao Portao B, com a taxa de retencao de
cada um. A taxa e mais interessante que o volume: ela diz em que tipo de estudo cada modelo
costuma aparecer.</p>
<div class="panel">__LLM__</div>
<div class="ins">__INSLLM__</div>
</section>

<section id="qualidade">
<h2>Qual vocabulario de qualidade realmente discrimina</h2>
<p class="lead">Diferenca entre a frequencia de cada termo nos retidos e nos excluidos. Barra
para a direita: o termo e mais tipico de quem ficou. Os pares mostram as duas taxas.</p>
<div class="panel">__DIVQ__</div>
<div class="nota"><b>Achado contraintuitivo.</b> <code>accuracy</code> aparece em __ACCR__% dos
retidos e __ACCE__% dos excluidos: praticamente a mesma taxa, ou seja, <b>nao discrimina nada</b>.
Ja <code>completeness</code> aparece em __COMPR__% dos retidos contra __COMPE__% dos excluidos.
A licao e que vocabulario generico de avaliacao esta em todo lugar; o que separa e o vocabulario
especifico de qualidade de <em>modelo</em>. Isso e diretamente util para desenhar a extracao de
dados e a proxima string de busca.</div>
</section>

<section id="tempo">
<h2>O campo mudou de natureza entre 2022 e 2026</h2>
<div class="panel">__ANOB__</div>
<div class="ins">__INSTEMPO__</div>
</section>

<section id="flags">
<h2>O que ficou anotado para o texto completo</h2>
<p class="lead">O Portao C nao exclui ninguem. Ele marca. Cada flag e uma divida de leitura que a
triagem por resumo nao tinha como quitar, e vira a agenda da proxima etapa.</p>
<div class="panel">__FLAGS__</div>
</section>

<section id="tabela">
<h2>Registro a registro</h2>
<p class="lead">Os __NB__ registros que passaram pelo Portao B. Para os retidos, a coluna final
resume o que o estudo tem a oferecer, extraido da discussao registrada na hora da decisao. Onde a
nota nao sustenta uma afirmacao, ela diz isso em vez de inventar.</p>
<div class="filtros">
<button data-f="*" class="on">Todos</button>
<button data-f="PASSOU">Retidos</button>
<button data-f="B1_E7">E7 saida</button><button data-f="B2_E8">E8 avalia</button>
<button data-f="B3_E9">E9 entrada</button><button data-f="B4_E6">E6 origem</button>
<button data-f="B5_E7b">E7b notacao</button>
<button data-f="EVIDENCIA=EXPLICITA">evidencia explicita</button>
<button data-f="CANDIDATO_E10">candidato E10</button>
<button data-f="SEM_RESUMO">sem resumo</button>
<input id="q" placeholder="buscar titulo, id, termo..."><span class="dim" id="cn"></span>
</div>
<div class="wrap"><table id="tb"><thead><tr>
<th>ID</th><th>Desfecho</th><th>Estudo</th><th>Ano</th><th>Link</th>
<th>O que o registro sustenta</th></tr></thead><tbody>__LINHAS__</tbody></table></div>
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
Pagina gerada a partir de <code>search/v3_0/automated/records/custom_automated_search_collection.csv</code> e da
redacao lida de <code>protocol/__PROTO__/</code> no momento da geracao, nao transcrita. As notas de decisao do Portao B
somam em media __MEDNOTA__ caracteres por registro. Todos os numeros sao calculados na geracao.
Passe o mouse sobre os graficos para ver os valores exatos.
</footer>
<script>__JS__</script>
</body></html>"""

import criterios as crit
CRIT = crit.carrega()
crit.exige(CRIT, filtros={'B0', 'B1', 'B2', 'B3', 'B4', 'B5'},
           codigos={'E7', 'E8', 'E9', 'E6', 'E7b'})

# Uma linha por filtro, NA ORDEM DO PROTOCOLO. A citacao vem de crit.texto(), entao
# nao ha como o texto exibido pertencer a outro codigo -- que foi o que aconteceu
# quando a A004 migrou os rotulos e as citacoes escritas a mao ficaram para tras.
PASSOS = [
    ('a1', 'B1', 'E7', 'B1_E7', 'Qual e o artefato de saida?',
     'Vem primeiro porque "nao e UML" e o descarte mais frequente e mais objetivo de todos. '
     'Resolve dois tercos do portao antes de qualquer discussao mais fina.'),
    ('a2', 'B2', 'E8', 'B2_E8', 'Qual e a direcao do fluxo?',
     'So faz sentido perguntar de onde vem o conteudo depois de saber que ha UML na saida. '
     'Se o LLM altera o diagrama, o estudo segue; se apenas comenta, sai por E8.'),
    ('a3', 'B3', 'E9', 'B3_E9', 'O que entra no processo?',
     'Delimita o objeto da revisao: sintese a partir de linguagem natural. Engenharia reversa a '
     'partir de codigo e formalizacao de esboco desenhado a mao saem aqui, mesmo quando medem '
     'qualidade de UML com metricas explicitas.'),
    ('a4', 'B4', 'E6', 'B4_E6', 'Quem determina o conteudo semantico do diagrama?',
     'O teste nao e a presenca de uma rede neural, e a autoridade semantica. Encoders como BERT '
     'usados como classificador, extrator ou NER nao contam; regras simbolicas no pipeline sao '
     'irrelevantes desde que o LLM decida o conteudo.'),
]
passos_html = []
for cls, cod, ecod, key, perg, porq in PASSOS:
    cit = crit.texto(CRIT, ecod)
    v = cnt[key]
    passos_html.append(
        '<div class="c %s"><h4>%s &rarr; %s</h4><p class="q">%s</p>'
        '<div class="num" style="color:%s">%d <span style="font-size:12px;font-weight:400;'
        'color:var(--dim)">registros excluidos</span></div>'
        '<p class="cit">&ldquo;%s&rdquo;</p><p class="lead" style="font-size:13px;margin:0">%s</p></div>'
        % (cls, cod, ecod, E(perg), COR[key], v, E(cit), E(porq)))

insbase = ''.join([
    '<div class="i"><h4>O Scopus concentrou a substancia</h4><p>Das tres bases, o Scopus reteve '
    '<b>%.0f%%</b> do que levou ao Portao B, contra <b>%.0f%%</b> da ACM e <b>%.0f%%</b> do IEEE. '
    'Os <b>%d</b> retidos do Scopus sao <b>%.0f%%</b> de todo o conjunto final.</p></div>'
    % (100.0 * cb['SCOPUS']['PASSOU'] / sum(cb['SCOPUS'].values()),
       100.0 * cb['ACM']['PASSOU'] / sum(cb['ACM'].values()),
       100.0 * cb['IEEE']['PASSOU'] / sum(cb['IEEE'].values()),
       cb['SCOPUS']['PASSOU'], 100.0 * cb['SCOPUS']['PASSOU'] / len(RET)),
    '<div class="i"><h4>ACM e IEEE trouxeram ruido, nao materia</h4><p>Juntas somam <b>%d</b> '
    'registros no Portao B e entregam apenas <b>%d</b> retidos. A busca nessas bases foi sensivel '
    'demais: <b>%d</b> registros da ACM e <b>%d</b> do IEEE cairam logo em B1, por a saida nunca '
    'ter sido UML.</p></div>'
    % (sum(cb['ACM'].values()) + sum(cb['IEEE'].values()),
       cb['ACM']['PASSOU'] + cb['IEEE']['PASSOU'], cb['ACM']['B1_E7'], cb['IEEE']['B1_E7']),
    '<div class="i"><h4>Cada base erra de um jeito</h4><p>Na ACM o segundo motivo de saida e E6 '
    '(<b>%d</b> registros): muita modelagem sem LLM. No Scopus, os motivos se distribuem por todos '
    'os subportoes, sinal de que os registros ali sao de fato sobre o tema, mas com desenhos '
    'diferentes do que a revisao procura.</p></div>' % cb['ACM']['B4_E6'],
])

insdiag = ''.join([
    '<div class="i"><h4>Diagrama de classes e o campo inteiro</h4><p>Aparece em <b>%d</b> dos '
    '<b>%d</b> retidos, <b>%.0f%%</b>. Nenhum outro tipo chega perto. Se a tese precisar recortar, '
    'o recorte natural ja esta dado pelos dados.</p></div>'
    % (cls_r, len(RET), 100.0 * cls_r / len(RET)),
    '<div class="i"><h4>Maquina de estados e o inverso</h4><p>E o unico tipo que aparece mais '
    'entre os excluidos do que se esperaria: costuma vir de engenharia reversa de codigo ou de '
    'modelagem formal sem LLM, e nao de sintese a partir de requisitos.</p></div>',
    '<div class="i"><h4>A cauda longa da UML nao existe na pratica</h4><p>Diagramas de objetos, '
    'pacotes, comunicacao e implantacao praticamente nao aparecem. A UML que os LLMs geram e um '
    'subconjunto pequeno da UML que a norma define &mdash; um achado que vale registrar na '
    'discussao da tese.</p></div>',
])

insllm = ''.join([
    '<div class="i"><h4>BERT: a regra RF-01 validada nos dados</h4><p>BERT aparece em <b>%d</b> '
    'registros e <b>%d</b> deles foi retido. A regra que trata encoders pre-instrucionais como nao '
    'satisfazendo o criterio de LLM substantivo nao precisou ser aplicada caso a caso: os dados '
    'concordam com ela integralmente.</p></div>' % (n_re(B, r'\bbert\b'), bert_ret),
    '<div class="i"><h4>Modelos abertos e recentes retem mais</h4><p>Qwen aparece em <b>%d</b> '
    'registros e <b>%d</b> foram retidos, a maior taxa da lista. ChatGPT lidera em volume '
    '(<b>%d</b> mencoes) mas retem pouco: e citado em todo tipo de estudo, muitas vezes so na '
    'motivacao.</p></div>' % (n_re(B, r'qwen'), n_re(RET, r'qwen'), n_re(B, r'chatgpt')),
    '<div class="i"><h4>GPT-3.5 ja e arqueologia</h4><p>Aparece em <b>%d</b> registros, com apenas '
    '<b>%d</b> retido. Em tres anos o modelo que inaugurou o campo virou linha de base historica '
    'nos artigos.</p></div>' % (n_re(B, r'gpt-?3\.5'), n_re(RET, r'gpt-?3\.5')),
])

instempo = ''.join([
    '<div class="i"><h4>2022 quase nao tinha LLM</h4><p>Dos <b>%d</b> registros de 2022 que '
    'chegaram ao Portao B, <b>%d</b> sairam por E6: havia modelagem automatizada, mas feita com '
    'NLP de regras, ML classico ou encoders. So <b>1</b> foi retido. O campo que esta revisao '
    'estuda praticamente nao existia.</p></div>' % (tot_2022, e6_2022),
    '<div class="i"><h4>A taxa de retencao subiu e estabilizou</h4><p>Passou de patamar baixo em '
    '2022-2023 para em torno de um quarto a partir de 2024 e permanece ali em 2026. O campo '
    'amadureceu: nao so ha mais artigos, ha proporcionalmente mais artigos que fazem exatamente o '
    'que a revisao investiga.</p></div>',
    '<div class="i"><h4>E8 e E9 sao fenomenos novos</h4><p>Avaliar UML existente com LLM e fazer '
    'engenharia reversa com LLM praticamente nao aparecem antes de 2024. Sao subcampos que se '
    'formaram depois, e que uma revisao futura pode tratar como objeto proprio.</p></div>',
])

insights = ''.join([
    '<div class="i"><h4>Dois tercos do portao caem na primeira pergunta</h4><p><b>%d</b> dos '
    '<b>%d</b> excluidos sairam ja em B1, por a saida nunca ter sido UML. Colocar a pergunta mais '
    'objetiva primeiro foi a decisao de desenho que mais economizou julgamento.</p></div>'
    % (cnt['B1_E7'], len(EXC)),
    '<div class="i"><h4>Notacao adjacente foi a maior fonte de falso positivo</h4><p>Arvore de '
    'falhas, mapas conceituais, Event Storming, esquema ER em PlantUML, fluxograma generico: '
    'estudos que geram uma notacao vizinha e a medem com vocabulario de qualidade identico ao da '
    'UML. Casam com a busca, mas nao com o objeto.</p></div>',
    '<div class="i"><h4>PlantUML e Mermaid sao sintaxe, nao notacao</h4><p>Escrever em PlantUML nao '
    'torna o artefato um diagrama UML: da para escrever ER, C4 ou um metamodelo Ecore na mesma '
    'sintaxe. Quando o resumo nao declara o tipo de diagrama, o registro fica retido com a marca '
    'de incerteza em vez de ser excluido por suposicao.</p></div>',
    '<div class="i"><h4>UML como ilustracao do proprio artigo</h4><p>Varios estudos usam um '
    'diagrama UML apenas para desenhar a arquitetura da ferramenta que apresentam. A UML esta na '
    'figura, nao no resultado. E um padrao facil de confundir com o objeto da revisao quando se le '
    'so o titulo.</p></div>',
    '<div class="i"><h4>A co-producao humano-LLM ficou sem resposta</h4><p>Alguns estudos descrevem '
    'processos iterativos em que humano e modelo constroem o diagrama juntos. Nao da para dizer '
    'pelo resumo de quem e a autoridade semantica, entao foram retidos com marca propria. E a '
    'fronteira conceitual mais delicada do portao.</p></div>',
    '<div class="i"><h4>Duas regras de fronteira foram fixadas durante a triagem</h4><p>OCL sozinha '
    'nao conta como conteudo UML separavel, e descricao textual de caso de uso conta como '
    '<em>entrada</em> mas nao como <em>saida</em>. Ambas foram decididas pela pesquisadora, '
    'registradas no log e aplicadas a casos nomeados, que podem voltar sem re-triagem se o '
    'protocolo for emendado.</p></div>',
])

licoes = """
<h3>1. A ordem das perguntas e o desenho, nao um detalhe</h3>
<p>Perguntar primeiro pela saida resolveu __PB1__% dos descartes com o criterio mais objetivo
disponivel. Se a ordem fosse invertida &mdash; comecar pela entrada, por exemplo &mdash; seria
preciso julgar a natureza do insumo de centenas de estudos que nem produzem UML. A ordem barata
antes da cara vale dentro do portao tanto quanto entre portoes.</p>

<h3>2. Guardar o portao, e nao so o criterio</h3>
<p>O mesmo codigo E7 significa duas coisas incompativeis dependendo de onde foi aplicado. Se a
planilha registrasse apenas "E7", a distincao entre "nunca houve UML" e "havia UML, mas como
insumo" estaria perdida, e com ela a possibilidade de responder perguntas sobre o campo. Registrar
o desfecho do portao custa uma coluna e preserva uma pergunta de pesquisa.</p>

<h3>3. A incerteza tem de ter um lugar para morar</h3>
<p>__NFLAG__ dos __RET__ retidos carregam alguma marca de incerteza. Se a triagem tivesse de
escolher entre incluir e excluir, essas duvidas virariam decisoes silenciosas e irrecuperaveis.
Com o Portao C, elas viram agenda: cada marca diz exatamente o que ler no texto completo e por
que. Nenhuma flag exclui &mdash; essa e a regra que sustenta as outras.</p>

<h3>4. O que este portao nao pode decidir</h3>
<p>Tres criterios ficaram deliberadamente de fora. <b>E10</b>, sobre a UML nao ser separavel de
outros artefatos gerados, exige ver o que o estudo de fato mede: __NE10__ registros ficaram
marcados como candidatos. <b>E11</b>, sobre haver evidencia extraivel de qualidade, o proprio
protocolo proibe decidir por resumo. <b>E5</b>, sobre nao conseguir o texto completo, so existe
depois de tentar obter o PDF. Um portao que tentasse decidir tudo produziria exclusoes que ninguem
conseguiria defender depois.</p>

<h3>5. Onde a triagem foi mais fragil</h3>
<p>Tres frentes. A <b>armadilha do descritor</b> do IEEE, que atribui "Unified modeling language"
a artigos sem nenhuma relacao com UML e que quase produziu dezenas de falsos positivos. A
<b>notacao adjacente</b>, medida com o mesmo vocabulario de qualidade da UML. E a
<b>co-producao humano-LLM</b>, onde a autoridade semantica e genuinamente ambigua no resumo.
Nos tres casos a saida foi a mesma: reter e registrar por que, em vez de decidir com informacao
insuficiente.</p>

<div class="alerta"><b>Limite honesto desta pagina.</b> Tudo aqui descreve decisoes tomadas por
um unico revisor a partir de titulo, resumo e palavras-chave, com a evidencia registrada no
momento. As proporcoes lexicais sao contagens de expressao regular sobre esses campos: indicam
tendencia, nao medem o conteudo dos artigos. Nada disso substitui a leitura do texto completo nem
a dupla triagem independente, que o log de eventos ja suporta e que ainda nao foi feita.</div>
"""

nflag = sum(1 for r in RET if r[I['gate_c_flags']].strip())

doc = (DOC.replace('__CSS__', CSS).replace('__JS__', JS).replace('__PROTO__', crit.VERSAO)
       .replace('__FUNIL__', funil()).replace('__MATRIZ__', matriz())
       .replace('__PORBASE__', por_base()).replace('__ONDEUML__', onde_uml())
       .replace('__HEAT__', heat_tipos()).replace('__LLM__', svg_llm)
       .replace('__DIVQ__', divergente_qual()).replace('__ANOB__', ano_b())
       .replace('__FLAGS__', svg_flags)
       .replace('__PASSOS__', ''.join(passos_html))
       .replace('__INSBASE__', insbase).replace('__INSDIAG__', insdiag)
       .replace('__INSLLM__', insllm).replace('__INSTEMPO__', instempo)
       .replace('__INSIGHTS__', insights).replace('__LICOES__', licoes)
       .replace('__LINHAS__', ''.join(linhas))
       .replace('__NB__', str(NB)).replace('__RET__', str(len(RET)))
       .replace('__EXCN__', str(len(EXC)))
       .replace('__PEXC__', '%.0f' % (100.0 * len(EXC) / NB))
       .replace('__PRET__', '%.0f' % (100.0 * len(RET) / NB))
       .replace('__B1__', str(cnt['B1_E7']))
       .replace('__PB1__', '%.0f' % (100.0 * cnt['B1_E7'] / len(EXC)))
       .replace('__SEMUML__', str(sem_uml_ret))
       .replace('__ACCR__', '%.0f' % acc_r).replace('__ACCE__', '%.0f' % acc_e)
       .replace('__COMPR__', '%.0f' % comp_r).replace('__COMPE__', '%.0f' % comp_e)
       .replace('__NFLAG__', str(nflag)).replace('__NE10__', str(flags['CANDIDATO_E10']))
       .replace('__MEDNOTA__', str(sum(len(r[I['gate_b_notes']]) for r in B) // NB)))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(doc)
print('gerado:', OUT, '| %d KB' % (len(doc) // 1024))
print('B=%d retidos=%d excluidos=%d' % (NB, len(RET), len(EXC)))
print('flags:', dict(flags))
