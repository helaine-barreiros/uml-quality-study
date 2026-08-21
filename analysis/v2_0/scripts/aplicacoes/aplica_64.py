import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: leitura do titulo, do resumo e das palavras-chave no CSV da busca automatizada, '
     'aplicando screening_manual_v1.md na ordem do Portao B. Este registro veio do subconjunto de 64 '
     'que, embora sem mencao literal a UML, traziam termo de modelagem capaz de encobrir UML por outro '
     'nome, e por isso foi lido individualmente em vez de entrar no lote de 320. ')
DISC7=('DISCUSSAO: verificado que o termo de modelagem nao resgata o registro. ')
FIM7=('O B1 decide, portanto, e os subportoes seguintes nao sao alcancados. Pela regra de ouro 5, a '
      'falha e de saida (I5/E7). Pela regra de ouro 3, o B1 e o primeiro portao que explica claramente '
      'o caso. DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. ')

# 43 exclusoes em B1 — razao especifica pela qual o termo suspeito nao resgata
E7={
'015_ACM':'O artefato produzido e a arvore de ataque-defesa, extensao de arvore de ataque usada por engenheiros de seguranca. Nao e notacao UML e nao ha componente UML separavel; o TTool-AI opera sobre arvores, nao sobre diagramas do metamodelo UML.',
'046_ACM':'O objeto e a qualidade de especificacoes algebricas geradas por LLM em AMPL, uma DSL de otimizacao matematica, comparada a codigo Python. O termo model-driven engineering situa o contexto, mas o artefato avaliado e codigo AMPL.',
'050_ACM':'O termo conceptual model aparece no sentido de conceitos biomedicos, nao de modelo conceitual de software. O artefato produzido e sumario extrativo de literatura PubMed.',
'059_ACM':'O artefato produzido sao casos de teste e codigo executavel para protocolos de rede. O termo model-driven nao corresponde a producao de modelo algum.',
'077_ACM':'O artefato produzido sao planos de aula. O metamodelo citado caracteriza a metodologia de ensino e serve de base para a ferramenta; nao e modelo UML nem e gerado pelo LLM como objeto de avaliacao. O MDE aqui e o ASSUNTO ensinado, nao a tecnica empregada.',
'080_ACM':'Os diagramas do Graphologue sao grafos interativos de no e aresta construidos a partir de respostas textuais do LLM para facilitar a leitura. Nao ha notacao de modelagem de software.',
'086_ACM':'O artefato produzido e codigo, a partir de requisitos e de documento de arquitetura. O documento arquitetural e ENTRADA e nao produto, e as metricas reportadas sao de conformidade arquitetural e corretude funcional do codigo.',
'091_ACM':'O artefato produzido sao Machine-readable Action Trees, arvores de acao legiveis por maquina que representam procedimentos clinicos. A mencao a model-driven engineering descreve o consumo posterior desses artefatos, nao a producao de UML.',
'101_ACM':'O artefato produzido sao automatos de protocolo extraidos de RFCs, isto e, maquinas de estado finito no sentido da teoria de automatos e nao diagramas de maquina de estados do metamodelo UML. Considerei a proximidade entre os dois conceitos e concluo que o resumo nao autoriza tratar o automato de protocolo como artefato UML.',
'106_ACM':'O artefato produzido sao microsservicos nativos de nuvem implantaveis, ou seja, codigo e artefatos de implantacao, a partir de requisitos. O Architect Agent decompoe servicos, mas nada no resumo indica producao de diagrama.',
'121_ACM':'O artefato produzido sao consultas em VQL, uma linguagem de consulta de modelos. Consulta nao e modelo; o contexto MDE nao torna a saida UML.',
'128_ACM':'O termo model refere-se ao proprio LLM e a distribuicao de carga entre CPU e GPU na inferencia. Nao ha artefato de modelagem de software em ponto algum.',
'136_ACM':'O artefato produzido e codigo. Os diagramas sao ENTRADA do benchmark, codificando o contexto do problema, e nao ha indicacao de que sejam UML.',
'146_ACM':'A maquina de estados finitos governa a emulacao de protocolo do honeypot em tempo de execucao. E componente de implementacao, nao artefato de modelagem produzido e avaliado.',
'154_ACM':'A notacao e AADL, Architecture Analysis and Design Language, notacao propria de sistemas ciberfisicos criticos e distinta da UML. Nao ha componente UML separavel.',
'161_ACM':'O artefato produzido e um modelo verificavel por maquina em Verus, consumido por solucionadores SMT. E modelo formal de verificacao, nao UML. Alem disso nao ha LLM: o Scope combina modelagem formal com verificacao de consistencia baseada em regras.',
'169_ACM':'Os modelos produzidos sao gemeos digitais executaveis baseados em simulacao de sistemas de manufatura, construidos pelo FactoryFlow. A modelagem estrutural citada descreve componentes de simulacao, nao diagramas UML.',
'174_ACM':'O artefato produzido e codigo. O termo structural modeling descreve a arquitetura interna do CodeForge-Q, com transformers enriquecidos por grafo, nao um artefato de modelagem produzido.',
'182_ACM':'O artefato produzido e a sintaxe concreta grafica de linguagens de modelagem especificas de dominio. Gerar a NOTACAO de uma DSML e distinto de gerar um modelo UML; a UML tem sintaxe concreta fixada pelo padrao OMG.',
'196_ACM':'O artefato produzido sao aplicacoes em plataformas de baixo codigo cuja camada de modelagem usa DSLs proprietarias. Nenhuma dessas DSLs e UML nem ha componente UML separavel.',
'222_ACM':'O artefato produzido sao artefatos de linguagem — sintaxe, semantica e ambientes de apoio — de linguagens de modelagem especificas de dominio. Construir uma DSML e distinto de produzir um modelo UML.',
'226_ACM':'A arquitetura hierarquica de agentes e componente de implementacao do sistema de interpretacao de politicas de educacao profissional. Nao ha artefato de modelagem de software produzido nem avaliado.',
'255_ACM':'Os domain models do DoME sao explicitamente tabelas de banco de dados com atributos e relacionamentos, evoluidas por operacoes CRUD em tempo de execucao. Nao sao diagramas UML. Registro que o registro tambem falharia no B2, pois a tecnica declarada e processamento de linguagem natural com autoadaptacao, sem LLM.',
'290_ACM':'O objeto do trabalho e o ensino de plataformas de baixo codigo e o artefato produzido pelos estudantes e uma aplicacao web. A mencao a common modeling languages descreve etapa preparatoria do exercicio didatico, sem que qualquer modelo seja produzido por LLM ou avaliado.',
'329_ACM':'O artefato produzido sao casos de garantia baseados em argumento para equidade de sistemas de IA, com coleta de evidencia justificada. Nao ha notacao de modelagem de software.',
'363_ACM':'Os artefatos sao esbocos informais mantidos em sincronia bidirecional com o codigo. O proprio resumo os qualifica como informais e os opoe a representacoes formais; nao ha notacao UML.',
'364_ACM':'O estudo caracteriza agentes de codificacao ao longo do ciclo de vida de pull requests, analisando 29.585 ciclos por taxonomia de iniciador e aprovador. Nao ha artefato de modelagem.',
'490_IEEE':'A notacao produzida e CMMN, Case Management Model and Notation, padrao OMG distinto da UML e voltado a gestao de casos. Nao ha componente UML separavel. Registro que, fosse a saida UML, o registro seria forte candidato a inclusao: a entrada sao cenarios em linguagem natural e ha avaliacao comparativa de quatro estrategias de prompt.',
'514_IEEE':'A direcao e inversa e a saida e texto: o trabalho gera descricao textual de fluxogramas complexos por decomposicao RPST. Alem disso o fluxograma nao e notacao UML, conforme a tabela da secao 4.1 do manual.',
'585_IEEE':'O trabalho e de comunicacoes sem fio, sobre probabilidade de indisponibilidade com desvanecimento Beaulieu-Xie. A IA generativa aparece como prova de conceito para reduzir carga cognitiva em experimentacao de rede. Nao ha artefato de modelagem de software.',
'587_IEEE':'O artefato produzido sao asserções SystemVerilog para verificacao de hardware. Os diagramas sao ENTRADA multimodal da especificacao, e nao ha indicacao de que sejam UML.',
'599_IEEE':'O trabalho avalia respostas do ChatGPT a questionarios, listas e laboratorios de um curso introdutorio de engenharia da computacao. O artefato produzido sao respostas.',
'621_IEEE':'O artefato produzido sao testes funcionais. A logica de estados citada e principio de teste a ser respeitado, nao diagrama produzido; e o processo de negocio nao e notacao UML.',
'634_IEEE':'A notacao e Object-Process Methodology, ISO 19450, com Object-Process Diagrams e Object-Process Language. E notacao unificadora distinta da UML e nao ha componente UML separavel. Registro que o resumo tampouco apresenta LLM, o que o levaria a E6 no B2.',
'641_IEEE':'O trabalho e de comunicacoes sem fio, sobre probabilidade media de erro de bit com desvanecimento Rician. A IA generativa e explorada acessoriamente. Nao ha artefato de modelagem de software.',
'713_IEEE':'A notacao produzida e PDEVS, Parallel Discrete Event System Specification, formalismo de simulacao de eventos discretos. Os statecharts citados sao statecharts PDEVS, construto proprio do formalismo com gramatica propria, e nao diagramas de maquina de estados do metamodelo UML. Considerei a proximidade historica entre statecharts de Harel e a UML e concluo que o resumo ancora o trabalho de forma consistente no DEVS.',
'729_IEEE':'O artefato produzido sao respostas a 120 questoes curadas sobre documentos de padronizacao em telecomunicacoes. Os diagramas embutidos nesses documentos sao ENTRADA e nao ha indicacao de que sejam UML.',
'732_IEEE':'O artefato extraido sao semanticas de maquinas de estado finitos para sintese de controle e geracao de HDL, no contexto de ferramentas de projeto assistido por computador. FSM aqui e abstracao de projeto digital, nao diagrama do metamodelo UML, e os diagramas sao entrada.',
'816_SCOPUS':'O artefato produzido e codigo Verilog para automacao de projeto de hardware. Nao ha artefato de modelagem de software.',
'855_SCOPUS':'O artefato produzido sao consultas estruturadas sobre grafos de conhecimento. O agentic state diagram e componente interno da interface que contextualiza o estado do agente, nao um modelo produzido e avaliado.',
'860_SCOPUS':'O artefato e um sistema de dialogo que transmite informacao sobre automatos finitos a pessoas com deficiencia visual. Os diagramas de estado sao a representacao tradicional que o trabalho quer SUBSTITUIR por dialogo, e sao automatos finitos da teoria da computacao, nao UML.',
'883_SCOPUS':'O trabalho compara ChatGPT e DeepSeek em aconselhamento genetico oncologico, com escalas validadas de qualidade informacional. Nao ha artefato de modelagem de software.',
'946_SCOPUS':'A notacao e TLA+, linguagem de especificacao formal para verificacao de modelos. O visualizador de diagrama de estados citado exibe grafos de transicao de estados do TLA+, nao diagramas UML.',
}

# 3 decisoes no B3
B3={
'137_ACM':('B3_E8','INCERTO_SAIDA',
 'EVIDENCIA: o resumo investiga a viabilidade de usar LLMs para automatizar a avaliacao da qualidade de '
 'diagramas de arquitetura de software. Propoe prompting estruturado que guia o ChatGPT-4o a "evaluate '
 'architectural diagrams against five established quality criteria", aplicado a diagramas de quatro '
 'artigos da trilha de ferramentas do SBES 2024, com revisao das avaliacoes por especialista. ',
 'DISCUSSAO: o B1 nao decide. A tabela da secao 4.1 do manual e explicita em que "architecture diagram" '
 'nao conta sozinho como UML, mas os diagramas vem de artigos de ferramentas de engenharia de software '
 'e poderiam ser diagramas de componentes ou de implantacao; afirmar o contrario seria atribuir ao '
 'resumo o que ele nao diz. E o terceiro caso do B1, que manda reter com INCERTO_SAIDA e seguir. O B3 '
 'decide sem depender dessa duvida: qualquer que seja a notacao, o diagrama e INSUMO e o produto do LLM '
 'e uma avaliacao de qualidade. E o segundo caso do B3, confirmado pela matriz da secao 4.3. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. Registro que o tema — avaliacao automatica '
 'de qualidade de diagrama por LLM — e proximo do interesse da revisao, mas a revisao investiga a '
 'qualidade da UML GERADA por LLM, e aqui o LLM e o avaliador e nao o gerador. Mantida a flag '
 'INCERTO_SAIDA: a duvida sobre a notacao nao foi resolvida, apenas tornou-se irrelevante. '),
'612_IEEE':('B3_E8','INCERTO_SAIDA',
 'EVIDENCIA: o resumo investiga duas abordagens para responder perguntas sobre modelos de software '
 'automotivos: prompting direto, com o modelo inteiro no contexto, e abordagem agentica com agentes LLM '
 'e ferramentas de acesso a arquivos. A avaliacao usa um metamodelo Ecore. ',
 'DISCUSSAO: o B1 nao decide. A tabela da secao 4.1 admite Ecore "quando destinado a codificar UML", e '
 'o resumo nao informa se o metamodelo automotivo o faz — terceiro caso do B1, reter com INCERTO_SAIDA. '
 'O B3 decide independentemente disso: o modelo e INSUMO da consulta e o produto sao respostas em '
 'linguagem natural. E o segundo caso do B3. Nenhum conteudo de modelo e produzido ou alterado. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. Mantida a flag INCERTO_SAIDA. '),
'554_IEEE':('B3_E7','INCERTO_SAIDA',
 'EVIDENCIA: o resumo apresenta abordagem que usa LLMs para o reconhecimento de diagramas de estado '
 'embutidos em especificacoes, a fim de gerar automaticamente codigo e testes unitarios, no contexto da '
 'Industria 4.0. Compara o desempenho dos LLMs com modelos tradicionais de visao computacional e '
 'reporta resultados sobre os protocolos PROFINET e OPC UA. ',
 'DISCUSSAO: o B1 nao decide, porque o resumo diz "state diagrams" sem informar se sao diagramas de '
 'maquina de estados do metamodelo UML ou maquinas de estado de protocolo industrial — terceiro caso, '
 'reter com INCERTO_SAIDA. O B3 decide: os diagramas sao INSUMO, reconhecidos a partir da '
 'especificacao, e o produto sao codigo e testes unitarios. E o terceiro caso do B3, "UML existente --> '
 'LLM --> codigo, testes, documentacao", confirmado pela matriz da secao 4.3. Registra-se B3_E7 e nao '
 'B1_E7 porque havia diagrama em jogo, so que na entrada. Considerei o E9, pois os diagramas entram '
 'como imagem, mas o B3 antecede o B4. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B3. Direcao inversa a investigada. '),
}

# 18 retencoes
RET={
'027_ACM':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','estudo que avalia a utilidade de LLMs com few-shot prompt learning para assistir a modelagem de dominio em contexto de MDE, oferecendo recomendacoes a modeladores','o artefato e chamado de "domain model" sem que a notacao seja nomeada. Em MDE, modelo de dominio e tipicamente diagrama de classes UML, mas o resumo nao o afirma','os modelos de dominio avaliados sao diagramas de classes UML? Ha metrica de qualidade sobre os elementos recomendados?'),
'061_ACM':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','arcabouco multi-etapa para geracao totalmente automatizada de modelos de dominio com LLMs, motivado por elementos faltantes e padroes avancados ausentes na abordagem anterior de etapa unica','a notacao do modelo de dominio nao e nomeada, embora o resumo fale em conceitos, relacionamentos e padroes avancados — vocabulario compativel com diagrama de classes','a notacao e UML? Quais elementos faltantes e padroes avancados sao medidos, e como?'),
'138_ACM':('INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR','artigo de visao que propoe metodo para gerar semiautomaticamente modelos de dominio e arquiteturas de software a partir de requisitos, gerando e avaliando multiplos candidatos em vez de um so','ha requisitos como entrada e modelo de dominio como saida, o padrao que a revisao investiga, mas a notacao nao e nomeada e o artigo e de visao','a notacao dos modelos de dominio gerados e UML? Sendo artigo de visao, ha avaliacao empirica ou apenas proposta? A segunda hipotese levaria a E1 ou E11 no texto completo.'),
'141_ACM':('INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR','visao de engenharia low-code caixa-branca em que o desenvolvedor cidadao especifica modelos de dominio semiformalmente, anexando restricoes e operacoes como anotacoes em linguagem natural','ha modelo de dominio com restricoes e operacoes, estrutura analoga a classe UML com OCL, mas nenhuma notacao e nomeada','a camada de modelo e UML? As anotacoes viram restricoes OCL? Ha avaliacao empirica ou e apenas visao?'),
'221_ACM':('INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR','criacao assistida por IA de modelos de dominio a partir de texto, com foco em explicabilidade e rastreabilidade das decisoes de modelagem','o resumo fala em modelos de dominio criados a partir de texto e cita NLP, ML e avancos recentes com LLMs, sem nomear a notacao nem deixar claro se o LLM tem autoridade semantica','a notacao e UML? O papel e de LLM gerativo ou de NLP e ML classicos, caso em que a RF-01 levaria a E6?'),
'292_ACM':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','metodo de mascaramento de gramatica que restringe a decodificacao do LLM para garantir validade sintatica dos modelos produzidos para uma gramatica livre de contexto','o trabalho e sobre validade SINTATICA de modelos gerados por LLM, exatamente uma das dimensoes de qualidade que a revisao investiga, mas a gramatica alvo nao e nomeada e pode ser de DSL e nao de UML','as gramaticas avaliadas incluem UML ou PlantUML? A medida de validade sintatica e reportada por linguagem?'),
'516_IEEE':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','arcabouco automatizado de geracao de modelos de requisitos a partir de descricoes em linguagem natural de documentos de requisitos de usuario, com prompting zero-shot baseado em ChatGPT, em sistemas embarcados','a entrada e inequivocamente textual e o LLM e nomeado, mas "requirements model" nao identifica a notacao — pode ser diagrama de casos de uso ou de atividade da UML, ou notacao propria de requisitos','que notacao tem o modelo de requisitos gerado? Se for diagrama de casos de uso, de atividade ou de classes, o registro e forte candidato a inclusao.'),
'518_IEEE':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','geracao de restricoes OCL a partir de especificacoes em linguagem natural com LLMs, incluindo coleta de conjunto de dados e fine-tuning','a OCL e linguagem companheira da UML no padrao OMG e suas restricoes se escrevem sobre elementos de um metamodelo, o que o proprio resumo confirma ao citar a exigencia de conhecimento de meta-modelo. Nao e diagrama, porem, e a tabela da secao 4.1 nao a lista','as restricoes OCL geradas sao definidas sobre modelos UML, o que caracterizaria artefato UML-portador, ou sobre metamodelos proprietarios? Esta pergunta e de fronteira e pode exigir decisao explicita sobre o estatuto da OCL no protocolo.'),
'521_IEEE':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','estudo comparativo abrangente de LLMs para modelagem de dominio totalmente automatizada, partindo de descricoes de problema escritas em linguagem natural que engenheiros tipicamente traduzem a mao','a entrada e explicitamente descricao de problema em linguagem natural e ha avaliacao comparativa declarada — o padrao central da revisao. Falta apenas a notacao ser nomeada','a notacao do modelo de dominio e UML, e de que tipo? Que metricas de qualidade sao usadas na comparacao? Este e o registro de leitura mais prioritaria do bloco.'),
'570_IEEE':('INCERTO_SAIDA;CANDIDATO_E10;EVIDENCIA=A_VERIFICAR','catalogo de exemplos de prompt para treinamento em engenharia de software com LLMs abertos como LLaMA e Mistral, mapeado as areas de conhecimento do SWEBoK, cobrindo elicitacao de requisitos, geracao de diagramas, simulacao de API e estimativa de esforco','"diagram generation" aparece como uma capacidade entre varias, sem que o tipo de diagrama seja nomeado nem medido separadamente','os diagramas gerados sao UML? Ha alguma medida de qualidade, ou o artigo apenas cataloga prompts? A flag CANDIDATO_E10 registra que a UML pode nao se separar das demais areas do SWEBoK.'),
'582_IEEE':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','metodo que assiste a especificacao de requisitos para que sejam convertidos semiautomaticamente em diagramas de transicao de estados, com avaliacao por distancia de edicao antes e depois da modificacao e aplicacao do mesmo apoio a LLMs','a direcao e requisitos para diagrama, o padrao correto, e ha metrica objetiva, mas o diagrama de transicao de estados destina-se a aprendizado por reforco e pode ser um automato de MDP e nao um diagrama de maquina de estados UML','os diagramas de transicao de estados sao diagramas de maquina de estados UML? O papel do LLM e gerar o diagrama ou apenas refinar os requisitos, questao que remete ao B2 e a RF-02?'),
'583_IEEE':('INCERTO_SAIDA;CANDIDATO_E10;EVIDENCIA=EXPLICITA','avaliacao da proficiencia do ChatGPT no desenvolvimento de software, com estudo de caso de um sistema de reserva de passeios turisticos, cobrindo analise de requisitos, modelagem de dominio, modelagem de projeto e implementacao','modelagem de dominio e modelagem de projeto sao citadas como fases em que o ChatGPT foi avaliado, o que sugere artefatos de modelagem, mas nenhuma notacao e nomeada e o estudo cobre o ciclo inteiro','que notacao tem os modelos de dominio e de projeto produzidos? Ha avaliacao de qualidade especifica desses modelos, separavel da avaliacao da implementacao? A flag CANDIDATO_E10 registra esse risco.'),
'623_IEEE':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','abordagem de few-shot prompt learning para automatizar a completude em atividades de modelagem de dominio, testada na completude de diagramas de dominio estaticos e dinamicos','a distincao entre diagramas estaticos e dinamicos e a mesma que a UML faz entre diagramas estruturais e comportamentais, o que torna a hipotese UML plausivel, mas a notacao nao e nomeada. A completude de modelo existente e tarefa legitima pelo I3, quarto caso do B3, pois altera o conteudo','os diagramas estaticos e dinamicos sao de classes e de maquina de estados UML? Como a eficacia da completude e medida?'),
'626_IEEE':('INCERTO_SAIDA;INCERTO_ENTRADA;EVIDENCIA=A_VERIFICAR','proposta de combinar IA generativa e engenharia baseada em modelos para automatizar o desenvolvimento de software automotivo, diante do desafio de integracao e validacao em nivel de sistema','ha MBSE declarado e LLMs nomeados, mas o resumo cita analise de requisitos e geracao de codigo como as tarefas automatizadas, sem nomear notacao de modelagem, e MBSE remete a SysML, cuja versao 1 e perfil de UML','a notacao e SysML e, sendo, e v1 ou v2? Ha diagrama do metamodelo UML nomeado? Qual e a entrada do processo?'),
'656_IEEE':('INCERTO_SAIDA;INCERTO_PAPEL_LLM;EVIDENCIA=A_VERIFICAR','trabalho preliminar com estudos de caso iniciais sobre a integracao de IA em MBSE, abrangendo visao computacional e LLMs em avaliacao de arquitetura, criacao de modelos e analise de requisitos','"model creation" com LLM em contexto MBSE e o padrao que interessa, mas o trabalho e preliminar, mistura visao computacional e LLM sem separar os papeis, e nao nomeia a notacao','em qual estudo de caso o LLM cria modelos, e de que notacao? A visao computacional e o LLM atuam sobre as mesmas tarefas? Sendo trabalho preliminar de estudos de caso iniciais, ha avaliacao ou apenas relato?'),
'851_SCOPUS':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','uso de LLMs para estender automaticamente diagramas de estado de seguranca, extraindo propriedades de seguranca de normas de aviacao e ampliando o diagrama basico para habilitar teste de seguranca, com algoritmo genetico na geracao de casos de teste','a extensao de um diagrama existente ALTERA seu conteudo, o que e tarefa legitima pelo I3 e cai no quarto caso do B3, e a entrada — propriedades extraidas de normas — e textual. Falta apenas saber se o diagrama de estados e UML','o diagrama de estado de seguranca e diagrama de maquina de estados UML? A qualidade do diagrama estendido e avaliada, ou so a dos casos de teste dele derivados? Se so os testes forem avaliados, o registro tende a E11 no texto completo.'),
'903_SCOPUS':('INCERTO_ENTRADA;EVIDENCIA=A_VERIFICAR','fluxo de trabalho em tempo de projeto conduzido por LLM para desenvolvimento de sistemas de IoT e gerencia de rede, combinando capacidades generativas e de sumarizacao dos LLMs com o rigor formal da engenharia dirigida por modelos, apoiado em modelos baseados em diagrama de atividade que fornecem semantica formal','o registro NAO deveria ter chegado a este bloco: ele nomeia diagrama de atividade, tipo do metamodelo UML, e escapou da varredura lexical apenas por grafar "activity-diagram" com hifen. Corrigida a leitura, o B1 se resolve pelo primeiro caso e o registro segue. O B2 passa, o LLM e gerativo; o B3 passa, o modelo e produto','qual e a entrada do projeto de topologia assistido por LLM — requisitos textuais, o que mantem o registro no escopo, ou codigo de configuracao, que pela delimitacao de 2026-08-16 levaria a E9? O resumo cita "reasoning about configuration code", o que suscita a segunda hipotese.'),
'932_SCOPUS':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA','estudo exploratorio sobre o alinhamento entre vibe coding e modelos conceituais, motivado por saidas nao deterministas, codigo alucinado, manutenibilidade limitada e conformidade, e apoiado na experiencia de MDE e de low-code sobre o valor de modelos conceituais explicitos','modelo conceitual explicito no contexto de MDE e frequentemente diagrama de classes UML, e ha estudo exploratorio declarado, mas a notacao nao e nomeada e o objeto pode ser o codigo e nao o modelo','os modelos conceituais do estudo sao UML? O que e medido: a qualidade do modelo, a do codigo produzido a partir dele, ou o alinhamento entre ambos?'),
}

assert len(E7)+len(B3)+len(RET)==64, (len(E7),len(B3),len(RET))

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
n=0
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid in E7:
        r[i['gate_b_outcome']]='B1_E7'
        r[i['gate_b_notes']]=MET+'EVIDENCIA E DISCUSSAO: '+E7[lid]+' '+FIM7
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E7'
    elif lid in B3:
        out,flags,ev,disc,dec=B3[lid]
        r[i['gate_b_outcome']]=out; r[i['gate_b_notes']]=MET+ev+disc+dec
        r[i['gate_c_flags']]=flags; r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
        r[i['excluded']]='true'; r[i['exclusion_criteria']]=out.split('_')[-1]
    elif lid in RET:
        flags,oque,porque,pauta=RET[lid]
        r[i['gate_b_outcome']]='PASSOU'
        r[i['gate_b_notes']]=(MET+'EVIDENCIA: o resumo apresenta '+oque+'. '+
          'DISCUSSAO: o B1 nao decide. '+porque[0].upper()+porque[1:]+'. E o terceiro caso do B1, '
          '"resumo nao deixa claro", que manda RETER sinalizando, e nao o segundo, que exigiria que o '
          'resumo declarasse OUTRA notacao — declaracao que ele nao faz. Pela regra de ouro 1, a '
          'incerteza retem: custa uma leitura, e a alternativa custa um estudo perdido. Os subportoes '
          'seguintes foram percorridos sem exclusao. '+
          'DECISAO DA PESQUISADORA: RETIDO para o texto completo. '
          'PERGUNTA QUE O TEXTO COMPLETO PRECISA RESPONDER: '+pauta+' ')
        r[i['gate_c_flags']]=flags; r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
    else:
        continue
    r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    n+=1

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

P='protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow([';'.join(sorted(E7)),AGORA,REV,'DECISAO_GATE','B1','','E7',
     'Quarenta e tres registros excluidos por E7 no B1, apos leitura individual. Vinham do subconjunto '
     'de 64 que, sem mencao literal a UML, traziam termo de modelagem capaz de encobrir UML por outro '
     'nome, e por isso foram retirados do lote automatico de 320. Verificado caso a caso que o termo '
     'nao resgata o registro. Notacoes vizinhas que saem por nao terem componente UML separavel: AADL '
     '(154), CMMN (490), Object-Process Methodology ISO 19450 (634), PDEVS (713), TLA+ (946), AMPL '
     '(046), DSLs de plataformas low-code (196, 222, 182). Automatos finitos da teoria da computacao, '
     'distintos de diagramas de maquina de estados UML: 101, 146, 732, 860. Casos em que o termo '
     '"model" designava outra coisa: 128 (o proprio LLM), 174 (arquitetura interna do arcabouco), 255 '
     '(tabelas de banco de dados), 077 (metamodelo da metodologia de ensino, sendo o MDE o assunto '
     'ensinado e nao a tecnica). Casos em que o diagrama era ENTRADA e o produto era outro artefato: '
     '086, 136, 514, 587, 729.',P])
    w.writerow([';'.join(sorted(B3)),AGORA,REV,'DECISAO_GATE','B3','','',
     'Tres registros decididos no B3 com INCERTO_SAIDA nao resolvida no B1, padrao ja aplicado a '
     '265_ACM: a duvida sobre a notacao permanece registrada, mas tornou-se irrelevante porque o B3 '
     'decide independentemente dela. 137_ACM e 612_IEEE saem por E8, o modelo e insumo e o produto e '
     'avaliacao ou resposta; 554_IEEE sai por E7, o diagrama e insumo e o produto sao codigo e testes. '
     'Registro que 137_ACM avalia automaticamente a qualidade de diagramas por LLM, tema vizinho ao da '
     'revisao, mas com o LLM no papel de avaliador e nao de gerador.',P])
    w.writerow([';'.join(sorted(RET)),AGORA,REV,'DECISAO_GATE','B','','',
     'Dezoito registros RETIDOS pelo terceiro caso do B1, resumo que nao deixa clara a notacao de saida, '
     'com pauta de leitura individual registrada em cada um. Nucleo de modelagem de dominio, o padrao '
     'central da revisao a espera apenas de confirmacao da notacao: 027, 061, 138, 141, 221, 521, 623. '
     'O 521_IEEE e o de leitura mais prioritaria — entrada explicitamente em linguagem natural e '
     'avaliacao comparativa declarada. Casos de fronteira que podem exigir decisao explicita de '
     'protocolo: 518_IEEE, geracao de OCL, cuja tabela da secao 4.1 nao lista a OCL embora ela seja '
     'linguagem companheira da UML no padrao OMG; e 292_ACM, validade sintatica de modelos gerados por '
     'LLM, dimensao de qualidade central para a revisao, mas sobre gramatica nao nomeada. Registro uma '
     'CORRECAO DE VARREDURA: 903_SCOPUS nomeia diagrama de atividade e nao deveria ter caido no '
     'subconjunto sem mencao a UML; escapou porque grafa "activity-diagram" com hifen e a expressao '
     'regular exigia espaco. A leitura individual do bloco corrigiu o erro, mas ele indica risco '
     'residual de falso negativo por hifenizacao nos lotes automaticos.',P])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('alterados:',n)
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
