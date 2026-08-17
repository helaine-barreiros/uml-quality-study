# Manual de triagem — v2

- Instrumento: eligibility manual previsto na secao *Reviewer calibration* do protocolo v1.7 (l. 1296)
- Protocolo de referencia: `appendix_two_layer_mapping_protocol_v1_7.tex`
- Emendas de referencia: `amendments/A003-screening-exclusion-criteria.md` (limite de uso substantivo do LLM) e `amendments/A004-screening-gate-redesign.md` (estrutura de portoes e criterios)
- Etapa: triagem completa, do registro bruto ao corpus elegivel
- Status: `Ativo`
- Substitui: `screening_manual_v1.md`, que permanece no repositorio como **registro da primeira passagem** sobre os 986 registros da busca automatizada e nao deve ser usado para triar
- Idioma: portugues, por ser o instrumento operacional dos revisores. As
  observacoes registradas nos campos `gate_*_notes` seguem o mesmo idioma.

> **O que mudou da v1 para a v2.** A v1 organizava a triagem em tres portoes com
> quatro perguntas no Portao B e adiava para o Portao C tres criterios (E5, E10,
> E11) que, conferidos, ou nao predicavam nada do estudo ou filtravam pela
> variavel dependente da propria revisao. A emenda A004 desfez isso. A v2
> acrescenta o pre-passe **D**, acrescenta o filtro **B0**, separa **B5**,
> reduz o Portao C a **uma unica saida**, converte falta de texto completo em
> **atricao** e realinha as duas tabelas de criterios em pares.

---

## 0. Principio orientador

> **Na triagem por titulo e resumo nao se inclui nada. So se exclui.**

Os criterios de inclusao **nao sao aplicados positivamente** por titulo e resumo.
A inclusao so e confirmada na leitura do texto completo. Titulo e resumo servem
para remover o que e claramente inelegivel; todo o resto avanca.

Base normativa (protocolo, l. 1263): *"At title and abstract screening,
uncertainty favors retention. A record is excluded only when an exclusion
criterion is clearly satisfied."*

Desfechos possiveis por registro:

- **EXCLUIDO**, com exatamente um criterio primario citado e justificado;
- **RETIDO**, com ou sem sinalizacao de incerteza;
- **NAO RECUPERADO**, que **nao e exclusao** (secao 8).

---

## 1. Regras operacionais de fronteira

Estas regras resolvem os pontos em que a redacao do I4 (antigo I2) admite mais de
uma leitura. Valem uniformemente para todos os registros e sao o nucleo estavel
que a v2 herda da v1 sem alteracao de conteudo.

### RF-01 — Encoders pre-instrucionais (BERT, RoBERTa e similares)

A autoidentificacao do relato como *language model* ou *foundation model* **nao
e condicao suficiente** para o I4. O criterio decisivo e o **papel operacional**
do modelo.

Um encoder pre-treinado satisfaz o I4 **somente** quando e usado para produzir,
transformar, completar, reparar, refinar ou revisar conteudo UML de forma
**gerativa ou semanticamente constitutiva**. Quando e usado apenas como
classificador, *sequence tagger*, extrator supervisionado, codificador de
*embeddings* ou componente de NER / *relation extraction*, o estudo e excluido
por **E6**.

**Ressalva obrigatoria:** quando titulo e resumo nao permitirem distinguir o
papel do modelo, o registro e **retido** para leitura de texto completo.

**Fundamentacao.** BERT foi proposto como modelo de representacao bidirecional,
adaptado a tarefas por *fine-tuning* com uma camada adicional, e nao como modelo
autorregressivo de geracao instrucional. RoBERTa e uma otimizacao do regime de
pre-treinamento do BERT e herda essa natureza de encoder no uso tipico.

**Consequencia metodologica.** Incluir todo estudo com BERT/RoBERTa apenas porque
sao "language models" misturaria NLP supervisionado de extracao de elementos com
geracao de artefatos UML por LLM, diluindo exatamente o fenomeno que a revisao
caracteriza: como um modelo produz um artefato que pode ser sintaticamente valido
e semanticamente inadequado.

### RF-02 — Autoridade semantica sobre o conteudo UML (pipelines hibridos)

O LLM e **substantivo** quando contribui diretamente para decidir, propor ou
revisar elementos UML portadores de significado: classes, atributos, metodos,
atores, casos de uso, relacoes *include* / *extend*, mensagens, *lifelines*,
estados, transicoes, atividades, componentes, dependencias.

O LLM **nao e substantivo** quando apenas prepara o texto, resume requisitos,
produz *embeddings*, corrige gramatica, formata a saida ou executa uma etapa
periferica **enquanto regras simbolicas determinam o conteudo do modelo**.

**A presenca de regras simbolicas no pipeline e irrelevante para a decisao.**
Praticamente todo sistema serio tera validacao, pos-processamento, *parser*,
*renderer* ou *templates*. A pergunta e sempre: **quem determina o conteudo
semantico do diagrama?**

### RF-03 — Riqueza da entrada, RAG e contexto prescritivo nao transferem autoridade semantica

**Enunciado.** Instrucoes tecnicas detalhadas, gabaritos de saida, exemplos
*few-shot*, documentos anexados, base de conhecimento e recuperacao aumentada
(*RAG*) **nao sao regras simbolicas** e **nao deslocam** a autoridade semantica
para fora do modelo. Contexto restringe o espaco de saida; nao o computa. Um
estudo que fornece requisitos ricos, ontologia de dominio ou documentos de
referencia e ainda assim pede ao modelo que **decida** classes, atributos,
relacoes, multiplicidades, atores ou mensagens continua satisfazendo o I4 e
**nao pode ser excluido por E6**.

**Teste operacional — variancia contrafactual.**

> Trocar o modelo, a semente ou a redacao do *prompt*, mantendo a mesma entrada,
> poderia produzir um conjunto diferente de classes, relacoes ou multiplicidades?

| Resposta | Leitura | Decisao |
|---|---|---|
| Nao, a saida e determinada pela entrada | O conteudo vem das regras; o modelo e transdutor | **E6** |
| Sim, e a variacao recai sobre elementos portadores de significado | O modelo tem autoridade semantica | **Retem** |
| Nao da para saber por titulo e resumo | Incerteza | **Retem** e sinaliza `INCERTO_PAPEL_LLM` |

**Fronteira com o E9.** Quando a entrada **ja carrega as decisoes de modelagem**
em forma estruturada — lista de classes e atributos, esquema relacional, modelo
existente, codigo-fonte — o caso nao e de papel do LLM, e de natureza da entrada.
Registra-se **E9**, nao E6.

**Consequencia metodologica.** A dissonancia so e atribuivel ao modelo quando a
entrada era suficiente: se o *prompt* era pobre, um diagrama semanticamente
errado e explicavel pela subespecificacao; se o *prompt* era rico, prescritivo e
aumentado por RAG e o diagrama ainda saiu inadequado, o descompasso e atribuivel
ao processo de geracao. **Entrada rica e razao para reter, nao para excluir.**

**Ressalva sobre o E6.** O E6 e um julgamento de **papel do modelo**. Nao e o
lugar para registrar que um estudo e alheio ao objeto, que o LLM aparece so na
motivacao, ou que a entrada nao e textual. Vale a regra de ouro numero 5.

---

## 2. Criterios

### 2.1 Inclusao, em ordem de filtro

| Codigo | Criterio | Filtro | Par |
|---|---|---|---|
| **I1** | Esta dentro do escopo temporal e de idioma da revisao. | A1 | E4 |
| **I2** | E um relato cientifico completo. | A2 | E1 |
| **I3** | E um estudo primario. | A3 | E2 |
| **I4** | Usa ao menos um LLM como componente substantivo do processo de geracao do diagrama. | B4 | E6 |
| **I5** | A tarefa produz, transforma, completa, repara, refina ou revisa conteudo de diagrama UML. | B2 | E8 |
| **I6** | A entrada inclui requisitos textuais, user stories, cenarios, especificacoes, problem statements ou descricoes textuais de dominio. | B3 | E9 |
| **I7** | O **resultado gerado** inclui conteudo UML explicito — PlantUML, outra representacao textual de UML, XMI, diagrama renderizado, ou representacao a partir da qual o UML seja avaliavel. | B1 | E7 |
| **I8** | O conteudo UML e **separavel**, tanto de outras notacoes quanto de outros artefatos, tarefas e saidas. | B5 e C1 | E7b e E12 |

A numeracao segue a **ordem dos filtros**, nao a ordem historica do protocolo
v1.7. A tabela de-para esta na A004, secao 5.

### 2.2 Exclusao

| Codigo | Criterio | Filtro |
|---|---|---|
| **E1** | Nao e relato cientifico completo: editorial, prefacio, keynote, tutorial, slides, poster, resumo-apenas, tese, livro, patente, conteudo web nao cientifico. | A2 |
| **E2** | E estudo secundario ou terciario. | A3 |
| **E3** | E duplicata ou membro menos completo de familia de publicacao. | D |
| **E4** | Esta fora do escopo temporal ou de idioma. | A1 |
| **E6** | Nao usa LLM como componente substantivo na producao, transformacao, complementacao, reparo, refinamento ou revisao de conteudo UML. | B4 |
| **E7** | O resultado gerado nao e UML. | B1 |
| **E7b** | Ha UML na saida, mas misturado a **outra notacao** sem contribuicao UML separavel: C4, ER, BPMN, SysML, Mermaid, esboco arquitetural. | B5 |
| **E8** | A tarefa apenas avalia, explica, resume, classifica ou discute um diagrama UML existente, sem produzir, transformar, completar, reparar, refinar ou revisar conteudo UML. | B2 |
| **E9** | A entrada e codigo, imagem, modelo UML existente, logs ou outro artefato nao textual, sem componente substantivo de requisitos ou descricao textual de dominio. | B3 |
| **E12** | Nao ha instancia de geracao identificavel: o resultado UML nao se separa de outros artefatos, tarefas ou saidas gerados na mesma execucao. | C1 |

**Codigos retirados pela A004, mantidos como lacunas declaradas:**

| Codigo | Situacao |
|---|---|
| **E5** | Retirado. Falta de texto completo virou **atricao** (secao 8). |
| **E10** | Retirado. Desdobrado em **E12** mais o atributo de extracao `atribuicao do resultado`. |
| **E11** | Retirado. Substituido pelos **eixos L, D e U** de extracao (secao 9). |

Os numeros nao foram recompactados de proposito. A lacuna e o rastro da emenda:
quem le a v1 ao lado da v2 precisa enxergar o que se moveu, e as 849 exclusoes ja
registradas continuam legiveis sem tabela de traducao.

**Por que E7b tem sufixo e E12 tem numero novo.** O E7b e literalmente a segunda
clausula do E7 publicado, e o sufixo preserva essa proveniencia. O E12 nao e o
E10 reescrito: mudou o enunciado, que era negativo e agregado (*"nao podem ser
separados"*) e passou a ser uma pergunta positiva e verificavel (*"ha instancia
de geracao identificavel?"*). Enunciado novo, codigo novo.

### 2.3 Decidibilidade por titulo e resumo

| Criterio | Decidivel aqui? | Observacao operacional |
|---|---|---|
| **E4** | Total | Metadado objetivo (`PY`, `LA`, veiculo). Sem julgamento. |
| **E1** | Total | Tipo de item, ausencia de autoria, resumo ou paginas; volume de anais, tese, livro, patente. |
| **E2** | Alta | Cuidado com *survey*: survey da literatura e E2; survey como questionario com participantes e estudo primario. |
| **E3** | Alta no nivel de registro | DOI e titulo normalizado resolvem duplicatas. **Familia de publicacao** frequentemente so se confirma no texto completo (secao 3). |
| **E7** | Parcial | So exclui quando o resumo nomeia explicitamente outro produto de saida. |
| **E8** | Parcial | So exclui quando o resumo deixa claro que o diagrama ja existe e nao e alterado. |
| **E9** | Parcial | So exclui quando o resumo declara explicitamente entrada de codigo, imagem, modelo existente ou logs, sem componente textual. |
| **E6** | Parcial | Aplicar com RF-01, RF-02 e RF-03. So em casos limpidos. |
| **E7b** | Parcial | Exclui quando o resumo nomeia outra notacao ao lado da UML e nao ha indicio de contribuicao UML separavel. Na duvida, `INCERTO_SEPARABILIDADE`. |
| **E12** | Nao decidivel | Exige texto completo, e resultados. Aqui apenas sinalizar. |

**Consequencia pratica:** por titulo e resumo, apenas **E4, E1, E2, E3** e os
casos limpidos de **E6 a E9** fecham um registro com seguranca. Todo o resto
avanca.

---

## 3. Estrutura de portoes

A ordem nao e arbitraria. O protocolo (l. 1253) manda registrar *"the first
criterion that clearly explains the exclusion"*, entao a sequencia determina qual
codigo aparece na tabela PRISMA. A ordem vai do mais objetivo e mais barato
(metadado) para o mais interpretativo (conteudo).

```
                    CORPUS BRUTO (todos os registros recuperados)
                                        |
========================================v=================================
  PRE-PASSE D - NIVEL DE CORPUS       (mecanico, antes da triagem)
==========================================================================
   D. E registro unico?  --- NAO ---> REMOVIDO ANTES DA TRIAGEM   E3
      (DOI, titulo normalizado)       PRISMA: "records removed before screening"
                | SIM                 Deduplicacao NAO destrutiva:
                v                     vincular em duplicate_group, nunca apagar
                                      Familia de publicacao NAO se decide aqui:
                                      vai para o texto completo (secao 3.1)
========================================v=================================
  PORTAO A - FORMAL / METADADO        (objetivo, sem julgamento de conteudo)
==========================================================================
   A1. Ano entre jan/2022 e a data da busca, e relato em ingles?
                --- NAO ---> EXCLUIR  E4
                | SIM
                v
   A2. E relato cientifico completo?
                --- NAO ---> EXCLUIR  E1
                | SIM        (preprint NAO e motivo de E1: protocolo l. 194)
                v
   A3. E estudo primario?
                --- NAO ---> PILHA DE BACKGROUND   E2
                | SIM        (materializada, nao descartada: alimenta
                v             snowballing e validacao da busca)
========================================v=================================
  PORTAO B - SUBSTANTIVO
==========================================================================
   B0. O LLM GERA OU ALTERA O CONTEUDO UML?
       (conjuncao I4 e I5 e I7 — e o enunciado do objeto da revisao)
                --- SIM ---> RETIDO, via rapida. Anotar B1..B5 como atributos.
                --- NAO ou DUVIDA ---> descer para B1
       *** B0 ABSOLVE MAS NAO CONDENA ***
       Um "nao" no B0 nunca vira codigo. Obriga a descer e nomear o filtro
       que explica. E a protecao estrutural contra a pergunta fundida que
       gerou o deposito do E6 na primeira passagem.
                |
                v
   B1. O RESULTADO GERADO INCLUI CONTEUDO UML?
       | UML explicito, PlantUML, XMI, representacao avaliavel  |--> B2
       | O produto e outra coisa: codigo, testes, documentacao, |--> EXCLUIR E7
       |   exercicios, OCL, outro modelo, ou nada de UML        |
       | Resumo ambiguo                                         |--> RETER, INCERTO_SAIDA
                |
                v
   B2. ESSE CONTEUDO E PRODUZIDO OU ALTERADO?
       | gerado, transformado, completado, reparado, refinado,  |--> B3
       |   revisado com alteracao de conteudo                    |
       | so avaliado, explicado, resumido, classificado,        |--> EXCLUIR E8
       |   criticado; o diagrama entra e sai igual               |
       | Resumo ambiguo                                          |--> RETER, INCERTO_TAREFA
                |
                v
   B3. O QUE ENTRA NO PROCESSO?
       | requisitos, user stories, cenarios, especificacoes,     |--> B4
       |   problem statements, descricoes textuais de dominio    |
       | SOMENTE codigo, imagem, modelo existente, logs, ou      |--> EXCLUIR E9
       |   entrada ja estruturada com as decisoes de modelagem   |
       | Nao declarado                                           |--> RETER, INCERTO_ENTRADA
                |
                v          B3 VEM ANTES DE B4 de proposito: o teste de
                |          variancia contrafactual do RF-03 pressupoe
                |          saber qual era a entrada.
                v
   B4. QUAL O PAPEL DO MODELO?  [RF-01 + RF-02 + RF-03]
       | LLM nomeado propondo, gerando ou revisando elementos    |--> B5
       |   portadores de significado. Vale ainda que o prompt    |
       |   seja longo e prescritivo, que haja RAG, ontologia,    |
       |   gabarito de saida ou exemplos few-shot                |
       | Sem LLM; ou NLP de regras / gramatica; ou ML            |--> EXCLUIR E6
       |   convencional; ou encoder como classificador,          |
       |   extrator ou NER; ou o LLM so parafraseia, resume ou   |
       |   formata ENQUANTO REGRAS SIMBOLICAS DETERMINAM O       |
       |   CONTEUDO DO MODELO                                    |
       | Papel indistinguivel no resumo                          |--> RETER, INCERTO_PAPEL_LLM
                |
                v
   B5. O UML E SEPARAVEL DE OUTRAS NOTACOES?
       | so UML, ou UML claramente destacavel do restante        |--> RETIDO
       | UML citado junto de C4, ER, BPMN, SysML ou Mermaid      |--> EXCLUIR E7b
       |   sem contribuicao UML separavel                        |
       | Resumo ambiguo                                          |--> RETER, INCERTO_SEPARABILIDADE
                |
========================================v=================================
  PORTAO C - TEXTO COMPLETO           (uma unica saida)
==========================================================================
   C1. HA INSTANCIA DE GERACAO IDENTIFICAVEL?
       | sim: da para dizer o que o modelo gerou e avalia-lo     |--> ELEGIVEL
       | nao: o UML se dissolve em um artefato agregado, uma     |--> EXCLUIR E12
       |   pipeline de multiplas saidas ou uma demonstracao      |
       |   sem resultado atribuivel                              |
                |
                v
       Confirmacao dos criterios retidos por incerteza no Portao B
       (E7, E7b, E8, E9, E6) e da familia de publicacao (E3).
                |
                v
       CLASSIFICACAO, que NAO exclui: eixos L, D e U (secao 9),
       atributo `atribuicao do resultado`, e os atributos de B1..B5.
```

### 3.1 Por que a familia de publicacao migra para o texto completo

Duplicata exata e mecanica: DOI e titulo normalizado resolvem, e o lugar disso e
o pre-passe D. **Familia de publicacao** — mesmo experimento, mesmo dataset,
mesmo artefato publicado em versoes de extensao — quase nunca e visivel no
resumo. Na primeira passagem, as 107 exclusoes por E3 foram todas mecanicas e
nenhuma familia foi detectada por titulo e resumo; a unica familia real do corpus
so se resolveu com os textos em maos. Manter a deteccao de familia no Portao A
produzia uma pergunta que o revisor nao tem como responder ali.

### 3.2 Por que o Portao A nao descarta estudo secundario

O A3 **roteia**, nao exclui de vez. Revisoes, mapeamentos e surveys da literatura
formam a **pilha de background materializada**: sao a fonte primaria de
snowballing e o instrumento de validacao da cobertura da busca. Um estudo
secundario cuja lista de referencias contem primarios que a nossa string nao
recuperou e um achado sobre a busca, nao lixo. A pilha e um arquivo proprio, com
os registros marcados, e nao um subproduto do descarte.

---

## 4. Manual de sinais

### 4.1 B1 — Identificar a saida

| Conta como UML | Nao conta sozinho |
|---|---|
| "UML", "Unified Modeling Language" | "diagram", "model", "diagrama" |
| Nome de tipo: class, use case, sequence, activity, state machine, component, deployment, object, communication, package, timing, interaction overview, composite structure | "architecture diagram", "flowchart", "graph" |
| PlantUML, XMI, Ecore quando destinados a codificar UML | Mermaid, C4, ER, BPMN, SysML, que vao para o B5 |

Regra do protocolo (l. 174): *PlantUML output is eligible only when it is intended
to encode UML.*

**Atencao a direcao.** O B1 predica o **resultado gerado**, nao a mera presenca de
UML no estudo. Um trabalho de UML-para-Java tem UML por toda parte e ainda assim
falha no B1, porque o produto e codigo. Esse foi o padrao dos 22 registros de
direcao invertida da primeira passagem.

### 4.2 B4 — Identificar a autoridade semantica

**Papel gerativo ou constitutivo (aceita):** generate, produce, synthesize,
construct, derive, propose, transform, complete, repair, refine, revise, correct.
Arquiteturas: prompt engineering, few-shot, chain-of-thought, RAG, fine-tuning,
multi-agent, self-refinement, feedback loop.

**Papel periferico (rejeita, E6):** classifica, rotula, extrai, indexa, recupera,
parafraseia, resume, formata, valida gramatica.

| Configuracao | Decisao | Razao |
|---|---|---|
| LLM le requisitos e propoe classes e relacoes; regras convertem para PlantUML | Retem | LLM determina o conteudo semantico; regras formatam |
| LLM gera PlantUML; parser valida e renderiza | Retem | Validacao nao retira o papel substantivo |
| LLM gera modelo inicial; ferramenta corrige sintaxe | Retem | Conteudo semantico originado no LLM |
| LLM revisa semanticamente diagrama gerado por regras, alterando conteudo | Retem | Revisao substantiva, prevista no I5 |
| LLM recebe prompt longo e prescritivo, ontologia ou documentos via RAG, e ainda assim decide classes, atributos e relacoes | **Retem** | RF-03: contexto restringe o espaco de saida, nao o computa |
| Regras extraem todas as classes e relacoes; o LLM so serializa em PlantUML | **E6** | O conteudo ja estava decidido antes do LLM |
| Entrada ja e lista de classes, esquema relacional, modelo existente ou codigo | **E9**, nao E6 | RF-03: o problema e a natureza da entrada |
| BERT/RoBERTa fine-tuned para classificar sentencas ou extrair elementos | E6 | Nao gera conteudo UML, apenas rotula ou extrai candidatos |
| BERT embeddings mais regras que montam o diagrama | E6 | A autoridade semantica esta nas regras |
| T5, BART, GPT ou modelo text-to-text gerando PlantUML, XMI ou descricao UML | Retem | O modelo produz conteudo UML avaliavel |
| Artigo chama BERT de "foundation model" mas o usa como classificador | E6 no texto completo | A autoidentificacao nao basta |
| "language model" de forma ambigua no resumo | Retem | A exclusao por titulo e resumo seria arriscada |
| LLM aparece so na motivacao, no trabalho relacionado ou em trabalhos futuros | **E7**, nao E6 | O registro nao produz UML; o E6 e julgamento de papel, nao deposito |

### 4.3 Matriz de direcao e entrada

| Padrao no resumo | Desfecho | Filtro |
|---|---|---|
| requisitos, user stories ou cenarios --> LLM --> UML | RETEM | passa B1..B5 |
| UML existente --> LLM --> avaliacao, explicacao, critica | E8 | B2 |
| UML existente --> LLM --> codigo, testes, documentacao, OCL | E7 | B1 |
| codigo, imagem ou logs --> LLM --> UML | E9 | B3 |
| requisitos --> regras ou gramatica --> UML, com LLM ausente ou marginal | E6 | B4 |
| requisitos --> LLM --> BPMN, ER, C4, SysML ou Mermaid, sem UML | E7 | B1 |
| requisitos --> LLM --> UML **e** Mermaid **e** C4, sem separar | E7b | B5 |
| LLM gera multiplos artefatos e o UML nao se separa | RETEM com `CANDIDATO_E12` | decide em C1 |

---

## 5. Atributos anotados no Portao B

Quando o **B0 absolve**, o revisor ainda percorre B1 a B5 e anota o que viu, **sem
poder de excluir**. Sao quatro campos:

| Campo | Origem | Exemplos de valor |
|---|---|---|
| `attr_saida` | B1 e B5 | tipos de diagrama nomeados; outras notacoes presentes |
| `attr_tarefa` | B2 | geracao, transformacao, reparo, refinamento, revisao |
| `attr_entrada` | B3 | requisitos, user stories, cenarios, especificacao, descricao de dominio |
| `attr_modelo` | B4 | familia e versao nomeadas no resumo |

**Por que.** Sao tres das dimensoes de incomensurabilidade que a revisao existe
para reconstruir — tipo de diagrama, especificacao de origem e familia de modelo
— e sao obtidas de graca, na mesma leitura que ja esta sendo feita.

**Duas regras que acompanham:**

1. **Atributo de triagem e provisorio.** Vive em campo separado do de extracao e
   nunca e usado como se fosse dado extraido do texto completo.
2. **Atributo nao entra no calculo de concordancia.** O kappa e calculado sobre o
   **B0** e sobre o **criterio nomeado**, nada mais. Exigir concordancia sobre
   atributos livres tornaria o instrumento do segundo revisor impraticavel.

---

## 6. Regras de ouro

1. **A incerteza retem.** Se houve hesitacao, o registro avanca. Custa uma
   leitura; a alternativa custa um estudo perdido.
2. **Ausencia de vocabulario de qualidade nunca exclui.** A busca foi desenhada
   sem termos de qualidade justamente porque os estudos usam terminologias
   divergentes (protocolo, l. 638 e 1253). Selecionar por vocabulario de
   qualidade seria selecionar pela variavel dependente.
3. **Um criterio primario por exclusao.** Quando mais de um se aplica, registre o
   primeiro que explica claramente, seguindo a ordem dos filtros. Os demais vao
   na observacao como secundarios.
4. **Exclusao e nao destrutiva.** O registro permanece na planilha, marcado e
   justificado.
5. **Nao sobrecarregue o E6.** Entrada e I6/E9, tarefa e I5/E8, saida e I7/E7,
   separabilidade e I8/E7b/E12. Rotular tudo como E6 destroi a tabela de
   exclusoes por criterio — foi exatamente o que aconteceu na primeira passagem,
   em que 45 registros sem qualquer conteudo UML tinham sido depositados no E6.
6. **Nao filtre pela variavel dependente.** Nenhum criterio desta v2 depende de o
   estudo reportar evidencia de qualidade. Foi por isso que o E11 saiu.

---

## 7. Registro obrigatorio de cada decisao

### 7.1 Onde registrar

| Portao | Desfecho | Revisor | Momento | Observacao |
|---|---|---|---|---|
| D — pre-passe | `dedup_outcome` | — | — | `duplicate_group`, `duplicate_role` |
| A — formal e metadado | `gate_a_outcome` | `gate_a_reviewer` | `gate_a_datetime` | `gate_a_notes` |
| B — substantivo | `gate_b_outcome` | `gate_b_reviewer` | `gate_b_datetime` | `gate_b_notes` |
| C — texto completo | `gate_c_outcome` | `gate_c_reviewer` | `gate_c_datetime` | `gate_c_notes` |

Valores admitidos:

- `dedup_outcome`: `UNICO` · `D_E3`
- `gate_a_outcome`: `PASSOU` · `A1_E4` · `A2_E1` · `A3_E2`
- `gate_b_outcome`: `PASSOU` · `B0_RAPIDO` · `B1_E7` · `B2_E8` · `B3_E9` ·
  `B4_E6` · `B5_E7b` · **vazio = ainda nao triado**
- `gate_c_outcome`: `ELEGIVEL` · `C1_E12` · `NAO_RECUPERADO` · **vazio = nao lido**
- `gate_c_flags`: lista separada por `;`, entre `INCERTO_SAIDA`,
  `INCERTO_TAREFA`, `INCERTO_ENTRADA`, `INCERTO_PAPEL_LLM`,
  `INCERTO_SEPARABILIDADE`, `CANDIDATO_E12`, `SEM_RESUMO`

O desfecho carrega o **filtro** que decidiu, e nao apenas o codigo. Isso preserva
distincoes que o codigo sozinho perde, e e o que dispensa a renumeracao: a
localizacao mora no desfecho, a identidade mora no codigo.

O vazio significa **nao triado**, nunca "triado e retido". Um registro que
sobreviveu recebe `PASSOU` explicito.

`gate_c_flags` **nunca exclui**. Ele existe para que a incerteza seja
consultavel: dele saem a amostra estratificada do segundo revisor (protocolo,
l. 1296, que exige todos os incertos) e a pauta de leitura do texto completo.

### 7.2 O que escrever na observacao

Nos `gate_*_notes`, sempre nesta estrutura:

- **Metodo:** qual portao e qual filtro decidiu o caso.
- **Evidencia:** o trecho do proprio titulo, resumo ou texto que sustenta a
  decisao, citado literalmente.
- **Discussao:** qual condicao falhou. Para E6, indicar explicitamente se foi
  RF-01, RF-02 ou RF-03. Apontar os criterios secundarios considerados e por que
  nao foram escolhidos como primarios.
- **Decisao:** o codigo aplicado. Se for retencao por incerteza, registrar **qual
  pergunta especifica o texto completo precisa responder**, convertendo a duvida
  em pauta de leitura.

Escreva no portao que decidiu. Um registro excluido em A3 nao precisa de prosa
em B nem em C.

### 7.3 Decisoes que nao sao desfecho de portao

Correcao de dado, interpretacao do protocolo, adiamento, proveniencia de
metadado, decisao de desenho e **revisao de decisao anterior** vao para
`search/automated/screening_decision_log.csv`, uma linha por evento:

```
logical_id, event_datetime, reviewer, event_type, gate,
criterion_before, criterion_after, notes, evidence_path
```

`event_type` entre `DECISAO_GATE`, `REVISAO_DECISAO`, `CORRECAO_DADOS`,
`INTERPRETACAO_PROTOCOLO`, `CONFERENCIA_CRITERIO`, `RECLASSIFICACAO`,
`DECISAO_DESENHO`, `ADIAMENTO` e `PROVENIENCIA`.

O log e o que sustenta a dupla triagem e o calculo do kappa (l. 1296).

---

## 8. Acesso ao texto completo — atricao, nao exclusao

Registro cujo texto completo nao e obtido **nao e excluido**. Vai para o estrato
**"identificado, nao recuperado"**, sem `excluded=true` e sem codigo de exclusao,
com `gate_c_outcome = NAO_RECUPERADO`.

### 8.1 Vias que precisam ser esgotadas

Nesta ordem, cada uma com registro proprio no log:

1. **Acesso aberto**: Unpaywall e versoes de repositorio (`oa_status`, `oa_pdf_url`).
2. **Assinatura institucional**: Portal de Periodicos CAPES, com e sem proxy.
   Bloqueio contratual conta como tentativa documentada, desde que registrado.
3. **Busca manual**: motor academico, arXiv, pagina pessoal, repositorio
   institucional, anais do evento.
4. **Autor correspondente**: pedido de copia ao endereco declarado. Sem endereco,
   busca de canal por ORCID publico e por cruzamento de coautoria.

### 8.2 Prazo

- Espera de **15 dias corridos** a partir do encerramento da rodada de pedidos.
- **Um unico lembrete**, no setimo dia.
- Vencido o prazo, o registro e movido para o estrato nao recuperado.
- Sem canal de contato recuperavel, **nao ha o que aguardar**: move-se na data em
  que a busca de canal se esgota, com o log declarando as vias tentadas.
- **Devolucao de entrega** ou **recusa explicita**: move-se imediatamente.

Na data de fechamento, o estrato **fecha**: nada e excluido, o estrato deixa de
receber novos textos e passa a ser contado e caracterizado.

### 8.3 Por que atricao e nao exclusao

Todos os demais criterios afirmam algo **sobre o registro**. O antigo E5 afirmava
algo **sobre nos** — sobre a capacidade de acesso da revisora dentro de uma
janela de tempo. O PRISMA 2020 ja separa as duas coisas: *Reports not retrieved*
precede e e disjunta de *Reports excluded, with reasons*.

O argumento decisivo e empirico. Na primeira passagem, dos 137 retidos, 84 tinham
texto e 53 nao, e a perda era **sistematica**: zero registros OPEN entre os 53;
periodico recuperado em 83% contra conferencia em 55%; e recencia caindo de 79%
em 2024 para 53% em 2025. Um codigo de exclusao teria escondido as tres
assimetrias.

### 8.4 Consequencia sobre a cobertura das questoes

| Questoes | Base |
|---|---|
| MQ1 | todos os retidos apos os Portoes A e B |
| MQ2, MQ3 | os com texto completo, com **verificacao de sensibilidade** contra os resumos do estrato nao recuperado |
| MQ4, MQ5, SQ1 a SQ6 | apenas os com texto completo |

O relatorio informa a atricao com as tres dimensoes de vies, nominalmente, na
secao de limitacoes.

---

## 9. O que o Portao C classifica sem excluir

A evidencia de qualidade **nao e criterio de elegibilidade**. Ela e registrada na
extracao, em tres eixos independentes, derivados das definicoes operacionais do
protocolo (l. 178, 179, 182, 184, 185) e das relacoes de Krogstie:

| Eixo | Relacao | Valores |
|---|---|---|
| **L** linguagem | modelo ↔ linguagem | `ausente` · `validade_textual` · `conformidade_uml` |
| **D** dominio | modelo ↔ dominio | `ausente` · `alegada` · `requisitos_fonte` · `modelo_referencia` · `julgamento_especialista` · `rubrica` |
| **U** uso | modelo ↔ interprete e uso | `ausente` · `alegada` · `compreensao` · `atividade_engenharia` · `retrabalho` |

Os tres eixos **nunca sao colapsados em uma escala unica**. Dobrar adequacao
pragmatica dentro do eixo de dominio repetiria a falha que produziu o deposito do
E6: pergunta fundida gera codigo fundido e a distincao fica irrecuperavel.

Mais o atributo herdado do antigo E10:

- `atribuicao do resultado` ∈ {`atribuivel_ao_uml`, `agregado_com_outros_artefatos`, `nao_reportado`}

**Os subconjuntos analiticos passam a ser calculados, nao presumidos:**

| Questoes | Subconjunto |
|---|---|
| MQ1 a MQ5 | todo o corpus elegivel |
| SQ1 a SQ3 | `D` ≠ `ausente` |
| **SQ4** | `L` ≠ `ausente` **e** `D` ≠ `ausente` |
| SQ6 | `U` ≠ `ausente` |

A SQ4 pergunta em que medida a evidencia reportada distingue qualidade sintatica
de qualidade semantica. Sob o E11 esse subconjunto era pressuposto; sob os eixos
ele e computado — que e a diferenca entre descrever a literatura e descrever o
proprio filtro.

Procedimento, confiabilidade e validade vao para campos de extracao da SQ5, nunca
para os eixos.

**Regra de extracao que vale para tudo:** registrar o **vocabulario nativo
primeiro** — o termo que o estudo usa e a definicao operacional que ele da —
antes de mapear para o esquema da revisao. Normalizar cedo demais apaga
exatamente a variacao terminologica que e o achado central.

---

## 10. Armadilhas ja comprovadas neste corpus

| Armadilha | Exemplo real | Como nao cair |
|---|---|---|
| `twin` lexical | 12 dos 25 registros excluidos por E4 na primeira passagem (extrusoras de rosca dupla, guindastes, security twin peaks) | Digital twin nao e objeto da revisao |
| `GPT` como substring | GPT em afiliacao, nome de projeto ou referencia bibliografica | Exigir o LLM no papel de gerador, no mesmo enunciado |
| Nome proprio anterior ao modelo | 376_ACM (2014), sistema "GEMINI" de analytics em saude | Checar ano e dominio |
| `use case` como cenario de aplicacao | 444_ACM | Distinguir de diagrama de casos de uso |
| `survey` ambiguo | 299_ACM, 413_ACM, 958_SCOPUS | Survey da literatura e E2; questionario com participantes e primario |
| `review` ambiguo | 616_IEEE, 829_SCOPUS | Review como tarefa do LLM difere de review como metodo do estudo |
| **Direcao invertida** | 22 registros UML-para-Java, OCL, Rebeca, casos de teste | O B1 predica o **resultado gerado**, nao a presenca de UML |
| **UML desenhada pelos autores** | 790, 844, 768, 910: os autores modelam um sistema de IA em UML; o LLM nao gera nada | O B0 e a pergunta certa; sem ele esses casos so morriam dois filtros depois |
| **Deposito no E6** | 45 registros sem qualquer conteudo UML codificados como E6 na primeira passagem | Regra de ouro 5, e a descida obrigatoria a partir do B0 |

A string de busca e deliberadamente ampla (`LLM AND UML AND geracao/fonte`, sem
termos de qualidade), portanto o ruido lexical e esperado por desenho e toda a
precisao foi transferida para a triagem.

---

## 11. Uso na calibracao

1. dois revisores avaliam independentemente uma amostra proposital contendo casos
   claramente elegiveis, claramente inelegiveis e ambiguos, representando
   diferentes tipos de diagrama UML e formatos de publicacao;
2. as divergencias sao discutidas e este manual e revisado;
3. a calibracao continua ate atingir ao menos 80 por cento de concordancia e
   Cohen kappa de ao menos 0,70 no conjunto piloto;
4. na producao, o revisor primario tria todos os registros e o segundo revisor
   tria uma amostra aleatoria estratificada de ao menos 20 por cento **mais todos
   os registros marcados como incertos**.

**O que entra no kappa:** a resposta do **B0** e o **criterio nomeado**. Os
atributos da secao 5 ficam de fora.

**Amostragem estratificada, regra de reprodutibilidade:** cada estrato usa
semente propria, derivada da semente do estudo mais um hash estavel do nome do
estrato. Uma unica sequencia pseudoaleatoria percorrendo os estratos em ordem faz
com que mudar o tamanho de um estrato reembaralhe todos os seguintes — defeito
detectado na primeira passagem, em que uma reclassificacao que nao tocou os
estratos E8, E9 e RETIDO ainda assim trocou 122 dos 201 sorteados.

O flag de incerteza e peca funcional do desenho de confiabilidade, e nao
anotacao decorativa.

---

## 12. Historico

| Versao | Data | Mudanca |
|---|---|---|
| v2 | 2026-08-17 | Versao para a re-execucao do estudo. Incorpora a emenda **A004**: pre-passe **D** no nivel de corpus; filtro **B0** que absolve mas nao condena; **B3 antes de B4**; novo filtro **B5** com codigo **E7b**; Portao C reduzido a uma unica saida (**C1**, codigo **E12**); familia de publicacao migrada para o texto completo; pilha de background materializada no A3; **E5** convertido em atricao; **E10** desdobrado; **E11** e o antigo I6 substituidos pelos eixos **L, D, U** de extracao; criterios de inclusao renumerados **I1-I8** em ordem de filtro; codigos de exclusao congelados, com E5, E10 e E11 mantidos como lacunas declaradas. Acrescenta a secao 5 (atributos sem poder de excluir) e a regra de semente por estrato na secao 11. |

Versoes v1 a v1.5 estao em `screening_manual_v1.md`, preservado como registro da
primeira passagem.
