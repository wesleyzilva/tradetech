# M16 — Hipóteses (CF-H##) — **congeladas em 2026-10-22, antes de rodar**

Regras e definições: [`METODO.md`](METODO.md). Veredito padrão: `docs/01_CONVENCOES.md` §2.
Número de estratégias com barreira testadas: **132** (declarado); o esperado por acaso com |t| ≥ 3 é < 1, mas com |t| ≥ 2 é ≈ 5–6 — por isso exigimos replicação.

| ID | Pergunta | Critério de veredito (congelado) | Status | Veredito |
|---|---|---|---|---|
| CF-H01 | A confluência (modo A) antecipa **expansão de range** maior do que cor em TF único? | Range da barra base seguinte ÷ média do mesmo horário: diferença confluência − TF único > 0 com t ≥ 3 na descoberta e > 0 com t ≥ 2 nos hold-outs 1 e 2 | EXECUTADA | **INCONCLUSIVA** — nenhum conjunto chega a t ≥ 3; com amostra grande (30+60, n ≈ 700) a diferença é ~0, e nos 5 min (n ≈ 40–110) falta poder (ANALISE_001 §3) |
| CF-H02 | A confluência tem **direção** (continuação ou fade)? | Retorno alinhado médio ≠ 0 em algum h: \|t\| ≥ 3 na descoberta, **mesmo sinal** com \|t\| ≥ 2 nos hold-outs 1 e 2 e mesmo sinal no WDO | EXECUTADA | **REFUTADA** nos conjuntos grandes (15+30 e 30+60, n ≥ 600): sinal positivo na descoberta e negativo nos hold-outs; os raros não têm poder (ANALISE_001 §4) |
| CF-H03 | **Quantos pontos** se pode capturar? (descritivo) | Sem veredito: distribuição de MFE e MAE em 60 min (p25, mediana, p75, p90) em pontos e em ATR | EXECUTADA | descritivo: MFE e MAE em 60 min são quase iguais (MFE > MAE em ~47–53 % dos eventos); a cor diz **amplitude**, não lado (ANALISE_001 §5) |
| CF-H04 | Existe estratégia com barreira (continuação ou fade) com esperança líquida positiva? | Esperança líquida (custo 5 pts) > 0 com `t_vs_nulo` ≥ 3 na descoberta e > 0 com `t_vs_nulo` ≥ 2 nos hold-outs 1 e 2 e bruto > 0 no WDO | EXECUTADA | **REFUTADA** — 0 de 114 estratégias passam; 1 passa a descoberta (n=40) e falha no hold-out 1 (ANALISE_001 §6) |
| CF-H05 | A confluência é melhor que o TF único com a mesma estratégia? | Diferença de PnL por pregão (confluência − TF único) > 0, t ≥ 2 (Welch por pregão) na descoberta e mesmo sinal nos dois hold-outs | EXECUTADA | **REFUTADA** — 5 passam na descoberta, 0 replicam nos dois hold-outs; a "vantagem" por pregão vem de operar menos (ANALISE_001 §6) |
| CF-H06 | O alerta é raro o suficiente para chamar atenção (≤ 3 por pregão no conjunto escolhido)? | Eventos por pregão do modo A ≤ 3 | EXECUTADA | descritivo: 5+15 N1 ≈ 0,4 alerta/pregão (modo A); 15+30 N1 ≈ 0,8; 30+60 N1 ≈ 0,5; triplas ≈ 0,01–0,2; N2 quase não ocorre em 2+ TFs |

Regra: se **nenhuma** estratégia satisfizer CF-H04, o veredito do motor é "sem vantagem demonstrável com os dados atuais" — e o alerta continua útil como **filtro de volatilidade/atenção**, não como gatilho direcional.

## Conclusão (ANALISE_001, 2026-10-22)

Com a grade congelada, **não há vantagem direcional demonstrável** na confluência de cor entre timeframes (WIN, 2014–2026; replicação em WDO). A confluência é **rara** (≤ 1 alerta por pregão) e **não é mais volatilidade** do que a cor em um TF só. Pode servir como alarme de atenção, não como gatilho de entrada.
Ressalva de poder: a base de 5 min tem só 491 pregões e os conjuntos com 3+ TFs têm menos de 40 eventos — resultado nulo ali significa "não detectável", não "provadamente zero".
