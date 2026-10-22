# ANALISE_001 — Confluência de cor em múltiplos timeframes (M16)

> Gerado por `motores/M16_confluencia_multitf/codigo/analise_001.py`. Não editar à mão. Regras: `METODO.md` e `HIPOTESES.md` (congeladas antes de rodar; a Emenda 1 foi anterior a qualquer resultado).

## 1. Dados e poder estatístico

| base | conjunto | pregões | início | fim |
|---|---|---|---|---|
| 5 min | descoberta | 256 | 2024-06-19 | 2025-06-30 |
| 5 min | hold1 | 127 | 2025-07-01 | 2025-12-30 |
| 5 min | hold2 | 108 | 2026-02-19 | 2026-07-24 |
| 5 min | wdo | 379 | 2024-06-26 | 2025-12-30 |
| 15 min | descoberta | 781 | 2020-11-04 | 2023-12-28 |
| 15 min | hold1 | 499 | 2024-01-02 | 2025-12-30 |
| 15 min | hold2 | 113 | 2026-02-19 | 2026-08-03 |
| 15 min | wdo | 1.279 | 2020-11-04 | 2025-12-30 |
| 30 min | descoberta | 1.448 | 2014-01-02 | 2019-12-30 |
| 30 min | hold1 | 1.489 | 2020-01-02 | 2025-12-30 |
| 30 min | hold2 | 109 | 2026-02-12 | 2026-07-24 |
| 30 min | wdo | 2.880 | 2014-01-02 | 2025-12-30 |

## 2. Frequência do alerta (CF-H06)

Eventos por pregão **no WINFUT inteiro** (descoberta + hold-out 1). `A` = TFs fecham juntos; `B` = TF superior fechou há no máximo 1 período.

| conjunto | nível | modo | eventos | por pregão |
|---|---|---|---|---|
| 15 (TF único) | N1 | A | 5.235 | 4,09 |
| 15 (TF único) | N2 | A | 1.188 | 0,93 |
| 15+30 | N1 | A | 1.004 | 0,78 |
| 15+30 | N1 | B | 1.310 | 1,02 |
| 15+30 | N2 | A | 64 | 0,05 |
| 15+30 | N2 | B | 67 | 0,05 |
| 15+30+60 | N1 | A | 225 | 0,18 |
| 15+30+60 | N1 | B | 321 | 0,25 |
| 15+30+60 | N2 | A | 3 | 0,00 |
| 15+30+60 | N2 | B | 3 | 0,00 |
| 15+60 | N1 | A | 323 | 0,25 |
| 15+60 | N1 | B | 602 | 0,47 |
| 15+60 | N2 | A | 8 | 0,01 |
| 15+60 | N2 | B | 11 | 0,01 |
| 30 (TF único) | N1 | A | 6.110 | 2,08 |
| 30 (TF único) | N2 | A | 703 | 0,24 |
| 30+60 | N1 | A | 1.445 | 0,49 |
| 30+60 | N1 | B | 1.751 | 0,60 |
| 30+60 | N2 | A | 78 | 0,03 |
| 30+60 | N2 | B | 80 | 0,03 |
| 5 (TF único) | N1 | A | 3.615 | 9,44 |
| 5 (TF único) | N2 | A | 470 | 1,23 |
| 5+15 | N1 | A | 150 | 0,39 |
| 5+15 | N1 | B | 317 | 0,83 |
| 5+15 | N2 | A | 14 | 0,04 |
| 5+15 | N2 | B | 24 | 0,06 |
| 5+15+30 | N1 | A | 27 | 0,07 |
| 5+15+30 | N1 | B | 42 | 0,11 |
| 5+15+30 | N2 | A | 3 | 0,01 |
| 5+15+30 | N2 | B | 3 | 0,01 |
| 5+15+30+60 | N1 | A | 4 | 0,01 |
| 5+15+30+60 | N1 | B | 5 | 0,01 |
| 5+15+60 | N1 | A | 5 | 0,01 |
| 5+15+60 | N1 | B | 13 | 0,03 |
| 5+30 | N1 | A | 51 | 0,13 |
| 5+30 | N1 | B | 124 | 0,32 |
| 5+30 | N2 | A | 3 | 0,01 |
| 5+30 | N2 | B | 3 | 0,01 |
| 5+30+60 | N1 | A | 6 | 0,02 |
| 5+30+60 | N1 | B | 22 | 0,06 |
| 5+60 | N1 | A | 10 | 0,03 |
| 5+60 | N1 | B | 96 | 0,25 |
| 5+60 | N2 | B | 1 | 0,00 |

## 3. CF-H01 — a confluência antecipa mais expansão de range que a cor em TF único?

`ratio` = range da barra base seguinte ÷ média do mesmo horário. `t` = Welch por pregão (confluência − TF único). Apenas linhas com ≥ 20 eventos.

| conjunto | nível | descoberta | hold1 | hold2 | wdo |
|---|---|---|---|---|---|
| 15+30 | N1 | 1,15 vs 1,21 (n=621, t=-1,8) | 0,84 vs 0,83 (n=383, t=0,5) | 1,06 vs 1,07 (n=65, t=-0,2) | 1,05 vs 1,06 (n=999, t=-0,6) |
| 15+30 | N2 | 1,04 vs 1,14 (n=23, t=-1,1) | 0,87 vs 0,87 (n=41, t=-0,1) |  | 1,12 vs 1,05 (n=109, t=1,3) |
| 15+30+60 | N1 | 1,24 vs 1,21 (n=151, t=0,7) | 0,86 vs 0,83 (n=74, t=0,6) |  | 1,15 vs 1,06 (n=256, t=2,0) |
| 15+60 | N1 | 1,25 vs 1,21 (n=208, t=0,8) | 0,82 vs 0,83 (n=115, t=-0,3) |  | 1,09 vs 1,06 (n=332, t=0,7) |
| 15+60 | N2 |  |  |  | 1,24 vs 1,05 (n=21, t=1,1) |
| 30+60 | N1 | 1,06 vs 1,04 (n=703, t=0,8) | 1,10 vs 1,09 (n=742, t=0,4) | 1,01 vs 1,09 (n=45, t=-0,9) | 1,09 vs 1,07 (n=1452, t=1,3) |
| 30+60 | N2 | 1,15 vs 1,03 (n=40, t=1,0) | 1,10 vs 1,05 (n=38, t=0,5) |  | 1,06 vs 1,09 (n=132, t=-0,6) |
| 5+15 | N1 | 1,15 vs 1,09 (n=107, t=0,9) | 1,48 vs 1,08 (n=43, t=1,3) | 1,31 vs 1,09 (n=52, t=1,4) | 1,15 vs 1,09 (n=155, t=1,0) |
| 5+15+30 | N1 | 1,01 vs 1,09 (n=21, t=-0,7) |  |  | 1,13 vs 1,09 (n=34, t=0,3) |
| 5+30 | N1 | 1,09 vs 1,09 (n=38, t=-0,0) |  |  | 1,24 vs 1,09 (n=72, t=1,7) |
| 5+60 | N1 |  |  |  | 1,19 vs 1,09 (n=25, t=0,6) |

**Conjuntos que satisfazem CF-H01:** nenhum.

## 4. CF-H02 — direção: retorno alinhado ao sinal (continuação > 0; fade < 0)

Retorno em pontos de `sinal × (c[i+h] − o[i+1])`; `t` por pregão. Modo A, conjuntos com ≥ 30 eventos na descoberta, ordenados por |t| na descoberta (top 20; a lista completa está no CSV).

| conjunto | nível | h (min) | n desc. | desc. | hold1 | hold2 | WDO |
|---|---|---|---|---|---|---|---|
| 30 (TF único) | N1 | 60 | 2978 | 31,2 (t=2,7) | -1,7 (t=-0,1) | -27,1 (t=-0,6) | 0,4 (t=1,6) |
| 30 (TF único) | N1 | 30 | 2978 | 20,3 (t=2,5) | -4,4 (t=-0,5) | -20,1 (t=-0,6) | 0,1 (t=0,3) |
| 5 (TF único) | N1 | 5 | 2428 | -6,1 (t=-2,3) | -5,1 (t=-1,6) | 3,6 (t=0,6) | -0,1 (t=-1,4) |
| 15+30 | N1 | 60 | 621 | 67,5 (t=2,1) | -16,4 (t=-0,6) | -74,5 (t=-0,8) | 1,3 (t=1,8) |
| 5+30 | N1 | 15 | 38 | -77,6 (t=-1,7) | -47,4 (t=-0,6) | 42,1 (t=0,5) | -0,5 (t=-0,5) |
| 30+60 | N1 | 60 | 703 | 38,1 (t=1,6) | -31,2 (t=-1,2) | -168,9 (t=-1,5) | 0,9 (t=1,6) |
| 30+60 | N2 | 30 | 40 | 153,3 (t=1,6) | -26,5 (t=-0,3) | -40,7 (t=-0,5) | -1,1 (t=-0,9) |
| 5 (TF único) | N2 | 15 | 317 | -28,4 (t=-1,6) | -23,2 (t=-1,4) | 28,5 (t=1,4) | 0,4 (t=1,3) |
| 30+60 | N1 | 30 | 703 | 26,6 (t=1,6) | -18,5 (t=-1,0) | -29,3 (t=-0,4) | -0,0 (t=-0,1) |
| 5+30 | N1 | 5 | 38 | -50,0 (t=-1,6) | 10,8 (t=0,2) | 33,8 (t=0,6) | -1,1 (t=-1,8) |
| 5 (TF único) | N1 | 15 | 2428 | -6,7 (t=-1,5) | -1,7 (t=-0,4) | 11,0 (t=1,2) | -0,0 (t=-0,3) |
| 5+15 | N1 | 5 | 107 | -28,6 (t=-1,5) | -15,1 (t=-0,5) | 39,8 (t=1,0) | -0,1 (t=-0,2) |
| 30+60 | N2 | 60 | 40 | 155,1 (t=1,5) | 14,1 (t=0,1) | -246,4 (t=-0,9) | -1,6 (t=-0,8) |
| 5 (TF único) | N1 | 60 | 2428 | -11,1 (t=-1,4) | 2,0 (t=0,2) | -2,5 (t=-0,2) | 0,1 (t=0,5) |
| 5 (TF único) | N1 | 30 | 2428 | -7,3 (t=-1,4) | -1,5 (t=-0,2) | 23,6 (t=1,7) | 0,0 (t=0,3) |
| 15+30 | N1 | 30 | 621 | 27,2 (t=1,2) | 1,6 (t=0,1) | -37,4 (t=-0,5) | 0,6 (t=1,2) |
| 5 (TF único) | N2 | 5 | 317 | -10,2 (t=-1,2) | -9,3 (t=-0,8) | 19,9 (t=1,6) | -0,1 (t=-0,8) |
| 5+30 | N1 | 30 | 38 | -77,2 (t=-1,2) | 59,4 (t=0,5) | 142,1 (t=1,0) | -0,1 (t=-0,1) |
| 5+15 | N1 | 15 | 107 | -42,8 (t=-1,2) | -62,1 (t=-1,8) | 86,7 (t=1,5) | -0,4 (t=-0,6) |
| 5 (TF único) | N2 | 30 | 317 | -23,6 (t=-1,1) | -5,3 (t=-0,2) | 23,2 (t=0,9) | 0,4 (t=1,0) |

**Combinações que satisfazem CF-H02:** nenhuma.

## 5. CF-H03 — quantos pontos dá para capturar (MFE e MAE em 60 min, WIN)

Descritivo, modo A, a favor da cor (continuação). `MFE` = máximo favorável a partir da abertura seguinte; `MAE` = máximo adverso. Valores em pontos (e em ATR da base). Por simetria, o MFE do **fade** é o MAE da continuação e vice-versa. WIN descoberta + hold-outs 1 e 2 agrupados.

| conjunto | nível | n | MFE med / p75 / p90 (pts) | MAE med / p75 / p90 (pts) | MFE med (ATR) | MAE med (ATR) | MFE > MAE % |
|---|---|---|---|---|---|---|---|
| 15 (TF único) | N1 | 5.586 | 435 / 766 / 1.178 | 428 / 775 / 1.226 | 1,11 | 1,10 | 49,8 |
| 15 (TF único) | N2 | 1.300 | 445 / 795 / 1.186 | 438 / 848 / 1.284 | 1,29 | 1,28 | 49,3 |
| 15+30 | N1 | 1.069 | 449 / 790 / 1.161 | 408 / 723 / 1.154 | 1,14 | 1,05 | 51,3 |
| 15+30 | N2 | 74 | 469 / 776 / 1.387 | 417 / 729 / 1.250 | 1,42 | 1,27 | 47,3 |
| 15+30+60 | N1 | 235 | 473 / 788 / 1.112 | 389 / 712 / 1.065 | 1,02 | 0,93 | 53,6 |
| 15+60 | N1 | 334 | 480 / 793 / 1.176 | 408 / 722 / 1.122 | 1,10 | 0,97 | 53,0 |
| 30 (TF único) | N1 | 6.314 | 388 / 721 / 1.106 | 357 / 670 / 1.070 | 0,66 | 0,60 | 51,8 |
| 30 (TF único) | N2 | 743 | 404 / 760 / 1.129 | 359 / 719 / 1.159 | 0,75 | 0,64 | 52,4 |
| 30+60 | N1 | 1.490 | 422 / 740 / 1.093 | 364 / 670 / 1.099 | 0,69 | 0,60 | 52,8 |
| 30+60 | N2 | 85 | 481 / 863 / 1.249 | 290 / 625 / 1.040 | 0,82 | 0,49 | 60,0 |
| 5 (TF único) | N1 | 4.574 | 225 / 428 / 696 | 230 / 422 / 665 | 1,36 | 1,40 | 49,4 |
| 5 (TF único) | N2 | 758 | 240 / 470 / 864 | 252 / 455 / 772 | 1,47 | 1,54 | 47,8 |
| 5+15 | N1 | 202 | 318 / 654 / 1.088 | 368 / 597 / 855 | 1,66 | 1,65 | 47,5 |
| 5+15+30 | N1 | 37 | 366 / 681 / 1.207 | 385 / 688 / 917 | 2,00 | 1,69 | 51,4 |
| 5+30 | N1 | 68 | 316 / 604 / 1.143 | 358 / 648 / 996 | 1,53 | 1,61 | 48,5 |

Leitura: se `MFE > MAE %` ≈ 50 e as medianas são parecidas, a cor não indica lado — o que o alerta entrega é **amplitude** (quantos pontos o mercado vai andar), não direção.

## 6. CF-H04 e CF-H05 — estratégias com barreira

Total testado: **114** (sem contar TF único). Critério: descoberta `t_vs_nulo` ≥ 3 com n ≥ 30 **e** hold-outs 1 e 2 com média líquida > 0 e `t_vs_nulo` ≥ 2 **e** WDO bruto > 0.

- Passam a descoberta (t ≥ 3, n ≥ 30): **1** de 114
- Passam descoberta **e** hold-out 1: **0**
- Passam **todos** os critérios (CF-H04): **0**

Top 12 pela descoberta (seleção feita **só** na descoberta; `t` = vs nulo; média líquida de 5 pts):

| conjunto | nível | lado | SL/SG (×ATR) | descoberta | hold1 | hold2 | WDO (R) |
|---|---|---|---|---|---|---|---|
| 30+60 | N2 | continuação | 0.5/1.5 | n=40 · 278,7 pts · t=3,0 | n=38 · 35,6 pts · t=0,5 | n=7 · -20,4 pts · t=-0,1 | -0,01 |
| 30+60 | N2 | continuação | 1.0/2.0 | n=40 · 259,7 pts · t=2,6 | n=38 · 23,4 pts · t=0,2 | n=7 · -158,3 pts · t=-0,8 | -0,04 |
| 30+60 | N1 | continuação | 0.5/1.5 | n=703 · 37,8 pts · t=2,5 | n=742 · -3,5 pts · t=-0,1 | n=45 · -86,8 pts · t=-1,3 | 0,05 |
| 5+15 | N1 | fade | 0.5/1.5 | n=107 · 35,2 pts · t=2,3 | n=43 · 32,3 pts · t=1,3 | n=52 · -35,9 pts · t=-0,8 | -0,04 |
| 30+60 | N2 | continuação | 1.0/3.0 | n=40 · 203,6 pts · t=2,2 | n=38 · 22,5 pts · t=0,2 | n=7 · -158,3 pts · t=-0,7 | -0,03 |
| 5+30 | N1 | fade | 1.0/3.0 | n=38 · 140,6 pts · t=2,1 | n=13 · 10,5 pts · t=0,1 | n=17 · -64,8 pts · t=-0,5 | -0,11 |
| 5+30 | N1 | fade | 1.0/2.0 | n=38 · 120,2 pts · t=2,1 | n=13 · 1,5 pts · t=0,1 | n=17 · -6,2 pts · t=0,0 | 0,03 |
| 30+60 | N1 | continuação | 1.0/2.0 | n=703 · 36,5 pts · t=1,9 | n=742 · -16,5 pts · t=-0,8 | n=45 · -111,5 pts · t=-1,3 | 0,07 |
| 30+60 | N1 | continuação | 1.0/3.0 | n=703 · 34,3 pts · t=1,8 | n=742 · -18,5 pts · t=-0,9 | n=45 · -149,8 pts · t=-1,5 | 0,07 |
| 15+30 | N1 | continuação | 1.0/2.0 | n=600 · 32,9 pts · t=1,7 | n=377 · -12,4 pts · t=-0,6 | n=63 · -87,0 pts · t=-1,3 | 0,10 |
| 5+30 | N1 | fade | 0.5/1.5 | n=38 · 61,2 pts · t=1,7 | n=13 · 7,5 pts · t=0,2 | n=17 · -17,1 pts · t=-0,1 | 0,11 |
| 5+15 | N1 | fade | 1.0/2.0 | n=107 · 46,9 pts · t=1,6 | n=43 · 4,2 pts · t=0,2 | n=51 · -62,0 pts · t=-1,0 | 0,08 |

### TF único (controle de comparação)

| base | nível | lado | SL/SG | descoberta | hold1 | hold2 |
|---|---|---|---|---|---|---|
| 5 min | N1 | continuação | 0.5/1.5 | n=2120 · -12,9 pts · WR 23% (BE 27%) | -8,0 pts | 4,8 pts |
| 5 min | N1 | continuação | 1.0/2.0 | n=1665 · -11,3 pts · WR 35% (BE 37%) | -2,4 pts | 8,4 pts |
| 5 min | N1 | continuação | 1.0/3.0 | n=1492 · -8,0 pts · WR 32% (BE 34%) | 3,3 pts | 3,5 pts |
| 5 min | N1 | fade | 0.5/1.5 | n=2134 · 0,4 pts · WR 28% (BE 27%) | -6,5 pts | -6,0 pts |
| 5 min | N1 | fade | 1.0/2.0 | n=1655 · 5,1 pts · WR 38% (BE 37%) | -11,8 pts | -13,3 pts |
| 5 min | N1 | fade | 1.0/3.0 | n=1511 · 0,2 pts · WR 35% (BE 35%) | -6,7 pts | -14,6 pts |
| 5 min | N2 | continuação | 0.5/1.5 | n=312 · -11,4 pts · WR 24% (BE 28%) | -21,8 pts | 21,8 pts |
| 5 min | N2 | continuação | 1.0/2.0 | n=304 · -13,6 pts · WR 36% (BE 39%) | -15,7 pts | 24,1 pts |
| 5 min | N2 | continuação | 1.0/3.0 | n=295 · -26,9 pts · WR 29% (BE 36%) | -8,8 pts | 4,0 pts |
| 5 min | N2 | fade | 0.5/1.5 | n=315 · -4,0 pts · WR 26% (BE 27%) | -4,6 pts | -29,1 pts |
| 5 min | N2 | fade | 1.0/2.0 | n=308 · 17,1 pts · WR 40% (BE 36%) | -0,6 pts | -40,4 pts |
| 5 min | N2 | fade | 1.0/3.0 | n=297 · 13,7 pts · WR 37% (BE 34%) | 9,3 pts | -26,5 pts |
| 15 min | N1 | continuação | 0.5/1.5 | n=2937 · -10,3 pts · WR 27% (BE 29%) | -2,1 pts | -5,3 pts |
| 15 min | N1 | continuação | 1.0/2.0 | n=2489 · -7,1 pts · WR 41% (BE 42%) | -11,0 pts | -66,4 pts |
| 15 min | N1 | continuação | 1.0/3.0 | n=2352 · -10,7 pts · WR 39% (BE 40%) | -10,7 pts | -90,3 pts |
| 15 min | N1 | fade | 0.5/1.5 | n=2968 · -19,1 pts · WR 26% (BE 28%) | 1,1 pts | 8,8 pts |
| 15 min | N1 | fade | 1.0/2.0 | n=2449 · -3,1 pts · WR 40% (BE 40%) | 5,1 pts | 75,1 pts |
| 15 min | N1 | fade | 1.0/3.0 | n=2313 · -7,5 pts · WR 39% (BE 40%) | 10,9 pts | 108,2 pts |
| 15 min | N2 | continuação | 0.5/1.5 | n=676 · -0,1 pts · WR 27% (BE 27%) | 13,9 pts | -52,1 pts |
| 15 min | N2 | continuação | 1.0/2.0 | n=655 · -13,2 pts · WR 39% (BE 40%) | 3,3 pts | -136,4 pts |
| 15 min | N2 | continuação | 1.0/3.0 | n=640 · -7,6 pts · WR 37% (BE 38%) | 5,5 pts | -135,2 pts |
| 15 min | N2 | fade | 0.5/1.5 | n=677 · -10,8 pts · WR 25% (BE 27%) | -16,4 pts | 59,8 pts |
| 15 min | N2 | fade | 1.0/2.0 | n=647 · 11,4 pts · WR 40% (BE 39%) | -12,7 pts | 177,3 pts |
| 15 min | N2 | fade | 1.0/3.0 | n=629 · -6,9 pts · WR 37% (BE 38%) | -17,3 pts | 177,4 pts |
| 30 min | N1 | continuação | 0.5/1.5 | n=2798 · 23,8 pts · WR 40% (BE 37%) | 5,1 pts | -40,2 pts |
| 30 min | N1 | continuação | 1.0/2.0 | n=2660 · 29,7 pts · WR 50% (BE 47%) | -3,9 pts | -54,7 pts |
| 30 min | N1 | continuação | 1.0/3.0 | n=2614 · 27,2 pts · WR 50% (BE 47%) | -5,1 pts | -61,9 pts |
| 30 min | N1 | fade | 0.5/1.5 | n=2826 · -27,3 pts · WR 34% (BE 38%) | -16,5 pts | 29,1 pts |
| 30 min | N1 | fade | 1.0/2.0 | n=2706 · -31,4 pts · WR 46% (BE 49%) | -6,5 pts | 104,5 pts |
| 30 min | N1 | fade | 1.0/3.0 | n=2681 · -29,9 pts · WR 45% (BE 49%) | -6,2 pts | 68,8 pts |
| 30 min | N2 | continuação | 0.5/1.5 | n=364 · 39,1 pts · WR 38% (BE 33%) | 35,8 pts | -86,6 pts |
| 30 min | N2 | continuação | 1.0/2.0 | n=362 · 34,0 pts · WR 48% (BE 44%) | 18,5 pts | -159,6 pts |
| 30 min | N2 | continuação | 1.0/3.0 | n=358 · 28,7 pts · WR 47% (BE 44%) | 27,8 pts | -177,8 pts |
| 30 min | N2 | fade | 0.5/1.5 | n=365 · -23,1 pts · WR 33% (BE 36%) | -1,5 pts | -32,0 pts |
| 30 min | N2 | fade | 1.0/2.0 | n=363 · -21,6 pts · WR 46% (BE 49%) | 19,4 pts | 88,0 pts |
| 30 min | N2 | fade | 1.0/3.0 | n=360 · -11,9 pts · WR 46% (BE 47%) | 10,6 pts | 48,4 pts |

(Resultados completos em `ANALISE_001_estrategias.csv`. O total de estratégias é menor que 132 porque os conjuntos N2 com 3 TFs quase não geram eventos.)

### CF-H05 — confluência × TF único

- Estratégias em que a confluência supera o TF único na descoberta (t ≥ 2 por pregão, n ≥ 30): **5**
- Dessas, com diferença positiva também nos hold-outs 1 **e** 2: **0**
- Cuidado ao ler: a diferença é por **pregão**, e o TF único opera muito mais vezes (até ~9 por pregão no 5 min) pagando custo e perdendo na média. Parte da "vantagem" da confluência é só operar menos. Compare por trade nas tabelas acima.

## 7. Veredito automático (regras congeladas)

| ID | Veredito |
|---|---|
| CF-H01 | NÃO CONFIRMADA (nenhum conjunto) |
| CF-H02 | NÃO CONFIRMADA (nenhuma combinação) |
| CF-H03 | descritivo (seção 5) |
| CF-H04 | NÃO CONFIRMADA (0 de 114) |
| CF-H05 | NÃO CONFIRMADA (5 passam na descoberta; 0 replicam) |
| CF-H06 | descritivo (seção 2) |

