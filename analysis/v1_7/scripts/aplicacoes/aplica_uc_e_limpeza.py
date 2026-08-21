import csv, os, datetime
BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

REGRA_UC=('REVISAO DE DECISAO em %s. REGRA FIXADA PELA PESQUISADORA, por extensao explicita da regra do OCL: '
 'a descricao TEXTUAL de caso de uso satisfaz I4 quando e ENTRADA (fonte substantiva para gerar a UML), mas '
 'NAO satisfaz I5 quando e a SAIDA, porque o produto principal nao e conteudo de diagrama UML separavel. '
 'Um estudo cujo produto declarado do LLM e a especificacao textual de caso de uso (narrativa, fluxo principal, '
 'fluxos alternativos, descricao da interacao ator-sistema) sai por E7 no Portao B1, mesmo que o texto seja '
 'rotulado pelos autores como "UML use case". A flag INCERTO_SAIDA, atribuida na triagem original pela regra de '
 'ouro 1 (a incerteza retem), fica resolvida por esta regra e e removida junto com os demais campos do Portao C, '
 'que so se aplica a registros retidos. ')%AGORA

MET=('METODO: releitura do titulo, do resumo e das palavras-chave deste registro no CSV da busca automatizada, '
     'reaplicando o Portao B na ordem B1 (saida), B2 (origem), B3 (direcao), B4 (entrada) sob a regra de saida '
     'acima. ')

UC={
 '837_SCOPUS':(
  'EVIDENCIA: o resumo declara que os casos de uso UML "specify the functional requirements of a system" e que '
  'sao eficazes "thanks to the use of natural languages"; a proposta ECHO e "a novel approach for supporting '
  'software engineers in enhancing the quality of UML use cases using LLMs", por engenharia de co-prompt e um '
  'processo iterativo e interativo com o LLM. ',
  'DISCUSSAO: o artefato sobre o qual o LLM opera e produz e o caso de uso em linguagem natural, nao o diagrama '
  'de casos de uso. O vocabulario de qualidade e explicito (inaccuracy, incompleteness, quality of UML use cases), '
  'o que na triagem original sustentou a retencao com EVIDENCIA=EXPLICITA, mas a regra de ouro 2 diz que a presenca '
  'de vocabulario de qualidade nunca inclui por si so: e preciso que o objeto medido seja conteudo UML separavel. '
  'Pela regra fixada agora, nao e. O B1 explica o caso sem resíduo, entao nao se desce a B3, onde a discussao sobre '
  'o caso de uso ja existir e ser alterado seria pertinente. ',
  'DECISAO: B1_E7. '),
 '871_SCOPUS':(
  'EVIDENCIA: o titulo e inequivoco quanto ao produto — "Automated Generation of Use Case Textual Descriptions '
  'from Requirements Specification" — e o resumo confirma: UCGen "generat[es] use case textual descriptions for '
  'requirements specifications", com tecnicas de prompting variadas e um pipeline human-in-the-loop de verificacao. ',
  'DISCUSSAO: a celula e requisitos textuais -> LLM -> descricao textual de caso de uso. A entrada satisfaz I4 (a '
  'especificacao de requisitos e fonte substantiva), e portanto o registro NAO sai por E9 no B4; mas o B1 e '
  'anterior e ja resolve, porque a saida e texto estruturado por template, nao conteudo de diagrama UML. Registro '
  'a distincao para o caso de o protocolo ser emendado: se a especificacao textual de caso de uso passar a contar '
  'como conteudo UML para I5, este registro retorna sem re-triagem, com entrada e papel do LLM ja verificados. ',
  'DECISAO: B1_E7. '),
 '923_SCOPUS':(
  'EVIDENCIA: o resumo afirma que "UML use case specifications use textual descriptions to define scenarios and '
  'behaviors that achieve user goals" e propoe "a test-driven approach to further refine UML use case '
  'specifications, leveraging large language models (LLMs) to facilitate the synchronization of natural language '
  'requirements, UML specifications, and test cases", com um formato estruturado que permite ao LLM transformar '
  'os artefatos. ',
  'DISCUSSAO: os proprios autores definem a UML use case specification como descricao textual, o que torna o caso '
  'limpido sob a nova regra: o produto do LLM e o texto refinado e os casos de teste sincronizados, nao um '
  'diagrama. Nenhum tipo de diagrama UML e nomeado no resumo. O B1 explica sem resíduo. ',
  'DECISAO: B1_E7. '),
 '975_SCOPUS':(
  'EVIDENCIA: o resumo propoe "a formal structure to guide LLMs in generating UCSs based on natural language '
  'requirements" e, separadamente, declara que "UML activity and state machine diagrams are used as specific '
  'modeling methods for such processes", os processos de negocio de alto nivel contra os quais a consistencia das '
  'UCSs e validada. ',
  'DISCUSSAO: este e o unico dos quatro em que tipos de diagrama UML sao nomeados, o que exige separar os papeis. '
  'O que o LLM gera e a UCS; os diagramas de atividade e de maquina de estados sao o referencial de comparacao, '
  'insumo do procedimento de validacao de consistencia, nao produto do modelo. Nao ha, no resumo, nenhuma '
  'declaracao de que o LLM sintetize esses diagramas, e as tres regras de consistencia descritas operam sobre '
  'objetos de negocio que conectam as UCSs aos modelos preexistentes. Logo a saida avaliada e a especificacao '
  'textual, e o B1 explica o caso sem resíduo. Anoto que, se a leitura do texto completo revelar que os diagramas '
  'de atividade e de maquina de estados tambem sao gerados pelo LLM e avaliados, o registro deve ser reaberto: e o '
  'candidato mais forte a reversao entre os quatro. ',
  'DECISAO: B1_E7. '),
}
assert len(UC)==4, len(UC)

rows=list(csv.reader(open(CSV,encoding='utf-8')))
i={c:n for n,c in enumerate(rows[0])}
GC=['gate_c_flags','gate_c_reviewer','gate_c_datetime','gate_c_notes']

# --- 1) reclassificacao dos quatro casos de uso textuais ---
n_uc=0
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid not in UC: continue
    assert r[i['gate_b_outcome']]=='PASSOU', (lid, r[i['gate_b_outcome']])
    ev,di,de=UC[lid]
    r[i['gate_b_outcome']]='B1_E7'
    r[i['gate_b_reviewer']]=REV
    r[i['gate_b_datetime']]=AGORA
    r[i['gate_b_notes']]=r[i['gate_b_notes']]+' || '+REGRA_UC+MET+ev+di+de
    for c in GC: r[i[c]]=''
    r[i['excluded']]='true'
    r[i['exclusion_criteria']]='E7'
    n_uc+=1
assert n_uc==4, n_uc

# --- 2) limpeza do residuo de gate_c em registros excluidos ---
limpos=[]
for r in rows[1:]:
    if r[i['excluded']]!='true': continue
    if not any(r[i[c]] for c in GC): continue
    limpos.append(r[i['logical_id']])
    for c in GC: r[i[c]]=''
assert len(limpos)==52, len(limpos)

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

NOTA_UC=('Aplicacao da regra de saida fixada pela pesquisadora para descricao textual de caso de uso, por extensao '
 'explicita da regra do OCL registrada no mesmo dia. A pesquisadora ja havia decidido que a descricao textual de '
 'caso de uso conta como ENTRADA e satisfaz I4 quando e fonte substantiva para gerar a UML; permanecia aberto o '
 'lado da SAIDA, motivo pelo qual estes quatro registros carregavam a flag INCERTO_SAIDA e haviam sido retidos pela '
 'regra de ouro 1. Consultada sobre a assimetria, a pesquisadora determinou que o mesmo criterio do OCL se aplica: '
 'quando o produto principal do LLM e a especificacao textual e nao conteudo de diagrama UML separavel, o registro '
 'sai por E7. Os quatro sao reclassificados de PASSOU para B1_E7 e os campos do Portao C sao esvaziados, por o '
 'Portao C so se aplicar a registros retidos. Ficam nomeados aqui para recuperacao sem re-triagem caso o I5 seja '
 'emendado: 837 (ECHO, melhoria de qualidade de casos de uso em linguagem natural), 871 (UCGen, geracao de '
 'descricoes textuais a partir de especificacao de requisitos), 923 (refinamento test-driven de especificacoes '
 'textuais), 975 (geracao de UCSs com validacao de consistencia contra diagramas de atividade e maquina de estados '
 'preexistentes). O 975 e o de reversao mais provavel, por nomear tipos de diagrama UML; a leitura do texto completo '
 'deve confirmar se esses diagramas sao apenas referencial de validacao, como o resumo indica, ou tambem produto do '
 'LLM. A decisao foi tomada com ciencia do custo: 837, 871 e 923 traziam vocabulario de qualidade explicito.')

NOTA_LIMPEZA=('Correcao de dado, sem efeito sobre nenhum desfecho de triagem. Foram encontrados 52 registros ja '
 'excluidos que ainda carregavam gate_c_flags igual a INCERTO_SAIDA, com revisor e data preenchidos e campo de '
 'notas vazio. A inspecao mostrou que essas marcas vieram de uma varredura lexical de rastreio de saida anterior a '
 'triagem do Portao B, e nao de decisoes do Portao C: 48 dos registros foram depois excluidos por E6, 3 por E8 e 1 '
 'por E7, e o bloco contiguo 378_ACM a 446_ACM evidencia a origem em varredura. Como o Portao C so se aplica a '
 'registros retidos e suas flags nunca excluem, a permanencia dessas marcas em registros excluidos nao tinha funcao '
 'e distorcia a contagem de flags do corpus retido. Os quatro campos gate_c foram esvaziados nesses 52 registros. '
 'Os desfechos dos Portoes A e B, os criterios de exclusao e as notas de decisao permanecem intactos, e o backup '
 'anterior a operacao esta em backups/. Registros afetados: ')+';'.join(limpos)+'.'

with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow(['837_SCOPUS;871_SCOPUS;923_SCOPUS;975_SCOPUS',AGORA,REV,'REVISAO_DECISAO','B','','',NOTA_UC,
                'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml; '
                'protocol/appendix_two_layer_mapping_protocol_v1_7.tex l.1245 (E7)'])
    w.writerow([';'.join(limpos),AGORA,REV,'CORRECAO','C','','',NOTA_LIMPEZA,
                'protocol/screening_manual_v1.md'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('reclassificados:',n_uc,'| gate_c limpos:',len(limpos))
print('VALIDOS=%d EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_b  :',dict(sorted(Counter(r[i['gate_b_outcome']] or '(nao triado)' for r in rows[1:]).items())))
print('criterio:',dict(sorted(Counter(r[i['exclusion_criteria']] for r in rows[1:] if r[i['excluded']]=='true').items())))
mau=0
for r in rows[1:]:
    a,b,ex,cr=r[i['gate_a_outcome']],r[i['gate_b_outcome']],r[i['excluded']],r[i['exclusion_criteria']]
    parou=(a!='PASSOU') or (b not in ('','PASSOU'))
    cod=(a.split('_')[-1] if a!='PASSOU' else (b.split('_')[-1] if b not in ('','PASSOU') else ''))
    if parou!=(ex=='true') or cod!=cr: mau+=1
print('divergencias:',mau)
print('validos nao triados no B:',sum(1 for r in rows[1:] if r[i['excluded']]!='true' and not r[i['gate_b_outcome']]))
print('gate_c preenchido em excluido:',sum(1 for r in rows[1:] if r[i['excluded']]=='true' and any(r[i[c]] for c in GC)))
fl=Counter()
for r in rows[1:]:
    if r[i['excluded']]=='true': continue
    for f in r[i['gate_c_flags']].split(';'):
        if f: fl[f]+=1
print('flags nos retidos:',dict(sorted(fl.items())))
