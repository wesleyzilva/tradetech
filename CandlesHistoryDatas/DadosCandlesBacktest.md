# DadosCandlesBacktest — Dataset de Candles WIN / WDO

> Dados históricos exportados da plataforma **Neologica Profit** para backtesting dos robôs da série `FORCA_*`.

---

## Estrutura de Pastas

```
DadosCandlesBacktest/
├── 2012_14/      ← candles 2012–2014
├── 2014_16/      ← candles 2014–2016
├── 2016_18/      ← candles 2016–2018
├── 2018_20/      ← candles 2018–2020
├── 2020_22/      ← candles 2020–2022
├── 2022_24/      ← candles 2022–2024
└── 2024_26/      ← candles 2024–2026
```

---

## Formato dos Arquivos CSV

| Campo | Coluna | Tipo | Obs |
|---|---|---|---|
| Ativo | col[0] | string | Ex: `WDOFUT`, `WINFUT` |
| Data | col[1] | `DD/MM/YYYY` | dayfirst=True |
| Hora | col[2] | `HH:MM` | combinado com Data |
| Open | col[3] | float | separador `,` |
| High | col[4] | float | |
| Low | col[5] | float | |
| Close | col[6] | float | |
| Volume | col[7] | int | |

- Separador de campo: `;`
- Separador decimal: `,`
- Encoding: `latin1`
- Separador de milhar: `.`

Padrão de nome: `*WD*_15min.csv` (WDO) / `*WI*_15min.csv` (WIN)

---

## Timeframes Disponíveis

| TF | Duração | Uso |
|---|---|---|
| `2min` | 2 min | Refinamento de gatilho |
| `5min` | 5 min | Operacional rápido |
| `15min` | 15 min | Operacional principal |
| `30min` | 30 min | Direção intraday |
| `60min` | 60 min | Contexto intraday |
| `diario` | 1 dia | Contexto estrutural |

---

## Volume de Dados (estimativa)

| Ativo | TF | Período | Candles aprox. |
|---|---|---|---|
| WDO | 15min | 2020–2026 | ~47.786 |
| WIN | 15min | 2020–2026 | ~47.787 |
| WDO | 5min | 2020–2026 | ~143.000 |
| WIN | 5min | 2020–2026 | ~143.000 |

---

## Scripts de Análise

| Script | Descrição | Uso |
|---|---|---|
| `analise_forca_sl.py` | Análise estatística completa: distribuição F, SL ótimo, MTF | `python analise_forca_sl.py` |
| `tabela_cenarios.py` | Comparação de cenários de entrada (verde/fúcsia, sequências) | `python tabela_cenarios.py` |
| `detector_areas.py` | Detecção automática de áreas S/R (implementa `instructions.md`) | `python detector_areas.py` |

---

## Parâmetros Calibrados (backtest 2020–2026)

| Ativo | TF | SL (pts) | TP (pts) | RR | Win% médio |
|---|---|---|---|---|---|
| WDO | 15min | 20 | 60 | 3.0 | 39–42% |
| WIN | 15min | 822 | 2466 | 3.0 | 43–47% |
| WDO | 5min | 12 | 36 | 3.0 | 39–42% |
| WIN | 5min | 342 | 1026 | 3.0 | 39–41% |

---

## Fórmula de Força

```
F = (Corpo / Range) × (Volume / MediaVolume) × 100
```

| Valor | Cor | Interpretação |
|---|---|---|
| F ≥ 85 | 🟣 Fúcsia | Exaustão compradora |
| 70 ≤ F < 85 | 🟢 Verde | Forte comprador |
| −85 < F ≤ −70 | 🔴 Vermelho | Forte vendedor |
| F ≤ −85 | 🟠 Laranja | Exaustão vendedora |
| \|F\| < 70 | ⚪ Branco | Sem sinal |

---

_Atualizado: 2026-05  |  Fonte: Neologica Profit export_
