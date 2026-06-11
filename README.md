<h1 align="center">TradeTech — Daytrade Study & Research Repository</h1>

<p align="center">
  <em>A structured knowledge base for intraday trading — Dow Theory, technical indicators, price action, and algorithmic strategies applied to the Brazilian futures market (WIN/WDO B3)</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Market-WIN%20%7C%20WDO%20B3-1B2A4A?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Approach-Price%20Action%20%2B%20Physics-FF6B35?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Timeframe-Intraday-27AE60?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Language-Python%20%7C%20NTSL%20%7C%20NTFL-3776AB?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active%20Research-F39C12?style=for-the-badge"/>
</p>

---

## Purpose

This repository documents the systematic study of intraday trading structures applied to the Brazilian equity index futures (WIN) and dollar futures (WDO) on B3. It is organised as a living knowledge base — not a signal service — covering theory, indicator construction, backtesting methodology, and algorithmic robot development.

The core research hypothesis: **physics-derived force models (F = M × A) applied to candlestick structure provide a more objective measure of trend strength than standard oscillators.**

---

## Research Domains

### 1. Dow Theory — Foundation
The structural basis for all trend analysis in this repository.

| Principle | Application |
|-----------|-------------|
| Markets move in trends (primary, secondary, minor) | Multi-timeframe alignment before entry |
| Trends consist of three phases (accumulation, participation, distribution) | Volume + price behaviour classification |
| Indices must confirm each other | WIN vs. S&P500 divergence signals |
| Volume must confirm the trend | Volume filter on all breakout setups |
| Trends remain in force until a reversal signal is clear | Stop placement and trailing logic |

---

### 2. Price Action — Structure Analysis

Key patterns under study:

- **Support & Resistance** — horizontal levels, prior highs/lows, volume nodes
- **Breakouts** — confirmed vs. false breakouts, volume confirmation model
- **Inside bars / Outside bars** — volatility compression and expansion cycles
- **Pin bars / Engulfing** — rejection signals at key levels
- **Market structure highs/lows** — trend continuation vs. reversal identification

---

### 3. Physics Applied to Price Action — F = M × A

Original research extending the [PriceAction_Fisica](https://github.com/wesleyzilva/PriceAction_Fisica) framework into indicator and robot form.

```
F (Force)        = Candle colour / direction strength   →  RGB colour scale
M (Mass)         = |Close - Open| / High-Low range      →  displacement ratio
A (Acceleration) = Volume / Average Volume              →  institutional pressure proxy

Result: Force score from -100% to +100%
```

**Colour scheme — identical across all robots and INDICADOR_FORCA_V1:**

| Score | Colour | RGB | Interpretation |
|-------|--------|-----|----------------|
| > +80% | 🟦 **Cyan** | `RGB(0,220,220)` | Buying exhaustion — exaustão compradora |
| +60% to +79% | 🟢 **Green** | `RGB(0,200,0)` | Strong buying force |
| +40% to +59% | 🩶 **Grey** | `RGB(130,130,130)` | Weak buying — watch only |
| Doji (body < 15% range) | ⬜ **White** | — | Indecision — skip |
| –40% to +40% | ⬜ **White** | — | No directional force |
| –40% to –59% | 🩶 **Grey** | `RGB(130,130,130)` | Weak selling — watch only |
| –60% to –79% | 🔴 **Red** | `RGB(200,0,0)` | Strong selling force |
| < –80% | 🩷 **Fuchsia** | `RGB(255,0,180)` | Selling exhaustion — exaustão vendedora |
| S/R zone, F < threshold | 🟡 **Yellow** | — | Zone active, no confirmation — wait |

---

### 4. Technical Indicators — Study & Implementation

Indicators under research and custom implementation:

**Trend**
- Moving averages (SMA, EMA, WMA) — period sensitivity analysis
- MACD — histogram divergence as early reversal signal
- ADX — trend strength quantification without direction bias

**Momentum**
- RSI — overbought/oversold in trending vs. ranging markets
- Stochastic — K/D crossover timing in relation to price structure
- IFR (Brazilian RSI notation) — native implementation in Profit NTSL

**Volume**
- VWAP — institutional reference price anchor
- Volume profile / POC — high-volume node identification
- OBV — accumulation/distribution confirmation

**Volatility**
- Bollinger Bands — squeeze detection before breakout
- ATR — dynamic stop sizing per volatility regime

---

### 5. Algorithmic Robots — Neologica Profit (NTSL / NTFL)

Robots and indicators developed on Neologica Profit platform targeting WIN B3:

- **NTSL** (Neologica Trading System Language) — strategy and robot source code (`.ntsl`)
- **NTFL** (Neologica Trading Framework Language) — advanced framework for complex indicator composition

**Indicadores visuais (NTFL — sem ordens, apenas visualização):**

| Indicator | Description | Language | Status |
|-----------|-------------|----------|--------|
| `INDICADOR_FORCA_V1` | F=MA 7-colour paintbar + F histogram sub-panel + S/R zone highlight + gold volume Plot9 | NTFL | ✅ v1.0 |

> Use NTFL no gráfico para leitura + NTSL separado para execução. O indicador e o robô compartilham a mesma fórmula F=M×A.

**Robôs de execução (NTSL — gerenciam ordens automaticamente):**

| Robot | Asset | TF | SL | TP | RR | Break-even | Status |
|-------|-------|----|----|----|----|------------|--------|
| `FORCA_SEMAFORO_CORES_SOM` | WDO/WIN | qualquer | fixo | configurável | configurável | ❌ | ✅ v9.0 — referência, não modificar |
| `FORCA_SEMAFORO_V10` | qualquer | qualquer | dinâmico `max(fixo, range×0.75)` | configurável | configurável | ✅ `ratio=0.5` | ✅ v10 |
| `FORCA_WDO_V11` | **WDO** | **15min** `60/30/15` | dinâmico `max(20, range×1.5)` | **60 pts** | **3.0** | ✅ `ratio=0.5` | ✅ v11 calibrado |
| `FORCA_WDO_V11` | **WDO** | **5min** `30/15/5` | dinâmico `max(12, range×2.0)` | **36 pts** | **3.0** | ✅ `ratio=0.5` | ✅ v11 calibrado |
| `FORCA_WIN_V11` | **WIN** | **15min** `60/30/15` | dinâmico `max(822, range×2.0)` | **2466 pts** | **3.0** | ✅ `ratio=0.5` | ✅ baseline calibrado |
| `FORCA_WIN_V14` | **WIN** | **15min** | dinâmico `max(822, range×2.0)` | **2466 pts** | **3.0** | ✅ `ratio=0.5` | 🧪 V11 + filtro 1º candle + hard SL intrabar |
| `FORCA_WIN_V15` | **WIN** | **15min** | **30 pts** | **50 pts** / teto 100 | 1.67–3.33 | ✅ `ratio=0.6` | 🧪 scalp curto, não rebacktestado |
| `FORCA_WIN_V15_5MIN` | **WIN** | **5min** | **30 pts** | **50 pts** / teto 100 | 1.67–3.33 | ✅ `ratio=0.6` | 🧪 scalp adaptado para 5min |
| `FORCA_WIN_V16` | **WIN** | same-TF MA5/MA20 | **75 pts** | **150 pts** | **2.0** | ✅ `ratio=0.333` + adaptativo | ⚠️ foco atual, não rebacktestado |
| `FORCA_WIN_V17_sinaisForcaComMedias` | **WIN** | 15min | **150 pts** | **1500 pts** | ~10 | ✅ 75 pts absolutos | ⚠️ experimental OCR/telas |

---

## Robot Comparison — How They Differ

All robots share the same core formula **F = M × A**. What differs is **when to enter**, **how much to risk**, and **which asset they are calibrated for**.

| Robot | Asset | Entry filter | Break-even | RR | Observação |
|-------|-------|-------------|------------|-----|------------|
| `FORCA_SEMAFORO_CORES_SOM` | WDO/WIN | F ≥ 55 degradê | ❌ não tem | config | Referência visual — **não modificar** |
| `FORCA_SEMAFORO_V10` | qualquer | F ≥ 55 ou F ≥ 70 (toggle) | ✅ `BreakEvenRatio=0.5` | config | Genérico — configure por ativo/TF |
| `FORCA_WDO_V11` | WDO | F ≥ 70 (fraco descartado) | ✅ `BreakEvenRatio=0.5` | **3.0** | 47.786 candles · win 39.5% |
| `FORCA_WIN_V11` | WIN | F ≥ 70 (fraco descartado) | ✅ `BreakEvenRatio=0.5` | **3.0** | Baseline estatístico; exaustão win 44.6% |
| `FORCA_WIN_V16` | WIN | F ≥ 70 no 1º candle + MA5/MA20 + volume | ✅ `BreakEvenRatio=0.333`, cor oposta e 5 brancos | **2.0** | Foco atual; precisa backtest antes de operar |
| `INDICADOR_FORCA_V1` | visual | — | — | — | 7 cores + zona S/R + gold volume |

> **Break-even:** V11/V14 usam `BreakEvenRatio=0.5`. O V16 usa `BreakEvenRatio=0.333` e também arma BE por cor oposta ou por 5 candles brancos consecutivos.

---

## Current Focus — FORCA_WIN_V16

`Robots/FORCA_WIN_V16` é o robô experimental atual para WIN. Ele parte da lógica V14, mas troca o perfil de gestão para uma operação mais curta e defensiva: `StopMinimo=75`, `TakeProfit=150`, `BreakEvenRatio=0.333`, trailing proporcional e limite de 6 barras em posição.

### O que ele faz

1. Calcula força do candle com `F = ((Close - Open) / (High - Low)) × (Volume / MediaVolume) × 100`, limitada entre -100 e +100.
2. Classifica a força em zonas: alerta visual `55–70`, força operacional `70–85` e exaustão `>=85`, com simetria para venda.
3. Pinta o candle em verde/vermelho por intensidade e usa cyano/fúcsia quando há instabilidade visual: 3 ou mais mudanças de zona dentro de uma janela de 5 candles.
4. Entra apenas no primeiro candle forte da sequência: compra se `fForca >= 70` e `fForca[1] < 70`; venda se `fForca <= -70` e `fForca[1] > -70`.
5. Exige contexto same-TF por médias: `MA5` direcional e `MA20` de contexto, além de volume mínimo `5000` quando o filtro de volume está ligado.
6. Protege a posição com hard SL por `Low/High`, stop por força contrária `70`, stop horário `17:45`, máximo de 6 barras, BE adaptativo e trailing proporcional após BE.

### Como operar/validar

| Etapa | Regra prática |
|---|---|
| Antes da sessão | Definir viés manual do dia e confirmar se WIN está com liquidez normal |
| Entrada | Esperar candle fechar com F operacional e médias alinhadas |
| Gestão | Não mover SL manualmente antes do BE; observar cor oposta, candles brancos e trailing |
| Validação | Backtestar V16 contra V14 no mesmo período antes de usar em conta real |
| Comparação mínima | N trades, win%, PnL, AvgWin, AvgLoss, payoff, expectancy e motivo de saída |

### Gaps encontrados no V16

| ID | Gap | Impacto | Próximo trabalho |
|---|---|---|---|
| G01 | V16 ainda não foi rebacktestado | Não há confirmação estatística do novo SL/TP/BE/trailing | Criar backtest V16 vs V14 no mesmo período |
| G02 | `iQtd` é calculado por risco, mas as ordens usam `BuyAtMarket`/`SellShortAtMarket` sem quantidade explícita | O robô pode depender da quantidade configurada na plataforma, não do sizing interno | Confirmar sintaxe NTSL para ordem com quantidade e ajustar se suportado |
| G03 | Janela de instabilidade é por bloco resetado de 5 candles, não janela deslizante real | Pode perder mudança relevante na borda entre blocos | Implementar contador deslizante se NTSL suportar histórico de zonas |
| G04 | Alerta de mudança tardia não mede tempo real do candle | NTSL roda no fechamento; a regra é só aproximação por borda | Manter desligado ou migrar para execução intrabar/tick se disponível |
| G05 | `fForcaAnterior` é atribuído mas não usado | Ruído de código e possível intenção incompleta | Remover ou usar na regra de cruzamento tardio |

---

### Key decision: which robot to use?

```
Análise visual / aprendizado
  └─► INDICADOR_FORCA_V1 — entender o sistema de cores sem enviar ordens

Qualquer ativo ou TF personalizado
  └─► FORCA_SEMAFORO_V10 — configure SL/TP/thresholds por ativo
      Tripletas testadas: 60/30/15 · 30/15/5 · 15/10/5

WDO (mini-dólar) — execução automática
  └─► FORCA_WDO_V11
        15min (tripleta 60/30/15): iJanelaDir=2 · iJanelaCtx=4 · SL=20 · TP=60
         5min (tripleta 30/15/5) : iJanelaDir=3 · iJanelaCtx=6 · SL=12 · TP=36
        10min (tripleta 60/30/10): iJanelaDir=3 · iJanelaCtx=6 · ajustar SL

WIN (mini-índice) — execução automática
  ├─► FORCA_WIN_V11 — baseline estatístico calibrado
        15min (tripleta 60/30/15): iJanelaDir=2 · iJanelaCtx=4 · SL=822  · TP=2466
         5min (tripleta 30/15/5) : iJanelaDir=3 · iJanelaCtx=6 · SL=342  · TP=1026
        10min (tripleta 60/30/10): iJanelaDir=3 · iJanelaCtx=6 · ajustar SL
  └─► FORCA_WIN_V16 — foco experimental atual
        same-TF: MA5/MA20 · SL=75 · TP=150 · BE=33% + cor oposta + 5 brancos
        usar apenas para simulação/backtest até validar estatística
```

> **Tripleta 60/30/10 (10min):** multiplicadores `iJanelaDir=3` (3×10=30min) e `iJanelaCtx=6` (6×10=60min) — matematicamente válida. SL sugerido: WDO ~22pts (2.2×range médio 10min ~10pts) · WIN ~880pts.

### Colour consistency rule

All V11 robots and INDICADOR_FORCA_V1 use the **same RGB values**:
- 🟢 Verde escuro `RGB(0,180,0)` — forte (F ≥ 70)
- 🟦 Cyan `RGB(0,220,220)` — exaustão compradora (F ≥ 85)
- 🔴 Vermelho `RGB(200,0,0)` — forte (F ≤ –70)
- 🩷 Fúcsia `RGB(255,0,180)` — exaustão vendedora (F ≤ –85)

SEMÁFORO_V10 uses its own 2-tone scheme (verde claro/escuro, verm claro/escuro) — **this is intentional and correct**.

V14+ execution robots use the newer green/red intensity palette. In V16, cyano/fúcsia are no longer exhaustion colours; they are instability overrides when zones change too often inside the configured window.

---

## Study Structure

```
tradetech/
├── Robots/                        NTSL/NTFL robot and indicator source code
│   ├── FORCA_SEMAFORO_CORES_SOM   v9.0 — original rainbow semaphore (WDO/WIN)
│   ├── FORCA_SEMAFORO_V10         v10  — genérico, SL dinâmico, break-even, qualquer TF
│   ├── FORCA_WDO_V11              v11  — WDO · SL=20(15min)/12(5min) · TP RR3 · BE=0.5
│   ├── FORCA_WIN_V11              v11  — WIN · baseline estatístico
│   ├── FORCA_WIN_V14..V17         versões experimentais WIN
│   ├── CHANGELOG.md               histórico de decisões por versão
│   ├── MAPA_FORCA_WIN.md          mapa de regras V16
│   └── RAID_LOG.md                riscos, premissas, issues e decisões
├── CandlesHistoryDatas/           dados históricos de candles
├── DailyNotesOperations/          notas de operação diária
├── ScreenToStudy_MaterOfTrades/   telas usadas para estudo visual e OCR
├── Notes/                         notas gerais de pesquisa
├── teoria/                        Theory notes — Dow, Price Action, indicators
├── indicadores/                   Custom indicator logic and formulas
├── referencias/                   External papers, books, and resources
├── gitCommands/                   comandos auxiliares de Git
└── rodar_analise.bat              Run all analysis scripts (Task Scheduler ready)
```

---

## Market Calibration — 2026 Data

Calibrated on **47,786 candles (WDO) and 47,787 candles (WIN)** · full historical series 2012–2026.

### Current Range Reference (2026 actual vs historical)

| Asset | TF | Historical avg range | **2026 avg range** | Change | Multiplier used |
|-------|----|--------------------|-------------------|--------|----------------|
| **WDO** | 15 min | 13.3 pts | **~17 pts** | +28% | 1.5× range |
| **WDO** | 5 min | 6.1 pts | **~7.5 pts** | +23% | 2.0× range |
| **WIN** | 15 min | 411 pts | **~480 pts** | +17% | 2.0× range |
| **WIN** | 5 min | 171 pts | **~200 pts** | +17% | 2.0× range |

> ⚠️ **2026 context:** BRL fiscal/political uncertainty has pushed ranges **15–30% above** the historical average used in backtests. The robots' default SL values were calibrated on historical ranges — in a high-volatility regime they become too tight, causing more noise-based stops and degraded win rate.

---

### 2026 SL/TP Adjustment — Recalibrate to Current Ranges

> **Rule:** SL must always equal `historical_multiplier × CURRENT range`. Never use historical SL on a higher-volatility environment.

| Asset | TF | Backtest SL | 2026 Range avg | **2026 Adjusted SL** | **2026 TP (RR=3)** | Min capital for 1 contract |
|-------|----|----|---|---|---|---|
| WDO | 15 min | 20 pts | 17 pts | **25 pts** (+25%) | **75 pts** | R$25k @ 1% / R$12.5k @ 2% |
| WDO | 5 min | 12 pts | 7.5 pts | **15 pts** (+25%) | **45 pts** | R$15k @ 1% / **R$7.5k @ 2%** |
| WIN | 15 min | 822 pts | 480 pts | **960 pts** (+17%) | **2.880 pts** | R$19.2k @ 1% / **R$9.6k @ 2%** |
| WIN | 5 min | 342 pts | 200 pts | **400 pts** (+17%) | **1.200 pts** | **R$8k @ 1%** / R$4k @ 2% |

> **Do NOT reduce SL to get more contracts.** A tighter SL on the same timeframe = more premature stops = lower win rate = negative edge. If capital is the constraint, the solution is a **shorter timeframe** (smaller absolute SL) or **more capital**, never a compressed stop.

---

### How much to adjust and with how many contracts — 2026 guide

**The adjustment is always UPWARD, not downward:**

- Historical SL was calibrated on avg range × multiplier (1.5× WDO, 2.0× WIN)
- In 2026 ranges are ~17–28% larger → apply the **same multiplier to the current range**
- Result: SL increases ~17–28% from the default robot values
- TP follows (RR=3 is maintained)
- Win rate should **improve or stay the same** because SL no longer clips on normal noise

```
2026 recalibration formula:
  SL_2026 = ceil(current_range_avg × multiplier / 5) × 5   ← round to nearest 5pts
  TP_2026 = SL_2026 × 3
  contracts = floor(capital × risk% / (SL_2026 × point_value))
```

**Example with R$10k — 2026 adjusted:**

| Capital | Risk | Asset | TF | SL 2026 | Risk/contract | Contracts |
|---------|------|-------|----|----|---------------|----------|
| R$10k | 1% = R$100 | **WIN** | **5 min** | 400 pts × R$0.20 = **R$80** | R$80 | **1 contract** ✅ |
| R$10k | 2% = R$200 | WIN | 5 min | 400 pts × R$0.20 = R$80 | R$80 | **2 contracts** ✅ |
| R$10k | 2% = R$200 | WDO | 5 min | 15 pts × R$10 = **R$150** | R$150 | **1 contract** ✅ |
| R$10k | 1% = R$100 | WDO | 5 min | 15 pts × R$10 = R$150 | R$150 | 0 contracts ❌ |
| R$10k | 2% = R$200 | WIN | 15 min | 960 pts × R$0.20 = **R$192** | R$192 | **1 contract** ✅ |
| R$10k | 1% = R$100 | WIN | 15 min | 960 pts × R$0.20 = R$192 | R$192 | 0 contracts ❌ |
| R$10k | any | WDO | 15 min | 25 pts × R$10 = R$250 | R$250 | ❌ needs R$12.5k+ |

**Best option in 2026 with R$10k:**

| Rank | Option | SL | Actual risk | Contracts | Notes |
|------|--------|----|------------|-----------|-------|
| 🥇 1st | **WIN 5min @ 1%** | 400 pts · R$80 | R$80 (~0.8%) | 1 | Best risk/reward — WIN exaustão 44.6% win |
| 🥈 2nd | **WIN 5min @ 2%** | 400 pts · R$80 | R$80 | 2 | 2 contracts if you accept 1.6% actual risk |
| 🥉 3rd | **WIN 15min @ 2%** | 960 pts · R$192 | R$192 (~1.9%) | 1 | Fewer trades, more reliable signal |
| 4th | WDO 5min @ 2% | 15 pts · R$150 | R$150 (~1.5%) | 1 | WDO has lower win% than WIN at exhaustion |

---

## Operating Guide — Entry Timing and Candle Management

### "The candle is almost closing with a signal — what do I do?"

**Always wait for the candle to fully close before entering.**

| Scenario | Action |
|----------|--------|
| Signal appears in the last 10–15 seconds of a candle | Let the candle close. Enter at the **next candle's open**. |
| Signal appears mid-candle (first 30%) at extreme force (F > 80) | Entry mid-candle is acceptable — force at extremes rarely reverses before close. |
| You are operating manually | Confirm the close, then place a market order on the new bar. |
| Robot is active | No action needed — Profit robots always act on **bar close** events automatically. |

**Why wait?** In the last seconds of a candle, two things can happen: (1) the candle partially reverses — reducing body/range ratio and dropping the force score — invalidating the signal, (2) other traders exit or enter aggressively at the close, creating momentary slippage. Entry on the next candle's open gives you a confirmed, settled signal.

---

### "How do I manage a trade on candles larger than 10 minutes?"

**Never try to exit within the signal candle on 15min or 30min timeframes.** The strategy uses point-based SL/TP, not time-based exits.

| Timeframe | Entry | Manage | Exit |
|-----------|-------|--------|------|
| 15 min | Enter at **next candle's open** after signal close | Monitor SL (dynamic) and TP in points | Exit at TP hit, SL hit, or opposite-direction force candle |
| 30 min | Same — enter next candle open | Break-even activates after 50% TP distance | Same exit rules |
| 60 min+ | Same — these are swing intraday setups | MaxBarrasEmPosicao = 4–6 recommended | Set a harder daily stop time (e.g., 16h) |

**Key protection mechanisms (automated):**
1. **Break-even**: V11/V14 use `BreakEvenRatio = 0.5`; V16 uses `0.333` plus adaptive triggers by opposite colour and 5 white candles.
2. **Stop candle contra** (`UsarStopCandleContra`): if an opposite-direction force candle at F ≥ 85 appears, position closes immediately — regardless of SL/TP.
3. **Stop horário** (17:45 default): all positions closed before market close.

> On larger candles you have **more time to analyse** but the same point-based logic applies. The robot handles all of this. Manually: watch for an opposite-colour extreme (fúcsia against your long, or cyan against your short) as your exit trigger.

---

## Manual Trading Guide — How to Read the Colours

### INDICADOR_FORCA_V1 — 7-colour paintbar (use this to trade manually)

| Colour | Force | What it means | Manual action |
|--------|-------|----------------|---------------|
| ⬛ **Black/White** | Doji (corpo < 15% range) | Market indecision — body too small to trust | **Skip — do not trade this bar** |
| ⬜ **White** | F = –40% to +40% | No directional force | **Skip** |
| 🩶 **Grey** | F = +40 to +59 (buying) or –40 to –59 (selling) | Weak force — possible early signal | **Watch only — do not enter** |
| 🟢 **Green** | F = +60 to +79 | Strong buying force | **Watch for entry if MTF aligned** |
| 🟦 **Cyan** | F > +80 | Buying exhaustion — momentum at extreme | **Enter long — highest priority; risk of reversal watch** |
| 🔴 **Red** | F = –60 to –79 | Strong selling force | **Watch for entry (short) if MTF aligned** |
| 🩷 **Fuchsia** | F < –80 | Selling exhaustion — momentum at extreme | **Enter short — highest priority** |
| 🟡 **Yellow** | Price in S/R zone, F < threshold | Zone touched, no force yet | **Wait for force confirmation — do not enter** |
| 🟡 **Gold bar (Plot 9)** | Volume > 1.5× average | Institutional activity — volume expressed | **Confirms any signal on the same candle** |

### Multi-Timeframe Alignment Check (mandatory before entry)

Before any entry, verify:
1. **Context TF (largest):** is the EMA slope pointing in your direction?
2. **Direction TF (middle):** same direction as Context?
3. **Trigger TF (current):** force candle in the same direction?

All three aligned = **enter**. Only 2 aligned = **skip or reduce size by 50%**.

---

## Robot Documentation (individual files)

Robot documentation lives in `Robots/`. Older versions have individual `.md` files; V14+ also use shared decision docs.

| Robot | Documentation | Purpose |
|-------|--------------|---------|
| `INDICADOR_FORCA_V1` | [INDICADOR_FORCA_V1.md](Robots/INDICADOR_FORCA_V1.md) | Visual indicator — 7 colours, doji, volume gold |
| `FORCA_WDO_V11` | [FORCA_WDO_V11.md](Robots/FORCA_WDO_V11.md) | WDO-calibrated robot — SL=20, TP=60, RR3 |
| `FORCA_WIN_V11` | [FORCA_WIN_V11.md](Robots/FORCA_WIN_V11.md) | WIN-calibrated robot — SL=822, TP=2466, RR3 |
| `FORCA_WIN_V16` | [MAPA_FORCA_WIN.md](Robots/MAPA_FORCA_WIN.md), [RAID_LOG.md](Robots/RAID_LOG.md), [CHANGELOG.md](Robots/CHANGELOG.md) | Foco atual — alertas de instabilidade, BE adaptativo e trailing proporcional |
| `FORCA_WIN_V14+` | [FORCA_WIN_V14plus.md](Robots/FORCA_WIN_V14plus.md) | Regras compartilhadas V14, V15, V16 e V17 |
| `FORCA_SEMAFORO_V10` | [FORCA_SEMAFORO_V10.md](Robots/FORCA_SEMAFORO_V10.md) | Genérico — 2 tons, SL dinâmico, break-even, qualquer ativo/TF |
| `FORCA_SEMAFORO_CORES_SOM` | [FORCA_SEMAFORO_CORES_SOM.md](Robots/FORCA_SEMAFORO_CORES_SOM.md) | Referência — v9 degradê, **não modificar** |

---

## Methodology

**Entry criteria (confluence obrigatória):**
1. Bias diário (1D) alinhado com a direção da operação — manual, antes de abrir o Profit
2. Contexto (TF maior: 60min) na mesma direção — `bCtxAlta` ou `bCtxBaixa` true
3. Direção (TF médio: 30min) confirmada — `bDirAlta` ou `bDirBaixa` true
4. Gatilho (TF de execução: 10min ou 15min) com F ≥ 70 (forte) ou F ≥ 85 (exaustão)
5. Volume ≥ mínimo configurado no robot (`VolumeMinimo`)

> Os itens 2, 3, 4 e 5 são verificados automaticamente pelo robot a cada candle fechado.
> O item 1 (bias 1D) é avaliação manual prévia à sessão.

**Timeframes em uso (tela operacional):**

| TF | Papel | Configuração no robot |
|----|-------|-----------------------|
| 1D | Bias diário — manual | Não entra no robot; define se aceita só LONG ou só SHORT |
| 60min | Contexto institucional | `iJanelaCtx = 6` (em gráfico 10min) ou `iJanelaCtx = 4` (em 15min) |
| 30min | Direção confirmada | `iJanelaDir = 3` (em gráfico 10min) ou `iJanelaDir = 2` (em 15min) |
| 20min | Confirmação visual auxiliar | Não é parâmetro do robot — use visualmente entre 10min e 30min |
| 15min | Gatilho (tripleta 60/30/15) | TF de execução do gráfico |
| 10min | Gatilho (tripleta 60/30/10) | TF de execução do gráfico |
| 5min | Gatilho (tripleta 30/15/5) | TF de execução — mais operações, SL menor |

**Gerenciamento de risco:**
- Risco máximo por trade: 1–2% do capital (ver tabela de sizing acima)
- SL dinâmico: `max(StopMinimo, range_candle × FatorRangeSL)`
- Break-even automático: V11/V14 usam `BreakEvenRatio=0.5`; V16 usa `0.333` e gatilhos adaptativos
- Stop candle contra: fecha posição se exaustão contrária (F ≥ 85) aparecer
- Stop horário: 17h45 — fecha tudo antes do fechamento do mercado
- Limite diário: 3% de drawdown → encerrar sessão manualmente

---

## Connection to PriceAction_Fisica

This repository is the applied trading layer of the theoretical framework developed in [PriceAction_Fisica](https://github.com/wesleyzilva/PriceAction_Fisica):

```
PriceAction_Fisica
    └─► defines physics concepts (F=MA, velocity, momentum, inertia)
    └─► documents theory and formulas

TradeTech (this repository)
    └─► implements those concepts as indicators and robots
    └─► backtests and validates against real market data
    └─► builds operational trading methodology
```

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Neologica NTSL](https://img.shields.io/badge/Neologica-NTSL-1B2A4A?style=flat-square)
![Neologica NTFL](https://img.shields.io/badge/Neologica-NTFL-2C3E50?style=flat-square)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![B3 WIN](https://img.shields.io/badge/B3-WIN%20%7C%20WDO-003087?style=flat-square)

---

## Disclaimer

> This repository is a **personal research and study project**. Nothing here constitutes financial advice or a trading recommendation. All backtests are historical and do not guarantee future results. Trade at your own risk.

---

## Author

**Wesley Gomes da Silva** · IT Manager · Agile Coach · Daytrade Researcher

[GitHub](https://github.com/wesleyzilva) · [LinkedIn](https://www.linkedin.com/in/wesleyzilva/) · [Portfolio](https://wesleyzilva.github.io/portfolioNearshoreWesIA/?utm_source=github&utm_medium=repo&utm_campaign=tradetech&utm_content=readme_footer)
