import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: leitura do titulo, do resumo e das palavras-chave deste registro no CSV da busca '
     'automatizada, aplicando screening_manual_v1.md e screening_flow_v1.puml na ordem do Portao B '
     '(B1 saida, B2 origem, B3 direcao, B4 entrada). ')

ESCOPO=('DELIMITACAO DE ESCOPO APLICADA: em 2026-08-16 a pesquisadora fixou, em funcao do fenomeno '
        'observado na pesquisa, que o objeto da revisao e a SINTESE DIRETA de conteudo UML por LLM a '
        'partir de especificacoes textuais em linguagem natural — requisitos, user stories, cenarios, '
        'problem statements ou descricoes textuais de dominio. Engenharia reversa a partir de codigo '
        'e formalizacao a partir de imagem ficam fora do escopo, ainda que meçam qualidade de UML '
        'gerada por LLM. Registro no log de eventos como INTERPRETACAO_PROTOCOLO. ')

# outcome, flags, EVIDENCIA, DISCUSSAO, DECISAO
R={}

# ---------------------------------------------------------------- B4_E9 (9)
E9_DISC=('DISCUSSAO: os tres primeiros subportoes sao vencidos. B1: a saida e UML explicita, primeiro '
 'caso do quadro. B2: ha LLM nomeado com autoridade semantica sobre o conteudo do modelo, satisfazendo '
 'a RF-02; nao ha pipeline de regras a que se pudesse atribuir a autoria. B3: a direcao e correta, o '
 'artefato UML e PRODUTO e nao insumo. A falha esta no B4, segundo caso: a entrada e explicitamente e '
 'SOMENTE artefato nao textual. A matriz da secao 4.3 do manual descreve exatamente este padrao — '
 '"codigo, imagem ou logs --> LLM --> UML" — e anota que o I2 ate passa e o que falha e a entrada. '
 'Pela regra de ouro 5, o criterio e I4/E9 e nao E6 nem E7. Pela regra de ouro 3, e o primeiro portao '
 'que explica claramente o caso. ')
E9_DEC=('DECISAO DA PESQUISADORA: EXCLUIDO por E9, decidido em B4. Registro que a exclusao NAO decorre '
 'de fragilidade metodologica do estudo, e sim da delimitacao de escopo: varios registros deste grupo '
 'apresentam evidencia de qualidade forte e explicita. ')

R['159_ACM']=('B4_E9','',
 'EVIDENCIA: o resumo declara o objetivo de definir uma abordagem de model-driven reverse engineering '
 'para extrair representacoes em Unified Modeling Language (UML) e Object Constraint Language (OCL) '
 '"from source code using Large Language Models (LLMs)". O contexto e a modernizacao de sistemas '
 'legados. As palavras-chave trazem "model driven reverse engineering (MDRE); unified modeling '
 'language (UML); object constraint language (OCL); large language models (LLMS)". A entrada e, '
 'literalmente, codigo-fonte de sistemas legados. ',E9_DISC,E9_DEC)
R['736_IEEE']=('B4_E9','',
 'EVIDENCIA: o resumo apresenta um pipeline agentico e multimodal que transforma diagramas informais e '
 'ad hoc em artefatos formais de MBSE. Descreve um "Transformer Agent that converts images of UML class '
 'diagrams into structured models and XMI" para ingestao em Cameo, Sparx EA e Visual Paradigm. As '
 'entradas sao nomeadas sem ambiguidade: esbocos nao estruturados e diagramas de ferramentas de '
 'escritorio, "e.g., Visio, PowerPoint, whiteboards". A saida e UML e XMI. ',E9_DISC,
 E9_DEC+'Nota-se que o registro tem ainda um Reviewer Agent que verifica conformidade a praticas de '
 'modelagem, o que seria evidencia de qualidade relevante caso o escopo admitisse entrada por imagem. ')
R['782_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o resumo relata estudo de cinco LLMs — StarCoder2, LLaMA, CodeLlama, Mistral e DeepSeek — '
 'para abstrair diagramas de classes UML "from code", com foco em acuracia, consistencia e F1, '
 'comparando programas Java e Python. As palavras-chave incluem "Model-driven Reverse Engineering '
 '(MDRE); UML Class Diagram; Java programs; Python programs". A entrada declarada e codigo-fonte. ',
 E9_DISC,E9_DEC+'Este e um caso exemplar do custo da delimitacao: o estudo mede exatamente acuracia e '
 'consistencia de UML gerada por LLM, mas a partir de codigo. ')
R['792_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o resumo descreve experimento em que o CodeT5, LLM pre-treinado em traducao de codigo, foi '
 'ajustado na tarefa de "generating sequence diagrams from Java methods", avaliando-se depois a '
 'generalizacao para metodos Python. As palavras-chave incluem "Reverse Engineering; Model '
 'Transformations; Java programming language". A entrada declarada sao metodos de codigo. ',E9_DISC,
 E9_DEC)
R['873_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o resumo declara que a pesquisa estuda "ChatGPT ability to generate class diagrams from '
 'source code", com prompt que recebe codigo-fonte e produz um diagrama de classes UML, aplicado a 40 '
 'sistemas e avaliado quanto a corretude e estrutura. Reporta que o ChatGPT captura 90 por cento das '
 'classes e atributos e 66 por cento das associacoes, com degradacao em projetos maiores. As '
 'palavras-chave sao "UML; ChatGPT; class diagrams; Large Language Models; software maintenance". ',
 E9_DISC,E9_DEC+'A evidencia de qualidade e das mais fortes do bloco — separa cobertura de classes e '
 'atributos da cobertura de associacoes, distincao proxima do interesse da revisao — e ainda assim a '
 'entrada e codigo-fonte. ')
R['908_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o titulo e o resumo declaram a geracao de codigo UML "from image-based UML diagrams" com '
 'um large multimodal language model, sobre conjuntos sinteticos de diagramas de atividade e de '
 'sequencia, comparando fine-tuning padrao com LoRA e medindo BLEU e SSIM (0,779 e 0,942 em diagramas '
 'de sequencia). A entrada declarada sao imagens de diagramas. ',
 E9_DISC.replace('a saida e UML explicita, primeiro caso do quadro',
   'a saida e codigo UML, isto e, a representacao legivel por maquina do proprio modelo, o que satisfaz '
   'o primeiro caso do quadro')+
 'Considerei o B3, porque ha UML tanto na entrada quanto na saida; nao se aplica o segundo nem o '
 'terceiro caso do B3, ja que o produto nao e avaliacao nem codigo de programa, mas o proprio modelo '
 'formalizado. O B3 portanto passa, e a decisao cai no B4. ',E9_DEC)
R['936_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o resumo explora o uso de LLMs, especificamente o GPT-4, "in generating class diagrams '
 'from code to emulate human abstraction", sobre cinco projetos substanciais com 4452 elementos de '
 'codigo e 338 elementos de modelo criados por especialistas. As palavras-chave sao "Class Diagrams; '
 'Large Language Models; Reverse Engineering". A entrada declarada e codebase. ',E9_DISC,
 E9_DEC+'O desenho comparativo contra abstracao criada por especialistas seria evidencia de qualidade '
 'de primeira ordem caso o escopo admitisse engenharia reversa. ')
R['953_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o titulo e explicito, "From image to UML", e o resumo declara a avaliacao da capacidade de '
 'diferentes LLMs de "convert images of (hand-drawn) UML class diagrams into the actual models '
 'represented in the images". O contexto e a formalizacao de desenhos feitos em quadro branco ou papel '
 'durante reunioes. As palavras-chave incluem "UML Diagram; Software Models; Image-based". A entrada '
 'declarada e imagem. ',E9_DISC,E9_DEC)
R['969_SCOPUS']=('B4_E9','',
 'EVIDENCIA: o titulo declara "Automated Software Architecture Design Recovery from Source Code Using '
 'LLMs" e o resumo avalia quatro modelos em tres tarefas, a primeira das quais e "identifying '
 'implementation-level class diagrams", em cenario realista com engenharia de prompt e mecanismo de '
 'Self-Reflection. As palavras-chave sao "Architecture Recovery; Large Language Models; Prompt '
 'Engineering; Software Architecture". A entrada declarada e codigo-fonte. ',
 E9_DISC+'Registro que o B1 exigiu atencao: o trabalho e de recuperacao arquitetural e boa parte de '
 'seus produtos sao estilos e padroes, nao UML; o diagrama de classes, porem, e nomeado como uma das '
 'tres tarefas avaliadas, o que caracteriza componente UML separavel e faz o B1 passar. ',E9_DEC)

# ---------------------------------------------------------------- B3_E8 (4)
E8_DEC=('DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. Nao ha sintese de conteudo UML: o '
 'modelo ja existe e permanece inalterado ao fim do processo. ')
R['265_ACM']=('B3_E8','INCERTO_SAIDA',
 'EVIDENCIA: o resumo apresenta um autograder baseado em LLM para diagramas leves, incluindo desenhados '
 'a mao, em curso de Sistemas Embarcados. O sistema "converts diagram images into a structured JSON '
 'representation using an LLM and then deterministically compares this representation with a reference '
 'solution to generate grades and feedback", com cerca de 90 por cento de acuracia sobre 345 '
 'submissoes. A UML aparece uma unica vez, e na caracterizacao do estado da arte que os autores querem '
 'superar: a avaliacao automatizada "often relies on formal notations such as UML and specialized '
 'tools". As palavras-chave sao "autograder; diagram; embedded systems", sem UML. ',
 'DISCUSSAO: o B1 nao decide com clareza. Os diagramas avaliados sao descritos como leves e o texto '
 'contrapoe a abordagem a das notacoes formais, mas nao afirma que nenhuma submissao seja UML — e o '
 'terceiro caso do B1, resumo ambiguo, que manda reter com INCERTO_SAIDA e seguir. O B3 decide sem '
 'depender dessa duvida: qualquer que seja a notacao, o diagrama e INSUMO, produzido pelo estudante, e '
 'o produto do LLM sao nota e feedback. E o segundo caso do B3, "UML existente --> LLM --> avaliacao, '
 'classificacao", e a matriz da secao 4.3 confirma o E8. Considerei o B2, porque converter imagem em '
 'JSON e transcricao e nao geracao, o que pela RF-02 levaria a E6; descartei porque a pergunta do B2 '
 'pressupoe um diagrama sendo produzido, e forcar sua aplicacao a um sistema que nao produz diagramas '
 'daria um rotulo menos informativo que o E8. Considerei tambem E9, pela entrada em imagem, mas o B3 '
 'antecede o B4. ',
 E8_DEC+'Mantida a flag INCERTO_SAIDA por transparencia: a duvida sobre a notacao das submissoes nao '
 'foi resolvida, apenas tornou-se irrelevante para o desfecho. ')
R['826_SCOPUS']=('B3_E8','',
 'EVIDENCIA: o resumo propoe alinhar deteccao de padroes de projeto a principios de MDE, "helping in '
 'the automation of extraction of code bases in the form of UML models and injecting them into an '
 'LLM-based design-pattern recognition flow", avaliado no repositorio P-MART e comparando diferentes '
 'LLMs com e sem comentarios. A frase decisiva e que os LLMs "are able to identify a variety of Gang of '
 'Four (GoF) design patterns using UML models as input". As palavras-chave sao "GoF design patterns; '
 'LLMs; MDE; P-MART; Software Models". ',
 'DISCUSSAO: B1 passa, ha UML explicita. B2 passa, ha LLMs nomeados. O B3 decide: o proprio resumo diz '
 'que os modelos UML sao INPUT do LLM e que a saida sao padroes identificados. E o segundo caso do B3, '
 'UML como insumo para classificacao, sem que nada no modelo seja produzido ou alterado. A extracao dos '
 'modelos UML a partir do codigo e feita por tecnicas de MDE, nao pelo LLM, de modo que nao ha sintese '
 'de UML por LLM em ponto algum do pipeline. ',E8_DEC)
R['897_SCOPUS']=('B3_E8','',
 'EVIDENCIA: o resumo investiga a capacidade do ChatGPT-4o de responder a 120 exercicios multimodais de '
 'cursos de computacao. Declara que "the multi-modal artifacts in these exercises include class '
 'diagrams, sequence diagrams, user interface images, analytical charts, workflow diagrams and '
 'object-flow diagrams", e reporta que o modelo vai bem justamente nos exercicios com diagramas de '
 'classes e de sequencia. As palavras-chave sao "academic assessments; multi-modal exercises; prompt '
 'engineering". ',
 'DISCUSSAO: B1 passa, porque diagramas de classes e de sequencia sao nomeados e constituem componente '
 'UML separavel entre os artefatos do estudo. B2 passa, o ChatGPT-4o e nomeado. O B3 decide: os '
 'diagramas sao INSUMO do enunciado e o produto do LLM e a resposta ao exercicio, comparada as '
 'respostas esperadas. E o segundo caso do B3. Nenhum diagrama e gerado, reparado ou refinado. '
 'Considerei o E9 pela entrada multimodal, mas o B3 antecede o B4. ',E8_DEC)
R['980_SCOPUS']=('B3_E8','',
 'EVIDENCIA: o resumo apresenta o ArchCrafter, arcabouco baseado em LLMs que detecta problemas '
 'arquiteturais. O nucleo CraftCore "integrates transformer-based language understanding with dynamic '
 'graph neural networks to analyze codebases and UML diagrams, pinpointing structural risks". Os '
 'produtos sao mapas de risco, previsoes, anotacoes colaborativas e recomendacoes de refatoracao, '
 'avaliados em 500 repositorios com 90 por cento de acuracia de deteccao. As palavras-chave sao "AI for '
 'software engineering; GenAI; LLMs; Software architecture". ',
 'DISCUSSAO: B1 passa, ha UML explicita. B2 passa, ha LLMs. O B3 decide: os diagramas UML sao INSUMO da '
 'analise, ao lado do codigo, e o produto sao diagnosticos de falha arquitetural e recomendacoes — '
 'segundo caso do B3. Nada de conteudo UML e produzido ou alterado; os module graphs do FlawMesh sao '
 'visualizacao de risco, nao modelo UML. Considerei o E9 pela entrada em codebase, mas o B3 antecede o '
 'B4. ',E8_DEC)

# ---------------------------------------------------------------- B3_E7 (3)
E7B3_DISC=('DISCUSSAO: B1 passa, porque ha UML explicita em jogo e o registro nao cai no segundo caso '
 '(outra notacao). B2 passa, ha LLM nomeado. O B3 decide pelo terceiro caso: "UML existente --> LLM --> '
 'codigo, testes, documentacao", em que o produto NAO e UML. A matriz da secao 4.3 confirma o E7 para '
 'este padrao. Registra-se o desfecho como B3_E7 e nao B1_E7 porque a distincao importa e o proprio '
 'manual a exige: aqui havia UML, so que na entrada; em um B1_E7 a UML nunca existiu. Pela regra de '
 'ouro 5, a falha e de saida (I5/E7) e nao de entrada. ')
E7B3_DEC=('DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B3. Trata-se de geracao de codigo a '
 'partir de modelo, direcao inversa a que a revisao investiga. ')
R['779_SCOPUS']=('B3_E7','',
 'EVIDENCIA: o resumo propoe abordagem baseada em LLM que "generates executable code directly from '
 'images of hand-drawn UML state diagrams", para que estudantes do ensino medio japones experimentem o '
 'comportamento dinamico de diagramas de estado desenhados a mao. Avalia acuracia de conversao por '
 'complexidade e confirma que o sistema nao corrige silenciosamente diagramas intencionalmente '
 'defeituosos. As palavras-chave incluem "Code Generation; Dynamic Behavior Verification; Hand-drawn '
 'Diagrams; UML". O produto declarado e codigo executavel. ',E7B3_DISC,
 E7B3_DEC+'O achado de que o sistema nao conserta diagramas defeituosos e interessante para qualidade, '
 'mas diz respeito a fidelidade da traducao para codigo, nao a qualidade de UML sintetizada. ')
R['846_SCOPUS']=('B3_E7','',
 'EVIDENCIA: o titulo declara a avaliacao das capacidades do GPT-4-Vision em "UML-Based Code '
 'Generation" e o resumo especifica a transformacao de diagramas de classes UML "into fully operating '
 'Java class files", sobre imagens exportadas de 18 diagramas, com tres prompts por entrada e sistema '
 'de pontuacao proprio; em media o modelo gerou codigo para 88 por cento dos elementos mostrados. As '
 'palavras-chave incluem "code generation; large language models; OOP; UML; Java programming '
 'language". O produto declarado sao arquivos de classe Java. ',E7B3_DISC,E7B3_DEC)
R['977_SCOPUS']=('B3_E7','',
 'EVIDENCIA: o titulo declara avaliacao de GPT-4o, Gemini e DeepSeek em "UML-to-Java Code Generation" e '
 'o resumo explica que a pergunta e se fornecer uma entrada formal — diagramas de classes UML — reduz '
 'os erros dos modelos em relacao a instrucoes em texto livre. Quatro diagramas de complexidade '
 'crescente sao convertidos em codigo Java 11, medindo-se acuracia estrutural, taxa de erro de '
 'compilacao e tempo. As palavras-chave incluem "Unified Modeling Language; Java programming language; '
 'Codegeneration". O produto declarado e codigo Java. ',E7B3_DISC,
 E7B3_DEC+'Note-se que aqui a UML e tratada como ENTRADA de qualidade controlada, variavel '
 'independente do experimento, e nao como objeto de avaliacao. ')

# ---------------------------------------------------------------- B1_E7 (2)
R['808_SCOPUS']=('B1_E7','',
 'EVIDENCIA: o resumo declara o uso de LLMs para automatizar "the derivation of IFML-like Graphical '
 'User Interface (GUI) models from mock-up images", estendendo o arcabouco low-code BESSER. A UML '
 'aparece na descricao do pipeline, que se apoia "on the UML (for the structural models) and IFML (for '
 'the GUI ones)". As palavras-chave sao "Design-to-Code; Graphical User Interface (GUI); IFML; Large '
 'Language Models; Web Engineering; Mockups". O artefato que o LLM deriva e o modelo de GUI em IFML. ',
 'DISCUSSAO: o B1 decide pelo segundo caso. O que o LLM produz e IFML, notacao distinta da UML, e a '
 'mencao a UML descreve outra camada do BESSER — os modelos estruturais — que nao e o que o LLM deriva '
 'neste trabalho. Avaliei se havia componente UML separavel e concluo que nao: o resumo nao atribui ao '
 'LLM a geracao dos modelos estruturais UML nem reporta qualquer medida sobre eles; as medidas '
 'reportadas sao de acuracia dos modelos de GUI e de similaridade estrutural das paginas web. '
 'Considerei o E9, pois a entrada sao imagens de mock-up, digitais e desenhadas a mao, mas o B1 '
 'antecede o B4. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Pergunta que ficaria para o texto completo '
 'caso o registro fosse reaberto: os modelos estruturais UML do BESSER sao gerados pelo LLM e avaliados '
 'separadamente dos modelos IFML? ')
R['889_SCOPUS']=('B1_E7','',
 'EVIDENCIA: o resumo apresenta uma taxonomia baseada em papeis para avaliacao automatizada de '
 'respostas abertas de estudantes, distinguindo LLMs generativos como avaliadores virtuais diretos, '
 'encoders transformers como ferramentas semanticas e modelos text-to-text intermediarios. Discute '
 'alucinacao, instabilidade probabilistica, interpretabilidade e vies, e apresenta um arcabouco com '
 'role prompting, correcao restrita por rubrica e RAG. As palavras-chave sao "automated assessment; '
 'large language models; open-ended questions; RAG; semantic analysis", sem qualquer termo de '
 'modelagem. ',
 'DISCUSSAO: o B1 decide pela clausula geral, a saida nao e UML. O trabalho produz notas, taxonomia e '
 'arcabouco de avaliacao educacional; nao ha artefato de modelagem em ponto algum. A ocorrencia lexical '
 'que trouxe este registro ao bloco de revisao nao corresponde a nenhum uso substantivo de UML no '
 'resumo. Nao e o terceiro caso do B1, porque o resumo e claro sobre o que produz. Pela regra de ouro '
 '5, falha de saida e I5/E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Registro tambem que o dominio e avaliacao '
 'educacional de respostas abertas, sem relacao com engenharia de software dirigida a modelos. ')

# ---------------------------------------------------------------- PASSOU (3)
R['787_SCOPUS']=('PASSOU','CANDIDATO_E10;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo relata benchmarking estruturado de ferramentas de IA generativa — GitHub '
 'Copilot, GPT-4, Codeium, Claude 3.5, Gemini 1.5, Supermaven, TabNine, Testim, Postman, Eraser.io e '
 'Lucidchart AI — nas fases de design, implementacao, depuracao e teste, com cinco avaliadores, prompts '
 'padronizados e papeis contrabalanceados. Entre as metricas estao iteracoes de prompt, tempo de '
 'conclusao, carga de correcao humana, frequencia de alucinacao, acuracia da saida e consistencia entre '
 'arquivos. Declara que as ferramentas aceleraram tarefas como "boilerplate generation and UML '
 'sketching". As palavras-chave incluem "UML Generation". ',
 'DISCUSSAO: B1 passa, "UML Generation" nas palavras-chave e "UML sketching" no resumo caracterizam '
 'componente UML declarado. B2 passa, ha multiplos LLMs nomeados em papel gerativo. B3 passa, a UML e '
 'produto. B4 passa, a entrada sao prompts padronizados, isto e, texto. Portao C: ha vocabulario de '
 'avaliacao abundante e explicito, com metricas nomeadas, logo EVIDENCIA=EXPLICITA. Sinalizo '
 'CANDIDATO_E10 porque a UML e uma tarefa entre muitas em um estudo cujo objeto e o conjunto das fases '
 'da engenharia de software; a matriz da secao 4.3 prescreve reter com essa flag quando o LLM gera '
 'multiplos artefatos e o UML nao se separa. ',
 'DECISAO DA PESQUISADORA: RETIDO para o texto completo. Percorreu os quatro subportoes sem exclusao. '
 'Pergunta que o texto completo precisa responder: ha metrica de qualidade reportada especificamente '
 'para a UML produzida, separavel das metricas das demais fases? Se nao houver, o registro e forte '
 'candidato a E10 na extracao. ')
R['822_SCOPUS']=('PASSOU','INCERTO_ENTRADA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo examina o papel do GitHub Copilot no apoio a arquitetos de software e enumera os '
 'artefatos em questao: "Unified Modeling Language (UML) diagrams, class diagrams, sequence diagrams, '
 'use case diagrams, component diagrams, deployment diagrams, activity diagrams, and state diagrams". '
 'Declara que avalia "how closely Copilot-generated outputs align with established architectural '
 'principles" e que, analisando os desvios, discute como prompts refinados produzem resultados mais '
 'acurados. As palavras-chave incluem "Generative AI (GenAI); Github Copilot; Software Architecture". ',
 'DISCUSSAO: B1 passa com folga, sao sete tipos de diagrama UML nomeados. B2 passa, o Copilot e nomeado '
 'e gera as saidas avaliadas. B3 passa, a UML e produto do Copilot. O B4 e o ponto fragil: o resumo nao '
 'declara o que entra no processo. Fala em "well-defined contexts" e em prompts refinados, o que sugere '
 'entrada textual, mas nao nomeia requisitos, user stories nem descricoes de dominio. E o terceiro caso '
 'do B4, entrada nao declarada, que manda reter sinalizando. Portao C: ha avaliacao de alinhamento a '
 'principios e analise de desvios, logo EVIDENCIA=EXPLICITA. ',
 'DECISAO DA PESQUISADORA: RETIDO para o texto completo, com INCERTO_ENTRADA. Pergunta que o texto '
 'completo precisa responder: qual e a entrada fornecida ao Copilot para produzir os diagramas — '
 'especificacao textual em linguagem natural, que mantem o registro no escopo, ou codigo existente, que '
 'o levaria a E9 pela delimitacao fixada nesta data? ')
R['900_SCOPUS']=('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo explora o conceito e o prototipo de um interpretador de modelos conceituais capaz '
 'de renderizar modelos visuais "generated in textual syntax by state-of-the-art LLMs such as Llama 2 '
 'and ChatGPT 4". Especifica que esses LLMs "can generate textual syntax for the PlantUML and Graphviz '
 'modeling software that is automatically rendered within a conversational user interface", e anuncia '
 'resultados experimentais para modelos gerados com ChatGPT 4 e Llama 2. As palavras-chave sao '
 '"Conceptual Model; Interpreter; Large Language Model; Code Generation". ',
 'DISCUSSAO: B1 passa. A saida e sintaxe textual PlantUML, e a regra do protocolo (l. 174) admite '
 'PlantUML quando destinado a codificar UML, o que e o caso, tratando-se de modelos conceituais '
 'renderizados como modelos visuais. A mencao paralela ao Graphviz nao descaracteriza o componente UML, '
 'que e separavel. B2 passa, Llama 2 e ChatGPT 4 sao nomeados e geram a sintaxe do modelo, satisfazendo '
 'a RF-02. B3 passa, o modelo e produto e o refinamento conversacional configura o quarto caso, revisao '
 'que altera o conteudo. B4 passa, a entrada e o dialogo em linguagem natural com o usuario. Portao C: '
 'ha resultados experimentais declarados, logo EVIDENCIA=EXPLICITA. ',
 'DECISAO DA PESQUISADORA: RETIDO para o texto completo. Percorreu os quatro subportoes sem exclusao. '
 'Pergunta para a extracao: os resultados experimentais medem a qualidade do modelo gerado (corretude, '
 'completude) ou apenas a taxa de renderizacao bem-sucedida da sintaxe? ')

assert len(R)==21, len(R)

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
n=0
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid not in R: continue
    out,flags,ev,disc,dec=R[lid]
    assert r[i['excluded']]!='true' and not r[i['gate_b_outcome']], lid
    r[i['gate_b_outcome']]=out; r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    nota=MET+ev+disc+dec
    if out.startswith('B4_E9'): nota+=ESCOPO
    r[i['gate_b_notes']]=nota
    if flags:
        r[i['gate_c_flags']]=flags; r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
    if out!='PASSOU':
        r[i['excluded']]='true'; r[i['exclusion_criteria']]=out.split('_')[-1]
    n+=1

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

g=lambda o:';'.join(sorted(k for k,v in R.items() if v[0]==o))
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); P='protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'
    w.writerow([g('B4_E9'),AGORA,REV,'INTERPRETACAO_PROTOCOLO','B4','','E9',
     'Delimitacao de escopo fixada pela pesquisadora em funcao do fenomeno observado na pesquisa: o '
     'objeto da revisao e a SINTESE DIRETA de conteudo UML por LLM a partir de especificacoes textuais '
     'em linguagem natural — requisitos, user stories, cenarios, problem statements ou descricoes '
     'textuais de dominio. Por consequencia, engenharia reversa a partir de codigo-fonte e formalizacao '
     'a partir de imagem ficam FORA do escopo, mesmo quando medem qualidade de UML gerada por LLM com '
     'metricas explicitas. A decisao foi tomada com ciencia do custo: sai deste bloco um conjunto de '
     'estudos metodologicamente fortes (873, ChatGPT em 40 sistemas com 90 por cento de classes e 66 '
     'por cento de associacoes; 936, GPT-4 contra abstracao de especialistas em 4452 elementos; 782, '
     'cinco LLMs com acuracia, consistencia e F1; 953, imagens de diagramas desenhados a mao; 792, '
     'CodeT5 e generalizacao entre linguagens). A alternativa considerada e recusada era emendar o I4 '
     'para admitir entrada nao textual, o que alargaria o escopo de "sintese de UML a partir de '
     'especificacao" para "geracao de UML por LLM em geral". Estes 9 registros ficam nomeados neste '
     'evento e sao recuperaveis sem re-triagem caso o I4 venha a ser emendado.',P])
    w.writerow([g('B3_E8'),AGORA,REV,'DECISAO_GATE','B3','','E8',
     'Quatro registros excluidos por E8 no B3: a UML e insumo e o LLM apenas avalia, classifica ou '
     'diagnostica, sem produzir nem alterar conteudo de modelo. 265_ACM correcao automatica de '
     'diagramas, retida a flag INCERTO_SAIDA porque a notacao das submissoes nao foi resolvida, embora '
     'irrelevante para o desfecho; 826_SCOPUS deteccao de padroes GoF com modelos UML como input '
     'declarado, sendo a extracao dos modelos feita por MDE e nao por LLM; 897_SCOPUS ChatGPT-4o '
     'respondendo exercicios cujos artefatos incluem diagramas de classes e de sequencia; 980_SCOPUS '
     'ArchCrafter analisando codebases e diagramas UML para apontar falhas arquiteturais.',P])
    w.writerow([g('B3_E7'),AGORA,REV,'DECISAO_GATE','B3','','E7',
     'Tres registros excluidos por E7 no B3, direcao inversa a investigada: a UML entra e o produto e '
     'codigo. 779_SCOPUS gera codigo executavel a partir de imagens de diagramas de estado desenhados a '
     'mao; 846_SCOPUS converte imagens de diagramas de classes em arquivos Java com GPT-4-Vision; '
     '977_SCOPUS avalia GPT-4o, Gemini e DeepSeek em UML-to-Java, tratando a UML como variavel '
     'independente de qualidade controlada e nao como objeto de avaliacao. O desfecho foi registrado '
     'como B3_E7 e nao B1_E7 porque havia UML no estudo, so que na entrada — distincao que a secao 6.1 '
     'do manual exige preservar.',P])
    w.writerow([g('B1_E7'),AGORA,REV,'DECISAO_GATE','B1','','E7',
     'Dois registros excluidos por E7 no B1. 808_SCOPUS: o LLM deriva modelos de GUI em IFML a partir de '
     'imagens de mock-up; a UML citada pertence a outra camada do arcabouco BESSER, nao e gerada pelo '
     'LLM nem medida, logo nao ha componente UML separavel. 889_SCOPUS: taxonomia e arcabouco de '
     'avaliacao automatizada de respostas abertas de estudantes, sem qualquer artefato de modelagem; a '
     'ocorrencia lexical de UML nao corresponde a uso substantivo.',P])
    w.writerow([g('PASSOU'),AGORA,REV,'DECISAO_GATE','B','','',
     'Tres registros RETIDOS apos percorrer os quatro subportoes do Portao B. 787_SCOPUS benchmarking de '
     'ferramentas de IA generativa nas fases da engenharia de software, com UML Generation nas '
     'palavras-chave e metricas fartas, retido com CANDIDATO_E10 porque a UML e uma tarefa entre muitas '
     'e pode nao se separar na extracao. 822_SCOPUS papel do GitHub Copilot no trabalho do arquiteto, '
     'com sete tipos de diagrama UML nomeados e avaliacao de alinhamento a principios, retido com '
     'INCERTO_ENTRADA porque o resumo nao declara o que entra no processo — questao que se tornou '
     'decisiva apos a delimitacao de escopo fixada nesta data. 900_SCOPUS interpretador de modelos '
     'conceituais em que Llama 2 e ChatGPT 4 geram sintaxe PlantUML renderizada em interface '
     'conversacional, admitido pela regra do protocolo (l. 174) que aceita PlantUML quando destinado a '
     'codificar UML.',P])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('alterados:',n,' linhas=%d cols=%d'%(len(rows),len(rows[0])))
val=sum(1 for r in rows[1:] if r[i['excluded']]!='true')
print('VALIDOS=%d EXCLUIDOS=%d'%(val,len(rows)-1-val))
print('gate_b  :',dict(sorted(Counter(r[i['gate_b_outcome']] or '(nao triado)' for r in rows[1:]).items())))
print('criterio:',dict(sorted(Counter(r[i['exclusion_criteria']] for r in rows[1:] if r[i['excluded']]=='true').items())))
print('flags   :',dict(sorted(Counter(r[i['gate_c_flags']] for r in rows[1:] if r[i['gate_c_flags']]).items())))
mau=0
for r in rows[1:]:
    a,b,ex,cr=r[i['gate_a_outcome']],r[i['gate_b_outcome']],r[i['excluded']],r[i['exclusion_criteria']]
    parou=(a!='PASSOU') or (b not in ('','PASSOU'))
    cod=(a.split('_')[-1] if a!='PASSOU' else (b.split('_')[-1] if b not in ('','PASSOU') else ''))
    if parou!=(ex=='true') or cod!=cr: mau+=1
print('divergencias:',mau)
t=[len(r[i['gate_b_notes']]) for r in rows[1:] if r[i['logical_id']] in R]
print('notas: n=%d min=%d max=%d'%(len(t),min(t),max(t)))
