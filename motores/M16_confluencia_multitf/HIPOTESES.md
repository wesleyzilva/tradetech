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

## ANALISE_002 — alinhamento no mesmo instante (congelado em 2026-10-22, antes de rodar)

**Pergunta do operador:** quando, no mesmo minuto, timeframes diferentes mostram a mesma cor, a probabilidade de o movimento continuar no intraday é maior? E com os limiares do robô (faixa inicial em |F| ≥ 60 e saturação em |F| ≥ 80, que corresponde ao percentil ~84 de |F| no 5 min)?

**Por que reabrir.** A ANALISE_001 exigia que as barras dos TFs **fechassem juntas** (modo A) e usava o estado Bollinger. Visualmente, o que se vê no gráfico é outra coisa: no instante T, a barra do TF maior **está em formação** e a cor dela até agora coincide com a do TF menor. Isso é o que se testa aqui. O modo A da ANALISE_001 continua válido para o que ele mediu.

**Definições (congeladas):**
- Âncora T = fechamento da barra do TF maior (15, 30 ou 60 min), dentro de 09:15–16:00.
- Cor do TF maior = estado da **própria barra que fecha em T** (fechamento conhecido em T).
- Cor do TF menor em T = estado da **última barra do TF menor fechada até T** (defasagem máxima = período do TF menor).
- Definições de cor: **Bollinger** (N1 = |z| ≥ 1,5; N2 = |z| ≥ 2,5) e **limiar fixo** (|F| ≥ 60 = faixa inicial; |F| ≥ 80 = saturação).
- Conjuntos: 2 TFs (5+15, 5+30, 5+60, 15+30, 15+60, 30+60) e 3+ TFs (5+15+30, 5+15+60, 15+30+60, 5+15+30+60), todos com a mesma família.
- Controle: a barra do TF maior sozinha, no mesmo nível de cor.
- Horizonte: retorno alinhado à cor, do fechamento em T até +15, +30, +60 e +120 min, dentro do mesmo pregão. Também MFE e MAE em 60 min.
- Estatística: t por pregão (soma diária). Descoberta = WINFUT até o corte da base; hold-out 1 = WINFUT depois; hold-out 2 = WINM26/WINQ26; replicação = WDO.
- Cortes por TF âncora: 15 min → 2023-12-31; 30 e 60 min → 2019-12-31.

| ID | Pergunta | Critério (congelado) | Status | Veredito |
|---|---|---|---|---|
| CF-H07 | O alinhamento simultâneo (barra do TF maior em formação incluída) tem direção? | Retorno alinhado ≠ 0 em algum horizonte: \|t\| ≥ 3 na descoberta (n ≥ 100), mesmo sinal com \|t\| ≥ 2 nos hold-outs 1 e 2 e mesmo sinal no WDO | PENDENTE | — |
| CF-H08 | O alinhamento supera a cor do TF maior sozinho? | Diferença de retorno alinhado (alinhado − TF maior só) > 0 com t ≥ 3 na descoberta e mesmo sinal com t ≥ 2 nos dois hold-outs | PENDENTE | — |
| CF-H09 | Os limiares fixos 60/80 mudam o resultado em relação ao Bollinger? | Comparar, no mesmo conjunto, a diferença de retorno alinhado entre as duas definições: \|t\| ≥ 3 e mesmo sinal nos dois hold-outs | PENDENTE | — |
