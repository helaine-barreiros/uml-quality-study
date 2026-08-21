import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: leitura integral do titulo, do resumo e das palavras-chave deste registro no CSV da '
     'busca automatizada, aplicando screening_manual_v1.md e screening_flow_v1.puml na ordem do '
     'Portao B (B1 saida, B2 origem, B3 direcao, B4 entrada). ')

D={
# ---------------- RETIDOS ----------------
'828_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: arcabouco de engenharia de requisitos que "focuses on specific Unified Modelling Language '
 '(UML) diagrams for preliminary system development" e integra LLMs a motores de raciocinio logico. O '
 'resumo declara que "the BEHAVIOURAL MODELS GENERATED WITH THE ASSISTANCE OF LLMs are automatically '
 'translated into formal logical specifications", e que a verificacao formal dedutiva assegura o '
 'tratamento dos requisitos logicos e das inter-relacoes entre artefatos. Ao fim, ha geracao automatica '
 'de esqueletos de programa. ',
 'DISCUSSAO: os quatro subportoes passam. B1: UML nomeada como objeto do arcabouco, com modelos '
 'comportamentais. B2: os modelos sao gerados pelos LLMs. B4: a entrada e a fase de requisitos. B3 '
 'merece nota, porque ha geracao de codigo ao fim: e o mesmo padrao texto -> UML -> codigo ja fixado em '
 '796, 806 e 810, que NAO e o E7 do B3, pois este pressupoe UML na entrada. Quanto ao I6, a verificacao '
 'formal dedutiva e mecanismo de aferimento de correcao sobre o modelo comportamental, mas incide sobre '
 'a traducao logica e nao ha metrica declarada sobre o diagrama. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR. Interessa a sintese como caso de verificacao formal '
 'aplicada a modelo comportamental gerado por LLM, familia de evidencia distinta das metricas de '
 'similaridade dominantes no corpus.'),

'829_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo abre justamente pelo problema desta revisao — "the QUALITY of generated '
 'artifacts, particularly COMPLEX GRAPHICAL MODELS, remains inconsistent and often below professional '
 'standards" — e propoe revisao colaborativa em que agentes LLM especializados trocam realimentacao '
 'iterativamente para refinar artefatos. A avaliacao contrapoe a abordagem a pipelines nao interativos '
 '"using a VALIDITY METRIC across three case studies", com ganhos discriminados por artefato: '
 'modelagem de dominio 31,03%, DIAGRAMAS DE SEQUENCIA 72,73%, DIAGRAMAS DE CLASSES 65,63%, '
 'implementacao 462,5% e teste 76,67%. ',
 'DISCUSSAO: os quatro subportoes passam. B1: dois tipos de diagrama nomeados. B2: os artefatos sao '
 'gerados e refinados pelos proprios agentes LLM. B3: ha producao e refinamento, e o refinamento e '
 'reparo de conteudo UML, tarefa que o I3 admite; nao e caso de E8, porque quem avalia tambem produz e '
 'o artefato E alterado. B4: os tres estudos de caso sao sistemas descritos textualmente. O I6 esta '
 'satisfeito de modo forte e raro: ha metrica de validade com valores REPORTADOS POR TIPO DE DIAGRAMA, '
 'o que permite extrair medidas separadas para diagrama de sequencia e diagrama de classes. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central; prioridade alta na fila de extracao.'),

'837_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: ECHO e abordagem para apoiar engenheiros de software no APRIMORAMENTO DA QUALIDADE de '
 'casos de uso UML com LLMs, por engenharia de prompt colaborativa e processo iterativo e interativo. '
 'Para provar a viabilidade, os autores instanciaram a abordagem com o ChatGPT e conduziram '
 'EXPERIMENTO CONTROLADO com sete profissionais: tres no grupo experimental usando ECHO, tres no grupo '
 'de controle aprimorando manualmente, e um setimo como ORACULO CEGO quanto aos grupos, que avaliou a '
 'qualidade dos casos de uso aprimorados qualitativamente por questionario e quantitativamente pela '
 'metrica de Pontos de Caso de Uso. ',
 'DISCUSSAO: B2, B3 e B4 passam com folga. A tarefa e aprimoramento, isto e, REPARO e REVISAO de '
 'conteudo, que o I3 admite expressamente, de modo que nao ha E8: o artefato E alterado, ao contrario '
 'de 839_SCOPUS e 861_SCOPUS. A entrada e caso de uso redigido em linguagem natural, ou seja, texto de '
 'requisitos, e nao modelo grafico preexistente, o que afasta o E9. Resta o B1, e a duvida e de '
 'fronteira do protocolo: o proprio resumo caracteriza os casos de uso como especificacao de '
 'requisitos funcionais "thanks to the USE OF NATURAL LANGUAGES", isto e, sao descricoes textuais no '
 'gabarito narrativo, e nao o diagrama de casos de uso. A especificacao da UML normatiza o DIAGRAMA, '
 'nao a narrativa, e a tabela da secao 4.1 do manual nao arrola a descricao textual. E a mesma questao '
 'ja aberta em 871_SCOPUS. O I6, em contrapartida, e dos mais fortes do corpus: experimento controlado '
 'com grupo de controle, oraculo cego e metrica quantitativa consagrada. ',
 'DECISAO: retido com INCERTO_SAIDA e EVIDENCIA=EXPLICITA. Reforca a urgencia de fixar, em evento '
 'INTERPRETACAO_PROTOCOLO antes da extracao, se a descricao textual de caso de uso conta como conteudo '
 'UML para efeito do I5.'),

'840_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: TIGRE e editor em linha para definicao de exercicios de modelagem UML em que o professor '
 'estabelece solucoes de referencia. O resumo declara que "the tool is enhanced by the interaction with '
 'recent Large Language Models for the AUTOMATED GENERATION OF REFERENCE SOLUTIONS STARTING FROM TEXT". '
 'O estudo de caso de prova de conceito gerou solucoes para dois exercicios e relata que "most of the '
 'relevant concepts have been represented correctly, but ISSUES EMERGED IN THE FORM OF UNNECESSARY '
 'CLASSES BEING INCLUDED AND INCORRECT UNDERSTANDING OF ASSOCIATIONS". ',
 'DISCUSSAO: registro do agrupamento educacional que, ao contrario de 753, 765, 771, 784, 807, 830, '
 '838 e 861, NAO sai por E8. A distincao e exatamente o eixo do B3: naqueles o diagrama e do estudante '
 'e o LLM o avalia; aqui o LLM GERA o diagrama de referencia a partir do enunciado textual do '
 'exercicio, e sao os autores que avaliam o resultado. Os quatro subportoes passam. O I6 esta '
 'satisfeito: ha analise de qualidade dos diagramas gerados, com dois modos de falha nomeados — '
 'classes supefluas e compreensao incorreta de associacoes —, o que e categoria de defeito diretamente '
 'aproveitavel na sintese, ainda que nao haja metrica numerica. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA.'),

'842_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR;CANDIDATO_E10',
 'EVIDENCIA: o resumo introduz abordagem que usa LLMs para apoiar modelagem de software, com '
 'aprendizado por prompt de poucos exemplos, "supporting various modeling activities without extensive '
 'training data", concentrando-se inicialmente "on STATIC AND BEHAVIORAL FORMALISMS LIKE UML DIAGRAMS" '
 'e visando estender-se a outros paradigmas e integrar-se ao pipeline de engenharia dirigida por '
 'modelos. Ha "user study" entre as palavras-chave. ',
 'DISCUSSAO: os quatro subportoes passam, com a ressalva de que o resumo nao nomeia tipos especificos '
 'de diagrama, dizendo apenas formalismos estaticos e comportamentais como diagramas UML — o que ainda '
 'assim identifica a UML de modo direto, e nao por comparacao, diferentemente de 825_SCOPUS. O que '
 'preocupa e o registro estilistico: os verbos sao de intencao ("we aim to extend", "we aim to"), e a '
 'expressao "this research introduces" sugere artigo curto de projeto de pesquisa, possivelmente de '
 'simposio de doutorado. A palavra-chave "user study" indica desenho empirico previsto, mas o resumo '
 'nao relata resultado algum. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR e CANDIDATO_E10. O E10 nao e decidivel em titulo e resumo '
 'e fica para a leitura integral.'),

'845_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o ecossistema CogniSim integra sistemas multiagente e LLMs, com agentes especializados em '
 'papeis de desenvolvedor, executor, verificador de qualidade e revisor de metodologia. A frase '
 'decisiva: "these agents PRODUCE DOCUMENTATION, MODELS, AND DIAGRAMS (E.G., UML) while adhering to '
 'PREDEFINED QUALITY AND PERFORMANCE MEASURES". Ha estudos de caso e simulacoes. ',
 'DISCUSSAO: B2, B3 e B4 passam: os agentes LLM produzem os artefatos, a direcao e de producao, e a '
 'entrada e o problema analisado, textual. O B1 fica em suspenso porque a UML aparece apenas como '
 'EXEMPLO PARENTETICO dentro de uma enumeracao generica de documentacao, modelos e diagramas, sem que '
 'nenhum tipo de diagrama seja nomeado — terceiro caso do B1. A mencao a medidas de qualidade '
 'predefinidas e promissora para o I6, mas o resumo nao diz se elas incidem sobre os diagramas ou '
 'sobre o desempenho dos agentes e das configuracoes de equipe, que e o objeto declarado das '
 'simulacoes. ',
 'DECISAO: retido com INCERTO_SAIDA e EVIDENCIA=A_VERIFICAR, pela regra de ouro 1.'),

'848_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo e "From Feature Description to UML Architecture: A Novel Framework for Automated '
 'Reasoning and MULTIMODAL EVALUATION of COMPONENT AND DEPLOYMENT DIAGRAM". O resumo, estruturado, '
 'declara no objetivo a construcao de "a viable end-to-end solution that can automatically CREATE AND '
 'VALIDATE UML diagrams" a partir de descricoes em linguagem natural, apontando a lacuna de que os '
 'metodos convencionais dependem de pericia humana e nao escalam. Palavras-chave autorais: raciocinio '
 'automatizado, avaliacao multimodal, modelagem de arquitetura de software, UMLCode e modelos de visao '
 'e linguagem. ',
 'DISCUSSAO: os quatro subportoes passam sem residuo. B1: dois tipos de diagrama nomeados no titulo, '
 'ambos arrolados na tabela da secao 4.1. B4: descricao de funcionalidade em linguagem natural, '
 'entrada exemplar. O I6 esta satisfeito no proprio titulo, com avaliacao multimodal por modelos de '
 'visao e linguagem — mesma familia de evidencia de 789_SCOPUS e 818_SCOPUS, que ja formam um '
 'agrupamento metodologico digno de nota na sintese: verificacao da UML gerada pela sua REPRESENTACAO '
 'GRAFICA, e nao apenas pelo codigo textual. Acrescente-se que diagramas de componentes e de '
 'implantacao sao sub-representados no corpus, dominado por classes e sequencia. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central; prioridade alta na fila de extracao.'),

'849_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: avaliacao de maquinas de estados finitos geradas por LLM a partir de descricoes de casos '
 'de negocio em linguagem natural, comparando ChatGPT 5.2 e Claude Sonnet 4.5 em doze casos de '
 'dificuldade variada, com tres estrategias de prompting. O resumo declara que "FSMs are GENERATED AS '
 'PLANTUML CODE and evaluated based on STATE AND TRANSITION ACCURACY, SEMANTIC ERRORS, PROCESS '
 'CONFUSION, and SELF-TRANSITION DETECTION", e conclui que a tecnica de prompting pesa mais na '
 'qualidade do que a escolha do modelo. ',
 'DISCUSSAO: B2, B3 e B4 passam de modo exemplar, e o I6 e dos mais ricos do corpus, com quatro '
 'construtos de qualidade nomeados e modos de falha catalogados. O B1 e que fica aberto, e a duvida e '
 'de fronteira. A saida e codigo PlantUML, que e SINTAXE PORTADORA e nao notacao; o tipo de artefato e '
 'nomeado — maquina de estados finitos —, mas os autores o tratam como formalismo comportamental '
 'geral, sem invocar a UML, e nem o titulo nem as palavras-chave autorais mencionam UML. Ora, a '
 'maquina de estados da UML e tipo arrolado na tabela da secao 4.1, e o diagrama de estados do '
 'PlantUML materializa essa notacao; mas uma FSM tambem existe fora da UML, e afirmar a identidade '
 'exigiria ver a sintaxe efetivamente usada. ',
 'DECISAO: retido com INCERTO_SAIDA e EVIDENCIA=EXPLICITA. Pela regra de ouro 1 a incerteza retem; a '
 'leitura integral deve verificar se o PlantUML gerado usa a notacao de diagrama de estados e se os '
 'autores a reivindicam como UML.'),

'852_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o artigo explora LLMs para automatizar a geracao de DIAGRAMAS DE CLASSES DE DOMINIO a '
 'partir de DESCRICOES ESTRUTURADAS DE CASOS DE USO. Distingue-se da literatura anterior, que aplicou '
 'LLMs a entradas nao estruturadas, ao usar formularios padronizados de descricao de caso de uso e o '
 'recurso de saidas estruturadas da OpenAI. Gera codigo PlantUML diretamente visualizavel, e "the '
 'approach is QUANTITATIVELY EVALUATED using a small set of structured use cases". ',
 'DISCUSSAO: os quatro subportoes passam. Duas observacoes. Primeira, o PlantUML nao gera incerteza '
 'aqui, porque o tipo de diagrama e nomeado no titulo e na palavra-chave autoral de abertura, '
 'resolvendo o segundo caso do B1. Segunda, e mais importante, a descricao estruturada de caso de uso '
 'esta na ENTRADA, como especificacao textual de requisitos, e nao na saida — de modo que a questao de '
 'protocolo aberta em 837 e 871 nao afeta este registro: o artefato UML produzido e inequivocamente o '
 'diagrama de classes. A avaliacao e quantitativa, ainda que sobre conjunto pequeno, o que interessa '
 'ao I6 e tambem a discussao sobre escala das evidencias. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA.'),

'854_SCOPUS':('PASSOU','INCERTO_SAIDA;CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: relato de iniciativa em que 44 estudantes de pos-graduacao em educacao computacional, em '
 '15 grupos, usaram LLMs para gerar conjuntos de dados sinteticos para seus projetos de pesquisa. '
 '"The resulting datasets were highly varied, INCLUDING buggy code in multiple languages, code with '
 'stylistic variations, UML DIAGRAMS, and natural language programming prompts." Os estudantes '
 'valorizaram a eficiencia e a escalabilidade, mas levantaram preocupacoes quanto a AUTENTICIDADE dos '
 'dados. ',
 'DISCUSSAO: ha, de fato, producao de diagramas UML por LLM (B1 e B2 satisfeitos em sentido literal) e '
 'a direcao e de producao (B3). O B4 nao permite excluir: a condicao restritiva do E9 exige que o '
 'resumo declare entrada de codigo, imagem, modelo existente ou registros, e nada disso e declarado — '
 'a entrada e o prompt do estudante pedindo dados sinteticos. Nenhum subportao do B, portanto, exclui '
 'este registro, e pela regra de ouro 1 ele nao pode ser descartado por mera impressao de '
 'irrelevancia. Duas reservas ficam anotadas. A UML e um item entre quatro numa enumeracao, sem tipo '
 'de diagrama nomeado e sem que se saiba se foi gerada a partir de descricao de dominio (terceiro caso '
 'do B1). E a preocupacao com autenticidade e dos ESTUDANTES quanto ao realismo dos dados, nao medida '
 'de qualidade do conteudo UML. ',
 'DECISAO: retido com INCERTO_SAIDA, CANDIDATO_E10 e EVIDENCIA=A_VERIFICAR. Prognostico fraco: o '
 'desfecho provavel e E10 na leitura integral, criterio de baixa que o manual proibe decidir em titulo '
 'e resumo.'),

'856_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: arcabouco agentico com LLMs para automatizar engenharia de ida e volta, com agentes '
 'especializados em transformacao, engenharia reversa e verificacao, sob processo com humano no laco. '
 'A frase decisiva: "we demonstrate the framework\'s feasibility with a PROOF-OF-CONCEPT that '
 'TRANSFORMS NATURAL LANGUAGE REQUIREMENTS INTO UML CLASS DIAGRAMS". ',
 'DISCUSSAO: a presenca de agente de ENGENHARIA REVERSA no arcabouco poderia sugerir E9 em B4, pela '
 'delimitacao de escopo que exclui a sintese a partir de codigo-fonte. Nao e o caso, e a razao e a '
 'regra de ouro 3: o que se deve triar e o estudo tal como conduzido, e a prova de conceito '
 'efetivamente demonstrada percorre o sentido requisitos em linguagem natural -> diagrama de classes '
 'UML, que retem. A engenharia reversa e capacidade prevista do arcabouco, nao o experimento relatado; '
 'se a leitura integral mostrar que o estudo tambem avalia o sentido inverso, isso se registra na '
 'extracao sem alterar o desfecho. Os quatro subportoes passam. O I6 e o ponto fraco: viabilidade e '
 'prova de conceito, sem metrica declarada. ',
 'DECISAO: retido com CANDIDATO_E10 e EVIDENCIA=A_VERIFICAR.'),

'858_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "Evaluating Large Language Models in Exercises of UML Use Case Diagrams Modeling". '
 'O objetivo declarado e "to ASSESS THE CAPABILITY OF LLM AGENTS TO GENERATE UML USE CASE DIAGRAMS '
 '(UCD), STARTING FROM SOFTWARE REQUIREMENTS IN NATURAL LANGUAGE", com a avaliacao conduzida em '
 'ambiente educacional, sobre exercicios de modelagem talhados para estudantes de mestrado. ',
 'DISCUSSAO: os quatro subportoes passam sem residuo. Registre-se que o artefato aqui e o DIAGRAMA de '
 'casos de uso, e nao a descricao textual, de modo que a questao de protocolo aberta em 837 e 871 nao '
 'o alcanca. Quanto ao B3, e outro registro educacional que retem: sao os autores que avaliam o que o '
 'LLM gerou, e nao o LLM que avalia o trabalho do estudante — eixo que separa este registro do '
 'agrupamento 753, 765, 771, 784, 807, 830, 838 e 861. O I6 esta no verbo nuclear do objetivo. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central.'),

'859_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo pergunta pelo impacto da CRITICA na geracao de modelos por LLM a partir de '
 'linguagem natural, no caso dos DIAGRAMAS DE ATIVIDADE. O resumo descreve o laco comum de geracao '
 'inicial seguida de critica e refinamento iterativos, e fixa dois requisitos que o processo precisa '
 'atender: "(1) STRUCTURAL CORRECTNESS - compliance with well-formedness rules - and (2) SEMANTIC '
 'ALIGNMENT - accurate reflection of the intended meaning in the source text". Apresenta o LADEX, '
 'pipeline para derivar diagramas de atividade de descricoes de processo em linguagem natural. '
 'Palavras-chave autorais incluem ainda "trace-based operational semantics" e "LLM-based '
 'activity-diagram matcher". ',
 'DISCUSSAO: os quatro subportoes passam sem residuo. Nao ha risco de E8: a critica e etapa INTERNA do '
 'proprio pipeline gerador, e o modelo E alterado pelo refinamento, o que caracteriza reparo admitido '
 'pelo I3 — condicao restritiva do E8 ("nao e alterado") nao satisfeita. Registro de valor '
 'metodologico excepcional: alem de satisfazer o I6, nomeia dois construtos de qualidade, ancora a '
 'conformidade em regras de boa formacao e propoe semantica operacional por tracos e um casador '
 'automatico de diagramas de atividade, isto e, contribui com INSTRUMENTO DE MEDICAO, tal como '
 '809_SCOPUS. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Prioridade maxima na fila de extracao.'),

# ---------------- B1: a saida nao e conteudo UML ----------------
'843_SCOPUS':('B1_E7','',
 'EVIDENCIA: arcabouco conceitual de ambiente multiagente com LLMs para projeto e refatoracao de '
 'software, com peritos especializados em desempenho, seguranca, interface e manutenibilidade, que '
 'colaboram por protocolos de consenso ou leilao "to synthesize DESIGN INSIGHTS AND REFACTORING '
 'RECOMMENDATIONS". A unica ocorrencia de UML esta na lista do que os AUTORES apresentam no artigo: '
 '"we present formal definitions of agent interactions..., A SEQUENCE DIAGRAM DEMONSTRATING AGENT '
 'COLLABORATION, a complexity analysis..., and an expanded reference list". ',
 'DISCUSSAO: o B1 resolve o caso. O produto dos agentes sao recomendacoes de refatoracao e percepcoes '
 'de projeto, nao conteudo UML. O diagrama de sequencia existe, mas e figura de exposicao desenhada '
 'pelos autores para ilustrar o proprio arcabouco, papel que a UML cumpre em incontaveis artigos de '
 'engenharia de software e que nunca satisfaz o I5. Nao ha producao, transformacao, reparo nem revisao '
 'de conteudo UML pelo metodo. Pela regra de ouro 3, o criterio primario e o primeiro portao que '
 'explica o caso com clareza, e e o B1. ',
 'DECISAO: excluido por E7 no subportao B1. Padrao de falso positivo frequente e ja recorrente no '
 'corpus: UML usada como ilustracao da arquitetura do proprio artigo.'),

# ---------------- B2: a origem do conteudo UML nao e LLM substantivo ----------------
'841_SCOPUS':('B2_E6','',
 'EVIDENCIA: o titulo e "Extracting UML Class Diagrams from Textual Specifications: COMPARATIVE '
 'ANALYSIS OF SOME DEEP LANGUAGE MODELS". O resumo nomeia os seis modelos comparados — "BERT, RoBERTa, '
 'SpanBERT, XLNet, MiniLM and Electra" — e a tarefa a que sao aplicados: "the task of EXTRACTING UML '
 'classes, attributes, methods and relationships from an ANNOTATED CORPUS". A palavra-chave autoral '
 'inclui "LLMs". ',
 'DISCUSSAO: e o caso paradigmatico para o qual a regra de fronteira RF-01 foi formulada. Todos os '
 'seis modelos sao codificadores pre-instrucionais, e nenhum e gerativo. A RF-01 fixa que codificadores '
 'como BERT e RoBERTa nao satisfazem o I2 automaticamente, e que o uso como classificador, marcador, '
 'EXTRATOR, incorporacao vetorial ou reconhecimento de entidades nomeadas leva a E6. O verbo do titulo '
 'e do resumo e justamente extrair, e a mencao a corpus ANOTADO confirma o desenho de rotulacao '
 'supervisionada de sequencia: os modelos identificam vaos de texto correspondentes a classes, '
 'atributos, metodos e relacoes, e a montagem do diagrama e posterior e determinista. Falha o I2 '
 'quanto a origem do conteudo. Registre-se que a palavra-chave "LLMs", atribuida pelos autores, e '
 'imprecisa e nao prevalece sobre a enumeracao explicita dos modelos no resumo. Nota de fronteira, '
 'para dupla triagem: pode-se objetar que a extracao E semanticamente constitutiva, pois determina '
 'quais classes existem; a RF-01, todavia, arrola o extrator entre os usos que levam a E6, e a '
 'excecao que ela abre e para o uso GERATIVO, ausente aqui. ',
 'DECISAO: excluido por E6 no subportao B2. Decisao de fronteira, expressamente sinalizada para '
 'conferencia pelo segundo revisor.'),

'844_SCOPUS':('B2_E6','',
 'EVIDENCIA: o titulo e "A UML PROFILE FOR Domain-specific Modelling of RETRIEVAL AUGMENTED GENERATION '
 '(RAG) SYSTEM ARCHITECTURE". O resumo parte das dependencias estruturais complexas que surgem ao '
 'integrar componentes probabilisticos de IA a software determinista, com falhas silenciosas como '
 'incompatibilidade de dimensao de vetores e transbordo de janela de contexto, e aplica Design Science '
 'Research "to develop a domain-specific UML Profile for RAG systems". Palavras-chave autorais: '
 'engenharia dirigida por modelos, OCL, RAG e perfil UML. ',
 'DISCUSSAO: ha conteudo UML abundante, autoral e de alto teor — um perfil, com estereotipos e '
 'restricoes OCL —, o que afasta o B1. Mas o B2 resolve o caso: o perfil e construido pelos '
 'PESQUISADORES, por metodo de Design Science, e o sistema RAG com seu LLM e o OBJETO MODELADO, nao o '
 'agente modelador. Nenhum LLM tem autoridade semantica sobre estereotipo, metaclasse ou restricao do '
 'perfil. Falha o I2 quanto a origem. E o mesmo padrao de 768_SCOPUS e 804_SCOPUS, em que o LLM e o '
 'sistema descrito. A coocorrencia de OCL nas palavras-chave nao muda o desfecho e nao se confunde com '
 'a questao de protocolo aberta em 758_SCOPUS e 518_IEEE, que trata de OCL GERADA POR LLM. ',
 'DECISAO: excluido por E6 no subportao B2.'),

# ---------------- B3: direcao invertida ----------------
'833_SCOPUS':('B3_E7','',
 'EVIDENCIA: Flow2Code e marco de avaliacao para geracao de codigo A PARTIR DE FLUXOGRAMAS. O conjunto '
 'de avaliacao "spans 15 programming languages and includes 5,622 code segments PAIRED WITH 16,866 '
 'FLOWCHARTS OF THREE TYPES: CODE, UML, AND PSEUDOCODE", e os experimentos com 13 LLMs multimodais '
 'mostram que os modelos ainda nao geram codigo a partir de fluxogramas perfeitamente. ',
 'DISCUSSAO: B1 e B2 passam, pois ha conteudo UML real e os LLMs sao substantivos. O B3 resolve: o '
 'fluxograma UML e INSUMO, ja existe no conjunto de dados e nao e alterado, e o produto avaliado e '
 'codigo-fonte. Recai na celula UML existente -> LLM -> codigo da matriz da secao 4.3, que fixa E7. '
 'Falha o I5, que exige conteudo UML na SAIDA. Note-se que a entrada e ainda multimodal, isto e, '
 'imagem de fluxograma, o que tambem faria falhar o I4, mas o B3 antecede o B4 e ja explica o caso com '
 'clareza. O desfecho B3_E7 preserva a distincao ante o B1_E7: aqui havia UML, mas na entrada. ',
 'DECISAO: excluido por E7 no subportao B3.'),

'853_SCOPUS':('B3_E7','',
 'EVIDENCIA: PFDial constroi conjunto de dados de dialogo dirigido por processo com 12.705 instrucoes '
 'em chines "DERIVED FROM 440 FLOWCHARTS containing 5,055 process nodes". O mecanismo e declarado: '
 '"Based on PlantUML specification, EACH UML FLOWCHART IS CONVERTED INTO ATOMIC DIALOGUE" instrucoes, '
 'que servem depois ao ajuste fino por instrucao de sistemas de dialogo sob restricoes estritas de '
 'processo. ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve: os 440 fluxogramas UML PREEXISTEM e sao a fonte da '
 'conversao; o produto e um conjunto de instrucoes de dialogo e, adiante, um modelo ajustado. Nao ha '
 'producao, transformacao, reparo nem revisao de conteudo UML — o fluxograma e consumido, e o que dele '
 'resulta e dado de treinamento, especie do genero documentacao na matriz da secao 4.3. Falha o I5. '
 'Registre-se que a mencao a especificacao PlantUML esta na ENTRADA, confirmando mais uma vez que a '
 'palavra-chave PlantUML nao e por si sinal de candidatura. ',
 'DECISAO: excluido por E7 no subportao B3.'),

'857_SCOPUS':('B3_E7','',
 'EVIDENCIA: o resumo lamenta que os diagramas UML criados no inicio do projeto de aplicativos Android '
 'sejam usados apenas como documentacao, e propoe "a program that GENERATES SOURCE CODE FOR ANDROID '
 'APPLICATIONS FROM UML CLASS DIAGRAMS", processo realizado "by INTERPRETING STANDARDIZED UML" '
 'representacoes. Palavras-chave autorais: aplicativos Android, geracao automatica de codigo, LLMs e '
 'engenharia dirigida por modelos. ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve sem residuo: o diagrama de classes ja existe, e produto do '
 'processo de projeto conduzido por humanos, e nao e alterado; o produto e codigo-fonte Android. '
 'Celula UML existente -> LLM -> codigo, que a matriz da secao 4.3 fixa como E7. Falha o I5. E o caso '
 'central da delimitacao de escopo fixada em 2026-08-16, que exclui expressamente a UML como insumo '
 'para gerar codigo. ',
 'DECISAO: excluido por E7 no subportao B3.'),

'830_SCOPUS':('B3_E8','',
 'EVIDENCIA: prova de conceito de assistente de AVALIACAO baseado em IA generativa, aplicado ao marco '
 'de projeto da disciplina de Engenharia de Software I da Universidade de Salamanca. O sistema '
 '"combines a MULTIMODAL PIPELINE TO PROCESS PDF REPORTS (INCLUDING TEXT AND USE CASE DIAGRAMS) with a '
 'flow of prompts ALIGNED WITH THE SUBJECT\'S RUBRIC". ',
 'DISCUSSAO: B1 e B2 passam. No B3 a direcao e inequivoca: o relatorio e os diagramas de casos de uso '
 'sao entregues pelos ESTUDANTES, ja existem, e o LLM os processa para produzir avaliacao conforme '
 'rubrica. Nao ha producao, transformacao, reparo nem revisao de conteudo UML, e a condicao restritiva '
 'do E8 esta satisfeita, pois o diagrama nao e alterado. A tabela da secao 4.2 e expressa: "LLM apenas '
 'avalia ou explica um diagrama ja existente -> E8". Falha o I3. Note-se que a entrada e PDF, isto e, '
 'imagem, o que tambem faria falhar o I4, mas o B3 antecede o B4. ',
 'DECISAO: excluido por E8 no subportao B3. Integra o agrupamento de avaliacao automatizada em '
 'contexto educacional.'),

'838_SCOPUS':('B3_E8','',
 'EVIDENCIA: o titulo pergunta "Can Multimodal Large Language Models GRADE LIKE AN EXPERT? A Study on '
 'UML CLASS DIAGRAM ASSESSMENT ACCURACY". O desenho e nitido: trinta e quatro estudantes de engenharia '
 'realizaram tarefa de projeto aplicando os cinco principios S.O.L.I.D., e "THEIR SOLUTIONS WERE '
 'INDEPENDENTLY ASSESSED BY THREE" avaliadores, com o estudo investigando a capacidade dos modelos '
 'multimodais de avaliar a qualidade dos diagramas de classes quanto a estrutura de classes e '
 'informacao de atributos. ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve: os diagramas sao produzidos pelos ESTUDANTES e o LLM '
 'multimodal apenas os nota, sem alterar conteudo algum — condicao restritiva do E8 plenamente '
 'satisfeita. Falha o I3. Cabe registrar a natureza onerosa desta exclusao: o artigo mede acuracia de '
 'AVALIACAO DE QUALIDADE de diagramas de classes contra gabarito de especialistas humanos, e portanto '
 'trata de instrumentos de medicao que interessam a esta revisao — mas a UML avaliada nao e gerada por '
 'LLM, e o I3 exige que o LLM produza, transforme, repare ou revise o conteudo. ',
 'DECISAO: excluido por E8 no subportao B3. Registro nomeado como trabalho adjacente de interesse para '
 'a discussao sobre validade de LLM-como-juiz, ainda que fora do escopo de inclusao.'),

'839_SCOPUS':('B3_E8','',
 'EVIDENCIA: MCeT e apresentado como "the first fully automated tool to EVALUATE THE CORRECTNESS OF A '
 'BEHAVIORAL MODEL, SEQUENCE DIAGRAMS IN PARTICULAR, AGAINST ITS CORRESPONDING REQUIREMENTS TEXT AND '
 'PRODUCE A LIST OF ISSUES that the model has". O metodo parte o diagrama em interacoes atomicas e o '
 'texto em itens autocontidos, com verificacao de autoconsistencia para mitigar alucinacoes. A '
 'precisao sobe de 0,58 para 0,81 sobre requisitos reais, e a abordagem encontra 90% mais problemas '
 'dos que os engenheiros experientes haviam encontrado. ',
 'DISCUSSAO: B1 e B2 passam. O B3 exige atencao redobrada, porque o resumo menciona autoaperfeicoamento '
 '— "enable AI assistants to SELF-EVALUATE AND SELF-ENHANCE their generated models". Essa frase, '
 'porem, descreve o USO FUTURO que outros sistemas poderiam fazer do MCeT, e nao o que o MCeT faz: o '
 'produto declarado da ferramenta e uma LISTA DE PROBLEMAS, e em nenhum momento ela altera o diagrama. '
 'A condicao restritiva do E8 ("o diagrama ja existe e NAO E ALTERADO") esta portanto satisfeita, ao '
 'contrario do que ocorreu em 215_ACM, onde havia deteccao E CORRECAO, e em 859_SCOPUS, onde a critica '
 'integra laco de refinamento que altera o modelo. Falha o I3. ',
 'DECISAO: excluido por E8 no subportao B3. Exclusao onerosa e nomeada para eventual recuperacao: e o '
 'unico registro do corpus que constroi e valida um instrumento automatico de correcao para diagramas '
 'de sequencia, com precisao medida contra juizo de engenheiros experientes, e sua motivacao declarada '
 'e justamente a crescente geracao de diagramas por LLM. Interessa a discussao metodologica desta '
 'revisao ainda que fora do escopo de inclusao.'),

'861_SCOPUS':('B3_E8','',
 'EVIDENCIA: titulo "ASSESSING UML DIAGRAMS BY GPT: Implications for education". O resumo situa o '
 'problema na tarefa demorada e trabalhosa que os educadores enfrentam "to REVIEW AND GRADE A LARGE '
 'NUMBER OF UML DIAGRAMS CREATED BY THE STUDENTS", e aponta os avancos recentes em IA generativa, como '
 'o GPT, como via para automatizar tarefas de engenharia de software. Palavras-chave autorais: GPT, '
 'avaliacao de modelo, educacao em modelagem de software e diagrama UML. ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve sem residuo: os diagramas sao criados pelos ESTUDANTES e o '
 'GPT os revisa e nota, sem alterar conteudo. Condicao restritiva do E8 satisfeita; falha o I3. '
 'Aplica-se diretamente a tabela da secao 4.2. ',
 'DECISAO: excluido por E8 no subportao B3.'),

# ---------------- B4: a entrada nao e especificacao textual ----------------
'863_SCOPUS':('B4_E9','',
 'EVIDENCIA: estudo sobre o potencial da IA generativa para facilitar a MIGRACAO DE APLICACOES LOCAIS '
 'PARA A NUVEM, com experimentacao em ambientes integrados de desenvolvimento e metodologias de '
 'migracao recomendadas por provedores. Entre os beneficios encontrados, "the value added by GitHub '
 'Copilot in DESCRIBING AND CREATING CODE FOR CLASS DIAGRAMS". A investigacao envolve "TESTING CODE '
 'CAPABILITIES AND EXPLANATIONS across various frameworks and projects", e os autores relatam ainda o '
 'uso do Gemini "to TURN LEGACY JENKINS CODE INTO GITHUB ACTIONS". ',
 'DISCUSSAO: a formula "creating code for Class Diagrams" e sintaticamente ambigua e nao permite '
 'decidir o B1 nem o B3: tanto pode significar gerar diagramas de classes a partir do codigo herdado '
 'quanto gerar codigo a partir de diagramas. Pela regra de ouro 3, desce-se ao subportao que explica o '
 'caso sem residuo, e e o B4. Qualquer que seja o sentido, a fonte de todo o trabalho e o ACERVO DE '
 'CODIGO das aplicacoes locais legadas — nao ha especificacao textual de requisitos, historia de '
 'usuario, cenario ou descricao de dominio em parte alguma do resumo. A condicao restritiva do E9 '
 '("entrada de codigo") esta expressamente satisfeita, e a delimitacao de escopo fixada em 2026-08-16 '
 'exclui a engenharia reversa a partir de codigo-fonte. Falha o I4. ',
 'DECISAO: excluido por E9 no subportao B4. Desfecho estavel sob qualquer das duas leituras possiveis '
 'da frase ambigua.'),
}

assert len(D)==24, len(D)
CRIT={'B1_E7':'E7','B2_E6':'E6','B3_E7':'E7','B3_E8':'E8','B4_E9':'E9'}

rows=list(csv.reader(open(CSV,encoding='utf-8')))
i={c:n for n,c in enumerate(rows[0])}
n=0
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid not in D: continue
    assert r[i['excluded']]!='true' and not r[i['gate_b_outcome']], lid
    out,flags,ev,di,de=D[lid]
    r[i['gate_b_outcome']]=out; r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    r[i['gate_b_notes']]=MET+ev+di+de
    if out=='PASSOU':
        r[i['gate_c_flags']]=flags; r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
        r[i['gate_c_notes']]=('Flags atribuidas na mesma leitura do Portao B; ver gate_b_notes para a '
            'evidencia e a discussao que as fundamentam. Pela regra de ouro 2, nenhuma flag exclui.')
    else:
        r[i['excluded']]='true'; r[i['exclusion_criteria']]=CRIT[out]
    n+=1
assert n==24, n

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

grp={}
for k,v in D.items(): grp.setdefault(v[0],[]).append(k)
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow([';'.join(sorted(D)),AGORA,REV,'DECISAO_GATE','B','','',
     'Quarto lote de leitura individual dos registros que mencionam UML no titulo ou no resumo: 24 '
     'registros triados, indices 72 a 95 da lista. Desfechos: 13 RETIDOS, 1 E7 em B1, 2 E6 em B2, 3 E7 '
     'em B3, 4 E8 em B3 e 1 E9 em B4. Candidatos centrais: 859_SCOPUS (LADEX, diagramas de atividade '
     'com laco de critica e refinamento, correcao estrutural e alinhamento semantico como construtos '
     'nomeados, alem de casador automatico de diagramas — contribui com INSTRUMENTO, como 809_SCOPUS), '
     '848_SCOPUS (diagramas de componentes e de implantacao com avaliacao multimodal, tipos '
     'sub-representados no corpus), 829_SCOPUS (metrica de validade REPORTADA POR TIPO DE DIAGRAMA, '
     'permitindo extracao separada para sequencia e classes), 858_SCOPUS e 837_SCOPUS (este com '
     'experimento controlado, grupo de controle, oraculo cego e metrica de Pontos de Caso de Uso, a '
     'evidencia empirica mais robusta encontrada ate aqui). Cinco achados metodologicos. (1) O '
     'agrupamento de AVALIACAO AUTOMATIZADA POR LLM ja soma oito registros, todos B3_E8 — 753, 765, '
     '771, 784, 807, 830, 838 e 861 —, e consolida-se como subarea ativa e adjacente, a ser nomeada no '
     'relato de metodo. (2) O eixo que separa esse agrupamento dos retidos e sempre o mesmo: quem '
     'produz e quem avalia. Em 840_SCOPUS e 858_SCOPUS ha contexto educacional identico, mas e o LLM '
     'que GERA e sao os autores que avaliam, e por isso retem. (3) Duas exclusoes onerosas ficam '
     'NOMEADAS para eventual recuperacao, por construirem instrumentos de medicao de qualidade sobre '
     'UML: 839_SCOPUS (MCeT, primeira ferramenta totalmente automatica de avaliacao de correcao de '
     'diagramas de sequencia contra o texto de requisitos, precisao de 0,58 para 0,81, motivada '
     'expressamente pela crescente geracao por LLM) e 838_SCOPUS (acuracia de LLM multimodal como '
     'avaliador contra gabarito humano). Saem por E8 porque a UML avaliada nao e gerada por LLM, mas '
     'interessam a discussao sobre LLM-como-juiz. (4) 841_SCOPUS e DECISAO DE FRONTEIRA expressamente '
     'sinalizada para o segundo revisor: compara BERT, RoBERTa, SpanBERT, XLNet, MiniLM e Electra na '
     'EXTRACAO de classes, atributos, metodos e relacoes de corpus ANOTADO. E o caso paradigmatico da '
     'RF-01, que arrola o uso como extrator entre os que levam a E6, reservando a excecao ao uso '
     'gerativo; cabe a objecao de que a extracao e semanticamente constitutiva, e por isso a decisao '
     'fica marcada. (5) Confirma-se em 839 e 859 a importancia da condicao restritiva do E8: em '
     '839_SCOPUS a mencao a autoaperfeicoamento descreve uso futuro POR TERCEIROS, e a ferramenta '
     'apenas produz lista de problemas, ao passo que em 859_SCOPUS a critica integra laco que ALTERA o '
     'modelo, o que caracteriza reparo admitido pelo I3 e retem.',
     'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('alterados:',n,{k:len(v) for k,v in sorted(grp.items())})
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
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
