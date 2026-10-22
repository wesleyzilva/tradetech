# M17 — Diagnóstico da ANALISE_001

Robustez do que apareceu na análise principal. Nada aqui muda um veredito; serve para entender de onde vem o sinal de lado e quão grande ele é.

## 1. Empates no rótulo

O rótulo `y_dir` trata `ret = 0` como queda. Sem esses casos (cerca de 0,4% a 1,3% das barras), com o mesmo modelo S2:

| TF | h | modelo | AUC sem empates | z |
|---|---|---|---|---|
| 30 | 1 | linear | 0,5123 | 3,60 |
| 30 | 1 | hgb | 0,5103 | 3,31 |
| 30 | 2 | linear | 0,5131 | 3,12 |
| 30 | 2 | hgb | 0,5157 | 3,81 |
| 60 | 1 | linear | 0,5122 | 2,51 |
| 60 | 1 | hgb | 0,5197 | 4,58 |
| 60 | 2 | linear | 0,5208 | 3,55 |
| 60 | 2 | hgb | 0,5213 | 3,73 |

## 2. De onde vem o sinal (AUC univariada, descritiva, toda a amostra WIN, h = 1)

AUC < 0,5 significa que valor alto da variável acompanha queda na barra seguinte (reversão); > 0,5, alta (continuação). Descritivo: não é teste fora da amostra.

**30 min:** `ret2` 0,4891; `z20` 0,4891; `corpo` 0,4916; `ret4` 0,4917; `q_rel` 0,5079; `ret1` 0,4923; `v_rel` 0,5077; `F` 0,4925

**60 min:** `ret_dia` 0,5097; `pos_dia` 0,5092; `slot` 0,5088; `est` 0,5067; `gap` 0,4954; `x_ret1` 0,5046; `x_ret_dia` 0,4955; `z_cor` 0,5039

## 3. A célula que passou (WIN, 60 min, h = 1, S2, árvores)

| ano | AUC | trades | líq. pb por trade |
|---|---|---|---|
| 2018 | 0,5615 | 1956 | 2,88 |
| 2019 | 0,5381 | 1980 | 1,98 |
| 2020 | 0,5129 | 1937 | 2,82 |
| 2021 | 0,4820 | 1972 | -0,37 |
| 2022 | 0,5191 | 1996 | 0,04 |
| 2023 | 0,5171 | 1980 | 0,55 |
| 2024 | 0,5275 | 2004 | 0,15 |
| 2025 | 0,5016 | 1996 | -0,88 |

Agregado: AUC 0,5208; esperança líquida 0,89 pb por trade (bruta 1,29); t por pregão 2,83; 8,0 trades por pregão.
Em pontos do WIN (preço médio do período 163806): cerca de 14,5 pts líquidos por trade, ou 116 pts por pregão por contrato, com custo de 5 pts e entrada exata na abertura da barra seguinte.
Um slippage de 5 pts por lado (10 por trade) já zera isso: o sinal existe estatisticamente, mas a margem econômica é da ordem do custo.

### Sensibilidade ao custo (esperança por trade, pb)

| custo por trade (pb) | esperança | t por pregão |
|---|---|---|
| 0,4 | 0,89 | 2,83 |
| 0,8 | 0,49 | 1,55 |
| 1,2 | 0,09 | 0,28 |
| 1,6 | -0,31 | -1,00 |
