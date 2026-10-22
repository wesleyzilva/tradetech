# Índice único de hipóteses

> **Gerado por** `ferramentas/indexar_hipoteses.py` — não editar à mão. A fonte de cada veredito é o `HIPOTESES.md` do motor/tese (coluna *Fonte*). Para criar uma hipótese nova, ver `docs/01_CONVENCOES.md` §2 e `docs/templates/HIPOTESE.md`.

## Resumo

| motor / tese | hipóteses | CONFIRMADA | PARCIAL | INCONCLUSIVA | NÃO SUPORTADA | REFUTADA | PENDENTE |
|---|---|---|---|---|---|---|---|
| M01 · cores | 45 | 19 | 3 | 5 | 4 | 1 | 13 |
| M01 · áreas | 8 | 0 | 0 | 1 | 0 | 0 | 7 |
| M01 · reversão | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| M02 · microestrutura | 15 | 2 | 0 | 3 | 0 | 3 | 7 |
| M16 · confluência multi-TF | 11 | 0 | 0 | 2 | 0 | 7 | 2 |
| M17 · aprendizado walk-forward | 8 | 1 | 0 | 2 | 0 | 4 | 1 |

## M01 · cores

Fonte: [`motores/M01_fma_forca/teses/cores/HIPOTESES.md`](../motores/M01_fma_forca/teses/cores/HIPOTESES.md)

| id | grupo | hipótese | veredito |
|---|---|---|---|
| H01 | Modelo | k é cosmético: com limiares adaptativos o estado independe de k (F×k ⇒ mesmo z) | CONFIRMADA |
| H02 | Modelo | m e a são componentes distintos (não redundantes) | CONFIRMADA |
| H03 | Modelo | O esforço (a) produz deslocamento: corpo/ATR cresce com a (lei de impacto) | CONFIRMADA |
| H04 | Modelo | O cruzamento m×a prevê atividade futura melhor que m ou a isolados | PARCIAL |
| H05 | Modelo | A cor do candle extremo carrega direção (retorno h1 alinhado ≠ 0) | INCONCLUSIVA |
| H06 | Pareto→Bollinger | A regra 80/20 vale para \|F\|: os 20% maiores candles concentram ≥ 80% da energia Σ\|F\| | REFUTADA |
| H07 | Pareto→Bollinger | O limiar fixo 70 equivale ao percentil ~80 de \|F\| em todos os TFs (âncora Pareto) | CONFIRMADA |
| H08 | Pareto→Bollinger | A cauda de \|F\| segue lei de potência (Pareto) e não exponencial | PARCIAL |
| H09 | Pareto→Bollinger | Com 70/85 fixos a hierarquia ignição < saturação se inverte (≥85 é mais comum que 70–85) | CONFIRMADA |
| H10 | Pareto→Bollinger | Com Bollinger a hierarquia é preservada (brilhante é mais raro que escuro) | CONFIRMADA |
| H11 | Pareto→Bollinger | Bollinger desacopla a quantidade diária de cores do regime de volatilidade do dia (o limiar fixo não) | CONFIRMADA |
| H12 | Pareto→Bollinger | Bollinger distribui a cor ao longo do dia de forma mais uniforme que o limiar fixo | INCONCLUSIVA |
| H13 | Pareto→Bollinger | Remover a sazonalidade do volume (a sazonal) elimina a concentração de cor na abertura | CONFIRMADA |
| H14 | Pareto→Bollinger | A cauda de F é mais pesada que a normal: 2.5σ ocorre bem mais que o previsto por um Bollinger gaussiano | CONFIRMADA |
| H15 | Pareto→Bollinger | O candle atual dentro da janela de μ/σ mascara extremos (auto-inclusão) | CONFIRMADA |
| H16 | Pareto→Bollinger | Em frequência igual, Bollinger e Pareto fixo preveem a atividade seguinte com a mesma qualidade (a migração é estrutural, não preditiva) | CONFIRMADA |
| H17 | Sinais | Cor persiste: candle colorido é seguido de candle colorido acima do esperado para a hora | PARCIAL |
| H18 | Sinais | Escuro = continuação (o preço segue na direção da cor — "manter posição") | INCONCLUSIVA |
| H19 | Sinais | Brilhante = exaustão (reversão à média após o clímax) | NÃO SUPORTADA |
| H20 | Sinais | Brilhante antecipa expansão de volatilidade (alerta de atividade, não de direção) | CONFIRMADA |
| H21 | Sinais | Neutro = sem vantagem direcional (abstenção) | CONFIRMADA |
| H22 | Operação | A cor é rara o bastante para saltar aos olhos (saliência visual) | CONFIRMADA |
| H23 | Operação | A abertura (9h) concentra as cores acima do seu peso em candles | CONFIRMADA |
| H24 | Operação | A quantidade diária de cores não indica dia de tendência nem de alta volatilidade (orçamento de cor ~constante) | CONFIRMADA |
| H25 | Próxima teoria | Clusters de cor similar formam áreas (faixas de preço) com comportamento próprio (suporte/resistência, retorno às bordas) | PENDENTE |
| H26 | Janela física | Em uma janela fixa de 100 minutos, frequência e persistência de estados são comparáveis entre 5 min e 15 min | INCONCLUSIVA |
| H27 |  | σ robusto (MAD) com μ/σ sem o candle atual reduz o auto-mascaramento do brilhante | NÃO SUPORTADA |
| H28 |  | O volume sazonal substitui o a canônico sem perder o alerta de volatilidade | NÃO SUPORTADA |
| H29 | Absorção | A absorção (a ≥ 2 e \|m\| < 0.3) tem atividade e persistência próprias | CONFIRMADA |
| H30 | Distribuição de cores | Dias muito direcionais têm uma distribuição de cores diferente dos demais | NÃO SUPORTADA |
| H31 | Áreas por cluster | O preço retorna às bordas dos clusters em até N candles mais que janelas aleatórias do mesmo horário e largura | INCONCLUSIVA |
| H32 |  | Os vereditos H06–H20 se mantêm em 2020–2024, nos timeframes com cobertura suficiente | PENDENTE |
| H33 |  | Trocar \|F\| ≥ 70 por "colorido" no robô V16 não muda o resultado no simulador | PENDENTE |
| H34 |  | Entrada antecipada: com volume confiável, iniciar antes da ignição poderia capturar mais do range disponível, mesmo abaixo de 1,5σ? | PENDENTE |
| H35 |  | Entrada na ignição: iniciar operação quando cruza 1,5σ e permanecer até saturação em 2,5σ poderia aproveitar o trecho entre os dois níveis? | PENDENTE |
| H36 |  | Quantas oportunidades operacionais válidas por sessão o motor permite, sob regras de sinal e de não duplicação previamente definidas? | PENDENTE |
| H37 |  | Qual faixa de ganho/SG é compatível com a distribuição de deslocamento observada após uma oportunidade válida? | PENDENTE |
| H38 |  | Qual regra de posicionamento do SL deve ser comparada: abertura, fechamento, mínima/máxima do candle de sinal ou outra referência estrutura… | PENDENTE |
| H39 | Alarmes multi-TF | Alarms coincidentes em dois ou mais timeframes têm maior próximo range/retorno do que alarmes isolados | CONFIRMADA |
| H40 | Transições | A duração das transições de família é descrita por mediana e percentis, sem inferir causalidade ou direção | CONFIRMADA |
| H44 |  | A primeira cor após neutro carrega direção em algum horizonte? | PENDENTE |
| H45 |  | A expansão após saturação decai em quantas barras? | PENDENTE |
| H46 |  | Com esforço alto, absorção e impulso têm desfechos diferentes? | PENDENTE |
| H47 |  | A anatomia do candle (pavio superior/inferior) acrescenta informação descritiva além de est? | PENDENTE |
| H48 |  | Os achados descritivos se mantêm entre janelas e séries de contrato sem duplicar timestamps? | PENDENTE |

## M01 · áreas

Fonte: [`motores/M01_fma_forca/teses/areas/HIPOTESES.md`](../motores/M01_fma_forca/teses/areas/HIPOTESES.md)

| id | grupo | hipótese | veredito |
|---|---|---|---|
| A01 |  | A família de um candle maior reaparece em candles menores na ARC após o fechamento | INCONCLUSIVA |
| A02 |  | A cadeia de confirmações entre timeframes aumenta a persistência | PENDENTE |
| A03 |  | Uma área declarada (ART, ACT, ARC ou ACC) contém a família correspondente | PENDENTE |
| A04 |  | A confirmação reforça o contexto, mas não a direção | PENDENTE |
| A05 |  | A contrapressão futura de família oposta associa-se a menor persistência da família do evento maior | PENDENTE |
| A06 |  | Timeframe maior tem mais valor como contexto do que como sinal direto | PENDENTE |
| A07 |  | O cluster colorido concentra mais correntes de confirmação que um único candle | PENDENTE |
| A08 |  | A confirmação de área preserva a família no menor timeframe | PENDENTE |

## M01 · reversão

Fonte: [`motores/M01_fma_forca/teses/reversao/HIPOTESES.md`](../motores/M01_fma_forca/teses/reversao/HIPOTESES.md)

| id | grupo | hipótese | veredito |
|---|---|---|---|
| R01 |  | Contrapressão colorida de timeframe menor após o fechamento do evento maior e dentro de sua faixa de preço é seguida por reversão persisten… | PENDENTE |

## M02 · microestrutura

Fonte: [`motores/M02_microestrutura_barreiras/HIPOTESES.md`](../motores/M02_microestrutura_barreiras/HIPOTESES.md)

| id | grupo | hipótese | veredito |
|---|---|---|---|
| MB-H01 |  | Após barra brilhante, o retorno futuro é no sentido do fade (alta → cai; baixa → sobe)? | INCONCLUSIVA |
| MB-H02 |  | O rompimento em fluxo neutro (ctx 3) tem continuação direcional? | REFUTADA |
| MB-H03 |  | A geometria SL 0,5 × ATR (piso 35) / SG 2,5 × ATR (piso 120) tem esperança positiva com um sinal sem edge? | REFUTADA |
| MB-H04 |  | Com 2–5 pts de custo, o robô continua positivo? | REFUTADA |
| MB-H05 |  | O stop-limit com offset de 5 pts produz perdas acima do SL nominal (armadilha)? | CONFIRMADA |
| MB-H06 |  | Algumas horas têm esperança maior (janela de ouro vs tarde)? | PENDENTE |
| MB-H07 |  | Limitar a frequência (cooldown, teto diário) reduz o custo sem perder o sinal? | PENDENTE |
| MB-H08 |  | O resultado depende do regime de ATR (alto × baixo, ATR vs ATR de 5 dias)? | PENDENTE |
| MB-H09 |  | O conceito sobrevive em 5 min (ATR 5×, piso de stop irrelevante)? | INCONCLUSIVA |
| MB-H10 |  | A barreira de tempo de 20 barras ajuda? | PENDENTE |
| MB-H11 |  | A estimativa do ATR incluindo a barra atual mascara extremos (como M01-H15) e muda a classificação "brilhante"? | PENDENTE |
| MB-H12 |  | Paridade: a réplica (avaliação no fechamento, fill no open seguinte) reproduz o trade log do robô no simulador do Profit? | PENDENTE |
| MB-H13 |  | Em timeframes ≥ 30 min, a geometria SL curto/SG longo (≤ ~100 min) tem esperança positiva mesmo com entrada aleatória (efeito de autocorrel… | INCONCLUSIVA |
| MB-H14 |  | A barra brilhante (≥ 1,7 × ATR) antecipa expansão do range seguinte em todos os timeframes (cor como alarme)? | CONFIRMADA |
| MB-H15 |  | Em 20–60 min o sinal do M02 (ctx 1–3) supera a entrada aleatória com a mesma saída? | PENDENTE |

## M16 · confluência multi-TF

Fonte: [`motores/M16_confluencia_multitf/HIPOTESES.md`](../motores/M16_confluencia_multitf/HIPOTESES.md)

| id | grupo | hipótese | veredito |
|---|---|---|---|
| CF-H01 |  | A confluência (modo A) antecipa expansão de range maior do que cor em TF único? | INCONCLUSIVA |
| CF-H02 |  | A confluência tem direção (continuação ou fade)? | REFUTADA |
| CF-H03 |  | Quantos pontos se pode capturar? (descritivo) | PENDENTE |
| CF-H04 |  | Existe estratégia com barreira (continuação ou fade) com esperança líquida positiva? | REFUTADA |
| CF-H05 |  | A confluência é melhor que o TF único com a mesma estratégia? | INCONCLUSIVA |
| CF-H06 |  | O alerta é raro o suficiente para chamar atenção (≤ 3 por pregão no conjunto escolhido)? | PENDENTE |
| CF-H07 |  | O alinhamento simultâneo (barra do TF maior em formação incluída) tem direção? | REFUTADA |
| CF-H08 |  | O alinhamento supera a cor do TF maior sozinho? | REFUTADA |
| CF-H09 |  | Os limiares fixos 60/80 mudam o resultado em relação ao Bollinger? | REFUTADA |
| CF-H10 |  | Alguma combinação fraco/forte do mesmo lado tem continuação? | REFUTADA |
| CF-H11 |  | Fraco continua e forte reverte, no 5 min sozinho? | REFUTADA |

## M17 · aprendizado walk-forward

Fonte: [`motores/M17_aprendizado_walkforward/HIPOTESES.md`](../motores/M17_aprendizado_walkforward/HIPOTESES.md)

| id | grupo | hipótese | veredito |
|---|---|---|---|
| ML-H01 |  | A estrutura (S2) prevê a amplitude melhor que a linha de base HAR (B1)? | CONFIRMADA |
| ML-H02 |  | Acrescentar o WDO (S3 contra S2) melhora a amplitude do WIN? | REFUTADA |
| ML-H03 |  | Acrescentar a cor (S4 contra S2) melhora a amplitude? | REFUTADA |
| ML-H04 |  | A estrutura (S2) prevê o lado? | PENDENTE |
| ML-H05 |  | O WDO (S3) acrescenta informação de lado ao WIN? | REFUTADA |
| ML-H06 |  | A cor (S4) acrescenta informação de lado? | REFUTADA |
| ML-H07 |  | A amplitude prevista dimensiona o stop melhor que um ATR fixo? | INCONCLUSIVA |
| ML-H08 |  | Teste final em 2026 (um disparo) | INCONCLUSIVA |

