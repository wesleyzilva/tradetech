# Histórico de Evolução — Robôs FORCA

> Registro cronológico de versões, decisões e resultados para afinar as estratégias.

---

## Linha do Tempo

| Versão | Ativo | Data criação | Melhoria principal | Resultado 5m PnL | Status |
|--------|-------|-------------|-------------------|-----------------|--------|
| FORCA_WDO_V11 | WDO | fev/2026 | Base — sem hard SL (bug) | -2875pts | 🔴 Substituído |
| FORCA_WDO_V12 | WDO | fev/2026 | Hard SL + BE 0.33 + Trailing + MaxPerdaDia | -275pts | ✅ Melhorou |
| FORCA_WIN_V11 | WIN | fev/2026 | Base — sem hard SL (bug) | 3494pts | 🔴 Substituído |
| FORCA_WIN_V12 | WIN | fev/2026 | Hard SL + BE 0.33 + Trailing + MaxPerdaDia | 4588pts | ✅ Melhorou |

---

## Por que criamos V12

### Bug crítico V11 — Hard Stop Loss ausente

- V11 calculava `fSL` apenas para **sizing** (tamanho de contratos), mas **NÃO colocava ordem de stop real**.
- A única proteção era `StopCandleContra` (fechar se aparecer candle de exaustão contrária).
- Resultado: em **03/03/2026**, WDO ficou numa compra de 23h sem stop → **perda de -1.365pts** (op #4).
  - Era o equivalente a 113× o stop mínimo de 12pts — destruiu o capital da carteira.
- V12 corrige: `if IsBought and (Low <= fEntrada - fSL) then ClosePosition` verificado intrabar.

### Outras melhorias V12

- **Break-even agressivo**: trigger em 33% do TP (era 50%) → protege lucro mais cedo
- **Trailing stop**: após BE ativo, acompanha o preço a cada `TrailingPasso` pts
- **MaxPerdaDia**: para de operar se perda acumulada no dia ≥ limite
- **Parâmetros default para 5min**: SL=12, TP=36, janela 3/6 (era 2/4 para 15min)

---

## Resultados por Versão e Timeframe

### WDO

| TF | V11 n | V11 Win% | V11 PnL | V12 n | V12 Win% | V12 PnL | Δ PnL |
|-----|-------|----------|---------|-------|----------|---------|-------|
| 5m | 165 | 30.3% | -2875 | 176 | 35.2% | -275 | ▲2600 |
| 10m | 100 | 42.0% | -780 | 113 | 42.5% | 655 | ▲1435 |
| 15m | 78 | 51.3% | 1970 | 90 | 46.7% | 1055 | ▼915 |
| 20m | 64 | 50.0% | 2710 | 80 | 46.2% | 870 | ▼1840 |
| 30m | 49 | 42.9% | 1510 | 54 | 59.3% | 3765 | ▲2255 |
| 60m | 31 | 38.7% | -650 | 39 | 48.7% | 360 | ▲1010 |
| diario | 0 | 0.0% | 0 | 7 | 57.1% | -865 | ▼865 |

### WIN

| TF | V11 n | V11 Win% | V11 PnL | V12 n | V12 Win% | V12 PnL | Δ PnL |
|-----|-------|----------|---------|-------|----------|---------|-------|
| 5m | 316 | 44.0% | 3494 | 387 | 51.2% | 4588 | ▲1094 |
| 10m | 188 | 44.7% | 4583 | 248 | 48.4% | 791 | ▼3792 |
| 15m | 134 | 44.8% | 5181 | 181 | 54.1% | 3392 | ▼1789 |
| 20m | 89 | 47.2% | 45 | 146 | 58.9% | 974 | ▲929 |
| 30m | 81 | 37.0% | -664 | 110 | 49.1% | -621 | ▲43 |
| 60m | 39 | 41.0% | -840 | 69 | 58.0% | -300 | ▲540 |
| diario | 14 | 35.7% | 690 | 15 | 60.0% | 1116 | ▲426 |

---

## Análise de Sequências — vermelho→fúcsia

> **Vermelho** = sinal de venda forte (F ≤ -70) → entrada SHORT
> **Fúcsia**   = sinal de venda extremo (F ≤ -85) → SHORT de máxima prioridade

A análise de sequência usa os trades de VENDA (V) como proxy do sinal vermelho/fúcsia:

### WDO_V12 @ 5m

**COMPRA (verde/cyan)** (n=87)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 59 | 25.4% |
| Após vitória | 24 | 33.3% |
| Max consecutivos negativos | — | 10 seguidos |

> ⚠️ Win% após derrota é baixo (25.4%) → padrão de "revenge trading" perigoso. Considere pausa após 6 perdas consecutivas.

**VENDA (vermelho/fúcsia)** (n=89)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 46 | 39.1% |
| Após vitória | 37 | 43.2% |
| Max consecutivos negativos | — | 7 seguidos |

> ⚠️ Win% após derrota é baixo (39.1%) → padrão de "revenge trading" perigoso. Considere pausa após 4 perdas consecutivas.

### WIN_V12 @ 5m

**COMPRA (verde/cyan)** (n=200)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 92 | 54.3% |
| Após vitória | 106 | 51.9% |
| Max consecutivos negativos | — | 4 seguidos |

**VENDA (vermelho/fúcsia)** (n=187)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 93 | 52.7% |
| Após vitória | 92 | 45.7% |
| Max consecutivos negativos | — | 6 seguidos |

---

## Distribuição de Trades por Timeframe — Calibração SL/TP

> Interpretar: `≤ -100` = perdeu mais que o SL configurado (trailing falhou/gap). `> 150` = capturou movimento grande (SG não limitou). `BE` = saiu no zero (break-even acionado com sucesso).

### WDO_V12 — SL ref=12pts | TP ref=36pts

| TF | n | ≤-100% | -100/-50% | -50/-1% | BE% | 1/50% | 50/150% | >150% | MaxGanho | MaxPerda |
|-----|---|--------|-----------|---------|-----|-------|---------|-------|----------|----------| 
| 5m | 176 | 15% | 20% | 25% | 5% | 9% | 16% | 10% | 650 | -500 |
| 10m | 113 | 16% | 19% | 21% | 1% | 10% | 16% | 17% | 730 | -500 |
| 15m | 90 | 20% | 18% | 13% | 2% | 10% | 18% | 19% | 650 | -490 |
| 20m | 80 | 19% | 19% | 14% | 2% | 11% | 16% | 19% | 560 | -500 |
| 30m | 54 | 11% | 13% | 15% | 2% | 7% | 30% | 22% | 550 | -235 |
| 60m | 39 | 28% | 18% | 5% | 0% | 8% | 15% | 26% | 405 | -350 |
| diario | 7 | 43% | 0% | 0% | 0% | 0% | 0% | 57% | 490 | -1380 |

### WIN_V12 — SL ref=342pts | TP ref=1026pts

| TF | n | ≤-100% | -100/-50% | -50/-1% | BE% | 1/50% | 50/150% | >150% | MaxGanho | MaxPerda |
|-----|---|--------|-----------|---------|-----|-------|---------|-------|----------|----------| 
| 5m | 387 | 14% | 18% | 17% | 1% | 7% | 36% | 7% | 500 | -338 |
| 10m | 248 | 21% | 14% | 16% | 1% | 6% | 32% | 11% | 353 | -388 |
| 15m | 181 | 21% | 10% | 15% | 0% | 6% | 33% | 16% | 982 | -834 |
| 20m | 146 | 23% | 10% | 8% | 0% | 10% | 29% | 20% | 416 | -486 |
| 30m | 110 | 29% | 10% | 12% | 0% | 5% | 26% | 17% | 479 | -525 |
| 60m | 69 | 33% | 6% | 3% | 0% | 3% | 33% | 22% | 830 | -1135 |
| diario | 15 | 40% | 0% | 0% | 0% | 7% | 13% | 40% | 666 | -616 |

---

## Matriz de Prioridade — Robôs × Timeframes

> **Legenda de status:** 
> 🟢 Operar — PnL positivo e Win% ≥ 45%  
> 🟡 Vigilância — PnL positivo mas Win% < 45% ou n < 30  
> 🔴 Pausar — PnL negativo  
> ⚫ Não testado / sem dados  

### WDO

| Timeframe | V11 | V12 | Recomendação |
|-----------|-----|-----|--------------|
| **5m** | 🔴 -2875pts (30%w) | 🔴 -275pts (35%w) | 🚫 Pausar — calibrar |
| **10m** | 🔴 -780pts (42%w) | 🟡 +655pts (42%w, n=113) | ⚠️ Monitorar |
| **15m** | 🟢 +1970pts (51%w) | 🟢 +1055pts (47%w) | ✅ Operar |
| **20m** | 🟢 +2710pts (50%w) | 🟢 +870pts (46%w) | ✅ Operar |
| **30m** | 🟡 +1510pts (43%w, n=49) | 🟢 +3765pts (59%w) | ✅ Prioridade ALTA |
| **60m** | 🔴 -650pts (39%w) | 🟢 +360pts (49%w) | ✅ Operar |
| **diario** | ⚫ sem dados | 🔴 -865pts (57%w) | 🚫 Pausar — calibrar |

### WIN

| Timeframe | V11 | V12 | Recomendação |
|-----------|-----|-----|--------------|
| **5m** | 🟡 +3494pts (44%w, n=316) | 🟢 +4588pts (51%w) | ✅ Prioridade ALTA |
| **10m** | 🟡 +4583pts (45%w, n=188) | 🟢 +791pts (48%w) | ✅ Operar |
| **15m** | 🟡 +5181pts (45%w, n=134) | 🟢 +3392pts (54%w) | ✅ Prioridade ALTA |
| **20m** | 🟢 +45pts (47%w) | 🟢 +974pts (59%w) | ✅ Prioridade ALTA |
| **30m** | 🔴 -664pts (37%w) | 🔴 -621pts (49%w) | 🚫 Pausar — calibrar |
| **60m** | 🔴 -840pts (41%w) | 🔴 -300pts (58%w) | 🚫 Pausar — calibrar |
| **diario** | 🟡 +690pts (36%w, n=14) | 🟡 +1116pts (60%w, n=15) | ✅ Operar |

---

## Checklist para próxima versão (V13)

- [ ] Analisar se MaxPerdaDia está muito amplo (precisa calibrar)
- [ ] Verificar se TrailingPasso=4 WDO é muito pequeno (noise de 4pts no 5min)
- [ ] Testar se filtro de volume VolumeMinimo=2000 está eliminando bons trades
- [ ] Considerar horário de operação mais restrito (evitar abertura e os últimos 30min)
- [ ] WIN: avaliar se SL=342pts está correto — max perda registrada nos resultados
- [ ] Backteste com fúcsia exclusivo (só trades F ≥ 85) vs todos (F ≥ 70)

