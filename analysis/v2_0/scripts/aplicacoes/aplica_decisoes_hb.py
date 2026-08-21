import csv, os, datetime
BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

REGRA_OCL=('REVISAO DE DECISAO em %s. REGRA FIXADA PELA PESQUISADORA: OCL sozinho nao satisfaz I5. '
 'OCL e linguagem formal de restricoes associada a modelos UML, mas nao e, por si so, conteudo de diagrama '
 'UML. Operacionalizacao: (a) OCL acompanhada de diagrama UML separavel PODE satisfazer I5; (b) OCL sozinha, '
 'sem diagrama UML gerado, NAO satisfaz I5; (c) OCL usada apenas como validacao ou verificacao de restricoes '
 'NAO satisfaz I5 sozinha. Consequencia: estudo que gera diagrama de classes mais invariantes OCL entra; '
 'estudo que gera apenas restricoes OCL a partir de requisitos sai por E7, porque o produto principal nao e '
 'conteudo de diagrama UML separavel. ')%AGORA

REGRA_UC=('REGRA FIXADA PELA PESQUISADORA em %s: descricao textual de caso de uso conta como ENTRADA textual '
 'e satisfaz I4 quando funciona como fonte substantiva para gerar a UML. Contam como especificacao textual: '
 'use case narrative, textual use case description, fluxo principal e fluxos alternativos, descricao de '
 'interacao ator-sistema e descricao de cenario. Ressalva: "use case" no sentido generico de caso de '
 'aplicacao nao e requisito nem diagrama de casos de uso. ')%AGORA

# ---------- 1. Agrupamento OCL ----------
OCL={
'518_IEEE':('B1_E7',
 'Aplicacao ao caso: o produto do trabalho sao restricoes OCL geradas a partir de especificacoes em '
 'linguagem natural sinteticas, com dataset de metamodelos e OCL sintaticamente validada, ajuste fino do '
 'Llama 3 8B e abordagem com recuperacao. Nenhum diagrama UML e gerado nem avaliado; a acuracia sintatica e '
 'a similaridade semantica medidas incidem sobre a OCL. Cai na hipotese (b) da regra. Portao: os metamodelos '
 'coletados nao sao declarados como modelos UML, e sim como metamodelos de engenharia de sistemas baseada em '
 'modelos, de modo que nao ha UML identificavel na entrada e o desfecho e B1_E7 e nao B3_E7. '
 'As flags do Portao C foram removidas porque o registro deixa de alcancar o Portao C; o INCERTO_SAIDA que '
 'as motivava era exatamente esta questao, agora respondida.'),
'758_SCOPUS':('B3_E7',
 'Aplicacao ao caso: o Codex gera restricoes OCL a partir de especificacoes em linguagem natural, com prompts '
 'enriquecidos pela informacao de 15 modelos UML preexistentes coletados de recursos educacionais. A avaliacao '
 '(validade sintatica, acuracia de execucao e similaridade de cosseno com OCL escrita por humanos) incide '
 'integralmente sobre a OCL. Nenhum diagrama UML e gerado. Cai na hipotese (b) da regra. Portao: como os '
 'modelos UML estao na ENTRADA, alimentando o prompt, o desfecho correto e B3_E7 e nao B1_E7, preservando a '
 'distincao entre "nunca houve UML" e "havia UML, mas na entrada". '
 'As flags do Portao C foram removidas porque o registro deixa de alcancar o Portao C.'),
'872_SCOPUS':('B3_E7',
 'Aplicacao ao caso: o PathOCL e tecnica de aumento de prompt baseada em caminhos para geracao de OCL com '
 'GPT-4, que seleciona um subconjunto de classes UML relevantes a especificacao em ingles para caber no '
 'limite de tokens. O produto sao restricoes OCL validas e corretas; o modelo de classes UML e insumo dado e '
 'e justamente o objeto do fatiamento. Cai na hipotese (b) da regra. Portao: UML na entrada, logo B3_E7. '
 'As flags do Portao C foram removidas porque o registro deixa de alcancar o Portao C.'),
'914_SCOPUS':('B1_E7',
 'Aplicacao ao caso: gera OCL a partir de linguagem natural para garantia de qualidade centrada em processo, '
 'e declara explicitamente "Unlike prior work focused on UML models, this work applies OCL to software '
 'process QA". Nao ha modelo UML nem na entrada nem na saida, e a medida reportada e a executabilidade das '
 'restricoes. Cai simultaneamente nas hipoteses (b) e (c) da regra. Portao: nunca houve UML, logo B1_E7. '
 'Este era o caso extremo do agrupamento, retido antes apenas pela regra de ouro 1 enquanto a questao '
 'estava aberta. As flags do Portao C foram removidas porque o registro deixa de alcancar o Portao C.'),
}

rows=list(csv.reader(open(CSV,encoding='utf-8')))
i={c:n for n,c in enumerate(rows[0])}
alt=[]
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid in OCL:
        assert r[i['gate_b_outcome']]=='PASSOU', (lid, r[i['gate_b_outcome']])
        out,txt=OCL[lid]
        r[i['gate_b_outcome']]=out
        r[i['gate_b_datetime']]=AGORA
        r[i['gate_b_notes']]=r[i['gate_b_notes']]+' || '+REGRA_OCL+txt
        for c in ('gate_c_flags','gate_c_reviewer','gate_c_datetime','gate_c_notes'): r[i[c]]=''
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E7'
        alt.append(lid)

    # ---------- 2. 879: E1 no Portao A ----------
    if lid=='879_SCOPUS':
        assert r[i['gate_a_outcome']]=='PASSOU', r[i['gate_a_outcome']]
        r[i['gate_a_outcome']]='A2_E1'; r[i['gate_a_reviewer']]=REV; r[i['gate_a_datetime']]=AGORA
        r[i['gate_a_notes']]=(r[i['gate_a_notes']]+' || REVISAO DE DECISAO em '+AGORA+'. Na triagem do Portao B '
         'levantei que este registro se autodeclara "Expert Voice", formato de coluna de opiniao convidada do '
         'periodico Software and Systems Modeling, e submeti a questao a pesquisadora em evento '
         'QUESTAO_PROTOCOLO em vez de reverter por conta propria uma decisao ja registrada no Portao A. '
         'DECISAO DA PESQUISADORA: "Expert Voice" da SoSyM tende a ser E1. Aplicado A2_E1: o item nao e '
         'relato cientifico completo, conforme a definicao de E1 na linha 1239 do protocolo v1.7, que abrange '
         'editorial, prefacio, keynote e conteudo analogo. Como o registro para no Portao A, o desfecho do '
         'Portao B e as flags do Portao C sao apagados; a analise anterior permanece integralmente no log de '
         'decisoes e no historico de backups.')
        r[i['gate_b_outcome']]=''; r[i['gate_b_reviewer']]=''; r[i['gate_b_datetime']]=''; r[i['gate_b_notes']]=''
        for c in ('gate_c_flags','gate_c_reviewer','gate_c_datetime','gate_c_notes'): r[i[c]]=''
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E1'
        alt.append(lid)

    # ---------- 3. 884/770: nao sao duplicados ----------
    if lid in ('884_SCOPUS','770_SCOPUS'):
        r[i['gate_b_notes']]=(r[i['gate_b_notes']]+' || CORRECAO em '+AGORA+'. Na triagem eu havia levantado '
         'suspeita de publicacao redundante entre 884_SCOPUS e 770_SCOPUS, por compartilharem autores, caso '
         'UVF, restricoes OCL e FIPA, frameworks JADE e PADE e conclusao sobre complexidade ciclomatica, e '
         'submeti a questao a pesquisadora. DECISAO DA PESQUISADORA: os estudos NAO sao duplicados. Nenhum '
         'valor e atribuido a duplicate_group nem a duplicate_role, e os dois registros permanecem '
         'independentes, cada um com seu proprio desfecho B3_E7. A suspeita fica registrada apenas como '
         'historico do raciocinio, sem efeito sobre a contagem PRISMA.')
        alt.append(lid)

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)
assert len(alt)==7, alt

with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow(['518_IEEE;758_SCOPUS;872_SCOPUS;914_SCOPUS',AGORA,REV,'INTERPRETACAO_PROTOCOLO','B','','',
      REGRA_OCL+'Aplicacao ao corpus: verificados todos os 149 registros retidos quanto a mencao de OCL em '
      'titulo, resumo ou palavras-chave. Cinco registros mencionam OCL. Quatro caem na hipotese (b) ou (c) e '
      'sao excluidos por E7: 518_IEEE e 914_SCOPUS em B1 (nao ha UML em nenhuma ponta) e 758_SCOPUS e '
      '872_SCOPUS em B3 (ha modelo UML na entrada, alimentando o prompt, mas o produto e OCL). O quinto, '
      '903_SCOPUS, PERMANECE RETIDO: ali a OCL e usada apenas para analise de seguranca em tempo de projeto, '
      'hipotese (c), mas ha diagrama de atividade UML gerado como componente separavel, hipotese (a). '
      'Encerra-se a primeira das questoes de protocolo pendentes.',
      'decisao da pesquisadora; protocol/screening_manual_v1.md'])
    w.writerow(['837_SCOPUS;871_SCOPUS;923_SCOPUS;975_SCOPUS',AGORA,REV,'INTERPRETACAO_PROTOCOLO','B','','',
      REGRA_UC+'Aplicacao ao corpus: a regra resolve o lado da ENTRADA e confirma que nenhum dos quatro '
      'registros do agrupamento sai por E9 em B4, pois todos partem de especificacao de requisitos ou de '
      'descricao textual de caso de uso, que a pesquisadora admite como fonte textual substantiva. '
      'PERMANECE ABERTO o lado da SAIDA, que e o que motivou a flag INCERTO_SAIDA nos quatro: nos quatro '
      'casos o produto do LLM e a descricao textual de caso de uso, nao um diagrama de casos de uso. '
      'Questao submetida a pesquisadora, sem alteracao de desfecho por ora, pela regra de ouro 1.',
      'decisao da pesquisadora; protocol/screening_manual_v1.md'])
    w.writerow(['879_SCOPUS',AGORA,REV,'REVISAO_DECISAO','A','','',
      'Decisao da pesquisadora sobre a questao levantada na triagem do Portao B: "Expert Voice" da SoSyM '
      'tende a ser E1. O registro passa de PASSOU para A2_E1 no Portao A, com excluded=true e '
      'exclusion_criteria=E1. Desfecho do Portao B (PASSOU) e flags do Portao C '
      '(EVIDENCIA=A_VERIFICAR;CANDIDATO_E10) sao apagados por o registro parar antes. A analise original '
      'permanece no evento de triagem deste registro e nos backups datados.',
      'decisao da pesquisadora; protocol/appendix_two_layer_mapping_protocol_v1_7.tex l.1239'])
    w.writerow(['770_SCOPUS;884_SCOPUS',AGORA,REV,'REVISAO_DECISAO','B','','',
      'Decisao da pesquisadora: os estudos NAO sao duplicados. A suspeita de publicacao redundante levantada '
      'na triagem fica sem efeito; duplicate_group e duplicate_role permanecem vazios e os dois registros '
      'seguem independentes, ambos excluidos por B3_E7. Registrada correcao nas notas dos dois registros. '
      'Observacao: esta decisao NAO alcanca a familia sob suspeita de fatiamento entre os RETIDOS (818, 848, '
      '868, 869, 877, 945, 963), que continua em aberto para a fase de texto completo.',
      'decisao da pesquisadora'])
    w.writerow(['974_SCOPUS',AGORA,REV,'REVISAO_DECISAO','B','','',
      'Decisao de fronteira submetida a pesquisadora e CONFIRMADA por ela: 974_SCOPUS permanece excluido em '
      'B1_E7. O artefato declarado e metamodelo Ecore e a PlantUML entra apenas como visualizacao do passo '
      'intermediario para retorno de especialistas humanos, nao como produto. Sem alteracao no CSV.',
      'decisao da pesquisadora'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('alterados:',len(alt),sorted(alt))
print('VALIDOS=%d EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_a  :',dict(sorted(Counter(r[i['gate_a_outcome']] for r in rows[1:]).items())))
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
print('gate_c preenchido em excluido:',sum(1 for r in rows[1:] if r[i['excluded']]=='true' and r[i['gate_c_flags']]))
