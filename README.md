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
| `FORCA_WIN_V16` | **WIN** | **15min** MA5/MA20 | **75 pts** | **150 pts** | **2.0** | ✅ `ratio=0.333` + adaptativo | 🧪 swing curto, não rebacktestado |
| **`FORCA_WIN_V16_scalper_sinaisForca`** | **WIN** | **5min** | **280 pts** | **560** (forte) / **840** (exaustão) | **2.0 / 3.0** | ✅ `ratio=0.333` + adaptativo | 🎯 **FOCO ATUAL — ✅ backtest 50k candles 2024–26** |
| `FORCA_WIN_V17_sinaisForcaComMedias` | **WIN** | 15min | **150 pts** | **1500 pts** | ~10 | ✅ 75 pts absolutos | ⚠️ experimental |

---

## Robot Comparison — How They Differ

All robots share the same core formula **F = M × A**. What differs is **when to enter**, **how much to risk**, and **which asset they are calibrated for**.

| Robot | Asset | Entry filter | Break-even | RR | Observação |
|-------|-------|-------------|------------|-----|------------|
| `FORCA_SEMAFORO_CORES_SOM` | WDO/WIN | F ≥ 55 degradê | ❌ não tem | config | Referência visual — **não modificar** |
| `FORCA_SEMAFORO_V10` | qualquer | F ≥ 55 ou F ≥ 70 (toggle) | ✅ `BreakEvenRatio=0.5` | config | Genérico — configure por ativo/TF |
| `FORCA_WDO_V11` | WDO | F ≥ 70 (fraco descartado) | ✅ `BreakEvenRatio=0.5` | **3.0** | 47.786 candles · win 39.5% |
| `FORCA_WIN_V11` | WIN | F ≥ 70 (fraco descartado) | ✅ `BreakEvenRatio=0.5` | **3.0** | Baseline estatístico; exaustão win 44.6% |
| `FORCA_WIN_V16` | WIN 15min | F ≥ 70 no 1º candle + MA5/MA20 + volume | ✅ `0.333` + cor oposta + 5 brancos | **2.0** | Swing curto; não rebacktestado |
| **`FORCA_WIN_V16_scalper_sinaisForca`** | **WIN 5min** | **F ≥ 70 no 1º candle + volume direcional** | ✅ **`0.333` + cor oposta + 5 brancos** | **2.0 (forte) / 3.0 (exaustão)** | 🎯 **FOCO ATUAL — WR 40.3% · +38.843 pts · 50k candles** |
| `INDICADOR_FORCA_V1` | visual | — | — | — | 7 cores + zona S/R + gold volume |

> **Break-even:** V11/V14 usam `BreakEvenRatio=0.5`. O scalper e V16 usam `BreakEvenRatio=0.333` + gatilhos adaptativos (cor oposta e 5 candles brancos).

---

## Current Focus — FORCA_WIN_V16_scalper_sinaisForca

`Robots/FORCA_WIN_V16_scalper_sinaisForca` é o robô operacional atual para WIN scalp em 5 minutos. Backtest validado em **50.000 candles 2024–2026**: WR 40.3% · BE em 25.0% das operações · PnL **+38.843 pts**.

> ⚠️ **Comparação direta do backtest:** `SL=280 TP=840 MAX=12` → **+38.843 pts (positivo)**. Os parâmetros antigos V16 15min (`SL=75 TP=188 MAX=6`) testados no 5min deram −21.446 pts. Use o scalper para 5min, o V16 somente para 15min.

### Como funciona

1. **Força (F = M × A):** `F = ((Close−Open)/(High−Low)) × (Volume/MediaVolume(20)) × 100`, limitado a [−100, +100].
2. **Zonas e cores (3 níveis por lado):**
   | Zona | Compra | Venda | Ação |
   |------|--------|-------|------|
   | Chegando `55–70` | 🟩 verde claro `RGB(210,255,210)` | 🟥 rosa claro `RGB(255,220,220)` | alerta visual, sem entrada |
   | Forte `70–85` | 🟢 verde médio `RGB(120,220,120)` | 🔴 vermelho médio `RGB(255,120,120)` | entrada com TP2=560 (RR 2.0) |
   | Exaustão `≥85` | 💚 verde escuro `RGB(0,150,0)` | 🔴 vermelho escuro `RGB(180,0,0)` | entrada com TP3=840 (RR 3.0) |
   | Instabilidade | 🔵 cyano `RGB(0,220,220)` | 🟣 fúcsia `RGB(255,0,180)` | override visual: ≥3 trocas de zona em 5 candles |
3. **Alerta sonoro no sinal:** toca no 1º candle que entra na zona operacional (F ≥ 70), independentemente de posição ou modo de operação.
4. **Gatilho de entrada:** `fForca >= 70 AND fForca[1] < 70` (1º candle da força) + `fCorpo > 0 AND Volume >= MediaVolume(20)` (compra); simétrico para venda.
5. **TP dinâmico por zona:** exaustão (F ≥ 85) → TP3 = 840 pts (RR 3.0); forte (70–85) → TP2 = 560 pts (RR 2.0).
6. **Gestão de risco:** SL=280 pts · BE em 33% do TP ativo · trailing proporcional 62% após BE · máximo 12 barras (60 min).

### Manual de operação — passo a passo

| Etapa | Regra prática |
|---|---|
| **Antes da sessão** | Identificar viés do dia (1D): LONG somente, SHORT somente, ou neutro |
| **Configuração de tela** | Abrir 2 gráficos WIN: **5min** com scalper ativo + **15min** com INDICADOR_FORCA_V1 (confirma cor MTF) |
| **Confirmação multi-TF** | Beep+cor no 5min **E** cor alinhada no 15min = alta confiança para scalp; beep só no 5min = aguardar |
| **Entrada automática** | Com `HabilitarOperacoes=true` o robô entra sozinho no 1º candle forte; confirme que viés do dia está alinhado |
| **TP ativo** | Exaustão (verde escuro / vermelho escuro) → TP=840; forte → TP=560 — robô já seleciona automaticamente |
| **Não mover SL manualmente** | Deixar BE, trailing e stop por cor oposta trabalharem; intervenção manual destrói a estatística do backtest |
| **Saída antecipada** | BE arma se lucro ≥ 33% do TP, candle fecha cor oposta, ou 5 brancos consecutivos |
| **Encerramento da sessão** | Stop horário 17:45 fecha tudo automaticamente; máx 12 barras em posição |
| **Após a sessão** | Registrar: zona de entrada, TP selecionado, motivo de saída (TP/SL/BE/candle contra/horário) |

### Cadeia de saídas (ordem de prioridade)

```
1. Hard SL intrabar — Low cai abaixo da entrada − 280 pts
2. Stop candle contra — forca oposta >= 70 fecha a posição
3. BE por cor oposta — candle fecha na cor contrária
4. BE por 5 brancos — 5 candles consecutivos sem força
5. BE clássico — lucro >= 33% do TP ativo (186 ou 280 pts)
6. Trailing proporcional — passo = 62% da distância restante ao TP (piso 10%)
7. Take Profit hard — 560 pts (forte) ou 840 pts (exaustão)
8. Max barras — 12 candles × 5min = 60 min máximo
9. Stop horário — 17h45
```

### Sizing com R$10k — 2026

| Capital | Risco | SL | Risco/contrato | Contratos |
|---------|-------|----|---------------|-----------|
| R$10k | 1% = R$100 | 280 pts × R$0.20 = R$56 | R$56 | **1 contrato** ✅ |
| R$10k | 2% = R$200 | 280 pts × R$0.20 = R$56 | R$56 | **3 contratos** ✅ |

> Com `CapitalReais=10000`, `RiscoPorcentagem=1`, `SL=280`, `PontoValorReais=0.20` → `iQtd = 1` contrato. O robô calcula mas a quantidade é configurada no contrato da plataforma.

### Status dos gaps

| ID | Item | Status |
|---|---|---|
| G01 | Backtest V16 scalper 50k candles 2024–26 | ✅ Resolvido — WR 40.3%, PnL +38.843 pts |
| G02 | `iQtd` calculado mas não passado para a ordem | ⚠️ Aberto — usar quantidade do contrato na plataforma enquanto `BuyAtMarket(n)` não é confirmado |
| G03 | Janela de instabilidade por bloco (não deslizante) | 🟡 Aceitável para operação atual |
| G04 | Alerta de mudança tardia (`UsarAlertaMudancaTardia=false`) | 🟡 Desligado intencionalmente |
| G05 | `fForcaAnterior` atribuído mas não usado | 🟡 Dead code sem impacto operacional |

---

### Key decision: which robot to use?

```
Análise visual / aprendizado
  └─► INDICADOR_FORCA_V1 — entender o sistema de cores sem enviar ordens

Qualquer ativo ou TF personalizado
  └─► FORCA_SEMAFORO_V10 — configure SL/TP/thresholds por ativo

WDO (mini-dólar) — execução automática
  └─► FORCA_WDO_V11
        15min (tripleta 60/30/15): iJanelaDir=2 · iJanelaCtx=4 · SL=20 · TP=60
         5min (tripleta 30/15/5) : iJanelaDir=3 · iJanelaCtx=6 · SL=12 · TP=36

WIN (mini-índice) — execução automática
  ├─► FORCA_WIN_V11 — baseline estatístico calibrado
  │     15min: SL=822 · TP=2466 · RR 3.0 · exaustão win 44.6%
  │
  ├─► FORCA_WIN_V16 — swing curto 15min (não rebacktestado)
  │     MA5/MA20 · SL=75 · TP=150 · BE=33% + adaptativo
  │
  └─► 🎯 FORCA_WIN_V16_scalper_sinaisForca — SCALP 5MIN (foco atual)
        SL=280 · TP2=560 (forte/RR2) · TP3=840 (exaustão/RR3)
        BE=33% do TP ativo + cor oposta + 5 brancos · MAX=12 barras
        Backtest: WR 40.3% · PnL +38.843 pts · 50k candles 2024–26
        Multi-TF: rodar junto com INDICADOR_FORCA_V1 no 15min
                  beep+cor simultâneos nos 2 TFs = alta confiança para o scalp
```

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

## Operating Guide — Scalp 5min (FORCA_WIN_V16_scalper_sinaisForca)

### Configuração de tela recomendada

| Gráfico | Robô / Indicador | Papel |
|---------|-----------------|-------|
| WIN 5min | `FORCA_WIN_V16_scalper_sinaisForca` com `HabilitarOperacoes=true` | Execução e alerta sonoro no sinal |
| WIN 15min | `INDICADOR_FORCA_V1` (sem ordens) | Confirmação visual MTF — cor do contexto |

> **Regra multi-TF:** beep no 5min **E** candle de cor forte/exaustão alinhado no 15min = entrada com alta confiança. Beep sem alinhamento no 15min = operação de menor confiança (considere reduzir tamanho ou aguardar).

---

### "O candle está quase fechando com sinal — o que eu faço?"

**Aguarde sempre o fechamento do candle.**

| Cenário | Ação |
|---------|------|
| Sinal aparece nos últimos 10–15s | Deixe fechar. O robô entra automaticamente no **próximo candle**. |
| Sinal aparece no início do candle (F > 80 logo de cara) | Entrada mid-candle é aceitável — exaustão extrema raramente reverte antes do fechamento. |
| Operação manual | Confirme o fechamento e mande ordem a mercado no início da nova barra. |
| Robô ativo | Nenhuma ação — NTSL sempre age no evento de **fechamento de candle**. |

---

### "Como gerenciar a posição no scalp 5min?"

| Etapa | Regra |
|-------|-------|
| Entrada | O robô seleciona TP automaticamente: F ≥ 85 → TP3=840 pts; F 70–84 → TP2=560 pts |
| Após abertura | Não mover SL manualmente — o BE automático assume quando lucro ≥ 33% do TP |
| Cor oposta no 5min | O robô fecha sozinho (stop candle contra ou BE por cor) |
| Lateralização | 5 candles brancos consecutivos → BE armado automaticamente |
| Trailing | Entra após BE; passo = 62% da distância restante ao TP (piso 10%) |
| Saída forçada | 12 barras (60 min) ou 17h45 — o que vier primeiro |

**Mecanismos de proteção automáticos (ordem de prioridade):**
1. Hard SL intrabar — `Low ≤ entrada − 280` ou `High ≥ entrada + 280`
2. Stop candle contra — F oposto ≥ 70 fecha posição imediatamente
3. BE por cor oposta — candle fecha na cor contrária à posição
4. BE por 5 brancos consecutivos — lateralização longa
5. BE clássico — lucro ≥ 33% do TP ativo (186 ou 280 pts)
6. Trailing proporcional — aperta após BE, protege lucros crescentes
7. TP hard — 560 ou 840 pts conforme zona de entrada
8. Max barras 12 → stop horário 17h45

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
| `INDICADOR_FORCA_V1` | [INDICADOR_FORCA_V1.md](Robots/INDICADOR_FORCA_V1.md) | Visual indicator — 7 cores, doji, volume gold |
| `FORCA_WDO_V11` | [FORCA_WDO_V11.md](Robots/FORCA_WDO_V11.md) | WDO-calibrated robot — SL=20, TP=60, RR3 |
| `FORCA_WIN_V11` | [FORCA_WIN_V11.md](Robots/FORCA_WIN_V11.md) | WIN-calibrated robot — SL=822, TP=2466, RR3 |
| **`FORCA_WIN_V16_scalper_sinaisForca`** | [MAPA_FORCA_WIN.md](Robots/MAPA_FORCA_WIN.md), [RAID_LOG.md](Robots/RAID_LOG.md), [CHANGELOG.md](Robots/CHANGELOG.md) | 🎯 **FOCO ATUAL** — scalp 5min, SL=280, TP2/3 dinâmico, alertas multi-nível, BE adaptativo |
| `FORCA_WIN_V16` | [FORCA_WIN_V14plus.md](Robots/FORCA_WIN_V14plus.md) | Swing curto 15min — MA5/MA20, SL=75, TP=150 |
| `FORCA_WIN_V14+` | [FORCA_WIN_V14plus.md](Robots/FORCA_WIN_V14plus.md) | Regras compartilhadas V14, V15, V16 e V17 |
| `FORCA_SEMAFORO_V10` | [FORCA_SEMAFORO_V10.md](Robots/FORCA_SEMAFORO_V10.md) | Genérico — 2 tons, SL dinâmico, break-even, qualquer ativo/TF |
| `FORCA_SEMAFORO_CORES_SOM` | [FORCA_SEMAFORO_CORES_SOM.md](Robots/FORCA_SEMAFORO_CORES_SOM.md) | Referência — v9 degradê, **não modificar** |

---

## Methodology

**Critérios de entrada (confluência obrigatória):**
1. Bias diário (1D) alinhado com a direção — avaliação manual antes de abrir o Profit
2. Contexto no 15min alinhado — `INDICADOR_FORCA_V1` no 15min pintando na mesma cor
3. Gatilho no 5min com F ≥ 70 (forte) ou F ≥ 85 (exaustão) — 1º candle que cruza o limiar
4. Volume direcional — `fCorpo > 0 AND Volume ≥ MediaVolume(20)` (compra); simétrico venda

> Itens 3 e 4 são verificados automaticamente pelo scalper. Itens 1 e 2 são avaliação manual prévia.

**Timeframes em uso:**

| TF | Papel | Como usar |
|----|-------|-----------|
| 1D | Bias diário — manual | Define se aceita só LONG, só SHORT ou neutro na sessão |
| 15min | Contexto / confirmação MTF | INDICADOR_FORCA_V1 (sem ordens) — cor alinhada reforça o sinal 5min |
| 5min | Gatilho — execução | `FORCA_WIN_V16_scalper_sinaisForca` — beep+cor + ordem automática |

**Gerenciamento de risco:**
- Risco máximo por trade: 1–2% do capital
- SL fixo: 280 pts = R$56/contrato (1.5× range médio 5min 2026 ~187 pts)
- TP dinâmico: forte (70–85) → TP=560 pts (RR 2.0); exaustão (≥85) → TP=840 pts (RR 3.0)
- Break-even: 33% do TP ativo + gatilhos adaptativos (cor oposta / 5 brancos)
- Stop candle contra: fecha se força oposta ≥ 70 aparecer
- Stop horário: 17h45 — fecha tudo antes do fechamento do mercado
- Limite diário sugerido: 3% de drawdown → encerrar sessão manualmente

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
