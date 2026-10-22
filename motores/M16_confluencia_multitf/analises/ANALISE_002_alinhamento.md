# ANALISE_002 — Alinhamento de cor no mesmo instante (M16)

> Gerado por `codigo/analise_002.py`. Regras em `HIPOTESES.md` (seção ANALISE_002), congeladas antes de rodar.

No minuto T em que a barra do TF maior fecha, olha-se a última barra fechada de cada TF menor: é o alinhamento que se vê no gráfico. Cor **Bollinger**: N1 = |z| ≥ 1,5 e N2 = |z| ≥ 2,5. Cor de **limiar fixo**: N1 = |F| ≥ 60 e N2 = |F| ≥ 80 (percentil ~84 de |F|).

**Períodos.** Âncora de 30 ou 60 min: descoberta até 2019, hold-out 1 = 2020–2025, hold-out 2 = contratos de 2026. Conjuntos que usam TF de 5 min não têm dados antes de 2024, então a descoberta deles é 2024–2025 e o único hold-out é 2026.

## 1. Frequência (WINFUT)

| conjunto | definição | nível | eventos | por pregão |
|---|---|---|---|---|
| 15+30 | bollinger | N1 | 1.002 | 0,35 |
| 15+30 | bollinger | N2 | 63 | 0,02 |
| 15+30+60 | bollinger | N1 | 225 | 0,08 |
| 15+60 | bollinger | N1 | 321 | 0,11 |
| 15+60 | bollinger | N2 | 8 | 0,00 |
| 30+60 | bollinger | N1 | 1.440 | 0,50 |
| 30+60 | bollinger | N2 | 77 | 0,03 |
| 5+15 | bollinger | N1 | 222 | 0,58 |
| 5+15 | bollinger | N2 | 40 | 0,11 |
| 5+15+30 | bollinger | N1 | 27 | 0,07 |
| 5+30 | bollinger | N1 | 51 | 0,13 |
| 5+60 | bollinger | N1 | 9 | 0,02 |
| 15+30 | fixo60 | N1 | 3.167 | 1,09 |
| 15+30 | fixo60 | N2 | 1.803 | 0,62 |
| 15+30+60 | fixo60 | N1 | 940 | 0,32 |
| 15+30+60 | fixo60 | N2 | 486 | 0,17 |
| 15+60 | fixo60 | N1 | 1.216 | 0,42 |
| 15+60 | fixo60 | N2 | 666 | 0,23 |
| 30+60 | fixo60 | N1 | 3.879 | 1,34 |
| 30+60 | fixo60 | N2 | 2.149 | 0,74 |
| 5+15 | fixo60 | N1 | 1.263 | 3,32 |
| 5+15 | fixo60 | N2 | 788 | 2,07 |
| 5+15+30 | fixo60 | N1 | 362 | 0,95 |
| 5+15+30 | fixo60 | N2 | 199 | 0,52 |
| 5+15+30+60 | fixo60 | N1 | 94 | 0,25 |
| 5+15+30+60 | fixo60 | N2 | 40 | 0,11 |
| 5+15+60 | fixo60 | N1 | 120 | 0,32 |
| 5+15+60 | fixo60 | N2 | 56 | 0,15 |
| 5+30 | fixo60 | N1 | 500 | 1,32 |
| 5+30 | fixo60 | N2 | 247 | 0,65 |
| 5+60 | fixo60 | N1 | 181 | 0,48 |
| 5+60 | fixo60 | N2 | 80 | 0,21 |

O divisor é aproximado (2.900 pregões para âncora de 30/60 min; 380 para conjuntos com 5 min) e serve para comparar frequências.

## 2. CF-H07 — o alinhamento tem direção?

Retorno de 60 min alinhado à cor, em pontos. `t` por pregão, `p` = fração dos eventos a favor da cor. Uma vantagem real teria o **mesmo sinal** na descoberta e nos hold-outs.

| conjunto | def | nível | descoberta | hold-out 1 | 2026 | WDO |
|---|---|---|---|---|---|---|
| 30+60 | fixo60 | N2 | 50 · t=2,6 · p=53% · n=1095 | -43 · t=-1,9 · p=49% · n=1054 | 118 (n=20) | 1 · t=2,1 · p=49% · n=2343 |
| 30+60 | fixo60 | N1 | 31 · t=2,2 · p=51% · n=1929 | -17 · t=-1,0 · p=50% · n=1950 | -53 (n=42) | 1 · t=2,6 · p=49% · n=3901 |
| 30+60 | bollinger | N1 | 41 · t=1,8 · p=54% · n=700 | -33 · t=-1,3 · p=49% · n=740 | 190 (n=14) | 1 · t=1,6 · p=50% · n=1447 |
| 30+60 | bollinger | N2 | 156 · t=1,5 · p=60% · n=40 | -11 · t=-0,1 · p=49% · n=37 | — | -2 · t=-0,8 · p=45% · n=132 |
| 5+15 | bollinger | N1 | 53 · t=1,4 · p=53% · n=222 | — | 143 (n=19) | -0 · t=-0,4 · p=46% · n=257 |
| 5+30 | bollinger | N1 | -72 · t=-1,1 · p=41% · n=51 | — | — | 1 · t=0,9 · p=51% · n=73 |
| 5+15+30+60 | fixo60 | N2 | -104 · t=-1,0 · p=45% · n=40 | — | — | 3 · t=1,3 · p=61% · n=72 |
| 5+60 | fixo60 | N1 | -37 · t=-0,9 · p=48% · n=181 | — | 123 (n=16) | 1 · t=1,2 · p=49% · n=256 |
| 5+15+30+60 | fixo60 | N1 | -50 · t=-0,8 · p=48% · n=94 | — | -108 (n=5) | 3 · t=1,7 · p=53% · n=140 |
| 5+15 | bollinger | N2 | 68 · t=0,8 · p=52% · n=40 | — | — | 1 · t=0,3 · p=52% · n=58 |
| 5+30 | fixo60 | N2 | -23 · t=-0,8 · p=49% · n=247 | — | 210 (n=22) | 0 · t=0,5 · p=50% · n=283 |
| 5+15+30 | fixo60 | N2 | -24 · t=-0,7 · p=49% · n=199 | — | 184 (n=15) | 0 · t=0,2 · p=50% · n=234 |
| 5+15+60 | fixo60 | N2 | -60 · t=-0,6 · p=46% · n=56 | — | — | 2 · t=1,3 · p=56% · n=91 |
| 5+15+60 | fixo60 | N1 | -34 · t=-0,6 · p=48% · n=120 | — | 214 (n=11) | 2 · t=1,8 · p=53% · n=173 |
| 5+15+30 | fixo60 | N1 | -15 · t=-0,6 · p=48% · n=362 | — | 81 (n=41) | 1 · t=1,0 · p=48% · n=404 |
| 5+30 | fixo60 | N1 | -10 · t=-0,5 · p=48% · n=500 | — | 52 (n=56) | 1 · t=1,2 · p=49% · n=519 |
| 5+60 | fixo60 | N2 | -31 · t=-0,5 · p=49% · n=80 | — | 493 (n=5) | 2 · t=1,2 · p=54% · n=123 |
| 5+15 | fixo60 | N1 | -6 · t=-0,4 · p=50% · n=1263 | — | -22 (n=138) | 0 · t=0,2 · p=48% · n=1353 |
| 5+15 | fixo60 | N2 | 8 · t=0,4 · p=50% · n=788 | — | -63 (n=88) | 0 · t=0,9 · p=50% · n=874 |

**CF-H07:** nenhuma combinação tem |t| ≥ 3 na descoberta com o mesmo sinal no hold-out.

## 3. CF-H08 — o alinhamento supera a cor do TF maior sozinho?

Diferença, em pontos por evento, do retorno de 60 min: alinhamento menos a barra do TF maior sozinha, no mesmo nível de cor. Positivo = o alinhamento rende mais.

| conjunto | def | nível | n | descoberta | hold-out 1 |
|---|---|---|---|---|---|
| 30+60 | bollinger | N1 | 700 | -1,9 | -35,7 |
| 30+60 | bollinger | N2 | 40 | 21,6 | -54,1 |
| 30+60 | fixo60 | N1 | 1.929 | 15,9 | -14,7 |
| 30+60 | fixo60 | N2 | 1.095 | 21,4 | -37,9 |
| 5+15 | bollinger | N1 | 222 | 57,1 | — |
| 5+15 | bollinger | N2 | 40 | 41,0 | — |
| 5+15 | fixo60 | N1 | 1.263 | -9,1 | — |
| 5+15 | fixo60 | N2 | 788 | 2,9 | — |
| 5+15+30 | fixo60 | N1 | 362 | -10,4 | — |
| 5+15+30 | fixo60 | N2 | 199 | -11,8 | — |
| 5+15+30+60 | fixo60 | N1 | 94 | -48,2 | — |
| 5+15+30+60 | fixo60 | N2 | 40 | -99,2 | — |
| 5+15+60 | fixo60 | N1 | 120 | -32,0 | — |
| 5+15+60 | fixo60 | N2 | 56 | -55,0 | — |
| 5+30 | bollinger | N1 | 51 | -66,7 | — |
| 5+30 | fixo60 | N1 | 500 | -5,8 | — |
| 5+30 | fixo60 | N2 | 247 | -11,3 | — |
| 5+60 | fixo60 | N1 | 181 | -34,5 | — |
| 5+60 | fixo60 | N2 | 80 | -26,3 | — |

Nenhuma diferença mantém o sinal entre a descoberta e o hold-out.

## 4. CF-H09 — limiar fixo 60/80 × Bollinger

| conjunto | nível | Bollinger | limiar fixo |
|---|---|---|---|
| 30+60 | N1 | 41 (n=700, t=1,8) | 31 (n=1929, t=2,2) |
| 30+60 | N2 | 156 (n=40, t=1,5) | 50 (n=1095, t=2,6) |
| 5+15 | N1 | 53 (n=222, t=1,4) | -6 (n=1263, t=-0,4) |
| 5+15 | N2 | 68 (n=40, t=0,8) | 8 (n=788, t=0,4) |
| 5+30 | N1 | -72 (n=51, t=-1,1) | -10 (n=500, t=-0,5) |

As duas definições dão o mesmo sinal onde dá para comparar. O limiar fixo gera de 2 a 6 vezes mais eventos e não muda a conclusão.

## 5. Quantos pontos andam (MFE e MAE em 60 min, WIN, Bollinger N1)

| conjunto | n | MFE med (pts) | MAE med (pts) | a favor da cor |
|---|---|---|---|---|
| 15+30 | 1.028 | 450 | 402 | 51,6 % |
| 15+30+60 | 225 | 471 | 384 | 54,2 % |
| 15+60 | 321 | 481 | 399 | 53,6 % |
| 30+60 | 1.454 | 420 | 358 | 53,3 % |
| 5+15 | 241 | 343 | 328 | 49,0 % |
| 5+30 | 51 | 277 | 344 | 47,1 % |

O máximo a favor e o máximo contra são praticamente iguais: o movimento fica a favor da cor em 48% a 53% dos casos.

## 6. Veredito

| ID | Veredito |
|---|---|
| CF-H07 | **REFUTADA** — nenhuma combinação; o melhor caso (t = 2,6) troca de sinal no hold-out |
| CF-H08 | **REFUTADA** — a diferença contra a cor do TF maior sozinho troca de sinal entre os períodos |
| CF-H09 | **REFUTADA** — limiar fixo 60/80 e Bollinger dão o mesmo sinal; o limiar só aumenta a frequência |

## 7. Por que o gráfico parece dizer o contrário

- **O movimento existe, o lado não.** Quando as cores alinham, o mercado anda bastante (MFE mediano de 350 a 470 pts em 60 min). O olho registra o deslocamento e esquece que o deslocamento contrário é do mesmo tamanho.
- **Viés de memória.** Os casos em que a cor acerta são memoráveis; os que erram parecem "o mercado mudou". A conta dos dois está na seção 5: empate.
- **Persistência curta.** Em 30 e 60 min o retorno tem autocorrelação positiva (ANALISE_002 do M02), então uma tendência em andamento tende a continuar por algumas barras. Isso vale para qualquer barra colorida, não só para as alinhadas, e não se sustenta depois de 2019.

