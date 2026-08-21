import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: leitura do titulo, do resumo e das palavras-chave deste registro no CSV da busca '
     'automatizada, aplicando screening_manual_v1.md e screening_flow_v1.puml na ordem do Portao B '
     '(saida, origem, direcao, entrada). ')

# ---------------------------------------------------------------- GRUPO A: E7 em B1
BASE_E7_DISC=(
 'DISCUSSAO: o fluxograma manda comecar pela saida. O segundo caso do B1 e "explicitamente OUTRA '
 'notacao SEM componente UML separavel", e e exatamente este. A notacao aqui nao e ambigua nem '
 'omitida: e nomeada pelos autores. Nao se aplica o terceiro caso do B1 ("resumo nao deixa claro"), '
 'que mandaria reter com INCERTO_SAIDA, porque o resumo deixa claro — so nao declara UML. A definicao '
 'operacional de "UML diagram" do protocolo admite excecao quando o componente UML e separavel; '
 'verifiquei os tres campos e nao ha nenhum elemento UML destacavel do artefato relatado. Pela regra '
 'de ouro 5, esta falha e de SAIDA (I5/E7) e nao deve ser rotulada como E6, que e reservado a origem '
 'do conteudo. Pela regra de ouro 3, o B1 e o primeiro portao que explica claramente o caso, de modo '
 'que os portoes seguintes nao chegam a ser avaliados. ')
DEC_E7=('DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Nenhuma flag de Portao C se aplica, '
        'porque o registro nao alcanca o Portao C. ')

A={
'007_ACM':('EVIDENCIA: os autores declaram que a tecnica leva LLMs (GPT-4, Llama, Cohere) a gerar '
  'automaticamente "goal models" a partir de user stories, produzindo representacao XML em '
  'Goal-oriented Requirements Language (GRL), visualizavel no jUCMNav. As palavras-chave confirmam: '
  '"goal-oriented requirement language (GRL); goal modeling; user story". Nenhum dos tres campos '
  'menciona UML ou qualquer tipo de diagrama UML. ',
  'Observe-se que o I2 esta plenamente satisfeito — ha LLM nomeado com autoridade semantica sobre o '
  'modelo — e o I4 tambem, pois a entrada e textual (user stories). O que falha e unicamente o I5. '
  'Este e o caso tipico que a regra de ouro 5 quer proteger de rotulacao errada. '),
'171_ACM':('EVIDENCIA: o resumo descreve a ferramenta GIVUP, que recebe descricao textual de processo '
  'e de propriedade funcional e transforma a primeira em BPMN e a segunda em formula de Logica '
  'Temporal Linear (LTL), verificando depois se o processo BPMN satisfaz a propriedade. As '
  'palavras-chave sao "BPMN; LLM; generation; model checking; verification". O BPMN e citado como '
  '"the standard modelling language" do dominio de processos de negocio. Nenhuma mencao a UML. ',
  'O BPMN esta nomeado no proprio texto do E7 no protocolo (l. 1245). A saida secundaria, a formula '
  'LTL, tampouco e UML. '),
'319_ACM':('EVIDENCIA: o resumo declara que os autores construiram manualmente um feature model '
  'inicial e depois usaram Large Language Models para expandi-lo e melhora-lo, por prompts '
  'estruturados sobre cinco modelos. As palavras-chave sao "feature modeling; software product '
  'lines; variability". O artefato produzido e um modelo de features do paradigma de Linha de '
  'Produto de Software. Nenhuma mencao a UML nos tres campos. ',
  'O feature model nao consta da lista literal do E7, mas cai na clausula geral "the output is not '
  'UML". Nao ha componente UML separavel: o modelo de features e integral e nao contem elemento de '
  'metamodelo UML destacavel. '),
'411_ACM':('EVIDENCIA: o resumo apresenta o TerrARA, que constroi automaticamente um Data Flow '
  'Diagram (DFD) enriquecido a partir de arquivos de configuracao Terraform, para eliciar ameacas de '
  'seguranca com o motor SPARTA. As palavras-chave abrem com "data flow diagram". O GPT-4o aparece '
  'apenas como termo de comparacao de desempenho, ao lado do StartLeft, e nao como componente da '
  'abordagem. Nenhuma mencao a UML. ',
  'Este registro falharia tambem no B4, porque a entrada e codigo de infraestrutura e nao texto '
  '(E9), e no B2, porque o LLM e so linha de base comparativa e nao componente substantivo (E6). '
  'Registram-se as tres leituras para transparencia, mas por regra de ouro 3 vale a primeira: o B1. '),
'495_IEEE':('EVIDENCIA: o titulo e o resumo declaram a geracao de modelos SysML v2 a partir de '
  'requisitos em linguagem natural com LLMs, avaliando prompting estruturado quanto a coerencia '
  'sintatica e riqueza semantica do SysML v2 gerado. As palavras-chave repetem "SysML v2". Nenhuma '
  'mencao a UML nos tres campos. ',
  'Ponto que exigiu deliberacao: o SysML consta nominalmente do E7, mas o SysML v1 e perfil de UML e '
  'reusa diagramas do metamodelo UML, o que poderia caracterizar componente separavel. Aqui, porem, '
  'trata-se especificamente do SysML v2, que rompe essa filiacao: e linguagem autonoma construida '
  'sobre o KerML, sem reuso do metamodelo UML. Nao ha, portanto, componente UML separavel a resgatar. '
  'A distincao entre v1 e v2 e substantiva e foi aplicada de forma consistente nesta leva — o '
  '018_ACM, que trata de modelos de comportamento SysML v1, foi retido por razao simetrica. '),
'509_IEEE':('EVIDENCIA: o resumo apresenta o SIG-GPT, um GPT-4 aumentado por gramatica textual e RAG '
  'para gerar Softgoal Interdependency Graphs (SIG), notacao de modelagem de requisitos '
  'nao-funcionais. As palavras-chave declaram "Softgoal Interdependency Graph (SIG); Visual Modeling '
  'Languages; Goal Modeling". As metricas reportadas (100 por cento de acuracia sintatica, 95 por '
  'cento de semantica) referem-se ao SIG. Nenhuma mencao a UML. ',
  'Como no 007_ACM, o I2 e o I4 estao satisfeitos e a evidencia de qualidade e explicita; o que '
  'falha e apenas a saida. '),
'568_IEEE':('EVIDENCIA: o titulo declara o mapeamento de especificacao em linguagem natural para um '
  'Entity Relationship Diagram pelo ChatGPT, e o resumo descreve a avaliacao dessa traducao contra '
  'abordagens de extracao de entidades e relacoes. A primeira palavra-chave e "entity relationship '
  'diagram". As aplicacoes citadas sao grafo de conhecimento, integracao de dados e projeto de '
  'esquema de banco. Nenhuma mencao a UML. ',
  'O diagrama entidade-relacionamento esta nomeado no texto do E7 (l. 1245). Nao ha diagrama de '
  'classes nem qualquer outro artefato UML separavel do ER relatado. '),
'573_IEEE':('EVIDENCIA: o resumo apresenta o processo CIAO, que recebe um repositorio GitHub e produz '
  'documentacao arquitetural de nivel de sistema com LLMs, segundo template derivado da ISO/IEC/IEEE '
  '42010, do SEI Views and Beyond e do modelo C4. A avaliacao com 22 desenvolvedores aponta '
  'limitacoes em "diagram quality" e "deployment views", sem nomear UML. As palavras-chave nao '
  'trazem UML. ',
  'O modelo C4 esta nomeado no texto do E7. A mencao a "deployment views" nao configura diagrama de '
  'implantacao UML: e visao arquitetural no sentido da 42010, e o proprio resumo a atribui ao '
  'template C4/SEI. Este registro tambem falharia no B4, por entrada ser codigo, e no B3, por o '
  'produto ser documentacao; prevalece o B1 pela regra de ouro 3. '),
'611_IEEE':('EVIDENCIA: o resumo propoe gerar automaticamente propriedades CTL a partir dos '
  'requisitos expressos em um modelo SysML, por processo baseado em IA e regras sintaticas, '
  'implementado no TTool-AI, um toolkit SysML aberto estendido com assistente baseado em LLM. As '
  'palavras-chave incluem "SysML; CTL; Formal verification; Properties generation". Nenhuma mencao a '
  'UML. ',
  'A saida do processo nao e sequer um diagrama: sao formulas de logica temporal ramificada (CTL) '
  'para verificacao de modelos. O SysML aparece como ENTRADA, nao como produto, o que reforca o E7 — '
  'nada de UML e produzido. O retrocesso das coberturas ao diagrama de requisitos SysML e '
  'apresentacao de resultado, nao geracao de conteudo de modelo. '),
}

# ---------------------------------------------------------------- GRUPO B: E6 em B2
B_DISC=(
 'DISCUSSAO: o script de apoio havia proposto E7 para este registro por detectar SysML na saida. '
 'Rejeitei essa leitura. O B1 nao decide com clareza aqui, porque o SysML v1 e perfil de UML e reusa '
 'do metamodelo UML os diagramas de atividade, sequencia, maquina de estados e caso de uso; afirmar '
 '"sem componente UML separavel" exigiria uma certeza que o resumo nao oferece. O B2, ao contrario, '
 'decide de forma inequivoca: nao ha modelo de linguagem algum no relato a que se pudesse atribuir '
 'autoridade semantica sobre o conteudo do modelo. Pela regra de ouro 3, o criterio primario e o '
 'primeiro portao que explica CLARAMENTE o caso, e esse e o B2, nao o B1. Nao se trata de discutir '
 'se o papel do LLM e substantivo ou acessorio, materia das regras RF-01 e RF-02: nao ha LLM. ')
DEC_B=('DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. Registrada a flag INCERTO_SAIDA, '
       'produzida no B1 e nao resolvida, para que a duvida sobre o estatuto UML do artefato SysML '
       'permaneca consultavel caso a decisao seja reaberta. ')

B={
'295_ACM':('EVIDENCIA: o resumo propoe um arcabouco de Model-Based Systems Engineering pela '
  'metodologia MagicGrid, empregando MagicDraw e SysML para projetar sistemas de alocacao de recursos '
  'em megaconstelacoes LEO, com matrizes de rastreabilidade ligando requisitos de usuario a '
  'arquitetura logica. As palavras-chave sao "Digital twin; LEO mega-constellations; Model-Based '
  'Systems Engineering; Resource allocation; SysML". Varredura dos tres campos: nenhum termo do bloco '
  'LLM — nem modelo nomeado, nem termo generico, nem encoder — e nenhum vocabulario de inteligencia '
  'artificial. A modelagem e integralmente humana, feita por engenheiros na ferramenta MagicDraw. '),
'351_ACM':('EVIDENCIA: o resumo apresenta o CPSAML, cujo pipeline parte de uma linguagem de '
  'modelagem especifica de dominio formulada pelo arquiteto, transforma esse modelo em SysML 2 para '
  'refinamento por engenheiros e, no ultimo passo, gera codigo para os dispositivos, um gemeo digital '
  'e a aplicacao de cockpit. As palavras-chave sao "multi-paradigm modeling; model-driven '
  'engineering; digital twin; cyber-physical systems". Varredura dos tres campos: nenhum termo do '
  'bloco LLM e nenhum vocabulario de inteligencia artificial. As transformacoes sao de engenharia '
  'dirigida por modelos, deterministicas e definidas por regras. '),
'384_ACM':('EVIDENCIA: o resumo trata de avaliacao continua e automatizada de confiabilidade em '
  'manufatura definida por software, apoiada em gemeos digitais, e aponta a transformacao '
  'Model-to-Model (M2M) como tecnologia habilitadora para gerar e sincronizar modelos hibridos de '
  'confiabilidade com os modelos de sistema disponiveis. As palavras-chave sao "model-to-model (M2M) '
  'transformation; digital twin; case study; SysML v2". Varredura dos tres campos: nenhum termo do '
  'bloco LLM e nenhum vocabulario de inteligencia artificial. A geracao automatica citada e '
  'transformacao M2M, nao geracao por modelo de linguagem. '),
'407_ACM':('EVIDENCIA: o resumo apresenta a arquitetura e a implementacao de uma camada de conversao '
  'que transforma um modelo SysML em representacao 3D, para superar a limitacao das vistas '
  'bidimensionais das ferramentas SysML comerciais. As palavras-chave sao "model validation; model '
  'execution; model conversion; Virtual Environment; SysML; Digital Twin; 3D modeling". Varredura dos '
  'tres campos: nenhum termo do bloco LLM e nenhum vocabulario de inteligencia artificial. Alem '
  'disso, o modelo SysML e ENTRADA da conversao e ja existe; nada de novo conteudo semantico e '
  'produzido. '),
}

# ---------------------------------------------------------------- GRUPO C: retidos
C={
'018_ACM':('B2_PASSOU','EVIDENCIA=EXPLICITA',
  'EVIDENCIA: o titulo declara a geracao de modelos de COMPORTAMENTO SysML por LLMs em estudo '
  'empirico. O resumo especifica tres tipos de modelo de comportamento e reporta acuracia semantica '
  'por tipo, com F1 medio de 95 por cento para ACT e queda para 50 por cento em SD — isto e, '
  'diagrama de atividade e diagrama de sequencia. Reporta ainda mais de 90 por cento de acuracia '
  'gramatical, um conjunto publicado de 107 modelos e regras de model checking para mitigar '
  'alucinacoes. As palavras-chave sao "SysML behavior models; model generation; large language '
  'models; hallucination; model checking". ',
  'DISCUSSAO: o script de apoio propos E7 por detectar SysML. Rejeitei. Os diagramas de '
  'comportamento do SysML v1 — atividade, sequencia, maquina de estados e caso de uso — sao reusados '
  'diretamente do metamodelo UML, e o resumo nomeia justamente dois deles, ACT e SD. O componente UML '
  'e, portanto, separavel no sentido exato da definicao operacional de "UML diagram" do protocolo, e '
  'o B1 resolve pelo primeiro caso, saida compativel. B2: os LLMs sao nomeados e determinam o '
  'conteudo dos modelos gerados, satisfazendo a RF-02. B3: a direcao e texto para modelo, o modelo e '
  'produto. B4: a entrada e a descricao textual de dominio dos 107 casos. Portao C: o resumo mede '
  'acuracia sintatica e semantica separadamente, classifica alucinacoes e propoe regras de '
  'verificacao, o que e vocabulario de qualidade explicito. ',
  'DECISAO DA PESQUISADORA: RETIDO para o texto completo. Percorreu os quatro subportoes do Portao B '
  'sem exclusao. Flag EVIDENCIA=EXPLICITA no Portao C. E candidato forte a inclusao: separa '
  'conformidade sintatica de correcao semantica, exatamente a distincao que a revisao investiga. '
  'Pergunta para o texto completo: os modelos ACT e SD avaliados sao tratados pelos autores como '
  'diagramas UML ou como construtos exclusivamente SysML? '),
'538_IEEE':('B2_PASSOU','INCERTO_SAIDA',
  'EVIDENCIA: o resumo relata um arcabouco leve que combina orientacao por recuperacao, refinamento '
  'de prompt e correcao iterativa para melhorar a corretude sintatica do codigo Mermaid gerado pelo '
  'Gemini. Os exemplos de diagrama citados sao escalonamento de processos e protocolos de rede. As '
  'palavras-chave sao "large language models; diagram generation; Mermaid; prompt engineering; '
  'retrieval-augmented generation". Em nenhum dos tres campos se declara o TIPO de diagrama Mermaid '
  'produzido. ',
  'DISCUSSAO: o script de apoio propos E7 por detectar Mermaid, que consta nominalmente do E7. '
  'Rejeitei, e a razao esta na propria definicao operacional de "UML diagram" do protocolo, que trata '
  'o PlantUML como elegivel "quando destinado a codificar UML". O Mermaid, como o PlantUML, e '
  'sintaxe PORTADORA e nao notacao: admite diagrama de classes, de sequencia e de estados ao lado de '
  'fluxogramas e diagramas de Gantt. Dizer que a saida e "explicitamente OUTRA notacao" seria '
  'atribuir ao resumo uma declaracao que ele nao faz. O caso e o terceiro do B1, "resumo nao deixa '
  'claro", que manda reter com INCERTO_SAIDA. Os exemplos citados nao sao UML, o que enfraquece o '
  'registro, mas exemplo ilustrativo nao e declaracao de escopo e a regra de ouro 1 manda reter na '
  'duvida. B2: o Gemini e nomeado e gera o codigo do diagrama, satisfazendo a RF-02. B3: o diagrama '
  'e produto. B4: a entrada nao e declarada. ',
  'DECISAO DA PESQUISADORA: RETIDO para o texto completo, com INCERTO_SAIDA. Pergunta que o texto '
  'completo precisa responder: entre os diagramas Mermaid avaliados ha tipos UML — classes, '
  'sequencia, estados — cuja qualidade seja mensurada separadamente? Se a resposta for negativa, o '
  'registro volta ao B1 e sai por E7 na etapa seguinte. '),
'539_IEEE':('B2_PASSOU','INCERTO_PAPEL_LLM;INCERTO_SAIDA',
  'EVIDENCIA: o titulo anuncia a aplicacao de IA generativa para facilitar a adocao de MBSE. O '
  'resumo, porem, descreve a tecnica como "ML technique based on Generative AI particularly Natural '
  'Language Processing (NLP)" e detalha a operacao como gerar entidades de modelo SysML "by training '
  'NLP model with labelled data". As palavras-chave sao "MBSE; SysML; NLP; Generative AI". Nenhum '
  'modelo de linguagem e nomeado; nao aparece "large language model", nem LLM, nem modelo proprio. '
  'Nao se declara que tipo de entidade SysML e gerada. ',
  'DISCUSSAO: o script de apoio propos E7 por detectar SysML. Rejeitei em dois niveis. No B1, vale o '
  'mesmo argumento do grupo reclassificado: o SysML v1 reusa diagramas do metamodelo UML e o resumo '
  'nao diz quais entidades gera, logo a saida nao esta claramente declarada como outra notacao — '
  'caso de INCERTO_SAIDA. No B2, ha tensao real entre os campos: o rotulo "Generative AI" sugere '
  'papel gerativo, mas a descricao operacional, treinar modelo de NLP com dados rotulados, e de '
  'classificador ou etiquetador, que pela RF-01 nao satisfaz o I2. O terceiro caso do B2 cobre '
  'exatamente esta situacao — rotulo amplo de IA sem especificacao do papel — e manda reter com '
  'INCERTO_PAPEL_LLM. Considerei excluir por E6 invocando a RF-01, e registro que houve hesitacao; '
  'pela regra de ouro 1 a hesitacao retem. ',
  'DECISAO DA PESQUISADORA: RETIDO para o texto completo, com INCERTO_PAPEL_LLM e INCERTO_SAIDA. '
  'Duas perguntas para o texto completo: (1) o modelo de NLP treinado com dados rotulados atua como '
  'classificador, caso em que a RF-01 leva a E6, ou determina o conteudo semantico das entidades '
  'geradas? (2) que entidades SysML sao produzidas, e alguma delas e diagrama reusado da UML? '
  'Registro tambem que este resumo nao apresenta vocabulario de avaliacao, medicao ou comparacao, o '
  'que o torna candidato a E11 no texto completo — decisao que, pela regra de ouro 2, nao pertence a '
  'esta etapa. '),
}

# ---------------------------------------------------------------- aplicacao
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
feito={}
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid in A:
        ev,extra=A[lid]
        r[i['gate_b_outcome']]='B1_E7'
        r[i['gate_b_notes']]=MET+ev+BASE_E7_DISC+extra+DEC_E7
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E7'
        feito[lid]='E7'
    elif lid in B:
        r[i['gate_b_outcome']]='B2_E6'
        r[i['gate_b_notes']]=MET+B[lid]+B_DISC+DEC_B
        r[i['gate_c_flags']]='INCERTO_SAIDA'
        r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E6'
        feito[lid]='E6'
    elif lid in C:
        _,flags,ev,disc,dec=C[lid]
        r[i['gate_b_outcome']]='PASSOU'
        r[i['gate_b_notes']]=MET+ev+disc+dec
        r[i['gate_c_flags']]=flags
        r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
        feito[lid]='RETIDO'
    else:
        continue
    r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

# ---------------------------------------------------------------- log de eventos
EV=[
 (';'.join(sorted(A)),'DECISAO_GATE','B1','','E7',
  'Exclusao de 9 registros por E7, decidida em B1. Em todos, os autores nomeiam explicitamente a '
  'notacao de saida — GRL, BPMN, feature model, DFD, SysML v2, SIG, entidade-relacionamento, C4 e '
  'propriedades CTL — e nenhum dos tres campos traz elemento UML separavel. Em varios deles o I2 e o '
  'I4 estao satisfeitos: ha LLM nomeado com autoridade semantica e entrada textual. A falha e '
  'exclusivamente de saida (I5), e a regra de ouro 5 proibe rotula-la como E6.'),
 (';'.join(sorted(B)),'REVISAO_DECISAO','B2','E7 (proposta do script)','E6',
  'Quatro registros que o script de apoio propos excluir por E7 foram reclassificados para E6 em B2. '
  'O script disparou por detectar SysML na saida, mas o B1 nao decide com clareza esses casos: o '
  'SysML v1 e perfil de UML e reusa do metamodelo UML os diagramas de atividade, sequencia, maquina '
  'de estados e caso de uso, de modo que afirmar ausencia de componente UML separavel exigiria '
  'certeza que o resumo nao oferece. Ja o B2 decide sem ambiguidade: nenhum dos quatro apresenta '
  'termo do bloco LLM nem vocabulario de inteligencia artificial em titulo, resumo ou palavras-chave. '
  'Sao trabalhos de MBSE e de engenharia dirigida por modelos com transformacoes deterministicas. '
  'Aplicada a regra de ouro 3: o criterio primario e o primeiro portao que explica claramente o caso. '
  'Todos receberam a flag INCERTO_SAIDA, nao resolvida no B1.'),
 (';'.join(sorted(C)),'REVISAO_DECISAO','B','E7 (proposta do script)','',
  'Tres registros que o script de apoio propos excluir por E7 foram RETIDOS. 018_ACM: os modelos de '
  'comportamento SysML avaliados sao ACT e SD, isto e, diagrama de atividade e de sequencia, '
  'reusados do metamodelo UML — componente UML separavel, B1 resolvido pelo primeiro caso; passou os '
  'quatro subportoes e recebeu EVIDENCIA=EXPLICITA. 538_IEEE: o Mermaid e sintaxe portadora e nao '
  'notacao, como o PlantUML, que a definicao operacional do protocolo admite quando destinado a '
  'codificar UML; o resumo nao declara o tipo de diagrama, logo o caso e o terceiro do B1 e nao o '
  'segundo — retido com INCERTO_SAIDA. 539_IEEE: alem da mesma indeterminacao de saida, o resumo diz '
  '"Generative AI" mas descreve treinar modelo de NLP com dados rotulados, o que pela RF-01 seria '
  'E6; houve hesitacao genuina e a regra de ouro 1 mandou reter, com INCERTO_PAPEL_LLM e '
  'INCERTO_SAIDA.'),
 ('018_ACM;495_IEEE','INTERPRETACAO_PROTOCOLO','B1','','',
  'Fixada a distincao entre SysML v1 e SysML v2 para efeito do B1. O E7 do protocolo (l. 1245) nomeia '
  'SysML, mas a definicao operacional de "UML diagram" admite excecao quando o componente UML e '
  'separavel. O SysML v1 e perfil de UML: seus diagramas de comportamento sao reusados do metamodelo '
  'UML, de modo que ha componente separavel sempre que o relato nomeie um deles. O SysML v2 rompe '
  'essa filiacao — e linguagem autonoma construida sobre o KerML, sem reuso do metamodelo UML — e '
  'nao oferece componente separavel. A regra foi aplicada de forma simetrica nesta leva: 018_ACM, que '
  'nomeia ACT e SD do SysML v1, foi retido; 495_IEEE, que trata de SysML v2, foi excluido por E7. '
  'Registros de SysML v1 que nao nomeiam o tipo de diagrama nao sao decididos no B1 e seguem com '
  'INCERTO_SAIDA.'),
]
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    for ids,tipo,gate,cb,ca,nota in EV:
        w.writerow([ids,AGORA,REV,tipo,gate,cb,ca,nota,
                    'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'])

# ---------------------------------------------------------------- verificacao
from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('registros alterados: %d  (E7=%d E6=%d RETIDO=%d)'%(len(feito),
      sum(1 for v in feito.values() if v=='E7'),
      sum(1 for v in feito.values() if v=='E6'),
      sum(1 for v in feito.values() if v=='RETIDO')))
print('linhas=%d colunas=%d'%(len(rows),len(rows[0])))
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('VALIDOS=%d  EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_b_outcome:',dict(sorted(Counter(r[i['gate_b_outcome']] or '(nao triado)' for r in rows[1:]).items())))
print('por criterio  :',dict(sorted(Counter(r[i['exclusion_criteria']] for r in rows[1:] if r[i['excluded']]=='true').items())))
print('gate_c_flags  :',dict(sorted(Counter(r[i['gate_c_flags']] or '(vazio)' for r in rows[1:]).items())))
mau=0
for r in rows[1:]:
    a,b,ex,cr=r[i['gate_a_outcome']],r[i['gate_b_outcome']],r[i['excluded']],r[i['exclusion_criteria']]
    parou=(a!='PASSOU') or (b not in ('','PASSOU'))
    cod=(a.split('_')[-1] if a!='PASSOU' else (b.split('_')[-1] if b not in ('','PASSOU') else ''))
    if parou!=(ex=='true') or cod!=cr: mau+=1
print('divergencias portao x colunas derivadas:',mau)
tam=[len(r[i['gate_b_notes']]) for r in rows[1:] if r[i['logical_id']] in feito]
print('observacoes: n=%d min=%d max=%d'%(len(tam),min(tam),max(tam)))
