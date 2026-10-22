# Dados

## Contrato

- `candles/<lote>/*.csv`: exports do Profit, **imutáveis**. Lotes nomeados pela cobertura real (ver [`../docs/02_ESTRUTURA_PASTAS.md`](../docs/02_ESTRUTURA_PASTAS.md) para o mapa das pastas antigas).
- `catalogo_candles.csv`: gerado por `python ferramentas/auditar_candles.py` — uma linha por arquivo (cobertura, sessões completas, qualidade, md5).
- Leitura **sempre** via `src/tradetech/dados.py`:

```python
import sys; sys.path.insert(0, "src")
from tradetech.dados import carregar_serie, catalogo_arquivos

d = carregar_serie("WINFUT", "5min")            # concatena lotes, remove duplicatas, exclui séries ajustadas
d = carregar_serie("WINQ26", "1min")            # contrato específico
cat = catalogo_arquivos()                        # quais arquivos existem
```

Colunas devolvidas: `dt` (abertura da barra), `o h l c`, `v` (volume **financeiro**), `q` (quantidade de contratos), `lote`.

## Formato Profit

`;` como separador, `latin-1`, ordem descendente no arquivo, números no formato brasileiro (`1.234,50`), timestamps de **abertura** da barra. O leitor normaliza tudo.

## Regras

1. Não editar nem duplicar CSVs; não colocar cópias em outras pastas.
2. Nome do lote = intervalo real coberto. Novo export de um período já coberto vira novo lote (ex.: `2024-2025_v2`) — o leitor deduplica por timestamp.
3. Exportar **sem ajuste de preço**, incluindo `Quantidade`, um arquivo por (série, timeframe) no intervalo completo; anotar o período no nome quando possível.
4. `*_alt` (preço ajustado) não entra nas análises: diferença de 5.700–7.200 pts no WIN.
5. Contratos específicos (`WINJ26`, `WINM26`, `WINQ26`…) são séries separadas; o contínuo (`WINFUT`) tem *gaps* de rolagem.

## Lacunas conhecidas (prioridade)

1. 1 min de WIN: 2024-01 → 2025-09 e 2026-01 → hoje (hoje só 99 pregões).
2. WINV26 (contrato atual) e fechamento da janela 2026-05-15 → 2026-06-17.
3. 1 min de WDO além de 29 pregões.
4. Trades/ticks de alguns pregões (para calibrar fill/slippage — motor M15 no catálogo).

Relatório completo: [`../docs/auditorias/AUDITORIA_DADOS.md`](../docs/auditorias/AUDITORIA_DADOS.md).
