# Leitura visual do motor FMA

> **Guia de interpretação do estado visual atual do motor.** Este documento descreve o que as cores significam matematicamente e como registrar uma possível primeira entrada para estudo. Não transforma a cor em recomendação operacional: entrada, SL e SG ainda precisam de teste próprio.

## 1. O que a cor representa

O motor calcula $F=m\cdot a\cdot100$, sua média móvel $\mu$, o desvio $\sigma$ e o escore $z=(F-\mu)/\sigma$. A cor só é atribuída quando o sinal de $F$ e o de $z$ estão alinhados. Verde representa família positiva; vermelho, família negativa; brilho diferencia o nível do estado, não a qualidade da operação.

| Estado | Cor visual | Condição no fechamento | Leitura estrita do motor |
|---|---|---|---|
| `VL` | 🟢 verde vivo | $F>0$ e $z\ge2.5$ | Família positiva, estado brilhante: desvio de força mais intenso. |
| `VD` | 🟩 verde escuro | $F>0$ e $1.5\le z<2.5$ | Família positiva, estado escuro: desvio de força acima do limiar de cor. |
| `N` | ⬜ branco | Nenhuma condição colorida satisfeita | Estado neutro/abstenção do motor; não indica compra ou venda. |
| `RD` | 🟥 vermelho escuro | $F<0$ e $-2.5<z\le-1.5$ | Família negativa, estado escuro: desvio de força negativa acima do limiar de cor. |
| `RV` | 🔴 vermelho vivo | $F<0$ e $z\le-2.5$ | Família negativa, estado brilhante: desvio de força negativa mais intenso. |

Os limites e símbolos seguem a implementação canônica em [analise_candles.py](analise_candles.py#L17) e [analise_candles.py](analise_candles.py#L52-L71). “Escuro”, “vivo” e “forte” descrevem a classificação; não significam, por si, continuação, reversão ou entrada validada.

## 2. Combinações de cores entre candles consecutivos

A seta descreve **estado anterior → estado recém-fechado**. A interpretação abaixo é visual/descritiva; não é regra automática de ordem.

| Combinação | O que mudou no motor | Como registrar visualmente por enquanto |
|---|---|---|
| ⬜ → 🟩 ou ⬜ → 🟢 | Surge estado positivo após estado neutro | **Primeiro candle positivo colorido:** marcar como possível candidato a compra para teste, não como entrada confirmada. 🟢 indica maior intensidade de estado que 🟩, não melhor preço de entrada. |
| ⬜ → 🟥 ou ⬜ → 🔴 | Surge estado negativo após estado neutro | **Primeiro candle negativo colorido:** marcar como possível candidato a venda para teste, não como entrada confirmada. 🔴 indica maior intensidade de estado que 🟥, não maior probabilidade de lucro. |
| 🟩 → 🟩 ou 🟥 → 🟥 | Mesma família e mesmo nível escuro | O estado colorido permanece; ainda não prova que o preço continuará na direção da cor. |
| 🟩 → 🟢 ou 🟥 → 🔴 | Mesma família, de escuro para brilhante | A classificação passou ao nível brilhante. Tratar como aumento do alerta de atividade, não como confirmação para entrar ou aumentar posição. |
| 🟢 → 🟩 ou 🔴 → 🟥 | Mesma família, de brilhante para escuro | A intensidade classificada diminuiu; não há regra de saída validada por essa mudança. |
| 🟢 → 🟢 ou 🔴 → 🔴 | Mesmo estado brilhante em candles consecutivos | Brilho repetido; não interpretar como exaustão ou continuação sem evidência adicional. |
| Qualquer verde → qualquer vermelho, ou vermelho → verde | Troca de família | Registrar como transição de família. Não chamar automaticamente de reversão nem abrir posição contrária. |
| Qualquer cor → ⬜ | O estado atual ficou neutro | O motor deixou de classificar o candle como colorido. Não equivale, por si só, a zeragem de uma posição. |
| ⬜ → ⬜ | Neutro permanece neutro | Sem novo estado colorido; leitura de abstenção. |

## 2.1 Uma cor ou duas: o que testar primeiro

**Não há hoje evidência para afirmar que uma cor ou duas cores sejam o melhor gatilho de entrada.** Uma cor é mais cedo, mas mais sujeita a ruído; duas cores da mesma família medem persistência, porém entram mais tarde. Os achados H17/H20 sustentam persistência/expansão de atividade em alguns recortes, não direção lucrativa.

| Variante de pesquisa | Evento objetivo | Momento simulado | O que responde |
|---|---|---|---|
| A — primeira cor | Após pelo menos 2 candles neutros consecutivos, fecha o primeiro estado colorido (`fam` +1 ou −1). | Próxima abertura, sem antecipar o fechamento. | O alerta mais cedo tem retorno futuro direcional líquido de custos ou apenas marca atividade? |
| B — confirmação de família | Depois do mesmo reset neutro, fecham 2 candles consecutivos coloridos da mesma família; escuro e vivo contam como a mesma família. | Próxima abertura após o segundo fechamento. | A persistência melhora os resultados o suficiente para compensar o atraso/preço pior? |
| C — mudança de intensidade | A família permanece igual e o estado passa de escuro a vivo (`|est|` de 1 para 2). | Só após o fechamento que confirma a mudança; entrada simulada na abertura seguinte, se essa regra for testada. | A intensidade acrescenta informação além da família, ou só avisa de maior atividade/range? |

Trate A, B e C como **variantes experimentais separadas**, definidas antes de olhar os resultados; não escolha retrospectivamente a que ficou mais bonita. Compare no mesmo conjunto de dias e sinais elegíveis, com custos/slippage, uma regra de stop/alvo previamente fixada e validação temporal fora da amostra. Registre uma entrada por evento/cluster para não contar candles consecutivos como oportunidades independentes. A regra de “2 neutros” é um reset operacional explícito para o experimento, não um limiar descoberto pelo motor.

**Resposta prática hoje:** se for preciso escolher o próximo teste, priorize A como alerta/candidato e B como controle de confirmação. Não opere A ou B em conta real com base apenas nesta leitura. O motor atual não demonstrou que a cor aponta a direção nem que uma espera de dois candles aumenta a expectativa líquida.

**Nota sobre “primeiro”:** para uma hipótese de entrada, definir previamente se é o primeiro candle colorido do pregão ou o primeiro após um estado neutro. A rotina de clusters do estudo pode unir candles da mesma família através de até um candle neutro; portanto, uma cor após uma pausa isolada pode pertencer ao mesmo cluster, não a uma oportunidade independente. Consulte a regra de clusters em [analise_candles.py](analise_candles.py#L125-L169).

## 3. Exemplo de observação no fechamento

1. A barra fecha e o estado final é 🟩 ou 🟢, depois de um estado ⬜: registrar **“candidato visual de compra”**. Para 🟥 ou 🔴, registrar **“candidato visual de venda”**.
2. Guardar horário, timeframe, OHLC, estado anterior/atual e valores de $F$, $z$ e ATR. A leitura visual fica vinculada ao fechamento da barra, não a uma cor que apareceu momentaneamente durante sua formação.
3. Em teste histórico sem antecipação, comparar uma execução definida previamente — por exemplo, próximo candle na abertura — e uma eventual regra de execução no fechamento apenas se ela for realizável e incluir custos. Não usar retrospectivamente máxima/mínima do candle já fechado como preço de entrada.
4. Medir o que ocorre depois (retorno, excursão favorável e adversa, range futuro e frequência de stop/alvo). Só então comparar possíveis regras de SL/SG.

Isto formaliza a visualização que se quer investigar: **o primeiro estado colorido pode marcar uma possível entrada**, mas não afirma que seja o momento mais apropriado. As hipóteses de entrada antecipada e entrada na ignição continuam pendentes de execução e validação em [HIPOTESES.md](HIPOTESES.md#L156-L180).

## 4. Evidência do motor disponível até agora

| Questão | Resultado registrado | Leitura permitida |
|---|---|---|
| A cor carrega direção? | H05 é inconclusiva; H18 (continuação no escuro) é inconclusiva; H19 (exaustão/reversão no brilhante) não é suportada. | Não usar a cor isolada para afirmar compra, venda, continuação ou reversão. |
| A cor tende a persistir? | H17: lift de cor seguinte ajustado por hora = 1.59 no 5min e 1.11 no 15min; resultado parcial. | Há evidência de persistência de **atividade colorida** mais forte no 5min, não de persistência direcional de cada cor. |
| O brilhante antecipa atividade? | H20: range do candle seguinte = 1.44× no 5min e 1.15× no 15min, com $t=+19.1$ e $+8.3$. | É o achado atual mais claro para alerta de expansão/risco, não para direção. |
| A primeira cor é uma entrada comprovada? | Não. H34–H35 seguem como testes operacionais propostos, ainda não testados. | “Candidato visual” é uma etiqueta para investigação, não sinal aprovado. |

Esses resultados e seus vereditos constam em [HIPOTESES.md](HIPOTESES.md#L25-L28) e [HIPOTESES.md](HIPOTESES.md#L156-L170). A análise específica de ignição/saturação também conclui que a leitura direcional não tem suporte claro em [ANALISE_IGNICAO_SATURACAO.md](ANALISE_IGNICAO_SATURACAO.md#L47-L59).

## 5. Limites antes de chamar de regra operacional

- O indicador passou por um smoke test visual no Profit, mas a paridade numérica Profit × Python ainda está pendente. Antes de tratar o gráfico como evidência final, comparar os mesmos timestamps e valores, conforme [PARIDADE_NTSL_PYTHON.md](PARIDADE_NTSL_PYTHON.md#L74-L96) e o status em [HIPOTESES.md](HIPOTESES.md#L192-L193).
- O estado usa os dados do candle atual; durante a formação da barra, OHLC, volume e $z$ podem mudar. Para uma regra “no fechamento”, congelar a decisão apenas quando a barra estiver completa.
- A tabela de combinações é uma **legenda descritiva**, não uma tabela de probabilidades por transição. As transições específicas 🟩→🟢, 🟢→🟩, troca de família e primeira cor ainda precisam ser quantificadas separadamente.
- O motor não produz por si só um SL/SG recomendado. Range/ATR podem servir como unidades para comparar alternativas, mas a escolha depende da distribuição de excursões após uma entrada precisamente definida, dos custos, da execução e de validação fora da amostra.

**Resumo visual:** verde = estado positivo; vermelho = estado negativo; escuro = faixa colorida inicial; vivo = faixa mais intensa; branco = neutro. A primeira cor após neutralidade é uma **possível entrada a estudar**. Nenhuma sequência de cores, isoladamente, foi validada como estratégia executável.
