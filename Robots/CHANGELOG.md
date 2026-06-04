# CHANGELOG — Robôs FORCA (NTSL)

> Log centralizado das versões dos robôs FORCA (F=M·A) em
> [`tradetech/Robots/`](./).
> Cada entrada cita o arquivo, a base, a justificativa, parâmetros-chave e
> as referências visuais usadas (telas em
> [`ScreenToStudy_MaterOfTrades/`](../ScreenToStudy_MaterOfTrades/)).

---

## [PADRÃO DE CORES] — 2026-06-04

A partir de agora todas as versões V14+ usam **4 cores fixas** (verde/vermelho × fraco/forte), substituindo o esquema antigo verde+ciano / vermelho+fúcsia.

| Zona F | Significado | Cor | RGB |
|---|---|---|---|
| F ≥ 85 | Exaustão compradora | **Verde forte** | `RGB(0, 150, 0)` |
| 70 ≤ F < 85 | Forte compradora | **Verde fraco** | `RGB(120, 220, 120)` |
| −85 < F ≤ −70 | Forte vendedora | **Vermelho fraco** | `RGB(255, 120, 120)` |
| F ≤ −85 | Exaustão vendedora | **Vermelho forte** | `RGB(180, 0, 0)` |

Aplicado em: `FORCA_WIN_V14`, `FORCA_WDO_V14`, `FORCA_WIN_V15`, `FORCA_WIN_V15_5MIN`.
Limiares de força não mudaram — só a paleta. Lógica de entrada/saída intacta.

---

## [FORCA_WIN_V17] — 2026-06-04

**Base:** [FORCA_WIN_V14](./FORCA_WIN_V14)
**Perfil:** Correção de parâmetros divergentes detectados via OCR direto das 27 imagens de `ScreenToStudy_MaterOfTrades`. O `telasAnalise.md` havia perdido 4 divergências críticas.
**Status:** ⚠️ Não rebacktestado.

### Método: OCR com Windows.Media.Ocr (PowerShell nativo)
Todos os PNGs foram processados com OCR sem Tesseract, extraindo valores visíveis nos painéis do ProfitPRO (stop0f, FR(RSD[9]) panel, logs de ordem).

### Divergências encontradas (V14 vs OCR real)

| Parâmetro | V14 (antigo) | V17 (OCR real) | Fonte |
|---|---|---|---|
| `StopMinimo` | 822 pts | **150 pts** | `stop0f. 150/155` em 6 imagens WIN |
| `FatorRangeSL` | 2.0 | **0.0** (fixo) | consequência do SL fixo |
| `ForcaMinimaForte` | 70 | **65** | linha inferior do painel FR(RSD[9]) = 65,00 |
| `ForcaExaustao` | 85 | **90** | linha superior do painel FR(RSD[9]) = 90,00 |
| Break-even | 50% do TP (=1233 pts) | **75 pts absolutos** | "50 pts → Stop 1" (Captura 04/05, derivado para WIN) |
| Trailing | desligado | **280 pts fixo** | "280,00 ts" em `2sinaisFortesOndeEstaStopTecnico` |
| Saídas | 100% no TP | **3 parcelas opcionales** (TP1=150, TP2=300) | "Venda I × 3, Comprado 3" em `3sinaisQuantosPontosBusco` |

### Notas
- `TakeProfit` ajustado para 1500 pts (hard cap conservador). **Ajustar após backtest.**
- Saídas parciais (`UsarSaidasParciais=false` por padrão) exigem `SellAtMarket(n)`/`BuyAtMarket(n)` — verificar suporte na plataforma antes de ativar.
- `ForcaStopContra=70` mantido do V14 (não havia evidência OCR para mudar).

---

## [FORCA_WIN_V16] — 2026-06-04

**Base:** [FORCA_WIN_V14](./FORCA_WIN_V14)
**Perfil:** V14 + alertas visuais de instabilidade + gestão adaptativa de stop/BE.
**Status:** ⚠️ Não rebacktestado.

### Novas regras (vs V14)

| # | Regra | Implementação | Parâmetro |
|---|---|---|---|
| 1 | **Alerta de instabilidade** — candle vira cyano (compra) ou fúcsia (venda) quando a cor muda muito | Janela rolante de 5 candles; ≥3 mudanças de zona = alerta | `JanelaInstabilidade=5`, `MaxMudancasCor=3` |
| 2 | **Alerta de mudança tardia** (opcional, off por padrão) | Aproximação: zona mudou neste candle E `|F|` está a ±10% do limiar (borda instável) | `UsarAlertaMudancaTardia=false`, `PctBordaZona=0.10` |
| 3 | **SL sempre menor que o sinal** | `fSL ≤ |corpo_candle_entrada| × 0.9` | `UsarSLMenorQueSinal=true`, `PctSLvsCorpo=0.9` |
| 4 | **Trailing proporcional** — passo = 10% da distância restante ao TP, aperta conforme avança | Piso de 2% do TP. Ativa só após BE armado | `TrailingPctInicial=0.10`, `TrailingPctPiso=0.02` |
| 5 | **BE por cor oposta** — candle contrário arma BE imediato | LONG + candle vermelho → BE; SHORT + candle verde → BE | `UsarBEPorCorOposta=true` |
| 6 | **BE por 5 brancos consecutivos** | Conta `|F| < 70` durante posição aberta | `CandlesBrancosParaBE=5` |

### Limitação técnica conhecida
- **Mudança tardia (regra 2):** NTSL roda no fechamento do candle. Detectar "últimos 10% do tempo" exigiria modo de execução intrabar/tick. A regra usa uma **aproximação por proximidade da borda da zona** — não é o "10% do tempo restante" literal. Por isso vem **desligada** por padrão.

### O que permaneceu do V14
Filtro 1º candle de força · MTF 60/30/15 · Hard SL intrabar · `ForcaStopContra=70` · BE clássico por % do TP · TP=2466 · SL piso 822 · Cores padrão verde/vermelho fraco/forte (override por cyano/fúcsia só em alerta).

---

## [FORCA_WIN_V15_5MIN] — 2026-06-04

**Base:** [FORCA_WIN_V15](./FORCA_WIN_V15)
**Perfil:** Mesma lógica scalp 50–100 pts, mas operando em **WIN 5min** para reduzir o whipsaw que castigaria o SL=30 pts no 15min.
**Status:** ⚠️ Não rebacktestado.

### Por que existe
No V15 (15min), SL=30 pts representa só 0.07× do range médio do candle (411 pts) — alto risco de stop por ruído intrabar. No 5min o range médio cai para ~171 pts, então:
- SL 30 pts ≈ 0.18× range (3× mais coerente)
- TP 50 pts ≈ 0.29× range (atingível em 1–2 candles)
- Teto 100 pts ≈ 0.58× range (1 candle direcional cobre)

### Mudanças vs V15 (15min)
| Parâmetro | V15 15min | V15 5min |
|---|---:|---:|
| Timeframe operacional | 15min | **5min** |
| `iJanelaDir` | 2 (→30min) | **3 (→15min)** |
| `iJanelaCtx` | 4 (→60min) | **6 (→30min)** |
| `MaxBarrasEmPosicao` | 3 (=45min) | **6 (=30min)** |

Todo o resto (TP=50, Teto=100, SL=30, Trailing 15, BE 0.6, ForcaStopContra=70, filtro 1º candle, volume mínimo, stop horário) é **idêntico**.

### Próximo passo
Backtestar V15 (15min) **e** V15-5min na mesma janela 2024–2026 e comparar:
- N (número de trades), Win%, Total pts, AvgWin, AvgLoss, Payoff, Expectancy
- Distribuição de saídas (TP1 / Trailing / Teto / SL / ForcaStopContra / MaxBarras)

---

## [FORCA_WIN_V15] — 2026-06-04

**Base:** [FORCA_WIN_V14](./FORCA_WIN_V14)
**Perfil:** **SCALP curto — alvo 50 a 100 pts por trade, nunca mais.**
**Status:** ⚠️ Não rebacktestado. Validar antes de operar real.

### Motivação
Solicitação direta: extrair 50–100 pts dos sinais identificados em
[`ScreenToStudy_MaterOfTrades/telasAnalise.md`](../ScreenToStudy_MaterOfTrades/telasAnalise.md).
Mantém **qualidade da entrada do V14** (filtro 1º candle, MTF, hard SL intrabar,
ForcaStopContra=70) e reescreve só o **perfil de saída** para scalp.

### O que mudou (V14 → V15)

| Parâmetro | V14 | V15 | Justificativa |
|---|---:|---:|---|
| `TakeProfit` | 2466 pts | **50 pts** | TP1 hard — alvo mínimo da janela 50–100 |
| `TetoMaximo` *(novo)* | — | **100 pts** | Hard cap: nunca passa de 100 pts intrabar |
| `StopMinimo` | 822 pts | **30 pts** | SL proporcional ao novo TP (RR 1.67 em TP1, 3.33 em teto) |
| `FatorRangeSL` | 2.0 | **0.0** | Desligado — não inflar SL pelo range do candle |
| `UsarTrailing` | false | **true** | Após BE, estende o trade até o teto |
| `TrailingPasso` *(novo)* | — | **15 pts** | Passo curto para travar progressão dentro da janela |
| `BreakEvenRatio` | 0.50 | **0.60** | BE em +30 pts (gatilho do trailing) |
| `MaxBarrasEmPosicao` | 0 (sem limite) | **3** | Scalp expira em 45 min (3 × 15min) |

### O que ficou igual (V14 preservado)
- Filtro do **1º candle de força** (`fForca[1] < limiar` para LONG / `> -limiar` para SHORT) — bloqueia o padrão **P1 "ENTROU ATRASADO"** (tela `Captura de tela 2026-05-12 142250.png`).
- **MTF** tripleta 60/30/15 (`iJanelaDir=2`, `iJanelaCtx=4`).
- **Hard SL intrabar** via Low/High (BUG FIX do V12 mantido).
- **ForcaStopContra=70** — saída antecipada por reversão de força (cobre P3 "SinalForteVoltoueDeuPerda").
- Cores, alertas, volume mínimo (5000), stop horário (17:45).

### Riscos conhecidos
1. **SL=30 pts ≈ 0.07× range médio WIN 15min (411 pts)** — alto risco de whipsaw stopar o trade antes do TP. Avaliar mover o gatilho para 5min (range médio 171 pts) ou 1min.
2. Trailing pode fechar trades vencedores cedo em movimentos voláteis. O teto de 100 pts é a única garantia dura do limite superior.
3. Sem rebacktest. Métricas do V14 (Win% 44.8%, AvgWin 258, AvgLoss -139) **não se aplicam** — perfil de saída mudou completamente.

### Próximos passos sugeridos
- [ ] Rodar backtest WIN 15min com TP=50 / SL=30 / Trailing 15 / Teto 100 (período 2024–2026).
- [ ] Comparar com versão 5min (tripleta 30/15/5: `iJanelaDir=3`, `iJanelaCtx=6`) — pode ser melhor para esse alvo.
- [ ] Avaliar se `ForcaExaustao=85` (apenas exaustão) melhora win% em TP curto.

---

## [FORCA_WIN_V14] — 2026-05-13

**Base:** [FORCA_WIN_V12](./FORCA_WIN_V12)
**Perfil:** Trend-following 15min, TP largo (RR 3.0).

### Resumo
- TF 5min → 15min (tripleta 60/30/15).
- `ForcaStopContra` 85 → 70 (saída antecipada).
- **Remove trailing** (V12 cortava AvgWin: 258 → 141 pts).
- **Remove perda máxima diária** (gerenciamento pelo sizing).
- `BreakEvenRatio` 0.33 → 0.50, checagem via Close (evita whipsaw intrabar).
- **NOVO:** filtro 1º candle de força — `fForca[1] < ForcaMinimaForte` para entrar.
- Hard SL intrabar (herdado V12).

### Backtest referência (V11 15min — pré-filtro 1º candle)
134 trades · Win% 44.8% · Total 5181 pts · AvgWin 258 · AvgLoss -139 · Payoff 1.85×

### Padrões cobertos das telas
| Padrão (telas) | V14 |
|---|---|
| P1 entrada atrasada | ✅ filtro 1º candle |
| P2 conflito TFs "PARAR" | ⚠️ parcial (MTF) |
| P3 sinal forte reverte | ✅ Hard SL + ForcaStopContra=70 |
| P5 sinal perdido em reversão | ❌ estrutural (trend-following) |
| P6 sinal diário no 60min | ✅ MA(4) ≈ 60min |

---

## [FORCA_WDO_V14] — 2026-05-13

**Base:** [FORCA_WDO_V12](./FORCA_WDO_V12)
**Perfil:** Trend-following 30min (melhor TF do WDO).

### Resumo
- TF default 5min → 30min (tripleta 120/60/30).
- `ForcaMinimaForte` 70 → 75 (filtro mais seletivo).
- `StopMinimo` 12 → 20 pts | `TakeProfit` 36 → 60 pts (RR 3.0).
- `TrailingPasso` 4 → 8 pts (proporcional ao range 30min).
- `ForcaStopContra` mantido em 85 (payoff alto já filtrado).

### Backtest referência (V12 30min, dez/2025–mai/2026)
54 trades · Win% 59.3% · Total 3.765 pts · AvgWin 170.6 · AvgLoss -80.7 · Payoff 2.11× · **Expectancy 68.2 pts/trade**

---

## Versões anteriores

- **FORCA_WIN_V13** — Tentativa intermediária 5min com bug de stop não aplicado intrabar. Substituída pelo V14. Erros de compilação documentados em [`FORCA_W_V13_errosAoCompilar`](./FORCA_W_V13_errosAoCompilar).
- **FORCA_WIN_V12** — Introduziu Hard SL intrabar e trailing. Trailing cortou AvgWin em 45%.
- **FORCA_WIN_V11 / FORCA_WDO_V11** — Baseline de calibração (47.787 candles, 2012–2026).
- **FORCA_SEMAFORO_V10 / V_SOM** — Indicadores visuais (não executam ordens).
- **INDICADOR_FORCA_V1 / V2** — Cálculo puro de F=M·A para estudo.

---

## Convenções

- Toda nova versão **incrementa o número** (Vnn) e cria entrada no topo deste arquivo.
- Toda mudança de **TP/SL/Trailing/Filtro** exige rebacktest registrado em [`Results/`](./Results/) antes de operar real.
- Telas usadas como referência ficam em [`ScreenToStudy_MaterOfTrades/`](../ScreenToStudy_MaterOfTrades/) e devem ser citadas pelo nome do arquivo.
- Justificativa estatística (n, win%, PnL, payoff) é obrigatória para mudanças de parâmetro.
