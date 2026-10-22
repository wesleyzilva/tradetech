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

**Correção de dados.** A primeira versão do retrato mostrava 2026 com mais barras brilhantes e ATR maior. Era um efeito dos contratos fora do vencimento líquido: `WINM26` fez 68 a 17 mil contratos por dia de janeiro a março e `WINQ26` no máximo 17 mil até maio, contra 7 a 18 milhões nos meses líquidos. Com só os pregões líquidos, o retrato fica assim:

- O ano tem **pouca coisa para comparar**: 17 a 20 pregões do WINM26 (15/04 a 14/05) e 25 a 28 do WINQ26 (a partir de 17/06). Faltam 2026-01 a 2026-04-14 e 2026-05-15 a 2026-06-16, que são os contratos `WING26` e `WINJ26`, e o WINM26 depois de 14/05. Para o ano inteiro, o caminho é exportar o `WINFUT` de 2026.
- Barras brilhantes e ATR ficam na faixa de 2020-2025 (por exemplo, 30 min: 1,5% e 2,8% contra 1,4%; ATR 582 e 538 pts contra 573).
- A cor continua sem lado: acerto entre 47% e 55% e |t| ≤ 1 na maior parte; o 60 min do Q26 mostra 67% de acerto com t = 2,1 em 25 pregões, o que é um número de amostra pequena e não vira regra.
- O alarme de amplitude em 5 min (t = 4,6 em 2024-2025) aparece de novo no M26 (1,17, t = 2,3) e mais fraco no Q26 (1,09, t = 1,3).

### O que o M17 acrescenta (walk-forward 2018–2025)

- **Amplitude é previsível e dá para dimensionar a saída.** Um modelo de estrutura (retornos, ATR, volume relativo, hora, gap) ganha de 5% a 9% da perda de uma linha de base de volatilidade tipo HAR, em 8 de 8 anos no WIN e também no WDO. O quantil 80% do range previsto cobre 79% a 80% dos casos; a dispersão de `range ÷ previsto` é 10% a 13% menor que a de `range ÷ ATR`. Em 2026 (47 pregões líquidos) o modelo de 30 min com árvores repete o ganho (12%, t = 5,8). **Entra na saída do robô** (stop e alvo em função do range previsto) como candidato M05.
- **O lado tem um sinal fraco e que decai.** AUC entre 0,51 e 0,525 em 20 de 24 células, contra um placebo que não passa de 2,3 em `z`. Mas a esperança líquida é de até +0,9 pb por trade (cerca de 14 pts) em 60 min, 1 pb de custo por trade a zera, o AUC cai de 0,56 em 2018 para 0,50 em 2025, e em 2026 não confirma (AUC 0,524, `z` = 0,83, sem poder). **Não entra no robô.** Fica CONDICIONAL a um export mais longo de 2026.
- **WDO e cor não acrescentam nada** (ML-H02, H03, H05, H06). O alarme de cor serve, como antes, para chamar atenção.

### O que o M18 e o M19 acrescentam (estrutura de um trade por dia)

- **M18 (intradiário, 35 testes):** nenhuma célula passa. Momentum do dia, dia da semana, gap e faixa de abertura não têm direção sustentada. A faixa 09:30 chega a t 3,45 e some no hold-out; o WDO tem sinal oposto.
- **M19 (diário e semanal, 10 testes):** nenhuma célula passa `|t| ≥ 3`. Momentum, NR7, inside bar e vencimento não têm direção. O quase-acerto é o fade da posição do fechamento de ontem (t −2,61 e −2,44, WDO −3,40, 9 de 12 anos), pré-registrado como DD-H05.
- **Consequência:** a trilha continua com R1 (assistente de risco) e R2 (casca de execução). O lado só entra se o DD-H05 se confirmar em dado novo (WINFUT D1 anterior a 2014 ou 2026 líquido). Cada motor gera tabela por ano, então 2026 entra como mais uma coluna.

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
