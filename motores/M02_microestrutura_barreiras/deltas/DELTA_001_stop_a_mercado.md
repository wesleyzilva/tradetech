# DELTA_001 — Stop a mercado (sem limite) para eliminar a armadilha do stop-limit

| Campo | Valor |
|---|---|
| Motor | M02 |
| Baseline | `ANALISE_001` / robô v1 |
| Status | PROPOSTO |
| Hipóteses | MB-H05 (armadilha), MB-H10 (tempo) |
| Alavanca única | tipo de ordem de stop: stop-limit com offset de 5 pts → stop a mercado (ou limite a ≥ 1 × ATR do gatilho) |

## Motivação

462 trades (15,4 %) tiveram o stop-limit passivo em algum momento; média −107 pts/trade e pior −1.585 (ANALISE_001 §5.2). O comparativo não é causal, mas o risco de cauda é estrutural (I02 da revisão).

## Mudança

NTSL: `SellToCoverStop(vStop, vStop - OffsetTicks)` → `SellToCoverStop(vStop)`; idem na venda. No simulador: novo parâmetro `stop_a_mercado: bool` em `Params` (a implementar): quando verdadeiro, o stop executa no `min(open, stop)` (compra) / `max(open, stop)` (venda) mais `slippage_stop_pts`, sem estado passivo.

```python
mb.com(mb.Params(), stop_a_mercado=True, slippage_stop_pts=5.0)
```

## Medição (congelada antes de rodar)

- Conjuntos: WINFUT 1 min e WINQ26 1 min (perfil fiel e ideal) + 5 min como escala.
- Métrica primária: média por trade com custo de 2 pts e slippage de stop de 5 pts.
- Salvaguardas: pior trade, DD máx, % de saídas por TEMPO.
- Decisão: ADOTAR se pior trade ≥ −300 pts **e** média com custo não piora mais que 1 pt vs v1; REJEITAR caso contrário; ADIAR se a diferença não for distinguível (|t| < 2 na diferença pareada por pregão).
- Variantes testadas: 1 (slippage 5 pts). Sensibilidade a 0 e 10 pts reportada, não usada para decidir.

## Resultado

—

## Decisão

—
