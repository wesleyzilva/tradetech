# Método da TeseFma_areas

## 1. Objetivo mensurável

Medir se a coincidência de cores entre timeframes funciona como contexto de confirmação, sem usar este efeito para estimar entrada, SL, SG ou risco.

## 2. Entrada de dados

Os dados devem ser provenientes da série canônica em `TeseFma_analiseCandle`.

Campo obrigatório:

- `dt`
- `o`
- `h`
- `l`
- `c`
- `est`
- `fam`
- `z`
- `F`
- `rng`
- `atr`

As séries devem ser ordenadas por timestamp e sem duplicatas.

## 3. Taxonomia e definição de área

Toda medição deve registrar uma das quatro áreas canônicas:

| sigla | nome | construção |
|:---|:---|:---|
| ART | Área de Range Temporal | envelope da menor mínima e maior máxima dos candles incluídos na janela/cluster. |
| ACT | Área de Corpo Temporal | envelope do menor limite inferior e maior limite superior dos corpos open-close dos candles incluídos. |
| ARC | Área de Range do Candle | mínima–máxima de um único candle de referência. |
| ACC | Área de Corpo do Candle | abertura–fechamento de um único candle de referência, normalizados como menor–maior. |

Para ART/ACT, registrar a janela exata e quais candles participam do envelope. Para ARC/ACC, registrar o timestamp e timeframe do candle de referência. Não chamar uma faixa de “área temporal” se ela foi extraída de um único candle.

Para cada evento de referência:

1. identificar o candle ou cluster no timeframe maior;
2. obter sua família;
3. escolher ART, ACT, ARC ou ACC e calcular os limites conforme a tabela acima;
4. escolher os candles do timeframe menor **posteriores ao fechamento** do candle/cluster de referência, dentro da janela temporal e da faixa de preço da área;
5. comparar a família dos candles menores com a família do evento maior;
6. registrar a distância em candles e em pontos.

Uma faixa high-low de candle individual é ARC; uma faixa open-close de candle individual é ACC. Os envelopes high-low e open-close de vários candles dentro de uma janela são, respectivamente, ART e ACT. A definição escolhida precisa ser registrada antes da execução.

## 4. Definição de confirmação

Um evento é considerado confirmado quando:

- a família do timeframe maior é preservada no menor timeframe;
- o alinhamento ocorre dentro da área selecionada;
- a ocorrência é repetida em pelo menos um nível inferior;
- a confirmação tem uma definição temporal, como próximos N candles ou próximos N minutos.

A confirmação não deve reutilizar candles menores que formam simultaneamente o candle maior: isso é sobreposição/identidade temporal, não confirmação posterior. Os CSVs do Profit registram o início da barra; então, para evento maior aberto em $t$ com duração $T$, a janela de acompanhamento começa em $t+T$. A duração da janela de acompanhamento é especificada antes do cálculo. A distância, a família avaliada e o horário precisam ser registrados.

## 5. Eventos de interesse

### 5.1 Ignição

Candle com estado de família `+1` ou `-1`.

### 5.2 Saturação

Candle com estado de família `+2` ou `-2`.

### 5.3 Área de confirmação

Área delimitada por candle ou cluster no timeframe maior.

### 5.4 Área de controle

Janela aleatória do mesmo horário e largura, no mesmo período.

## 6. Métricas descritivas

- frequência de confirmação;
- taxa de confirmação por família;
- distância média em pontos;
- número de timeframes confirmados;
- persistência por N minutos ou N candles;
- duração da confirmação;
- proporção de sinais contrários;
- taxa de confirmação dentro da área;
- taxa de confirmação fora da área;
- taxa de confirmação em conjunto de controle.

## 7. Critérios de veredito

### 7.1 Confirmada

Uma condição de confirmação deve ser superior ao controle e ter significância estatística adequada, por exemplo $|t| \ge 3$.

### 7.2 Parcial

A confirmação supera o controle em alguns níveis ou períodos, mas não em todos.

### 7.3 Inconclusiva

O efeito tem magnitude ou variância insuficiente, ou a amostra é pequena.

### 7.4 Não suportada

O efeito não supera o controle ou não existe evidência empírica.

### 7.5 Refutada

O efeito oposto é estatisticamente mais forte ou consistente.

## 8. Controle e validação

- não usar os mesmos dados para selecionar e validar a hipótese;
- manter a definição de área fixa durante uma comparação;
- comparar com controles do mesmo horário e de mesma largura;
- registrar separadamente resultados positivos, negativos e inconclusivos;
- repetir a análise em pelo menos dois períodos guardados;
- testar apenas critérios previstos em Axx.

### 8.1 Controle lateral pareado inicial

Para o teste inicial de frequência A01/A03 usando **ARC**, pode-se usar um controle espacial local: manter o mesmo candle maior, horário, janela posterior ao seu fechamento e timeframe menor, e comparar a faixa de range `[l, h]` com faixas adjacentes de largura igual (`[l-w, l)` e `(h, h+w]`, onde `w = h-l`). Contar, por evento, se há pelo menos um candle menor da mesma família em cada região. Para ACT/ACC, usar a largura do corpo predefinido; para ART, fixar o intervalo temporal e seu envelope antes de construir o controle. Não reutilizar o controle ARC para outras geometrias sem ajustar os limites.

Só incluir eventos coloridos com faixa positiva e uma janela completa, com o número esperado de timestamps do timeframe menor; janelas parciais, lacunas e dados faltantes são reportados como incompletos, não tratados como ausência de sinal. As taxas da faixa inferior e superior ficam separadas, e sua média pode servir como comparação exploratória. Essa regra não controla sozinha a diferença de distribuição entre preços adjacentes, volatilidade, bordas/abertura de sessão ou dependência de eventos; portanto, não autoriza veredito de hipótese sem diagnóstico de suporte, pareamento por período/sessão e validação fora da amostra.

Este controle responde somente “a família do evento aparece mais na faixa original do que em faixas laterais igualmente largas, no mesmo intervalo observado?”. Não testa se o preço reverte, retoma ou se a área é suporte/resistência.

## 9. Artefatos esperados

- tabela de eventos de referência;
- tabela de confirmações;
- gráfico de cadeias de timeframes;
- gráfico de área do candle/cluster;
- gráfico de persistência após confirmação;
- gráfico de comparação com controle;
- tabelas de sinais contrários;
- arquivo de resultados reprodutível.

## 10. Separação de tópicos

| Estudo | Responsabilidade |
|:---|:---|
| TeseFma_areas | confirmação de área por múltiplos timeframes |
| TeseFma_reversao | sinais contrários e reversão |
| TeseFma_SL | seleção e comparação de SL |
| TeseFma_analiseCandle | motor, cores, famílias, clusters e validação canônica |

Nenhum resultado de área, reversão ou SL será promovido para operação sem passar por análise e validação separados.

### 10.1 Sinal contrário e reversão

Quando a área/evento de timeframe maior tem família $f$ e um candle colorido de timeframe menor **após o fechamento do maior**, na janela de confirmação e dentro da faixa de preço, tem família $-f$, registrar o candle menor como **sinal contrário (contrapressão futura)**. Famílias `+1/+2` e `-1/-2` são opostas por lado; família neutra `0` não é contrária.

Esse encontro não basta para chamar o evento de reversão. Pode ser contrapressão temporária, pausa, alternância de estado ou mudança persistente. A classificação do desfecho requer medir o comportamento posterior do preço sob uma regra temporal e de preço previamente fixada, além de compará-lo com controles; essa análise será feita na TeseFma_reversao (R01), não neste módulo de área.
