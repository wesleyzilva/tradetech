# M19 — ANALISE_001: estrutura diária e semanal

Gerado por `codigo/analise_001.py`. Protocolo congelado em [`METODO.md`](../METODO.md) e [`HIPOTESES.md`](../HIPOTESES.md) antes de rodar. WINFUT D1 e W1, 2014–2025; replicação em WDOFUT. Descoberta 2014–2019, hold-out 2020–2025. Poder baixo (≈ 1.500 dias e ≈ 310 semanas por período): nulo = "não detectável".

## 1. Resumo (calculado)

- Células com `|t| ≥ 3` na descoberta: **0** de 10; passam o critério inteiro: **0**.
- Maior `|t|` na descoberta: 2,61; no hold-out: 2,44.
- Vereditos: DD-H01 **REFUTADA**; DD-H02 **REFUTADA**; DD-H03 **REFUTADA**; DD-H04 **REFUTADA**.

## 2. Células

Média: excedente em pb por trade (DD-H01, DD-H04), desvio da razão de amplitude (DD-H02) ou diferença semana − demais (DD-H03: razão de amplitude e pb).

| célula | desc: média | t | acerto | n | hold: média | t | acerto | WDO: média | t | anos | margem | passa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DD-H04 · posição do fechamento de ontem | -12,943 | -2,61 | 46,2 % | 738 | -11,749 | -2,44 | 46,4 % | -8,333 | -3,40 | 9/12 | 30,9 | não |
| DD-H04 · corpo de ontem | -6,967 | -1,98 | 48,4 % | 1472 | -6,977 | -2,14 | 48,1 % | -3,799 | -2,21 | 9/12 | 17,4 | não |
| DD-H02 · NR7 | -0,052 | -1,94 | 37,2 % | 218 | -0,001 | -0,04 | 44,0 % | -0,052 | -3,07 | 9/12 | – | não |
| DD-H01 · semanal k=1 | -33,498 | -1,88 | 48,6 % | 313 | -0,444 | -0,03 | 51,6 % | 4,055 | 0,51 | 8/12 | 42,5 | não |
| DD-H02 · inside bar | 0,040 | 1,42 | 46,9 % | 177 | 0,010 | 0,34 | 42,5 % | -0,048 | -2,61 | 7/12 | – | não |
| DD-H03 · amplitude na semana do vencimento | -0,036 | -1,20 | 37,9 % | 169 | -0,034 | -1,09 | 39,1 % | -0,012 | -0,56 | 9/12 | – | não |
| DD-H01 · semanal k=4 | -20,286 | -1,13 | 51,0 % | 310 | 17,603 | 1,16 | 52,2 % | 1,205 | 0,15 | 5/12 | 3,2 | não |
| DD-H01 · diário k=5 | -1,646 | -0,47 | 50,0 % | 1477 | 1,018 | 0,31 | 49,7 % | -2,031 | -1,18 | 5/12 | 0,8 | não |
| DD-H01 · diário k=20 | -1,336 | -0,38 | 49,8 % | 1461 | 3,443 | 1,06 | 51,1 % | 0,461 | 0,27 | 6/12 | -2,7 | não |
| DD-H03 · retorno do dia na semana do vencimento | -2,965 | -0,29 | 47,9 % | 169 | -2,717 | -0,30 | 49,7 % | 2,301 | 0,46 | 5/12 | – | não |

## 3. Por ano (média da célula)

| célula | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DD-H04 · posição do fechamento de ontem | -7,81 | -5,90 | -30,88 | -12,47 | -20,13 | 3,89 | -42,76 | -46,25 | 12,91 | 15,41 | -10,64 | -1,16 |
| DD-H04 · corpo de ontem | -7,73 | -7,55 | -12,41 | -4,81 | -10,20 | 0,94 | -21,32 | -19,50 | 2,40 | 2,42 | -2,16 | -3,74 |
| DD-H02 · NR7 | 0,05 | -0,06 | -0,09 | -0,07 | -0,04 | -0,09 | -0,07 | -0,03 | 0,06 | 0,10 | -0,03 | -0,02 |
| DD-H01 · semanal k=1 | -6,92 | -61,83 | -62,18 | -10,64 | -21,88 | -36,99 | 10,16 | -9,18 | -41,88 | 8,77 | 5,73 | 25,02 |
| DD-H02 · inside bar | 0,16 | 0,03 | 0,06 | -0,03 | -0,00 | 0,05 | -0,06 | 0,03 | 0,16 | -0,02 | 0,02 | -0,02 |
| DD-H03 · amplitude na semana do vencimento | 0,08 | -0,01 | -0,07 | -0,10 | -0,17 | 0,05 | -0,05 | -0,06 | -0,01 | 0,03 | -0,07 | -0,04 |
| DD-H01 · semanal k=4 | -34,85 | -66,08 | 42,97 | 9,00 | -33,98 | -40,84 | 89,49 | 5,99 | 8,97 | 23,37 | 26,42 | -49,76 |
| DD-H01 · diário k=5 | 1,71 | 0,45 | -3,25 | 0,11 | -8,12 | -0,75 | 3,18 | -2,16 | 0,59 | -1,59 | 1,30 | 4,78 |
| DD-H01 · diário k=20 | -1,12 | -5,39 | 0,82 | 3,03 | -0,23 | -5,10 | 16,61 | 1,76 | -2,71 | 11,52 | 2,98 | -9,45 |
| DD-H03 · retorno do dia na semana do vencimento | 12,06 | -28,00 | 15,17 | -4,47 | -12,00 | -2,35 | 13,98 | 6,70 | -55,71 | 10,65 | 2,97 | 1,79 |
