# M02 — Registro de hipóteses (MB-H##)

Regras de veredito e congelamento: [`docs/01_CONVENCOES.md`](../../docs/01_CONVENCOES.md) §2. Template: [`docs/templates/HIPOTESE.md`](../../docs/templates/HIPOTESE.md).

> **Honestidade de procedimento.** MB-H01 a MB-H05 e MB-H13 a MB-H15 foram avaliadas na ANALISE_001 *depois* de ver parte dos números (análise exploratória do robô existente), portanto os vereditos abaixo valem como **exploratórios**. Para virar evidência, devem ser refeitas com regra congelada (novo ID) em dados novos.

## 1. Painel

| ID | Pergunta | Evidência (ANALISE_001) | Status | Veredito |
|---|---|---|---|---|
| MB-H01 | Após barra brilhante, o retorno futuro é no sentido do fade (alta → cai; baixa → sobe)? | Só WINFUT 1 min replica: h=1 brilhante alta −10,9 pts (t −3,06), brilhante baixa +10,4 (t +2,08). WINQ26 1 min: ~0 (t 0,09 / 0,58). WINFUT 5 min: sinais opostos em h=5/10; WINQ26 5 min h=1 com sinal oposto (+38,7; t 2,20) | EXECUTADA (exploratória) | **INCONCLUSIVA** — não replica |
| MB-H02 | O rompimento em fluxo neutro (ctx 3) tem continuação direcional? | 3.669 sinais WINFUT 1 min: −1,6 / −4,3 / −3,0 / +2,8 pts (h = 1/5/10/20), |t| ≤ 1,6; WINQ26 1 min h=20 −23,8 (t −2,0); 5 min: |t| ≤ 1 | EXECUTADA (exploratória) | **REFUTADA** (sem efeito detectável antes das barreiras) |
| MB-H03 | A geometria SL 0,5 × ATR (piso 35) / SG 2,5 × ATR (piso 120) tem esperança positiva com um sinal sem edge? | Nulo aleatório com a mesma saída: média −1,0 pt (WINFUT) e −2,1 (WINQ26) — negativo mesmo sem sinal; 64 % das saídas são SL; WR 19–21 % ≈ breakeven 21 % | EXECUTADA | **REFUTADA** (a geometria sozinha não cria vantagem) |
| MB-H04 | Com 2–5 pts de custo, o robô continua positivo? | Médio com custo 2 pts: −8,2 (WINFUT), −1,8 (WINQ26); com 5 pts: −11,2 (t −4,05) e −4,8 | EXECUTADA | **REFUTADA** (negativo com custo) |
| MB-H05 | O stop-limit com offset de 5 pts produz perdas acima do SL nominal (armadilha)? | Descritivo: 462 de 2.991 trades (15,4 %) tiveram stop passivo em algum momento: média −107 pts/trade (pior −1.585) contra +14,8 nos demais. **Não causal** (a armadilha só aparece em trades que já estão andando contra) | EXECUTADA (descritiva) | **CONFIRMADA** como risco de cauda; magnitude real depende do fill (ver MB-H12) |
| MB-H06 | Algumas horas têm esperança maior (janela de ouro vs tarde)? | Hora 10: −10,8 pts/trade; hora 11: +1,7; hora 16: +5,4 (n = 154). Sem t-stat; ruído provável | PENDENTE | — |
| MB-H07 | Limitar a frequência (cooldown, teto diário) reduz o custo sem perder o sinal? | ~30 trades/pregão; custo domina | PENDENTE | — |
| MB-H08 | O resultado depende do regime de ATR (alto × baixo, ATR vs ATR de 5 dias)? | não medido | PENDENTE | — |
| MB-H09 | O conceito sobrevive em 5 min (ATR 5×, piso de stop irrelevante)? | Perfil fiel: +4,0 / +9,6 / −5,5 pts por trade (WINFUT / WINM26 / WINQ26 5 min), t < 0,8; perfil ideal ≈ 0 | EXECUTADA | **INCONCLUSIVA** |
| MB-H10 | A barreira de tempo de 20 barras ajuda? | TEMPO: 103 trades, média −193 pts, mas confundida com a armadilha (stop passivo → só sai por tempo) | PENDENTE | — |
| MB-H11 | A estimativa do ATR incluindo a barra atual mascara extremos (como M01-H15) e muda a classificação "brilhante"? | não medido; no M01 a auto-inclusão limita z a √19 | PENDENTE | — |
| MB-H12 | **Paridade:** a réplica (avaliação no fechamento, fill no open seguinte) reproduz o trade log do robô no simulador do Profit? | não medido (precisa export do Profit nos mesmos pregões) | PENDENTE | — |
| MB-H13 | Em timeframes ≥ 30 min, a geometria SL curto/SG longo (≤ ~100 min) tem esperança positiva **mesmo com entrada aleatória** (efeito de autocorrelação positiva)? | WINFUT, entrada aleatória: 60 min +20,2 pts/trade (t 5,6; 11/12 anos positivos), 30 min +8,6 (t 3,8; 10/12); ≤ 15 min ≈ 0 ou negativo. ρ lag-1 do retorno ÷ ATR: +0,021 (t 3,3) em 60 min. **WDO não replica** (|t| ≤ 1,1 em todos os TFs) | EXECUTADA (exploratória, ANALISE_002) | **INCONCLUSIVA** — consistente no tempo no WIN, não replica no WDO |
| MB-H14 | A barra brilhante (≥ 1,7 × ATR) antecipa expansão do range seguinte em todos os timeframes (cor como alarme)? | Range seguinte ÷ média da hora: 1,29 (5 min), 1,22 (10), 1,15 (15), 1,14 (20), 1,20 (30), 1,15 (60); t por pregão 6,4 a 9,3. Replica M01 H20 | EXECUTADA (ANALISE_002) | **CONFIRMADA** (volatilidade, não direção) |
| MB-H15 | Em 20–60 min o sinal do M02 (ctx 1–3) supera a entrada aleatória com a mesma saída? | Percentil vs nulo (com 5 pts): 60 min 86–96, 30 min 90–98, 20 min 56–98, ≤ 15 min 8–60; mas o nulo já é positivo (MB-H13) e a vantagem sobre ele é pequena; sem t da diferença pareada | PENDENTE (exige teste pareado por pregão) | — |

## 2. Backlog priorizado

1. **MB-H12** (paridade) — sem ela, o resto é condicionado à réplica. Exportar o relatório de trades do Profit para os pregões 1 min de 2025-10 a 2025-12 e comparar entrada/saída/PnL trade a trade.
2. **Novos dados 1 min** (ver README): ≥ 300 pregões para qualquer teste de sinal com poder razoável.
3. **MB-H01 reformulada** com regra congelada: retorno a h=1/5 após barra brilhante, estratificado por hora e por direção do dia, em dados novos (novo ID `MB-H13`).
4. Deltas de execução (baratos, não dependem de sinal): `DELTA_001` stop a mercado, `DELTA_002` cooldown/teto diário — ver [`deltas/README.md`](deltas/README.md).
5. **MB-H08**/**MB-H06** só depois de haver dados para hold-out.

## 3. Ligações com o M01

| M02 | M01 |
|---|---|
| estado brilhante/escuro (range ÷ ATR) | estados 1,5σ/2,5σ de F = m·a (H10, H14) |
| MB-H01 (fade pós-brilhante) | H19 (brilhante = exaustão): INCONCLUSIVA em 5/15 min; H20 (brilhante antecipa **expansão** de range): CONFIRMADA |
| MB-H11 (auto-inclusão) | H15 CONFIRMADA |

Leitura combinada: no M01 o brilhante prevê **volatilidade**, não direção. É coerente com o M02 não ter edge direcional; o uso mais promissor do estado brilhante é como **filtro/dimensionamento** (aumentar alvo/stop, evitar entradas), não como gatilho de fade.

**Nota de correção (2026-10-22).** Os números de `WINM26` e `WINQ26` citados acima foram calculados antes de descartar os pregões de contrato sem liquidez (Quantidade diária < 1 milhão). Os valores recalculados estão em `analises/ANALISE_001_baseline.md` (por exemplo, WINQ26 1 min: 28 pregões, +1,5 pt/trade bruto, −3,5 com custo de 5 pts). Nenhum veredito acima muda de sentido; os números de WINFUT não mudam.
