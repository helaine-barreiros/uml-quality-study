# -*- coding: utf-8 -*-
"""Gera a pagina de orientacao e trabalho do segundo revisor.

Duas metades:
  1. o instrumento (o que a revisao procura, os portoes, as regras de fronteira);
  2. a fila de trabalho CEGA, sorteada com semente fixa.

A fila nao mostra a decisao da primeira revisora. Se mostrasse, a concordancia
medida seria concordancia com uma resposta ja vista, e o kappa nao significaria
nada. Por isso o HTML nao carrega os campos gate_*_outcome dos registros sorteados.
"""
import csv, hashlib, html, math, os, random, re

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSV  = os.path.join(BASE, 'search/automated/custom_automated_search_collection.csv')
OUT  = os.path.join(BASE, 'analysis/manual_revisor2.html')
CSS  = open(os.path.join(BASE, 'analysis/scripts/css_gate.css'), encoding='utf-8').read()

SEMENTE = 20260817          # data em que a amostra foi sorteada
FRACAO  = 0.20              # protocolo v1.8 l.1435: ao menos 20 por cento

rows = list(csv.reader(open(CSV, encoding='utf-8')))
i = {c: n for n, c in enumerate(rows[0])}
data = rows[1:]


def limpa(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()


def e(s):
    return html.escape(limpa(s))


# ------------------------------------------------------------------ numeros
ret = [r for r in data if r[i['excluded']] != 'true']
exc = [r for r in data if r[i['excluded']] == 'true']
crit = {}
for r in exc:
    crit[r[i['exclusion_criteria']]] = crit.get(r[i['exclusion_criteria']], 0) + 1
com_texto = [r for r in ret if r[i['pdf_status']].startswith('OK_')]

FLAGS_INCERTAS = {'INCERTO_SAIDA', 'INCERTO_PAPEL_LLM', 'INCERTO_ENTRADA',
                  'CANDIDATO_E10', 'SEM_RESUMO'}


def flags(r):
    return {f.strip() for f in (r[i['gate_c_flags']] or '').split(';') if f.strip()}


incertos = [r for r in ret if flags(r) & FLAGS_INCERTAS]

# ------------------------------------------------------------------ amostra
# Estrato = o desfecho real, usado apenas para sortear de forma proporcional.
# O estrato nunca e impresso ao lado do registro na fila de trabalho.
def estrato(r):
    if r[i['excluded']] != 'true':
        return 'RETIDO'
    return r[i['exclusion_criteria']] or 'SEM_CRITERIO'


estratos = {}
for r in data:
    estratos.setdefault(estrato(r), []).append(r)

def semente_do_estrato(nome):
    """Semente propria por estrato (manual v2, secao 11).

    Um unico fluxo random.Random(SEMENTE) percorrendo os estratos em ordem faz o
    sorteio de cada estrato depender do TAMANHO de todos os anteriores: mudar a
    contagem de E1 reembaralha E12, E2, E3 e todos os seguintes, ainda que esses
    estratos nao tenham sido tocados. O defeito foi observado na primeira
    passagem, quando uma reclassificacao que nao mexeu em E8, E9 nem RETIDO
    trocou 122 dos 201 sorteados. Derivar a semente do nome do estrato isola cada
    sorteio: reclassificar um registro so remexe os dois estratos envolvidos.

    sha256 e usado por ser estavel entre execucoes e entre maquinas, ao contrario
    de hash(), que o Python aleatoriza por processo.
    """
    h = hashlib.sha256(nome.encode('utf-8')).digest()[:4]
    return SEMENTE + int.from_bytes(h, 'big')


amostra_ids = set()
linhas_estrato = []
for nome in sorted(estratos):
    grupo = sorted(estratos[nome], key=lambda r: r[i['logical_id']])
    # arredonda para CIMA: o protocolo pede 'ao menos' 20 por cento, e
    # arredondar para baixo em varios estratos derrubaria o total abaixo do minimo
    k = max(1, math.ceil(len(grupo) * FRACAO))
    sel = random.Random(semente_do_estrato(nome)).sample(grupo, k)
    amostra_ids.update(r[i['logical_id']] for r in sel)
    linhas_estrato.append((nome, len(grupo), k))

ids_incertos = {r[i['logical_id']] for r in incertos}
fila_ids = amostra_ids | ids_incertos
fila = [r for r in data if r[i['logical_id']] in fila_ids]
fila.sort(key=lambda r: r[i['logical_id']])
so_incerto = len(ids_incertos - amostra_ids)

# ------------------------------------------------------------------ blocos
def tab(cabec, linhas, classes=''):
    th = ''.join('<th%s>%s</th>' % (' class="n"' if c.startswith('#') else '', e(c.lstrip('#')))
                 for c in cabec)
    tr = ''
    for ln in linhas:
        tds = ''.join('<td%s>%s</td>' % (' class="n"' if isinstance(v, int) else '',
                                         v if isinstance(v, str) and v.startswith('<') else
                                         (str(v) if isinstance(v, int) else e(str(v))))
                      for v in ln)
        tr += '<tr>%s</tr>' % tds
    return '<table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (classes, th, tr)


kpis = ''.join(
    '<div class="kpi %s"><b>%s</b><span>%s</span></div>' % (c, v, s)
    for v, s, c in [
        (len(data), 'registros na busca', ''),
        (len(exc), 'excluidos ate aqui', 'wr'),
        (len(ret), 'retidos', 'ok'),
        (len(com_texto), 'com texto completo', 'ac'),
        (len(fila), 'na sua fila', 'ac'),
    ])

tab_crit = tab(['Criterio', 'O que diz', '#Registros'], [
    ('E1', 'Nao e relato cientifico completo', crit.get('E1', 0)),
    ('E2', 'Estudo secundario ou terciario', crit.get('E2', 0)),
    ('E3', 'Duplicata ou membro menos completo de familia de publicacao', crit.get('E3', 0)),
    ('E4', 'Fora do escopo temporal ou de idioma', crit.get('E4', 0)),
    ('E5', 'Texto completo inacessivel apos tentativas documentadas', crit.get('E5', 0)),
    ('E6', 'LLM nao e componente substantivo na producao do conteudo UML', crit.get('E6', 0)),
    ('E7', 'A saida nao e UML, ou nao ha resultado UML separavel', crit.get('E7', 0)),
    ('E8', 'So avalia, explica ou classifica UML existente, sem alterar conteudo', crit.get('E8', 0)),
    ('E9', 'A entrada e codigo, imagem, modelo ou log, sem componente textual', crit.get('E9', 0)),
    ('E10', 'O resultado UML nao se separa de outros artefatos ou tarefas', crit.get('E10', 0)),
    ('E11', 'Nao ha evidencia extraivel sobre a qualidade do UML gerado', crit.get('E11', 0)),
])

tab_decid = tab(['Criterio', 'Decidivel no resumo?', 'Observacao operacional'], [
    ('E4', 'Total', 'Metadado objetivo (ano, idioma, veiculo). Sem julgamento.'),
    ('E1', 'Total', 'Tipo de item, ausencia de autoria ou paginas, volume de anais, tese, livro, patente.'),
    ('E2', 'Alta', 'Cuidado com survey: survey da literatura e E2; questionario com participantes e primario.'),
    ('E3', 'Alta no nivel de registro', 'DOI e titulo normalizado resolvem duplicata. Familia de publicacao costuma so se confirmar no texto completo.'),
    ('E7', 'Parcial', 'So exclui quando o resumo nomeia outra notacao sem componente UML separavel.'),
    ('E8', 'Parcial', 'So exclui quando fica claro que o diagrama ja existe e nao e alterado.'),
    ('E6', 'Parcial', 'Aplicar com RF-01 e RF-02. So em casos limpidos.'),
    ('E9', 'Parcial', 'So exclui quando o resumo declara entrada de codigo, imagem, modelo ou log sem componente textual.'),
    ('E10', 'Baixa', 'Quase sempre exige texto completo. Aqui apenas sinalizar.'),
    ('E11', 'Nao decidivel', 'Regra explicita do protocolo. Ausencia de vocabulario de qualidade nunca exclui.'),
    ('E5', 'Fora desta etapa', 'Pertence a fase de obtencao do PDF.'),
])

tab_b1 = tab(['Conta como UML', 'Nao conta sozinho'], [
    ('"UML", "Unified Modeling Language"', '"diagram", "model", "diagrama"'),
    ('Nome de tipo: class, use case, sequence, activity, state machine, component, deployment, object, communication, package, timing',
     '"architecture diagram", "flowchart", "graph"'),
    ('PlantUML, XMI, Ecore quando destinados a codificar UML',
     'Mermaid, C4, ER, BPMN, SysML, fora salvo componente UML separavel'),
])

tab_rf = tab(['Configuracao', 'Decisao', 'Razao'], [
    ('LLM le requisitos e propoe classes e relacoes; regras convertem para PlantUML', 'Retem', 'O LLM determina o conteudo semantico; as regras formatam'),
    ('LLM gera PlantUML; parser valida e renderiza', 'Retem', 'Validacao nao retira o papel substantivo'),
    ('LLM gera modelo inicial; ferramenta corrige sintaxe', 'Retem', 'Conteudo semantico originado no LLM'),
    ('LLM revisa semanticamente diagrama gerado por regras, alterando conteudo', 'Retem', 'Revisao substantiva, prevista no I3'),
    ('Regras extraem tudo; LLM apenas transforma em PlantUML', 'E6, ou E10 conforme o caso', 'O LLM e formatador superficial, nao gerador semantico'),
    ('BERT/RoBERTa fine-tuned para classificar sentencas ou extrair classes e relacoes', 'E6', 'Nao gera conteudo UML, apenas rotula ou extrai candidatos'),
    ('BERT embeddings mais regras que montam o diagrama', 'E6', 'A autoridade semantica esta nas regras'),
    ('T5, BART, GPT ou modelo text-to-text gerando PlantUML, XMI ou descricao UML', 'Retem', 'O modelo produz conteudo UML avaliavel'),
    ('Artigo chama BERT de "foundation model" mas o usa como classificador', 'E6 no texto completo', 'A autoidentificacao nao basta; o papel operacional decide'),
    ('Artigo usa "language model" de forma ambigua no resumo', 'Retem', 'Excluir por titulo e resumo seria arriscado'),
    ('LLM apenas avalia ou explica diagrama existente', 'E8', 'Nao ha producao, transformacao, reparo ou revisao'),
])

tab_dir = tab(['Padrao no resumo', 'Desfecho'], [
    ('requisitos, user stories ou cenarios --> LLM --> UML', 'RETEM'),
    ('UML existente --> LLM --> avaliacao, explicacao, critica', 'E8'),
    ('UML existente --> LLM --> codigo, testes, documentacao', 'E7'),
    ('codigo, imagem ou logs --> LLM --> UML', 'E9 (o I2 passa; falha a entrada)'),
    ('requisitos --> regras ou gramatica --> UML, com LLM ausente ou marginal', 'E6'),
    ('requisitos --> LLM --> BPMN, ER, C4, SysML ou Mermaid sem UML separavel', 'E7'),
    ('LLM gera multiplos artefatos e o UML nao se separa', 'RETEM com flag E10'),
])

tab_armadilha = tab(['Armadilha', 'Caso real no corpus', 'Como nao cair'], [
    ('"twin" lexical', '12 dos 25 excluidos por E4 eram extrusoras de rosca dupla, guindastes, security twin peaks', 'Digital twin nao e objeto da revisao'),
    ('"GPT" como substring', 'GPT em afiliacao, nome de projeto ou referencia bibliografica', 'Exigir o LLM no papel de gerador, no mesmo enunciado'),
    ('Nome proprio anterior ao modelo', '376_ACM, de 2014, sistema "GEMINI" de analytics em saude', 'Checar ano e dominio'),
    ('"use case" como cenario de aplicacao', '444_ACM', 'Distinguir de diagrama de casos de uso'),
    ('"survey" ambiguo', '299_ACM, 413_ACM, 958_SCOPUS', 'Survey da literatura e E2; questionario com participantes e primario'),
    ('"review" ambiguo', '616_IEEE, 829_SCOPUS', 'Review como tarefa do LLM difere de review como metodo do estudo'),
])

tab_estrato = tab(['Estrato (desfecho da 1a revisao)', '#Total', '#Sorteados'],
                  [(n, t, k) for n, t, k in linhas_estrato])

# ------------------------------------------------------------------ fila cega
CRITS = ['E1', 'E2', 'E3', 'E4', 'E6', 'E7', 'E8', 'E9', 'E10']
opts = ''.join('<option value="%s">%s</option>' % (c, c) for c in CRITS)

cards = []
for r in fila:
    lid = r[i['logical_id']]
    veic = limpa(r[i['T2']]) or limpa(r[i['J2']])
    ano = limpa(r[i['PY']])
    ab = limpa(r[i['AB']])
    kw = limpa(r[i['KW']])
    doi = limpa(r[i['DO']])
    meta = ' &middot; '.join(x for x in [e(veic), e(ano), e(limpa(r[i['TY']]) or limpa(r[i['M3']]))] if x)
    corpo = ('<p class="ab">%s</p>' % e(ab) if ab
             else '<p class="ab semab">Este registro nao tem resumo na base. '
                  'Decida pelo titulo, veiculo e palavras-chave, e assinale <b>incerto</b> '
                  'se isso nao bastar.</p>')
    lk = ''
    if doi:
        lk = ('<a class="lk" target="_blank" rel="noopener" href="https://doi.org/%s">DOI</a>'
              % html.escape(doi, True))
    cards.append(
        '<article class="rec" data-id="%s">'
        '<div class="rhd"><code>%s</code>%s</div>'
        '<h4>%s</h4><div class="meta">%s</div>%s'
        '%s'
        '<div class="form">'
        '<label class="op"><input type="radio" name="d_%s" value="RETER"><span>Reter</span></label>'
        '<label class="op"><input type="radio" name="d_%s" value="EXCLUIR"><span>Excluir</span></label>'
        '<label class="op"><input type="radio" name="d_%s" value="INCERTO"><span>Incerto</span></label>'
        '<select data-crit="%s"><option value="">criterio...</option>%s</select>'
        '<input type="text" data-nota="%s" placeholder="justificativa breve">'
        '</div></article>'
        % (html.escape(lid, True), e(lid), lk, e(r[i['TI']]), meta,
           ('<div class="kw">%s</div>' % e(kw)) if kw else '', corpo,
           html.escape(lid, True), html.escape(lid, True), html.escape(lid, True),
           html.escape(lid, True), opts, html.escape(lid, True)))

JS = """
(function(){
  var K='rev2.v1';
  var S=JSON.parse(localStorage.getItem(K)||'{}');
  function salvar(){localStorage.setItem(K,JSON.stringify(S));contar();}
  function contar(){
    var n=0,t=document.querySelectorAll('.rec').length;
    for(var k in S){if(S[k]&&S[k].d)n++;}
    var el=document.getElementById('prog');
    if(el)el.textContent=n+' de '+t+' decididos';
  }
  document.addEventListener('change',function(ev){
    var a=ev.target.closest('.rec'); if(!a)return;
    var id=a.dataset.id; S[id]=S[id]||{};
    if(ev.target.type==='radio')S[id].d=ev.target.value;
    if(ev.target.tagName==='SELECT')S[id].c=ev.target.value;
    salvar();
  });
  document.addEventListener('input',function(ev){
    var a=ev.target.closest('.rec'); if(!a)return;
    if(!ev.target.dataset.nota)return;
    var id=a.dataset.id; S[id]=S[id]||{}; S[id].n=ev.target.value; salvar();
  });
  document.querySelectorAll('.rec').forEach(function(a){
    var s=S[a.dataset.id]; if(!s)return;
    if(s.d){var r=a.querySelector('input[value="'+s.d+'"]'); if(r)r.checked=true;}
    if(s.c){var sel=a.querySelector('select'); if(sel)sel.value=s.c;}
    if(s.n){var t=a.querySelector('input[type=text]'); if(t)t.value=s.n;}
  });
  contar();
  var b=document.getElementById('exp');
  if(b)b.addEventListener('click',function(){
    var l=['logical_id,decisao,criterio,justificativa'];
    document.querySelectorAll('.rec').forEach(function(a){
      var id=a.dataset.id,s=S[id]; if(!s||!s.d)return;
      var q=function(v){v=(v||'').replace(/"/g,'""');return /[",\\n]/.test(v)?'"'+v+'"':v;};
      l.push([id,s.d,s.c||'',q(s.n||'')].join(','));
    });
    var bl=new Blob([l.join('\\n')],{type:'text/csv;charset=utf-8'});
    var u=URL.createObjectURL(bl),a=document.createElement('a');
    a.href=u;a.download='revisor2_decisoes.csv';a.click();URL.revokeObjectURL(u);
  });
  var f=document.getElementById('filtro');
  if(f)f.addEventListener('input',function(){
    var q=f.value.toLowerCase();
    document.querySelectorAll('.rec').forEach(function(a){
      a.style.display=a.textContent.toLowerCase().indexOf(q)>=0?'':'none';
    });
  });
  var p=document.getElementById('pend');
  if(p)p.addEventListener('click',function(){
    document.querySelectorAll('.rec').forEach(function(a){
      var s=S[a.dataset.id];a.style.display=(s&&s.d)?'none':'';
    });
  });
})();
"""

EXTRA = """
.rec{background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:16px 18px;margin:14px 0}
.rec .rhd{display:flex;gap:10px;align-items:center;margin-bottom:6px}
.rec code{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--ac);
  background:var(--pan2);border:1px solid var(--ln);border-radius:6px;padding:2px 8px}
.rec h4{margin:2px 0 4px;font-size:15.5px;line-height:1.4}
.rec .meta{color:var(--dim);font-size:12.5px;margin-bottom:8px}
.rec .kw{color:var(--dim);font-size:11.5px;font-family:ui-monospace,Menlo,monospace;
  margin-bottom:8px;padding-bottom:8px;border-bottom:1px dashed var(--ln)}
.rec .ab{font-size:13.5px;color:#c8cede;max-width:none;margin:0 0 12px}
.rec .ab.semab{color:var(--wr);font-style:italic}
.rec .form{display:flex;gap:10px;flex-wrap:wrap;align-items:center;
  border-top:1px solid var(--ln);padding-top:12px}
.op{display:inline-flex;align-items:center;gap:5px;font-size:13px;
  background:var(--pan2);border:1px solid var(--ln);border-radius:8px;padding:5px 11px;cursor:pointer}
.op input{margin:0}
.form select,.form input[type=text]{background:var(--pan2);color:var(--tx);
  border:1px solid var(--ln);border-radius:8px;padding:6px 10px;font:13px inherit}
.form input[type=text]{flex:1;min-width:220px}
.lk{font-size:11.5px;text-decoration:none;border:1px solid var(--ln);border-radius:6px;padding:2px 8px;color:var(--dim)}
.barra{position:sticky;top:41px;z-index:8;background:rgba(15,17,21,.95);backdrop-filter:blur(8px);
  border:1px solid var(--ln);border-radius:12px;padding:12px 16px;margin:18px 0;
  display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.barra input[type=text]{background:var(--pan2);color:var(--tx);border:1px solid var(--ln);
  border-radius:8px;padding:7px 12px;font:13px inherit;flex:1;min-width:200px}
.barra button{background:var(--pan2);color:var(--tx);border:1px solid var(--ln);
  border-radius:8px;padding:7px 14px;font:13px inherit;cursor:pointer}
.barra button:hover{border-color:var(--ac);color:var(--ac)}
#prog{color:var(--ok);font-size:13px;font-variant-numeric:tabular-nums}
.alerta{background:#1e1a10;border-left:3px solid var(--wr);padding:14px 18px;border-radius:0 10px 10px 0;margin:18px 0}
.nota{background:#0f1a12;border-left:3px solid var(--ok);padding:14px 18px;border-radius:0 10px 10px 0;margin:18px 0}
pre.flow{background:var(--pan);border:1px solid var(--ln);border-radius:12px;padding:16px;
  overflow-x:auto;font:12px/1.5 ui-monospace,Menlo,monospace;color:#c8cede}
ol.passos{max-width:88ch}ol.passos li{margin:8px 0}
"""

FLUXO = """                REGISTRO (titulo + resumo + palavras-chave + metadados)
                                   |
==================================== v ==========================================
  PORTAO A - FORMAL / METADADO        (objetivo, sem julgamento de conteudo)
================================================================================
   A1. Ano entre jan/2022 e a data da busca, e relato em ingles? -- NAO --> E4
   A2. E relato cientifico completo?                             -- NAO --> E1
       (nao e editorial, keynote, tutorial, slides, poster,
        resumo-apenas, tese, livro, patente, volume de anais)
   A3. E estudo primario?                                        -- NAO --> E2
       (nao e revisao, mapeamento, survey da literatura)
   A4. E registro unico?                                         -- NAO --> E3
       (nao e duplicata nem membro menos completo de familia)
                                   |
==================================== v ==========================================
  PORTAO B - SUBSTANTIVO   (saida, origem, direcao, entrada, nesta ordem)
================================================================================
   B1. QUAL E O ARTEFATO DE SAIDA?
       UML explicito, ou PlantUML/XMI do qual UML seja avaliavel -> segue
       Outra notacao SEM componente UML separavel                -> E7
       Resumo ambiguo                                            -> RETER, sinalizar
   B2. QUEM DETERMINA O CONTEUDO SEMANTICO?          [RF-01 + RF-02]
       LLM nomeado propondo, gerando ou revisando elementos      -> segue
       Sem LLM; regras; ML convencional; encoder classificador;
         LLM que so parafraseia, resume ou formata               -> E6
       "AI-assisted" sem especificar papel                       -> RETER, sinalizar
   B3. QUAL E A DIRECAO DO FLUXO?
       texto -> LLM -> UML   (o UML e PRODUTO)                   -> segue
       UML existente -> LLM -> avaliacao, resumo, critica        -> E8
       UML existente -> LLM -> codigo, testes, documentacao      -> E7
       LLM revisa ou repara UML ALTERANDO o conteudo             -> segue (I3)
   B4. O QUE ENTRA NO PROCESSO?
       Requisitos, user stories, cenarios, descricoes de dominio -> RETER
       SOMENTE codigo, imagem, modelo existente ou logs          -> E9
       Nao declarado no resumo                                   -> RETER, sinalizar
                                   |
==================================== v ==========================================
  PORTAO C - EVIDENCIA DE QUALIDADE       *** NAO EXCLUI NESTA ETAPA ***
================================================================================
   C1. O resumo menciona avaliacao, medicao, acuracia, correcao,
       completude, comparacao, estudo com humanos, benchmark?
             SIM -> RETIDO, flag EVIDENCIA=EXPLICITA
             NAO -> RETIDO, flag EVIDENCIA=A_VERIFICAR
                                   |
                    +-------------------------------+
                    |  RETIDO PARA TEXTO COMPLETO   |
                    |  E10 e E11 decididos la       |
                    +-------------------------------+"""

HTML = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Manual do segundo revisor &mdash; qualidade de UML gerada por LLM</title>
<style>__CSS__</style></head><body>
<header>
<div class="eyebrow">Revisao sistematica &middot; Universidade de Pernambuco</div>
<h1>Manual do segundo revisor</h1>
<p>Qualidade de diagramas UML gerados por modelos de linguagem a partir de
especificacoes textuais. Este documento apresenta o instrumento de triagem e
entrega a sua fila de trabalho. Pagina autocontida: funciona offline, nao envia
nada para lugar nenhum, e o que voce responder fica gravado neste navegador.</p>
</header>

<div class="nav">
<a href="#objeto">O objeto</a><a href="#papel">Seu papel</a><a href="#principio">Principio</a>
<a href="#criterios">Criterios</a><a href="#fluxo">Fluxograma</a><a href="#a">Portao A</a>
<a href="#b">Portao B</a><a href="#c">Portao C</a><a href="#ouro">Regras de ouro</a>
<a href="#armadilhas">Armadilhas</a><a href="#amostra">A amostra</a><a href="#fila">Sua fila</a>
</div>

<main>
<div class="kpis">__KPIS__</div>

<section id="objeto"><h2>1. O que a revisao investiga</h2>
<p>A pergunta e se um modelo de linguagem, ao receber <b>texto</b> &mdash; requisitos,
user stories, cenarios, descricoes de dominio &mdash; produz <b>UML</b> cuja qualidade
possa ser avaliada. O interesse central e a dissonancia entre sintaxe e semantica:
um diagrama pode estar formalmente bem construido e, ainda assim, dizer a coisa
errada sobre o dominio.</p>
<p>Tres elementos precisam estar presentes ao mesmo tempo para um estudo interessar:
a <b>entrada</b> e textual, o <b>LLM</b> tem autoridade sobre o conteudo semantico do
diagrama, e a <b>saida</b> e UML separavel. Falhando qualquer um deles o estudo sai,
por E9, E6 ou E7 respectivamente.</p>
<div class="nota"><b>A string de busca e deliberadamente ampla.</b> Ela nao exige termos
de qualidade, porque estudos usam terminologias divergentes e exigir "semantico" ou
"correctness" na busca eliminaria trabalhos legitimos. O preco disso e ruido lexical
alto, e toda a precisao foi transferida para a triagem que voce vai fazer.</div>
</section>

<section id="papel"><h2>2. O que se espera de voce</h2>
<p>O protocolo (l. 1439) determina que cada registro retido seja avaliado de forma
<b>independente</b> por dois revisores, com discordancias resolvidas por discussao e
impasses por um adjudicador com experiencia em Engenharia de Software e UML ou
modelagem baseada em LLM.</p>
<ol class="passos">
<li>Decidir cada registro da sua fila por <b>titulo, resumo, palavras-chave e
metadados</b>, sem consultar o texto completo nesta etapa.</li>
<li>Registrar <b>reter</b>, <b>excluir</b> ou <b>incerto</b>. Ao excluir, citar
<b>exatamente um</b> criterio primario e justificar em uma linha.</li>
<li>Exportar o CSV ao final e devolve-lo. A concordancia e o kappa de Cohen sao
calculados a partir dele.</li>
</ol>
<div class="alerta"><b>Voce nao ve as decisoes da primeira revisora.</b> Isso e
proposital e nao e desconfianca: uma segunda avaliacao que enxerga a primeira mede
concordancia com uma resposta ja conhecida, e o kappa resultante nao significa nada.
A pagina nao carrega esses campos. A comparacao acontece depois, fora daqui.</div>
<p>A calibracao prevista no protocolo (l. 1431) continua ate <b>80 por cento de
concordancia</b> e <b>kappa de Cohen de ao menos 0,70</b>. Abaixo disso, a divergencia
e discutida e o manual e revisado &mdash; ou seja, discordar tem consequencia sobre o
instrumento, nao so sobre o registro.</p>
</section>

<section id="principio"><h2>3. O principio que governa esta etapa</h2>
<div class="nota" style="font-size:16px"><b>Na triagem por titulo e resumo nao se
inclui nada. So se exclui.</b></div>
<p>Os criterios de inclusao I1 a I6 <b>nao sao aplicados positivamente</b> aqui. A
inclusao so se confirma na leitura do texto completo. Titulo e resumo servem para
remover o que e claramente inelegivel; todo o resto avanca.</p>
<p class="lead">Base normativa, protocolo l. 1395: <i>"At title and abstract screening,
uncertainty favors retention. A record is excluded only when an exclusion criterion is
clearly satisfied."</i></p>
</section>

<section id="criterios"><h2>4. Os criterios de exclusao</h2>
<p>Os onze criterios, com quantos registros cada um ja fechou nesta revisao. A coluna
de contagem serve para voce calibrar expectativa: E7 e de longe o mais frequente.</p>
__TAB_CRIT__
<h3>4.1 O que da para decidir so com o resumo</h3>
<p>Nem todo criterio e decidivel nesta etapa. Aplicar um criterio pouco decidivel a
partir do resumo e a principal fonte de falso negativo.</p>
__TAB_DECID__
<p><b>Na pratica:</b> apenas E4, E1, E2, E3 e os casos limpidos de E6 a E9 fecham um
registro com seguranca. Todo o resto avanca.</p>
</section>

<section id="fluxo"><h2>5. O fluxograma</h2>
<p>A ordem nao e arbitraria. O protocolo (l. 1317) manda registrar <i>"the first
criterion that clearly explains the exclusion"</i>, entao a sequencia determina qual
codigo aparece na tabela PRISMA. Ela vai do mais objetivo e barato (metadado) para o
mais interpretativo (conteudo), e dentro do conteudo vai da saida para a entrada.</p>
<pre class="flow">__FLUXO__</pre>
</section>

<section id="a"><h2>6. Portao A &mdash; formal e de metadado</h2>
<p>Quatro perguntas objetivas, sem julgamento de conteudo. Resolvem volume barato e
sao altamente reprodutiveis entre revisores. Se o Portao A fecha o registro, nao se
discute conteudo.</p>
<p><b>A4 merece atencao.</b> Duplicata no nivel de registro se resolve por DOI e titulo
normalizado. <b>Familia de publicacao</b> &mdash; mesmo experimento, mesmo dataset,
mesmo artefato, fatiado em varias publicacoes &mdash; e diferente, e costuma so se
confirmar no texto completo. Nesta revisao ja houve um caso assim, com sete registros
do mesmo grupo, resolvido mantendo o membro mais completo e excluindo os demais por E3.</p>
<div class="alerta">Exclusao e <b>nao destrutiva</b>. O registro permanece na planilha,
marcado e justificado, para sustentar a contagem PRISMA e a rastreabilidade da busca.
Nada e apagado.</div>
</section>

<section id="b"><h2>7. Portao B &mdash; substantivo</h2>
<p>Quatro perguntas, nesta ordem: <b>saida, origem, direcao, entrada</b>. Comecar pela
saida e mais eficiente porque "nao e UML" e o descarte mais frequente e mais objetivo.
A direcao vem depois da origem porque so faz sentido perguntar de onde vem o conteudo
depois de saber que ha um LLM em jogo.</p>

<h3>7.1 B1 &mdash; identificar a saida</h3>
__TAB_B1__
<p class="lead">Regra do protocolo (l. 176): <i>PlantUML output is eligible only when it
is intended to encode UML.</i></p>

<h3>7.2 B2 &mdash; identificar a autoridade semantica</h3>
<p>Esta e a pergunta mais dificil do instrumento, e duas regras de fronteira foram
escritas <b>antes</b> da triagem justamente para que ela nao fosse decidida caso a caso.</p>

<div class="panel"><h3 style="margin-top:0">RF-01 &mdash; encoders pre-instrucionais (BERT, RoBERTa e similares)</h3>
<p>A autoidentificacao do relato como <i>language model</i> ou <i>foundation model</i>
<b>nao e condicao suficiente</b>. O criterio decisivo e o <b>papel operacional</b> do modelo.</p>
<p>Um encoder pre-treinado satisfaz o criterio <b>somente</b> quando produz, transforma,
completa, repara, refina ou revisa conteudo UML de forma gerativa ou semanticamente
constitutiva. Quando e usado como classificador, <i>sequence tagger</i>, extrator
supervisionado, codificador de <i>embeddings</i> ou componente de NER, o estudo sai por <b>E6</b>.</p>
<p><b>Por que.</b> BERT foi proposto como modelo de representacao bidirecional, adaptado
por <i>fine-tuning</i>, e nao como modelo autorregressivo de geracao instrucional.
Incluir todo estudo com BERT apenas por ser "foundation model" misturaria NLP
supervisionado de extracao com geracao de artefatos por LLM, e diluiria exatamente o
fenomeno que a revisao caracteriza.</p>
<p><b>Ressalva obrigatoria:</b> quando titulo e resumo nao permitirem distinguir o papel
do modelo, o registro e <b>retido</b> para texto completo.</p></div>

<div class="panel"><h3 style="margin-top:0">RF-02 &mdash; autoridade semantica em pipelines hibridos</h3>
<p>O LLM e <b>substantivo</b> quando contribui para decidir, propor ou revisar elementos
UML portadores de significado: classes, atributos, metodos, atores, casos de uso,
relacoes <i>include</i> e <i>extend</i>, mensagens, <i>lifelines</i>, estados,
transicoes, atividades, componentes.</p>
<p>O LLM <b>nao e substantivo</b> quando apenas prepara o texto, resume requisitos,
produz <i>embeddings</i>, corrige gramatica ou formata a saida enquanto regras
simbolicas determinam o conteudo do modelo.</p>
<p><b>A presenca de regras simbolicas no pipeline e irrelevante para a decisao.</b>
Praticamente todo sistema serio tera validacao, <i>parser</i>, <i>renderer</i> ou
<i>templates</i>. A pergunta e sempre a mesma: <b>quem determina o conteudo semantico
do diagrama?</b></p></div>

<p><b>Papel gerativo, aceita:</b> generate, produce, synthesize, construct, derive,
propose, transform, complete, repair, refine, revise, correct. Arquiteturas: prompt
engineering, few-shot, chain-of-thought, RAG, fine-tuning, multi-agent, self-refinement.</p>
<p><b>Papel periferico, rejeita por E6:</b> classifica, rotula, extrai, indexa, recupera,
parafraseia, resume, formata, valida gramatica. Tambem quando as regras extraem todas as
classes e relacoes e o LLM apenas converte para PlantUML.</p>
__TAB_RF__

<h3>7.3 B3 e B4 &mdash; direcao e entrada</h3>
__TAB_DIR__
</section>

<section id="c"><h2>8. Portao C &mdash; evidencia de qualidade</h2>
<div class="alerta"><b>Este portao ainda nao tem manual, e voce nao trabalha nele
agora.</b> Ele esta descrito aqui para que voce saiba para onde vao os registros que
voce retiver, e sera detalhado quando a leitura de texto completo comecar.</div>
<p>Na triagem por titulo e resumo o Portao C <b>nao exclui nada</b>. Ele apenas
classifica: se o resumo menciona avaliacao, medicao, acuracia, correcao, completude,
comparacao, estudo com humanos ou benchmark, o registro recebe
<span class="mono">EVIDENCIA=EXPLICITA</span>; caso contrario,
<span class="mono">EVIDENCIA=A_VERIFICAR</span>.</p>
<p>Os dois criterios que o Portao C decide, ja no texto completo, sao:</p>
<ul>
<li><b>E10</b> &mdash; o resultado UML nao se separa de outros artefatos, tarefas ou
saidas. Tipico de estudos que geram codigo, testes, documentacao e diagramas de uma vez
e reportam so uma metrica agregada.</li>
<li><b>E11</b> &mdash; o relato nao fornece evidencia extraivel sobre qualidade,
validade, correcao, completude, consistencia ou adequacao pragmatica do UML gerado.</li>
</ul>
<p>Hoje ha <b>__N_RET__</b> registros retidos, dos quais <b>__N_TXT__</b> ja com texto
completo obtido. Destes, <b>__N_INC__</b> carregam alguma marca de incerteza que o texto
completo tera de resolver.</p>
</section>

<section id="ouro"><h2>9. Regras de ouro</h2>
<ol class="passos">
<li><b>A incerteza retem.</b> Se voce hesitou, o registro avanca. Custa uma leitura; a
alternativa custa um estudo perdido.</li>
<li><b>Ausencia de vocabulario de qualidade nunca exclui.</b> A busca foi desenhada sem
termos de qualidade justamente porque os estudos usam terminologias divergentes.</li>
<li><b>Um criterio primario por exclusao.</b> Quando mais de um se aplica, registre o
primeiro que explica claramente a exclusao, seguindo a ordem do fluxograma. Os demais
vao na justificativa como secundarios.</li>
<li><b>Exclusao e nao destrutiva.</b> Nada e apagado; tudo fica marcado e justificado.</li>
<li><b>Nao sobrecarregue o E6.</b> Ele e para ausencia de papel substantivo do modelo,
nao para "nao gostei do estudo".</li>
</ol>
</section>

<section id="armadilhas"><h2>10. Armadilhas ja comprovadas neste corpus</h2>
<p>Nao sao hipoteses. Cada linha aconteceu com registros reais desta busca.</p>
__TAB_ARM__
</section>

<section id="amostra"><h2>11. Como sua fila foi montada</h2>
<p>O protocolo (l. 1435) determina que o segundo revisor avalie <b>uma amostra aleatoria
estratificada de ao menos 20 por cento</b> mais <b>todos os registros marcados como
incertos</b>. Sua fila e exatamente a uniao desses dois conjuntos.</p>
<p>O sorteio usa semente fixa <span class="mono">__SEMENTE__</span>, portanto e
reprodutivel: qualquer pessoa que rode o gerador obtem a mesma amostra. O estrato e o
desfecho da primeira revisao, usado <b>apenas para sortear de forma proporcional</b> e
nunca impresso ao lado do registro.</p>
<p>Cada estrato sorteia com <b>semente propria</b>, derivada da semente do estudo mais um
hash estavel do nome do estrato. A alternativa, um unico fluxo aleatorio percorrendo os
estratos em ordem, faz o sorteio de cada estrato depender do tamanho de todos os
anteriores: uma reclassificacao que nao toca um estrato ainda assim reembaralha a amostra
dele. Isso foi observado na primeira passagem, quando uma mudanca que nao mexeu em E8, E9
nem RETIDO trocou 122 dos 201 sorteados. Com semente por estrato, reclassificar um
registro so remexe os dois estratos envolvidos.</p>
__TAB_EST__
<p>Somando, <b>__N_AM__</b> registros vieram do sorteio e <b>__N_SO_INC__</b> entraram
apenas por estarem marcados como incertos, totalizando <b>__N_FILA__</b>.</p>
</section>

<section id="fila"><h2>12. Sua fila de trabalho</h2>
<p>Cada cartao traz identificador, titulo, veiculo, ano, palavras-chave e resumo. Marque
<b>reter</b>, <b>excluir</b> com um criterio, ou <b>incerto</b>. A justificativa breve e
o que torna a discussao de divergencia possivel depois &mdash; sem ela, discordar vira
opiniao contra opiniao.</p>
<div class="barra">
<input type="text" id="filtro" placeholder="filtrar por titulo, id, veiculo, palavra do resumo...">
<span id="prog">0 decididos</span>
<button id="pend">So os pendentes</button>
<button id="exp">Exportar CSV</button>
</div>
<div class="nota">O progresso fica gravado <b>neste navegador</b>. Nao troque de maquina
no meio, e exporte o CSV ao terminar. Limpar os dados do site apaga o trabalho.</div>
__CARDS__
</section>
</main>
<script>__JS__</script></body></html>"""

pg = (HTML.replace('__CSS__', CSS + EXTRA)
        .replace('__JS__', JS)
        .replace('__FLUXO__', html.escape(FLUXO))
        .replace('__KPIS__', kpis)
        .replace('__TAB_CRIT__', tab_crit)
        .replace('__TAB_DECID__', tab_decid)
        .replace('__TAB_B1__', tab_b1)
        .replace('__TAB_RF__', tab_rf)
        .replace('__TAB_DIR__', tab_dir)
        .replace('__TAB_ARM__', tab_armadilha)
        .replace('__TAB_EST__', tab_estrato)
        .replace('__N_RET__', str(len(ret)))
        .replace('__N_TXT__', str(len(com_texto)))
        .replace('__N_INC__', str(len(incertos)))
        .replace('__SEMENTE__', str(SEMENTE))
        .replace('__N_AM__', str(len(amostra_ids)))
        .replace('__N_SO_INC__', str(so_incerto))
        .replace('__N_FILA__', str(len(fila)))
        .replace('__CARDS__', ''.join(cards)))

open(OUT, 'w', encoding='utf-8').write(pg)
print('gerado:', OUT)
print('corpus %d | retidos %d | com texto %d | incertos %d' % (len(data), len(ret), len(com_texto), len(incertos)))
print('amostra %d (%.1f%%) | so incertos %d | fila %d'
      % (len(amostra_ids), 100.0 * len(amostra_ids) / len(data), so_incerto, len(fila)))
