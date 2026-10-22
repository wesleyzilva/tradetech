# M19 — Hipóteses (DD-H##) — **congeladas em 2026-10-22, antes de rodar**

Regras e definições: [`METODO.md`](METODO.md). Veredito padrão: `docs/01_CONVENCOES.md` §2.
Total de testes declarado: **10**. Limiar de descoberta: `|t| ≥ 3,0`. Poder baixo: nulo = "não detectável".

| ID | Pergunta | Critério de veredito (congelado) | Status | Veredito |
|---|---|---|---|---|
| DD-H01 | O retorno dos últimos 5 ou 20 dias (ou 1 ou 4 semanas) prevê o sinal do período seguinte? | Alguma das 4 células passa o critério do `METODO.md` | EXECUTADA | **REFUTADA** (maior `|t|` 1,88; sinais trocam entre os períodos) |
| DD-H02 | Depois de NR7 ou inside bar o range seguinte é maior que o normal? | Alguma das 2 células passa | EXECUTADA | **REFUTADA** (maior `|t|` 1,94; no hold-out ≈ 0) |
| DD-H03 | A semana do vencimento tem amplitude ou retorno diferentes das demais? | Alguma das 2 células passa | EXECUTADA | **REFUTADA** (maior `|t|` 1,20) |
| DD-H04 | O corpo ou a posição do fechamento de ontem prevê o dia de hoje? | Alguma das 2 células passa | EXECUTADA | **REFUTADA** pela regra congelada (`|t|` 2,61 < 3); quase-acerto, ver nota |
| DD-H05 | O dia seguinte reverte a posição do fechamento de ontem na faixa do dia (fechamento perto da máxima, o dia seguinte tende a cair; perto da mínima, a subir)? | **Só dado novo, nunca os 2014–2025 já vistos.** Confirma se, em WINFUT D1 anterior a 2014 **ou** em 2026 líquido, o excedente médio da célula "posição do fechamento de ontem" (definição idêntica à do DD-H04) tiver sinal **negativo** com `|t| ≥ 2` (ou, em 2026, sinal negativo e margem sobre o custo ≥ 2). Refuta se o sinal for positivo ou `|t| < 1` com `n ≥ 500` | PENDENTE | — |

## Notas

- **Resultado da ANALISE_001:** 0 de 10 células passam `|t| ≥ 3` na descoberta; o maior `|t|` é 2,61. A regra não foi relaxada.
- **Quase-acerto (DD-H04):** a posição do fechamento de ontem tem excedente de −12,9 pb por dia na descoberta (t −2,61, n 738) e −11,7 pb no hold-out (t −2,44), −8,3 pb no WDO (t −3,40), 9 de 12 anos com o mesmo sinal e margem 30,9 sobre o custo. Os anos de 2022 e 2023 têm sinal oposto, então não é estável. Foi uma de 10 células; a chance de ver ao menos uma com `|t| ≥ 2,4` nos dois períodos por acaso não é pequena. Por isso o DD-H05 só aceita dado que não entrou em nenhum teste.
- **DD-H05 foi congelada em 2026-10-22, antes de qualquer dado novo ser testado.** Rodar `codigo/analise_001.py` com o WINFUT D1 de antes de 2014 ou de 2026 acrescenta a coluna do ano, sem mexer nos vereditos acima.
