# Hipóteses da TeseFma_areas

## 1. Convenção

- `Axx`: hipótese de área;
- veredito: `CONFIRMADA`, `PARCIAL`, `INCONCLUSIVA`, `NÃO SUPORTADA`, `REFUTADA`, `PENDENTE`;
- o veredito descreve a evidência do contexto;
- a hipótese operativa não é confirmada apenas porque a hipótese descreve uma coincidência;
- nenhum resultado desta tese define entrada, SL, SG, risco ou quantidade.

## 2. Registro atual

| id | hipótese | critério de decisão | status |
|:---|:---|:---|:---|
| A01 | A família de um candle maior reaparece em candles menores na ARC após o fechamento | frequência na ARC maior que em controle lateral pareado, com intervalo de confiança apropriado | INCONCLUSIVA — consulta anterior simultânea não é confirmação posterior |
| A02 | A cadeia de confirmações entre timeframes aumenta a persistência | persistência cresce com o número de níveis confirmados | PENDENTE |
| A03 | Uma área declarada (ART, ACT, ARC ou ACC) contém a família correspondente | frequência dentro do tipo de área pré-declarado excede controles espaciais pareados; controles incompletos não contam como ausência | PENDENTE |
| A04 | A confirmação reforça o contexto, mas não a direção | direção completa ou reversão não é inferida dos eventos | PENDENTE |
| A05 | A contrapressão futura de família oposta associa-se a menor persistência da família do evento maior | após o fechamento do candle maior, comparar persistência posterior com e sem candle menor colorido oposto dentro da faixa, sob controle temporal e de densidade | PENDENTE |
| A06 | Timeframe maior tem mais valor como contexto do que como sinal direto | comparação de valor preditivo dos vários níveis | PENDENTE |
| A07 | O cluster colorido concentra mais correntes de confirmação que um único candle | frequência de confirmação dentro do cluster vs. candle único | PENDENTE |
| A08 | A confirmação de área preserva a família no menor timeframe | instâncias da família são mais frequentes dentro da área | PENDENTE |

## 3. Fila de análise

1. A01 — presença de confirmação no menor timeframe.
2. A03 — localização da confirmação dentro da área.
3. A02 — efeito do número de timeframes confirmados.
4. A07 — comparação cluster vs. candle.
5. A08 — persistência da família na área.
6. A06 — valor relativo dos timeframes.
7. A04 — separação de contexto e direção.
8. A05 — relação entre contrapressão e persistência da família, sem classificar reversão.

## 4. Regras para adicionar hipótese

- Cada hipótese deve ter evento, critério, período, controle e definição de sucesso.
- Cada teste de área deve declarar ART, ACT, ARC ou ACC; mudanças de tipo são variantes separadas e não podem ser agrupadas no mesmo resultado.
- Se a definição mudar, deve ser criado outro id.
- O resultado de um exemplo não torna hipótese definitiva.
- O teste deve usar dados fora da seleção quando possível.
- Informação visual deve ser registrada sem transformar a imagem em métrica.
- A hipótese precisa ser descrita como contexto, não como cenário operacional.

## 5. Limites explícitos

- A existência de cores em vários timeframes não implica continuação.
- Cor maior não é automaticamente um gatilho de entrada.
- Confirmação não significa confirmação de direção.
- Uma família oposta no timeframe menor, mesmo dentro da área maior, é apenas sinal contrário/contrapressão; sozinha não confirma reversão.
- O teste de reversão versus retomada do preço pertence exclusivamente à [TeseFma_reversao](../TeseFma_reversao/README.md), hipótese R01.
- SL e SG serão tratados exclusivamente em TeseFma_SL.
- Entrada será tratada somente na fila operacional futura.

## 6. Taxonomia de área obrigatória

Toda ficha ou medição Axx identifica seu tipo: ART (Área de Range Temporal), ACT (Área de Corpo Temporal), ARC (Área de Range do Candle) ou ACC (Área de Corpo do Candle). Resultados de tipos diferentes permanecem em estratos/tabelas separados. O histórico de coincidência high-low do candle maior é ARC.
