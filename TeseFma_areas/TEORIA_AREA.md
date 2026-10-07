# Teoria de área — rascunho de contexto visual

## 1. Resumo executivo

A ideia central das imagens é a seguinte:

- um candle, um cluster ou uma família de cor em um timeframe maior cria uma faixa de preço que parece funcionar como memória de pressão;
- o timeframe menor não reage ao acaso a essa faixa; ele a "testa", a "acumula" ou a "rejeita";
- a repetição da mesma faixa em 2 ou mais timeframes torna a área mais relevante para leitura, mas não torna a área um sinal operacional por si só;
- a área funciona como contexto, não como entrada pronta.

Em outras palavras, o que as imagens sugerem não é "o candle da cor manda o mercado"; é "a faixa de preço da cor cria um espaço de atenção no qual os candles menores se comportam de forma distinta".

## 2. O que as imagens repetem

As imagens mostram um padrão consistente:

1. um timeframe maior cria uma faixa friccionada (caixa ou faixa); 
2. o timeframe menor começa a se acumular dentro dessa faixa;
3. a área fica como uma zona de pressão, com vários candles menores entrando e saindo dela;
4. ou a área é respeitada e o movimento continua dentro da faixa;
5. ou a área falha e o preço atravessa para o lado contrário;
6. o mesmo padrão pode aparecer em mais de um timeframe, reforçando a zona.

Essa repetição é a base da teoria de área: a banda não é só um desenho; é uma zona de memória do preço.

## 3. Teoria de área

### 3.1 Definição canônica e nomes

Neste estudo, **área** significa uma faixa vertical de preço observada numa referência temporal declarada. O nome indica se os limites vêm dos extremos ou do corpo e se a referência é uma janela ou um candle individual. Não misturar os quatro tipos em uma mesma medição.

| sigla | nome canônico | referência | limites de preço |
|:---|:---|:---|:---|
| **ART** | **Área de Range Temporal** | todos os candles de uma janela/cluster $W$ | $[\min_{i\in W}(L_i),\ \max_{i\in W}(H_i)]$ |
| **ACT** | **Área de Corpo Temporal** | corpos de todos os candles da janela/cluster $W$ | $[\min_{i\in W}(\min(O_i,C_i)),\ \max_{i\in W}(\max(O_i,C_i))]$ |
| **ARC** | **Área de Range do Candle** | um candle de referência $j$ | $[L_j,H_j]$ |
| **ACC** | **Área de Corpo do Candle** | um candle de referência $j$ | $[\min(O_j,C_j),\ \max(O_j,C_j)]$ |

Onde $O$, $H$, $L$, $C$ são abertura, máxima, mínima e fechamento. “Range” sempre usa máxima–mínima; “corpo” sempre usa abertura–fechamento, ordenados do menor para o maior. “Temporal” usa o envelope dos candles explicitamente incluídos na janela, não a soma de área geométrica, nem uma faixa móvel implícita.

**Exemplo de convenção:** dois candles na janela, primeiro $O=100,H=110,L=95,C=105$ e segundo $O=104,H=108,L=98,C=99$. ART $=[95,110]$; ACT $=[99,105]$; ARC do primeiro $=[95,110]$; ACC do primeiro $=[100,105]$. ARC e ACC do segundo seriam, respectivamente, $[98,108]$ e $[99,104]$.

A janela $W$, candle de referência $j$, timeframe, limites temporais e tipo devem ser registrados antes da medição. Se mudar o tipo, trata-se de uma variante de área que deve ser comparada separadamente; não se substituem os limites após olhar o resultado.

Uma área não é, por si só, uma entrada, suporte/resistência confirmado, SL, SG ou prova de reversão. A sobreposição de timeframes é uma propriedade adicional da área, não um quinto tipo geométrico.

### 3.2 Interpretação

A área representa:

- concentração de volume perceptível;
- fricção de preço;
- memória de reação anterior;
- lugar onde o mercado tende a testar, confirmar ou rejeitar a continuidade.

A área é uma região de preço para localizar e descrever eventos. A família maior e as famílias menores podem ser comparadas dentro dela, mas a faixa sozinha não afirma que houve reação ou causalidade.

### 3.3 O que a área não é

A área não é, por si só:

- uma entrada garantida;
- um SL fixo;
- um alvo definitivo;
- uma comprovação de reversão;
- um sinal operacional sem confirmação;
- um critério que dispense o comportamento do menor timeframe.

## 4. Estrutura do comportamento visual

O padrão observado pode ser dividido em três fases:

### 4.1 Geração da área

A área nasce quando um candle ou um cluster do timeframe maior define uma faixa visível de pressão.

O que importa aqui não é a cor isolada, mas a amplitude e a repetição da zona.

### 4.2 Teste do menor timeframe

Os candles menores entram na faixa de forma repetida.

Esse teste pode ocorrer como:

- empurrão para a borda;
- rejeição parcial;
- pin bar dentro da área;
- acumulação sem rompimento;
- seio de candles dentro da faixa.

### 4.3 Validação da zona

A zona fica mais forte quando a mesma faixa é testada em múltiplos timeframes ou quando a família do timeframe maior se preserva ao menos em parte dos candles menores.

Essa validação não significa direção. Significa que a área tem relevância de contexto.

## 5. Ideia central da hipótese

A hipótese central é:

- quando uma área de preço é repetida em mais de um timeframe e o menor timeframe entra nessa zona sem quebrá-la em conjunto, a área se torna uma região de interesse;
- a decisão operacional não nasce da área sozinha, mas da resposta do mercado dentro dela;
- a área serve como filtro de contexto para a próxima resposta do preço.

A ideia é similar a uma "caixa de densidade": a zona não diz para comprar ou vender, mas diz que a região tem maior chance de ser sensível e mais cara em termos de reação.

## 6. Hipóteses de construção da tese

### A09 — área como memória do preço

Se uma área criada por um timeframe maior é testada por candles do timeframe menor dentro da mesma zona, a área tem maior chance de ser relevante do que uma janela aleatória do mesmo horário e largura.

Critério de decisão:

- frequência de teste dentro da área > controle;
- mesma família ou mesma região de comportamento;
- sem inferir direção direta.

Status: PENDENTE.

### A10 — confirmação por sobreposição de timeframes

Se a mesma faixa é compartilhada por 2 ou mais timeframes, a probabilidade de pressão ou reação na região aumenta em relação à mesma faixa isolada.

Critério de decisão:

- 2 ou mais TFs compartilham a faixa;
- a área é testada por candles menores;
- a família de maior TF é preservada na maior parte dos testes.

Status: PENDENTE.

### Sinal de família oposta — contrapressão, não reversão

Quando um candle colorido de timeframe menor dentro da janela/faixa da área tem família oposta à do evento maior, registrar uma **ocorrência de contrapressão**. Isso pode preceder reversão, pausa ou retomada da família maior; a cor oposta isolada não distingue esses resultados. A TeseFma_areas pode medir a frequência desse evento e sua associação com persistência (A05), mas não deve rotulá-lo como reversão. O desfecho do preço será testado separadamente na [hipótese R01 da TeseFma_reversao](../TeseFma_reversao/HIPOTESES.md), com horizonte, limiar, persistência e controle pré-definidos.

### A11 — entrada em contexto de área

Se o mercado entra na área e o menor timeframe reage na direção da família maior sem quebrar a zona em sentido adverso, a área funciona como contexto para uma entrada condicional.

Critério de decisão:

- entrada na área somente após rejeição ou suporte visível;
- a confirmação vem do comportamento do menor timeframe;
- não usar apenas a área como gatilho.

Status: HIPÓTESE DE CONTEXTO, não confirmada operacionalmente.

### A12 — SL por área

Se a área é a região de pressão, então o stop pode ser posicionado fora da área, em direção à perda de validade da hipótese, e não no centro do movimento.

Critério de decisão:

- SL fora da borda da área ou do último suporte/resistência relevante;
- risco medido pela largura da área e pela consistência da resposta;
- definição precisa da borda antes do teste.

Status: HIPÓTESE DE CONTEXTO, não confirmada operacionalmente.

### A13 — SG por largura da área

Se a área funciona como zona de referência, o alvo pode ser medido pela largura da área, pelo deslocamento do próximo cluster ou pela própria expansão do movimento em direção à família maior.

Critério de decisão:

- medir SG em termos da zona, da extensão da área ou do próximo pacote de movimento;
- não assumir um alvo antes de observar a distribuição real.

Status: HIPÓTESE DE CONTEXTO, não confirmada operacionalmente.

## 7. Como o rascunho deve ser lido

Este documento não diz que a área é um sistema pronto. Ele diz que:

- a área aparece de forma repetida;
- o preço parece responder à sua presença;
- o comportamento dentro da área é o que merece ser medido;
- a entrada, o SL e o SG só serão discutidos após a área ser observada e comparada corretamente.

## 8. Limites explícitos

- o que se vê na imagem é contexto visual, não operação confirmada;
- a área pode ser forte ou fraca dependendo da densidade do menor timeframe;
- uma área pode ser respeitada sem ser válida para operar;
- a presença de 2 ou 3 timeframes sobrepostos não prova direção;
- a hipótese de entrada, SL e SG deve ficar em análise separada e não em operação real.

## 9. Próximo passo

O próximo passo é transformar esse rascunho em exemplos concretos, com:

1. data;
2. ativo;
3. timeframe maior;
4. área desenhada;
5. confirmação em 1 ou mais TFs menores;
6. resposta de rejeição ou continuidade;
7. comparação com controle do mesmo horário e largura;
8. conclusão descritiva;
9. separação clara entre contexto e operação.
