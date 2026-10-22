# DELTA_002 — Cooldown entre trades e teto diário de operações

| Campo | Valor |
|---|---|
| Motor | M02 |
| Baseline | `ANALISE_001` / robô v1 |
| Status | PROPOSTO |
| Hipóteses | MB-H07 |
| Alavanca única | frequência de entrada: `cooldown_barras` (esperar N barras após a saída) e `max_trades_dia` |

## Motivação

~30 trades por pregão em 1 min. Com sinal sem edge detectável, a frequência só multiplica o custo (ANALISE_001 §4). Reduzir a frequência é a única forma de reduzir custo sem acreditar no sinal.

## Mudança

NTSL: contador `vTradesDia` e `vBarrasDesdeSaida`; `Se vTradesDia < MaxTradesDia E vBarrasDesdeSaida >= Cooldown`. Simulador: parâmetros novos em `Params` (a implementar), default = comportamento v1 (`0` e `None`).

## Medição (congelada antes de rodar)

- Grade **pré-declarada** (6 combinações): `cooldown ∈ {0, 10, 30}` × `max_trades_dia ∈ {None, 8}`.
- Conjuntos: WINFUT 1 min (descoberta) e WINQ26 1 min (validação); custo de 2 pts.
- Métrica primária: PnL total por pregão com custo; **o resultado é comparado com o nulo aleatório de mesma frequência**, para que reduzir frequência não seja confundido com melhorar o sinal.
- Decisão: ADOTAR apenas se a melhor combinação na descoberta melhora também na validação e supera o p95 do nulo; caso contrário REJEITAR (o efeito esperado é só menos prejuízo, não lucro).

## Resultado

—

## Decisão

—
