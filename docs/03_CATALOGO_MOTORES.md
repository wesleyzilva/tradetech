# Catálogo de motores

Motores existentes e **candidatos** a explorar com os candles que temos. Cada candidato tem uma hipótese nuclear, o teste mínimo (com controle nulo) e a viabilidade medida pelos dados reais. Quando um candidato for iniciado, criar `motores/M##_nome/` a partir de `docs/templates/FICHA_MOTOR.md`.

## 1. Dados disponíveis (resumo; detalhes em `docs/auditorias/AUDITORIA_DADOS.md`)

| Série | Timeframe | Cobertura | Pregões completos | Uso |
|---|---|---|---|---|
| WIN / WDO contínuos | 60 e 30 min | 2014-01 → 2025-12 | ~2.900 | sazonalidade, regimes, tendência intradia de 12 anos |
| WIN / WDO contínuos | 20 min | 2018-07 → 2025-12 | ~1.850 | idem, com mais barras por pregão |
| WIN / WDO contínuos | 15 min | 2020-11 → 2025-12 | ~1.280 | padrões intradia de 5,5 anos |
| WIN / WDO contínuos | 10 min | 2022-08 → 2025-12 | ~830 | |
| WIN / WDO contínuos | 5 min | 2024-06 → 2025-12 | ~380 | + WINM26 (2026-1S), WINQ26 (2026-2S) |
| WIN / WDO | 1 min | WIN 2025-09 → 2025-12 (64) + WINQ26 2026-05 → 07 (35); WDO 29 | ~100 | só testes de execução/microestrutura |
| WIN / WDO | D1 / W1 | 2014 → 2025 | ~2.900 dias | tendência, sazonalidade, gaps |

Restrições que valem para todos: contínuo com *gaps* de rolagem; `Volume` financeiro (usar `Quantidade`); nenhum dado de book/ticks/ofertas; WIN e WDO compartilham calendário (permite análises cruzadas); o `_alt` (preço ajustado) fica fora.

**Regra de poder estatístico (aproximada):** para detectar um efeito de 0,05 desvio-padrão por trade com |t| ≥ 3 são necessários ≈ 3.600 eventos independentes. Em 1 min isso não existe; em 15–60 min (≥ 1.200 pregões) existe para eventos ≥ 3 por pregão. Isso define a prioridade abaixo.

## 2. Motores existentes

| ID | Nome | Status | Veredito vigente | Onde |
|---|---|---|---|---|
| M01 | Força F = m·a (cores, áreas, reversão) | ATIVO | descritivo robusto (H20, H29 confirmadas); sem edge direcional (H05, H18, H19, H21) | `motores/M01_fma_forca/` |
| M02 | Microestrutura com barreiras (WIN 1 min) | ATIVO | sem vantagem detectável; execução frágil | `motores/M02_microestrutura_barreiras/` |

Índice de todas as hipóteses: [`INDICE_HIPOTESES.md`](INDICE_HIPOTESES.md).

## 3. Candidatos

Prioridade: **P1** = barato, dados abundantes e prior razoável; **P2** = interessante, dados parcialmente suficientes; **P3** = só com dados novos.

| ID prov. | Prefixo | Motor candidato | Hipótese nuclear (enunciado testável) | Dados | Teste mínimo e controle | Prior | Prio |
|---|---|---|---|---|---|---|---|
| M03 | `OR` | **Abertura: gap e Opening Range** | (a) o gap de abertura (open do pregão − close anterior) se preenche mais que o esperado por acaso; (b) o rompimento da faixa 09:00–09:30 tem continuação até 12:00 | WIN/WDO 5–30 min (2014→2025 em 30 min) | retorno 09:30→12:00 condicional ao rompimento vs mesmo horário em dias sem rompimento; nulo = faixa de mesma largura em dias embaralhados | médio | P1 |
| M04 | `SZ` | **Sazonalidade intradiária e semanal** | o retorno por faixa de horário (e dia da semana/semana do vencimento) tem média ≠ 0 estável entre anos | WIN/WDO 30–60 min (12 anos) | média por faixa × ano; t por pregão; estabilidade em anos pares × ímpares | médio-baixo | P1 |
| M05 | `VR` | **Regime de volatilidade (overlay)** | o range do próximo candle/dia é previsível pelo range recente e pela hora (HAR/EWMA); dimensionar alvo e stop pela previsão aumenta a razão ganho/risco do M01/M02 | tudo (60 min → 5 min) | R² fora da amostra vs modelo ingênuo (média do mesmo horário); depois delta no M02 com SL/SG por previsão | **alto** (M01 H20 já mostra expansão após brilhante) | **P1** |
| M06 | `LL` | **Lead-lag WIN × WDO** | o retorno do WDO (dólar) na barra *t* antecipa o retorno do WIN em *t+1* (correlação negativa, mercado risk-on/off) | WIN e WDO mesmos timestamps, 5–60 min | correlação cruzada com defasagens 0..3 e t por pregão; nulo = defasagem de dias diferentes | médio (efeito pequeno; em 5 min pode estar arbitrado) | P1 |
| M07 | `MO` | **Momentum da primeira hora → resto do pregão** | o retorno 09:00–10:00 tem sinal igual ao do retorno 10:00–17:00 mais frequentemente que 50 % | WIN/WDO 5–30 min | proporção de acertos com IC binomial por pregão; nulo = pares de dias distintos | médio | P1 |
| M08 | `TS` | **Momentum / reversão diária (D1)** | o retorno acumulado de k dias (k = 5, 20, 60) prevê o retorno do próximo dia/semana, ajustado por gaps de rolagem | D1/W1 2014→2025 | regressão com HAC; amostra de 12 anos (~3.000 dias) ⇒ poder baixo; nulo = embaralhar blocos | baixo-médio | P2 |
| M09 | `ES` | **Esforço sem resultado (absorção) como motor próprio** | barras de alto esforço (`Quantidade` ÷ média do horário ≥ 2) e corpo curto (|C−O|/range < 0,3) são seguidas de range ≥ 1,5× e de retorno direcional a favor do lado da absorção | WIN 5–15 min (M01 H29 já confirma o range) | herdar H29/H46; adicionar o teste de **direção** com lado definido pelo pavio dominante (H47) | médio | P2 |
| M10 | `CP` | **Compressão → expansão (NR4/NR7, inside bar)** | após o menor range dos últimos 4–7 candles/dias, o range e a direção do rompimento são maiores que o esperado | WIN D1, 60/30/15 min | razão de range futuro vs controle do mesmo horário; direção = lado do primeiro rompimento | médio-baixo | P2 |
| M11 | `NV` | **Níveis: máx/mín do dia anterior, números redondos, VWAP** | o preço rejeita (reverte ≥ X pts em N barras) mais nesses níveis do que em níveis aleatórios do mesmo espaçamento | WIN 5–15 min | taxa de rejeição em níveis × níveis deslocados aleatoriamente; relaciona com M01 H31 (áreas) | médio-baixo | P2 |
| M12 | `VW` | **Reversão à VWAP intradia** | o afastamento da VWAP da sessão (em z do range) acima de 2σ reverte em N barras mais que o acaso | WIN 5–15 min (VWAP aproximado com `Quantidade` e preço típico) | retorno condicional a z vs z aleatório do mesmo horário; custo explícito | médio-baixo | P2 |
| M13 | `FL` | **Fluxo por barra (delta aproximado)** | a relação corpo × quantidade (m·a do M01) separa barras de continuação e de exaustão por contexto de tendência do TF maior (H05 sugeria contexto) | WIN/WDO 5–15 min | continuação do M01 H05 com contexto; só confirmar se replicar em WDO | médio-baixo | P2 |
| M14 | `VC` | **Calendário de vencimentos** | a semana do vencimento (WIN: quarta mais próxima do dia 15 em meses pares) tem volatilidade/retorno distintos | D1 + 60 min 2014→2025 | média por posição no ciclo, estabilidade por ano | baixo-médio | P2 |
| M15 | `EX` | **Execução e custo (modelo de fill)** | um modelo de slippage por volatilidade e horário reproduz os trades do Profit; define o custo mínimo para qualquer motor intradia | exports de trades do Profit + 1 min | calibração: trades do Profit × simulador; é pré-requisito dos motores intradia | **alto (infra)** | **P1** |
| M17 | `PA` | **Par WIN × WDO (spread/ratio)** | o log-ratio WIN/WDO é estacionário/cointegrado e seu desvio reverte | 30–60 min | ADF/Engle-Granger com janelas deslizantes | baixo (dólar e índice não são cointegrados de forma estável) | P3 |
| M18 | `TK` | **Tape reading / book** | agressão e desequilíbrio de fila antecipam deslocamento | **não há dados** (ticks/book) | — | — | P3 (exige dados) |

Observações:

- **Nenhum candidato é recomendado para o robô** sem passar o ciclo de hipótese → controle nulo → custo → hold-out (`docs/01_CONVENCOES.md`).
- **Ordem sugerida:** M15 (execução/custo) em paralelo com M05 (regime) → M03/M04/M06/M07 (testes baratos, 12 anos em 30–60 min) → os P2 que herdam do M01 (M09, M11, M13) → só depois combinar.
- **Combinações naturais:** M05 (regime) como filtro/dimensionador do M02 e do M01; M03/M07 como contexto direcional para M09/M11.
- **Armadilha comum:** testar muitas janelas/horários e eleger a melhor. Declarar a grade completa antes (convenções §4) e contar os testes.

## 4. Como promover um candidato a motor

1. Criar pasta e ficha: `motores/M##_nome/` com `README.md` (template `FICHA_MOTOR.md`), `HIPOTESES.md`, `METODO.md`, `codigo/`, `analises/`, `deltas/`.
2. Escrever **antes** as hipóteses `<PREFIXO>-H01…` com regra congelada.
3. Implementar a análise em `codigo/analise_001.py` regenerando `analises/ANALISE_001_*.md` e, se houver trades, um simulador com testes em `tests/`.
4. Atualizar este catálogo (status `ATIVO`) e rodar `python ferramentas/indexar_hipoteses.py`.
