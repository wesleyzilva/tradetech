# FORCA WIN V13
### Robô de trading para WIN (mini-índice Bovespa) — Neologica Profit

---

## O que mudou do V12 para o V13

| # | Mudança | V12 | V13 |
|---|---|---|---|
| 1 | **Saída principal** | SL / TP / BE / Trailing | **Candle branco** (perda de momentum) |
| 2 | **Break-even trigger** | 33% do TP (~340pts) | **70% do TP (70pts)** |
| 3 | **Break-even proteção** | Stop move para entrada (0pts) | **Stop em entrada +20pts** |
| 4 | **Take Profit** | 1.026 pts | **100 pts** (segurança, candle branco é a saída normal) |

---

## Filosofia do V13

> **"Fica enquanto a cor durar. Sai quando virar branco."**

O V12 esperava atingir um alvo fixo grande. O V13 opera enquanto o candle estiver colorido (verde ou vermelho) e fecha assim que a força some — o candle fecha branco. Isso captura moves de momentum sem deixar o lucro evaporar.

---

## Fórmula — F = M × A

| Componente | Cálculo | Significado |
|---|---|---|
| **Massa** | `Corpo ÷ Range` | Direcionalidade da vela (–1 a +1) |
| **Aceleração** | `Volume ÷ MediaVolume(20)` | Intensidade relativa do volume |
| **Força** | `M × A × 100` | Resultado final, limitado [–100, +100] |

---

## Cores e Zonas

| Cor | Condição | Ação do Robô |
|---|---|---|
| ⬜ Branco | –70 < F < 70 | Fora da zona — **fecha posição se aberta** |
| 🟢 Verde escuro | F ≥ 70 | Entra LONG (se contexto confirmar) |
| 🟩 Verde claro | F ≥ 85 | Entra LONG — sinal de maior qualidade |
| 🔴 Vermelho escuro | F ≤ –70 | Entra SHORT (se contexto confirmar) |
| 🩷 Vermelho claro | F ≤ –85 | Entra SHORT — sinal de maior qualidade |

---

## Condição de Entrada

### LONG (Compra)
```
fForca >= 70           → candle verde (escuro ou claro)
bCtxAlta = true        → Close > média longa E média longa subindo
bDirAlta = true        → Close > média curta E média curta subindo
Volume >= 2000         → filtro de volume mínimo
```

### SHORT (Venda)
```
fForca <= -70          → candle vermelho
bCtxBaixa = true       → Close < média longa E média longa caindo
bDirBaixa = true       → Close < média curta E média curta caindo
Volume >= 2000         → filtro de volume mínimo
```

### Multi-Timeframe (tripleta padrão 5min)
| Janela | Parâmetro | Equivalente |
|---|---|---|
| Contexto | `iJanelaCtx = 6` velas | ~30 minutos |
| Direção | `iJanelaDir = 3` velas | ~15 minutos |
| Gatilho | vela atual | 5 minutos |

---

## Saídas — Ordem de Prioridade

| Prioridade | Gatilho | Quando ocorre |
|---|---|---|
| 1 | **Hard Stop Loss** | Low/High cruza `entrada ± 342pts` intrabar |
| 2 | **Candle Contra** | Vela extrema oposta (F ≥ 85 do lado contrário) |
| 3 | **Candle Branco** ← principal | Fechamento com –70 < F < 70 |
| 4 | **Break-even** | Após +70pts, fecha se preço recuar até entrada +20pts |
| 5 | **Trailing Stop** | Após BE ativo, fecha se preço recuar 100pts do pico |
| 6 | **Take Profit** | Preço atinge entrada ± 100pts intrabar |
| 7 | **Stop Horário** | 17h45 — fecha tudo |
| 8 | **Perda Diária** | Acumulado ≥ 1.026pts no dia |

---

## Break-even V13 — Exemplo

```
Entrada:          100.000 pts
BE trigger:       100.000 + 70 = 100.070  →  bBreakEven = true
Stop protegido:   100.000 + 20 = 100.020  →  fecha se Low <= 100.020
Take Profit:      100.000 + 100 = 100.100
```

Resultado possível por trade:
- Candle vira branco com +40pts → fecha em **+40pts** (R$8/contrato)
- Preço recua ao stop BE → fecha em **+20pts** (R$4/contrato — nunca perde após BE)
- TP atingido intrabar → fecha em **+100pts** (R$20/contrato)
- SL atingido → fecha em **–342pts** (R$68/contrato)

---

## Gerenciamento de Risco

| Parâmetro | Valor | Significado |
|---|---|---|
| `CapitalReais` | 10.000 | Capital base para sizing |
| `RiscoPorcentagem` | 1% | R$100 de risco por trade |
| `PontoValorReais` | R$0,20 | 1 ponto WIN mini = R$0,20 |
| `StopMinimo` | 342 pts | R$68 de risco/contrato |
| `MaxPerdaDiaria` | 1.026 pts | Para de operar se perder 1 TP no dia |
| `MaxContratos` | 10 | Limite de contratos por operação |

### Sizing automático
```
iQtd = Capital × (Risco% / 100) ÷ (SL × PontoValor)
iQtd = 10.000 × 0.01 ÷ (342 × 0.20)
iQtd = 100 ÷ 68.40 = 1 contrato
```

---

## Parâmetros Completos

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `ForcaMinimaForte` | 70 | Limiar mínimo para zona colorida |
| `ForcaExaustao` | 85 | Limiar de exaustão (cor mais intensa) |
| `PeriodoMediaVolume` | 20 | Período da média de volume |
| `UsarFiltroVolume` | true | Ativa filtro de volume mínimo |
| `VolumeMinimo` | 2000 | Volume mínimo por vela |
| `iJanelaDir` | 3 | Janela de direção (velas) |
| `iJanelaCtx` | 6 | Janela de contexto (velas) |
| `StopMinimo` | 342 | SL base em pontos |
| `FatorRangeSL` | 2.0 | SL = max(StopMinimo, Range × 2) |
| `TakeProfit` | 100 | Alvo máximo em pontos |
| `UsarBreakEven` | true | Ativa break-even |
| `BreakEvenRatio` | 0.70 | Trigger BE = 70% do TP (70pts) |
| `BreakEvenProtectRatio` | 0.20 | Proteção BE = entrada + 20% do TP (20pts) |
| `UsarTrailing` | true | Ativa trailing após BE |
| `TrailingPasso` | 100 | Recuo máximo após pico (pts) |
| `MaxPerdaDiaria` | 1026 | Stop dia em pontos |
| `StopHorario_H` | 17 | Hora do stop horário |
| `StopHorario_M` | 45 | Minuto do stop horário |
| `UsarStopCandleContra` | true | Fecha em candle extremo oposto |
| `ForcaStopContra` | 85 | Força mínima para candle contra |
| `PermitirReversao` | true | Fecha e reverte em sinal oposto |
| `HabilitarOperacoes` | true | Liga/desliga execução de ordens |
| `MostrarAlertas` | true | Emite bip nas mudanças de cor |

---

## Configuração para outros Timeframes

| TF | `StopMinimo` | `TakeProfit` | `iJanelaDir` | `iJanelaCtx` | Capital mínimo |
|---|---|---|---|---|---|
| **5 min** ← padrão | 342 | 100 | 3 | 6 | R$7.000 |
| 15 min | 822 | 100 | 2 | 4 | R$17.000 |
| 60 min | 1400 | 100 | 2 | 4 | R$28.000 |

> **Nota:** com TP=100pts fixo, o candle branco passa a ser a saída dominante em todos os TFs. O SL permanece calibrado pelo range do TF.

---

## Diferença operacional V12 × V13

```
V12 — espera o alvo grande
  Entrada verde → aguarda 1.026pts de lucro OU leva o stop
  Operação dura em média 8–15 velas
  Poucos trades, gains grandes, poucos stops

V13 — segue o momentum
  Entrada verde → fecha quando virar branco
  Operação dura em média 2–5 velas
  Mais trades, gains menores, menos drawdown por trade
  BE protege +20pts antes de virar branco
```
