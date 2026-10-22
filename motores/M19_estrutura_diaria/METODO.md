# M19 — Método (congelado em 2026-10-22, antes de rodar)

Pergunta do motor: no horizonte de um dia a uma semana, a direção ou a amplitude do período seguinte depende do que veio antes (retorno recente, compressão, semana de vencimento, dia anterior)? Reúne os candidatos M08 (momentum/reversão diária), M10 (compressão) e M14 (vencimentos) do catálogo. Triagem de baixa frequência: o poder é baixo (≈ 1.500 dias por período), então um resultado nulo significa "não detectável", não "provadamente zero".

## Dados

WINFUT diário (`D1`), 2014-01-02 → 2025-12-30 (decide); WDOFUT (replica). O semanal é montado do diário (segunda a sexta): o `W1` do Profit só traz 521 semanas e deixa buracos em 2018–2019, descoberto na primeira execução; a primeira execução com o `W1` não mudou nenhum veredito. Lote padrão. Quando o `WINFUT` de 2026 existir, os anos novos entram como colunas nas tabelas por ano e não entram nos vereditos.

## Definições

Retorno em pb do preço de entrada. Entrada na abertura do período seguinte, saída no fechamento dele. Custo por trade: 0,4 pb. `ATR20(t)` = média do range (máxima − mínima) dos 20 pregões que terminam em `t`. Excedente = `lado × (retorno − média dos retornos de todos os períodos do mesmo intervalo de anos)`.

## Hipóteses e grade (10 testes, declarados)

| ID | Teste | Células |
|---|---|---|
| DD-H01 | **Momentum ou reversão.** Lado = sinal do retorno acumulado dos últimos `k` períodos (fechamento a fechamento). Entra na abertura seguinte e sai no fechamento. | diário k ∈ {5, 20} → pregão seguinte (2); semanal k ∈ {1, 4} → semana seguinte (2) |
| DD-H02 | **Compressão → expansão (amplitude).** Após NR7 (range do dia é o menor dos últimos 7) e após inside bar (máxima menor e mínima maior que as do dia anterior), `range(t+1) ÷ ATR20(t)` menos a média dessa razão em todos os dias do período. | NR7, inside bar (2) |
| DD-H03 | **Semana do vencimento.** Semana (segunda a sexta) que contém a quarta-feira mais próxima do dia 15 dos meses pares. Welch contra as demais semanas. | amplitude (`range ÷ ATR20(t−1)`) e retorno abertura→fechamento do dia (2) |
| DD-H04 | **Dia anterior.** Hoje, abertura→fechamento. (a) lado = sinal do corpo de ontem (C−O); (b) lado = +1 se o fechamento de ontem está nos 20% superiores do range de ontem, −1 se nos 20% inferiores, sem trade no meio. | (a), (b) (2) |

## Estatística e veredito

- Uma observação por período em cada célula; `t` = média ÷ erro-padrão (Welch em DD-H03). **Descoberta** 2014–2019, **hold-out** 2020–2025, **replicação** WDOFUT 2014–2025.
- Uma célula **passa** se: `|t| ≥ 3,0` na descoberta, mesmo sinal com `|t| ≥ 2` no hold-out, mesmo sinal no WDO, e mesmo sinal em pelo menos 8 dos 12 anos. Nas células com lado (DD-H01, DD-H04) também: excedente médio líquido de 0,4 pb > 0 nos dois períodos.
- Hipótese **CONFIRMADA** se alguma célula passa; **REFUTADA** se nenhuma tem `|t| ≥ 3` na descoberta ou se as que têm trocam de sinal; **INCONCLUSIVA** nos demais casos. Margem = excedente médio ÷ custo, informada nas células com lado.
