#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolve os 23 residuos de incerteza do Portao B entre os registros com texto.

Sinalizadores tratados: INCERTO_SAIDA (B1), INCERTO_ENTRADA (B3) e
INCERTO_PAPEL_LLM (B4). Todos foram abertos na triagem por titulo e resumo por
falta de informacao, nao por divergencia. Com o texto completo, cada um se
decide pela secao de metodo.

DEFEITO DE INSTRUMENTO CORRIGIDO NESTE LOTE: a varredura de contexto usava
\\bUML\\b, que NAO casa com "PlantUML". Um registro (903_SCOPUS) apareceu com
duas ocorrencias de UML (lista de abreviaturas e titulo de referencia) quando
tem onze de PlantUML, e chegou a ser classificado como E7. A revarredura com
regex separada corrigiu o veredicto. Todos os 23 foram reconferidos; os demais
excluidos por E7 tem PlantUML=0, exceto 626_IEEE, cuja unica ocorrencia e um
diagrama declaradamente feito a mao pelos autores.
"""
import csv, sys

CSV = 'custom_automated_search_collection.csv'
DT = '2026-08-17T00:00:00-03:00'
REV = 'Helaine Barreiros'

CAB = ('=== RESOLUCAO DE INCERTEZA COM TEXTO COMPLETO (2026-08-17) ===\n')

MET = ('METODO: o registro chegou ao Portao C com sinalizador de incerteza aberto na '
       'triagem por titulo e resumo. Com o PDF em maos, o texto integral foi extraido '
       '(pdftotext) e varrido por familias de notacao (UML e PlantUML em regex '
       'separadas, tipos de diagrama, BPMN, SysML, ER, Ecore, metamodelo, codigo) '
       'cruzadas com verbos de geracao, e as sentencas de metodo foram lidas uma a '
       'uma. ')

def bloco(ev, disc, dec):
    return CAB + MET + 'EVIDENCIA: ' + ev + ' DISCUSSAO: ' + disc + ' DECISAO: ' + dec


# ------------------------------------------------------------------ RETIDOS
R = {
 '027_ACM': dict(flags='EVIDENCIA=EXPLICITA', ev=
   'o estudo define seu objeto assim: "domain modeling [...] focuses on externalizing core '
   'domain concepts and relationships among them, typically relying on a subset of the Unified '
   'Modeling Language (UML) Class Diagram notation". O prompt executado e literal: "Generate '
   'missing attributes for each class in this class diagram." A ferramenta MAGDA foi avaliada '
   'em estudo com 30 sujeitos no Canada e na Espanha.', disc=
   'B1 satisfeito: o resultado gerado e conteudo de diagrama de classes UML. B2 satisfeito na '
   'modalidade alteracao, nao producao: e completacao de modelo, que o criterio admite '
   'expressamente. B3 satisfeito: entra o modelo em construcao mais descricao textual. B4 '
   'satisfeito: o LLM propoe classes e atributos, elementos portadores de significado. '
   'O estudo de usuarios com 30 sujeitos e evidencia do eixo U.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '061_ACM': dict(flags='EVIDENCIA=EXPLICITA', ev=
   'formulacao explicita do problema: "Domain modeling involves converting a textual description '
   'of the system in natural language into a structured domain model represented as a class '
   'diagram." A avaliacao "relies on reference domain models constructed by experts to evaluate '
   'the quality of a generated domain model", com precisao, recall e F1 sobre classes, '
   'relacionamentos e atributos.', disc=
   'B1 satisfeito: o modelo de dominio gerado e um diagrama de classes. B3 satisfeito: entrada e '
   'descricao textual do problema. B4 satisfeito: o LLM gera os elementos do modelo e um '
   'mecanismo de auto-realimentacao os revisa. Eixo D presente na modalidade modelo_de_'
   'referencia, com referencia construida por especialistas.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '138_ACM': dict(flags='EVIDENCIA=A_VERIFICAR', ev=
   'e artigo de visao, mas relata testes preliminares proprios, e as duas frases decisivas sao o '
   'fenomeno central da revisao dito com as palavras dos autores: "we noticed that the models '
   'struggle to create reasonable PlantUML code" e "instead of modeling the domain, the LLMs '
   'tried to model the system itself". Segue-se: "In a second iteration, we improved the results '
   'substantially with basic prompt engineering. Instead of PlantUML, we asked directly for the '
   'domain concepts and relations."', disc=
   'ATENCAO AO INSTRUMENTO: a busca por \\bUML\\b retorna zero ocorrencias neste texto; as tres '
   'ocorrencias sao de PlantUML, que aquela regex nao casa. Sem a regex separada o registro '
   'teria sido excluido por engano. B1 satisfeito: o resultado gerado e codigo PlantUML. B3 '
   'satisfeito: entrada sao requisitos funcionais e nao funcionais em linguagem natural. B4 '
   'satisfeito. Nao cabe E1: a lista do E1 e fechada (editorial, keynote, tutorial, poster, '
   'resumo-apenas, tese, livro, patente) e nao inclui artigo de visao, que e relato cientifico '
   'completo ainda que sem resultados consolidados. Nao cabe E12: a geracao de UML e a primeira '
   'etapa e se separa da geracao de arquitetura; o que e magro e o relato, nao a separabilidade. '
   'Eixo L presente ("reasonable PlantUML code") e eixo D presente (modelar o sistema em vez do '
   'dominio), ambos sem vocabulario canonico de qualidade — regra de ouro 2.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '292_ACM': dict(flags='EVIDENCIA=EXPLICITA', ev=
   'o proprio texto nomeia a saida: os autores "use an FSL-based approach on the GPT-3.5-turbo-'
   '1106 LLM to produce textual UML Models in XML notation based on natural-language input". A '
   'escala e declarada: "several class diagrams and structured English models were generated, '
   'the parsing subset (4.225 CD4A models and 359 SEN models)".', disc=
   'B1 satisfeito: modelos UML textuais em XML, e CD4A e a notacao textual de diagrama de classes '
   'para analise. B3 satisfeito: entrada em linguagem natural. B4 satisfeito: GPT-3.5-turbo com '
   'few-shot; o mascaramento por gramatica restringe a forma da saida, nao o conteudo do modelo, '
   'e portanto nao e regra simbolica determinando o conteudo (RF-03). O objeto declarado do '
   'estudo e validade sintatica: eixo L explicito.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '521_IEEE': dict(flags='EVIDENCIA=EXPLICITA', ev=
   '"In domain modeling, engineers typically convert a textual domain specification into a domain '
   'model represented as a class diagram." O desenho e declarado: "We conduct experiments with '
   'two LLMs, GPT3.5 and GPT4 with various prompt engineering methods on the newly created data '
   'set to evaluate the generated models with quantitative and qualitative criteria", sobre "ten '
   'diverse modeling examples with reference solutions created by modeling experts", com '
   '"a semantic scoring technique".', disc=
   'B1, B3 e B4 satisfeitos sem ambiguidade. Registro de alto valor para a funcao constitutiva '
   'da revisao: traz eixo D operacionalizado por modelo de referencia de especialista e uma '
   'tecnica propria de pontuacao semantica, que e exatamente o tipo de operacionalizacao que a '
   'revisao precisa reconstruir.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '623_IEEE': dict(flags='EVIDENCIA=EXPLICITA', ev=
   'ha prompts e saidas transcritos para duas notacoes. Para classes: "Prompt: Generate missing '
   'attributes for each class in this class diagram: package company: employee: [...]". Para '
   'comportamento: "Prompt and generated text for the Activity Diagram" e "To create our prompt, '
   'we design 3 shots using real activity diagrams extracted from a public repository". A '
   'avaliacao e explicita nos dois eixos: "From a conceptual point of view, it fits perfectly the '
   'domain being modeled; and from a syntactic point of view, the completion suggested comply '
   'with the activity diagram syntax."', disc=
   'B1 satisfeito para diagrama de classes e diagrama de atividades. B2 na modalidade '
   'completacao. B4 satisfeito: few-shot prompt learning, e o RF-03 e explicito quanto a exemplos '
   'few-shot nao descaracterizarem o papel do modelo. A ultima frase citada separa julgamento '
   'conceitual de julgamento sintatico: eixos D e L nomeados lado a lado pelo proprio estudo.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '755_SCOPUS': dict(flags='EVIDENCIA=A_VERIFICAR', ev=
   'a saida e nomeada duas vezes: "Given a set of URLs as input, the system executes all stages '
   'sequentially and produces a draft class diagram as output" e "Using the consolidated '
   'terminology as input, it produces a PlantUML class diagram". Ha ainda controle de validade: '
   '"To support the production of syntactically valid artifacts, the agent uses UML tools for '
   'validation and can retry its operations when it produces invalid metamodels."', disc=
   'o titulo fala em metamodelagem, o que abriu a duvida sobre a saida. O texto resolve: o '
   'artefato produzido e um diagrama de classes em PlantUML, validado por ferramentas UML. B1 '
   'satisfeito. B3 satisfeito: a entrada e um corpus de documentacao textual, que e descricao '
   'textual de dominio. B4 satisfeito: sistema multiagente baseado em LLM. Eixo L presente e '
   'operacionalizado por validacao ferramental com repeticao.', dec=
   'RETIDO. INCERTO_SAIDA resolvido.'),

 '903_SCOPUS': dict(flags='EVIDENCIA=A_VERIFICAR', ev=
   'quanto a entrada, que era a duvida: "constructSystem processes freeform textual requirements '
   'and the metamodel to generate an instance model", e a tabela de APIs registra '
   '"constructSystem POST Requirements and metamodel Instance model". Quanto a saida, o prompt e '
   'literal: "You are updating a PlantUML activity diagram describing a telecom management '
   'activity sequence [...] given as {current-activity-sequence}"; as APIs devolvem "PlantUML '
   'activity diagram code" e "PNG of PlantUML class diagram". O criterio de sucesso e: "a '
   'successful completion requires the construction of a syntactically and semantically correct '
   'activity sequence".', disc=
   'ATENCAO AO INSTRUMENTO: este registro esteve a um passo de ser excluido por engano. A '
   'varredura com \\bUML\\b devolvia duas ocorrencias, ambas irrelevantes — a lista de '
   'abreviaturas e o titulo de uma referencia — porque aquela regex nao casa com "PlantUML", que '
   'aparece onze vezes. B3, que era a duvida, esta satisfeito: ha requisitos textuais em formato '
   'livre. Parte do fluxo consome script YANG, que isolado seria E9, mas o criterio exige entrada '
   'SOMENTE nao textual, e nao e o caso. B1 satisfeito. O criterio de sucesso citado separa '
   'correcao sintatica de correcao semantica na mesma frase: e o eixo L e o eixo D nomeados pelo '
   'proprio estudo, no vocabulario da dissonancia que a revisao investiga.', dec=
   'RETIDO. INCERTO_ENTRADA resolvido.'),

 '922_SCOPUS': dict(flags='EVIDENCIA=A_VERIFICAR', ev=
   '"we designed the modeling tasks of these three UML models for 45 undergraduate students who '
   'participated in a requirements modeling course, with the help of LLMs". O procedimento de '
   'analise: "By manually analyzing the created UML models as well as the human-LLM conversation '
   'for this modeling tasks in their project reports, we found that LLM can aid in the creation '
   'and optimization of these three types of UML models, but LLMs still have some shortcomings '
   'and limitations." E ainda: "The output formats of the LLM-aided UML models were summarized to '
   'explore the impact factors of applying LLMs in the UML modeling tasks."', disc=
   'B4, que era a duvida, esta satisfeito: o LLM cria e otimiza os modelos, nao apenas formata. '
   'A analise das conversas humano-LLM torna a instancia de geracao identificavel, o que tambem '
   'antecipa C1 favoravelmente. Tres eixos presentes: L pelo levantamento de formatos de saida, D '
   'pelas limitacoes apontadas nos modelos criados, U pelo desenho com 45 analistas novatos. '
   'Registro de alto valor: e explicitamente exploratorio sobre como o LLM auxilia, que e a '
   'pergunta pragmatica menos coberta.', dec=
   'RETIDO. INCERTO_PAPEL_LLM resolvido.'),

 '456_IEEE': dict(flags='EVIDENCIA=EXPLICITA', ev=
   'a arquitetura e declarada assim: "The method combines dependency parsing, rule-based '
   'filtering of subject-verb-object triplets, and a local large language model to produce '
   'syntactically valid PlantUML code." Contra a leitura de papel meramente formatador, o proprio '
   'artigo credita ganho de desempenho ao modelo: "Incorporating multi-level filtering and '
   'LLM-guided code generation contributed to higher recall and precision, especially in '
   'documents with complex sentence structures", em comparacao com "a rule-based baseline model '
   'that lacks semantic filtering and LLM integration". A favor da leitura oposta: "the use of a '
   'lightweight local LLM ensures privacy and computational efficiency during diagram '
   'generation", que descreve escolha de implementacao.', disc=
   'CASO CONTESTADO, decidido pela regra de ouro 5. A evidencia e genuinamente dividida: atores e '
   'casos de uso saem do parsing de dependencias e da filtragem por regras, o que puxa para o E6 '
   'pelo RF-02 (o LLM formata enquanto regras simbolicas determinam o conteudo); mas o artigo '
   'atribui ganho de recall e precisao a geracao guiada pelo LLM, o que puxa para reter. A tabela '
   'de decidibilidade manda aplicar E6 "so em casos limpidos", e este nao e limpido. Retem-se, e '
   'o papel do modelo passa a ser dado de extracao, registrado no atributo do modelo, e nao '
   'motivo de exclusao. Decisao aprovada pela revisora em 2026-08-17.', dec=
   'RETIDO. INCERTO_PAPEL_LLM resolvido como contestado, com o papel do modelo remetido a '
   'extracao.'),

 '951_SCOPUS': dict(flags='EVIDENCIA=A_VERIFICAR', ev=
   'a camada de processamento e descrita assim: "Implements core conversion logic using the '
   'DeepSeek engine, where a semantic parser extracts class/method entities via a BERT model, a '
   'pattern recognition module matches predefined UML structure templates, and a code generator '
   'converts them into PlantUML syntax." O objeto declarado: "a deep learning-based UML '
   'intelligent generation framework, aiming to directly generate standardized PlantUML code from '
   'natural language requirements", com "multi-view collaborative mechanism to support the joint '
   'generation of class diagrams, sequence diagrams, and use case diagrams" e "dynamic syntax '
   'validation pipelines". A motivacao cita medidas: "a 23% error rate in generated PlantUML '
   'syntax" e "ChatGPT-4 achieves approximately 65% syntax accuracy in simple class diagram '
   'generation tasks".', disc=
   'CASO CONTESTADO, decidido pela regra de ouro 5. Arquitetura hibrida: BERT como extrator de '
   'entidades cai no RF-01 e templates predefinidos de estrutura UML caem no RF-02, o que puxa '
   'para E6; mas o motor DeepSeek e nomeado como implementando a logica de conversao central, e o '
   'texto nao permite decidir onde termina o template e onde comeca o modelo. Nao e caso '
   'limpido, e E6 so se aplica em caso limpido. Retem-se, com o papel do modelo remetido a '
   'extracao. Eixo L presente e quantificado. Decisao aprovada pela revisora em 2026-08-17.', dec=
   'RETIDO. INCERTO_PAPEL_LLM resolvido como contestado, com o papel do modelo remetido a '
   'extracao.'),
}

# ------------------------------------- RETIDOS COM C1 EM ABERTO (CANDIDATO_E12)
RC = {
 '221_ACM': dict(flags='CANDIDATO_E12;EVIDENCIA=A_VERIFICAR', ev=
   'e artigo de simposio doutoral: "During the doctoral research, our aim is to answer which '
   'methods and tools should be developed [...]" e a secao 5 se intitula "PLAN FOR EVALUATION", '
   'com "we plan to experiment with reference solutions" e "we will start with the development of '
   'the explainability and traceability". Ha implementacao inicial: "we have developed a prototype '
   'that uses the BESSER-bot framework". A unica frase com UML e sobre trabalho de terceiros: "It '
   'was possible to create UML class diagrams; however, the output model contains semantic '
   'errors".', disc=
   'nao cabe E1: a lista do E1 e fechada e nao inclui artigo de simposio doutoral, que e relato '
   'cientifico completo. B1 e plausivelmente satisfeito, ja que o assistente sugere elementos de '
   'modelo sobre a plataforma BESSER, de base UML. O que falta e o C1: nao ha instancia de '
   'geracao executada e avaliada, so plano. Pela regra de ouro 1 a incerteza retem, e a decisao '
   'de C1 fica para o bloco proprio.', dec=
   'RETIDO com CANDIDATO_E12. INCERTO_SAIDA resolvido.'),

 '788_SCOPUS': dict(flags='CANDIDATO_E12;EVIDENCIA=A_VERIFICAR', ev=
   'ha geracao de UML pelo modelo, documentada em gravacao de tela: "The participant first asked '
   'ChatGPT to assist in generating UML diagrams for every class (i.e., \u201cthe information '
   'above\u201d), then the participant requested ChatGPT to produce Java code based on the UML '
   'diagram". A tabela de recursos registra o uso "Generate code snippets, seek explanations, '
   'draw UML diagrams" em 11 de 20 participantes do grupo experimental. Mas o que se mede e a '
   'nota do aluno: "Participants\u2019 UML designs are evaluated against a set of predefined '
   'criteria [...] with a total score of 40 points", com media 27,45 no grupo ChatGPT contra '
   '28,91 no grupo controle, e tempo de 30,76 contra 44,99 minutos.', disc=
   'B4, que era a duvida, esta satisfeito: o modelo gera diagramas UML de classes a partir da '
   'descricao textual da tarefa, e isso e papel substantivo. O que permanece em aberto e o C1 sob '
   'outra forma: o artefato avaliado e o diagrama entregue pelo aluno, que pode ou nao incorporar '
   'a saida do modelo, e o estudo nao separa uma coisa da outra. E o atributo atribuicao do '
   'resultado na modalidade agregado. O sinalizador CANDIDATO_E10, aberto na passagem anterior, e '
   'convertido em CANDIDATO_E12 conforme a emenda A004. Registre-se que o valor deste estudo esta '
   'no eixo U: efeito sobre tempo e correcao do trabalho humano, com direcao oposta nas duas '
   'medidas.', dec=
   'RETIDO com CANDIDATO_E12. INCERTO_PAPEL_LLM resolvido; CANDIDATO_E10 convertido em '
   'CANDIDATO_E12.'),

 '845_SCOPUS': dict(flags='CANDIDATO_E12;EVIDENCIA=A_VERIFICAR', ev=
   'o texto tem uma unica mencao a UML, e e uma alegacao de capacidade: "These agents produce '
   'documentation, models, and diagrams (e.g., UML) while adhering to predefined quality and '
   'performance measures." A unica figura de modelo e "Figure 3: Concept Diagram", que descreve a '
   'arquitetura do proprio sistema CogniSim e nao e UML. O texto integral tem menos de dez mil '
   'caracteres.', disc=
   'B1 fica em sim ambiguo: a UML e nomeada como saida dos agentes, mas entre parenteses e a '
   'titulo de exemplo, sem nenhuma instancia mostrada. O filtro decisivo e o C1: nao ha execucao, '
   'nao ha artefato, nao ha resultado — e a UML e um item de uma lista de saidas do mesmo fluxo, '
   'que e literalmente o enunciado do E12. Pela regra de ouro 1 retem-se e decide-se no bloco '
   'proprio.', dec=
   'RETIDO com CANDIDATO_E12. INCERTO_SAIDA resolvido.'),

 '854_SCOPUS': dict(flags='CANDIDATO_E12;EVIDENCIA=A_VERIFICAR', ev=
   'ha instancia de geracao nomeada: "They used ChatGPT-4o-mini to first generate a set of UML '
   'task descriptions, and then from those descriptions, corresponding UML diagrams (by '
   'generating PlantUML source code)." Mas ela e um subprojeto entre varios: "The resulting '
   'datasets were highly varied, including buggy code in multiple languages, code with stylistic '
   'variations, UML diagrams, and natural language programming prompts", e "two projects explored '
   'more visual data (Groups D, J), specifically UML diagrams (Group D) and weighted graphs '
   '(Group J)".', disc=
   'B1, B2, B3 e B4 satisfeitos para o Grupo D. O objeto do artigo, porem, e a viabilidade de '
   'projetos de pos-graduacao com dados sinteticos, e a UML e um caso entre dez. O C1 depende de '
   'haver resultado atribuivel ao artefato UML e nao ao conjunto de projetos. CANDIDATO_E10 '
   'convertido em CANDIDATO_E12 conforme a A004.', dec=
   'RETIDO com CANDIDATO_E12. INCERTO_SAIDA resolvido; CANDIDATO_E10 convertido em '
   'CANDIDATO_E12.'),

 '890_SCOPUS': dict(flags='CANDIDATO_E12;EVIDENCIA=A_VERIFICAR', ev=
   'ha atribuicao explicita de autoria a um modelo: "Figure 2: Partial Activity diagram of '
   'Indirect channel processes generated by CoPilot". A metodologia recomendada parte do texto do '
   'caso: "first capture the user experience (UX personas) of the actors identified from the case '
   'narrative and understand the functional roles of these actors in the business processes '
   'described in the case using UML activity diagram(s)".', disc=
   'B1 satisfeito: diagrama de atividades UML. B3 satisfeito: a narrativa do caso e a entrada. B4 '
   'satisfeito: o CoPilot gera o diagrama. O aberto e o C1: o artigo e um estudo de caso didatico '
   'para curso de analise de sistemas, e o diagrama gerado convive com personas de UX e user '
   'stories no mesmo fluxo, sem resultado isolado atribuivel ao diagrama. CANDIDATO_E10 '
   'convertido em CANDIDATO_E12 conforme a A004.', dec=
   'RETIDO com CANDIDATO_E12. INCERTO_SAIDA resolvido; CANDIDATO_E10 convertido em '
   'CANDIDATO_E12.'),
}

# ------------------------------------------------------------ EXCLUIDOS EM B
X = {
 '141_ACM': dict(cod='E7', out='B1_E7', ev=
   'a divisao de trabalho e a tese do artigo: "rather than having LLMs generate entire '
   'applications from single prompts, we advocate for a white-box approach allowing citizen '
   'developers to specify domain models semi-formally". O modelo de dominio e humano: "we let the '
   'citizen developer define an invariable domain model, which consists only of structural '
   'elements (e.g., classes, attributes, and associations)". A saida do LLM e codigo: "The '
   'generated Java code contains static elements such as classes, fields and getters/setters" e '
   '"Usage of a LLM contextualized with the existing source code in order to fill in the '
   'generated stubs one after another". As duas mencoes a UML sao de trabalho relacionado ("They '
   'use ChatGPT to create ER, UML, BPMN and Heraklit diagrams").', disc=
   'B1 nao satisfeito: o resultado gerado pelo modelo e codigo-fonte Java, nao conteudo UML. O '
   'modelo de dominio, que e o artefato de modelagem, entra no processo pronto, feito pela '
   'pessoa. Nao cabe E1, porque a lista do E1 e fechada e nao inclui artigo de visao. Nao cabe E9 '
   'antes de E7, porque B1 precede B3 e ja e decisivo. Verificacao de instrumento: PlantUML '
   'aparece zero vezes no texto integral.', dec=
   'EXCLUIDO por E7 no Portao B, filtro B1. INCERTO_SAIDA resolvido.'),

 '539_IEEE': dict(cod='E7', out='B1_E7', ev=
   'a saida e SysML em todas as passagens de metodo: "The same technique to be utilized for '
   'generating Systems Modeling Language (SysML) model entities by training NLP model with '
   'labelled data" e "The ML tool trained with multi-disciplinary data would generate textual '
   'entities which when integrated with MBSE tool would help in assisting generation of '
   'requirements and SysML models automatically or semi-automatically". As quatro ocorrencias de '
   'UML estao todas em trabalho relacionado e em titulos de referencias (RAPID, "Generating UML '
   'Diagrams from Natural Language Specifications").', disc=
   'B1 nao satisfeito. O manual e explicito nesta rota: requisitos para LLM produzindo BPMN, ER, '
   'C4, SysML ou Mermaid, sem UML, e E7 no filtro B1. O registro tambem tinha INCERTO_PAPEL_LLM '
   'aberto, e o treinamento de modelo NLP com dados rotulados apontaria para E6, mas B1 precede '
   'B4 e a regra de ouro 3 manda registrar um so criterio primario. Verificacao de instrumento: '
   'PlantUML aparece zero vezes.', dec=
   'EXCLUIDO por E7 no Portao B, filtro B1. INCERTO_SAIDA e INCERTO_PAPEL_LLM resolvidos.'),

 '563_IEEE': dict(cod='E7', out='B1_E7', ev=
   'a saida e BPMN, declarada sem ambiguidade: "In this paper, regardless of whether it is '
   'generating a process model or modifying a process model, multi-agent operate on the BPMN '
   'text", e ha uma tabela intitulada "The BPMN elements and descriptions". As quatro ocorrencias '
   'de UML sao de enquadramento e de referencia: "Commonly used modeling languages include BPMN, '
   'UML, Petri Net, EPC, and YAWL" e a citacao da especificacao OMG.', disc=
   'B1 nao satisfeito: nenhum conteudo UML no resultado gerado. Mesma rota do manual que se '
   'aplica a SysML. Verificacao de instrumento: PlantUML aparece zero vezes.', dec=
   'EXCLUIDO por E7 no Portao B, filtro B1. INCERTO_SAIDA resolvido.'),

 '626_IEEE': dict(cod='E7', out='B1_E7', ev=
   'o fluxo gerado e de metamodelo, modelo de instancia, restricoes formais e codigo: "Meta Model '
   '(e.g., in Ecore)", "Formal constraints (e.g., in OCL)", "The code generation process takes '
   'three inputs: the metamodel, the instance model, and a code generation template". A unica '
   'ocorrencia de PlantUML no texto integral declara autoria humana: "To illustrate the outcome, '
   'we provide a manually created activity diagram using PlantUML (Fig. 4)". As mencoes a UML sao '
   'de padroes e de referencia bibliografica.', disc=
   'B1 nao satisfeito: o unico artefato UML do artigo foi feito a mao pelos autores para ilustrar '
   'o resultado, e ilustracao de autoria humana nao e resultado gerado. Verificacao de '
   'instrumento: a unica ocorrencia de PlantUML foi lida em contexto justamente para descartar o '
   'erro de regex que quase custou o 903_SCOPUS. O INCERTO_ENTRADA tambem estava aberto e fica '
   'prejudicado, porque B1 precede B3.', dec=
   'EXCLUIDO por E7 no Portao B, filtro B1. INCERTO_SAIDA e INCERTO_ENTRADA resolvidos.'),

 '825_SCOPUS': dict(cod='E7', out='B1_E7', ev=
   'a saida e SysML: "SysML version 2 models were utilized along with Retrieval-Augmented '
   'Generation (RAG) were used to add information to the LLM to improve model accuracy and '
   'specificity in the MBSE domain", e o proposito e "the generation of MBSE elements as well as '
   'gain support on the application of any portion of the MBSE/SysML". As cinco ocorrencias de '
   'UML sao de trabalho relacionado e de titulo de referencia.', disc=
   'B1 nao satisfeito, pela mesma rota do manual. Observe-se que o RAG aqui nao muda nada: pelo '
   'RF-03 o RAG e razao para reter, nao para excluir, mas o que decide e a notacao da saida, e '
   'ela nao e UML. O CANDIDATO_E10 aberto na passagem anterior fica prejudicado, porque o '
   'registro sai antes de chegar ao Portao C. Verificacao de instrumento: PlantUML aparece zero '
   'vezes.', dec=
   'EXCLUIDO por E7 no Portao B, filtro B1. INCERTO_SAIDA resolvido; CANDIDATO_E10 prejudicado.'),

 '813_SCOPUS': dict(cod='E6', out='B4_E6', ev=
   'o sistema avaliado nao e um LLM, e os proprios autores o dizem ao se compararem com LLMs: '
   '"two transformer-based approaches are proposed: a Sequence-to-Sequence (Seq2Seq) model '
   'designed for direct diagram code generation, and a Sequence-to-Abstract-Syntax-Tree (Seq2AST) '
   'model that incorporates syntactic constraints", e "the proposed framework achieves accuracy '
   'comparable to general-purpose large language models while offering greater determinism and '
   'stronger domain alignment. Furthermore, it operates with significantly lower computational '
   'requirements". Os modelos sao treinados sobre conjunto proprio (PlantUCD-dataset). Todas as '
   'mencoes a LLM sao de trabalho relacionado.', disc=
   'CASO CONTESTADO, decidido a favor da exclusao porque, ao contrario dos outros dois '
   'contestados, aqui a evidencia e limpida: os autores declaram que seu sistema nao e um LLM e '
   'constroem o argumento do artigo justamente sobre a diferenca. O I4 exige ao menos um LLM como '
   'componente substantivo, e nao ha. O RF-01 admite encoder quando generativo e constitutivo, '
   'mas isso resolve o caso de encoder dentro de um LLM, nao o caso de tradutor neural treinado '
   'do zero para a tarefa. Registre-se com todas as letras que este e o registro '
   'substantivamente mais proximo do objeto da revisao entre os excluidos deste lote: trata de '
   'geracao de diagrama de classes a partir de requisitos, com validacao sintatica por arvore de '
   'sintaxe abstrata, ou seja, opera exatamente no eixo L. Sai por escopo de tecnologia, nao por '
   'irrelevancia, e e candidato forte a pilha de background. Decisao aprovada pela revisora em '
   '2026-08-17.', dec=
   'EXCLUIDO por E6 no Portao B, filtro B4. INCERTO_PAPEL_LLM resolvido. Encaminhado a pilha de '
   'background.'),
}

# --------------------------------------------------------------- EXCLUIDO EM A
A = {
 '051_ACM': dict(cod='E1', out='A2_E1', ev=
   'a propria ficha ACM do artigo declara a extensao: "In ACM Conference on International '
   'Computing Education Research V.2 (ICER 2025 Vol. 2) [...] ACM, New York, NY, USA, 1 page." O '
   'texto integral extraido tem cerca de seis mil caracteres e consiste em resumo, conceitos CCS, '
   'palavras-chave e quatro referencias, sem secao de metodo nem de resultados. O volume 2 da '
   'ICER e o volume de posteres e apresentacoes relampago.', disc=
   'E1 e criterio do Portao A, filtro A2, e precede todo o Portao B. O registro havia passado o '
   'Portao A por titulo e resumo e so se revelou poster com o texto em maos — o mesmo padrao dos '
   'tres casos de familia de publicacao que so foram resolvidos no texto completo. Registre-se '
   'que o conteudo seria de interesse (ha medidas como "2.4 prompt iterations for usable '
   'diagrams" e a afirmacao de que "diagramming tools can produce precise UML models with minimal '
   'effort"), mas um resumo de uma pagina nao sustenta extracao de operacionalizacao de '
   'construto, que e a funcao constitutiva desta revisao. O INCERTO_PAPEL_LLM e o CANDIDATO_E10 '
   'ficam prejudicados, porque o registro sai antes do Portao B.', dec=
   'EXCLUIDO por E1 no Portao A, filtro A2. INCERTO_PAPEL_LLM e CANDIDATO_E10 prejudicados.'),
}


def main(apply=False):
    with open(CSV, newline='', encoding='utf-8') as f:
        rd = csv.DictReader(f)
        campos = rd.fieldnames
        L = list(rd)
    idx = {r['logical_id']: r for r in L}
    saida = []

    for lid, n in list(R.items()) + list(RC.items()):
        r = idx[lid]
        r['gate_b_notes'] = (r['gate_b_notes'] + '\n\n' + bloco(n['ev'], n['disc'], n['dec'])).strip()
        r['gate_b_reviewer'] = REV
        r['gate_b_datetime'] = DT
        r['gate_c_flags'] = n['flags']
        r['gate_c_reviewer'] = REV
        r['gate_c_datetime'] = DT
        saida.append((lid, 'RETIDO', n['flags']))

    for lid, n in X.items():
        r = idx[lid]
        r['gate_b_notes'] = (r['gate_b_notes'] + '\n\n' + bloco(n['ev'], n['disc'], n['dec'])).strip()
        r['gate_b_outcome'] = n['out']
        r['gate_b_reviewer'] = REV
        r['gate_b_datetime'] = DT
        r['exclusion_criteria'] = n['cod']
        r['excluded'] = 'true'
        r['gate_c_flags'] = ''
        r['gate_c_notes'] = ''
        r['gate_c_reviewer'] = ''
        r['gate_c_datetime'] = ''
        saida.append((lid, n['cod'], n['out']))

    for lid, n in A.items():
        r = idx[lid]
        r['gate_a_notes'] = (r['gate_a_notes'] + '\n\n' + bloco(n['ev'], n['disc'], n['dec'])).strip()
        r['gate_a_outcome'] = n['out']
        r['gate_a_reviewer'] = REV
        r['gate_a_datetime'] = DT
        r['exclusion_criteria'] = n['cod']
        r['excluded'] = 'true'
        r['gate_b_outcome'] = ''
        r['gate_c_flags'] = ''
        r['gate_c_notes'] = ''
        r['gate_c_reviewer'] = ''
        r['gate_c_datetime'] = ''
        saida.append((lid, n['cod'], n['out']))

    if apply:
        with open(CSV, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(L)

    for t in sorted(saida):
        print('%-12s %-8s %s' % t)
    print('---\ntotal', len(saida))
    ex = sum(1 for r in L if r['excluded'] == 'true')
    print('corpus %d | excluidos %d | retidos %d' % (len(L), ex, len(L) - ex))


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
