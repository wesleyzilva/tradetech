# ANALISE_001 — Baseline do motor M02 (Robo_Microestrutura_Barreiras_v1)

> Gerado por `motores/M02_microestrutura_barreiras/codigo/analise_001.py`. **Não edite à mão**: reexecute o script.

## 1. Pergunta

O robô, exatamente como está no fonte NTSL de 22/10/2026, tem vantagem estatística nos candles de WIN que temos? Nenhum parâmetro foi otimizado: a réplica (`mb_motor.py`, validada por `tests/test_mb_motor.py`) usa os valores do fonte.

## 2. Dados usados

| conjunto | barras | pregões completos | início | fim |
|---|---|---|---|---|
| WINFUT 1min | 36.058 | 64 | 2025-09-29 | 2025-12-30 |
| WINQ26 1min | 19.552 | 35 | 2026-05-19 | 2026-07-24 |
| WINFUT 5min | 43.256 | 383 | 2024-06-19 | 2025-12-30 |
| WINM26 5min | 6.546 | 58 | 2026-02-19 | 2026-05-14 |
| WINQ26 5min | 7.764 | 69 | 2026-04-16 | 2026-07-24 |

Só entram pregões com ≥ 90 % das barras do p95 (descarta início ralo de contrato). Série **padrão** (sem `_alt`). O robô foi desenhado para 1 min: só há ~99 pregões nesse timeframe (ver `docs/auditorias/AUDITORIA_DADOS.md`). O 5 min entra como teste de **escala/robustez**, não como validação do robô (20 barras de 5 min = 100 min).

**Convenções da simulação:** sinal no fechamento → entrada na abertura seguinte; stop e alvo recalculados a cada barra (logo a barra de entrada fica sem proteção no perfil *fiel*; o perfil *ideal* assume ordens ativas desde a abertura); stop antes do alvo na mesma barra; custo e slippage em pontos por trade (aqui 0 salvo onde dito). Ver `METODO.md`.

## 3. Resultado bruto (sem custos)

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 1min — fiel | 1.970 | 64 | 30,8 | 18,8 | 21,1 | -6,19 | 0,87 | -2,27 | -12.194 | -14.598 | -1.017 |
| WINFUT 1min — ideal | 2.172 | 64 | 33,9 | 17,4 | 18,9 | -3,88 | 0,91 | -1,72 | -8.435 | -10.807 | -165 |
| WINQ26 1min — fiel | 1.021 | 35 | 29,2 | 21,4 | 21,3 | 0,21 | 1,00 | 0,03 | 216 | -5.200 | -1.585 |
| WINQ26 1min — ideal | 1.115 | 35 | 31,9 | 19,6 | 18,3 | 4,38 | 1,09 | 0,93 | 4.880 | -4.457 | -320 |
| WINFUT 5min — fiel | 2.559 | 383 | 6,7 | 20,8 | 20,1 | 4,03 | 1,05 | 0,74 | 10.325 | -12.997 | -2.086 |
| WINFUT 5min — ideal | 2.884 | 383 | 7,5 | 17,8 | 17,8 | -0,01 | 1,00 | -0,00 | -25 | -10.903 | -502 |
| WINM26 5min — fiel | 413 | 58 | 7,1 | 20,6 | 19,5 | 9,56 | 1,07 | 0,46 | 3.949 | -7.431 | -3.115 |
| WINM26 5min — ideal | 469 | 58 | 8,1 | 18,1 | 18,0 | 0,84 | 1,01 | 0,05 | 394 | -10.008 | -1.640 |
| WINQ26 5min — fiel | 472 | 69 | 6,8 | 21,8 | 22,7 | -5,48 | 0,95 | -0,32 | -2.587 | -14.871 | -1.915 |
| WINQ26 5min — ideal | 524 | 69 | 7,6 | 20,2 | 19,0 | 7,65 | 1,08 | 0,54 | 4.010 | -6.751 | -254 |

**Leitura:** `WR breakeven` é a taxa de acerto necessária dado o payoff observado; o robô fica abaixo dela quando `WR %` < `WR breakeven %`. `t (pregão)` agrega o PnL por pregão (cluster) — |t| < 2 não se distingue de ruído.

## 4. Sensibilidade a custos (perfil fiel)

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 1min — custo 0 pt | 1.970 | 64 | 30,8 | 18,8 | 21,1 | -6,19 | 0,87 | -2,27 | -12.194 | -14.598 | -1.017 |
| WINFUT 1min — custo 2 pt | 1.970 | 64 | 30,8 | 18,8 | 21,8 | -8,19 | 0,83 | -2,99 | -16.134 | -18.283 | -1.019 |
| WINFUT 1min — custo 5 pt | 1.970 | 64 | 30,8 | 18,7 | 22,9 | -11,19 | 0,78 | -4,05 | -22.044 | -23.842 | -1.022 |
| WINQ26 1min — custo 0 pt | 1.021 | 35 | 29,2 | 21,4 | 21,3 | 0,21 | 1,00 | 0,03 | 216 | -5.200 | -1.585 |
| WINQ26 1min — custo 2 pt | 1.021 | 35 | 29,2 | 21,4 | 21,8 | -1,79 | 0,97 | -0,28 | -1.826 | -5.946 | -1.587 |
| WINQ26 1min — custo 5 pt | 1.021 | 35 | 29,2 | 21,3 | 22,6 | -4,79 | 0,93 | -0,76 | -4.889 | -7.065 | -1.590 |

Custo realista de WIN (corretagem + emolumentos + slippage de uma ponta a mercado) fica na ordem de 2–5 pontos por volta; com ~30 trades por pregão o custo come toda a margem mesmo se houvesse edge bruto.

## 5. Decomposição (WINFUT + WINQ26 1 min, perfil fiel, sem custo)

### 5.1 Por contexto

Contexto 1 = fade de alta brilhante (vende); 2 = fade de baixa brilhante (compra); 3 = rompimento em fluxo neutro com SMA20.

| ctx | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| 1 — fade alta | 17 | 11,8 | -93,76 | 0,35 | -1.594 | -1.585 |
| 2 — fade baixa | 25 | 12,0 | -43,00 | 0,46 | -1.075 | -665 |
| 3 — fluxo neutro | 2.949 | 19,8 | -3,16 | 0,94 | -9.309 | -1.420 |

Sinais **gerados** (antes de descartar os que chegam com posição aberta): ctx 1: 18, ctx 2: 28, ctx 3: 5.532. Os fades (ctx 1 e 2) quase nunca disparam porque exigem *rompimento da mínima/máxima da barra brilhante já no fechamento da barra seguinte*; na prática o robô é um rompedor de fluxo neutro com SMA20.


### 5.2 Por motivo de saída

| motivo | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| SG | 539 | 100,0 | 252,76 | — | 136.240 | 120 |
| SL | 1.918 | 0,0 | -53,24 | 0,00 | -102.111 | -243 |
| STOP_PASSIVO | 431 | 0,5 | -60,90 | 0,00 | -26.246 | -150 |
| TEMPO | 103 | 45,6 | -192,83 | 0,18 | -19.861 | -1.585 |

`STOP_PASSIVO` = stop-limit enviado quando o fechamento já estava além do limite (a ordem fica passiva e só executa se o preço voltar): é a **armadilha do stop-limit** — a perda realizada excede em muito o SL nominal. `SL` e `SG` são as barreiras normais; `TEMPO` é a barreira temporal de 20 barras.

Saídas por `STOP_PASSIVO`: **431** trades (14,4 % do total) somam **-26.246 pts**; o PnL total do robô é -11.978 pts.

Trades em que o stop-limit chegou a ficar **passivo** em algum momento (armadilha), saindo por qualquer motivo:

| grupo | n | médio (pts) | total (pts) | pior (pts) |
|---|---|---|---|---|
| com armadilha | 462 | -107,18 | -49.516 | -1.585 |
| sem armadilha | 2.529 | 14,84 | 37.538 | -243 |

### 5.3 Por lado

| lado | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| venda | 1.494 | 19,0 | -6,57 | 0,87 | -9.810 | -1.585 |
| compra | 1.497 | 20,3 | -1,45 | 0,97 | -2.168 | -1.055 |

### 5.4 Por hora de entrada

| hora | n | WR % | médio (pts) | PF | total (pts) | pior (pts) |
|---|---|---|---|---|---|---|
| 9 | 477 | 20,3 | -4,22 | 0,93 | -2.012 | -1.055 |
| 10 | 601 | 19,8 | -10,76 | 0,86 | -6.469 | -1.585 |
| 11 | 634 | 19,9 | 1,72 | 1,03 | 1.090 | -660 |
| 12 | 13 | 15,4 | -2,54 | 0,95 | -33 | -150 |
| 14 | 573 | 19,7 | -2,85 | 0,92 | -1.635 | -515 |
| 15 | 539 | 16,9 | -6,96 | 0,79 | -3.752 | -505 |
| 16 | 154 | 26,0 | 5,41 | 1,18 | 833 | -188 |

### 5.5 Distância do stop

O stop nominal é `max(0,5×ATR, 35)`. Em **31,9 %** dos trades o piso de 35 pts é o que vale (ATR1min mediano na entrada = 97,8 pts; SL mediano = 48 pts; SG mediano = 238 pts). Um stop dessa ordem em 1 min está dentro do ruído de uma única barra.

MAE ≥ SL em 82,8 % dos trades; MFE ≥ SG em 19,0 %.

## 6. Controle: entrada aleatória com a mesma saída

Mesmas janelas, mesma frequência de sinais, lado sorteado, **mesma geometria de saída** (SL/SG/tempo, perfil fiel); 100 repetições. Se o robô não supera esse controle, o desempenho vem da geometria de saída e do custo, não do sinal.

| conjunto | robô: médio (pts) | nulo: média | nulo p5 | nulo p95 | percentil do robô | robô: PF | nulo: PF médio |
|---|---|---|---|---|---|---|---|
| WINFUT 1min | -6,19 | -1,02 | -5,87 | 4,31 | 3 | 0,87 | 0,98 |
| WINQ26 1min | 0,21 | -2,09 | -10,95 | 6,76 | 66 | 1,00 | 0,97 |

Percentil do robô acima de 95 indicaria sinal; abaixo de 5, sinal *pior* que o acaso.

## 7. Teste de hipótese de sinal: retorno futuro por estado (MB-H01)

Independente das barreiras: retorno da abertura da barra seguinte até o fechamento `h` barras depois, só dentro das janelas de entrada, por estado da barra de sinal. Se os fades (brilhante alta → cair; brilhante baixa → subir) existissem, `brilhante alta` teria retorno **negativo** e `brilhante baixa` **positivo**, com |t| ≥ 3.

| h (barras) | estado | n | retorno médio (pts) | incondicional (pts) | diferença (pts) | t (pregão) |
|---|---|---|---|---|---|---|
| 1 | neutro | 24.684 | 0,58 | 0,57 | 0,01 | 0,02 |
| 1 | escuro alta | 1.770 | -1,09 | 0,57 | -1,66 | -0,82 |
| 1 | escuro baixa | 1.712 | 1,63 | 0,57 | 1,05 | 0,53 |
| 1 | brilhante alta | 832 | -5,77 | 0,57 | -6,35 | -2,12 |
| 1 | brilhante baixa | 755 | 8,86 | 0,57 | 8,29 | 1,88 |
| 5 | neutro | 24.684 | 2,66 | 2,44 | 0,22 | 0,12 |
| 5 | escuro alta | 1.770 | 0,05 | 2,44 | -2,39 | -0,45 |
| 5 | escuro baixa | 1.712 | 4,90 | 2,44 | 2,46 | 0,49 |
| 5 | brilhante alta | 832 | -10,77 | 2,44 | -13,21 | -2,04 |
| 5 | brilhante baixa | 755 | 9,86 | 2,44 | 7,42 | 0,99 |
| 10 | neutro | 24.684 | 5,27 | 4,82 | 0,45 | 0,13 |
| 10 | escuro alta | 1.770 | 5,24 | 4,82 | 0,43 | 0,05 |
| 10 | escuro baixa | 1.712 | 4,38 | 4,82 | -0,44 | -0,06 |
| 10 | brilhante alta | 832 | -13,93 | 4,82 | -18,74 | -1,74 |
| 10 | brilhante baixa | 755 | 10,69 | 4,82 | 5,87 | 0,66 |
| 20 | neutro | 24.684 | 7,96 | 8,36 | -0,39 | -0,06 |
| 20 | escuro alta | 1.770 | 13,95 | 8,36 | 5,60 | 0,47 |
| 20 | escuro baixa | 1.712 | 4,59 | 8,36 | -3,77 | -0,31 |
| 20 | brilhante alta | 832 | -1,55 | 8,36 | -9,90 | -0,59 |
| 20 | brilhante baixa | 755 | 27,51 | 8,36 | 19,16 | 1,42 |

**Replicação por conjunto** (só estados brilhantes; 20 testes na tabela acima ⇒ um |t| ≈ 3 isolado não basta, o que importa é o sinal repetir em conjuntos independentes):

| conjunto | h (barras) | estado | n | diferença (pts) | t (pregão) |
|---|---|---|---|---|---|
| WINFUT 1min | 1 | brilhante alta | 498 | -10,92 | -3,06 |
| WINFUT 1min | 1 | brilhante baixa | 470 | 10,35 | 2,08 |
| WINFUT 1min | 5 | brilhante alta | 498 | -19,67 | -2,70 |
| WINFUT 1min | 5 | brilhante baixa | 470 | 2,24 | 0,23 |
| WINFUT 1min | 10 | brilhante alta | 498 | -21,08 | -2,00 |
| WINFUT 1min | 10 | brilhante baixa | 470 | 1,05 | 0,10 |
| WINQ26 1min | 1 | brilhante alta | 334 | 0,47 | 0,09 |
| WINQ26 1min | 1 | brilhante baixa | 285 | 4,89 | 0,58 |
| WINQ26 1min | 5 | brilhante alta | 334 | -3,59 | -0,30 |
| WINQ26 1min | 5 | brilhante baixa | 285 | 15,96 | 1,40 |
| WINQ26 1min | 10 | brilhante alta | 334 | -15,50 | -0,70 |
| WINQ26 1min | 10 | brilhante baixa | 285 | 13,68 | 0,87 |
| WINFUT 5min | 1 | brilhante alta | 755 | -6,29 | -0,79 |
| WINFUT 5min | 1 | brilhante baixa | 686 | 3,59 | 0,59 |
| WINFUT 5min | 5 | brilhante alta | 755 | 13,47 | 0,66 |
| WINFUT 5min | 5 | brilhante baixa | 686 | -1,93 | -0,13 |
| WINFUT 5min | 10 | brilhante alta | 755 | 15,75 | 0,60 |
| WINFUT 5min | 10 | brilhante baixa | 686 | -1,91 | -0,08 |
| WINM26 5min | 1 | brilhante alta | 105 | 6,93 | 0,28 |
| WINM26 5min | 1 | brilhante baixa | 127 | 17,18 | 0,87 |
| WINM26 5min | 5 | brilhante alta | 105 | 20,86 | 0,42 |
| WINM26 5min | 5 | brilhante baixa | 127 | 48,83 | 0,98 |
| WINM26 5min | 10 | brilhante alta | 105 | -82,67 | -1,17 |
| WINM26 5min | 10 | brilhante baixa | 127 | 38,55 | 0,51 |
| WINQ26 5min | 1 | brilhante alta | 157 | 38,65 | 2,20 |
| WINQ26 5min | 1 | brilhante baixa | 151 | 4,83 | 0,24 |
| WINQ26 5min | 5 | brilhante alta | 157 | -0,28 | -0,01 |
| WINQ26 5min | 5 | brilhante baixa | 151 | 0,43 | 0,01 |
| WINQ26 5min | 10 | brilhante alta | 157 | -30,25 | -0,50 |
| WINQ26 5min | 10 | brilhante baixa | 151 | -20,37 | -0,32 |

Critério (`docs/01_CONVENCOES.md`): mesmo sinal em ≥ 2 conjuntos independentes, |t| ≥ 3 na descoberta e |t| ≥ 2 no teste. O `t (pregão)` aqui é a média por pregão da soma dos desvios dos eventos em relação ao incondicional (pregões sem evento contam zero). A interpretação fica em `HIPOTESES.md` (MB-H01).

### 7.1 Retorno alinhado dos sinais do contexto 3 (MB-H02)

Todos os sinais de fluxo neutro (não só os que viram trade), retorno na direção do sinal da abertura seguinte até `h` barras depois. Positivo = o rompimento tem continuação; zero ou negativo = não há edge direcional antes das barreiras.

| conjunto | h (barras) | n sinais | retorno alinhado médio (pts) | % positivos | t (pregão) |
|---|---|---|---|---|---|
| WINFUT 1min | 1 | 3.669 | -1,58 | 47,5 | -1,62 |
| WINFUT 1min | 5 | 3.669 | -4,31 | 46,5 | -1,41 |
| WINFUT 1min | 10 | 3.669 | -3,03 | 46,4 | -0,70 |
| WINFUT 1min | 20 | 3.669 | 2,81 | 47,1 | 0,41 |
| WINQ26 1min | 1 | 1.863 | 0,69 | 45,4 | 0,36 |
| WINQ26 1min | 5 | 1.863 | 5,30 | 49,9 | 0,86 |
| WINQ26 1min | 10 | 1.863 | 8,15 | 49,8 | 1,02 |
| WINQ26 1min | 20 | 1.863 | -23,80 | 45,9 | -2,01 |
| WINFUT 5min | 1 | 4.517 | -0,57 | 47,2 | -0,30 |
| WINFUT 5min | 5 | 4.517 | 3,21 | 47,6 | 0,59 |
| WINFUT 5min | 10 | 4.517 | 0,98 | 48,5 | 0,12 |
| WINFUT 5min | 20 | 4.517 | -2,28 | 49,6 | -0,19 |
| WINM26 5min | 1 | 773 | 3,70 | 48,1 | 0,44 |
| WINM26 5min | 5 | 773 | 24,56 | 50,3 | 0,97 |
| WINM26 5min | 10 | 773 | 39,84 | 51,6 | 0,98 |
| WINM26 5min | 20 | 773 | -9,64 | 49,7 | -0,19 |
| WINQ26 5min | 1 | 858 | -1,71 | 47,9 | -0,30 |
| WINQ26 5min | 5 | 858 | -12,70 | 47,7 | -0,82 |
| WINQ26 5min | 10 | 858 | -14,74 | 47,0 | -0,55 |
| WINQ26 5min | 20 | 858 | -11,08 | 48,6 | -0,35 |

## 8. Teste de escala (5 min)

Mesmos parâmetros em barras de 5 min (ATR 5× maior, pisos de 35/120 pts irrelevantes, 20 barras = 100 min). Não valida o robô, mas diz se o conceito (fade de barra brilhante, rompimento neutro) sobrevive a uma escala em que o piso de stop não domina.

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 5min — fiel | 2.559 | 383 | 6,7 | 20,8 | 20,1 | 4,03 | 1,05 | 0,74 | 10.325 | -12.997 | -2.086 |
| WINFUT 5min — ideal | 2.884 | 383 | 7,5 | 17,8 | 17,8 | -0,01 | 1,00 | -0,00 | -25 | -10.903 | -502 |
| WINM26 5min — fiel | 413 | 58 | 7,1 | 20,6 | 19,5 | 9,56 | 1,07 | 0,46 | 3.949 | -7.431 | -3.115 |
| WINM26 5min — ideal | 469 | 58 | 8,1 | 18,1 | 18,0 | 0,84 | 1,01 | 0,05 | 394 | -10.008 | -1.640 |
| WINQ26 5min — fiel | 472 | 69 | 6,8 | 21,8 | 22,7 | -5,48 | 0,95 | -0,32 | -2.587 | -14.871 | -1.915 |
| WINQ26 5min — ideal | 524 | 69 | 7,6 | 20,2 | 19,0 | 7,65 | 1,08 | 0,54 | 4.010 | -6.751 | -254 |

## 9. Estabilidade temporal (perfil fiel, sem custo)

| cenário | n | pregões | trades/pregão | WR % | WR breakeven % | médio (pts) | PF | t (pregão) | total (pts) | DD máx (pts) | pior (pts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WINFUT 1min — 1ª metade | 959 | 32 | 30,0 | 20,8 | 20,4 | 0,99 | 1,02 | 0,28 | 951 | -4.623 | -960 |
| WINFUT 1min — 2ª metade | 1.011 | 32 | 31,6 | 16,9 | 21,4 | -13,00 | 0,75 | -3,47 | -13.145 | -13.245 | -1.017 |
| WINQ26 1min — 1ª metade | 511 | 17 | 30,1 | 23,7 | 23,1 | 2,04 | 1,03 | 0,23 | 1.042 | -4.406 | -1.585 |
| WINQ26 1min — 2ª metade | 510 | 18 | 28,3 | 19,0 | 19,5 | -1,62 | 0,97 | -0,17 | -826 | -5.200 | -665 |

## 10. Conclusões desta análise

1. **Sem vantagem bruta.** Perfil fiel, sem custo: média de -6,19 pts/trade (WINFUT) e 0,21 pts/trade (WINQ26); t por pregão de -2,27 e 0,03. Com custo, só piora (seção 4).
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

