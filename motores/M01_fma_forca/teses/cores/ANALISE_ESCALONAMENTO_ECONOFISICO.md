# WIN — escalonamento econofísico do motor F=m·a

_Gerado por `analise_escalonamento_econofisico.py`. Janela comum entre timeframes: 2024-06-19 a 2026-05-14. Parser e cálculo: motor Python canônico._

## Pergunta

Como o deslocamento corporal normalizado pelo ATR (`body/ATR`) escala com esforço volumétrico `a`, eficiência geométrica `|m|` e produto `|F|`, e a relação varia entre faixas horárias?

## Definições e desenho

- Usa `ler_csv()` e `calcular()` de `analise_candles.py`; mantém a definição e janela do motor. Calcula cada contrato dentro do próprio arquivo, seleciona por pregão o contrato com volume próximo do máximo, aplica a prioridade das pastas canônicas e não mistura rolagens dentro de janelas móveis.
- `body/ATR = |Close−Open| / ATR`; `a = volume / média de volume anterior`; `m = (Close−Open)/range`; `F = m×a×100`.
- Para cada variável, agrupa observações positivas em 20 quantis, calcula a mediana de x e body/ATR em cada faixa e ajusta `log(body/ATR) = α + β log(x)`. Também reporta Spearman candle a candle. O `R² log-log` é descritivo e calculado sobre as 20 medianas das faixas.
- O intervalo de confiança do β para `a` reamostra pregões inteiros; não reamostra candles independentes. Sessões horárias estão fixadas antes da leitura: 09h; 10–11h; 12–13h; 14–17h.
- São medidas internas descritivas: `body/ATR` já é derivado do preço no mesmo candle e `a` participa de F. Logo, associação e ajuste não estabelecem causalidade física independente.
- Validação temporal H03: treino = início da janela até 2025-06-18 (12 meses); holdout = 2025-06-19 a 2026-05-14. Quantis e bordas são calculados apenas no treino e congelados no holdout.

## 5min

Amostra: 50.773 candles. 473 pregões. de 2024-06-19 a 2026-05-14.

### Esforço de volume a

- Spearman com corpo/ATR: ρ=0.438. Curva mediana em faixas equifrequentes: β=0.76, R² log-log=0.969.

| Faixa | a mediano | corpo/ATR mediano | n |
|---:|---:|---:|---:|
| 1 | 0.256 | 0.205 | 2445 |
| 2 | 0.395 | 0.219 | 2445 |
| 3 | 0.474 | 0.233 | 2445 |
| 4 | 0.532 | 0.251 | 2445 |
| 5 | 0.583 | 0.275 | 2445 |
| 6 | 0.628 | 0.295 | 2444 |
| 7 | 0.673 | 0.308 | 2445 |
| 8 | 0.718 | 0.321 | 2445 |
| 9 | 0.765 | 0.334 | 2445 |
| 10 | 0.816 | 0.379 | 2445 |
| 11 | 0.869 | 0.406 | 2444 |
| 12 | 0.929 | 0.422 | 2445 |
| 13 | 0.998 | 0.447 | 2445 |
| 14 | 1.077 | 0.501 | 2445 |
| 15 | 1.171 | 0.546 | 2445 |
| 16 | 1.292 | 0.562 | 2444 |
| 17 | 1.461 | 0.598 | 2445 |
| 18 | 1.707 | 0.677 | 2445 |
| 19 | 2.138 | 0.769 | 2445 |
| 20 | 3.450 | 1.210 | 2445 |

### Eficiência geométrica |m|

- Spearman com corpo/ATR: ρ=0.885. Curva mediana em faixas equifrequentes: β=1.16, R² log-log=0.993.

### Produto |F|=|m·a·100|

- Spearman com corpo/ATR: ρ=0.918. Curva mediana em faixas equifrequentes: β=0.94, R² log-log=0.996.

IC percentil 95% de β(a), bootstrap por pregão (300 réplicas, semente 20261006): [0.72, 0.80].

### Estabilidade intradiária do escalonamento de a

| Faixa horária | Candles | Pregões | β(a) | R² log-log | ρ(a, corpo/ATR) |
|---|---:|---:|---:|---:|---:|
| abertura 09h | 5408 | 469 | 0.93 | 0.924 | 0.519 |
| manhã 10–11h | 10810 | 470 | 0.84 | 0.976 | 0.416 |
| meio-dia 12–13h | 10759 | 472 | 0.95 | 0.928 | 0.407 |
| tarde 14–17h | 21535 | 472 | 0.88 | 0.938 | 0.449 |

**Leitura:** β<1 é compatível com retornos decrescentes do deslocamento mediano conforme aumenta o esforço de volume; β≈1 seria proporcionalidade; β>1 seria superlinear. Isso descreve associação entre variáveis construídas pelo próprio motor, não causalidade física provada.

## 15min

Amostra: 17.365 candles. 473 pregões. de 2024-06-19 a 2026-05-14.

### Esforço de volume a

- Spearman com corpo/ATR: ρ=0.482. Curva mediana em faixas equifrequentes: β=0.74, R² log-log=0.939.

| Faixa | a mediano | corpo/ATR mediano | n |
|---:|---:|---:|---:|
| 1 | 0.211 | 0.207 | 842 |
| 2 | 0.328 | 0.181 | 842 |
| 3 | 0.409 | 0.189 | 842 |
| 4 | 0.464 | 0.196 | 842 |
| 5 | 0.508 | 0.220 | 842 |
| 6 | 0.548 | 0.246 | 842 |
| 7 | 0.588 | 0.263 | 841 |
| 8 | 0.628 | 0.301 | 842 |
| 9 | 0.672 | 0.313 | 842 |
| 10 | 0.722 | 0.343 | 842 |
| 11 | 0.783 | 0.343 | 842 |
| 12 | 0.861 | 0.442 | 842 |
| 13 | 0.967 | 0.435 | 842 |
| 14 | 1.118 | 0.457 | 841 |
| 15 | 1.311 | 0.531 | 842 |
| 16 | 1.541 | 0.575 | 842 |
| 17 | 1.816 | 0.641 | 842 |
| 18 | 2.150 | 0.711 | 842 |
| 19 | 2.623 | 0.907 | 842 |
| 20 | 3.464 | 1.256 | 842 |

### Eficiência geométrica |m|

- Spearman com corpo/ATR: ρ=0.856. Curva mediana em faixas equifrequentes: β=1.17, R² log-log=0.990.

### Produto |F|=|m·a·100|

- Spearman com corpo/ATR: ρ=0.914. Curva mediana em faixas equifrequentes: β=0.94, R² log-log=0.997.

IC percentil 95% de β(a), bootstrap por pregão (300 réplicas, semente 20261006): [0.71, 0.77].

### Estabilidade intradiária do escalonamento de a

| Faixa horária | Candles | Pregões | β(a) | R² log-log | ρ(a, corpo/ATR) |
|---|---:|---:|---:|---:|---:|
| abertura 09h | 1845 | 470 | 0.89 | 0.819 | 0.442 |
| manhã 10–11h | 3679 | 470 | 0.92 | 0.917 | 0.394 |
| meio-dia 12–13h | 3636 | 472 | 1.04 | 0.885 | 0.413 |
| tarde 14–17h | 7285 | 472 | 1.05 | 0.918 | 0.430 |

**Leitura:** β<1 é compatível com retornos decrescentes do deslocamento mediano conforme aumenta o esforço de volume; β≈1 seria proporcionalidade; β>1 seria superlinear. Isso descreve associação entre variáveis construídas pelo próprio motor, não causalidade física provada.

## H03 — validação temporal sem alterar a hipótese

Regra original: β>0.25 e R²≥0.80 na relação log-log entre a e body/ATR, estimada sobre 20 faixas. Para evitar recalibrar no holdout, as bordas equifrequentes são aprendidas no treino e mantidas fixas na validação.

Este é um anexo de robustez para H03, não uma nova hipótese nem alteração do critério original. O corte temporal é fixado pelo desenho e os quantis de treino são reutilizados sem recalibração no holdout.

| TF | Período treino | n treino | β treino | R² treino | Critério treino | Período holdout | n holdout | β holdout | IC95% β holdout (pregão) | R² holdout | Critério holdout |
|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---|
| 5min | 2024-06-19–2025-06-18 | 28142 (250 pregões) | 0.85 | 0.988 | passa | 2025-06-19–2026-05-14 | 22631 (223 pregões) | 0.72 | [0.67, 0.78] | 0.941 | passa |
| 15min | 2024-06-19–2025-06-18 | 9482 (250 pregões) | 0.80 | 0.945 | passa | 2025-06-19–2026-05-14 | 7883 (223 pregões) | 0.70 | [0.65, 0.74] | 0.914 | passa |

## Síntese

- **5min:** escalonamento `a → body/ATR` β=0.76, R²=0.969, ρ=0.438, IC95% por pregão [0.72, 0.80].
- **15min:** escalonamento `a → body/ATR` β=0.74, R²=0.939, ρ=0.482, IC95% por pregão [0.71, 0.77].

A hipótese mecanicista mais estreita compatível com este desenho é: ‘maior a acompanha maior corpo/ATR mediano’, caso a relação positiva se replique por pregões e faixas horárias. Mesmo se sustentada, isso não prova volume como força causal nem permite chamar `a` de aceleração física: volume de contratos é uma proxy de atividade/fluxo.
A H03 permanece a mesma hipótese. Este holdout é uma verificação temporal do critério existente, não uma hipótese nova. A decisão de replicação exige que treino e holdout satisfaçam separadamente β>0.25 e R²≥0.80. O IC95% do holdout informa a incerteza do beta, mas não foi acrescentado à regra original.

## Próximo teste rigoroso

1. Congelar este desenho e replicar β em blocos temporais sem sobreposição (ex.: estimação 2020–2023; verificação 2024–2026), incluindo intervalos por pregão.
2. Comparar a contribuição incremental de `a` além de `|m|` por regressão/validação por blocos, pois `F` já contém ambos; reportar desempenho descritivo em body/ATR, não direção nem rentabilidade.
3. Se blocos temporais discordarem, reportar não-estacionariedade em vez de escolher outra faixa pós-hoc.
