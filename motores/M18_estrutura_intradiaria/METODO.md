# M18 — Método (congelado em 2026-10-22, antes de rodar)

Pergunta do motor: a estrutura do pregão (primeira hora, hora do dia, dia da semana, gap e faixa de abertura) tem direção que se sustenta entre períodos, com baixa frequência (um trade por pregão por teste), de modo que o custo importe pouco? Reúne os candidatos M03 (abertura), M04 (sazonalidade) e M07 (momentum da primeira hora) do catálogo.

## Dados

WINFUT 30 min, 2014-01-02 → 2025-12-30 (decide), WDOFUT 30 min (replica). Lote padrão. Só pregões com as 17 barras de 09:00 a 17:00 (abertura). Quando o `WINFUT` de 2026 for exportado, os anos novos entram sozinhos como colunas de "ano novo" nas tabelas por ano e **não** entram nos vereditos.

A série contínua não tem saltos de rolagem relevantes (os maiores gaps são eventos: março de 2020, eleições). Mantêm-se todos os pregões; como as caudas são pesadas, cada teste também reporta o acerto (fração de pregões a favor) e a mediana.

## Definições

Barra = 30 min, carimbo de abertura. `preço(HH:MM)` = abertura da barra HH:MM. Entrada sempre na abertura de uma barra, saída no fechamento de uma barra. Retorno em pontos básicos (pb) do preço de entrada. Custo por trade: 0,4 pb (equivale a 5 pts).

- `EOD` = fechamento da barra de 17:00 (17:30). `ATRd` = média do range diário (máxima − mínima) dos 20 pregões anteriores.

## Hipóteses e grade (35 testes, declarados)

| ID | Teste | Células |
|---|---|---|
| ID-H01 | **Momentum do dia.** Lado = sinal de `preço(O) − abertura do dia`. Entra em `O`, sai no `EOD`. | O ∈ {10:00, 14:00, 16:00} (3) |
| ID-H02 | **Sazonalidade por faixa.** Retorno de cada barra (abertura→fechamento) menos a média das 17 barras do mesmo dia. | 17 faixas (09:00 … 17:00) |
| ID-H03 | **Dia da semana.** Retorno do pregão (abertura 09:00 → `EOD`) de cada dia da semana menos o dos demais. | 5 dias |
| ID-H04 | **Gap.** Lado = −sinal do gap (abertura − fechamento anterior). Entra na abertura 09:00. | saída ∈ {10:00, 12:00, `EOD`} × subconjunto ∈ {todos, \|gap\| ≥ 0,5 ATRd} (6) |
| ID-H05 | **Faixa de abertura (OR).** OR = máxima e mínima das barras iniciais. O primeiro fechamento de barra, até as 11:00 (inclusive), fora da faixa define o lado; entra na abertura da barra seguinte; um trade por pregão. | OR ∈ {09:00–09:30, 09:00–10:00} × saída ∈ {12:00, `EOD`} (4) |

## Controle de deriva

Retornos de entradas com lado (ID-H01, H04, H05) usam o **excedente**: `lado × (retorno − média dos retornos do mesmo par entrada→saída em todos os pregões do período)`. Isso tira o ganho de estar sempre comprado quando o mercado sobe. ID-H02 e ID-H03 já são relativos por construção.

## Estatística e veredito

- Uma observação por pregão por célula. `t` = média ÷ erro-padrão entre pregões. ID-H03 usa Welch (dia contra demais).
- **Descoberta** = 2014–2019. **Hold-out** = 2020–2025. **Replicação** = WDOFUT 2014–2025.
- Uma célula **passa** se: `|t| ≥ 3,0` na descoberta (limiar de Bonferroni para 35 testes), mesmo sinal com `|t| ≥ 2` no hold-out, mesmo sinal no WDO, média líquida de 0,4 pb > 0 nos dois períodos (no sentido do sinal), e mesmo sinal em pelo menos 8 dos 12 anos.
- Uma hipótese é **CONFIRMADA** se alguma de suas células passa; **REFUTADA** se nenhuma tem `|t| ≥ 3` na descoberta ou se as que têm trocam de sinal no hold-out; **INCONCLUSIVA** nos demais casos.
- Além do veredito, cada célula mostra a margem = excedente médio ÷ custo (o portão de "vale montar" exige ≥ 2).
