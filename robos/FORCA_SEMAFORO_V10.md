# FORCA_SEMAFORO_V10 — Documentação Técnica

> **Versão:** 10.0 · **Plataforma:** Neologica Profit (NTSL) · **Ativos:** WDO e WIN (configurável)  
> **Tipo:** Estratégia executável — envia ordens de compra e venda automaticamente  
> **Base:** FORCA_SEMAFORO_CORES_SOM v9.0 (referência funcional)

---

## O que faz?

Robot genérico de força com **2 tons fixos** (fraco + forte). Diferente dos robots V11 (calibrados por ativo), este robot é configurável para qualquer ativo e timeframe — basta ajustar os parâmetros. Introduz três melhorias sobre o v9: **stop dinâmico por range**, **break-even automático**, e **filtro de qualidade EntrarSomenteForte**.

---

## Diferenças em relação ao V9.0 (FORCA_SEMAFORO_CORES_SOM)

| Feature | V9.0 (referência) | V10.0 (este robot) |
|---------|-------------------|---------------------|
| Esquema de cores | Degradê contínuo (6+ tons) | **2 tons fixos** (fraco + forte) |
| Stop Loss | Fixo em pontos | **Dinâmico** (max(fixo, range × fator)) |
| Break-even | Não tem | ✅ **Automático** |
| Filtro entrada | Fraco (F ≥ 55) ou forte (F ≥ 70) | Configurável via `EntrarSomenteForte` |
| Gerenciamento de risco | Manual (qtd fixa) | **Sizing automático** por % de capital |

---

## Esquema de Cores (2 tons)

| Cor | Força | Interpretação | Ação manual |
|-----|-------|----------------|-------------|
| ⬜ **Branco** | F < ForcaMinimaEntrada (55) | Sem sinal | Skip |
| 🟢 **Verde claro** | F ≥ 55 (alta) | Força compradora fraca | **Aguardar confirmação** |
| 🟢 **Verde escuro** | F ≥ 70 (alta) | Força compradora forte | **Entrada LONG prioritária** |
| 🔴 **Vermelho claro** | F ≤ –55 (baixa) | Força vendedora fraca | **Aguardar confirmação** |
| 🔴 **Vermelho escuro** | F ≤ –70 (baixa) | Força vendedora forte | **Entrada SHORT prioritária** |

> **Diferença de apenas ~2–3 pp de Win%** entre tom fraco e tom forte. O 2 tons torna a leitura visual mais imediata sem perda de informação.

---

## Parâmetros Configuráveis por Ativo

### WDO 15 min (configuração recomendada)

| Parâmetro | Valor | Nota |
|-----------|-------|------|
| `ForcaMinimaEntrada` | 55 | Limiar cor + entrada fraca |
| `ForcaMinimaEntrada2` | 70 | Limiar entrada forte e cor escura |
| `EntrarSomenteForte` | false | true = opera só F ≥ 70 |
| `StopPontosFixo` | 10 pts | SL mínimo |
| `FatorRangeSL` | 0.75 | SL = max(10, range × 0.75) |
| `TakeProfit` | 30 pts | RR 3.0 |
| `PontoValorReais` | R$10.00 | Mini-dólar |

### WIN 15 min (configuração recomendada)

| Parâmetro | Valor | Nota |
|-----------|-------|------|
| `ForcaMinimaEntrada` | 55 | Limiar cor + entrada fraca |
| `ForcaMinimaEntrada2` | 70 | Limiar entrada forte |
| `StopPontosFixo` | 300 pts | SL mínimo WIN |
| `FatorRangeSL` | 0.75 | SL dinâmico |
| `TakeProfit` | 900 pts | RR 3.0 |
| `PontoValorReais` | R$0.20 | Mini-índice |

### WDO 5 min

| Parâmetro | Valor |
|-----------|-------|
| `StopPontosFixo` | 8 pts |
| `TakeProfit` | 20 pts (RR 2.5) |
| `iJanelaDir` | 3 |
| `iJanelaCtx` | 6 |

---

## Stop Loss Dinâmico — Como Funciona

```
SL = max(StopPontosFixo, round(RangeCandle × FatorRangeSL))

Exemplo WDO 15min, candle com range = 18 pts:
  SL = max(10, round(18 × 0.75)) = max(10, 14) = 14 pts

Exemplo WDO 15min, candle com range = 6 pts (compressão):
  SL = max(10, round(6 × 0.75)) = max(10, 5) = 10 pts  ← SL mínimo prevalece
```

> O SL dinâmico evita que candles grandes criem stops irrealisticamente pequenos (que seriam acertados por ruído) enquanto mantém o SL mínimo como proteção base.

---

## Fluxo de Execução Automática

```
A cada candle fechado:
  1. Calcula F = (corpo/range) × (volume/mediaVolume) × 100  → clamp [-100, +100]
  2. Verifica filtro de volume
  3. Calcula EMAs MTF (iJanelaDir, iJanelaCtx)
  4. Determina cor (branco / verde claro / verde escuro / verm claro / verm escuro)
  5. Se HabilitarOperacoes = true e bDeveOperar = true:
       Se EntrarSomenteForte = true:
           ├── F ≥ ForcaMinimaEntrada2 + MTF Alta → BuyAtMarket
           └── F ≤ -ForcaMinimaEntrada2 + MTF Baixa → SellShortAtMarket
       Se EntrarSomenteForte = false:
           ├── F ≥ ForcaMinimaEntrada + MTF Alta → BuyAtMarket
           └── F ≤ -ForcaMinimaEntrada + MTF Baixa → SellShortAtMarket
  6. Gerencia SL dinâmico, break-even, MaxBarrasEmPosicao
  7. Stop horário: 17:45
```

---

## Como Operar Manualmente com as Cores

### Leitura dos tons
- **Verde claro:** sinal existe, mas fraco. Se MTF alinhado, **pode entrar com tamanho reduzido** (50% do normal).
- **Verde escuro:** sinal forte. MTF alinhado = **entrada completa**.
- **Vermelho claro / escuro:** mesmas regras para SHORT.

### Pré-requisitos antes de entrar
1. ✅ Candle de sinal **fechou**
2. ✅ Cor diferente de branco
3. ✅ EMA direção e contexto na **mesma direção** do sinal
4. ✅ Definir se vai operar **só tom forte** ou os dois tons

### Stop e Alvo
- SL: `max(StopPontosFixo, range_candle × FatorRangeSL)` → nunca abaixo do mínimo
- TP: `TakeProfit` pontos
- Break-even: ao atingir 50% do TP, mover SL para entrada

### Candle quase fechando com sinal
> **Aguarde o fechamento. Entre no próximo candle.**  
> O tom do candle pode mudar nos últimos segundos (corpo se reduz, força cai, cor volta para branco). Confirme o fechamento antes de agir.

### Candles grandes (15min+)
> Não tente sair dentro do candle de sinal. O SL e TP são em pontos — o tempo não é o critério de saída.  
> Use o `MaxBarrasEmPosicao` para limitar a duração máxima do trade se necessário.

---

## Sizing (genérico, aplicar fórmula)

```
Contratos = floor(Capital × RiscoPct% / (SL × PontoValor))

WDO 15min (SL=10pts): floor(10000 × 0.01 / (10 × 10)) = floor(100/100) = 1 contrato
WIN 15min (SL=300pts): floor(10000 × 0.01 / (300 × 0.20)) = floor(100/60) = 1 contrato
```

---

## Tripletas Multi-TF Válidas

| TF do candle | Tripleta | iJanelaDir | iJanelaCtx |
|:---:|:---:|:---:|:---:|
| **15 min** | 60 / 30 / 15 | 2 | 4 |
| **5 min** | 30 / 15 / 5 | 3 | 6 |
| **5 min** | 15 / 10 / 5 | 2 | 3 |
