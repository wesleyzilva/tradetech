# M02 — Microestrutura com barreiras (WIN 1 min)

| Campo | Valor |
|---|---|
| Status | ATIVO — baseline medido, **sem vantagem estatística detectável** |
| Instrumento / timeframe | WIN (mini-índice), 1 min (testado também em 5 min) |
| Tese | O estado de volatilidade da barra (range ÷ ATR20) separa regimes: barras "brilhantes" (≥ 1,7 × ATR) tenderiam a exaustão (fade) e o fluxo neutro (barras < 1,3 × ATR) tenderia a romper em convexidade, com barreira tripla assimétrica (stop 0,5 × ATR, alvo 2,5 × ATR, 20 barras) |
| Sinal | ctx 1: fade de alta brilhante (venda) · ctx 2: fade de baixa brilhante (compra) · ctx 3: rompimento da máx/mín anterior em regime neutro, com SMA20 e cor da barra |
| Saída | stop-limit (`stop ∓ 5 pts`), alvo limitado, tempo (20 barras), zeramento 17:20; piso de 35 pts (SL) e 120 pts (SG) |
| Janelas | 09:15–12:00 e 14:00–16:15 (almoço bloqueado) |
| Robô vigente | [`robo/Robo_Microestrutura_Barreiras_v1_20261022.ntsl`](robo/Robo_Microestrutura_Barreiras_v1_20261022.ntsl) |
| Simulador | [`codigo/mb_motor.py`](codigo/mb_motor.py) (testes: `tests/test_mb_motor.py`) |
| Baseline | [`analises/ANALISE_001_baseline.md`](analises/ANALISE_001_baseline.md); timeframes e cor como alarme: [`ANALISE_002`](analises/ANALISE_002_timeframes_rr.md) |

## Veredito do baseline (ANALISE_001)

- **Bruto, sem custos:** WINFUT 1 min −6,2 pts/trade (t = −2,3), WINQ26 1 min +1,5 pt/trade (28 pregões líquidos, t ≈ 0). O robô fica no percentil 3 do controle de entrada aleatória no WINFUT e no 70 no WINQ26: o sinal não supera o acaso.
- **Com 2 a 5 pts de custo:** negativo nos dois conjuntos.
- **Quase todo o fluxo vem do contexto 3** (≈ 99,2 % dos sinais). Os fades (ctx 1 e 2) quase não disparam por exigirem rompimento da barra brilhante já na barra seguinte.
- **Estrutura de execução:** ~30 trades por pregão; 64 % saem no SL; stop mínimo de 35 pts é ruído em 1 min; stop-limit com offset de 5 pts vira ordem passiva em movimentos rápidos e deixa perdas muito acima do SL nominal (ver `REVISAO_CODIGO_NTSL.md`).
- **Dados:** só ~92 pregões de 1 min existem (64 WINFUT + 28 WINQ26 líquidos; os 7 pregões anteriores de WINQ26 tinham volume de contrato fora do vencimento e saíram, ver `docs/05_TRILHA_ROBO.md`). Conclusões têm incerteza alta; as hipóteses do motor foram escritas para ser retestadas com mais dados.

## Como reproduzir

```bash
pip install -r requirements.txt
python -m unittest tests.test_mb_motor
python motores/M02_microestrutura_barreiras/codigo/analise_001.py   # ~15 s, regenera analises/
```

## Mapa

| Arquivo | Para quê |
|---|---|
| [`METODO.md`](METODO.md) | convenções da simulação (fill, barras, custos, controles) |
| [`HIPOTESES.md`](HIPOTESES.md) | registro MB-H## com vereditos e backlog |
| [`REVISAO_CODIGO_NTSL.md`](REVISAO_CODIGO_NTSL.md) | revisão linha a linha do robô e riscos |
| [`deltas/`](deltas/README.md) | mudanças propostas e decididas (um delta = uma alavanca) |
| [`CHANGELOG.md`](CHANGELOG.md) | versões do robô e do simulador |

## Dados que faltam para decidir

1. Candles de **1 min** de 2024-01 → 2025-09 e 2026-01 → hoje (contrato líquido) — hoje só 99 pregões.
2. **WINV26** (contrato atual).
3. Se possível, **trades/ticks** de alguns pregões para medir o fill real de stop-limit (a maior incerteza do simulador).
4. Backtest do próprio robô no simulador do Profit nos mesmos pregões (paridade `fiel` × Profit).
