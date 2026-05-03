# FORCA_WDO_V11 — Documentação Técnica

> **Versão:** 11.0 · **Plataforma:** Neologica Profit (NTSL) · **Ativo:** WDO (mini-dólar B3)  
> **Tipo:** Estratégia executável — envia ordens de compra e venda automaticamente

---

## O que faz?

Robot de força calibrado especificamente para o **WDO (mini-dólar)**. Usa a fórmula F = M × A para medir força direcional em cada candle, entra quando a força atinge o limiar forte (padrão F ≥ 70) com 3 timeframes alinhados, e gerencia o trade com SL dinâmico, break-even e TP fixo.

> **Para visualização das cores no gráfico:** use o `INDICADOR_FORCA_V1` (NTFL) em paralelo no mesmo gráfico.

---

## Calibração Estatística (WDO 15 min · 2012–2026)

| Zona de força | % candles | Win@1c | Avg move | Uso |
|---------------|-----------|--------|----------|-----|
| 0–30 (branco) | 48.4% | 46.3% | –0.19 pts | **Sem sinal** |
| 30–55 (cinza) | 23.0% | 45.7% | –0.29 pts | **Sem sinal** |
| 55–70 (fraco) | 7.4% | 44.5% | –0.48 pts | ⚠️ Pior zona — NÃO operar |
| 70–85 (forte) | 5.1% | 46.7% | –0.12 pts | ✅ Entrada forte |
| 85–100 (exaustão) | 16.0% | 47.9% | +0.14 pts | ✅ Melhor zona |

**Backtest completo (SL=20, TP=60, RR 3.0 · tripleta 60/30/15):**

| Modo | Trades | Win% | PnL total |
|------|--------|------|-----------|
| Forte (F 70–85) | 1.563 | 40.2% | +18.980 pts |
| Exaustão (F 85–100) | 5.158 | 39.4% | +59.240 pts |
| **Ambos (F ≥ 70)** | **6.721** | **39.5%** | **+78.220 pts** |

> Win% de 39–40% é suficiente com RR 3.0: precisa de apenas 25% de acerto para break-even.

---

## Esquema de Cores (4 tons)

| Cor | Força | Interpretação | Ação manual |
|-----|-------|----------------|-------------|
| ⬜ **Branco** | F < 55 (abs) | Sem sinal | Skip |
| 🟢 **Verde escuro** | F ≥ 70 (alta) | Força compradora forte | **Entrada LONG prioritária** |
| 🟦 **Cyan** | F ≥ 85 (exaustão alta) | Momentum comprador extremo | **Entrada LONG — maior frequência** |
| 🔴 **Vermelho escuro** | F ≤ –70 (baixa) | Força vendedora forte | **Entrada SHORT prioritária** |
| 🩷 **Fúcsia** | F ≤ –85 (exaustão baixa) | Momentum vendedor extremo | **Entrada SHORT — máxima prioridade** |

> 🟠 **Laranja** não é cor de candle — é o sinal de **volume expresso** (Plot9 gold/laranja quando volume > 1.5× média, plotado no sub-painel do INDICADOR_FORCA_V1).

> A zona 55–70 (sinal fraco) **não tem cor específica** neste robot — estatisticamente é a pior zona e foi deliberadamente omitida.

---

## Parâmetros de Operação (WDO 15 min)

| Parâmetro | Valor padrão | Justificativa |
|-----------|-------------|---------------|
| `ForcaMinimaForte` | 70.0 | Entrada somente em tom forte |
| `ForcaExaustao` | 85.0 | Tom exaustão — alerta + cor destacada |
| `StopMinimo` | 20 pts | P80 adversidade @1c no 15min · nunca reduzir |
| `FatorRangeSL` | 1.5 | SL = max(20, range_candle × 1.5) |
| `TakeProfit` | 60 pts | RR 3.0 — melhor resultado histórico |
| `BreakEvenRatio` | 0.5 | Move SL → entrada após 50% do TP |
| `iJanelaDir` | 2 | EMA direção (2 × 15min = 30min) |
| `iJanelaCtx` | 4 | EMA contexto (4 × 15min = 60min) |
| `CapitalReais` | 10.000 | Capital de referência para sizing |
| `RiscoPorcentagem` | 1.0% | R$100 de risco por trade (1% de R$10k) |
| `PontoValorReais` | R$10.00 | Mini-dólar: 1 ponto = R$10 |

**Para operar no 5 min:** altere `iJanelaDir=3`, `iJanelaCtx=6`, `StopMinimo=12`, `TakeProfit=36`.

---

## Sizing — Contratos por Capital (WDO)

| Capital | Risco | TF | SL | Risco/contrato | Contratos |
|---------|-------|----|----|----------------|-----------|
| R$10k | 1% = R$100 | 15min | 20 pts × R$10 = R$200 | R$200 | ❌ 0 (insuficiente) |
| R$10k | 2% = R$200 | 15min | 20 pts × R$10 = R$200 | R$200 | ✅ 1 contrato |
| R$10k | 2% = R$200 | 5min | 12 pts × R$10 = R$120 | R$120 | ✅ 1 contrato |
| R$20k | 1% = R$200 | 15min | 20 pts × R$10 = R$200 | R$200 | ✅ 1 contrato |
| R$50k | 1% = R$500 | 15min | 20 pts × R$10 = R$200 | R$200 | ✅ 2 contratos |

> **Regra**: `contratos = floor(Capital × Risco% / (SL × R$10))`. Nunca arredondar para cima.

---

## Fluxo de Execução Automática (como o robot decide)

```
A cada candle fechado:
  1. Calcula F = (corpo/range) × (volume/mediaVolume) × 100  → clamp [-100, +100]
  2. Verifica filtro de volume (Volume ≥ VolumeMinimo)
  3. Calcula EMAs de direção e contexto (MTF)
  4. Se HabilitarOperacoes = true e bDeveOperar = true:
       ├── F ≥ ForcaMinimaForte  + MTF Alta  → BuyAtMarket (LONG)
       └── F ≤ -ForcaMinimaForte + MTF Baixa → SellShortAtMarket (SHORT)
  5. Após entrada:
       ├── SL dinâmico = max(StopMinimo, range_candle × FatorRangeSL)
       ├── TP = TakeProfit pts
       ├── Break-even: quando preço chega a 50% do TP → SL move para entrada
       └── Stop candle contra: se candle oposto F ≥ ForcaStopContra → fecha posição
  6. Stop horário: 17:45 → fecha tudo
```

---

## Como Operar Manualmente com as Cores

### Pré-requisitos antes de entrar
1. ✅ O candle de sinal **fechou** (não entrar antes do fechamento)
2. ✅ Cor **verde escuro, fúcsia, vermelho escuro ou laranja** (F ≥ 70 abs)
3. ✅ EMA 30min e EMA 60min apontando na **mesma direção** do sinal
4. ✅ Volume do candle de sinal **acima da média** (preferencialmente)

### Entrada
- **Mercado na abertura do candle seguinte** ao de sinal
- Se for cyan/fúcsia (F ≥ 85 compra / F ≤ –85 venda): entrada ainda mais prioritária — maior frequência histórica

### Stop Loss
- `SL = max(20, range_candle_sinal × 1.5)` em pontos
- **Mínimo 20 pts** — nunca reduzir abaixo disso no WDO 15min

### Alvo (Take Profit)
- **60 pts** = 3 × SL mínimo (RR 3.0)
- Quando preço avançar 30 pts (50% do TP): mover SL para entrada (break-even manual)

### Saída antecipada
- Aparecer candle **fúcsia** (exaustão vendedora) contra sua posição LONG → fechar
- Aparecer candle **cyan** (exaustão compradora) contra sua posição SHORT → fechar
- Horário limite: 17:45

### Candle quase fechando com sinal
> **Aguarde o fechamento. Entre no próximo candle.**  
> Nos últimos segundos, o candle pode reverter parcialmente (reduzindo corpo/range e invalidando o sinal). A entrada no próximo candle é sempre mais segura e com preço já confirmado.

---

## Tripletas Multi-TF Válidas

| TF do candle | Tripleta | iJanelaDir | iJanelaCtx |
|:---:|:---:|:---:|:---:|
| **15 min** | 60 / 30 / 15 | 2 | 4 |
| **5 min** | 30 / 15 / 5 | 3 | 6 |

> Apenas múltiplos inteiros são válidos. 30/15/10 usa multiplicador 1.5 — inválido.
