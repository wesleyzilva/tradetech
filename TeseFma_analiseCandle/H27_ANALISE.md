# H27 — análise do z-score robusto sem o candle atual

## Pergunta

A hipótese H27 testa se a classificação brilhante do motor fica mais estável quando o z-score é calculado com a média e a escala do período sem incluir o candle atual.

A ideia é simples:

- o cálculo canônico usa o próprio candle na janela móvel;
- isso pode mascarar extremos no mesmo candle;
- a variante robusta remove o candle atual antes de computar a média e a MAD;
- se a variante preserva o alerta de atividade com pouca perda, ela é uma alternativa mais estável.

## Definição do teste

- variável de alvo: `F`
- base: série canônica WIN
- janelas: 5min, 10min, 15min, 20min, 30min, 60min
- critério de brilho: `F > 0` e `z >= 2.5`
- robusto: `z_robusto = (F - mu_antes) / (1.4826 * MAD_antes)` com a janela calculada no período anterior ao candle atual

## Evidência dos dados

Execução usada para esta análise:

```powershell
$env:PYTHONPATH = 'E:\wesleyzilva\repo\tradetech\TeseFma_analiseCandle'; python -c "import sys, json; sys.path.insert(0, r'E:\wesleyzilva\repo\tradetech\TeseFma_analiseCandle'); from analise_candles import Contexto; from validacao_econofisica import medir_h27; c = Contexto(pastas=['2020_22','2022_24','2024_26','2026','CandlesHistoricos2026'], ativo='WIN', tfs=['5min','10min','15min','20min','30min','60min'], tf_foco=['5min','15min']); out = {}; 
for tf in ['5min','10min','15min','20min','30min','60min']:
    d = c.serie('WIN', tf)
    m = medir_h27(d, janela=20, k=2.5)
    out[tf] = m
print(json.dumps(out, indent=2, default=str))"
```

Resultado observado:

| TF | Candles canônicos | Candles robustos | Lift robusto | Expansão robusta | Expansão canônica | Dif. expansão |
|---|---:|---:|---:|---:|---:|---:|
| 5min | 506 | 715 | 1.273 | 1.184 | 1.700 | 0.516 |
| 10min | 243 | 271 | 1.208 | 1.141 | 1.519 | 0.378 |
| 15min | 128 | 36 | 1.444 | 1.283 | 1.362 | 0.079 |
| 20min | 163 | 17 | 1.180 | 1.037 | 1.387 | 0.350 |
| 30min | 31 | 0 | NaN | NaN | 1.210 | NaN |
| 60min | 12 | 0 | NaN | NaN | 1.121 | NaN |

## Leitura

### 1) O robusto aumenta a contagem de eventos em 5min e 10min

No 5min e no 10min, a variante robusta gera mais eventos do que a canônica.

Isso sugere que o cálculo canônico pode, de fato, mascarar eventos brilhantes quando o próprio candle entra na janela.

Mas essa mudança não significa que a variante seja melhor em termos de alerta de atividade. A simples presença de mais eventos não é suficiente.

### 2) A expansão do próximo range cai bastante

O ponto mais importante é a expansão do próximo range:

- 5min: 1.184 robusto vs 1.700 canônico
- 10min: 1.141 robusto vs 1.519 canônico
- 15min: 1.283 robusto vs 1.362 canônico
- 20min: 1.037 robusto vs 1.387 canônico

A robusta diminui o efeito de expansão bastante. Em outras palavras, o excesso de brilho pode estar sendo reforçado pela auto-inclusão do candle atual.

Mas a hipótese H27 não é apenas “o shiny event muda”; ela pretende que o robusto preserve o alerta sem um efeito colapsado. Isso não acontece de forma convincente:

- a diferença de expansão em 5min é 0.516x
- em 10min é 0.378x
- em 20min é 0.350x

Esses valores são muito além do que a hipótese original considerava como ajuste aceitável.

### 3) Em TFs mais altos, o robusto quase desaparece

A contagem robusta cai para 36 no 15min, 17 no 20min e 0 no 30min/60min.

Isso significa que a variante robusta não é estável como regra geral do motor; ela depende do timeframe e da amostra.

## Conclusão da análise

A análise confirma o que já estava apontado no registro de hipóteses: H27 não se sustenta como alternativa forte para o motor.

Os dados mostram:

- o robusto remove o auto-mascaramento em alguns TFs;
- mas ele não preserva a expansão do próximo range de forma consistente;
- em TFs mais altos ele quase desaparece;
- e a mudança de magnitude é grande demais para ser tratada como simples refinamento.

## Veredito qualificado

- H27: não sustentada como substituição do cálculo canônico
- interpretação apropriada: a auto-inclusão do candle atual importa, mas não basta para justificar um z-score robusto como regra canônica
- próxima ação: manter o cálculo canônico como referência e tratar a robusta como diagnóstico adicional, não como definição principal do motor

## Próximo passo

A próxima hipótese do motor a seguir é H26, porque ela testa se a janela física fixa melhora a comparabilidade entre timeframes antes de qualquer mudança na métrica principal.
