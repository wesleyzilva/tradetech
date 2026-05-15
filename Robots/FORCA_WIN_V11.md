# FORCA_WIN_V11 — Documentação Técnica

> **Versão:** 11.0 · **Plataforma:** Neologica Profit (NTSL) · **Ativo:** WIN (mini-índice B3)  
> **Tipo:** Estratégia executável — envia ordens de compra e venda automaticamente

---

## O que faz?

Robot de força calibrado especificamente para o **WIN (mini-índice Bovespa)**. Mesma lógica F = M × A do WDO_V11, com parâmetros ajustados para a escala de pontos e comportamento estatístico diferente do índice. O WIN apresenta resultado muito superior ao WDO na zona de exaustão — o que torna este robot especialmente atraente.

> **Para visualização das cores no gráfico:** use o `INDICADOR_FORCA_V1` (NTFL) em paralelo no mesmo gráfico.

---

## Por que WIN é diferente do WDO?

| Diferença | WDO | WIN |
|-----------|-----|-----|
| Ponto em R$ (mini) | R$10.00 | R$0.20 |
| Range médio 15min | 13.3 pts | 411 pts |
| Win% zona exaustão | 39.4% | **44.6%** |
| PnL exaustão (14 anos) | +59.240 pts | **+3.058.662 pts** |
| Contratos viáveis com R$10k | ❌ 0 (15min, 1%) | ✅ 1 (5min, 1%) |

> **WIN exaustão é a melhor combinação de todos os robots** — win% 44.6% com RR 3.0 resulta em PnL 3× maior que WDO no mesmo período.

---

## Calibração Estatística (WIN 15 min · 2012–2026)

| Zona de força | % candles | Win@1c | Uso |
|---------------|-----------|--------|-----|
| 0–30 (branco) | 44.5% | 48.0% | **Sem sinal** |
| 30–55 (cinza) | 25.3% | 47.6% | **Sem sinal** |
| 55–70 (fraco) | 9.4% | 49.1% | Melhor que WDO fraco, mas avg_move ruim |
| 70–85 (forte) | 6.0% | varia | ✅ Entrada forte |
| 85–100 (exaustão) | 4.2% | **44.6%** | ✅ **MELHOR zona — prioridade máxima** |

**Backtest completo (SL=822, TP=2466, RR 3.0 · tripleta 60/30/15):**

| Modo | Trades | Win% | PnL total |
|------|--------|------|-----------|
| Forte (F 70–85) | 1.796 | 41.2% | +956.808 pts |
| Exaustão (F 85–100) | 4.735 | **44.6%** | **+3.058.662 pts** |
| **Ambos (F ≥ 70)** | **6.531** | **43.7%** | **+4.015.470 pts** |

---

## Esquema de Cores (4 tons — idêntico ao WDO_V11)

| Cor | Força | Interpretação | Ação manual |
|-----|-------|----------------|-------------|
| ⬜ **Branco** | F < 55 (abs) | Sem sinal | Skip |
| 🟢 **Verde escuro** | F ≥ 70 (alta) | Força compradora forte | **Entrada LONG prioritária** |
| � **Cyan** | F ≥ 85 (exaustão alta) | Momentum comprador extremo | **Entrada LONG — máxima prioridade** |
| 🔴 **Vermelho escuro** | F ≤ –70 (baixa) | Força vendedora forte | **Entrada SHORT prioritária** |
| 🩷 **Fúcsia** | F ≤ –85 (exaustão baixa) | Momentum vendedor extremo | **Entrada SHORT — máxima prioridade** |

> 🟠 **Laranja** não é cor de candle — é o sinal de **volume expresso** (Plot9 gold/laranja quando volume > 1.5× média, plotado no sub-painel do INDICADOR_FORCA_V1).

---

## Parâmetros de Operação (WIN 15 min)

| Parâmetro | Valor padrão | Justificativa |
|-----------|-------------|---------------|
| `ForcaMinimaForte` | 70.0 | Entrada somente em tom forte |
| `ForcaExaustao` | 85.0 | Tom exaustão — melhor zona do WIN |
| `StopMinimo` | 822 pts | 2× range médio WIN 15min · nunca reduzir |
| `FatorRangeSL` | 2.0 | SL = max(822, range_candle × 2.0) |
| `TakeProfit` | 2.466 pts | RR 3.0 |
| `BreakEvenRatio` | 0.5 | Move SL → entrada após 50% do TP |
| `iJanelaDir` | 2 | EMA direção (2 × 15min = 30min) |
| `iJanelaCtx` | 4 | EMA contexto (4 × 15min = 60min) |
| `CapitalReais` | 10.000 | Capital de referência |
| `RiscoPorcentagem` | 1.0% | R$100 de risco por trade |
| `PontoValorReais` | R$0.20 | Mini-índice: 1 ponto = R$0.20 |

**Para operar no 5 min:** altere `iJanelaDir=3`, `iJanelaCtx=6`, `StopMinimo=342`, `TakeProfit=1026`.

---

## Sizing — Contratos por Capital (WIN)

| Capital | Risco | TF | SL | Risco/contrato | Contratos |
|---------|-------|----|----|----------------|-----------|
| R$10k | 1% = R$100 | **5min** | 342 pts × R$0.20 = **R$68** | R$68 | ✅ **1 contrato** |
| R$10k | 2% = R$200 | 5min | 342 pts × R$0.20 = R$68 | R$68 | ✅ 2 contratos |
| R$10k | 1% = R$100 | 15min | 822 pts × R$0.20 = R$164 | R$164 | ❌ 0 (insuficiente) |
| R$10k | 2% = R$200 | 15min | 822 pts × R$0.20 = R$164 | R$164 | ✅ 1 contrato |
| R$20k | 1% = R$200 | 15min | 822 pts × R$0.20 = R$164 | R$164 | ✅ 1 contrato |
| R$50k | 1% = R$500 | 15min | 822 pts × R$0.20 = R$164 | R$164 | ✅ 3 contratos |

> **Melhor opção para R$10k:** WIN 5min com 1% de risco = 1 contrato, R$68 de risco real (~0.7%).

---

## Fluxo de Execução Automática (como o robot decide)

```
A cada candle fechado:
  1. Calcula F = (corpo/range) × (volume/mediaVolume) × 100  → clamp [-100, +100]
  2. Verifica filtro de volume (Volume ≥ 5000 — WIN tem volume maior que WDO)
  3. Calcula EMAs de direção e contexto (MTF)
  4. Se HabilitarOperacoes = true e bDeveOperar = true:
       ├── F ≥ 70 + MTF Alta  → BuyAtMarket (LONG)
       └── F ≤ –70 + MTF Baixa → SellShortAtMarket (SHORT)
  5. Após entrada:
       ├── SL dinâmico = max(822, range_candle × 2.0) em pts
       ├── TP = 2.466 pts
       ├── Break-even: quando preço chega a 1.233 pts → SL move para entrada
       └── Stop candle contra: candle oposto F ≥ 85 → fecha posição
  6. Stop horário: 17:45 → fecha tudo
```

---

## Como Operar Manualmente com as Cores

### Pré-requisitos antes de entrar
1. ✅ O candle de sinal **fechou** completamente
2. ✅ Cor **verde escuro, cyan, vermelho escuro ou fúcsia** (F ≥ 70 abs)
3. ✅ EMA 30min e EMA 60min na **mesma direção** do sinal
4. ✅ Volume acima da média (cyan/fúcsia = prioridade máxima no WIN)

### Entrada
- **Mercado na abertura do candle seguinte** ao de sinal
- **Cyan ou fúcsia** (F ≥ 85 compra / F ≤ –85 venda): prioridade máxima no WIN — win% 44.6%

### Stop Loss e Alvo
- SL mínimo: **822 pts** no 15min · **342 pts** no 5min
- TP: **2.466 pts** no 15min · **1.026 pts** no 5min
- Break-even manual: ao atingir metade do TP, mover SL para entrada

### Saída antecipada
- Candle **fúcsia** (exaustão vendedora) contra sua posição LONG → fechar
- Candle **cyan** (exaustão compradora) contra sua posição SHORT → fechar
- Horário limite: **17:45**

### Candle quase fechando com sinal
> **Aguarde o fechamento. Entre no próximo candle.**  
> Com SL de 822 pts no WIN 15min, a diferença de 10–15 pts de slippage nos últimos segundos é irrelevante. Mas o risco de reversão parcial do candle (invalidando o sinal) é real. Aguardar o fechamento é a abordagem mais segura.

### Gerenciamento em candles grandes (15min e 30min)
> Não tente sair dentro do candle de sinal. A estratégia é baseada em SL/TP em pontos.  
> O break-even automaticamente protege a posição após metade do caminho ao TP.  
> Se surgir um candle fúcsia ou cyan contrário, essa é sua saída antecipada.

---

## Tripletas Multi-TF Válidas

| TF do candle | Tripleta | iJanelaDir | iJanelaCtx |
|:---:|:---:|:---:|:---:|
| **15 min** | 60 / 30 / 15 | 2 | 4 |
| **5 min** | 30 / 15 / 5 | 3 | 6 |
