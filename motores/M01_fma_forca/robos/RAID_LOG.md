# RAID LOG — FORCA_WIN (família de robôs)

> **RAID** = Risks · Assumptions · Issues · Decisions
> Atualizar a cada mudança de lógica, parâmetro ou comportamento de saída.

---

## DECISIONS

| ID | Data | Versão | Decisão | Justificativa |
|----|------|--------|---------|---------------|
| D01 | 2026-06-05 | V16 | SL fixo em 75 pts (`StopMinimo=75`, `FatorRangeSL=0`) | Reduz exposição em relação ao V14 e cria RR nominal 2:1 com `TakeProfit=150`. |
| D02 | 2026-06-05 | V16 | TP fixo em 150 pts | O fonte atual não usa TP variável por zona; todo trade busca `TakeProfit=150`. |
| D03 | 2026-06-05 | V16 | Trailing proporcional ativo após BE para qualquer posição | Código usa `UsarTrailingProporcional=true` e não restringe por zona de entrada. |
| D04 | 2026-06-05 | V16 | `BreakEvenRatio=0.333` aplicado sobre `TakeProfit` | Com TP=150, BE clássico arma perto de 50 pts; cor oposta e 5 brancos também armam BE. |
| D05 | 2026-06-05 | V16 | MaxBarrasEmPosicao=6 (90min de exposição máxima) | WIN 15min: 6 candles = 90min. Evita posição aberta durante mudanças de contexto intraday. |
| D06 | 2026-06-05 | V16 | `TrailingPctInicial=0.62`, `TrailingPctPiso=0.10` | Com TP=150, trail inicial usa 62% da distância restante ao alvo e piso mínimo de 15 pts. |
| D07 | 2026-06-05 | V16 | Manter comentários no fonte até a V16 estabilizar | O robô ainda não foi rebacktestado; comentários ajudam auditoria manual no Profit. |
| D08 | 2026-06-05 | V14→V16 | UsarBEPorCorOposta=true + CandlesBrancosParaBE=5 | BE adaptativo: fecha no zero se surgir candle contra-tendência ou lateralização longa (5 brancos). |
| D09 | 2026-06-05 | V16 | UsarSLMenorQueSinal=false | SL fixo de 75 pts não deve ser reduzido pelo corpo do candle enquanto não houver backtest; evita stop excessivamente curto. |
| D10 | 2026-06-05 | V16 | `TakeProfit=150` usado em runtime | BE, trailing e TP hard usam o mesmo parâmetro `TakeProfit`. |
| D11 | 2026-06-05 | V16 | Volume mínimo filtra entrada, não pintura | O paintbar usa força/zona; o filtro `Volume >= 5000` só bloqueia ordens quando `UsarFiltroVolume=true`. |
| D12 | 2026-06-05 | V16 | Contexto substituído: iJanelaDir=5 / iJanelaCtx=20 (MA5 e MA20) | MA2/MA4 eram proxies sem valor estrutural real. MA5 (~1h15) reage rápido ao impulso da manhã; MA20 (~5h) ancora contexto do dia anterior. bDirAlta verifica cruzamento MA5 > MA20. Indicado para janela 10h–12h do WIN. |
| D13 | 2026-06-05 | V16 | RR nominal 2:1 (`SL=75`, `TP=150`) | Estrutura atual exige winrate menor que a variação TP curto anterior, mas ainda precisa validação estatística. |

---

## ASSUMPTIONS

| ID | Premissa | Impacto se falsa |
|----|----------|------------------|
| A01 | Range médio do WIN 15min ≈ 411 pts | SL/TP podem ser noise-level ou excessivos fora desta faixa |
| A02 | NTSL executa no fechamento do candle (não intrabar) | Hard SL via Low/High só dispara no candle seguinte |
| A03 | MA5/MA20 no mesmo timeframe é proxy suficiente de direção/contexto intraday | Pode filtrar tarde em reversões rápidas ou aceitar tendência já madura |
| A04 | Volume mínimo de 5000 filtra ruído sem eliminar entradas válidas em WIN | Pode filtrar excessivamente em períodos de baixa liquidez |
| A05 | Ponto do WIN = R$ 0,20 (mini-índice) | Sizing incorreto se operado no contrato cheio (R$ 1,00/pt) |

---

## ISSUES

| ID | Status | Versão | Descrição | Workaround |
|----|--------|--------|-----------|------------|
| I01 | Aberto | V16 | V16 não tem backtest registrado com SL=75, TP=150, BE 0.333 e trailing 0.62/0.10 | Rodar backtest antes de operar real. |
| I02 | Aberto | todos | NTSL não permite acesso a dados de outro timeframe — proxy via Media() | Confirmado e documentado em `/memories/repo/ntsl-limitacoes.md` |
| I03 | Aberto | V16 | `iQtd` é calculado por risco, mas ordens usam `BuyAtMarket`/`SellShortAtMarket` sem quantidade explícita | Confirmar sintaxe NTSL para ordem com quantidade e ajustar se suportado. |
| I04 | Fechado | V16 | MaxBarrasEmPosicao declarado duas vezes no bloco input → erro de sintaxe | Removida duplicata; mantida apenas no bloco SAIDAS |
| I05 | Aberto | V16 | `bAlertaTardio` existe no código mas `UsarAlertaMudancaTardia=false` — regra reservada | Manter para ativação futura; não gera impacto operacional. |
| I06 | Aberto | V16 | Janela de instabilidade é resetada em blocos de 5 candles, não deslizante | Avaliar implementação com histórico de zonas se NTSL suportar. |

---

## RISKS

| ID | Probabilidade | Impacto | Risco | Mitigação |
|----|--------------|---------|-------|-----------|
| R01 | Alta | Alto | V16 não foi rebacktestado com os parâmetros atuais | Backteste obrigatório antes de uso em conta real |
| R02 | Média | Alto | TP=150pts pode ser afetado por spread, slippage e execução em mercado rápido | Testar com simulation order no NeoTrader antes de live |
| R03 | Baixa | Médio | Trailing com piso de 10% do TP pode fechar cedo em candle volátil | Monitorar eficiência do trailing em backtest |
| R04 | Média | Médio | Alerta de instabilidade (cyano/fúcsia) pode pintar muitos candles em range lateral inibindo entradas | Ajustar MaxMudancasCor se ocorrer excesso visual |

---

## PARÂMETROS ATIVOS — V16 (snapshot)

```
ForcaMinimaForte  = 70
ForcaExaustao     = 85
ForcaAlerta       = 55
StopMinimo        = 75 pts
FatorRangeSL      = 0.0
TakeProfit        = 150 pts
BreakEvenRatio    = 0.333
TrailingPctInicial= 0.62
TrailingPctPiso   = 0.10
MaxBarrasEmPosicao= 6
iJanelaDir        = 5  (MA5 direcional)
iJanelaCtx        = 20 (MA20 contexto)
JanelaInstabilidade = 5
MaxMudancasCor    = 3
CandlesBrancosParaBE = 5
UsarSLMenorQueSinal = false
VolumeMinimo      = 5000
```
