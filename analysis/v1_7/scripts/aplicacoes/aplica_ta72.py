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
'796_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o produto final declarado no titulo e no resumo e codigo de workflow para operacao de '
 'redes. Mas o metodo decompoe a geracao em quatro passos explicitos — "API selection, dataflow '
 'analysis, SEQUENCE DIAGRAM DESIGN, and workflow code generation" — e os resultados experimentais '
 'atribuem o ganho de acuracia justamente a "inclusion and precise sequencing of intermediate steps". ',
 'DISCUSSAO: a tentacao e classificar E7 em B3, porque o entregavel e codigo. Seria erro de ordem. '
 'Em B3 o que exclui e a UML estar na ENTRADA e o produto ser codigo; aqui nao ha UML alguma na '
 'entrada, que e linguagem natural, e o diagrama de sequencia e PRODUZIDO pelo proprio LLM a partir '
 'dela. Logo a celula da matriz da secao 4.3 e requisitos -> LLM -> UML, que retem, e o codigo e '
 'consumidor a jusante, nao substituto. Resta a duvida do B1: o resumo nomeia o tipo de diagrama '
 '(sequencia), o que satisfaz o segundo caso, mas nao declara que seja UML nem qual sintaxe portadora '
 'usa, e o passo pode ser mera cadeia de pensamento estruturada em texto. Ha ainda medicao de acuracia, '
 'mas do CODIGO, nao do diagrama, de sorte que a evidencia de qualidade sobre conteudo UML fica a '
 'verificar no texto completo. ',
 'DECISAO: retido com INCERTO_SAIDA e EVIDENCIA=A_VERIFICAR. Pela regra de ouro 1 a incerteza retem; '
 'a leitura do texto completo deve confirmar se o passo intermediario materializa diagrama de '
 'sequencia UML e se ha qualquer medida sobre ele.'),

'797_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o resumo propoe agente conversacional que conduz interessados por fluxos de dialogo '
 'estruturado, "translating their natural language inputs into a formal CIM-Domain Specific Language '
 '(CIM-DSL)", e afirma que "these DSL commands are then transformed into CIM artifacts, such as '
 'Business Process Model and Notation (BPMN) diagrams and UNIFIED MODELING LANGUAGE (UML) USE CASES". '
 'Declara ainda que "the approach emphasizes quality assurance through interactive validation, '
 'consistency checks, and strategies to mitigate LLM limitations". ',
 'DISCUSSAO: B1 satisfeito, porque o resumo nomeia caso de uso, tipo arrolado na tabela da secao 4.1. '
 'B4 satisfeito, porque a entrada e fala do interessado em linguagem natural. B3 satisfeito, porque a '
 'direcao e texto -> modelo. O ponto delicado e o B2 sob a RF-02: a etapa DSL -> artefato UML e '
 'transformacao simbolica determinista, e poderia parecer que a autoridade semantica nao e do LLM. Nao '
 'e o caso: quem decide QUAIS casos de uso, QUAIS atores e QUAIS relacoes existem e o LLM, ao produzir '
 'os comandos da DSL; a transformacao posterior apenas troca a sintaxe portadora. A RF-02 e expressa '
 'em que regras simbolicas no pipeline sao irrelevantes, importando quem determina o conteudo '
 'semantico. Quanto ao I6, o resumo fala em garantia de qualidade e verificacao de consistencia, mas o '
 'verbo dominante e prospectivo ("We anticipate this method will significantly improve"), o que sugere '
 'artigo de proposta sem avaliacao empirica consumada. ',
 'DECISAO: retido, com CANDIDATO_E10 pelo risco de ser proposta sem estudo, e EVIDENCIA=A_VERIFICAR. '
 'O E10 e de baixa e nao e decidivel em titulo e resumo (manual, secao 3).'),

'801_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: ferramenta em prototipo inicial para projeto conceitual automatizado de banco de dados, '
 'com prompting zero-shot e escolha entre tres LLMs de ponta pelo usuario. O resumo diz que a '
 'ferramenta "enables automatic synthesis of the target conceptual database model represented by a '
 'PlantUML model" e que "the preliminary evaluation results imply very high effectiveness of LLM-based '
 'CDM synthesis". A palavra-chave AUTORAL de abertura e "class diagram", seguida de "conceptual '
 'database model", "LLM" e "PlantUML". ',
 'DISCUSSAO: aqui o PlantUML nao e sinal ambiguo, porque a palavra-chave autoral "class diagram" '
 'declara o tipo de diagrama, resolvendo o segundo caso do B1 (contraste com 759_SCOPUS, em que o '
 'PlantUML servia para desenhar arvore de falhas). O modelo conceitual de dados expresso como diagrama '
 'de classes e conteudo UML portador de significado. Entrada textual, direcao texto -> modelo, LLM com '
 'autoridade semantica plena: B2, B3 e B4 passam sem atrito. Ha avaliacao preliminar de efetividade, '
 'mas o resumo nao nomeia metrica nem gabarito. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR. O I6 depende de identificar, no texto completo, que '
 'construto de qualidade a "efetividade" operacionaliza.'),

'802_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo declara "Automated Feature Extraction and UML Modeling from Real-World '
 'Unstructured Egyptian Arabic Text". A entrada sao publicacoes, comentarios, opinioes e realimentacao '
 'de usuarios em plataformas digitais, tratados como fonte primaria para mineracao e modelagem de '
 'requisitos. As palavras-chave autorais sao "embeddings; feature mining; feature modeling; '
 'hierarchical clustering; large language models; natural language processing; topic modeling; USE '
 'CASE DIAGRAMS". ',
 'DISCUSSAO: B1 satisfeito, porque diagrama de casos de uso e nomeado como palavra-chave autoral. B4 '
 'satisfeito de modo exemplar: texto nao estruturado em linguagem natural de dominio, exatamente a '
 'delimitacao de escopo fixada para o I4. B3 satisfeito. O ponto aberto e o B2 sob a RF-01 e a RF-02: '
 'a pilha metodologica anunciada e majoritariamente NAO gerativa — embeddings, modelagem de topicos e '
 'agrupamento hierarquico —, e os LLMs aparecem na lista sem que o resumo diga em que etapa atuam. Se '
 'os LLMs so produzem representacoes vetoriais ou rotulos de topico e o diagrama for montado por '
 'heuristica sobre os agrupamentos, a autoridade semantica sobre os elementos UML nao e do LLM e o '
 'caso seria E6. Se os LLMs sintetizam os atores e os casos de uso, retem. O resumo nao permite '
 'distinguir. ',
 'DECISAO: retido com INCERTO_PAPEL_LLM. A RF-01 e expressa em que, quando o titulo e o resumo nao '
 'permitem distinguir uso gerativo de uso classificatorio, o registro e retido para leitura integral.'),

'803_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o titulo e "UML Sequence Diagram Generation: A Multi-Model, Multi-Domain Evaluation". O '
 'resumo investiga o uso de LLMs para automatizar a geracao de diagramas de sequencia UML A PARTIR DE '
 'REQUISITOS EM LINGUAGEM NATURAL, e avalia tres LLMs de ponta — GPT-4o, Mixtral 8x7B e Llama 3.1 8B — '
 'em multiplos conjuntos de dados, publicos e proprios. ',
 'DISCUSSAO: todos os quatro subportoes passam sem ambiguidade. Tipo de diagrama nomeado no titulo '
 '(B1); tres LLMs nomeados como agentes geradores (B2); direcao requisitos -> UML (B3); entrada '
 'textual de requisitos (B4). E o caso paradigmatico da delimitacao de escopo desta revisao. O I6 esta '
 'satisfeito ja no titulo: o desenho do estudo E uma avaliacao comparativa multimodelo e multidominio, '
 'de modo que ha necessariamente construto de qualidade operacionalizado sobre a UML gerada. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central; prioridade alta na fila de extracao.'),

'806_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: o titulo e "LLM-Driven MDA Pipeline for Generating UML Class Diagrams and Code". O resumo '
 'combina interpretacao de linguagem natural por modelos transformadores com estruturacao explicita de '
 'conceitos por uma DSL, "designed as a pivotal intermediate layer", assegurando continuidade entre '
 'extracao semantica, modelagem UML e geracao automatica de codigo Python. O pipeline "follows a '
 'structured progression from text to model to code". ',
 'DISCUSSAO: B1 satisfeito (diagrama de classes nomeado no titulo e na primeira palavra-chave '
 'autoral). B4 satisfeito (especificacoes textuais). B3 e o subportao que exige cuidado, porque o '
 'codigo tambem e produto: a distincao do manual e entre B1_E7, em que nunca houve UML, e B3_E7, em '
 'que a UML esta na ENTRADA e o produto e codigo. Nenhum dos dois se aplica, pois aqui a UML e '
 'PRODUZIDA a partir do texto e so depois consumida pelo gerador de codigo, replicando a estrutura de '
 '796_SCOPUS. B2 satisfeito, com a mesma leitura da RF-02 aplicada a 797_SCOPUS: a camada DSL e '
 'simbolica, mas o conteudo semantico vem do transformador. Observe-se que o resumo diz "transformer '
 'models" e a palavra-chave diz "LLMs", sem nomear modelo especifico. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR. Verificar no texto completo se ha medida sobre o diagrama '
 'de classes ou apenas sobre o codigo gerado.'),

'809_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "Large Language Models for UML Class Diagram Modeling: A Preliminary Empirical '
 'Evaluation". Os autores constroem "a difficulty-stratified dataset of 30 UML class diagram '
 'exercises" e propoem "an automated weighted evaluation metric over generated PlantUML code", '
 'observando que ambos "are rarely constructed and systematically applied". Criticam a literatura '
 'existente por concentrar-se em modelos unicos e fechados com estrategias simples de prompting, sem '
 'comparacao sistematica entre tipos de modelo, tecnicas de engenharia de prompt e refinamento '
 'iterativo. Palavras-chave autorais: refinamento iterativo, LLMs, engenharia de prompt, diagrama de '
 'classes UML. ',
 'DISCUSSAO: os quatro subportoes passam. Registro de valor metodologico excepcional para esta '
 'revisao: nao apenas satisfaz o I6, como PROPOE uma metrica ponderada de avaliacao, isto e, contribui '
 'com instrumento de medicao de qualidade, que e o objeto declarado da revisao. O refinamento '
 'iterativo tambem interessa, por caracterizar reparo de conteudo UML, tarefa admitida pelo I3. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central e provavel fonte de instrumento na '
 'sintese; prioridade maxima na fila de extracao.'),

'810_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: VeriGen, arcabouco de automacao ponta a ponta do ciclo de vida, de especificacao de '
 'requisitos a geracao de codigo. O resumo situa o trabalho reconhecendo que a pesquisa anterior tratou '
 'de subtarefas fragmentadas, entre elas "requirements formalization, UML CLASS DIAGRAM GENERATION, UML '
 'SEQUENCE DIAGRAM GENERATION, and skeletal code generation", e declara como problema que "unreliable '
 'outputs are frequently caused by instability, omissions, and HALLUCINATIONS in LLM-generated '
 'artifacts". Palavras-chave autorais incluem "sequence diagram generation" e "RUPPs templates". ',
 'DISCUSSAO: B1 satisfeito, porque diagramas de classes e de sequencia sao nomeados e a palavra-chave '
 'autoral confirma que a geracao de diagrama de sequencia integra o proprio arcabouco, e nao apenas a '
 'resenha. B4 satisfeito: os modelos RUPP sao gabaritos de sentenca de requisito em linguagem natural '
 'estruturada, entrada textual tipica. B3 satisfeito pela mesma razao de 806_SCOPUS: a UML e produzida '
 'a partir do texto, o codigo vem depois. B2 satisfeito. Quanto ao I6, o resumo nomeia instabilidade, '
 'omissoes e alucinacoes como problemas atacados, o que e vocabulario de qualidade, mas nao declara '
 'metrica nem estudo. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR. Verificar se a verificacao anunciada no nome VeriGen '
 'produz medida sobre os diagramas ou apenas sobre o codigo.'),

'811_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "Comparative Structural and Semantic Evaluation of Fine-Tuned Large Language '
 'Models for UML Activity Diagram Generation". O resumo declara que a criacao manual de diagramas de '
 'atividade a partir de requisitos em linguagem natural e demorada e sujeita a erro, e que os LLMs '
 'recentes "lack the ability to maintain STRUCTURAL AND SEMANTIC CORRECTNESS". Explora LLMs de codigo '
 'aberto para geracao automatica de diagramas de atividade PlantUML executaveis a partir de requisitos '
 'em linguagem natural, com tres modelos ajustados por instrucao, entre eles Qwen 2.5-Coder. '
 'Palavras-chave autorais incluem "Direct Preference Optimization" e "Supervised FineTuning". ',
 'DISCUSSAO: os quatro subportoes passam sem ambiguidade. O I6 esta no proprio titulo, com dois '
 'construtos de qualidade distintos e nomeados — correcao estrutural e correcao semantica —, o que faz '
 'deste um registro de alto valor para a taxonomia de metricas da sintese. O ajuste fino nao afeta o '
 'I2: modelos ajustados por instrucao continuam sendo LLMs em uso gerativo, e a RF-01 so restringe '
 'codificadores pre-instrucionais em uso nao gerativo. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central; prioridade alta na fila de extracao.'),

'812_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR;CANDIDATO_E10',
 'EVIDENCIA: ferramenta que "converts natural language inputs into MBSE models by combining large '
 'language models, natural language processing techniques, and retrieval augmented generation with '
 'MBSE software APIs". O sumario dirigido a pesquisadores especifica que "the tool\'s core capabilities '
 'include the automatic creation of SysML components like BLOCK DEFINITION DIAGRAMS and STATE MACHINE '
 'DIAGRAMS, as well as reading and analyzing the models". A ferramenta e apresentada como agente '
 'conversacional em que o usuario pede atualizacoes de modelo. ',
 'DISCUSSAO: o B1 exige decidir a questao SysML. A regra fixada e que a SysML v1 e perfil da UML e '
 'reusa atividade, sequencia, maquina de estados e caso de uso do metamodelo, havendo componente '
 'separavel quando o resumo nomeia um desses tipos, ao passo que a v2, construida sobre KerML sem '
 'reuso do metamodelo, sai por E7. Duas evidencias fixam a v1: o resumo nomeia expressamente DIAGRAMA '
 'DE MAQUINA DE ESTADOS, que e tipo UML reusado; e "block definition diagram" e vocabulario da v1, '
 'substituido por "part definition" na v2. Logo ha componente UML separavel. B4 satisfeito (entrada em '
 'linguagem natural, com RAG apenas fornecendo contexto documental). B3 satisfeito. B2 satisfeito. '
 'Note-se que a ferramenta tambem le e analisa modelos, mas isso e capacidade adicional, e nao o '
 'converte em caso de E8, pois a criacao automatica e declarada como capacidade central. Quanto ao I6, '
 'o resumo e de artigo de ferramenta, com afirmacoes de produtividade e acuracia sem estudo declarado. ',
 'DECISAO: retido com EVIDENCIA=A_VERIFICAR e CANDIDATO_E10. A extracao deve confirmar se ha avaliacao '
 'e se ela incide sobre os diagramas de maquina de estados, unico componente UML inequivoco.'),

'813_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: o resumo formula a geracao de diagramas UML como tarefa estruturada de traducao '
 'automatica a partir de requisitos em linguagem natural, e propoe duas abordagens transformadoras: um '
 'modelo sequencia-a-sequencia para geracao direta do codigo do diagrama e um modelo '
 'sequencia-a-arvore-de-sintaxe-abstrata que incorpora restricoes sintaticas "to ensure structural '
 'correctness while maintaining the intended semantics". Ha aprendizado multitarefa com extracao de '
 'elementos UML e recomendacao de padroes de projeto reusaveis. Os resultados indicam que "the '
 'proposed framework achieves accuracy comparable to GENERAL-PURPOSE LARGE LANGUAGE MODELS while '
 'offering greater determinism". ',
 'DISCUSSAO: B1, B3 e B4 passam. O B2 e o problema, e e problema de fronteira do I2, nao de leitura. '
 'Os modelos propostos sao transformadores treinados para a tarefa, e a propria frase de resultado os '
 'CONTRAPOE aos "general-purpose large language models", usados como linha de base. Pela RF-01, '
 'codificadores nao satisfazem o I2 automaticamente, mas satisfazem quando o uso e gerativo e '
 'semanticamente constitutivo do conteudo UML — e aqui e exatamente esse o uso, pois o Seq2Seq e o '
 'Seq2AST GERAM o codigo do diagrama e determinam quais classes e relacoes existem. Persiste, todavia, '
 'a duvida quanto a escala e a natureza dos modelos, que o resumo nao informa, e quanto a se a linha de '
 'base por LLM de proposito geral e ela propria objeto de avaliacao no estudo — hipotese em que o '
 'registro interessa duplamente. O I6 esta satisfeito: acuracia medida, correcao estrutural e '
 'preservacao semantica declaradas como criterios, e artefatos publicos. ',
 'DECISAO: retido com INCERTO_PAPEL_LLM e EVIDENCIA=EXPLICITA. Pela regra de ouro 1, a incerteza sobre '
 'o I2 retem; a leitura integral decide, e havendo comparacao com LLMs de proposito geral o registro '
 'entra ainda que os modelos propostos nao qualifiquem.'),

'818_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "A Novel AI-Driven Approach to UML Dataset Generation and Multimodal Verification '
 'in the Design Phase". O resumo parte da escassez de conjuntos de dados UML de alta qualidade e '
 'propoe pipeline de dois modelos: "LLaMA 3.2-1B-Instruct generates detailed technical specifications, '
 'while DeepSeek-R1-Distill-Qwen-32B" produz os diagramas. Palavras-chave autorais: geracao '
 'automatizada de UML, LLMs, verificacao multimodal e modelos de visao e linguagem. ',
 'DISCUSSAO: B2, B3 e B4 passam: dois LLMs nomeados, direcao especificacao -> diagrama, e a entrada do '
 'modelo gerador de UML e a especificacao tecnica textual. Cabe registrar que essa especificacao e ela '
 'propria sintetica, produzida pelo primeiro modelo, mas isso nao afeta o I4, que exige entrada '
 'textual de requisitos ou de dominio, sem exigir origem humana. O B1 passa por forca do titulo e das '
 'palavras-chave, ainda que o resumo nao nomeie o tipo de diagrama. O I6 esta satisfeito pela '
 'verificacao multimodal, que e mecanismo declarado de aferimento de qualidade e usa modelos de visao '
 'e linguagem sobre a representacao grafica. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Interessa a sintese tanto pela metrica quanto pelo conjunto '
 'de dados, insumo reaproveitavel por estudos posteriores.'),

'823_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: titulo "A comparison of different Large Language Models for the generation of UML class '
 'diagrams". O resumo declara que o artigo "builds on previous work COMPARING HUMAN-MADE AND '
 'LLM-GENERATED DIAGRAMS by evaluating the performance of four state-of-the-art LLMs, including both '
 'proprietary and open-source models". Palavras-chave autorais: LLMs, engenharia de requisitos, '
 'educacao em engenharia de software e modelagem UML. ',
 'DISCUSSAO: os quatro subportoes passam. O I6 esta satisfeito de modo forte e com o desenho de maior '
 'interesse para esta revisao: comparacao com gabarito humano, que e a forma mais direta de '
 'operacionalizar qualidade de modelo. A mencao a educacao em engenharia de software nas '
 'palavras-chave nao aproxima o registro do agrupamento de realimentacao automatizada (753, 765, 771, '
 '784, 807), que sai por E8: ali o diagrama e do estudante e o LLM apenas o avalia, ao passo que aqui '
 'e o LLM que GERA o diagrama e sao os autores que o avaliam. A distincao e o eixo do B3. ',
 'DECISAO: retido com EVIDENCIA=EXPLICITA. Candidato central; prioridade alta na fila de extracao.'),

'825_SCOPUS':('PASSOU','INCERTO_SAIDA;CANDIDATO_E10',
 'EVIDENCIA: poster sobre trabalho em curso para incorporar IA generativa a MBSE. O resumo afirma que '
 '"MBSE uses a form of XML called SysML to represent the MBSE model and a set of diagrams LIKE UML '
 'DIAGRAMS used in the software development arena", e que o trabalho explora "how GenAI can generate '
 'the MBSE content and support the end user in providing crucial feedback on the rules and processes '
 'involved with MBSE while generating MBSE content", com RAG. Encerra dizendo que "the application of '
 'GenAI with MBSE is still in the infant stages and this work seeks to explore the effectiveness of '
 'that integration". ',
 'DISCUSSAO: ha geracao de conteudo por IA generativa (B2 satisfeito) e a direcao e producao, nao '
 'avaliacao de modelo alheio (B3 satisfeito). O B1 e que nao se resolve: ao contrario de 812_SCOPUS, '
 'este resumo NAO nomeia nenhum tipo de diagrama, nao distingue SysML v1 de v2, e a formula "like UML '
 'diagrams" e comparacao, nao identificacao. Recai portanto no terceiro caso do B1, o INCERTO_SAIDA, '
 'exatamente como Mermaid e PlantUML sem tipo declarado. Soma-se que e poster de trabalho em curso, '
 'com a efetividade posta como objetivo a explorar, nao como resultado. ',
 'DECISAO: retido com INCERTO_SAIDA e CANDIDATO_E10. Pela regra de ouro 1 a incerteza retem, mas o '
 'registro tem prognostico fraco: se o texto completo confirmar poster sem estudo, sai por E10 na fase '
 'de leitura integral.'),

# ---------------- B1: a saida nao e conteudo UML ----------------
'799_SCOPUS':('B1_E7','',
 'EVIDENCIA: a unica ocorrencia de UML esta na primeira oracao do resumo, como exemplo de ferramenta '
 'da area: "IS engineering (ISE) uses tools such as UML and BPMN, but it lacks a theoretical '
 'foundation that is useful and teachable". O artigo relata trinta anos de esforco do autor para '
 'articular um fundamento teorico para a engenharia de sistemas de informacao, ancorado na teoria de '
 'sistemas de trabalho. A unica mencao a LLM e condicional e prospectiva: os projetos atuais '
 'concentram-se em consolidar passos anteriores "by using knowledge graphs, POSSIBLY in conjunction '
 'with carefully structured prompting of large language models". ',
 'DISCUSSAO: o B1 resolve o caso antes de qualquer outro subportao. Nao ha producao, transformacao, '
 'reparo nem revisao de conteudo UML: a UML e citada como pano de fundo disciplinar. O produto '
 'declarado sao teorias, arcaboucos, taxonomia de objetos de conhecimento e conjunto de gabaritos, '
 'nenhum deles conteudo UML. Pela regra de ouro 3, o criterio primario e o primeiro portao que explica '
 'o caso com clareza, e e o B1. Registre-se que o B2 tambem falharia, pois o uso de LLM e hipotetico, '
 'mas anotar E6 inverteria a ordem do fluxograma. ',
 'DECISAO: excluido por E7 no subportao B1. Falso positivo por mencao disciplinar de UML somada a '
 'mencao incidental de LLM em partes distintas do resumo.'),

# ---------------- B2: a origem do conteudo UML nao e LLM substantivo ----------------
'804_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo propoe metodologia que integra IA e logica difusa para engenharia de requisitos '
 'de seguranca cibernetica, "specifically focused on MODELING AND PRIORITIZING THE REQUIREMENTS OF THE '
 'CHATGPT SYSTEM". Foi desenvolvido arcabouco baseado em TOPSIS difuso, em que os interessados '
 'exprimem preferencias por variaveis linguisticas convertidas em numeros difusos triangulares. As '
 'palavras-chave autorais incluem "ChatGPT", "Class diagram" e "UCD". ',
 'DISCUSSAO: a armadilha e a coocorrencia de ChatGPT, diagrama de classes e diagrama de casos de uso '
 'nas palavras-chave, que a primeira vista sugere geracao de UML por LLM. A leitura desfaz a '
 'aparencia: o ChatGPT e o SISTEMA MODELADO, o objeto cujos requisitos os autores levantam e '
 'priorizam, e nao o agente modelador. Os diagramas sao construidos pelos autores, e o unico '
 'mecanismo automatico e o TOPSIS difuso, que ordena requisitos e nao tem autoridade semantica alguma '
 'sobre elementos UML. Falha portanto o I2 quanto a ORIGEM do conteudo. E o mesmo padrao de '
 '768_SCOPUS, em que o LLM e o objeto modelado, e nao o modelador. O B1 nao resolve o caso, pois ha '
 'conteudo UML genuino e proprio; quem resolve com clareza e o B2, na forma da regra de ouro 3. ',
 'DECISAO: excluido por E6 no subportao B2.'),

'814_SCOPUS':('B2_E6','',
 'EVIDENCIA: a proposta integra cadeia de blocos, tokens nao fungiveis e LLMs em ambiente de metaverso '
 'para gemeos digitais medicos. O papel do LLM e declarado sem ambiguidade: "an LLM-powered '
 'NON-PLAYER CHARACTER (NPC) enables intelligent real-time user interactions and personalized '
 'insights". A unica ocorrencia de UML esta na descricao do que os autores apresentam: "we present the '
 'system architecture, SEQUENCE DIAGRAMS, and algorithms, along with the implementation and testing '
 'details". A avaliacao mede custo, seguranca e tempo de resposta dos contratos inteligentes e do LLM. ',
 'DISCUSSAO: ha conteudo UML real e do proprio artigo — diagramas de sequencia —, de modo que o B1 nao '
 'e o subportao decisivo. Mas esses diagramas sao documentacao de projeto escrita pelos autores para '
 'descrever a arquitetura da solucao, e o LLM opera dentro do sistema construido, como personagem nao '
 'jogavel que conversa com o paciente. Nao ha autoridade semantica do LLM sobre elemento UML algum: '
 'ele nao produz, nao transforma, nao repara e nao revisa o diagrama. Falha o I2 quanto a origem. '
 'Padrao ja registrado em 790_SCOPUS e 960_SCOPUS, em que o LLM e componente do sistema projetado. ',
 'DECISAO: excluido por E6 no subportao B2.'),

'817_SCOPUS':('B2_E6','',
 'EVIDENCIA: o artigo valida em campo um caso de uso centrado no paciente para saude de precisao como '
 'servico. O metodo declarado e participativo e humano: "we establish and validate design rules using '
 'an emphatic, participatory approach called SOFT SYSTEMS MODELING (SSM), prioritising '
 'patient-centricity. Drawing on prior research, WE UTILISED Unified Modeling Language (UML) '
 'techniques to model and refine these rules". A IA generativa aparece na frase de abertura, entre '
 'dispositivos vestiveis e computacao quantica, como tendencia que motiva o reimaginar do futuro. ',
 'DISCUSSAO: ha UML abundante e autoral, o que afasta o B1. O sujeito dos verbos modelar e refinar, '
 'porem, e a primeira pessoa do plural: sao os autores e os participantes que modelam, por metodologia '
 'de sistemas flexiveis, e a validacao e de campo, com pessoas. A IA generativa nao e componente do '
 'metodo nem agente sobre os modelos; e contexto retorico. Falha o I2 quanto a origem. Padrao '
 'identico ao de 740_SCOPUS, em que a unica mencao a LLM tambem estava na frase de abertura. ',
 'DECISAO: excluido por E6 no subportao B2.'),

'821_SCOPUS':('B2_E6','',
 'EVIDENCIA: o resumo propoe "a mechanism for extracting Cartoon images via UML Models based on '
 'natural language-based specifications, MAPPING a cut image\'s cartoon elements with UML properties '
 'EXTRACTED THROUGH LINGUISTIC TEXTUAL ANALYSIS in software engineering". A IA generativa aparece '
 'apenas nas duas primeiras oracoes, como panorama: a pesquisa em IA generativa tem sido ativa, '
 'concentrando-se em gerar saidas de varios tipos a partir de entradas textuais, mas compreender o '
 'sentido dos prompts permanece desafio. Nenhum LLM e nomeado. ',
 'DISCUSSAO: ha conteudo UML produzido a partir de especificacao textual, o que satisfaz B1, B3 e B4 e '
 'impede resolver o caso nesses subportoes. O B2 e decisivo: o mecanismo que extrai as propriedades '
 'UML e declaradamente ANALISE LINGUISTICA TEXTUAL, tecnica simbolica de processamento de linguagem '
 'natural, nao modelo de linguagem de grande porte. Ainda que haja IA generativa no pipeline, o que o '
 'resumo permite inferir e que ela produziria a IMAGEM do desenho, e nao o modelo UML; a autoridade '
 'semantica sobre os elementos UML e do analisador linguistico. Pela RF-02, o que importa e quem '
 'determina o conteudo semantico do artefato UML. Falha o I2 quanto a origem. ',
 'DECISAO: excluido por E6 no subportao B2. Decisao passivel de revisao se o texto completo revelar '
 'LLM na etapa de extracao das propriedades UML, hipotese que o resumo nao sustenta.'),

# ---------------- B3: direcao invertida ----------------
'798_SCOPUS':('B3_E7','',
 'EVIDENCIA: o titulo declara "automatic test case generation FROM USE CASE DIAGRAM using LLMs and '
 'prompt engineering". O metodo e explicito quanto ao sentido da transformacao: "by getting '
 'information from the XML REPRESENTATION OF USE CASE DIAGRAMS, we can create detailed instructions '
 'that guide a generative AI model to make test cases for each use case scenario". ',
 'DISCUSSAO: B1 e B2 passam — ha conteudo UML e ha LLM substantivo —, de modo que o caso so se resolve '
 'no B3. A matriz da secao 4.3 do manual fixa a celula com precisao: UML existente -> LLM -> codigo, '
 'testes ou documentacao equivale a E7. O diagrama de casos de uso e INSUMO, ja existe e nao e '
 'alterado, e o produto sao casos de teste executaveis. Falha o I5, que exige conteudo UML na SAIDA. '
 'Note-se que o desfecho preserva a distincao que o codigo sozinho perderia: B3_E7 significa que havia '
 'UML, mas na entrada, ao contrario de B1_E7, em que nunca houve UML. ',
 'DECISAO: excluido por E7 no subportao B3.'),

'815_SCOPUS':('B3_E7','',
 'EVIDENCIA: titulo "ChatGPT\'s Aptitude in Utilizing UML Diagrams for Software Engineering Exercise '
 'Generation". O resumo declara: "we use ChatGPT to GENERATE EXERCISES based on the information from '
 'UPLOADED UML DIAGRAMS by analyzing textual UML representations such as Mermaid and graphical '
 'diagrams". Palavra-chave autoral de abertura: "AI-Generated Exercises". ',
 'DISCUSSAO: ha UML e ha LLM substantivo, logo B1 e B2 passam e o caso se decide no B3. Os diagramas '
 'de classes e de sequencia sao CARREGADOS pelos autores, ja existem, e o produto do ChatGPT sao '
 'enunciados de exercicio, isto e, texto didatico. Recai na celula UML existente -> LLM -> '
 'documentacao, que a matriz da secao 4.3 fixa como E7. Falha o I5. Cabe distinguir de E8: nao e caso '
 'de o LLM avaliar ou explicar o diagrama, mas de produzir artefato novo de outra natureza a partir '
 'dele, e por isso o desfecho e E7 e nao E8. Registre-se que a mencao a Mermaid confirma seu estatuto '
 'de sintaxe portadora, aqui na ENTRADA. ',
 'DECISAO: excluido por E7 no subportao B3.'),

'807_SCOPUS':('B3_E8','',
 'EVIDENCIA: titulo "Teaching UML using a RAG-based LLM". O resumo apresenta ferramenta em nuvem que '
 '"CAPTURES AND ANALYZES UML DIAGRAMS CREATED BY STUDENTS during their interactions with a UML" '
 'ambiente de modelagem, com o proposito declarado de que os professores "understand the students\' '
 'behavior along with their modeling activities to PROVIDE SUGGESTIONS AND FEEDBACK to avoid more '
 'frequent mistakes". ',
 'DISCUSSAO: B1 e B2 passam. No B3 a direcao e inequivoca: o diagrama e criado pelo ESTUDANTE, o LLM '
 'com RAG apenas captura, analisa e devolve realimentacao, e nada no conteudo UML e alterado pelo '
 'modelo. A tabela da secao 4.2 do manual resolve exatamente esta situacao: "LLM apenas avalia ou '
 'explica um diagrama ja existente -> E8", porque nao ha producao, transformacao, reparo ou revisao de '
 'conteudo UML. A condicao restritiva do E8 esta satisfeita, ja que o resumo deixa claro que o '
 'diagrama preexiste e nao e alterado — foi a verificacao dessa condicao que, em 215_ACM, levou ao '
 'desfecho diverso, pois la havia correcao. Falha o I3. ',
 'DECISAO: excluido por E8 no subportao B3. Quinto membro do agrupamento tematico de realimentacao '
 'automatizada para ensino de modelagem UML, ao lado de 753, 765, 771 e 784, todos Scopus.'),

# ---------------- B4: a entrada nao e especificacao textual ----------------
'819_SCOPUS':('B4_E9','',
 'EVIDENCIA: OOWM estrutura raciocinio corporificado para planejamento robotico. O resumo declara que '
 'o arcabouco "leverages the Unified Modeling Language (UML) to materialize this definition: it '
 'employs CLASS DIAGRAMS TO GROUND VISUAL PERCEPTION into rigorous object hierarchies, and ACTIVITY '
 'DIAGRAMS to operationalize planning into executable control flows". Ha treinamento em tres estagios '
 'com ajuste supervisionado e GRPO, e avaliacao no marco MRoom-30k quanto a coerencia de planejamento, '
 'sucesso de execucao e FIDELIDADE ESTRUTURAL. ',
 'DISCUSSAO: os tres primeiros subportoes passam com folga — dois tipos de diagrama UML nomeados, LLM '
 'como agente gerador, direcao de producao, e ha ate metrica de fidelidade estrutural sobre a '
 'estrutura gerada. O caso se decide no B4. A fonte que o diagrama de classes formaliza e '
 'declaradamente a PERCEPCAO VISUAL do ambiente, isto e, imagem, e nao especificacao textual de '
 'requisitos, historia de usuario, cenario ou descricao de dominio. A condicao restritiva do E9 exige '
 'que o resumo declare explicitamente entrada de codigo, imagem, modelo existente ou registros, sem '
 'componente textual de requisitos, e a declaracao aqui e expressa. Falha o I4. E precisamente a '
 'hipotese contemplada na delimitacao de escopo fixada em 2026-08-16, que exclui a formalizacao a '
 'partir de imagem ainda quando ha metrica explicita de qualidade sobre a UML gerada. ',
 'DECISAO: excluido por E9 no subportao B4. Exclusao onerosa e consciente: o registro mede fidelidade '
 'estrutural de diagramas de classes e de atividade gerados por LLM, e seria forte candidato caso o I4 '
 'venha a ser emendado. Fica nomeado para eventual recuperacao sem re-triagem.'),

'820_SCOPUS':('B4_E9','',
 'EVIDENCIA: relato de experiencia sobre migracao e reengenharia de variantes existentes para linha de '
 'produtos de software com assistentes baseados em LLM. O resumo declara: "we revisit four '
 'illustrative cases of the literature where the challenge is to MIGRATE VARIANTS WRITTEN IN DIFFERENT '
 'FORMALISM (UML CLASS DIAGRAMS, Java, GraphML, STATECHARTS)", relatando a experiencia com o ChatGPT-4 '
 'e comparando-a com a abordagem BUT4Reuse. ',
 'DISCUSSAO: B2 passa, com LLM nomeado e substantivo. O B1 e o B3 nao resolvem o caso com clareza, '
 'porque o resumo nao diz de que natureza sao os artefatos reusaveis sintetizados: se a linha de '
 'produtos extraida das variantes UML for ela propria expressa em UML, havera conteudo UML na saida e '
 'a direcao sera modelo -> modelo, que o protocolo admite como transformacao. Justamente por isso a '
 'regra de ouro 3 manda descer ate o subportao que explica o caso sem residuo, e esse e o B4: seja '
 'qual for a saida, a ENTRADA e declaradamente um conjunto de modelos e programas ja existentes — '
 'diagramas de classes UML, Java, GraphML e diagramas de estados —, sem qualquer componente textual de '
 'requisitos. A condicao restritiva do E9 ("modelo existente") esta expressamente satisfeita e a '
 'delimitacao de escopo exige sintese a partir de especificacao textual em linguagem natural. Falha o '
 'I4. ',
 'DECISAO: excluido por E9 no subportao B4. Desfecho estavel: ainda que o texto completo revele UML na '
 'saida, o I4 continuaria insatisfeito.'),
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
     'Terceiro lote de leitura individual dos registros que mencionam UML no titulo ou no resumo: 24 '
     'registros triados, indices 48 a 71 da lista. Desfechos: 14 RETIDOS, 1 E7 em B1, 4 E6 em B2, 2 E7 '
     'em B3, 1 E8 em B3 e 2 E9 em B4. Lote de rendimento muito superior aos anteriores, por concentrar '
     'a faixa 796-825 do Scopus, tematicamente proxima do objeto da revisao. Candidatos centrais: '
     '803_SCOPUS (geracao de diagramas de sequencia com avaliacao de tres LLMs em multiplos dominios), '
     '809_SCOPUS (que alem de avaliar PROPOE metrica ponderada automatica sobre PlantUML gerado, sobre '
     'conjunto estratificado por dificuldade), 811_SCOPUS (correcao estrutural e semantica de '
     'diagramas de atividade por LLMs ajustados por instrucao) e 823_SCOPUS (comparacao de quatro LLMs '
     'contra gabarito humano). Quatro achados metodologicos. (1) Consolida-se um PADRAO ESTRUTURAL '
     'novo, o do pipeline texto -> UML -> codigo (796, 806, 810), em que o entregavel final e codigo '
     'mas a UML e produzida pelo proprio LLM a partir de texto: NAO e E7 em B3, porque o E7 de B3 '
     'pressupoe UML na ENTRADA; a celula correta da matriz da secao 4.3 e requisitos -> LLM -> UML, e '
     'os tres ficam retidos. (2) A questao SysML foi decidida em 812_SCOPUS pela via da v1: o resumo '
     'nomeia diagrama de maquina de estados, tipo reusado do metamodelo UML, e usa "block definition '
     'diagram", vocabulario da v1 substituido por "part definition" na v2; ja 825_SCOPUS, que nao '
     'nomeia tipo algum, fica em INCERTO_SAIDA. (3) 819_SCOPUS e a exclusao mais onerosa do lote e fica '
     'nomeada para eventual recuperacao: gera diagramas de classes e de atividade por LLM e mede '
     'fidelidade estrutural, mas a fonte que o diagrama formaliza e a PERCEPCAO VISUAL do ambiente, '
     'entrada de imagem, hipotese que a delimitacao de escopo de 2026-08-16 exclui por E9. (4) Duas '
     'armadilhas lexicais confirmadas: 804_SCOPUS reune ChatGPT, diagrama de classes e diagrama de '
     'casos de uso nas palavras-chave, mas o ChatGPT e o SISTEMA MODELADO e nao o modelador, mesmo '
     'padrao de 768_SCOPUS; e 813_SCOPUS abre uma questao de fronteira do I2, pois seus transformadores '
     'Seq2Seq e Seq2AST sao expressamente CONTRAPOSTOS aos "general-purpose large language models" '
     'usados como linha de base — retido com INCERTO_PAPEL_LLM pela regra de ouro 1. Registre-se ainda '
     'que 807_SCOPUS e o quinto membro do agrupamento de realimentacao automatizada para ensino de '
     'modelagem UML (753, 765, 771, 784), todos com desfecho uniforme B3_E8.',
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
