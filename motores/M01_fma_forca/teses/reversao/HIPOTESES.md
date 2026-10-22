# Hipóteses da TeseFma_reversao

## Convenção

- `Rxx`: hipótese de reversão;
- estados possíveis: `PENDENTE`, `INCONCLUSIVA`, `CONFIRMADA`, `PARCIAL`, `NÃO SUPORTADA`, `REFUTADA`;
- nenhum veredito define operação ou gestão de risco;
- só contar como sinal contrário um candle colorido (`fam` em `{-2,-1,1,2}`) cujo lado difere do lado colorido do evento de referência.

## Registro

| id | hipótese | evento e critério previsto | controle / limite | status |
|:---|:---|:---|:---|:---|
| R01 | Contrapressão colorida de timeframe menor após o fechamento do evento maior e dentro de sua faixa de preço é seguida por reversão persistente mais frequentemente do que por retomada do contexto | Evento: família menor oposta durante a hora completa seguinte ao evento maior, dentro da faixa de preço do candle maior. Desfecho: preço futuro assinado contra a família maior cruza magnitude mínima pré-registrada e permanece além dela no horizonte fixado. Comparar também com retomada e sem desfecho. | Pareamento por timeframe, horário, período, amplitude/ATR e densidade; observações sem dados futuros são excluídas e contabilizadas; validação em período reservado. | PENDENTE — regra quantitativa a congelar antes da execução |

## Pré-condições de R01

Antes de calcular R01, registrar em `METODO.md`:

1. família/contexto de referência e o que constitui contrapressão, usando só barras menores posteriores ao fechamento do evento maior para desfecho;
2. instante de início do relógio do desfecho, sem look-ahead;
3. horizonte(s) em tempo físico e regra para gaps/sessões;
4. magnitude mínima, persistência e desempate entre reversão/retomada;
5. controle pareado e unidade estatística independente;
6. período de descoberta e período de validação.

Até esses parâmetros estarem congelados, não calcular uma taxa de reversão nem atribuir veredito empírico.