# Tradetech — pesquisa de motores quantitativos para WIN/WDO

Repositório de pesquisa: candles do Profit + robôs NTSL + simuladores Python + registro canônico de hipóteses. A ideia é evoluir cada **motor** por *deltas* pequenos, medidos contra um baseline reproduzível.

## Comece por aqui

| Quero… | Vá para |
|---|---|
| entender as regras e a estrutura | [`docs/00_INDICE.md`](docs/00_INDICE.md) |
| ver a situação do robô atual (M02, NTSL de 22/10/2026) | [`motores/M02_microestrutura_barreiras/README.md`](motores/M02_microestrutura_barreiras/README.md) |
| ver todas as hipóteses e vereditos | [`docs/INDICE_HIPOTESES.md`](docs/INDICE_HIPOTESES.md) |
| ver outros motores que podem ser explorados | [`docs/03_CATALOGO_MOTORES.md`](docs/03_CATALOGO_MOTORES.md) |
| saber se os candles fazem sentido | [`docs/auditorias/AUDITORIA_DADOS.md`](docs/auditorias/AUDITORIA_DADOS.md) |
| propor uma mudança no robô | `docs/templates/DELTA.md` → `motores/<motor>/deltas/` |

## Estrutura

```
dados/candles/<lote>/   CSVs Profit imutáveis (+ catalogo_candles.csv gerado)
src/tradetech/          leitor canônico de candles
motores/M01_fma_forca/  F = m·a: cores, áreas, reversão, robôs V10–V18
motores/M02_microestrutura_barreiras/   robô atual de 1 min + simulador + baseline
docs/                   convenções, catálogo de motores, auditorias, templates
ferramentas/            auditoria de dados, índice de hipóteses
tests/                  testes dos simuladores
```

## Reproduzir

```bash
pip install -r requirements.txt
python -m unittest discover tests
python ferramentas/auditar_candles.py
python motores/M02_microestrutura_barreiras/codigo/analise_001.py
python ferramentas/indexar_hipoteses.py
```

O guia operacional antigo do WIN (parâmetros dos robôs M01) está em [`motores/M01_fma_forca/robos/GUIA_OPERACIONAL_WIN.md`](motores/M01_fma_forca/robos/GUIA_OPERACIONAL_WIN.md).
