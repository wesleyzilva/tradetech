# Teoria dos Robôs — Linha do Tempo V9 → V13

> **Atualizado:** 2026-05-07 | **Ativos:** WIN e WDO | **Plataforma:** Neologica Profit (NTSL/NTFL)

---

## A Teoria Base — F = M × A

Todos os robôs desta família usam **um único indicador próprio**: o `INDICADOR_FORCA_V1` (e V2), que não existe na plataforma por padrão — foi criado do zero.

```
Força = (Corpo / Range) × (Volume / MediaVolume) × 100

  Corpo/Range  = "Massa"       → proporção direcional do candle (0 = doji, 1 = candle perfeito)
  Volume/Média = "Aceleração"  → força relativa do volume (1.0 = normal, 2.0 = dobro da média)
  × 100        = escala 0-100  → clampado em [-100, +100]
```

**Premissa:** um candle só tem força real quando o corpo é grande E o volume é acima da média. Doji com volume alto = indecisão com liquidez, não sinal. Candle cheio com volume baixo = movimento fraco sem confirmação.

**Não usamos:** RSI, MACD, Bollinger, Médias tradicionais como sinal de entrada. O único "indicador" é a própria Força calculada pela física acima.

**Usamos médias apenas como filtro MTF:**
- EMA iJanelaDir × TF = direção de curto prazo
- EMA iJanelaCtx × TF = contexto de médio prazo
- Entrada só quando as duas apontam na mesma direção do sinal de Força

---

## Linha do Tempo das Versões

```
V9  (Semáforo)   → Base funcional. Cores em degradê. Sem break-even. Sem sizing.
V10 (Semáforo)   → Stop dinâmico + break-even + sizing automático.
V11 (WDO/WIN)    → Calibração estatística por ativo. 4 tons fixos. SL/TP otimizados por TF.
V12 (WDO/WIN)    → Refinamento do filtro de entrada. Win% ↑ mas RR começou a cair.
V13 (WDO/WIN)    → Win% continua subindo. RR caiu para ~1.0 em vários TFs.
```

---

## Detalhamento por Versão

### V9 — FORCA_SEMAFORO_CORES_SOM (referência histórica)

| Item | Detalhe |
|---|---|
| Cores | Degradê contínuo (suave — difícil leitura rápida) |
| Stop | Fixo em pontos |
| Break-even | Não tem |
| Sizing | Manual (qtd fixa) |
| Filtro MTF | 3 TFs alinhados |
| Melhor resultado | WDO 15min: +R$8.058 (jan–mar 2026) |

---

### V10 — FORCA_SEMAFORO_V10 (transição)

| Item | Detalhe |
|---|---|
| Cores | 2 tons (fraco verde claro / forte verde escuro) |
| Stop | **Dinâmico**: `max(fixo, range × fator)` |
| Break-even | ✅ Automático após 50% do TP |
| Sizing | ✅ Automático por % de capital |
| Filtro MTF | 3 TFs alinhados |
| Status | Base para V11 |

---

### V11 — FORCA_WDO_V11 / FORCA_WIN_V11 (primeira calibração)

**Filosofia:** parâmetros derivados de backtest estatístico 2012–2026 (47k+ candles). SL/TP calibrados por ativo. Zona fraca (F 55–70) deliberadamente omitida.

#### Parâmetros WDO
| TF | SL | TP | iDir | iCtx | RR |
|---|---|---|---|---|---|
| 15min | 20 pts | 60 pts | 2 | 4 | 3.0 |
| 5min | 12 pts | 36 pts | 3 | 6 | 3.0 |

#### Parâmetros WIN
| TF | SL | TP | iDir | iCtx | RR |
|---|---|---|---|---|---|
| 15min | 822 pts | 2466 pts | 2 | 4 | 3.0 |
| 5min | 342 pts | 1026 pts | 3 | 6 | 3.0 |

#### Resultados V11 (período dez/25–mai/26)

| Ativo | TF | Ops | Win% | PnL (pts) | RR real | Rating |
|---|---|---|---|---|---|---|
| WDO | 5m | 165 | 30.3% | **-2875** | 1.45 | ❌ |
| WDO | 10m | 100 | 42.0% | -780 | 1.16 | ⭐ |
| WDO | 15m | 78 | 51.3% | **+1970** | 1.32 | ⭐⭐⭐⭐ |
| WDO | 20m | 64 | 50.0% | **+2710** | 1.68 | ⭐⭐⭐⭐⭐ |
| WDO | 30m | 49 | 42.9% | +1510 | 1.87 | ⭐⭐⭐⭐ |
| WDO | 60m | 31 | 38.7% | -650 | 1.25 | ❌ |
| WIN | 5m | 316 | 44.0% | **+3494** | 1.47 | ⭐⭐⭐ |
| WIN | 10m | 188 | 44.7% | **+4583** | 1.72 | ⭐⭐⭐⭐ |
| WIN | 15m | 134 | 44.8% | **+5181** | 1.85 | ⭐⭐⭐⭐ |
| WIN | 20m | 89 | 47.2% | +45 | 1.13 | ⭐⭐⭐ |
| WIN | 30m | 81 | 37.0% | -664 | 1.56 | ⭐ |
| WIN | 60m | 39 | 41.0% | -840 | 1.26 | ⭐ |
| WIN | diario | 14 | 35.7% | +690 | 2.37 | ⭐⭐⭐⭐ |

---

### V12 — FORCA_WDO_V12 / FORCA_WIN_V12 (refinamento do filtro)

**O que mudou:** ajuste no filtro de entrada que aumentou o Win%, mas comprimiu o RR. O robô ficou "mais seletivo" — menos trades, maior acerto percentual, porém ganhos menores por trade.

#### Resultados V12 (período ~fev/26–mai/26)

| Ativo | TF | Ops | Win% | PnL (pts) | RR real | Delta vs V11 | Rating |
|---|---|---|---|---|---|---|---|
| WDO | 5m | 176 | 35.2% | -275 | 1.65 | ↑ (era -2875) | ⭐ |
| WDO | 10m | 113 | 42.5% | **+655** | 1.47 | ↑ | ⭐⭐⭐ |
| WDO | 15m | 90 | 46.7% | +1055 | 1.31 | ↓ (era +1970) | ⭐⭐⭐⭐ |
| WDO | 20m | 80 | 46.2% | +870 | 1.32 | ↓ (era +2710) | ⭐⭐⭐⭐ |
| WDO | 30m | 54 | **59.3%** | **+3765** | **2.11** | ↑↑ | ⭐⭐⭐⭐⭐⭐ |
| WDO | 60m | 39 | 48.7% | **+360** | 1.18 | ↑ | ⭐⭐⭐ |
| WIN | 5m | 387 | 51.2% | **+4588** | 1.23 | ↑ | ⭐⭐⭐⭐ |
| WIN | 10m | 248 | 48.4% | +791 | 1.11 | ↓ (era +4583) | ⭐⭐⭐⭐ |
| WIN | 15m | 181 | 54.1% | **+3392** | 1.12 | ↓ (era +5181) | ⭐⭐⭐⭐ |
| WIN | 20m | 146 | **58.9%** | +974 | 0.77 | ↑ | ⭐⭐⭐⭐ |
| WIN | 30m | 110 | 49.1% | -621 | 0.96 | ↓ | ⭐⭐ |
| WIN | 60m | 69 | 58.0% | -300 | 0.70 | ↑ leve | ⭐⭐ |
| WIN | diario | 15 | 60.0% | **+1116** | 1.04 | ↑ | ⭐⭐⭐⭐ |

---

### V13 — FORCA_WDO_V13 / FORCA_WIN_V13 (ajuste incremental)

**O que mudou:** win% seguiu subindo, mas RR colapsou para ~1.0 em quase todos os TFs do WIN. O robô está operando muito perto do breakeven — qualquer custo operacional (corretagem, slippage) torna negativo.

#### Resultados V13 (período ~fev/26–mai/26)

| Ativo | TF | Ops | Win% | PnL (pts) | RR real | Delta vs V12 | Rating |
|---|---|---|---|---|---|---|---|
| WDO | 5m | 151 | 36.4% | -255 | 1.48 | ≈ | ❌ |
| WDO | 10m | 103 | 44.7% | +385 | 1.24 | ↓ | ⭐⭐ |
| WDO | 15m | 78 | 47.4% | +880 | 1.27 | ↓ | ⭐⭐⭐⭐ |
| WDO | 20m | 76 | 42.1% | **-535** | 1.16 | ↓↓ | ⭐ |
| WDO | 30m | 55 | 54.5% | **+2600** | 1.76 | ↓ (era +3765) | ⭐⭐⭐⭐⭐ |
| WDO | 60m | 33 | 45.5% | +5 | 1.14 | ↓ | ⭐⭐⭐ |
| WIN | 5m | 329 | 49.8% | +2851 | 1.21 | ↓ (era +4588) | ⭐⭐⭐⭐ |
| WIN | 10m | 215 | 49.3% | +123 | 1.03 | ↓↓ | ⭐⭐⭐ |
| WIN | 15m | 168 | 54.2% | +2061 | 1.04 | ↓ | ⭐⭐⭐⭐ |
| WIN | 20m | 215 | 49.3% | +123 | 1.03 | ↓↓ | ⭐⭐⭐ |
| WIN | 30m | 99 | 51.5% | -44 | 0.92 | ↑ leve | ⭐⭐ |
| WIN | 60m | 58 | 55.2% | **-1276** | 0.60 | ↓↓↓ | ⭐⭐ |

---

## Diagnóstico: O Padrão de Evolução

```
          V11        V12        V13
WIN 15m:
  Win%    44.8%  →  54.1%  →  54.2%   (+9pp de win, plateau)
  RR      1.85   →  1.12   →  1.04    (-44% no RR — colapso)
  PnL     +5181  →  +3392  →  +2061   (-60% no PnL)

WIN 10m:
  Win%    44.7%  →  48.4%  →  49.3%   (+4.6pp)
  RR      1.72   →  1.11   →  1.03    (-40% no RR)
  PnL     +4583  →  +791   →  +123    (-97% no PnL)
```

**Conclusão:** o ajuste que melhorou o Win% provavelmente **apertou o TP ou alargou o SL**, encurtando o upside de cada trade. Com RR ~1.0 e Win% ~50%, o sistema opera com zero edge — qualquer custo operacional consome o lucro.

O V12 representa o **melhor equilíbrio WDO** (30m com RR 2.11 e Win% 59.3%). O V11 representa o **melhor equilíbrio WIN** (15m e 10m com RR 1.7–1.8 e PnL alto).

---

## Semáforo — Resultados em Paralelo

O `FORCA_SEMAFORO_CORES_SOM` (V9/semáforo visual) foi testado nos mesmos TFs como comparativo:

| Ativo | TF | PnL (pts) | RR real | Destaque |
|---|---|---|---|---|
| WIN | 10m | **+7902** | 1.76 | 🏆 melhor de todos |
| WIN | 15m | +6132 | 1.85 | Excelente |
| WIN | 5m | +3888 | 1.74 | Bom |
| WIN | 20m | +3117 | 1.45 | Bom |
| WDO | 15m | +2455 | ~1.5 | Bom |
| WDO | 20m | +2425 | ~1.5 | Bom |
| WDO | 30m | +1315 | ~1.8 | Bom |
| WIN | diario | +1374 | 2.06 | ⭐ alto RR |
| WIN | 30m | **-2004** | 1.39 | ❌ Pior |
| WDO | 5m | -2755 | 1.74 | ❌ Pior |

---

## Recomendação: Qual Usar em Produção Agora

### ✅ CANDIDATOS CONFIRMADOS

| Prioridade | Robô | TF | Capital mín. | Risco/trade | Por quê |
|---|---|---|---|---|---|
| 🥇 **1** | **SEMAFORO — WIN 10m** | 10min | R$10k | 1 contrato | Melhor PnL absoluto (+7902), RR 1.76, Win% 48.3% |
| 🥈 **2** | **SEMAFORO — WIN 15m** | 15min | R$20k | 1 contrato | RR 1.85 melhor, PnL +6132, Win% 45.2% |
| 🥉 **3** | **WDO V12 — 30m** | 30min | R$20k | 1 contrato | Melhor Win% WDO: 59.3%, RR 2.11, PnL +3765 |
| 4 | **WIN V11 — 15m** | 15min | R$20k | 1 contrato | RR alto (1.85), boa consistência, Win% 44.8% |
| 5 | **WIN V12 — 5m** | 5min | R$10k | 1 contrato | PnL +4588, maior volume de trades |

### ❌ NÃO USAR AGORA

| Robô | TF | Motivo |
|---|---|---|
| Qualquer V13 WIN | 10m/20m | RR ~1.03 — zero edge operacional |
| WIN V12/V13 | 60m | RR < 0.70 — sistema invertido |
| WDO V11/V13 | 5m | Consistentemente negativo todas versões |
| WIN V11 | 30m/60m | Negativo e alta seq. de perdas (10–11) |

### Configuração para começar

```
Opção A — Menor capital (R$10k):
  Robô:     SEMAFORO_WIN TF 10min
  Capital:  R$10.000
  Contratos: 1
  SL:       ~300–400 pts (range médio WIN 10min × 2)
  TP:       ~850–1000 pts (RR 2.5–3.0)
  Horário:  09:30–17:30 (fechar antes de 17:45)

Opção B — Melhor relação risco-retorno (R$20k):
  Robô:     SEMAFORO_WIN TF 15min  OU  WIN_V11 TF 15min
  Capital:  R$20.000
  Contratos: 1
  SL:       822 pts × R$0.20 = R$164 de risco
  TP:       2466 pts × R$0.20 = R$493 de ganho
  Horário:  09:30–17:30

Opção C — WDO (se preferir dólar):
  Robô:     WDO_V12 TF 30min
  Capital:  R$20.000
  Contratos: 1
  SL:       20 pts × R$10 = R$200 de risco
  TP:       60 pts × R$10 = R$600 de ganho
  Horário:  09:30–17:30
```

---

## Por que ainda não ir para V14?

O problema não é o filtro de entrada (win% já está ótimo em V12/V13). O problema é o **RR colapsado**. Antes de criar V14, é necessário entender:

1. O que o V12 WDO 30m faz diferente que gera RR 2.11 com Win% 59%?
2. Por que o V11 WIN 15m tinha RR 1.85 e o V13 caiu para 1.04?
3. A mudança foi no TP? No SL? No filtro de candle contra?

**V14 só faz sentido se tiver hipótese clara:** recuperar RR ≥ 1.5 mantendo Win% ≥ 45%. A direção é ampliar o TP nos TFs que o V13 comprimiu.

---

*Arquivo de teoria. Atualizar após cada nova versão ou backtest significativo.*
