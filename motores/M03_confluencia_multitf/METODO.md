# M03 — Método (congelado em 2026-10-22, antes de rodar a análise)

## Cor (canônica do M01)

`calcular(d, janela=20)` de `motores/M01_fma_forca/teses/cores/analise_candles.py`: `F = m·a·100` (m = corpo ÷ range; a = volume financeiro ÷ média das 20 barras anteriores), `z` = z-score de F em 20 barras (inclui a barra atual), estados `est ∈ {−2,−1,0,+1,+2}`:

- **N1 (colorido / ignição):** `|z| ≥ 1,5` com F de mesmo sinal → `|est| ≥ 1`
- **N2 (brilhante / saturação):** `|z| ≥ 2,5` → `|est| = 2`
- Família `fam = sign(est)`: +1 compradora, −1 vendedora.

O estado de cada timeframe é calculado **nos candles do próprio timeframe** (CSV do Profit daquele TF), como o operador vê no gráfico.

## Evento de confluência

Instante `T` = fechamento de uma barra do **TF base** (o menor do conjunto). Janela: barra base com abertura entre 09:15 e 16:10.

- **Modo A (simultâneo, primário):** a barra base e **uma barra de cada TF superior do conjunto fecham em T**, todas com a mesma `fam` e nível ≥ N.
- **Modo B (contexto, sensibilidade):** a barra base fecha colorida em T e a **última barra fechada** de cada TF superior (fechada ≤ T, no mesmo pregão, há no máximo 1 período daquele TF) tem a mesma `fam` e nível ≥ N. O modo A é subconjunto do B.
- **TF único (controle de comparação):** a barra base está colorida no mesmo nível, sem exigir TF superior.
- **Nulo:** barras sorteadas na mesma janela, lado sorteado, mesma saída.

Conjuntos testados (TF base → TFs superiores): base 5 min → {15}, {30}, {60}, {15,30}, {15,60}, {30,60}, {15,30,60}; base 15 min → {30}, {60}, {30,60}; base 30 min → {60}. Níveis N1 e N2. **11 conjuntos × 2 níveis.**

## Execução e saída (simulador `mb_motor.py`, perfil *ideal* = stop manual colocado na entrada)

- Entrada na **abertura da barra base seguinte**, mesmo pregão; uma posição por vez.
- **Continuação:** lado = `fam` do evento. **Fade:** lado = −`fam`.
- Barreiras em múltiplos do ATR(20) do TF base: (SL, SG) ∈ {(0,5; 1,5), (1; 2), (1; 3)}; sem pisos; stop **a mercado** (`stop_a_mercado=True`); stop antes do alvo na mesma barra.
- Tempo máximo: 60 minutos (12 barras de 5 min; 4 de 15 min). Zeramento 17:20.
- Custo: **5 pts por trade no WIN** (WDO só bruto, em múltiplos de ATR).
- **Estratégias testadas:** 11 conjuntos × 2 níveis × 2 lados × 3 geometrias = **132** (mais 12 de TF único e o nulo).

## Conjuntos de dados (descoberta × replicação)

| Base | Descoberta | Hold-out 1 | Hold-out 2 | Replicação cruzada |
|---|---|---|---|---|
| 5 min | WINFUT 2024-06-19 → 2025-06-30 | WINFUT 2025-07-01 → 2025-12-30 | WINM26 até 2026-05-14 + WINQ26 depois | WDOFUT 2024-06-25 → 2025-12-30 |
| 15 min | WINFUT 2020-11-03 → 2023-12-31 | WINFUT 2024-01-01 → 2025-12-30 | WINM26 até 2026-05-14 + WINQ26 depois | WDOFUT 2020-11-03 → 2025-12-30 |
| 30 min | WINFUT 2014-01-02 → 2019-12-31 | WINFUT 2020-01-01 → 2025-12-30 | WINM26 até 2026-05-14 + WINQ26 depois | WDOFUT 2014-01-02 → 2025-12-30 |

Só pregões completos (≥ 90 % das barras do p95). WINM26/WINQ26 são simulados cada um na própria série (sem juntar contratos); o hold-out 2 usa os trades de cada contrato no seu intervalo.

## Estatística

- Unidade = **pregão**. `t` por pregão (soma por dia, dias sem evento contam zero).
- `t_vs_nulo`: soma por dia de `pnl − média_do_nulo` por trade; a média do nulo vem de 20 repetições de entradas aleatórias (probabilidade 3 % por barra de janela, lado sorteado) com a mesma geometria, no mesmo conjunto.
- Alinhamento de retorno: `sinal × (c[i+h] − o[i+1])`, mesmo pregão, h em barras base de 5, 15, 30 e 60 minutos.
- MFE/MAE: extremos favorável/adverso em relação à entrada nas 12 barras (5 min) ou 4 barras (15 min) seguintes, em pontos e em ATR.

## Emenda 1 (antes de qualquer resultado)

A contagem de eventos de uma simulação de verificação mostrou que, na base de 5 min (383 pregões), o modo A tem ~150 eventos no N1 para {15} e quase nenhum para {15,30,60}: **poder estatístico baixo**. Para ter uma amostra com poder real foi acrescentada a **base de 30 min com TF superior 60 min** (12 anos). Nenhuma estatística de desempenho tinha sido calculada nesse momento.
