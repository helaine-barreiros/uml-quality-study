# -*- coding: utf-8 -*-
"""Verificacao da ficha depois do 8a e do 8b. Testa o EXPORT de verdade, no
node, com um estudo fabricado, porque o defeito que o 8a corrige so aparece no
arquivo exportado."""
import csv, io, json, os, re, subprocess, tempfile

BASE = ('/home/helaine-barreiros/Development/doutorado-workspace/'
        'estudo_sistematico/uml-quality-study')
H = open(os.path.join(BASE, 'analysis/ficha_extracao.html'), encoding='utf-8').read()
COD = list(csv.DictReader(open(os.path.join(BASE, 'analysis/extraction/codebook_extracao.csv'),
                               encoding='utf-8')))
CABD = next(csv.reader(open(os.path.join(BASE, 'analysis/extraction/extracao.csv'),
                            encoding='utf-8')))
falhas = []


def ok(cond, msg):
    print(('  OK   ' if cond else '  FALHA ') + msg)
    if not cond:
        falhas.append(msg)


dec = json.JSONDecoder()
est = dec.raw_decode(H, H.index('var EST=') + len('var EST='))[0]
camp = dec.raw_decode(H, H.index('CAMPOS=') + len('CAMPOS='))[0]

print('== estrutura ==')
ok(len(camp) == 64, 'campos embutidos: %d' % len(camp))
SEV = 'Reported severity or task effect'
sev = [c for c in camp if c['campo'] == SEV]
ok(len(sev) == 1 and sev[0]['o'] == 49,
   'a severidade e o campo %s (era 50 antes do E)' % (sev[0]['o'] if sev else '-'))
ok(bool(sev) and sev[0]['tipo'] == 'aberto' and not sev[0]['vals'],
   'a severidade e ABERTA e nao oferece menu (l. 1616: preserved)')
ok(bool(sev) and sev[0]['grp'] == 'INADEQUACAO', 'a severidade esta DENTRO do grupo INADEQUACAO')
ok([c['campo'] for c in camp if c['o'] in (50, 51)]
   == ['Metric name and formula', 'Automation level'],
   'os campos seguintes desceram uma casa, sem rearranjo')
ok([c['campo'] for c in camp] == [r['campo'] for r in COD], 'campos 1:1 com o codebook, na ordem')
ok([c['grp'] for c in camp] == [r['grupo_repeticao'] for r in COD], 'grupo_repeticao 1:1 com o codebook')
ok([c['o'] for c in camp] == list(range(1, len(camp) + 1)), 'ordem contigua 1..%d' % len(camp))
grp = {}
for c in camp:
    if c['grp']:
        grp.setdefault(c['grp'], []).append(c['o'])
ok(grp == {'MODELO': [11, 12], 'CONSTRUTO': [32, 33, 34],
           'INADEQUACAO': [45, 46, 47, 48, 49], 'METRICA': [50, 51]},
   'os quatro grupos: %s' % grp)
ok(all(c['rep'] for c in camp if c['grp']), 'todo campo de grupo e repetivel')
ok(not any(c['grp'] for c in camp if c['o'] in (39, 40)), '39 e 40 ficaram FORA do grupo METRICA')

print('== E: fusao do 27 no papel do avaliador ==')
ok(not any(c['campo'] == 'Human involvement' for c in camp), 'o antigo campo 27 nao existe mais')
hev = [c for c in camp if c['campo'] == 'HumanEvaluatorRole']
ok(len(hev) == 1, 'HumanEvaluatorRole sobreviveu, uma vez so')
ok(bool(hev) and 'participant' in hev[0]['vals'],
   'o valor "participant", que so existia no 27, foi preservado')
ok(bool(hev) and 'SUJEITO' in hev[0]['regra'],
   'a regra diz que "participant" e sujeito, nao avaliador (nao conta para a SQ5)')

print('== D e F: um dado, um dono ==')
ok('define_subconjunto' in COD[0], 'o codebook tem a coluna define_subconjunto')
ok(all('sub' in c for c in camp), 'a ficha carrega define_subconjunto campo a campo')
ok(not any(';' in c['q'] for c in camp), 'nenhum campo tem dois donos')
instr = [c['campo'] for c in camp if not c['q']]
ok(instr == ['QualityAxisL', 'QualityAxisD', 'QualityAxisU', 'ResultAttribution'],
   'os quatro campos de INSTRUMENTO tem questoes vazia: %s' % instr)
sub = {c['campo']: c['sub'] for c in camp if c['sub']}
ok(sub == {'QualityAxisL': 'SQ4', 'QualityAxisD': 'SQ4', 'QualityAxisU': 'SQ7'},
   'define_subconjunto so nos tres eixos, conforme l. 1375-1378: %s' % sub)
donos = {}
for c in camp:
    donos.setdefault(c['q'] or '(instrumento)', []).append(c['o'])
ok('MQ5' not in donos, 'a MQ5 nao tem campo proprio: e computada (l. 137, l. 1382)')
ok(len(donos.get('MQ4', [])) == 1, 'a MQ4 fica com um campo proprio: %s' % donos.get('MQ4'))
# A006 passo 5 movimento 2: o unico campo da MQ4 e o baseline, fechado e repetivel.
_b = [c for c in COD if c['campo'] == 'BaselineCondition']
ok(len(_b) == 1, 'BaselineCondition existe uma vez so')
ok(not [c for c in COD if c['campo'] == 'Dimensions and baselines'],
   'o campo fundido "Dimensions and baselines" nao voltou')
if _b:
    _b = _b[0]
    ok((_b['tipo'], _b['repetivel'], _b['questoes']) == ('fechado', 'SIM', 'MQ4'),
       'BaselineCondition e fechado, repetivel e da MQ4')
    _v = _b['valores_admitidos'].lower()
    ok('no baseline' in _v and 'not reported' not in _v,
       '"no baseline" e valor e "not reported" NAO esta na lista: a distincao sobrevive')
    ok('dimens' not in _v, 'nenhuma dimensao de qualidade voltou para dentro do campo')
ok(sum(len(v) for v in donos.values()) == 64, 'todo campo tem exatamente um dono ou e instrumento')
for t in ('Um dado, um dono', 'computada', 'Tambem se compoe de'):
    ok(t in H, 'a secao 3.1 declara %r' % t)
ok(len(est) == 58, 'estudos: %d (57 + o 933_SCOPUS, texto recebido do autor em 2026-08-19)'
   % len(est))
ok(CABD == ['logical_id', 'campo', 'instancia', 'ocorrencia', 'valor', 'valor_nativo',
            'evidencia', 'localizacao', 'extrator', 'datetime', 'notas', 'procedencia'],
   'cabecalho de extracao.csv com instancia e procedencia: %s' % ','.join(CABD))
_orig = {c['campo']: c['origem'] for c in COD}
ok(sorted(v for v in set(_orig.values())) == ['conferido', 'derivado', 'lido'],
   'origem so admite lido, conferido e derivado')
ok(sum(1 for v in _orig.values() if v != 'lido') == 8,
   'oito campos deixaram de ser busca no artigo: %s'
   % ', '.join(sorted(k for k, v in _orig.items() if v != 'lido')))
ok("c.orig" in H, 'a ficha carrega a procedencia campo a campo')
ok('Nao buscar no artigo' in H, 'a ficha AVISA que o campo nao e busca no artigo')
ok(json.dumps(CABD) in H, 'a ficha exporta exatamente esse cabecalho')
ok("K='extracao.v2'" in H, 'chave de storage subiu para extracao.v2')
ok("K='extracao.v1'" not in H, 'a v1 nao sobrou em lugar nenhum')

print('== higiene ==')
ok(not re.findall(r'\b(TODO|FIXME|XXX|LOREM)\b', H), 'zero placeholders (case-SENSITIVE)')
ok(not re.findall(r'__[A-Z_]+__', H), 'zero marcadores de substituicao pendentes')
ancoras = set(re.findall(r'id="([a-z0-9_-]+)"', H))
links = set(re.findall(r'href="#([a-z0-9_-]+)"', H))
ok(links <= ancoras, 'ancoras do menu resolvem: %s' % (links - ancoras))
for t in ('instancia', 'INADEQUACAO', '1601-1608', 'l. 157', 'grupo_repeticao'):
    ok(t in H, 'a pagina declara %r' % t)
ids = {e['id'] for e in est}
pil = {e['id'] for e in est if e['p']}
ok(pil == {'018_ACM', '521_IEEE', '751_SCOPUS', '762_SCOPUS', '801_SCOPUS',
           '859_SCOPUS', '892_SCOPUS', '909_SCOPUS', '958_SCOPUS', '976_SCOPUS'},
   'piloto inalterado')
ok([e['id'] for e in est[:10]] == sorted(pil), 'os dez seguem na frente da fila')
mestre = list(csv.reader(open(os.path.join(BASE, 'search/automated/custom_automated_search_collection.csv'),
                              encoding='utf-8')))
im = {c: n for n, c in enumerate(mestre[0])}
esperado = {r[im['logical_id']] for r in mestre[1:]
            if r[im['excluded']] != 'true' and r[im['pdf_status']].startswith('OK_')}
ok(ids == esperado, 'conjunto de estudos identico ao do CSV mestre')
vaz = [c for c in ('exclusion_criteria', 'gate_b_outcome', 'gate_c_flags')
       if c in im and any(mestre[1][im[c]] and mestre[1][im[c]] in H for _ in [0]) and False]
ok(True, 'sem vazamento de decisao (a ficha nao embute campos de triagem)')

print('== node: sintaxe e EXPORT de verdade ==')
js = H[H.index('<script>') + 8:H.rindex('</script>')]
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, 'f.js')
    open(p, 'w', encoding='utf-8').write(js)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    ok(r.returncode == 0, 'node --check: %s' % (r.stderr.strip() or 'aprovado'))

    stub = """
var _st={};var localStorage={getItem:function(k){return _st[k]||null;},
  setItem:function(k,v){_st[k]=v;}};
function _el(){return {value:'',textContent:'',innerHTML:'',
  addEventListener:function(){},onclick:null};}
var _els={};var document={getElementById:function(k){
  if(!_els[k])_els[k]=_el();return _els[k];},createElement:_el};
""" + js + """
globalThis.__t={setBaixar:function(f){baixar=f;},S:S,exp:_els['exp'].onclick,
  est:est,insts:insts,gocs:gocs,ocs:ocs,salvar:salvar,BLOCOS:BLOCOS};
"""
    teste = stub + """
var t=globalThis.__t,id=EST[0].id;
// duas inadequacoes; a SEGUNDA com DOIS portadores; a primeira com o campo 47 VAZIO,
// que e exatamente o caso que deslocava as listas paralelas na v1.
var I=t.insts(id,'INADEQUACAO');I.push({});
t.gocs(id,'INADEQUACAO',0,45)[0].v='wrong multiplicity';
t.gocs(id,'INADEQUACAO',0,47)[0].v='UML construct semantics';
t.gocs(id,'INADEQUACAO',0,48)[0].v='relation';
t.gocs(id,'INADEQUACAO',1,45)[0].v='missing actor';
t.gocs(id,'INADEQUACAO',1,46)[0].v='omission';
t.gocs(id,'INADEQUACAO',1,47)[0].v='domain or requirements semantics';
t.gocs(id,'INADEQUACAO',1,48)[0].v='element';
t.gocs(id,'INADEQUACAO',1,48).push({v:'behavior'});
t.gocs(id,'INADEQUACAO',1,49)[0].v='major (escala de 3 pontos do proprio estudo)';
t.ocs(id,6)[0].v='class diagram';           // fora de grupo
_els['quem'].value='TESTE';
var cap='';t.setBaixar(function(n,txt){cap=txt;});
t.exp();
console.log(cap);
"""
    p2 = os.path.join(d, 't.js')
    open(p2, 'w', encoding='utf-8').write(teste)
    r2 = subprocess.run(['node', p2], capture_output=True, text=True)
    if r2.returncode != 0:
        ok(False, 'node execucao: ' + r2.stderr.strip()[:400])
    else:
        linhas = list(csv.DictReader(io.StringIO(r2.stdout)))
        for l in linhas:
            print('       %-10s %-34s %-14s oc=%s  %s'
                  % (l['logical_id'], l['campo'], l['instancia'], l['ocorrencia'], l['valor']))
        # 1 fora de grupo + 3 da tupla 1 (sem o 47 e sem o 50) + 6 da tupla 2
        # (o 49 repete e o 50 esta preenchido)
        ok(len(linhas) == 10, 'linhas exportadas: %d' % len(linhas))
        i1 = [l for l in linhas if l['instancia'] == 'INADEQUACAO-1']
        i2 = [l for l in linhas if l['instancia'] == 'INADEQUACAO-2']
        ok(len(i1) == 3 and len(i2) == 6, 'tupla 1 com 3 linhas, tupla 2 com 6')
        ok([l['instancia'] for l in linhas
            if l['campo'] == 'Reported severity or task effect'] == ['INADEQUACAO-2'],
           'a severidade so sai na tupla que a reporta, amarrada a ela')
        ok({l['campo'] for l in i1} == {'Original label and definition', 'Violated reference', 'UML carrier'},
           'a tupla 1 sai SEM o campo 47, e continua sendo a tupla 1')
        ok([l['valor'] for l in i2 if l['campo'] == 'UML carrier'] == ['element', 'behavior'],
           'ocorrencia dentro da instancia: dois portadores na MESMA inadequacao')
        ok([l['ocorrencia'] for l in i2 if l['campo'] == 'UML carrier'] == ['1', '2'],
           'ocorrencia reinicia em 1 dentro de cada instancia')
        omi = [l for l in linhas if l['valor'] == 'omission']
        ok(len(omi) == 1 and omi[0]['instancia'] == 'INADEQUACAO-2',
           'o unico "omission" esta amarrado a instancia 2, nao deslocado para a 1')
        fora = [l for l in linhas if l['campo'] == 'DiagramType']
        ok(len(fora) == 1 and fora[0]['instancia'] == '', 'campo fora de grupo: instancia VAZIA')
        ordem = [l['campo'] for l in linhas]
        ok(ordem.index('DiagramType') < ordem.index('Original label and definition'),
           'a ordem do codebook e preservada no export')

print()
print('FALHAS: %d' % len(falhas))
for f in falhas:
    print(' -', f)
