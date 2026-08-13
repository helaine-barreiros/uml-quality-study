# Estados de unidades de busca manual

- `PENDING`: unidade planejada, ainda não iniciada.
- `IN_PROGRESS`: inventário ou inspeção em andamento.
- `COMPLETE`: unidade concluída e auditável.
- `BLOCKED`: unidade impedida por limitação documentada.

Futuramente, uma unidade só poderá ser `COMPLETE` quando o universo documental tiver sido estabelecido; todos os itens tiverem sido percorridos; todos os `InventoryConflict` relevantes tiverem sido reconciliados; totais e candidatos tiverem sido registrados; e as fontes de inventário estiverem preservadas no manifest. Apenas documentar um conflito não é suficiente para `COMPLETE`. Se houver conflito ainda não resolvido e sua ausência de resolução impedir o encerramento da unidade, o estado deve ser `BLOCKED`.

`DocumentaryCollectionStatus` representa separadamente o progresso desde o estabelecimento do `PRIMARY_TOC` até a materialização e auditoria do normalized inventory. Seus valores são `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE` e `BLOCKED`.

`DiscoveryPhaseStatus` representa o progresso da classificação de discovery. Seus valores são `NOT_STARTED`, `DEFERRED_UNTIL_PRE_DISCOVERY_COLLECTION_CLOSED`, `IN_PROGRESS`, `COMPLETE` e `BLOCKED`; o estado deferido proíbe discovery até uma decisão auditável de fechamento da primeira onda.

A unit with `DocumentaryCollectionStatus=COMPLETE` remains `IN_PROGRESS` until discovery, candidate counts, and all completion criteria defined by protocol v1.7 are satisfied.

Os estados globais distinguem `PRE_DISCOVERY_DOCUMENTARY_COLLECTION`, `DISCOVERY_AND_SCREENING`, `FINAL_SEARCH_UPDATE` e `CLOSED`. `PRE_DISCOVERY_COLLECTION_CLOSED` encerra apenas a primeira onda necessária para iniciar discovery; `FINAL_SEARCH_UPDATE_COMPLETE` encerra as rotas de identificação antes da síntese.

A coleta documental pode ser reaberta de forma controlada durante a atualização final quando a revisão pós-screening de triggers ativar um venue. Todo novo registro deve percorrer o mesmo pipeline raw, normalized, discovery e screening. Uma unidade nunca pode ser marcada `COMPLETE` apenas porque sua coleta documental terminou.

`FinalSearchUpdateStatus=COMPLETE` significa que uma execução da onda foi concluída; isso não equivale automaticamente ao fechamento final. `FinalUpdateIterationStatus=STABLE` indica uma iteração completa sem novos estudos elegíveis, novas ativações, triggers pendentes, citações pendentes ou conflitos documentais materiais não resolvidos. `FinalSearchClosureStatus=CLOSED` exige decisão humana auditável posterior à estabilidade.

Nova evidência pode reabrir a atualização e a revisão de triggers. Um novo estudo Layer 1 pode reabrir snowballing, e uma nova ativação pode reabrir a coleta documental. Estados de unidades documentais e estados globais do processo não devem ser confundidos.
