# ANALISE-WDO_V11

> **Ativo:** WDO | **Robô:** Força V11 | **Análise gerada em:** 2026-05-07

## Resumo por Timeframe

| TF | Ops | Win% | PnL (pts) | Avg Ganho | Avg Perda | RR | Max+ | Max- | Seq+↑ | Seq-↓ | Rating |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10m | 100 | 42.0% | -780 | +142 | -123 | 1.16 | +575 | -1365 | 8 | 11 | ⭐ |
| 15m | 78 | 51.3% | +1970 | +177 | -135 | 1.32 | +550 | -715 | 5 | 6 | ⭐⭐⭐⭐ |
| 20m | 64 | 50.0% | +2710 | +209 | -124 | 1.68 | +780 | -925 | 7 | 8 | ⭐⭐⭐⭐⭐ |
| 30m | 49 | 42.9% | +1510 | +250 | -134 | 1.87 | +780 | -410 | 5 | 9 | ⭐⭐⭐⭐ |
| 5m | 165 | 30.3% | -2875 | +117 | -81 | 1.45 | +665 | -1365 | 4 | 8 | ❌ |
| 60m | 31 | 38.7% | -650 | +267 | -214 | 1.25 | +815 | -925 | 4 | 5 | ❌ |

## Análise por Timeframe

### 10m

- **Período:** 03/02/2026 → 04/05/2026
- **Resultado geral:** NEGATIVO — PnL `-780 pts`
- **Operações:** 100 total | 42 ganhos | 55 perdas | 3 empates
- **Win Rate:** `42.0%`
- **Médias:** Ganho médio `+142 pts` | Perda média `-123 pts`
- **RR implícito:** `1.16`
- **Range de pontos:** Maior ganho `+575` | Maior perda `-1365`
- **Sequências:** Máx ganhos seguidos `8` | Máx perdas seguidas `11`
- **Direção:** 38 Compras | 62 Vendas

### 15m

- **Período:** 04/02/2026 → 04/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+1970 pts`
- **Operações:** 78 total | 40 ganhos | 38 perdas | 0 empates
- **Win Rate:** `51.3%`
- **Médias:** Ganho médio `+177 pts` | Perda média `-135 pts`
- **RR implícito:** `1.32`
- **Range de pontos:** Maior ganho `+550` | Maior perda `-715`
- **Sequências:** Máx ganhos seguidos `5` | Máx perdas seguidas `6`
- **Direção:** 34 Compras | 44 Vendas

### 20m 🏆 **MELHOR**

- **Período:** 03/02/2026 → 04/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+2710 pts`
- **Operações:** 64 total | 32 ganhos | 32 perdas | 0 empates
- **Win Rate:** `50.0%`
- **Médias:** Ganho médio `+209 pts` | Perda média `-124 pts`
- **RR implícito:** `1.68`
- **Range de pontos:** Maior ganho `+780` | Maior perda `-925`
- **Sequências:** Máx ganhos seguidos `7` | Máx perdas seguidas `8`
- **Direção:** 27 Compras | 37 Vendas

### 30m

- **Período:** 04/02/2026 → 04/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+1510 pts`
- **Operações:** 49 total | 21 ganhos | 28 perdas | 0 empates
- **Win Rate:** `42.9%`
- **Médias:** Ganho médio `+250 pts` | Perda média `-134 pts`
- **RR implícito:** `1.87`
- **Range de pontos:** Maior ganho `+780` | Maior perda `-410`
- **Sequências:** Máx ganhos seguidos `5` | Máx perdas seguidas `9`
- **Direção:** 18 Compras | 31 Vendas

### 5m ⚠️ **PIOR**

- **Período:** 04/02/2026 → 04/05/2026
- **Resultado geral:** NEGATIVO — PnL `-2875 pts`
- **Operações:** 165 total | 50 ganhos | 108 perdas | 7 empates
- **Win Rate:** `30.3%`
- **Médias:** Ganho médio `+117 pts` | Perda média `-81 pts`
- **RR implícito:** `1.45`
- **Range de pontos:** Maior ganho `+665` | Maior perda `-1365`
- **Sequências:** Máx ganhos seguidos `4` | Máx perdas seguidas `8`
- **Direção:** 79 Compras | 86 Vendas

### 60m

- **Período:** 05/02/2026 → 04/05/2026
- **Resultado geral:** NEGATIVO — PnL `-650 pts`
- **Operações:** 31 total | 12 ganhos | 18 perdas | 1 empates
- **Win Rate:** `38.7%`
- **Médias:** Ganho médio `+267 pts` | Perda média `-214 pts`
- **RR implícito:** `1.25`
- **Range de pontos:** Maior ganho `+815` | Maior perda `-925`
- **Sequências:** Máx ganhos seguidos `4` | Máx perdas seguidas `5`
- **Direção:** 14 Compras | 17 Vendas

## Insights para Próximos Ajustes

- ✅ **TFs lucrativos:** `15m`, `20m`, `30m` — manter ou refinar parâmetros
- ❌ **TFs negativos:** `10m`, `5m`, `60m` — revisar SL/TP ou descartar
- ⚠️ **RR baixo (<1.5):** `10m`, `15m`, `5m`, `60m` — aumentar TP ou reduzir SL
- 🔴 **Alta sequência negativa (≥5):** `10m`, `15m`, `20m`, `30m`, `5m`, `60m` — considerar filtro de mercado ou pausa

## Próximos Experimentos Sugeridos

- [ ] Testar ajuste de SL em ±10% nos TFs lucrativos
- [ ] Testar filtro MTF: só operar se TF superior também der sinal
- [ ] Avaliar janela horária (ex: evitar abertura e fechamento)
- [ ] Comparar desempenho em dias da semana (seg-sex)
- [ ] Avaliar stop por resultado diário (-3 ops perdidas = sem operar)

---
*Gerado automaticamente por `analisar_grupos.py` em 2026-05-07 16:41*