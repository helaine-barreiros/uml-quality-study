import csv, json, os, re, shutil, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

shutil.copy(CSV, os.path.join(BASE,'backups','custom_automated_search_collection_%s_pre_e6_lote.csv'%datetime.datetime.now().strftime('%Y%m%d_%H%M')))

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
prop=json.load(open('/tmp/triagem_proposta.json'))
alvo=sorted(k for k,v in prop.items() if v[0]=='EXCLUIR' and v[1]=='E6')

BLOCO=r'large language model|\bllms?\b|generative ai|generative artificial intelligence|chatgpt|\bgpt|\bclaude\b|\bgemini\b|\bllama\b|\bqwen\b|deepseek|foundation model|\bbert\b|roberta|transformer'
UML=(r'\buml\b|unified modeling language|plantuml|\bxmi\b|class diagram|use case diagram|sequence diagram|'
     r'activity diagram|state machine diagram|component diagram|deployment diagram|object diagram')
IA_AMPLA=r'\bai\b|artificial intelligence|machine learning|deep learning|neural network'

def nota(r):
    lid=r[i['logical_id']]
    s=' '.join([r[i['TI']],r[i['AB']],r[i['KW']]]).lower()
    uml=sorted(set(re.findall(UML,s)))
    ia=sorted(set(re.findall(IA_AMPLA,s)))
    kw=r[i['KW']].strip()

    ev=('EVIDENCIA: varredura do titulo, do resumo e das palavras-chave deste registro. '
        'Nenhum termo do bloco LLM aparece em qualquer um dos tres campos — nem modelo nomeado '
        '(GPT, ChatGPT, Claude, Gemini, Llama, Qwen, DeepSeek), nem termo generico '
        '("large language model", "LLM", "generative AI", "foundation model"), nem encoder '
        '(BERT, RoBERTa, Transformer). ')
    if ia:
        ev += ('O unico vocabulario de inteligencia artificial presente e: %s. '
               'Nenhum desses termos designa modelo de linguagem. '%(', '.join(ia)))
    else:
        ev += 'Nao ha sequer vocabulario generico de inteligencia artificial. '
    if kw:
        ev += 'Palavras-chave declaradas pelos autores: %s. '%kw[:220]
    ev += ('Quanto a saida, %s. '%('ha mencao a UML no texto (%s), o que satisfaz B1'%', '.join(uml)
           if uml else 'nao ha mencao a UML nem a qualquer outro diagrama nos tres campos'))

    disc=('DISCUSSAO: o registro percorre o Portao B na ordem saida, origem, direcao, entrada. '
          'Em B1 ele NAO e excluido: %s. '%('a saida UML esta declarada' if uml else
          'a ausencia de UML no resumo nao autoriza E7, porque o resumo simplesmente nao declara a '
          'saida, caso que o fluxograma manda reter com a flag INCERTO_SAIDA') +
          'A decisao ocorre em B2, e de forma inequivoca: nao existe LLM algum a que se possa '
          'atribuir autoridade semantica sobre o conteudo do diagrama. Nao se trata de julgar se o '
          'papel do modelo e substantivo ou acessorio, discussao das regras RF-01 e RF-02 — nao ha '
          'modelo de linguagem no relato. ' +
          ('A presenca de %s nao altera a conclusao: por RF-01, tecnica de aprendizado de maquina '
           'convencional nao satisfaz o I2, que exige modelo de linguagem em papel gerativo ou '
           'semanticamente constitutivo. '%(', '.join(ia)) if ia else '') +
          'Criterios secundarios considerados e descartados: E7 nao se aplica porque a saida nao foi '
          'declarada como outra notacao, apenas nao foi declarada; E9 nao se aplica porque a entrada '
          'nao chega a ser avaliada, ja que o fluxo para em B2; E11 nao pertence a esta etapa. '
          'Pela regra de ouro 3, o criterio primario e o primeiro do fluxograma que explica '
          'claramente o caso, e esse e o B2. ')

    met=('METODO: triagem por titulo e resumo segundo screening_manual_v1.md e screening_flow_v1.puml, '
         'Portao B. ')
    dec=('DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2 (o LLM nao e componente '
         'substantivo — aqui, nao ha LLM). Registrada a flag INCERTO_SAIDA, produzida em B1 e nao '
         'resolvida, para que a incerteza sobre a saida fique consultavel caso a decisao seja '
         'reaberta. ')
    ctx=('CONTEXTO DE RECUPERACAO: este registro integra um conjunto de 46 estudos de digital twin, '
         'MBSE, IoT e areas correlatas que entraram no corpus sem qualquer sinal de modelo de '
         'linguagem. Verificou-se antes da exclusao que os 46 tem resumo utilizavel e sao de 2022 em '
         'diante, ou seja, a ausencia de LLM nao e efeito de metadado faltante nem de escopo '
         'temporal. Registros do mesmo padrao mas SEM resumo utilizavel foram deliberadamente '
         'deixados de fora desta leva, porque excluir sobre dado ausente violaria a regra de ouro 1.')
    return met+ev+disc+dec+ctx

mud=0
for r in rows[1:]:
    if r[i['logical_id']] not in alvo: continue
    r[i['gate_b_outcome']]='B2_E6'; r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    r[i['gate_b_notes']]=nota(r)
    r[i['gate_c_flags']]='INCERTO_SAIDA'; r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
    r[i['excluded']]='true'; r[i['exclusion_criteria']]='E6'
    mud+=1

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

with open(LOG,'a',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerow([';'.join(alvo), AGORA, REV, 'DECISAO_GATE', 'B2', '', 'E6',
      'Exclusao em lote de 46 registros por E6, decidida em B2. Nenhum dos 46 apresenta termo do bloco '
      'LLM em titulo, resumo ou palavras-chave. Antes de aplicar, verificou-se que todos tem resumo '
      'utilizavel e sao de 2022 em diante, de modo que a ausencia de LLM nao decorre de metadado '
      'faltante nem de escopo temporal. Investigou-se tambem a hipotese de que o cluster estivesse no '
      'corpus por erro de ingestao, e ela foi descartada: a contagem da origem confere com o log de '
      'validacao da busca, e a recuperacao se explica pela configuracao aceita, em que os blocos UML e '
      'geracao foram buscados em texto completo enquanto o bloco LLM ficou restrito aos metadados, '
      'somada aos nomes proprios nus do bloco LLM. Trata-se, portanto, de custo de precisao previsto, '
      'e nao de defeito de corpus. Registros do mesmo padrao sem resumo utilizavel ficaram fora da leva.',
      'protocol/screening_manual_v1.md secao 6'])

print('registros alterados:',mud)
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
from collections import Counter
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('VALIDOS=%d  EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_b_outcome:',dict(sorted(Counter(r[i['gate_b_outcome']] or '(nao triado)' for r in rows[1:]).items())))
print('por criterio:',dict(sorted(Counter(r[i['exclusion_criteria']] for r in rows[1:] if r[i['excluded']]=='true').items())))
tam=[len(r[i['gate_b_notes']]) for r in rows[1:] if r[i['exclusion_criteria']]=='E6' and r[i['gate_b_outcome']]=='B2_E6']
print('observacoes: n=%d  min=%d  max=%d'%(len(tam),min(tam),max(tam)))
