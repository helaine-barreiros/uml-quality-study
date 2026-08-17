# Manual de triagem por titulo e resumo — v1

- Instrumento: eligibility manual previsto na secao *Reviewer calibration* do protocolo v1.7 (l. 1296)
- Protocolo de referencia: `appendix_two_layer_mapping_protocol_v1_7.tex`
- Emendas de referencia: `amendments/A003-screening-exclusion-criteria.md` e
  `amendments/A004-screening-gate-redesign.md`
- Etapa: primeira triagem (titulo, resumo, palavras-chave e metadados)
- Status: `Superado por screening_manual_v2.md. Preservado como registro da primeira passagem; nao usar para triar.`
- Sucessor: `screening_manual_v2.md`

> **Aviso de versao (v1.5, 2026-08-17).** A emenda **A004** redesenhou a estrutura
> de portoes e realinhou as tabelas de criterios. As secoes **2, 3 e 4 deste
> manual descrevem a estrutura efetivamente executada** sobre os 986 registros da
> busca automatizada, e por isso **nao foram reescritas**: reescreve-las faria o
> instrumento deixar de descrever o que foi feito, que e o mesmo motivo pelo qual
> a A004 optou por congelar os codigos de exclusao em vez de renumera-los.
> A estrutura nova esta na A004, secao 6, e passa a valer da re-triagem em diante.
> Continuam validas e aplicaveis sem ressalva: a secao 0 (RF-01, RF-02, RF-03),
> a secao 1, a secao 5, a secao 6, a secao 7, a secao 8 e a secao 10.
>
> | Onde estava | Onde esta agora |
> |---|---|
> | E5 (seccao 10) | atricao, estrato "identificado, nao recuperado" — A004 secao 3 |
> | E10 | filtro C1 mais atributo `atribuicao do resultado` — A004 secao 2 |
> | E11 e I6 | eixos de extracao L, D, U — A004 secao 1 |
> | clausula de mistura de notacao do E7 | filtro B5, codigo E7b — A004 secao 2 |
> | I1 e I5 fundidos | I1-I8 renumerados em ordem de filtro — A004 secoes 4 e 5 |
- Idioma: portugues, por ser o instrumento operacional dos revisores. As
  observacoes registradas nos campos `gate_*_notes` seguem o mesmo idioma.
  Uma versao em ingles pode ser derivada para o apendice da tese.

---

## 0. Regras operacionais de fronteira

Estas regras resolvem os pontos em que a redacao do I2 admite mais de uma
leitura. As RF-01 e RF-02 foram decididas antes da triagem de producao. A RF-03
foi acrescentada em 2026-08-17, durante a conferencia do corpus ja triado, e por
isso exige verificacao retroativa dos registros ja excluidos por E6 — o
resultado dessa verificacao esta no `screening_decision_log.csv`. Todas valem
uniformemente para todos os registros.

### RF-01 — Encoders pre-instrucionais (BERT, RoBERTa e similares)

A autoidentificacao do relato como *language model* ou *foundation model* **nao
e condicao suficiente** para o I2. O criterio decisivo e o **papel operacional**
do modelo.

Um encoder pre-treinado satisfaz o I2 **somente** quando e usado para produzir,
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
pre-treinamento do BERT e herda essa natureza de encoder no uso tipico. Isso
difere do uso de modelos autorregressivos ou instrucionais, cujo desenho enfatiza
geracao e *few-shot prompting*.

**Consequencia metodologica.** Incluir todo estudo com BERT/RoBERTa apenas porque
sao "language models" ou "foundation models" misturaria NLP supervisionado de
extracao de elementos com geracao de artefatos UML por LLM. Isso diluiria
exatamente o fenomeno que a revisao caracteriza: como um modelo produz um
artefato que pode ser sintaticamente valido e semanticamente inadequado. O
conceito de *foundation model* e mais amplo que o fenomeno de interesse, pois
abrange modelos treinados em dados amplos e adaptaveis a muitos dominios e
tarefas, nao necessariamente geracao instrucional de artefatos.

### RF-02 — Autoridade semantica sobre o conteudo UML (pipelines hibridos)

O LLM e **substantivo** quando contribui diretamente para decidir, propor ou
revisar elementos UML portadores de significado: classes, atributos, metodos,
atores, casos de uso, relacoes *include* / *extend*, mensagens, *lifelines*,
estados, transicoes, atividades, componentes, dependencias.

O LLM **nao e substantivo** quando apenas prepara o texto, resume requisitos,
produz *embeddings*, corrige gramatica, formata a saida ou executa uma etapa
periferica enquanto regras simbolicas determinam o conteudo do modelo.

**A presenca de regras simbolicas no pipeline e irrelevante para a decisao.**
Praticamente todo sistema serio tera validacao, pos-processamento, *parser*,
*renderer* ou *templates*. A pergunta e sempre: **quem determina o conteudo
semantico do diagrama?**

**Consequencia metodologica.** Permissividade excessiva incluiria estudos em que
a qualidade semantica do diagrama e majoritariamente efeito de regras, gramaticas
ou extratores deterministicos, o que comprometeria a analise de dissonancia
sintatico-semantica, pois a origem do descompasso deixaria de ser atribuivel ao
processo de geracao por LLM. Restricao excessiva eliminaria pipelines hibridos
relevantes que usam LLM com *parsers*, validadores, PlantUML, lacos de reparo ou
regras de formatacao. O hibrido e admissivel quando o LLM tem autoridade
semantica sobre o conteudo UML.

### RF-03 — Riqueza da entrada, RAG e contexto prescritivo nao transferem autoridade semantica

Esta regra fecha uma lacuna do RF-02 detectada na conferencia do corpus. O RF-02
so retira a autoridade semantica do LLM quando **regras simbolicas determinam o
conteudo do modelo**. Essa qualificacao e a protecao inteira da regra, e o
fluxograma a havia perdido. Sem ela, "o LLM apenas transforma" passa a poder ser
lido como "o LLM apenas segue instrucoes", o que excluiria por E6 exatamente a
configuracao de maior valor probatorio para esta revisao.

**Enunciado.** Instrucoes tecnicas detalhadas, gabaritos de saida, exemplos
*few-shot*, documentos anexados, base de conhecimento e recuperacao aumentada
(*RAG*) **nao sao regras simbolicas** e **nao deslocam** a autoridade semantica
para fora do modelo. Contexto restringe o espaco de saida; nao o computa. Um
estudo que fornece requisitos ricos, ontologia de dominio ou documentos de
referencia e ainda assim pede ao modelo que **decida** classes, atributos,
relacoes, multiplicidades, atores ou mensagens continua satisfazendo o I2 e
**nao pode ser excluido por E6**.

**Teste operacional — variancia contrafactual.** Diante de um pipeline hibrido,
pergunte:

> Trocar o modelo, a semente ou a redacao do *prompt*, mantendo a mesma entrada,
> poderia produzir um conjunto diferente de classes, relacoes ou multiplicidades?

| Resposta | Leitura | Decisao |
|---|---|---|
| Nao, a saida e determinada pela entrada | O conteudo vem das regras; o modelo e transdutor | **E6** |
| Sim, e a variacao recai sobre elementos portadores de significado | O modelo tem autoridade semantica | **Retem** |
| Nao da para saber por titulo e resumo | Incerteza | **Retem** e sinaliza `INCERTO_PAPEL_LLM` |

O teste e uma reformulacao operacional do RF-02, nao um criterio novo: ele apenas
torna verificavel a pergunta "quem determina o conteudo semantico do diagrama?".

**Fronteira com o E9.** Quando a entrada **ja carrega as decisoes de modelagem**
em forma estruturada — lista de classes e atributos, esquema relacional, modelo
existente, codigo-fonte — o caso nao e de papel do LLM, e de natureza da entrada.
Registra-se **E9**, nao E6. Confundir os dois inflaciona o E6 e apaga da tabela
PRISMA a razao real da exclusao.

**Consequencia metodologica.** O fenomeno que esta revisao caracteriza e a
**dissonancia entre adequacao sintatica e adequacao semantica** do artefato
gerado. Essa dissonancia so e atribuivel ao modelo quando a entrada era
suficiente: se o *prompt* era pobre, um diagrama semanticamente errado e
explicavel pela subespecificacao; se o *prompt* era rico, prescritivo e
aumentado por RAG e o diagrama ainda saiu semanticamente inadequado, o
descompasso e atribuivel ao processo de geracao. **Entrada rica e, portanto,
razao para reter, nao para excluir.** Uma leitura que excluisse esses estudos
removeria do corpus os casos de maior poder explicativo e enviesaria a revisao
na direcao de trabalhos com entrada pobre, onde o fenomeno e menos diagnostico.

**Ressalva sobre o E6 em geral.** O E6 e um julgamento de **papel do modelo**.
Ele nao e o lugar para registrar que um estudo e alheio ao objeto, que o LLM
aparece so na motivacao ou em trabalhos futuros, ou que a entrada nao e textual.
Vale a regra de ouro numero 5: **nao sobrecarregar o E6**.

---

## 1. Principio orientador da primeira etapa

> **Na primeira etapa nao se inclui nada. So se exclui.**

Os criterios I1 a I6 **nao sao aplicados positivamente** nesta etapa. A inclusao
so e confirmada na leitura do texto completo. Titulo e resumo servem para
remover o que e claramente inelegivel; todo o resto avanca.

Desfechos possiveis nesta etapa:

- **EXCLUIDO**, com exatamente um criterio E primario citado e justificado;
- **RETIDO**, com ou sem sinalizacao de incerteza.

Base normativa (protocolo, l. 1263): *"At title and abstract screening,
uncertainty favors retention. A record is excluded only when an exclusion
criterion is clearly satisfied."*

---

## 2. Decidibilidade dos criterios em titulo e resumo

| Criterio | Decidivel aqui? | Observacao operacional |
|---|---|---|
| **E4** fora do escopo temporal ou de idioma | Total | Metadado objetivo (`PY`, `LA`, veiculo). Sem julgamento. |
| **E1** nao e relato cientifico completo | Total | Tipo de item, ausencia de autoria/resumo/paginas, volume de anais, tese, livro, patente. |
| **E2** estudo secundario ou terciario | Alta | Cuidado com *survey*: survey da literatura e E2; survey como questionario com participantes e estudo primario. |
| **E3** duplicata ou familia de publicacao | Alta no nivel de registro | DOI e titulo normalizado resolvem duplicatas. Familia de publicacao (mesmo dataset, experimento ou artefato) frequentemente so se confirma no texto completo. |
| **E7** saida nao e UML | Parcial | So exclui quando o resumo nomeia explicitamente outra notacao sem componente UML separavel. |
| **E8** so avalia UML existente | Parcial | So exclui quando o resumo deixa claro que o diagrama ja existe e nao e alterado. |
| **E6** LLM nao substantivo | Parcial | Aplicar com RF-01, RF-02 e RF-03. So em casos limpidos. Nao usar como deposito de registros alheios ao objeto: se o registro nao produz UML, o criterio que explica primeiro e o **E7**. |
| **E9** entrada nao textual | Parcial | So exclui quando o resumo declara explicitamente entrada de codigo, imagem, modelo existente ou logs, sem componente textual de requisitos. |
| **E10** UML nao separavel | Baixa | Quase sempre exige texto completo. Aqui apenas sinalizar. |
| **E11** sem evidencia extraivel de qualidade | Nao decidivel | Regra explicita do protocolo (l. 1253 e 1308). A ausencia de terminologia de qualidade no resumo nao autoriza exclusao. |
| **E5** texto completo inacessivel | Deixou de ser criterio de exclusao (v1.4) | Passou a **atricao**: estrato "identificado, nao recuperado", sem `excluded=true` e sem codigo. Ver secao 10. |

**Consequencia pratica:** nesta etapa apenas **E4, E1, E2, E3** e os casos
limpidos de **E6 a E9** fecham um registro com seguranca. Todo o resto avanca.

---

## 3. Fluxograma

> **Versao visual:** diagrama de atividade UML em `screening_flow_v1.puml`,
> com as saidas renderizadas em `screening_flow_v1.svg` e `screening_flow_v1.png`.
> E a versao para consulta rapida do revisor em caso de duvida. O texto abaixo
> e normativo; o diagrama e sua representacao.

A ordem nao e arbitraria. O protocolo (l. 1253) manda registrar *"the first
criterion that clearly explains the exclusion"*, entao a sequencia determina qual
codigo aparece na tabela PRISMA de exclusoes. A ordem vai do mais objetivo e mais
barato (metadado) para o mais interpretativo (conteudo), e dentro do conteudo vai
da saida para a entrada.

```
                        REGISTRO (titulo + resumo + palavras-chave + metadados)
                                              |
============================================= v =========================================
  PORTAO A - FORMAL / METADADO       (objetivo, sem julgamento de conteudo)
========================================================================================
                                              |
   A1. O ano esta entre jan/2022 e a data da busca? ----- NAO ------------> EXCLUIR  E4
       E o relato esta em ingles?                                          (verificar antes a
                                              | SIM                         clausula de extensao)
                                              v
   A2. E um relato cientifico completo?  ---- NAO ------------------------> EXCLUIR  E1
       (nao e editorial, prefacio, keynote, tutorial, slides,
        poster, resumo-apenas, tese, livro, patente, volume de anais)
                                              | SIM
                                              v
   A3. E estudo primario?  ------------------ NAO ------------------------> EXCLUIR  E2
       (nao e revisao, mapeamento, survey da literatura,                   (guardar para
        revisao de revisoes, bibliometria)                                  snowballing e
                                              | SIM                         validacao da busca)
                                              v
   A4. E registro unico?  -------------------- NAO -----------------------> EXCLUIR  E3
       (nao e duplicata nem membro menos completo                          (deduplicacao NAO
        de familia de publicacao)                                           destrutiva: vincular,
                                              | SIM                         nunca apagar)
                                              v
============================================= v =========================================
  PORTAO B - SUBSTANTIVO   (quatro perguntas, nesta ordem: saida, origem,
                            direcao, entrada)
========================================================================================
                                              |
   B1. QUAL E O ARTEFATO DE SAIDA?
       +--------------------------------------------------------------+
       | UML explicito, ou PlantUML/XMI/representacao da qual UML      |--> segue para B2
       | seja avaliavel                                                |
       +--------------------------------------------------------------+
       | Explicitamente OUTRA notacao (BPMN, ER, C4, SysML, Mermaid    |--> EXCLUIR  E7
       | generico, esboco arquitetural) SEM componente UML separavel   |
       +--------------------------------------------------------------+
       | Resumo nao deixa claro / ambiguo                              |--> RETER (sinalizar)
       +--------------------------------------------------------------+
                                              |
                                              v
   B2. QUEM DETERMINA O CONTEUDO SEMANTICO DESSE DIAGRAMA?  [RF-01 + RF-02 + RF-03]
       +--------------------------------------------------------------+
       | LLM nomeado (GPT, ChatGPT, Claude, Gemini, Llama, Qwen,       |--> segue para B3
       | DeepSeek, Mistral, T5, BART...) propondo, gerando ou          |
       | revisando elementos portadores de significado.                |
       | Vale ainda que o prompt seja longo e prescritivo, que haja    |
       | RAG, ontologia, gabarito de saida ou exemplos few-shot        |
       | (RF-03: contexto nao e regra simbolica)                       |
       +--------------------------------------------------------------+
       | Sem LLM em parte alguma do pipeline; ou NLP de regras /       |--> EXCLUIR  E6
       | gramatica; ou ML convencional; ou encoder (BERT/RoBERTa)      |
       | como classificador / extrator / NER;                          |
       | ou o LLM so parafraseia, resume ou formata ENQUANTO REGRAS    |
       | SIMBOLICAS DETERMINAM O CONTEUDO DO MODELO.                   |
       | Teste RF-03: trocar modelo, semente ou redacao do prompt      |
       | NAO poderia mudar classes, relacoes ou multiplicidades        |
       +--------------------------------------------------------------+
       | "AI-assisted", "automated modeling", "language model"         |--> RETER (sinalizar)
       | sem especificar papel; ou papel do LLM indistinguivel         |
       | do papel das regras no resumo                                 |
       +--------------------------------------------------------------+
                                              |
                                              v
   B3. QUAL E A DIRECAO DO FLUXO?
       +--------------------------------------------------------------+
       | texto --> LLM --> UML   (o UML e PRODUTO)                     |--> segue para B4
       +--------------------------------------------------------------+
       | UML existente --> LLM --> avaliacao, explicacao, resumo,      |--> EXCLUIR  E8
       | classificacao, critica  (o UML e INSUMO, nada e alterado)     |
       +--------------------------------------------------------------+
       | UML existente --> LLM --> codigo, testes, documentacao        |--> EXCLUIR  E7
       |                          (o produto nao e UML)                |
       +--------------------------------------------------------------+
       | LLM revisa, repara ou refina um UML ja existente,             |--> segue para B4
       | ALTERANDO o conteudo                                          |    (e I3 legitimo)
       +--------------------------------------------------------------+
                                              |
                                              v
   B4. O QUE ENTRA NO PROCESSO?
       +--------------------------------------------------------------+
       | Requisitos, user stories, cenarios, especificacoes,           |--> RETER p/ texto completo
       | problem statements, descricoes textuais de dominio            |
       +--------------------------------------------------------------+
       | Explicitamente e SOMENTE codigo, imagem, modelo existente,    |--> EXCLUIR  E9
       | logs ou outro artefato nao textual                            |
       +--------------------------------------------------------------+
       | Nao declarado no resumo                                       |--> RETER (sinalizar)
       +--------------------------------------------------------------+
                                              |
============================================= v =========================================
  PORTAO C - EVIDENCIA DE QUALIDADE        *** NAO EXCLUI NESTA ETAPA ***
========================================================================================
                                              |
   C1. O resumo menciona avaliacao, medicao, acuracia, correcao,
       completude, comparacao, estudo com humanos, benchmark?
             SIM --> RETIDO  .  flag EVIDENCIA=EXPLICITA
             NAO --> RETIDO  .  flag EVIDENCIA=A_VERIFICAR
                                              |
                                              v
                              +-------------------------------+
                              |  RETIDO PARA TEXTO COMPLETO   |
                              |  (E10 e E11 decididos la;     |
                              |   E5 na obtencao do PDF)      |
                              +-------------------------------+
```

**Justificativa da ordem.** O Portao A usa metadado, e reprodutivel entre
triadores e resolve o volume barato sem gastar julgamento. Dentro do Portao B,
comecar pela saida (B1) e mais eficiente porque "nao e UML" e o descarte mais
frequente e mais objetivo; a direcao (B3) vem depois da origem (B2) porque so faz
sentido perguntar de onde vem o conteudo depois de saber que ha um LLM em jogo.

---

## 4. Manual de sinais

### 4.1 B1 — Identificar a saida

| Conta como UML | Nao conta sozinho |
|---|---|
| "UML", "Unified Modeling Language" | "diagram", "model", "diagrama" |
| Nome de tipo: class, use case, sequence, activity, state machine, component, deployment, object, communication, package, timing, interaction overview, composite structure | "architecture diagram", "flowchart", "graph" |
| PlantUML, XMI, Ecore quando destinados a codificar UML | Mermaid, C4, ER, BPMN, SysML, que ficam fora salvo componente UML separavel |

Regra do protocolo (l. 174): *PlantUML output is eligible only when it is intended
to encode UML.*

### 4.2 B2 — Identificar a autoridade semantica

**Papel gerativo ou constitutivo (aceita):** generate, produce, synthesize,
construct, derive, propose, transform, complete, repair, refine, revise, correct.
Arquiteturas: prompt engineering, few-shot, chain-of-thought, RAG, fine-tuning,
multi-agent, self-refinement, feedback loop.

**Papel periferico (rejeita, E6):** classifica, rotula, extrai, indexa, recupera,
parafraseia, resume, formata, valida gramatica. Tambem quando as regras extraem
todas as classes e relacoes e o LLM apenas converte para PlantUML.

**Tabela de casos (RF-01 e RF-02):**

| Configuracao | Decisao | Razao |
|---|---|---|
| LLM le requisitos e propoe classes e relacoes; regras convertem para PlantUML | Retem | LLM determina o conteudo semantico; regras formatam |
| LLM gera PlantUML; parser valida e renderiza | Retem | Validacao nao retira o papel substantivo |
| LLM gera modelo inicial; ferramenta corrige sintaxe | Retem | Conteudo semantico originado no LLM |
| LLM sugere mensagens de sequence diagram; regras ordenam e formalizam | Retem, se a contribuicao semantica for clara | LLM participa da composicao do conteudo UML |
| LLM revisa semanticamente diagrama gerado por regras, alterando conteudo | Retem | Revisao substantiva, prevista no I3 |
| Regras extraem todas as classes e relacoes; o LLM recebe essa lista pronta e so a serializa em PlantUML | E6, ou E10 conforme o caso | O conteudo ja estava decidido antes do LLM; ele e transdutor de formato |
| LLM recebe prompt longo e prescritivo, ontologia de dominio ou documentos via RAG, e ainda assim decide classes, atributos e relacoes | **Retem** | RF-03: contexto restringe o espaco de saida, nao o computa; a autoridade semantica continua no modelo |
| Entrada ja e uma lista de classes e atributos, um esquema relacional, um modelo existente ou codigo-fonte | **E9**, nao E6 | RF-03: o problema e a natureza da entrada, nao o papel do modelo |
| BERT/RoBERTa fine-tuned para classificar sentencas ou extrair classes, atributos, atores ou relacoes | E6 | Nao gera conteudo UML, apenas rotula ou extrai candidatos |
| BERT embeddings mais regras que montam o diagrama | E6 | A autoridade semantica esta nas regras e no pipeline |
| BERT/RoBERTa como componente de NER ou relation extraction | E6 | Extracao supervisionada, nao geracao por LLM |
| T5, BART, GPT, ChatGPT ou modelo text-to-text gerando PlantUML, XMI ou descricao UML | Retem, se satisfizer os demais criterios | O modelo produz conteudo UML avaliavel |
| Artigo chama BERT de "foundation model" mas o usa como classificador | E6 no texto completo | A autoidentificacao nao basta; o papel operacional decide |
| Artigo usa "language model" de forma ambigua no resumo | Retem | A exclusao por titulo e resumo seria arriscada |
| LLM apenas avalia ou explica um diagrama ja existente | E8 | Nao ha producao, transformacao, reparo ou revisao de conteudo UML |

### 4.3 B3 e B4 — Matriz de direcao e entrada

| Padrao no resumo | Desfecho |
|---|---|
| requisitos, user stories ou cenarios --> LLM --> UML | RETEM |
| UML existente --> LLM --> avaliacao, explicacao, critica | E8 |
| UML existente --> LLM --> codigo, testes, documentacao | E7 |
| codigo, imagem ou logs --> LLM --> UML | E9 (o I2 ate passa; falha a entrada) |
| requisitos --> regras ou gramatica --> UML, com LLM ausente ou marginal | E6 |
| requisitos --> LLM --> BPMN, ER, C4, SysML ou Mermaid sem UML separavel | E7 |
| LLM gera multiplos artefatos e o UML nao se separa | RETEM com flag E10 |

---

## 5. Regras de ouro

1. **A incerteza retem.** Se houve hesitacao, o registro avanca. Custa uma
   leitura; a alternativa custa um estudo perdido.
2. **Ausencia de vocabulario de qualidade nunca exclui.** A busca foi desenhada
   sem termos de qualidade justamente porque os estudos usam terminologias
   divergentes (protocolo, l. 638 e 1253).
3. **Um criterio primario por exclusao.** Quando mais de um se aplica, registre o
   primeiro que explica claramente a exclusao, seguindo a ordem do fluxograma. Os
   demais vao na observacao como criterios secundarios.
4. **Exclusao e nao destrutiva.** O registro permanece na planilha, marcado e
   justificado, para sustentar a contagem PRISMA e a rastreabilidade da busca.
5. **Nao sobrecarregue o I2 e o E6.** Entrada e I4/E9, tarefa e I3/E8, saida e
   I5/E7, evidencia e I6/E11. Rotular tudo como E6 destroi a tabela de exclusoes
   por criterio.

---

## 6. Registro obrigatorio de cada decisao

### 6.1 Onde registrar

O inventario da busca automatizada
(`search/automated/custom_automated_search_collection.csv`) tem um bloco de
quatro campos por portao. O registro vai **no portao que decidiu o caso**, nao
em um campo unico de triagem.

| Portao | Desfecho | Revisor | Momento | Observacao |
|---|---|---|---|---|
| A — formal e metadado | `gate_a_outcome` | `gate_a_reviewer` | `gate_a_datetime` | `gate_a_notes` |
| B — substantivo | `gate_b_outcome` | `gate_b_reviewer` | `gate_b_datetime` | `gate_b_notes` |
| C — evidencia | `gate_c_flags` | `gate_c_reviewer` | `gate_c_datetime` | `gate_c_notes` |

Valores admitidos nos desfechos:

- `gate_a_outcome`: `PASSOU` · `A1_E4` · `A2_E1` · `A3_E2` · `A4_E3`
- `gate_b_outcome`: `PASSOU` · `B1_E7` · `B2_E6` · `B3_E8` · `B3_E7` · `B4_E9`
  · **vazio = ainda nao triado**
- `gate_c_flags`: lista separada por `;`, entre `INCERTO_SAIDA`,
  `INCERTO_PAPEL_LLM`, `INCERTO_ENTRADA`, `EVIDENCIA=EXPLICITA`,
  `EVIDENCIA=A_VERIFICAR`, `CANDIDATO_E10`, `SEM_RESUMO`

O desfecho carrega o **sub-portao** que decidiu, e nao apenas o codigo de
exclusao. Isso preserva a distincao entre um E7 decidido em B1 (a saida nunca
foi UML) e um E7 decidido em B3 (havia UML na entrada, mas o produto e codigo,
teste ou documentacao) — distincao que o codigo sozinho perde.

O vazio em `gate_b_outcome` significa **nao triado**, nunca "triado e retido".
Um registro que sobreviveu ao Portao B recebe `PASSOU` explicito. Sem isso nao
ha como saber quanto da triagem foi feita, nem interromper e retomar o trabalho.

`gate_c_flags` nunca exclui. Ele existe para que a incerteza seja
**consultavel**: e dele que saem a amostra estratificada do segundo revisor
(protocolo, l. 1296, que exige todos os incertos), a pauta de leitura do texto
completo e os candidatos a E10 e E11.

### 6.2 O que escrever na observacao

Nos `gate_*_notes`, seguindo a estrutura ja adotada no corpus:

- **Metodo:** qual portao e qual pergunta do fluxograma decidiu o caso.
- **Evidencia:** o trecho do proprio titulo ou resumo que sustenta a decisao,
  citado literalmente.
- **Discussao:** qual condicao falhou. Para E6, indicar explicitamente se foi
  RF-01 (natureza do modelo) ou RF-02 (autoridade semantica). Apontar os
  criterios secundarios considerados e por que nao foram escolhidos como
  primarios.
- **Decisao:** o codigo aplicado. Se for retencao por incerteza, registrar **qual
  pergunta especifica o texto completo precisa responder**, convertendo a duvida
  da triagem em pauta de leitura.

Escreva no portao que decidiu. Um registro excluido em A3 nao precisa de prosa
em B nem em C — o curto-circuito do fluxograma e a propria justificativa de que
os portoes seguintes nao foram alcancados. Isso e a regra de ouro 3 aplicada ao
registro: **um criterio primario, uma observacao substantiva**.

Campos correlatos: `excluded` e `exclusion_criteria`, que sao **derivados** dos
desfechos de portao e servem so de resumo para o PRISMA; e, para duplicatas,
`duplicate_group` e `duplicate_role`.

### 6.3 Decisoes que nao sao desfecho de portao

Correcao de dado, interpretacao do protocolo, adiamento, proveniencia de
metadado e **revisao de decisao anterior** nao cabem nos campos de portao, que
guardam apenas o **estado atual**. Elas sao multiplas por registro e tem
historia. Vao para `search/automated/screening_decision_log.csv`, uma linha por
evento:

```
logical_id, event_datetime, reviewer, event_type, gate,
criterion_before, criterion_after, notes, evidence_path
```

`event_type` entre `DECISAO_GATE`, `REVISAO_DECISAO`, `CORRECAO_DADOS`,
`INTERPRETACAO_PROTOCOLO`, `ADIAMENTO` e `PROVENIENCIA`.

O log tambem e o que sustenta a dupla triagem: dois eventos `DECISAO_GATE` no
mesmo portao com revisores diferentes, mais um evento de consenso. A
concordancia e o kappa de Cohen exigidos pelo protocolo (l. 1296) sao calculados
a partir dele, sem duplicar os campos de portao no inventario.

---

## 7. Armadilhas ja comprovadas neste corpus

| Armadilha | Exemplo real | Como nao cair |
|---|---|---|
| `twin` lexical | 12 dos 25 registros excluidos por E4 (extrusoras de rosca dupla, guindastes, security twin peaks) | Digital twin nao e objeto da revisao |
| `GPT` como substring | GPT em afiliacao, nome de projeto ou referencia bibliografica | Exigir o LLM no papel de gerador, no mesmo enunciado |
| Nome proprio anterior ao modelo | 376_ACM (2014), sistema "GEMINI" de analytics em saude | Checar ano e dominio |
| `use case` como cenario de aplicacao | 444_ACM | Distinguir de diagrama de casos de uso |
| `survey` ambiguo | 299_ACM, 413_ACM, 958_SCOPUS | Survey da literatura e E2; questionario com participantes e primario |
| `review` ambiguo | 616_IEEE, 829_SCOPUS | Review como tarefa do LLM difere de review como metodo do estudo |

A string de busca e deliberadamente ampla (`LLM AND UML AND geracao/fonte`, sem
termos de qualidade), portanto o ruido lexical e esperado por desenho e toda a
precisao foi transferida para esta etapa de triagem.

---

## 8. Uso na calibracao

Este manual e o instrumento revisado durante a calibracao prevista na secao
*Reviewer calibration* do protocolo (l. 1296):

1. dois revisores avaliam independentemente uma amostra proposital contendo casos
   claramente elegiveis, claramente inelegiveis e ambiguos, representando
   diferentes tipos de diagrama UML e formatos de publicacao;
2. as divergencias sao discutidas e este manual e revisado;
3. a calibracao continua ate atingir ao menos 80 por cento de concordancia e
   Cohen kappa de ao menos 0,70 no conjunto piloto;
4. na producao, o revisor primario tria todos os registros e o segundo revisor
   tria uma amostra aleatoria estratificada de ao menos 20 por cento **mais todos
   os registros marcados como incertos**.

O flag de incerteza dos Portoes B e C e, portanto, peca funcional do desenho de
confiabilidade, e nao anotacao decorativa.

---

## 9. Historico

| Versao | Data | Mudanca |
|---|---|---|
| v1 | 2026-08-15 | Versao inicial. Consolida o fluxograma de triagem por titulo e resumo, a tabela de decidibilidade dos criterios I1-I6 e E1-E11, e as regras operacionais de fronteira RF-01 (encoders pre-instrucionais) e RF-02 (autoridade semantica em pipelines hibridos). |
| v1.5 | 2026-08-17 | Acrescenta o aviso de versao no cabecalho, que registra a emenda **A004** (decisoes **alfa**, **beta**, **gama**, **delta** e **epsilon**) e congela as secoes 2 a 4 como registro da estrutura efetivamente executada sobre os 986 registros. Atualiza a linha do E5 na tabela de decidibilidade. Nenhuma secao operacional foi reescrita: a estrutura nova de portoes e a tabela realinhada de criterios vivem na A004, secao 6, e valem da re-triagem em diante. |
| v1.4 | 2026-08-17 | Decisao de desenho **gamma**: o E5 deixa de ser criterio de exclusao e passa a **atricao**, no estrato "identificado, nao recuperado". Reescreve a secao 10 (verbo do corte muda de *excluir por E5* para **fechar o estrato**; 10.5 passa a justificar a mudanca de estatuto com o perfil sistematico da perda) e atualiza a linha do E5 na tabela de decidibilidade. Prazo de 2026-09-01 inalterado. Pendente de formalizacao na emenda A004, junto com **alfa** (E11 vira variavel de extracao em tres eixos) e **beta** (E7b volta ao Portao B; E10 vira C1 mais atributo de atribuicao). |
| v1.3 | 2026-08-17 | Acrescenta a **RF-03**, que fixa que riqueza de prompt, RAG, ontologia e gabarito de saida nao deslocam a autoridade semantica para fora do LLM, define o **teste de variancia contrafactual** como criterio operacional e separa a fronteira E6 / E9. Corrige a caixa B2 do fluxograma, que havia perdido a qualificacao *"enquanto regras simbolicas determinam o conteudo"* presente na RF-02, e desdobra a linha ambigua da tabela de casos. Motivada pela conferencia do corpus descrita no `screening_decision_log.csv`. Sem alteracao nos criterios do protocolo. |
| v1.2 | 2026-08-17 | Acrescenta a secao 10, que fixa a regra operacional do E5: prazo de espera, lembrete unico, data de corte e tratamento dos registros sem canal de contato. Sem alteracao nos criterios, no fluxograma ou nas regras de fronteira. |
| v1.1 | 2026-08-16 | Reescrita da secao 6. O registro passa de um campo unico (`filter_1_observations`) para um bloco de quatro campos por portao (desfecho, revisor, momento, observacao), com o sub-portao codificado no desfecho e as flags do Portao C em campo proprio e consultavel. Acrescenta a secao 6.3, que separa decisoes fora dos portoes para um log de eventos (`screening_decision_log.csv`). Sem alteracao nos criterios, no fluxograma ou nas regras de fronteira. |

---

## 10. Regra operacional do acesso ao texto completo — atricao, nao exclusao

> **Mudanca de estatuto (v1.4, decisao de desenho gamma, 2026-08-17).** O E5
> deixou de ser criterio de exclusao e passou a ser tratado como **atricao**.
> Nenhum registro recebe `excluded=true` nem codigo de exclusao por falta de
> texto completo: ele vai para o estrato **"identificado, nao recuperado"**.
> A razao esta em 10.5. Toda esta secao continua valendo como regra de
> esgotamento de vias e de prazo; o que mudou foi **o verbo do corte**, que era
> *excluir por E5* e passou a ser **fechar o estrato**.

O protocolo define o E5 como *"The full text cannot be obtained after documented
access attempts"* (l. 1243 e seguintes), mas nao diz quantas tentativas, por
quais vias, nem quanto tempo se espera. Sem essa definicao o desfecho vira
decisao caso a caso, indefensavel em banca e impossivel de replicar. Esta secao
fixa a regra.

### 10.1 Vias que precisam ser esgotadas

Um registro so pode ir para o estrato **nao recuperado** depois de percorridas, nesta ordem, todas as vias
aplicaveis, cada uma com registro proprio no log:

1. **Acesso aberto**: consulta ao Unpaywall e as versoes de repositorio
   (`oa_status`, `oa_pdf_url`).
2. **Assinatura institucional**: Portal de Periodicos CAPES, com e sem proxy.
   Bloqueio contratual ou de borda conta como tentativa documentada, desde que a
   evidencia seja registrada.
3. **Busca manual**: motor academico, arXiv, pagina pessoal, repositorio
   institucional, anais do evento.
4. **Autor correspondente**: pedido de copia ao endereco declarado no registro.
   Nao havendo endereco declarado, busca de canal por ORCID publico e por
   cruzamento de coautoria com os demais registros do corpus.

### 10.2 Prazo

- O prazo e contado a partir de **2026-08-17**, data em que a rodada de pedidos
  se encerrou e em que esta regra foi fixada.
- **Espera de 15 dias corridos.**
- **Um unico lembrete**, no setimo dia. Um lembrete, nunca mais de um: insistir
  alem disso e desproporcional para um pedido de cortesia e nao aumenta a taxa
  de resposta de forma relevante.
- Vencidos os 15 dias sem resposta, o registro e **movido para o estrato nao
  recuperado**.

| Marco | Data |
|---|---|
| Inicio da contagem | 2026-08-17 |
| Lembrete unico | **2026-08-24** |
| Fechamento do estrato nao recuperado | **2026-09-01** |

A data de corte e unica para todo o corpus. Escalonar por registro produziria uma
dezena de datas diferentes sem ganho metodologico, e a data unica e a mais
generosa para os autores contactados antes.

Ate o corte, os registros sem resposta permanecem **pendentes**. Cada texto que
chegar nesse intervalo e incorporado normalmente, com o `pdf_status` atualizado
e o recebimento registrado no log. Em 2026-09-01 o estrato **fecha**: o que
ainda estiver pendente e contado e caracterizado como nao recuperado, e o
estrato deixa de receber novos textos.

### 10.3 Registros sem canal de contato

Registro sem endereco declarado e sem canal recuperavel pelas vias de 10.1
**nao espera os 15 dias**: nao ha o que aguardar. Vai para o estrato nao
recuperado na data em que a busca de canal se esgota, com o log declarando quais
vias foram tentadas.

### 10.4 Resposta negativa ou devolucao

- **Devolucao de entrega** (endereco inexistente) sem canal alternativo: estrato
  nao recuperado imediato, como no caso ja registrado do 832_SCOPUS.
- **Recusa explicita do autor**: estrato nao recuperado imediato. O prazo perde
  funcao.

### 10.5 Por que atricao e nao exclusao

Todos os demais criterios afirmam algo **sobre o registro**: o ano, o tipo de
publicacao, o objeto, o papel do modelo, a separabilidade. O E5 afirma algo
**sobre nos** — sobre a capacidade de acesso da revisora dentro de uma janela de
tempo. Relatar *"excluidos por E5: 53"* faz o leitor ler *"53 inelegiveis"*,
quando o enunciado correto e *"53 elegiveis que nao consegui ler"*.

O PRISMA 2020 ja separa as duas coisas em caixas distintas do fluxo: *Reports
not retrieved* e anterior e disjunta de *Reports excluded, with reasons*. Manter
o E5 na tabela de criterios funde caixas que a diretriz separa.

O argumento decisivo, porem, e empirico: **a perda nao e aleatoria**. Entre os
137 retidos apos os Portoes A e B, 84 tem texto e 53 nao tem, e os 53 concentram-se
sistematicamente em tres dimensoes:

| Dimensao | Padrao observado |
|---|---|
| Modelo de acesso | **zero** registros OPEN entre os 53 (50 CLOSED); 42 OPEN entre os 84 |
| Tipo e base | periodico 25/30 (83%) vs. conferencia 58/105 (55%); ACM 96%, Scopus 55%, IEEE 40% |
| Recencia | 2024: 79% recuperado · 2025: 53% · 2026: 62% |

O vies de recencia e o mais grave, porque o objeto da revisao e de literatura
rapida e a fatia mais recente e a mais informativa sobre familias de modelo e
estrategias de prompt. Dizer "53 excluidos" apagaria essas tres assimetrias
dentro de um codigo de exclusao. Dizer "53 identificados e nao recuperados, com
este perfil" declara a ameaca a validade externa.

**Mitigacao.** 52 dos 53 possuem resumo, o que torna o estrato rotulado e nao
uma contagem vazia. Cobertura por questao:

| Questoes | Base |
|---|---|
| MQ1 | os 137 retidos |
| MQ2, MQ3 | os 84 com texto, com **verificacao de sensibilidade** contra os 52 resumos |
| MQ4, MQ5, SQ1-SQ6 | apenas os 84, por dependerem de operacionalizacao que nunca esta no resumo |

O relatorio final informa a atricao com as tres dimensoes de vies nominalmente,
na secao de limitacoes.
