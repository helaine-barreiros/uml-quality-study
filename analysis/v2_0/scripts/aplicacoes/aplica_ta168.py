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
'934_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: apresenta o StructGen, framework de geracao de codigo em nivel de funcao que usa diagramas de '
 'atividade UML como guia estrutural. Dois papeis colaborativos baseados em LLM: um Designer que infere os '
 'requisitos e modela os esquemas de projeto com diagramas de atividade UML, e um Coder que gera codigo '
 'guiado por esses esquemas, com o Designer revisando o projeto e o Coder reparando o codigo por retorno de '
 'teste. Resultados: StructGen supera todas as baselines com melhora relativa de 9,4% a 37,3%; os esquemas '
 'baseados em diagrama de atividade melhoram LLMs e baselines em 2,1% a 112,1%. ',
 'DISCUSSAO: este e o padrao estrutural "texto -> UML -> codigo" ja fixado nos registros 796, 806, 810, 828 '
 'e 870. Nao e B3_E7, porque o E7 de B3 pressupoe UML na entrada; aqui o diagrama de atividade e produzido '
 'pelo proprio LLM a partir dos requisitos, o que corresponde a celula "requisitos -> LLM -> UML" da secao '
 '4.3 do manual. B1 saida inclui conteudo UML nomeado, B2 origem e LLM, B4 entrada e requisito textual. '
 'Ressalva de E10: a qualidade medida e a do codigo (taxa de acerto contra baselines), nunca a do diagrama. '
 'A ablacao que isola a contribuicao dos esquemas de projeto mede o efeito do diagrama sobre o codigo, nao '
 'atributos do diagrama. Pela regra de ouro 2 a ausencia de medida de qualidade da UML nao exclui aqui, e '
 'E11 e proibido em titulo e resumo. ',
 'DECISAO: retido no Portao B; flags CANDIDATO_E10 e EVIDENCIA=A_VERIFICAR. No texto completo verificar se '
 'ha alguma medida sobre os diagramas em si; caso contrario e candidato forte a E10 ou E11.'),

'935_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: apresenta o SuPReA, ferramenta web de codigo aberto que gera um pacote coerente de artefatos de '
 'especificacao a partir de uma breve descricao de projeto em linguagem natural. Orquestra agentes de IA '
 'sem estado, cada um responsavel por um tipo de artefato: visao de produto, requisitos funcionais, '
 'personas, casos de uso, diagramas UML, modelos de dados, esbocos de interface, cenarios e roadmaps, com '
 'template de prompt configuravel e saida JSON estruturada. Valida saidas e reconsulta o modelo quando a '
 'resposta e incompleta ou malformada. Declara: "we report an initial verification focused on output '
 'completeness and format reliability" e "The paper focuses on the tool design and workflow rather than on '
 'a full empirical evaluation". ',
 'DISCUSSAO: B1 saida inclui diagramas UML entre os artefatos. B2 origem sao agentes de LLM. B3 direcao e '
 'descricao textual do projeto para artefatos. B4 entrada e descricao em linguagem natural, dentro do '
 'escopo. Nenhum portao exclui. Duas ressalvas fortes: o diagrama UML e um item entre oito ou mais tipos de '
 'artefato gerados no mesmo fluxo, e o resumo nao indica que resultados sejam reportados por tipo, hipotese '
 'literal de E10; e a propria autoria declara ausencia de avaliacao empirica completa, com verificacao '
 'limitada a completude de saida e confiabilidade de formato, o que aponta para E11 na fase de texto '
 'completo. Nenhum dos dois criterios e decidivel em titulo e resumo. ',
 'DECISAO: retido no Portao B; flags CANDIDATO_E10 e EVIDENCIA=A_VERIFICAR.'),

'937_SCOPUS':('B4_E9','',
 'EVIDENCIA: o titulo declara "abstracting UML and OCL representations from Java and Python programs". O '
 'resumo situa o trabalho em manutencao e evolucao de sistemas legados, com engenharia reversa para gerar '
 'representacoes e modelos de software abstraindo diversos tipos de diagrama a partir de bases de codigo, '
 'apoiada por MDE. KW: Java programs, Legacy systems, Object constraint language (OCL), Python programs, '
 'Reverse engineering, Unified modeling language (UML). ',
 'DISCUSSAO: B1 nao exclui, o produto e conteudo UML e OCL. B2 nao exclui, os LLMs fazem a abstracao. B3 nao '
 'exclui, a direcao termina em UML. B4 explica sem residuo: a entrada e programa Java ou Python, sem '
 'qualquer componente de especificacao textual de requisitos. E o caso de engenharia reversa que a '
 'delimitacao de escopo de 2026-08-16 coloca fora por I4. Note-se que a questao pendente sobre OCL nao '
 'altera este desfecho, pois a exclusao se da pela entrada, nao pela saida. ',
 'DECISAO: excluido em B4 por E9. Exclusao onerosa, nomeada para recuperacao sem re-triagem caso I4 seja '
 'emendado, junto de 865, 921 e 930.'),

'939_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: estudo de caso que investiga a capacidade de ChatGPT, Claude, Gemini e Microsoft Copilot de '
 'gerar projetos a partir de requisitos em linguagem natural, com os projetos representados como diagramas '
 'de classes UML, avaliados em termos de corretude e complexidade (texto truncado no CSV apos "correctness '
 'and c"). KW: design complexity, design generation, evaluation, LLM, tacit knowledge, UML class diagrams. ',
 'DISCUSSAO: B1 saida e diagrama de classes UML, declarado como a forma de representacao do projeto. B2 '
 'origem sao quatro LLMs comerciais. B3 direcao e requisitos em linguagem natural para UML. B4 entrada e '
 'requisito textual. Nenhum portao exclui. Corretude e complexidade de projeto sao atributos de qualidade '
 'de I6, e a comparacao entre quatro modelos permite extracao por modelo. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Conferir no texto completo a definicao operacional '
 'de complexidade de projeto e o instrumento de corretude, pois o resumo esta truncado no CSV.'),

'940_SCOPUS':('B3_E8','',
 'EVIDENCIA: artigo de dados que descreve um corpus diagramatico em XML de modelos UML produzidos por '
 'estudantes e o retorno formativo correspondente gerado por IA, em disciplina de Engenharia de Software na '
 'Universidade Constantine the Philosopher em Nitra. Combina 112 registros anonimizados de estudantes, 448 '
 'registros de retorno formativo em eslovaco e 700 relatorios XML brutos produzidos no Enterprise Architect '
 'v16. KW: AI feedback generation, Automated assessment, Prompt-based evaluation. ',
 'DISCUSSAO: B1 nao exclui, ha modelos UML. B2 nao exclui, o LLM gera o retorno. B3 explica sem residuo: os '
 'modelos UML sao produzidos pelos estudantes e o LLM apenas avalia e comenta, celula "UML existente -> LLM '
 '-> avaliacao/explicacao/critica" da secao 4.3 do manual. Verificada a condicao restritiva do E8 na linha '
 '107 do manual: o retorno e formativo e nao ha declaracao de que o modelo seja alterado pelo LLM, apenas de '
 'que o retorno e produzido e registrado. Decimo primeiro registro do agrupamento de avaliacao automatizada '
 'por LLM (753, 765, 771, 784, 807, 830, 838, 861, 891, 896). ',
 'DECISAO: excluido em B3 por E8. Nao satisfaz I3. Trabalho nomeado como adjacente de interesse: o corpus '
 'anotado pode ser util na discussao metodologica sobre LLM como avaliador.'),

'941_SCOPUS':('B3_E8','',
 'EVIDENCIA: investiga a viabilidade de usar LLMs para automatizar a correcao de diagramas de classes UML em '
 'disciplina de projeto de software. O metodo desenha estudos de caso com restricoes que guiam as escolhas '
 'de projeto dos alunos, converte os diagramas visuais em descricoes textuais e usa LLMs para avaliar as '
 'submissoes. Avaliacao com 92 submissoes de estudantes, comparando notas de tres monitores com as de tres '
 'LLMs (Llama, GPT o1-mini e Claude). ',
 'DISCUSSAO: B3 explica sem residuo: os diagramas sao produzidos pelos alunos e o LLM atribui nota, sem '
 'alterar o modelo, condicao restritiva do E8 satisfeita. Decimo segundo registro do agrupamento de '
 'avaliacao automatizada. O eixo discriminante continua sendo quem produz e quem avalia; aqui o LLM esta '
 'integralmente do lado do avaliador. Ha ainda entrada por conversao de diagrama visual em descricao '
 'textual, que reforca que a UML precede o LLM. ',
 'DECISAO: excluido em B3 por E8. Nao satisfaz I3. Trabalho nomeado como adjacente de interesse para a '
 'discussao sobre concordancia entre LLM e avaliador humano, ao lado de 839 e 838.'),

'942_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: apresenta abordagem automatizada para gerar modelos comportamentais, especificamente diagramas '
 'de sequencia, a partir de requisitos em linguagem natural expressos como user stories, e investiga a '
 'eficacia de um LLM em comparacao com uma abordagem baseada em regras, como anuncia o titulo ("Unleashing '
 'the Power of Generative AI vs. a Rule-Based Approach"). ',
 'DISCUSSAO: B1 saida e diagrama de sequencia UML. B2 origem e LLM generativo, e a abordagem baseada em '
 'regras figura como comparador, nao como produtora do artefato retido. B3 direcao e user story para UML. '
 'B4 entrada e user story, item nomeado literalmente na delimitacao de escopo fixada pela pesquisadora. '
 'Nenhum portao exclui. O desenho comparativo LLM contra baseline simbolica e exatamente o tipo de evidencia '
 'que I6 requer, e permite extrair o ganho atribuivel ao LLM. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA.'),

'943_SCOPUS':('B1_E7','',
 'EVIDENCIA: propoe pedagogia centrada em verificacao para programacao orientada a objetos introdutoria, com '
 'o ChatGPT posicionado como andaime controlado e nao como fonte de respostas. O desenho exige rotina de '
 'explicar antes de gerar, fluxo UML-testes-codigo, pontos de checagem de letramento em prompt e artefatos '
 'auditaveis de verificacao. Os desfechos medidos sao ganhos no inventario de conceitos de POO, coesao e '
 'especificacao explicita de invariantes por rubrica de qualidade de projeto, cobertura de testes, escore '
 'de mutacao, densidade de defeitos e telemetria de processo. ',
 'DISCUSSAO: B1 explica sem residuo. A UML aparece apenas como etapa nomeada de um fluxo didatico '
 '(UML-tests-code), sem tipo de diagrama declarado e sem que qualquer atributo do diagrama seja medido. O '
 'produto avaliado e o resultado de aprendizagem do estudante e a qualidade do codigo e dos testes. Nao ha '
 'sintese de conteudo UML por LLM sob avaliacao, e o ChatGPT e explicitamente restringido a andaime. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'944_SCOPUS':('B1_E7','',
 'EVIDENCIA: relata o desenvolvimento de um prototipo de chatbot tutorial com Azure AI e GPT-4, que responde '
 'e formula perguntas no estilo do professor da disciplina, variando conteudo e formulacao conforme a '
 'circunstancia. O topico do tutorial sao casos de uso em UML: o sistema faz perguntas sobre conceitos '
 'centrais e os explica, usando as regras praticas e simplificacoes que o proprio professor usaria, a partir '
 'da ingestao de instrucoes em linguagem natural e documentos centrais. ',
 'DISCUSSAO: B1 explica sem residuo. O produto do LLM e dialogo tutorial em linguagem natural sobre UML, nao '
 'conteudo UML. A UML e o assunto ensinado, nao o artefato sintetizado, o que e uma variante da armadilha ja '
 'documentada em que a UML aparece como tema e nao como produto. Nao ha diagrama gerado nem medida de '
 'qualidade de diagrama. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'945_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: framework de construcao e validacao automatizada de um dataset para geracao de codigo UML. '
 'Arquitetura de dois modelos: LLaMA 3.2 1B-Instruct gera descricoes de funcionalidades na perspectiva do '
 'usuario final e DeepSeek-R1-Distill-Qwen-32B produz os diagramas de casos de uso UML correspondentes, com '
 'tracos de raciocinio. Dataset de 3.000 amostras, cada uma com descricao de funcionalidade pareada a um '
 'diagrama UML. Sistema de verificacao visual multimodelo com tres modelos de visao e linguagem avaliando o '
 'alinhamento entre entrada textual e diagrama gerado, com escore de 1 a 6 e agregacao ponderada por '
 'desempenho no benchmark MMMU. ',
 'DISCUSSAO: B1 saida e diagrama de casos de uso UML nomeado; PlantUML e sintaxe portadora. B2 origem sao '
 'LLMs generativos. B3 direcao e descricao textual de funcionalidade para UML. B4 entrada e descricao '
 'textual; observe-se que ela e por sua vez gerada por LLM, o que nao a retira do escopo, pois continua '
 'sendo especificacao textual em linguagem natural, mas afeta a validade externa e deve constar da '
 'extracao. O escore de alinhamento por modelos de visao e linguagem e instrumento explicito de qualidade. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. ALERTA DE REDUNDANCIA: pertence a familia de '
 'publicacoes que compartilham pipeline de dois LLMs e validacao multimodal por modelos de visao, junto de '
 '963_SCOPUS (que declara "extends our framework" e sintetiza diagramas de sequencia com os mesmos dois '
 'modelos), 818, 848, 868, 869 e 877. A eleicao do relato mais completo deve ser feita na fase de texto '
 'completo.'),

'947_SCOPUS':('B1_E7','',
 'EVIDENCIA: propoe framework assistido por IA que usa LLMs para interpretar cenarios de banco de dados em '
 'linguagem natural, gerar diagramas Entidade-Relacionamento e esquemas relacionais de referencia em '
 'formato PlantUML, e comparar submissoes de estudantes com as solucoes geradas pelo sistema para avaliar '
 'corretude, com mecanismo de escore de similaridade semantica e estrutural de entidades, relacionamentos, '
 'chaves e mapeamentos de tabela. ',
 'DISCUSSAO: B1 explica sem residuo. Diagrama Entidade-Relacionamento e esquema relacional nao pertencem ao '
 'metamodelo UML nem sao perfis dele; o PlantUML aqui e apenas sintaxe portadora, e a regra do manual e '
 'clara em que sintaxe portadora nao constitui notacao. Trata-se do mesmo padrao de notacao adjacente ja '
 'registrado em 759, 781, 895 e 905. Ha ainda um segundo motivo, que nao chego a acionar por ordem dos '
 'portoes: a avaliacao incide sobre submissoes de estudantes, o que levaria a E8 em B3. Como B1 ja explica '
 'sem residuo, o desfecho e B1_E7 e permanece estavel sob qualquer leitura. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'948_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: compara uma abordagem tradicional de NLP baseada em regras com LLMs ajustados por fine-tuning '
 'na geracao automatica de diagramas UML a partir de requisitos em linguagem natural, em contexto '
 'educacional. O resumo problematiza que "their capability to produce accurate and structured '
 'diagrams-particularly in instructional settings-has not been thoroughly examined" (texto truncado no CSV '
 'apos "This work compares a traditional"). KW inclui diagram usability e prompt engineering. ',
 'DISCUSSAO: B1 saida e diagrama UML. B2 origem sao LLMs ajustados, e a abordagem baseada em regras e o '
 'comparador. B3 direcao e requisitos para UML. B4 entrada e requisito em linguagem natural. Nenhum portao '
 'exclui. A acuracia e a estruturacao dos diagramas sao declaradas como objeto do exame, e a usabilidade '
 'do diagrama consta em KW, o que sinaliza avaliacao pragmatica alem da sintatica. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Conferir os instrumentos no texto completo, pois o '
 'resumo esta truncado no CSV.'),

'949_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: apresenta o QuaRUM, primeiro framework a automatizar de ponta a ponta a metodologia de Analise '
 'Qualitativa de Dados (codificacao aberta, axial e seletiva) para geracao de modelo de dominio UML, '
 'combinando LLMs com geracao aumentada por recuperacao. Processa requisitos por ingestao de documentos, '
 'indexacao semantica e codificacao com recuperacao, ancorando cada elemento do modelo no texto-fonte para '
 'mitigar alucinacao. Resultados: F1 entre 0,85 e 0,98 em tres dominios; kappa de Cohen ate 0,92, superando '
 'a concordancia entre codificadores humanos; recupera 37 atributos validos e 23 relacionamentos que '
 'analistas humanos deixaram passar; analise de custo-beneficio com ROI de 218% no uso inicial e 1.131% em '
 'usos repetidos. ',
 'DISCUSSAO: B1 saida e modelo de dominio UML. B2 origem e LLM com RAG, com autoridade semantica sobre os '
 'elementos codificados. B3 direcao e documento de requisitos para UML. B4 entrada e documento textual de '
 'requisitos, caso canonico do escopo. Nenhum portao exclui. A evidencia de qualidade e das mais completas '
 'do corpus ate aqui: metrica por elemento, concordancia contra baseline humana e analise de erro por '
 'omissao humana. A ancoragem no texto-fonte como mitigacao de alucinacao e ela propria um mecanismo de '
 'qualidade a extrair. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Integra o nucleo de modelagem de dominio ja em '
 'formacao (027, 061, 138, 141, 221, 623) e e prioridade alta na leitura de texto completo.'),

'950_SCOPUS':('B3_E8','',
 'EVIDENCIA: o resumo explora a aplicacao de LLMs multimodais em engenharia baseada em modelos "to evaluate '
 'their capacity for understanding and identifying relationships, features, and functionalities embedded in '
 'UML and EMF diagrams", com sumarizacao multimodal avaliada em desenvolvimento de software automotivo. Os '
 'diagramas UML e EMF sao descritos como contendo grande quantidade de informacao multimodal e dados '
 'relacionais. ',
 'DISCUSSAO: B1 nao exclui, ha UML no caso. B2 nao exclui, o LLM multimodal e substantivo. B3 explica sem '
 'residuo: os diagramas preexistem e o LLM os le, compreende e sumariza, o que e a celula "UML existente -> '
 'LLM -> avaliacao/explicacao/critica" da secao 4.3 e corresponde a linha 282 do manual ("LLM apenas avalia '
 'ou explica um diagrama ja existente"). Condicao restritiva do E8 verificada: nao ha declaracao de que o '
 'diagrama seja alterado. O que se mede e a capacidade de compreensao do modelo de linguagem, nao a '
 'qualidade de UML gerada. Se o caso sobrevivesse a B3, sairia em B4, pois a entrada e o proprio diagrama. ',
 'DECISAO: excluido em B3 por E8. Nao satisfaz I3.'),

'951_SCOPUS':('PASSOU','INCERTO_PAPEL_LLM;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: propoe framework de geracao inteligente de UML baseado em aprendizado profundo, para gerar '
 'diretamente codigo PlantUML padronizado a partir de requisitos em linguagem natural, com parsing semantico '
 'profundo, mecanismos colaborativos multi-visao e pipelines de validacao sintatica dinamica. Situa a '
 'motivacao nos avancos de Generative Artificial Intelligence (AIGC). Resultado reportado: "the framework '
 'can compress the modeling cycle from hours to minutes, significantly improving modeling efficiency". ',
 'DISCUSSAO: B1 saida e modelo UML em PlantUML, com o resumo falando em geracao ponta a ponta de requisitos '
 'para modelos UML; nenhum tipo de diagrama e nomeado, mas "multi-view" e "UML models" sustentam que o '
 'produto e conteudo UML. B3 e B4 nao excluem, a entrada e requisito em linguagem natural. B2 e o ponto '
 'aberto: o resumo diz "deep learning-based" e cita AIGC como contexto, sem nomear modelo, familia ou uso '
 'gerativo, de modo que nao e possivel distinguir em titulo e resumo se ha LLM na acepcao de I2 ou um modelo '
 'profundo ad hoc de parsing. A RF-01 manda reter quando titulo e resumo nao permitem distinguir. Segunda '
 'ressalva: o unico desfecho reportado e tempo de ciclo de modelagem, metrica de eficiencia e nao de '
 'qualidade do artefato. ',
 'DECISAO: retido no Portao B pela regra de ouro 1; flags INCERTO_PAPEL_LLM e EVIDENCIA=A_VERIFICAR. No '
 'texto completo verificar qual e o modelo e se ha qualquer medida sobre o diagrama; e candidato tanto a E6 '
 'quanto a E11.'),

'952_SCOPUS':('PASSOU','CANDIDATO_E10;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: propoe o Xd-CodeGen para gerar codigo Java de larga escala em quatro fases. Na analise de '
 'requisitos o ChatGPT 3.5 decompoe e reformula os requisitos do usuario, com grafo de conhecimento '
 'descrevendo entidades e relacoes e formulas de Propositional Projection Temporal Logic definindo '
 'propriedades. Na fase de modelagem, "we use knowledge graphs to enhance prompts and generate UML class '
 'and activity diagrams for each sub-requirement using ChatGPT 3.5". Na geracao de codigo, o Java e '
 'produzido a partir dos modelos UML estabelecidos, e na verificacao emprega-se verificacao em tempo de '
 'execucao. Aplicado a um projeto web Java pratico. ',
 'DISCUSSAO: padrao "texto -> UML -> codigo" ja fixado (796, 806, 810, 828, 870, 934): nao e B3_E7, porque '
 'os diagramas de classes e de atividade sao produzidos pelo proprio ChatGPT a partir dos sub-requisitos. '
 'B2: pela RF-02 o grafo de conhecimento e as formulas PPTL sao enriquecimento de prompt e definicao de '
 'propriedade, e a autoridade semantica sobre os elementos do diagrama permanece com o LLM. B4 entrada e '
 'requisito de usuario em linguagem natural. Ressalva de E10: o desfecho reportado e o codigo Java '
 'verificado, e nada indica medida sobre os diagramas intermediarios. ',
 'DECISAO: retido no Portao B; flags CANDIDATO_E10 e EVIDENCIA=A_VERIFICAR.'),

'954_SCOPUS':('B1_E7','',
 'EVIDENCIA: o trabalho integra LLMs a sistemas de recuperacao de informacao em ciberseguranca, no sistema '
 'Cyber Aggregator de monitoramento de midias sociais, automatizando indexacao semantica, reformulacao de '
 'consultas, sumarizacao, digestos analiticos, identificacao de eventos-chave e mapas semanticos. A unica '
 'mencao a UML e: "The paper also presents a UML diagram illustrating the key components of the system, '
 'along with a mathematical formalization of the main processes". ',
 'DISCUSSAO: B1 explica sem residuo. A UML aqui e ilustracao da arquitetura do proprio sistema descrito no '
 'artigo, desenhada pelos autores como recurso expositivo, e nao produto gerado nem objeto de avaliacao. '
 'Mesmo padrao de falso positivo ja registrado em 843_SCOPUS. Acuracia, completude e relevancia sao medidas, '
 'mas sobre resultados de busca, nao sobre UML, e a regra de ouro 2 nao opera no sentido inverso. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'955_SCOPUS':('B1_E7','',
 'EVIDENCIA: propoe o TEXTFLOW para compreensao de fluxogramas, em duas etapas: um VISION TEXTUALIZER que '
 'gera representacao textual a partir da imagem do fluxograma e um estagio de raciocinio sobre esse texto, '
 'em alternativa a modelos de visao e linguagem ponta a ponta. Motivacao declarada: controlabilidade '
 'limitada e falta de explicabilidade dos VLMs. ',
 'DISCUSSAO: B1 explica sem residuo por duas razoes independentes. Primeira, fluxograma generico nao e '
 'notacao UML: nao ha mencao a diagrama de atividade nem a qualquer tipo do metamodelo, e o proprio termo '
 'usado e flowchart. Segunda, o produto nao e diagrama, e representacao textual intermediaria e resposta a '
 'tarefas de compreensao. Caso o registro sobrevivesse a B1, sairia em B4, pois a entrada e imagem, hipotese '
 'expressamente excluida pela delimitacao de escopo de 2026-08-16. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'956_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: avalia o desempenho de LLMs na geracao de plantas de arquitetura de software, especificamente '
 'diagramas de componentes UML, a partir de especificacoes informais em linguagem natural. Declara: "We '
 'develop a formal characterization of component diagrams to derive quantitative metrics for analyzing '
 'LLM-generated diagrams, comparing them against expert-drawn ground truths associated with the '
 'specifications". Conclusao: as abordagens com LLM ainda carecem da acuracia necessaria para uso real. ',
 'DISCUSSAO: B1 saida e diagrama de componentes UML nomeado. B2 origem sao LLMs. B3 direcao e especificacao '
 'informal para UML. B4 entrada e especificacao textual em linguagem natural, exatamente o objeto delimitado '
 'pela pesquisadora, inclusive no ponto de a especificacao ser informal. Nenhum portao exclui. A evidencia e '
 'do tipo mais forte para esta revisao: metrica quantitativa derivada de caracterizacao formal do tipo de '
 'diagrama, com gabarito desenhado por especialista. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Prioridade alta na leitura de texto completo, pela '
 'construcao explicita do instrumento de medida.'),

'958_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: investigacao empirica sobre a eficacia do GPT-4-turbo na geracao de quatro tipos fundamentais '
 'de diagrama UML: classes, implantacao, casos de uso e sequencia. Os autores desenvolveram framework de '
 'engenharia de prompt baseado em regras que transforma cenarios de dominio em prompts otimizados (texto '
 'truncado no CSV apos "transforms domain scenarios into opt"). O titulo indica ainda levantamento de '
 'avaliacao centrado no estudante. KW: empirical evaluation, prompt engineering, software engineering '
 'education. ',
 'DISCUSSAO: B1 saida sao quatro tipos do metamodelo UML, todos nomeados. B2 origem e GPT-4-turbo; o '
 'framework de prompt baseado em regras opera sobre a entrada e nao retira do LLM a autoridade semantica, '
 'conforme RF-02. B3 direcao e cenario de dominio para UML. B4 entrada e descricao textual de dominio, item '
 'nomeado na delimitacao de escopo. Nenhum portao exclui. Como os quatro tipos sao todos UML, nao ha '
 'hipotese de E10, que trata de mistura com artefatos de outra natureza; a extracao devera ser feita por '
 'tipo de diagrama. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Verificar no texto completo se o instrumento e '
 'apenas percepcao dos estudantes ou tambem medida direta sobre os diagramas.'),

'959_SCOPUS':('B2_E6','',
 'EVIDENCIA: apresenta abordagem assistida por IA para transformar o modelo de dois hemisferios de iniciacao '
 'de projeto de TI em backlog de produto estruturado. A solucao gera documentacao de escopo e listas de '
 'tarefas a partir de user stories extraidas do modelo de processo do dominio do problema e "create the '
 'problem domain UML use case diagram from the two-hemisphere model". A pesquisa define regras de '
 'transformacao para converter elementos de processo em itens de backlog. Sobre o LLM, declara: "Large '
 'Language Model is integrated into the solution to automate task generation, prioritization, and '
 'decomposition". ',
 'DISCUSSAO: B1 nao exclui, ha diagrama de casos de uso UML como produto. B2 explica sem residuo: o papel do '
 'LLM e declarado e circunscrito a geracao, priorizacao e decomposicao de tarefas do backlog, ao passo que o '
 'diagrama de casos de uso resulta de regras de transformacao definidas pelos autores sobre o modelo de dois '
 'hemisferios. Pela RF-02, quem detem autoridade semantica sobre os elementos do diagrama sao as regras, nao '
 'o modelo de linguagem. Ha um segundo motivo, nao acionado por ordem dos portoes: a entrada e um modelo de '
 'processo preexistente e nao especificacao textual, o que levaria a E9 em B4. O desfecho de exclusao e '
 'portanto estavel sob as duas leituras. ',
 'DECISAO: excluido em B2 por E6. Nao satisfaz I2 na funcao exigida.'),

'961_SCOPUS':('B3_E8','',
 'EVIDENCIA: introduz funcionalidade de apoio a aprendizagem de construcao de diagramas de classes UML, '
 'construida sobre LLM com geracao aumentada por recuperacao, que fornece retorno enriquecido a partir de '
 'conhecimento acumulado. E implementada na ferramenta UML Miner, plugin do Visual Paradigm que captura e '
 'analisa diagramas UML gerados por estudantes aplicando mineracao de processos. Objetivo declarado: '
 'retorno personalizado e apoio continuo durante a modelagem, para melhorar resultados de aprendizagem e '
 'engajamento. ',
 'DISCUSSAO: B3 explica sem residuo: os diagramas sao produzidos pelos estudantes, capturados pelo plugin, e '
 'o LLM apenas gera retorno. Condicao restritiva do E8 verificada: o retorno e formativo e nao ha '
 'declaracao de que a ferramenta altere o diagrama do aluno. Decimo terceiro registro do agrupamento de '
 'avaliacao automatizada por LLM. ',
 'DECISAO: excluido em B3 por E8. Nao satisfaz I3.'),

'962_SCOPUS':('B1_E7','',
 'EVIDENCIA: apresenta o ScalePulse, framework dirigido por LLM que analisa continuamente codigo e artefatos '
 'arquiteturais para identificar e explicar riscos de escalabilidade. O componente PulseCore e um '
 'transformer hibrido com atencao dinamica sobre grafos de dependencia e modelos UML para calcular escores '
 'de risco por modulo; os demais componentes propagam risco, preveem gargalos e produzem justificativas com '
 'SHAP e LIME. Avaliacao em plataforma bancaria de microsservicos e aplicacao web de codigo aberto, com 92% '
 'de precisao, 89% de revocacao e ate 30% de ganho de vazao. ',
 'DISCUSSAO: B1 explica sem residuo. Nenhum conteudo UML e produzido: os modelos UML sao insumo para o '
 'calculo de risco, ao lado de codigo e grafos de dependencia, e o produto avaliado sao escores de risco de '
 'escalabilidade do sistema. Note-se que este caso nao e E8: em E8 o LLM avalia o proprio diagrama, ao passo '
 'que aqui o avaliado e o sistema de software, com a UML servindo apenas de fonte de sinal. Precisao e '
 'revocacao sao medidas, mas de deteccao de risco, nao de qualidade de UML. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'963_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: pipeline de duas etapas que combina LLaMA 3.2 1B-Instruct, para gerar especificacoes tecnicas '
 'detalhadas, com DeepSeek-R1-Distill-Qwen-32B, para produzir o codigo PlantUML correspondente, sintetizando '
 'diagramas de sequencia UML. Produz dataset de 1.000 amostras com descricao tecnica, codigo PlantUML e '
 'diagrama resultante. Para validar fidelidade semantica e estrutural, emprega avaliacao multimodal '
 'automatizada com tres modelos de visao e linguagem (Qwen2.5-VL-3B, LLaMA3.2-VL-11B, Aya-Vision-8B), cada '
 'um pontuando o alinhamento entre especificacao textual e representacao visual gerada, com agregacao '
 'ponderada pelo desempenho no benchmark MMMU. Declara explicitamente "This paper extends our framework". ',
 'DISCUSSAO: B1 saida e diagrama de sequencia UML nomeado. B2 origem sao LLMs generativos. B3 direcao e '
 'especificacao tecnica textual para UML. B4 entrada e texto, gerado por LLM, o que vale a mesma ressalva '
 'de validade externa feita em 945. Nenhum portao exclui. Fidelidade semantica e estrutural com escore '
 'agregado e instrumento explicito de qualidade, e o proprio artigo apresenta o sistema de pontuacao como '
 'metodo de garantia de qualidade automatizada, o que o torna duplamente relevante para a revisao: como '
 'estudo primario e como proposta de instrumento de medida. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. ALERTA DE REDUNDANCIA: e continuacao declarada de '
 '945_SCOPUS, com mesma arquitetura de dois modelos e mesma validacao multimodal, mudando o tipo de diagrama '
 '(sequencia em vez de casos de uso) e o tamanho do dataset (1.000 em vez de 3.000). Resolver na fase de '
 'texto completo junto com 818, 848, 868, 869 e 877.'),
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
NOTA=('Setimo lote da triagem do Portao B sobre os registros que mencionam UML em titulo ou resumo '
 '(indices 144 a 167 da ordem de leitura). 24 registros decididos: 12 retidos, 6 B1_E7, 1 B2_E6, '
 '4 B3_E8, 1 B4_E9. '
 'Padrao "texto -> UML -> codigo" confirmado em mais dois registros, 934 (StructGen) e 952 (Xd-CodeGen), '
 'ambos retidos com CANDIDATO_E10: o diagrama e gerado pelo LLM a partir dos requisitos e serve de guia '
 'para o codigo, mas a qualidade medida e a do codigo. Junta-se a 796, 806, 810, 828 e 870. '
 'Notacao adjacente sai em B1: 947 (diagrama Entidade-Relacionamento e esquema relacional em PlantUML) e '
 '955 (fluxograma generico a partir de imagem), somando-se a 759, 781, 895 e 905. UML como ilustracao da '
 'arquitetura do proprio artigo reaparece em 954, mesmo padrao de 843. '
 'Agrupamento de avaliacao automatizada por LLM chega a 13 registros com 940, 941, 950 e 961, todos B3_E8. '
 '950 e variante nova: sumarizacao multimodal de diagramas UML e EMF, isto e, o LLM explica o diagrama em '
 'vez de o pontuar; a linha 282 do manual cobre o caso. '
 'ALERTA DE REDUNDANCIA: 963 declara literalmente "This paper extends our framework" e usa a mesma '
 'arquitetura de dois modelos (LLaMA 3.2 1B-Instruct mais DeepSeek-R1-Distill-Qwen-32B) e a mesma validacao '
 'por tres modelos de visao com agregacao ponderada por MMMU de 945, mudando apenas o tipo de diagrama e o '
 'tamanho do dataset. A familia sob suspeita de fatiamento passa a ter sete membros retidos: 818, 848, 868, '
 '869, 877, 945 e 963. A eleicao do relato mais completo e tarefa da fase de texto completo. '
 'Registros de nucleo identificados: 949 (QuaRUM, F1 de 0,85 a 0,98, kappa de 0,92 acima da concordancia '
 'humana e analise de omissoes de analistas), 956 (caracterizacao formal do diagrama de componentes para '
 'derivar metricas quantitativas contra gabarito de especialista), 939, 942, 948 e 958. '
 '951 e retido pela regra de ouro 1 com INCERTO_PAPEL_LLM: o resumo diz apenas "deep learning-based" e cita '
 'AIGC, sem permitir decidir se ha LLM na acepcao de I2.')
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
