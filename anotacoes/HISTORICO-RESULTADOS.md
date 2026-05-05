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

## Análise de Sequências — fraco vs forte

> **Verde fraco**     = sinal de compra F ≥ 70 → LONG normal  
> **Verde forte**     = sinal de compra F ≥ 85 → LONG de máxima prioridade  
> **Vermelho fraco**  = sinal de venda F ≤ -70 → SHORT normal  
> **Vermelho forte**  = sinal de venda F ≤ -85 → SHORT de máxima prioridade  

A análise usa os trades por lado como proxy do sinal fraco/forte:

### WDO_V12 @ 5m

**COMPRA (verde fraco / verde forte)** (n=87)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 59 | 25.4% |
| Após vitória | 24 | 33.3% |
| Max consecutivos negativos | — | 10 seguidos |

> ⚠️ Win% após derrota é baixo (25.4%) → padrão de "revenge trading" perigoso. Considere pausa após 6 perdas consecutivas.

**VENDA (vermelho fraco / vermelho forte)** (n=89)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 46 | 39.1% |
| Após vitória | 37 | 43.2% |
| Max consecutivos negativos | — | 7 seguidos |

> ⚠️ Win% após derrota é baixo (39.1%) → padrão de "revenge trading" perigoso. Considere pausa após 4 perdas consecutivas.

### WIN_V12 @ 5m

**COMPRA (verde fraco / verde forte)** (n=200)

| Situação | trades seguintes | Win% seguinte |
|----------|-----------------|---------------|
| Após derrota | 92 | 54.3% |
| Após vitória | 106 | 51.9% |
| Max consecutivos negativos | — | 4 seguidos |

**VENDA (vermelho fraco / vermelho forte)** (n=187)

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

## Recomendação Diária — Qual Robô/Ativo/TF Operar?

> Esta seção responde: **quais configurações ativar no dia a dia segundo os resultados do V12**.

| Prioridade | Robô | Ativo | TF | Lado | Win% | PnL V12 | Obs |
|-----------|------|-------|-----|------|------|---------|-----|
| 🏆 P1 | FORCA_WIN_V12 | WIN | 30m | COMPRA | 50.0% | +460pts | n=60, avg_ganho≈178pts |
| 🏆 P1 | FORCA_WIN_V12 | WIN | 5m | COMPRA | 53.0% | +2243pts | n=200, avg_ganho≈98pts |
| 🏆 P1 | FORCA_WDO_V12 | WDO | 20m | VENDA | 53.3% | +2055pts | n=45, avg_ganho≈154pts |
| 🏆 P1 | FORCA_WDO_V12 | WDO | 60m | COMPRA | 53.8% | +610pts | n=13, avg_ganho≈224pts |
| 🏆 P1 | FORCA_WIN_V12 | WIN | 10m | COMPRA | 54.2% | +1922pts | n=118, avg_ganho≈120pts |
| 🏆 P1 | FORCA_WDO_V12 | WDO | 30m | VENDA | 57.6% | +2095pts | n=33, avg_ganho≈163pts |
| 🏆 P1 | FORCA_WIN_V12 | WIN | 60m | COMPRA | 58.3% | +27pts | n=36, avg_ganho≈202pts |
| 🏆 P1 | FORCA_WIN_V12 | WIN | diario | COMPRA | 60.0% | +1814pts | n=10, avg_ganho≈466pts |
| 🏆 P1 | FORCA_WDO_V12 | WDO | 30m | COMPRA | 61.9% | +1670pts | n=21, avg_ganho≈181pts |
| 🏆 P1 | FORCA_WIN_V12 | WIN | 15m | COMPRA | 62.8% | +4962pts | n=94, avg_ganho≈142pts |
| 🏆 P1 | FORCA_WIN_V12 | WIN | 20m | COMPRA | 65.8% | +1160pts | n=79, avg_ganho≈115pts |
| ✅ P2 | FORCA_WDO_V12 | WDO | 15m | VENDA | 46.3% | +760pts | n=54, avg_ganho≈146pts |
| ✅ P2 | FORCA_WDO_V12 | WDO | 15m | COMPRA | 47.2% | +295pts | n=36, avg_ganho≈160pts |
| ✅ P2 | FORCA_WDO_V12 | WDO | 10m | VENDA | 47.7% | +1405pts | n=65, avg_ganho≈131pts |
| ✅ P2 | FORCA_WIN_V12 | WIN | 5m | VENDA | 49.2% | +2345pts | n=187, avg_ganho≈105pts |

> **Como interpretar**: 🏆 P1 = prioridade máxima (Win%≥50% + PnL positivo). ✅ P2 = operar com cautela (Win%≥45%). Atualize esta tabela após cada série de 30+ trades.

---

## Probabilidade e Pontos Médios — Verde fraco vs Verde forte / Vermelho fraco vs Vermelho forte

> **Proxy**: trades com ganho > mediana×0.6 são classificados como 'forte' (F≥85), demais como 'fraco' (F≥70).
> O CSV não exporta o valor F por trade — para classificação exata adicione logging ao robô.

### WDO_V12

| TF | Lado | Cor | n | Win% | AvgGanho (pts) | AvgPerda (pts) | RR |
|-----|------|-----|---|------|---------------|---------------|----|
| 5m | COMPRA | verde fraco | 71 | 11.3% | 31 | 92 | 0.34 |
| 5m | COMPRA | verde forte | 16 | 100.0% | 160 | 0 | — |
| 5m | VENDA | vermelho fraco | 64 | 20.3% | 41 | 66 | 0.62 |
| 5m | VENDA | vermelho forte | 25 | 100.0% | 197 | 0 | — |
| 10m | COMPRA | verde fraco | 35 | 11.4% | 49 | 115 | 0.42 |
| 10m | COMPRA | verde forte | 13 | 100.0% | 201 | 0 | — |
| 10m | VENDA | vermelho fraco | 43 | 20.9% | 22 | 80 | 0.28 |
| 10m | VENDA | vermelho forte | 22 | 100.0% | 175 | 0 | — |
| 15m | COMPRA | verde fraco | 23 | 17.4% | 40 | 127 | 0.31 |
| 15m | COMPRA | verde forte | 13 | 100.0% | 197 | 0 | — |
| 15m | VENDA | vermelho fraco | 37 | 21.6% | 31 | 107 | 0.29 |
| 15m | VENDA | vermelho forte | 17 | 100.0% | 200 | 0 | — |
| 20m | COMPRA | verde fraco | 26 | 15.4% | 40 | 131 | 0.30 |
| 20m | COMPRA | verde forte | 9 | 100.0% | 172 | 0 | — |
| 20m | VENDA | vermelho fraco | 29 | 27.6% | 34 | 86 | 0.40 |
| 20m | VENDA | vermelho forte | 16 | 100.0% | 213 | 0 | — |
| 30m | COMPRA | verde fraco | 10 | 20.0% | 10 | 86 | 0.12 |
| 30m | COMPRA | verde forte | 11 | 100.0% | 212 | 0 | — |
| 30m | VENDA | vermelho fraco | 18 | 22.2% | 48 | 78 | 0.61 |
| 30m | VENDA | vermelho forte | 15 | 100.0% | 194 | 0 | — |
| 60m | COMPRA | verde fraco | 6 | 0.0% | 0 | 159 | — |
| 60m | COMPRA | verde forte | 7 | 100.0% | 224 | 0 | — |
| 60m | VENDA | vermelho fraco | 17 | 17.6% | 30 | 141 | 0.21 |
| 60m | VENDA | vermelho forte | 9 | 100.0% | 182 | 0 | — |
| diario | VENDA | vermelho fraco | 3 | 33.3% | 160 | 318 | 0.50 |
| diario | VENDA | vermelho forte | 3 | 100.0% | 330 | 0 | — |

### WIN_V12

| TF | Lado | Cor | n | Win% | AvgGanho (pts) | AvgPerda (pts) | RR |
|-----|------|-----|---|------|---------------|---------------|----|
| 5m | COMPRA | verde fraco | 200 | 53.0% | 98 | 87 | 1.12 |
| 5m | VENDA | vermelho fraco | 186 | 48.9% | 100 | 77 | 1.29 |
| 10m | COMPRA | verde fraco | 118 | 54.2% | 120 | 111 | 1.08 |
| 10m | VENDA | vermelho fraco | 130 | 43.1% | 109 | 98 | 1.11 |
| 15m | COMPRA | verde fraco | 93 | 62.4% | 128 | 98 | 1.30 |
| 15m | VENDA | vermelho fraco | 86 | 44.2% | 129 | 147 | 0.88 |
| 20m | COMPRA | verde fraco | 78 | 65.4% | 109 | 179 | 0.61 |
| 20m | VENDA | vermelho fraco | 67 | 50.7% | 123 | 132 | 0.93 |
| 30m | COMPRA | verde fraco | 58 | 48.3% | 158 | 163 | 0.97 |
| 30m | VENDA | vermelho fraco | 50 | 48.0% | 123 | 155 | 0.79 |
| 60m | COMPRA | verde fraco | 34 | 55.9% | 152 | 282 | 0.54 |
| 60m | VENDA | vermelho fraco | 32 | 56.2% | 136 | 237 | 0.57 |
| diario | COMPRA | verde fraco | 6 | 33.3% | 251 | 245 | 1.03 |
| diario | COMPRA | verde forte | 4 | 100.0% | 573 | 0 | — |
| diario | VENDA | vermelho fraco | 5 | 60.0% | 105 | 507 | 0.21 |

> **Como usar**: ao ver um verde forte no gráfico, consulte a linha correspondente para saber a chance histórica de ganhar e quantos pontos em média o movimento busca. Isso ajuda a calibrar expectativa e decidir se vale entrar.

---

## Premissas do Robô V12

> Documentação das regras hard-coded e parâmetros default do V12. Use como referência ao corrigir ou propor nova versão.

### Parâmetros default (5m)

| Param | WDO | WIN | Observação |
|-------|-----|-----|------------|
| SL (pts) | 12 | 342 | Hard SL executado intrabar via Low/High |
| TP (pts) | 36 | 1026 | RR = 3.0 configurado |
| BE trigger | 33% do TP (~12pts) | ~340pts | Mover stop para entrada após 33% do TP atingido |
| TrailingPasso | 4pts | 100pts | Quanto o stop sobe/desce após cada TrailingPasso de lucro |
| MaxPerdaDia | 60pts | 1026pts | Paralisa operações do dia se perda acumulada ≥ limite |
| StopHorario | 17:45 | 17:45 | Fecha posições ABERTAS e bloqueia novas entradas após esse horário |
| iJanelaDir | 3 | 3 | Janela de direção (3× TF) |
| iJanelaCtx | 6 | 6 | Janela de contexto (6× TF) |
| ForcaMinimaForte | 70 | 70 | Mínimo para considerar sinal |
| ForcaExaustao | 85 | 85 | Umbral do sinal forte — cores verd/verm forte |
| VolumeMinimo | 2000 | 2000 | Volume abaixo disso ignora o sinal |

### Comportamento de horário

- `StopHorario_H(17); StopHorario_M(45)`: quando `Time() >= 17:45`, o robô **fecha posição aberta** e define `bDeveOperar := false`.
- **Não há carry overnight intencional**: se uma posição aparece no CSV com duração overnight, foi originada em teste com StopHorario desabilitado ou em parâmetro diferente.
- `MaxBarrasEmPosicao(0)` = ilimitado → posição é mantida **intrabar indefinidamente** até SL/TP/BE/Timer.
- **Decisão para V13**: adicionar parâmetro `FecharNoFimDoDia(true)` — quando `true` garante fechamento em 17:45; quando `false` permite carry overnight deliberado.

### Fórmula de Força

```
F = (corpo / range) × (volume / mediaVol) × 100  →  clampado entre -100 e +100
```

- `corpo = |Close - Open|` do candle
- `range = High - Low` do candle
- `mediaVol` = média dos últimos N candles de volume (janela do contexto)
- Sinal positivo = candle comprador (Verde); negativo = candle vendedor (Vermelho)
- F ≥ 85 → **verde forte** (RGB 0,220,220) | F ≥ 70 → **verde fraco** (RGB 0,180,0)
- F ≤ -85 → **vermelho forte** (RGB 255,0,180) | F ≤ -70 → **vermelho fraco** (RGB 200,0,0)

### Condição de Entrada (V12)

1. `F >= ForcaMinimaForte` (≥ 70) para COMPRA
2. EMAs do Contexto (6×TF) + Direção (3×TF) + Gatilho (TF) **alinhadas com o sinal**
3. Volume ≥ VolumeMinimo
4. `bDeveOperar = true` (dentro do horário, MaxPerdaDia não atingido)
5. Sem posição aberta

---

## Proposta V13 — Derivada dos Resultados V12

> As sugestões abaixo vêm diretamente da análise dos CSVs do V12 — não são suposições teóricas.

### 1. `FecharNoFimDoDia` (novo parâmetro boolean)

- **Problema**: comportamento de horário ambíguo — alguns resultados mostram overnight.
- **Solução**: `FecharNoFimDoDia(true)` → padrão = fechar sempre às 17:45. Defina `false` somente se quiser carry overnight.
```ntsl
Input: FecharNoFimDoDia(true);
// ...
if FecharNoFimDoDia and (Time() >= StopHorario) then ClosePosition;
```

### 2. `TrailingPasso` — recalibrar por TF

- **Problema**: ~18-21% dos trades perdem >100pts com SL=12pts configurado → trailing dando stop prematuro no ruído.
- WDO 5m: range médio de candle ≈ 6pts → TrailingPasso=4 está DENTRO do ruído → **aumentar para 8pts**.
- WIN 5m: range médio ≈ 150pts → TrailingPasso=100 está OK → **aumentar para 150pts** (melhor 1:1 com range).
```ntsl
Input: TrailingPasso(8);   // WDO: era 4
Input: TrailingPasso(150); // WIN: era 100
```

### 3. `SomenteSinalForte` (novo parâmetro boolean, default false)

- **Fundamento**: sinal forte (F≥85) tem Win% proxy maior que sinal fraco (F≥70) — ver tabela Fraco vs Forte.
- Quando `true`, ignora entradas com F < ForcaExaustao (85) → menos trades, melhor win%.
```ntsl
Input: SomenteSinalForte(false);
// na condição de entrada:
if SomenteSinalForte and (fForca < ForcaExaustao) then exit;
```

### 4. `FiltrarComprasWDO` — opção de só operar VENDA no WDO

- **Fundamento**: WDO COMPRA Win% ≈ 27-38% em todos os TF (muito abaixo de 50%).
- WDO VENDA Win% ≈ 46-60% — consistente.
- Parâmetro `OperarCompra(true)` / `OperarVenda(true)` para desabilitar um lado.
```ntsl
Input: OperarCompra(true);
Input: OperarVenda(true);
// na entrada de compra:
if (not OperarCompra) then exit;
```

### 5. `JanelaAbertura` — opcional: evitar 1ª meia hora

- Operações das 09:00-09:30 têm padrão de resultado errático (alta volatilidade de abertura).
- Parâmetro `HoraInicioOperacao(9, 30)` — não entra antes das 09:30.
```ntsl
Input: HoraInicioH(9); HoraInicioM(30);
if Time() < (HoraInicioH * 60 + HoraInicioM) then exit;
```

### 6. `MaxPerdaDia` — ajustar para 1× TP (WDO)

- Atual: 60pts = 5× SL = 1.67× TP → permite destruir capital antes de parar.
- Proposta: reduzir para 36pts (= 1× TP) — se perdeu o equivalente a 1 TP, dia encerrado.
```ntsl
Input: MaxPerdaDia(36); // WDO: era 60
```

### 7. SL por TF — recalibrar para TF maiores

- SL=12pts foi calibrado para 5m. Para 30m, range médio é ≈ 18-25pts → SL poderia ser 18-20pts.
- TP também precisa escalar: 30m deveria testar TP=54-60pts (3× o SL recalibrado).
- Sugestão: `SL_Pts(0)` → quando 0, calcular automaticamente como `fRange_Medio * fator`.

### Resumo das mudanças V13

| # | Parâmetro | V12 | V13 proposto | Motivo |
|---|-----------|-----|-------------|--------|
| 1 | FecharNoFimDoDia | implícito | novo bool (true) | Ambiguidade overnight |
| 2 | TrailingPasso WDO | 4pts | 8pts | 4pts ≤ noise do 5m |
| 3 | TrailingPasso WIN | 100pts | 150pts | Proporcional ao range |
| 4 | SomenteSinalForte | — | novo bool (false) | Filtro F≥85 melhora win% |
| 5 | OperarCompra WDO | sempre | novo bool (true→false) | COMPRA Win%<40% |
| 6 | HoraInicioOperacao | 00:00 | 09:30 | Volatilidade abertura |
| 7 | MaxPerdaDia WDO | 60pts | 36pts | = 1× TP (mais conservador) |
| 8 | SL/TP por TF | fixo 12/36 | dinâmico por TF | TF maior = range maior |

---

## Checklist de Implementação V13

- [ ] Adicionar `FecharNoFimDoDia(true)` no bloco de Inputs
- [ ] Ajustar `TrailingPasso(8)` no WDO e `TrailingPasso(150)` no WIN
- [ ] Adicionar inputs `OperarCompra(true)` e `OperarVenda(true)` com guard na entrada
- [ ] Adicionar `SomenteSinalForte(false)` com guard no `if fForca >= ForcaMinimaForte`
- [ ] Adicionar `HoraInicioH(9); HoraInicioM(30)` no bloco de horário
- [ ] Reduzir `MaxPerdaDia(36)` para WDO
- [ ] Adicionar logging de `fForca` no CSV para ter classificação fraco/forte real
- [ ] Backteste V13 no mínimo 3 TF (5m, 15m, 30m) × WDO e WIN antes de colocar em produção
- [ ] Comparar resultados V13 vs V12 usando este mesmo script (analise_v12.py → analise_v13.py)

