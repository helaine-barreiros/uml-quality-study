# -*- coding: utf-8 -*-
"""Gera a pagina de orientacao e trabalho do segundo revisor.

Duas metades:
  1. o instrumento (o que a revisao procura, os portoes, as regras de fronteira);
  2. a fila de trabalho CEGA, sorteada com semente fixa.

A fila nao mostra a decisao da primeira revisora. Se mostrasse, a concordancia
medida seria concordancia com uma resposta ja vista, e o kappa nao significaria
nada. Por isso o HTML nao carrega os campos gate_*_outcome dos registros sorteados.
"""
import criterios as crit
CRIT = crit.carrega()
crit.exige(CRIT, filtros={'A1', 'A2', 'A3', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5'},
           codigos={'E1', 'E2', 'E4', 'E6', 'E7', 'E7b', 'E8', 'E9'})

import csv, hashlib, html, math, os, random, re

BASE = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study'
CSV  = os.path.join(BASE, 'search/v1_7/automated/records/custom_automated_search_collection.csv')
OUT  = os.path.join(BASE, 'search/v3_0/manual_revisor2.html')
CSS  = open(os.path.join(BASE, 'search/v3_0/scripts/css_gate.css'), encoding='utf-8').read()

SEMENTE = 20260817          # data em que a amostra foi sorteada
FRACAO  = crit.fracao_segundo_revisor(CRIT)   # lida do protocolo, nao fixada aqui

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

# Le o vocabulario de sinalizacao GRAVADO NO CSV, que e o da primeira passagem e
# nao foi migrado: CANDIDATO_E10 continua sendo o nome dos 10 registros marcados
# antes da A004, e o equivalente sob a A004 e CANDIDATO_E12. Os dois ficam no
# conjunto, junto dos nomes novos de B2 e B5, para que a fila continue completa
# quando a revisora primaria passar a usar o vocabulario novo.
FLAGS_INCERTAS = {'INCERTO_SAIDA', 'INCERTO_TAREFA', 'INCERTO_ENTRADA',
                  'INCERTO_PAPEL_LLM', 'INCERTO_SEPARABILIDADE',
                  'CANDIDATO_E10', 'CANDIDATO_E12', 'SEM_RESUMO'}


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

tab_crit = tab(['Codigo', 'O que diz', 'Filtro', '#Registros'], [
    ('E1', 'Nao e relato cientifico completo: editorial, prefacio, keynote, tutorial, slides, poster, resumo-apenas, tese, livro, patente, conteudo web nao cientifico', 'A2', crit.get('E1', 0)),
    ('E2', 'E estudo secundario ou terciario', 'A3', crit.get('E2', 0)),
    ('E3', 'E duplicata ou membro menos completo de familia de publicacao', 'D', crit.get('E3', 0)),
    ('E4', 'Esta fora do escopo temporal ou de idioma', 'A1', crit.get('E4', 0)),
    ('E6', 'Nao usa LLM como componente substantivo na producao, transformacao, complementacao, reparo, refinamento ou revisao de conteudo UML', 'B4', crit.get('E6', 0)),
    ('E7', 'O resultado gerado nao e UML', 'B1', crit.get('E7', 0)),
    ('E7b', 'Ha UML na saida, mas misturado a outra notacao sem contribuicao UML separavel: C4, ER, BPMN, SysML, Mermaid, esboco arquitetural', 'B5', crit.get('E7b', 0)),
    ('E8', 'A tarefa apenas avalia, explica, resume, classifica ou discute um diagrama UML existente, sem alterar conteudo', 'B2', crit.get('E8', 0)),
    ('E9', 'A entrada e codigo, imagem, modelo UML existente, logs ou outro artefato nao textual, sem componente substantivo de requisitos', 'B3', crit.get('E9', 0)),
    ('E12', 'Nao ha instancia de geracao identificavel: o resultado UML nao se separa de outros artefatos, tarefas ou saidas gerados na mesma execucao', 'C1', crit.get('E12', 0)),
])

tab_retirado = tab(['Codigo', 'Situacao', '#Registros'], [
    ('E5', 'Retirado. Falta de texto completo virou atricao: estrato "identificado, nao recuperado", que nao e exclusao.', crit.get('E5', 0)),
    ('E10', 'Retirado. Desdobrado em E12 mais o atributo de extracao "atribuicao do resultado".', crit.get('E10', 0)),
    ('E11', 'Retirado. Substituido pelos eixos L, D e U de extracao. Exigir evidencia de qualidade era filtrar pela variavel dependente da propria revisao.', crit.get('E11', 0)),
])

tab_decid = tab(['Criterio', 'Decidivel no resumo?', 'Observacao operacional'], [
    ('E4', 'Total', 'Metadado objetivo (PY, LA, veiculo). Sem julgamento.'),
    ('E1', 'Total', 'Tipo de item, ausencia de autoria, resumo ou paginas; volume de anais, tese, livro, patente.'),
    ('E2', 'Alta', 'Cuidado com survey: survey da literatura e E2; survey como questionario com participantes e estudo primario.'),
    ('E3', 'Alta no nivel de registro', 'DOI e titulo normalizado resolvem duplicata. Familia de publicacao frequentemente so se confirma no texto completo.'),
    ('E7', 'Parcial', 'So exclui quando o resumo nomeia explicitamente outro produto de saida.'),
    ('E8', 'Parcial', 'So exclui quando o resumo deixa claro que o diagrama ja existe e nao e alterado.'),
    ('E9', 'Parcial', 'So exclui quando o resumo declara explicitamente entrada de codigo, imagem, modelo existente ou logs, sem componente textual.'),
    ('E6', 'Parcial', 'Aplicar com RF-01, RF-02 e RF-03. So em casos limpidos.'),
    ('E7b', 'Parcial', 'Exclui quando o resumo nomeia outra notacao ao lado da UML e nao ha indicio de contribuicao UML separavel. Na duvida, INCERTO_SEPARABILIDADE.'),
    ('E12', 'Nao decidivel', 'Exige texto completo, e resultados. Aqui apenas sinalizar como CANDIDATO_E12.'),
])

tab_b1 = tab(['Conta como UML', 'Nao conta sozinho'], [
    ('"UML", "Unified Modeling Language"', '"diagram", "model", "diagrama"'),
    ('Nome de tipo: class, use case, sequence, activity, state machine, component, deployment, object, communication, package, timing, interaction overview, composite structure',
     '"architecture diagram", "flowchart", "graph"'),
    ('PlantUML, XMI, Ecore quando destinados a codificar UML',
     'Mermaid, C4, ER, BPMN, SysML, que vao para o B5'),
])

tab_rf = tab(['Configuracao', 'Decisao', 'Razao'], [
    ('LLM le requisitos e propoe classes e relacoes; regras convertem para PlantUML', 'Retem', 'O LLM determina o conteudo semantico; as regras formatam'),
    ('LLM gera PlantUML; parser valida e renderiza', 'Retem', 'Validacao nao retira o papel substantivo'),
    ('LLM gera modelo inicial; ferramenta corrige sintaxe', 'Retem', 'Conteudo semantico originado no LLM'),
    ('LLM revisa semanticamente diagrama gerado por regras, alterando conteudo', 'Retem', 'Revisao substantiva, prevista no I5'),
    ('LLM recebe prompt longo e prescritivo, ontologia ou documentos via RAG, e ainda assim decide classes, atributos e relacoes', 'Retem', 'RF-03: contexto restringe o espaco de saida, nao o computa'),
    ('Regras extraem todas as classes e relacoes; o LLM so serializa em PlantUML', 'E6', 'O conteudo ja estava decidido antes do LLM'),
    ('Entrada ja e lista de classes, esquema relacional, modelo existente ou codigo', 'E9, nao E6', 'RF-03: o problema e a natureza da entrada'),
    ('BERT/RoBERTa fine-tuned para classificar sentencas ou extrair elementos', 'E6', 'Nao gera conteudo UML, apenas rotula ou extrai candidatos'),
    ('BERT embeddings mais regras que montam o diagrama', 'E6', 'A autoridade semantica esta nas regras'),
    ('T5, BART, GPT ou modelo text-to-text gerando PlantUML, XMI ou descricao UML', 'Retem', 'O modelo produz conteudo UML avaliavel'),
    ('Artigo chama BERT de "foundation model" mas o usa como classificador', 'E6 no texto completo', 'A autoidentificacao nao basta; o papel operacional decide'),
    ('"language model" de forma ambigua no resumo', 'Retem', 'Excluir por titulo e resumo seria arriscado'),
    ('LLM aparece so na motivacao, no trabalho relacionado ou em trabalhos futuros', 'E7, nao E6', 'O registro nao produz UML; o E6 e julgamento de papel, nao deposito'),
])

tab_dir = tab(['Padrao no resumo', 'Desfecho', 'Filtro'], [
    ('requisitos, user stories ou cenarios --> LLM --> UML', 'RETEM', 'passa B1..B5'),
    ('UML existente --> LLM --> avaliacao, explicacao, critica', 'E8', 'B2'),
    ('UML existente --> LLM --> codigo, testes, documentacao, OCL', 'E7', 'B1'),
    ('codigo, imagem ou logs --> LLM --> UML', 'E9', 'B3'),
    ('requisitos --> regras ou gramatica --> UML, com LLM ausente ou marginal', 'E6', 'B4'),
    ('requisitos --> LLM --> BPMN, ER, C4, SysML ou Mermaid, sem UML', 'E7', 'B1'),
    ('requisitos --> LLM --> UML e Mermaid e C4, sem separar', 'E7b', 'B5'),
    ('LLM gera multiplos artefatos e o UML nao se separa', 'RETEM com CANDIDATO_E12', 'decide em C1'),
])

tab_armadilha = tab(['Armadilha', 'Caso real no corpus', 'Como nao cair'], [
    ('"twin" lexical', '12 dos 25 excluidos por E4 eram extrusoras de rosca dupla, guindastes, security twin peaks', 'Digital twin nao e objeto da revisao'),
    ('"GPT" como substring', 'GPT em afiliacao, nome de projeto ou referencia bibliografica', 'Exigir o LLM no papel de gerador, no mesmo enunciado'),
    ('Nome proprio anterior ao modelo', '376_ACM, de 2014, sistema "GEMINI" de analytics em saude', 'Checar ano e dominio'),
    ('"use case" como cenario de aplicacao', '444_ACM', 'Distinguir de diagrama de casos de uso'),
    ('"survey" ambiguo', '299_ACM, 413_ACM, 958_SCOPUS', 'Survey da literatura e E2; questionario com participantes e primario'),
    ('"review" ambiguo', '616_IEEE, 829_SCOPUS', 'Review como tarefa do LLM difere de review como metodo do estudo'),
    ('Direcao invertida', '22 registros de UML-para-Java, OCL, Rebeca, casos de teste', 'O B1 predica o RESULTADO GERADO, nao a presenca de UML no estudo'),
    ('UML desenhada pelos autores', '790, 844, 768, 910: os autores modelam um sistema de IA em UML e o LLM nao gera nada', 'O B0 e a pergunta certa; sem ele esses casos so morriam dois filtros depois'),
    ('Deposito no E6', '45 registros sem qualquer conteudo UML foram codificados como E6 na primeira passagem', 'Regra de ouro 5, e a descida obrigatoria a partir do B0'),
])

tab_estrato = tab(['Estrato (desfecho da 1a revisao)', '#Total', '#Sorteados'],
                  [(n, t, k) for n, t, k in linhas_estrato])

# ------------------------------------------------------------------ fila cega
# E12 fica fora: o manual v2 o declara nao decidivel por titulo e resumo. Quando o
# caso aparecer, o caminho e reter e marcar CANDIDATO_E12 na lista de incerteza.
CRITS = ['E1', 'E2', 'E3', 'E4', 'E6', 'E7', 'E7b', 'E8', 'E9']
opts = ''.join('<option value="%s">%s</option>' % (c, c) for c in CRITS)

FLAGS = ['INCERTO_SAIDA', 'INCERTO_TAREFA', 'INCERTO_ENTRADA', 'INCERTO_PAPEL_LLM',
         'INCERTO_SEPARABILIDADE', 'CANDIDATO_E12', 'SEM_RESUMO']
opts_flag = ''.join('<option value="%s">%s</option>' % (f, f) for f in FLAGS)

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
    q = html.escape(lid, True)
    cards.append(
        '<article class="rec" data-id="%s">'
        '<div class="rhd"><code>%s</code>%s</div>'
        '<h4>%s</h4><div class="meta">%s</div>%s'
        '%s'
        '<div class="form b0"><span class="rot">B0 &mdash; o LLM gera ou altera conteudo UML?</span>'
        '<label class="op"><input type="radio" name="b_%s" value="SIM"><span>Sim</span></label>'
        '<label class="op"><input type="radio" name="b_%s" value="NAO_OU_DUVIDA">'
        '<span>Nao ou duvida</span></label></div>'
        '<div class="form"><span class="rot">Desfecho</span>'
        '<label class="op"><input type="radio" name="d_%s" value="RETER"><span>Reter</span></label>'
        '<label class="op"><input type="radio" name="d_%s" value="EXCLUIR"><span>Excluir</span></label>'
        '<label class="op"><input type="radio" name="d_%s" value="INCERTO"><span>Incerto</span></label>'
        '<select data-crit="%s"><option value="">criterio, so se excluir...</option>%s</select>'
        '<select data-flag="%s"><option value="">sinalizacao, opcional...</option>%s</select>'
        '<input type="text" data-nota="%s" placeholder="justificativa breve">'
        '</div></article>'
        % (q, e(lid), lk, e(r[i['TI']]), meta,
           ('<div class="kw">%s</div>' % e(kw)) if kw else '', corpo,
           q, q, q, q, q, q, opts, q, opts_flag, q))

JS = """
(function(){
  // v2 no lugar de v1 de proposito: a chave antiga guardava respostas dadas sob o
  // instrumento anterior a A004. Reaproveita-las aqui misturaria dois manuais no
  // mesmo CSV e o kappa deixaria de significar alguma coisa.
  var K='rev2.v2';
  var S=JSON.parse(localStorage.getItem(K)||'{}');
  function salvar(){localStorage.setItem(K,JSON.stringify(S));contar();}
  function contar(){
    var n=0,t=document.querySelectorAll('.rec').length;
    for(var k in S){if(S[k]&&S[k].d&&S[k].b)n++;}
    var el=document.getElementById('prog');
    if(el)el.textContent=n+' de '+t+' completos';
  }
  document.addEventListener('change',function(ev){
    var a=ev.target.closest('.rec'); if(!a)return;
    var id=a.dataset.id; S[id]=S[id]||{};
    if(ev.target.type==='radio'){
      if(ev.target.name.indexOf('b_')===0)S[id].b=ev.target.value;
      else S[id].d=ev.target.value;
    }
    if(ev.target.tagName==='SELECT'){
      if(ev.target.dataset.crit!==undefined)S[id].c=ev.target.value;
      if(ev.target.dataset.flag!==undefined)S[id].f=ev.target.value;
    }
    salvar();
  });
  document.addEventListener('input',function(ev){
    var a=ev.target.closest('.rec'); if(!a)return;
    if(!ev.target.dataset.nota)return;
    var id=a.dataset.id; S[id]=S[id]||{}; S[id].n=ev.target.value; salvar();
  });
  document.querySelectorAll('.rec').forEach(function(a){
    var s=S[a.dataset.id]; if(!s)return;
    if(s.b){var rb=a.querySelector('input[name^="b_"][value="'+s.b+'"]'); if(rb)rb.checked=true;}
    if(s.d){var r=a.querySelector('input[name^="d_"][value="'+s.d+'"]'); if(r)r.checked=true;}
    if(s.c){var sc=a.querySelector('select[data-crit]'); if(sc)sc.value=s.c;}
    if(s.f){var sf=a.querySelector('select[data-flag]'); if(sf)sf.value=s.f;}
    if(s.n){var t=a.querySelector('input[type=text]'); if(t)t.value=s.n;}
  });
  contar();
  var b=document.getElementById('exp');
  if(b)b.addEventListener('click',function(){
    var l=['logical_id,b0,decisao,criterio,sinalizacao,justificativa'];
    document.querySelectorAll('.rec').forEach(function(a){
      var id=a.dataset.id,s=S[id]; if(!s||!s.d)return;
      var q=function(v){v=(v||'').replace(/"/g,'""');return /[",\\n]/.test(v)?'"'+v+'"':v;};
      l.push([id,s.b||'',s.d,s.c||'',s.f||'',q(s.n||'')].join(','));
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
      var s=S[a.dataset.id];a.style.display=(s&&s.d&&s.b)?'none':'';
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
.rec .form.b0{padding-bottom:12px}
.rec .form .rot{font-size:12px;color:var(--dim);min-width:78px}
.rec .form.b0 .rot{color:var(--ac);min-width:0;font-weight:600}
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

FLUXO = """                  CORPUS BRUTO (todos os registros recuperados)
                                   |
==================================== v ==========================================
  PRE-PASSE D - NIVEL DE CORPUS            (mecanico, ANTES da triagem)
================================================================================
   D. E registro unico? (DOI, titulo normalizado)  -- NAO --> E3
      PRISMA: "records removed before screening". Nao destrutivo: vincula em
      duplicate_group, nunca apaga. FAMILIA de publicacao NAO se decide aqui.
                                   |
==================================== v ==========================================
  PORTAO A - FORMAL / METADADO        (objetivo, sem julgamento de conteudo)
================================================================================
   A1. Ano entre jan/2022 e a data da busca, e relato em ingles? -- NAO --> E4
   A2. E relato cientifico completo?                             -- NAO --> E1
       (preprint NAO e motivo de E1)
   A3. E estudo primario?                          -- NAO --> PILHA DE BACKGROUND
       (revisao, mapeamento, survey da literatura)          E2, roteia, nao descarta
                                   |
==================================== v ==========================================
  PORTAO B - SUBSTANTIVO
================================================================================
   B0. O LLM GERA OU ALTERA O CONTEUDO UML?   (conjuncao de I4, I5 e I7)
       SIM            -> RETIDO por via rapida. Anote B1..B5 como atributo.
       NAO ou DUVIDA  -> DESCA e nomeie o filtro que explica.
       *** O B0 ABSOLVE MAS NAO CONDENA ***
       Um "nao" no B0 nunca vira codigo por si. E a protecao estrutural contra
       a pergunta fundida que gerou o deposito de 45 registros no E6.
                                   |
                                   v
   B1. O RESULTADO GERADO INCLUI CONTEUDO UML?
       UML explicito, PlantUML, XMI, representacao avaliavel     -> B2
       O produto e outra coisa: codigo, testes, documentacao,
         exercicios, OCL, outro modelo, ou nada de UML           -> E7
       Resumo ambiguo                                            -> RETER, INCERTO_SAIDA
   B2. ESSE CONTEUDO E PRODUZIDO OU ALTERADO?
       gerado, transformado, completado, reparado, refinado,
         revisado COM alteracao de conteudo                      -> B3
       so avaliado, explicado, resumido, classificado,
         criticado; o diagrama entra e sai igual                 -> E8
       Resumo ambiguo                                            -> RETER, INCERTO_TAREFA
   B3. O QUE ENTRA NO PROCESSO?
       requisitos, user stories, cenarios, especificacoes,
         problem statements, descricoes textuais de dominio      -> B4
       SOMENTE codigo, imagem, modelo existente, logs, ou
         entrada ja estruturada com as decisoes de modelagem     -> E9
       Nao declarado                                             -> RETER, INCERTO_ENTRADA
       B3 VEM ANTES DE B4 de proposito: o teste de variancia
       contrafactual do RF-03 pressupoe saber qual era a entrada.
   B4. QUAL O PAPEL DO MODELO?          [RF-01 + RF-02 + RF-03]
       LLM nomeado propondo, gerando ou revisando elementos
         portadores de significado. Vale ainda que o prompt seja
         longo e prescritivo, que haja RAG, ontologia, gabarito
         de saida ou exemplos few-shot                           -> B5
       Sem LLM; NLP de regras ou gramatica; ML convencional;
         encoder como classificador, extrator ou NER; ou o LLM
         so parafraseia, resume ou formata ENQUANTO REGRAS
         SIMBOLICAS DETERMINAM O CONTEUDO DO MODELO              -> E6
       Papel indistinguivel no resumo                            -> RETER, INCERTO_PAPEL_LLM
   B5. O UML E SEPARAVEL DE OUTRAS NOTACOES?
       so UML, ou UML claramente destacavel do restante          -> RETIDO
       UML citado junto de C4, ER, BPMN, SysML ou Mermaid
         sem contribuicao UML separavel                          -> E7b
       Resumo ambiguo                                     -> RETER, INCERTO_SEPARABILIDADE
                                   |
==================================== v ==========================================
  PORTAO C - TEXTO COMPLETO                    (uma unica saida)
================================================================================
   C1. HA INSTANCIA DE GERACAO IDENTIFICAVEL?
       sim: da para dizer o que o modelo gerou e avalia-lo       -> ELEGIVEL
       nao: o UML se dissolve em artefato agregado, pipeline de
         multiplas saidas ou demonstracao sem resultado
         atribuivel                                              -> E12
                                   |
       Confirmacao dos retidos por incerteza no Portao B
       (E7, E7b, E8, E9, E6) e da familia de publicacao (E3).
                                   |
       CLASSIFICACAO, que NAO exclui: eixos L, D e U, atributo
       "atribuicao do resultado", e os atributos de B1..B5."""

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
<a href="#criterios">Criterios</a><a href="#fluxo">Fluxograma</a><a href="#d">Pre-passe D</a>
<a href="#a">Portao A</a><a href="#b">Portao B</a><a href="#c">Portao C</a>
<a href="#ouro">Regras de ouro</a>
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
<p>Quatro condicoes precisam valer ao mesmo tempo para um estudo interessar: o
<b>resultado gerado</b> inclui UML (I7), esse conteudo e <b>produzido ou alterado</b>
e nao apenas comentado (I5), a <b>entrada</b> tem componente textual (I6), e o
<b>LLM</b> tem autoridade sobre o conteudo semantico (I4). Falhando cada uma delas o
estudo sai por E7, E8, E9 e E6, nessa ordem. Uma quinta condicao, a
<b>separabilidade</b> do UML (I8), fecha por E7b quando ele se mistura a outra
notacao e por E12 quando ele se dissolve em um artefato agregado.</p>
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
<li>Responder o <b>B0</b>: o LLM gera ou altera conteudo UML? Sim, ou nao/duvida.</li>
<li>Registrar <b>reter</b>, <b>excluir</b> ou <b>incerto</b>. Ao excluir, citar
<b>exatamente um</b> criterio primario e justificar em uma linha.</li>
<li>Exportar o CSV ao final e devolve-lo. A concordancia e o kappa de Cohen sao
calculados a partir dele.</li>
</ol>
<div class="nota"><b>O kappa e calculado sobre duas coisas apenas:</b> a sua resposta
ao <b>B0</b> e o <b>criterio nomeado</b> nas exclusoes. Os atributos descritivos que o
manual preve no Portao B (tipo de diagrama, tarefa, entrada, familia de modelo) sao
anotados pela revisora primaria e <b>ficam fora do calculo</b>: exigir concordancia
sobre texto livre tornaria este instrumento impraticavel. Voce nao precisa preenche-los.
A sinalizacao de incerteza tambem e opcional e nao entra no kappa; ela serve para dizer
<i>qual</i> pergunta o texto completo tera de responder.</div>
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
<p>Os criterios de inclusao I1 a I8 <b>nao sao aplicados positivamente</b> aqui. A
inclusao so se confirma na leitura do texto completo. Titulo e resumo servem para
remover o que e claramente inelegivel; todo o resto avanca.</p>
<p>Os oito criterios de inclusao estao numerados <b>na ordem em que os filtros os
testam</b>, e cada um tem um criterio de exclusao correspondente. Isso e proposital:
a lista de inclusao e a lista de exclusao sao a mesma lista lida de dois lados. Quando
voce nomeia um E, esta dizendo qual I falhou.</p>
<p class="lead">Base normativa, protocolo l. 1395: <i>"At title and abstract screening,
uncertainty favors retention. A record is excluded only when an exclusion criterion is
clearly satisfied."</i></p>
</section>

<section id="criterios"><h2>4. Os criterios de exclusao</h2>
<p>Dez criterios vigentes, com quantos registros cada um ja fechou nesta revisao e em
qual filtro cada um e testado. A coluna de contagem serve para voce calibrar
expectativa: E7 e de longe o mais frequente.</p>
__TAB_CRIT__
<h3>4.1 Tres criterios foram retirados</h3>
<p>Se voce ja viu uma versao anterior deste manual, vai sentir falta de <b>E5</b>,
<b>E10</b> e <b>E11</b>. Eles nao existem mais como motivo de exclusao. <b>Nao os
use</b>, e se um registro parecer pedir um deles, veja para onde a coluna manda.</p>
__TAB_RETIRADO__
<div class="alerta">Os codigos do lado E <b>nunca sao renumerados</b>, mesmo com tres
deles fora. Renumerar apagaria o rastro da emenda e invalidaria centenas de decisoes ja
registradas com justificativa campo a campo. Por isso a numeracao tem buracos: e o
historico ficando visivel, nao um descuido.</div>
<h3>4.2 O que da para decidir so com o resumo</h3>
<p>Nem todo criterio e decidivel nesta etapa. Aplicar um criterio pouco decidivel a
partir do resumo e a principal fonte de falso negativo.</p>
__TAB_DECID__
<p><b>Na pratica:</b> apenas E4, E1, E2, E3 e os casos limpidos de E6 a E9 fecham um
registro com seguranca. <b>E7b</b> quase nunca fecha, porque exige ver se o UML se
separa da outra notacao, e <b>E12</b> nao fecha nunca nesta etapa: por isso ele nem
aparece na sua lista de criterios. Se voce suspeitar dele, retenha e marque a
sinalizacao <span class="mono">CANDIDATO_E12</span>. Todo o resto avanca.</p>
</section>

<section id="fluxo"><h2>5. O fluxograma</h2>
<p>A ordem nao e arbitraria. O protocolo (l. 1317) manda registrar <i>"the first
criterion that clearly explains the exclusion"</i>, entao a sequencia determina qual
codigo aparece na tabela PRISMA. Ela vai do mais objetivo e barato (metadado) para o
mais interpretativo (conteudo), e dentro do conteudo vai da saida para a entrada.</p>
<pre class="flow">__FLUXO__</pre>
</section>

<section id="d"><h2>6. Pre-passe D &mdash; duplicatas</h2>
<div class="nota"><b>Voce nao executa este passo.</b> Ele ja rodou sobre o corpus
inteiro antes de a fila ser montada, e esta descrito para explicar por que voce nao vai
encontrar dois registros identicos na sua fila.</div>
<p>A deduplicacao <b>nao e uma pergunta de triagem</b>: e uma operacao mecanica no nivel
do corpus, feita por DOI e por titulo normalizado, antes de qualquer julgamento. Por
isso ela vem antes do Portao A e nao dentro dele. Um registro removido aqui nunca chega
a ser lido, e sai por <b>E3</b>.</p>
<p><b>Familia de publicacao e outra coisa.</b> Mesmo experimento, mesmo dataset, mesmo
artefato, fatiado em varias publicacoes: nao ha DOI repetido nem titulo igual, e o
reconhecimento depende de comparar metodo e resultados. Por isso a familia <b>nao</b> e
resolvida aqui e migra para o texto completo, onde tambem fecha por E3, mantendo-se o
membro mais completo. Nesta revisao ja houve um caso assim, com sete registros do mesmo
grupo.</p>
<div class="alerta">Exclusao e <b>nao destrutiva</b>. O registro permanece na planilha,
marcado e justificado, para sustentar a contagem PRISMA e a rastreabilidade da busca.
Nada e apagado.</div>
</section>

<section id="a"><h2>7. Portao A &mdash; formal e de metadado</h2>
<p>Tres perguntas objetivas, sem julgamento de conteudo. Resolvem volume barato e
sao altamente reprodutiveis entre revisores. Se o Portao A fecha o registro, nao se
discute conteudo.</p>
<ol class="passos">
<li><b>A1 &mdash; escopo.</b> Esta dentro da janela temporal, do idioma e do tipo de
publicacao? Nao, sai por <b>E4</b>.</li>
<li><b>A2 &mdash; relato completo.</b> E resumo, poster, editorial, keynote, tutorial ou
registro de indice sem conteudo? Sim, sai por <b>E1</b>. <b>Preprint nao e E1</b>: um
preprint completo e um relato completo.</li>
<li><b>A3 &mdash; primario.</b> E survey, revisao, mapeamento ou artigo de posicao? Sim,
sai por <b>E2</b>.</li>
</ol>
<div class="nota"><b>O A3 encaminha, nao descarta.</b> Um secundario sai do corpus de
extracao por E2, mas vai para a <b>pilha de background</b>: e onde se procura estudo
primario que a busca nao alcancou, e e insumo da discussao. Marcar E2 nao e jogar fora.</div>
</section>

<section id="b"><h2>8. Portao B &mdash; substantivo</h2>
<p>Uma pergunta de cabeceira, o <b>B0</b>, seguida de cinco filtros nesta ordem:
<b>saida</b> (B1), <b>tarefa</b> (B2), <b>entrada</b> (B3), <b>papel do modelo</b> (B4) e
<b>separabilidade</b> (B5).</p>

<h3>8.1 B0 &mdash; a pergunta de cabeceira</h3>
<p class="lead">O LLM <b>gera ou altera</b> o conteudo UML?</p>
<p>E o enunciado do objeto da revisao em uma linha: a conjuncao de I4, I5 e I7. Se a
resposta for <b>sim</b>, o registro e retido pela via rapida e os cinco filtros viram
apenas anotacao descritiva.</p>
<div class="alerta"><b>O B0 absolve mas nao condena.</b> Um "nao" no B0 nunca vira
codigo de exclusao por si. Ele obriga voce a <b>descer e nomear</b> qual dos cinco
filtros explica a saida. Essa e a protecao estrutural contra a pergunta fundida que, na
primeira passagem, transformou o E6 em deposito de tudo que incomodava: sem o degrau
intermediario, "isso nao me parece o nosso objeto" virava E6 sem que ninguem tivesse de
dizer <i>por que</i>.</div>
<p>Na sua fila, o B0 e o campo cuja concordancia sera medida. Responder "nao ou duvida"
e legitimo e nao obriga voce a excluir: se nenhum dos cinco filtros fecha claramente,
o registro e <b>retido como incerto</b>.</p>

<h3>8.2 Por que esta ordem</h3>
<p>Comecar pela <b>saida</b> e mais eficiente porque "o produto nao e UML" e o descarte
mais frequente e mais objetivo &mdash; sozinho, o E7 responde por mais da metade das
exclusoes deste corpus. A <b>tarefa</b> vem em seguida porque separa gerar de apenas
comentar, o que ainda se decide com pouco texto.</p>
<div class="nota"><b>O B3 vem antes do B4 de proposito.</b> O teste de variancia
contrafactual do RF-03 pressupoe saber qual era a entrada: so da para julgar se o modelo
tinha autoridade semantica depois de saber o que lhe foi dado. Perguntar o papel do
modelo antes da entrada e o que produz a confusao entre E6 e E9.</div>

<h3>8.3 B1 &mdash; identificar a saida</h3>
__TAB_B1__
<p class="lead">Regra do protocolo (l. 176): <i>PlantUML output is eligible only when it
is intended to encode UML.</i></p>

<h3>8.4 B2 &mdash; a tarefa: produzido ou apenas comentado</h3>
<p>O conteudo UML e <b>gerado, transformado, completado, reparado, refinado ou revisado
com alteracao de conteudo</b>? Entao segue. Se ele e apenas <b>avaliado, explicado,
resumido, classificado ou criticado</b> &mdash; o diagrama entra e sai igual &mdash; sai
por <b>E8</b>. Resumo ambiguo: retenha e marque
<span class="mono">INCERTO_TAREFA</span>.</p>
<p>O caso classico de E8 e o estudo que pede ao modelo para <i>explicar</i> ou
<i>avaliar</i> um diagrama pronto. Ha produto textual, ha LLM, ha UML &mdash; e nao ha
geracao. O criterio de decisao e simples: <b>o diagrama mudou?</b></p>

<h3>8.5 B3 &mdash; o que entra no processo</h3>
<p>Entrada com componente textual &mdash; requisitos, user stories, cenarios,
especificacoes, <i>problem statements</i>, descricoes de dominio &mdash; segue. Entrada
<b>somente</b> de codigo, imagem, modelo existente, logs, ou ja estruturada com as
decisoes de modelagem tomadas, sai por <b>E9</b>. Nao declarada: retenha e marque
<span class="mono">INCERTO_ENTRADA</span>.</p>
<div class="nota"><b>Entrada rica nao exclui.</b> Prompt longo e prescritivo, RAG,
ontologia, gabarito de saida ou exemplos <i>few-shot</i> continuam sendo entrada textual
e sao <b>motivo para reter</b>, nao para excluir. A fronteira e outra: quando a entrada
<b>ja carrega as decisoes de modelagem</b> &mdash; a lista de classes e relacoes ja
vem pronta e ao modelo resta transcrever &mdash; entao e <b>E9</b>, nao E6. Um erro
frequente e classificar esse caso como falta de papel do modelo, quando o que falta e
espaco de decisao na entrada.</div>

<h3>8.6 B4 &mdash; identificar a autoridade semantica</h3>
<p>Esta e a pergunta mais dificil do instrumento, e as regras de fronteira foram
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

<div class="panel"><h3 style="margin-top:0">RF-03 &mdash; entrada rica nao transfere autoridade</h3>
<p>Prompt prescritivo, RAG, ontologia de apoio, contexto de dominio e exemplos
<i>few-shot</i> <b>nao</b> retiram do modelo a autoridade semantica. Todos sao formas de
condicionar a geracao, e condicionar nao e determinar.</p>
<p><b>Teste de variancia contrafactual:</b> pergunte se o diagrama <b>poderia sair
diferente</b> mantendo a mesma entrada. Se sim, o modelo esta decidindo, e o registro
segue. Se a entrada determina univocamente a saida &mdash; as classes, os atributos e as
relacoes ja estao dadas e o modelo so muda o formato &mdash; entao nao ha decisao a
avaliar, e o codigo e <b>E9</b> pela entrada, nao E6 pelo papel.</p>
<p>Este teste so pode ser aplicado depois do B3, e e por isso que o B3 vem antes do B4.</p></div>

<p><b>Papel gerativo, aceita:</b> generate, produce, synthesize, construct, derive,
propose, transform, complete, repair, refine, revise, correct. Arquiteturas: prompt
engineering, few-shot, chain-of-thought, RAG, fine-tuning, multi-agent, self-refinement.</p>
<p><b>Papel periferico, rejeita por E6:</b> classifica, rotula, extrai, indexa, recupera,
parafraseia, resume, formata, valida gramatica. Tambem quando as regras extraem todas as
classes e relacoes e o LLM apenas converte para PlantUML.</p>
__TAB_RF__

<h3>8.7 B5 &mdash; separabilidade do UML</h3>
<p>O estudo trata <b>so de UML</b>, ou o UML e claramente destacavel do restante? Entao
o registro e retido. Se o UML aparece citado junto de <b>C4, ER, BPMN, SysML ou
Mermaid</b> e <b>nao ha contribuicao UML separavel</b>, sai por <b>E7b</b>. Resumo
ambiguo: retenha e marque <span class="mono">INCERTO_SEPARABILIDADE</span>.</p>
<div class="nota"><b>Citar outra notacao nao basta.</b> O E7b exige que o UML <i>no
resultado gerado</i> nao se separe. Um estudo que gera diagrama de classes e, de
passagem, menciona que tambem experimentou ER continua sendo E7 ou continua retido,
conforme o caso &mdash; o que importa e se sobra contribuicao UML avaliavel sozinha.
Neste corpus o E7b fechou <b>um</b> registro: e uma fronteira estreita, nao uma vala.</div>

<h3>8.8 A matriz de direcao</h3>
<p>Grande parte dos erros de triagem e erro de <b>direcao</b>: de que lado do processo o
UML esta. UML na entrada com saida sem UML nao e o nosso objeto, por mais que titulo e
resumo estejam cheios das palavras certas.</p>
__TAB_DIR__
</section>

<section id="c"><h2>9. Portao C &mdash; texto completo</h2>
<div class="alerta"><b>Voce nao trabalha neste portao agora.</b> Ele esta descrito para
que voce saiba para onde vao os registros que retiver, e o que acontece com as
sinalizacoes de incerteza que voce deixar marcadas.</div>
<p>O Portao C tem <b>uma unica saida</b>, a pergunta <b>C1</b>: ha instancia de geracao
identificavel? Se da para dizer o que o modelo gerou e avalia-lo, o registro e
<b>elegivel</b>. Se o UML se dissolve em um artefato agregado, em uma pipeline de
multiplas saidas ou em uma demonstracao sem resultado atribuivel, sai por <b>E12</b>.</p>
<p>Alem disso o Portao C <b>confirma</b>, com o texto em maos, os registros que voce
retiver por incerteza no Portao B (E7, E7b, E8, E9, E6) e resolve a <b>familia de
publicacao</b> (E3). E por isso que a sua sinalizacao e util mesmo sendo opcional: ela
diz qual pergunta a leitura tera de responder primeiro.</p>

<h3>9.1 Evidencia de qualidade nao e criterio de elegibilidade</h3>
<p>Esta e a mudanca mais importante em relacao a versoes anteriores do instrumento. A
evidencia de qualidade <b>nao exclui ninguem</b>: ela e registrada na extracao, em tres
eixos independentes derivados das relacoes de Krogstie.</p>
<ul>
<li><b>Eixo L</b>, linguagem: relacao entre modelo e linguagem &mdash; validade textual,
conformidade UML.</li>
<li><b>Eixo D</b>, dominio: relacao entre modelo e dominio &mdash; alegada, contra
requisitos fonte, contra modelo de referencia, julgamento de especialista, rubrica.</li>
<li><b>Eixo U</b>, uso: relacao entre modelo e interprete &mdash; compreensao, atividade
de engenharia, retrabalho.</li>
</ul>
<p>Os tres <b>nunca sao colapsados em uma escala unica</b>. Dobrar adequacao pragmatica
dentro do eixo de dominio repetiria a falha que produziu o deposito do E6: pergunta
fundida gera codigo fundido, e a distincao fica irrecuperavel depois.</p>
<div class="nota"><b>Regra de extracao:</b> registrar o <b>vocabulario nativo primeiro</b>
&mdash; o termo que o estudo usa e a definicao operacional que ele da &mdash; antes de
mapear para o esquema da revisao. Normalizar cedo demais apaga exatamente a variacao
terminologica que e o achado central desta revisao.</div>

<h3>9.2 Texto completo nao obtido e atricao, nao exclusao</h3>
<p>Registro cujo texto completo nao se consegue obter <b>nao e excluido</b>: vai para o
estrato <b>identificado, nao recuperado</b>, sem codigo de exclusao. Todos os demais
criterios afirmam algo <b>sobre o registro</b>; o antigo E5 afirmava algo <b>sobre
nos</b>, sobre a capacidade de acesso dentro de uma janela de tempo. O PRISMA 2020 ja
separa as duas coisas.</p>
<p>O argumento e empirico: na primeira passagem a perda foi <b>sistematica</b> &mdash;
nenhum registro de acesso aberto entre os nao recuperados, periodico recuperado em 83
por cento contra conferencia em 55, e recencia caindo de 79 por cento em 2024 para 53 em
2025. Um codigo de exclusao teria escondido as tres assimetrias.</p>
<p>Hoje ha <b>__N_RET__</b> registros retidos, dos quais <b>__N_TXT__</b> ja com texto
completo obtido. Destes, <b>__N_INC__</b> carregam alguma marca de incerteza que o texto
completo tera de resolver.</p>
</section>

<section id="ouro"><h2>10. Regras de ouro</h2>
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
nao para "nao gostei do estudo". Na primeira passagem 45 registros <b>sem nenhum
conteudo UML</b> foram codificados como E6 &mdash; eram E7.</li>
<li><b>Nao filtre pela variavel dependente.</b> Excluir um estudo porque ele nao mediu
qualidade, ou porque mediu de um jeito fraco, seria selecionar pelo desfecho: a revisao
passaria a descrever o proprio filtro em vez da literatura. O que o estudo mediu vai
para os eixos L, D e U, na extracao.</li>
</ol>
</section>

<section id="armadilhas"><h2>11. Armadilhas ja comprovadas neste corpus</h2>
<p>Nao sao hipoteses. Cada linha aconteceu com registros reais desta busca.</p>
__TAB_ARM__
</section>

<section id="amostra"><h2>12. Como sua fila foi montada</h2>
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

<section id="fila"><h2>13. Sua fila de trabalho</h2>
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
        .replace('__TAB_RETIRADO__', tab_retirado)
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
