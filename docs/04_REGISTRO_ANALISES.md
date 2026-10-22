# Registro de análises

> Gerado por `ferramentas/indexar_analises.py` a partir de `docs/registro/analises.csv`. Para incluir uma análise, acrescente uma linha no CSV e rode o script. Vocabulário e regras: `docs/01_CONVENCOES.md` §8. A decisão de cada peça no robô está em `docs/05_TRILHA_ROBO.md`.

## Contagem

| decisão | quantas |
|---|---|
| Entra no robô | 3 |
| Só entra com a ressalva registrada | 2 |
| Ainda não decide parâmetro | 2 |
| Fica fora do robô | 4 |
| Fora do protocolo (não usar como evidência) | 1 |

## Por decisão

### Entra no robô

| id | classe | análise | período | nota |
|---|---|---|---|---|
| M01-IGN | volatilidade | [`Ignição e saturação`](../motores/M01_fma_forca/teses/cores/ANALISE_IGNICAO_SATURACAO.md) | WIN 2024-06 a 2026-05 | Usar a barra brilhante como alarme de volatilidade. Não usar ignição nem saturação para escolher o lado. |
| M01-ESC | econofisica | [`Escalonamento esforço-deslocamento`](../motores/M01_fma_forca/teses/cores/ANALISE_ESCALONAMENTO_ECONOFISICO.md) | WIN 5 min, 2024-06 a 2026-05 | O corpo cresce com o volume relativo (beta cerca de 0,7) de forma estável. Descreve o candle |
| M17-A001 | volatilidade | [`Walk-forward 2018-2025: amplitude prevista e dimensionamento do stop`](../motores/M17_aprendizado_walkforward/analises/ANALISE_001_walkforward.md) | WIN e WDO, 30 e 60 min, 2014-2025 (teste 2018-2025) e 2026 líquido | O range seguinte é previsível além do HAR (5% a 9% da perda, 8 de 8 anos). O quantil 80% cobre 79% a 80%. WDO e cor não acrescentam. Candidato a dimensionar stop e alvo (M05) |

### Só entra com a ressalva registrada

| id | classe | análise | período | nota |
|---|---|---|---|---|
| M02-A002 | geometria | [`Risco/retorno por timeframe`](../motores/M02_microestrutura_barreiras/analises/ANALISE_002_timeframes_rr.md) | WIN e WDO, 5 a 60 min, 2014-2025 | A geometria de saída (stop curto, alvo longo) tem esperança positiva no WIN de 30 e 60 min mesmo com entrada aleatória. Não replica no WDO e o efeito some depois de 2019. Não vira parâmetro. |
| M17-A002 | direcao | [`Lado com walk-forward e teste final de 2026`](../motores/M17_aprendizado_walkforward/analises/ANALISE_002_2026.md) | WIN e WDO, 30 e 60 min, 2018-2025 e 2026 com só 47 pregões líquidos | Sinal fraco (AUC 0,51 a 0,525, z até 5,7, placebo ≤ 2,3) que decai de 0,56 em 2018 para 0,50 em 2025 e some com 1 pb de custo por trade. Em 2026 AUC 0,524 sem poder (z 0,83). Fica condicional a um export de 2026 mais longo |

### Ainda não decide parâmetro

| id | classe | análise | período | nota |
|---|---|---|---|---|
| M01-H27 | descritiva | [`Janela física de 100 minutos`](../motores/M01_fma_forca/teses/cores/H27_ANALISE.md) | WIN 5 a 60 min | Frequência de cor comparável entre timeframes |
| ANO-2026 | descritiva | [`Retrato do comportamento de 2026`](../docs/ano_foco/2026/RETRATO.md) | WINM26 até 2026-05 e WINQ26 até 2026-07, contra 2014-2019 e 2020-2025 | Estudo do ano. Não extrai parâmetro do robô. Corrigido: os contratos de 2026 tinham meses sem negociação (volume < 1 milhão por dia) e inflavam brilhantes e ATR |

### Fica fora do robô

| id | classe | análise | período | nota |
|---|---|---|---|---|
| M02-A001 | direcao | [`Baseline do robô de barreiras`](../motores/M02_microestrutura_barreiras/analises/ANALISE_001_baseline.md) | WIN 1 e 5 min, 2024-2026 parcial | Sem vantagem contra entrada aleatória. A execução é frágil: a barra de entrada fica sem proteção e o stop-limite vira ordem passiva. |
| M16-A001 | direcao | [`Confluência de cor com barras fechando juntas`](../motores/M16_confluencia_multitf/analises/ANALISE_001_confluencia.md) | WIN 2014-2026 e WDO, bases 5/15/30 min | 0 de 114 estratégias passam. A cor alinhada indica amplitude (MFE parecido com MAE), não o lado. |
| M16-A002 | direcao | [`Alinhamento no mesmo minuto, com limiares 60 e 80`](../motores/M16_confluencia_multitf/analises/ANALISE_002_alinhamento.md) | WIN 2014-2026 e WDO | O melhor caso (+50 pts até 2019) troca de sinal em 2020-2025. Limiar fixo e Bollinger contam a mesma história. |
| M16-A003 | direcao | [`Tabela fraco/forte cruzada no 5 e no 15 min`](../motores/M16_confluencia_multitf/analises/ANALISE_003_fraco_forte.md) | WIN 5 min desde 2024-06 e WDO | Nenhuma das 4 combinações do mesmo lado tem continuação. Fraco não continua e forte não reverte. |

### Fora do protocolo (não usar como evidência)

| id | classe | análise | período | nota |
|---|---|---|---|---|
| LEG-SEMAFORO | legado | [`Backtests do semáforo no Profit`](../motores/M01_fma_forca/robos/Results/) | janelas de poucos meses em 2026 | Resultados como +R$ 8 mil não seguem hipótese congelada nem hold-out. Ficam como histórico, fora da trilha do robô. |

Hipóteses ligadas a cada análise estão na coluna `hipoteses` do CSV e no [`INDICE_HIPOTESES.md`](INDICE_HIPOTESES.md).

