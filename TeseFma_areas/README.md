# TeseFma_areas — confirmação de áreas por múltiplos timeframes

## 1. Objetivo

Estudar se uma cor ou família de candle em um timeframe maior funciona como contexto de confirmação para os mesmos fenômenos em timeframes menores.

Esta tese **não define**:

- entrada;
- preço de entrada;
- stop loss;
- take profit;
- tamanho da posição;
- risco;
- direção operacional.

A tese também não presume que a cor maior seja causa da cor menor. Ela deve medir ocorrência, persistência, coerência e força de confirmação.

## 2. Escopo

### 2.1 Timeframes

- 5 min: análise detalhada;
- 15 min: confirmação de contexto;
- 20/30/60 min: comparação auxiliar, sem impor prioridade automática;
- 1D/1W: contexto macro, usado somente para observar tendência ou estrutura, não como gatilho operacional.

### 2.2 Eventos de estudo

- candle vermelho ou verde colorido;
- brilho ignição/saturação;
- cluster de cor similar;
- intervalo de um candle ou cluster;
- coincidência de cor entre timeframes;
- sequência de confirmações por nível de timeframe.

## 3. Definições canônicas

### 3.1 Cor e família

A família vem do estado econofísico:

- `+1`: verde claro/ignição;
- `+2`: verde brilhante/saturação;
- `-1`: vermelho claro/ignição;
- `-2`: vermelho brilhante/saturação;
- `0`: neutro.

Uma família é o lado da cor, não a direção operacional.

### 3.2 Cluster

Um cluster é uma sequência consecutiva de candles da mesma família, tolerando até um neutro entre eles.

O cluster possui:

- família;
- quantidade de candles;
- número de candles do intervalo;
- abertura do primeiro candle;
- fechamento do último candle;
- faixa mínima e máxima;
- amplitude em pontos;
- amplitude em ATR;
- presença de brilho.

A área do cluster é a faixa entre o menor low e o maior high dentro do cluster.

### 3.3 Tipos canônicos de área

- **ART — Área de Range Temporal:** envelope mínima–máxima de todos os candles de uma janela ou cluster.
- **ACT — Área de Corpo Temporal:** envelope dos corpos abertura–fechamento dos candles de uma janela ou cluster.
- **ARC — Área de Range do Candle:** mínima–máxima de um candle individual de referência.
- **ACC — Área de Corpo do Candle:** abertura–fechamento do corpo de um candle individual, com limites ordenados.

ART/ACT são construídas ao longo do tempo; ARC/ACC pertencem a um único candle. Registrar sigla, timeframe, janela/candle de origem e limites antes do teste. As variantes devem ser medidas separadamente, sem trocar de definição após ver os dados.

### 3.4 Confirmação de área

A confirmação é um evento descritivo definido por:

1. uma cor ou evento de maior timeframe;
2. um ou mais eventos correspondentes no timeframe imediatamente inferior;
3. preservação da família ou da direção indicada;
4. ocorrência em dentro ou próximo da área do candle/cluster;
5. comparação com uma janela de controle do mesmo horário e tamanho.

A presença de confirmação não significa que o movimento continuará. A medição preliminar já registrada utilizou a faixa mínima–máxima de um único candle maior, isto é, **ARC**; ela não mediu ART, ACT ou ACC.

**Regra temporal:** os CSVs do Profit usam timestamp de abertura da barra. Para evitar contar barras menores que já formam o candle de referência, uma confirmação posterior começa somente após o fechamento desse candle. A apuração antiga da mesma hora do candle maior é simultânea/constitutiva e fica apenas como diagnóstico, não evidência de A01.

## 4. Estado da análise original

### 4.1 H31 — clusters

H31 mede se o preço retorna às bordas dos clusters mais que janelas aleatórias comparáveis.

Resultado atual:

- 5 min: 87.1% vs 95.0%, com $t=-8.21$;
- 15 min: 92.9% vs 95.1%, com $t=-3.54$.

Conclusão atual: H31 não suporta a teoria de que o cluster seja uma área forte de suporte/resistência ou um ponto de entrada. O resultado permanece apenas como descrição do comportamento dos clusters.

### 4.2 H39 — alarmes coincidentes

H39 mede diferenças de range/ATR e retorno entre alarmes coincidentes e isolados.

Resultado atual:

- range/ATR: 1.89 vs 1.29;
- retorno: 39.49 vs -9.04;
- significância: $t=+14.53$ e $t=+6.89$.

Conclusão: H39 confirma maior atividade futura em eventos coincidentes. Não confirma direção, entrada, SL, SG ou qualidade operacional.

### 4.3 H41–H43

Estas hipóteses permanecem futuras e operacionais:

- H41: entrada pela área do candle;
- H42: SL pela área do candle;
- H43: SG pela distribuição de deslocamento.

Nenhuma daquelas hipóteses deve ser simulada nesta pasta antes da conclusão de A01–A05.

## 5. Ordem de trabalho

1. Registrados exemplos visuais e dados de referência.
2. Definir área de candle e área de cluster.
3. Medir frequência de confirmação entre timeframes.
4. Medir persistência após a confirmação.
5. Comparar com janelas aleatórias.
6. Separar confirmação de cor, confirmação de nível e confirmação de direção.
7. Avaliar reversões em TeseFma_reversao, sem misturar com áreas.
8. Avaliar SL em TeseFma_SL, sem misturar com áreas.
9. Somente depois, decidir se existe uma hipótese operacional.

Próximo teste quantitativo de A01/A03: usar a hora seguinte completa ao fechamento do evento maior, controlar pela janela temporal idêntica e comparar a área de preço com faixas laterais da mesma largura; exigir cobertura intraintervalo completa. A comparação permanece espacial/descritiva e não classifica reversão.

Um sinal colorido de família oposta no timeframe menor, ainda que apareça dentro da faixa de preço da área maior, é registrado aqui como **contrapressão**. Não é sinônimo de reversão. A área pode medir a associação entre contrapressão e persistência da família (A05); o desfecho “reversão versus retomada” pertence à hipótese R01 da tese independente [TeseFma_reversao](../TeseFma_reversao/README.md).

## 6. Preservação da originalidade

O motor original e os cálculos de F, m, a, z, cores, famílias e estados continuam preservados na pasta `TeseFma_analiseCandle`.

A nova pasta deve manter o modelo as-is e adicionar somente:

- medições de organização entre timeframes;
- gráficos e exemplos;
- testes determinísticos;
- registro de hipóteses da área.

## 7. Arquivos deste escopo

- `README.md`: mapa desta tese;
- `HIPOTESES.md`: registro formal;
- `METODO.md`: definição de eventos e cálculo;
- `ANALISE_AREA.md`: exemplos e observações;
- `analise_areas.py`: implementação experimental;
- `test_analise_areas.py`: testes determinísticos;
- [TeseFma_reversao](../TeseFma_reversao/README.md): estudo separado do desfecho de sinais contrários;
- `exemplos/`: prints e imagens do usuário;
- `resultados/`: saídas numéricas e gráficos;
- `registros/`: anotações e versões de decisão.

## 8. Regras do estudo

- Não criar regra de entrada nesta pasta.
- Não calcular SL ou SG nesta pasta.
- Não usar resultado futuro para definir área.
- Todo exemplo deve incluir data, ativo, timeframes e limite da área.
- Cada hipótese deve ter critério antes do teste.
- Ao encontrar uma correlação, separar efeito de direção.
- Sinais opostos são registrados como contrapressão; o desfecho de reversão é testado separadamente em [TeseFma_reversao](../TeseFma_reversao/README.md).
- A conclusão pode ser descritiva mesmo que a hipótese não seja operacional.
