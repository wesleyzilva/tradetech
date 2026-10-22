# Índice da documentação

| Documento | Para quê |
|---|---|
| [`01_CONVENCOES.md`](01_CONVENCOES.md) | regras comuns: IDs, ciclo de hipótese, dados, estatística, deltas |
| [`02_ESTRUTURA_PASTAS.md`](02_ESTRUTURA_PASTAS.md) | árvore, mapa antigo → novo, onde colocar cada coisa |
| [`03_CATALOGO_MOTORES.md`](03_CATALOGO_MOTORES.md) | motores existentes e candidatos a explorar (com viabilidade nos dados) |
| [`04_REGISTRO_ANALISES.md`](04_REGISTRO_ANALISES.md) | (gerado) cada análise, com classe e decisão para o robô |
| [`05_TRILHA_ROBO.md`](05_TRILHA_ROBO.md) | o que já pode entrar no robô, a ordem dos próximos passos e a regra do ano foco |
| [`ano_foco/2026/RETRATO.md`](ano_foco/2026/RETRATO.md) | (gerado) comportamento de 2026 comparado com 2014-2019 e 2020-2025 |
| [`INDICE_HIPOTESES.md`](INDICE_HIPOTESES.md) | (gerado) todas as hipóteses de todos os motores com veredito |
| [`auditorias/AUDITORIA_DADOS.md`](auditorias/AUDITORIA_DADOS.md) | (gerado) qualidade e cobertura dos candles |
| [`templates/`](templates) | `HIPOTESE`, `DELTA`, `ANALISE`, `FICHA_MOTOR` |
| [`teoria/`](teoria) | notas teóricas |

- Robôs a construir e o que não vale montar: [`06_ROBOS_A_CONSTRUIR.md`](06_ROBOS_A_CONSTRUIR.md)

## Motores

| Motor | Entrada |
|---|---|
| M01 — F = m·a | [`motores/M01_fma_forca/README.md`](../motores/M01_fma_forca/README.md) |
| M02 — Microestrutura com barreiras | [`motores/M02_microestrutura_barreiras/README.md`](../motores/M02_microestrutura_barreiras/README.md) |
| M16 — Confluência de cor multi-TF | [`motores/M16_confluencia_multitf/README.md`](../motores/M16_confluencia_multitf/README.md) |
| M18 — Estrutura intradiária (abertura, faixas, momentum do dia) | [`motores/M18_estrutura_intradiaria/README.md`](../motores/M18_estrutura_intradiaria/README.md) |
| M17 — Aprendizado com walk-forward (amplitude e lado) | [`motores/M17_aprendizado_walkforward/README.md`](../motores/M17_aprendizado_walkforward/README.md) |

## Rotina de trabalho (resumo)

1. **Dados novos?** Colocar em `dados/candles/<lote>/` e rodar `python ferramentas/auditar_candles.py`.
2. **Ideia nova?** Registrar como hipótese no `HIPOTESES.md` do motor (ou linha no catálogo de motores).
3. **Mudança no robô?** `deltas/DELTA_###_*.md` (uma alavanca) → medir contra o baseline → decidir.
4. **Fim do dia:** `python ferramentas/indexar_hipoteses.py` e `python ferramentas/indexar_analises.py` para atualizar os índices, e `python ferramentas/gerar_painel.py` para o painel ([`painel/painel.html`](painel/painel.html), abrir no navegador; precisa de internet para o Plotly).
5. **Chegou dado de 2026?** Lote `dados/candles/2026-atual/` e `python ferramentas/bateria_ano_foco.py`. A regra de uso está em [`05_TRILHA_ROBO.md`](05_TRILHA_ROBO.md).

## Comandos úteis

```bash
pip install -r requirements.txt
python -m unittest discover tests                                   # testes
python ferramentas/auditar_candles.py                               # auditoria de dados (~20 s)
python motores/M02_microestrutura_barreiras/codigo/analise_001.py   # baseline M02 (~15 s)
python motores/M16_confluencia_multitf/codigo/analise_001.py       # confluência multi-TF (~30 s)
python motores/M16_confluencia_multitf/codigo/analise_002.py       # alinhamento no mesmo instante (~10 s)
python motores/M18_estrutura_intradiaria/codigo/analise_001.py     # estrutura intradiária (~10 s)
python motores/M17_aprendizado_walkforward/codigo/analise_001.py    # walk-forward 2018–2025 e placebo (~15 min)
python motores/M17_aprendizado_walkforward/codigo/analise_002.py    # teste final de 2026 (~5 s)
python ferramentas/gerar_painel.py                                # painel HTML interativo: docs/painel/painel.html (usa --refazer para recalcular o cache do M02)
python ferramentas/indexar_hipoteses.py                             # índice de hipóteses
python ferramentas/indexar_analises.py                              # registro de análises
python ferramentas/bateria_ano_foco.py                              # retrato de 2026 (~15 s)
```
