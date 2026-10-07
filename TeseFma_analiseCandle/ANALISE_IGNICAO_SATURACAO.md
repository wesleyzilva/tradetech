# WIN — análise descritiva de ignição e saturação Bollinger

_Gerado pelo script `analise_ignicao_saturacao.py`, usando `analise_candles.ler_csv()` e `analise_candles.calcular()`. Janela comum: 2024-06-19 a 2026-05-14. Limiares: ignição 1.5σ–<2.5σ; saturação ≥2.5σ._

## Método

- Escore direcional = `z × sign(F)`. A classe ignição usa [1.5, 2.5); saturação usa ≥2.5; o restante é controle/base.
- `F`, `m`, `a`, `μ`, `σ`, `z`, `est` e `fam` vêm diretamente de `analise_candles.py`; o estudo não implementa uma fórmula paralela nem altera a regra do motor.
- Retorno alinhado = `sign(F) × (fechamento futuro − fechamento do evento)`, em pontos.
- Expansão = `range/ATR` do candle futuro. O controle usa candles de outras classes na mesma sessão e na mesma hora, com média calculada por sessão.
- Efeitos e erros-padrão são calculados sobre a média diária dos eventos, não tratando cada candle como observação independente. Os valores t são descritivos, não decisão de hipótese nem correção para múltiplos testes.
- Somente horizontes que permanecem no mesmo dia entram nas métricas. Para montar WIN contínuo, cada CSV de contrato é calculado pelo motor; por dia, mantém-se a série de maior volume, com a prioridade das pastas canônicas em empates.

## Frequência e composição dos eventos

| TF | Classe | Candles | % da amostra | Dias com evento | Eventos/dia | mediana abs(m) | mediana a | mediana abs(F) | mediana z direcional |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5min | Ignição | 4761 | 9.38% | 465 | 10.07 | 0.733 | 1.291 | 91.60 | 1.80 |
| 5min | Saturação | 1349 | 2.66% | 461 | 2.85 | 0.771 | 3.307 | 219.92 | 3.05 |
| 15min | Ignição | 1647 | 9.48% | 455 | 3.48 | 0.678 | 1.876 | 109.09 | 1.87 |
| 15min | Saturação | 802 | 4.62% | 424 | 1.70 | 0.738 | 2.959 | 196.30 | 3.02 |

## Transição de ignição para saturação

Percentual de eventos de ignição cuja barra seguinte, dentro da mesma sessão, é saturação:

| TF | Ignições | Seguidas por saturação na próxima barra | Percentual |
|---|---:|---:|---:|
| 5min | 4761 | 201 | 4.22% |
| 15min | 1647 | 145 | 8.80% |

## O que acontece depois — evento versus controle por hora

`Δ` compara a média diária dos eventos com a média dos candles-controle da mesma sessão e hora. `t_dia` é o efeito médio dividido pelo erro-padrão entre dias.

| TF | Classe | h | Dias | Retorno alinhado (pts) | Δ retorno (pts) | t_dia retorno | range/ATR futuro | Δ range/ATR | t_dia range |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5min | Ignição | 1 | 465 | -2.2 | -3.8 ± 3.5 | -1.10 | 1.125 | -0.080 ± 0.073 | -1.09 |
| 5min | Ignição | 3 | 464 | 2.2 | -2.7 ± 6.1 | -0.43 | 1.029 | -0.046 ± 0.034 | -1.38 |
| 5min | Saturação | 1 | 458 | -2.1 | -7.7 ± 7.7 | -1.00 | 1.861 | 0.537 ± 0.059 | 9.18 |
| 5min | Saturação | 3 | 455 | -1.9 | -12.9 ± 11.3 | -1.14 | 1.372 | 0.154 ± 0.038 | 4.08 |
| 15min | Ignição | 1 | 454 | -6.0 | -15.4 ± 12.1 | -1.28 | 1.404 | -0.086 ± 0.032 | -2.67 |
| 15min | Ignição | 3 | 451 | -7.3 | -17.0 ± 19.8 | -0.86 | 1.302 | -0.004 ± 0.026 | -0.15 |
| 15min | Saturação | 1 | 420 | 9.7 | 12.1 ± 13.5 | 0.90 | 1.661 | -0.039 ± 0.038 | -1.02 |
| 15min | Saturação | 3 | 419 | 18.4 | 8.6 ± 22.6 | 0.38 | 1.466 | -0.176 ± 0.031 | -5.65 |

## Leitura atual

- **Saturação WIN 5min:** evento raro (2.66%); a expansão do próximo range/ATR é maior que o controle horário e o efeito diário continua marcado nos dois horizontes aqui medidos (t_dia 9.18 e 4.08). O retorno alinhado médio, porém, não supera claramente o controle quando a unidade de análise é o dia. Isso sustenta uma descrição de atividade/volatilidade, não de direção.
- **Ignição WIN 5min:** ocorre cerca de dez vezes por sessão nesta definição, mas as diferenças ajustadas por hora para retorno e expansão não mostram efeito diário claro nos horizontes testados.
- **WIN 15min:** a saturação mostra contraste de expansão mais fraco e dependente do horizonte; ignição tampouco mostra aumento claro de atividade. Não misturar estes resultados com o 5min.
- No candle imediatamente seguinte, ignição transita para saturação em 201 de 4761 eventos no 5min (4.22%); a tabela inclui também 15min. É uma taxa descritiva, não uma regra operacional.

## Limites e próximos testes do motor

1. Este é um recorte exploratório WIN 5min/15min; não é validação fora da amostra, não demonstra causalidade e não é análise de execução.
2. Sobreposição de eventos e dependência intrassessão ainda podem afetar as incertezas. Um próximo teste estatístico deve usar bootstrap por sessão ou blocos temporais e controle pareado pré-especificado.
3. Sensibilidade de limiar deve ser tratada como grade exploratória com correção por múltiplas comparações, ou como novas hipóteses congeladas antes do período de validação.
4. Sem alteração de limiares, o achado inicial mais nítido é: saturação 5min está associada a expansão futura do range; a interpretação direcional permanece sem suporte claro neste teste.
