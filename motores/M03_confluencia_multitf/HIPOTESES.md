# M03 — Hipóteses (CF-H##) — **congeladas em 2026-10-22, antes de rodar**

Regras e definições: [`METODO.md`](METODO.md). Veredito padrão: `docs/01_CONVENCOES.md` §2.
Número de estratégias com barreira testadas: **132** (declarado); o esperado por acaso com |t| ≥ 3 é < 1, mas com |t| ≥ 2 é ≈ 5–6 — por isso exigimos replicação.

| ID | Pergunta | Critério de veredito (congelado) | Status | Veredito |
|---|---|---|---|---|
| CF-H01 | A confluência (modo A) antecipa **expansão de range** maior do que cor em TF único? | Range da barra base seguinte ÷ média do mesmo horário: diferença confluência − TF único > 0 com t ≥ 3 na descoberta e > 0 com t ≥ 2 nos hold-outs 1 e 2 | PENDENTE | — |
| CF-H02 | A confluência tem **direção** (continuação ou fade)? | Retorno alinhado médio ≠ 0 em algum h: \|t\| ≥ 3 na descoberta, **mesmo sinal** com \|t\| ≥ 2 nos hold-outs 1 e 2 e mesmo sinal no WDO | PENDENTE | — |
| CF-H03 | **Quantos pontos** se pode capturar? (descritivo) | Sem veredito: distribuição de MFE e MAE em 60 min (p25, mediana, p75, p90) em pontos e em ATR | PENDENTE | descritivo |
| CF-H04 | Existe estratégia com barreira (continuação ou fade) com esperança líquida positiva? | Esperança líquida (custo 5 pts) > 0 com `t_vs_nulo` ≥ 3 na descoberta e > 0 com `t_vs_nulo` ≥ 2 nos hold-outs 1 e 2 e bruto > 0 no WDO | PENDENTE | — |
| CF-H05 | A confluência é melhor que o TF único com a mesma estratégia? | Diferença de PnL por pregão (confluência − TF único) > 0, t ≥ 2 (Welch por pregão) na descoberta e mesmo sinal nos dois hold-outs | PENDENTE | — |
| CF-H06 | O alerta é raro o suficiente para chamar atenção (≤ 3 por pregão no conjunto escolhido)? | Eventos por pregão do modo A ≤ 3 | PENDENTE | descritivo |

Regra: se **nenhuma** estratégia satisfizer CF-H04, o veredito do motor é "sem vantagem demonstrável com os dados atuais" — e o alerta continua útil como **filtro de volatilidade/atenção**, não como gatilho direcional.
