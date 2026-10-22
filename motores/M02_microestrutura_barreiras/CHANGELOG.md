# M02 — Changelog

## 2026-10-22
- **Robô v1** (`robo/Robo_Microestrutura_Barreiras_v1_20261022.ntsl`): versão recebida, sem alterações.
- **Simulador** `codigo/mb_motor.py` + `tests/test_mb_motor.py` (12 testes).
- **ANALISE_001** (baseline): sem vantagem estatística detectável; ver `HIPOTESES.md`.
- Revisão do código NTSL registrada em `REVISAO_CODIGO_NTSL.md`.
- **ANALISE_002** (risco/retorno por timeframe, geometria como nulo, cor como alarme): `codigo/analise_002_timeframes.py`; `Params.gap_max_min` para TFs > 10 min.
- `Params.stop_a_mercado` (implementa a mecânica do `DELTA_001` no simulador, sem alterar o baseline: padrão `False`); usado pelo M16.
