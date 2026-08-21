import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: tentativa de triagem no Portao B a partir de titulo e palavras-chave apenas. Este '
     'registro NAO possui resumo no CSV: a exportacao da ACM veio sem o campo e a recuperacao por '
     'OpenAlex, que restituiu 404 dos 454 resumos ACM, nao o alcancou. ')
REGRA=('DISCUSSAO: sem resumo, os quatro subportoes do Portao B ficam indecidiveis. O B1 exige '
       'identificar o artefato de saida, o B2 a autoridade semantica, o B3 a direcao do fluxo e o B4 a '
       'entrada — nenhum deles se resolve por titulo e palavras-chave sem atribuir ao trabalho '
       'afirmacoes que ele nao fez. A regra de ouro 1 do manual e explicita: a incerteza retem, custa '
       'uma leitura, e a alternativa custa um estudo perdido. Excluir aqui seria pior: seria excluir '
       'por AUSENCIA DE DADO, e nao por evidencia contraria, o que confundiria a contagem PRISMA. ')
DEC=('DECISAO DA PESQUISADORA: RETIDO para o texto completo, por indecidibilidade e nao por '
     'verificacao. O desfecho PASSOU registra apenas que o registro nao foi excluido no Portao B; a '
     'flag SEM_RESUMO qualifica esse desfecho e impede que ele seja lido como triagem cumprida. Pelo '
     'protocolo (l. 1296), todo registro marcado como incerto entra obrigatoriamente na amostra do '
     'segundo revisor. ')

# sinal do titulo -> pauta de leitura individualizada
S={
'075_ACM':('agente de ensino de design thinking baseado em LLM, com "reasoning enhancement" nas '
  'palavras-chave','O titulo situa o trabalho em educacao e agentes de ensino, sem qualquer indicio de '
  'artefato de modelagem. Pergunta para o texto completo: ha producao de algum diagrama UML, ou o '
  '"design" do titulo e design thinking no sentido de metodologia de ideacao? A segunda hipotese e a '
  'mais provavel e levaria a E7 no B1.'),
'089_ACM':('estudo com usuarios sobre IA generativa em projetos de desenvolvimento de software de '
  'estudantes','As palavras-chave — engenharia de software educacional, tutoria por IA, experimento — '
  'apontam para estudo de experiencia e autoeficacia, nao para geracao de modelos. Pergunta: algum '
  'artefato UML e produzido e avaliado, ou o estudo mede percepcao dos estudantes?'),
'099_ACM':('cfgLLM, arcabouco agentico de fusao multi-LLM para assistencia automatizada a requisitos '
  'de software','Este e candidato real. Requisitos de software sao entrada textual legitima pelo I4 e o '
  'arcabouco e multi-LLM. Pergunta decisiva: a assistencia produz modelos UML ou apenas texto de '
  'requisitos, casos de teste e artefatos textuais? As palavras-chave citam Software Testing, o que '
  'sugere a segunda hipotese e levaria a E7 no B1.'),
'100_ACM':('LLMs e exercicios introdutorios de laboratorio, tratando suscetibilidade e resistencia',
  'O titulo situa o trabalho em avaliacao de exercicios de programacao introdutoria. Pergunta: algum '
  'exercicio envolve diagrama UML cuja qualidade seja medida?'),
'108_ACM':('avaliacao do impacto de LLMs em curriculos de ciencia da computacao','Estudo curricular. '
  'Pergunta: ha componente de modelagem UML tratado separadamente, ou o impacto e discutido no '
  'agregado do curriculo?'),
'113_ACM':('avaliacao de LLMs de proposito geral para geracao de design a partir de representacoes de '
  'prompt ontologicas, com "design patterns" e "object-oriented programming" nas palavras-chave',
  'Este e o candidato mais forte dos 18. Ha avaliacao declarada, LLMs de proposito geral e geracao de '
  'design orientado a objetos. Duas perguntas: (1) o artefato de design gerado e UML, e de que tipo? '
  '(2) a "representacao de prompt ontologica" e especificacao textual em linguagem natural, o que '
  'mantem o registro no escopo, ou e uma ontologia formal, entrada nao textual que pela delimitacao '
  'fixada em 2026-08-16 levaria a E9 no B4?'),
'170_ACM':('paradigma de orquestracao de software para desenvolvimento e avaliacao de seguranca usando '
  'ChatGPT','Ha LLM nomeado no titulo. Pergunta: a orquestracao produz modelos UML ou codigo e '
  'artefatos de seguranca? O par "desenvolvimento e avaliacao de seguranca" sugere a segunda hipotese.'),
'307_ACM':('construcao de modelos modulares hierarquicos em representacoes alternativas e '
  'intercambiaveis','Ha modelagem no titulo, mas nenhuma notacao e nomeada e nao ha indicio de LLM. '
  'Duas perguntas: a notacao e UML ou formalismo de simulacao como DEVS, e ha algum modelo de '
  'linguagem envolvido? Se nao houver LLM, o desfecho e E6 no B2.'),
'324_ACM':('uso de modelos pre-treinados de larga escala baseados em GPT junto a simulacao','Ha LLM '
  'nomeado. Pergunta: o dominio e simulacao, e o artefato produzido e modelo de simulacao ou UML? A '
  'primeira hipotese levaria a E7 no B1.'),
'380_ACM':('modelos de gemeo digital para sistemas de servico orientados a recurso, com REST, DevOps e '
  'middleware nas palavras-chave','Perfil tipico da armadilha lexical "twin" documentada na secao 7 do '
  'manual. Nao ha indicio de LLM nem de UML. Desfecho provavel: E6 no B2, por ausencia de modelo de '
  'linguagem. Pergunta: ha algum LLM no trabalho?'),
'383_ACM':('caracteristicas, modelos e servicos de gemeos digitais','Mesmo perfil. Parece capitulo '
  'panoramico ou tutorial, o que suscita tambem o E2 no Portao A, ja ultrapassado. Perguntas: e relato '
  'primario, ha LLM, ha UML?'),
'386_ACM':('padronizacao da integracao de gemeos digitais em sistemas de manufatura','Mesmo perfil, '
  'dominio de manufatura. Perguntas: ha LLM, ha UML?'),
'390_ACM':('uma introducao a gemeos digitais','O titulo anuncia texto introdutorio, o que suscita E2 '
  'como estudo nao primario alem da ausencia provavel de LLM e UML. Perguntas: e relato primario, ha '
  'LLM, ha UML?'),
'397_ACM':('analise do impacto de veiculos eletricos em sistemas locais de energia por gemeos digitais',
  'Dominio de energia, sem indicio de engenharia de software dirigida a modelos. Desfecho provavel: E6 '
  'no B2 ou E7 no B1. Pergunta: ha LLM e ha UML?'),
'399_ACM':('metodologia de teste para modelos DEVS no Cadmium','DEVS e formalismo de simulacao de '
  'eventos discretos, nao UML, e o Cadmium e sua ferramenta. Desfecho provavel: E7 no B1. Pergunta: ha '
  'componente UML separavel e ha LLM?'),
'422_ACM':('modelo de maturidade para gemeos digitais em saude','"Modelo de maturidade" e instrumento '
  'de avaliacao organizacional, nao artefato de modelagem de software. Desfecho provavel: E7 no B1. '
  'Pergunta: ha UML e ha LLM?'),
'427_ACM':('modelagem de controle operacional em sistemas logisticos de eventos discretos e seus gemeos '
  'digitais','Mesmo dominio de simulacao de eventos discretos do 399. Perguntas: a notacao e UML e ha '
  'LLM?'),
'439_ACM':('interoperabilidade semantica de asset administration shells por abordagem baseada em '
  'ontologia, com "model-driven engineering" e "industry 4.0" nas palavras-chave','Ha engenharia '
  'dirigida a modelos declarada, o que exige cautela. Perguntas: a notacao e UML ou ontologia OWL, e ha '
  'algum LLM? Sem LLM, o desfecho e E6 no B2.'),
}

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
n=0
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid not in S: continue
    assert r[i['excluded']]!='true' and not r[i['gate_b_outcome']] and not r[i['AB']].strip(), lid
    sinal,pauta=S[lid]
    kw=r[i['KW']].strip()
    ev=('EVIDENCIA: o unico material disponivel e o titulo, que anuncia %s'%sinal+
        (', e as palavras-chave "%s". '%kw.rstrip(';') if kw else ', sem palavras-chave declaradas. '))
    r[i['gate_b_outcome']]='PASSOU'; r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    r[i['gate_b_notes']]=MET+ev+REGRA+DEC+'PAUTA DE LEITURA: '+pauta+' '
    r[i['gate_c_flags']]='SEM_RESUMO;EVIDENCIA=A_VERIFICAR'
    r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
    r[i['gate_c_notes']]=('Portao C nao avaliado por ausencia de resumo. A flag EVIDENCIA=A_VERIFICAR '
        'e consequencia da falta de dado, nao constatacao de ausencia de vocabulario de qualidade; '
        'pela regra de ouro 2, ausencia de vocabulario de qualidade nunca exclui.')
    n+=1

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

with open(LOG,'a',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerow([';'.join(sorted(S)),AGORA,REV,'DECISAO_GATE','B','','',
     'Dezoito registros ACM sem resumo RETIDOS por indecidibilidade no Portao B, com flag SEM_RESUMO. '
     'Nenhum dos quatro subportoes se resolve por titulo e palavras-chave sem atribuir ao trabalho '
     'afirmacoes que ele nao fez; excluir seria excluir por ausencia de dado e nao por evidencia '
     'contraria, contra a regra de ouro 1. Registrada em cada um a pauta de leitura derivada do sinal '
     'do titulo. Perfil do conjunto: oito sao trabalhos de gemeo digital (380, 383, 386, 390, 397, 422, '
     '427, 439), a armadilha lexical "twin" documentada na secao 7 do manual, com desfecho provavel E6 '
     'no B2 por ausencia de LLM; cinco sao de educacao em computacao (075, 089, 100, 108, 170); dois '
     'sao de simulacao de eventos discretos com formalismo DEVS (399, 427); e dois sao candidatos reais '
     'que merecem leitura prioritaria — 113_ACM, avaliacao de LLMs de proposito geral para geracao de '
     'design a partir de prompts ontologicos, e 099_ACM, arcabouco multi-LLM para requisitos de '
     'software. A causa da ausencia e a exportacao da ACM sem campo de resumo; a recuperacao por '
     'OpenAlex restituiu 404 dos 454 resumos ACM e nao alcancou estes.',
     'protocol/screening_manual_v1.md'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('alterados:',n)
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('VALIDOS=%d EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_b:',dict(sorted(Counter(r[i['gate_b_outcome']] or '(nao triado)' for r in rows[1:]).items())))
naotriado=sum(1 for r in rows[1:] if r[i['excluded']]!='true' and not r[i['gate_b_outcome']])
print('validos ainda nao triados no B:',naotriado)
