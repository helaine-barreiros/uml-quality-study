# -*- coding: utf-8 -*-
"""Gera a ficha de extracao: Portao C mais os 64 campos, numa leitura so.

A ficha e DIRIGIDA PELO CODEBOOK. O formulario nao esta escrito neste arquivo:
ele e montado a partir de analysis/extraction/codebook_extracao.csv, campo a
campo. Revisar o codebook depois do piloto muda a pagina sem tocar em codigo,
que e exatamente o que o protocolo l. 1558 preve ao dizer que revisao material
do formulario dispara revisao retrospectiva.

Por que um instrumento so. O C1, os quatro atributos de triagem e os 64 campos
se respondem todos com o PDF aberto. Separar em duas passagens obrigaria a abrir
52 artigos duas vezes, e a segunda leitura reconstruiria de memoria o que a
primeira ja tinha visto.

O formulario e renderizado no navegador, um estudo por vez, a partir de duas
tabelas embutidas: a lista de estudos e a lista de campos. Renderizar 52 x 64
campos no HTML produziria um arquivo inutilmente grande.

Saida: analysis/ficha_extracao.html, autocontida e offline. A exportacao produz
CSV no MESMO cabecalho de analysis/extraction/extracao.csv, e a decisao do
Portao C sai em CSV separado, porque o desfecho de portao mora no CSV mestre e
nao no arquivo de extracao (manual v2, secao 7.1).
"""
import csv, html, json, os, re

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
        'q':     c['questoes'],
        'regra': c['regra_extracao'],
        # exemplos nao viram opcao: em campo aberto a lista do protocolo e
        # ilustrativa, e transforma-la em menu induziria a escolher da lista em
        # vez de registrar o vocabulario nativo.
        'vals':  (vals + ausentes_faltantes(vals)) if fechado else [],
        'ex':    vals if not fechado else [],
    })

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

kpis = ''.join(
    '<div class="kpi %s"><b>%s</b><span>%s</span></div>' % (cls, v, k)
    for v, k, cls in [
        (len(EST), 'estudos com texto', 'ac'),
        (n_c1, 'sem decisao C1', 'wr'),
        (len(CAMPOS), 'campos do protocolo', ''),
        (n_rep, 'campos repetiveis', ''),
        (10, 'minimo do piloto', 'ok'),
    ])


def tab(cab, linhas):
    h = '<table><thead><tr>' + ''.join('<th>%s</th>' % c for c in cab) + '</tr></thead><tbody>'
    for ln in linhas:
        h += '<tr>' + ''.join('<td>%s</td>' % html.escape(str(c)) for c in ln) + '</tr>'
    return h + '</tbody></table>'


tab_secoes = tab(
    ['Secao', 'Faceta', '#Campos', 'Repetiveis'],
    [(sec, fac,
      sum(1 for c in CAMPOS if c['sec'] == sec and c['fac'] == fac),
      sum(1 for c in CAMPOS if c['sec'] == sec and c['fac'] == fac and c['rep']))
     for sec, facs in SECOES for fac in facs])

tab_est = tab(
    ['Registro', 'Ano', 'Tipo', 'Veiculo'],
    [(e_['id'], e_['py'], e_['ty'], e_['t2'][:78]) for e_ in EST])

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
"""

# ------------------------------------------------------------------ js
JS = """
var EST=__EST__,CAMPOS=__CAMPOS__,AUS=__AUS__;
var K='extracao.v1',S=JSON.parse(localStorage.getItem(K)||'{}');
var cur=0;
function salvar(){localStorage.setItem(K,JSON.stringify(S));}
function est(id){if(!S[id])S[id]={gc:'',gcn:'',f:{}};return S[id];}
function ocs(id,o){var e=est(id);if(!e.f[o])e.f[o]=[{}];return e.f[o];}
function preenchido(r){return !!((r.v&&r.v.length)||(r.nat&&r.nat.length));}
function contaEstudo(id){var e=S[id];if(!e)return 0;var n=0;
  for(var o in e.f){if(e.f[o].some(preenchido))n++;}return n;}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

function opcoes(c,sel){var h='<option value="">--</option>';
  c.vals.forEach(function(v){h+='<option value="'+esc(v)+'"'+(v===sel?' selected':'')+'>'+esc(v)+'</option>';});
  return h;}
function ausSel(sel){var h='<option value="">--</option>';
  AUS.forEach(function(v){h+='<option value="'+esc(v)+'"'+(v===sel?' selected':'')+'>'+esc(v)+'</option>';});
  return h;}

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
  CAMPOS.forEach(function(c){
    if(c.sec!==sec){sec=c.sec;fac='';h+='<h3 style="color:var(--tx);border-bottom:2px solid var(--ln);padding-bottom:6px">'+esc(sec)+'</h3>';}
    if(c.fac!==fac){fac=c.fac;h+='<div class="fac">'+esc(fac)+'</div>';}
    var lst=ocs(e0.id,c.o),cheio=lst.some(preenchido);
    h+='<div class="cp'+(cheio?' on':'')+'" data-o="'+c.o+'"><div class="top"><span class="nm">'+esc(c.campo)+'</span>'
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
    h+='</div>';
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
  var o=cp.dataset.o,n=+oc.dataset.n,r=ocs(e0.id,o)[n],k=t.dataset.k;
  if(k==='t'){r.t=t.value;if(!r.v||AUS.indexOf(r.v)<0)r.v=t.value;}
  else r[k]=t.value;
  cp.classList.toggle('on',ocs(e0.id,o).some(preenchido));
  salvar();atualizaProg();
});
document.getElementById('form').addEventListener('change',function(ev){
  if(ev.target.name==='gc'){est(EST[cur].id).gc=ev.target.value;salvar();atualizaProg();}
});
document.getElementById('form').addEventListener('click',function(ev){
  var b=ev.target.closest('[data-mais]');if(!b)return;
  ocs(EST[cur].id,b.dataset.mais).push({});salvar();render();
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
  EST.forEach(function(x){
    var e=S[x.id];if(!e)return;
    CAMPOS.forEach(function(c){
      (e.f[c.o]||[]).forEach(function(r,n){
        if(!preenchido(r))return;
        out.push([x.id,c.campo,n+1,r.v||'',r.nat||'',r.ev||'',r.loc||'',quem,ts,r.nt||'']);
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
extracao do protocolo. Pagina autocontida: funciona offline, nao envia nada para
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
<li><b>Exportar</b> os dois CSV ao final: o da extracao e o do Portao C.</li>
</ol>
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
</section>

<section id="mapa"><h2>3. Mapa dos campos</h2>
<p>São <b>__N_CAMPOS__</b> campos, transcritos das duas tabelas do protocolo: __N_FECHADO__
fechados, __N_ABERTO__ abertos e __N_COMP__ compostos, dos quais __N_REP__ admitem mais de
uma ocorrencia por estudo.</p>
__TAB_SECOES__
<div class="nota"><b>Esta ficha e montada a partir do codebook</b>, o arquivo
<span class="mono">analysis/extraction/codebook_extracao.csv</span>. Nenhum campo esta
escrito no gerador. Corrigir o codebook e regerar a pagina muda o formulario sem tocar em
codigo &mdash; e o que torna a revisao do formulario depois do piloto uma operacao barata
em vez de uma reescrita.</div>
<div class="alerta"><b>Duas colunas do codebook sao inferencia nossa, nao do protocolo.</b>
A coluna <b>repetivel</b> nao existe nas tabelas do protocolo: foi marcada <span
class="mono">NAO</span> onde a lista oferece valvula de escape (<i>multiple UML types</i>,
<i>mixed task</i>, <i>mixed textual input</i>, <i>mixed representation</i>) e <span
class="mono">SIM</span> onde nao oferece. A coluna <b>questoes</b> foi derivada em nivel de
<b>faceta</b> da tabela de rastreabilidade, porque as tabelas de extracao nao trazem o
mapeamento campo a campo, embora o texto de abertura afirme que cada campo o tem. As duas
sao as primeiras coisas que o piloto deve testar.</div>
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
<span class="mono">analysis/extraction/extracao.csv</span>; a do Portao C sai separada,
porque desfecho de portao mora no CSV mestre.</div>
<div id="form"></div>
</section>
</main>
<footer>Gerado por analysis/scripts/gera_ficha_extracao.py a partir de
analysis/extraction/codebook_extracao.csv. Nenhum dado sai desta pagina.</footer>
<script>__JS__</script></body></html>"""

opcoes = ''.join(
    '<option value="%d">%s &middot; %s</option>' % (n, html.escape(e_['id']),
                                                   html.escape(e_['ti'][:88]))
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
        .replace('__OPCOES__', opcoes)
        .replace('__N_CAMPOS__', str(len(CAMPOS)))
        .replace('__N_FECHADO__', str(n_fechado))
        .replace('__N_ABERTO__', str(n_aberto))
        .replace('__N_COMP__', str(n_comp))
        .replace('__N_REP__', str(n_rep))
        .replace('__N_EST__', str(len(EST)))
        .replace('__N_C1__', str(n_c1)))

open(OUT, 'w', encoding='utf-8').write(pg)
print('gerado:', OUT)
print('estudos %d | sem C1 %d | campos %d (fechado %d, aberto %d, composto %d) | repetiveis %d'
      % (len(EST), n_c1, len(CAMPOS), n_fechado, n_aberto, n_comp, n_rep))
