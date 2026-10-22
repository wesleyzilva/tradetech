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
