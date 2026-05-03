# SCALPER_ZONA_V1 — Documentação Técnica

> **Versão:** 1.0 · **Plataforma:** Neologica Profit (NTSL) · **Ativos:** WDO e WIN (configurável)  
> **Tipo:** Estratégia executável — envia ordens de compra e venda automaticamente  
> **Base:** FORCA_WDO_V11 + detector_areas.py (análise de zonas S/R)

---

## O que faz?

Scalper de **zona suporte/resistência confirmada por força**. Enquanto os robots V11 entram em qualquer candle com F ≥ 70, este robot só entra quando **duas condições se somam**:

1. **Preço está tocando uma zona S/R relevante** (máximas/mínimas dos últimos N candles)
2. **Força confirma a direção** (F ≥ ForcaMinima) na mesma barra

O resultado: menos trades, maior qualidade, SL menor (borda da zona em vez de múltiplo do range).

---

## Conceito: Por que zona + força?

```
FORCA_V11 (sem filtro de zona):
  Entre qualquer candle forte → mais trades, SL dinâmico grande

SCALPER_ZONA_V1 (com filtro de zona):
  Entra APENAS quando preço está na zona → menos trades, SL = distância até borda
  → SL naturalmente menor (a zona é o seu stop)
  → RR mantido em 2.0 (menor que V11) mesmo com SL menor
```

---

## Esquema de Cores (mesmo visual do INDICADOR_FORCA_V1)

| Cor | Condição | Ação |
|-----|----------|------|
| 🟡 **Amarelo** | Preço em zona S/R, F < ForcaMinima | **Aguardar** — zona ativa mas sem força |
| 🟢 **Verde escuro** | Preço em zona Suporte, F ≥ ForcaMinima, MTF alta | **Robot entra LONG** |
| 🔴 **Vermelho escuro** | Preço em zona Resistência, F ≥ ForcaMinima, MTF baixa | **Robot entra SHORT** |
| ⬜ **Branco** | Fora de zona, qualquer F | Sem sinal — skip |

> Zona ativa sem força (amarelo) é o **aviso visual mais importante** deste robot: aguardar a força confirmar antes de agir.

---

## Parâmetros Configuráveis por Ativo

### WDO 15 min

| Parâmetro | Valor | Nota |
|-----------|-------|------|
| `ZonaPontos` | 20 pts | Amplitude da zona S/R |
| `ToleranciaZona` | 5 pts | Margem de toque (preço pode estar até 5 pts dentro/fora da zona) |
| `ForcaMinima` | 55.0 | F ≥ 55 confirma direção dentro da zona |
| `StopMinimo` | 20 pts | Borda oposta da zona + buffer |
| `TakeProfit` | 40 pts | RR 2.0 |
| `PontoValorReais` | R$10.00 | |
| `MaxBarrasEmPosicao` | 8 | Sai após 8 candles (scalp curto) |

### WDO 5 min

| Parâmetro | Valor |
|-----------|-------|
| `ZonaPontos` | 12 pts |
| `ToleranciaZona` | 3 pts |
| `StopMinimo` | 12 pts |
| `TakeProfit` | 24 pts (RR 2.0) |

### WIN 15 min

| Parâmetro | Valor |
|-----------|-------|
| `ZonaPontos` | 822 pts |
| `ToleranciaZona` | 200 pts |
| `StopMinimo` | 411 pts |
| `TakeProfit` | 822 pts (RR 2.0) |

### WIN 5 min

| Parâmetro | Valor |
|-----------|-------|
| `ZonaPontos` | 342 pts |
| `ToleranciaZona` | 100 pts |
| `StopMinimo` | 171 pts |
| `TakeProfit` | 342 pts (RR 2.0) |

---

## Como a Zona é Detectada

```
JanelaZona = 3 candles para trás (padrão)

Zona de resistência: Close atual toca o High dos últimos 3 candles (± ToleranciaZona)
Zona de suporte:     Close atual toca o Low dos últimos 3 candles (± ToleranciaZona)

Toque de resistência: |Close - MaxZona| < ToleranciaZona
Toque de suporte:     |Close - MinZona| < ToleranciaZona
```

---

## Fluxo de Execução Automática

```
A cada candle fechado:
  1. Calcula F = (corpo/range) × (volume/mediaVolume) × 100
  2. Detecta zona: Max e Min dos últimos JanelaZona candles
  3. Verifica toque de zona (bZonaResistencia ou bZonaSuporte)
  4. Verifica MTF (se UsarFiltroMTF = true)
  5. Condição de entrada LONG:
       bToqueSuporte AND F >= ForcaMinima AND bCtxAlta AND bDirAlta
       → BuyAtMarket
  6. Condição de entrada SHORT:
       bToqueResistencia AND F <= -ForcaMinima AND bCtxBaixa AND bDirBaixa
       → SellShortAtMarket
  7. SL = borda oposta da zona (StopMinimo como mínimo)
  8. TP = TakeProfit pts (RR 2.0)
  9. MaxBarrasEmPosicao = 8 → sai após 8 candles (scalp curto)
 10. PermitirReversao = false → não reverte dentro da zona
 11. Stop horário: 17:45
```

---

## Como Operar Manualmente com as Cores

### Passo a passo

**1. Identifique a zona (candle amarelo ou preço próximo de max/min recente)**
- O candle ficou amarelo? → preço tocou zona, aguardar força
- Sem amarelo mas preço visualmente perto de máxima/mínima dos últimos 3 candles? → zona potencial

**2. Aguarde a força confirmar**
- Candle amarelo seguido de **verde escuro**: força comprou dentro da suporte → **Entrada LONG**
- Candle amarelo seguido de **vermelho escuro**: força vendeu dentro da resistência → **Entrada SHORT**
- Força fraca (cinza) dentro da zona: **aguardar mais** — sinal insuficiente

**3. Verifique MTF (obrigatório)**
- EMA 30min e EMA 60min na mesma direção do sinal
- Se MTF contra: **skip** — zona com força mas MTF contra é trap

**4. Entrada**
- Mercado na **abertura do candle seguinte** ao de confirmação
- SL na borda oposta da zona (distância menor que SL do V11)

### Stop e Alvo
- SL: borda da zona + buffer mínimo (StopMinimo)
- TP: RR 2.0 × SL
- Break-even: ao atingir 50% do TP, mover SL para entrada
- Saída forçada: MaxBarrasEmPosicao = 8 candles

### Candle quase fechando com sinal de zona
> **Aguarde o fechamento.** O candle ainda pode sair da zona (invalidando o toque) antes de fechar. Confirme o fechamento dentro da zona antes de agir.

### Candles grandes (15min+) no scalper
> Este robot usa `MaxBarrasEmPosicao = 8`. Em candles de 15min isso significa 2 horas de holding máximo. Para candles de 5min são 40 minutos.  
> Se o trade não atingiu TP em 8 candles → o robot fecha automaticamente. Manualmente: faça o mesmo.

---

## Diferenças em relação ao FORCA_WDO_V11

| Critério | FORCA_WDO_V11 | SCALPER_ZONA_V1 |
|----------|---------------|-----------------|
| Filtro de zona | ❌ Não | ✅ Sim |
| SL | Dinâmico (1.5× range) | Borda da zona (menor) |
| RR | 3.0 | 2.0 |
| MaxBarrasEmPosicao | 0 (ilimitado) | 8 (scalp curto) |
| PermitirReversao | true | false |
| Frequência de trades | Alta | Baixa (filtro de zona) |
| Qualidade de trades | Boa | Maior |

---

## Tripletas Multi-TF Válidas

| TF do candle | Tripleta | iJanelaDir | iJanelaCtx |
|:---:|:---:|:---:|:---:|
| **15 min** | 60 / 30 / 15 | 2 | 4 |
| **5 min** | 30 / 15 / 5 | 3 | 6 |
