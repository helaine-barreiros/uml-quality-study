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
'866_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: metodo de geracao automatica de modelos de visao de arquitetura de sistemas e de sistemas '
 'de sistemas com LLM em torno da SysML. O LLM e conduzido a gerar dados XML conformes a tarefa de '
 'modelagem, com base de conhecimento local em RAGFlow, e um algoritmo em DOM4J converte o XML ao '
 'paradigma SysML. O resumo e explicito quanto aos tipos: "focusing on BLOCK DEFINITION DIAGRAM, '
 'INTERNAL BLOCK DIAGRAM, ACTIVITY DIAGRAM", com veiculo submarino nao tripulado como estudo de caso, '
 'e "relevant INDICATORS are introduced to EVALUATE THE VALIDITY AND ACCURACY of the generated models". ',
 'DISCUSSAO: a questao SysML resolve-se pela v1, e por dois sinais convergentes, como em 812_SCOPUS: o '
 'resumo nomeia DIAGRAMA DE ATIVIDADE, tipo reusado do metamodelo UML e arrolado na tabela da secao '
 '4.1, e usa "block definition diagram", vocabulario da v1 substituido por "part definition" na v2. Ha '
 'portanto componente UML separavel, e o B1 passa. B2 passa pela RF-02: a conversao DOM4J e simbolica, '
 'mas quem determina o conteudo semantico do modelo e o LLM que gera o XML. B3 e B4 passam. O I6 esta '
 'satisfeito com dois construtos nomeados, validade e acuracia, medidos por indicadores. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA.'),

'867_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o artigo gera regras de configuracao e conceitos de projeto com o ChatGPT, tomando a '
 'configuracao de sistemas de propulsao hibrida de aeronaves como exemplo. A frase decisiva: "it is '
 'shown how a system configuration can be GENERATED AND PRESENTED IN THE FORM OF UML COMPONENT '
 'DIAGRAMS". Sobre o I6: "Large Language Models usually have an element of randomness... This makes '
 'them inherently non-deterministic, and the result IS NOT ALWAYS CORRECT. Therefore, STATISTICAL '
 'PROPERTIES ARE STUDIED such that the PROBABILITY OF GETTING A CORRECT RESULT CAN BE ESTIMATED, and '
 'prompts can be tweaked to provide the best result." ',
 'DISCUSSAO: os quatro subportoes passam. B1: diagrama de componentes nomeado, tipo arrolado na secao '
 '4.1 e sub-representado no corpus. B4: a entrada e o prompt em linguagem natural que descreve a '
 'tarefa de configuracao, com separacao entre parte geral reusavel e parte especifica. O I6 e de '
 'natureza incomum e valiosa: em vez de comparar um artefato a um gabarito, o estudo trata a correcao '
 'como VARIAVEL ALEATORIA e estima a probabilidade de resultado correto sob repeticao, atacando '
 'diretamente o nao determinismo do LLM. E familia de evidencia distinta das metricas de similaridade '
 'e da comparacao com especialistas, e merece registro proprio na taxonomia da sintese. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Interessa tambem por ser dominio de engenharia aeronautica, '
 'fora do nucleo de engenharia de software do corpus.'),

'868_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "MULTIMODAL VALIDATION IN UML SYNTHESIS: A DUAL-CASE STUDY ON SEQUENCE AND CLASS '
 'DIAGRAM GENERATION PIPELINES". O resumo apresenta processo unificado de sintese automatizada e '
 'validacao multimodal de diagramas UML, avaliado com diagramas de classes e de sequencia, em '
 'abordagem de tres fases. Palavras-chave autorais: AuCodeUML, LLMs, raciocinio de modelo, validacao '
 'multimodal, PlantUML e diagrama de classes UML. ',
 'DISCUSSAO: os quatro subportoes passam. B1: dois tipos nomeados no titulo. O I6 esta no titulo, com '
 'validacao multimodal. Registre-se a filiacao: este registro pertence a uma familia de quatro '
 'trabalhos do corpus que compartilham vocabulario, sigla UMLCode e a mesma tecnica de validacao por '
 'modelos de visao e linguagem — 818, 848, 869 e 877 —, todos retidos. Ha risco de PUBLICACAO '
 'REDUNDANTE entre eles, isto e, de o mesmo estudo aparecer fatiado em varias saidas. Isso nao se '
 'decide em titulo e resumo e nao e motivo de exclusao nesta etapa; fica anotado para verificacao na '
 'leitura integral, quando entao se decidira se ha um estudo unico com varios relatos, caso em que se '
 'elege o relato mais completo e os demais se vinculam a ele. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA, com alerta de possivel publicacao redundante na familia '
 '818, 848, 868, 869 e 877.'),

'869_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo declara a lacuna — "unstructured requirements, limited automated pipelines, and '
 'the LACK OF RELIABLE EVALUATION METHODS" — e apresenta arquitetura que reune desenvolvimento de '
 'requisitos, sintese de UML e validacao multimodal. O pipeline e de dois LLMs: "LLaMA-3.2-1B-Instruct '
 'was utilized to generate user-focused requirements. Then, DeepSeek-R1-Distill-Qwen-32B applies its '
 'reasoning skills to TRANSFORM THESE REQUIREMENTS INTO PLANTUML CODE." Foi construido conjunto '
 'sintetico de 11.997 diagramas UML. Palavras-chave autorais: geracao automatizada de conjunto de '
 'dados, validacao multimodal, UMLCode e modelos de visao e linguagem. ',
 'DISCUSSAO: os quatro subportoes passam, com a mesma leitura ja aplicada a 818_SCOPUS: a '
 'especificacao de requisitos e ela propria sintetica, produzida pelo primeiro modelo, o que nao afeta '
 'o I4, pois este exige entrada textual de requisitos ou de dominio sem exigir origem humana. O I6 '
 'esta satisfeito pela validacao multimodal, e o proprio resumo identifica a ausencia de metodos '
 'confiaveis de avaliacao como a lacuna atacada, o que faz do registro fonte direta para a questao de '
 'pesquisa desta revisao. A escala do conjunto, quase doze mil diagramas, e a maior do corpus. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Mesmo alerta de publicacao redundante da familia 818, 848, '
 '868, 869 e 877, a resolver na leitura integral.'),

'870_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o artigo analisa as fases tradicionais do desenvolvimento de solucoes em cadeia de blocos '
 'e demonstra como LLMs podem acelerar cada uma, com estudo de caso de gestao de medicamentos '
 'controlados. A frase decisiva: "we utilize a customized version of ChatGPT to automate and '
 'accelerate the generation of REQUIREMENTS, SEQUENCE DIAGRAMS, SMART CONTRACT CODE, UNIT TESTS, and '
 'cost and security analyses, WITH EACH PHASE BUILDING ON THE OUTPUT OF THE PREVIOUS ONE". Os autores '
 'testam e validam a abordagem e a comparam com o desenvolvimento manual. ',
 'DISCUSSAO: os quatro subportoes passam. B1: diagrama de sequencia nomeado. B3 merece nota, porque ha '
 'geracao de codigo de contrato inteligente e de testes: e de novo o padrao texto -> UML -> codigo, '
 'ja fixado em 796, 806, 810 e 828, que nao e o E7 do B3, pois este pressupoe UML na entrada — aqui o '
 'diagrama de sequencia e produzido pelo LLM a partir dos requisitos, que o proprio LLM elicitou. '
 'Quanto ao I6, ha comparacao com abordagem manual, mas os resultados relatados sao de ACELERACAO E '
 'EFICIENCIA, nao de qualidade do diagrama. Ha ainda risco de E10: como cada fase se apoia na saida da '
 'anterior, pode nao ser possivel separar o resultado referente a UML dos demais artefatos. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR. O E10 e de baixa e nao e decidivel nesta etapa.'),

'872_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: PathOCL e metodo de aumento de prompt por caminhos para geracao de OCL com GPT-4. O '
 'resumo afirma que "LLMs have demonstrated their ability to EXPRESS UML MODEL SPECIFICATIONS USING '
 'FORMAL LANGUAGES LIKE THE OBJECT CONSTRAINT LANGUAGE (OCL)", e ataca a limitacao de tamanho de '
 'contexto que se agrava a medida que cresce o modelo de classes UML. Palavras-chave autorais: modelo '
 'de fundacao, GPT, LLM, OCL, engenharia de prompt e caminho simples. ',
 'DISCUSSAO: B2, B3 e B4 passam com a mesma leitura de 758_SCOPUS: o modelo de classes UML entra no '
 'prompt como CONTEXTO, selecionado por caminhos para caber na janela, e a fonte da restricao e a '
 'especificacao em linguagem natural. Nao e, portanto, caso de E9, pois nao ha transformacao de modelo '
 'existente, mas uso de modelo existente como contexto. O B1 fica em suspenso pela mesma questao de '
 'fronteira: a OCL e norma da OMG companheira da UML e anexa-se a elementos do modelo, sendo nesse '
 'sentido conteudo semantico portador de significado, mas nao e diagrama e nao consta da tabela da '
 'secao 4.1. ',
 'DECISAO: retido com INCERTO_SAIDA e EVIDENCIA=A_VERIFICAR. Terceiro registro afetado pela questao de '
 'protocolo da OCL, ao lado de 758_SCOPUS e 518_IEEE, o que torna a fixacao dessa fronteira condicao '
 'previa da extracao.'),

'876_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: UCD-LLM e arcabouco multiagente para modelagem de requisitos em diagramas de casos de uso, '
 'com resumo estruturado. Objetivo: "leverage LLMs to automatically extract COMPLEX USE CASE DIAGRAM '
 'ELEMENTS FROM NATURAL LANGUAGE TEXT". Metodo: LLMs guiados por prompts, mecanismo de autorreflexao '
 'contra alucinacao e mecanismo de DEBATE MULTIAGENTE que emula a discussao entre modeladores. '
 'Resultados: avaliado na extracao de atores, casos de uso e relacoes, "compared with a traditional '
 'machine-learning method and three zero-shot LLM baselines, it achieves superior results on most '
 'metrics", com melhora de FEF de 148% a 167% em cinco casos classicos e RNF de 0,693 no conjunto '
 'ReqUCD60, 16,2% acima do modelo Qwen basico, alem de estudos de ablacao. Codigo publico. ',
 'DISCUSSAO: os quatro subportoes passam. Cabe registrar o contraste deliberado com 841_SCOPUS, que '
 'saiu por E6: ambos usam o verbo EXTRAIR, mas ali os modelos eram codificadores pre-instrucionais '
 'aplicados a rotulacao de corpus anotado, ao passo que aqui sao LLMs generativos guiados por prompt, '
 'com autorreflexao e debate, isto e, uso gerativo e semanticamente constitutivo, que a RF-01 admite '
 'expressamente. O I6 e dos mais fortes do corpus: metricas nomeadas, conjunto de dados proprio, '
 'linhas de base tradicionais e por LLM, ablacao e codigo disponivel. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central; prioridade maxima na fila de extracao.'),

'877_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o artigo estende o arcabouco de geracao automatizada de UML para a sintese de DIAGRAMAS '
 'DE CLASSES, com pipeline de dois modelos: "a lightweight LLM (LLaMA 3.2 1B-Instruct) generates '
 'detailed technical specifications, which are then TRANSLATED INTO PLANTUML CLASS DIAGRAM CODE by a '
 'powerful reasoning" model. Palavras-chave autorais: geracao automatizada de UML, LLMs, raciocinio de '
 'modelo, validacao multimodal, PlantUML e diagrama de classes UML. ',
 'DISCUSSAO: os quatro subportoes passam, com a mesma leitura de 818 e 869. O I6 esta satisfeito pela '
 'validacao multimodal declarada nas palavras-chave autorais. A expressao "extends OUR framework" '
 'confirma expressamente a continuidade com os demais membros da familia, e reforca o alerta de '
 'publicacao redundante. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA, com alerta de possivel publicacao redundante na familia '
 '818, 848, 868, 869 e 877, a resolver na leitura integral.'),

'878_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR;CANDIDATO_E10',
 'EVIDENCIA: myChatCT e assistente educacional para pensamento computacional no ensino medio. A frase '
 'decisiva: "utilizing the ChatGPT API, myChatCT navigates users through the stages of CT... while '
 'CONVERTING NATURAL LANGUAGE INPUTS INTO STRUCTURED ACTIVITY DIAGRAMS. These diagrams serve as a '
 'conduit between conceptual understanding and code execution... and GENERATING ANNOTATED CODE". Para '
 'aferir a eficacia, "LOAD TESTS were conducted to simulate diverse user scenarios, analyzing RESPONSE '
 'TIMES, ERROR RATES, and RESOURCE UTILIZATION". ',
 'DISCUSSAO: os quatro subportoes passam: diagrama de atividade nomeado no titulo e na primeira '
 'palavra-chave autoral (B1), ChatGPT como gerador (B2), producao a partir de entrada em linguagem '
 'natural (B3 e B4). E mais um registro educacional que RETEM, pela mesma razao de 840 e 858: e o LLM '
 'que gera o diagrama, e nao o LLM que avalia o do estudante. O ponto fraco esta no I6: a avaliacao '
 'declarada e de DESEMPENHO DE SISTEMA — tempo de resposta, taxa de erro e uso de recurso —, e nao de '
 'qualidade do conteudo UML. Pela regra de ouro 2, a ausencia de vocabulario de qualidade nunca '
 'exclui nesta etapa, e o E11 e expressamente proibido em titulo e resumo pelo protocolo. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR e CANDIDATO_E10.'),

'879_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR;CANDIDATO_E10',
 'EVIDENCIA: o resumo declara que "this EXPERT VOICE addresses a significant gap in the evaluation of '
 'these models, advocating for the need for standardized benchmarking frameworks", e propoe arcabouco '
 'conceitual "to ASSESS THEIR QUALITY IN SOFTWARE MODEL GENERATION", visando a padronizacao do '
 'processo de aferimento comparativo. O arcabouco "is illustrated using UML CLASS DIAGRAMS AS A '
 'RUNNING EXAMPLE". ',
 'DISCUSSAO: o registro toca o nucleo tematico desta revisao — como medir a qualidade de modelos '
 'gerados por LLM — mas nao e estudo primario de geracao: ninguem gera diagrama neste artigo, e o '
 'diagrama de classes serve de exemplo condutor do arcabouco proposto. Nenhum subportao do Portao B '
 'exclui com clareza. Aplicar E7 em B1 seria distorcao, porque o E7 e falha do I5 por o produto ser '
 'artefato de outra natureza, e aqui simplesmente nao ha pipeline de producao. QUESTAO A DECIDIR COM A '
 'PESQUISADORA, registrada tambem em evento proprio no log: "Expert Voice" e coluna convidada de '
 'opiniao periodica da revista Software and Systems Modeling, e o criterio E1 do protocolo (l. 1239) '
 'abrange item "not a complete scientific report, such as an editorial, preface, keynote, tutorial", '
 'hipotese em que a exclusao caberia no Portao A, e nao no B. O item foi triado no Portao A com '
 'PASSOU, de modo que reverte-lo exigiria evento de revisao de decisao. Nao o faco de oficio. ',
 'DECISAO: retido no Portao B, com EVIDENCIA=A_VERIFICAR e CANDIDATO_E10, e com a questao do E1 '
 'submetida a pesquisadora. Ainda que venha a ser excluido, o registro deve ser citado na discussao '
 'metodologica, por propor arcabouco de aferimento comparativo padronizado para o objeto desta revisao.'),

'880_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o artigo propoe arcabouco LLM-SysML de quatro passos — coleta e analise de requisitos, '
 'abstracao de elementos assistida por LLM, implementacao do modelo SysML e avaliacao de desempenho — '
 'para a funcao de protecao de flanco em sistema de controle autonomo de trens. A frase decisiva: '
 '"three SysML models are developed using commercial LLM tools, i.e., USE CASE DIAGRAM, SEQUENCE '
 'DIAGRAM and requirement diagram. Results demonstrate that LLM-SysML offers HIGHER ACCESSIBILITY AND '
 'FEWER FALSE ALARMS COMPARED TO TRADITIONAL MANUAL MODELING APPROACHES." ',
 'DISCUSSAO: a questao SysML resolve-se pela v1 sem esforco: dois dos tres modelos desenvolvidos sao '
 'DIAGRAMA DE CASOS DE USO e DIAGRAMA DE SEQUENCIA, ambos reusados do metamodelo UML e arrolados na '
 'tabela da secao 4.1, restando apenas o diagrama de requisitos como especifico da SysML. Ha, '
 'portanto, componente UML separavel e o B1 passa. B4 passa: o primeiro passo do arcabouco e coleta e '
 'analise de requisitos, entrada textual exemplar. B2 e B3 passam. O I6 esta satisfeito por comparacao '
 'com a modelagem manual, com dois construtos, acessibilidade e taxa de falsos alarmes — este ultimo '
 'incomum e interessante, por medir conteudo espurio no modelo gerado, que e forma de precisao. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Interessa tambem por ser dominio ferroviario critico de '
 'seguranca, fora do nucleo de engenharia de software do corpus.'),

'886_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo e "Towards CLASS DIAGRAM GENERATION FROM USER STORIES Using LLMs". O resumo '
 'aponta a geracao automatica de diagramas de classes UML a partir de HISTORIAS DE USUARIO como '
 'aplicacao promissora, e declara que "the proposed approach is ASSESSED BASED ON KEY METRICS SUCH AS '
 'EASE OF INTEGRATION AND ITS ABILITY TO INTERPRET AMBIGUOUS OR INCOMPLETE REQUIREMENTS". ',
 'DISCUSSAO: os quatro subportoes passam sem residuo, e a entrada — historia de usuario — esta '
 'nomeada expressamente na delimitacao de escopo fixada em 2026-08-16. Duas reservas quanto ao I6. As '
 'metricas citadas sao heterogeneas: facilidade de integracao e atributo da ferramenta, nao qualidade '
 'do diagrama; ja a capacidade de interpretar requisitos ambiguos ou incompletos e, essa sim, '
 'propriedade do conteudo gerado, aparentada da completude. Alem disso, o "Towards" do titulo e o '
 '"takes the first step" do resumo sinalizam trabalho preliminar. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR.'),

'888_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "EVALUATING THE QUALITY OF CLASS DIAGRAMS GENERATED BY GPT-4 MODEL". O resumo '
 'situa a geracao de diagramas de classes a partir de requisitos em linguagem natural e afirma que '
 '"for GPT-4 to gain traction within requirements engineering, THE QUALITY OF ITS CLASS DIAGRAMS IS '
 'ESSENTIAL". O desenho e explicito: "this study evaluates GPT-4\'s class diagrams by COMPARING THEM '
 'TO THOSE CREATED BY EXPERTS AND EXISTING TOOLS, using PRECISION, RECALL, AND F1 MEASURES, which '
 'reveal significant variability. GPT-4\'s precision ranges from 0.61 to 0.88". ',
 'DISCUSSAO: os quatro subportoes passam sem residuo. E o registro que mais literalmente coincide com '
 'o objeto desta revisao: qualidade de UML gerada por LLM e o titulo do artigo. Reune tres elementos '
 'de forca rara: gabarito duplo, de especialistas humanos E de ferramentas preexistentes; metricas '
 'consagradas e comparaveis entre estudos; e relato de VARIABILIDADE com intervalo numerico, que '
 'permite discutir estabilidade e nao apenas media. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Prioridade maxima na fila de extracao.'),

'894_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR;CANDIDATO_E10',
 'EVIDENCIA: relato de arcabouco educacional apoiado por IA para ensino de arquitetura de software e '
 'prototipagem em sistemas embarcados, na Universidade de Genova. O curso integra tecnicas basicas de '
 'modelagem — "UML diagrams, finite state machines and communication protocols" — a ferramentas locais '
 'de IA generativa, e a integracao "is CENTRED ON FACILITATING THE GENERATION OF UML DIAGRAMS, '
 'component design, code development, and debugging, with a focus on transparency and critical '
 'evaluation". Os resultados empiricos relatados sao "increased DEVELOPMENT SPEED, deeper '
 'ARCHITECTURAL REASONING, and improved ENGAGEMENT". ',
 'DISCUSSAO: B2, B3 e B4 passam: a IA generativa gera os diagramas, a direcao e de producao e o curso '
 'parte de requisitos ("From Requirements to Prototyping", no titulo). O B1 e limitrofe mas passa, '
 'porque a UML e nomeada diretamente e nao por comparacao, ainda que nenhum tipo de diagrama seja '
 'especificado. As reservas sao duas e recaem sobre o I6 e o E10: os desfechos medidos sao '
 'EDUCACIONAIS — velocidade, raciocinio e engajamento —, nao propriedades do conteudo UML gerado; e a '
 'geracao de diagramas aparece amalgamada a projeto de componentes, desenvolvimento e depuracao, o que '
 'pode impedir separar o resultado referente a UML. Pela regra de ouro 2, a ausencia de vocabulario de '
 'qualidade nunca exclui nesta etapa. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR e CANDIDATO_E10.'),

# ---------------- B1: a saida nao e conteudo UML ----------------
'874_SCOPUS':('B1_E7','',
 'EVIDENCIA: o artigo trata do processamento e da analise de grandes volumes de textos heterogeneos em '
 'linguagem natural para IDENTIFICACAO DE ROBOS EM REDES SOCIAIS, por aprendizado profundo por '
 'transferencia, com discussao de redes neurais artificiais e aprendizado de maquina para automatizar '
 'a analise de usuarios. Palavras-chave autorais: grandes volumes de dados, deteccao de robos, analise '
 'de dados, mineracao de dados, LLMs e redes neurais. Nao ha uma unica mencao a UML em qualquer parte '
 'do resumo, do titulo ou das palavras-chave autorais. ',
 'DISCUSSAO: o B1 resolve o caso. Nao ha producao, transformacao, reparo nem revisao de conteudo UML: '
 'o produto e classificacao de contas em redes sociais. O registro entrou na busca pela conjuncao de '
 'termos genericos de modelagem e de LLM, sem relacao com o objeto da revisao. Pela regra de ouro 3, o '
 'criterio primario e o primeiro portao que explica o caso com clareza. ',
 'DECISAO: excluido por E7 no subportao B1.'),

'887_SCOPUS':('B1_E7','',
 'EVIDENCIA: o sistema e uma extensao de navegador com IA para assistir a navegacao no console de '
 'gestao da Amazon AWS, com LLMs ajustados no AWS Bedrock que oferecem orientacao passo a passo '
 'sensivel ao contexto do dominio. O artigo contrasta ajuste fino e geracao aumentada por recuperacao. '
 'Palavras-chave autorais: aumento de interface guiado por atencao, inferencia de padrao bem '
 'arquitetado da AWS, analise de intencao intermodal, mitigacao de alucinacao, destilacao de '
 'conhecimento procedimental, travessia de fibra do React e DOM sombra. Nenhuma mencao a UML. ',
 'DISCUSSAO: o B1 resolve o caso. O produto e orientacao textual ao usuario e aumento de interface, '
 'nao conteudo UML. Nao ha producao, transformacao, reparo nem revisao de diagrama. Falso positivo por '
 'vocabulario generico de arquitetura e de modelo. ',
 'DECISAO: excluido por E7 no subportao B1.'),

'895_SCOPUS':('B1_E7','',
 'EVIDENCIA: o artigo examina o papel do ChatGPT na geracao de MAPAS CONCEITUAIS para a educacao, '
 'situando os LLMs no enriquecimento da experiencia de aprendizagem e no apoio personalizado a '
 'estudantes. Palavras-chave autorais: mapas conceituais, tecnologias educacionais e LLMs. ',
 'DISCUSSAO: o B1 resolve o caso. O mapa conceitual e notacao de representacao de conhecimento oriunda '
 'da psicologia da aprendizagem, com nos de conceito e arcos rotulados por frases de ligacao; nao e '
 'tipo de diagrama da UML, nao consta da tabela da secao 4.1 e nao tem metamodelo OMG. Ha, portanto, '
 'geracao de diagrama por LLM a partir de texto, mas em notacao alheia — o mesmo caso de 759_SCOPUS, '
 'que usava PlantUML para arvore de falhas, e de 781_SCOPUS. Falha o I5. ',
 'DECISAO: excluido por E7 no subportao B1. Armadilha lexical de notacao vizinha, ja recorrente no '
 'corpus.'),

# ---------------- B2: a origem do conteudo UML nao e LLM substantivo ----------------
'864_SCOPUS':('B2_E6','',
 'EVIDENCIA: estudo de desenvolvimento de servico de saude inteligente para adolescentes, pais e '
 'professores de saude escolar, por abordagem de projeto centrado no usuario, com avaliacao de '
 'necessidades (revisao de 65 estudos, inquerito com 96 participantes e 30 entrevistas) e avaliacao de '
 'usabilidade com 76 participantes. A frase decisiva quanto a autoria do modelo: "WE CREATED A USE '
 'CASE DIAGRAM illustrating the interaction between various users and the services, a flowchart '
 'outlining the service algorithm, and a lifelog data collection system". A IA generativa aparece '
 'apenas como descritor MeSH indexado ("Generative Artificial Intelligence"), ao lado de Adolescent, '
 'Female, Humans e Male, e o que o servico usa sao robos de conversa. ',
 'DISCUSSAO: ha conteudo UML autoral, o que afasta o B1. O B2 resolve: o sujeito do verbo criar e a '
 'primeira pessoa do plural, isto e, os pesquisadores, e o robo de conversa e COMPONENTE DO SERVICO '
 'PROJETADO, sem autoridade semantica alguma sobre atores ou casos de uso. Falha o I2 quanto a origem. '
 'Padrao ja registrado em 790, 814 e 960. Registre-se ainda a armadilha de indexacao: o descritor MeSH '
 'de IA generativa e vocabulario controlado atribuido pelo indexador, e nao declaracao dos autores — '
 'variante, em base biomedica, do fenomeno ja documentado para os descritores do IEEE Xplore. ',
 'DECISAO: excluido por E6 no subportao B2.'),

'875_SCOPUS':('B2_E6','',
 'EVIDENCIA: estudo juridico sobre responsabilidade penal pelo uso criminoso de tecnologia de '
 'falsificacao profunda. O resumo enumera os metodos empregados pelos AUTORES: "using classification, '
 'topology building, cross-impact analysis, judicial content analysis, regression, scenario modeling, '
 'and UML FORMALIZATION, the study shows that automation, diffusion, and institutional targeting drive '
 'the most severe outcomes". A IA generativa aparece na primeira oracao como causa do fenomeno '
 'estudado: "Generative AI has accelerated deepfake crime". ',
 'DISCUSSAO: ha formalizacao em UML, o que afasta o B1, e ela e conduzida pelos proprios '
 'pesquisadores, como um entre sete metodos de analise juridica. O B2 resolve: a IA generativa e o '
 'OBJETO DO ESTUDO — a tecnologia cuja criminalizacao se discute — e nao o agente modelador. Nenhum '
 'LLM tem autoridade semantica sobre elemento UML algum. Falha o I2 quanto a origem. Mesmo padrao de '
 '768, 804 e 844, em que o sistema de IA e o objeto modelado. ',
 'DECISAO: excluido por E6 no subportao B2.'),

# ---------------- B3: direcao invertida ----------------
'882_SCOPUS':('B3_E7','',
 'EVIDENCIA: o titulo declara a direcao sem ambiguidade — "Harnessing ChatGPT for MODEL TRANSFORMATION '
 'in Software Architecture: FROM UML STATE DIAGRAMS TO REBECA MODELS for Formal Verification". O '
 'resumo explica que a UML tem semantica formalizada, mas nao foi concebida para verificacao de '
 'modelos, ao passo que Rebeca, linguagem de modelagem baseada em atores, permite a verificacao formal '
 'de sistemas reativos concorrentes. Palavra-chave autoral: "Unified Modeling Language (UML) state '
 'diagram". ',
 'DISCUSSAO: B1 e B2 passam, pois ha conteudo UML e o ChatGPT e substantivo. O B3 resolve: o diagrama '
 'de estados UML e INSUMO, ja existe e nao e alterado, e o produto e um modelo Rebeca, artefato de '
 'outra linguagem, destinado a verificacao formal. Falha o I5, que exige conteudo UML na SAIDA. Cabe '
 'notar que a matriz da secao 4.3 arrola codigo, testes e documentacao como produtos que levam a E7; a '
 'transformacao para outra linguagem formal de modelagem nao esta nomeada, mas e da mesma especie, '
 'pois o que a caracteriza e a UML ser consumida e nao produzida. Nao e caso de E8, porque nao ha '
 'avaliacao nem explicacao do diagrama, e sim transformacao dele em outro artefato. ',
 'DECISAO: excluido por E7 no subportao B3.'),

'884_SCOPUS':('B3_E7','',
 'EVIDENCIA: abordagem de desenvolvimento agil dirigido por modelos que usa o GPT-4 para gerar codigo. '
 'O resumo e explicito quanto a autoria e a direcao: "in the first and second layer of our proposed '
 'approach, WE MODELLED the structural and behavioural aspects of the case-study USING UML", '
 'acrescentando OCL e ontologia FIPA como restricoes de metamodelagem, e "ultimately, GPT-4 IS USED TO '
 'AUTO-GENERATE CODE FROM THE MODEL in both Java and Python". A avaliacao final incide sobre o CODIGO '
 'gerado, com alinhamento ao diagrama de sequencia esperado e comparacao de complexidade ciclomatica. ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve: os diagramas UML sao construidos pelos PESQUISADORES nas '
 'duas primeiras camadas, ja existem quando o GPT-4 entra em cena, e o produto e codigo Java e Python. '
 'Celula UML existente -> LLM -> codigo da matriz da secao 4.3, que fixa E7. Falha o I5. Note-se que a '
 'complexidade ciclomatica medida e do codigo, nao do modelo. PUBLICACAO REDUNDANTE: este registro e '
 'versao anterior de 770_SCOPUS ("LLM as a Code Generator in Agile Model Driven Development"), ja '
 'excluido como B3_E7. Mesmos autores, mesmo estudo de caso da frota de veiculos nao tripulados, '
 'mesmas restricoes OCL e FIPA, mesmos arcaboucos JADE e PADE, mesma conclusao sobre complexidade '
 'ciclomatica sob metamodelo restringido por ontologia; 884 e a versao de congresso de 2024 e 770 a '
 'versao estendida de 2026. O vinculo nao altera desfecho algum, ja que ambos saem pelo mesmo '
 'criterio, mas fica registrado para a contagem PRISMA e submetido a pesquisadora, a quem cabe decidir '
 'se convem preencher duplicate_group e duplicate_role. ',
 'DECISAO: excluido por E7 no subportao B3, com nota de publicacao redundante em relacao a 770_SCOPUS.'),

'891_SCOPUS':('B3_E8','',
 'EVIDENCIA: o estudo investiga "the capacity of a large language model to GENERATE FORMATIVE FEEDBACK '
 'FOR STUDENT-CREATED UML DIAGRAMS in a university software engineering course". O desenho e robusto: '
 'duas coortes, N = 262, com comparacao entre realimentacao gerada por IA, gerada pelo professor e '
 'ausencia de realimentacao, analisando percepcoes dos estudantes, resultados de aprendizagem e '
 'FIDEDIGNIDADE DA AVALIACAO. ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve: os diagramas sao criados pelos ESTUDANTES, o LLM produz '
 'realimentacao formativa a respeito deles e nada no conteudo UML e alterado — condicao restritiva do '
 'E8 plenamente satisfeita. Aplica-se a tabela da secao 4.2: "LLM apenas avalia ou explica um diagrama '
 'ja existente -> E8". Falha o I3. Registre-se que os desfechos medidos sao educacionais e '
 'psicometricos, e nao propriedades do conteudo UML, o que confirma o desfecho por segunda via. ',
 'DECISAO: excluido por E8 no subportao B3. Integra o agrupamento de realimentacao e avaliacao '
 'automatizada em contexto educacional, e e o de maior porte amostral encontrado ate aqui.'),

'896_SCOPUS':('B3_E8','',
 'EVIDENCIA: o estudo introduz abordagem de andaimagem apoiada por IA para aprimorar a aprendizagem de '
 'modelagem de software por meio de diagramas UML, concentrando-se em definir os principios e as '
 'funcoes que compoem a andaimagem. A frase decisiva quanto ao escopo do que foi implementado: "we '
 'present the initial implementation of the scaffolding, SPECIFICALLY HIGHLIGHTING THE FEEDBACK '
 'FUNCTION". ',
 'DISCUSSAO: B1 e B2 passam. O B3 resolve: a unica funcao efetivamente implementada e a de '
 'REALIMENTACAO sobre a modelagem do estudante, e a andaimagem, por definicao pedagogica, apoia o '
 'aprendiz a produzir, sem produzir por ele. Nao ha producao, transformacao, reparo nem revisao de '
 'conteudo UML pela IA, e o diagrama do estudante nao e alterado — condicao restritiva do E8 '
 'satisfeita. Falha o I3. ',
 'DECISAO: excluido por E8 no subportao B3. Integra o agrupamento de realimentacao automatizada para '
 'ensino de modelagem.'),

# ---------------- B4: a entrada nao e especificacao textual ----------------
'865_SCOPUS':('B4_E9','',
 'EVIDENCIA: o titulo e "Using Large Language Models to EXTRACT UML CLASS DIAGRAMS FROM JAVA '
 'PROGRAMS". O resumo situa o trabalho na modernizacao de sistemas legados e declara que "REVERSE '
 'ENGINEERING is used to extract different representations of software systems, and the model-driven '
 'engineering approach can be used to assist the reverse engineering process, leading to MODEL-DRIVEN '
 'REVERSE ENGINEERING (MDRE)". Palavras-chave autorais: diagrama de classes, programas Java, LLMs, '
 'sistemas legados e MDRE. ',
 'DISCUSSAO: B1, B2 e B3 passam sem qualquer atrito — ha diagrama de classes na saida, o LLM e o '
 'agente gerador e a direcao e de producao. O caso se decide inteiramente no B4: a entrada e '
 'CODIGO-FONTE JAVA, declarada de modo expresso ja no titulo, sem componente textual de requisitos, o '
 'que satisfaz a condicao restritiva do E9. A delimitacao de escopo fixada em 2026-08-16 exclui '
 'nominalmente a engenharia reversa a partir de codigo-fonte, ainda que haja metrica explicita de '
 'qualidade sobre a UML gerada. Falha o I4. ',
 'DECISAO: excluido por E9 no subportao B4. Exclusao onerosa e consciente, do mesmo tipo de 819 e 820: '
 'o registro fica NOMEADO para recuperacao sem re-triagem caso o I4 venha a ser emendado, por ser um '
 'dos casos mais limpos de engenharia reversa por LLM com diagrama de classes como produto.'),
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
     'Quinto lote de leitura individual dos registros que mencionam UML no titulo ou no resumo: 24 '
     'registros triados, indices 96 a 119 da lista. Desfechos: 14 RETIDOS, 3 E7 em B1, 2 E6 em B2, 2 '
     'E7 em B3, 2 E8 em B3 e 1 E9 em B4. Candidatos centrais: 888_SCOPUS (avalia a qualidade de '
     'diagramas de classes do GPT-4 contra gabarito DUPLO, de especialistas e de ferramentas, com '
     'precisao, revocacao e F1, e relata variabilidade com intervalo numerico — e o registro que mais '
     'literalmente coincide com o objeto da revisao), 876_SCOPUS (UCD-LLM, com conjunto proprio '
     'ReqUCD60, linhas de base tradicionais e por LLM, estudos de ablacao e codigo publico) e '
     '866_SCOPUS, 880_SCOPUS e 867_SCOPUS. Cinco achados. (1) A questao SysML consolidou-se: em '
     '866_SCOPUS (diagrama de atividade, com "block definition diagram" da v1) e em 880_SCOPUS '
     '(diagrama de casos de uso e de sequencia), ambos com componente UML separavel e ambos retidos, '
     'confirmando o criterio ja aplicado em 812_SCOPUS. (2) Amplia-se a diversidade de DOMINIO entre '
     'os retidos, ate aqui concentrados em engenharia de software: 867_SCOPUS e projeto de sistemas de '
     'aeronaves e 880_SCOPUS e controle autonomo de trens, dominio critico de seguranca. (3) '
     '867_SCOPUS traz FAMILIA NOVA DE EVIDENCIA DE QUALIDADE: em vez de comparar o artefato a um '
     'gabarito, trata a correcao como variavel aleatoria e estima a PROBABILIDADE DE RESULTADO '
     'CORRETO sob repeticao, atacando o nao determinismo do LLM. Merece registro proprio na taxonomia '
     'de metricas da sintese. (4) PUBLICACAO REDUNDANTE detectada: 884_SCOPUS ("Coding by Design: '
     'GPT-4 Empowers Agile Model Driven Development", congresso, 2024) e 770_SCOPUS ("LLM as a Code '
     'Generator in Agile Model Driven Development", capitulo Springer, 2026) relatam o MESMO estudo — '
     'mesmos autores, mesmo caso da frota de veiculos nao tripulados, mesmas restricoes OCL e FIPA, '
     'mesmos arcaboucos JADE e PADE, mesma conclusao sobre complexidade ciclomatica. Ambos ja saiam '
     'por B3_E7, de modo que o desfecho nao muda; submete-se a pesquisadora se convem preencher '
     'duplicate_group e duplicate_role. Ha ainda suspeita de FAMILIA de publicacoes fatiadas entre os '
     'RETIDOS 818, 848, 868, 869 e 877, que compartilham a sigla UMLCode, o pipeline de dois LLMs e a '
     'validacao multimodal por modelos de visao e linguagem, e que 877 confirma ao dizer "extends OUR '
     'framework" — a resolver na leitura integral, elegendo-se o relato mais completo. (5) 872_SCOPUS '
     'e o TERCEIRO registro travado pela questao de protocolo da OCL, ao lado de 758_SCOPUS e '
     '518_IEEE, o que torna a fixacao dessa fronteira condicao previa da extracao. Registre-se por fim '
     'que 895_SCOPUS gera MAPAS CONCEITUAIS, notacao vizinha e nao UML, e sai por E7 em B1, engrossando '
     'o padrao de 759 (arvore de falhas) e 781 (diagrama de componentes em acepcao de neurociencia).',
     'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'])
    w.writerow(['879_SCOPUS',AGORA,REV,'QUESTAO_PROTOCOLO','A','','',
     'QUESTAO SUBMETIDA A PESQUISADORA, nao decidida de oficio. 879_SCOPUS ("Towards standarized '
     'benchmarks of LLMs in software modeling tasks: a conceptual framework") declara no proprio '
     'resumo ser um "EXPERT VOICE", que e coluna convidada de opiniao da revista Software and Systems '
     'Modeling. O criterio E1 do protocolo (l. 1239) abrange item que "is not a complete scientific '
     'report, such as an editorial, preface, keynote, tutorial, slide deck, poster-only item...", '
     'hipotese em que a exclusao caberia no PORTAO A, e nao no B. O registro foi triado no Portao A com '
     'PASSOU, e reverte-lo exigiria evento de revisao de decisao; por isso foi apenas RETIDO no Portao '
     'B, com CANDIDATO_E10. Argumento em sentido contrario: o texto propoe arcabouco conceitual de '
     'aferimento comparativo padronizado para avaliar a qualidade de modelos gerados por LLM, isto e, '
     'toca o nucleo tematico desta revisao, e ainda que excluido merece citacao na discussao '
     'metodologica. Decisao pendente.',
     'protocol/appendix_two_layer_mapping_protocol_v1_7.tex l. 1239'])

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
