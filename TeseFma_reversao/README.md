# TeseFma_reversao — sinais contrários e desfechos

## 1. Objetivo

Estudar descritivamente se um sinal econofísico de família oposta ao contexto antecedente é seguido por reversão persistente, retomada do contexto ou ausência de deslocamento relevante.

Esta tese não define entrada, saída, SL, SG, risco, quantidade ou regra operacional. Um candle contrário é uma observação; não é, por si só, prova de reversão.

## 2. Relação com a tese de áreas

Quando um evento colorido do timeframe maior pertence à família $f$ e um candle colorido menor na hora posterior ao fechamento do evento, ainda dentro da faixa de preço original, pertence ao lado $-f$, a tese de áreas registra **contrapressão futura**. A classificação do movimento posterior é encaminhada para esta tese. Família neutra `0` não é contrária; as classes `+1/+2` e `-1/-2` são opostas por lado. Profit timestamps são timestamps de abertura.

Na TeseFma_areas, a associação entre contrapressão e persistência é A05; a classificação do desfecho como reversão ou retomada é somente R01. A análise de confirmação de área continua separada e não muda seu veredito por haver sinais contrários.

## 3. Desfechos que serão distinguidos

- **Reversão persistente:** o preço se desloca contra a família do evento por uma regra de horizonte e magnitude fixada antes do teste.
- **Retomada:** após contrapressão, o preço volta a deslocar-se no sentido compatível com a família do evento.
- **Sem desfecho classificado:** nenhum limite previamente definido é atingido no horizonte ou faltam dados.

Família de cor descreve o estado do motor e não deve ser confundida com retorno futuro ou direção operacional. O sentido de preço será calculado explicitamente a partir do fechamento/preço de referência do evento.

## 4. Ordem de estudo

1. Fixar o evento, a janela temporal e a área herdados da análise de áreas.
2. Descrever frequência e posição temporal dos candles opostos.
3. Medir retorno e excursão de preço posteriores em horizontes não sobrepostos.
4. Comparar eventos com contrapressão a controles pareados por horário, timeframe, período e amplitude/volatilidade observada.
5. Separar ignição/saturação, timeframe menor, posição dentro da área e persistência da sequência.
6. Replicar em período reservado e, quando disponível, no WDO.

Não selecionar limites depois de ver qual deles favorece a hipótese. Relatar dados insuficientes e resultados inconclusivos sem forçar veredito.

## 5. Limites

- Um candle ou alarme de cor oposta é **contrapressão**, não confirmação de reversão.
- A hipótese exige desfecho posterior observável, persistência e controle.
- A frequência de candles opostos não é probabilidade de reversão.
- Não inferir entrada, execução, SL, SG, lucro ou risco.
- A área, o sinal contrário e o desfecho devem manter timestamps e controles reproduzíveis.

## 6. Arquivos

- `README.md`: mapa e limites;
- `HIPOTESES.md`: registro prévio de hipóteses;
- `METODO.md`: definições, desfechos e controles;
- `ANALISE_REVERSAO.md`: evidências e vereditos.

**Status atual:** arquitetura registrada; análise empírica de reversão ainda não iniciada. Primeiro passo futuro: R01, após congelar controles e desfecho observável.