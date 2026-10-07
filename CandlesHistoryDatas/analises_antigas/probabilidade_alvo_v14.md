# Probabilidade de Alvo — FORCA_WIN_V14

> Gerado em 2026-05-15 09:16 | Dados: WIN 15min 2024-2026
> Parametros V14: SL=822 pts | TP=2466 pts | RR 3.0x | BE em 1233 pts

---

## 1. Resumo dos Sinais V14 Detectados

| Metrica | Valor |
|---|---|
| Total de sinais detectados | **234** |
| Sinais LONG | 121 |
| Sinais SHORT | 113 |
| TP atingido | 68 (29.1%) |
| SL atingido | 139 (59.4%) |
| Break-even | 25 (10.7%) |
| Timeout (80c) | 2 (0.9%) |
| Win rate total (TP+BE) | **39.7%** |
| AvgWin (pts) | 2438 |
| AvgLoss (pts) | -818 |
| Payoff ratio | 2.98x |
| EV por trade (pts) | **230** |
| EV por trade (R$ x1c) | **R$ 45.95** |
| Mediana candles ate resolucao | 10.0 |

---

## 2. Probabilidade de Atingir Cada Alvo

> **P(MFE≥X)**: o preco chegou ate X pts de lucro a qualquer momento (independente do desfecho).
> **P(X antes SL)**: simulacao completa — X atingido ANTES do SL de 822 pts ser tocado.
> **EV**: esperanca matematica se usado como TP fixo com SL=822 pts.

| Alvo (pts) | RR | P(MFE≥X) | P(X antes SL) | EV (pts) | EV (R$/1c) |
|---:|---:|---:|---:|---:|---:|
| 200 | 0.24 | 81.2% | 81.2% | 8 | R$ 1.57 |
| 400 | 0.49 | 66.2% | 66.2% | -13 | R$ -2.51 |
| 600 | 0.73 | 58.5% | 58.5% | 11 | R$ 2.11 |
| 822 ◄ SL | 1.0 | 53.0% | 53.0% | 49 | R$ 9.84 |
| 1000 | 1.22 | 48.7% | 48.7% | 66 | R$ 13.13 |
| 1233 ◄ BE | 1.5 | 44.9% | 44.9% | 100 | R$ 20.02 |
| 1500 | 1.82 | 41.9% | 41.9% | 150 | R$ 30.09 |
| 2000 ◄ MELHOR | 2.43 | 34.6% | 36.8% | 215 | R$ 43.03 |
| 2466 ◄ V14 | 3.0 | 29.1% | 30.8% | 190 | R$ 37.94 |
| 3000 | 3.65 | 3.8% | 25.6% | 158 | R$ 31.60 |

---

## 3. Distribuicao MAE — Calibracao do SL

> MAE = maximo movimento adverso em qualquer ponto do trade (antes de resolucao).

| Percentil | MAE (pts) | Interpretacao |
|---:|---:|---|
| P50 | 875.0 | Metade dos trades nunca ultrapassam este adverso |
| P70 | 1030.0 | 70% sobrevivem com SL acima deste valor |
| P80 | 1135.0 | SL conservador — protege 80% dos trades |
| P90 | 1350.0 | SL muito conservador — poucos stops prematuros |
| P95 | 1715.0 | SL extremamente largo |

> SL atual V14: **822 pts** → cobre ~41% dos trades sem parar prematuramente.

---

## 4. Distribuicao MFE — Potencial de Ganho

> MFE = maximo movimento favoravel registrado durante o trade.

| Percentil | MFE (pts) | Interpretacao |
|---:|---:|---|
| P25 | 258.0 | 1/4 dos trades mal chegam aqui |
| P50 | 940.0 | Mediana do ganho potencial |
| P70 | 2420.0 | 70% dos trades alcancam este nivel |
| P80 | 2535.0 | TP conservador — capturado em 80% |
| P90 | 2747.0 | TP agressivo — capturado em 10% |

---

## 5. Analise RR e Recomendacao

### RR com maior EV encontrado nos dados

- **Alvo otimo**: 2000 pts
- **RR**: 2.43x
- **P(win)**: 36.8%
- **EV por trade**: 215 pts | R$ 43.03 x1c

### Comparativo V14 parametros atuais

- **TP atual (V14)**: 2466 pts | RR 3.0x
- P(win): 30.8%
- EV: 190 pts | R$ 37.94

### Conclusao

> ⚠ **O alvo otimo (2000 pts / RR 2.43x) supera o V14 (2466 pts / RR 3.0x) em EV por mais de 10%.**
> Considerar ajuste do TP em V15.

---

## 6. Notas Metodologicas

- **Dados**: WIN 15min, contratos continuos e correntes (WINFUT + WINJ26 + WINM26).
- **Sinal V14**: F >= 70 (LONG) ou F <= -70 (SHORT), primeiro candle da sequencia (F[1] fora da zona), MTF alinhado (SMA 2/4), Volume >= 5000.
- **Simulacao**: candle a candle, pessimista (SL dispara antes de TP se ambos no mesmo candle).
- **Break-even**: Close retorna ao entry apos MFE >= 1233 pts.
- **P(X antes SL)**: simulacao independente por cada nivel de TP — nao usa BE.
- **Timeout**: trades nao resolvidos em 80 candles sao fechados pelo Close — contados como loss na tabela RR.
- **Limitacao**: SMA aproxima Media() do NTSL. Resultado pode variar ~5-10% vs backtest nativo.
