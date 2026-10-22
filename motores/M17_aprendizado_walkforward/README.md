# M17 — Aprendizado supervisionado com walk-forward (amplitude e lado)

| Campo | Valor |
|---|---|
| Status | ATIVO — ANALISE_001 e ANALISE_002 concluídas: **amplitude previsível; lado fraco, decrescente e sem confirmação em 2026** |
| Instrumentos / timeframes | WIN (decide) e WDO (replica); 30 e 60 min; horizontes de 1 e 2 barras |
| Tese | Um modelo mais flexível que uma regra de cor, validado com um protocolo que não deixa o acaso passar por achado, mostra o que é previsível nos candles e o que não é |
| Método | [`METODO.md`](METODO.md) · Hipóteses: [`HIPOTESES.md`](HIPOTESES.md) (ML-H01 a ML-H08) |
| Análises | [`ANALISE_001`](analises/ANALISE_001_walkforward.md) · [`ANALISE_002`](analises/ANALISE_002_2026.md) · [`DIAGNOSTICO_001`](analises/DIAGNOSTICO_001.md) |
| Código | `codigo/ml_motor.py` (variáveis, rótulos, modelos, walk-forward) · `analise_001.py` · `analise_002.py` · `diagnostico_001.py` |

## O que o protocolo tem que o resto do repositório não tinha

- Hipóteses, variáveis, modelos e hiperparâmetros fixados **antes** de rodar; nada é ajustado.
- Treino só no passado, teste em cada ano de 2018 a 2025, estatística por pregão (bootstrap por dia).
- **Placebo:** o mesmo pipeline sobre rótulos embaralhados diz que `z` o acaso entrega quando se roda 12 células por TF (máximo 2,3).
- Duas linhas de base de amplitude: média do slot (B0) e tipo HAR (B1). O modelo só conta se ganhar de B1.
- Um teste final (2026) em um disparo, só para o que passou.

## Resultado em uma tela

- **Amplitude (ML-H01, confirmada).** O modelo ganha de 5% a 9% da perda de B1 em 8 de 8 anos no WIN e no WDO; contra a média do slot, 25% a 32%. Em 2026 o modelo de 30 min com árvores ganha 12% (t = 5,8).
- **Dimensionar o stop (ML-H07, inconclusiva).** Cobertura do quantil 80% fica em 79% a 80% e a dispersão de `range ÷ previsto` é 10% a 13% menor que a de `range ÷ ATR` (9,5% em 60 min / h = 2). Em 2026 (47 pregões líquidos), 25% a 34% menor.
- **Lado (ML-H04, confirmada fraca; ML-H08, inconclusiva).** 20 de 24 células têm AUC entre 0,51 e 0,525 com `z ≥ 3` (placebo ≤ 2,3). Só uma cumpre o critério inteiro (60 min, h = 1, árvores): AUC 0,5208, esperança líquida +0,9 pb. O AUC vai de 0,56 em 2018 a 0,50 em 2025, 1 pb de custo por trade zera a esperança, e em 2026 dá 0,5238 sem poder para confirmar.
- **WDO e cor (ML-H02, H03, H05, H06, refutadas).** Acrescentar o outro ativo ou a cor do M01 não melhora amplitude nem lado.

## Dado que mudou o jeito de ler 2026

Os contratos `WINM26` e `WINQ26` têm meses sem negociação (centenas a poucos milhares de contratos por dia). `carregar_serie` passou a descartá-los (`docs/01_CONVENCOES.md` §3). Sobraram 47 pregões líquidos de 2026. Para testar o ano, falta exportar o `WINFUT` de 2026.

## Como rodar

```bash
python3 motores/M17_aprendizado_walkforward/codigo/analise_001.py     # ~15 min (inclui 20 repetições de placebo)
python3 motores/M17_aprendizado_walkforward/codigo/analise_002.py     # teste final de 2026
python3 motores/M17_aprendizado_walkforward/codigo/diagnostico_001.py # empates, variáveis, sensibilidade ao custo
```

Depende de `scikit-learn` e `scipy` (`requirements.txt`).
