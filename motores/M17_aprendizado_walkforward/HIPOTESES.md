# M17 — Hipóteses (ML-H##) — **congeladas em 2026-10-22, antes de rodar**

Regras e definições: [`METODO.md`](METODO.md). Veredito padrão: `docs/01_CONVENCOES.md` §2.
Total de células declarado: **96** (24 de amplitude e 24 de lado, em WIN e em WDO). Limiar de lado ajustado a isso: `z ≥ 3,0` (p unilateral ≈ 0,0013).

| ID | Pergunta | Critério de veredito (congelado) | Status | Veredito |
|---|---|---|---|---|
| ML-H01 | A estrutura (S2) prevê a **amplitude** melhor que a linha de base HAR (B1)? | Em alguma célula do WIN: ganho de perda quadrática sobre B1 > 0 com t por pregão ≥ 3, positivo em ≥ 6 dos 8 anos de teste e positivo no WDO | PENDENTE | — |
| ML-H02 | Acrescentar o WDO (S3 contra S2) melhora a amplitude do WIN? | Diferença de perda S2 − S3 > 0 com t ≥ 3 em alguma célula e positiva em ≥ 6 de 8 anos | PENDENTE | — |
| ML-H03 | Acrescentar a cor (S4 contra S2) melhora a amplitude? | Idem ML-H02 com S4 | PENDENTE | — |
| ML-H04 | A estrutura (S2) prevê o **lado**? | Em alguma célula do WIN: AUC fora da amostra > 0,5 com `z ≥ 3,0`, AUC > 0,5 em ≥ 6 de 8 anos, esperança líquida (custo 0,4 pb) > 0 com t por pregão ≥ 2, `z` observado acima do maior `z` dos 10 placebos e AUC > 0,5 no WDO | PENDENTE | — |
| ML-H05 | O WDO (S3) acrescenta informação de lado ao WIN? | Mesmo critério de ML-H04 em S3, e AUC(S3) − AUC(S2) > 0 com `z ≥ 3,0` | PENDENTE | — |
| ML-H06 | A cor (S4) acrescenta informação de lado? | Mesmo critério de ML-H04 em S4, e AUC(S4) − AUC(S2) > 0 com `z ≥ 3,0` | PENDENTE | — |
| ML-H07 | A amplitude prevista dimensiona o stop melhor que um ATR fixo? | Regra: usa o modelo de amplitude de S2 com menor perda em 2018–2021. Distância D = exp(previsto + quantil 80% dos resíduos do treino). (a) cobertura de `range ≤ D` entre 77% e 83% no agregado e entre 72% e 88% em cada ano; (b) coeficiente de variação de `range ÷ previsto` ≥ 10% menor que o de `range ÷ ATR` | PENDENTE | — |
| ML-H08 | Teste final em 2026 (um disparo) | Só entram aqui as células que cumpriram ML-H01 a ML-H07 em 2018–2025. Treina em 2014–2025 e testa em WINM26/WINQ26. Amplitude: ganho sobre B1 > 0. Lado: AUC > 0,5 com `z ≥ 1,65` | PENDENTE | — |

Regra: se nenhuma célula de lado satisfizer ML-H04 a ML-H06, o veredito do motor é "lado não extraível dos candles de 30 e 60 min com os dados atuais", e 2026 não é aberto para lado. Isso é resultado, não falha.
