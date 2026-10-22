# DELTA_### — <título: o que muda, em uma linha>

| Campo | Valor |
|---|---|
| Motor | M## |
| Baseline | `ANALISE_###_*` / robô `vN` |
| Status | PROPOSTO \| CONGELADO \| EXECUTADO \| ADOTADO \| REJEITADO \| ADIADO |
| Hipóteses | `<PREFIXO>-H##` |
| Alavanca única | parâmetro/regra alterada (nome em `Params`) |
| Congelado em | AAAA-MM-DD (commit `abc1234`) |

## Motivação

Qual evidência (análise, linha de `HIPOTESES.md`, risco da revisão de código) motivou o delta.

## Mudança

Antes → depois, em termos de código NTSL **e** de `Params`/função do simulador. Nada além dessa alavanca muda.

```python
# exemplo: mb.com(Params(), protecao_na_barra_de_entrada=True)
```

## Medição (congelada antes de rodar)

- Conjuntos: os mesmos do baseline + hold-out (qual).
- Métrica primária: (ex.: PnL médio por trade com custo de 2 pts; percentil vs nulo).
- Métricas de salvaguarda: (ex.: pior trade, DD máx, trades/pregão).
- Critério de decisão: ADOTAR se …; REJEITAR se …; ADIAR se amostra insuficiente.
- Nº de variantes testadas: (se > 1, declarar todas).

## Resultado

Tabela antes × depois (gerada por script) e link para o relatório.

## Decisão

`ADOTADO` / `REJEITADO` / `ADIADO` + data + justificativa em 2–3 linhas.
Se adotado: nova versão do robô (`robo/<Nome>_v<N+1>_<data>.ntsl`), novo baseline (`ANALISE_###`), linha no `CHANGELOG.md` do motor.
