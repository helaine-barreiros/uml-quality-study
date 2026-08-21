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
'898_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo declara que agentes LLM geram diagramas de classes UML a partir de 20 exercicios '
 'de modelagem de requisitos coletados em fontes web, e que as solucoes do LLM foram comparadas as de um '
 'solucionador humano em termos de corretude sintatica, semantica e pragmatica e de distancia em relacao '
 'a uma solucao de referencia. Reporta resultado direcional: numero significativamente maior de erros '
 'semanticos e maior diferenca textual, sem diferenca significativa em qualidade sintatica e pragmatica. ',
 'DISCUSSAO: B1 saida e conteudo UML nomeado (diagrama de classes). B2 origem e agente LLM com autoridade '
 'semantica plena sobre o modelo produzido. B3 direcao e enunciado textual do exercicio para UML, celula '
 '"requisitos -> LLM -> UML" da secao 4.3 do manual. B4 entrada e especificacao textual em linguagem '
 'natural, dentro do escopo fixado. Nenhum portao explica exclusao. O trio sintatico/semantico/pragmatico '
 'e exatamente o vocabulario de qualidade de I6, com instrumento e solucao de referencia declarados. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Registro de nucleo para a extracao: fornece '
 'metricas por dimensao de qualidade e comparacao com baseline humano.'),

'901_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo descreve a construcao de diagrama de classes UML a partir de descricao de requisitos '
 'usando POS tagging do dominio de NLP, parsing pelo NLTK com gramatica de estrutura sintagmatica do ingles '
 'e analise de dependencia sobre as arvores de parse, em iteracoes, para determinar nomes de classes, '
 'metodos, atributos e relacionamentos. O LLM aparece apenas como motivacao declarada: "motivated by the '
 'wide usage and popularity of natural languages in prompting queries to Large Language Models (LLM) in '
 'recent times to generate a code". "Large Language Model (LLM)" consta em KW. ',
 'DISCUSSAO: B1 saida e conteudo UML nomeado, entao o portao B1 nao explica o caso. B2 origem e onde ele se '
 'resolve sem residuo: quem determina classes, atributos, metodos e relacionamentos e o pipeline simbolico '
 '(tagger, parser, gramatica, analise de dependencia), nao um modelo de linguagem. Pela RF-02 o criterio e '
 'autoridade semantica sobre os elementos portadores de significado, e aqui ela e integralmente simbolica; '
 'o LLM nao participa da producao e sequer e usado no experimento. Caso de armadilha lexical: LLM em KW e '
 'no corpo do resumo sem qualquer papel constitutivo. ',
 'DECISAO: excluido em B2 por E6. Nao satisfaz I2.'),

'904_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo propoe um framework de aceleracao para verificacao de sistemas de tempo real dirigidos '
 'a interrupcao contra propriedades temporais de valor de relogio explicito, com reducao de ordem parcial e '
 'codificacao em logica de primeira ordem, e a ferramenta PARCEL. Diagramas de sequencia aparecem so na '
 'contextualizacao ("designers often model these systems using automata or sequence diagrams"). LLMs '
 'aparecem apenas como sintetizadores de modelos de larga escala para o experimento ("large-scale models '
 'synthesized by LLMs"). O desfecho medido e velocidade de verificacao. ',
 'DISCUSSAO: B1 e o primeiro portao e ja explica o caso sem residuo: o produto avaliado nao e conteudo UML, '
 'e desempenho de verificacao formal. Os modelos sintetizados por LLM sao insumo experimental para escalar '
 'o benchmark, e em nenhum momento sua qualidade como UML e objeto de medida. Nao ha necessidade de descer '
 'a B2, B3 ou B4 pela regra de ouro 3. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'905_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo trata de Event Storming (ES) no metodo Domain-Driven Design, com experimento '
 'controlado de 240 participantes em 60 equipes sob tres condicoes (ES manual, ES assistido por LLM com '
 'prompt basico e com prompt otimizado). Os modelos gerados foram avaliados quantitativamente em Accuracy, '
 'Completeness e Consistency. UML aparece somente como termo de contraste: "Compared to traditional UML '
 'modeling techniques, ES emphasizes collaborative exploration and rapid iteration". Nenhum tipo de diagrama '
 'UML e nomeado como produto. ',
 'DISCUSSAO: B1 explica o caso sem residuo. Event Storming e notacao adjacente, nao pertence ao metamodelo '
 'UML nem e perfil dele: seus elementos sao eventos de dominio, comandos, agregados e politicas em quadro '
 'colaborativo. Mesmo padrao ja registrado em 759_SCOPUS (arvore de falhas), 781_SCOPUS (diagrama de '
 'componentes de neurociencia) e 895_SCOPUS (mapas conceituais). A qualidade e medida com o vocabulario '
 'exato de I6, mas sobre artefato que nao e UML, e a regra de ouro 2 nao converte ausencia de UML em '
 'inclusao. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5. Trabalho nomeado como adjacente de interesse: se o '
 'protocolo vier a admitir notacoes de modelagem conceitual alem da UML, e recuperavel sem re-triagem, '
 'pois traz desenho experimental forte e metricas de qualidade explicitas.'),

'906_SCOPUS':('B3_E7','',
 'EVIDENCIA: o resumo declara que o sistema "extracts use cases from UML Use Case Diagrams and employs a '
 'Generative AI Model to generate descriptive text for each extracted use case", com o objetivo de reduzir '
 'o tempo de documentacao e uniformizar a descricao das funcoes de software. O resultado reportado e '
 'reducao de trabalho manual mantendo clareza e abrangencia da documentacao. ',
 'DISCUSSAO: B1 nao exclui, ha UML no caso. B2 nao exclui, o modelo generativo e substantivo. B3 explica sem '
 'residuo: a direcao e a celula "UML existente -> LLM -> codigo/testes/documentacao" da secao 4.3 do manual. '
 'O diagrama de casos de uso e insumo dado, produzido fora do escopo do estudo, e o produto avaliado e texto '
 'descritivo de documentacao. Nao ha sintese de conteudo UML a partir de especificacao textual, que e o '
 'objeto delimitado da revisao. ',
 'DECISAO: excluido em B3 por E7. Nao satisfaz I5.'),

'907_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: experimento empirico com 39 grupos de graduandos comparando abordagem plan-driven e iterativa '
 'na modelagem colaborativa humano-LLM. Os participantes colaboraram com GPT ou Gemini para elicitar '
 'requisitos e criar diagramas UML de casos de uso, de classes e de sequencia, refinando os modelos. Um '
 'avaliador independente julgou a qualidade semantica dos modelos finais em termos de validade e '
 'completude. Observacoes qualitativas registram alucinacoes do modelo no fluxo plan-driven e deriva de '
 'contexto e regressao do modelo no fluxo iterativo. ',
 'DISCUSSAO: B1 saida e UML com tres tipos nomeados. B2 origem e LLM generativo com autoridade semantica '
 'sobre o conteudo produzido, ainda que sob refinamento humano. B3 direcao e requisitos para UML. B4 entrada '
 'e o cenario textual do exercicio. Nenhum portao exclui. A ressalva e de atribuicao: a qualidade medida e '
 'do artefato co-produzido por humano e LLM, e o desenho nao isola a contribuicao de cada um, o que so pode '
 'ser resolvido no texto completo. Isso nao e E10, que trata de inseparabilidade em relacao a outros '
 'artefatos gerados, e sim de inseparabilidade em relacao ao agente; a flag INCERTO_PAPEL_LLM cobre o ponto. '
 'Validade e completude sao termos literais de I6. ',
 'DECISAO: retido no Portao B; flags INCERTO_PAPEL_LLM e EVIDENCIA=EXPLICITA. Ler o texto completo para '
 'verificar se ha condicao de controle sem LLM que permita atribuir a qualidade ao modelo.'),

'909_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: apresenta o UMLBot, aplicacao web de codigo aberto que usa LLMs para gerar fonte PlantUML '
 'editavel e diagramas UML renderizados a partir de descricoes em linguagem natural ou diretamente de '
 'trechos de codigo. Suporta refinamento iterativo por interface de chat, acesso configuravel a LLMs '
 'compativeis com OpenAI, renderizacao PlantUML, autocorrecao e nova tentativa, e implantacao por Docker '
 'Compose. Nenhuma metrica de qualidade e reportada no resumo. ',
 'DISCUSSAO: B1 saida e conteudo UML, com o titulo declarando "editable UML diagrams" e o resumo falando em '
 'representacao visual padronizada da UML; PlantUML aqui e sintaxe portadora do produto, nao o produto. B2 '
 'origem e LLM generativo. B3 direcao inclui descricao em linguagem natural para UML. B4 entrada e '
 'disjuntiva, linguagem natural OU trecho de codigo; como ha componente textual declarado, E9 nao se aplica, '
 'diferentemente de 921_SCOPUS e 930_SCOPUS, cuja entrada e exclusivamente codigo. Trata-se de artigo de '
 'ferramenta, sem avaliacao de qualidade no resumo; pela regra de ouro 2 a ausencia de vocabulario de '
 'qualidade nao exclui nesta etapa, e E11 e proibido em titulo e resumo. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=A_VERIFICAR. Verificar no texto completo se ha avaliacao; se '
 'houver apenas descricao da arquitetura, e candidato a E11 na fase de texto completo.'),

'910_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo estuda conversas com chatbots baseados em LLM sob a perspectiva de elicitacao de '
 'conhecimento, com o objetivo de avaliar a confianca do humano no conhecimento elicitado. A abordagem e '
 'apoiada pela DSML KEML (Knowledge Elicitation Modeling Language), com sintaxe abstrata e visual e '
 'semantica por transformacao de modelos para analise de confianca. As conversas sao modeladas por '
 'combinacao de diagramas de sequencia e grafos de argumentacao estendidos. ',
 'DISCUSSAO: B1 nao exclui, pois ha diagrama de sequencia nomeado. B2 explica sem residuo: quem produz os '
 'modelos e o analista humano usando a KEML, e o LLM e o objeto modelado, nao o gerador. A inversao e '
 'completa em relacao ao escopo da revisao: aqui a conversa com o LLM e a entrada e a UML e o instrumento '
 'de analise construido pelos autores. Mesmo padrao ja registrado em 864_SCOPUS e 875_SCOPUS, em que a '
 'formalizacao UML e obra dos autores. ',
 'DECISAO: excluido em B2 por E6. Nao satisfaz I2 na funcao exigida.'),

'911_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo propoe a criacao de um corpus anotado segundo esquema IOB customizado, destinado a '
 'treinar modelos de Named Entity Recognition (NER) para extracao automatica de elementos UML a partir de '
 'texto. O esquema integra rotulos para classes, atributos, metodos e relacionamentos (associacao, '
 'agregacao, composicao, heranca). KW lista Deep learning, IOB annotation, LLMs, NLP. ',
 'DISCUSSAO: B1 nao exclui, pois os elementos alvo sao elementos de diagrama de classes. B2 explica sem '
 'residuo pela RF-01: uso de modelos para reconhecimento de entidades nomeadas e uso extrativo e '
 'classificatorio, nao gerativo, e nao satisfaz I2 mesmo quando o rotulo "LLM" aparece nas palavras-chave. '
 'Alem disso o produto do trabalho e o dataset anotado e o treinamento dos modelos, nao um diagrama '
 'sintetizado. Decisao alinhada a 841_SCOPUS, que compara BERT, RoBERTa, XLNet e outros na extracao de '
 'classes de corpus anotado e tambem saiu por B2_E6, e contrastada com 876_SCOPUS, que usa o mesmo verbo '
 '"extract" mas com LLMs generativos, prompts e debate multiagente e foi retido. ',
 'DECISAO: excluido em B2 por E6. Registro sinalizado, junto com 841_SCOPUS, como decisao de fronteira da '
 'RF-01 para conferencia pelo segundo revisor.'),

'912_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo descreve metodo que converte requisitos em diagramas UML no contexto de MDA, com tres '
 'componentes: esquema JSON intermediario restrito gerado por um LLM, conversao deterministica para '
 'PlantUML e exportacao XMI para verificacao por ferramenta, alem de comparacao baseada em regras. Declara '
 'que o sistema "evaluates structural extraction quality for vital UML elements". ',
 'DISCUSSAO: B1 saida e conteudo UML exportado em XMI, formato do proprio metamodelo. B2 origem: o LLM gera '
 'o esquema JSON que carrega classes, atributos e relacionamentos, e as etapas deterministas apenas '
 'transcrevem para PlantUML e XMI; pela RF-02 a autoridade semantica e do LLM e as regras simbolicas no '
 'pipeline sao irrelevantes para o portao. B3 direcao e requisitos para UML. B4 entrada e requisitos em '
 'linguagem natural. Ha metrica declarada de qualidade estrutural dos elementos UML gerados. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA.'),

'913_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo propoe arquitetura hibrida GraphRAG que combina LLMs e recuperacao semantica baseada '
 'em grafo com Neo4j para gerar diagramas de sequencia UML a partir de documentos de Especificacao de '
 'Requisitos de Software (SRS). Declara melhora de acuracia por prompting com recuperacao aumentada e teste '
 'da tecnica em quatro casos (texto truncado no CSV apos "four diffe..."). ',
 'DISCUSSAO: B1 saida e diagrama de sequencia UML nomeado no titulo e no resumo. B2 origem e LLM generativo; '
 'o grafo e mecanismo de recuperacao de contexto, nao substitui a autoridade semantica do modelo. B3 direcao '
 'e SRS para UML. B4 entrada e documento textual de requisitos, o caso canonico do escopo fixado. Acuracia '
 'e declarada como desfecho medido. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Conferir no texto completo qual instrumento sustenta '
 'a acuracia reportada, pois o resumo esta truncado no CSV.'),

'914_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo propoe usar LLMs para gerar OCL (Object Constraint Language) a partir de linguagem '
 'natural, com prompting baseado em esquema e reparos baseados em DSL, para garantia de qualidade centrada '
 'em processo em dominios criticos de seguranca. Avalia seis LLMs, aponta o1-mini e Codestral como '
 'melhores, e reporta que os reparos automaticos tornam executaveis entre 22% e 44% das restricoes OCL '
 'geradas que de outro modo permaneceriam nao executaveis por erro. Declara explicitamente: "Unlike prior '
 'work focused on UML models, this work applies OCL to software process QA". ',
 'DISCUSSAO: B2, B3 e B4 nao excluem: LLM generativo, direcao de texto em linguagem natural para artefato '
 'formal, entrada textual de requisitos regulatorios. Toda a decisao recai sobre B1, e ela depende de uma '
 'questao de protocolo ainda aberta: OCL conta como conteudo UML para I5? Este registro e mais dificil que '
 'os anteriores porque a propria OCL aqui nao esta ancorada em modelo UML algum, e o texto se afasta '
 'explicitamente dessa tradicao. Ainda assim, se a resposta a questao pendente for que OCL integra a '
 'especificacao UML da OMG e portanto conta como conteudo UML, este trabalho seria retido. Pela regra de '
 'ouro 1, incerteza retem, e nao antecipo a resposta excluindo agora. ',
 'DECISAO: retido no Portao B com flag INCERTO_SAIDA; EVIDENCIA=EXPLICITA pelas taxas de executabilidade '
 'reportadas. Quarto registro do agrupamento OCL, junto de 758_SCOPUS, 518_IEEE e 872_SCOPUS, e o caso '
 'extremo do agrupamento: se a questao for respondida admitindo OCL apenas quando ancorada em modelo UML, '
 'este sai e os outros tres permanecem.'),

'917_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo introduz a UM1NN, uma nova linguagem de modelagem para redes neurais, e declara que '
 '"traditional universal system modeling languages like UML and SysML fall short when it comes to neural '
 'network modeling". A contribuicao e a linguagem em si, com descricao detalhada e duas demonstracoes de '
 'uso: descrever o GPT-2 e definir seu fine-tuning para Question-Answering. ',
 'DISCUSSAO: B1 explica sem residuo. UML e SysML aparecem como termo de contraste e insuficiencia declarada, '
 'nao como produto. A UM1NN nao e perfil de UML nem reusa o metamodelo, ao contrario da SysML v1, entao a '
 'regra de separabilidade de perfil nao se aplica. Alem disso nao ha LLM gerando modelo: o GPT-2 e o '
 'sistema descrito pela linguagem, nao o gerador da descricao, o que tambem levaria a E6 em B2 caso o caso '
 'sobrevivesse a B1. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'918_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o resumo investiga o GPT-4 e o plugin Diagrams Show Me, que usa sintaxe Mermaid, para gerar os '
 'diagramas de sequencia, atividade, estado, atividade UML, IDEF0 e DoDAF OV-5b a partir de um mesmo estudo '
 'de caso, permitindo comparacao entre tipos. Investiga tambem o efeito de parafrasear a descricao do caso '
 'sobre compreensao de texto e identificacao de entidades. Resultados qualitativos: a visualizacao teve '
 'desempenho competente em formas simples (sequencia, atividade, estado) e os leiautes mudaram visivelmente '
 'apos a parafrase, ficando mais lineares e menos adequados a arquitetura de sistemas. ',
 'DISCUSSAO: B1 saida nomeia tipos de diagrama do metamodelo UML (sequencia, atividade, estado), entao nao e '
 'o terceiro caso de B1: a sintaxe Mermaid e apenas portadora e o tipo esta declarado. B2 origem e GPT-4. B3 '
 'direcao e descricao textual do caso para diagrama. B4 entrada e a descricao do estudo de caso, textual. '
 'Nenhum portao exclui. Duas ressalvas: os diagramas UML sao produzidos junto com IDEF0 e DoDAF OV-5b e os '
 'resultados podem ser reportados de forma agregada, o que e a hipotese exata de E10; e a avaliacao e '
 'declaradamente qualitativa, sem metrica. Pela regra de ouro 2 nenhuma das duas exclui aqui. ',
 'DECISAO: retido no Portao B; flags CANDIDATO_E10 e EVIDENCIA=A_VERIFICAR. No texto completo verificar se '
 'os resultados por tipo de diagrama UML sao separaveis dos das notacoes nao UML.'),

'921_SCOPUS':('B4_E9','',
 'EVIDENCIA: o resumo propoe geracao automatizada de Descricoes de Arquitetura de Software a partir de '
 'codigo-fonte, combinando engenharia reversa com LLM. Recupera visao estatica e comportamental extraindo '
 'diagrama de componentes abrangente, filtra componentes centrais por analise guiada por prompt do LLM e '
 'gera diagramas de maquina de estados para modelar o comportamento dos componentes com base na logica do '
 'codigo. Demonstrado com exemplos em C++. ',
 'DISCUSSAO: B1 nao exclui, o produto e conteudo UML nomeado (componentes e maquina de estados). B2 nao '
 'exclui, o LLM tem autoridade semantica sobre a filtragem arquitetural e sobre as maquinas de estados '
 'geradas. B3 nao exclui, a direcao termina em UML. B4 explica sem residuo: a entrada e codigo-fonte C++, '
 'sem qualquer componente de especificacao textual de requisitos. E o caso de engenharia reversa que a '
 'delimitacao de escopo fixada em 2026-08-16 coloca fora, por I4. ',
 'DECISAO: excluido em B4 por E9. Exclusao onerosa, nomeada para recuperacao sem re-triagem caso I4 venha a '
 'ser emendado: e um dos casos mais limpos de engenharia reversa por LLM com UML como produto, ao lado de '
 '865_SCOPUS e 930_SCOPUS.'),

'922_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: estudo exploratorio sobre como LLMs auxiliam analistas novatos a criar tres tipos de modelos '
 'UML: modelos de casos de uso, diagramas de classes e diagramas de sequencia. Foram desenhadas tarefas de '
 'modelagem para 45 graduandos de um curso de modelagem de requisitos, com auxilio de LLMs. A analise foi '
 'feita sobre os relatorios de projeto dos alunos, concluindo que os LLMs podem auxiliar novatos mas tem '
 'deficiencias e limitacoes a considerar. ',
 'DISCUSSAO: B1 saida e UML com tres tipos nomeados. B2 origem e LLM generativo em papel de assistencia. B3 '
 'direcao e tarefa de modelagem de requisitos para UML, nao avaliacao de diagrama preexistente, o que o '
 'separa do agrupamento B3_E8 de retorno formativo (753, 765, 771, 784, 807, 830, 838, 861, 891, 896): ali '
 'o LLM avalia UML de aluno, aqui o LLM ajuda a produzir. B4 entrada e o enunciado textual das tarefas. '
 'Ressalvas: o papel do LLM e declarado como "assist", sem isolar sua contribuicao da do aluno, e a '
 'evidencia vem de analise qualitativa de relatorios de projeto, sem metrica declarada no resumo. ',
 'DECISAO: retido no Portao B; flags INCERTO_PAPEL_LLM e EVIDENCIA=A_VERIFICAR. Mesmo perfil de 907_SCOPUS '
 'e 924_SCOPUS: co-producao humano-LLM em cenario educacional, a ser reexaminada no texto completo.'),

'923_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o resumo propoe abordagem dirigida a testes para refinar especificacoes de casos de uso UML '
 'com LLMs, sincronizando requisitos em linguagem natural, especificacoes UML e casos de teste. Introduz '
 'formato estruturado que permite ao LLM transformar requisitos ambiguos em especificacoes de casos de uso '
 'precisas e conformes a UML, das quais casos de teste sao gerados automaticamente; modificacoes nos testes '
 'sao propagadas de volta as especificacoes, em laco iterativo de consistencia bidirecional. Avaliacao '
 'experimental em dois projetos reais. O resumo declara que "UML use case specifications use textual '
 'descriptions to define scenarios and behaviors". ',
 'DISCUSSAO: B2 nao exclui, o LLM transforma e refina com autoridade semantica. B4 nao exclui, a entrada e '
 'requisito em linguagem natural. B3 exige cuidado: ha um ramo especificacao para casos de teste, que '
 'isolado seria a celula "UML existente -> LLM -> testes" e E7, mas o ramo constitutivo do trabalho e '
 'requisitos ambiguos para especificacao de caso de uso, e o produto refinado ao longo do laco e a propria '
 'especificacao, nao o teste. B1 e o ponto aberto: o produto e a descricao textual do caso de uso, nao o '
 'diagrama, e a questao de protocolo sobre descricao textual de caso de uso continua sem decisao. Pela '
 'regra de ouro 1, incerteza retem. ',
 'DECISAO: retido no Portao B com flag INCERTO_SAIDA; EVIDENCIA=A_VERIFICAR, pois "precisas" e "consistencia '
 'bidirecional" sao afirmacoes sem instrumento declarado no resumo. Terceiro registro do agrupamento de '
 'descricao textual de caso de uso, junto de 871_SCOPUS e 837_SCOPUS.'),

'924_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: investigacao preliminar sobre uso de LLM em fluxo tradicional de engenharia de sistemas. '
 'Engenheiros de sistemas foram incumbidos de criar uma lista de requisitos e um diagrama de casos de uso '
 'para atender a um cenario de sistema de sistemas apresentado em documento de proposta, modelando um '
 'ambiente de saude. Tres grupos: acesso aberto a um LLM, recebimento de material preliminar gerado por LLM, '
 'e fluxo normal sem LLM. Um especialista avaliador pontuou cada modelo segundo completude, consistencia, '
 'corretude, simplicidade e rastreabilidade. ',
 'DISCUSSAO: B1 saida e diagrama de casos de uso, tipo do metamodelo UML. B2 origem inclui conteudo gerado '
 'por LLM em dois dos tres bracos. B3 direcao e do documento de proposta para o modelo. B4 entrada e cenario '
 'textual de usuario, dentro do escopo. Nenhum portao exclui. O desenho e o mais forte deste lote quanto a '
 'atribuicao: o terceiro braco e controle sem LLM, o que permite comparar a qualidade do modelo com e sem '
 'assistencia, e as cinco dimensoes pontuadas sao vocabulario literal de I6. Mantenho INCERTO_PAPEL_LLM '
 'porque o artefato final e sempre revisado pelo engenheiro humano. ',
 'DECISAO: retido no Portao B; flags INCERTO_PAPEL_LLM e EVIDENCIA=EXPLICITA. Registro de nucleo para a '
 'extracao, por ter grupo de controle e rubrica de qualidade multidimensional.'),

'925_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: apresenta o NOMAD, framework multiagente modular que decompoe a geracao de UML em subtarefas '
 'especializadas por papel (extracao de entidades, classificacao de relacionamentos, sintese de diagrama), a '
 'partir de requisitos em linguagem natural. Avaliacao de desenho misto: estudo de caso amplo (Northwind) '
 'para sondagem e analise de erros, e exercicios UML de autoria humana para amplitude. NOMAD supera todas as '
 'baselines selecionadas, com desafio persistente na extracao de atributos de granularidade fina. Introduz '
 '"the first systematic taxonomy of errors in LLM-generated UML diagrams", categorizando erros estruturais, '
 'de relacionamento e logicos, e examina verificacao como sonda de projeto. ',
 'DISCUSSAO: B1 saida e diagrama de classes UML. B2 origem e sistema multiagente de LLMs, com autoridade '
 'semantica plena. B3 direcao e requisitos para UML. B4 entrada e requisitos em linguagem natural. Nenhum '
 'portao exclui. A taxonomia de erros em UML gerada por LLM e exatamente o tipo de evidencia extraivel que '
 'I6 exige, e provavelmente sera insumo direto da sintese, nao apenas um registro incluido. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Prioridade alta na leitura de texto completo, ao '
 'lado de 521_IEEE, pela taxonomia de erros.'),

'926_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: compara dois pipelines dirigidos por GPT-4 para transformar user stories em diagramas de '
 'sequencia: o pipeline A converte diretamente e o pipeline B insere etapa intermediaria de geracao de '
 'cenarios de caso de uso. Dez user stories foram processadas nos dois pipelines e avaliadas quanto a '
 'acuracia, clareza, eficiencia e escalabilidade. O pipeline B melhorou significativamente a qualidade e o '
 'detalhamento dos diagramas de sequencia, mantendo consistencia logica e reduzindo ambiguidade. ',
 'DISCUSSAO: B1 saida e diagrama de sequencia UML. B2 origem e GPT-4. B3 direcao e user story para UML. B4 '
 'entrada e user story, item nomeado literalmente na delimitacao de escopo fixada pela pesquisadora. Nenhum '
 'portao exclui. O cenario de caso de uso e etapa intermediaria interna ao pipeline, nao insumo preexistente, '
 'portanto nao ha UML na entrada e B3 nao se aplica. Acuracia, clareza e consistencia logica sao vocabulario '
 'de I6, com comparacao entre dois tratamentos. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Amostra pequena (dez user stories) a registrar na '
 'avaliacao de qualidade do estudo, nao na triagem.'),

'927_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: apresenta o Structura-AI, aplicacao web que cria diagramas UML a partir de instrucoes em '
 'linguagem natural, com front-end React.js, back-end Flask e renderizacao por Graphviz, apoiada em NLP '
 'baseada em GPT via API g4f, que interpreta a intencao do usuario e produz a sintaxe especifica do '
 'diagrama. Resultados declarados: queda significativa do trabalho manual, "user-reported accuracy of 95%" '
 'e tempo medio de geracao abaixo de 20 segundos. KW inclui Class Diagram, Sequence Diagram e Code-to-UML. ',
 'DISCUSSAO: B1 saida e UML com tipos nomeados em KW. B2 origem e modelo GPT com autoridade semantica sobre '
 'a intencao interpretada e a sintaxe produzida. B3 direcao e instrucao em linguagem natural para diagrama; '
 '"Code-to-UML" aparece so em KW, sem correspondencia no corpo do resumo, e nao muda a direcao declarada. '
 'B4 entrada e instrucao textual. Nenhum portao exclui. A acuracia de 95% e autorreportada pelos usuarios, '
 'instrumento fraco, e o resumo mistura resultado de produto com metrica de engenharia (tempo de geracao). ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=A_VERIFICAR. No texto completo verificar se ha instrumento de '
 'qualidade do diagrama alem da percepcao do usuario; caso contrario e candidato a E11.'),

'930_SCOPUS':('B4_E9','',
 'EVIDENCIA: o resumo propoe framework em que LLMs como ChatGPT e Claude automatizam a transformacao '
 'bidirecional entre codigo e diagramas, usando PlantUML e TikZ, com Neo4j para recuperacao em linguagem '
 'natural e consultas Cypher, visando depuracao, documentacao e versionamento de bases de codigo extensas. '
 'KW: C4, Code as Diagrams, Diagrams as Code, PlantUML, TikZ. Casos de uso qualitativos iniciais. ',
 'DISCUSSAO: B1 e delicado: PlantUML e TikZ sao sintaxe portadora e C4 nao pertence ao metamodelo UML; '
 'nenhum tipo de diagrama UML e nomeado, o que a primeira vista seria o terceiro caso de B1 e levaria a '
 'reter com INCERTO_SAIDA. Aplico a regra de ouro 3 e desco ate o portao que explica sem residuo. B4: o '
 'problema declarado e base de codigo extensa, dificil de navegar e documentar, e a entrada da direcao "code '
 'as diagrams" e o proprio codigo-fonte; nao ha em nenhuma leitura especificacao textual de requisitos, '
 'user story ou descricao de dominio na entrada. A recuperacao em linguagem natural via Neo4j e consulta '
 'sobre o repositorio consolidado, nao especificacao de origem. Sob qualquer leitura de B1, portanto, o '
 'registro sai em B4, o que torna o desfecho estavel. ',
 'DECISAO: excluido em B4 por E9. Mesmo padrao de 921_SCOPUS e 865_SCOPUS, nomeado para recuperacao sem '
 're-triagem caso I4 seja emendado.'),

'931_SCOPUS':('B3_E7','',
 'EVIDENCIA: o resumo propoe transformacoes modelo-para-texto/codigo com LLMs e pipelines RAG para software '
 'quantico e hibrido, e valida a ideia de "generating code out of UML model instances of software systems", '
 'produzindo codigo Python com a biblioteca Qiskit. O pipeline RAG incorpora codigo Qiskit de repositorios '
 'publicos do GitHub. Resultado medido: prompts bem construidos melhoram o CodeBLEU em ate quatro vezes. ',
 'DISCUSSAO: B1 nao exclui, ha UML no caso. B2 nao exclui, o LLM e generativo. B3 explica sem residuo: a '
 'direcao e a celula "UML existente -> LLM -> codigo" da secao 4.3 do manual. As instancias de modelo UML '
 'sao insumo dado e o produto avaliado e codigo quantico, medido por CodeBLEU, metrica de similaridade de '
 'codigo. Nenhuma qualidade de conteudo UML e medida. ',
 'DECISAO: excluido em B3 por E7. Nao satisfaz I5. Preservada no desfecho a distincao em relacao a B1_E7: '
 'aqui havia UML, mas na entrada.'),

'933_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: propoe framework multiagente com humano no laco para transformar requisitos em linguagem '
 'natural em diagramas de casos de uso e cenarios estruturados. Emprega um Requirement Parsing Agent para '
 'extrair atores e casos de uso e um Scenario Generation Agent para produzir e avaliar cenarios por '
 'mecanismo de multiplos juizes que afere completude, corretude e relevancia. Validacao humana integrada em '
 'etapas-chave para garantir alinhamento estrutural e semantico. Avaliacao em multiplos sistemas mostra '
 'cobertura de elementos e identificacao de relacionamentos melhores que ferramentas comerciais. ',
 'DISCUSSAO: B1 saida e diagrama de casos de uso, tipo do metamodelo UML. B2 origem e sistema multiagente de '
 'LLMs; o Requirement Parsing Agent extrai atores e casos de uso, mas por RF-01 e RF-02 o que decide e que a '
 'extracao aqui e feita por agentes generativos com autoridade semantica sobre o conteudo do diagrama, nao '
 'por NER treinado, o que o separa de 911_SCOPUS e 841_SCOPUS. B3 direcao e requisitos para UML. B4 entrada '
 'e requisito em linguagem natural. Completude, corretude e relevancia sao vocabulario de I6, com '
 'comparacao contra ferramentas comerciais como baseline. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. O mecanismo de multiplos juizes por LLM e a '
 'validacao humana devem ser examinados no texto completo como instrumento de medida, nao como resultado.'),
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
NOTA=('Sexto lote da triagem do Portao B sobre os registros que mencionam UML em titulo ou resumo '
 '(indices 120 a 143 da ordem de leitura). 24 registros decididos: 14 retidos, 3 B1_E7, 3 B2_E6, '
 '2 B3_E7, 2 B4_E9. Nenhum B3_E8 neste lote. '
 'Padroes consolidados: (a) notacao adjacente gerada por LLM e medida com vocabulario de qualidade mas '
 'fora do metamodelo UML sai em B1 — Event Storming (905) junta-se a arvore de falhas (759), diagrama de '
 'componentes de neurociencia (781) e mapas conceituais (895); (b) engenharia reversa por LLM com UML como '
 'produto sai em B4 — 921 (codigo C++ para diagrama de componentes e maquina de estados) e 930 '
 '(transformacao bidirecional codigo-diagrama), ambos nomeados para recuperacao sem re-triagem junto de '
 '865; (c) RF-01 aplicada de novo a NER e a pipeline simbolico — 911 (corpus IOB para treinar NER) e 901 '
 '(POS tagging, NLTK e gramatica de estrutura sintagmatica, com LLM apenas na motivacao) saem em B2, '
 'alinhados a 841 e contrastados com 933, cujo agente de parsing e generativo. '
 'Agrupamento novo de co-producao humano-LLM: 907, 922 e 924 medem qualidade de modelo produzido em '
 'conjunto por estudante ou engenheiro e LLM. Todos retidos com INCERTO_PAPEL_LLM. 924 e o mais forte por '
 'ter braco de controle sem LLM e rubrica de cinco dimensoes. Distinguem-se do agrupamento B3_E8 de retorno '
 'formativo porque ali o LLM avalia UML de terceiro e aqui ele ajuda a produzir. '
 'Questoes de protocolo pendentes ganharam registros: 914 e o quarto caso de OCL (com 758, 518 e 872) e o '
 'mais extremo, pois a OCL gerada nem sequer esta ancorada em modelo UML; 923 e o terceiro caso de '
 'descricao textual de caso de uso (com 871 e 837). Ambos retidos pela regra de ouro 1. '
 'Registros de nucleo identificados para a extracao: 925 (NOMAD, primeira taxonomia sistematica de erros em '
 'UML gerada por LLM), 898 (corretude sintatica, semantica e pragmatica com solucao de referencia), 924 '
 '(grupo de controle e rubrica multidimensional), 933, 926, 912 e 913.')
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow([';'.join(sorted(D)),AGORA,REV,'DECISAO_GATE','B','','',NOTA,
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
