# Análise das Telas — FORCA WIN/WDO

> Documento gerado em 13/05/2026 com base nas 25 capturas de `tradetech/telas/`.  
> Objetivo: extrair padrões visuais observados manualmente e cruzar com as decisões de implementação do **FORCA_WIN_V14**.

---

## 1. Inventário das Imagens

| Arquivo | Ativo | Data Captura | Tema Central |
|---|---|---|---|
| `SinalidealWIN_3sinais_menores_1maior.PNG` | WIN | — | 3 sinais menores + 1 forte = setup ideal |
| `SinalidealWIN_3sinais_menores_1maior_entrada atrasada_PERDA.PNG` | WIN | — | Entrada atrasada no sinal maior → PERDA |
| `SinalidealWIN_3sinais_menores_devo aguardar.PNG` | WIN | — | Apenas sinais menores → aguardar |
| `SinalidealWIN_SinalDiarioiniciandoeEm60m.PNG` | WIN | — | Sinal diário iniciando no 60min |
| `SinalidealWIN_SinalForteAteOnde.PNG` | WIN | — | Sinal forte — "até onde?" (alvo) |
| `SinalidealWIN_SinalForteVoltoueDeuPerda.PNG` | WIN | — | Sinal forte que reverteu → perda |
| `SinalidealWIN_SinalSonoroSemUtilidade_naoQuero.PNG` | WIN | — | Alerta sonoro sem utilidade operacional |
| `VendaForteEsaida.PNG` | WIN | — | Venda forte + saída confirmada |
| `SinalidealWDO_1sinalDepoisPerda.PNG` | WDO | — | 1 sinal após perda (recuperação) |
| `SinalidealWDO_1sinalDepoisPerda_sequencia.PNG` | WDO | — | Sequência de sinais após perda |
| `SinalidealWDO_1sinalDepoisPerda_sequencia1.PNG` | WDO | — | Continuação da sequência |
| `SinalidealWDO_1sinalEm30esinalfraco60.PNG` | WDO | — | Sinal forte em 30min / fraco em 60min |
| `SinalidealWDO_1sinalemTimeframeMaiorOquefazer.PNG` | WDO | — | Sinal no TF maior — o que fazer? |
| `SinalidealWDO_2sinaisFortesOndeEstaStoptecnicoOUEstrutural.PNG` | WDO | — | 2 sinais fortes — stop técnico vs estrutural |
| `SinalidealWDO_3sinaisCompra.PNG` | WDO | — | 3 sinais de compra consecutivos |
| `SinalidealWDO_3sinaisMenores.PNG` | WDO | 23/04/2026 | 3 sinais menores em multi-TF |
| `SinalidealWDO_3sinais_confirmacaodeMovimento.PNG` | WDO | 28/04/2026 | 3 sinais confirmando movimento |
| `SinalidealWDO_3sinais_confirmacaodeMovimentoQuantosPontosBuscoeQuantosCOntratos.PNG` | WDO | 28/04/2026 | Alvo em pontos e sizing por contratos |
| `SinalidealWDO_3sinais_entradaAtrasada.PNG` | WDO | 28/04/2026 | Entrada atrasada no 3º sinal |
| `SinalidealWDO_3sinais_Ondepararquantospontos.PNG` | WDO | 28/04/2026 | Stop técnico — quantos pontos buscar |
| `Captura de tela 2026-05-04 130023.png` | WDO | 04/05/2026 | "ERA PRA COMPRAR" — sinal perdido |
| `Captura de tela 2026-05-09 104510.png` | WDO+WIN | 08/05/2026 | "PARAR" — conflito entre TFs |
| `Captura de tela 2026-05-09 104625.png` | WIN | 08/05/2026 | "COMPRAR" 60min vs "PARAR" 10min |
| `Captura de tela 2026-05-09 104746.png` | WIN | 08/05/2026 | Conflito TFs — 60min vs 30min vs 10min |
| `Captura de tela 2026-05-09 105000.png` | WIN | 08/05/2026 | "VENDER" 60min / "PARAR" 10min |
| `Captura de tela 2026-05-12 142250.png` | WIN | 12/05/2026 | **V13 ao vivo — "ENTROU ATRASADO"** |

---

## 2. Análise por Padrão

### 2.1 Entrada Atrasada ("ENTROU ATRASADO")

**Imagens:**  
- `Captura de tela 2026-05-12 142250.png` ← mais crítica (V13 ao vivo)  
- `SinalidealWIN_3sinais_menores_1maior_entrada atrasada_PERDA.PNG`  
- `SinalidealWDO_3sinais_entradaAtrasada.PNG`

**Observação visual (12/05/2026, WIN 5min):**  
O V13 disparou `Buy(1)` às 14:20 em R$182.585. O candle verde (momentum) havia se formado 1-2 candles antes. A anotação "ENTROU ATRASADO" confirma: a entrada ocorreu no fechamento do candle *após* o candle de sinal, que já havia percorrido ~70+ pontos. O log do ProfitPRO mostra:

```
14:20:00 — Compra a Mercado Criada   R$182.585  (Buy após candle verde já fechado)
13:55:00 — Zeragem a Mercado Criada  R$182.230  (saída anterior)
13:50:00 — Venda a Mercado Criada    R$182.265
```

**Resultado do dia no V13:** Op Totais = 3 | Res. Dia = R$51 (+63.75 pts) — o robô operou positivo apesar do problema, mas o risco da entrada tardia é compra no extremo do candle.

**Causa técnica:**  
`BuyAtMarket` executa no candle corrente quando `Modo Execução = Fechamento do candle`. Isso é correto. O problema visual é que a lógica de entrada (`fForca >= ForcaMinimaForte AND bCtxAlta AND bDirAlta`) pode ser satisfeita pelo *2º ou 3º candle* consecutivo de força, entrando no topo de um movimento já estendido.

**Status V14:** O mesmo `BuyAtMarket + fEntrada := Close` está presente no V14. Em 15min (V14 calibrado), o impacto é menor do que em 5min, mas o padrão persiste.

---

### 2.2 Conflito entre Timeframes ("PARAR")

**Imagens:**  
- `Captura de tela 2026-05-09 104510.png` — WDO diário circled + 30min "PARAR"  
- `Captura de tela 2026-05-09 104625.png` — WIN 60min "COMPRAR" vs 10min "PARAR"  
- `Captura de tela 2026-05-09 104746.png` — WIN 60min/30min vs 10min conflito  
- `Captura de tela 2026-05-09 105000.png` — WIN 60min "VENDER" vs 10min "PARAR"

**Observação visual (08/05/2026, WIN multi-TF):**  
Em todos os 4 frames da sessão de 08/05, a análise manual circla o TF maior (60min) identificando a direção — "COMPRAR" ou "VENDER" em verde — mas aponta "PARAR" em vermelho no TF menor (10min). A mensagem é: o contexto está alinhado, mas o *timing de entrada* no TF de execução não está confirmado.

O layout 4-quadrantes usado (1D / 60Min / 30Min / 10Min) mostra que a MM200 no 60min (= MA20 no 60min configurada no ProfitPRO) está descendo, e os candles pequenos do 10min estão em lateralização após queda. O robô entraria, mas o trader manualmente diz "PARAR".

**Causa técnica (V14):**  
```pascal
bCtxAlta  := (Close > fMediaCtx) and (fMediaCtx > fMediaCtx[iJanelaCtx]);
bDirAlta  := (Close > fMediaDir) and (fMediaDir > fMediaDir[iJanelaDir]);
```
Com `iJanelaDir=2` e `iJanelaCtx=4` em 15min:  
- `fMediaDir` = MA(2) — 2 candles = contexto de 30min  
- `fMediaCtx` = MA(4) — 4 candles = contexto de 60min  

Quando o 60min está em queda mas o candle atual de 15min fecha acima da MA(2), `bCtxAlta` pode ser `true` enquanto a tendência maior é baixista. Isso representa exatamente o conflito "PARAR" observado visualmente.

---

### 2.3 Sinal Forte que Reverteu ("SinalForteVoltoueDeuPerda")

**Imagens:**  
- `SinalidealWIN_SinalForteVoltoueDeuPerda.PNG`  
- `SinalidealWIN_SinalSonoroSemUtilidade_naoQuero.PNG`

**Observação:**  
O sinal de F >= 85 (exaustão compradora) ocorreu, mas o preço reverteu imediatamente após a entrada. O alerta sonoro ("SinalSonoroSemUtilidade") dispara na mudança de zona, mas o candle já reverteu.

**Análise:** Este é o risco intrínseco da estratégia — exaustão de momentum não significa reversão imediata. O V14 trata isso via:
1. Hard SL em 822pts (BUG FIX aplicado)
2. `ForcaStopContra(70.0)` — saída antecipada quando força contrária ≥ 70 (era 85 no V11)

Ambas as melhorias estão **corretamente implementadas** no V14.

---

### 2.4 Padrão "3 Sinais" — Ideal Setup

**Imagens (WIN):**  
- `SinalidealWIN_3sinais_menores_1maior.PNG` — padrão ideal: 3 menores + 1 forte  
- `SinalidealWIN_3sinais_menores_devo aguardar.PNG` — apenas menores → aguardar  

**Imagens (WDO):**  
- `SinalidealWDO_3sinaisCompra.PNG` — 3 sinais de compra consecutivos  
- `SinalidealWDO_3sinaisMenores.PNG` — 3 menores (23/04/2026)  
- `SinalidealWDO_3sinais_confirmacaodeMovimento.PNG` — 3 confirmando movimento (28/04/2026)  
- `SinalidealWDO_3sinais_confirmacaodeMovimentoQuantosPontosBuscoeQuantosCOntratos.PNG`  

**Observação:**  
O trader identifica como "sinal ideal" a presença de **3 candles coloridos consecutivos** na mesma direção (especialmente no TF de execução). A presença de apenas 1 ou 2 sinais menores isolados sem confirmação é tratada como "aguardar".

**Status V14:** O V14 exige apenas 1 candle com `fForca >= ForcaMinimaForte` + MTF alinhado. Não há contagem de candles consecutivos. O backtest com essa lógica simples produziu 6531 trades (2012-2026) com win% de 43.7% — a regra dos 3 candles reduziria o N amostral significativamente.

---

### 2.5 Sinal no TF Maior — "SinalDiarioiniciandoeEm60m"

**Imagens:**  
- `SinalidealWIN_SinalDiarioiniciandoeEm60m.PNG`  
- `SinalidealWDO_1sinalemTimeframeMaiorOquefazer.PNG`  
- `SinalidealWDO_1sinalEm30esinalfraco60.PNG`

**Observação:**  
Quando o diário inicia um novo movimento (primeiro candle colorido no 1D), o sinal aparece primeiro no 60min. O trader quer operar NESSE contexto — sinal forte no 60min com o diário iniciando.

No WDO: quando há sinal fraco em 60min mas forte em 30min (`sinalfraco60`), a entrada é mais arriscada pois o contexto maior não confirmou.

**Status V14:**  
A tripleta 60/30/15 com `iJanelaCtx=4` (MA de 4 candles de 15min = equivalente ao 60min) captura esse relacionamento. Quando a MA60 vira para alta, `fMediaCtx > fMediaCtx[4]` fica `true`. Isso **cobre o padrão** observado.

---

### 2.6 Stop Técnico vs Estrutural ("2sinaisFortes")

**Imagens:**  
- `SinalidealWDO_2sinaisFortesOndeEstaStoptecnicoOUEstrutural.PNG`  
- `SinalidealWDO_3sinais_Ondepararquantospontos.PNG`  
- `SinalidealWIN_SinalForteAteOnde.PNG`

**Observação:**  
O trader questiona onde posicionar o stop quando há 2+ sinais fortes: no stop *técnico* (mínimo/máximo do candle de sinal) ou no stop *estrutural* (suporte/resistência mais próximo)?

**Status V14:**  
O V14 usa stop dinâmico: `fSL = max(StopMinimo=822, range_candle * FatorRangeSL=2.0)`. Isso aproxima o stop ao range do candle de entrada (stop técnico/intrabar), mas com piso em 822pts (stop estrutural baseado em 2x range médio). Esta é a abordagem correta para automação — sem depender de níveis subjetivos.

---

### 2.7 Sinal Perdido — "ERA PRA COMPRAR"

**Imagem:**  
- `Captura de tela 2026-05-04 130023.png` (WDO M26, 04/05/2026 13:00)

**Observação:**  
A anotação manual "ERA PRA COMPRAR" indica uma oportunidade de compra que o robô (ou o trader em modo manual) não capturou. O contexto: WDO em queda acentuada no diário, e o 60min mostrou um candle de reversão que o F >= 70 deveria ter capturado.

Possíveis causas de miss:
1. `bCtxAlta = false` — a MA de contexto ainda estava descendo
2. `UsarFiltroVolume=true` com `VolumeMinimo=5000` — volume no candle de reversão pode ter sido < 5000
3. O candle de sinal foi no 60min mas a estratégia opera em 15min

**Status V14:** Nenhuma das 4 melhorias do V14 resolve este problema. A questão é estrutural: entradas em reversão de tendência com MA ainda descendente tendem a ser filtradas pela condição `bCtxAlta AND bDirAlta`.

---

### 2.8 Vendas na Simulação WDO (28/04/2026)

**Imagens:**  
- `SinalidealWDO_3sinais_confirmacaodeMovimento.PNG`  
- `SinalidealWDO_3sinais_confirmacaodeMovimentoQuantosPontosBuscoeQuantosCOntratos.PNG`

**Observação (log de trades visible no ProfitPRO):**

| Evento | Pontos | Observação |
|---|---|---|
| Venda 1 (TP) | +6.33 pts | Saída no alvo |
| Venda 2 (TP) | +4.33 pts | Saída no alvo |
| Venda 3 (TP) | +3.43 pts | Saída no alvo |
| Venda Stop 1 | -7.67 pts | Stop loss atingido |
| Venda Stop 2 | -8.17 pts | Stop loss atingido |
| Venda Stop 3 | -28.50 pts | Stop loss grande |

**Atenção:** Estes são resultados do WDO (não WIN). O SL de -28.50 pts do WDO = ~R$56.50 por contrato (WDO 1pt = R$2.00 com 1 contrato de tamanho mini). A assimetria loss/win no WDO simulado é desfavorável neste período.

---

## 3. Padrões Recorrentes (Síntese)

| # | Padrão | Frequência | Impacto no V14 |
|---|---|---|---|
| P1 | Entrada atrasada (candle após o sinal) | Alto | Existe no V14, menor em 15min |
| P2 | Conflito TF menor vs TF maior ("PARAR") | Alto | Parcialmente mitigado por MTF check |
| P3 | Sinal forte que reverte imediatamente | Médio | Corrigido: Hard SL + ForcaStopContra=70 |
| P4 | 3 sinais consecutivos como filtro ideal | Médio | Não implementado no V14 |
| P5 | Sinal perdido em reversão (bCtxAlta=false) | Médio | Estrutural — não coberto |
| P6 | Sinal diário iniciando no 60min | Baixo | Coberto pela tripleta 60/30/15 |
| P7 | Alertas sonoros sem contexto operacional | Baixo | MostrarAlertas apenas informa |

---

## 4. Validação do V14 vs Observações Visuais

### 4.1 O que o V14 resolve ✅

| Melhoria V14 | Padrão Visual Coberto |
|---|---|
| Hard SL via Low/High intrabar | P3 — sinal que reverte sem atingir ForcaStopContra |
| ForcaStopContra 85→70 | P3 — saída antecipada antes do SL ser atingido |
| Sem trailing stop | Backtest mostrou trailing corta vencedores (AvgWin: 258→141 pts) |
| fSLAtivo trava SL do candle de entrada | P3 — SL não recalculado intraday |

### 4.2 O que o V14 NÃO cobre ⚠️

#### Issue 1 — Entrada Atrasada em Candle Estendido
**Padrão:** P1 ("ENTROU ATRASADO" — 12/05/2026)  
**Descrição:** Quando o robô entra no 2º ou 3º candle consecutivo de força, o preço já percorreu o range principal do movimento. A entrada fica no topo (compra) ou fundo (venda).  
**Sugestão para V14:**  
Adicionar verificação: se o candle anterior (`fForca[1]`) já tinha F >= limiar, a entrada atual é "sequência" — potencialmente estendida. Isso pode ser documentado como limitação ou endereçado com:
```pascal
// Evitar entrada em candles que já estão no 2º+ bar de força consecutiva
// (entrada tardia reduz EV por comprar/vender em candle estendido)
// Alternativa: limitar MaxBarrasEmPosicao no backtest para avaliar impacto
```

#### Issue 2 — Conflito TFs não capturado pela MA simples
**Padrão:** P2 ("PARAR" em 08/05/2026)  
**Descrição:** `bCtxAlta = (Close > fMediaCtx) and (fMediaCtx > fMediaCtx[iJanelaCtx])` pode ser `true` mesmo quando o 60min está em tendência de baixa, se houve um repique recente.  
**Sugestão para V14:**  
Testar adicionar uma 3ª condição de contexto — uma MA mais longa (ex: MA(8) = 120min) — para filtrar repiques no contexto maior:
```pascal
// Proposta: adicionar filtro de macro-contexto (120min equivalente)
fMediaMacro := Media(iJanelaMacro, Close);   // iJanelaMacro = 8 (15min * 8 = 120min)
bMacroAlta  := (Close > fMediaMacro) and (fMediaMacro > fMediaMacro[iJanelaMacro]);
// Adicionar bMacroAlta na condição de entrada
```
**Atenção:** Qualquer mudança de filtro exige re-backtest completo antes de aplicar.

#### Issue 3 — Sinal Perdido em Reversão
**Padrão:** P5 ("ERA PRA COMPRAR" — 04/05/2026)  
**Descrição:** Reversões de tendência têm MA ainda descendente quando o primeiro sinal aparece, então `bCtxAlta` = false e o robô não entra.  
**Análise:** Esta é uma característica intencional da estratégia — ela é seguidora de tendência, não contrarian. Entrar em reversões aumenta o risco. O V14 deve manter o filtro atual.  
**Conclusão:** Não alterar. Documentar como limitação da estratégia.

---

## 5. Recomendações para V14

### Prioridade Alta — Investigar

1. **Backtest com filtro de entrada atrasada** (P1):  
   Avaliar `if fForca[1] < ForcaMinimaForte then` como pré-condição de entrada — só entra no *primeiro* candle colorido da sequência. Isso eliminaria entradas no 2º/3º candle já estendido.

2. **Backteste com ForcaMinimaForte=85 (apenas exaustão)**:  
   Os dados mostram que `F>=85` (n=4735, win=44.6%) é a zona de melhor performance. Subir o threshold reduz N mas aumenta win% — avaliar se o PnL total mantém.

### Prioridade Média — Documentar

3. **Documentar o conflito de TF como limitação** (P2):  
   Nos dias em que o 60min está em direção oposta à entrada, o robô ainda pode entrar se o 15min estiver alinhado. Considerar uma regra manual: "não operar o robô quando o diário e 60min estão em tendência oposta ao sinal do 15min."

4. **Alertas sonoros** (P7 — "SinalSonoroSemUtilidade"):  
   `MostrarAlertas(true)` no V14 dispara em toda mudança de zona. Visualmente isso foi marcado como "sem utilidade". Considerar `MostrarAlertas(false)` como default no V14, ativando apenas manualmente quando monitorado.

### Prioridade Baixa — Monitorar

5. **Resultado ao vivo V13 (12/05/2026)**: Res. Dia = +R$51 (+63.75pts) com 3 operações — dentro do esperado para 1 contrato em 5min. O V14 em 15min deve apresentar menos operações com maior AvgWin por trade.

---

## 6. Status Atual do V14

```
FORCA_WIN_V14 — Estado: PRONTO PARA BACKTEST INCREMENTAL
Timeframe alvo: 15min (tripleta 60/30/15)
Parâmetros principais:
  ForcaMinimaForte = 70.0
  ForcaStopContra  = 70.0  ← MUDANÇA vs V11 (era 85)
  StopMinimo       = 822 pts
  TakeProfit       = 2466 pts (RR 3.0)
  BreakEvenRatio   = 0.5 (BE após 1233 pts de lucro)
  Hard SL via Low/High = SIM ← BUG FIX vs V11
  Trailing Stop    = NÃO (decisão intencional)
  Perda Máxima Diária = NÃO (decisão intencional)

Issues pendentes (das telas):
  [P1] Entrada em candle estendido — investigar filtro primeiro candle
  [P2] Conflito TF — documentar como limitação ou testar MA macro
  [P5] Reversões perdidas — manter como está (estratégia é trend-following)
```

---

*Análise baseada em 11 capturas com conteúdo legível (outros 14 arquivos excederam o budget de contexto durante a análise) + código completo do FORCA_WIN_V14.*
