import csv
from collections import deque

# ─── Parametros V16 ───────────────────────────────────────────
SL = 75.0
TP2 = 150.0   # nivel 2: forte 70-85   RR 2.0
TP3 = 188.0   # nivel 3: exaustao >=85 RR 2.5
F_FORTE = 70.0
F_EXAUSTAO = 85.0
MA_VOL = 20
MAX_BARRAS = 6
STOP_H, STOP_M = 17, 45


def parse_time(t):
    h, m, s = t.split(":")
    return int(h) * 60 + int(m)


candles = []
with open("2026/WINM26_F_0_15min.csv", encoding="utf-8") as f:
    for row in csv.reader(f, delimiter=";"):
        if len(row) < 9:
            continue
        try:
            candles.append({
                "date": row[1], "time": row[2],
                "open":  float(row[3].replace(",", ".")),
                "high":  float(row[4].replace(",", ".")),
                "low":   float(row[5].replace(",", ".")),
                "close": float(row[6].replace(",", ".")),
                "vol":   float(row[8].replace(",", "."))
            })
        except:
            pass

candles.sort(key=lambda r: (r["date"].split(
    "/")[2]+r["date"].split("/")[1]+r["date"].split("/")[0], r["time"]))

vol_buf = deque(maxlen=MA_VOL)
prev_f = 0.0
results = []

i = 0
while i < len(candles):
    c = candles[i]
    vol_buf.append(c["vol"])
    vol_media = sum(vol_buf) / len(vol_buf) if vol_buf else 1

    corpo = c["close"] - c["open"]
    rng = c["high"] - c["low"]
    if rng <= 0:
        rng = 0.0001
    massa = corpo / rng
    acel = c["vol"] / vol_media if vol_media > 0 else 0
    f = max(-100.0, min(100.0, massa * acel * 100))

    t_min = parse_time(c["time"])
    apos_stop = (t_min >= STOP_H * 60 + STOP_M)

    nivel = 0
    if not apos_stop and abs(f) >= F_FORTE and abs(prev_f) < F_FORTE:
        vol_ok = (corpo > 0 and c["vol"] >= vol_media) if f > 0 else \
                 (corpo < 0 and c["vol"] >= vol_media)
        if vol_ok:
            nivel = 3 if abs(f) >= F_EXAUSTAO else 2

    if nivel > 0:
        tp_alvo = TP3 if nivel == 3 else TP2
        direcao = 1 if f > 0 else -1
        entrada = c["close"]
        pnl = None
        barras = 0

        for j in range(i + 1, min(i + 1 + MAX_BARRAS, len(candles))):
            nc = candles[j]
            t2 = parse_time(nc["time"])
            barras += 1

            if direcao == 1:
                sl_hit = nc["low"] <= entrada - SL
                tp_hit = nc["high"] >= entrada + tp_alvo
            else:
                sl_hit = nc["high"] >= entrada + SL
                tp_hit = nc["low"] <= entrada - tp_alvo

            if sl_hit and tp_hit:
                pnl = -SL
            elif tp_hit:
                pnl = tp_alvo
            elif sl_hit:
                pnl = -SL
            elif t2 >= STOP_H * 60 + STOP_M or barras >= MAX_BARRAS:
                pnl = (nc["close"] - entrada) * direcao
                break

            if pnl is not None:
                break

        if pnl is None:
            pnl = 0.0

        results.append((nivel, pnl, c["date"], c["time"], round(f, 1)))

    prev_f = f
    i += 1

# ─── Estatísticas ─────────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  BACKTEST V16 — WIN 15min 2026")
print(f"  SL={SL}pts | TP2={TP2}pts (RR2.0) | TP3={TP3}pts (RR2.5)")
print(f"  Filtro: corpo direcional + Volume >= MA{MA_VOL}")
print(f"{'='*55}")

total_pnl = 0
for nv, label, tp_alvo in [(2, "FORTE     (70-85)", TP2), (3, "EXAUSTAO  (>=85) ", TP3)]:
    trades = [(p, d, t, fv) for n, p, d, t, fv in results if n == nv]
    if not trades:
        print(f"\n  Nivel {nv} — sem sinais")
        continue
    total = len(trades)
    wins = sum(1 for p, *_ in trades if p > 0)
    pnl_t = sum(p for p, *_ in trades)
    wr = wins / total * 100
    avg_w = sum(p for p, *_ in trades if p > 0) / wins if wins else 0
    avg_l = sum(p for p, *_ in trades if p <= 0) / \
        (total-wins) if total-wins > 0 else 0
    min_wr = SL / (SL + tp_alvo) * 100
    total_pnl += pnl_t

    print(f"\n  Nivel {nv} — {label}")
    print(f"  {'─'*45}")
    print(f"  Trades         : {total}")
    print(f"  Win rate       : {wr:.1f}%   (break-even: {min_wr:.1f}%)")
    print(f"  Ganhos/Perdas  : {wins} / {total - wins}")
    print(f"  PnL total      : {pnl_t:+.0f} pts")
    print(
        f"  Avg win        : {avg_w:+.1f} pts  |  Avg loss: {avg_l:+.1f} pts")
    print(f"  Resultado      : {'✓ LUCRATIVO' if pnl_t > 0 else '✗ NEGATIVO'}")

print(f"\n{'='*55}")
print(f"  PnL TOTAL (ambos niveis): {total_pnl:+.0f} pts")
print(f"  Total candles analisados: {len(candles)}")
print(f"{'='*55}\n")
