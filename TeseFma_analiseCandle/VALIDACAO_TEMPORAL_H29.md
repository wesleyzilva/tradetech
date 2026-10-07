# H29 — validação temporal da hipótese de absorção

_Gerado por `validar_h29_temporal.py`. Universo comum WIN: 2024-06-19 a 2026-05-14. Parser, features e cálculo de F vêm de `analise_candles.py`; critério de H29 vem de `validacao_econofisica.medir_h29()`._

## Desenho preservado

- Evento canônico: `a ≥ 2` e `|m| < 0.3`; horizonte = próximo candle da mesma sessão.
- Regra original de H29: razão média range/ATR do evento para controle ≥1.50 e |t_exp|≥3; não se interpreta retorno como direção.
- Corte temporal pré-fixado para este anexo: treino 2024-06-19 a 2025-06-18; holdout 2025-06-19 a 2026-05-14.
- Não há busca de limiar ou edição da definição após observar o holdout. Trata-se de robustez temporal de H29, não de nova hipótese.

| TF | Bloco | Candles | Pregões | Eventos H29 | Expansão evento | Expansão controle | Razão | t_exp Welch | Critério H29 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 5min | treino | 28142 | 250 | 571 | 1.544 | 0.990 | 1.560 | 15.935 | passa |
| 5min | holdout | 22631 | 223 | 554 | 1.637 | 1.010 | 1.620 | 8.484 | passa |
| 15min | treino | 9482 | 250 | 376 | 1.684 | 0.968 | 1.739 | 19.688 | passa |
| 15min | holdout | 7883 | 223 | 376 | 1.777 | 0.965 | 1.840 | 16.198 | passa |

## Sensibilidade: efeito pareado por pregão

Para controlar a sazonalidade horária e a dependência intrassessão, em cada estrato pregão×hora com ≥1 evento e ≥2 controles calcula-se a diferença entre expansão média do evento e dos controles. Os estratos são agregados a uma diferença por pregão, ponderando pelo número de eventos H29; IC percentil bootstrap por pregão (3000 réplicas, semente 20261006). Esta é sensibilidade, não altera a regra histórica de H29.

| TF | Bloco | Pregões elegíveis | Δ range/ATR pareado | IC95% bootstrap | t sobre diferenças diárias |
|---|---|---:|---:|---:|---:|
| 5min | treino | 227 | 0.185 | [0.113, 0.261] | 4.816 |
| 5min | holdout | 198 | 0.346 | [0.125, 0.657] | 2.488 |
| 15min | treino | 194 | 0.033 | [-0.058, 0.125] | 0.670 |
| 15min | holdout | 177 | 0.098 | [-0.020, 0.217] | 1.599 |

## Interpretação

O critério original H29 (Welch candle a candle, razão ≥1.50 e |t|≥3) passa em treino e holdout para 5min e 15min. A sensibilidade mais estrita, com controles da mesma hora e erro agregado por pregão, tem IC95% acima de zero nos dois blocos do 5min; nos dois blocos do 15min os IC95% incluem zero. Portanto, a robustez temporal do efeito intradiário é mais convincente no 5min; no 15min, a incerteza por pregão não sustenta o mesmo grau de estabilidade. Nenhum desses resultados prova direção, causalidade ou resultado operacional.

## Limitações estatísticas importantes

- O t de decisão original é o Welch existente em H29 e trata candles de evento/controle como observações independentes. A tabela de sensibilidade agrega em pregão e controla a hora para reduzir esse problema; é evidência complementar e mais conservadora, não substitui nem reescreve o critério histórico.
- O holdout preserva o corte cronológico e a regra fixa, mas os dados de treino e holdout pertencem ao mesmo ativo e a regimes de mercado temporalmente próximos; não equivale a replicação externa independente.
- A sensibilidade por pregão×hora é complementar ao Welch histórico, que continua sendo o único critério de aprovação de H29. O pareamento reduz diferenças horárias e dependência intrassessão, mas não torna independentes pregões próximos nem corrige por todos os testes da tese.
- Para 5min, o acervo canônico disponível não cobre 2020–2023; o split comum aqui começa em 2024-06-19.
