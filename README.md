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

| Robot | Strategy | Language | Status |
|-------|----------|----------|--------|
| `FORCA_SEMAFORO_CORES_SOM` | F=MA rainbow semaphore, 6 colours | NTSL | ✅ v9.0 |
| `FORCA_SEMAFORO_V10` | 2-tone (forte+exaustão), dynamic SL, break-even | NTSL | ✅ Backtested |
| `FORCA_WDO_V11` | WDO-calibrated: SL=20, TP=60, RR=3, 4 colours | NTSL | ✅ Calibrated |
| `FORCA_WIN_V11` | WIN-calibrated: SL=822, TP=2466, RR=3, 4 colours | NTSL | ✅ Calibrated |
| `SCALPER_ZONA_V1` | Zone S/R + Force (F≥55) confirmation, RR=2 | NTSL | 🔄 In testing |
| `IFR_reversal` | RSI reversal at structure support/resistance | NTSL | 🔲 Planned |
| `VWAP_pullback` | Pullback to VWAP in trending session | NTSL | 🔲 Planned |

---

## Robot Comparison — How They Differ

All robots share the same core formula **F = M × A**. What differs is **when to enter**, **how much to risk**, and **which asset they are calibrated for**.

| Robot | Asset | Entry filter | Colours | SL logic | RR | Special |
|-------|-------|-------------|---------|----------|----|--------|
| `FORCA_SEMAFORO_CORES_SOM` | WDO/WIN | F ≥ threshold (rainbow) | 6-colour gradient | fixed | configurable | **Reference only — do not modify** |
| `FORCA_SEMAFORO_V10` | Any (generic) | F ≥ 55 (fraco) or F ≥ 70 (forte) | 2-tone: verde claro+escuro / verm claro+escuro | dynamic: max(fixo, range×0.75) | configurable | `EntrarSomenteForte` toggle — adaptable to any asset |
| `FORCA_WDO_V11` | **WDO only** | F ≥ 70 (zona fraca descartada) | Verde / Cyan / Verm / Fúcsia | dynamic: max(20, range×1.5) | **3.0** | Calibrated on 47,786 candles 2012–2026 |
| `FORCA_WIN_V11` | **WIN only** | F ≥ 70 (zona fraca descartada) | Verde / Cyan / Verm / Fúcsia | dynamic: max(822, range×2.0) | **3.0** | Best backtest: exaustão 44.6% win, RR3 |
| `SCALPER_ZONA_V1` | WDO/WIN | F ≥ 55 **inside S/R zone only** | Verde / Fúcsia / Amarelo (zona) | dynamic: max(zona, range×1.2) | **2.0** | Quality > quantity; max 8 candles held |
| `INDICADOR_FORCA_V1` | Visual only | — | 7 cores + amarelo + gold volume | — | — | Companion visual for all NTSL robots |

### Key decision: which robot to use?

```
Manual trading / learning phase
  └─► INDICADOR_FORCA_V1 (visual only) — understand the colour system first

Generic or custom asset
  └─► FORCA_SEMAFORO_V10 — configure SL/TP/thresholds per asset

WDO (mini-dollar) — automated execution
  └─► FORCA_WDO_V11 — pre-calibrated, SL=20pts, TP=60pts

WIN (mini-index) — automated execution
  └─► FORCA_WIN_V11 — pre-calibrated, SL=822pts, TP=2466pts

Conservative / zone-based
  └─► SCALPER_ZONA_V1 — fewer trades, higher confidence, shorter hold
```

### Colour consistency rule

All V11 robots and INDICADOR_FORCA_V1 use the **same RGB values**:
- 🟢 Verde escuro `RGB(0,180,0)` — forte (F ≥ 70)
- 🟦 Cyan `RGB(0,220,220)` — exaustão compradora (F ≥ 85)
- 🔴 Vermelho `RGB(200,0,0)` — forte (F ≤ –70)
- 🩷 Fúcsia `RGB(255,0,180)` — exaustão vendedora (F ≤ –85)

SEMÁFORO_V10 uses its own 2-tone scheme (verde claro/escuro, verm claro/escuro) — **this is intentional and correct**.

---

## Study Structure

```
tradetech/
├── robos/                         NTSL/NTFL robot and indicator source code
│   ├── FORCA_SEMAFORO_CORES_SOM   v9.0 — original rainbow semaphore (WDO/WIN)
│   ├── FORCA_SEMAFORO_V10         v10  — 2 tones, dynamic SL, break-even
│   ├── FORCA_WDO_V11              v11  — WDO-calibrated (SL=20, TP=60, RR3)
│   ├── FORCA_WIN_V11              v11  — WIN-calibrated (SL=822, TP=2466, RR3)
│   └── SCALPER_ZONA_V1            v1   — Zone S/R + Force confirmation scalper
├── DadosCandlesBacktest/          Raw CSVs (WIN/WDO 2012–2026, multi-TF)
│   ├── detector_areas.py          Detects S/R zones from candle data
│   ├── analise_forca_sl.py        Full statistical analysis (zone dist., SL grid)
│   ├── tabela_cenarios.py         Entry sequence comparison (verde/fúcsia)
│   ├── instructions.md            Agent spec for zone detection
│   └── DadosCandlesBacktest.md    Dataset documentation
├── teoria/                        Theory notes — Dow, Price Action, indicators
├── indicadores/                   Custom indicator logic and formulas
├── anotacoes/                     Session review notes — what worked, what failed
├── referencias/                   External papers, books, and resources
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
1. **Break-even** (`BreakEvenRatio = 0.5`): after price moves 50% toward TP, SL moves to entry price → trade becomes risk-free.
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

Each robot has its own `.md` file in `robos/`:

| Robot | Documentation | Purpose |
|-------|--------------|---------|
| `INDICADOR_FORCA_V1` | [INDICADOR_FORCA_V1.md](robos/INDICADOR_FORCA_V1.md) | Visual indicator — 7 colours, doji, volume gold |
| `FORCA_WDO_V11` | [FORCA_WDO_V11.md](robos/FORCA_WDO_V11.md) | WDO-calibrated robot — SL=20, TP=60, RR3 |
| `FORCA_WIN_V11` | [FORCA_WIN_V11.md](robos/FORCA_WIN_V11.md) | WIN-calibrated robot — SL=822, TP=2466, RR3 |
| `FORCA_SEMAFORO_V10` | [FORCA_SEMAFORO_V10.md](robos/FORCA_SEMAFORO_V10.md) | 2-tone semaphore, dynamic SL, break-even |
| `SCALPER_ZONA_V1` | [SCALPER_ZONA_V1.md](robos/SCALPER_ZONA_V1.md) | Zone S/R + force confirmation scalper |
| `FORCA_SEMAFORO_CORES_SOM` | [FORCA_SEMAFORO_CORES_SOM.md](robos/FORCA_SEMAFORO_CORES_SOM.md) | Reference robot — v9 rainbow semaphore |

---

## Methodology

**Entry criteria (minimum confluence required):**
1. Trend alignment on 3 timeframes (15m · 60m · daily)
2. Price at a significant structure level (support, resistance, VWAP)
3. Force score ≥ +60% or ≤ -60% on the trigger candle
4. Volume ≥ 1.2× average at entry bar

**Risk management:**
- Maximum risk per trade: 1–2% of capital (see sizing table above)
- Stop placement: dynamic — SL = max(StopMinimo, range × FatorRangeSL)
- Daily loss limit: 3% → session ends

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
