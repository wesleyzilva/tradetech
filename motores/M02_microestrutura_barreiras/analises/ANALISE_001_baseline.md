# ANALISE_001 — Baseline do motor M02 (Robo_Microestrutura_Barreiras_v1)

> Gerado por `motores/M02_microestrutura_barreiras/codigo/analise_001.py`. **Não edite à mão**: reexecute o script.

## 1. Pergunta

O robô, exatamente como está no fonte NTSL de 22/10/2026, tem vantagem estatística nos candles de WIN que temos? Nenhum parâmetro foi otimizado: a réplica (`mb_motor.py`, validada por `tests/test_mb_motor.py`) usa os valores do fonte.

## 2. Dados usados

| conjunto | barras | pregões completos | início | fim |
|---|---|---|---|---|
| WINFUT 1min | 36.058 | 64 | 2025-09-29 | 2025-12-30 |
| WINQ26 1min | 15.768 | 28 | 2026-06-17 | 2026-07-24 |
| WINFUT 5min | 43.256 | 383 | 2024-06-19 | 2025-12-30 |
| WINM26 5min | 2.260 | 20 | 2026-04-15 | 2026-05-14 |
| WINQ26 5min | 3.164 | 28 | 2026-06-17 | 2026-07-24 |

Só entram pregões com ≥ 90 % das barras do p95 (descarta início ralo de contrato). Série **padrão** (sem `_alt`). O robô foi desenhado para 1 min: só há ~99 pregões nesse timeframe (ver `docs/auditorias/AUDITORIA_DADOS.md`). O 5 min entra como teste de **escala/robustez**, não como validação do robô (20 barras de 5 min = 100 min).

**Convenções da simulação:** sinal no fechamento → entrada na abertura seguinte; stop e alvo recalculados a cada barra (logo a barra de entrada fica sem proteção no perfil *fiel*; o perfil *ideal* assume ordens ativas desde a abertura); stop antes do alvo na mesma barra; custo e slippage em pontos por trade (aqui 0 salvo onde dito). Ver `METODO.md`.

## 3. Resultado bruto (sem custos)

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 1min — fiel | 1.970 | 64 | 30,8 | 18,8 | 21,1 | -6,19 | 0,87 | -2,27 | -12.194 | -14.598 | -1.017 |
| WINFUT 1min — ideal | 2.172 | 64 | 33,9 | 17,4 | 18,9 | -3,88 | 0,91 | -1,72 | -8.435 | -10.807 | -165 |
| WINQ26 1min — fiel | 792 | 28 | 28,3 | 20,1 | 19,7 | 1,49 | 1,03 | 0,20 | 1.184 | -5.200 | -1.585 |
| WINQ26 1min — ideal | 857 | 28 | 30,6 | 17,7 | 17,6 | 0,38 | 1,01 | 0,07 | 327 | -4.457 | -160 |
| WINFUT 5min — fiel | 2.559 | 383 | 6,7 | 20,8 | 20,1 | 4,03 | 1,05 | 0,74 | 10.325 | -12.997 | -2.086 |
| WINFUT 5min — ideal | 2.884 | 383 | 7,5 | 17,8 | 17,8 | -0,01 | 1,00 | -0,00 | -25 | -10.903 | -502 |
| WINM26 5min — fiel | 133 | 20 | 6,7 | 17,3 | 18,0 | -5,04 | 0,95 | -0,19 | -670 | -3.316 | -390 |
| WINM26 5min — ideal | 146 | 20 | 7,3 | 16,4 | 17,5 | -7,95 | 0,93 | -0,32 | -1.160 | -4.227 | -264 |
| WINQ26 5min — fiel | 179 | 28 | 6,4 | 22,3 | 19,3 | 22,39 | 1,20 | 0,74 | 4.008 | -4.428 | -1.655 |
| WINQ26 5min — ideal | 195 | 28 | 7,0 | 19,5 | 17,0 | 18,27 | 1,19 | 0,65 | 3.563 | -3.897 | -254 |

**Leitura:** `WR breakeven` é a taxa de acerto necessária dado o payoff observado; o robô fica abaixo dela quando `WR %` < `WR breakeven %`. `t (pregão)` agrega o PnL por pregão (cluster) — |t| < 2 não se distingue de ruído.

## 4. Sensibilidade a custos (perfil fiel)

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 1min — custo 0 pt | 1.970 | 64 | 30,8 | 18,8 | 21,1 | -6,19 | 0,87 | -2,27 | -12.194 | -14.598 | -1.017 |
| WINFUT 1min — custo 2 pt | 1.970 | 64 | 30,8 | 18,8 | 21,8 | -8,19 | 0,83 | -2,99 | -16.134 | -18.283 | -1.019 |
| WINFUT 1min — custo 5 pt | 1.970 | 64 | 30,8 | 18,7 | 22,9 | -11,19 | 0,78 | -4,05 | -22.044 | -23.842 | -1.022 |
| WINQ26 1min — custo 0 pt | 792 | 28 | 28,3 | 20,1 | 19,7 | 1,49 | 1,03 | 0,20 | 1.184 | -5.200 | -1.585 |
| WINQ26 1min — custo 2 pt | 792 | 28 | 28,3 | 20,1 | 20,2 | -0,51 | 0,99 | -0,07 | -400 | -5.946 | -1.587 |
| WINQ26 1min — custo 5 pt | 792 | 28 | 28,3 | 19,9 | 20,9 | -3,51 | 0,94 | -0,46 | -2.776 | -7.065 | -1.590 |

Custo realista de WIN (corretagem + emolumentos + slippage de uma ponta a mercado) fica na ordem de 2–5 pontos por volta; com ~30 trades por pregão o custo come toda a margem mesmo se houvesse edge bruto.

## 5. Decomposição (WINFUT + WINQ26 1 min, perfil fiel, sem custo)

### 5.1 Por contexto

Contexto 1 = fade de alta brilhante (vende); 2 = fade de baixa brilhante (compra); 3 = rompimento em fluxo neutro com SMA20.

| ctx | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| 1 — fade alta | 17 | 11,8 | -93,76 | 0,35 | -1.594 | -1.585 |
| 2 — fade baixa | 24 | 8,3 | -57,08 | 0,31 | -1.370 | -665 |
| 3 — fluxo neutro | 2.721 | 19,3 | -2,96 | 0,94 | -8.046 | -1.017 |

Sinais **gerados** (antes de descartar os que chegam com posição aberta): ctx 1: 18, ctx 2: 26, ctx 3: 5.052. Os fades (ctx 1 e 2) quase nunca disparam porque exigem *rompimento da mínima/máxima da barra brilhante já no fechamento da barra seguinte*; na prática o robô é um rompedor de fluxo neutro com SMA20.


### 5.2 Por motivo de saída

| motivo | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| SG | 483 | 100,0 | 251,96 | — | 121.699 | 120 |
| SL | 1.807 | 0,0 | -52,81 | 0,00 | -95.431 | -165 |
| STOP_PASSIVO | 381 | 0,0 | -61,82 | 0,00 | -23.552 | -150 |
| TEMPO | 91 | 50,5 | -150,84 | 0,23 | -13.726 | -1.585 |

`STOP_PASSIVO` = stop-limit enviado quando o fechamento já estava além do limite (a ordem fica passiva e só executa se o preço voltar): é a **armadilha do stop-limit** — a perda realizada excede em muito o SL nominal. `SL` e `SG` são as barreiras normais; `TEMPO` é a barreira temporal de 20 barras.

Saídas por `STOP_PASSIVO`: **381** trades (13,8 % do total) somam **-23.552 pts**; o PnL total do robô é -11.010 pts.

Trades em que o stop-limit chegou a ficar **passivo** em algum momento (armadilha), saindo por qualquer motivo:

| grupo | n | médio (pts) | total (pts) | pior (pts) |
|---|---|---|---|---|
| com armadilha | 409 | -99,79 | -40.814 | -1.585 |
| sem armadilha | 2.353 | 12,67 | 29.804 | -165 |

### 5.3 Por lado

| lado | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| venda | 1.368 | 18,1 | -6,90 | 0,86 | -9.441 | -1.585 |
| compra | 1.394 | 20,2 | -1,13 | 0,98 | -1.569 | -1.017 |

### 5.4 Por hora de entrada

| hora | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| 9 | 439 | 19,8 | -4,86 | 0,92 | -2.132 | -814 |
| 10 | 557 | 19,9 | -7,08 | 0,91 | -3.942 | -1.585 |
| 11 | 585 | 18,8 | -0,24 | 1,00 | -139 | -660 |
| 12 | 12 | 16,7 | 9,75 | 1,21 | 117 | -73 |
| 14 | 530 | 19,1 | -3,33 | 0,90 | -1.763 | -345 |
| 15 | 499 | 16,8 | -6,60 | 0,80 | -3.292 | -505 |
| 16 | 140 | 24,3 | 1,01 | 1,03 | 141 | -188 |

### 5.5 Distância do stop

O stop nominal é `max(0,5×ATR, 35)`. Em **32,1 %** dos trades o piso de 35 pts é o que vale (ATR1min mediano na entrada = 96,9 pts; SL mediano = 47 pts; SG mediano = 236 pts). Um stop dessa ordem em 1 min está dentro do ruído de uma única barra.

MAE ≥ SL em 83,2 % dos trades; MFE ≥ SG em 18,4 %.

## 6. Controle: entrada aleatória com a mesma saída

Mesmas janelas, mesma frequência de sinais, lado sorteado, **mesma geometria de saída** (SL/SG/tempo, perfil fiel); 100 repetições. Se o robô não supera esse controle, o desempenho vem da geometria de saída e do custo, não do sinal.

| conjunto | robô: médio (pts) | nulo: média | nulo p5 | nulo p95 | percentil do robô | robô: PF | nulo: PF médio |
|---|---|---|---|---|---|---|---|
| WINFUT 1min | -6,19 | -1,02 | -5,87 | 4,31 | 3 | 0,87 | 0,98 |
| WINQ26 1min | 1,49 | -1,79 | -10,87 | 7,56 | 70 | 1,03 | 0,97 |

Percentil do robô acima de 95 indicaria sinal; abaixo de 5, sinal *pior* que o acaso.

## 7. Teste de hipótese de sinal: retorno futuro por estado (MB-H01)

Independente das barreiras: retorno da abertura da barra seguinte até o fechamento `h` barras depois, só dentro das janelas de entrada, por estado da barra de sinal. Se os fades (brilhante alta → cair; brilhante baixa → subir) existissem, `brilhante alta` teria retorno **negativo** e `brilhante baixa` **positivo**, com |t| ≥ 3.

| h (barras) | estado | n | retorno médio (pts) | incondicional (pts) | diferença (pts) | t (pregão) |
|---|---|---|---|---|---|---|
| 1 | neutro | 22.957 | 0,82 | 0,67 | 0,16 | 0,38 |
| 1 | escuro alta | 1.674 | -2,02 | 0,67 | -2,68 | -1,29 |
| 1 | escuro baixa | 1.593 | 1,23 | 0,67 | 0,56 | 0,28 |
| 1 | brilhante alta | 774 | -7,70 | 0,67 | -8,36 | -2,95 |
| 1 | brilhante baixa | 686 | 10,12 | 0,67 | 9,45 | 2,02 |
| 5 | neutro | 22.957 | 3,21 | 2,57 | 0,64 | 0,35 |
| 5 | escuro alta | 1.674 | -3,30 | 2,57 | -5,87 | -1,13 |
| 5 | escuro baixa | 1.593 | 4,16 | 2,57 | 1,59 | 0,30 |
| 5 | brilhante alta | 774 | -14,14 | 2,57 | -16,71 | -2,76 |
| 5 | brilhante baixa | 686 | 10,66 | 2,57 | 8,09 | 1,06 |
| 10 | neutro | 22.957 | 6,14 | 5,04 | 1,10 | 0,32 |
| 10 | escuro alta | 1.674 | 1,59 | 5,04 | -3,45 | -0,44 |
| 10 | escuro baixa | 1.593 | 0,74 | 5,04 | -4,30 | -0,58 |
| 10 | brilhante alta | 774 | -18,65 | 5,04 | -23,69 | -2,25 |
| 10 | brilhante baixa | 686 | 13,34 | 5,04 | 8,29 | 0,92 |
| 20 | neutro | 22.957 | 10,02 | 8,91 | 1,10 | 0,16 |
| 20 | escuro alta | 1.674 | 6,93 | 8,91 | -1,99 | -0,18 |
| 20 | escuro baixa | 1.593 | -3,91 | 8,91 | -12,82 | -1,18 |
| 20 | brilhante alta | 774 | -11,50 | 8,91 | -20,41 | -1,23 |
| 20 | brilhante baixa | 686 | 29,66 | 8,91 | 20,75 | 1,53 |

**Replicação por conjunto** (só estados brilhantes; 20 testes na tabela acima ⇒ um |t| ≈ 3 isolado não basta, o que importa é o sinal repetir em conjuntos independentes):

| conjunto | h (barras) | estado | n | diferença (pts) | t (pregão) |
|---|---|---|---|---|---|
| WINFUT 1min | 1 | brilhante alta | 498 | -10,92 | -3,06 |
| WINFUT 1min | 1 | brilhante baixa | 470 | 10,35 | 2,08 |
| WINFUT 1min | 5 | brilhante alta | 498 | -19,67 | -2,70 |
| WINFUT 1min | 5 | brilhante baixa | 470 | 2,24 | 0,23 |
| WINFUT 1min | 10 | brilhante alta | 498 | -21,08 | -2,00 |
| WINFUT 1min | 10 | brilhante baixa | 470 | 1,05 | 0,10 |
| WINQ26 1min | 1 | brilhante alta | 276 | -3,80 | -0,81 |
| WINQ26 1min | 1 | brilhante baixa | 216 | 7,49 | 0,72 |
| WINQ26 1min | 5 | brilhante alta | 276 | -11,46 | -1,05 |
| WINQ26 1min | 5 | brilhante baixa | 216 | 20,81 | 1,94 |
| WINQ26 1min | 10 | brilhante alta | 276 | -28,84 | -1,27 |
| WINQ26 1min | 10 | brilhante baixa | 216 | 23,95 | 1,43 |
| WINFUT 5min | 1 | brilhante alta | 755 | -6,29 | -0,79 |
| WINFUT 5min | 1 | brilhante baixa | 686 | 3,59 | 0,59 |
| WINFUT 5min | 5 | brilhante alta | 755 | 13,47 | 0,66 |
| WINFUT 5min | 5 | brilhante baixa | 686 | -1,93 | -0,13 |
| WINFUT 5min | 10 | brilhante alta | 755 | 15,75 | 0,60 |
| WINFUT 5min | 10 | brilhante baixa | 686 | -1,91 | -0,08 |
| WINM26 5min | 1 | brilhante alta | 38 | -12,09 | -0,32 |
| WINM26 5min | 1 | brilhante baixa | 56 | 37,39 | 1,12 |
| WINM26 5min | 5 | brilhante alta | 38 | 33,10 | 0,51 |
| WINM26 5min | 5 | brilhante baixa | 56 | 46,66 | 0,59 |
| WINM26 5min | 10 | brilhante alta | 38 | -115,77 | -1,03 |
| WINM26 5min | 10 | brilhante baixa | 56 | 35,40 | 0,29 |
| WINQ26 5min | 1 | brilhante alta | 56 | 40,69 | 1,60 |
| WINQ26 5min | 1 | brilhante baixa | 49 | 44,62 | 1,53 |
| WINQ26 5min | 5 | brilhante alta | 56 | -18,66 | -0,23 |
| WINQ26 5min | 5 | brilhante baixa | 49 | 23,71 | 0,39 |
| WINQ26 5min | 10 | brilhante alta | 56 | -12,59 | -0,11 |
| WINQ26 5min | 10 | brilhante baixa | 49 | -29,50 | -0,32 |

Critério (`docs/01_CONVENCOES.md`): mesmo sinal em ≥ 2 conjuntos independentes, |t| ≥ 3 na descoberta e |t| ≥ 2 no teste. O `t (pregão)` aqui é a média por pregão da soma dos desvios dos eventos em relação ao incondicional (pregões sem evento contam zero). A interpretação fica em `HIPOTESES.md` (MB-H01).

### 7.1 Retorno alinhado dos sinais do contexto 3 (MB-H02)

Todos os sinais de fluxo neutro (não só os que viram trade), retorno na direção do sinal da abertura seguinte até `h` barras depois. Positivo = o rompimento tem continuação; zero ou negativo = não há edge direcional antes das barreiras.

| conjunto | h (barras) | n sinais | retorno alinhado médio (pts) | % positivos | t (pregão) |
|---|---|---|---|---|---|
| WINFUT 1min | 1 | 3.669 | -1,58 | 47,5 | -1,62 |
| WINFUT 1min | 5 | 3.669 | -4,31 | 46,5 | -1,41 |
| WINFUT 1min | 10 | 3.669 | -3,03 | 46,4 | -0,70 |
| WINFUT 1min | 20 | 3.669 | 2,81 | 47,1 | 0,41 |
| WINQ26 1min | 1 | 1.383 | -0,45 | 44,5 | -0,20 |
| WINQ26 1min | 5 | 1.383 | -0,74 | 48,3 | -0,12 |
| WINQ26 1min | 10 | 1.383 | 1,19 | 49,0 | 0,15 |
| WINQ26 1min | 20 | 1.383 | -26,16 | 45,8 | -2,46 |
| WINFUT 5min | 1 | 4.517 | -0,57 | 47,2 | -0,30 |
| WINFUT 5min | 5 | 4.517 | 3,21 | 47,6 | 0,59 |
| WINFUT 5min | 10 | 4.517 | 0,98 | 48,5 | 0,12 |
| WINFUT 5min | 20 | 4.517 | -2,28 | 49,6 | -0,19 |
| WINM26 5min | 1 | 219 | -2,88 | 47,0 | -0,28 |
| WINM26 5min | 5 | 219 | 2,37 | 48,4 | 0,07 |
| WINM26 5min | 10 | 219 | 3,49 | 51,6 | 0,06 |
| WINM26 5min | 20 | 219 | 26,28 | 52,1 | 0,37 |
| WINQ26 5min | 1 | 298 | -4,90 | 46,6 | -0,48 |
| WINQ26 5min | 5 | 298 | -20,35 | 47,0 | -0,85 |
| WINQ26 5min | 10 | 298 | -5,52 | 46,6 | -0,14 |
| WINQ26 5min | 20 | 298 | -18,24 | 48,7 | -0,45 |

## 8. Teste de escala (5 min)

Mesmos parâmetros em barras de 5 min (ATR 5× maior, pisos de 35/120 pts irrelevantes, 20 barras = 100 min). Não valida o robô, mas diz se o conceito (fade de barra brilhante, rompimento neutro) sobrevive a uma escala em que o piso de stop não domina.

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 5min — fiel | 2.559 | 383 | 6,7 | 20,8 | 20,1 | 4,03 | 1,05 | 0,74 | 10.325 | -12.997 | -2.086 |
| WINFUT 5min — ideal | 2.884 | 383 | 7,5 | 17,8 | 17,8 | -0,01 | 1,00 | -0,00 | -25 | -10.903 | -502 |
| WINM26 5min — fiel | 133 | 20 | 6,7 | 17,3 | 18,0 | -5,04 | 0,95 | -0,19 | -670 | -3.316 | -390 |
| WINM26 5min — ideal | 146 | 20 | 7,3 | 16,4 | 17,5 | -7,95 | 0,93 | -0,32 | -1.160 | -4.227 | -264 |
| WINQ26 5min — fiel | 179 | 28 | 6,4 | 22,3 | 19,3 | 22,39 | 1,20 | 0,74 | 4.008 | -4.428 | -1.655 |
| WINQ26 5min — ideal | 195 | 28 | 7,0 | 19,5 | 17,0 | 18,27 | 1,19 | 0,65 | 3.563 | -3.897 | -254 |

## 9. Estabilidade temporal (perfil fiel, sem custo)

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 1min — 1ª metade | 959 | 32 | 30,0 | 20,8 | 20,4 | 0,99 | 1,02 | 0,28 | 951 | -4.623 | -960 |
| WINFUT 1min — 2ª metade | 1.011 | 32 | 31,6 | 16,9 | 21,4 | -13,00 | 0,75 | -3,47 | -13.145 | -13.245 | -1.017 |
| WINQ26 1min — 1ª metade | 395 | 14 | 28,2 | 22,8 | 19,4 | 13,48 | 1,22 | 1,29 | 5.323 | -3.219 | -1.585 |
| WINQ26 1min — 2ª metade | 397 | 14 | 28,4 | 17,4 | 20,6 | -10,43 | 0,81 | -0,99 | -4.139 | -5.200 | -665 |

## 10. Conclusões desta análise

1. **Sem vantagem bruta.** Perfil fiel, sem custo: média de -6,19 pts/trade (WINFUT) e 1,49 pts/trade (WINQ26); t por pregão de -2,27 e 0,20. Com custo, só piora (seção 4).
2. **Frequência excessiva** (dezenas de trades por pregão) multiplica o custo; a barreira de 35 pts é ruído em 1 min.
3. **Risco estrutural de execução**: a barra de entrada sem proteção e o stop-limit passivo geram perdas muito maiores que o SL nominal (seção 5.2).
4. **O controle aleatório** (seção 6) separa o efeito do sinal do efeito da geometria de saída.
5. **As hipóteses de fade** (MB-H01, seção 7) devem ser lidas com o limiar |t| ≥ 3 do `docs/01_CONVENCOES.md`; todas as cifras acima são **amostras curtas** (≈ 99 pregões de 1 min) e não substituem uma validação com mais dados.

## 11. Limitações

- Amostra de 1 min: 64 + 35 pregões; os resultados têm largura de intervalo grande.
- Candles sem fila de ordens: não se sabe se o stop-limit realmente executaria; o modelo é pessimista (fiel) ou otimista (ideal), e a verdade está entre os dois.
- `Time` do NTSL assumido igual ao horário de abertura da barra do CSV.
- Preços de contratos distintos (WINFUT contínuo × WINQ26) são tratados separadamente; não há rolagem dentro de um mesmo conjunto 1 min.
- Volume do CSV é financeiro, não usado por este motor.

## 12. Próximos deltas sugeridos

Registrados em `HIPOTESES.md` (IDs `MB-H*`) com status; cada delta deve criar `deltas/DELTA_NNN_*.md` a partir do template `docs/templates/DELTA.md`.

