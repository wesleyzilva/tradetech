# Auditoria dos dados de candles

> **Gerado por** `ferramentas/auditar_candles.py` — não editar à mão; rodar novamente após incluir novos CSVs. Catálogo por arquivo: [`dados/catalogo_candles.csv`](../../dados/catalogo_candles.csv).

## 1. Resumo executivo

- 127 arquivos em `dados/candles/` (9 lotes, 8 séries). WIN: 59 arquivos; WDO: 50.
- Todos os timestamps são da **abertura** da barra (convenção Profit). Preço/volume usam notação brasileira; o leitor canônico é `src/tradetech/dados.py`.
- Violações OHLC (máx < max(o,c) ou mín > min(o,c)): **0**. Timestamps duplicados dentro de arquivo: **0**.
- **Os nomes das pastas antigas (`2012_14`, `2024_26` …) não correspondiam ao conteúdo real**; os lotes foram renomeados pela cobertura verificada (ver §2).
- A exportação `2024-2025_alt` do WINFUT usa **preço ajustado** (centavos) e fica ~5.700–7.200 pts acima da série padrão: nunca misturar (ver §5).

## 2. Lotes (cobertura real por arquivo mais longo)

| lote | séries | arquivos | início | fim |
|---|---|---|---|---|
| 2014-2015 | WDOFUT, WINFUT | 8 | 2014-01-02 | 2015-12-30 |
| 2016-2017 | WDOFUT, WINFUT | 8 | 2016-01-04 | 2017-12-28 |
| 2018-2019 | WDOFUT, WINFUT | 8 | 2018-01-02 | 2019-12-30 |
| 2020-2021 | WDOFUT, WINFUT | 12 | 2020-01-02 | 2021-12-30 |
| 2022-2023 | WDOFUT, WINFUT | 14 | 2022-01-03 | 2023-12-28 |
| 2024-2025 | WDOFUT, WDOJ26, WINFUT, WINJ26 | 36 | 2024-01-02 | 2025-12-30 |
| 2024-2025_alt | WINFUT, WINFUTV | 18 | 2024-01-02 | 2025-12-30 |
| 2026-1S_M26 | WDOM26, WINM26 | 14 | 2026-01-02 | 2026-05-14 |
| 2026-2S_Q26 | WINQ26 | 9 | 2026-02-13 | 2026-08-03 |

Mapa antigo → novo: `2012_14`+`2014_16` → `2014-2015` · `2016_18` → `2016-2017` · `2018_20` → `2018-2019` · `2020_22` → `2020-2021` · `2022_24` → `2022-2023` · `2024_26` → `2024-2025` · `2026` (WINM26/WDOM26) → `2026-1S_M26` · `2026` (WINFUT/WINFUTV com sufixo de datas) e `CandlesHistoricos2026/WINFUT_*` → `2024-2025_alt` · `CandlesHistoricos2026/WINQ26_*` → `2026-2S_Q26`.

## 3. Cobertura útil por timeframe (série padrão, sessões completas)

Sessão completa = pelo menos 90% das barras do percentil 95 de barras/sessão do próprio arquivo. Contratos com vencimento têm início ralo (pouca liquidez) e por isso `sessoes_total` ≠ `sessoes_completas`.

| serie | tf | 1ª sessão completa | última sessão completa | sessões completas | sessões no arquivo |
|---|---|---|---|---|---|
| WINFUT | 1min | 2025-09-29 | 2025-12-30 | 64 | 65 |
| WINFUT | 5min | 2024-06-19 | 2025-12-30 | 383 | 385 |
| WINFUT | 10min | 2022-09-01 | 2025-12-30 | 827 | 832 |
| WINFUT | 15min | 2020-11-04 | 2025-12-30 | 1.280 | 1.286 |
| WINFUT | 20min | 2018-07-06 | 2025-12-30 | 1.853 | 1.862 |
| WINFUT | 30min | 2014-01-02 | 2025-12-30 | 2.937 | 2.953 |
| WINFUT | 60min | 2014-01-02 | 2025-12-30 | 2.937 | 2.953 |
| WINFUT | D1 | 2014-01-02 | 2025-12-30 | 2.977 | 2.977 |
| WINFUT | W1 | 2014-01-06 | 2025-12-29 | 521 | 521 |
| WINJ26 | 1min | 2025-12-18 | 2025-12-30 | 7 | 90 |
| WINJ26 | 5min | 2025-12-18 | 2025-12-30 | 7 | 90 |
| WINJ26 | 10min | 2025-12-18 | 2025-12-30 | 7 | 90 |
| WINJ26 | 15min | 2025-12-18 | 2025-12-30 | 7 | 90 |
| WINJ26 | 20min | 2025-12-17 | 2025-12-30 | 8 | 90 |
| WINJ26 | 30min | 2025-12-16 | 2025-12-30 | 9 | 90 |
| WINJ26 | 60min | 2025-09-03 | 2025-12-30 | 32 | 90 |
| WINJ26 | D1 | 2025-08-22 | 2025-12-30 | 90 | 90 |
| WINJ26 | W1 | 2025-08-22 | 2025-12-29 | 20 | 20 |
| WINM26 | 5min | 2026-02-19 | 2026-05-14 | 58 | 90 |
| WINM26 | 10min | 2026-02-19 | 2026-05-14 | 58 | 90 |
| WINM26 | 15min | 2026-02-19 | 2026-05-14 | 58 | 90 |
| WINM26 | 20min | 2026-02-19 | 2026-05-14 | 58 | 90 |
| WINM26 | 30min | 2026-02-12 | 2026-05-14 | 59 | 90 |
| WINM26 | 60min | 2026-01-14 | 2026-05-14 | 69 | 90 |
| WINM26 | D1 | 2026-01-02 | 2026-05-14 | 90 | 90 |
| WINQ26 | 1min | 2026-05-19 | 2026-07-24 | 35 | 109 |
| WINQ26 | 5min | 2026-04-16 | 2026-07-24 | 69 | 109 |
| WINQ26 | 10min | 2026-04-15 | 2026-07-24 | 70 | 109 |
| WINQ26 | 15min | 2026-04-15 | 2026-08-03 | 75 | 115 |
| WINQ26 | 20min | 2026-04-15 | 2026-07-24 | 70 | 109 |
| WINQ26 | 30min | 2026-04-15 | 2026-07-24 | 70 | 109 |
| WINQ26 | 60min | 2026-03-31 | 2026-07-24 | 75 | 109 |
| WINQ26 | D1 | 2026-02-13 | 2026-07-24 | 109 | 109 |
| WINQ26 | W1 | 2026-02-13 | 2026-07-20 | 24 | 24 |
| WDOFUT | 1min | 2025-11-17 | 2025-12-30 | 29 | 30 |
| WDOFUT | 5min | 2024-06-26 | 2025-12-30 | 379 | 381 |
| WDOFUT | 10min | 2022-09-01 | 2025-12-30 | 828 | 832 |
| WDOFUT | 15min | 2020-11-04 | 2025-12-30 | 1.279 | 1.286 |
| WDOFUT | 20min | 2018-07-06 | 2025-12-30 | 1.852 | 1.862 |
| WDOFUT | 30min | 2014-01-02 | 2025-12-30 | 2.880 | 2.898 |
| WDOFUT | 60min | 2014-01-02 | 2025-12-30 | 2.882 | 2.898 |
| WDOFUT | D1 | 2014-01-02 | 2025-12-30 | 2.977 | 2.977 |
| WDOFUT | W1 | 2014-01-06 | 2025-12-29 | 521 | 521 |
| WDOJ26 | 1min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | 5min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | 10min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | 15min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | 20min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | 30min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | 60min | 2025-12-30 | 2025-12-30 | 1 | 10 |
| WDOJ26 | D1 | 2025-12-05 | 2025-12-30 | 10 | 10 |
| WDOJ26 | W1 | 2025-12-05 | 2025-12-29 | 5 | 5 |
| WDOM26 | 5min | 2026-04-02 | 2026-05-12 | 22 | 63 |
| WDOM26 | 10min | 2026-03-31 | 2026-05-12 | 28 | 63 |
| WDOM26 | 15min | 2026-03-25 | 2026-05-12 | 31 | 63 |
| WDOM26 | 20min | 2026-03-23 | 2026-05-14 | 35 | 64 |
| WDOM26 | 30min | 2026-03-09 | 2026-05-12 | 38 | 63 |
| WDOM26 | 60min | 2026-03-03 | 2026-05-12 | 47 | 63 |
| WDOM26 | D1 | 2026-02-03 | 2026-05-14 | 64 | 64 |

**Leituras importantes**

- **1 min** (timeframe do robô atual): só existe WINFUT de 2025-09-26 a 2025-12-30 (64 sessões completas) e WINQ26 de 2026-02-13 a 2026-07-24, onde só a parte final é líquida (35 sessões completas). Total ≈ 99 sessões; não há 1 min para 2024, para o WINM26 nem para o WINV26.
- **5 min contínuo** começa em 2024-06-19; 10/15/20/30/60 min e diário começam em 2014 (60 min/diário), 2018 (20/30 min), 2020 (15 min), 2022 (10 min).
- Faltam de 2026-05-15 a 2026-06-17 em contrato líquido (WINM26 termina em 2026-05-14) e **tudo após 2026-07-24** (o contrato atual é WINV26; não há CSV).
- Arquivos com exatamente 10.000 linhas foram truncados pelo limite de exportação do Profit (§4).

## 4. Qualidade por arquivo

**Possível truncamento por limite de exportação (10.000 linhas)**

| lote | arquivo | linhas | inicio | fim |
|---|---|---|---|---|
| 2018-2019 | WDOFUT_F_0_20min.csv | 10.000 | 2018-07-05 | 2019-12-30 |
| 2018-2019 | WINFUT_F_0_20min.csv | 10.000 | 2018-07-05 | 2019-12-30 |

**Arquivos com > 20% de sessões ralas** (tipicamente contratos ainda sem liquidez):

| lote | arquivo | sessoes | sessoes_completas | % ralas |
|---|---|---|---|---|
| 2024-2025 | WDOJ26_F_0_10min.csv | 10 | 1 | 90 |
| 2024-2025 | WDOJ26_F_0_15min.csv | 10 | 1 | 90 |
| 2024-2025 | WDOJ26_F_0_1min.csv | 10 | 1 | 90 |
| 2024-2025 | WDOJ26_F_0_20min.csv | 10 | 1 | 90 |
| 2024-2025 | WDOJ26_F_0_30min.csv | 10 | 1 | 90 |
| 2024-2025 | WDOJ26_F_0_5min.csv | 10 | 1 | 90 |
| 2024-2025 | WDOJ26_F_0_60min.csv | 10 | 1 | 90 |
| 2026-1S_M26 | WDOM26_F_0_10min.csv | 63 | 28 | 55,6 |
| 2026-1S_M26 | WDOM26_F_0_15min.csv | 63 | 31 | 50,8 |
| 2026-1S_M26 | WDOM26_F_0_20min.csv | 64 | 35 | 45,3 |
| 2026-1S_M26 | WDOM26_F_0_30min.csv | 63 | 38 | 39,7 |
| 2026-1S_M26 | WDOM26_F_0_5min.csv | 63 | 22 | 65,1 |
| 2026-1S_M26 | WDOM26_F_0_60min.csv | 63 | 47 | 25,4 |
| 2024-2025 | WINJ26_F_0_10min.csv | 90 | 7 | 92,2 |
| 2024-2025 | WINJ26_F_0_15min.csv | 90 | 7 | 92,2 |
| 2024-2025 | WINJ26_F_0_1min.csv | 90 | 7 | 92,2 |
| 2024-2025 | WINJ26_F_0_20min.csv | 90 | 8 | 91,1 |
| 2024-2025 | WINJ26_F_0_30min.csv | 90 | 9 | 90 |
| 2024-2025 | WINJ26_F_0_5min.csv | 90 | 7 | 92,2 |
| 2024-2025 | WINJ26_F_0_60min.csv | 90 | 32 | 64,4 |
| 2026-1S_M26 | WINM26_F_0_10min.csv | 90 | 58 | 35,6 |
| 2026-1S_M26 | WINM26_F_0_15min.csv | 90 | 58 | 35,6 |
| 2026-1S_M26 | WINM26_F_0_20min.csv | 90 | 58 | 35,6 |
| 2026-1S_M26 | WINM26_F_0_30min.csv | 90 | 59 | 34,4 |
| 2026-1S_M26 | WINM26_F_0_5min.csv | 90 | 58 | 35,6 |
| 2026-1S_M26 | WINM26_F_0_60min.csv | 90 | 69 | 23,3 |
| 2026-2S_Q26 | WINQ26_F_0_10min.csv | 109 | 70 | 35,8 |
| 2026-2S_Q26 | WINQ26_F_0_15min.csv | 115 | 75 | 34,8 |
| 2026-2S_Q26 | WINQ26_F_0_1min.csv | 109 | 35 | 67,9 |
| 2026-2S_Q26 | WINQ26_F_0_20min.csv | 109 | 70 | 35,8 |
| 2026-2S_Q26 | WINQ26_F_0_30min.csv | 109 | 70 | 35,8 |
| 2026-2S_Q26 | WINQ26_F_0_5min.csv | 109 | 69 | 36,7 |
| 2026-2S_Q26 | WINQ26_F_0_60min.csv | 109 | 75 | 31,2 |

**Séries cujos timeframes terminam em datas diferentes** (exportações feitas em momentos distintos; use a interseção ao comparar timeframes):

| serie | lote | fim mais antigo | fim mais recente | dias de diferença |
|---|---|---|---|---|
| WINQ26 | 2026-2S_Q26 | 2026-07-24 | 2026-08-03 | 10 |

**Barras de 1 min com range zero** (O=H=L=C; ausência de negócio no minuto, não erro):

| lote | arquivo | linhas | range_zero |
|---|---|---|---|
| 2024-2025 | WDOJ26_F_0_1min.csv | 64 | 54 |
| 2024-2025 | WINJ26_F_0_1min.csv | 5.129 | 2.711 |
| 2026-2S_Q26 | WINQ26_F_0_1min.csv | 35.574 | 4.269 |

## 5. Consistência entre fontes

### 5.1 Entre timeframes (mesma série padrão, agregando o timeframe menor)

Percentual de barras cujo OHLC/quantidade coincide exatamente com a agregação do timeframe menor (rótulo de abertura).

| serie | de | para | barras_comuns | o_igual_pct | h_igual_pct | l_igual_pct | c_igual_pct | q_igual_pct |
|---|---|---|---|---|---|---|---|---|
| WINFUT | 1min | 5min | 7.329 | 100,0 | 100,0 | 100 | 100 | 100,0 |
| WINFUT | 5min | 15min | 14.606 | 100 | 100 | 100 | 100 | 100,0 |
| WINFUT | 5min | 30min | 7.305 | 100,0 | 100 | 100,0 | 100 | 100,0 |
| WINFUT | 5min | 60min | 3.846 | 100,0 | 100,0 | 100,0 | 100 | 100,0 |
| WDOFUT | 1min | 5min | 3.363 | 100,0 | 100,0 | 100 | 100 | 100,0 |
| WDOFUT | 5min | 15min | 14.455 | 100,0 | 100,0 | 100 | 100 | 100,0 |
| WDOFUT | 5min | 30min | 7.228 | 100,0 | 100,0 | 100 | 100 | 100,0 |
| WDOFUT | 5min | 60min | 3.804 | 100,0 | 100 | 100 | 100 | 100,0 |
| WINQ26 | 1min | 5min | 8.428 | 100 | 100 | 100 | 100 | 100 |

Conclusão: preços e quantidade são coerentes entre timeframes. O **volume financeiro** (`Volume`) **não é aditivo** entre timeframes (≈ quantidade × preço × R$ 0,20 com preço de referência específico da barra); para features de volume use `Quantidade` ou o mesmo timeframe de origem.

### 5.2 Série padrão × exportação ajustada (`*_alt`)

| serie | tf | barras_comuns | inicio | fim | Δ fech. mín | Δ fech. mediana | Δ fech. máx | quantidade igual % |
|---|---|---|---|---|---|---|---|---|
| WINFUT | 5min | 33.592 | 2024-10-18 | 2025-12-30 | 5.713,9 | 6.292,5 | 7.191,1 | 100 |
| WINFUT | 10min | 28.498 | 2024-01-02 | 2025-12-30 | 5.715,9 | 6.416,1 | 7.186,8 | 100 |
| WINFUT | 15min | 19.001 | 2024-01-02 | 2025-12-30 | 5.715,9 | 6.416,1 | 7.191,1 | 100 |
| WINFUT | 20min | 14.501 | 2024-01-02 | 2025-12-30 | 5.724,0 | 6.416,0 | 7.186,8 | 100 |
| WINFUT | 30min | 9.502 | 2024-01-02 | 2025-12-30 | 5.715,9 | 6.416,1 | 7.182,7 | 100 |
| WINFUT | 60min | 5.002 | 2024-01-02 | 2025-12-30 | 5.728,1 | 6.415,4 | 7.175,3 | 100 |
| WINFUT | D1 | 501 | 2024-01-02 | 2025-12-30 | 5.728,1 | 6.419,0 | 7.168,9 | 100 |

A quantidade é idêntica, mas o nível de preço difere em milhares de pontos e a diferença **deriva ao longo do tempo** (ajuste de rolagem). Consequências: (i) pontos de SL/TP e ATR são comparáveis, níveis absolutos não; (ii) misturar as bases cria saltos falsos; (iii) `carregar_serie()` usa só a base padrão por omissão.

### 5.3 Contrato × contínuo (basis)

| contrato | continuo | tf | barras_comuns | dias_comuns | dias_liquidos | primeiro_dia_liquido | dif_mediana | dif_p5 | dif_p95 |
|---|---|---|---|---|---|---|---|---|---|
| WINJ26 | WINFUT | 5min | 2.424 | 90 | 7 | 2025-12-18 | 15 | -43,8 | 78 |
| WINJ26 | WINFUT | 15min | 1.381 | 90 | 7 | 2025-12-18 | 15 | -42,8 | 75,5 |
| WDOJ26 | WDOFUT | 5min | 49 | 10 | 1 | 2025-12-30 | 0,1 | -4,3 | 6,7 |
| WDOJ26 | WDOFUT | 15min | 42 | 10 | 1 | 2025-12-30 | 2,5 | -8,2 | 8,8 |

O contínuo (`WINFUT`/`WDOFUT`) troca de contrato na rolagem; o contrato explícito (J26, M26, Q26) tem liquidez irregular antes de virar o vencimento mais próximo.

## 6. Saltos de rolagem e gaps overnight (WINFUT, diário)

120 aberturas com gap ≥ 1,5% sobre o fechamento anterior (rolagens e eventos de mercado se confundem).

| data | fech. anterior | abertura | gap % |
|---|---|---|---|
| 2021-02-22 | 184.702 | 186.085 | -4,4 |
| 2021-08-19 | 190.435 | 185.853 | -1,5 |
| 2021-09-20 | 176.996 | 176.181 | -1,8 |
| 2021-11-26 | 163.288 | 164.469 | -3,1 |
| 2022-02-24 | 175.022 | 171.530 | -2,2 |
| 2022-06-13 | 156.845 | 158.065 | -1,8 |
| 2022-06-17 | 151.478 | 154.072 | -2,0 |
| 2022-06-22 | 150.693 | 150.006 | -1,9 |
| 2022-10-03 | 171.659 | 167.821 | 3,1 |
| 2022-10-31 | 169.394 | 162.990 | -3,5 |
| 2024-03-08 | 160.081 | 159.077 | -1,7 |
| 2024-08-05 | 152.609 | 149.807 | -2,4 |
| 2025-04-04 | 144.337 | 146.655 | -1,6 |
| 2025-04-07 | 142.347 | 142.075 | -1,6 |
| 2025-05-12 | 153.884 | 155.754 | 1,5 |

Rolagens do WIN: meses pares (G, J, M, Q, V, Z), vencimento na quarta-feira mais próxima do dia 15. Estratégias intradiárias não são afetadas; qualquer análise overnight/diária precisa excluir ou ajustar essas datas.

## 7. Barras com volume extremo (para inspeção antes de usar como evidência)

**WINFUT 1min** — maiores razões quantidade/média(20):

| dt | o | h | l | c | q | range/ATR20 | q/média20 |
|---|---|---|---|---|---|---|---|
| 2025-10-01 09:01 | 156.888 | 157.245 | 156.856 | 156.894 | 138.847 | 10,6 | 34,8 |
| 2025-10-10 09:03 | 151.547 | 151.670 | 151.504 | 151.595 | 117.933 | 4,7 | 27,4 |
| 2025-10-23 09:01 | 154.376 | 154.851 | 154.293 | 154.793 | 160.920 | 13,4 | 25,9 |
| 2025-10-27 09:00 | 156.551 | 156.807 | 156.473 | 156.702 | 104.029 | 8,4 | 25,0 |
| 2025-12-16 09:03 | 168.208 | 168.313 | 167.207 | 167.259 | 220.479 | 14,8 | 22,9 |

**WINFUT 5min** — maiores razões quantidade/média(20):

| dt | o | h | l | c | q | range/ATR20 | q/média20 |
|---|---|---|---|---|---|---|---|
| 2024-10-22 09:00 | 154.564 | 154.664 | 153.833 | 153.897 | 640.179 | 12,0 | 18,9 |
| 2025-10-23 09:00 | 154.345 | 155.284 | 154.293 | 155.268 | 516.451 | 13,8 | 16,9 |
| 2025-10-27 09:00 | 156.551 | 156.911 | 156.473 | 156.848 | 382.439 | 7,0 | 14,4 |
| 2024-10-24 09:00 | 153.704 | 153.850 | 153.359 | 153.634 | 541.948 | 5,8 | 13,1 |
| 2024-07-05 09:00 | 154.418 | 154.654 | 153.934 | 154.309 | 395.365 | 10,2 | 13,0 |

**WINM26 5min** — maiores razões quantidade/média(20):

| dt | o | h | l | c | q | range/ATR20 | q/média20 |
|---|---|---|---|---|---|---|---|
| 2026-03-31 16:05 | 192.270 | 192.300 | 191.970 | 192.070 | 4.910 | 1,3 | 76,8 |
| 2026-04-15 09:00 | 202.885 | 203.005 | 202.230 | 202.370 | 226.478 | 5,9 | 54,6 |
| 2026-03-09 10:30 | 185.295 | 185.655 | 185.085 | 185.485 | 3.158 | 1,7 | 47,6 |
| 2026-02-09 09:40 | 192.465 | 192.465 | 192.000 | 192.180 | 201 | 5,4 | 43,7 |
| 2026-02-02 16:05 | 190.110 | 190.135 | 190.110 | 190.135 | 42 | 1,9 | 38,2 |

**WINQ26 1min** — maiores razões quantidade/média(20):

| dt | o | h | l | c | q | range/ATR20 | q/média20 |
|---|---|---|---|---|---|---|---|
| 2026-02-23 15:55 | 200.340 | 200.340 | 200.340 | 200.340 | 24.915 | 0 | 12.457,5 |
| 2026-05-06 14:48 | 194.155 | 194.160 | 193.980 | 194.005 | 2.741 | 6,5 | 527,1 |
| 2026-06-17 09:02 | 172.820 | 172.820 | 172.575 | 172.655 | 69.006 | 4,3 | 319,9 |
| 2026-04-16 11:16 | 205.330 | 205.330 | 205.155 | 205.200 | 1.474 | 2,7 | 176,5 |
| 2026-06-09 18:14 | 173.650 | 173.650 | 173.610 | 173.610 | 1.014 | 2,5 | 143,8 |

Picos de volume na abertura (09:00–09:03) e em leilões são esperados; picos fora desses horários merecem checagem de unidade, rolagem ou notícia antes de entrar em estatísticas.

## 8. Recomendações

1. **Exportar 1 min do WINFUT (ou do contrato líquido de cada período) para 2024-01 → 2025-09 e 2026-01 → hoje**; sem isso o motor M02 (1 min) fica com poucas dezenas de sessões líquidas (ver §3).
2. **Exportar WINV26** (contrato atual) e fechar a janela 2026-05-15 → 2026-06-17 com o contrato líquido (WINM26 até o vencimento).
3. Padronizar a exportação: sempre **sem ajuste de preço**, sempre incluindo `Quantidade`, um arquivo por (série, timeframe) cobrindo o intervalo total, e anotar o período no nome (`WINFUT_F_0_1min_2024-01-02_2025-12-30.csv`).
4. Nas análises, usar `tradetech.carregar_serie(serie, tf)`: concatena lotes, remove duplicatas e exclui a base ajustada. Não usar globs recursivos sobre `dados/candles` (misturariam bases).
5. Preferir `Quantidade` (contratos) a `Volume` financeiro em features de esforço.

