# Estados de unidades de busca manual

- `PENDING`: unidade planejada, ainda não iniciada.
- `IN_PROGRESS`: inventário ou inspeção em andamento.
- `COMPLETE`: unidade concluída e auditável.
- `BLOCKED`: unidade impedida por limitação documentada.

Futuramente, uma unidade só poderá ser `COMPLETE` quando o universo documental tiver sido estabelecido; todos os itens tiverem sido percorridos; todos os `InventoryConflict` relevantes tiverem sido reconciliados; totais e candidatos tiverem sido registrados; e as fontes de inventário estiverem preservadas no manifest. Apenas documentar um conflito não é suficiente para `COMPLETE`. Se houver conflito ainda não resolvido e sua ausência de resolução impedir o encerramento da unidade, o estado deve ser `BLOCKED`.

`DocumentaryCollectionStatus` representa separadamente o progresso desde o estabelecimento do `PRIMARY_TOC` até a materialização e auditoria do normalized inventory. Seus valores são `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE` e `BLOCKED`.

`DiscoveryPhaseStatus` representa o progresso da classificação de discovery. Seus valores são `NOT_STARTED`, `DEFERRED_BY_A002`, `IN_PROGRESS`, `COMPLETE` e `BLOCKED`; `DEFERRED_BY_A002` proíbe intencionalmente discovery enquanto o gate de coleta documental estiver fechado.

A unit with `DocumentaryCollectionStatus=COMPLETE` remains `IN_PROGRESS` until discovery, candidate counts, and all completion criteria defined by protocol v1.7 are satisfied.
