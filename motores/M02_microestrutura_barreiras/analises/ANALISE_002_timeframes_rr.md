# ANALISE_002 — Risco/retorno por timeframe e cor como alarme (M02)

> Gerado por `motores/M02_microestrutura_barreiras/codigo/analise_002_timeframes.py`. Não editar à mão.

## 1. Perguntas

1. Em qual timeframe e com qual razão SL:SG o sinal do M02 supera o acaso **com custo**?
2. A barra brilhante (a cor do robô) é um alarme de volatilidade em todos os timeframes?

## 2. Dados e grade (pré-declarada)

WINFUT contínuo, série padrão, pregões completos. Mesmos sinais do robô (3 contextos, mesmas janelas), pisos de 35/120 pts desligados (só fazem sentido em 1 min), tempo máximo ≈ 100 minutos em qualquer TF, custo de 5 pts/trade, entrada na abertura seguinte, stop primeiro. Grade: 6 TFs × 4 geometrias = 24 combinações — **nenhuma foi escolhida a posteriori**; com 24 testes, esperar ~1 combinação com |t| ≥ 2 por acaso.

| TF | barras | pregões | início | fim | ATR mediano (pts) | custo 5 pts ÷ ATR | barras de tempo |
|---|---|---|---|---|---|---|---|
| 5 min | 43.256 | 383 | 2024-06-19 | 2025-12-30 | 159 | 3.1 % | 20 |
| 10 min | 46.512 | 827 | 2022-09-01 | 2025-12-30 | 265 | 1.9 % | 10 |
| 15 min | 47.655 | 1.280 | 2020-11-04 | 2025-12-30 | 388 | 1.3 % | 7 |
| 20 min | 51.777 | 1.853 | 2018-07-06 | 2025-12-30 | 491 | 1.0 % | 5 |
| 30 min | 54.050 | 2.937 | 2014-01-02 | 2025-12-30 | 596 | 0.8 % | 4 |
| 60 min | 27.618 | 2.937 | 2014-01-02 | 2025-12-30 | 851 | 0.6 % | 4 |

O custo fixo pesa 1/20 do ATR em 60 min mas mais de 1/5 em 5 min: **a escala favorece timeframes maiores por custo**, não por sinal.

## 3. Risco/retorno × timeframe — perfil ideal (limite superior; ordens ativas desde a abertura)

| TF | SL×ATR | SG×ATR | RR nominal | n | trades/pregão | WR % | WR breakeven % | bruto (pts) | líquido 5 pts | PF líq. | t (pregão) | percentil vs nulo | nulo líq. médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 min | 0,5 | 2,5 | 5,0 | 2.884 | 7,5 | 17,8 | 18,7 | -0,01 | -5,01 | 0,94 | -1,15 | 60 | -6,11 |
| 5 min | 1,0 | 2,0 | 2,0 | 2.353 | 6,1 | 35,6 | 35,2 | 7,02 | 2,02 | 1,02 | 0,33 | 94 | -6,64 |
| 5 min | 1,0 | 3,0 | 3,0 | 2.078 | 5,4 | 31,4 | 30,4 | 11,21 | 6,21 | 1,05 | 0,83 | 92 | -4,38 |
| 5 min | 1,0 | 1,0 | 1,0 | 3.043 | 7,9 | 50,4 | 50,7 | 3,99 | -1,01 | 0,99 | -0,28 | 98 | -6,61 |
| 10 min | 0,5 | 2,5 | 5,0 | 2.891 | 3,5 | 21,9 | 23,8 | -6,73 | -11,73 | 0,90 | -2,07 | 12 | -5,76 |
| 10 min | 1,0 | 2,0 | 2,0 | 2.530 | 3,1 | 38,7 | 39,7 | -1,53 | -6,53 | 0,96 | -0,83 | 52 | -7,29 |
| 10 min | 1,0 | 3,0 | 3,0 | 2.439 | 3,0 | 36,4 | 37,3 | -1,38 | -6,38 | 0,96 | -0,74 | 36 | -4,59 |
| 10 min | 1,0 | 1,0 | 1,0 | 2.943 | 3,6 | 49,9 | 51,6 | -3,94 | -8,94 | 0,94 | -1,61 | 26 | -6,56 |
| 15 min | 0,5 | 2,5 | 5,0 | 3.115 | 2,5 | 25,8 | 27,2 | -5,71 | -10,71 | 0,93 | -1,38 | 24 | -3,98 |
| 15 min | 1,0 | 2,0 | 2,0 | 2.794 | 2,3 | 40,2 | 42,0 | -10,81 | -15,81 | 0,93 | -1,59 | 12 | -4,40 |
| 15 min | 1,0 | 3,0 | 3,0 | 2.727 | 2,2 | 39,1 | 40,8 | -11,23 | -16,23 | 0,93 | -1,51 | 8 | -2,14 |
| 15 min | 1,0 | 1,0 | 1,0 | 3.122 | 2,5 | 48,1 | 49,9 | -8,18 | -13,18 | 0,93 | -1,68 | 30 | -8,69 |
| 20 min | 0,5 | 2,5 | 5,0 | 3.361 | 2,0 | 31,5 | 30,3 | 16,15 | 11,15 | 1,06 | 1,20 | 98 | -1,83 |
| 20 min | 1,0 | 2,0 | 2,0 | 3.109 | 1,8 | 45,4 | 45,3 | 6,22 | 1,22 | 1,00 | 0,11 | 56 | -1,84 |
| 20 min | 1,0 | 3,0 | 3,0 | 3.079 | 1,8 | 44,9 | 43,7 | 18,39 | 13,39 | 1,05 | 1,11 | 90 | 0,28 |
| 20 min | 1,0 | 1,0 | 1,0 | 3.357 | 2,0 | 50,4 | 50,6 | 3,89 | -1,11 | 1,00 | -0,12 | 84 | -8,77 |
| 30 min | 0,5 | 2,5 | 5,0 | 3.921 | 1,6 | 33,6 | 31,7 | 23,85 | 18,85 | 1,09 | 1,98 | 98 | 3,88 |
| 30 min | 1,0 | 2,0 | 2,0 | 3.716 | 1,5 | 46,4 | 44,5 | 26,60 | 21,60 | 1,08 | 1,86 | 96 | 1,62 |
| 30 min | 1,0 | 3,0 | 3,0 | 3.699 | 1,5 | 46,2 | 43,9 | 31,48 | 26,48 | 1,10 | 2,17 | 98 | 2,98 |
| 30 min | 1,0 | 1,0 | 1,0 | 3.990 | 1,6 | 50,1 | 49,4 | 12,49 | 7,49 | 1,03 | 0,77 | 90 | -6,61 |
| 60 min | 0,5 | 2,5 | 5,0 | 2.219 | 1,2 | 41,5 | 37,9 | 44,09 | 39,09 | 1,16 | 2,62 | 96 | 18,05 |
| 60 min | 1,0 | 2,0 | 2,0 | 2.154 | 1,2 | 50,5 | 47,7 | 40,15 | 35,15 | 1,12 | 1,99 | 88 | 11,25 |
| 60 min | 1,0 | 3,0 | 3,0 | 2.152 | 1,2 | 50,4 | 47,3 | 43,52 | 38,52 | 1,13 | 2,12 | 86 | 13,00 |
| 60 min | 1,0 | 1,0 | 1,0 | 2.262 | 1,2 | 52,6 | 50,6 | 28,54 | 23,54 | 1,08 | 1,49 | 94 | -5,03 |

`percentil vs nulo`: posição do resultado líquido do robô na distribuição de entradas aleatórias com a mesma saída e custo. ≥ 95 = sinal; ≤ 5 = pior que o acaso.

## 4. Perfil fiel (barra de entrada sem proteção, como o NTSL v1)

| TF | SL×ATR | SG×ATR | RR nominal | n | WR % | WR breakeven % | bruto (pts) | líquido 5 pts | PF líq. | t (pregão) |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 min | 0,5 | 2,5 | 5,0 | 2.559 | 20,8 | 20,9 | 4,04 | -0,96 | 0,99 | -0,18 |
| 5 min | 1,0 | 2,0 | 2,0 | 2.312 | 36,0 | 35,7 | 6,51 | 1,51 | 1,01 | 0,24 |
| 5 min | 1,0 | 3,0 | 3,0 | 2.042 | 31,8 | 31,0 | 10,20 | 5,20 | 1,04 | 0,67 |
| 5 min | 1,0 | 1,0 | 1,0 | 2.925 | 49,9 | 50,4 | 2,81 | -2,19 | 0,98 | -0,55 |
| 10 min | 0,5 | 2,5 | 5,0 | 2.685 | 25,0 | 26,7 | -5,44 | -10,44 | 0,92 | -1,47 |
| 10 min | 1,0 | 2,0 | 2,0 | 2.498 | 39,6 | 40,3 | 0,17 | -4,83 | 0,97 | -0,59 |
| 10 min | 1,0 | 3,0 | 3,0 | 2.406 | 37,3 | 38,0 | 0,12 | -4,88 | 0,97 | -0,55 |
| 10 min | 1,0 | 1,0 | 1,0 | 2.837 | 49,6 | 51,0 | -3,03 | -8,03 | 0,95 | -1,33 |
| 15 min | 0,5 | 2,5 | 5,0 | 2.953 | 29,1 | 29,7 | 0,12 | -4,88 | 0,97 | -0,52 |
| 15 min | 1,0 | 2,0 | 2,0 | 2.769 | 41,1 | 42,1 | -3,85 | -8,85 | 0,96 | -0,83 |
| 15 min | 1,0 | 3,0 | 3,0 | 2.702 | 40,0 | 41,0 | -4,01 | -9,01 | 0,96 | -0,79 |
| 15 min | 1,0 | 1,0 | 1,0 | 3.029 | 48,3 | 49,0 | -0,20 | -5,20 | 0,97 | -0,60 |
| 20 min | 0,5 | 2,5 | 5,0 | 3.223 | 35,2 | 34,7 | 9,31 | 4,31 | 1,02 | 0,38 |
| 20 min | 1,0 | 2,0 | 2,0 | 3.079 | 46,0 | 46,1 | 4,55 | -0,45 | 1,00 | -0,04 |
| 20 min | 1,0 | 3,0 | 3,0 | 3.049 | 45,6 | 44,5 | 16,88 | 11,88 | 1,05 | 0,95 |
| 20 min | 1,0 | 1,0 | 1,0 | 3.263 | 49,7 | 50,3 | -0,03 | -5,03 | 0,98 | -0,48 |
| 30 min | 0,5 | 2,5 | 5,0 | 3.784 | 37,4 | 35,6 | 23,78 | 18,78 | 1,08 | 1,62 |
| 30 min | 1,0 | 2,0 | 2,0 | 3.686 | 47,1 | 45,4 | 24,56 | 19,56 | 1,07 | 1,58 |
| 30 min | 1,0 | 3,0 | 3,0 | 3.669 | 47,0 | 44,9 | 29,72 | 24,72 | 1,09 | 1,91 |
| 30 min | 1,0 | 1,0 | 1,0 | 3.867 | 50,1 | 49,1 | 15,02 | 10,02 | 1,04 | 0,92 |
| 60 min | 0,5 | 2,5 | 5,0 | 2.163 | 44,9 | 42,0 | 39,78 | 34,78 | 1,13 | 1,96 |
| 60 min | 1,0 | 2,0 | 2,0 | 2.143 | 51,3 | 48,3 | 42,75 | 37,75 | 1,13 | 2,06 |
| 60 min | 1,0 | 3,0 | 3,0 | 2.141 | 51,2 | 48,0 | 45,98 | 40,98 | 1,14 | 2,18 |
| 60 min | 1,0 | 1,0 | 1,0 | 2.201 | 52,7 | 50,7 | 29,53 | 24,53 | 1,09 | 1,45 |

## 5. Controle: a geometria de saída sozinha (entrada aleatória, perfil ideal)

A coluna `nulo líq. médio` da seção 3 sugere que **a própria geometria (stop curto, alvo longo, ≤ ~100 min) tem esperança positiva em timeframes grandes**, independentemente do sinal. Esta seção isola esse efeito: entradas em barras sorteadas (15 % das barras de janela), lado sorteado, 20 repetições, t agregado por pregão, e replicação na série WDO (outro instrumento; o custo de 5 pts só vale para o WIN).

| série | TF | SL×ATR | SG×ATR | bruto (pts/trade) | líquido 5 pts | t (pregão) | 1ª metade | 2ª metade | anos positivos |
|---|---|---|---|---|---|---|---|---|---|
| WINFUT | 5 min | 0,5 | 2,5 | -0,21 | -5,21 | 0,26 | 0,10 | 0,53 | 1/2 |
| WINFUT | 5 min | 1,0 | 2,0 | -1,26 | -6,26 | -1,93 | -2,07 | -2,18 | 0/2 |
| WINFUT | 10 min | 0,5 | 2,5 | -1,94 | -6,94 | -0,66 | -3,50 | 1,17 | 2/4 |
| WINFUT | 10 min | 1,0 | 2,0 | -2,66 | -7,66 | -2,19 | -4,11 | -2,67 | 0/4 |
| WINFUT | 15 min | 0,5 | 2,5 | -0,90 | -5,90 | 0,38 | 2,08 | -0,40 | 2/6 |
| WINFUT | 15 min | 1,0 | 2,0 | 1,01 | -3,99 | -0,10 | -0,20 | -0,19 | 3/6 |
| WINFUT | 20 min | 0,5 | 2,5 | 2,73 | -2,27 | 1,78 | 6,71 | 2,09 | 6/8 |
| WINFUT | 20 min | 1,0 | 2,0 | 2,47 | -2,53 | 0,69 | 2,46 | 0,26 | 6/8 |
| WINFUT | 30 min | 0,5 | 2,5 | 8,59 | 3,59 | 3,81 | 7,72 | 11,05 | 10/12 |
| WINFUT | 30 min | 1,0 | 2,0 | 5,90 | 0,90 | 2,87 | 4,42 | 6,01 | 9/12 |
| WINFUT | 60 min | 0,5 | 2,5 | 20,19 | 15,19 | 5,60 | 21,29 | 21,73 | 11/12 |
| WINFUT | 60 min | 1,0 | 2,0 | 14,55 | 9,55 | 5,21 | 16,01 | 10,84 | 9/12 |
| WDOFUT | 5 min | 0,5 | 2,5 | -0,09 | n/a (pontos de WDO) | -1,37 | -0,04 | -0,08 | 0/2 |
| WDOFUT | 5 min | 1,0 | 2,0 | -0,05 | n/a (pontos de WDO) | -1,87 | -0,13 | -0,02 | 0/2 |
| WDOFUT | 10 min | 0,5 | 2,5 | -0,03 | n/a (pontos de WDO) | -0,02 | -0,08 | 0,08 | 1/4 |
| WDOFUT | 10 min | 1,0 | 2,0 | -0,02 | n/a (pontos de WDO) | -1,24 | -0,11 | -0,01 | 2/4 |
| WDOFUT | 15 min | 0,5 | 2,5 | -0,02 | n/a (pontos de WDO) | 0,56 | 0,02 | 0,05 | 4/6 |
| WDOFUT | 15 min | 1,0 | 2,0 | 0,02 | n/a (pontos de WDO) | -0,41 | 0,00 | -0,05 | 4/6 |
| WDOFUT | 20 min | 0,5 | 2,5 | 0,02 | n/a (pontos de WDO) | 0,77 | -0,05 | 0,15 | 5/8 |
| WDOFUT | 20 min | 1,0 | 2,0 | 0,01 | n/a (pontos de WDO) | -0,54 | -0,07 | 0,01 | 4/8 |
| WDOFUT | 30 min | 0,5 | 2,5 | 0,02 | n/a (pontos de WDO) | 1,05 | 0,01 | 0,14 | 7/12 |
| WDOFUT | 30 min | 1,0 | 2,0 | -0,03 | n/a (pontos de WDO) | -0,64 | -0,05 | -0,02 | 4/12 |
| WDOFUT | 60 min | 0,5 | 2,5 | 0,09 | n/a (pontos de WDO) | 0,80 | 0,06 | 0,11 | 6/12 |
| WDOFUT | 60 min | 1,0 | 2,0 | -0,03 | n/a (pontos de WDO) | -0,28 | -0,06 | 0,02 | 5/12 |

Explicação candidata (hipótese MB-H13): retorno positivamente autocorrelacionado na escala do ATR — um stop curto corta a continuação adversa e deixa correr a favorável. Se for isso, aparece como ρ(lag 1) > 0:

| série | TF | ρ lag-1 (C−O ÷ ATR) | t | n |
|---|---|---|---|---|
| WINFUT | 5 min | -0,007 | -1,45 | 42.854 |
| WINFUT | 10 min | -0,004 | -0,92 | 45.666 |
| WINFUT | 15 min | 0,007 | 1,45 | 46.356 |
| WINFUT | 20 min | 0,005 | 1,13 | 49.905 |
| WINFUT | 30 min | 0,009 | 2,11 | 51.095 |
| WINFUT | 60 min | 0,021 | 3,28 | 24.664 |
| WDOFUT | 5 min | -0,009 | -1,88 | 42.795 |
| WDOFUT | 10 min | -0,010 | -2,22 | 45.722 |
| WDOFUT | 15 min | -0,005 | -1,06 | 46.323 |
| WDOFUT | 20 min | -0,002 | -0,42 | 49.880 |
| WDOFUT | 30 min | 0,001 | 0,32 | 50.089 |
| WDOFUT | 60 min | 0,008 | 1,19 | 24.186 |

## 6. A cor como alarme de volatilidade

Evento: barra brilhante (range ≥ 1,7 × ATR20). Medida: range da barra seguinte ÷ média do range **no mesmo horário** (controle de sazonalidade intradiária). Razão > 1 = o alarme antecipa expansão. O `t` agrega por pregão a soma dos desvios em relação ao controle.

| TF | eventos | range seguinte ÷ média da hora | controle | t (pregão) |
|---|---|---|---|---|
| 5 min | 2.810 | 1,29 | 1,00 | 6,41 |
| 10 min | 3.987 | 1,22 | 1,00 | 8,61 |
| 15 min | 4.184 | 1,15 | 1,00 | 7,68 |
| 20 min | 4.480 | 1,14 | 1,00 | 7,07 |
| 30 min | 3.526 | 1,20 | 1,00 | 9,28 |
| 60 min | 1.816 | 1,15 | 1,00 | 6,79 |

Como o alarme descreve **tamanho** e não **direção**, ele serve para decidir *quando* ter alvo/stop mais largos ou ficar de fora, não para decidir lado.

