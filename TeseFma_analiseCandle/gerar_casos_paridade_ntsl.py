"""Prepare a fixed ten-case Python reference batch for manual Profit/NTSL parity.

Run from any working directory with the repository's configured Python environment:
    python TeseFma_analiseCandle/gerar_casos_paridade_ntsl.py

The selected WINQ26 5-minute timestamps are stratified across neutral/dark/bright states
and near-threshold/broad-threshold examples. They are diagnostic parity cases, not a
performance sample and not evidence of profitability.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent
DATA_FILE = REPO_ROOT / "CandlesHistoryDatas" / "CandlesHistoricos2026" / "WINQ26_F_0_5min.csv"
OUT_FILE = BASE / "PARIDADE_NTSL_CASOS.csv"
PREVIOUS_BARS = 39

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from TeseFma_analiseCandle.analise_candles import SIMBOLO, calcular, ler_csv  # noqa: E402

CASES = [
    ("P10", "2026-06-01 10:20:00", "vermelho brilhante; intensidade intermediária"),
    ("P03", "2026-06-11 13:10:00", "verde escuro próximo de +1.5σ"),
    ("P01", "2026-06-15 09:20:00", "neutro; z próximo de zero"),
    ("P05", "2026-06-23 13:05:00", "verde brilhante próximo de +2.5σ"),
    ("P02", "2026-07-01 14:05:00", "neutro imediatamente abaixo de -1.5σ"),
    ("P07", "2026-07-03 13:25:00", "vermelho escuro próximo de -1.5σ"),
    ("P06", "2026-07-08 09:00:00", "verde brilhante; evento intenso para testar escala/volume"),
    ("P04", "2026-07-09 11:00:00", "verde escuro próximo de +1.5σ"),
    ("P09", "2026-07-10 14:15:00", "vermelho brilhante próximo de -2.5σ"),
    ("P08", "2026-07-13 09:20:00", "vermelho escuro próximo de -2.5σ"),
]

PROFIT_VISUAL_COLUMNS = [
    "profit_visual_timestamp", "profit_candle_no", "profit_visual_o", "profit_visual_h",
    "profit_visual_l", "profit_visual_c", "profit_visual_indicator",
    "profit_visual_indicator_scale", "evidence_screenshot", "profit_capture_notes",
]

# Transcrição do print P01 anexado pelo usuário em 2026-10-07.
# Os valores numéricos internos do motor (m/a/F/mu/sigma/z) não são expostos no Profit.
PROFIT_VISUAL_OBSERVATIONS = {
    "P01": {
        "profit_visual_timestamp": "2026-06-15 09:20:00",
        "profit_candle_no": 5,
        "profit_visual_o": 176420.0,
        "profit_visual_h": 176480.0,
        "profit_visual_l": 176150.0,
        "profit_visual_c": 176315.0,
        "profit_visual_indicator": "FORCA_WIN_ESTUDO_FMA",
        "profit_visual_indicator_scale": "Escala e plots visíveis; valores do eixo não tratados como valores da barra selecionada.",
        "evidence_screenshot": "anexo_conversa_2026-10-07_P01",
        "profit_capture_notes": "Timestamp, candle 5 e OHLC legíveis; sem Data Window/valores internos do motor.",
        "profit_bar_time_basis": "Tooltip mostra 09:20; Profit não explicita no print se timestamp é abertura ou fechamento.",
        "comparison_status": "VISUAL_SOMENTE",
    }
}


def main() -> None:
    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Arquivo WINQ26 requerido não encontrado: {DATA_FILE}")

    raw = ler_csv(DATA_FILE)
    calculated = calcular(raw)
    raw_positions = pd.Series(range(len(raw)), index=raw["dt"])
    candle_number_by_time = pd.Series(
        raw.groupby(raw["dt"].dt.normalize()).cumcount().to_numpy() + 1,
        index=raw["dt"],
    )
    calculated_by_time = calculated.set_index("dt", drop=False)
    output_rows = []

    for case_id, timestamp, reason in CASES:
        target = pd.Timestamp(timestamp)
        if target not in calculated_by_time.index:
            raise ValueError(f"Timestamp do caso {case_id} não existe na série calculada: {target}")
        row = calculated_by_time.loc[target]
        if isinstance(row, pd.DataFrame):
            raise ValueError(f"Timestamp duplicado no caso {case_id}: {target}")
        source_rows_before = int(raw_positions.loc[target])
        if source_rows_before < PREVIOUS_BARS:
            raise ValueError(
                f"Caso {case_id} tem somente {source_rows_before} barras anteriores; "
                f"são necessárias {PREVIOUS_BARS}."
            )
        context_start_index = source_rows_before - PREVIOUS_BARS
        context_start = raw.iloc[context_start_index]
        previous_bar = raw.iloc[source_rows_before - 1]

        est = int(row["est"])
        output = {
            "case_id": case_id,
            "asset": "WINQ26",
            "timeframe": "5min",
            "source_file": DATA_FILE.name,
            "timestamp": target.strftime("%Y-%m-%d %H:%M:%S"),
            "candle_no_python": int(candle_number_by_time.loc[target]),
            "source_rows_before_target": source_rows_before,
            "context_bars_required": PREVIOUS_BARS,
            "context_start_timestamp": context_start["dt"].strftime("%Y-%m-%d %H:%M:%S"),
            "context_start_candle_no": int(candle_number_by_time.loc[context_start["dt"]]),
            "previous_bar_timestamp": previous_bar["dt"].strftime("%Y-%m-%d %H:%M:%S"),
            "same_session_bars_before": int(candle_number_by_time.loc[target]) - 1,
            "o": row["o"],
            "h": row["h"],
            "l": row["l"],
            "c": row["c"],
            "v": row["v"],
            "rng": row["rng"],
            "m": row["m"],
            "a": row["a"],
            "F": row["F"],
            "mu": row["mu"],
            "sigma": row["sd"],
            "z": row["z"],
            "fam": int(row["fam"]),
            "est": est,
            "cor_python": SIMBOLO[est],
            "limiar_escuro_sigma": 1.5,
            "limiar_brilhante_sigma": 2.5,
            "caso_objetivo": reason,
            "profit_visual_status": "EVIDENCIA_VISUAL_RECEBIDA" if case_id in PROFIT_VISUAL_OBSERVATIONS else "AGUARDANDO_EVIDENCIA_VISUAL",
            "comparison_status": "PENDENTE",
            "profit_bar_time_basis": "",
        }
        output.update({column: "" for column in PROFIT_VISUAL_COLUMNS})
        output.update(PROFIT_VISUAL_OBSERVATIONS.get(case_id, {}))
        output_rows.append(output)

    result = pd.DataFrame(output_rows)
    result.to_csv(OUT_FILE, sep=";", index=False, encoding="utf-8-sig", decimal=",")
    print(f"Arquivo de referência gravado: {OUT_FILE}")
    print(f"Casos: {len(result)}; todos têm {PREVIOUS_BARS} barras de contexto disponíveis antes do alvo.")
    print(result[["case_id", "timestamp", "candle_no_python", "context_start_timestamp", "context_start_candle_no", "est"]].to_string(index=False))


if __name__ == "__main__":
    main()
