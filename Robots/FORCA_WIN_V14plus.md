# FORCA WIN — Regras de Negócio V14+

> Documento de referência para as versões **V14, V15, V15_5MIN, V16 e V17**.
> Edite este arquivo para ajustar parâmetros antes de alterar o código NTSL.
> Atualizado em: 2026-06-04

---

## 1. Fórmula central — F = M × A

```
Corpo  = Close − Open
Range  = High − Low  (mínimo 0.0001)
Massa       = Corpo / Range              → varia de −1.0 a +1.0
Aceleração  = Volume / MediaVolume(20)   → relativo à média
Força (F)   = Massa × Aceleração × 100  → clampeado em [−100, +100]
```

- **Positivo** → pressão compradora  
- **Negativo** → pressão vendedora  
- **Perto de zero** → candle indeciso / volume fraco

---

## 2. Zonas de Força

| Zona | Faixa F | Descrição |
|------|---------|-----------|
| Exaustão compradora | F ≥ Exaustão | Compra extrema; entrada mais confiável |
| Forte compradora | Mínimo ≤ F < Exaustão | Compra relevante |
| Neutra / branco | −Mínimo < F < +Mínimo | Sem sinal — não entrar |
| Forte vendedora | −Exaustão < F ≤ −Mínimo | Venda relevante |
| Exaustão vendedora | F ≤ −Exaustão | Venda extrema |

> Limiares por versão: veja seção **7. Parâmetros comparativos**.

---

## 3. Regras de Cor (PaintBar)

### Paleta padrão V14+ (4 cores fixas)

| Cor | RGB | Condição |
|-----|-----|----------|
| **Verde forte** | `(0, 150, 0)` | F ≥ Exaustão compradora |
| **Verde fraco** | `(120, 220, 120)` | Mínimo ≤ F < Exaustão |
| **Vermelho fraco** | `(255, 120, 120)` | −Exaustão < F ≤ −Mínimo |
| **Vermelho forte** | `(180, 0, 0)` | F ≤ −Exaustão vendedora |
| **Branco** | `(255, 255, 255)` | Zona neutra |

### Override de cores (V14 e V16)

| Situação | Cor override | RGB | Versão |
|----------|-------------|-----|--------|
| Zona virou para compra (anterior era 0 ou venda) | **Cyano** | `(0, 220, 220)` | V14 |
| Zona virou para venda (anterior era 0 ou compra) | **Fúcsia** | `(255, 0, 180)` | V14 |
| Instabilidade: ≥3 mudanças de zona em 5 candles + zona compra | **Cyano** | `(0, 220, 220)` | V16 |
| Instabilidade: ≥3 mudanças de zona em 5 candles + zona venda | **Fúcsia** | `(255, 0, 180)` | V16 |

> **V16 nota:** o override por alerta de instabilidade substitui o flip simples de zona. Em V14, qualquer flip gera cyano/fúcsia; em V16, somente quando há muita oscilação na janela.

---

## 4. Multi-TF (tripleta de médias)

```
fMediaDir = Media(iJanelaDir, Close)   → direcional curto
fMediaCtx = Media(iJanelaCtx, Close)   → contexto longo

Contexto de alta  : Close > fMediaCtx  E  fMediaCtx > fMediaCtx[iJanelaCtx]
Contexto de baixa : Close < fMediaCtx  E  fMediaCtx < fMediaCtx[iJanelaCtx]
Direcional alta   : Close > fMediaDir  E  fMediaDir > fMediaDir[iJanelaDir]
Direcional baixa  : Close < fMediaDir  E  fMediaDir < fMediaDir[iJanelaDir]
```

| Timeframe | iJanelaDir | iJanelaCtx | Tripleta resultante |
|-----------|-----------|-----------|---------------------|
| 15 min    | 2         | 4         | 60 / 30 / 15 min ← padrão V14+ |
| 5 min     | 3         | 6         | 30 / 15 / 5 min (V15_5MIN) |

---

## 5. Regras de Entrada

### 5.1 Condições obrigatórias (todas as versões V14+)

#### COMPRA (Long)
```
F >= ForcaMinimaForte          → forca atual suficiente
F[1] < ForcaMinimaForte        → PRIMEIRO candle da sequência (V14 — evita entrada atrasada)
bCtxAlta = true                → contexto longo em alta
bDirAlta = true                → direcional curto em alta
Volume >= VolumeMinimo         → filtro de liquidez (se UsarFiltroVolume=true)
HabilitarOperacoes = true
bDeveOperar = true             → fora do stop horário e max barras
Não está comprado              → se PermitirReversao=true, fecha venda antes
```

#### VENDA (Short)
```
F <= −ForcaMinimaForte
F[1] > −ForcaMinimaForte       → PRIMEIRO candle
bCtxBaixa = true
bDirBaixa = true
Volume >= VolumeMinimo
```

### 5.2 Ação na entrada
```
BuyAtMarket / SellShortAtMarket
fEntrada  := Close             → preço de referência travado
fSLAtivo  := fSL               → SL calculado travado no candle de entrada
iBarras   := 0
bBreakEven := false
Alert(RGB verde/vermelho)      → se MostrarAlertas=true
```

---

## 6. Regras de Saída (ordem de prioridade)

### 6.1 Stop Horário *(prioritário — encerra tudo)*
```
Se Time() >= 17:45 → ClosePosition, bDeveOperar := false
```

### 6.2 Máximo de Barras em Posição
```
Se MaxBarrasEmPosicao > 0  E  iBarras >= MaxBarrasEmPosicao → ClosePosition
```
- V14/V16/V17: `MaxBarrasEmPosicao = 0` (desligado)  
- V15 / V15_5MIN: `MaxBarrasEmPosicao = 3` (15min) / `6` (5min)

### 6.3 Hard Stop Loss via Low/High intrabar *(V14 — bug fix vs V11)*
```
LONG : Low  <= fEntrada − fSLAtivo → ClosePosition
SHORT: High >= fEntrada + fSLAtivo → ClosePosition
```
> **fSLAtivo** é travado no candle de entrada. SL dinâmico calculado a cada barra, mas só o valor da entrada conta para proteção.

### 6.4 Stop Candle Contra *(V14: limiar baixado 85→70)*
```
LONG : F <= −ForcaStopContra → ClosePosition   (ForcaStopContra=70 em todos V14+)
SHORT: F >= +ForcaStopContra → ClosePosition
```
> Fecha imediatamente ao detectar força forte contrária (sem esperar TP/SL).

### 6.5 Break-Even
Mecanismo varia por versão:

| Versão | Gatilho BE | Verificação |
|--------|-----------|-------------|
| V14 | `Close − fEntrada >= TakeProfit × 0.50` (1233 pts) | por Close do candle |
| V15 | `Close − fEntrada >= TakeProfit × 0.60` (30 pts) | por Close |
| V16 | % do TP (V14) + cor oposta + 5 brancos consecutivos | qualquer dos três arma |
| V17 | 75 pts absolutos fixos | por Close |

**Depois de armado:**
```
LONG : Close <= fEntrada → ClosePosition
SHORT: Close >= fEntrada → ClosePosition
```

### 6.6 Trailing Stop
| Versão | Trailing | Configuração |
|--------|---------|-------------|
| V14 | **Desligado** | Intencional — V12 com trailing derrubou AvgWin 45% |
| V15 | Ligado — passo fixo 15 pts | Ativa após BE; teto hard 100 pts |
| V15_5MIN | Ligado — passo fixo 15 pts | Igual V15 |
| V16 | Proporcional: `passo = (TP − lucroAtual) × 10%` (piso 2% TP) | Ativa após BE |
| V17 | Fixo 280 pts | Ativa após BE armado |

### 6.7 Take Profit
```
LONG : High >= fEntrada + TakeProfit → ClosePosition
SHORT: Low  <= fEntrada − TakeProfit → ClosePosition
```

### 6.8 Saídas Parciais — V17 *(UsarSaidasParciais=false por padrão)*
```
TP1 (1/3 posição) : lucro >= TP1Pts (150) → arma BE automaticamente
TP2 (1/3 posição) : lucro >= TP2Pts (300) → ativa trailing no restante
TP3 (resto)       : trailing 280 pts ou TakeProfit hard (1500 pts)
```
> ⚠️ Requer `SellAtMarket(n)` / `BuyAtMarket(n)` — verificar suporte na plataforma antes de ativar.

---

## 7. SL Dinâmico e Sizing

### Cálculo do SL por candle
```
fSL := StopMinimo
Se (fRange × FatorRangeSL) > fSL → fSL := fRange × FatorRangeSL

V16 extra: Se UsarSLMenorQueSinal → fSL := min(fSL, |Corpo| × 0.90)
V17      : FatorRangeSL = 0 → SL sempre fixo em StopMinimo (150 pts)
```

### Sizing por risco
```
iQtd = (CapitalReais × RiscoPorcentagem%) / (fSL × PontoValorReais)
Mínimo: 1 contrato
Máximo: MaxContratos (5)
```

| Parâmetro | Valor padrão |
|-----------|-------------|
| CapitalReais | R$ 10.000 |
| RiscoPorcentagem | 1% |
| PontoValorReais | R$ 0,20 (WIN mini) |
| MaxContratos | 5 |

---

## 8. Parâmetros Comparativos por Versão

| Parâmetro | V14 | V15 (15min) | V15_5MIN | V16 | V17 |
|-----------|-----|-------------|----------|-----|-----|
| **Timeframe** | 15min | 15min | 5min | 15min | 15min |
| **Tripleta** | 60/30/15 | 60/30/15 | 30/15/5 | 60/30/15 | 60/30/15 |
| **ForcaMinimaForte** | 70 | 70 | 70 | 70 | **65** |
| **ForcaExaustao** | 85 | 85 | 85 | 85 | **90** |
| **StopMinimo** | 822 | 30 | 30 | 822 | **150** |
| **FatorRangeSL** | 2.0 | 0.0 | 0.0 | 2.0 | **0.0** |
| **TakeProfit** | 2466 | 50 | 50 | 2466 | **1500** |
| **BreakEven gatilho** | 50% TP (1233 pts) | 60% TP (30 pts) | 60% TP (30 pts) | 50% TP + cor + brancos | **75 pts absolutos** |
| **Trailing** | ❌ OFF | ✅ passo 15 pts + teto 100 | ✅ passo 15 pts + teto 100 | ✅ proporcional 10% | ✅ **fixo 280 pts** |
| **ForcaStopContra** | 70 | 70 | 70 | 70 | 70 |
| **MaxBarrasEmPosicao** | 0 (∞) | 3 | 6 | 0 (∞) | 0 (∞) |
| **SL < Corpo** | ❌ | ❌ | ❌ | ✅ 90% do corpo | ❌ |
| **Saídas parciais** | ❌ | ❌ | ❌ | ❌ | ⚙️ flag off |
| **RR nominal** | 3.0 | 1.67 a 3.33 | 1.67 a 3.33 | 3.0 | ~10 (ajustar) |
| **Status backtest** | ⚠️ filtro 1º candle pendente | ❌ não testado | ❌ não testado | ❌ não testado | ❌ não testado |

---

## 9. Backtest de Referência (V11 — base histórica)

> Dados WIN 15min | tripleta 60/30/15 | 47.787 candles | 2012–2026  
> *(sem filtro de 1º candle e sem os ajustes de cada versão — serve como linha de base)*

| Modo | N trades | Win% | PnL (pts) |
|------|---------|------|-----------|
| Forte (F 70–85) | 1.796 | 41,2% | +956.808 |
| Exaustão (F 85–100) | 4.735 | 44,6% | +3.058.662 |
| **Ambos (F ≥ 70)** | **6.531** | **43,7%** | **+4.015.470** ← melhor |

| Métrica | V11 15min (referência) | V12 (trailing) | Meta V14 |
|---------|----------------------|----------------|---------|
| Trades | 134 | — | ~80–100 (−30% pelo filtro 1º candle) |
| Win% | 44,8% | — | ≥ 43% |
| AvgWin | 258 pts | 141 pts | ≥ 250 pts |
| AvgLoss | −139 pts | — | ~−110 pts |
| Payoff | 1,85× | — | ≥ 2.0× |

---

## 10. Decisões Estratégicas (base para próximas versões)

| # | Decisão | Razão |
|---|---------|-------|
| 1 | **Filtro 1º candle** (V14+) | V13 ao vivo entrou atrasado no 2º candle — comprou no topo do move |
| 2 | **Sem trailing no V14** | V12 com trailing 100 pts derrubou AvgWin de 258 → 141 pts (−45%) |
| 3 | **ForcaStopContra 85→70** | Reage mais rápido à inversão; meta reduzir AvgLoss sem impactar AvgWin |
| 4 | **BE por Close** (não Low/High) | Evita whipsaw intrabar que dispara saída prematura |
| 5 | **SL=822 derivado de range** | 2× range médio 15min (~411 pts) — dá espaço para respirar |
| 6 | **V17: SL=150 (OCR)** | Imagens ProfitPRO mostram "stop0f. 150/155" — divergência real vs V14 |
| 7 | **V17: F mínimo=65 (OCR)** | Painel FR(RSD[9]) marca 65,00 como linha inferior — não 70 |
| 8 | **V17: Exaustão=90 (OCR)** | Painel FR(RSD[9]) marca 90,00 como linha superior — não 85 |
| 9 | **Não entrar zona neutra** | Win% da zona neutra é inferior a todas as zonas de sinal |

---

## 11. Checklist antes de operar real

- [ ] Backtest rodado com os parâmetros da versão escolhida (período ≥ 2024)
- [ ] Comparado com versão anterior no mesmo período
- [ ] SL em pontos revisado vs range médio do período atual
- [ ] Sizing calculado para o capital real (não R$10k de referência)
- [ ] `HabilitarOperacoes = true` (confirmar antes de subir)
- [ ] Stop horário ajustado para o horário da sessão (17:45 padrão)
- [ ] `UsarSaidasParciais` testado isoladamente se for ativar no V17
- [ ] Volume mínimo validado para o horário de operação

---

## 12. Glossário

| Símbolo | Significado |
|---------|------------|
| F | Força = M × A × 100 |
| M (Massa) | Corpo / Range — direcionalidade do candle |
| A (Aceleração) | Volume / MediaVolume — força relativa do volume |
| fEntrada | Preço Close do candle de entrada |
| fSLAtivo | SL calculado e travado no momento da entrada |
| fTrailingRef | Nível de referência do trailing (atualizado barra a barra) |
| BE | Break-even — move o stop para o preço de entrada |
| iZonaAtual | 2=exaustão compra / 1=forte compra / 0=neutro / −1=forte venda / −2=exaustão venda |
| bCtxAlta | Contexto longo em tendência de alta |
| bDirAlta | Direcional curto em alta (filtro MTF) |
| RR | Risk/Reward = TakeProfit / StopMinimo |
