"""
Backtest fiel do FORCA_WIN_V16_scalper_sinaisForca.

Objetivo:
- Simular WIN 5min com a mesma ordem de gestao do robo NTSL.
- Separar motivos de saida: SL, stop contra, BE, trailing, TP, max barras e horario.
- Manter foco operacional exclusivamente em WIN.

Execute a partir de CandlesHistoryDatas:
  C:/Program Files/Python312/python.exe backtest_win_scalper_fiel.py
"""

from __future__ import annotations

import csv
import glob
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path


F_FORTE = 70.0
F_EXAUSTAO = 85.0
F_ALERTA = 55.0
MA_VOL = 20

SL = 280.0
TP_NIVEL_2 = 560.0
TP_NIVEL_3 = 840.0
BREAK_EVEN_RATIO = 0.333
TRAILING_PCT_INICIAL = 0.62
TRAILING_PCT_PISO = 0.10

STOP_H = 17
STOP_M = 45
MAX_BARRAS = 12
CANDLES_BRANCOS_BE = 5
FORCA_STOP_CONTRA = 70.0
FORCA_MIN_BE_COR_OPOSTA = 70.0
BLOQUEAR_REENTRADA_MESMO_CANDLE = True


@dataclass
class Candle:
    date: str
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class Position:
    direction: int
    entry: float
    sl: float
    tp: float
    level: int
    entry_date: str
    entry_time: str
    entry_force: float
    bars: int = 0
    break_even: bool = False
    trailing_ref: float = 0.0
    white_bars: int = 0


@dataclass
class Trade:
    level: int
    direction: int
    entry_date: str
    entry_time: str
    exit_date: str
    exit_time: str
    entry_force: float
    reason: str
    pnl: float


def parse_num(value: str) -> float:
    return float(value.strip().replace(".", "").replace(",", "."))


def parse_minutes(time_value: str) -> int:
    hour, minute = time_value[:5].split(":")
    return int(hour) * 60 + int(minute)


def sort_key(candle: Candle) -> tuple[str, str]:
    day, month, year = candle.date.split("/")
    return year + month + day, candle.time


def load_csv(path: str) -> list[Candle]:
    rows: list[Candle] = []
    for encoding in ("latin-1", "utf-8", "cp1252"):
        try:
            with open(path, encoding=encoding, newline="") as file:
                for row in csv.reader(file, delimiter=";"):
                    if len(row) < 9 or row[0].strip().lower() == "ativo":
                        continue
                    try:
                        rows.append(
                            Candle(
                                date=row[1].strip(),
                                time=row[2].strip()[:5],
                                open=parse_num(row[3]),
                                high=parse_num(row[4]),
                                low=parse_num(row[5]),
                                close=parse_num(row[6]),
                                # Mantem a mesma convencao dos backtests existentes: Quantidade.
                                volume=parse_num(row[8]),
                            )
                        )
                    except (ValueError, IndexError):
                        continue
            return rows
        except UnicodeDecodeError:
            continue
    return rows


def load_win_5min(base_dir: Path) -> list[Candle]:
    paths = sorted(
        glob.glob(str(base_dir / "**" / "WIN*_F_0_5min.csv"), recursive=True))
    all_rows: list[Candle] = []
    for path in paths:
        all_rows.extend(load_csv(path))

    all_rows.sort(key=sort_key)
    seen: set[tuple[str, str]] = set()
    candles: list[Candle] = []
    for candle in all_rows:
        key = (candle.date, candle.time)
        if key in seen:
            continue
        seen.add(key)
        candles.append(candle)
    return candles


def force_and_zone(candle: Candle, vol_media: float) -> tuple[float, int, float]:
    body = candle.close - candle.open
    candle_range = max(candle.high - candle.low, 0.0001)
    force = (body / candle_range) * \
        (candle.volume / max(vol_media, 1.0)) * 100.0
    force = max(-100.0, min(100.0, force))

    if force >= F_EXAUSTAO:
        zone = 3
    elif force >= F_FORTE:
        zone = 2
    elif force >= F_ALERTA:
        zone = 1
    elif force <= -F_EXAUSTAO:
        zone = -3
    elif force <= -F_FORTE:
        zone = -2
    elif force <= -F_ALERTA:
        zone = -1
    else:
        zone = 0
    return force, zone, body


def close_trade(position: Position, candle: Candle, reason: str, exit_price: float) -> Trade:
    pnl = (exit_price - position.entry) * position.direction
    return Trade(
        level=position.level,
        direction=position.direction,
        entry_date=position.entry_date,
        entry_time=position.entry_time,
        exit_date=candle.date,
        exit_time=candle.time,
        entry_force=position.entry_force,
        reason=reason,
        pnl=pnl,
    )


def run_backtest(
    candles: list[Candle],
    *,
    use_stop_contra: bool = False,
    use_be_force: bool = False,
    use_be_white: bool = False,
    use_be_classic: bool = False,
    use_trailing: bool = False,
    block_same_candle_reentry: bool = True,
) -> list[Trade]:
    vol_buffer: deque[float] = deque(maxlen=MA_VOL)
    previous_force = 0.0
    position: Position | None = None
    trades: list[Trade] = []

    for candle in candles:
        saiu_neste_candle = False
        vol_buffer.append(candle.volume)
        vol_media = sum(vol_buffer) / len(vol_buffer)
        force, zone, body = force_and_zone(candle, vol_media)
        minutes = parse_minutes(candle.time)
        stop_minutes = STOP_H * 60 + STOP_M
        deve_operar = minutes < stop_minutes

        if position is not None and not deve_operar:
            trades.append(close_trade(position, candle,
                          "STOP_HORARIO", candle.close))
            position = None
            saiu_neste_candle = True

        if position is not None:
            position.bars += 1
        else:
            # Espelha reset do robo quando esta flat.
            pass

        if position is not None and position.bars >= MAX_BARRAS:
            trades.append(close_trade(position, candle,
                          "MAX_BARRAS", candle.close))
            position = None
            deve_operar = False
            saiu_neste_candle = True

        if position is not None:
            if position.direction == 1 and candle.low <= position.entry - position.sl:
                trades.append(close_trade(position, candle, "SL",
                              position.entry - position.sl))
                position = None
                saiu_neste_candle = True
            elif position.direction == -1 and candle.high >= position.entry + position.sl:
                trades.append(close_trade(position, candle, "SL",
                              position.entry + position.sl))
                position = None
                saiu_neste_candle = True

        if position is not None and use_stop_contra:
            if position.direction == 1 and force <= -FORCA_STOP_CONTRA:
                trades.append(close_trade(position, candle,
                              "STOP_CONTRA", candle.close))
                position = None
                saiu_neste_candle = True
            elif position.direction == -1 and force >= FORCA_STOP_CONTRA:
                trades.append(close_trade(position, candle,
                              "STOP_CONTRA", candle.close))
                position = None
                saiu_neste_candle = True

        if position is not None:
            if zone == 0:
                position.white_bars += 1
            else:
                position.white_bars = 0

            if use_be_force and not position.break_even:
                if position.direction == 1 and force <= -FORCA_MIN_BE_COR_OPOSTA:
                    position.break_even = True
                elif position.direction == -1 and force >= FORCA_MIN_BE_COR_OPOSTA:
                    position.break_even = True

            if use_be_white and not position.break_even and position.white_bars >= CANDLES_BRANCOS_BE:
                position.break_even = True

        if position is not None and use_be_classic:
            if not position.break_even:
                current_profit = (
                    candle.close - position.entry) * position.direction
                if current_profit >= position.tp * BREAK_EVEN_RATIO:
                    position.break_even = True

            if position.break_even:
                if position.direction == 1 and candle.close <= position.entry:
                    trades.append(close_trade(
                        position, candle, "BE", candle.close))
                    position = None
                    saiu_neste_candle = True
                elif position.direction == -1 and candle.close >= position.entry:
                    trades.append(close_trade(
                        position, candle, "BE", candle.close))
                    position = None
                    saiu_neste_candle = True

        if position is not None and position.break_even and use_trailing:
            current_profit = (candle.close - position.entry) * \
                position.direction
            trail_step = (position.tp - current_profit) * TRAILING_PCT_INICIAL
            trail_floor = position.tp * TRAILING_PCT_PISO
            if trail_step < trail_floor:
                trail_step = trail_floor

            if position.direction == 1:
                new_ref = candle.close - trail_step
                if new_ref > position.trailing_ref:
                    position.trailing_ref = new_ref
                if position.trailing_ref > position.entry and candle.low <= position.trailing_ref:
                    trades.append(close_trade(position, candle,
                                  "TRAILING", position.trailing_ref))
                    position = None
                    saiu_neste_candle = True
            elif position.direction == -1:
                new_ref = candle.close + trail_step
                if position.trailing_ref == 0 or new_ref < position.trailing_ref:
                    position.trailing_ref = new_ref
                if position.trailing_ref < position.entry and candle.high >= position.trailing_ref:
                    trades.append(close_trade(position, candle,
                                  "TRAILING", position.trailing_ref))
                    position = None
                    saiu_neste_candle = True

        if position is not None:
            if position.direction == 1 and candle.high >= position.entry + position.tp:
                trades.append(close_trade(position, candle, "TP",
                              position.entry + position.tp))
                position = None
                saiu_neste_candle = True
            elif position.direction == -1 and candle.low <= position.entry - position.tp:
                trades.append(close_trade(position, candle, "TP",
                              position.entry - position.tp))
                position = None
                saiu_neste_candle = True

        can_enter = deve_operar and (position is None) and (
            (not block_same_candle_reentry) or (not saiu_neste_candle)
        )
        if can_enter:
            long_signal = force >= F_FORTE and previous_force < F_FORTE
            short_signal = force <= -F_FORTE and previous_force > -F_FORTE
            long_volume_ok = body > 0 and candle.volume >= vol_media
            short_volume_ok = body < 0 and candle.volume >= vol_media

            if long_signal and long_volume_ok:
                level = 3 if force >= F_EXAUSTAO else 2
                tp = TP_NIVEL_3 if level == 3 else TP_NIVEL_2
                position = Position(
                    direction=1,
                    entry=candle.close,
                    sl=SL,
                    tp=tp,
                    level=level,
                    entry_date=candle.date,
                    entry_time=candle.time,
                    entry_force=force,
                    trailing_ref=candle.close - SL,
                )
            elif short_signal and short_volume_ok:
                level = 3 if force <= -F_EXAUSTAO else 2
                tp = TP_NIVEL_3 if level == 3 else TP_NIVEL_2
                position = Position(
                    direction=-1,
                    entry=candle.close,
                    sl=SL,
                    tp=tp,
                    level=level,
                    entry_date=candle.date,
                    entry_time=candle.time,
                    entry_force=force,
                    trailing_ref=candle.close + SL,
                )

        previous_force = force

    return trades


def print_summary(label: str, trades: list[Trade], candles: list[Candle]) -> None:
    print("=" * 72)
    print(f"BACKTEST FIEL | {label}")
    print(f"Candles: {len(candles)} | Trades: {len(trades)}")
    if candles:
        print(
            f"Periodo: {candles[0].date} {candles[0].time} -> {candles[-1].date} {candles[-1].time}")
    print(
        f"SL={SL:.0f} | TP2={TP_NIVEL_2:.0f} | TP3={TP_NIVEL_3:.0f} | MAX={MAX_BARRAS}")
    print("=" * 72)

    if not trades:
        return

    total_pnl = sum(trade.pnl for trade in trades)
    wins = sum(1 for trade in trades if trade.pnl > 0)
    losses = sum(1 for trade in trades if trade.pnl < 0)
    flats = len(trades) - wins - losses
    print(f"Total PnL: {total_pnl:+.0f} pts")
    print(
        f"Win rate : {wins / len(trades) * 100:.1f}% | wins={wins} losses={losses} flat={flats}")

    print("\nPor nivel:")
    for level in (2, 3):
        scoped = [trade for trade in trades if trade.level == level]
        if not scoped:
            continue
        pnl = sum(trade.pnl for trade in scoped)
        win_count = sum(1 for trade in scoped if trade.pnl > 0)
        print(
            f"  Nv{level}: n={len(scoped):5d} WR={win_count / len(scoped) * 100:5.1f}% "
            f"PnL={pnl:+10.0f} pts"
        )

    print("\nPor motivo de saida:")
    counts = Counter(trade.reason for trade in trades)
    for reason, count in counts.most_common():
        scoped = [trade for trade in trades if trade.reason == reason]
        pnl = sum(trade.pnl for trade in scoped)
        avg = pnl / count
        print(f"  {reason:13s} n={count:5d} PnL={pnl:+10.0f} avg={avg:+8.1f}")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    candle_rows = load_win_5min(base)
    profiles = [
        (
            "ATUAL: SL/TP/MAX/horario puro (sem BE/trailing/stop contra)",
            dict(use_stop_contra=False, use_be_force=False,
                 use_be_white=False, use_be_classic=False, use_trailing=False),
        ),
        (
            "BE classico apenas + SL/TP/MAX/horario",
            dict(use_stop_contra=False, use_be_force=False,
                 use_be_white=False, use_be_classic=True, use_trailing=False),
        ),
        (
            "BE classico + trailing (sem stop contra/forca/brancos)",
            dict(use_stop_contra=False, use_be_force=False,
                 use_be_white=False, use_be_classic=True, use_trailing=True),
        ),
        (
            "SEM stop contra e SEM BE por forca; BE 5 brancos + trailing",
            dict(use_stop_contra=False, use_be_force=False,
                 use_be_white=True, use_be_classic=True, use_trailing=True),
        ),
        (
            "SEM BE por forca; stop contra + BE 5 brancos + trailing",
            dict(use_stop_contra=True, use_be_force=False,
                 use_be_white=True, use_be_classic=True, use_trailing=True),
        ),
        (
            "SEM stop contra; BE adaptativo + trailing",
            dict(use_stop_contra=False, use_be_force=True,
                 use_be_white=True, use_be_classic=True, use_trailing=True),
        ),
        (
            "LEGADO: stop contra + BE adaptativo + trailing",
            dict(use_stop_contra=True, use_be_force=True,
                 use_be_white=True, use_be_classic=True, use_trailing=True),
        ),
    ]
    for profile_label, kwargs in profiles:
        result_trades = run_backtest(candle_rows, **kwargs)
        print_summary(profile_label, result_trades, candle_rows)
        print()
