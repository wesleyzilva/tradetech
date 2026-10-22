# M02 — Deltas

Um delta = **uma alavanca**, medida contra o baseline vigente, com decisão registrada. Fluxo e regras: [`docs/01_CONVENCOES.md`](../../../docs/01_CONVENCOES.md) §6. Template: [`docs/templates/DELTA.md`](../../../docs/templates/DELTA.md).

Criar um delta:

```bash
cp docs/templates/DELTA.md motores/M02_microestrutura_barreiras/deltas/DELTA_003_slug.md
```

## Índice

| Delta | Alavanca | Hipótese | Status |
|---|---|---|---|
| [DELTA_001](DELTA_001_stop_a_mercado.md) | stop a mercado (sem limite) | MB-H05 | PROPOSTO |
| [DELTA_002](DELTA_002_cooldown_e_teto_diario.md) | cooldown entre trades e teto diário | MB-H07 | PROPOSTO |

## Backlog de ideias (ainda sem arquivo)

| Ideia | Alavanca | Motivação |
|---|---|---|
| SL/SG congelados no ATR do sinal | `Params.atr_congelado` (a criar) | I03 da revisão do código |
| Proteção na barra de entrada (stop emitido junto da entrada) | `protecao_na_barra_de_entrada=True` | I01; depende de suporte do Profit a ordens OCO na entrada |
| Piso de SL proporcional ao ATR (1 × ATR) | `sl_min`, `mult_sl` | MB-H03 |
| Apenas ctx 3 | `contextos=(3,)` | ctx 1/2 quase não disparam |
| Filtro de regime de ATR | novo parâmetro | MB-H08 |
| Brilhante como alerta de volatilidade (alvo maior após brilhante) | novo parâmetro | M01 H20 |
| Janelas por hora | `hora_ouro_*`, `mod_*` | MB-H06 (só com hold-out) |
