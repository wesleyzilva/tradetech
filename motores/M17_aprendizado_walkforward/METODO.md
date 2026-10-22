# M17 — Método (congelado em 2026-10-22, antes de rodar qualquer modelo)

Pergunta do motor: com um modelo estatístico mais flexível que uma regra de cor, e com um protocolo que não deixa o acaso passar por achado, **o que é previsível nos candles de 30 e 60 min do WIN, e o que não é?** Dois alvos separados: a **amplitude** (quanto o preço vai andar) e o **lado** (para onde).

## Dados

| Papel | Série | Período |
|---|---|---|
| Treino e teste (walk-forward) | WINFUT 30 e 60 min | 2014-01-02 → 2025-12-30 |
| Replicação | WDOFUT 30 e 60 min | 2014-01-02 → 2025-12-30 |
| Cruzamento (variáveis do grupo D) | WDOFUT para o WIN, WINFUT para o WDO | idem |
| Teste final, um disparo | WINM26 até 2026-05-13 e WINQ26 depois | 2026-01-02 → 2026-07-24 |

Lote padrão (sem `_alt`). Nenhum parâmetro, variável ou hiperparâmetro é escolhido olhando 2026.

## Evento

Uma observação por barra do TF base que **fecha** entre 09:30 e 17:00, desde que as `h` barras seguintes existam, sejam consecutivas e caiam no mesmo pregão. Os rótulos nunca cruzam pregões, então não há sobreposição entre dias e o embargo é de 1 pregão.

## Rótulos (h = 1 e h = 2 barras do TF base: 30 e 60 min na base de 30; 60 e 120 min na base de 60)

- **Amplitude:** `y_vol = ln[(max H − min L das h barras seguintes) ÷ C da barra do sinal]`.
- **Lado:** `ret_h = C da barra t+h − O da barra t+1` (entra na abertura seguinte, como no simulador). `y_dir = 1` se `ret_h > 0`. O resultado econômico usa `sinal × ret_h` em pontos básicos do preço, com custo de **0,4 pb** por trade (equivale a 5 pts no WIN).

## Variáveis (biblioteca fixa; todas conhecidas no fechamento da barra do sinal)

| Grupo | Variáveis |
|---|---|
| A — estrutura | `ret1`, `ret2`, `ret4` (variação do fechamento em ATR), `corpo` = (C−O)/ATR, `rng_rel` = range/ATR, `atr_ratio` = média 5 ÷ média 60 do range, `z20` = (C − SMA20)/desvio20, `pos_dia` = posição do fechamento entre mínima e máxima do dia até ali, `ret_dia` = (C − abertura do dia)/ATR, `gap` = (abertura do dia − fechamento anterior)/ATR, `amp_ant` = range do dia anterior ÷ média dos 20 dias anteriores |
| B — tempo | `slot` (barras desde a abertura), `slot2`, `dow` |
| C — volume | `v_rel` = volume financeiro ÷ média do mesmo slot nos 20 pregões anteriores, `q_rel` = o mesmo para Quantidade |
| V — memória de volatilidade | `lrng1` = ln(range/C), `lrng5`, `lrng20` (médias de `ln(range/C)`), `B0` = média de `y_vol` do mesmo slot nos 60 pregões anteriores |
| D — cruzamento | no WIN: variação do WDO na mesma barra em ATR do WDO (`x_ret1`, `x_ret2`, `x_ret4`, `x_ret_dia`). No WDO: o mesmo com o WIN |
| E — cor (M01) | `F = m·a·100`, `est` ∈ −2..2 e `z_cor` de `calcular` do M01 (janela 20) |

ATR = média de 20 barras do range, incluindo a barra do sinal. `ret*` e `gap` são cortados em ±6 ATR (vencimento de contrato e dados ruins).

Conjuntos: **S2 = A+B+C+V** (estrutura), **S3 = S2 + D**, **S4 = S2 + E**.

## Modelos (hiperparâmetros fixos, nenhum é ajustado)

- Linear: `Ridge(alpha=10)` para amplitude e `LogisticRegression(C=0,1)` para lado; imputação pela mediana do treino e padronização.
- Árvores: `HistGradientBoosting` com `max_depth=3`, `learning_rate=0,05`, `max_iter=200`, `min_samples_leaf=200`, `l2_regularization=1`, `random_state=0`.

## Validação

- **Walk-forward expansivo:** treina em todos os anos anteriores ao ano de teste; testa em cada ano de **2018 a 2025** (8 dobras). Concatena as previsões fora da amostra.
- **Descoberta = 2018–2021; confirmação = 2022–2025** (usadas só para ler a consistência, nenhuma escolha usa a confirmação).
- Estatística por **pregão** (bootstrap por dia, 400 repetições; o desvio da métrica vem dessa reamostragem). `z = (métrica − referência) ÷ desvio bootstrap`.
- **Placebo:** o mesmo pipeline do lado é rodado 10 vezes com `y_dir` embaralhado entre pregões do mesmo ano e do mesmo slot. O maior `z` entre as células de cada placebo dá a distribuição do que o acaso entrega.

## Células

Por ativo: 2 TFs × 2 horizontes × 3 conjuntos × 2 modelos = **24 células de lado** e **24 de amplitude**. Total declarado: **96** (WIN e WDO). A decisão do WIN é a que vale; o WDO só replica.

## Linhas de base de amplitude

- **B0:** média de `y_vol` do mesmo slot nos 60 pregões anteriores.
- **B1 (tipo HAR):** OLS de `y_vol` em `B0, lrng1, lrng5, lrng20`, reajustada a cada dobra. Um modelo só conta se ganhar de **B1**, não de B0.
