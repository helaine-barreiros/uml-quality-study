import csv, os, re, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'
IDS=[l.strip() for l in open('/tmp/b1_limpos.txt') if l.strip()]

UML=r'\buml\b|class diagram|sequence diagram|use case diagram|activity diagram|state ?machine diagram|state ?chart|component diagram|deployment diagram|object diagram|plantuml'
# artefato efetivamente produzido / manipulado
SAIDA={
 'codigo-fonte':r'source code|code generation|generate[sd]? code|code snippet|program translation|implementation code',
 'comentario de codigo':r'code comment|method comment|docstring|documentation comment',
 'texto em linguagem natural':r'\breport generation|natural language (answer|response|explanation)|summar[iy]|explanation|narrative',
 'resposta a questao':r'question answering|\bvqa\b|answer(ing)? (the )?(test |exam |multiple.choice )?questions?|multiple.choice',
 'imagem':r'text-to-image|image generation|generated image',
 'modelo/artefato de arquitetura':r'architecture (view|model|description|recovery|knowledge)|architectural (view|model|decision)',
 'fluxograma':r'flowchart',
 'caso de teste':r'test case|test input|fuzzing|harness',
 'grafo/ontologia':r'knowledge graph|ontolog|graph-of-thought',
 'modelo formal':r'\balloy\b|formal (model|specification)|temporal logic|\bctl\b|\bltl\b|model check',
 'transformacao modelo-a-modelo':r'model-to-model|model transformation',
}
NOTACAO=r'\bbpmn\b|\bsysml\b|\berd?\b|entity.relationship|\bgrl\b|feature model|data flow diagram|\bdfd\b|mermaid|\bc4\b|\bifml\b|petri net|\bsbvr\b|goal model'
IA={'LLM nomeado':r'\bgpt\b|gpt-?[0-9o]|chatgpt|\bclaude\b|\bgemini\b|\bllama\b|\bqwen\b|deepseek|\bmistral\b|copilot|codex',
    'termo generico de LLM':r'large language model|\bllms?\b|foundation model|generative ai|\bgenai\b',
    'encoder pre-instrucional':r'\bbert\b|roberta|\bt5\b|codebert|transformer-based'}
NAOTXT=r'source code|codebase|from code|reverse engineer|repositor|\bgithub\b|\bimage\b|hand.?drawn|screenshot|mock.?up|\bvideo\b|\baudio\b|event log|issue log|bytecode'

MET=('METODO: leitura do titulo, do resumo e das palavras-chave deste registro no CSV da busca '
     'automatizada, aplicando screening_manual_v1.md e screening_flow_v1.puml na ordem do Portao B '
     '(B1 saida, B2 origem, B3 direcao, B4 entrada). ')

def acha(rx,blob):
    return sorted(set(m if isinstance(m,str) else m[0] for m in re.findall(rx,blob)))

def nota(r,i):
    ti,ab,kw=r[i['TI']],r[i['AB']],r[i['KW']]
    blob=(ti+' '+ab+' '+kw).lower()
    p=[MET]
    # EVIDENCIA
    e=['EVIDENCIA: varredura dos tres campos deste registro. ']
    e.append('Nenhuma ocorrencia de "UML" nem de qualquer tipo de diagrama do metamodelo UML '
             '(classes, sequencia, caso de uso, atividade, maquina de estados, componentes, '
             'implantacao, objetos) ou de PlantUML em titulo, resumo ou palavras-chave. ')
    if kw.strip():
        e.append('As palavras-chave declaradas sao: "%s". '%kw.strip().rstrip(';').replace('\n','; ')[:300])
    else:
        e.append('O registro nao traz palavras-chave. ')
    arte=[k for k,rx in SAIDA.items() if re.search(rx,blob)]
    if arte:
        e.append('O artefato que o trabalho produz ou manipula, pelo que os autores declaram, e de '
                 'outra natureza: %s. '%', '.join(arte))
    outr=acha(NOTACAO,blob)
    if outr:
        e.append('Ha mencao a notacao de modelagem nao-UML (%s), que o E7 nomeia expressamente. '%', '.join(outr))
    ias=[k for k,rx in IA.items() if re.search(rx,blob)]
    if ias:
        e.append('Quanto a origem, o registro apresenta %s, de modo que o I2 nao e o ponto de falha. '%(' e '.join(ias)))
    if re.search(NAOTXT,blob):
        e.append('Ha tambem sinal de entrada nao textual (%s), que foi o gatilho da proposta '
                 'automatica de E9. '%', '.join(acha(NAOTXT,blob)[:6]))
    p.append(''.join(e))
    # DISCUSSAO
    d=['DISCUSSAO: o fluxograma manda comecar pela saida, e e ai que este registro para. ']
    d.append('O script de apoio havia proposto E9 no B4, por detectar sinal de entrada nao textual. '
             'Rejeitei essa proposta por erro de ordem: o script testou a entrada sem antes confirmar '
             'a saida, e o B4 so e alcancado por registros que tenham passado o B1. ')
    if outr:
        d.append('Aplica-se o segundo caso do B1, saida explicitamente em OUTRA notacao sem componente '
                 'UML separavel. ')
    else:
        d.append('Aplica-se a clausula geral do B1, a saida nao e UML. Nao e o terceiro caso ("resumo '
                 'nao deixa claro", que mandaria reter com INCERTO_SAIDA), porque o resumo e claro '
                 'sobre o que o trabalho produz: apenas nao produz UML. ')
    d.append('A definicao operacional de "UML diagram" do protocolo admite excecao quando o componente '
             'UML e separavel do artefato relatado; nao havendo uma unica ocorrencia de UML nos tres '
             'campos, nao ha componente algum a destacar. ')
    d.append('Pela regra de ouro 5, esta e uma falha de SAIDA (I5/E7) e nao deve ser rotulada como E6, '
             'reservado a origem do conteudo, nem como E9, reservado a entrada. Pela regra de ouro 3, '
             'o criterio primario e o primeiro portao que explica claramente o caso, e esse e o B1; '
             'os subportoes seguintes nao chegam a ser avaliados. ')
    p.append(''.join(d))
    # DECISAO
    p.append('DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Nenhuma flag de Portao C se '
             'aplica, porque o registro nao alcanca o Portao C. ')
    p.append('CONTEXTO: decidido na varredura sistematica do B1 sobre os 647 registros ainda nao '
             'triados no Portao B. A particao foi feita por varredura lexical dos tres campos em busca '
             'de "UML", "Unified Modeling Language", dos doze tipos de diagrama do metamodelo, de '
             'PlantUML e de XMI. Este registro caiu no subconjunto sem nenhuma dessas ocorrencias E sem '
             'termo de modelagem que pudesse encobrir UML por outro nome (class model, conceptual ou '
             'domain model, diagrama comportamental, geracao de modelo, MDE, MBSE, metamodelo, '
             'requisitos para modelo, ou mesmo "diagram" generico) — os 64 registros que traziam algum '
             'desses termos foram separados para leitura individual em vez de entrar neste lote. A '
             'decisao apoia-se em titulo, resumo e palavras-chave; caso o texto completo revele '
             'componente UML separavel, o registro pode ser reaberto pelo log de eventos. ')
    return ''.join(p)

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
n=0
for r in rows[1:]:
    if r[i['logical_id']] not in IDS: continue
    assert r[i['excluded']]!='true' and not r[i['gate_b_outcome']], r[i['logical_id']]
    r[i['gate_b_outcome']]='B1_E7'; r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    r[i['gate_b_notes']]=nota(r,i)
    r[i['excluded']]='true'; r[i['exclusion_criteria']]='E7'
    n+=1
with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

with open(LOG,'a',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerow([';'.join(IDS),AGORA,REV,'REVISAO_DECISAO','B1','E9 (proposta do script)','E7',
     'Varredura sistematica do B1 sobre os 647 registros que restavam sem triagem no Portao B. A '
     'particao lexical dos tres campos separou 245 registros com mencao a UML, 18 sem resumo e 384 sem '
     'nenhuma mencao. Destes 384, 64 traziam termo de modelagem capaz de encobrir UML por outro nome '
     '(class model, conceptual ou domain model, diagrama comportamental, geracao de modelo, MDE, MBSE, '
     'metamodelo, requisitos para modelo, ou "diagram" generico) e foram retirados do lote para leitura '
     'individual, em respeito a regra de ouro 1. Os 320 restantes formam este lote: nenhuma ocorrencia '
     'de UML, de tipo de diagrama do metamodelo, de PlantUML ou de XMI, e nenhum termo de modelagem '
     'ambiguo. Sem componente UML separavel, o B1 decide pela clausula geral e os subportoes seguintes '
     'nao sao alcancados. Amostra de conferencia confirmou o perfil do lote: codificacao de sintomas '
     'medicos, grafos de conhecimento, educacao em computacao, classificacao de texto, aconselhamento '
     'psicologico — o ruido lexical esperado por desenho da string ampla, documentado na secao 7 do '
     'manual. Todos os 320 possuem resumo, portanto nenhuma exclusao se apoia em dado ausente.',
     'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('alterados:',n,' linhas=%d cols=%d'%(len(rows),len(rows[0])))
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('VALIDOS=%d EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_b:',dict(sorted(Counter(r[i['gate_b_outcome']] or '(nao triado)' for r in rows[1:]).items())))
print('criterio:',dict(sorted(Counter(r[i['exclusion_criteria']] for r in rows[1:] if r[i['excluded']]=='true').items())))
mau=0
for r in rows[1:]:
    a,b,ex,cr=r[i['gate_a_outcome']],r[i['gate_b_outcome']],r[i['excluded']],r[i['exclusion_criteria']]
    parou=(a!='PASSOU') or (b not in ('','PASSOU'))
    cod=(a.split('_')[-1] if a!='PASSOU' else (b.split('_')[-1] if b not in ('','PASSOU') else ''))
    if parou!=(ex=='true') or cod!=cr: mau+=1
print('divergencias:',mau)
t=[len(r[i['gate_b_notes']]) for r in rows[1:] if r[i['logical_id']] in IDS]
print('notas: n=%d min=%d max=%d'%(len(t),min(t),max(t)))
