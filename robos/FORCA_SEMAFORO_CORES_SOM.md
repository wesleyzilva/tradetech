# FORCA_SEMAFORO_CORES_SOM — Documentação Técnica

> **Versão:** 9.0 · **Plataforma:** Neologica Profit (NTSL/NTFL) · **Ativos:** WDOFUT · WINFUT

---

## O que faz?

Coloração de candles com semáforo visual (verde/vermelho em degradê) combinada com um **robô de entradas automáticas**, usando o princípio físico **Força = Massa × Aceleração** aplicado ao price action.

Entradas só ocorrem quando **3 timeframes estão alinhados** (Contexto + Direção + Gatilho), reduzindo ruídos e entradas contra a tendência dominante.

---

## O Cálculo da Força (F = M × A)

```
Força = Massa × Aceleração × 100

Massa       = Corpo / Range
              (proporção do corpo em relação ao range total do candle)
              Varia de -1 a +1 (positivo = candle de alta, negativo = baixa)

Aceleração  = Volume / MediaVolume(n)
              (volume relativo à média — mede "impulso" do movimento)

Resultado   = clampado em [-100, +100]
```

**Exemplo prático:**
- Candle com corpo = 100% do range (fechou no topo), volume 2× a média → Força = +200 → clampado para +100
- Candle doji (corpo ≈ 0), qualquer volume → Força ≈ 0 → sem sinal (branco)

---

## Esquema de Cores (Semáforo)

| Cor | Condição | Significado |
|-----|----------|-------------|
| ⬜ Branco | `abs(Força) < ForcaMinimaEntrada` | Sem sinal — doji, candle fraco |
| 🟢 Verde (degradê) | `Força >= ForcaMinimaEntrada` | Força compradora ativa |
| 🔴 Vermelho (degradê) | `Força <= -ForcaMinimaEntrada` | Força vendedora ativa |

### Cálculo do Degradê

A intensidade da cor é proporcional à magnitude da força, com **curva quadrática** para realçar diferenças:

```
escala = (|Força| - ForcaMinima) / (ForcaMaxima - ForcaMinima)  → [0..1]
escala = escala²  (curva quadrática: sinal fraco = cor fraca, sinal forte = cor intensa)

Verde:    R = 110→0,   G = 110→255, B = 110→0
Vermelho: R = 110→255, G = 110→0,   B = 110→0
```

---

## Multi-Timeframe: Confirmação em 3 TFs

O robô só entra quando os 3 níveis de análise estão alinhados na mesma direção.

```
TF Contexto  (maior)  →  iJanelaCtx  ×  TF Gatilho
TF Direção   (médio)  →  iJanelaDir  ×  TF Gatilho
TF Gatilho   (menor)  →  candle atual
```

### Tripletas Válidas (multiplicadores inteiros — regra matemática)

| TF Gatilho | Tripleta | iJanelaDir | iJanelaCtx | Backtest 01/01–01/04/2026 |
|:---:|:---:|:---:|:---:|:---:|
| 15 min | **60 / 30 / 15** | 2 (2×15=30) | 4 (4×15=60) | **+R$8.058** · FL 1.25 ✅ |
| 5 min | **30 / 15 / 5** | 3 (3×5=15) | 6 (6×5=30) | **+R$6.336** · FL 1.11 ✅ |
| 5 min | **15 / 10 / 5** | 2 (2×5=10) | 3 (3×5=15) | falta backtest ⚠️ |

> ⚠️ **Tripletas inválidas (evitar):** 30/15/10 → multiplicador 1.5× (não inteiro). Usar 30/20/10 ou 30/15/5.

### Critério de alinhamento

```
Contexto Alta  → Close > MediaCtx  E  MediaCtx > MediaCtx[iJanelaCtx]  (EMA subindo)
Direção  Alta  → Close > MediaDir  E  MediaDir > MediaDir[iJanelaDir]   (EMA subindo)
Gatilho  Alta  → Força >= ForcaMinimaEntrada (candle atual)

Contexto Baixa → Close < MediaCtx  E  MediaCtx < MediaCtx[iJanelaCtx]
Direção  Baixa → Close < MediaDir  E  MediaDir < MediaDir[iJanelaDir]
Gatilho  Baixa → Força <= -ForcaMinimaEntrada
```

---

## Lógica de Entradas

### Compra (BuyAtMarket)
```
Força >= ForcaMinimaEntrada   [gatilho]
AND ContextoAlta              [TF maior em alta]
AND DirecaoAlta               [TF médio em alta]
AND Volume >= VolumeMinimo    [filtro de liquidez, se ativo]
AND HabilitarOperacoes = true
AND Não está comprado ou vendido (ou PermitirReversao = true)
```

### Venda (SellShortAtMarket)
```
Força <= -ForcaMinimaEntrada  [gatilho]
AND ContextoBaixa             [TF maior em baixa]
AND DirecaoBaixa              [TF médio em baixa]
AND Volume >= VolumeMinimo
AND HabilitarOperacoes = true
```

### Reversão
Se `PermitirReversao = true`: fecha a posição oposta antes de entrar na nova direção — permite girar de comprado para vendido em um único candle.

---

## Lógica de Saídas (Stops)

| Stop | Condição | Ação |
|------|----------|------|
| **Stop Horário** | `Hora >= 17:45` | Fecha posição + bloqueia novas entradas |
| **Stop Candle Contra** | Candle forte na direção oposta (`abs(Força) >= ForcaStopContra`) | Fecha imediatamente |
| **Stop por Barras** | `MaxBarrasEmPosicao > 0` e atingido | Fecha após N barras em posição |

---

## Sistema de Alertas

- **Alerta visual + sonoro** ao entrar em posição (`Alert(RGB(...))`)
- Verde → compra, Vermelho → venda
- **Segundo checkpoint opcional** (`UsarSegundoCheckpointAlerta`): só alerta se `|Força| >= ForcaMinimaAlerta` (ex: 70) — reduz alertas em entradas fracas

---

## Parâmetros de Configuração

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `VolumeMinimo` | 2000 | Volume mínimo para operar |
| `PeriodoMediaVolume` | 20 | Período da média de volume |
| `ForcaMinimaEntrada` | 55 | Limiar de força para sinal + início do degradê |
| `ForcaMaximaCor` | 100 | Máximo de força para o degradê |
| `UsarFiltroVolume` | true | Exige Volume >= VolumeMinimo |
| `HabilitarOperacoes` | true | Permite bloquer entradas sem perder coloração |
| `PermitirReversao` | true | Gira de comprado para vendido automaticamente |
| `MostrarAlertas` | true | Alertas sonoros |
| `UsarSegundoCheckpointAlerta` | true | Exige ForcaMinimaAlerta para alertar |
| `ForcaMinimaAlerta` | 70 | Segundo limiar para alerta |
| `iJanelaDir` | 2 | Multiplicador do TF de direção |
| `iJanelaCtx` | 4 | Multiplicador do TF de contexto |
| `StopHorario_H` | 17 | Hora do stop horário |
| `StopHorario_M` | 45 | Minuto do stop horário |
| `UsarStopCandleContra` | true | Fecha se candle forte oposto |
| `ForcaStopContra` | 55 | Limiar de força para stop candle contra |
| `MaxBarrasEmPosicao` | 0 | 0 = desativado; N = fecha após N barras |

---

## Fluxo de Execução (por candle)

```
1. Calcula Corpo, Range, MediaVolume
2. Calcula Força = (Corpo/Range) × (Volume/MediaVolume) × 100
3. Calcula MediaDir e MediaCtx (EMAs dos TFs superiores)
4. Define bContextoAlta/Baixa e bDirecaoAlta/Baixa
5. Coloração do candle (degradê verde/vermelho/branco)
6. Verifica Stop Horário → fecha + bloqueia se necessário
7. Atualiza contador de barras em posição
8. Verifica MaxBarrasEmPosicao → fecha se atingido
9. Verifica StopCandleContra → fecha se candle forte oposto
10. Lógica de Entradas — BuyAtMarket ou SellShortAtMarket
11. Emite alerta sonoro/visual se configurado
```

---

## Como usar no Profit

1. Abra o gráfico do ativo no **TF Gatilho** (ex: 15min para tripleta 60/30/15)
2. Insira o robô com os parâmetros da tripleta desejada:
   - Tripleta 60/30/15 → `iJanelaDir = 2`, `iJanelaCtx = 4`
   - Tripleta 30/15/5  → `iJanelaDir = 3`, `iJanelaCtx = 6`
3. O gráfico exibirá os candles coloridos; o robô opera automaticamente
4. Ajuste `HabilitarOperacoes = false` para usar somente a coloração visual, sem ordens automáticas

---

## Resultados de Backtest (01/01/2026 – 01/04/2026)

| Tripleta | Resultado | Fator de Lucro | Status |
|----------|-----------|:--------------:|--------|
| 60/30/15 (15min) | **+R$8.058** | 1.25 | ✅ Aprovado |
| 30/15/5  (5min)  | **+R$6.336** | 1.11 | ✅ Aprovado |
| 15/10/5  (5min)  | — | — | ⚠️ Pendente |

> Dados: WDOFUT e WINFUT · Período de 3 meses
