# M19 — Estrutura diária e semanal (momentum, NR7, vencimento, dia anterior)

| Campo | Valor |
|---|---|
| Status | ATIVO — ANALISE_001 concluída: **0 de 10 testes passam**; 1 quase-acerto pré-registrado (DD-H05) |
| Instrumentos / timeframes | WINFUT (decide) e WDOFUT (replica), D1 e W1 (semanal montada a partir do D1), 2014–2025 |
| Tese | Um trade por dia tem margem sobre o custo muito maior que os modelos de 30 e 60 min; se a estrutura diária tem direção, ela aparece aqui |
| Reúne | candidatos M08 (momentum/reversão), M10 (compressão), M14 (vencimentos) do catálogo |
| Método | [`METODO.md`](METODO.md) · Hipóteses: [`HIPOTESES.md`](HIPOTESES.md) (DD-H01 a DD-H05) |
| Análise | [`analises/ANALISE_001_estrutura_diaria.md`](analises/ANALISE_001_estrutura_diaria.md) |
| Código | `codigo/dd_motor.py` (células; reaproveita as estatísticas do M18) · `codigo/analise_001.py` |

## Resultado em uma tela

- **Momentum/reversão (DD-H01), compressão (DD-H02) e semana do vencimento (DD-H03): refutadas.** Maior `|t|` de 1,2 a 1,9 na descoberta; sinais trocam entre períodos.
- **Dia anterior (DD-H04): refutada pela regra congelada, mas é quase-acerto.** O dia seguinte tende a reverter a posição do fechamento de ontem: −12,9 pb (t −2,61) na descoberta, −11,7 pb (t −2,44) no hold-out, −8,3 pb (t −3,40) no WDO, 9 de 12 anos, margem 30,9 sobre o custo. 2022 e 2023 têm sinal oposto.
- A regra `|t| ≥ 3` não foi relaxada. A célula virou **DD-H05**, pré-registrada: só se confirma em dado que não entrou nos 10 testes (WINFUT D1 anterior a 2014 ou 2026 líquido).

## Reprodução por ano

`ANALISE_001_por_ano.csv` e a seção 3 do relatório trazem a média de cada célula em cada ano. Com dado novo no `WINFUT` D1, `python3 motores/M19_estrutura_diaria/codigo/analise_001.py` acrescenta o ano como coluna.

## Como rodar

```bash
python3 motores/M19_estrutura_diaria/codigo/analise_001.py
```
