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
'964_SCOPUS':('B1_E7','',
 'EVIDENCIA: o artigo examina o processo de elaboracao de uma especificacao de requisitos de sistema e '
 'propoe abordagem para sua verificacao formal com o servico ChatGPT, com formalizacao matematica do objeto '
 'de pesquisa, modelo estruturado de preparacao de requisitos e metodologia de verificacao por interacao '
 'com prompts. A unica mencao a UML e instrumental: "To support the analysis, relevant tabular data and UML '
 'diagrams are provided". A novidade declarada e a verificacao de requisitos modelando o comportamento '
 'esperado do sistema futuro com o ChatGPT. ',
 'DISCUSSAO: B1 explica sem residuo. Os diagramas UML sao recurso expositivo dos autores para apoiar a '
 'analise, ao lado de tabelas, e nao produto gerado por LLM nem objeto de avaliacao. O produto do trabalho '
 'e a especificacao de requisitos e o metodo de verificacao. Mesmo padrao de falso positivo ja registrado '
 'em 843_SCOPUS e 954_SCOPUS: UML como ilustracao do proprio artigo. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'965_SCOPUS':('PASSOU','INCERTO_ENTRADA;EVIDENCIA=EXPLICITA',
 'EVIDENCIA: investiga a integracao de LLMs em arquitetura codificador-decodificador para documentacao '
 'arquitetural em tempo real e conversao entre modelos semiformais (por exemplo, diagramas UML) e '
 'descricoes em linguagem natural, em ambos os sentidos. O decodificador "helps transform text-based '
 'process descriptions into structured architectural models". A eficacia e avaliada "by comparing '
 'reconstructed models with their originals, assessing how well information is preserved and how accurately '
 'the transformations are performed". ',
 'DISCUSSAO: B1 saida inclui modelo arquitetural estruturado, exemplificado como diagrama UML. B2 origem e '
 'LLM. B3 e bidirecional: o ramo modelo-para-texto isolado seria E7, mas o ramo texto-para-modelo e '
 'constitutivo e corresponde a celula "requisitos -> LLM -> UML" da secao 4.3. B4 e o ponto aberto: no '
 'desenho de ida e volta, o texto que alimenta o decodificador e ele proprio derivado de um modelo '
 'preexistente pelo codificador, e nao uma especificacao textual autonoma, o que aproximaria o caso de E9. '
 'O resumo tambem menciona descricoes de processo de organizacoes, que seriam entrada textual legitima. '
 'Nao e decidivel em titulo e resumo; pela regra de ouro 1, incerteza retem. A comparacao entre modelo '
 'reconstruido e original com medida de preservacao de informacao e instrumento explicito de qualidade. ',
 'DECISAO: retido no Portao B com flag INCERTO_ENTRADA; EVIDENCIA=EXPLICITA. No texto completo verificar se '
 'ha experimento partindo de descricao textual genuina ou apenas reconstrucao de ida e volta.'),

'966_SCOPUS':('B3_E7','',
 'EVIDENCIA: propoe o UML2Dep, framework de geracao de codigo passo a passo. Introduz um diagrama de '
 'sequencia UML estendido para arquiteturas orientadas a servicos, que amplia a sintaxe visual tradicional '
 'integrando tabelas de decisao e especificacoes de API, e uma tarefa de inferencia de dependencia de dados '
 '(DDI) formalizada como raciocinio matematico sob restricoes. Resultados: 89,97% de revocacao, 95,06% de '
 'precisao e 92,33% de F1 na tarefa de DDI; a integracao ao pipeline aumenta a taxa de compilacao em 8,83% '
 'e a de testes unitarios em 11,66%. ',
 'DISCUSSAO: B1 nao exclui, ha UML no caso. B2 nao exclui, o LLM e generativo. B3 explica sem residuo: a '
 'extensao do diagrama de sequencia e contribuicao de notacao feita pelos autores, e o diagrama entra no '
 'pipeline como especificacao formal nao ambigua de origem; o produto avaliado e codigo, medido por '
 'compilacao e testes. E a celula "UML existente -> LLM -> codigo" da secao 4.3. Distingue-se de 934 e 952 '
 'justamente aqui: la o diagrama e sintetizado pelo LLM a partir dos requisitos, aqui ele precede o LLM. '
 'Toda a metrica de qualidade reportada incide sobre dependencias de dados e codigo, nunca sobre o '
 'diagrama. ',
 'DECISAO: excluido em B3 por E7. Nao satisfaz I5. Preservada no desfecho a distincao em relacao a B1_E7: '
 'aqui havia UML, mas na entrada.'),

'968_SCOPUS':('B3_E7','',
 'EVIDENCIA: propoe metodo de geracao automatica de codigo Java que integra diagramas de classes UML a LLMs. '
 'Usa DOM4J e templates FreeMarker para transformar o XML de UML exportado por ferramenta em representacao '
 'unificada, constroi o dataset umltocode de pares alinhados de XML UML e Java, e ajusta o CodeLlama para '
 'geracao direta de UML para Java. A qualidade e avaliada por estrategia de pontuacao orientada a '
 'consistencia estrutural, com melhora reportada em fidelidade de estrutura de codigo e acuracia semantica. ',
 'DISCUSSAO: B3 explica sem residuo: o diagrama de classes e exportado de ferramenta de modelagem, precede '
 'integralmente o LLM, e o produto avaliado e codigo-fonte Java. Celula "UML existente -> LLM -> codigo" da '
 'secao 4.3. A consistencia estrutural medida e entre codigo e diagrama de origem, ou seja, mede a fidelidade '
 'da traducao, nao a qualidade do conteudo UML. ',
 'DECISAO: excluido em B3 por E7. Nao satisfaz I5.'),

'970_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: explora o uso de LLMs com tecnica de prompting Chain-of-Thought adaptada para automatizar a '
 'derivacao de diagramas de classes a partir de user stories em engenharia de requisitos agil. Estudo '
 'preliminar abrangente comparando tecnicas de prompting e comparando as abordagens com LLM contra extracao '
 'humana guiada e nao guiada. Achados: as abordagens com LLM, sobretudo com prompts few-shot bem '
 'construidos, superam a extracao humana guiada na identificacao de classes; analise qualitativa identifica '
 'areas de desempenho suboptimo. ',
 'DISCUSSAO: B1 saida e diagrama de classes. B2 origem e LLM generativo; o verbo "extraction" aqui nao '
 'aciona a RF-01, porque o mecanismo declarado e prompting de LLM generativo e nao NER ou classificador, '
 'mesma distincao ja aplicada em 876 e 933 contra 841 e 911. B3 direcao e user story para UML. B4 entrada e '
 'user story, item nomeado literalmente na delimitacao de escopo. Nenhum portao exclui. O comparador humano '
 'em duas condicoes (guiada e nao guiada) e desenho de alta qualidade para atribuir a diferenca ao LLM. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA.'),

'971_SCOPUS':('B4_E9','',
 'EVIDENCIA: relata experimento de engenharia reversa de simulacoes NetLogo para diagramas de sequencia UML '
 'restritos que representam cenarios de execucao, produzidos por agentes generativos especializados, com '
 'auditorias de conformidade intermediarias guiadas por personas e regras de dominio. Avaliacao sobre dez '
 'simulacoes NetLogo publicas pareadas com oito modelos de IA generativa, totalizando 80 execucoes; Gemini '
 '2.5 Flash obteve o melhor resultado, seguido de GPT-5-mini, GPT-5 e Devstral. KW inclui ReversEngineering. ',
 'DISCUSSAO: B1 nao exclui, o produto e diagrama de sequencia UML. B2 nao exclui, sao agentes generativos. '
 'B3 nao exclui, a direcao termina em UML. B4 explica sem residuo: a entrada e codigo NetLogo, sem qualquer '
 'componente de especificacao textual de requisitos. E o caso de engenharia reversa que a delimitacao de '
 'escopo de 2026-08-16 coloca fora por I4. ',
 'DECISAO: excluido em B4 por E9. Exclusao onerosa, nomeada para recuperacao sem re-triagem caso I4 seja '
 'emendado: mede conformidade do modelo gerado em 80 execucoes com oito LLMs, desenho comparativo forte. '
 'Junta-se a 865, 921, 930, 937 e 982.'),

'972_SCOPUS':('B3_E8','',
 'EVIDENCIA: avalia LLMs multimodais, especificamente GPT-4o e GPT-4o-mini, na identificacao precisa de '
 'elementos semanticos em imagens de diagramas de casos de uso UML. Experimentos sobre novo conjunto de '
 'diagramas coletados de fontes online. Resultado: ambos os modelos tiveram dificuldade em identificar e '
 'interpretar corretamente elementos-chave, com erros de classificacao e omissoes. ',
 'DISCUSSAO: B1 nao exclui, ha UML. B2 nao exclui, sao LLMs multimodais. B3 explica sem residuo: o diagrama '
 'preexiste, foi coletado pronto, e o LLM apenas o le e interpreta, celula "UML existente -> LLM -> '
 'avaliacao/explicacao/critica" da secao 4.3 e linha 282 do manual. Condicao restritiva do E8 verificada: o '
 'diagrama nao e alterado. O que se mede e a capacidade de reconhecimento do modelo, nao a qualidade de UML '
 'gerada. Se o caso sobrevivesse a B3, sairia em B4, pois a entrada e imagem. Mesma configuracao de '
 '950_SCOPUS. ',
 'DECISAO: excluido em B3 por E8. Nao satisfaz I3.'),

'974_SCOPUS':('B1_E7','',
 'EVIDENCIA: introduz abordagem automatizada de construcao de metamodelo especifico de dominio apoiada em '
 'LLM, com foco no dominio automotivo. Prototipo em Python como servico web usando GPT-4o. Declara que a '
 'abordagem "successfully constructs Ecore metamodel based on set of automotive requirements" e que a '
 'novidade e a sinergia entre abordagem iterativa e "intermediate step visualization relying on PlantUML '
 'notation", para que especialistas humanos deem retorno e refinem o resultado. ',
 'DISCUSSAO: B1 explica sem residuo. O artefato produzido e um metamodelo Ecore, linguagem de metamodelagem '
 'do EMF, que nao pertence ao metamodelo UML nem e perfil dele. A PlantUML entra apenas como visualizacao '
 'do passo intermediario para permitir retorno humano, isto e, como recurso de apresentacao do Ecore, e '
 'nenhum tipo de diagrama UML e nomeado como produto. Nao e o terceiro caso de B1 previsto no manual, que '
 'trata de trabalhos cujo produto e um artefato PlantUML de tipo nao declarado; aqui o produto esta '
 'declarado e nao e UML. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5. Decisao de fronteira registrada para o segundo revisor: '
 'quem entenda que a renderizacao PlantUML de um metamodelo constitui conteudo UML chegaria a retencao com '
 'INCERTO_SAIDA. Nomeado para recuperacao sem re-triagem.'),

'975_SCOPUS':('PASSOU','INCERTO_SAIDA;EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: propoe abordagem dirigida a testes assistida por LLM que introduz estrutura formal para guiar '
 'o LLM na geracao de especificacoes de casos de uso (UCS) a partir de requisitos em linguagem natural. '
 'Para validar a consistencia dos fluxos das UCS com a logica de processos de negocio de alto nivel, '
 '"UML activity and state machine diagrams are used as specific modeling methods for such processes". Tres '
 'regras novas de validacao, com objetos de negocio conectando UCS aos modelos e ligando niveis de '
 'abstracao, rastreabilidade bidirecional entre requisitos e testes e laco de retorno. Resultado declarado: '
 'melhora da qualidade da especificacao de requisitos e geracao semiautomatica de casos de teste. ',
 'DISCUSSAO: B2 nao exclui, o LLM gera as especificacoes. B4 nao exclui, a entrada e requisito em linguagem '
 'natural. B3: os diagramas de atividade e de maquina de estados figuram como metodo de modelagem dos '
 'processos de negocio contra os quais a consistencia e verificada, e nao como produto do LLM, o que '
 'poderia sugerir E8; mas o artefato produzido e refinado pelo laco e a propria UCS, nao o diagrama, de modo '
 'que a celula de avaliacao de diagrama preexistente nao se aplica com clareza. B1 e o ponto aberto: o '
 'produto do LLM e a especificacao textual de caso de uso, e a questao de protocolo sobre descricao textual '
 'de caso de uso continua sem decisao. Pela regra de ouro 1, incerteza retem. ',
 'DECISAO: retido no Portao B com flag INCERTO_SAIDA; EVIDENCIA=A_VERIFICAR, pois a melhora de qualidade e '
 'afirmada sem instrumento declarado no resumo. Quarto registro do agrupamento de descricao textual de caso '
 'de uso, junto de 871, 837 e 923.'),

'976_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: investiga as capacidades do ChatGPT em tarefas de modelagem e como assistente de modeladores, '
 'buscando identificar suas principais deficiencias. Achado declarado: em contraste com a geracao de '
 'codigo, o desempenho do ChatGPT em modelagem de software e limitado, "with various syntactic and semantic '
 'deficiencies, lack of consistency in responses and scalability issues". Encerra com a visao dos autores '
 'sobre o papel dos LLMs na disciplina de modelagem. KW: ChatGPT, Modeling languages, Software models, UML. ',
 'DISCUSSAO: B1 saida e modelo de software em UML. B2 origem e ChatGPT. B3 direcao e de tarefa de modelagem '
 'para modelo. B4 entrada e enunciado textual das tarefas. Nenhum portao exclui. Deficiencia sintatica, '
 'deficiencia semantica e falta de consistencia sao vocabulario literal de I6, e o registro e um relato de '
 'experiencia seminal do periodo, provavelmente muito citado pelos demais do corpus. Note-se que "experience '
 'report" nao aciona E1: e artigo cientifico completo em periodico, nao editorial, prefacio ou coluna de '
 'opiniao, diferentemente da questao levantada em 879_SCOPUS. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Prioridade alta na leitura de texto completo, tanto '
 'como estudo primario quanto como referencia de contextualizacao.'),

'978_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: explora o uso do paradigma de geracao aumentada por recuperacao para extracao automatica de '
 'requisitos e geracao de diagramas UML, com foco em diagramas de casos de uso e de sequencia. Analisa '
 'vantagens e desafios da metodologia "with a particular focus on model accuracy" e apresenta implementacao '
 'pratica. O estudo de caso foi fornecido pelo Ministerio da Justica italiano, por meio da Direzione '
 'Generale per i Sistemi Informativi Automatizzati. ',
 'DISCUSSAO: B1 saida sao dois tipos nomeados do metamodelo UML. B2 origem e LLM com RAG. B3 direcao e '
 'documento de requisitos para UML. B4 entrada e documentacao textual de um orgao publico, especificacao '
 'em linguagem natural. Nenhum portao exclui. A acuracia do modelo e declarada como foco, mas o resumo nao '
 'nomeia instrumento, gabarito nem resultado numerico, e o texto tem feicao de relato de experiencia '
 'aplicado. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=A_VERIFICAR. Verificar no texto completo se ha medida sobre os '
 'diagramas; caso contrario e candidato a E11. O caso real de orgao publico tem valor proprio para a '
 'discussao de validade externa.'),

'981_SCOPUS':('B1_E7','',
 'EVIDENCIA: desenvolve plugin para VSCode e abordagem baseada em LLM para recuperar elos de rastreabilidade '
 'entre requisitos de seguranca e codigo-fonte, motivada por normas como a ISO 26262. Resultado: os LLMs '
 'sao capazes da tarefa por combinarem compreensao de codigo e de texto, com o Llama atingindo precisao de '
 '0,8. A unica mencao a UML e na enumeracao de artefatos do processo: "such as source code, test cases, or '
 'various UML diagrams". ',
 'DISCUSSAO: B1 explica sem residuo. Nenhum conteudo UML e gerado nem avaliado: a UML aparece em lista '
 'ilustrativa de artefatos que uma norma manda rastrear. O produto e o elo de rastreabilidade entre '
 'requisito e codigo, e a precisao medida e a da recuperacao de elos. Armadilha lexical classica de mencao '
 'de UML em contextualizacao. ',
 'DECISAO: excluido em B1 por E7. Nao satisfaz I5.'),

'982_SCOPUS':('B4_E9','',
 'EVIDENCIA: avalia empiricamente cinco LLMs (ChatGPT-4.5, DeepSeek V3, DeepHermes 3 LLaMA 3 8B, QwQ 32B e '
 'OlympicCoder 32B) no paradigma de transformacao de modelos por exemplo, em tres cenarios de complexidade '
 'crescente: RDBMS-to-UML, UML-to-Java e SysML-to-AAS, cada um sob tres configuracoes que variam o numero '
 'de pares de exemplo. Os LLMs geram diretamente os modelos-alvo a partir do modelo-fonte, dos pares de '
 'exemplo e de regras de mapeamento iniciais. As saidas sao avaliadas por corretude e por metricas de '
 'sucesso ponderado que consideram fidelidade estrutural e semantica. ',
 'DISCUSSAO: B1 nao exclui, um dos cenarios (RDBMS-to-UML) tem UML como produto. B2 nao exclui, sao LLMs. '
 'B3 e misto: UML-to-Java isolado seria E7, RDBMS-to-UML termina em UML. B4 explica sem residuo e torna o '
 'desfecho estavel sob qualquer leitura: em todos os tres cenarios a entrada e um modelo preexistente '
 '(esquema relacional, modelo UML ou modelo SysML), nunca especificacao textual de requisitos, user story '
 'ou descricao de dominio. E transformacao modelo-para-modelo, hipotese que a delimitacao de escopo de '
 '2026-08-16 coloca fora por I4. ',
 'DECISAO: excluido em B4 por E9. Exclusao onerosa, nomeada para recuperacao sem re-triagem caso I4 seja '
 'emendado: corretude e fidelidade estrutural e semantica sobre modelos gerados por cinco LLMs, com desenho '
 'fatorial. Junta-se a 865, 921, 930, 937 e 971.'),

'983_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: apresenta comparacao abrangente de LLMs de codigo aberto e fechado combinados com as tecnicas '
 'de prompting mais eficazes e acessiveis, sobre um novo conjunto de especificacoes de caso de alta '
 'qualidade, com "an automated evaluation on generated UML class diagrams". Avalia como o tamanho do modelo '
 'e a complexidade do caso afetam a qualidade dos modelos gerados e qual LLM e qual tecnica de prompting '
 'escolher para cada tarefa. Dataset e codigo experimental disponibilizados em repositorio publico. ',
 'DISCUSSAO: B1 saida e diagrama de classes UML como modelo conceitual. B2 origem sao LLMs generativos. B3 '
 'direcao e especificacao textual para UML. B4 entrada e especificacao de caso em texto, caso canonico do '
 'escopo. Nenhum portao exclui. E um dos registros mais fortes do corpus: avaliacao automatizada declarada, '
 'analise de fatores moderadores (tamanho do modelo e complexidade do caso) e artefatos de replicacao '
 'publicos, o que sustenta tanto a extracao de resultados quanto a avaliacao de qualidade do estudo. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Registro de nucleo e prioridade alta de leitura.'),

'984_SCOPUS':('B3_E7','',
 'EVIDENCIA: compara a eficacia da geracao de codigo por LLMs, de base e ajustados (DeepSeek e LLama2), com '
 'geradores de codigo produzidos pelo processo de code-generation by example, que usa aprendizado de '
 'maquina simbolico para sintetizar geradores em MDE. O resumo declara que os geradores resultantes '
 '"map from UML/OCL specifications to the target programming language" e situa a comparacao no contexto de '
 'MDE agil. ',
 'DISCUSSAO: B3 explica sem residuo: as especificacoes UML e OCL sao insumo dado e o produto avaliado e '
 'codigo executavel, com a discussao girando em torno de confiabilidade, consistencia e corretude do codigo '
 'gerado. Celula "UML existente -> LLM -> codigo" da secao 4.3. A questao pendente sobre OCL nao altera o '
 'desfecho, pois aqui a OCL esta na entrada, nao na saida. ',
 'DECISAO: excluido em B3 por E7. Nao satisfaz I5.'),

'985_SCOPUS':('PASSOU','EVIDENCIA=EXPLICITA',
 'EVIDENCIA: examina o papel de tres ferramentas de IA (GitHub Copilot, ChatGPT e BlackBoxAI) no apoio a '
 'arquitetos durante a fase de projeto, avaliando "how closely the generated outputs adhere to established '
 'architectural principles". Situa como artefatos tipicos do arquiteto os diagramas UML, de classes, de '
 'sequencia, de casos de uso e de estados. Analisa desvios, explora como prompts refinados e contexto '
 'adicional melhoram a acuracia, e inclui comparacao entre ferramentas. ',
 'DISCUSSAO: B1 saida sao diagramas UML com quatro tipos nomeados. B2 origem sao assistentes generativos. B3 '
 'direcao e do contexto de projeto para o diagrama. B4 entrada e contexto textual fornecido em prompt. '
 'Nenhum portao exclui. A aderencia a principios arquiteturais estabelecidos e uma forma de adequacao '
 'pragmatica prevista em I6, e a analise de desvios com comparacao entre tres ferramentas produz evidencia '
 'extraivel por ferramenta. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=EXPLICITA. Verificar no texto completo a operacionalizacao de '
 '"principios arquiteturais estabelecidos", que pode ser rubrica qualitativa e nao metrica.'),

'986_SCOPUS':('PASSOU','EVIDENCIA=A_VERIFICAR',
 'EVIDENCIA: explora o uso de aprendizado profundo, em particular LLMs, para automatizar a extracao de '
 'diagramas de classes UML a partir de descricoes textuais. Revisa abordagens existentes, linguisticas e '
 'estatisticas, e propoe novo metodo baseado em modelos de aprendizado profundo "to improve accuracy and '
 'flexibility compared to current extraction tools". O titulo comeca por "Towards an Approach", indicando '
 'trabalho em curso. ',
 'DISCUSSAO: B1 saida e diagrama de classes UML. B2 origem: o resumo diz "deep learning techniques, more '
 'specifically Large Language Models (LLMs)", nomeando a familia exigida por I2, o que afasta a RF-01 '
 'apesar do verbo "extracting" no titulo; nao ha mencao a NER, tagger ou classificador. B3 direcao e '
 'descricao textual para UML. B4 entrada e especificacao textual. Nenhum portao exclui. A acuracia e '
 'declarada como objetivo de melhoria, mas nao ha resultado, gabarito nem instrumento no resumo, e a '
 'formulacao "propose a new method" sugere proposta ainda sem avaliacao empirica consolidada. Pela regra de '
 'ouro 2 isso nao exclui nesta etapa e E11 e proibido em titulo e resumo. ',
 'DECISAO: retido no Portao B; flag EVIDENCIA=A_VERIFICAR. Candidato a E11 na fase de texto completo se '
 'confirmar-se como artigo de posicao sem avaliacao.'),
}
assert len(D)==17, len(D)

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
assert n==17, n
with open(CSV,'w',newline='',encoding='utf-8') as fh:
    csv.writer(fh).writerows(rows)

grp={}
for k,v in D.items(): grp.setdefault(v[0],[]).append(k)
NOTA=('Oitavo e ultimo lote da triagem do Portao B sobre os registros que mencionam UML em titulo ou resumo '
 '(indices 168 a 184 da ordem de leitura). 17 registros decididos: 8 retidos, 3 B1_E7, 3 B3_E7, 1 B3_E8, '
 '2 B4_E9. Encerra-se com isto a leitura da lista ordenada de 185 registros com mencao a UML. '
 'Padroes confirmados: (a) UML na entrada com codigo como produto sai em B3_E7 (966 UML2Dep, 968 '
 'UML-para-Java com CodeLlama, 984 comparacao LLM contra geradores CGBE), e a distincao em relacao a '
 '934 e 952 e que naqueles o diagrama e sintetizado pelo proprio LLM a partir dos requisitos; (b) UML como '
 'ilustracao do proprio artigo sai em B1_E7 (964), somando-se a 843 e 954; (c) mencao de UML em enumeracao '
 'de artefatos de processo tambem sai em B1_E7 (981); (d) transformacao modelo-para-modelo e engenharia '
 'reversa saem em B4_E9 (971 NetLogo para diagrama de sequencia, 982 transformacao por exemplo com '
 'RDBMS-to-UML, UML-to-Java e SysML-to-AAS). '
 'Decisao de fronteira registrada para o segundo revisor em 974: o produto declarado e metamodelo Ecore e a '
 'PlantUML entra so como visualizacao intermediaria para retorno humano; excluido em B1_E7, mas quem '
 'entenda a renderizacao PlantUML como conteudo UML chegaria a retencao com INCERTO_SAIDA. '
 'O agrupamento de descricao textual de caso de uso chega a quatro registros (871, 837, 923, 975) e '
 'permanece dependente da questao de protocolo pendente. 965 recebe INCERTO_ENTRADA por desenho de ida e '
 'volta: o texto que alimenta o decodificador pode ser derivado de um modelo preexistente. '
 'Registros de nucleo identificados: 983 (comparacao de LLMs abertos e fechados por tecnica de prompting '
 'com avaliacao automatizada e artefatos publicos), 976 (relato seminal sobre deficiencias sintaticas e '
 'semanticas do ChatGPT em modelagem), 970 (comparacao contra extracao humana guiada e nao guiada) e 985.')
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
print('flags:',dict(sorted(Counter(f for r in rows[1:] if r[i['gate_b_outcome']]=='PASSOU' for f in r[i['gate_c_flags']].split(';') if f).items())))
