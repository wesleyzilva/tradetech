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

| Score range | Colour | Interpretation |
|-------------|--------|----------------|
| > +80% | 🟢 Green | Maximum buying force |
| +60% to +79% | 🔵 Cyan | Strong buying |
| +40% to +59% | 🟨 Yellow | Weak buying |
| -15% to +15% | ⚫ Grey | No directional force |
| -40% to -59% | 🟫 Brown | Weak selling |
| < -80% | 🔴 Red | Maximum selling force |

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

| Robot | Strategy | Language | Status |
|-------|----------|--------|
| `FORCA_SEMAFORO_CORES_SOM` | F=MA rainbow semaphore, 6 colours | NTSL | ✅ v9.0 |
| `FORCA_SEMAFORO_V10` | 2-tone (forte+exaustão), dynamic SL, break-even | NTSL | ✅ Backtested |
| `FORCA_WDO_V11` | WDO-calibrated: SL=20, TP=60, RR=3, 4 colours | NTSL | ✅ Calibrated |
| `FORCA_WIN_V11` | WIN-calibrated: SL=822, TP=2466, RR=3, 4 colours | NTSL | ✅ Calibrated |
| `SCALPER_ZONA_V1` | Zone S/R + Force (F≥55) confirmation, RR=2 | NTSL | 🔄 In testing |
| `IFR_reversal` | RSI reversal at structure support/resistance | NTSL | 🔲 Planned |
| `VWAP_pullback` | Pullback to VWAP in trending session | NTSL | 🔲 Planned |

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

## Methodology

**Entry criteria (minimum confluence required):**
1. Trend alignment on 3 timeframes (15m · 60m · daily)
2. Price at a significant structure level (support, resistance, VWAP)
3. Force score ≥ +60% or ≤ -60% on the trigger candle
4. Volume ≥ 1.2× average at entry bar

**Risk management:**
- Maximum risk per trade: 1% of capital
- Stop placement: below/above nearest structure with ATR buffer
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
