# -*- coding: utf-8 -*-
"""Portao C, bloco C1 (14 candidatos) + duas familias de publicacao.

Aprovado pela usuaria em 2026-08-17: "concordo com os 14 e com as duas familias,
aplique".

Mudanca de esquema: cria a coluna gate_c_outcome, normativa em
screening_manual_v2.md linha 460 (ELEGIVEL / C1_E12 / NAO_RECUPERADO / vazio),
inserida antes de gate_c_flags para espelhar o padrao dos Portoes A e B.
"""
import csv, os

CSV = '/home/helaine-barreiros/Development/doutorado-workspace/estudo_sistematico/uml-quality-study/search/automated/custom_automated_search_collection.csv'
DT = '2026-08-17 21:30'
REV = 'HB'

CAB = ('DECISAO DO PORTAO C, subportao C1 (ha instancia de geracao identificavel?), '
       'em %s. ' % DT)
MET = ('METODO: o registro chegou ao C1 com sinalizador de candidato aberto na triagem '
       'por titulo e resumo. Com o texto completo em maos, a extracao (pdftotext) foi '
       'varrida por familias de notacao, com UML e PlantUML em expressoes regulares '
       'separadas para nao repetir o defeito de \\bUML\\b, cruzadas com verbos de geracao. '
       'O teste do C1 e nominal e nao vocabular: exige que se possa nomear o modelo, a '
       'entrada e o artefato UML produzido, e que algum resultado relatado seja atribuivel '
       'a essa instancia. Ausencia de vocabulario canonico de qualidade nunca exclui '
       '(regra de ouro 2). ')


def bloco(ev, disc, dec):
    return CAB + MET + 'EVIDENCIA: ' + ev + ' DISCUSSAO: ' + disc + ' DECISAO: ' + dec


# ---------------------------------------------------------------- ELEGIVEIS
ELE = {
 '856_SCOPUS': bloco(
  'o texto declara a instancia por escrito: "Each SRS was used to generate UML Class '
  'Diagrams, and the resulting artifacts were compared according to the following three '
  'dimensions" e "UML diagrams are generated in PlantUML syntax". As figuras sao '
  'individualizadas por modelo e por passe: "Figure 3: Generated UML Class Diagram '
  '(Bigger LLM, First Pass)", "Figure 4: Generated UML Class Diagram (Bigger LLM, Third '
  'Pass)" e "Figure 5: Generated UML Class Diagram (Smaller LLM)".',
  'entrada nomeada (SRS), modelo nomeado e contrastado em dois portes, artefato nomeado '
  '(diagrama de classes em PlantUML) e resultado atribuivel a cada combinacao de modelo e '
  'passe. O sinalizador CANDIDATO_E10 nasceu do titulo, que fala em artefatos multimodais '
  'sincronizados; a leitura mostra que o conteudo UML e destacavel e avaliado em separado, '
  'em tres dimensoes proprias.',
  'ELEGIVEL. Retirado o CANDIDATO_E10. O contraste entre portes de modelo e entre passes '
  'e material de primeira ordem para o eixo L da extracao.'),

 '918_SCOPUS': bloco(
  'ha secoes de avaliacao por diagrama, nomeadas: "Evaluation of the Sequence Diagram" e '
  '"Evaluation of the UML/SysML Activity Diagram". Um achado de qualidade e enunciado em '
  'termos do proprio artefato: "they lacked the tool-specific elements that are typical of '
  'UML". O desenho contrasta Original Cases e Paraphrased Cases.',
  'a manipulacao de parafrase e uma variacao controlada da entrada textual com a mesma '
  'tarefa, o que torna o resultado atribuivel a instancia e nao ao acaso da redacao. O '
  'achado citado e exatamente a dissonancia sintatico-semantica que a revisao persegue: '
  'artefato renderizavel e conforme, porem carente dos elementos que o dominio da notacao '
  'exige. O CANDIDATO_E10 caiu porque, embora o titulo una UML e SysML, o texto avalia '
  'cada diagrama em secao propria.',
  'ELEGIVEL. Retirado o CANDIDATO_E10. Registrar na extracao a rotulagem hibrida '
  '"UML/SysML" como vocabulario nativo, sem normalizar.'),

 '089_ACM': bloco(
  'as instancias sao contadas: "Diagram generation (n=2)" e "creating diagrams and charts '
  '(n=5)". Os desfechos sao atribuidos a elas: "both mentions were accompanied by '
  'complaints that the diagrams were not correct or detailed enough" e "one student '
  'specifically mentioned the lack of content in the generated diagram".',
  'e o caso limitrofe dos tres. A instancia existe e o resultado lhe e atribuido, mas a '
  'atribuicao e autorrelatada por estudante em projeto de disciplina, sem que o artefato '
  'gerado tenha sido inspecionado pelos autores. Isso e uma limitacao de forca da '
  'evidencia, nao ausencia de instancia, e o C1 pergunta pela existencia da instancia. '
  'Excluir aqui seria filtrar pela qualidade da medida, prima da regra de ouro 6. Registre-se '
  'ainda que este registro so chegou vivo ate aqui por causa da emenda A004: sob o E11 '
  'antigo teria morrido por medir qualidade sem o vocabulario canonico, e sob o E10 antigo '
  'teria morrido pela agregacao de artefatos.',
  'ELEGIVEL com atribuicao fraca. Retirado o CANDIDATO_E12. Anotar no campo de atribuicao '
  'do resultado que a evidencia e autorrelato, para que a extracao pese o registro '
  'adequadamente e para que ele nao contamine estimativas de incidencia.'),
}

# ---------------------------------------------------------------- E12 no C1
E12 = {
 '108_ACM': bloco(
  'as ocorrencias de UML sao itens de marcador dentro de uma tabela de observacoes de sala '
  'de aula. Nenhuma sentenca nomeia modelo, entrada e artefato ao mesmo tempo, e nao ha '
  'resultado enunciado sobre o diagrama produzido.',
  'sem modelo, entrada e artefato nomeaveis, nao ha instancia a que atribuir qualquer '
  'resultado, e portanto nao ha unidade de analise para a extracao de construto. Assim '
  'como 089_ACM, este registro so sobreviveu ate o C1 por causa da A004; a diferenca entre '
  'os dois nao esta no vocabulario e sim na existencia da instancia.',
  'EXCLUIR por E12 no C1. Exclusao nao destrutiva: os desfechos dos Portoes A e B '
  'permanecem, pois estavam corretos diante do que titulo e resumo ofereciam.'),

 '170_ACM': bloco(
  'a unica passagem relevante e uma assercao agregada: "ChatGPT effectively supports '
  'software design documentation, generating PlantUML and various UML diagrams". A varredura '
  'por sentencas de resultado retornou zero ocorrencias.',
  'a frase e uma afirmacao de capacidade em bloco, sem execucao relatada, sem entrada '
  'identificada e sem artefato exibido ou avaliado. "various UML diagrams" e precisamente '
  'a formulacao que impede individualizar a instancia. Nao ha o que extrair.',
  'EXCLUIR por E12 no C1. Exclusao nao destrutiva.'),

 '221_ACM': bloco(
  'o texto descreve um plano de trabalho sobre explicabilidade e rastreabilidade em '
  'modelagem de dominio assistida por IA. Nao ha execucao relatada nem artefato produzido.',
  'chegou a ser cogitado o E1, por ser trabalho de perspectiva, mas a lista do E1 no manual '
  'v2 e fechada e nao inclui vision paper nem simposio doutoral. O criterio correto e o '
  'primeiro que efetivamente falha na ordem do fluxo, e ele e o C1: sem instancia executada, '
  'nao ha geracao identificavel.',
  'EXCLUIR por E12 no C1, e nao por E1. Regra de ouro 3: um unico criterio primario, o '
  'primeiro que falha na ordem dos portoes.'),

 '788_SCOPUS': bloco(
  'o diagrama que recebe pontuacao no estudo e o produzido pelo estudante, com ou sem apoio '
  'da ferramenta. Nao ha saida do modelo isolada e avaliada.',
  'a unidade de analise e o desempenho do estudante, e o modelo entra como tratamento. O '
  'resultado nao e atribuivel a uma instancia de geracao, e sim a uma condicao experimental '
  'que mistura a contribuicao do modelo com a do estudante. Isso e exatamente o que o E12 '
  'nomeia: o resultado UML nao se separa das demais saidas da mesma execucao.',
  'EXCLUIR por E12 no C1. Bom candidato a pilha de background pelo desenho experimental.'),

 '845_SCOPUS': bloco(
  'ha uma unica mencao parentetica a UML no corpo do texto, sem instancia associada.',
  'o trabalho e sobre sistemas multiagente aumentados por LLM, e a UML aparece como '
  'ilustracao de notacao possivel. Nenhuma execucao, artefato ou resultado.',
  'EXCLUIR por E12 no C1.'),

 '854_SCOPUS': bloco(
  'a UML aparece confinada ao Grupo D entre dez grupos de projeto, sem nenhum resultado '
  'atribuivel ao conteudo UML.',
  'o estudo trata de dados sinteticos de pesquisa em projetos de pos-graduacao; o Grupo D '
  'e um caso entre dez e nao tem medida propria. Sem resultado atribuivel, nao ha instancia '
  'no sentido do C1.',
  'EXCLUIR por E12 no C1.'),

 '890_SCOPUS': bloco(
  'nao ha avaliacao do artefato. Alem disso ha inconsistencia interna de atribuicao: o '
  'corpo do texto diz que o diagrama foi "created by ChatGPT" e a legenda da figura diz '
  '"generated by CoPilot".',
  'a inconsistencia e por si so fatal ao C1, que exige que se possa nomear o modelo. Sem '
  'saber qual modelo produziu o artefato, nenhum resultado poderia ser atribuido a uma '
  'instancia, mesmo que houvesse avaliacao, e nao ha.',
  'EXCLUIR por E12 no C1. Anotada a inconsistencia por interesse metodologico: ela ilustra '
  'a fragilidade de atribuicao que motivou desdobrar o antigo E10 em E12 mais o atributo '
  'de atribuicao do resultado.'),

 '935_SCOPUS': bloco(
  'os proprios autores declaram: "The paper focuses on the tool design and workflow rather '
  'than on a full empirical evaluation".',
  'e uma descricao de arquitetura de ferramenta baseada em agentes modulares. Ha pipeline, '
  'ha artefatos previstos, mas nao ha execucao relatada com resultado atribuivel. A '
  'declaracao vem dos autores, o que torna a evidencia limpida.',
  'EXCLUIR por E12 no C1. Retirado o CANDIDATO_E10.'),

 '787_SCOPUS': bloco(
  'as ferramentas comparadas sao Lucidchart, Eraser.io, UIzard e Mermaid.js combinado com '
  'Bing AI. A unica medida e "subjective accuracy", aplicada de forma agregada sobre '
  'diagramas UML e telas de interface de um mesmo aplicativo exemplar. O texto caracteriza '
  'o processo como "template-driven creation".',
  'duas razoes convergem. Primeira, a medida e unica e cobre UML e UI juntos, de modo que '
  'nenhum resultado e atribuivel ao conteudo UML isoladamente. Segunda, "template-driven '
  'creation" descreve preenchimento de gabarito, no qual as regras simbolicas determinam o '
  'conteudo do modelo (RF-02), o que enfraquece a instancia mesmo onde ela pareceria '
  'existir. O criterio primario permanece o C1 porque e ele que falha primeiro na ordem do '
  'fluxo entre os que se aplicam a este registro.',
  'EXCLUIR por E12 no C1. Retirado o CANDIDATO_E10. Ver tambem o vinculo de familia '
  'FAM-C-003 registrado a seguir.'),
}

# ---------------------------------------------------------------- E7b no B5
E7B = {
 '797_SCOPUS': (
  'DECISAO TARDIA DO PORTAO B, subportao B5 (o conteudo UML e separavel de outras '
  'notacoes?), tomada em %s durante a leitura do bloco C1. ' % DT
  + MET +
  'EVIDENCIA: o que o modelo gera sao comandos de uma linguagem intermediaria, e as '
  'metricas incidem sobre ela e nao sobre UML: "Syntactic Validity Rate (SVR): The '
  'percentage of generated CIM-DSL commands that successfully parse against the EBNF '
  'grammar". O mapeamento da DSL para notacao e simbolico e predominantemente BPMN: '
  '"DEFINE_PROCESS instantiates a BPMN Collaboration (Pool), ADD_ACTOR generates a UML '
  'Actor or BPMN Lane, and ADD_STEP creates a BPMN Task". '
  'DISCUSSAO: o registro entrou no C1 como CANDIDATO_E10, mas falha antes, no B5. O '
  'artefato avaliado e a DSL; a UML surge apenas como um dos alvos de uma traducao '
  'deterministica posterior, feita por regras e nao pelo modelo. Pela RF-02, quando as '
  'regras simbolicas determinam o conteudo do modelo, a contribuicao do LLM nao e '
  'constitutiva do artefato UML. E pelo criterio de separabilidade, "a UML Actor or BPMN '
  'Lane" e a formulacao que mostra a ausencia de contribuicao UML destacavel. Regra de ouro '
  '3 manda registrar o primeiro criterio que falha na ordem dos portoes, que aqui e o B5 e '
  'nao o C1. '
  'DECISAO: EXCLUIR por E7b no B5. Retirado o CANDIDATO_E10. Exclusao nao destrutiva.'),
}

# ------------------------------------------------- familias de publicacao (E3)
FAM_CAB = ('EXCLUSAO TARDIA NO PORTAO C em %s, criterio E3 (membro menos completo de '
           'familia de publicacao). ' % DT)

FAM_A_MET = (
 'METODO: durante a leitura integral do bloco C1, a coincidencia de autoria, abordagem e '
 'conjunto de tarefas entre tres registros levou a comparacao direta dos textos completos, '
 'buscando declaracao explicita de derivacao. ')
FAM_A_EV = (
 'EVIDENCIA: 027_ACM (TOSEM 2026, DOI 10.1145/3744920) declara literalmente: "Our proposed '
 'approach builds upon our prior work on domain model completion utilizing LLMs [11]." A '
 'referencia [11] e 623_IEEE (ICSE-NIER 2023, DOI 10.1109/ICSE-NIER58687.2023.00008). '
 '842_SCOPUS (MODELS 2024, DOI 10.1145/3652620.3676877, Chaaben como autor unico) reporta '
 'estagio intermediario da mesma linha, com o mesmo grupo de autores (Chaaben, Burgueno, '
 'Sahraoui). ')
FAM_A_DISC = (
 'DISCUSSAO: o protocolo define E3 como duplicata ou membro menos completo de familia de '
 'publicacao. 027_ACM e o membro mais completo: e o artigo de periodico que consolida a '
 'linha e assume por escrito a derivacao dos anteriores. A consequencia e desconfortavel e '
 'precisa ficar registrada: 623_IEEE havia sido retido como registro elegivel no lote '
 'anterior, aprovado em 2026-08-17, e esta decisao o reverte. A reversao e correta porque o '
 'pre-passe D e de nivel de corpus e precede a analise de elegibilidade, e porque manter os '
 'tres contaria o mesmo estudo tres vezes em qualquer sintese de incidencia. ')

FAM_B_MET = (
 'METODO: comparacao de autoria, titulo, ferramentas avaliadas e desenho entre os dois '
 'registros, apos a leitura integral de 787_SCOPUS no bloco C1. ')
FAM_B_EV = (
 'EVIDENCIA: mesma equipe (Roy, Horielko, Omojokun) e mesmo objeto, a comparacao de '
 'ferramentas de IA para educacao em engenharia de software. 051_ACM e o poster de uma '
 'pagina em ICER 2025 Volume 2 (DOI 10.1145/3702653.3744328); 787_SCOPUS e o artigo '
 'completo em SIGCSE TS 2026 (DOI 10.1145/3770762.3772551). ')
FAM_B_DISC = (
 'DISCUSSAO: 051_ACM havia sido excluido neste mesmo dia por E1, como resumo de uma pagina, '
 'e a leitura estava correta. Mas sob a emenda A004 o pre-passe D precede o Portao A, de '
 'modo que o criterio primario correto e E3 e nao E1. A recodificacao muda a justificativa e '
 'nao o desfecho: o registro permanece excluido. Registre-se que 787_SCOPUS, o membro mais '
 'completo e portanto o primario da familia, e ele proprio excluido por E12 no C1 nesta '
 'mesma rodada. Isso nao e contradicao: a resolucao de familia e de nivel de corpus e '
 'independe da elegibilidade do primario. ')

FAM = {
 '027_ACM': dict(grupo='FAM-C-002', papel='primario', excl=False, notas=(
   FAM_CAB.replace('EXCLUSAO TARDIA', 'VINCULO DE FAMILIA REGISTRADO').replace(
     ', criterio E3 (membro menos completo de familia de publicacao)',
     ', na condicao de membro MAIS completo e primario do grupo FAM-C-002')
   + FAM_A_MET + FAM_A_EV + FAM_A_DISC +
   'DECISAO: manter 027_ACM retido como primario da familia FAM-C-002. Os membros 623_IEEE '
   'e 842_SCOPUS passam a E3, com desfechos historicos dos Portoes A e B preservados.')),

 '623_IEEE': dict(grupo='FAM-C-002', papel='duplicata', excl=True, notas=(
   FAM_CAB + FAM_A_MET + FAM_A_EV + FAM_A_DISC +
   'DECISAO: EXCLUIR por E3, vinculado a 027_ACM no grupo FAM-C-002. Preservacao de rastro: '
   'este registro era o primario do grupo DUP-A-022, de duplicata exata por DOI com '
   '235_ACM; aquele vinculo continua descrito por extenso nas notas do Portao A de 235_ACM, '
   'que permanece excluido por E3 e nao e afetado. Os desfechos dos Portoes A e B deste '
   'registro sao preservados, pois estavam corretos diante da informacao entao disponivel.')),

 '842_SCOPUS': dict(grupo='FAM-C-002', papel='duplicata', excl=True, notas=(
   FAM_CAB + FAM_A_MET + FAM_A_EV + FAM_A_DISC +
   'DECISAO: EXCLUIR por E3, vinculado a 027_ACM no grupo FAM-C-002. O criterio E3 precede '
   'o C1, de modo que o CANDIDATO_E10 que este registro carregava deixa de ser decidido e e '
   'apenas retirado. Preservacao de rastro: este registro era o primario do grupo '
   'DUP-A-007, de duplicata exata por DOI com 032_ACM; aquele vinculo continua descrito por '
   'extenso nas notas do Portao A de 032_ACM. Desfechos dos Portoes A e B preservados.')),

 '787_SCOPUS': dict(grupo='FAM-C-003', papel='primario', excl=None, notas=(
   'VINCULO DE FAMILIA REGISTRADO em %s, na condicao de membro MAIS completo e primario do '
   'grupo FAM-C-003. ' % DT + FAM_B_MET + FAM_B_EV + FAM_B_DISC +
   'DECISAO: primario de FAM-C-003. A exclusao propria deste registro e por E12 no C1, '
   'registrada acima. Preservacao de rastro: era primario do grupo DUP-A-020, de duplicata '
   'exata por DOI com 210_ACM, vinculo descrito nas notas do Portao A daquele registro.')),

 '051_ACM': dict(grupo='FAM-C-003', papel='duplicata', excl=True, notas=(
   FAM_CAB + FAM_B_MET + FAM_B_EV + FAM_B_DISC +
   'DECISAO: recodificar o criterio primario de E1 para E3, vinculado a 787_SCOPUS no grupo '
   'FAM-C-003. O registro segue excluido. O desfecho historico do Portao A, A2_E1, e '
   'preservado no campo proprio, porque a leitura de uma pagina estava correta; o que muda '
   'e qual criterio governa, dado que o pre-passe D antecede o Portao A.')),
}


def add(cur, novo):
    cur = (cur or '').strip()
    return (cur + ' || ' + novo) if cur else novo


def limpa_flags(f, remover):
    v = [p for p in (f or '').split(';') if p and p not in remover]
    return ';'.join(v)


def main(apply=False):
    with open(CSV, encoding='utf-8') as fh:
        rd = csv.DictReader(fh)
        campos = list(rd.fieldnames)
        linhas = list(rd)

    if 'gate_c_outcome' not in campos:
        campos.insert(campos.index('gate_c_flags'), 'gate_c_outcome')
        for x in linhas:
            x['gate_c_outcome'] = ''

    tocados = []
    for x in linhas:
        lid = x['logical_id']

        if lid in ELE:
            x['gate_c_outcome'] = 'ELEGIVEL'
            x['gate_c_flags'] = limpa_flags(x['gate_c_flags'], {'CANDIDATO_E12', 'CANDIDATO_E10'})
            x['gate_c_reviewer'] = REV
            x['gate_c_datetime'] = DT
            x['gate_c_notes'] = add(x['gate_c_notes'], ELE[lid])
            tocados.append((lid, 'ELEGIVEL'))

        elif lid in E12:
            x['gate_c_outcome'] = 'C1_E12'
            x['gate_c_flags'] = limpa_flags(x['gate_c_flags'], {'CANDIDATO_E12', 'CANDIDATO_E10'})
            x['gate_c_reviewer'] = REV
            x['gate_c_datetime'] = DT
            x['gate_c_notes'] = add(x['gate_c_notes'], E12[lid])
            x['excluded'] = 'true'
            x['exclusion_criteria'] = 'E12'
            tocados.append((lid, 'E12'))

        elif lid in E7B:
            x['gate_b_outcome'] = 'B5_E7b'
            x['gate_b_notes'] = add(x['gate_b_notes'], E7B[lid])
            x['gate_c_outcome'] = ''
            x['gate_c_flags'] = limpa_flags(x['gate_c_flags'], {'CANDIDATO_E12', 'CANDIDATO_E10'})
            x['gate_c_reviewer'] = REV
            x['gate_c_datetime'] = DT
            x['excluded'] = 'true'
            x['exclusion_criteria'] = 'E7b'
            tocados.append((lid, 'E7b'))

        if lid in FAM:
            f = FAM[lid]
            x['duplicate_group'] = f['grupo']
            x['duplicate_role'] = f['papel']
            x['gate_c_reviewer'] = REV
            x['gate_c_datetime'] = DT
            x['gate_c_notes'] = add(x['gate_c_notes'], f['notas'])
            if f['excl'] is True:
                x['excluded'] = 'true'
                x['exclusion_criteria'] = 'E3'
                x['gate_c_outcome'] = ''
                x['gate_c_flags'] = limpa_flags(x['gate_c_flags'], {'CANDIDATO_E12', 'CANDIDATO_E10'})
            tocados.append((lid, 'FAM ' + f['grupo'] + '/' + f['papel']))

    for lid, o in tocados:
        print('%-12s %s' % (lid, o))
    print('registros tocados:', len(tocados))

    if apply:
        tmp = CSV + '.tmp'
        with open(tmp, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=campos)
            w.writeheader()
            w.writerows(linhas)
        os.replace(tmp, CSV)
        print('APLICADO. colunas =', len(campos))
    else:
        print('SIMULACAO. colunas seriam =', len(campos))


if __name__ == '__main__':
    import sys
    main(apply='--apply' in sys.argv)
