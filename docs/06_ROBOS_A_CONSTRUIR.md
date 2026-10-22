# Robôs a construir

Lista viva do que vale montar com o que os dados já sustentam, do que ainda não vale, e do que falta para mudar essa resposta. Quem decide o que entra é [`05_TRILHA_ROBO.md`](05_TRILHA_ROBO.md); aqui fica a anotação para construir depois.

Resposta curta: **não há robô de entrada que valha montar hoje.** Vale montar três peças que servem a qualquer robô futuro e não dependem de achar o lado.

## Vale montar

### R1. Assistente de risco do operador (alarme + stop e tamanho pela amplitude prevista)

| | |
|---|---|
| O que faz | Avisa (som e cor) quando a barra fecha brilhante; sugere distância de stop e alvo e o tamanho da posição para risco fixo em R$, a partir da amplitude prevista do próximo candle. A entrada continua sendo do operador. |
| Evidência | Amplitude é previsível além da linha de base de volatilidade: ganho de 5% a 9% (M17-A001, ML-H01), 8 de 8 anos, WIN e WDO; 12% em 2026 no modelo de 30 min com árvores. Alarme de barra brilhante: H20, H29 do M01. |
| O que ele **não** faz | Não cria esperança de lucro. Mantém o risco por trade constante e evita stop curto demais em dia de volatilidade alta (o piso de 35 pts do M02 era ruído em 1 min). A dispersão de `range ÷ previsto` é só 10% a 13% menor que a de `range ÷ ATR`. |
| Para construir | Modelo linear (Ridge, `S2`) tem coeficientes que cabem em NTSL; o de árvores não cabe e exige um serviço em Python. Limitar as razões de volume (`v_rel`, `q_rel`) ao intervalo visto no treino: o modelo linear extrapolou e errou em 2026 quando o volume do contrato saltou 300 vezes. |
| Antes de ligar | Medir se o stop e o alvo propostos reduzem a variância do resultado por trade na simulação do M02, num delta (`DELTA_###`), sem mudar o gatilho. |
| Status | pronto para virar delta do M02 |

### R2. Casca de execução (a parte do M02 que presta)

| | |
|---|---|
| O que faz | Gerencia a ordem depois que um gatilho qualquer manda entrar: stop a mercado, barra de entrada protegida, saída por tempo, zeragem no fim do pregão, limite de perda diária, chave de parada. |
| Evidência | M02-A001: a barra de entrada ficava sem proteção e o stop-limite virava ordem passiva (14% dos trades, −23 mil pts). `DELTA_001` já tem o stop a mercado no simulador. |
| Para construir | Reescrever o robô NTSL com o gatilho como módulo trocável, e conferir cada regra contra `mb_motor.py` (há testes). |
| Status | o gatilho atual (rompimento de fluxo neutro) fica de fora: não tem vantagem |

### R3. Modo sombra do modelo de lado (sem ordens)

| | |
|---|---|
| O que faz | A cada fechamento de 60 min, grava a probabilidade de alta do modelo `S2` (árvores) e depois o resultado. Não manda ordem. |
| Por quê | É o único jeito de ter dados fora da amostra que ninguém escolheu. O sinal de lado é fraco (AUC 0,52), decai (0,56 em 2018, 0,50 em 2025) e não confirmou em 2026 por falta de poder (47 pregões líquidos). |
| Regra de parada, fixada agora | Avaliar com pelo menos 250 pregões líquidos. Passa se AUC > 0,5 com `z ≥ 2` e esperança líquida > 0 com custo real medido (M15). Com menos que isso, nenhuma decisão. |
| Observação | Exportar o `WINFUT` de 2026 inteiro dá um teste imediato com ~130 pregões a mais, antes de esperar. |
| Status | barato; começar quando houver o export |

## Não vale montar (por enquanto)

| Ideia | Por quê |
|---|---|
| Robô de entrada pela cor (um ou vários timeframes, limiar 60/80, tabela fraco/forte) | O lado não se sustenta fora da descoberta em nenhum teste (M16-A001 a A003, M17: a cor não acrescenta nada ao lado) |
| M02 do jeito que está | Opera ~30 vezes por pregão, o custo come o ATR e não bate o acaso |
| Robô de lado com ordens reais pelo modelo de 60 min | Margem líquida da ordem do custo (1 pb zera), sinal decrescente, sem confirmação em 2026 |
| Lead-lag WIN × WDO (M06) | No M17 o WDO acrescentou ΔAUC ≈ 0 no lado e nada na amplitude em 30 e 60 min |

## O que pode virar candidato, em ordem de custo

O M17 mostrou de onde vem o pouco de lado que existe: no 60 min, `ret_dia`, `pos_dia` e a hora (o dia que subiu tende a continuar; a parte final do pregão sobe mais); no 30 min, reversão da barra anterior. Isso aponta para testes baratos, com 12 anos de dados:

1. **M07 + M04 juntos:** momentum da primeira hora para o resto do pregão e média por faixa de horário, com a grade declarada antes e a contagem de testes. É o que explica o sinal do M17 em termos que dá para operar.
2. **M03:** gap e rompimento da abertura.
3. **M15 (custo real):** é pré-requisito de qualquer robô intradiário. Precisa de um export de trades do Profit; sem ele, o custo usado (5 pts) é uma suposição.

Só depois de um desses mostrar vantagem fora da amostra com custo, abre-se um robô de entrada (R4), construído sobre a casca R2 e dimensionado por R1.

## Fila de análises até um robô de entrada

### Regra de "vale montar" (portão único)

Um candidato só vira robô se passar nos seis pontos, nesta ordem:

1. Esperança **líquida** de custo > 0 na descoberta, com `|t| ≥ 3` depois de contar todos os testes declarados.
2. Mesmo sinal e `|t| ≥ 2` no hold-out e no WDO (ou em outro período independente).
3. Supera o controle nulo (entrada aleatória com a mesma saída) e o placebo.
4. Margem líquida de pelo menos **2 vezes** o custo medido, para o slippage não zerar o resultado.
5. Estável em pelo menos 6 de cada 8 anos.
6. Confirmado em 2026 líquido (ou no modo sombra R3 com a regra de parada acima).

### Por que baixar a frequência

No M17 a margem do lado era da ordem do custo porque o modelo opera cerca de 8 vezes por pregão e ganha ~1 pb por trade. Um sinal de um trade por pregão, com movimento esperado de uns 100 pb, tem margem muitas vezes maior para o mesmo acerto. Com ~2.900 pregões, um acerto de **53%** já dá `z = 3`. Por isso a fila abaixo é toda de baixa frequência, e a decisão do M17 de ficar em 30 e 60 min não é o fim: é o ponto de partida para testar horizontes mais longos.

### Fila (cada passo declara a grade e conta os testes antes de rodar)

| # | Análise | Pergunta | Motor / prefixo | Dados | Depende de |
|---|---|---|---|---|---|
| 0 | Dados | Exportar `WINFUT` e `WDOFUT` de 2026 inteiro; história anterior a 2014; um export de trades do Profit | — | Profit | você |
| 1 | **FEITO (M18)** Estrutura intradiária (M07 + M04) | A direção da primeira hora (09:00–10:00) e do dia até 16:00 continua até o fim do pregão? A média por faixa de horário é estável entre anos? | novo, `ID` | WIN/WDO 30–60 min, 2014→2025 | nada |
| 2 | **FEITO (M18)** Abertura (M03) | O gap se preenche mais que o acaso? O rompimento da faixa de abertura continua até o meio-dia? | `OR` | WIN/WDO 30 min | nada |
| 3 | **FEITO (M19)** Diário (M08, M10, M14) | Retorno de k dias (5, 20), compressão de range (NR7) e semana de vencimento prevêem o dia ou a semana seguinte? | `TS`, `CP`, `VC` | D1/W1, 2014→2025 | nada; poder baixo, serve de triagem |
| 4 | M17 diário | Um modelo linear sobre o alvo "retorno de 10:00 a 17:00" com variáveis da primeira hora, gap, amplitude e regime ganha de 50% fora da amostra? | M17-A003 | WIN 30 min, 2.900 pregões | passos 1 a 3 (escolhem as variáveis) |
| 5 | Custo real (M15) | Qual o slippage por volatilidade e horário? | `EX` | export de trades | passo 0 |
| 6 | Modo sombra (R3) | O modelo de lado de 60 min se confirma fora da amostra? | M17 | ao vivo | passo 0 |

Os passos 1 a 3 foram executados (M18: 35 testes, M19: 10 testes) e nenhuma célula passou o portão. Resta um quase-acerto, o fade da posição do fechamento de ontem (DD-H05, pré-registrado), que só se confirma com dado novo: WINFUT D1 anterior a 2014 ou o ano de 2026. O passo 4 só roda depois deles para não escolher variável olhando o teste.

### Quando parar

- Os passos 1 a 4 somam, no máximo, cerca de 40 testes declarados. Aplica-se a correção de múltiplos testes sobre o conjunto.
- Se **nada** passar no portão: o veredito é "lado não extraível de candles com os dados atuais". Constroem-se só R1 e R2, e a investigação de lado fica parada até chegar dado novo (tick ou book, M18).
- Se **algo** passar: abre-se o robô de entrada (R4) sobre a casca R2, dimensionado por R1, com 2026 (ou o modo sombra) como confirmação.
