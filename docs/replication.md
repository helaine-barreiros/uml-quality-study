# Estados de unidades de busca manual

- `PENDING`: unidade planejada, ainda não iniciada.
- `IN_PROGRESS`: inventário ou inspeção em andamento.
- `COMPLETE`: unidade concluída e auditável.
- `BLOCKED`: unidade impedida por limitação documentada.

Futuramente, uma unidade só poderá ser `COMPLETE` quando o universo documental tiver sido estabelecido; todos os itens tiverem sido percorridos; todos os `InventoryConflict` relevantes tiverem sido reconciliados; totais e candidatos tiverem sido registrados; e as fontes de inventário estiverem preservadas no manifest. Apenas documentar um conflito não é suficiente para `COMPLETE`. Se houver conflito ainda não resolvido e sua ausência de resolução impedir o encerramento da unidade, o estado deve ser `BLOCKED`.
