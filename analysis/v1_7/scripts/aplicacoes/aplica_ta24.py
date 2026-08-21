import csv, os, datetime

BASE='/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated'
CSV=os.path.join(BASE,'custom_automated_search_collection.csv')
LOG=os.path.join(BASE,'screening_decision_log.csv')
AGORA=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
REV='HB'

MET=('METODO: leitura integral do titulo, do resumo e das palavras-chave deste registro no CSV da '
     'busca automatizada, aplicando screening_manual_v1.md e screening_flow_v1.puml na ordem do '
     'Portao B (B1 saida, B2 origem, B3 direcao, B4 entrada). ')

# id -> (desfecho, flags, evidencia, discussao, decisao)
D={

'456_IEEE':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo anuncia um arcabouco de automacao baseado em PlantUML para modelagem de casos '
 'de uso. O resumo declara que a abordagem extrai relacoes de especificacoes de software em linguagem '
 'natural e gera os diagramas de casos de uso correspondentes, combinando analise de dependencias, '
 'filtragem por regras de triplas sujeito-verbo-objeto e um modelo de linguagem de grande porte local '
 'para produzir codigo PlantUML sintaticamente valido. A avaliacao usa cinco conjuntos publicos de '
 'documentos de requisitos e mede precisao, revocacao e F1. ',
 'DISCUSSAO: B1 passa sem duvida: a saida e diagrama de casos de uso, tipo nomeado do metamodelo UML, '
 'e o PlantUML aqui e sintaxe portadora com o tipo de diagrama declarado, o que afasta o terceiro caso '
 'do B1. B3 passa: a direcao e requisitos -> modelo, a primeira linha da matriz da secao 4.3. B4 '
 'passa: a entrada e especificacao textual em linguagem natural, no centro da delimitacao de escopo. '
 'O B2 e que exige ressalva. O pipeline e hibrido: a analise de dependencias e a filtragem por regras '
 'identificam as triplas, e o LLM produz o codigo PlantUML. Pela RF-02, a presenca de regras '
 'simbolicas e por si irrelevante; o que decide e quem detem a autoridade semantica sobre os elementos '
 'portadores de significado, isto e, sobre quais atores e casos de uso existem e como se relacionam. '
 'O resumo nao permite fixar se o LLM constitui esse conteudo ou se apenas o serializa em PlantUML a '
 'partir de triplas ja extraidas pelo componente simbolico. Na segunda hipotese o LLM seria mero '
 'transdutor de sintaxe e o desfecho seria E6. Pela regra de ouro 1, a incerteza retem. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU no Portao B. Flag INCERTO_PAPEL_LLM pela ambiguidade '
 'acima; flag EVIDENCIA=EXPLICITA porque precisao, revocacao e F1 sao metricas declaradas sobre o '
 'artefato gerado. PAUTA DE LEITURA: o LLM determina atores e casos de uso, ou apenas traduz para '
 'PlantUML triplas fixadas pelas regras? Se apenas traduz, o desfecho e E6 em B2. '),

'467_IEEE':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo nomeia geracao de UML a partir de linguagem natural. O resumo abre constatando '
 'que os LLMs ja geram diagramas UML a partir de requisitos, mas com erros sistematicos que ele nomeia '
 'um a um: atributos alucinados, estruturas superprojetadas e violacoes de antipadroes. Atribui essas '
 'falhas a duas causas — prompts irrestritos sem orientacao metodologica e saidas sem ancoragem em '
 'notacao estabelecida — e propoe abordagem em duas etapas: um pipeline de validacao em tres camadas '
 'que avalia os requisitos em oito dimensoes de qualidade, e um gerador com recuperacao aumentada que '
 'busca padroes na documentacao oficial do PlantUML. ',
 'DISCUSSAO: os quatro subportoes passam. B1: a saida e diagrama UML, declarado no titulo. B2: o '
 'ChatGPT e nomeado e detem a autoridade semantica sobre os elementos gerados. B3: a direcao e '
 'requisitos -> LLM -> UML. B4: a entrada e requisitos em linguagem natural. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: '
 'alucinacao de atributos, superprojeto e violacao de antipadroes sao defeitos de qualidade nomeados '
 'no resumo, e ha oito dimensoes de qualidade declaradas. Candidato central da revisao. '),

'738_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo declara geracao automatica de diagramas de casos de uso a partir de requisitos '
 'por pipelines baseados em modelo de linguagem. O resumo situa o problema na ambiguidade dos '
 'requisitos escritos em linguagem natural e propoe dois pipelines com foco em reduzir a quantidade '
 'necessaria de dados anotados de treino: o primeiro combina reconhecimento de entidades nomeadas com '
 'aprendizado ativo; o segundo, cortado na exportacao, presume-se baseado em LLM. ',
 'DISCUSSAO: B1 passa: a saida e diagrama de casos de uso, tipo nomeado do metamodelo UML. B3 e B4 '
 'passam: requisitos em linguagem natural -> modelo. O B2 merece atencao: o primeiro pipeline usa '
 'reconhecimento de entidades nomeadas, e pela RF-01 o uso de encoder como NER NAO satisfaz o I2. Mas '
 'o titulo fala em "Language Model-based Pipelines" no plural e as palavras-chave declaram "Large '
 'language models (LLM)", de modo que ao menos um dos pipelines e generativo. Havendo dois pipelines e '
 'sendo ao menos um deles baseado em LLM, ha componente substantivo separavel e o registro segue. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU no Portao B. Flag EVIDENCIA=A_VERIFICAR: o resumo '
 'exportado esta truncado e nao chega as metricas; pela regra de ouro 2, ausencia de vocabulario de '
 'qualidade nunca exclui. PAUTA DE LEITURA: qual dos dois pipelines usa LLM generativo e como a '
 'qualidade dos diagramas gerados foi medida. '),

'742_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo anuncia arcabouco automatizado para transformar documentos industriais em '
 'ontologia e modelos conceituais. O resumo e explicito quanto a saida: conversao de documentos nao '
 'estruturados em ontologia estruturada (OWL) e modelos conceituais (UML), integrando MinerU, '
 'recuperacao aumentada, modelos de linguagem de grande porte e agrupamento por K-Means para extrair '
 'entidades, relacoes e estruturas hierarquicas. ',
 'DISCUSSAO: B1 passa com ressalva de escopo: a saida e dupla, ontologia OWL e modelo conceitual UML. '
 'Ha, portanto, componente UML separavel, e a definicao operacional de "UML diagram" do protocolo '
 'admite expressamente a excecao quando o componente UML se separa do artefato composto. B2 passa, os '
 'LLMs sao a peca central da extracao. B3 passa, a direcao e documento -> modelo. B4 exige exame: a '
 'entrada e documentacao tecnica e normativa industrial, texto tecnico nao estruturado, e o MinerU com '
 'OCR serve para converter o PDF em texto, nao para interpretar imagem como fonte semantica. Trata-se, '
 'portanto, de entrada textual, dentro da delimitacao fixada, e nao de formalizacao a partir de imagem. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=A_VERIFICAR: o '
 'resumo fala em conversao "precisa" e "acurada" sem declarar metrica. PAUTA DE LEITURA: qual tipo de '
 'diagrama UML e produzido, o componente UML se separa da ontologia OWL na avaliacao, e como a '
 'qualidade foi medida. '),

'748_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo e inequivoco — "Model Generation with LLMs: From Requirements to UML Sequence '
 'Diagrams". O resumo investiga a capacidade do ChatGPT de gerar diagramas de sequencia UML a partir '
 'de requisitos em linguagem natural, por estudo qualitativo que examina os diagramas gerados para 28 '
 'requisitos. ',
 'DISCUSSAO: os quatro subportoes passam sem qualquer ressalva. B1: diagrama de sequencia, tipo '
 'nomeado do metamodelo UML. B2: ChatGPT nomeado, com autoridade semantica. B3: requisitos -> LLM -> '
 'UML, a primeira linha da matriz da secao 4.3. B4: requisitos em linguagem natural. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: o '
 'estudo qualitativo examina os diagramas produzidos, o que constitui avaliacao do artefato. Candidato '
 'central da revisao. '),

'749_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo declara geracao de modelo de classes a partir de requisitos por LLMs. O resumo '
 'investiga GPT-5, Claude Sonnet 4.0, Gemini 2.5 Flash Thinking e Llama-3.1-8B-Instruct na geracao '
 'automatica de diagramas de classes UML a partir de requisitos em linguagem natural, e propoe um '
 'arcabouco de avaliacao abrangente para aferir eficacia e confiabilidade da geracao. ',
 'DISCUSSAO: os quatro subportoes passam sem ressalva. B1: diagrama de classes UML. B2: quatro LLMs '
 'nomeados. B3: requisitos -> LLM -> UML. B4: requisitos em linguagem natural. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=EXPLICITA: o '
 'proprio resumo anuncia arcabouco de avaliacao para eficacia e confiabilidade dos modelos gerados. '
 'Candidato central da revisao, e com comparacao entre quatro LLMs de geracoes recentes. '),

'751_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores. O resumo relata que um modelo GPT foi '
 'treinado sobre um conjunto de dados de elementos de diagrama de componentes UML, no contexto de '
 'engenharia de sistemas baseada em modelos centrada no usuario. A frase decisiva e explicita: '
 '"Complex relationships between the UML elements were not only understood, they were also generated '
 'using natural-language text". Os problemas relatados sao a extensao do XMI, a limitacao de contexto '
 'e os identificadores unicos dos elementos UML. ',
 'DISCUSSAO: os quatro subportoes passam. B1: diagrama de componentes UML, tipo nomeado do metamodelo. '
 'B2: modelo GPT ajustado por fine-tuning, com autoridade semantica sobre os elementos e suas '
 'relacoes. B3: a direcao e texto em linguagem natural -> UML, conforme a frase citada. B4: a entrada '
 'e texto em linguagem natural. Registre-se que o XMI comparece como formato de SAIDA e como fonte de '
 'dificuldade tecnica, e nao como entrada, o que afastaria o B4. ',
 'DECISAO DA PESQUISADORA: RETIDO, com PASSOU nos quatro subportoes. Flag EVIDENCIA=A_VERIFICAR: o '
 'resumo qualifica os resultados como "promissores" e fala em "contribution quality", mas nao declara '
 'metrica sobre o artefato. PAUTA DE LEITURA: como a qualidade dos diagramas de componentes gerados '
 'foi aferida. '),

'755_SCOPUS':('PASSOU','INCERTO_SAIDA',
 'EVIDENCIA: o titulo anuncia sistemas multiagente movidos a LLM para metamodelagem dirigida por '
 'documentacao. O resumo situa a metamodelagem como atividade inicial de um pipeline de engenharia '
 'dirigida a modelos e descreve a tarefa como extrair conhecimento de dominio de documentacao textual '
 'e estabelecer as CLASSES, RELACOES e RESTRICOES que depois formalizarao o metamodelo. Aponta a etapa '
 'como custosa, propensa a erro e sujeita a vies e expertise do modelador. ',
 'DISCUSSAO: B2, B3 e B4 passam: agentes baseados em LLM detem a autoridade semantica, a direcao e '
 'documentacao textual -> modelo e a entrada e texto. O B1 e que fica em suspenso, e a duvida e '
 'especifica. O artefato produzido e um METAMODELO, e os elementos nomeados — classes, relacoes e '
 'restricoes — sao os do diagrama de classes; a pratica corrente exprime metamodelos em Ecore ou MOF, '
 'que compartilham o nucleo estrutural da UML sem serem UML. O resumo nao nomeia a notacao nem o '
 'formato de serializacao. Este e o terceiro caso do B1 — "o resumo nao deixa claro" — que o '
 'fluxograma manda reter com INCERTO_SAIDA, e nao excluir. Excluir aqui seria atribuir aos autores uma '
 'escolha de notacao que eles nao declararam. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_SAIDA, por indecidibilidade do B1. PAUTA DE LEITURA: o '
 'metamodelo e expresso em diagrama de classes UML, em Ecore ou em MOF? Se Ecore ou MOF sem componente '
 'UML separavel, o desfecho e E7 em B1, como ja decidido para 523_IEEE. '),

'720_IEEE':('PASSOU','INCERTO_ENTRADA;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o resumo declara que o arcabouco gera representacoes estruturadas usando DIAGRAMAS DE '
 'ATIVIDADE em PlantUML, para capturar fluxos de trabalho, dependencias e interacoes entre componentes '
 'e partes interessadas. A entrada, porem, e expressamente multimodal: LLMs interpretam fontes '
 'textuais e modelos de visao e linguagem extraem informacao de artefatos VISUAIS, a saber fluxos de '
 'processo e diagramas operacionais. Ha ainda tecnicas de engenharia dirigida a modelos e modelagem '
 'baseada em regras para validacao formal. ',
 'DISCUSSAO: B1 passa: diagrama de atividade e tipo nomeado do metamodelo UML, e o PlantUML aqui e '
 'sintaxe portadora com o tipo declarado. B2 passa: LLMs e VLMs generativos. B3 passa: a direcao e '
 'fonte -> UML, o UML e produto. O B4 e o problema. Pela delimitacao de escopo fixada em 2026-08-16, a '
 'entrada admissivel e especificacao textual em linguagem natural, e a formalizacao a partir de imagem '
 'ou esboco leva a E9. Aqui a entrada e MISTA: ha fontes textuais lidas por LLM e ha artefatos visuais '
 'lidos por VLM. O resumo nao permite saber se o componente textual e suficiente por si, isto e, se os '
 'diagramas de atividade gerados derivam do texto com o visual apenas complementando, ou se o visual e '
 'fonte semantica indispensavel. Pela regra de ouro 1, a incerteza retem. ',
 'DECISAO DA PESQUISADORA: RETIDO com INCERTO_ENTRADA, por indecidibilidade do B4. Flag '
 'EVIDENCIA=A_VERIFICAR: o resumo fala em transparencia e identificacao de perigos, nao em metrica '
 'sobre o diagrama. PAUTA DE LEITURA: os diagramas de atividade sao derivados do texto, com o visual '
 'como complemento, ou o artefato visual e fonte semantica necessaria? Na segunda hipotese o desfecho '
 'e E9 em B4. '),

'051_ACM':('PASSOU','INCERTO_PAPEL_LLM;CANDIDATO_E10;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo relata estudo de benchmarking de ferramentas de IA generativa em quatro fases da '
 'engenharia de software, sendo a primeira a documentacao de projeto. Para essa fase, as metricas '
 'aplicadas foram acuracia do diagrama, completude, esforco do usuario e integracao com o ambiente de '
 'desenvolvimento. O resumo, cortado na exportacao, chega a afirmar que as ferramentas de diagramacao '
 'podem produzir UML preciso. As ferramentas avaliadas na fase de projeto sao Lucidchart, Mermaid.js e '
 'UIzard; nas demais fases entram GPT-4, Claude 3.5 Sonnet, Copilot e outras. ',
 'DISCUSSAO: B1 passa quanto a fase de documentacao de projeto, em que ha UML produzido e medido, e ha '
 'componente separavel do restante do benchmark. O B2 e o ponto sensivel. Das tres ferramentas da fase '
 'de projeto, o Mermaid.js e biblioteca de renderizacao e nao modelo de linguagem, o Lucidchart e '
 'ferramenta de diagramacao cujo componente generativo varia por versao, e o UIzard e gerador de '
 'interface. Os LLMs nomeados — GPT-4 e Claude — comparecem na fase de DEPURACAO, nao na de projeto. '
 'Ha, portanto, risco real de que o UML medido nao tenha sido produzido por LLM, o que levaria a E6. O '
 'resumo nao resolve. Pela regra de ouro 1, a incerteza retem. ',
 'DECISAO DA PESQUISADORA: RETIDO. Flags INCERTO_PAPEL_LLM pela duvida acima, EVIDENCIA=EXPLICITA '
 'porque acuracia e completude de diagrama sao dimensoes de qualidade medidas, e CANDIDATO_E10 porque '
 'o desenho e de benchmark exploratorio com muitas ferramentas e poucas observacoes por celula. PAUTA '
 'DE LEITURA: qual ferramenta produziu o UML avaliado e ela e baseada em LLM? '),

'739_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo descreve a geracao de artigos cientificos inteiros exclusivamente por ChatGPT ou '
 'Jenni AI, comparados a rascunhos escritos por humanos. Foram encomendados aos dois sistemas tres '
 'artigos, sobre "History of Digital Education in Austria", "A History of Women in Computer Science" e '
 '"Modelling of Mental Arithmetic Strategies Using UML". A conclusao versa sobre esforco criativo, '
 'originalidade e rigor academico da redacao. ',
 'DISCUSSAO: a unica ocorrencia de UML no registro esta no TITULO DE UM DOS ARTIGOS ENCOMENDADOS a IA. '
 'E armadilha lexical: a UML e assunto de um texto gerado, e nao artefato gerado. O que o LLM produz '
 'aqui e prosa cientifica, e o que o estudo avalia e a qualidade dessa prosa. Pelo B1, a saida nao e '
 'UML e nao ha componente UML separavel a destacar: nenhum diagrama e produzido, avaliado ou sequer '
 'mencionado como artefato. Nao se aplica o terceiro caso do B1, porque nao ha obscuridade quanto ao '
 'artefato. Pela regra de ouro 5, falha de saida e I5/E7. Pela regra de ouro 3, o B1 decide e os '
 'subportoes seguintes nao chegam a ser avaliados. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Registre-se a armadilha lexical para o '
 'relato de metodo: correspondencia por titulo de artefato encomendado ao LLM, e nao por artefato '
 'produzido. '),

'744_SCOPUS':('B1_E7','',
 'EVIDENCIA: o resumo trata de deteccao de fraude em sinistros de plano de saude sobre blockchain, com '
 'LLM e recuperacao aumentada. O que o trabalho produz sao julgamentos de fraude e mecanismos de '
 'integridade de dados; nao ha artefato de modelagem entre os resultados. ',
 'DISCUSSAO: pelo B1 a saida nao e UML e nao ha componente UML separavel. O resumo e claro sobre o que '
 'o trabalho produz, de modo que nao se aplica o terceiro caso do B1. Pela regra de ouro 5, falha de '
 'saida e I5/E7, e nao E6, reservado a origem. Pela regra de ouro 3, o B1 decide. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. '),

'757_SCOPUS':('B1_E7','',
 'EVIDENCIA: o titulo — "Unintended Changes: How LLMs Corrupt and Correct Textual Models" — e o resumo '
 'descrevem avaliacao de em que medida abordagens de desenvolvimento dirigido a modelos assistidas por '
 'IA alteram involuntariamente partes de um modelo, afetando-lhe a semantica, PARTICULARMENTE QUANDO O '
 'MODELO E DEFINIDO EM UMA LINGUAGEM ESPECIFICA DE DOMINIO desconhecida do LLM. Discute ainda o uso da '
 'metrica de perplexidade como indicador de linguagens de modelagem suscetiveis. As palavras-chave '
 'declaram DSL, MDE e AI4SE. ',
 'DISCUSSAO: o objeto do trabalho sao modelos textuais em linguagens especificas de dominio, e o '
 'proprio recorte experimental depende de a linguagem ser DESCONHECIDA do LLM — condicao que exclui a '
 'UML, que e das notacoes mais representadas nos corpora de treino. Pelo B1, a saida nao e UML e nao '
 'ha componente UML separavel. Este registro entrou na fila de leitura por termos de engenharia '
 'dirigida a modelos, nao por mencao a UML como artefato. Pela regra de ouro 5, falha de saida e '
 'I5/E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B1. Observacao para o relato de metodo: o '
 'trabalho e sobre preservacao semantica em modelos textuais, tema vizinho ao da revisao, mas a '
 'notacao nao e UML. '),

'678_IEEE':('B2_E6','',
 'EVIDENCIA: "UML" e palavra-chave declarada pelos autores e o resumo confirma a presenca de conteudo '
 'UML: a interacao do usuario e facilitada por "UML-based visual representations" que permitem '
 'compreensao intuitiva da implementacao do contrato inteligente. A ferramenta tem quatro componentes '
 'nomeados: um Codec para codificacao e decodificacao do contrato, um Auditor apoiado no Slither para '
 'avaliacao de seguranca, um banco de dados para controle de versao, e um Assistente de IA baseado em '
 'gpt-3.5-turbo PARA ANOTACOES AUTOMATIZADAS. A avaliacao usa o questionario NASA-TLX, instrumento de '
 'carga de trabalho. ',
 'DISCUSSAO: o B1 passa, ha conteudo UML no trabalho. O B2 e que decide, e decide com clareza. O '
 'resumo atribui papeis nominais a cada componente, e o papel do LLM esta circunscrito: ANOTACOES. As '
 'representacoes visuais UML derivam do contrato inteligente pelo Codec e pelos componentes de '
 'visualizacao, nao do gpt-3.5-turbo. Pela RF-02, o que decide e quem detem a autoridade semantica '
 'sobre os elementos UML portadores de significado; aqui essa autoridade e do decodificador do '
 'contrato, e o LLM opera sobre a camada de comentario. Pela regra de ouro 5, falha de origem e I2/E6. '
 'Registre-se que, ainda que o B2 passasse, a entrada seria codigo de contrato inteligente, o que '
 'levaria a E9 em B4 pela delimitacao de escopo; mas pela regra de ouro 3 o criterio primario e o '
 'primeiro portao que explica claramente o caso, e esse e o B2. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. '),

'740_SCOPUS':('B2_E6','',
 'EVIDENCIA: ha conteudo UML abundante e declarado. O resumo propoe metodologia conforme a Arquitetura '
 'Dirigida a Modelos que adota diagrama de sequencia e diagrama de classes UML como descritor do '
 'modelo independente de plataforma, um modelo especifico de plataforma generico baseado em regras de '
 'producao, e um PERFIL UML desenvolvido pelos autores para suprir lacunas do modelo de sequencia. O '
 'mapeamento entre PIM e PSM e automatizado por QVT. A unica mencao a modelo de linguagem esta na '
 'PRIMEIRA FRASE do resumo, de carater retorico: "Symbolic AI is indispensable for the current LLM '
 'agents that are used for example to reason the context of the questions". ',
 'DISCUSSAO: o B1 passa com folga. O B2 decide: nao ha LLM algum no metodo proposto. A frase de '
 'abertura situa o trabalho no debate sobre IA simbolica e agentes, sem que nenhum modelo de linguagem '
 'participe da producao dos diagramas. A autoridade semantica sobre as classes, as mensagens do '
 'diagrama de sequencia e o perfil UML e integralmente dos autores e das transformacoes QVT, que sao '
 'regras deterministas. Pela RF-02, e exatamente o caso de coocorrencia de mencao a LLM e a UML no '
 'mesmo resumo sem relacao produtiva entre eles. Pela regra de ouro 5, falha de origem e I2/E6, nao '
 'E7: a saida E UML, o que falta e o LLM. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. Registre-se para o relato de metodo que a '
 'correspondencia veio de mencao retorica a LLM na frase de abertura, padrao recorrente na busca. '),

'753_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo apresenta o UML Miner, plugin do Visual Paradigm para apoiar o ENSINO e a '
 'APRENDIZAGEM de UML, que captura e analisa as atividades de modelagem DOS ESTUDANTES para devolver '
 'realimentacao personalizada e sensivel ao contexto. A ferramenta registra acoes de modelagem em log '
 'de eventos, armazena para cada diagrama uma descricao em linguagem natural e a representacao XML, '
 'reconstroi o comportamento de modelagem por mineracao de processos e o compara com um modelo de '
 'referencia. As palavras-chave declaram verificacao de conformidade, descoberta de processos, '
 'recuperacao aumentada e modelos de linguagem de grande porte. ',
 'DISCUSSAO: o B1 passa, ha diagramas UML no trabalho. O B2 decide: quem produz os diagramas sao os '
 'ESTUDANTES; o LLM entra a jusante, para gerar realimentacao textual sobre o processo de modelagem '
 'reconstruido. Pela RF-02, a autoridade semantica sobre os elementos UML e dos estudantes, e o LLM '
 'nao propoe, nao gera nem revisa elementos portadores de significado — comenta o comportamento de '
 'quem os produziu. Pela regra de ouro 5, falha de origem e I2/E6. Registre-se que, ainda que se '
 'entendesse o LLM como operando sobre o diagrama, o desfecho seria E8 em B3 (UML existente -> LLM -> '
 'avaliacao, explicacao, critica, sem alteracao do modelo), tambem exclusao; mas o B2 e o primeiro '
 'portao que explica claramente o caso. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. '),

'754_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo relata estudo educacional que aplica o Block Model para segmentar conteudo '
 'instrucional de programacao orientada a objetos em Java e integra diagramas de classes UML a esse '
 'modelo para compor um arcabouco de ensino estruturado. Os resultados sao ganhos significativos no '
 'pos-teste dos ESTUDANTES. A IA generativa aparece ao final, como perspectiva de personalizacao '
 'adaptativa, e nao como componente do arcabouco avaliado. ',
 'DISCUSSAO: o B1 passa, ha diagramas de classes UML. O B2 decide: os diagramas integram o material '
 'didatico e sao de autoria dos docentes ou dos estudantes; nenhum modelo de linguagem os produz. A '
 'variavel medida e o desempenho de aprendizagem, nao propriedade de artefato gerado por LLM. Pela '
 'RF-02 nao ha autoridade semantica de LLM sobre elemento UML algum. Pela regra de ouro 5, falha de '
 'origem e I2/E6. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E6, decidido em B2. '),

'019_ACM':('B3_E7','',
 'EVIDENCIA: o resumo descreve o OCPPuzz, arcabouco de fuzzing baseado em especificacao para sistemas '
 'de gestao de estacoes de recarga. A frase decisiva quanto a direcao e esta: o arcabouco extrai '
 'automaticamente estruturas de mensagem, restricoes de campo e regras de dependencia da especificacao '
 'do protocolo OCPP, "as well as valid CS-CSMS state transitions described in its USE CASE DIAGRAMS". '
 'Para lidar com especificacoes expressas em linguagem natural e em diagramas semiformais, combina '
 'extracao por regras heuristicas com um LLM. Os resultados sao 930 defeitos de implementacao e 155 '
 'defeitos de especificacao reportados. ',
 'DISCUSSAO: B1 e B2 passam: ha conteudo UML — diagramas de casos de uso — e ha LLM operando sobre '
 'ele. O B3 decide. A direcao e diagrama UML EXISTENTE -> LLM -> entradas de teste e relatorios de '
 'defeito. O UML e INSUMO, e o produto e material de teste. E a terceira linha da matriz da secao 4.3, '
 '"UML existente -> LLM -> codigo, testes, documentacao", cujo desfecho e E7. Nao e E8: o E8 pressupoe '
 'que a tarefa seja avaliar, explicar ou criticar o proprio diagrama, e aqui o diagrama nao e objeto '
 'de juizo, e fonte de conhecimento para gerar casos de teste do sistema sob teste. Nao e E6: ha LLM '
 'com papel substantivo na interpretacao dos diagramas semiformais. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B3. O desfecho registra B3_E7 e nao B1_E7 '
 'porque HAVIA conteudo UML no trabalho, na entrada; a distincao e exigida pela secao 6.1 do manual e '
 'perdida se apenas o codigo for gravado. '),

'090_ACM':('B3_E7','',
 'EVIDENCIA: o resumo apresenta o RealBench, benchmark de geracao de codigo em nivel de repositorio '
 'alinhado a pratica industrial. A frase decisiva e: "Each example includes both natural language '
 'requirements and UML DIAGRAMS AS SYSTEM DESIGN, matching how developers typically receive '
 'specifications". Entre os achados, os autores relatam que "LLMs are good at finding and creating '
 'modules DEFINED IN UML DIAGRAMS, but the quality of generated modules is often poor due to grammar '
 'and logic errors". ',
 'DISCUSSAO: B1 e B2 passam: ha conteudo UML e ha LLMs. O B3 decide, e de forma limpida. Os diagramas '
 'UML integram a ENTRADA de cada exemplo do benchmark, ao lado dos requisitos textuais; o produto '
 'avaliado e codigo em nivel de repositorio, com cinco metricas e duas granularidades. E a terceira '
 'linha da matriz da secao 4.3, "UML existente -> LLM -> codigo", cujo desfecho e E7. A qualidade '
 'medida no resumo — erros de gramatica e de logica — e a do CODIGO gerado, nao a de qualquer diagrama '
 'produzido, o que confirma que o artefato de interesse do estudo nao e UML. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B3. O desfecho preserva o sub-portao: havia '
 'UML na entrada, e o produto e codigo. '),

'746_SCOPUS':('B3_E7','',
 'EVIDENCIA: o resumo investiga o uso do ChatGPT-4 para reduzir complexidade acidental em '
 'transformacoes de modelo. A frase decisiva e: "Using a semi-automated pipeline, we applied ChatGPT-4 '
 'to 99 UML CLASS DIAGRAM MODELS, GENERATING JAVA PROGRAMS and comparing them with ground truth '
 'programs created by a state-of-the-art modelling tool". Os resultados sao taxas cumulativas de '
 'sucesso de 94% apos tres iteracoes, caindo a 17% em modelos complexos. ',
 'DISCUSSAO: B1 e B2 passam: ha 99 diagramas de classes UML e ha o ChatGPT-4. O B3 decide. A direcao e '
 'diagrama de classes UML -> LLM -> programa Java: o UML e ENTRADA e o produto e codigo. E exatamente '
 'a terceira linha da matriz da secao 4.3, cujo desfecho e E7. A comparacao com programas de '
 'referencia confirma que a variavel medida e propriedade do CODIGO gerado, nao do modelo. Pela '
 'delimitacao de escopo fixada em 2026-08-16, a revisao trata da sintese direta de conteudo UML a '
 'partir de especificacao textual; transformacao de UML em codigo esta expressamente fora. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E7, decidido em B3. O desfecho preserva o sub-portao: havia '
 'UML na entrada, e o produto e codigo. '),

'616_IEEE':('B3_E8','',
 'EVIDENCIA: o titulo anuncia revisao automatica, sensivel a diagramas, de documentos de projeto de '
 'software por modelos de linguagem multimodais. O resumo situa o trabalho como continuacao de '
 'pesquisa anterior sobre revisao automatizada de documentos compostos de texto e tabelas, e declara '
 'que agora "diagram-based artifacts such as UML or screen transition diagrams" entram no escopo da '
 'analise. Diz que revisar tais documentos exige interpretacao acurada de elementos estruturais e '
 'semanticos, incluindo nos, arestas e condicoes de transicao, e propoe metodo hibrido de compreensao '
 'de diagramas. ',
 'DISCUSSAO: B1 e B2 passam: ha conteudo UML e ha LLMs multimodais. O B3 decide. A direcao e diagrama '
 'UML JA EXISTENTE, integrante do documento de projeto -> LLM -> revisao. O UML e insumo e nada nele e '
 'alterado: o produto e um parecer de revisao sobre o documento. E a segunda linha da matriz da secao '
 '4.3, "UML existente -> LLM -> avaliacao, explicacao, critica", cujo desfecho e E8, e satisfaz a '
 'condicao restritiva da secao 3 para o E8 ("so exclui quando o resumo deixa claro que o diagrama ja '
 'existe e nao e alterado"), que aqui esta satisfeita. Pela regra de ouro 5, falha de tarefa e I3/E8, '
 'e nao E6 nem E7. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. Registre-se para o relato de metodo que '
 'este e um caso limpido do E8: a revisao de artefatos UML por LLM multimodal e literalmente a tarefa '
 'do trabalho. '),

'750_SCOPUS':('B3_E8','',
 'EVIDENCIA: o titulo anuncia assistencia a partes interessadas na INTERPRETACAO de diagramas de '
 'classes com LLMs. O resumo parte da dificuldade de alguns interessados em lidar com representacoes '
 'visuais e explora o uso de LLMs para assisti-los fornecendo EXPLICACOES TEXTUAIS AUTOMATICAS e '
 'orientacao contextual, ajudando-os a interpretar elementos de notacao e a compreender a estrutura e '
 'o significado do diagrama. "Class diagrams" consta das palavras-chave. ',
 'DISCUSSAO: B1 e B2 passam: ha diagramas de classes e ha LLMs. O B3 decide. A direcao e diagrama de '
 'classes JA EXISTENTE -> LLM -> explicacao textual. O UML e insumo e nao e alterado: o produto e '
 'prosa explicativa dirigida ao interessado. O fluxograma nomeia essa exata situacao no segundo caso '
 'do B3, que arrola "avaliacao, EXPLICACAO, resumo, classificacao, critica" como tarefas que levam ao '
 'E8, e a matriz da secao 4.3 repete "explicacao". A condicao restritiva da secao 3 esta satisfeita: o '
 'diagrama ja existe e nao e alterado. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. Registre-se que o trabalho e declarado '
 '"work in progress", o que nao muda o desfecho, ja decidido pela direcao do fluxo. '),

'756_SCOPUS':('B3_E8','',
 'EVIDENCIA: o titulo anuncia o estabelecimento de RASTREABILIDADE entre requisitos em linguagem '
 'natural e artefatos de software combinando recuperacao aumentada e LLMs. O resumo especifica o elo: '
 'rastreabilidade de requisitos de casos de uso em linguagem natural ate CLASSES DE UM DIAGRAMA DE '
 'CLASSES UML, e destas ate a implementacao em codigo. Justifica a necessidade pela avaliacao de '
 'impacto de mudancas e pela reusabilidade. ',
 'DISCUSSAO: B1 e B2 passam: ha diagrama de classes UML e ha LLMs. O B3 decide. Tanto os requisitos '
 'quanto o diagrama de classes JA EXISTEM; o produto do trabalho sao ELOS DE RASTREABILIDADE entre '
 'eles. Nenhum elemento UML e criado, alterado ou reparado: o LLM classifica correspondencias. E a '
 'segunda linha da matriz da secao 4.3, na modalidade classificacao, cujo desfecho e E8, e a condicao '
 'restritiva da secao 3 esta satisfeita, pois o resumo deixa claro que o diagrama ja existe e nao e '
 'alterado. Pela regra de ouro 5, falha de tarefa e I3/E8. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E8, decidido em B3. '),

'215_ACM':('B4_E9','',
 'EVIDENCIA: o titulo anuncia consistencia dirigida por IA de diagramas SysML. O resumo trata da '
 'manutencao de consistencia entre VISTAS de linguagens graficas de modelagem, observa que metodos '
 'tradicionais baseados em regras sao insuficientes em linguagens como a UML, e apresenta arcabouco '
 'que automatiza a DETECCAO E A CORRECAO de inconsistencias entre vistas, com regras formalmente '
 'definidas e o GPT da OpenAI, implementado na ferramenta TTool. O foco declarado e a consistencia '
 'entre diagramas de CASO DE USO e diagramas de BLOCOS. ',
 'DISCUSSAO: B1 passa: ha componente UML separavel, porque o diagrama de casos de uso do SysML v1 '
 'reusa o metamodelo da UML — a distincao entre SysML v1, perfil da UML, e SysML v2, autonomo sobre '
 'KerML, foi fixada em evento de INTERPRETACAO_PROTOCOLO. B2 passa: o GPT e nomeado. O B3 nao decide: '
 'o segundo caso do B3 e o E8 exigem, pela condicao restritiva da secao 3, que o diagrama ja exista E '
 'NAO SEJA ALTERADO, e aqui ele e alterado, pois o arcabouco nao so detecta como CORRIGE as '
 'inconsistencias. Ha, portanto, producao de conteudo UML, e o registro segue ao B4. O B4 e que '
 'decide: a entrada sao MODELOS SysML JA EXISTENTES, sem componente textual de requisitos. Pela '
 'delimitacao de escopo fixada em 2026-08-16, o objeto da revisao e a sintese direta de conteudo UML a '
 'partir de especificacao textual em linguagem natural; e a secao 3 do manual admite o E9 quando o '
 'resumo declara explicitamente entrada de codigo, imagem, MODELO EXISTENTE ou logs, sem componente '
 'textual de requisitos, que e precisamente este caso. ',
 'DECISAO DA PESQUISADORA: EXCLUIDO por E9, decidido em B4. Registre-se que a exclusao NAO se apoia no '
 'B3: o reparo de modelo altera conteudo UML e por isso nao e E8. Este e o decimo registro do conjunto '
 'de E9 nomeado no evento de INTERPRETACAO_PROTOCOLO da delimitacao de escopo, e como aqueles e '
 'recuperavel sem re-triagem caso o I4 venha a ser emendado para admitir modelo existente como '
 'entrada. Trata-se de reparo de modelo, subarea vizinha e forte, cuja saida e consequencia consciente '
 'da delimitacao. '),
}

assert len(D)==24, len(D)
CRIT={'B1_E7':'E7','B2_E6':'E6','B3_E7':'E7','B3_E8':'E8','B4_E9':'E9'}

rows=list(csv.reader(open(CSV,encoding='utf-8'))); i={c:n for n,c in enumerate(rows[0])}
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

with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

grp={}
for k,v in D.items(): grp.setdefault(v[0],[]).append(k)
with open(LOG,'a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    w.writerow([';'.join(sorted(D)),AGORA,REV,'DECISAO_GATE','B','','',
     'Primeiro lote de leitura individual dos 185 registros que mencionam UML no titulo ou no resumo: '
     '24 registros triados. Desfechos: 10 RETIDOS, 3 E7 em B1, 4 E6 em B2, 3 E7 em B3, 3 E8 em B3 e 1 '
     'E9 em B4. Quatro sao candidatos centrais sem qualquer ressalva (467_IEEE, 748_SCOPUS, '
     '749_SCOPUS, 742_SCOPUS): geracao de UML a partir de requisitos por LLM com avaliacao declarada '
     'do artefato. Tres decisoes merecem registro proprio. (1) 215_ACM foi excluido por E9 em B4, e '
     'NAO por E8: o arcabouco nao apenas detecta como CORRIGE inconsistencias entre diagramas SysML, '
     'de modo que ha alteracao de conteudo UML e a condicao restritiva do E8 na secao 3 do manual '
     '("so exclui quando o diagrama ja existe e nao e alterado") nao se satisfaz; o que o exclui e a '
     'entrada ser modelo existente, sem componente textual de requisitos. E o decimo registro do '
     'conjunto de E9 alcancado pela delimitacao de escopo, recuperavel sem re-triagem. (2) 739_SCOPUS '
     'e armadilha lexical de tipo novo: a unica ocorrencia de UML esta no TITULO DE UM DOS ARTIGOS '
     'ENCOMENDADOS ao ChatGPT ("Modelling of Mental Arithmetic Strategies Using UML"); a UML e assunto '
     'de texto gerado, nao artefato gerado. (3) 740_SCOPUS traz UML farta e propria (diagrama de '
     'sequencia, diagrama de classes e um perfil UML desenvolvido pelos autores), mas a unica mencao a '
     'modelo de linguagem esta na frase retorica de abertura do resumo; e coocorrencia sem relacao '
     'produtiva, decidida por E6 em B2 pela RF-02.',
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
