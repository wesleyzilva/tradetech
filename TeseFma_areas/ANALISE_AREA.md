# Análise de áreas — registro do estudo

## 1. Status

- **Status da tese:** início;
- **Status dos dados:** dados canônicos disponíveis;
- **Status do motor:** preservado em `TeseFma_analiseCandle`;
- **Status operacional:** não iniciado;
- **Entrada:** não definida;
- **SL:** não definido;
- **SG:** não definido;
- **Reversão:** estudo separado.

**Taxonomia aplicada às evidências:** a área high-low de um único candle maior usada nas apurações preliminares é **ARC — Área de Range do Candle**. Não é ART (envelope ao longo de vários candles) nem área de corpo. Nenhum resultado de ART, ACT ou ACC foi calculado ainda.

## 2. Estrutura de um exemplo

Cada exemplo deve conter:

- data e horário;
- ativo;
- timeframe do evento;
- família do evento;
- cor de ignição ou saturação;
- timeframe menor testado;
- área utilizada;
- candles confirmados;
- candles contrários;
- direção da família;
- próximos N candles;
- próximo intervalo;
- referência visual;
- observação qualitativa;
- resultado da hipótese.

## 3. Formato de gráfico

Cada gráfico deve mostrar:

1. candles do timeframe maior;
2. área do candle ou cluster;
3. candles dos timeframes menores;
4. família de cada candle;
5. marcação de confirmação;
6. marcação de sinal contrário;
7. eventual limite de controle;
8. eixo de tempo e preço claros.

O gráfico não deve inserir linhas de entrada, SL ou SG.

## 4. Registro canônico de exemplo

Exemplo ainda não criado.

Para cada exemplo, preencher:

| campo | valor |
|:---|:---|
| data | — |
| ativo | — |
| timeframe maior | — |
| evento | — |
| família | — |
| timeframe menor | — |
| área | — |
| tipo de área (ART/ACT/ARC/ACC) | — |
| confirmação | — |
| contrários | — |
| próximos candles | — |
| persistência | — |
| controle | — |
| veredito | — |
| observação | — |

## 5. Ordem de avaliação

### Passo 1 — exemplo único

Registrar um exemplo visual e comparar o evento com a mesma hora e o mesmo tamanho de janela em controle.

### Passo 2 — frequência

Contar quantas vezes a família maior aparece no timeframe menor dentro da área.

### Passo 3 — persistência

Medir quanto do movimento permanece após a confirmação.

### Passo 4 — densidade

Comparar um, dois ou mais níveis inferiores confirmando a mesma família.

### Passo 5 — contrário

Registrar quando a família oposta aparece dentro da mesma área ou intervalo de confirmação.

### Passo 6 — controle

Comparar o resultado com janelas aleatórias e com outros horários.

## 6. Evidência inicial A01

A medição inicial usou candles de 15 minutos como evento e candles de 5 minutos no intervalo simultâneo para contar a mesma família. Essa definição reutiliza candles que formam o candle maior e, portanto, não é confirmação posterior.

Resultado histórico da consulta simultânea (não evidência de A01):

- eventos de 15 minutos: 7.651;
- candles menores da família maior contados: 1.420;
- razão bruta registrada: 18,56%;
- candles menores que cruzaram a faixa high/low: 2.701.

Os números são mantidos como histórico da medição antiga, não como confirmação posterior. A faixa high/low do candle maior também contém ou cruza muitas barras que o constituem, e não havia controle espacial/temporal comparável.

O resultado atual é **INCONCLUSIVO**: a ocorrência é observável, mas ainda não supera um controle comparável. Não há evidência de entrada, SL, SG ou direção.

## 7. Evidência ampliada para múltiplos timeframes

A apuração preliminar foi ampliada para 60 minutos como timeframe maior e 5, 10, 15, 20 e 30 minutos. Ela consultou candles menores da **mesma hora que compõe o candle de 60 min**. Como os timestamps do Profit marcam a abertura da barra, esses dados não são confirmação posterior; são sobreposição temporal/simultânea. Portanto, a tabela abaixo é preservada somente como diagnóstico da medição anterior e **não** serve como evidência de A01 nem como confirmação.

| timeframe maior | timeframe menor | eventos | confirmados | taxa de confirmação | interpretação |
|:---|:---|---:|---:|---:|:---|
| 60 min | 5 min | 15.452 | 4.836 | 31,30% | frequência simultânea descritiva; sem precedência nem controle |
| 60 min | 10 min | 15.452 | 8.944 | 57,88% | ocorrência descritiva, sem controle |
| 60 min | 15 min | 15.452 | 13.026 | 84,30% | coincidência descritiva dentro da área |
| 60 min | 20 min | 15.452 | 14.719 | 95,26% | coincidência descritiva, sensível à sobreposição temporal |
| 60 min | 30 min | 15.452 | 14.691 | 95,07% | coincidência descritiva, sensível à sobreposição temporal |

A execução posterior corrigiu algumas contagens da apuração manual. As taxas, embora reproduzíveis para essa consulta, continuam descrevendo sobreposição do candle maior com seus componentes menores, sem controle comparável e sem precedência temporal.

A leitura limitada da apuração anterior é a seguinte:

- a frequência bruta cresce com a proximidade entre timeframes;
- as barras de 20 e 30 min se sobrepõem mais no tempo e resultam em taxas próximas;
- isto não prova continuação, reversão, direção, relevância da área ou qualidade.

A hipótese A01 permanece **INCONCLUSIVA**. Não se inferem reversão nem direção dessas frequências.

## 8. Sinais contrários: separação entre área e reversão

Se um evento de 60 min pertence a uma família colorida e um candle colorido de timeframe menor dentro da mesma janela temporal e faixa de preço pertence ao lado oposto, o registro da tese de áreas deve chamá-lo de **contrapressão**. `+1/+2` são opostos a `-1/-2`; família `0` é neutra e não entra na contagem de sinais contrários.

O sinal contrário, por si só, **não significa reversão**. Para classificar um desfecho como reversão, é necessário observar o preço posterior contra o lado do evento maior por uma regra de preço e horizonte definida antes do cálculo, distinguindo-o de um recuo temporário ou retomada. Na tese de áreas, contar sinais contrários e testar apenas a associação com persistência (A05), mantendo controles. A classificação do desfecho como reversão ou retomada é exclusivamente [R01 em TeseFma_reversao](../TeseFma_reversao/HIPOTESES.md); ainda não há resultado empírico para essa hipótese.

**Próxima apuração, com ordem temporal correta:** aguardar o fechamento do evento de 60 min e então medir a janela posterior previamente escolhida; para a medição inicial, usar a próxima hora completa. Comparar a área do evento com as duas faixas adjacentes de largura igual, no mesmo bloco de candles menores posterior. Uma janela só é elegível quando contém todas as sub-barras esperadas no TF menor; buracos ficam marcados como incompletos. O controle mede diferença espacial de ocorrência, não resultado posterior. Ainda falta executar em todo o histórico, avaliar suporte/seleção por sessão e validar fora da amostra. Os intervalos de 40 e 50 min continuam indisponíveis e não serão interpolados.

## 9. Para não perder o que foi aprendido

A evidência deve ser registrada em duas camadas:

1. **Descrição:** o que aconteceu;
2. **Interpretação:** o que parece significar;
3. **Teste:** se a evidência se mantém;
4. **Conclusão:** o que a hipótese sustenta;
5. **Limite:** o que não foi comprovado.

## 10. Próximo exemplo

Antes de usar qualquer print, registrar:

- data;
- ativo;
- timeframes;
- intervalo visual;
- definição da área;
- família do evento;
- resultado esperado sem operação.

## 11. Regras de decisão

- Um exemplo positivo não confirma a tese.
- Uma série de exemplos positivos não confirma uma hipótese de operação.
- Um exemplo negativo não refuta a tese sem controle.
- A conclusão somente será aceita quando o efeito for maior no mesmo horário e na área de controle.
- Sinais de reversão serão retirados deste documento e avaliados em `TeseFma_reversao`.
