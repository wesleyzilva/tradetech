# Econofísica no TradeTech — o que já está medido e o que falta para um mestrado

Este texto separa o que o repositório **já mediu** do que ainda é analogia. Serve para decidir o que pode virar dissertação e o que precisa ser abandonado.

## 1. O que a analogia de fluidos pede e o que os dados respondem

A ideia de fundo é tratar o fluxo de ordens como um fluido: `F = m·a`, com massa = eficiência do candle e aceleração = volume relativo. A tabela abaixo confronta cada peça da analogia com uma medida que já existe.

| Peça da analogia | Medida no repositório | Resultado | Onde |
|---|---|---|---|
| `a` (volume relativo) produz deslocamento | lei de impacto: corpo/ATR cresce com `a` | β ≈ 0,68–0,76, R² ≈ 0,94–0,97, estável no hold-out | M01 H03; `ANALISE_ESCALONAMENTO_ECONOFISICO.md` |
| `m` e `a` são dimensões distintas | correlação de postos | ρ ≈ 0,10–0,12 | M01 H02 |
| A escala `k` importa | estados com k=1 e k=100 | 0 divergências | M01 H01 |
| Regra 80/20 da energia | concentração de \|F\| | top 20% concentra ~55%, não 80% | M01 H06, **refutada** |
| Cauda de lei de potência | R² log-log × semilog | depende do timeframe | M01 H08, parcial |
| Cauda mais pesada que a normal | frequência em 2,5σ ÷ previsão gaussiana | 2,2× a 3,6×; α de Hill 2,1–2,9 | M01 H14 |
| Ignition e saturação como regime | limiares fixos 70/85 | a hierarquia **se inverte**: ≥ 85 é mais comum que 70–85 | M01 H09 |
| Sazonalidade do volume | aceleração dessazonalizada | remove a concentração de cor na abertura | M01 H13 |
| Absorção (muito esforço, pouco deslocamento) | `a ≥ 2` e \|m\| < 0,3 | range seguinte 1,6×–1,7×, persiste | M01 H29 |
| "Turbulência" = barra brilhante | range seguinte ÷ média da hora | 1,15×–1,44×, t de 8 a 19 | M01 H20 |
| Cor indica a direção do fluxo | retorno alinhado, vários horizontes | \|t\| < 3 ou troca de sinal no período seguinte | M01 H05, H18, H19; M16 CF-H02, CF-H07 |

O que sobrevive é a **cinemática**: esforço volumétrico e deslocamento se relacionam de forma estável, com cauda pesada e sazonalidade forte. O que não sobrevive é a **dinâmica**: nada disso prevê o sinal do próximo movimento.

## 2. O que falta medir para a analogia ficar honesta

Estas grandezas são o próximo passo natural e todas são calculáveis com os candles que já temos. Nenhuma foi medida ainda.

| Grandeza | Definição operacional | Pergunta |
|---|---|---|
| Número de Reynolds do pregão | `Re = v·L/ν`, com `v` = \|retorno\| acumulado, `L` = duração, `ν` = variância do fluxo de volume | dias de Re alto têm mais reversões (turbulentos) ou mais continuação (laminares)? |
| Viscosidade | razão entre esforço (`a`) e deslocamento obtido (corpo/ATR), por faixa de horário | a "viscosidade" cai na abertura e sobe no meio do dia? |
| Intermitência | momentos da distribuição de retornos normalizados e fator de curtose por escala (5, 15, 30, 60 min) | a curtose cai com a escala como em turbulência? |
| Cascata de energia | correlação entre o \|retorno\| de uma barra de 60 min e a soma dos \|retornos\| das barras de 5 min dentro dela | a volatilidade do TF menor é prevista pelo TF maior? |
| Tempo de relaxação | autocorrelação do retorno alinhado depois de um evento de saturação, até voltar a zero | quanto tempo o mercado leva para "esquecer" o impulso? |

Cada uma vira uma hipótese `CF-H` ou `H` com critério declarado antes de rodar, no mesmo formato das que já existem.

## 3. Outros conceitos de econofísica que cabem nestes dados

| Conceito | O que mediria | Viabilidade com os dados atuais |
|---|---|---|
| Expoente de Hurst (memória longa) | `H` do retorno por escala; `H > 0,5` = persistência | alta: 12 anos de 30 e 60 min |
| Distribuição de retornos e lei de potência | cauda de retornos intradiários, α de Hill por horário | alta; M01 H14 já começou |
| Analogia com temperatura | variância do retorno como temperatura; "equilíbrio" = retorno à média da variância | média: precisa definir o análogo com cuidado |
| Criticalidade (avalanches) | tamanho das sequências de barras na mesma direção segue lei de potência? | média |
| Potencial e poços | regiões de preço onde o mercado passa mais tempo (já esboçado nos clusters de cor, H25) | média; H25 está pendente |
| Entropia de transferência | fluxo de informação entre WIN e WDO (quem lidera quem) | média: as séries têm timestamps compatíveis |
| Microestrutura clássica | impacto de ordem, spread efetivo | **inviável**: não há dados de tick nem de book |

## 4. O que um mestrado pode defender com isto

Um trabalho defensável tem uma frase central e evidência dos dois lados. Com o que já está medido, há dois caminhos.

**Caminho A — a relação esforço-deslocamento.** "O deslocamento normalizado de um candle do índice futuro cresce com o volume relativo segundo uma potência estável (β ≈ 0,7), com cauda mais pesada que a gaussiana e sazonalidade intradiária que, uma vez removida, elimina a concentração de eventos extremos na abertura." Isso está praticamente todo medido (H02, H03, H13, H14) e falta só replicar em WDO e no hold-out mais recente com o mesmo script.

**Caminho B — a ausência de previsibilidade direcional.** "Indicadores de estado derivados de volume e geometria do candle, inclusive alinhados entre timeframes e com limiares calibrados, não produzem retorno direcional que sobreviva a uma divisão temporal dos dados." Isso também está medido (H05, H18, H19, CF-H02, CF-H07 a CF-H09) e é um resultado publicável: a contribuição é o protocolo (hipótese congelada, custo, hold-out, comparação com entrada aleatória), não a descoberta de uma estratégia.

Os dois caminhos juntos formam um argumento completo: o mercado tem estrutura física descritiva e, mesmo assim, essa estrutura não dá vantagem direcional. É exatamente o que a seção 7 da `ANALISE_002_alinhamento.md` mostra com os números do alinhamento entre timeframes.

## 5. O que não dá para defender

- Qualquer estratégia de entrada baseada em cor, sozinha ou alinhada entre timeframes: os testes CF-H04, CF-H07, CF-H08 e CF-H09 falharam com o critério declarado antes de rodar.
- A narrativa de "saturação = exaustão" ou "ignição = continuação": H18 e H19 não se confirmaram.
- Analogias que não tenham uma grandeza medida por trás. Reynolds, viscosidade e cascata estão na seção 2 justamente porque ainda são nomes, não números.
