# Trilha do robô

Onde cada análise entra na construção do robô, e como tratar os dados de 2026. O registro completo está em [`04_REGISTRO_ANALISES.md`](04_REGISTRO_ANALISES.md).

## O que os dados autorizam hoje

Não há gatilho de entrada com probabilidade a favor do lado. A configuração mais próxima de um robô, com o que já foi testado, é um **alarme de volatilidade** mais uma **saída ainda em aberto**.

| Peça | Decisão | No robô |
|---|---|---|
| Barra brilhante como alarme de amplitude (H20, M01-IGN) | USAR | som e cor para chamar atenção; o próximo candle tende a ter range maior |
| Cor, ignição ou saturação para escolher o lado | NAO_USAR | vale em um timeframe só e em vários; vale com Bollinger e com limiar 60/80 (M16-A001, M16-A002) |
| Confluência de timeframes como confirmação | NAO_USAR | é mais rara e não é mais direcional que um timeframe só |
| Robô M02 em 1 min, do jeito que está | NAO_USAR | opera demais, o custo come o ATR, e a execução deixa a entrada sem proteção |
| Stop a mercado no lugar do stop-limite | USAR como execução | tira a armadilha do stop passivo (`DELTA_001`). Não cria vantagem |
| Stop curto e alvo longo em 30–60 min | CONDICIONAL | a geometria sozinha teve esperança no WIN antigo e não replicou no WDO nem depois de 2019 (M02-A002). Fica em aberto, sem virar parâmetro |
| Backtests do semáforo no Profit | FORA_DO_PROTOCOLO | janela curta, sem hold-out. Não entram na conta |

Enquanto a linha de direção estiver em NAO_USAR, o robô não tem entrada automática. O alarme avisa que o mercado vai andar; o lado continua sendo uma decisão sem evidência.

## Ordem para chegar num robô com risco/retorno

Cada passo mexe numa alavanca só, no formato de delta (`docs/01_CONVENCOES.md` §6).

1. **Ano foco.** Manter o retrato de 2026 atualizado (`docs/ano_foco/2026/RETRATO.md`). Serve para ver se o ano se parece com 2020-2025. Não nasce parâmetro aqui.
2. **Dimensionar a saída pela volatilidade prevista** (candidato M05 do catálogo). É a única peça com evidência (a amplitude é previsível) e é o que muda o risco/retorno de verdade: stop e alvo em função do range esperado, não um múltiplo fixo.
3. **Custo real de execução** (candidato M15). Sem slippage medido, um retorno de poucos pontos por trade não é operável.
4. **Um gatilho de lado novo**, só depois dos dois anteriores, com hipótese congelada e com 2026 como confirmação, não como lugar onde a regra foi escolhida.

### Leitura do retrato atual (dados até julho de 2026)

- 2026 teve mais barras brilhantes: 3% a 5% em 30 e 60 min, contra cerca de 1,4% em 2020-2025. No M26 de 5 min o ATR mediano foi 224 pts, contra 158 em 2024-2025.
- A cor continua sem lado. O acerto fica entre 45% e 52% nos dois contratos, e o sinal do M26 não se repete no Q26.
- O alarme de volatilidade em 5 min, que em 2024-2025 tem t = 4,6, ainda não aparece nos cerca de 90 pregões de 2026 (t ≤ 0,9).

## Ano foco: 2026

2026 é o ano para **entender o comportamento**, não para escolher o melhor parâmetro. Uma regra que só funciona em 2026 descreve o ano; ela não entra no robô.

| Papel da janela | O que pode sair dali |
|---|---|
| 2014-2019 e 2020-2025 | descoberta e primeira confirmação de uma regra |
| 2026 | retrato do ano e segunda confirmação de regra que já existia antes |
| Só 2026 | descrição do ano. Fica no retrato, com decisão PENDENTE, até aparecer em outro período |

### Quando chegar o export novo

1. Criar o lote `dados/candles/2026-atual/`, um CSV por série e timeframe, sem ajuste de preço e com a coluna `Quantidade`. Não editar os lotes que já existem.
2. Se for um contrato novo (por exemplo WINV26), acrescentar o nome em `SERIES_ANO` dentro de `ferramentas/bateria_ano_foco.py`.
3. Rodar `python ferramentas/auditar_candles.py` e depois `python ferramentas/bateria_ano_foco.py`.
4. Ler o retrato ao lado de 2020-2025. O que mudou no ano vira nota; o que se repete sustenta a peça que já estava em USAR.
5. Atualizar o registro se a leitura mudar uma decisão: uma linha em `docs/registro/analises.csv` e `python ferramentas/indexar_analises.py`.

## Como classificar uma análise nova

Uma linha no CSV, com uma classe e uma decisão:

| Classe | A análise responde | Vira, no robô |
|---|---|---|
| `direcao` | o sinal acerta o lado? | gatilho de entrada, ou a prova de que ele não existe |
| `volatilidade` | o sinal prevê o tamanho do movimento? | alarme e tamanho de stop/alvo |
| `geometria` | a saída, sozinha, tem esperança? | parâmetros de stop, alvo e tempo |
| `execucao` | a ordem é executada como se imagina? | tipo de ordem e custo |
| `descritiva` | com que frequência e com que forma isso acontece? | contexto; não vira parâmetro |
| `econofisica` | a estrutura física se sustenta? | dissertação e hipótese futura |
| `legado` | resultado anterior ao protocolo | nenhum |

Decisões: `USAR`, `NAO_USAR`, `CONDICIONAL`, `PENDENTE`, `FORA_DO_PROTOCOLO`. Mudou a regra ou o período, abre-se um id novo (`M16-A003`); o antigo fica no registro com o veredito que tinha.
