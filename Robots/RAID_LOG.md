# RAID LOG — FORCA_WIN (família de robôs)

> **RAID** = Risks · Assumptions · Issues · Decisions
> Atualizar a cada mudança de lógica, parâmetro ou comportamento de saída.

---

## DECISIONS

| ID | Data | Versão | Decisão | Justificativa |
|----|------|--------|---------|---------------|
| D01 | 2026-06-05 | V16 | SL fixo em 150 pts (FatorRangeSL=0) | Stop real observado nas telas de análise (stop0f. 150). SL por range produzia stops instáveis em WIN 15min. |
| D02 | 2026-06-05 | V16 | TP dinâmico por zona de entrada: exaustão=100pts / forte=50pts | Sinal de exaustão (F≥85) justifica alvo maior. Sinal forte (F 70–84) é mais fraco — alvo menor reduz exposição. |
| D03 | 2026-06-05 | V16 | Trailing ativo apenas para entradas em zona de exaustão (iZonaEntrada=±2) | Exaustão sinaliza impulso forte: deixar correr com trailing captura mais. Forte (±1): só BE, sem trailing — protege no zero sem arriscar reversão. |
| D04 | 2026-06-05 | V16 | BreakEvenRatio=0.333 aplicado sobre fTPAtivo | BE proporcional ao TP ativo: zona 2 arma em ~33pts, zona 1 em ~17pts. Mantém consistência relativa independente do TP. |
| D05 | 2026-06-05 | V16 | MaxBarrasEmPosicao=6 (90min de exposição máxima) | WIN 15min: 6 candles = 90min. Evita posição aberta durante mudanças de contexto intraday. |
| D06 | 2026-06-05 | V16 | TrailingPctInicial=0.62, TrailingPctPiso=0.10 | Com fTPAtivo=100pts: trail inicia em ~62pts, piso=10pts. Proporcional ao alvo da operação. |
| D07 | 2026-06-05 | V16 | Comentários explicativos removidos do código | Código limpo; toda documentação de decisão centralizada neste RAID log. |
| D08 | 2026-06-05 | V14→V16 | UsarBEPorCorOposta=true + CandlesBrancosParaBE=5 | BE adaptativo: fecha no zero se surgir candle contra-tendência ou lateralização longa (5 brancos). |
| D09 | 2026-06-05 | V16 | UsarSLMenorQueSinal=false | SL fixo de 150pts não deve ser reduzido pelo corpo do candle de entrada — evita stop muito curto. |
| D10 | 2026-06-05 | V16 | TakeProfit(450) mantido no input block como referência | Não é usado em runtime (substituído por fTPAtivo). Mantido para não quebrar o parser NTSL. |
| D11 | 2026-06-05 | V16 | Volume < fVolMedia → candle pintado branco (sem cor de sinal) | Volume abaixo da média indica movimento sem confirmação. Sinal de força sem volume não deve induzir entrada visual. Alerta de instabilidade (cyano/fúcsia) mantém override independente do volume. |
| D12 | 2026-06-05 | V16 | Contexto substituído: iJanelaDir=5 / iJanelaCtx=20 (MA5 e MA20) | MA2/MA4 eram proxies sem valor estrutural real. MA5 (~1h15) reage rápido ao impulso da manhã; MA20 (~5h) ancora contexto do dia anterior. bDirAlta verifica cruzamento MA5 > MA20. Indicado para janela 10h–12h do WIN. |
| D13 | 2026-06-05 | V16 | SL e TP dinâmicos por zona com RR 2:1 | Zona 1 (cor clara): SL=75, TP=150, BE~50pts. Zona 2 (cor escura): SL=100, TP=250, BE~83pts. Objetivo: positivas (TP), breakeven (BE armado + retorno), negativas (SL imediato). RR 2:1 e 2.5:1 respectivamente — breakeven a 34% de acerto. |
| D12 | 2026-06-05 | V16 | Contexto substituído: iJanelaDir=9 / iJanelaCtx=20 (MA9 e MA20) | MA2/MA4 eram proxies de 30/60min mas cobriam apenas 2–4 candles — sem valor estrutural real. MA9 (~2h15) e MA20 (~5h) no 15min mapeiam estrutura intraday usada pelo operador no diário. bDirAlta agora verifica cruzamento MA9 > MA20 (alinhamento estrutural) em vez de lookback curto. |

---

## ASSUMPTIONS

| ID | Premissa | Impacto se falsa |
|----|----------|------------------|
| A01 | Range médio do WIN 15min ≈ 411 pts | SL/TP podem ser noise-level ou excessivos fora desta faixa |
| A02 | NTSL executa no fechamento do candle (não intrabar) | Hard SL via Low/High só dispara no candle seguinte |
| A03 | Multi-TF via Media(iJanelaDir/Ctx, Close) é proxy válido para 30min/60min no chart de 15min | Sinal MTF pode estar defasado em até 1 candle |
| A04 | Volume mínimo de 5000 filtra ruído sem eliminar entradas válidas em WIN | Pode filtrar excessivamente em períodos de baixa liquidez |
| A05 | Ponto do WIN = R$ 0,20 (mini-índice) | Sizing incorreto se operado no contrato cheio (R$ 1,00/pt) |

---

## ISSUES

| ID | Status | Versão | Descrição | Workaround |
|----|--------|--------|-----------|------------|
| I01 | Aberto | V16 | RR negativo: SL=150 vs TP=100 (zona 2) = RR 0.67:1; TP=50 (zona 1) = RR 0.33:1 | Estratégia depende de alta taxa de acerto. Monitorar winrate em backtest antes de operar real. |
| I02 | Aberto | todos | NTSL não permite acesso a dados de outro timeframe — proxy via Media() | Confirmado e documentado em `/memories/repo/ntsl-limitacoes.md` |
| I03 | Aberto | V16 | fTPAtivo=0 no início antes da primeira entrada pode causar divisão por zero no BE se BreakEvenRatio for aplicado sem posição | Guard `if fTPAtivo > 0` pode ser necessário em versão futura |
| I04 | Fechado | V16 | MaxBarrasEmPosicao declarado duas vezes no bloco input → erro de sintaxe | Removida duplicata; mantida apenas no bloco SAIDAS |
| I05 | Aberto | V16 | bAlertaTardio existe no código mas UsarAlertaMudancaTardia=false — dead code | Manter para ativação futura; não gera impacto operacional |

---

## RISKS

| ID | Probabilidade | Impacto | Risco | Mitigação |
|----|--------------|---------|-------|-----------|
| R01 | Alta | Alto | V16 não foi rebacktestado com os parâmetros atuais (TP dinâmico por zona) | Backteste obrigatório antes de uso em conta real |
| R02 | Média | Alto | TP=50pts para zona forte pode ser atingido por spread + slippage em mercado rápido | Testar com simulation order no NeoTrader antes de live |
| R03 | Baixa | Médio | Trailing com passo muito pequeno próximo do TP (piso=10% de fTPAtivo) pode gerar stop e reversão falsa | Monitorar eficiência do trailing em backtest |
| R04 | Média | Médio | Alerta de instabilidade (cyano/fúcsia) pode pintar muitos candles em range lateral inibindo entradas | Ajustar MaxMudancasCor se ocorrer excesso visual |

---

## PARÂMETROS ATIVOS — V16 (snapshot)

```
ForcaMinimaForte  = 70
ForcaExaustao     = 85
StopMinimo        = 150 pts
fTPAtivo (zona ±2)= 100 pts  ← exaustão
fTPAtivo (zona ±1)=  50 pts  ← forte
BreakEvenRatio    = 0.333
TrailingPctInicial= 0.62
TrailingPctPiso   = 0.10
MaxBarrasEmPosicao= 6
iJanelaDir        = 2  (proxy ~30min)
iJanelaCtx        = 4  (proxy ~60min)
JanelaInstabilidade = 5
MaxMudancasCor    = 3
CandlesBrancosParaBE = 5
```
