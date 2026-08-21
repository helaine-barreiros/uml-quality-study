import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: leitura do titulo, do resumo e das palavras-chave deste registro no CSV da busca '
     'automatizada, aplicando screening_manual_v1.md e screening_flow_v1.puml na ordem do Portao B '
     '(B1 saida, B2 origem, B3 direcao, B4 entrada). ')

ARTEFATO=('ARTEFATO DE INDEXACAO: este registro entrou na fila de leitura porque casa com o termo '
  '"UML". A ocorrencia, porem, nao esta no titulo nem no resumo: esta apenas na cauda de descritores '
  'do vocabulario controlado do IEEE Xplore, onde "Unified modeling language" aparece entre termos '
  'genericos atribuidos pelo indexador (Training, Accuracy, Codes, Semantics e afins) e nunca entre '
  'as palavras-chave declaradas pelos autores. Nos 43 registros IEEE deste bloco o padrao e o mesmo, '
  'sem uma unica excecao. Nao ha, portanto, mencao a UML de autoria dos autores. ')

UMLS=('COLISAO UMLS: neste registro a atribuicao do descritor tem causa identificavel. O trabalho e '
  'de dominio biomedico e usa o UMLS, Unified Medical Language System, tesauro do NIH sem qualquer '
  'relacao com a Unified Modeling Language. A colisao de sigla propagou-se para o indexador. E uma '
  'armadilha lexical nova, do mesmo genero das ja documentadas na secao 7 do manual ("twin", "GPT" '
  'como subcadeia, "GEMINI" como sistema de 2014). ')

DISC=('DISCUSSAO: o fluxograma manda comecar pela saida, e e ai que este registro para. O resumo e '
  'claro sobre o que o trabalho produz, e o que produz nao e UML. Nao se aplica o terceiro caso do '
  'B1 ("o resumo nao deixa claro", que mandaria reter com INCERTO_SAIDA), porque nao ha obscuridade '
  'quanto ao artefato: ha apenas ausencia de UML. A definicao operacional de "UML diagram" do '
  'protocolo admite excecao quando o componente UML e separavel do artefato relatado; nao havendo '
  'mencao autoral a UML, nao ha componente algum a destacar. Pela regra de ouro 5, esta e uma falha '
  'de SAIDA (I5/E7) e nao deve ser rotulada como E6, reservado a origem do conteudo, nem como E9, '
  'reservado a entrada. Pela regra de ouro 3, o criterio primario e o primeiro portao que explica '
  'claramente o caso, e esse e o B1; os subportoes seguintes nao chegam a ser avaliados. ')

DEC=('DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Nenhuma flag de Portao C se aplica, '
     'porque o registro nao alcanca o Portao C. ')

CTX=('CONTEXTO: decidido na revisao do bloco de 60 registros em que a unica ocorrencia de UML estava '
  'nas palavras-chave, e nao no titulo ou no resumo. Desse bloco, 47 sairam por E7 em B1, 2 por E6 em '
  'B2 e 11 foram retidos. A decisao apoia-se em titulo, resumo e palavras-chave; caso o texto '
  'completo revele componente UML separavel, o registro pode ser reaberto pelo log de eventos. ')

# ---- B1_E7: id -> (o que o trabalho de fato produz, marcador de colisao UMLS)
E7={
'493_IEEE':('casos de teste de aceitacao a partir de requisitos em coreano, por grafo causa-efeito, '
  'arvore C3Tree e tabela de decisao',0),
'499_IEEE':('juizos de deteccao de ambiguidade, inconsistencia e incompletude em especificacoes de '
  'requisitos de veiculos autonomos, por modelos de visao e linguagem',0),
'506_IEEE':('julgamentos de completude de requisitos em linguagem natural, num arcabouco NL2NL',0),
'508_IEEE':('medidas de tamanho funcional COSMIC a partir de casos de uso textuais',0),
'511_IEEE':('casos de teste ponta a ponta para servicos distribuidos',0),
'512_IEEE':('respostas de diagnostico medico preliminar de um chatbot ajustado por fine-tuning',1),
'517_IEEE':('codigo Python, avaliado sob engenharia de prompt dirigida a testes',0),
'523_IEEE':('modelos de instancia em XMI conformes a metamodelos Ecore, no ecossistema EMF',0),
'530_IEEE':('casos de teste em chines, por um modelo DeepSeek-7B ajustado com LoRA',0),
'532_IEEE':('respostas de um sistema de dialogo orientado a tarefa, otimizado por aprendizado por '
  'reforco offline',0),
'535_IEEE':('diagramas de negocio — analise SWOT, organogramas e graficos de Gantt — por realidade '
  'aumentada e blocos fisicos',0),
'553_IEEE':('codigo executavel, estatico e comportamental, gerado a partir de metamodelos '
  'industriais em XMI e XSD por transformacao QVT',0),
'557_IEEE':('texto clinico higienizado e normalizacao de conceitos medicos',1),
'561_IEEE':('modelos de instancia de Asset Administration Shell para gemeos digitais da Industria 4.0',0),
'566_IEEE':('classificacoes de sindrome do desconforto respiratorio agudo a partir de laudos '
  'radiologicos',1),
'576_IEEE':('respostas a perguntas clinicas de cardiologia, ancoradas em grafo de conhecimento '
  'bilingue',1),
'577_IEEE':('analise de requisitos e oportunidades para letramento em saude, com simplificacao '
  'textual',1),
'579_IEEE':('laudos oftalmologicos, por modelo multimodal enriquecido por grafo de conhecimento',0),
'588_IEEE':('uma retrospectiva conceitual sobre composicao de servicos web sensivel a qualidade de '
  'servico',0),
'596_IEEE':('sumarios simplificados de notas de alta hospitalar',1),
'606_IEEE':('um metodo de ajuste por instrucao com recuperacao para linguas de poucos recursos',0),
'607_IEEE':('predicoes de risco precoce de depressao a partir de posts em arabe',1),
'609_IEEE':('um grafo de conhecimento de doencas e farmacos a partir de diretrizes medicas',1),
'622_IEEE':('respostas a consultas biomedicas por orquestracao de multiplos LLMs especializados',1),
'635_IEEE':('respostas de um assistente virtual de saude enriquecido por grafo de conhecimento',1),
'636_IEEE':('extracoes de padroes de consumo de alcool a partir de notas clinicas bilingues',1),
'638_IEEE':('um indice de deteccao de personificacao de papel em texto oncologico gerado por IA',1),
'657_IEEE':('mapeamentos de diagnosticos em texto livre para codigos ICD-10 e SNOMED-CT',1),
'660_IEEE':('respostas a perguntas medicas sobre neoplasias hematologicas',1),
'662_IEEE':('um benchmark de sondagem de conhecimento biomedico em modelos decoder-only',1),
'668_IEEE':('respostas a perguntas biomedicas em grego',1),
'672_IEEE':('casos de teste por uma tecnica de modelagem action-state apoiada em maquinas de estado '
  'finitas e estendidas (FSM e EFSM), que sao formalismos de teste baseado em modelos e nao '
  'diagramas do metamodelo UML',0),
'677_IEEE':('reconhecimento de entidades nomeadas por ajuste baseado em instrucao',1),
'686_IEEE':('normalizacao de entidades clinicas de laudos radiologicos contra uma ontologia',1),
'687_IEEE':('estimativas de otimizacao de custo e alocacao de recursos ao longo do ciclo de vida de '
  'desenvolvimento',0),
'701_IEEE':('sumarios de dialogos medicos, por destilacao professor-aluno',1),
'704_IEEE':('prompts medicos otimizados por algoritmo evolutivo',1),
'707_IEEE':('deteccao de momentos de destaque em transcricoes de transmissoes ao vivo',0),
'709_IEEE':('extracao de entidades estruturadas no dominio de telecomunicacoes 6G',0),
'712_IEEE':('classificacoes explicaveis de dados relacionados a depressao, por atencao cruzada sobre '
  'diretrizes clinicas',1),
'716_IEEE':('traducao de fala para texto ponta a ponta',0),
'724_IEEE':('uma celula robotica e um assistente de voz para uma linha de producao sob os principios '
  'da Industria 5.0',0),
'731_IEEE':('consultas booleanas de busca para revisoes sistematicas biomedicas',0),
'764_SCOPUS':('um conjunto estavel de sentencas e regras num modulo de base de conhecimento, sob uma '
  'arquitetura de computacao autonomica em malha fechada sobre o ChatGPT, avaliada pela metrica MASE',0),
'783_SCOPUS':('hipoteses de diagnostico de falhas em aviónica, por recuperacao aumentada sobre '
  'arvores semanticas hierarquicas e grafos de conhecimento',0),
'899_SCOPUS':('codigo Verilog gerado e verificado a partir de reconhecimento de imagem de diagramas '
  'de temporizacao',0),
'902_SCOPUS':('codigo Verilog sintetizavel otimizado para potencia, desempenho e area',0),
}

# marcadores especificos que substituem o bloco ARTEFATO nos registros Scopus
SCOPUS_KW={
'764_SCOPUS':('ORIGEM DA CORRESPONDENCIA: aqui, ao contrario dos 43 registros IEEE deste bloco, '
  '"PlantUML" e palavra-chave declarada pelos autores, e nao descritor de indexador. Ainda assim o '
  'resumo, que e longo e explicito sobre a arquitetura proposta, nao atribui ao PlantUML papel algum '
  'de artefato produzido: descreve modulo sensor DOMifire, sistema especialista, gerente autonomico e '
  'base de conhecimento. O uso mais provavel do PlantUML e o de ferramenta com que os proprios '
  'autores desenharam a figura de arquitetura do artigo, o que nao e saida do trabalho. '),
'783_SCOPUS':('ORIGEM DA CORRESPONDENCIA: este registro nao traz UML em nenhum dos tres campos; '
  'entrou na fila por termo de modelagem ambiguo. Os "timing diagrams" que o resumo cita sao '
  'diagramas de temporizacao de eletronica digital, insumo de datasheets, e nao diagramas do '
  'metamodelo UML. '),
'899_SCOPUS':('ORIGEM DA CORRESPONDENCIA: os "timing diagrams" do resumo sao diagramas de '
  'temporizacao de hardware, lidos por reconhecimento de imagem como ENTRADA; nao sao diagramas do '
  'metamodelo UML nem saida do trabalho. '),
'902_SCOPUS':('ORIGEM DA CORRESPONDENCIA: este registro nao traz UML de autoria dos autores; a '
  'correspondencia vem de termos de indexacao de projeto de hardware. '),
}

# ---- B2_E6
E6={
'915_SCOPUS':(
 'EVIDENCIA: "Semantic UML" e palavra-chave declarada pelos autores, de modo que a mencao a UML e '
 'autoral e nao artefato de indexacao. O resumo, porem, faz uma afirmacao decisiva e explicita sobre '
 'a origem do conteudo: "Unlike statistical approaches to summarization and explanation such as Large '
 'Language Models (LLMs), our approach of direct representation can be inspected and verified '
 'directly". Os autores contrapoem expressamente o seu metodo aos LLMs. O que constroem sao grafos de '
 'conhecimento dinamicos baseados em processo, com explicacoes causais estruturadas, exemplificados '
 'por um modelo da teoria da Terra Bola de Neve, e um prototipo de interface grafica. ',
 'DISCUSSAO: o B1 nao decide com clareza. A palavra-chave "Semantic UML" sugere que a notacao '
 'empregada tenha componente UML, e o resumo nao nomeia o tipo de diagrama, o que a rigor configuraria '
 'o terceiro caso do B1 e mandaria reter. O B2, em compensacao, decide de forma limpida: nao ha modelo '
 'de linguagem algum no trabalho, e os autores dizem isso eles mesmos, em oposicao declarada. A regra '
 'de ouro 3 manda tomar como criterio primario o PRIMEIRO portao que explica CLARAMENTE o caso; aqui o '
 'primeiro portao claro nao e o B1, que fica indeciso, mas o B2. Pela regra de ouro 5, falha de origem '
 'e I2/E6. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. Registra-se que o B1 ficou indeciso e que '
 'a exclusao NAO se apoia nele. '),
'960_SCOPUS':(
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores. O resumo descreve o projeto e a '
 'implementacao de um sistema de informacao para gestao de etica em pesquisa (REMIS) na Botswana Open '
 'University, com submissao online, notificacoes automaticas e relatorios. A inteligencia artificial '
 'generativa comparece como uma FUNCIONALIDADE do sistema — um chatbot assistente para consultas de '
 'usuario — e nao como produtora de modelo. A UML comparece como notacao com que os proprios autores '
 'documentaram o projeto do sistema. ',
 'DISCUSSAO: o B1 passa, porque ha conteudo UML no trabalho. O B2 e que decide: a autoridade semantica '
 'sobre os elementos UML e dos autores humanos, nao de um modelo de linguagem. Pela RF-02, o que '
 'importa e quem determina o conteudo semantico dos elementos portadores de significado, e aqui o '
 'chatbot nao toca a modelagem: atende consultas de usuario final sobre submissao de propostas. E o '
 'caso classico de coocorrencia de LLM e UML no mesmo artigo sem relacao produtiva entre eles. Pela '
 'regra de ouro 5, falha de origem e I2/E6, nao E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. Registra-se que este registro constava '
 'como pendencia de decisao em texto completo de sessao anterior; o resumo, relido integralmente, e '
 'suficiente para decidir, porque explicita o papel do componente generativo. Caso o texto completo '
 'revele que a UML foi gerada pelo assistente, o registro pode ser reaberto pelo log de eventos. '),
}

# ---- RETIDOS: id -> (flags, evidencia, discussao, decisao)
RET={
'743_SCOPUS':('EVIDENCIA=EXPLICITA',
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores. O titulo — "Leveraging LLMs for Domain '
 'Modeling: The Impact of Granularity and Strategy on Quality" — nomeia a qualidade como objeto. O '
 'resumo relata experimento com dois LLMs de ponta (GPT-4o e outro) variando granularidade da '
 'descricao (texto inteiro versus paragrafo a paragrafo) e estrategia de modelagem (baseada em modelo '
 'versus baseada em lista), medindo o efeito sobre a qualidade dos modelos de dominio gerados. ',
 'DISCUSSAO: os quatro subportoes passam. B1: a saida e modelo de dominio, e a palavra-chave UML dos '
 'autores identifica a notacao. B2: dois LLMs generativos detem a autoridade semantica. B3: a direcao '
 'e texto -> LLM -> modelo, a linha "requisitos -> LLM -> UML" da matriz da secao 4.3, que retem. B4: '
 'a entrada e descricao textual, dentro da delimitacao de escopo. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA porque '
 'a qualidade e variavel dependente declarada no titulo, e nao mencao incidental. Candidato central da '
 'revisao: e exatamente um estudo sobre o efeito de escolhas de prompt na qualidade de UML gerada. '),
'916_SCOPUS':('EVIDENCIA=EXPLICITA',
 'EVIDENCIA: "class diagram" e a primeira palavra-chave declarada pelos autores. O resumo apresenta o '
 'MoRe, abordagem de geracao de modelo de dominio a partir de requisitos por LLM com auto-refinamento '
 'hibrido, e nomeia como problema exatamente os defeitos de qualidade: modelos "redundantes, '
 'inconsistentes ou estruturalmente insanos" produzidos por alucinacao. O refinamento combina LLM com '
 'um verificador baseado em regras. ',
 'DISCUSSAO: B1 passa, a saida e diagrama de classes. B2 passa: o LLM produz o rascunho inicial e '
 'detem a autoridade semantica; o verificador simbolico e posterior e corretivo, e pela RF-02 regras '
 'simbolicas no pipeline nao descaracterizam a origem. B3 passa, a direcao e requisitos -> LLM -> UML. '
 'B4 passa, a entrada e requisitos textuais. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: '
 'redundancia, consistencia e sanidade estrutural sao dimensoes de qualidade nomeadas no proprio '
 'resumo. Candidato central. '),
'957_SCOPUS':('EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores. O resumo avalia a capacidade de Llama 4, '
 'Gemini 2.0 e OpenAI o3 de gerar arquitetura de software a partir de requisitos textuais nao '
 'estruturados, num contexto de microsservicos. ',
 'DISCUSSAO: B1 passa, com ressalva: a saida declarada e "arquitetura de software", e a palavra-chave '
 'UML dos autores indica que a arquitetura e expressa em UML, mas o resumo nao nomeia o tipo de '
 'diagrama. Como a palavra-chave e autoral, e nao descritor de indexador, ha base para reconhecer '
 'componente UML; a incerteza remanescente e sobre o TIPO, nao sobre a existencia. B2 passa, tres LLMs '
 'nomeados detem a autoridade semantica. B3 passa, requisitos -> LLM -> arquitetura. B4 passa, a '
 'entrada e requisitos textuais nao estruturados. ',
 'DECISAO DA PESQUISADORA: RETIDO. Flag EVIDENCIA=A_VERIFICAR: o resumo fala em qualidade e '
 'manutenibilidade na motivacao, mas nao declara metrica; pela regra de ouro 2, ausencia de '
 'vocabulario de qualidade nunca exclui. PAUTA DE LEITURA: qual o tipo de diagrama UML produzido e '
 'como a avaliacao das arquiteturas geradas foi operacionalizada. '),
'893_SCOPUS':('EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: "unified modeling language" e "use case modeling" sao palavras-chave declaradas pelos '
 'autores. O resumo descreve metodo que integra um LLM de pesos abertos para extrair atores e casos de '
 'uso de requisitos de software por engenharia de prompt avancada, avaliado em estudo exploratorio com '
 'cinco engenheiros de software profissionais, comparando modelagem manual tradicional com a abordagem '
 'baseada em LLM. ',
 'DISCUSSAO: B1 passa, a saida e modelo de casos de uso, e atores e casos de uso sao elementos do '
 'metamodelo UML. B2 passa, o LLM extrai e nomeia os elementos, detendo a autoridade semantica. B3 '
 'passa, requisitos -> LLM -> UML. B4 passa, a entrada e requisitos textuais. ',
 'DECISAO DA PESQUISADORA: RETIDO. Flag EVIDENCIA=A_VERIFICAR: ha comparacao com modelagem manual, o '
 'que sugere criterio avaliativo, mas o resumo nao nomeia as dimensoes medidas. PAUTA DE LEITURA: '
 'quais criterios os cinco profissionais aplicaram e se ha diagrama de casos de uso ou apenas listas '
 'de atores e casos de uso. '),
'832_SCOPUS':('EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: "UML modeling" e palavra-chave declarada pelos autores. O resumo descreve a '
 'semi-automacao dos processos de modelagem de classes e de validacao de requisitos, com metodos '
 'estruturados destinados a mitigar alucinacoes do LLM. Um toolkit de linguagem natural extrai '
 'etiquetas morfossintaticas, informacao de constituencia e pontuacao, e algoritmos selecionam classes '
 'candidatas; essa selecao alimenta o prompt do LLM. ',
 'DISCUSSAO: B1 passa, a saida e modelo de classes. B2 exige cautela e e a razao da retencao com '
 'ressalva: ha um pipeline hibrido em que algoritmos simbolicos selecionam as classes candidatas e o '
 'LLM opera sobre essa selecao. Pela RF-02, o que decide nao e a presenca de regras simbolicas, e sim '
 'quem determina o conteudo semantico dos elementos UML. O resumo nao permite fixar se o LLM constitui '
 'o modelo ou apenas o valida contra uma lista previamente calculada. Pela regra de ouro 1, a '
 'incerteza retem. B3 e B4 passam: requisitos textuais -> UML. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_PAPEL_LLM. PAUTA DE LEITURA: o LLM constitui o modelo de '
 'classes ou apenas valida candidatos gerados pelo parser? Se apenas valida, o desfecho e E6 em B2. '),
'881_SCOPUS':('EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: "UML Modelling" e palavra-chave declarada pelos autores, ao lado de "Requirements Model". '
 'O resumo apresenta o GCSS, arcabouco interativo e iterativo de geracao, comparacao, selecao e '
 'suplementacao, que guia LLMs na geracao de modelos a partir de linguagem natural, com decisoes do '
 'usuario incorporadas a cada rodada e realimentacao automatica. ',
 'DISCUSSAO: B1 passa: a saida e modelo de requisitos e a palavra-chave autoral identifica a notacao '
 'como UML, embora o resumo nao nomeie o tipo de diagrama. B2 passa, o LLM gera os modelos. B3 passa, '
 'requisitos -> LLM -> UML. B4 passa, a entrada e linguagem natural. Ha intervencao humana no laco '
 '(decisoes do usuario na etapa de selecao), o que nao descaracteriza a origem: o conteudo continua '
 'sendo proposto pelo LLM. ',
 'DECISAO DA PESQUISADORA: RETIDO. Flag EVIDENCIA=A_VERIFICAR: o resumo diz apenas que os modelos '
 'gerados "alinham-se as expectativas", formulacao vaga que nao constitui metrica declarada. PAUTA DE '
 'LEITURA: qual o tipo de diagrama e como o alinhamento foi medido. '),
'871_SCOPUS':('INCERTO_SAIDA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: "Unified Modeling Language (UML)" e "Use Case Modeling" sao palavras-chave declaradas '
 'pelos autores. O resumo apresenta o UCGen, abordagem baseada em LLM com humano no laco para gerar '
 'DESCRICOES TEXTUAIS de casos de uso a partir de especificacoes de requisitos, aplicada a dez '
 'conjuntos do PURE. A avaliacao mede completude, correcao e redundancia, e conclui que as descricoes '
 'geradas sao em media mais completas, mais corretas e menos redundantes que as derivadas por humanos. ',
 'DISCUSSAO: B2, B3 e B4 passam sem duvida: LLM com autoridade semantica, direcao requisitos -> '
 'modelo, entrada textual. O B1 e que fica em suspenso, e a questao e de fronteira do protocolo. O '
 'artefato produzido e a descricao textual de caso de uso, o gabarito narrativo de ator, objetivo, '
 'fluxo principal e fluxos alternativos. A UML normativa define o DIAGRAMA de casos de uso; a '
 'descricao textual e pratica consagrada de engenharia de requisitos, popularizada por Cockburn, que a '
 'especificacao da UML nao normatiza. A tabela da secao 4.1 do manual nao a arrola. Por outro lado os '
 'proprios autores declaram UML como palavra-chave e falam em "use case models", e atores e casos de '
 'uso sao elementos do metamodelo UML independentemente da forma de apresentacao. Pela regra de ouro '
 '1, a incerteza retem: custa uma leitura, e a alternativa custa um estudo perdido. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_SAIDA. Flag EVIDENCIA=EXPLICITA porque completude, '
 'correcao e redundancia sao dimensoes de qualidade medidas e reportadas. PAUTA DE LEITURA e QUESTAO '
 'DE PROTOCOLO A DECIDIR: descricao textual de caso de uso conta como conteudo UML para efeito do I5? '
 'A resposta afeta outros registros e deve ser fixada em evento de INTERPRETACAO_PROTOCOLO antes da '
 'extracao. '),
'563_IEEE':('INCERTO_SAIDA',
 'EVIDENCIA: a unica ocorrencia de UML esta na cauda de descritores do IEEE Xplore, nao em palavra-'
 'chave autoral. O resumo, porem, descreve geracao automatica de MODELOS DE PROCESSO a partir de '
 'descricao textual, por orquestracao multiagente sobre LLMs, em quatro fases (geracao, refinamento, '
 'revisao de alucinacoes semanticas e correcao de erros de formato por ferramenta externa). Os '
 'resultados sao comparados com modelagem manual, com ganhos de 89%, 61%, 52% e 75% em quatro '
 'processos. ',
 'DISCUSSAO: B2, B3 e B4 passam: LLMs sao a pedra angular dos agentes, a direcao e texto -> modelo e a '
 'entrada e descricao textual. O B1 e o problema. "Process model" nao nomeia notacao: pode ser BPMN, '
 'caso em que o desfecho seria E7 pela linha "requisitos -> LLM -> BPMN" da matriz da secao 4.3, ou '
 'pode ser diagrama de atividades da UML, caso em que o registro esta no escopo. O resumo nao decide. '
 'Este e precisamente o terceiro caso do B1 — "o resumo nao deixa claro qual notacao" — que o '
 'fluxograma manda reter com INCERTO_SAIDA, e nao excluir. Excluir aqui seria atribuir aos autores uma '
 'escolha de notacao que eles nao declararam. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_SAIDA, por indecidibilidade do B1 e nao por verificacao. '
 'PAUTA DE LEITURA: em que notacao os modelos de processo sao expressos? Se BPMN ou rede de Petri, '
 'E7 em B1; se diagrama de atividades UML, o registro segue para extracao. '),
'929_SCOPUS':('CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores. O resumo apresenta estudo exploratorio '
 'sobre COMO os usuarios interagem com LLMs em tarefas de modelagem conceitual e sobre a utilidade '
 'percebida, e diz expressamente que "existing works focus on various quality metrics of LLM outcomes, '
 'yet limited attention is given to how users interact with LLMs for such modeling tasks". Isto e, o '
 'trabalho posiciona-se por CONTRASTE com os estudos de qualidade do produto. ',
 'DISCUSSAO: B1, B2, B3 e B4 passam: ha modelagem conceitual com UML declarada, LLMs generativos, '
 'direcao texto -> modelo e entrada em linguagem natural. O que este registro suscita nao e questao de '
 'Portao B, e sim de Portao C e, adiante, de E10: se a variavel medida for comportamento de interacao '
 'e percepcao de utilidade, e nao propriedade do artefato UML produzido, a evidencia de qualidade do '
 'MODELO pode ser tenue ou ausente. O E10 nao e decidivel por titulo e resumo, conforme o manual, e a '
 'regra de ouro 2 e taxativa: ausencia de vocabulario de qualidade do produto nunca exclui nesta '
 'etapa. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flags CANDIDATO_E10 e '
 'EVIDENCIA=A_VERIFICAR. PAUTA DE LEITURA: o estudo mede alguma propriedade dos modelos gerados, ou '
 'apenas comportamento e percepcao dos participantes? '),
'890_SCOPUS':('INCERTO_SAIDA;CANDIDATO_E10',
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores. O resumo descreve um ESTUDO DE CASO '
 'DIDATICO para disciplina de analise e projeto de sistemas: apresenta o problema de negocio da '
 'empresa ficticia GlobePort e pede que o LEITOR assuma o papel de analista e use ferramentas de IA '
 'generativa para definir escopo funcional, modelos de requisitos com dependencias e prioridades, '
 'modelos de dados e de processo, e planos de sprint ageis. ',
 'DISCUSSAO: B2 passa, ha ferramentas de IA generativa. B3 e B4 passam, a direcao e descricao textual '
 'de problema -> modelos. O B1 fica em suspenso por duas razoes somadas. Primeira, os artefatos '
 'nomeados no resumo sao modelos de requisitos, de dados e de processo, sem que se nomeie notacao; a '
 'palavra-chave UML dos autores sugere UML, mas nao a fixa. Segunda, e mais delicada, o artigo e um '
 'enunciado de estudo de caso: quem produz os modelos e o leitor-estudante, e nao os autores, de modo '
 'que pode nao haver artefato gerado e avaliado dentro do proprio trabalho. Isso toca tambem a '
 'natureza do relato, ja ultrapassada no Portao A. Pela regra de ouro 1, a incerteza retem. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_SAIDA e CANDIDATO_E10. PAUTA DE LEITURA: o artigo '
 'apresenta modelos UML efetivamente gerados por IA generativa e alguma avaliacao deles, ou e apenas '
 'material didatico que propoe a tarefa? '),
'892_SCOPUS':('EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo nomeia os tres elementos decisivos — "Generative AI in the Software Modeling '
 'Classroom: An Experience Report With ChatGPT and Unified Modeling Language". O resumo, porem, e um '
 'unico periodo de teaser da revista, sem metodo nem resultados: afirma que o uso de chatbots de IA '
 'generativa em avaliacao formativa afere o progresso de aprendizagem, eleva o desempenho academico '
 'frente a metodologia tradicional e conscientiza os estudantes sobre os tradeoffs. As palavras-chave '
 'incluem avaliacao formativa e somativa, programacao orientada a objetos e ensino. ',
 'DISCUSSAO: os quatro subportoes passam pelo titulo — ha ChatGPT, ha UML e ha sala de aula de '
 'modelagem de software —, mas passam com apoio quase nulo do resumo, que nao diz o que foi gerado '
 'nem o que foi medido. A situacao aproxima-se da dos registros sem resumo tratados neste mesmo dia: o '
 'desfecho PASSOU registra que o registro nao foi excluido, e nao que a triagem foi cumprida com '
 'evidencia suficiente. ',
 'DECISAO DA PESQUISADORA: RETIDO. Flag EVIDENCIA=A_VERIFICAR. PAUTA DE LEITURA: os diagramas UML sao '
 'gerados pelo ChatGPT e avaliados, ou os estudantes e que modelam e o ChatGPT serve de tutor? A '
 'segunda hipotese levaria a E6 em B2. '),
}

assert len(E7)+len(E6)+len(RET)==60, (len(E7),len(E6),len(RET))

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
nE7=nE6=nR=0
for r in rows[1:]:
    lid=r[i['logical_id']]
    if lid not in E7 and lid not in E6 and lid not in RET: continue
    assert r[i['excluded']]!='true' and not r[i['gate_b_outcome']], lid
    r[i['gate_b_reviewer']]=REV; r[i['gate_b_datetime']]=AGORA
    if lid in E7:
        saida,umls=E7[lid]
        origem=SCOPUS_KW.get(lid,ARTEFATO)
        ev=('EVIDENCIA: varredura dos tres campos deste registro. Nao ha ocorrencia de UML nem de '
            'qualquer tipo de diagrama do metamodelo UML no titulo ou no resumo. '+origem+
            (UMLS if umls else '')+
            'O que o trabalho de fato produz, pelo que os autores declaram no resumo, e outra coisa: '
            +saida+'. ')
        r[i['gate_b_outcome']]='B1_E7'
        r[i['gate_b_notes']]=MET+ev+DISC+DEC+CTX
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E7'
        nE7+=1
    elif lid in E6:
        ev,di,de=E6[lid]
        r[i['gate_b_outcome']]='B2_E6'
        r[i['gate_b_notes']]=MET+ev+di+de+CTX
        r[i['excluded']]='true'; r[i['exclusion_criteria']]='E6'
        nE6+=1
    else:
        flags,ev,di,de=RET[lid]
        r[i['gate_b_outcome']]='PASSOU'
        r[i['gate_b_notes']]=MET+ev+di+de
        r[i['gate_c_flags']]=flags; r[i['gate_c_reviewer']]=REV; r[i['gate_c_datetime']]=AGORA
        r[i['gate_c_notes']]=('Flags atribuidas na mesma leitura do Portao B; ver gate_b_notes para a '
            'evidencia e a discussao que as fundamentam. Pela regra de ouro 2, nenhuma flag exclui.')
        nR+=1

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow([';'.join(sorted(E7)),AGORA,REV,'DECISAO_GATE','B1','','E7',
     'Quarenta e sete registros EXCLUIDOS por E7 em B1, do bloco de 60 em que a unica ocorrencia de '
     'UML estava nas palavras-chave e nao no titulo ou no resumo. Achado metodologico do bloco: em 43 '
     'registros do IEEE, a correspondencia vinha exclusivamente do descritor "Unified modeling '
     'language" do vocabulario controlado do IEEE Xplore, atribuido pelo indexador entre termos '
     'genericos (Training, Accuracy, Codes, Semantics) e jamais declarado pelos autores. Em 21 desses '
     '43 a causa e identificavel: sao trabalhos biomedicos que usam o UMLS, Unified Medical Language '
     'System, tesauro do NIH sem relacao com a Unified Modeling Language; a colisao de sigla '
     'propagou-se para a indexacao. E armadilha lexical nova, a acrescentar a secao 7 do manual. Os '
     'outros 4 sao do Scopus e caem por razao propria: 764 tem PlantUML como palavra-chave autoral mas '
     'produz regras de base de conhecimento, 783 e 899 tem "timing diagrams" de eletronica digital que '
     'nao sao do metamodelo UML, e 902 gera Verilog. Todos os 47 possuem resumo, portanto nenhuma '
     'exclusao se apoia em dado ausente.',
     'protocol/screening_manual_v1.md; protocol/screening_flow_v1.puml'])
    w.writerow([';'.join(sorted(E6)),AGORA,REV,'DECISAO_GATE','B2','','E6',
     'Dois registros EXCLUIDOS por E6 em B2, ambos com UML declarada como palavra-chave pelos autores '
     'e portanto sem artefato de indexacao. Em 915_SCOPUS os proprios autores contrapoem expressamente '
     'o seu metodo aos LLMs ("Unlike statistical approaches ... such as Large Language Models"), de '
     'modo que nao ha modelo de linguagem no trabalho; registre-se que o B1 ficou indeciso e que a '
     'exclusao nao se apoia nele, aplicada a regra de ouro 3 na sua formulacao exata (primeiro portao '
     'que explica CLARAMENTE o caso). Em 960_SCOPUS a UML e notacao com que os autores documentaram o '
     'projeto do sistema e a IA generativa e uma funcionalidade de chatbot para consultas de usuario '
     'final: coocorrencia sem relacao produtiva, decidida pela RF-02. O 960_SCOPUS constava como '
     'pendencia de decisao em texto completo desde sessao anterior; fica decidido no resumo.',
     'protocol/screening_manual_v1.md'])
    w.writerow([';'.join(sorted(RET)),AGORA,REV,'DECISAO_GATE','B','','',
     'Onze registros RETIDOS do bloco de 60. Quatro sao candidatos centrais da revisao, todos com UML '
     'declarada pelos autores e qualidade como objeto: 743_SCOPUS mede o efeito de granularidade e '
     'estrategia de prompt sobre a qualidade de modelos de dominio gerados por GPT-4o; 916_SCOPUS '
     '(MoRe) nomeia redundancia, inconsistencia e sanidade estrutural de diagramas de classes gerados; '
     '893_SCOPUS gera modelos de casos de uso avaliados por cinco profissionais; 957_SCOPUS avalia '
     'Llama 4, Gemini 2.0 e o3 na geracao de arquitetura a partir de requisitos nao estruturados. '
     'Tres retencoes sao por indecidibilidade do B1: 563_IEEE gera "process models" sem nomear a '
     'notacao (terceiro caso do B1; se BPMN, E7); 890_SCOPUS e enunciado de estudo de caso didatico em '
     'que quem modela e o leitor; 871_SCOPUS gera DESCRICOES TEXTUAIS de casos de uso, o que abre uma '
     'QUESTAO DE PROTOCOLO a fixar antes da extracao: descricao textual de caso de uso, gabarito '
     'narrativo nao normatizado pela especificacao da UML e ausente da tabela da secao 4.1 do manual, '
     'conta como conteudo UML para efeito do I5? Uma retencao e por incerteza de papel do LLM '
     '(832_SCOPUS, pipeline hibrido em que um parser seleciona classes candidatas antes do LLM; se o '
     'LLM apenas valida, E6). Duas sao por evidencia a verificar (881_SCOPUS, 892_SCOPUS, este ultimo '
     'com resumo de periodo unico). E uma e candidata a E10 (929_SCOPUS, que mede comportamento de '
     'interacao e percepcao, e nao propriedade do artefato).',
     'protocol/screening_manual_v1.md'])

from collections import Counter
rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
print('E7=%d E6=%d RETIDOS=%d'%(nE7,nE6,nR))
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
