# M02 — Método de simulação

Réplica Python do robô NTSL em [`codigo/mb_motor.py`](codigo/mb_motor.py). Os parâmetros de `Params()` são os do fonte; qualquer desvio é um delta.

## Cálculos

| Item | Definição |
|---|---|
| TR | `max(H−L, |H−C₋₁|, |L−C₋₁|)` |
| ATR | média simples do TR em 20 barras **incluindo a barra atual** (= `AvgTrueRange(20,0)`) |
| Estado da barra | range ≥ 1,7 × ATR → brilhante (3 alta / 4 baixa); ≥ 1,3 × ATR → escuro (1 alta / 2 baixa); senão 0. Alta = `C ≥ O` |
| SL / SG | `max(round(ATR × 0,5), 35)` / `max(round(ATR × 2,5), 120)` pontos (ATR da barra que acabou de fechar) |
| SMA | `Media(20, Close)` |
| Janelas | HHMM da barra: [0915, 1200) ∪ [1400, 1615] |

## Sinais (no fechamento da barra *i*)

1. ctx 1 (venda): estado anterior = 3, `C₋₁ > O₋₁`, `C < L₋₁`
2. ctx 2 (compra): estado anterior = 4, `C₋₁ < O₋₁`, `C > H₋₁`
3. ctx 3: estado atual = anterior = 0 e (`C > SMA`, `C > O`, `C > H₋₁` → compra) ou (`C < SMA`, `C < O`, `C < L₋₁` → venda)

Prioridade ctx 1 > 2 > 3, como no `Senao Se` do NTSL. Só avalia sem posição aberta.

## Execução

- **Entrada:** ordem a mercado no fechamento de *i* → preenchida na **abertura de *i+1*** (sem slippage; custo em pontos por trade via `custo_pts`).
- **Ordens de proteção:** o NTSL reenvia alvo/stop **a cada barra** com posição aberta, calculadas sobre `BuyPrice/SellPrice` e o ATR da barra que acabou de fechar. Logo:
  - perfil **fiel** (`protecao_na_barra_de_entrada=False`): a barra de entrada fica **sem proteção**; as ordens passam a valer na barra seguinte;
  - perfil **ideal** (`True`): proteção ativa desde a abertura da entrada (limite superior otimista).
- **Stop-limit:** gatilho em `stop`, limite em `stop ∓ 5`. Se, ao enviar a ordem, o fechamento já estiver além do limite, a ordem fica **passiva** (executa só se o preço voltar ao limite): é a *armadilha do stop-limit*. Sem dados de ticks, o fill de um stop-limit com gap é modelado: preenche no limite quando o preço o toca de volta, caso contrário permanece em aberto até o tempo/zeramento.
- **Mesma barra com stop e alvo:** stop primeiro (pior caso).
- **Saída por tempo:** `MaxBarrasTrade = 20` contadas a partir da barra de entrada; saída a mercado na abertura da barra seguinte.
- **Zeramento:** `Time ≥ 1720`; fim do pregão fecha no último fechamento.
- **Sem alavancagem/tamanho:** 1 contrato; resultados em pontos.

## Controles

- **Nulo aleatório** (`aleatorio_mesma_saida`): mesmas janelas, mesma frequência de sinais por barra de janela, lado sorteado, mesma geometria de saída; 100 repetições (`--reps`). Resultado do robô é reportado como percentil do nulo.
- **Custos:** 0, 2 e 5 pontos por trade.
- **Estabilidade:** 1ª × 2ª metade dos pregões.
- **Escala:** os mesmos parâmetros em 5 min (apenas robustez do conceito).

## Limitações conhecidas

- Candle OHLC não diz a ordem H/L dentro da barra; "stop primeiro" é conservador.
- O NTSL no Profit pode avaliar a lógica **a cada tick** da barra em formação (Close = último preço); a réplica assume avaliação **no fechamento**. Paridade com o Profit é um item aberto (`MB-H12`).
- `Time` do NTSL assumido igual à abertura da barra do CSV.
- Fill de stop-limit e de ordens a mercado em movimentos rápidos não é observável nos candles.
- Conjuntos 1 min são curtos (64 e 35 pregões completos).

## Validação do simulador

`tests/test_mb_motor.py` cobre: SL, SG, stop e alvo na mesma barra, simetria da venda, entrada sem proteção (fiel × ideal), stop-limit passivo, tempo de 20 barras, ausência de entrada na última barra, custo por trade, pisos de distância, bordas das janelas e classificação de estados.
