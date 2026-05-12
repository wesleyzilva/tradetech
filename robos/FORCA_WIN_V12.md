# FORCA_WIN_V12 — Documentação Técnica

> **Versão:** 12.0 · **Plataforma:** Neologica Profit (NTSL) · **Ativo:** WIN (mini-índice B3)  
> **Tipo:** Estratégia executável — envia ordens de compra e venda automaticamente  
> **Base:** FORCA_WIN_V11 + 5 correções críticas

---

## O que mudou da V11 para a V12

| # | Melhoria | V11 | V12 |
|---|----------|-----|-----|
| 1 | **Hard Stop Loss intrabar** | `fSL` usado só para sizing — sem ordem real | Verifica `Low/High` a cada barra → sai quando SL atingido |
| 2 | **Break-even agressivo** | Ratio 0.50 (trigger em 50% do TP) | **Ratio 0.33** (trigger em 33% do TP ≈ 340pts no 5min) |
| 3 | **Trailing Stop pós-BE** | Inexistente | `TrailingPasso = 100pts` — segue o preço após BE ativo |
| 4 | **Perda máxima diária** | Inexistente | Para se `fPerdaDia ≥ MaxPerdaDiaria pts` |
| 5 | **Alarmes de zona** | 3 estados — exaustão silenciosa ao escalar de forte | **5 estados** — alarme em toda mudança de cor |

> **Default ajustado para 5 min** — melhor timeframe para WIN com R$10k.

---

## A Fórmula — F = M × A

```
Massa       = Corpo / Range          → quão direcional é o candle  (–1 a +1)
Aceleração  = Volume / Média(Volume) → quão acima da média o volume está
Força       = Massa × Aceleração × 100  → clamp [–100, +100]
```

**Intuição:** `F = +90` significa candle forte de alta **com** volume muito acima da média — há massa e combustível. `F = +90` com volume abaixo da média resulta em valor menor, mesmo que o candle seja grande.

---

## Esquema de Cores (5 min)

| Cor da barra | Faixa de F | Interpretação | Alarme |
|---|---|---|---|
| ⬜ Branco | –70 < F < +70 | Neutro — sem sinal | ✗ silêncio |
| 🟢 Verde escuro | +70 ≤ F < +85 | Força compradora forte | ✓ bip verde |
| 🟩 Verde claro | F ≥ +85 | **Exaustão compradora** — máxima prioridade | ✓ bip verde claro |
| 🔴 Vermelho escuro | –85 < F ≤ –70 | Força vendedora forte | ✓ bip vermelho |
| 🩷 Vermelho claro | F ≤ –85 | **Exaustão vendedora** — máxima prioridade | ✓ bip vermelho claro |

> **Regra do alarme:** dispara em **toda mudança de cor** (incluindo escalada e descida entre zonas). Silencia apenas quando permanece na mesma cor ou retorna ao neutro.

---

## Calibração Estatística (WIN 15 min · 2012–2026 · 14 anos)

| Zona | Trades | Win% | PnL total |
|------|--------|------|-----------|
| Forte (F 70–84) | 1.796 | 41.2% | +956.808 pts |
| **Exaustão (F ≥ 85)** | **4.735** | **44.6%** | **+3.058.662 pts** ← melhor zona |
| **Ambos (F ≥ 70)** | **6.531** | **43.7%** | **+4.015.470 pts** |

> WIN exaustão é a melhor combinação ativo/zona de todos os robôs da família FORCA.

---

## Leitura Multi-Timeframe — do Maior para o Menor

O robô opera em **um único gráfico** (ex: 5 min), mas simula três perspectivas simultaneamente usando EMAs de janelas proporcionais.

### Tripleta padrão 5 min: `30 / 15 / 5`

```
iJanelaCtx = 6  →  EMA(6) sobre fechamentos de 5min = visão de 30min (CONTEXTO)
iJanelaDir = 3  →  EMA(3) sobre fechamentos de 5min = visão de 15min (DIREÇÃO)
Candle atual    →  5min (GATILHO / FORÇA)
```

### Como ler na prática

```
┌─────────────────────────────────────────────────────┐
│  NÍVEL 1 — CONTEXTO (30 min)                        │
│  Close > EMA(6) e EMA(6) subindo  → bias de ALTA    │
│  Close < EMA(6) e EMA(6) caindo   → bias de BAIXA   │
│  Sem isso: operação bloqueada                        │
├─────────────────────────────────────────────────────┤
│  NÍVEL 2 — DIREÇÃO (15 min)                         │
│  Close > EMA(3) e EMA(3) subindo  → directionality  │
│  Close < EMA(3) e EMA(3) caindo   → directionality  │
│  Sem alinhamento com nível 1: sem entrada            │
├─────────────────────────────────────────────────────┤
│  NÍVEL 3 — GATILHO (5 min)                          │
│  F ≥ 70 + volume ≥ mínimo → ENTRADA                 │
│  Cor do candle = intensidade do sinal                │
└─────────────────────────────────────────────────────┘
```

### Regra de ouro para leitura manual

1. **Olhe o gráfico de 30 min primeiro** — o preço está acima ou abaixo da EMA de contexto? A EMA está subindo ou caindo?
2. **Confirme no 15 min** — EMA de direção alinhada com o contexto?
3. **Espere o sinal no 5 min** — candle verde (F ≥ 70) com contexto e direção alinhados = entrada LONG. Candle vermelho = SHORT.

> **Nunca entre contra o contexto de 30 min**, mesmo que o candle de 5 min seja exaustão. O MTF é o filtro mais importante do sistema.

### Tripleta para 15 min: `60 / 30 / 15`

Altere: `iJanelaDir=2` e `iJanelaCtx=4` (2×15=30min, 4×15=60min).

---

## Range de Pontos Esperado — 1 Contrato WIN

### No 5 min (configuração padrão)

| Evento | Pontos | Valor em R$ (1 contrato mini) |
|--------|--------|-------------------------------|
| SL mínimo | 342 pts | **R$ 68,40** |
| SL dinâmico típico | 342–600 pts | R$ 68–120 |
| Break-even trigger | ~340 pts (33% de 1026) | — |
| **TP alvo** | **1.026 pts** | **R$ 205,20** |
| Trailing após BE | 100 pts de folga | — |
| Perda máxima diária | 1.026 pts | **R$ 205,20** |

> **RR = 3.0** — para cada R$68 arriscado, o alvo é R$205.

### No 15 min

| Evento | Pontos | Valor em R$ (1 contrato mini) |
|--------|--------|-------------------------------|
| SL mínimo | 822 pts | **R$ 164,40** |
| **TP alvo** | **2.466 pts** | **R$ 493,20** |
| Break-even trigger | ~813 pts (33% de 2466) | — |
| Capital mínimo sugerido | — | **R$ 20.000** (para 1% de risco) |

### Sizing com 1% de risco por trade

| Capital | TF | Risco | SL | Risco/contrato | Contratos viáveis |
|---------|----|----|----|----|---|
| R$10k | **5 min** | R$100 | 342 pts × R$0,20 = R$68 | R$68 | ✅ **1 contrato** |
| R$10k | 15 min | R$100 | 822 pts × R$0,20 = R$164 | R$164 | ❌ capital insuficiente |
| R$20k | 15 min | R$200 | 822 pts × R$0,20 = R$164 | R$164 | ✅ 1 contrato |
| R$50k | 5 min | R$500 | 342 pts × R$0,20 = R$68 | R$68 | ✅ 7 contratos |

---

## Probabilidade de Transição entre Zonas

> **Nota:** os dados abaixo derivam da distribuição estatística do backtest (2012–2026, WIN 15 min). Uma matriz de transição precisa exige análise barra a barra do histórico raw. Use estes números como referência de ordem de grandeza.

### Distribuição de candles por zona (WIN 15 min)

| Zona | % candles | Candles/dia estimados (6h × 4/h = 24 candles) |
|------|-----------|-----------------------------------------------|
| Neutro (|F| < 70) | ~89.2% | ~21 candles |
| Forte long (70–84) | ~3.0% | ~0.7 candles |
| Exaustão long (≥85) | ~2.1% | ~0.5 candles |
| Forte short (–84 a –70) | ~3.0% | ~0.7 candles |
| Exaustão short (≤–85) | ~2.1% | ~0.5 candles |

### Transições mais prováveis (estimativa baseada na calibração)

| Sinal atual | Próximo candle mais provável | Estimativa |
|---|---|---|
| Neutro → **Forte** | Retorna ao neutro | ~65–70% |
| Neutro → **Forte** | Escala para exaustão | ~30–35% |
| **Forte** → permanece forte | — | ~40% |
| **Forte** → escala para exaustão | — | ~35% ← entrada mais lucrativa |
| **Forte** → retorna ao neutro | — | ~25% |
| **Exaustão** → permanece exaustão | — | ~45% |
| **Exaustão** → cai para forte | — | ~35% |
| **Exaustão** → retorna ao neutro | — | ~20% |

> **O que isso significa na prática:**
> - Um sinal de **forte** tem ~35% de chance de escalar para exaustão — o "segundo bip" é o momento de maior convicção.
> - Um sinal de **exaustão** tem ~45% de chance de continuar na zona — sustentação do move.
> - A transição exaustão → neutro direto (~20%) é a mais perigosa para quem entra tarde.

### Impacto no trading manual

```
Cenário ideal (maior probabilidade de ganho):
  1. Candle forte (verde escuro) — primeiro bip → monitore
  2. Candle seguinte escala para exaustão (verde claro) — segundo bip → ENTRADA
  Racional: você confirma a escalada E ainda está dentro do move inicial.

Cenário de cautela:
  1. Exaustão já ativa há 2+ candles (iZonaAnterior = 2 sem alarme)
  2. Sem novo bip = sem nova energia entrando
  Racional: o move pode estar esgotando — aguarde retorno ao forte ou novo bip.
```

---

## Fluxo de Execução Automática — Barra a Barra

```
A cada candle (barra fechada ou intrabar no 5 min):

  [CÁLCULOS]
  1. F = (Close–Open)/(High–Low) × (Volume/EMA20Vol) × 100  → clamp [–100,+100]
  2. SL = max(StopMinimo=342, Range × 2.0)
  3. Qtd = Capital × 1% / (SL × R$0,20)  → clamp [1, MaxContratos=10]

  [PROTEÇÕES INTRABAR — em posição]
  4. Hard SL: Low ≤ Entrada – SL → fecha LONG  /  High ≥ Entrada + SL → fecha SHORT
  5. Stop candle contra: F ≤ –85 com LONG aberto → fecha  /  F ≥ +85 com SHORT → fecha
  6. Break-even: move ≥ 340pts (33% do TP) → BE ativo → fecha se tocar entrada
  7. Trailing (pós-BE): trailing de 100pts → fecha se Low/High tocar referência
  8. Take Profit: move ≥ 1026pts → fecha

  [STOP HORÁRIO / RISCO DIÁRIO]
  9. Hora ≥ 17:45 → fecha tudo, para
  10. fPerdaDia ≥ 1026pts → fecha tudo, para

  [ENTRADAS — sem posição]
  11. F ≥ 70 + MTF Alta (bCtxAlta e bDirAlta) + Volume ≥ 2000 → BuyAtMarket
  12. F ≤ –70 + MTF Baixa (bCtxBaixa e bDirBaixa) + Volume ≥ 2000 → SellShortAtMarket
```

---

## Parâmetros Completos

### 5 min (padrão)

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `ForcaMinimaForte` | 70.0 | Threshold mínimo para entrada |
| `ForcaExaustao` | 85.0 | Threshold de exaustão |
| `StopMinimo` | 342 pts | 2× range médio WIN@5min (~170pts) |
| `FatorRangeSL` | 2.0 | SL = max(StopMinimo, Range × 2.0) |
| `TakeProfit` | 1.026 pts | RR 3.0 |
| `BreakEvenRatio` | 0.33 | Trigger BE em 33% do TP |
| `TrailingPasso` | 100 pts | Passo do trailing após BE ativo |
| `MaxPerdaDiaria` | 1.026 pts | Stop dia = 1× TP |
| `iJanelaDir` | 3 | EMA direcional (3 × 5min = 15min) |
| `iJanelaCtx` | 6 | EMA contexto (6 × 5min = 30min) |

### 15 min

| Parâmetro | Valor |
|-----------|-------|
| `StopMinimo` | 822 pts |
| `TakeProfit` | 2.466 pts |
| `TrailingPasso` | 200 pts (sugerido) |
| `iJanelaDir` | 2 |
| `iJanelaCtx` | 4 |

---

## Variáveis de Estado Persistentes

| Variável | Tipo | Papel |
|----------|------|-------|
| `iZonaAnterior` | integer | Zona da barra anterior: 0=neutro, ±1=forte, ±2=exaustão |
| `fEntrada` | float | Preço de entrada da posição aberta |
| `fSLAtivo` | float | SL calculado no momento da entrada |
| `fTrailingRef` | float | Referência atual do trailing stop |
| `bBreakEven` | boolean | `true` quando BE foi ativado |
| `iBarras` | integer | Contador de barras em posição |
| `fPerdaDia` | float | Perda acumulada no dia (pts) |
| `iDiaAtual` | integer | Data do dia corrente (reset diário) |
