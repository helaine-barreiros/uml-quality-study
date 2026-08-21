#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica ao CSV mestre as decisoes do bloco SEM_RESUMO com texto completo (17 registros).

Reenquadramento: SEM_RESUMO nao e trabalho de Portao C. E Portao B adiado --
o registro chegou ao Portao C sem que B pudesse ser decidido por falta de resumo.
Com o texto em maos, o Portao B se decide agora, e so o que sobreviver segue para C.

Ordem dos filtros preservada (v1 executada): B1 saida -> B2 origem -> B3 direcao
-> B4 papel. Regra de ouro 3 (um so criterio primario) e regra de ouro 5 (nao
sobrecarregar E6): quando nao ha UML na saida gerada, o criterio primario e E7,
mesmo que o registro tambem falhasse em B4.
"""
import csv, shutil, sys

CSV = 'custom_automated_search_collection.csv'
DT = '2026-08-17T00:00:00-03:00'
REV = 'Helaine Barreiros'

CAB = ('=== REVISAO COM TEXTO COMPLETO (2026-08-17) — resolucao do sinalizador '
       'SEM_RESUMO ===\n')

M_G1 = ('METODO: o registro havia chegado ao Portao C com o sinalizador SEM_RESUMO, '
        'isto e, sem resumo no CSV nao foi possivel decidir o Portao B por titulo e '
        'palavras-chave. Com o PDF recuperado, o texto integral foi extraido '
        '(pdftotext) e varrido por tres familias de expressoes: ocorrencia de UML '
        '(\\bUML\\b|Unified Modeling Language|PlantUML), tipos de diagrama '
        '(class/use case/sequence/activity/state machine/component/deployment/object '
        'diagram) e presenca de modelo de linguagem (LLM|GPT|ChatGPT|Claude|Gemini|'
        'Llama|Mistral|Qwen|DeepSeek|large language model). As sentencas de contexto '
        'foram lidas uma a uma. ')

M_G2 = M_G1

def notas(metodo, evidencia, discussao, decisao):
    return (metodo + 'EVIDENCIA: ' + evidencia + ' DISCUSSAO: ' + discussao +
            ' DECISAO: ' + decisao)

# ---------------------------------------------------------------- grupo 1
# Nenhuma ocorrencia de modelo de linguagem no texto integral. A UML que aparece
# (quando aparece) e desenhada pelos proprios autores como notacao de exposicao.
D_G1 = ('nenhuma UML e produzida ou alterada por modelo de linguagem, porque nao ha '
        'modelo de linguagem no estudo. O registro falharia tanto em B1 (nao ha UML '
        'na saida gerada) quanto em B4 (nao ha papel de LLM a avaliar). Pela ordem '
        'dos filtros, B1 vem antes de B4, e pela regra de ouro 3 registra-se um so '
        'criterio primario. Nao se usa E6 aqui: E6 e para estudo que tem LLM cujo '
        'papel nao qualifica, e nao para estudo que nao tem LLM nenhum '
        '(regra de ouro 5).')
DEC_G1 = 'EXCLUIDO por E7 no Portao B, filtro B1. Sinalizador SEM_RESUMO resolvido.'

G1 = {
 '307_ACM': 'a busca por LLM no texto integral retorna zero ocorrencias. A UML citada e '
   'ferramenta de exposicao dos proprios autores: "UML Component modeling lends itself to '
   'visually developing prototypical component-based models"; "UML component diagrams can be '
   'developed using professional tools such as Astah (Astah 2024)"; "Figure 6 illustrates the '
   'UML class diagrams for some of the parts of the PVM framework". O objeto do estudo e a '
   'construcao de modelos modulares hierarquicos em arcaboucos de simulacao.',
 '383_ACM': 'zero ocorrencias de LLM no texto integral. Duas mencoes a UML, ambas descritivas '
   'do proprio artefato dos autores: "A Unified Modeling Language (UML) class diagram model is '
   'used to describe the main elements of the model" e "Data are modeled using UML class '
   'diagrams, in which each class represents a table". O objeto e gemeos digitais: '
   'caracteristicas, modelos e servicos.',
 '390_ACM': 'zero ocorrencias de LLM no texto integral. As mesmas duas sentencas de 383_ACM '
   '("A Unified Modeling Language (UML) class diagram model is used to describe the main '
   'elements of the model"; "Data are modeled using UML class diagrams, in which each class '
   'represents a table") — os dois registros sao textos dos mesmos autores sobre gemeos '
   'digitais, e a UML e notacao de exposicao em ambos.',
 '386_ACM': 'zero ocorrencias de LLM no texto integral, contra nove sentencas com UML, todas '
   'de modelagem manual conforme IEC 62264: "The corresponding attributes are depicted in the '
   'following UML Class diagram; Figure 2" e "ISO have also recommended to base the modelling '
   'approach of the DT on general standard such as IEC 62264, which consists of using the '
   'robust UML formalism". O diagrama e produzido pelos autores.',
 '397_ACM': 'zero ocorrencias de LLM e zero ocorrencias do termo UML no texto integral. O unico '
   'sinal de modelagem comportamental e uma maquina de estados finitos que nao e apresentada '
   'como UML: "we model the EVs as a finite-state machine having the states that an EV is '
   'either driving or parked at home" e "Figure 3: Modeling of the EVs inside the digital twin '
   'as finite-state machine". O objeto e o impacto de veiculos eletricos em sistemas locais de '
   'energia.',
 '422_ACM': 'zero ocorrencias de LLM no texto integral, contra onze sentencas com UML, todas de '
   'uso expositivo pelos autores: "Section 5 uses Unified Modeling Language (UML) notation, '
   'which is a visual modeling language frequently employed in IS/IT for the design of software '
   'artifacts" e "The UML interaction diagram in Figure 2 (a) illustrates the interaction '
   'between the environment actor (healthcare system) and the decisionmaker actor". O objeto e '
   'um modelo de maturidade para gemeos digitais em saude.',
 '427_ACM': 'zero ocorrencias de LLM e zero ocorrencias do termo UML no texto integral. Ha '
   'diagramas comportamentais, mas construidos pelos autores em ferramenta de simulacao: "A '
   'sequence diagram is shown in Figure 4 to depict the dynamic behavior of the operational '
   'controller" e "The controller agents\u2019 behavior is designed using AnyLogic\u2122 finite '
   'state machines".',
 '439_ACM': 'zero ocorrencias de LLM no texto integral, contra vinte e tres sentencas com UML. '
   'Todas descrevem transformacao simbolica entre formalismos, sem modelo de linguagem: "the '
   'OML Adapter [8] provides a transformation basis from OWL ontologies to OML and UML models"; '
   '"the OML adapter only provides round-trip transformation between OML and UML"; "the first '
   'stage (OWL to UML profile conversion) only needs to be performed once, as long as the '
   'ontology concepts do not changed". A geracao e determinada por regras, nao por LLM.',
}

# ---------------------------------------------------------------- grupo 2
# Ha modelo de linguagem, mas a UML no texto e mencao lateral: pano de fundo,
# trabalho relacionado, titulo de referencia ou figura desenhada pelos autores.
D_G2 = ('ha modelo de linguagem no estudo, e portanto B4 seria uma pergunta legitima. '
        'Mas o filtro B1 vem antes e ja e decisivo: o resultado gerado pelo modelo nao '
        'inclui conteudo UML. A UML aparece no texto como pano de fundo, trabalho '
        'relacionado, titulo de referencia ou figura de exposicao dos autores — nunca '
        'como artefato produzido pelo modelo. Nao ha instancia de geracao de UML a '
        'observar, e portanto nao ha dissonancia sintatico-semantica a extrair. '
        'Registra-se E7 como criterio primario, nao E6 (regra de ouro 5).')
DEC_G2 = 'EXCLUIDO por E7 no Portao B, filtro B1. Sinalizador SEM_RESUMO resolvido.'

G2 = {
 '075_ACM': 'seis sentencas com LLM e zero ocorrencias do termo UML. Ha diagramas '
   'comportamentais, mas sao a documentacao da arquitetura construida pelos proprios autores: '
   '"Figure 3: System Deployment Diagram" e "Figure 4: State Machine Diagram", esta ultima '
   'descrevendo o agente pedagogico dos autores ("the state machine automatically jumps to the '
   'Refinement-Reconstruction state"). O objeto e um agente de ensino de design thinking; a '
   'saida do LLM e conteudo pedagogico, nao modelo.',
 '100_ACM': 'cento e cinco sentencas com LLM e uma unica com UML, e essa unica e especulativa '
   'sobre o futuro da industria de ferramentas: "that history suggests that features such as '
   '\u201cUML\u2192code\u201d generators will do the same". O objeto e a suscetibilidade de '
   'exercicios de laboratorio introdutorio a resolucao por LLM.',
 '324_ACM': 'cinquenta e quatro sentencas com LLM e duas com UML, ambas de enquadramento: '
   '"Although modeling languages (e.g., UML, SysML) can be familiar tools for model '
   'development, their steep learning curve for participants also presents an obstacle" e '
   '"Since schema (e.g., UML, causal maps) often depict concepts and their relations, the '
   'corresponding NLG task is known as graph-to-text". A UML e citada como classe de linguagem, '
   'nao como saida gerada. O objeto e o uso de modelos GPT em simulacao.',
 '099_ACM': 'cento e oito sentencas com LLM e duas mencoes a diagrama, ambas em trabalho '
   'relacionado: "[11] employed ChatGPT as a sequence diagram generator from the provided '
   'natural-language requirements" e o titulo de uma referencia, "Model Generation with LLMs: '
   'From Requirements to UML Sequence Diagrams". O que o cfgLLM gera sao artefatos de '
   'requisitos, nao UML. Observacao para a busca por referencias: a referencia citada e '
   'candidata legitima ao corpus e deve ser conferida no snowballing.',
 '399_ACM': 'trinta e sete sentencas com LLM e uma unica mencao a diagrama, dentro do titulo '
   'de uma referencia: "Automatic Test Data Generation Using the Activity Diagram and '
   'Search-Based Technique". A unica sentenca com UML descreve trabalho de terceiros ("They '
   'would take UML model diagrams and convert them into an XML format"), e ainda assim na '
   'direcao invertida, com UML como entrada. O objeto e metodologia de teste para modelos DEVS '
   'em Cadmium.',
}

# ---------------------------------------------------------------- grupo 3
G3_NOTAS = {
 '113_ACM': dict(
   flags='',
   metodo=('METODO: sinalizador SEM_RESUMO resolvido por leitura do texto integral extraido do '
           'PDF, aplicando o Portao B na ordem B1 saida, B2 origem, B3 direcao, B4 papel, e em '
           'seguida o Portao C. '),
   evidencia=('nove sentencas com UML e setenta com LLM. O desenho experimental esta explicito: '
              '"The prompt was provided to three large language models\u2014ChatGPT, Gemini, and '
              'Perplexity\u2014resulting in the solutions presented in Code Snippets 4, 5, and 6, '
              'with corresponding UML representations". As figuras sao nomeadas por variante '
              '("Comparison of UML generated for ChatGPT variant"; "The 3-level UML diagram is '
              'generated by ChatGPT variant and 2-level UML diagram is generated by Gemini '
              'variant") e ha referencia de comparacao humana: "manually constructed UML diagrams '
              'are used to compare and interpret the resulting designs".'),
   discussao=('B1 satisfeito: UML esta na saida gerada. B2 satisfeito: os diagramas sao '
              'produzidos pelos modelos, nao editados a partir de um modelo preexistente. B3 '
              'satisfeito: a entrada e um enunciado textual (prompt). B4 satisfeito: os tres '
              'modelos decidem o conteudo do diagrama, sem regra simbolica determinando a '
              'estrutura (RF-02). B5 satisfeito: os diagramas UML sao apresentados e comparados '
              'separadamente do codigo. No Portao C, C1: a instancia de geracao e identificavel '
              'por variante de modelo, o que permite atribuir o resultado ao artefato UML. Nos '
              'eixos de extracao: L presente (conformidade da representacao gerada), D presente '
              'com referencia de comparacao do tipo modelo_de_referencia (os diagramas '
              'construidos manualmente), U por verificar.'),
   decisao=('ELEGIVEL. Passa o Portao C sem ressalva. Sinalizador SEM_RESUMO removido; segue '
            'para extracao.')),
 '170_ACM': dict(
   flags='CANDIDATO_E12',
   metodo=('METODO: sinalizador SEM_RESUMO resolvido por leitura do texto integral extraido do '
           'PDF, aplicando o Portao B e em seguida o Portao C. '),
   evidencia=('quinze sentencas com LLM e duas com UML, ambas afirmando geracao: "This phase '
              'includes code generation and creating Unified Modeling Language (UML) diagrams to '
              'illustrate the system\u2019s architecture and component interactions" e '
              '"Additionally, ChatGPT effectively supports software design documentation, '
              'generating PlantUML and various UML diagrams, highlighting its potential beyond '
              'code generation".'),
   discussao=('o Portao B esta satisfeito: ha UML na saida (B1), produzida pelo modelo (B2), a '
              'partir de entrada textual (B3), com o modelo decidindo o conteudo (B4). O ponto '
              'em aberto e o filtro C1 e o atributo de atribuicao do resultado: a UML e um '
              'artefato entre varios de um fluxo de orquestracao que inclui codigo, documentacao '
              'e avaliacao de seguranca, e a frase "effectively supports" e um juizo agregado '
              'sobre o fluxo, nao uma medida atribuivel ao diagrama. Se o texto nao isolar uma '
              'instancia de geracao de UML com resultado proprio, o registro sai por E12; se '
              'isolar, entra com o atributo atribuicao do resultado = agregado_com_outros_'
              'artefatos. Nao se decide agora: a regra de ouro 1 manda a incerteza reter.'),
   decisao=('RETIDO com CANDIDATO_E12. Sinalizador SEM_RESUMO removido. A decisao de C1 fica '
            'para o bloco de candidatos a E12.')),
 '108_ACM': dict(
   flags='CANDIDATO_E12',
   metodo=('METODO: sinalizador SEM_RESUMO resolvido por leitura do texto integral extraido do '
           'PDF, aplicando o Portao B e em seguida o Portao C. '),
   evidencia=('noventa e cinco sentencas com LLM e cinco com UML. As decisivas sao achados de '
              'avaliacao: "As of now, LLMs couldn\u2019t generate UML class, sequence, component, '
              'deployment, and usecase diagrams"; "For instance, LLMs tend to draw UML diagrams '
              'in a textual format"; e a identificacao das disciplinas afetadas, "software '
              'engineering courses with UML".'),
   discussao=('o estudo relata desempenho de LLMs na producao de diagramas UML, ou seja, mede '
              'qualidade do artefato gerado — e mede sem usar o vocabulario canonico de '
              'qualidade. Pela regra de ouro 2, a ausencia de vocabulario de qualidade nunca '
              'exclui: descartar aqui seria selecionar pela variavel dependente, exatamente o '
              'vies que o racional do estudo proibe. A observacao sobre formato textual toca o '
              'eixo L (relacao modelo-linguagem) e a afirmacao de incapacidade toca o eixo D. O '
              'que esta em aberto e C1: se o texto nao individualiza a instancia de geracao '
              '(qual modelo, qual entrada, qual diagrama), o resultado nao e atribuivel e o '
              'registro sai por E12. Registre-se que este registro so chegou vivo ate aqui por '
              'causa da decisao alpha: sob o E11 anterior ele teria morrido por falta de '
              'vocabulario de qualidade.'),
   decisao=('RETIDO com CANDIDATO_E12. Sinalizador SEM_RESUMO removido. A decisao de C1 fica '
            'para o bloco de candidatos a E12.')),
 '089_ACM': dict(
   flags='CANDIDATO_E12',
   metodo=('METODO: sinalizador SEM_RESUMO resolvido por leitura do texto integral extraido do '
           'PDF, aplicando o Portao B e em seguida o Portao C. '),
   evidencia=('vinte sentencas com LLM; o termo UML nao aparece, mas os tipos de diagrama '
              'aparecem cinco vezes, e a evidencia e substantiva: "This is likely due to the '
              'limitations of most AI tools in generating syntactically correct diagrams, such '
              'as class or sequence diagrams, which are heavily used in this phase"; "Diagram '
              'generation (n=2) in this phase attempts to generate class diagrams that are '
              'simple in design and complexity"; "Experiences with AI tools were mostly negative '
              'when it came to diagrams, such as class or sequence diagrams"; e a lista de '
              'artefatos exigidos aos times, "class diagrams, BPMN diagrams, sequence diagrams '
              'and state diagrams".'),
   discussao=('e um estudo de uso em projetos estudantis de desenvolvimento. A frase sobre '
              '"syntactically correct diagrams" e uma afirmacao sobre o eixo L, e o relato de '
              'experiencia negativa e evidencia do eixo U — o eixo pragmatico, o menos coberto '
              'segundo o racional do estudo. A ausencia do termo UML nao exclui: os tipos '
              'nomeados (class, sequence, state) sao construtos UML. O que esta em aberto e C1: '
              'o relato e agregado sobre a experiencia dos times, e pode nao haver instancia de '
              'geracao individualizavel. Como 108_ACM, este registro so sobrevive por causa da '
              'decisao alpha e da retirada de E10: sob as regras anteriores ele sairia duas '
              'vezes.'),
   decisao=('RETIDO com CANDIDATO_E12. Sinalizador SEM_RESUMO removido. A decisao de C1 fica '
            'para o bloco de candidatos a E12.')),
}


def main(apply=False):
    with open(CSV, newline='', encoding='utf-8') as f:
        rd = csv.DictReader(f)
        campos = rd.fieldnames
        linhas = list(rd)
    idx = {r['logical_id']: r for r in linhas}

    tocados = []
    for lid, ev in list(G1.items()) + list(G2.items()):
        r = idx[lid]
        d, dec = (D_G1, DEC_G1) if lid in G1 else (D_G2, DEC_G2)
        bloco = CAB + notas(M_G1, ev, d, dec)
        r['gate_b_notes'] = (r['gate_b_notes'] + '\n\n' + bloco).strip()
        r['gate_b_outcome'] = 'B1_E7'
        r['gate_b_reviewer'] = REV
        r['gate_b_datetime'] = DT
        r['exclusion_criteria'] = 'E7'
        r['excluded'] = 'true'
        r['gate_c_flags'] = ''
        r['gate_c_notes'] = ''
        r['gate_c_reviewer'] = ''
        r['gate_c_datetime'] = ''
        tocados.append((lid, 'E7', r['gate_b_outcome']))

    for lid, n in G3_NOTAS.items():
        r = idx[lid]
        bloco = CAB + notas(n['metodo'], n['evidencia'], n['discussao'], n['decisao'])
        r['gate_c_notes'] = (r['gate_c_notes'] + '\n\n' + bloco).strip()
        r['gate_c_flags'] = n['flags']
        r['gate_c_reviewer'] = REV
        r['gate_c_datetime'] = DT
        tocados.append((lid, 'RETIDO', n['flags'] or 'ELEGIVEL'))

    if apply:
        with open(CSV, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(linhas)

    for t in tocados:
        print('%-10s %-8s %s' % t)
    print('---')
    print('total tocados', len(tocados))
    excl = sum(1 for r in linhas if r['excluded'] == 'true')
    print('corpus %d | excluidos %d | retidos %d' % (len(linhas), excl, len(linhas) - excl))


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
