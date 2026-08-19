# -*- coding: utf-8 -*-
"""Gera a ficha de extracao: Portao C mais os 65 campos, numa leitura so.

A ficha e DIRIGIDA PELO CODEBOOK. O formulario nao esta escrito neste arquivo:
ele e montado a partir de analysis/extraction/codebook_extracao.csv, campo a
campo. Revisar o codebook depois do piloto muda a pagina sem tocar em codigo,
que e exatamente o que o protocolo l. 1558 preve ao dizer que revisao material
do formulario dispara revisao retrospectiva.

Por que um instrumento so. O C1, os quatro atributos de triagem e os 65 campos
se respondem todos com o PDF aberto. Separar em duas passagens obrigaria a abrir
52 artigos duas vezes, e a segunda leitura reconstruiria de memoria o que a
primeira ja tinha visto.

O formulario e renderizado no navegador, um estudo por vez, a partir de duas
tabelas embutidas: a lista de estudos e a lista de campos. Renderizar 52 x 65
campos no HTML produziria um arquivo inutilmente grande.

Saida: analysis/ficha_extracao.html, autocontida e offline. A exportacao produz
CSV no MESMO cabecalho de analysis/extraction/extracao.csv, e a decisao do
Portao C sai em CSV separado, porque o desfecho de portao mora no CSV mestre e
nao no arquivo de extracao (manual v2, secao 7.1).
"""
import collections, csv, html, json, os, re

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSV  = os.path.join(BASE, 'search/automated/custom_automated_search_collection.csv')
COD  = os.path.join(BASE, 'analysis/extraction/codebook_extracao.csv')
DADOS = os.path.join(BASE, 'analysis/extraction/extracao.csv')
OUT  = os.path.join(BASE, 'analysis/ficha_extracao.html')
CSS  = open(os.path.join(BASE, 'analysis/scripts/css_gate.css'), encoding='utf-8').read()

# Codigos de ausencia do protocolo, l. 1554. Sao quatro e sao distintos: nao
# reportado nao e o mesmo que nao aplicavel, e nenhum dos dois e indefinido.
AUSENTES = ['NAO_REPORTADO', 'NAO_APLICAVEL', 'INDEFINIDO', 'NAO_ACESSIVEL']


def limpa(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()


# ------------------------------------------------------------------ entrada
rows = list(csv.reader(open(CSV, encoding='utf-8')))
i = {c: n for n, c in enumerate(rows[0])}
data = rows[1:]

codebook = list(csv.DictReader(open(COD, encoding='utf-8')))
CAB_DADOS = next(csv.reader(open(DADOS, encoding='utf-8')))

ret = [r for r in data if r[i['excluded']] != 'true']
com_texto = [r for r in ret if r[i['pdf_status']].startswith('OK_')]
com_texto.sort(key=lambda r: r[i['logical_id']])

# ------------------------------------------------------------------ piloto
# A amostra do piloto e uma LISTA CONGELADA, e nao um sorteio recalculado a cada
# execucao. A primeira versao deste arquivo recalculava, e estava errada: o
# sorteio depende do conjunto de estudos com texto, que CRESCE quando um autor
# responde ao pedido de copia. Verificado em 2026-08-18, ao entrar 907_SCOPUS:
# a amostra trocava 762_SCOPUS por 927_SCOPUS sozinha. Uma amostra que se
# reembaralha a cada recuperacao nao e amostra, e o piloto registrado no log
# deixaria de bater com o que a pagina mostra.
#
# COMO ESTES DEZ FORAM OBTIDOS, para quem auditar: sorteio estratificado por ano
# x tipo de veiculo sobre os 52 estudos com texto em 2026-08-18, uma vaga por
# estrato nao vazio e as vagas restantes para os estratos maiores, com semente
# 20260818 combinada por sha256 com o nome do estrato. Ano e tipo de veiculo sao
# os dois UNICOS eixos de diversidade da l. 1558 conheciveis antes de extrair.
# A cota igual por estrato foi deliberada: o piloto submete o formulario a casos
# diferentes, nao representa o corpus em proporcao. Nada olhou para o CONTEUDO
# dos estudos, o que selecionaria pela variavel dependente e violaria a sexta
# regra de ouro do manual v2. O procedimento completo esta no log, linha
# DECISAO_DESENHO de 2026-08-18T02:45.
#
# Registros recuperados DEPOIS do sorteio entram na fila de extracao, mas nao
# entram no piloto: trocar a amostra a cada chegada tornaria o piloto um alvo
# movel e invalidaria a comparacao entre o que foi planejado e o que foi feito.
SEMENTE_PILOTO = 20260818        # semente do sorteio que produziu a lista abaixo
PILOTO = {
    '018_ACM', '521_IEEE', '751_SCOPUS', '762_SCOPUS', '801_SCOPUS',
    '859_SCOPUS', '892_SCOPUS', '909_SCOPUS', '958_SCOPUS', '976_SCOPUS',
}
N_PILOTO = len(PILOTO)

estratos = collections.OrderedDict()
for r in com_texto:
    estratos.setdefault((r[i['PY']].strip(), r[i['TY']].strip()), []).append(r)

ausentes = PILOTO - {r[i['logical_id']] for r in com_texto}
assert not ausentes, 'registro do piloto sumiu da fila com texto: %s' % sorted(ausentes)

# Os do piloto vem primeiro na fila para que as setas os percorram em sequencia.
com_texto.sort(key=lambda r: (r[i['logical_id']] not in PILOTO, r[i['logical_id']]))

# ------------------------------------------------------------------ estudos
# Ano e tipo de veiculo viajam junto porque sao os dois eixos com que o piloto
# do protocolo (l. 1558) pede diversidade e que ja estao disponiveis. Tipo de
# diagrama e referencial de avaliacao, os outros dois eixos exigidos, so se
# conhecem DEPOIS de extrair: a selecao do piloto por esses dois e circular e
# tem de ser conferida ao final, nao antes.
EST = []
for r in com_texto:
    EST.append({
        'id':  r[i['logical_id']],
        'ti':  limpa(r[i['TI']]),
        't2':  limpa(r[i['T2']]),
        'py':  limpa(r[i['PY']]),
        'ty':  limpa(r[i['TY']]),
        'doi': limpa(r[i['DO']]),
        'pdf': limpa(r[i['pdf_file']]),
        'gc':  limpa(r[i['gate_c_outcome']]),
        'p':   r[i['logical_id']] in PILOTO,
        'st':  limpa(r[i['pdf_status']]),
    })

# ------------------------------------------------------------------ campos
def ausentes_faltantes(vals):
    """Quais dos quatro codigos de ausencia a lista do protocolo ainda nao cobre.

    Varias listas do protocolo ja trazem 'unclear' ou 'not reported' como valor
    proprio. Acrescentar INDEFINIDO ao lado de 'unclear' criaria duas grafias
    para a mesma coisa e a contagem final somaria errado.
    """
    t = ' ; '.join(v.lower() for v in vals)
    falta = []
    if 'not reported' not in t and 'none reported' not in t:
        falta.append('NAO_REPORTADO')
    if 'not applicable' not in t:
        falta.append('NAO_APLICAVEL')
    if 'unclear' not in t:
        falta.append('INDEFINIDO')
    falta.append('NAO_ACESSIVEL')      # nunca aparece nas listas do protocolo
    return falta


CAMPOS = []
for c in codebook:
    vals = [v.strip() for v in c['valores_admitidos'].split(';') if v.strip()]
    fechado = c['tipo'] == 'fechado'
    CAMPOS.append({
        'o':     int(c['ordem']),
        'sec':   c['secao'],
        'fac':   c['faceta'],
        'campo': c['campo'],
        'tipo':  c['tipo'],
        'rep':   c['repetivel'] == 'SIM',
        # Grupo de repeticao: campos que descrevem CONJUNTAMENTE um mesmo
        # objeto e por isso compartilham indice. Sem ele a chave do arquivo de
        # extracao produz LISTAS PARALELAS, e nada vincula a ocorrencia 3 de um
        # campo a ocorrencia 3 do vizinho. O protocolo l. 1601-1608 define
        # inadequacao como TUPLA, e a comparacao constante (l. 1626) e a
        # analise de casos negativos (l. 1628) operam sobre casos.
        'grp':   c['grupo_repeticao'],
        'q':     c['questoes'],
        # Duas relacoes diferentes, que a coluna questoes fundia ate o item F:
        # "e dado de" (l. 133-145) e "define o subconjunto de" (l. 1375-1378).
        'sub':   c['define_subconjunto'],
        'regra': c['regra_extracao'],
        # exemplos nao viram opcao: em campo aberto a lista do protocolo e
        # ilustrativa, e transforma-la em menu induziria a escolher da lista em
        # vez de registrar o vocabulario nativo.
        'vals':  (vals + ausentes_faltantes(vals)) if fechado else [],
        'ex':    vals if not fechado else [],
    })

# Numero de ordem por NOME. Duas renumeracoes numa sessao so (a entrada da
# severidade e a fusao do campo de envolvimento humano) mostraram que amarrar
# trava ou texto ao numero do campo e amarrar ao que muda. Daqui para baixo o
# numero e sempre DERIVADO do nome.
ORD = {c['campo']: c['o'] for c in CAMPOS}
assert len(ORD) == len(CAMPOS), 'nome de campo repetido no codebook'

# ------------------------------------------------- 8d-4: fonte unica dos codigos
# O codebook da TAXONOMIA (l. 1634) e o de EXTRACAO descrevem o mesmo
# vocabulario em arquivos diferentes: os codigos da taxonomia SAO os valores dos
# campos de operacao e de referencia, e os portadores admitidos SAO os valores
# do campo de portador. Foi
# exatamente esse tipo de duplicacao sem reconciliacao, entre duas secoes do
# protocolo, que produziu as cinco divergencias resolvidas no item 8c. O assert
# abaixo existe para que o defeito nao possa renascer entre dois arquivos
# nossos: qualquer edicao de um lado so INTERROMPE a geracao da ficha.
TAX = list(csv.DictReader(open(os.path.join(
    BASE, 'analysis/extraction/codebook_taxonomia.csv'), encoding='utf-8')))
_v = {c['campo']: c['vals'] if c['tipo'] != 'fechado' else
      [x.strip() for x in
       next(r['valores_admitidos'] for r in codebook if r['campo'] == c['campo']).split(';')
       if x.strip()]
      for c in CAMPOS}
OPER, REF, PORT = 'Normalized discrepancy operation', 'Violated reference', 'UML carrier'
_por_pai = collections.OrderedDict()
for t in TAX:
    _por_pai.setdefault(t['categoria_pai'], []).append(t['codigo'])
assert _por_pai.get('OPERACAO_DE_DISCREPANCIA') == _v[OPER], \
    'codebook da taxonomia diverge do campo %d' % ORD[OPER]
assert _por_pai.get('REFERENCIA_VIOLADA') == _v[REF], \
    'codebook da taxonomia diverge do campo %d' % ORD[REF]
for t in TAX:
    assert [p.strip() for p in t['portadores_admitidos'].split(';')] == _v[PORT], \
        'portadores admitidos de %r divergem do campo %d' % (t['codigo'], ORD[PORT])
n_tax = len(TAX)
n_tax_construido = sum(1 for t in TAX if t['procedencia_exemplo'] == 'construido')

SECOES = []
for sec in ('MAPEAMENTO', 'QUALIDADE'):
    facetas = []
    for c in CAMPOS:
        if c['sec'] == sec and (not facetas or facetas[-1] != c['fac']):
            if c['fac'] not in facetas:
                facetas.append(c['fac'])
    SECOES.append((sec, facetas))

# ------------------------------------------------------------------ numeros
n_fechado = sum(1 for c in CAMPOS if c['tipo'] == 'fechado')
n_aberto  = sum(1 for c in CAMPOS if c['tipo'] == 'aberto')
n_comp    = sum(1 for c in CAMPOS if c['tipo'] == 'composto')
n_rep     = sum(1 for c in CAMPOS if c['rep'])
n_c1      = sum(1 for e_ in EST if not e_['gc'])

# Grupos de repeticao, na ordem em que aparecem. Todo campo de grupo tem de ser
# repetivel, e o grupo tem de ser contiguo na ordem do codebook: sem isso a
# instancia nao poderia ser renderizada como um cartao unico na tela.
GRUPOS = collections.OrderedDict()
for c in CAMPOS:
    if c['grp']:
        GRUPOS.setdefault(c['grp'], []).append(c['o'])
for g, oo in GRUPOS.items():
    assert oo == list(range(oo[0], oo[0] + len(oo))), 'grupo %s nao contiguo: %s' % (g, oo)
    assert all(c['rep'] for c in CAMPOS if c['grp'] == g), 'grupo %s com campo nao repetivel' % g
n_grp = sum(len(oo) for oo in GRUPOS.values())

# 8b: um unico campo NAO vem das duas tabelas de extracao do protocolo. A tupla
# da l. 1601-1608 tem cinco dimensoes e a severidade (Se) nao tinha casa em
# nenhuma das tabelas. O assert existe para que a pagina nunca afirme "um campo
# nosso" apontando para outra coisa.
NOSSO = 'Reported severity or task effect'
assert ORD[NOSSO] in GRUPOS['INADEQUACAO'], \
    'o campo acrescentado no 8b saiu de dentro do grupo INADEQUACAO'
n_tab = len(CAMPOS) - 1

# Perguntas: quem e dono de que. Vazio em questoes significa INSTRUMENTO da
# revisao, e sao exatamente os quatro campos de eixo e atribuicao.
DONOS = collections.OrderedDict()
for c in CAMPOS:
    DONOS.setdefault(c['q'] or '(instrumento)', []).append(c['o'])
assert not any(';' in c['q'] for c in CAMPOS), 'sobrou campo com dois donos'
assert len(DONOS['(instrumento)']) == 4, DONOS['(instrumento)']
QUESTOES = ('MQ1', 'MQ2', 'MQ3', 'MQ4', 'MQ5',
            'SQ1', 'SQ2', 'SQ3', 'SQ4', 'SQ5', 'SQ6', 'SQ7')
SEM_CAMPO = [q for q in QUESTOES if q not in DONOS]
assert SEM_CAMPO == ['MQ5'], SEM_CAMPO   # a MQ5 e computada (l. 137, l. 1382)

# A correspondencia com as tabelas do protocolo, derivada e nao escrita: a
# insercao da severidade e a fusao do campo de envolvimento humano se cancelam
# depois da severidade.
O_ULT_IGUAL = ORD['Dimensions and baselines']


def faixa(g):
    oo = GRUPOS[g]
    return '%d-%d' % (oo[0], oo[-1])

kpis = ''.join(
    '<div class="kpi %s"><b>%s</b><span>%s</span></div>' % (cls, v, k)
    for v, k, cls in [
        (len(EST), 'estudos com texto', 'ac'),
        (n_c1, 'sem decisao C1', 'wr'),
        # "da ficha", e nao "do protocolo": desde o item 8b um dos campos e
        # nosso, e o rotulo antigo passaria a afirmar falsidade.
        (len(CAMPOS), 'campos da ficha', ''),
        (n_rep, 'campos repetiveis', ''),
        (n_grp, 'em grupo de repeticao', ''),
        (len(PILOTO), 'sorteados para o piloto', 'ok'),
    ])


def tab(cab, linhas):
    h = '<table><thead><tr>' + ''.join('<th>%s</th>' % c for c in cab) + '</tr></thead><tbody>'
    for ln in linhas:
        h += '<tr>' + ''.join('<td>%s</td>' % html.escape(str(c)) for c in ln) + '</tr>'
    return h + '</tbody></table>'


tab_secoes = tab(
    ['Secao', 'Faceta', '#Campos', 'Repetiveis', 'Grupo de repeticao'],
    [(sec, fac,
      sum(1 for c in CAMPOS if c['sec'] == sec and c['fac'] == fac),
      sum(1 for c in CAMPOS if c['sec'] == sec and c['fac'] == fac and c['rep']),
      ' '.join(sorted({c['grp'] for c in CAMPOS
                       if c['sec'] == sec and c['fac'] == fac and c['grp']})))
     for sec, facs in SECOES for fac in facs])

PRODUTO = {
    'MQ1': 'Publication and evidence landscape',
    'MQ2': 'Diagram, task, and data map',
    'MQ3': 'Technical configuration map',
    'MQ4': 'Evaluation and reproducibility map',
    'MQ5': 'Research concentration and gap map',
    'SQ1': 'Quality construct matrix',
    'SQ2': 'Taxonomy of reported inadequacies',
    'SQ3': 'Evaluation reference and metric catalogue',
    'SQ4': 'Syntax-semantic dissonance evidence map',
    'SQ5': 'Assessment credibility matrix',
    'SQ6': 'Generation context knowledge map',
    'SQ7': 'Pragmatic and rework evidence map',
}
# De onde cada produto se compõe quando a pergunta nao e dona do campo. Nao e
# opiniao: sai da tabela de rastreabilidade l. 133-145 comparada com a posse.
# A SQ6 saiu daqui: depois da divisao da A006 secao 10 ela e dona dos seus dois
# campos e nao le mais campo da MQ3.
DERIVA = {
    'MQ4': 'MQ1, SQ3 e SQ5',
    'MQ5': 'MQ2, MQ3 e MQ4',
}
tab_donos = tab(
    ['Pergunta', '#Campos proprios', 'Campos', 'Tambem se compoe de', 'Produto'],
    [(q, len(DONOS.get(q, [])), ' '.join(str(o) for o in DONOS.get(q, [])) or '(nenhum)',
      DERIVA.get(q, ''), PRODUTO[q]) for q in QUESTOES]
    + [('(instrumento)', len(DONOS['(instrumento)']),
        ' '.join(str(o) for o in DONOS['(instrumento)']), '',
        'Eixos e atribuicao: computam subconjuntos, nao respondem pergunta')])

tab_est = tab(
    ['Registro', 'Piloto', 'Ano', 'Tipo', 'Veiculo'],
    [(e_['id'], 'PILOTO' if e_['p'] else '', e_['py'], e_['ty'], e_['t2'][:78])
     for e_ in EST])

tab_piloto = tab(
    ['Registro', 'Ano', 'Tipo', 'Procedencia do texto', 'Titulo'],
    [(e_['id'], e_['py'], e_['ty'], e_['st'], e_['ti'][:70])
     for e_ in EST if e_['p']])

tab_estratos = tab(
    ['Ano', 'Tipo', '#Com texto', '#No piloto'],
    [(a, t, len(estratos[(a, t)]),
      sum(1 for r in estratos[(a, t)] if r[i['logical_id']] in PILOTO))
     for a, t in sorted(estratos)])

# ------------------------------------------------------------------ css
EXTRA = """
.barra{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:16px 0;position:sticky;top:41px;z-index:8;background:rgba(15,17,21,.96);padding:10px 0}
.barra select,.barra input{font:inherit;font-size:13px;background:var(--pan2);color:var(--tx);border:1px solid var(--ln);border-radius:8px;padding:6px 11px}
.barra select{max-width:520px}
.barra button{font:inherit;font-size:12.5px;cursor:pointer;background:var(--pan2);color:var(--tx);border:1px solid var(--ln);border-radius:999px;padding:5px 14px}
.barra button.pri{background:var(--ac);color:#0f1115;border-color:var(--ac);font-weight:600}
.cab{background:var(--pan);border:1px solid var(--ln);border-radius:14px;padding:16px 18px;margin:14px 0}
.cab h3{margin:0 0 4px;font-size:17px}
.cab .meta{color:var(--dim);font-size:12.5px}
.gc{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid var(--ln)}
.gc label{display:flex;gap:6px;align-items:center;font-size:13px;cursor:pointer}
.fac{margin:22px 0 8px;font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--ac)}
.cp{background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:13px 15px;margin:10px 0}
.cp.on{border-color:#2f5d3a}
.cp .top{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.cp .nm{font-weight:600;font-size:14px}
.cp .tg{font-size:10.5px;padding:1px 7px;border-radius:5px;border:1px solid var(--ln);color:var(--dim)}
.cp .rg{color:var(--dim);font-size:12.5px;margin:5px 0 9px;max-width:96ch}
.oc{border-left:2px solid var(--ln);padding-left:11px;margin:9px 0}
.oc .lin{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.oc select,.oc input,.oc textarea{font:inherit;font-size:13px;background:var(--pan2);color:var(--tx);border:1px solid var(--ln);border-radius:8px;padding:5px 10px}
.oc textarea{width:100%;min-height:52px;resize:vertical}
.oc input.nat{min-width:250px}
.oc input.ev{flex:1;min-width:320px}
.oc input.loc{min-width:110px}
.oc .ord{color:var(--dim);font-size:11px;padding-top:7px}
.cp .mais{font:inherit;font-size:12px;cursor:pointer;background:transparent;color:var(--ac);border:1px dashed var(--ln);border-radius:8px;padding:3px 11px}
.prog{color:var(--dim);font-size:12.5px}
.grp{border:1px solid var(--ac);border-radius:14px;padding:11px 13px;margin:12px 0;background:rgba(90,160,255,.03)}
.grp>.grph{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:var(--ac);margin-bottom:4px}
.grp>.grph .tg{text-transform:none;letter-spacing:0;font-size:10.5px;padding:1px 7px;border-radius:5px;border:1px solid var(--ln);color:var(--dim)}
.grp>.mais{font:inherit;font-size:12px;cursor:pointer;background:transparent;color:var(--ac);border:1px dashed var(--ac);border-radius:8px;padding:4px 13px;margin-top:4px}
.inst{border-left:3px solid var(--ac);padding-left:12px;margin:10px 0 14px}
.inst .insth{font-size:12px;color:var(--dim);margin-bottom:4px}
.inst .menos{font:inherit;font-size:11px;cursor:pointer;background:transparent;color:var(--dim);border:1px dashed var(--ln);border-radius:7px;padding:1px 8px;margin-left:6px}
"""

# ------------------------------------------------------------------ js
JS = """
var EST=__EST__,CAMPOS=__CAMPOS__,AUS=__AUS__;
/* Chave nova de proposito. A v1 guardava os campos numa lista por campo; a v2
   guarda os campos AGRUPADOS por instancia. Reaproveitar a chave misturaria as
   duas formas no mesmo objeto e o export sairia meio tupla, meio lista. */
var K='extracao.v2',S=JSON.parse(localStorage.getItem(K)||'{}');
var cur=0;
/* BLOCOS dobra campos consecutivos do mesmo grupo num bloco so. Fora do grupo,
   cada bloco tem um campo e nada muda em relacao a v1. */
var BLOCOS=[];
CAMPOS.forEach(function(c){var b=BLOCOS[BLOCOS.length-1];
  if(c.grp&&b&&b.grp===c.grp)b.cs.push(c);else BLOCOS.push({grp:c.grp||'',cs:[c]});});
function salvar(){localStorage.setItem(K,JSON.stringify(S));}
function est(id){if(!S[id])S[id]={gc:'',gcn:'',f:{},g:{}};
  if(!S[id].f)S[id].f={};if(!S[id].g)S[id].g={};return S[id];}
function ocs(id,o){var e=est(id);if(!e.f[o])e.f[o]=[{}];return e.f[o];}
/* Uma instancia e uma TUPLA: um objeto {ordem: [linhas]} que carrega os campos
   do grupo juntos. Duas inadequacoes sao duas instancias, e cada campo dentro
   de uma instancia ainda pode repetir (uma inadequacao com dois portadores). */
function insts(id,g){var e=est(id);if(!e.g[g])e.g[g]=[{}];return e.g[g];}
function gocs(id,g,k,o){var it=insts(id,g)[k];if(!it[o])it[o]=[{}];return it[o];}
function preenchido(r){return !!((r.v&&r.v.length)||(r.nat&&r.nat.length));}
function contaEstudo(id){var e=S[id];if(!e)return 0;var vis={},n=0;
  for(var o in (e.f||{})){if(e.f[o].some(preenchido))vis[o]=1;}
  for(var g in (e.g||{})){e.g[g].forEach(function(it){
    for(var o2 in it){if(it[o2].some(preenchido))vis[o2]=1;}});}
  for(var k in vis)n++;return n;}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

function opcoes(c,sel){var h='<option value="">--</option>';
  c.vals.forEach(function(v){h+='<option value="'+esc(v)+'"'+(v===sel?' selected':'')+'>'+esc(v)+'</option>';});
  return h;}
function ausSel(sel){var h='<option value="">--</option>';
  AUS.forEach(function(v){h+='<option value="'+esc(v)+'"'+(v===sel?' selected':'')+'>'+esc(v)+'</option>';});
  return h;}

/* Um cartao de campo. extra carrega data-g e data-i quando o campo esta dentro
   de uma instancia de grupo; vazio quando nao esta. E o mesmo cartao nos dois
   casos de proposito: o campo nao muda por estar agrupado, so ganha vinculo. */
function cartao(c,lst,extra){
  var h='<div class="cp'+(lst.some(preenchido)?' on':'')+'" data-o="'+c.o+'"'+extra+'>'
    +'<div class="top"><span class="nm">'+esc(c.campo)+'</span>'
    +'<span class="tg">'+esc(c.tipo)+'</span>'+(c.rep?'<span class="tg">repetivel</span>':'')
    +'<span class="tg">'+esc(c.q)+'</span></div>';
  if(c.regra)h+='<div class="rg">'+esc(c.regra)+'</div>';
  if(c.ex.length)h+='<div class="rg"><i>exemplos do protocolo:</i> '+esc(c.ex.join('; '))+'</div>';
  lst.forEach(function(r,n){
    h+='<div class="oc" data-n="'+n+'"><div class="lin">';
    if(c.rep)h+='<span class="ord">#'+(n+1)+'</span>';
    if(c.tipo==='fechado'){
      h+='<select data-k="v">'+opcoes(c,r.v)+'</select>'
        +'<input class="nat" data-k="nat" placeholder="termo nativo do estudo" value="'+esc(r.nat)+'">';
    }else{
      h+='<select data-k="v" class="ausx">'+ausSel(AUS.indexOf(r.v)>=0?r.v:'')+'</select>';
    }
    h+='<input class="ev" data-k="ev" placeholder="evidencia: trecho literal, dentro dos limites de citacao" value="'+esc(r.ev)+'">'
      +'<input class="loc" data-k="loc" placeholder="p. / secao" value="'+esc(r.loc)+'">'
      +'</div>';
    if(c.tipo!=='fechado')
      h+='<textarea data-k="t" placeholder="valor, no vocabulario do estudo">'+esc(AUS.indexOf(r.v)>=0?(r.t||''):(r.t||r.v||''))+'</textarea>';
    h+='</div>';
  });
  if(c.rep)h+='<button class="mais" data-mais="'+c.o+'">+ ocorrencia</button>';
  return h+'</div>';
}

function render(){
  var e0=EST[cur],e=est(e0.id);
  var h='<div class="cab"><h3>'+esc(e0.ti)+'</h3><div class="meta"><span class="mono">'+esc(e0.id)+'</span> &middot; '
    +esc(e0.t2)+' &middot; '+esc(e0.py)+' &middot; '+esc(e0.ty)
    +(e0.doi?' &middot; <a target="_blank" rel="noopener" href="https://doi.org/'+esc(e0.doi)+'">DOI</a>':'')
    +(e0.pdf?' &middot; <span class="mono">'+esc(e0.pdf)+'</span>':'')+'</div>'
    +'<div class="gc"><b>Portao C &mdash; C1: ha instancia de geracao identificavel?</b>'
    +'<label><input type="radio" name="gc" value="ELEGIVEL"'+(e.gc==='ELEGIVEL'?' checked':'')+'> Sim, ELEGIVEL</label>'
    +'<label><input type="radio" name="gc" value="C1_E12"'+(e.gc==='C1_E12'?' checked':'')+'> Nao, C1_E12</label>'
    +'<input id="gcn" style="flex:1;min-width:300px" placeholder="metodo, evidencia, discussao, decisao" value="'+esc(e.gcn)+'">'
    +'</div></div>';
  var sec='',fac='';
  BLOCOS.forEach(function(b){
    var c0=b.cs[0];
    if(c0.sec!==sec){sec=c0.sec;fac='';h+='<h3 style="color:var(--tx);border-bottom:2px solid var(--ln);padding-bottom:6px">'+esc(sec)+'</h3>';}
    if(c0.fac!==fac){fac=c0.fac;h+='<div class="fac">'+esc(fac)+'</div>';}
    if(!b.grp){h+=cartao(c0,ocs(e0.id,c0.o),'');return;}
    var lst=insts(e0.id,b.grp);
    h+='<div class="grp"><div class="grph">'+esc(b.grp)+' &middot; '+lst.length+(lst.length>1?' instancias':' instancia')
      +' <span class="tg">os '+b.cs.length+' campos abaixo descrevem O MESMO objeto e saem na mesma tupla</span></div>';
    lst.forEach(function(it,k){
      var vazia=b.cs.every(function(c){return !((it[c.o]||[]).some(preenchido));});
      h+='<div class="inst"><div class="insth">#'+(k+1)+' &middot; <span class="mono">'+esc(b.grp+'-'+(k+1))+'</span>'
        +(vazia&&lst.length>1?' <button class="menos" data-menosg="'+b.grp+'" data-i="'+k+'">remover</button>':'')
        +'</div>';
      b.cs.forEach(function(c){
        h+=cartao(c,gocs(e0.id,b.grp,k,c.o),' data-g="'+b.grp+'" data-i="'+k+'"');
      });
      h+='</div>';
    });
    h+='<button class="mais" data-maisg="'+b.grp+'">+ instancia de '+esc(b.grp.toLowerCase())+'</button></div>';
  });
  document.getElementById('form').innerHTML=h;
  document.getElementById('sel').value=String(cur);
  atualizaProg();
}

function atualizaProg(){
  var tot=0;EST.forEach(function(x){tot+=contaEstudo(x.id);});
  var gc=EST.filter(function(x){var e=S[x.id];return e&&e.gc;}).length;
  document.getElementById('prog').textContent=
    contaEstudo(EST[cur].id)+' de '+CAMPOS.length+' campos neste estudo | '
    +gc+' de '+EST.length+' com C1 | '+tot+' campos no total';
}

document.getElementById('form').addEventListener('input',function(ev){
  var t=ev.target,e0=EST[cur],e=est(e0.id);
  if(t.id==='gcn'){e.gcn=t.value;salvar();return;}
  if(t.name==='gc'){e.gc=t.value;salvar();return;}
  var oc=t.closest('.oc'),cp=t.closest('.cp');if(!oc||!cp)return;
  var o=cp.dataset.o,n=+oc.dataset.n,k=t.dataset.k;
  var lst=cp.dataset.g?gocs(e0.id,cp.dataset.g,+cp.dataset.i,o):ocs(e0.id,o);
  var r=lst[n];
  if(k==='t'){r.t=t.value;if(!r.v||AUS.indexOf(r.v)<0)r.v=t.value;}
  else r[k]=t.value;
  cp.classList.toggle('on',lst.some(preenchido));
  salvar();atualizaProg();
});
document.getElementById('form').addEventListener('change',function(ev){
  if(ev.target.name==='gc'){est(EST[cur].id).gc=ev.target.value;salvar();atualizaProg();}
});
document.getElementById('form').addEventListener('click',function(ev){
  var id=EST[cur].id;
  var bg=ev.target.closest('[data-maisg]');
  if(bg){insts(id,bg.dataset.maisg).push({});salvar();render();return;}
  var bm=ev.target.closest('[data-menosg]');
  if(bm){insts(id,bm.dataset.menosg).splice(+bm.dataset.i,1);salvar();render();return;}
  var b=ev.target.closest('[data-mais]');if(!b)return;
  var cp=b.closest('.cp');
  if(cp.dataset.g)gocs(id,cp.dataset.g,+cp.dataset.i,cp.dataset.o).push({});
  else ocs(id,b.dataset.mais).push({});
  salvar();render();
});

document.getElementById('sel').addEventListener('change',function(){cur=+this.value;render();window.scrollTo(0,0);});
document.getElementById('ant').onclick=function(){if(cur>0){cur--;render();window.scrollTo(0,0);}};
document.getElementById('pro').onclick=function(){if(cur<EST.length-1){cur++;render();window.scrollTo(0,0);}};

function csv(linhas){return linhas.map(function(l){return l.map(function(c){
  c=(c==null?'':String(c));return /[",\\n]/.test(c)?'"'+c.replace(/"/g,'""')+'"':c;}).join(',');}).join('\\n');}
function baixar(nome,txt){var a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([txt],{type:'text/csv;charset=utf-8'}));
  a.download=nome;a.click();}

document.getElementById('exp').onclick=function(){
  var quem=document.getElementById('quem').value.trim()||'SEM_NOME';
  var ts=new Date().toISOString();
  var out=[__CAB__];
  /* instancia e o que amarra a tupla: INADEQUACAO-2 num campo do grupo e a MESMA
     inadequacao que INADEQUACAO-2 no campo vizinho. Vazio fora de grupo. A ordem de
     BLOCOS preserva a ordem do codebook. */
  EST.forEach(function(x){
    var e=S[x.id];if(!e)return;
    BLOCOS.forEach(function(b){
      if(!b.grp){
        var c=b.cs[0];
        ((e.f||{})[c.o]||[]).forEach(function(r,n){
          if(!preenchido(r))return;
          out.push([x.id,c.campo,'',n+1,r.v||'',r.nat||'',r.ev||'',r.loc||'',quem,ts,r.nt||'']);
        });
        return;
      }
      ((e.g||{})[b.grp]||[]).forEach(function(it,k){
        var inst=b.grp+'-'+(k+1);
        b.cs.forEach(function(c){
          (it[c.o]||[]).forEach(function(r,n){
            if(!preenchido(r))return;
            out.push([x.id,c.campo,inst,n+1,r.v||'',r.nat||'',r.ev||'',r.loc||'',quem,ts,r.nt||'']);
          });
        });
      });
    });
  });
  baixar('extracao_'+quem+'.csv',csv(out));
};
document.getElementById('expc').onclick=function(){
  var quem=document.getElementById('quem').value.trim()||'SEM_NOME';
  var ts=new Date().toISOString();
  var out=[['logical_id','gate_c_outcome','gate_c_reviewer','gate_c_datetime','gate_c_notes']];
  EST.forEach(function(x){var e=S[x.id];if(e&&e.gc)out.push([x.id,e.gc,quem,ts,e.gcn||'']);});
  baixar('gate_c_'+quem+'.csv',csv(out));
};
document.getElementById('quem').value=localStorage.getItem(K+'.quem')||'';
document.getElementById('quem').addEventListener('input',function(){localStorage.setItem(K+'.quem',this.value);});
render();
"""

# ------------------------------------------------------------------ html
HTML = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ficha de extracao &mdash; qualidade de UML gerada por LLM</title>
<style>__CSS__</style></head><body>
<header>
<div class="eyebrow">Revisao sistematica &middot; Portao C e extracao</div>
<h1>Ficha de extracao</h1>
<p>Um instrumento so para a decisao do Portao C e para os __N_CAMPOS__ campos de
extracao. Pagina autocontida: funciona offline, nao envia nada para
lugar nenhum, e o que voce responder fica gravado neste navegador.</p>
</header>

<div class="nav">
<a href="#comor">Como usar</a><a href="#piloto">O piloto</a><a href="#mapa">Mapa dos campos</a>
<a href="#estudos">Os estudos</a><a href="#ficha">A ficha</a>
</div>

<main>
<div class="kpis">__KPIS__</div>

<section id="comor"><h2>1. Como usar</h2>
<p>Cada estudo se resolve numa <b>leitura so</b>. Com o PDF aberto, responda primeiro o
<b>C1</b> e depois percorra os campos. Foi por isso que o Portao C e a extracao ficaram
no mesmo instrumento: separa-los obrigaria a abrir o mesmo artigo duas vezes, e a segunda
leitura reconstruiria de memoria o que a primeira ja tinha visto.</p>
<ol class="passos">
<li><b>C1 &mdash; ha instancia de geracao identificavel?</b> Se da para dizer o que o
modelo gerou e avalia-lo, <span class="mono">ELEGIVEL</span>. Se o UML se dissolve num
artefato agregado, numa pipeline de multiplas saidas ou numa demonstracao sem resultado
atribuivel, <span class="mono">C1_E12</span>. Esta e a <b>unica</b> saida do Portao C.</li>
<li><b>Campo fechado:</b> escolha o valor normalizado <b>e</b> escreva o termo que o
estudo usa. Os dois, sempre que diferirem.</li>
<li><b>Campo aberto ou composto:</b> escreva no vocabulario do estudo. O menu ao lado
serve so para marcar ausencia.</li>
<li><b>Evidencia:</b> o trecho que sustenta o valor, com pagina ou secao.</li>
<li><b>Grupo de repeticao:</b> nos blocos com borda azul, use <b>+ instancia</b> para cada
objeto novo &mdash; cada inadequacao, cada construto, cada metrica, cada modelo. Use
<b>+ ocorrencia</b> dentro de um campo so quando <b>aquele mesmo objeto</b> tiver mais de
um valor naquele campo, como uma inadequacao que atinge dois portadores.</li>
<li><b>Exportar</b> os dois CSV ao final: o da extracao e o do Portao C.</li>
</ol>
<div class="alerta"><b>Instancia, e nao lista paralela.</b> O protocolo (l. 1601-1608)
define inadequacao como uma <b>tupla</b>, nao como quatro listas soltas. Ate aqui a chave
do arquivo de extracao era <span class="mono">(logical_id, campo, ocorrencia, extrator)</span>,
e nela <b>nada dizia</b> que a terceira ocorrencia de <i>Violated reference</i> pertencia a
terceira de <i>UML carrier</i>: bastava um campo ficar em branco numa das quatro listas para
todas as tuplas seguintes se deslocarem em silencio. A coluna <span class="mono">instancia</span>
amarra a tupla, e por isso os campos de um grupo aparecem juntos num cartao so. Sem esse
vinculo a <b>comparacao constante</b> (l. 1626) e a <b>analise de casos negativos</b>
(l. 1628) nao teriam sobre que operar, porque as duas trabalham com <b>casos</b>.</div>
<div class="nota"><b>Vocabulario nativo primeiro.</b> Em todo campo fechado ha um lugar
para o <b>termo do proprio estudo</b>, e ele nao e decorativo. Normalizar antes de
registrar apaga a variacao terminologica entre os estudos &mdash; e essa variacao e o
achado central desta revisao, nao ruido a limpar. Preencha o termo nativo mesmo quando o
mapeamento parecer obvio.</div>
<div class="alerta"><b>Quatro codigos de ausencia, e eles nao sao sinonimos.</b>
<span class="mono">NAO_REPORTADO</span> e o estudo silenciar sobre algo que se aplica;
<span class="mono">NAO_APLICAVEL</span> e a pergunta nao fazer sentido para aquele
desenho; <span class="mono">INDEFINIDO</span> e o estudo falar de modo que nao permite
decidir; <span class="mono">NAO_ACESSIVEL</span> e a informacao existir em material
suplementar que nao se obteve. O protocolo (l. 1554) proibe <b>inferir</b> versao de
modelo, prompt, parametro, metrica ou qualificacao de avaliador a partir de suposicao
externa. Na duvida entre reportado e inferido, e ausente.</div>
<div class="alerta"><b>Evidencia e citacao, nao copia.</b> O campo de evidencia recebe
trecho curto, dentro dos limites de citacao. Definicoes vao "verbatim ou quase verbatim
dentro dos limites de direito autoral", nas palavras do proprio protocolo.</div>
</section>

<section id="piloto"><h2>2. O piloto vem antes</h2>
<p>O protocolo (l. 1558) manda pilotar o formulario em <b>ao menos dez estudos</b>,
diversos em tempo e metodo, cobrindo tipos de diagrama e referenciais de avaliacao
diferentes. O piloto avalia clareza dos campos, tempo de extracao, sobreposicao de
categorias, frequencia de dado ausente e viabilidade da extracao em nivel de elemento.</p>
<div class="nota"><b>A selecao do piloto e parcialmente circular, e isso fica declarado.</b>
Dois dos quatro eixos de diversidade exigidos &mdash; tipo de diagrama e referencial de
avaliacao &mdash; so se conhecem <b>depois</b> de extrair. Os outros dois, ano e tipo de
veiculo, estao disponiveis agora e sustentam a escolha inicial. A cobertura dos dois
primeiros tem de ser <b>conferida ao final do piloto</b>, e ampliada se ficar concentrada.</div>
<div class="alerta"><b>Duas exigencias do protocolo que mudam quem faz o trabalho.</b>
Todos os campos <b>interpretativos de evidencia de qualidade</b> sao extraidos
<b>independentemente por dois revisores</b>; metadado objetivo de mapeamento pode sair de
um revisor so, com <b>auditoria independente de ao menos 20 por cento</b>. E qualquer
revisao material do formulario ou do codebook dispara <b>revisao retrospectiva</b> do que
ja foi extraido &mdash; o que e mais um motivo para o piloto vir antes da producao.</div>

<h3>2.1 A amostra sorteada</h3>
<p>Estratos: <b>ano x tipo de veiculo</b>. Uma vaga por estrato nao vazio, e as vagas
restantes para os estratos maiores, com semente <span class="mono">__SEMENTE__</span>
sobre os 52 estudos que tinham texto em 2026-08-18. A cota igual por estrato e proposital
&mdash; o piloto existe para submeter o formulario a casos <b>diferentes</b>, nao para
representar o corpus em proporcao.</p>
<div class="alerta"><b>A amostra esta CONGELADA, e nao e mais recalculada.</b> A primeira
versao do gerador refazia o sorteio a cada execucao, e isso estava errado: o sorteio
depende do conjunto de estudos com texto, que <b>cresce</b> quando um autor responde ao
pedido de copia. Verificado ao entrar o 907_SCOPUS &mdash; a amostra trocava
<span class="mono">762_SCOPUS</span> por <span class="mono">927_SCOPUS</span> sozinha, e a
pagina deixaria de bater com o piloto registrado no log. Os dez agora sao lista fixa;
a regra da semente fica ao lado apenas como <b>proveniencia</b> de como foram obtidos.
Registros recuperados depois entram na fila de extracao, mas <b>nao</b> entram no piloto:
amostra que se reembaralha a cada chegada e alvo movel.</div>
__TAB_ESTRATOS__
__TAB_PILOTO__
<div class="nota"><b>Nada na selecao olhou para o conteudo dos estudos.</b> So ano, tipo de
veiculo e semente. Escolher o piloto pelo que o titulo sugere sobre avaliacao de qualidade
seria selecionar pela <b>variavel dependente</b>, que e a sexta regra de ouro do manual v2.
A procedencia do texto aparece na tabela como informacao, nao como criterio: ela nao entrou
no sorteio.</div>

<h3>2.2 Dois desvios declarados neste piloto</h3>
<div class="alerta"><b>Desvio 1 &mdash; extrator unico.</b> O protocolo exige extracao
independente por <b>dois</b> revisores nos campos interpretativos de qualidade. Este piloto
roda com <b>um so</b>. A consequencia e explicita: o piloto <b>nao fecha o V10 nesta
condicao</b>. Ou entra depois a segunda passagem, que o arquivo de extracao ja acomoda sem
retrabalho porque a chave inclui o extrator, ou o desvio vira <b>emenda</b> e tem de constar
do relato final. O que nao pode e a exigencia sumir em silencio.<br>
<b>Desvio 2 &mdash; tempo medido fora da ficha.</b> Tempo de extracao e uma das cinco
medidas que o protocolo manda o piloto avaliar, e a unica que <b>nao se reconstroi depois</b>.
A ficha nao a captura; ela sera anotada por fora. Se a anotacao falhar, a medida se perde e
o piloto responde quatro das cinco perguntas.</div>
<p>As outras quatro medidas saem do proprio material exportado: <b>frequencia de dado
ausente</b> por contagem dos codigos de ausencia, <b>sobreposicao de categorias</b> e
<b>clareza dos campos</b> pelas notas por campo, e <b>viabilidade da extracao em nivel de
unidade</b> pelo numero de ocorrencias que os campos repetiveis realmente receberem.</p>

<h3>2.3 O desvio que nao e do piloto: a l. 1638 fala do corpus inteiro</h3>
<div class="alerta"><b>Desvio 3 &mdash; dupla codificacao da inadequacao.</b> O desvio 1 acima
e a versao pequena de uma exigencia bem maior, e convem nao confundir as duas. A l. 1558
pede dois extratores nos campos interpretativos <b>do piloto</b>; a l. 1638 abre com
<i>two reviewers independently code <b>all</b> inadequacy data from included studies</i>
&mdash; e do <b>corpus inteiro</b>, nao de dez estudos. Hoje o plano em execucao cobre
<b>zero</b> disso.<br>
<b>O que a exigencia NAO e:</b> ela nao pede dupla codificacao dos 65 campos. Ela diz
<i>inadequacy data</i>, que sao os campos <b>__G_INADEQUACAO__</b>, o grupo <span
class="mono">INADEQUACAO</span>. Isso e o que torna a exigencia praticavel, e vale registrar
antes que ela seja lida como grande demais para caber.</div>
<div class="nota"><b>Consequencia operacional, ja acomodada:</b> a l. 1638 termina exigindo
que <i>the consensus code is stored <b>separately</b> from the original reviewer codes</i>.
A chave do arquivo de extracao ja inclui <span class="mono">extrator</span>, entao o
consenso entra como <span class="mono">extrator=CONSENSO</span> em linhas proprias e os
codigos originais dos dois revisores permanecem recuperaveis, que e o que a linha protege.
<b>Mas isso cria um risco que precisa de regra escrita:</b> cada dado de inadequacao passa a
existir em ate <b>tres</b> linhas, e qualquer contagem que nao filtre por <span
class="mono">extrator</span> triplica. Regra: a <b>sintese</b> le so
<span class="mono">CONSENSO</span>; o calculo de <b>concordancia</b> le so os dois
revisores; nenhuma analise le os tres juntos.</div>
<div class="nota"><b>Qual estatistica, campo a campo</b> &mdash; a propria l. 1638 decide.
Kappa de Cohen serve a decisoes nominais <b>mutuamente exclusivas</b>, o caso dos campos
<b>47</b> e <b>48</b>, que admitem um valor por inadequacao. Alfa de Krippendorff e
<i>preferred when categories are multiple, data are missing, or more than two coders are
involved</i>: e o caso do campo <b>49</b>, que e repetivel e aceita varios portadores na
mesma inadequacao, e do campo <b>50</b>, cuja ausencia e <b>por construcao</b>, ja que so se
preenche quando o estudo reporta. Nao e escolha de gosto, e leitura.</div>
<div class="alerta"><b>O que continua em aberto, e e o que de fato bloqueia:</b> medir
concordancia pressupoe que os dois revisores estejam falando <b>das mesmas unidades</b>. A
l. 1638 diz em que niveis medir, mas <b>nao</b> diz como alinhar as unidades &mdash; e dois
revisores lendo o mesmo estudo podem registrar cinco e sete inadequacoes. Sem regra de
alinhamento nao existe tabela de contingencia e nenhum kappa e computavel. Ha pelo menos
duas saidas &mdash; usar o <b>rotulo nativo</b> (campo __O_ROTULO__) como chave de pareamento, ou
fixar a lista de unidades numa primeira passagem e codificar as dimensoes numa segunda
&mdash; e a escolha <b>tem de ser feita antes</b> das duas passagens, nunca depois de
gerados os dados. Nada disto foi decidido aqui: esta declarado para que nao seja descoberto
na hora de medir.</div>

<h3>2.4 Uma pergunta que o piloto tem de responder: a instancia de avaliacao</h3>
<div class="alerta"><b>O protocolo define tres niveis de analise e este instrumento
implementa um.</b> A l. 157 nomeia o relato, o <b>estudo primario</b> e a <b>instancia de
avaliacao</b>, esta ultima definida como uma combinacao extraivel de tipo de diagrama,
corpus de entrada, configuracao do modelo, condicao de geracao e procedimento de avaliacao.
A ficha extrai <b>por estudo</b>. Um estudo que compare tres modelos em dois tipos de
diagrama e uma linha so, e a variacao interna se perde.<br>
Isso <b>nao</b> foi resolvido agora, e a razao esta na propria l. 1558: a
<b>viabilidade da extracao em nivel de unidade</b> e uma das cinco perguntas que o piloto
existe para responder. Decidir antes de medir seria inverter a ordem &mdash; ou se cria uma
chave que ninguem consegue preencher, ou se descarta uma distincao de que a sintese vai
precisar. Os grupos de repeticao ja registram <b>modelo</b>, <b>construto</b>,
<b>inadequacao</b> e <b>metrica</b> como objetos separados, o que e a metade do caminho; o
que falta e saber se o campo __O_DIAG__ (<i>DiagramType</i>, hoje de nivel de estudo e nao repetivel)
e as condicoes de geracao precisam subir para a mesma granularidade. <b>Ao final do piloto,
com dados na mao, isto volta a mesa</b> e, se mudar, vira emenda com revisao retrospectiva
dos dez.</div>
</section>

<section id="mapa"><h2>3. Mapa dos campos</h2>
<p>São <b>__N_CAMPOS__</b> campos: __N_TAB__ transcritos das duas tabelas do protocolo e
<b>um</b> acrescentado por nos, o 50. Em tipo, __N_FECHADO__ fechados, __N_ABERTO__ abertos
e __N_COMP__ compostos, dos quais __N_REP__ admitem mais de uma ocorrencia por estudo.</p>
__TAB_SECOES__
<div class="nota"><b>Esta ficha e montada a partir do codebook</b>, o arquivo
<span class="mono">analysis/extraction/codebook_extracao.csv</span>. Nenhum campo esta
escrito no gerador. Corrigir o codebook e regerar a pagina muda o formulario sem tocar em
codigo &mdash; e o que torna a revisao do formulario depois do piloto uma operacao barata
em vez de uma reescrita.</div>
<div class="alerta"><b>Tres colunas do codebook sao inferencia nossa, nao do protocolo.</b>
A coluna <b>repetivel</b> nao existe nas tabelas do protocolo: foi marcada <span
class="mono">NAO</span> onde a lista oferece valvula de escape (<i>multiple UML types</i>,
<i>mixed task</i>, <i>mixed textual input</i>, <i>mixed representation</i>) e <span
class="mono">SIM</span> onde nao oferece. A coluna <b>questoes</b> foi derivada em nivel de
<b>faceta</b> da tabela de rastreabilidade, porque as tabelas de extracao nao trazem o
mapeamento campo a campo, embora o texto de abertura afirme que cada campo o tem. A coluna
<b>grupo_repeticao</b> tambem e nossa: o protocolo enuncia a tupla da inadequacao
(l. 1601-1608) mas <b>nao</b> diz que construto, metrica e modelo tem o mesmo problema de
vinculo &mdash; estender o mecanismo aos quatro foi decisao nossa, porque trata-lo so na
SQ2 deixaria os outros tres com o mesmo defeito, silencioso. A quarta,
<b>define_subconjunto</b>, existe porque a coluna <b>questoes</b> fundia duas relacoes
diferentes: <i>e dado de</i> (l. 133-145) e <i>define o subconjunto de</i> (l. 1375-1378).
A confusao era visivel dentro de <b>uma unica linha</b> &mdash; no eixo D a coluna
<span class="mono">questoes</span> dizia <span class="mono">SQ1;SQ4</span> enquanto a regra
de extracao, ao lado, dizia que ele <i>define os subconjuntos de SQ1 a SQ3</i>. Hoje o eixo D
define <b>apenas</b> o subconjunto da SQ4: a A006 secao 4 devolveu SQ1 a SQ3 ao corpus
inteiro, porque construto, inadequacao e metrica podem ser puramente sintaticos e um
denominador de dominio os apagaria. As quatro colunas sao as primeiras coisas que o piloto
deve testar.</div>
<div class="alerta"><b>O campo __O_SEV__ e o unico que nao vem das tabelas do protocolo.</b>
A l. 1601-1608 define a inadequacao como a tupla <span class="mono">&lt;Rv, Od, Cu, Se,
Ex&gt;</span> e a l. 1616 poe a severidade como quinta dimensao da codificacao, mas nenhuma
das duas tabelas de extracao lhe deu casa: <i>Rv</i>, <i>Od</i> e <i>Cu</i> sao os campos __O_REF__,
__O_OPER__ e __O_PORT__, e <i>Ex</i> sao as colunas <span class="mono">evidencia</span> e <span
class="mono">localizacao</span>, que ja existem em <b>toda</b> linha do arquivo de extracao.
So <i>Se</i> ficava de fora, e sem ela a tupla nao fecha.<br>
<b>E aberto, e nao fechado, por leitura literal.</b> A l. 1616 diz que a severidade e
<i>preserved when the study reports a severity scale or task effect</i>: <b>preservada, nao
classificada</b>. Uma lista fechada inventaria uma escala que o estudo nao tem e
normalizaria exatamente o que a linha manda conservar. Preencher <b>so</b> quando o estudo
reporta, com o rotulo e a escala dele; quando nao reporta, escrever <span class="mono">not
reported</span>.<br>
<b>Consequencia mecanica:</b> os campos seguintes desceram uma casa. Nao havia alternativa
&mdash; a severidade e dimensao da inadequacao, entao ela tem de ficar <b>dentro</b> do
grupo <span class="mono">INADEQUACAO</span>, e o grupo tem de ser contiguo. A auditoria
contra o protocolo continua valendo porque a <b>ordem</b> nao mudou: houve uma insercao
declarada, nao um rearranjo.</div>
<div class="nota"><b>A numeracao e nossa, e a correspondencia com as tabelas do protocolo
tem tres trechos.</b> Duas mudancas mexeram nela: entrou a severidade e saiu o campo de
envolvimento humano, fundido no de papel do avaliador. As duas <b>se cancelam</b> depois da
severidade, entao a conversao e simples e vale a pena registra-la em vez de deixa-la para
quem for reler:
<span class="mono">1&ndash;__O_ULT_IGUAL__</span> tem a mesma posicao no protocolo;
<span class="mono">__O_PRIM_MAIS__&ndash;__O_ULT_MAIS__</span> tem posicao <b>numero mais
um</b>, porque o campo 27 do protocolo foi fundido;
<span class="mono">__O_SEV__</span> e nosso e nao tem posicao no protocolo; e de
<span class="mono">__O_PRIM_IGUAL__</span> em diante a posicao volta a coincidir.</div>
<div class="nota"><b>Quatro grupos, doze campos.</b> <span class="mono">MODELO</span> (__G_MODELO__),
<span class="mono">CONSTRUTO</span> (__G_CONSTRUTO__), <span class="mono">INADEQUACAO</span> (__G_INADEQUACAO__) e
<span class="mono">METRICA</span> (__G_METRICA__). O criterio foi estreito de proposito: entram os
campos que descrevem <b>conjuntamente um mesmo objeto</b>. Os campos __O_MET1__ e __O_MET2__, embora tambem
sejam da faceta <i>Metric</i> e repetiveis, ficaram <b>fora</b> &mdash; sao descricoes
abertas e autonomas de procedimento, sem campo irmao com que se alinhar, e agrupa-las criaria
posicoes que nunca se preenchem.</div>

<h3>3.1 Um dado, um dono</h3>
<p>Cada campo pertence a <b>uma</b> pergunta. Antes, doze campos apareciam marcados com
duas, o que parecia inofensivo e nao era: quando o mesmo dado responde a duas perguntas com
<b>bases diferentes</b>, os dois numeros divergem e nada no arquivo diz qual esta certo. O
caso limpo era o contexto de geracao, que a MQ3 relatava sobre <b>todo</b> o corpus enquanto
a SQ6 o relataria sobre o subconjunto de eixo U nao ausente.<br>
<b>Esse caso foi resolvido dividindo a pergunta, e nao mudando o campo de dono.</b> A SQ6
antiga era <b>fundida</b>: perguntava como o conhecimento e fornecido <i>e</i> como os
efeitos pragmaticos sao medidos, e as duas metades pedem <b>denominadores diferentes</b>.
Mover os campos de conhecimento para dentro dela teria feito o estrago que se queria evitar,
porque eles herdariam o subconjunto de eixo U. A <b>SQ6</b> ficou com o conhecimento
fornecido, sobre <b>todo</b> o corpus (l. 1375), e a nova <b>SQ7</b> ficou com os efeitos,
sobre o subconjunto de eixo U nao ausente (l. 1378).</p>
__TAB_DONOS__
<div class="nota"><b>Perder o campo nao e perder a pergunta.</b> Posse de campo e uma coisa;
composicao do produto de sintese e outra. A MQ4 continua produzindo o seu mapa de avaliacao
e reprodutibilidade &mdash; so que a partir de campos cujo dono e MQ1, SQ3 e SQ5, mais o seu
proprio.</div>
<div class="alerta"><b>A MQ5 nao tem campo nenhum, e isso esta certo.</b> Zero campos aqui
seria lido como esquecimento, entao fica declarado: a l. 137 diz que o dado da MQ5 sao
<i>combined categories from MQ2 to MQ4</i> e a l. 1382 explica por que ela e <b>computada</b>
&mdash; uma analise de lacunas rodada sobre um corpus filtrado por relato de evidencia
relataria o filtro da propria revisao como lacuna da literatura. Criar campo para a MQ5
seria pedir ao extrator que respondesse o que a sintese tem de calcular.<br>
<b>O que a tabela acima torna impossivel de ignorar:</b> a MQ3 tem
<b>__N_MQ3__</b> campos proprios e a SQ2 tem <b>__N_SQ2__</b>, sendo a SQ2 a taxonomia de
inadequacoes, que o racional do estudo poe como precedencia numero um. O formulario esta
calibrado para um mapping study convencional. Isso <b>nao</b> foi resolvido: depende de o
piloto medir quantos dos __N_MQ3__ campos da MQ3 realmente se preenchem.</div>

<h3>3.2 O codebook da taxonomia e um segundo artefato</h3>
<p>O arquivo <span class="mono">analysis/extraction/codebook_taxonomia.csv</span> nao e o
mesmo que o de extracao e nao substitui nenhum campo. O de extracao diz <b>quais campos
preencher</b>; o da taxonomia diz <b>o que cada valor significa</b>. Ele cumpre a l. 1634,
que exige de cada codigo definicao, regra de inclusao, regra de exclusao, exemplo positivo,
exemplo negativo, categoria pai, portadores admitidos e historico de revisao. Sao
<b>__N_TAX__ codigos</b>: as __N_TAX_REF__ referencias violadas do campo __O_REF__ e as
__N_TAX_OPE__ operacoes de discrepancia do campo __O_OPER__.</p>
<div class="nota"><b>Portador nao e codigo, e atributo &mdash; por isso sao 14 e nao 25.</b>
A prova esta na propria l. 1634, que poe <i>allowed UML carriers</i> entre os atributos de
cada codigo: se o portador fosse um codigo, o atributo seria circular. Isso bate com a
l. 1668, que poe operacoes e referencias no nivel <b>transversal</b> e deixa os portadores
ao nivel <b>especifico</b>, que e tabulacao cruzada derivada da extracao e nao um segundo
conjunto de codigos a definir a mao. Na v1.0 os __N_TAX__ codigos admitem <b>todos</b> os 11
portadores, e isso e leitura e nao preguica: a restricao real de portador e governada pelo
<b>tipo de diagrama</b> &mdash; nao ha <i>message</i> fora de interacao nem <i>state</i> fora
de maquina de estados &mdash; e estreitar por codigo antes dos dados seria inventar
restricao. Estreitar e tarefa do piloto e da revisao do <i>UML domain validator</i>
(l. 1711).</div>
<div class="alerta"><b>Os __N_TAX_CONSTR__ exemplos da v1.0 sao CONSTRUIDOS, e nenhum deles
pode sobreviver a versao estavel.</b> A l. 1624 manda o codebook existir <b>antes</b> do
piloto, mas a l. 1626 so produz exemplos de fronteira <b>depois</b>, ao comparar codigos
entre estudos. Escrever agora exemplos com cara de literatura seria <b>fabricar
evidencia</b>, e havia um risco pior: exemplos inventados por mim seriam moldados pela
hipotese da dissonancia sintatico-semantica, que e o que a revisao existe para
<b>descobrir</b>. Por isso cada linha declara
<span class="mono">procedencia_exemplo</span>, hoje <span class="mono">construido</span> em
todas as __N_TAX__, e o passo 4 da l. 1626 tem de substitui-las por
<span class="mono">corpus</span>, com <span class="mono">logical_id</span> e pagina. A l. 1755
ja listava <i>codebook provenance</i> como mitigacao declarada da ameaca de normalizacao
taxonomica.<br>
Um codigo nao tem sequer exemplo construido: <span class="mono">emergent category</span>, e
por construcao. Qualquer exemplo positivo inventado ali seria a proposta de uma categoria
nova feita <b>antes</b> dos dados, que e exatamente o que essa categoria existe para impedir.</div>
<div class="nota"><b>Os dois codebooks descrevem o mesmo vocabulario, e isso e um risco.</b>
Os codigos da taxonomia <b>sao</b> os valores dos campos __O_OPER__ e __O_REF__, e os portadores admitidos
<b>sao</b> os valores do campo __O_PORT__. Foi esse tipo de duplicacao sem reconciliacao, entre duas
secoes do protocolo, que produziu as cinco divergencias resolvidas no item 8c. Para que o
defeito nao renasca entre dois arquivos nossos, o gerador <b>interrompe a geracao desta
pagina</b> se os dois lados divergirem em um unico valor ou na ordem.</div>
</section>

<section id="estudos"><h2>4. Os estudos</h2>
<p><b>__N_EST__</b> registros retidos ja tem texto completo, e <b>__N_C1__</b> deles ainda
nao passaram pelo C1. Os retidos <b>sem</b> texto nao aparecem aqui: eles estao no estrato
de atricao, que nao e exclusao, e cujo prazo ainda corre.</p>
<div class="wrap">__TAB_EST__</div>
</section>

<section id="ficha"><h2>5. A ficha</h2>
<div class="barra">
<button id="ant">&larr;</button><select id="sel">__OPCOES__</select><button id="pro">&rarr;</button>
<input id="quem" placeholder="seu nome ou sigla" style="min-width:170px">
<span class="prog" id="prog"></span>
<button id="exp" class="pri">Exportar extracao</button>
<button id="expc">Exportar Portao C</button>
</div>
<div class="nota">O progresso fica gravado <b>neste navegador</b>. Nao troque de maquina no
meio, e exporte os dois CSV ao terminar. Limpar os dados do site apaga o trabalho. A
exportacao da extracao sai no formato longo de
<span class="mono">analysis/extraction/extracao.csv</span>, agora com a coluna
<span class="mono">instancia</span> no formato <span class="mono">INADEQUACAO-2</span>,
vazia fora dos grupos; a do Portao C sai separada, porque desfecho de portao mora no CSV
mestre. A chave de gravacao no navegador passou a <span class="mono">extracao.v2</span>:
a forma guardada mudou, e reaproveitar a v1 misturaria dois formatos no mesmo export.</div>
<div id="form"></div>
</section>
</main>
<footer>Gerado por analysis/scripts/gera_ficha_extracao.py a partir de
analysis/extraction/codebook_extracao.csv. Nenhum dado sai desta pagina.</footer>
<script>__JS__</script></body></html>"""

# Os do piloto foram postos na frente da fila, entao sao os len(PILOTO)
# primeiros e a numeracao "1/10" e simplesmente a posicao.
opcoes = ''.join(
    '<option value="%d">%s%s &middot; %s</option>'
    % (n, 'PILOTO %d/%d &middot; ' % (n + 1, len(PILOTO)) if e_['p'] else '',
       html.escape(e_['id']), html.escape(e_['ti'][:82]))
    for n, e_ in enumerate(EST))

js = (JS.replace('__EST__', json.dumps(EST, ensure_ascii=False))
        .replace('__CAMPOS__', json.dumps(CAMPOS, ensure_ascii=False))
        .replace('__AUS__', json.dumps(AUSENTES))
        .replace('__CAB__', json.dumps(CAB_DADOS)))

pg = (HTML.replace('__CSS__', CSS + EXTRA)
        .replace('__JS__', js)
        .replace('__KPIS__', kpis)
        .replace('__TAB_SECOES__', tab_secoes)
        .replace('__TAB_EST__', tab_est)
        .replace('__TAB_PILOTO__', tab_piloto)
        .replace('__TAB_ESTRATOS__', tab_estratos)
        .replace('__SEMENTE__', str(SEMENTE_PILOTO))
        .replace('__OPCOES__', opcoes)
        .replace('__N_CAMPOS__', str(len(CAMPOS)))
        .replace('__N_TAB__', str(n_tab))
        .replace('__G_MODELO__', faixa('MODELO'))
        .replace('__G_CONSTRUTO__', faixa('CONSTRUTO'))
        .replace('__G_INADEQUACAO__', faixa('INADEQUACAO'))
        .replace('__G_METRICA__', faixa('METRICA'))
        .replace('__O_SEV__', str(ORD[NOSSO]))
        .replace('__O_OPER__', str(ORD[OPER]))
        .replace('__O_REF__', str(ORD[REF]))
        .replace('__O_PORT__', str(ORD[PORT]))
        .replace('__O_ROTULO__', str(ORD['Original label and definition']))
        .replace('__O_DIAG__', str(ORD['DiagramType']))
        .replace('__O_MET1__', str(ORD['SyntacticMetricOrProcedure']))
        .replace('__O_MET2__', str(ORD['SemanticMetricOrProcedure']))
        .replace('__O_ULT_IGUAL__', str(O_ULT_IGUAL))
        .replace('__O_PRIM_MAIS__', str(O_ULT_IGUAL + 1))
        .replace('__O_ULT_MAIS__', str(ORD[NOSSO] - 1))
        .replace('__O_PRIM_IGUAL__', str(ORD[NOSSO] + 1))
        .replace('__TAB_DONOS__', tab_donos)
        .replace('__N_FECHADO__', str(n_fechado))
        .replace('__N_ABERTO__', str(n_aberto))
        .replace('__N_COMP__', str(n_comp))
        .replace('__N_REP__', str(n_rep))
        .replace('__N_EST__', str(len(EST)))
        .replace('__N_TAX__', str(n_tax))
        .replace('__N_TAX_REF__', str(len(_por_pai['REFERENCIA_VIOLADA'])))
        .replace('__N_TAX_OPE__', str(len(_por_pai['OPERACAO_DE_DISCREPANCIA'])))
        .replace('__N_TAX_CONSTR__', str(n_tax_construido))
        .replace('__N_MQ3__', str(len(DONOS['MQ3'])))
        .replace('__N_SQ2__', str(len(DONOS['SQ2'])))
        .replace('__N_C1__', str(n_c1)))

open(OUT, 'w', encoding='utf-8').write(pg)
print('gerado:', OUT)
print('estudos %d | sem C1 %d | campos %d (fechado %d, aberto %d, composto %d) | repetiveis %d'
      % (len(EST), n_c1, len(CAMPOS), n_fechado, n_aberto, n_comp, n_rep))
print('taxonomia: %d codigos (%d referencias, %d operacoes), %d exemplos construidos'
      % (n_tax, len(_por_pai['REFERENCIA_VIOLADA']),
         len(_por_pai['OPERACAO_DE_DISCREPANCIA']), n_tax_construido))
print('piloto %d (semente %d):' % (len(PILOTO), SEMENTE_PILOTO),
      ' '.join(e_['id'] for e_ in EST if e_['p']))
