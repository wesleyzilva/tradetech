# ANALISE-WDO_V13

> **Ativo:** WDO | **Robô:** Força V13 | **Análise gerada em:** 2026-05-07

## Resumo por Timeframe

| TF | Ops | Win% | PnL (pts) | Avg Ganho | Avg Perda | RR | Max+ | Max- | Seq+↑ | Seq-↓ | Rating |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10m | 103 | 44.7% | +385 | +114 | -92 | 1.24 | +345 | -500 | 6 | 4 | ⭐⭐ |
| 15m | 78 | 47.4% | +880 | +125 | -99 | 1.27 | +460 | -410 | 4 | 7 | ⭐⭐⭐⭐ |
| 20m | 76 | 42.1% | -535 | +127 | -109 | 1.16 | +295 | -500 | 4 | 8 | ⭐ |
| 30m | 55 | 54.5% | +2600 | +159 | -91 | 1.76 | +345 | -355 | 7 | 4 | ⭐⭐⭐⭐⭐ |
| 5m | 151 | 36.4% | -255 | +101 | -68 | 1.48 | +400 | -500 | 3 | 9 | ❌ |
| 60m | 33 | 45.5% | +5 | +175 | -154 | 1.14 | +405 | -355 | 2 | 4 | ⭐⭐⭐ |

## Análise por Timeframe

### 10m

- **Período:** 03/02/2026 → 06/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+385 pts`
- **Operações:** 103 total | 46 ganhos | 53 perdas | 4 empates
- **Win Rate:** `44.7%`
- **Médias:** Ganho médio `+114 pts` | Perda média `-92 pts`
- **RR implícito:** `1.24`
- **Range de pontos:** Maior ganho `+345` | Maior perda `-500`
- **Sequências:** Máx ganhos seguidos `6` | Máx perdas seguidas `4`
- **Direção:** 47 Compras | 56 Vendas

### 15m

- **Período:** 03/02/2026 → 06/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+880 pts`
- **Operações:** 78 total | 37 ganhos | 38 perdas | 3 empates
- **Win Rate:** `47.4%`
- **Médias:** Ganho médio `+125 pts` | Perda média `-99 pts`
- **RR implícito:** `1.27`
- **Range de pontos:** Maior ganho `+460` | Maior perda `-410`
- **Sequências:** Máx ganhos seguidos `4` | Máx perdas seguidas `7`
- **Direção:** 34 Compras | 44 Vendas

### 20m ⚠️ **PIOR**

- **Período:** 04/02/2026 → 06/05/2026
- **Resultado geral:** NEGATIVO — PnL `-535 pts`
- **Operações:** 76 total | 32 ganhos | 42 perdas | 2 empates
- **Win Rate:** `42.1%`
- **Médias:** Ganho médio `+127 pts` | Perda média `-109 pts`
- **RR implícito:** `1.16`
- **Range de pontos:** Maior ganho `+295` | Maior perda `-500`
- **Sequências:** Máx ganhos seguidos `4` | Máx perdas seguidas `8`
- **Direção:** 34 Compras | 42 Vendas

### 30m 🏆 **MELHOR**

- **Período:** 12/02/2026 → 06/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+2600 pts`
- **Operações:** 55 total | 30 ganhos | 24 perdas | 1 empates
- **Win Rate:** `54.5%`
- **Médias:** Ganho médio `+159 pts` | Perda média `-91 pts`
- **RR implícito:** `1.76`
- **Range de pontos:** Maior ganho `+345` | Maior perda `-355`
- **Sequências:** Máx ganhos seguidos `7` | Máx perdas seguidas `4`
- **Direção:** 22 Compras | 33 Vendas

### 5m

- **Período:** 03/02/2026 → 06/05/2026
- **Resultado geral:** NEGATIVO — PnL `-255 pts`
- **Operações:** 151 total | 55 ganhos | 85 perdas | 11 empates
- **Win Rate:** `36.4%`
- **Médias:** Ganho médio `+101 pts` | Perda média `-68 pts`
- **RR implícito:** `1.48`
- **Range de pontos:** Maior ganho `+400` | Maior perda `-500`
- **Sequências:** Máx ganhos seguidos `3` | Máx perdas seguidas `9`
- **Direção:** 74 Compras | 77 Vendas

### 60m

- **Período:** 11/02/2026 → 05/05/2026
- **Resultado geral:** LUCRATIVO — PnL `+5 pts`
- **Operações:** 33 total | 15 ganhos | 17 perdas | 1 empates
- **Win Rate:** `45.5%`
- **Médias:** Ganho médio `+175 pts` | Perda média `-154 pts`
- **RR implícito:** `1.14`
- **Range de pontos:** Maior ganho `+405` | Maior perda `-355`
- **Sequências:** Máx ganhos seguidos `2` | Máx perdas seguidas `4`
- **Direção:** 13 Compras | 20 Vendas

## Insights para Próximos Ajustes

- ✅ **TFs lucrativos:** `10m`, `15m`, `30m`, `60m` — manter ou refinar parâmetros
- ❌ **TFs negativos:** `20m`, `5m` — revisar SL/TP ou descartar
- ⚠️ **RR baixo (<1.5):** `10m`, `15m`, `20m`, `5m`, `60m` — aumentar TP ou reduzir SL
- 🔴 **Alta sequência negativa (≥5):** `15m`, `20m`, `5m` — considerar filtro de mercado ou pausa

## Próximos Experimentos Sugeridos

- [ ] Testar ajuste de SL em ±10% nos TFs lucrativos
- [ ] Testar filtro MTF: só operar se TF superior também der sinal
- [ ] Avaliar janela horária (ex: evitar abertura e fechamento)
- [ ] Comparar desempenho em dias da semana (seg-sex)
- [ ] Avaliar stop por resultado diário (-3 ops perdidas = sem operar)

---
*Gerado automaticamente por `analisar_grupos.py` em 2026-05-07 16:41*