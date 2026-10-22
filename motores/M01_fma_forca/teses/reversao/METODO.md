# Método da TeseFma_reversao

## 1. Unidade de análise

A unidade primária é um evento colorido de timeframe maior, identificado sem duplicidade. Os timestamps dos CSVs do Profit indicam abertura das barras; portanto, a janela de contrapressão só começa após o fechamento do evento de referência, nunca dentro do candle maior que ainda estava sendo formado. Candidatos de família oposta nessa janela posterior e dentro da faixa de preço de referência são registrados como contrapressão; neutros e sinais do mesmo lado são classes distintas.

Eventos cujas janelas se sobrepõem não podem ser tratados como observações independentes sem controle explícito. A análise deve agrupar/parear por sessão ou evento e evitar inflar o tamanho amostral contando múltiplos candles menores como eventos independentes.

## 2. Separar cor de movimento do preço

A família do motor (`fam`) é estado econofísico/cor. O desfecho de reversão é medido separadamente em preço. Para evento com lado $s=\operatorname{sign}(fam_{maior})$, um retorno futuro contrário ao contexto tem sinal $-s$; essa convenção não transforma família em recomendação direcional.

## 3. Desfechos a classificar

Após pré-registro dos parâmetros, classificar cada evento em uma única categoria:

- reversão persistente;
- retomada do contexto;
- nenhum limiar atingido no horizonte;
- não avaliável por falta de candles/timestamps futuros.

O teste deve calcular retorno assinado, excursão favorável/adversa e tempo até primeiro cruzamento. Uma passagem intrabar isolada não basta para “persistente”; a regra de fechamento, duração ou número de barras deve ser decidida antes de observar os resultados.

## 4. Controles e validação

- mesmo ativo, timeframe maior/menor e período;
- mesmo horário/sessão, com gaps de sessão respeitados;
- amplitude da área, ATR/range e densidade comparáveis;
- controlar seleção por saturação/ignição e cluster/candle;
- reservar um período cronológico fora da amostra;
- usar erros/confiança que reconheçam dependência dentro do dia e eventos sobrepostos.

Não usar a faixa fora da área como controle automaticamente: ela pode ter outra distribuição de preço, distância, horário e densidade. Definir o pareamento antes do cálculo e registrar falhas de suporte comum.

## 5. Suficiência e veredito

Reportar eventos elegíveis, contrapressão, cada desfecho, não avaliáveis, cobertura temporal, controles pareados e incerteza. Se não houver controle comparável ou período reservado, resultado máximo permitido é descritivo/inconclusivo; sem amostra e definição adequadas, manter `PENDENTE`.

Não criar limiares de magnitude/horizonte olhando os retornos realizados. Uma mudança na definição de R01 exige novo identificador.

## 6. Escopo proibido

Este método não transforma contrapressão em entrada ou reversão operacional e não calcula SL, SG, risco, quantidade, custos de trade ou execução.