# Estrutura de pastas

```
.
├── README.md                      ponto de entrada
├── pyproject.toml / requirements.txt
├── dados/
│   ├── README.md                  contrato dos dados
│   ├── catalogo_candles.csv       (gerado) um registro por arquivo
│   └── candles/<lote>/            CSVs Profit imutáveis
├── src/tradetech/                 código compartilhado (leitor canônico, utilidades)
├── tests/                         testes dos simuladores e do leitor
├── ferramentas/                   scripts transversais (auditoria de dados, git helpers)
├── docs/
│   ├── 00_INDICE.md
│   ├── 01_CONVENCOES.md
│   ├── 02_ESTRUTURA_PASTAS.md     (este arquivo)
│   ├── 03_CATALOGO_MOTORES.md     motores existentes e candidatos
│   ├── 04_REGISTRO_ANALISES.md    (gerado) análises classificadas
│   ├── 05_TRILHA_ROBO.md          decisão do que entra no robô
│   ├── registro/analises.csv      fonte do registro
│   ├── ano_foco/<ano>/RETRATO.md  (gerado) comportamento do ano
│   ├── auditorias/                relatórios gerados sobre os dados
│   ├── teoria/                    notas teóricas
│   └── templates/                 HIPOTESE, DELTA, ANALISE, FICHA_MOTOR
├── motores/
│   ├── M01_fma_forca/             F = m·a, cores, áreas, reversão (legado rico)
│   │   ├── README.md              ficha + índice unificado das hipóteses H01–H48
│   │   ├── teses/{cores,areas,reversao}/
│   │   ├── robos/                 NTSL V10–V18 + RAID_LOG + Results/
│   │   └── backtests_legados/
│   └── M02_microestrutura_barreiras/
│       ├── README.md              ficha do motor
│       ├── METODO.md              convenções da simulação
│       ├── HIPOTESES.md           MB-H01…
│       ├── REVISAO_CODIGO_NTSL.md revisão do fonte (riscos/decisões)
│       ├── robo/                  fontes NTSL versionados
│       ├── codigo/                simulador Python + scripts de análise
│       ├── analises/              ANALISE_###_*.md + CSVs gerados
│       └── deltas/                DELTA_###_*.md
├── diario/                        notas operacionais
└── estudo_visual/                 material visual (capturas)
```

Regra de ouro: **um motor = uma pasta autocontida** com `robo/`, `codigo/`, `analises/`, `deltas/`, `HIPOTESES.md`. Dados e código compartilhado ficam fora dos motores.

## Mapa antigo → novo

### Dados

| Antes | Depois | Observação |
|---|---|---|
| `CandlesHistoryDatas/2012_14`, `2014_16` | `dados/candles/2014-2015` | o conteúdo cobre 2014-2015; `2014_16` era cópia idêntica (md5) |
| `…/2016_18` | `dados/candles/2016-2017` | |
| `…/2018_20` | `dados/candles/2018-2019` | |
| `…/2020_22` | `dados/candles/2020-2021` | |
| `…/2022_24` | `dados/candles/2022-2023` | |
| `…/2024_26` | `dados/candles/2024-2025` | inclui 1/5/10/15/20/30/60 min e D1/W1 |
| `…/2024_26/2026`, `…/2026` (WINM26/WDOM26) | `dados/candles/2026-1S_M26` | |
| `…/2026` (WINFUT/WINFUTV com datas), `CandlesHistoricos2026/WINFUT_*` | `dados/candles/2024-2025_alt` | preço **ajustado**; fora das análises por padrão |
| `CandlesHistoricos2026/WINQ26_*` | `dados/candles/2026-2S_Q26` | |
| `CandlesHistoryDatas/CandlesHistoryDatas/**`, `CandlesHistoryDatas.zip` | removidos | cópias idênticas (verificadas por md5) |
| `CandlesHistoryDatas/analises_antigas` | `motores/M01_fma_forca/backtests_legados` | |
| `CandlesHistoryDatas/roboAtual20261022.md` | `motores/M02_microestrutura_barreiras/robo/Robo_Microestrutura_Barreiras_v1_20261022.ntsl` | robô atual |

### Código, robôs e teses

| Antes | Depois |
|---|---|
| `Robots/**` | `motores/M01_fma_forca/robos/**` |
| `TeseFma_analiseCandle/**` (cores) | `motores/M01_fma_forca/teses/cores/` |
| `TeseFma_areas`, `TeseFma_reversao` | `motores/M01_fma_forca/teses/{areas,reversao}/` |
| `Notes/*` | `backtests_legados/` e `robos/HISTORICO-RESULTADOS.md` |
| `README.md` (guia operacional WIN) | `motores/M01_fma_forca/robos/GUIA_OPERACIONAL_WIN.md` (o novo `README.md` é o índice) |
| `DailyNotesOperations/WIN.md` | `diario/WIN.md` |
| `ScreenToStudy_MaterOfTrades/**` | `estudo_visual/` |
| `gitCommands/*` | `ferramentas/git/` |

O histórico completo de renomeações está no git (`git log --follow -M`). Os scripts do M01 já foram atualizados para os novos caminhos; a leitura de dados dos scripts legados (`backtests_legados/`) continua usando as pastas-padrão antigas por nome de lote.

## Onde colocar cada coisa nova

| Tenho… | Coloco em… |
|---|---|
| Novo export de candles | `dados/candles/<lote>/` + `python ferramentas/auditar_candles.py` |
| Nova hipótese do motor X | linha em `motores/X/HIPOTESES.md` (template `docs/templates/HIPOTESE.md`) |
| Nova análise | `motores/X/codigo/analise_###.py` → `motores/X/analises/ANALISE_###_*.md` |
| Mudança proposta no robô | `motores/X/deltas/DELTA_###_*.md` (template `docs/templates/DELTA.md`) |
| Nova versão do robô | `motores/X/robo/<Nome>_v<N>_<data>.ntsl` |
| Ideia de motor novo | linha em `docs/03_CATALOGO_MOTORES.md`; pasta só quando virar `ATIVO` |
| Utilidade usada por ≥ 2 motores | `src/tradetech/` + teste em `tests/` |
