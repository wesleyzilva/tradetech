# M01 — Força F = m·a (cores, áreas, reversão)

| Campo | Valor |
|---|---|
| Status | ATIVO — fase descritiva consolidada; fase operacional (entradas/saídas) ainda não validada |
| Instrumentos / timeframes | WIN e WDO; foco 5 e 15 min (também 10/20/30/60) |
| Tese | Um candle é um "evento de força" `F = m·a` (m = (C−O)/(H−L) mede a eficiência do corpo; a = volume ÷ média do horário mede o esforço). Padronizada por z-score (Bollinger 1,5σ/2,5σ) resulta nos estados *neutro / escuro (ignição) / brilhante (saturação)* |
| Sinal | estados de cor; clusters/áreas (ART/ACT/ARC/ACC); reversão (contrapressão) |
| Robôs | `robos/` (V10 → V18), versão viva `FORCA_WIN_V16_scalper_sinaisForca` |
| Hipóteses | H01–H48 (cores), A01–A08 (áreas), R01 (reversão) — índice único em [`docs/INDICE_HIPOTESES.md`](../../docs/INDICE_HIPOTESES.md) |

## O que a evidência já sustenta

| Achado | Hipóteses | Veredito |
|---|---|---|
| m e a são dimensões distintas; esforço produz deslocamento (lei de impacto β ≈ 0,7) | H02, H03 | CONFIRMADA |
| Brilhante **antecipa expansão de volatilidade** (range seguinte 1,44× em 5 min, 1,15× em 15 min) | H20 | CONFIRMADA |
| Absorção (a ≥ 2, |m| < 0,3) tem atividade e persistência próprias | H29 | CONFIRMADA (com split temporal) |
| Neutro não tem edge direcional | H21 | CONFIRMADA |
| A cor **não** carrega direção estável (continuação/exaustão) | H05, H18, H19 | INCONCLUSIVA / NÃO SUPORTADA |
| 80/20 de energia não vale; 70 ≈ P79 (percentil disfarçado); auto-inclusão da janela mascara extremos | H06, H07, H15 | REFUTADA / CONFIRMADA |
| Bollinger restabelece a hierarquia ignição < saturação | H09, H10 | CONFIRMADA |

**Leitura consolidada:** o motor é um excelente descritor de **regime de atividade** (quando algo vai acontecer), não de **direção**. O caminho consistente é usar a cor como filtro/dimensionador de risco e buscar direção em contexto (TF maior, área, horário) — daí as teses de áreas e reversão e os candidatos M05/M09/M11 do catálogo.

## Mapa

| Pasta | Conteúdo |
|---|---|
| `teses/cores/` | teoria, scripts, `HIPOTESES.md` (painel automático), validações, paridade NTSL × Python |
| `teses/areas/` | hipóteses A01–A08 (confirmação multi-timeframe) |
| `teses/reversao/` | hipótese R01 (contrapressão) |
| `robos/` | fontes NTSL V10–V18, `RAID_LOG.md`, `HISTORICO-RESULTADOS.md`, `Results/` do simulador, `GUIA_OPERACIONAL_WIN.md` (antigo README) |
| `backtests_legados/` | scripts de backtest/diagnóstico anteriores (leem `dados/candles/` pelos lotes padrão) |

## Como reproduzir (exemplos)

```bash
python -m motores.M01_fma_forca.teses.cores.validacao_econofisica   # regrava o painel de HIPOTESES.md
python -m motores.M01_fma_forca.teses.cores.analise_candles
```

## Pendências para o próximo ciclo

1. **H32:** repetir H06–H20 em 2020–2024 (há 15 min desde 2020-11 e 30/60 min desde 2014; 5 min só desde 2024-06).
2. **H44–H48** (exploratórias): primeira cor após neutro, decaimento pós-saturação, estratos de esforço, anatomia (pavios), robustez entre séries. Congelar regra antes (template `docs/templates/HIPOTESE.md`) e **gerar a análise como script** (`codigo/` do motor ou da tese).
3. **H33/H34/H35/H36–H38** — entradas e saídas: só depois de existir um simulador com testes (como o do M02) e controle nulo; hoje os robôs V16–V18 só têm resultados do simulador do Profit.
4. **Unificar o painel automático** com o formato `deltas/` (hoje as mudanças de robô vivem em `robos/CHANGELOG.md` e `RAID_LOG.md`).
5. Nota: o painel automático de `teses/cores/HIPOTESES.md` ainda cita as pastas antigas de dados (`2024_26`, `2026`, `CandlesHistoricos2026`) no cabeçalho gerado; ele se atualiza na próxima execução do script.
