# Índice da documentação

| Documento | Para quê |
|---|---|
| [`01_CONVENCOES.md`](01_CONVENCOES.md) | regras comuns: IDs, ciclo de hipótese, dados, estatística, deltas |
| [`02_ESTRUTURA_PASTAS.md`](02_ESTRUTURA_PASTAS.md) | árvore, mapa antigo → novo, onde colocar cada coisa |
| [`03_CATALOGO_MOTORES.md`](03_CATALOGO_MOTORES.md) | motores existentes e candidatos a explorar (com viabilidade nos dados) |
| [`INDICE_HIPOTESES.md`](INDICE_HIPOTESES.md) | (gerado) todas as hipóteses de todos os motores com veredito |
| [`auditorias/AUDITORIA_DADOS.md`](auditorias/AUDITORIA_DADOS.md) | (gerado) qualidade e cobertura dos candles |
| [`templates/`](templates) | `HIPOTESE`, `DELTA`, `ANALISE`, `FICHA_MOTOR` |
| [`teoria/`](teoria) | notas teóricas |

## Motores

| Motor | Entrada |
|---|---|
| M01 — F = m·a | [`motores/M01_fma_forca/README.md`](../motores/M01_fma_forca/README.md) |
| M02 — Microestrutura com barreiras | [`motores/M02_microestrutura_barreiras/README.md`](../motores/M02_microestrutura_barreiras/README.md) |
| M16 — Confluência de cor multi-TF | [`motores/M16_confluencia_multitf/README.md`](../motores/M16_confluencia_multitf/README.md) |

## Rotina de trabalho (resumo)

1. **Dados novos?** Colocar em `dados/candles/<lote>/` e rodar `python ferramentas/auditar_candles.py`.
2. **Ideia nova?** Registrar como hipótese no `HIPOTESES.md` do motor (ou linha no catálogo de motores).
3. **Mudança no robô?** `deltas/DELTA_###_*.md` (uma alavanca) → medir contra o baseline → decidir.
4. **Fim do dia:** `python ferramentas/indexar_hipoteses.py` para atualizar o índice único e `python ferramentas/gerar_painel.py` para atualizar o painel ([`painel/painel.html`](painel/painel.html), abrir no navegador; precisa de internet para o Plotly).

## Comandos úteis

```bash
pip install -r requirements.txt
python -m unittest discover tests                                   # testes
python ferramentas/auditar_candles.py                               # auditoria de dados (~20 s)
python motores/M02_microestrutura_barreiras/codigo/analise_001.py   # baseline M02 (~15 s)
python motores/M16_confluencia_multitf/codigo/analise_001.py       # confluência multi-TF (~30 s)
python ferramentas/gerar_painel.py                                # painel HTML interativo: docs/painel/painel.html (usa --refazer para recalcular o cache do M02)
python ferramentas/indexar_hipoteses.py                             # índice de hipóteses
```
