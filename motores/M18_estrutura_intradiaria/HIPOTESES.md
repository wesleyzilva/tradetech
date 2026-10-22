# M18 — Hipóteses (ID-H##) — **congeladas em 2026-10-22, antes de rodar**

Regras e definições: [`METODO.md`](METODO.md). Veredito padrão: `docs/01_CONVENCOES.md` §2.
Total de testes declarado: **35**. Limiar de descoberta: `|t| ≥ 3,0`.

| ID | Pergunta | Critério de veredito (congelado) | Status | Veredito |
|---|---|---|---|---|
| ID-H01 | O sentido do dia até 10:00, 14:00 ou 16:00 continua até o fim do pregão? | Alguma das 3 origens passa o critério do `METODO.md` | EXECUTADA | **REFUTADA** — nenhuma das 3 origens passa de `|t|` 1,0 na descoberta (acerto 49% a 50%). O dia que subiu até as 10:00, 14:00 ou 16:00 não continua além do acaso |
| ID-H02 | Alguma faixa de 30 min rende mais ou menos que as outras do mesmo dia, de forma estável? | Alguma das 17 faixas passa o critério | EXECUTADA | **INCONCLUSIVA** — uma faixa em 17 chega a `|t| ≥ 3`: 09:30 (+2,2 pb sobre a média do dia, t = 3,45, acerto 53%; 10 de 12 anos). No hold-out o sinal é o mesmo mas fraco (+1,2 pb, t = 1,63 < 2), decai (2022–2025: −1,7; +1,6; −0,8; +0,6) e o WDO tem sinal **oposto** (−1,3 pb, t = −2,4) |
| ID-H03 | Algum dia da semana rende diferente dos demais? | Algum dos 5 dias passa o critério | EXECUTADA | **REFUTADA** — nenhum dos 5 dias passa de `|t|` 2,2 na descoberta; a segunda-feira muda de sinal no hold-out |
| ID-H04 | O gap de abertura é desfeito (fade) até 10:00, 12:00 ou o fim do pregão? | Alguma das 6 células passa o critério | EXECUTADA | **REFUTADA** — maior `|t|` 2,7 (gap ≥ 0,5 ATRd, saída 10:00: o gap continua em vez de ser desfeito, −13 pb, 10 de 12 anos), abaixo do limiar; no hold-out cai para t = −0,9 e o WDO tem sinal oposto |
| ID-H05 | O rompimento da faixa de abertura continua até 12:00 ou o fim do pregão? | Alguma das 4 células passa o critério | EXECUTADA | **REFUTADA** — maior `|t|` 1,5 (OR 09:00–10:00, saída no fim do pregão, 11 de 12 anos com o mesmo sinal, +4 a +5 pb); sem poder para ser distinguido do acaso |

Regra: se nenhuma hipótese for CONFIRMADA, o veredito do motor é "sem estrutura intradiária com direção sustentada em 2014–2025", e o passo 4 da fila (M17 diário) perde as variáveis de entrada.

## Conclusão (ANALISE_001, 2026-10-22)

Das 35 células, 1 chega a `|t| ≥ 3` na descoberta (o acaso daria 0,1) e 0 passam o critério inteiro. A estrutura intradiária de 30 min não tem direção que se sustente entre 2014–2019, 2020–2025 e WDO.

O que fica como observação, sem ser achado: a faixa 09:30–10:00 do WIN rende acima do resto do dia até 2021 e some depois; o WDO faz o oposto na mesma faixa. Qualquer hipótese que nasça daqui (por exemplo, ligada ao horário de abertura das ações) foi sugerida por estes dados e só pode ser confirmada em dado novo (WINFUT de 2026), não neste.
