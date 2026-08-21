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
'758_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo abre definindo a OCL como linguagem declarativa que acrescenta restricoes e '
 'expressoes de consulta a modelos MOF, e afirma que "OCL can provide precision and conciseness to '
 'UML models". Os autores compilaram conjunto de 15 MODELOS UML e 168 especificacoes, montaram '
 'manualmente um gabarito de prompt com lacunas a preencher COM A INFORMACAO UML DOS MODELOS, e '
 'investigaram a confiabilidade das restricoes OCL geradas pelo Codex a partir de especificacoes em '
 'linguagem natural, em regimes zero-shot e few-shot. A avaliacao mede validade sintatica e acuracia '
 'de execucao, e ainda a similaridade de cosseno entre embeddings das restricoes geradas e das '
 'escritas por humanos. ',
 'DISCUSSAO: B2, B3 e B4 passam: o Codex e LLM nomeado com autoridade semantica sobre as restricoes '
 'produzidas, a direcao e especificacao em linguagem natural -> artefato, e a entrada e textual (o '
 'modelo UML entra no prompt como CONTEXTO, nao como fonte a ser transformada). O B1 e que fica em '
 'suspenso, e a duvida e de fronteira do protocolo, nao de leitura. O artefato produzido e restricao '
 'OCL. A OCL e norma da OMG companheira da UML, e a especificacao da UML a incorpora como mecanismo '
 'de expressao de restricoes sobre elementos do modelo; nesse sentido a restricao OCL E conteudo '
 'semantico portador de significado ANEXO a um diagrama UML. Por outro lado, a OCL nao e diagrama, e '
 'a tabela da secao 4.1 do manual, que fixa o que conta como UML, nao a arrola. Pela regra de ouro 1, '
 'a incerteza retem. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_SAIDA. Flag EVIDENCIA=EXPLICITA porque validade '
 'sintatica, acuracia de execucao e similaridade com o artefato humano sao metricas declaradas sobre '
 'a saida. QUESTAO DE PROTOCOLO A DECIDIR, em conjunto com 518_IEEE, que apresenta o mesmo problema: '
 'restricao OCL conta como conteudo UML para efeito do I5? A resposta afeta um conjunto de registros '
 'e deve ser fixada em evento de INTERPRETACAO_PROTOCOLO antes da extracao. '),

'760_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo anuncia ferramenta interativa para esclarecer e gerar modelos UML com base em '
 'LLMs. O resumo parte da constatacao de que a modelagem UML manual e demorada e propensa a erro, '
 'critica as abordagens existentes por dependerem de metodos indiretos como analise de PlantUML, e '
 'apresenta o AUG, movido pelo modelo GLM4UML, para automatizar a modelagem UML, PARTICULARMENTE '
 'DIAGRAMAS DE CLASSES, DE CASOS DE USO E DE SEQUENCIA. A ferramenta integra edicao dinamica, '
 'AVALIACAO DE QUALIDADE e mecanismos de realimentacao, compondo um paradigma automatizado de '
 'avaliacao e otimizacao. "quality assessment" consta das palavras-chave. ',
 'DISCUSSAO: os quatro subportoes passam sem ressalva. B1: tres tipos de diagrama do metamodelo UML '
 'sao nomeados expressamente, o que afasta qualquer duvida de saida. B2: o GLM4UML e modelo de '
 'linguagem ajustado, com autoridade semantica sobre os elementos. B3: requisitos -> LLM -> UML, a '
 'primeira linha da matriz da secao 4.3. B4: a entrada e requisitos em linguagem natural. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: a '
 'avaliacao de qualidade nao e mencao incidental, e componente arquitetural declarado da ferramenta e '
 'palavra-chave dos autores. Candidato central da revisao. '),

'761_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o resumo apresenta metodo de ensino de engenharia de software com o ChatGPT. A frase '
 'decisiva descreve o papel do LLM: "The approach involves ChatGPT assisting in collecting user '
 'stories, creating a USE CASE AND CLASS DIAGRAMS, and formulating SEQUENCE DIAGRAMS". A estrategia e '
 'agil, centrada em user stories selecionadas, e estimula a interacao do estudante com o ChatGPT. ',
 'DISCUSSAO: os quatro subportoes passam. B1: tres tipos de diagrama do metamodelo UML sao nomeados. '
 'B2: o ChatGPT cria os diagramas, detendo autoridade semantica sobre os elementos. B3: a direcao e '
 'user stories -> LLM -> UML, a primeira linha da matriz da secao 4.3, com as user stories nomeadas '
 'expressamente na delimitacao de escopo como entrada admissivel. B4: entrada textual. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flags CANDIDATO_E10, porque o '
 'proposito declarado e pedagogico e o desenho pode nao produzir evidencia sistematica sobre o '
 'artefato, e EVIDENCIA=A_VERIFICAR, porque o resumo nao declara metrica. Pela regra de ouro 2, '
 'ausencia de vocabulario de qualidade nunca exclui nesta etapa, e o E10 nao e decidivel por titulo e '
 'resumo. PAUTA DE LEITURA: ha avaliacao dos diagramas gerados, ou apenas relato de experiencia '
 'didatica? '),

'762_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo anuncia geracao de diagramas de classes com casos de teste apoiada por LLM. O '
 'resumo declara que consultas em linguagem natural sao o ponto de partida para gerar um diagrama de '
 'classes, aplicavel quando o diagrama modela os dados que devem estar disponiveis no banco de dados '
 'de um sistema de informacao, e que se pretende entregar as partes interessadas tanto o diagrama de '
 'classes quanto casos de teste tipicos. As palavras-chave declaram LLM, consultas em linguagem '
 'natural, PlantUML e diagrama de classes UML. ',
 'DISCUSSAO: os quatro subportoes passam. B1: diagrama de classes UML, tipo nomeado do metamodelo, com '
 'o PlantUML como sintaxe portadora e o tipo declarado, o que afasta o terceiro caso do B1. Os casos '
 'de teste sao saida ADICIONAL, e o componente UML e separavel, conforme admite a definicao '
 'operacional do protocolo. B2: LLM com autoridade semantica. B3: consultas em linguagem natural -> '
 'LLM -> UML. B4: entrada textual. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=A_VERIFICAR: o '
 'resumo nao declara metrica sobre o diagrama gerado. PAUTA DE LEITURA: ha avaliacao do diagrama de '
 'classes, ou a validacao se da apenas pelos casos de teste? '),

'769_SCOPUS':('PASSOU','INCERTO_SAIDA;INCERTO_ENTRADA',
 'EVIDENCIA: o resumo examina como assistir a modelagem em engenharia de sistemas com IA generativa e '
 'GPT-4, e descreve DOIS caminhos. No primeiro, o GPT-4 e customizado com um METAMODELO DE ATIVIDADE '
 'especificado em Eclipse Ecore, ou com DIAGRAMAS DE ATIVIDADE PREDEFINIDOS codificados em formato '
 'textual, para aprender a partir de instancias. No segundo, o texto descritivo produzido pelo LLM '
 'alimenta um analisador sintatico, resultando numa atividade transformavel em modelo DEVS com '
 'capacidade de simulacao. O fecho declara que a abordagem e demonstrada com diagramas de atividade e '
 'de fluxo "in a manner applicable to SysML, UML, and systems engineering at large". ',
 'DISCUSSAO: B2 passa, o GPT-4 e nomeado. B1 e B4 ficam ambos em suspenso, e por razoes distintas. No '
 'B1, o artefato final do segundo caminho e um modelo DEVS, formalismo de simulacao de eventos '
 'discretos que nao e UML e cuja presenca isolada levaria a E7; mas ha diagrama de atividade no '
 'percurso, tipo nomeado do metamodelo UML, e o proprio resumo declara aplicabilidade a UML, de modo '
 'que pode haver componente UML separavel. No B4, a entrada do primeiro caminho e metamodelo Ecore ou '
 'diagramas de atividade PREEXISTENTES, o que pela delimitacao de escopo levaria a E9; ja o cenario '
 'descrito ao final parte de "a simplified text describing a generic process", entrada textual '
 'admissivel. O resumo nao permite fixar qual configuracao e a central do trabalho. Pela regra de ouro '
 '1, a incerteza retem, e a regra de ouro 3 nao socorre porque nenhum dos dois portoes explica '
 'CLARAMENTE o caso. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_SAIDA e INCERTO_ENTRADA. PAUTA DE LEITURA: (1) o '
 'artefato avaliado e o diagrama de atividade UML ou o modelo DEVS? (2) a entrada e texto descritivo '
 'ou metamodelo e diagramas preexistentes? A combinacao "DEVS a partir de modelo preexistente" leva a '
 'exclusao; a combinacao "diagrama de atividade a partir de texto" mantem no escopo. '),

'773_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo e literalmente o objeto da revisao — "Evaluating the Quality of Class Diagrams '
 'Created by a Generative AI: Findings, Guidelines and Automation Options". O resumo declara tres '
 'objetivos: analisar o trabalho cientifico anterior para sumarizar os achados sobre a qualidade de '
 'diagramas de classes gerados por IA, relatar TESTES PROPRIOS realizados pelos autores, e a partir '
 'dai oferecer diretrizes para avaliacao manual de qualidade e discutir opcoes de automacao dessa '
 'avaliacao. As palavras-chave declaram ChatGPT, diagrama de classes, modelagem de dominio, PlantUML e '
 '"Quality Checking". ',
 'DISCUSSAO: os quatro subportoes passam. B1: diagrama de classes. B2: o ChatGPT e nomeado. B3: '
 'requisitos -> LLM -> UML. B4: entrada textual de dominio. Registre-se uma ressalva que NAO decide '
 'nesta etapa: o trabalho tem componente de sintese da literatura, o que suscitaria o E2 como estudo '
 'secundario; mas o resumo afirma expressamente que "Own tests were carried out too", havendo '
 'portanto componente primario, e de todo modo o Portao A ja foi vencido por este registro e o E2 nao '
 'se decide no Portao B. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: a '
 'qualidade e o objeto declarado no titulo. Candidato central e, pela natureza mista, provavel fonte '
 'de instrumentos de avaliacao reaproveitaveis na extracao. PAUTA DE LEITURA: verificar a proporcao '
 'entre sintese secundaria e teste proprio, para decidir eventual E2 no texto completo. '),

'788_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;CANDIDATO_E10',
 'EVIDENCIA: o resumo relata experimento controlado com 56 participantes sobre o papel do ChatGPT em '
 'disciplina introdutoria de programacao. A tarefa e descrita assim: "Participants were tasked with '
 'CREATING A UML DIAGRAM and subsequently implementing its design through programming", seguida de '
 'pos-avaliacao com consulta fechada e questionario. Todo o processo foi gravado em tela. As variaveis '
 'declaradas sao resultados de aprendizagem e comportamento dos estudantes. ',
 'DISCUSSAO: B1 passa, ha diagrama UML na tarefa, embora o tipo nao seja nomeado. O B2 e que fica em '
 'suspenso. O resumo nao diz se o diagrama UML foi produzido PELO ChatGPT, com o estudante conduzindo, '
 'ou PELO ESTUDANTE, com o ChatGPT auxiliando em outra parte da tarefa. Pela RF-02, so ha I2 '
 'satisfeito se o LLM detiver autoridade semantica sobre os elementos do diagrama; na segunda '
 'hipotese, o desfecho seria E6. Como se trata de experimento controlado com gravacao de tela, o texto '
 'completo certamente resolve. Pela regra de ouro 1, a incerteza retem. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_PAPEL_LLM. Flag CANDIDATO_E10 porque a variavel medida '
 'declarada e desempenho de aprendizagem e comportamento, e nao propriedade do diagrama; o E10, '
 'porem, nao e decidivel por titulo e resumo, e pela regra de ouro 2 a ausencia de vocabulario de '
 'qualidade do artefato nunca exclui nesta etapa. PAUTA DE LEITURA: quem produziu o diagrama UML, e '
 'alguma propriedade dele foi medida? '),

'789_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo apresenta pipeline ponta a ponta que automatiza a geracao E A AVALIACAO '
 'MULTIMODAL de diagramas de OBJETOS e de SEQUENCIA UML. Um LLM leve sintetiza descricoes realistas de '
 'funcionalidades de software; em seguida o DeepSeek-R1-Distill-Qwen-32B traduz essas descricoes em '
 'codigo PlantUML. A contribuicao central declarada e o arcabouco de avaliacao multimodal, que usa '
 'conjunto de tres modelos de visao e linguagem (Qwen2.5-VL, LLaMA-3.2-11B-Vision e Aya-Vision) para '
 'aferir a fidelidade diagramatica. Os resultados distinguem perfis de geracao — diagramas de objetos '
 'com alta competencia e baixa variabilidade, diagramas de sequencia com desfecho polarizado — e os '
 'escores dos VLMs mostram correlacao estatisticamente significativa com julgamentos de 155 '
 'especialistas humanos. ',
 'DISCUSSAO: os quatro subportoes passam sem ressalva. B1: diagramas de objetos e de sequencia, dois '
 'tipos nomeados do metamodelo UML, com PlantUML como sintaxe portadora e o tipo declarado. B2: LLMs '
 'nomeados com autoridade semantica. B3: descricao textual -> LLM -> UML. B4: a entrada e descricao '
 'textual de funcionalidade; o fato de essa descricao ser ela propria sintetizada por um LLM leve nao '
 'a descaracteriza como especificacao textual em linguagem natural, que e o que a delimitacao de '
 'escopo exige. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: ha '
 'metrica de fidelidade, comparacao entre tipos de diagrama e validacao contra 155 especialistas '
 'humanos. Candidato central da revisao, e dos mais fortes ate aqui, tanto pela comparacao entre tipos '
 'estruturais e comportamentais quanto pela validacao do proprio instrumento de avaliacao. '),

'791_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo descreve arcabouco que converte descricoes textuais de sistema em componentes '
 'SysML compativeis com o Papyrus, e a frase decisiva quanto a saida e esta: "Both pipelines output '
 'Papyrus standard .uml, .di, and .notation files". Sao apresentados dois caminhos de extracao, um '
 'baseado em regras com spaCy e outro baseado em LLM com consultas por engenharia de prompt ao GPT-4o. '
 'A avaliacao e extensa: modelo de referencia manual verificado, corpus sintetico de 100 sistemas '
 'aeroespaciais, motor de perturbacao que injeta ruido lexico, semantico e estrutural, metrica de '
 'Graph Edit Distance para fidelidade topologica alem do F1 por token, e laco agentico de '
 'autocorrecao. Reporta-se que o caminho por LLM entrega revocacao mais alta em estruturas de relacao '
 'complexas. ',
 'DISCUSSAO: os quatro subportoes passam. B1: a saida e SysML serializado em arquivos .uml do Papyrus, '
 'que implementa SysML v1; conforme fixado em evento de INTERPRETACAO_PROTOCOLO, o SysML v1 e PERFIL '
 'da UML e reusa o metamodelo, havendo portanto componente UML separavel — e aqui a propria extensao '
 'de arquivo o confirma. B2: o GPT-4o e nomeado; o caminho baseado em regras com spaCy e alternativa '
 'comparada, nao substituto, de modo que ha componente por LLM separavel e comparavel. B3: descricao '
 'textual -> LLM -> modelo. B4: a entrada sao documentos e descricoes textuais de sistema. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: Graph '
 'Edit Distance, F1, robustez a ruido e fidelidade topologica sao metricas declaradas sobre o artefato '
 'gerado. Candidato central, com o interesse adicional de comparar diretamente pipeline por LLM e '
 'pipeline por regras — desenho que informa a RF-02. PAUTA DE LEITURA: quais tipos de diagrama SysML '
 'sao gerados, e quais deles reusam o metamodelo UML. '),

'795_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o resumo, de artigo declarado work in progress, apresenta metodologia para integrar IA '
 'generativa no ensino de graduacao em engenharia de software, adotada em disciplinas panoramicas de '
 'multiplas instituicoes, com promessa substancial no ensino de conceitos de projeto e modelagem de '
 'software USANDO A UML. Afirma que as capacidades das ferramentas baseadas em LLM ainda sao LIMITADAS '
 'no que toca ao projeto de software, e que essas limitacoes nao devem ser vistas como impedimento — '
 'formulacao que sugere aproveitamento pedagogico das falhas. ',
 'DISCUSSAO: os quatro subportoes passam, ainda que com apoio modesto do resumo. B1: a UML e nomeada '
 'como notacao ensinada e produzida, embora o tipo de diagrama nao seja declarado. B2: as ferramentas '
 'sao baseadas em LLM. B3 e B4: a direcao e enunciado de projeto -> modelo, com entrada textual. ',
 'DECISAO DA PESQUISADORA: RETIDO. Flags CANDIDATO_E10, por ser work in progress de pratica '
 'inovadora, desenho que frequentemente nao produz evidencia sistematica, e EVIDENCIA=A_VERIFICAR, '
 'porque a afirmacao sobre limitacoes das ferramentas no projeto de software E juizo de qualidade, mas '
 'sem metrica declarada. Pela regra de ouro 2, isso nunca exclui nesta etapa. PAUTA DE LEITURA: as '
 'limitacoes relatadas foram caracterizadas sistematicamente, com algum instrumento, ou sao impressao '
 'docente? '),

'759_SCOPUS':('B1_E7','',
 'EVIDENCIA: o titulo declara geracao de ANALISE DE ARVORE DE FALHAS por IA generativa, com caso de '
 'uso de falha do sensor LIDAR em conducao autonoma. O resumo situa o trabalho em seguranca funcional '
 'automotiva, explora LLMs de codigo aberto e aprofunda-se em um deles para estudar suas respostas. As '
 'palavras-chave sao FMEA, FTA, seguranca funcional, IA generativa, hardware e software, e PlantUML. ',
 'DISCUSSAO: B1 decide. O artefato produzido e a arvore de falhas, notacao de analise de seguranca '
 'que nao integra o metamodelo UML e nao consta da tabela da secao 4.1 do manual. A palavra-chave '
 'PlantUML nao salva o registro: conforme fixado, o PlantUML e SINTAXE PORTADORA e nao notacao, e '
 'aqui o tipo de diagrama esta declarado sem ambiguidade — e arvore de falhas. Nao se aplica, '
 'portanto, o terceiro caso do B1 ("o resumo nao deixa claro qual notacao"), mas o segundo: saida '
 'explicitamente em outra notacao, sem componente UML separavel. A linha 174 do protocolo e expressa '
 'ao dizer que a saida em PlantUML so e elegivel quando se destina a codificar UML. Pela regra de ouro '
 '5, falha de saida e I5/E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Registre-se o padrao para o relato de '
 'metodo: PlantUML usado como ferramenta de desenho para notacao NAO-UML, caso que a leitura mecanica '
 'da palavra-chave classificaria erradamente como candidato. '),

'772_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo trata do mapeamento de entradas de listas de sinais de entrada e saida para '
 'blocos de funcao de controle em automacao industrial, tarefa dificil de automatizar por causa do '
 'formato nao padronizado das listas. A unica mencao a UML e retrospectiva e negativa: "Previous '
 'approaches proposed mapping of IO list contents to common data schemas, such as ontologies OR UML '
 'MODELS, but did not provide means to automate the initial data import from heterogeneous input '
 'formats". O proprio trabalho propoe o IO-AutoMapper, metodo apoiado em LLM, e as palavras-chave '
 'declaram IEC 61131-3 e geracao de logica de controle. ',
 'DISCUSSAO: B1 decide. A UML aparece na descricao do TRABALHO ALHEIO, como uma das opcoes que '
 'abordagens ANTERIORES adotaram, e nao como artefato produzido por este trabalho, cuja saida e o '
 'mapeamento de sinais para blocos de funcao e a logica de controle conforme a IEC 61131-3. Nao ha '
 'componente UML separavel a destacar. Trata-se de correspondencia por mencao a trabalho relacionado, '
 'padrao de falso positivo distinto dos ja documentados. Pela regra de ouro 5, falha de saida e I5/E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. '),

'775_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo trata da melhoria do atendimento automatizado ao cliente de operadora movel por '
 'sistema de recuperacao aumentada combinado a diferentes modelos de linguagem, com analise '
 'comparativa entre eles. O que o trabalho produz sao respostas de atendimento; nao ha artefato de '
 'modelagem entre os resultados. ',
 'DISCUSSAO: B1 decide: a saida nao e UML e nao ha componente UML separavel. O resumo e claro sobre o '
 'que o trabalho produz, de modo que nao se aplica o terceiro caso do B1. Pela regra de ouro 5, falha '
 'de saida e I5/E7, nao E6. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. '),

'778_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo situa o trabalho na modelagem MULTINIVEL e observa que, embora muitos estudos ja '
 'tenham investigado o uso de LLMs para construir modelos conceituais de DOIS NIVEIS, "such as UML '
 'class diagrams", nenhuma pesquisa ainda tratou do apoio a construcao de modelos conceituais '
 'multinivel. Relata entao experimentos com o ChatGPT para apoiar o RE-ENGENHARIA de modelos, e as '
 'palavras-chave declaram FMMLx, "model deepening" e modelagem multinivel. ',
 'DISCUSSAO: B1 decide, pelo seu SEGUNDO caso. A mencao a diagramas de classes UML e feita para situar '
 'o que a literatura ANTERIOR fez e para contrastar com o que ESTE trabalho faz: o artefato produzido '
 'e modelo multinivel em FMMLx, linguagem de modelagem multinivel autonoma que nao integra o '
 'metamodelo UML e nao consta da tabela da secao 4.1. Nao ha componente UML separavel no produto. '
 'Registre-se que o diagrama de classes UML pode comparecer como ENTRADA a ser aprofundada, o que '
 'levaria alternativamente a E9 em B4 pela delimitacao de escopo; mas pela regra de ouro 3 o criterio '
 'primario e o primeiro portao que explica claramente o caso, e esse e o B1, porque a saida em outra '
 'notacao esta declarada sem ambiguidade. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Registre-se que o tema — aprofundamento de '
 'modelo conceitual por LLM — e vizinho ao da revisao, e que a exclusao decorre da notacao de saida, '
 'nao do merito. '),

'781_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo propoe roteiro tecnologico para automatizar a criacao de uma Arquitetura de '
 'Referencia do Cerebro Inteira. A notacao empregada e nomeada com precisao: DIAGRAMAS DE FLUXO DE '
 'INFORMACAO CEREBRAL (BIF), baseados na anatomia mesoscopica do cerebro, e DIAGRAMAS DE COMPONENTES '
 'HIPOTETICOS (HCD) para as funcionalidades computacionais correspondentes. O LLM automatiza a '
 'construcao e a verificacao dessas estruturas, notadamente extraindo estruturas anatomicas de artigos '
 'cientificos. ',
 'DISCUSSAO: B1 decide, pelo seu segundo caso. As notacoes de saida sao BIF e HCD, formalismos '
 'especificos do dominio de neurociencia computacional, sem relacao com o metamodelo UML e ausentes da '
 'tabela da secao 4.1. A expressao "Hypothetical Component Diagram" nao designa o diagrama de '
 'componentes da UML, e a coincidencia parcial de nome e armadilha lexical. Nao ha componente UML '
 'separavel. Pela regra de ouro 5, falha de saida e I5/E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Registre-se a armadilha lexical '
 '"component diagram" em acepcao alheia a UML. '),

'794_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo trata de alucinacao de agentes de LLM em tarefas de decisao de horizonte longo e '
 'propoe transformar o HISTORICO DE DECISAO em diagramas visuais, num arcabouco de fluxo duplo '
 'realcado visualmente. As palavras-chave declaram tomada de decisao, agentes de LLM, visao '
 'computacional e "Flowcharting". ',
 'DISCUSSAO: B1 decide. O artefato produzido e representacao visual do historico de decisao do agente, '
 'da familia do fluxograma, sem qualquer relacao com o metamodelo UML; nenhum tipo de diagrama UML e '
 'nomeado. O proposito e melhorar a decisao do agente, nao produzir modelo de software. Nao ha '
 'componente UML separavel. Pela regra de ouro 5, falha de saida e I5/E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. '),

'768_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo apresenta o FALAA, arcabouco que padroniza a DESCRICAO de arquiteturas de '
 'agentes de linguagem por um conjunto estruturado de componentes — Planner, Executor, Evaluator, '
 'Reflector, Memory e Environment — e por metodologia de dois niveis que combina DIAGRAMAS UML e '
 'ESPECIFICACOES OCL. O proposito declarado e dar clareza conceitual e precisao formal, permitindo '
 'definicoes inequivocas de comportamento de agente e tornando as arquiteturas comparaveis, '
 'reproduziveis e extensiveis. ',
 'DISCUSSAO: o B1 passa com folga: ha diagramas UML e especificacoes OCL. O B2 decide. Os agentes de '
 'linguagem sao o OBJETO DESCRITO pelo arcabouco, e nao os autores dos diagramas: quem modela sao os '
 'pesquisadores, que propõem uma notacao padronizada para descrever arquiteturas alheias. Pela RF-02, '
 'a autoridade semantica sobre os elementos UML e integralmente humana; nenhum LLM propõe, gera ou '
 'revisa elemento portador de significado. E o caso, distinto e recorrente, em que o LLM e o TEMA do '
 'artigo e nao o produtor do modelo. Pela regra de ouro 5, falha de origem e I2/E6, nao E7: a saida E '
 'UML, o que falta e o LLM na origem. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. Registre-se para o relato de metodo o '
 'padrao "LLM como objeto modelado, nao como modelador", que a busca por coocorrencia nao distingue. '),

'790_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo dedica-se ao desenvolvimento de arquitetura hibrida de software baseada em '
 'inteligencia artificial, USANDO DIAGRAMA DE CASOS DE USO da UML para modelar os requisitos '
 'funcionais do sistema; considera os diagramas de precedentes como ferramenta para identificar e '
 'formalizar interacoes entre usuarios e sistema. A essencia do enfoque hibrido, nas palavras do '
 'resumo, e que COMPONENTES DE INTELIGENCIA ARTIFICIAL SERAO USADOS para aumentar a capacidade do '
 'software. As palavras-chave declaram modelo de linguagem de grande porte, aprendizado de maquina e '
 'redes neurais ao lado de diagrama de casos de uso. ',
 'DISCUSSAO: o B1 passa, ha diagrama de casos de uso. O B2 decide. O modelo de linguagem e COMPONENTE '
 'DO SISTEMA PROJETADO, e nao produtor do modelo: os autores desenham o diagrama de casos de uso para '
 'especificar um sistema que, entre outras coisas, embarca IA. Pela RF-02, a autoridade semantica '
 'sobre os atores e casos de uso e dos autores. E o mesmo padrao ja decidido para 960_SCOPUS: '
 'coocorrencia de UML e LLM no mesmo resumo sem relacao produtiva entre eles, com a UML servindo de '
 'documentacao de projeto do sistema que hospeda o LLM. Pela regra de ouro 5, falha de origem e I2/E6. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. '),

'770_SCOPUS':('B3_E7','',
 'EVIDENCIA: o titulo e inequivoco quanto ao papel do LLM — "LLM as a CODE GENERATOR in Agile Model '
 'Driven Development". O resumo defende o desenvolvimento dirigido a modelos como estrategia para '
 'superar a ambiguidade das descricoes de software em linguagem natural, e propõe abordagem agil que '
 'emprega o GPT-4 como gerador de codigo a partir dos modelos. As palavras-chave declaram geracao de '
 'codigo por GPT-4, desenvolvimento dirigido a modelos, complexidade ciclomatica e LINGUAGEM DE '
 'RESTRICAO DE OBJETOS. ',
 'DISCUSSAO: B1 e B2 passam: ha modelos com restricoes OCL e ha o GPT-4. O B3 decide. A direcao e '
 'modelo EXISTENTE, enriquecido por OCL -> LLM -> codigo. O modelo e INSUMO e o produto e codigo, '
 'avaliado inclusive por complexidade ciclomatica, metrica de codigo e nao de modelo. E a terceira '
 'linha da matriz da secao 4.3, "UML existente -> LLM -> codigo, testes, documentacao", cujo desfecho '
 'e E7. Pela delimitacao de escopo fixada em 2026-08-16, UML como insumo para gerar codigo esta '
 'expressamente fora. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B3. O desfecho preserva o sub-portao: havia '
 'UML, mas na entrada, e o produto e codigo. '),

'765_SCOPUS':('B3_E8','',
 'EVIDENCIA: o resumo apresenta extensao do Athena, sistema aberto de realimentacao integrado a '
 'plataforma Artemis, para apoiar exercicios de modelagem com humano no laco. Abre reconhecendo que '
 '"Automated assessment of student modeling tasks is difficult to scale because UML DIAGRAMS ARE '
 'OPEN-ENDED, GRAPHICAL, AND HIGHLY CONTEXTUAL". Introduz o ApollonUML, representacao textual '
 'especifica de dominio que melhora a interpretabilidade pelo LLM preservando vinculos precisos com os '
 'elementos do diagrama, e, combinada a instrucoes de correcao em forma de rubrica, gera realimentacao '
 'contextualizada e pedagogicamente alinhada. As palavras-chave declaram realimentacao formativa e '
 'atribuicao de nota. ',
 'DISCUSSAO: B1 e B2 passam: ha diagramas UML e ha LLM operando sobre eles. O B3 decide. A direcao e '
 'diagrama UML JA EXISTENTE, produzido pelo ESTUDANTE -> LLM -> avaliacao e realimentacao. O UML e '
 'insumo e nao e alterado: o produto e nota e comentario pedagogico. E a segunda linha da matriz da '
 'secao 4.3, e a condicao restritiva da secao 3 para o E8 ("so exclui quando o resumo deixa claro que '
 'o diagrama ja existe e nao e alterado") esta plenamente satisfeita. A tabela da secao 4.2 e ainda '
 'mais direta ao arrolar "LLM apenas avalia ou explica um diagrama ja existente" com desfecho E8. Pela '
 'regra de ouro 5, falha de tarefa e I3/E8, e nao E6. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. '),

'771_SCOPUS':('B3_E8','',
 'EVIDENCIA: o titulo anuncia realimentacao por IA com recuperacao aumentada para o ensino de UML. O '
 'resumo declara continuidade de trabalho em curso sobre mecanismo de realimentacao dirigido por IA '
 'para APOIAR A CONSTRUCAO de diagramas UML, com aprimoramento do componente RAG-LLM dentro do plugin '
 'UML Miner ja existente. O sistema analisa o COMPORTAMENTO DE MODELAGEM DOS ESTUDANTES e oferece '
 'orientacao personalizada em tempo real. As palavras-chave declaram diagramas de classes UML e ensino '
 'de modelagem de software. ',
 'DISCUSSAO: B1 e B2 passam: ha diagramas de classes UML e ha LLM com RAG operando sobre eles. O B3 '
 'decide. A direcao e diagrama produzido PELO ESTUDANTE -> LLM -> orientacao e realimentacao. O LLM '
 'nao propõe nem gera elementos do diagrama: comenta o que o estudante fez. E a segunda linha da '
 'matriz da secao 4.3 e a linha expressa da tabela da secao 4.2, com desfecho E8. Este registro e da '
 'mesma linha de pesquisa de 753_SCOPUS, e recebe o mesmo desfecho, por coerencia. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. '),

'784_SCOPUS':('B3_E8','',
 'EVIDENCIA: o resumo apresenta middleware para tornar a realimentacao gerada por IA mais transparente '
 'e acionavel em contextos educacionais nos quais os ESTUDANTES CONSTROEM ITERATIVAMENTE artefatos '
 'estruturados, "such as UML diagrams". Diferentemente das abordagens que avaliam apenas o produto '
 'final, o sistema incorpora TRACOS COMPORTAMENTAIS para gerar realimentacao ancorada no processo do '
 'aprendiz, estruturada em quatro dimensoes: Evidencia Localizada, Pistas de Raciocinio, Alternativas '
 'Acionaveis e Traco Sensivel ao Processo. Integra mineracao de processos, analise estruturada de '
 'acoes e recuperacao aumentada. ',
 'DISCUSSAO: B1 e B2 passam. O B3 decide, pela mesma razao dos registros 753, 765 e 771: o diagrama '
 'UML e construido pelo ESTUDANTE e o LLM produz realimentacao sobre ele e sobre o processo que o '
 'gerou. Nada no conteudo UML e criado ou alterado pelo LLM. E a segunda linha da matriz da secao 4.3 '
 'e a linha expressa da tabela da secao 4.2, com desfecho E8. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. Registre-se que este e o quarto registro '
 'de um agrupamento tematico nitido — realimentacao automatizada para ensino de modelagem UML — que '
 'sai integralmente por E8 e que merece mencao no relato de metodo como subarea vizinha e ativa. '),

'763_SCOPUS':('B4_E9','',
 'EVIDENCIA: o titulo declara abordagem sistematica para DERIVAR modelos conceituais A PARTIR DE '
 'MODELOS BPMN. O resumo explicita a transicao: de modelos de processo de negocio, "typically '
 'represented as BPMN diagrams", para Modelos Conceituais, "represented as UML Class Diagrams", e '
 'atribui a dificuldade as diferencas intrinsecas entre as duas notacoes. As palavras-chave declaram '
 'BPMN, modelo conceitual, modelos de linguagem de grande porte e desenvolvimento dirigido a modelos. ',
 'DISCUSSAO: B1 passa, e passa bem: a SAIDA e diagrama de classes UML, tipo nomeado do metamodelo. B2 '
 'passa, ha LLMs declarados. B3 passa: o UML e PRODUTO, e nao insumo, de modo que nem o E8 nem o E7 de '
 'direcao se aplicam. O B4 e que decide. A entrada e MODELO BPMN JA EXISTENTE, e nao especificacao '
 'textual em linguagem natural. Pela delimitacao de escopo fixada em 2026-08-16, o objeto da revisao e '
 'a sintese direta de conteudo UML a partir de requisitos, user stories, cenarios ou descricoes '
 'textuais de dominio; e a secao 3 do manual admite o E9 quando o resumo declara explicitamente '
 'entrada de codigo, imagem, MODELO EXISTENTE ou logs, sem componente textual de requisitos — que e '
 'exatamente este caso. Trata-se de transformacao modelo-a-modelo. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E9, decidido em B4. Registre-se que este e um trabalho forte e '
 'no tema, cuja saida decorre exclusivamente da natureza da entrada; integra o conjunto de registros '
 'recuperaveis sem re-triagem caso o I4 venha a ser emendado para admitir modelo existente. '),

'774_SCOPUS':('B4_E9','',
 'EVIDENCIA: o resumo apresenta caso de uso educacional de criacao de material de avaliacao com o '
 'Chat-GPT 3.5 turbo, em duas frentes declaradas: "(a) alter specific aspects of a GENERIC DOMAIN '
 'MODEL (UML CLASS DIAGRAM)" e "(b) generate requirement texts (problem scenarios) that creatively '
 'describe the previously altered model". Os desafios nomeados sao alterar apenas as variaveis contidas '
 'no modelo generico de modo que o modelo resultante faca sentido, e gerar textos de requisitos que '
 'descrevam correta e criativamente o modelo alterado. ',
 'DISCUSSAO: B1 passa, ha diagrama de classes UML e ele e alterado, havendo portanto producao de '
 'conteudo UML. B2 passa, o Chat-GPT e nomeado. O B3 nao exclui: nao e E8, porque o modelo NAO '
 'permanece intacto — e justamente alterado —, e a condicao restritiva da secao 3 para o E8 exige que '
 'o diagrama "nao seja alterado". O B4 e que decide. A entrada e um MODELO DE DOMINIO GENERICO JA '
 'EXISTENTE, e a direcao da segunda frente e ate inversa a da revisao: do modelo PARA o texto de '
 'requisitos. Nao ha especificacao textual de origem: o texto e saida, nao entrada. Pela delimitacao '
 'de escopo e pela secao 3 do manual, entrada de modelo existente sem componente textual de requisitos '
 'leva a E9. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E9, decidido em B4. Registre-se que a exclusao NAO se apoia no '
 'B3, porque ha alteracao de conteudo UML; e o mesmo raciocinio ja aplicado a 215_ACM. '),
}

assert len(D)==24, len(D)
CRIT={'B1_E7':'E7','B2_E6':'E6','B3_E7':'E7','B3_E8':'E8','B4_E9':'E9'}

# ---- correcao de 753_SCOPUS: B2_E6 -> B3_E8
COR753=(
 'CORRECAO DE DESFECHO (%s): este registro fora decidido como E6 em B2, ao fundamento de que a '
 'autoridade semantica sobre os diagramas e dos estudantes e nao do LLM. A releitura da tabela da '
 'secao 4.2 do manual mostra que o proprio manual ja resolve expressamente esta situacao, com desfecho '
 'diverso: a linha "LLM apenas avalia ou explica um diagrama ja existente" tem desfecho E8, com a '
 'justificativa "Nao ha producao, transformacao, reparo ou revisao de conteudo UML". O E6 fica '
 'reservado aos casos em que o LLM nao e substantivo ou sequer toca o conteudo UML; quando o LLM opera '
 'sobre o diagrama, mas apenas para avalia-lo, explica-lo ou critica-lo, o criterio e o da TAREFA, '
 'I3/E8, conforme a regra de ouro 5. Corrijo o desfecho para B3_E8, mantendo intacta a evidencia acima '
 'e alinhando este registro aos congeneres 765_SCOPUS, 771_SCOPUS e 784_SCOPUS, da mesma subarea de '
 'realimentacao automatizada para ensino de modelagem. A exclusao permanece; muda o criterio, de E6 '
 'para E8. '%AGORA)

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
n=0; ok753=False
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid=='753_SCOPUS':
        assert r[i['gate_b_outcome']]=='B2_E6'
        r[i['gate_b_outcome']]='B3_E8'; r[i['exclusion_criteria']]='E8'
        r[i['gate_b_datetime']]=AGORA
        r[i['gate_b_notes']]=r[i['gate_b_notes']]+COR753
        ok753=True; continue
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
assert ok753

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

grp={}
for k,v in D.items(): grp.setdefault(v[0],[]).append(k)
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow(['753_SCOPUS',AGORA,REV,'REVISAO_DECISAO','B','E6 (B2)','E8 (B3)',
     'Correcao de desfecho decidida horas antes na mesma sessao. O 753_SCOPUS (UML Miner, plugin que '
     'analisa a modelagem dos estudantes e devolve realimentacao por LLM) fora classificado como E6 em '
     'B2, ao fundamento de que a autoridade semantica sobre os diagramas e dos estudantes. A releitura '
     'da tabela da secao 4.2 do manual mostra que ela ja resolve expressamente a situacao com desfecho '
     'diverso: "LLM apenas avalia ou explica um diagrama ja existente" -> E8, porque "nao ha producao, '
     'transformacao, reparo ou revisao de conteudo UML". A distincao importa e nao e mera etiqueta: o '
     'E6 e falha de ORIGEM (I2), reservado a quando o LLM nao e substantivo ou nao toca o conteudo '
     'UML; o E8 e falha de TAREFA (I3), quando o LLM opera sobre o diagrama mas apenas para avaliar, '
     'explicar ou criticar. Confundi-los violaria a regra de ouro 5, que veda sobrecarregar o E6, e '
     'distorceria a tabela de exclusoes por criterio no PRISMA. Com a correcao, os quatro registros da '
     'subarea de realimentacao automatizada para ensino de modelagem (753, 765, 771 e 784, todos '
     'Scopus) recebem desfecho uniforme B3_E8. Verificados os demais E6 ja gravados: 678_IEEE (o LLM '
     'anota o contrato, nao avalia o diagrama), 740_SCOPUS (nao ha LLM algum no metodo), 754_SCOPUS (a '
     'IA generativa e perspectiva futura, nao componente), 790_SCOPUS e 960_SCOPUS (o LLM e componente '
     'do sistema projetado) e 915_SCOPUS (os autores contrapoem-se expressamente aos LLMs) — em nenhum '
     'deles o LLM avalia ou explica diagrama, de modo que o E6 permanece correto.',
     'protocol/screening_manual_v1.md'])
    w.writerow([';'.join(sorted(D)),AGORA,REV,'DECISAO_GATE','B','','',
     'Segundo lote de leitura individual dos registros que mencionam UML no titulo ou no resumo: 24 '
     'registros triados. Desfechos: 10 RETIDOS, 6 E7 em B1, 2 E6 em B2, 1 E7 em B3, 3 E8 em B3 e 2 E9 '
     'em B4. Candidatos centrais do lote: 789_SCOPUS (geracao de diagramas de objetos e de sequencia '
     'com avaliacao multimodal por tres VLMs, validada contra 155 especialistas humanos), 791_SCOPUS '
     '(SysML em arquivos .uml do Papyrus, com Graph Edit Distance e robustez a ruido, comparando '
     'pipeline por LLM e pipeline por regras), 773_SCOPUS (qualidade de diagramas de classes gerados '
     'por IA e o objeto declarado no titulo), 760_SCOPUS (ferramenta AUG, com avaliacao de qualidade '
     'como componente arquitetural). Tres achados metodologicos. (1) Emerge um agrupamento tematico '
     'nitido de realimentacao automatizada para ensino de modelagem UML — 753, 765, 771 e 784 — que '
     'sai integralmente por E8 em B3, porque o diagrama e do estudante e o LLM apenas o avalia. (2) '
     '758_SCOPUS gera restricoes OCL a partir de especificacoes em linguagem natural, com validade '
     'sintatica e acuracia de execucao medidas; junto com 518_IEEE, impoe QUESTAO DE PROTOCOLO a fixar '
     'antes da extracao: restricao OCL conta como conteudo UML para efeito do I5? A OCL e norma da OMG '
     'companheira da UML e anexa-se a elementos do modelo, mas nao e diagrama e nao consta da tabela '
     'da secao 4.1. Ambos ficam retidos com INCERTO_SAIDA. (3) Duas armadilhas lexicais novas: '
     '759_SCOPUS usa PlantUML para desenhar ARVORE DE FALHAS, notacao nao-UML, confirmando que a '
     'palavra-chave PlantUML nao e por si sinal de candidatura (l. 174 do protocolo); e 781_SCOPUS '
     'emprega "Hypothetical Component Diagram" em acepcao de neurociencia computacional, alheia ao '
     'diagrama de componentes da UML. Registre-se ainda 772_SCOPUS, em que a UML aparece apenas na '
     'descricao de TRABALHO ANTERIOR alheio, padrao de falso positivo ainda nao documentado.',
     'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('alterados:',n,{k:len(v) for k,v in sorted(grp.items())},'+ correcao 753')
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
