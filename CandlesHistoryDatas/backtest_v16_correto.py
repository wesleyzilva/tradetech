"""
Backtest WIN 15min — força F=MA com parser CORRETO
Parser fix: preços 2020-2025 usam '.' como milhar → remover antes de parsear
Execute: C:/Program Files/Python312/python.exe backtest_v16_correto.py
"""
import csv
import glob
from collections import deque


def parse_num(s):
    """Remove separador de milhar (.) e converte decimal (,) → ponto."""
    return float(s.strip().replace(".", "").replace(",", "."))


def carregar_csv(path):
    rows = []
    for enc in ["latin-1", "utf-8", "cp1252"]:
        try:
            with open(path, encoding=enc) as f:
                for row in csv.reader(f, delimiter=";"):
                    if len(row) < 9:
                        continue
                    try:
                        rows.append({
                            "date":  row[1].strip(),
                            "time":  row[2].strip()[:5],
                            "open":  parse_num(row[3]),
                            "high":  parse_num(row[4]),
                            "low":   parse_num(row[5]),
                            "close": parse_num(row[6]),
                            "vol":   parse_num(row[8]),
                        })
                    except:
                        pass
            return rows
        except:
            pass
    return rows


def carregar_todos():
    arquivos = sorted(glob.glob("**/WIN*_F_0_15min.csv", recursive=True))
    all_c = []
    for a in arquivos:
        all_c.extend(carregar_csv(a))
    all_c.sort(key=lambda r: (
        r["date"].split("/")[2] + r["date"].split("/")[1] +
        r["date"].split("/")[0],
        r["time"]
    ))
    seen = set()
    candles = []
    for c in all_c:
        k = (c["date"], c["time"])
        if k not in seen:
            seen.add(k)
            candles.append(c)
    return candles


def backtest(candles, F_FORTE=70, F_EXAUST=85, SL=822, TP2=2466, TP3=2466,
             MA_VOL=20, MAX_BARRAS=20, STOP_H=17, STOP_M=45, filtro_vol=True,
             hora_ini=None, hora_fim=None, nivel_min=2):
    vol_buf = deque(maxlen=MA_VOL)
    prev_f = 0.0
    results = []
    for i, c in enumerate(candles):
        vol_buf.append(c["vol"])
        vm = sum(vol_buf) / len(vol_buf) if vol_buf else 1
        corpo = c["close"] - c["open"]
        rng = max(c["high"] - c["low"], 0.0001)
        f = max(-100.0, min(100.0, (corpo / rng) * (c["vol"] / vm) * 100))
        hm = int(c["time"][:2]) * 60 + int(c["time"][3:5])
        ok_hora = (hora_ini is None) or (hora_ini * 60 <= hm < hora_fim * 60)
        ok_stop = hm < STOP_H * 60 + STOP_M
        nivel = 0
        if ok_hora and ok_stop and abs(f) >= F_FORTE and abs(prev_f) < F_FORTE:
            v_ok = (not filtro_vol) or (
                (corpo > 0 and c["vol"] >= vm) if f > 0
                else (corpo < 0 and c["vol"] >= vm)
            )
            if v_ok:
                nivel = 3 if abs(f) >= F_EXAUST else 2
        if nivel >= nivel_min:
            tp = TP3 if nivel == 3 else TP2
            d = 1 if f > 0 else -1
            ent = c["close"]
            pnl = None
            tipo = ""
            for j in range(i + 1, min(i + 1 + MAX_BARRAS, len(candles))):
                nc = candles[j]
                t2 = int(nc["time"][:2]) * 60 + int(nc["time"][3:5])
                sh = nc["low"] <= ent - \
                    SL if d == 1 else nc["high"] >= ent + SL
                th = nc["high"] >= ent + \
                    tp if d == 1 else nc["low"] <= ent - tp
                if sh and th:
                    pnl = -SL
                    tipo = "SL"
                    break
                elif th:
                    pnl = tp
                    tipo = "TP"
                    break
                elif sh:
                    pnl = -SL
                    tipo = "SL"
                    break
                elif t2 >= STOP_H * 60 + STOP_M or j == min(i + MAX_BARRAS, len(candles) - 1):
                    pnl = (nc["close"] - ent) * d
                    tipo = "TMP"
                    break
            if pnl is not None:
                yr = int(c["date"].split("/")[2])
                results.append(
                    {"nivel": nivel, "pnl": pnl, "tipo": tipo, "ano": yr})
        prev_f = f
    return results


def pr(results, label, SL, TP2, TP3, niveis=(2, 3)):
    for nv in niveis:
        tp = TP3 if nv == 3 else TP2
        t = [x for x in results if x["nivel"] == nv]
        if not t:
            continue
        tot = len(t)
        w = sum(1 for x in t if x["pnl"] > 0)
        pnl = sum(x["pnl"] for x in t)
        be = SL / (SL + tp) * 100
        wr = w / tot * 100
        tp_n = sum(1 for x in t if x["tipo"] == "TP")
        sl_n = sum(1 for x in t if x["tipo"] == "SL")
        tm_n = sum(1 for x in t if x["tipo"] == "TMP")
        e = "✓" if pnl > 0 else "✗"
        print(f"  Nv{nv} {label:42s}| n={tot:5d} WR={wr:5.1f}% be={be:4.1f}% "
              f"PnL={pnl:+10.0f} [TP:{tp_n:3d} SL:{sl_n:4d} TMP:{tm_n:4d}] {e}")


if __name__ == "__main__":
    candles = carregar_todos()
    print(
        f"Total: {len(candles)} candles | {candles[0]['date']} → {candles[-1]['date']}\n")

    print("CENARIO RECOMENDADO — SL=822 TP=2466 RR3 MAX=20 (params historicos otimos)")
    r = backtest(candles)
    pr(r, "SL=822 TP=2466 MAX=20", 822, 2466, 2466)
    print("\nPor ano Nv3:")
    for ano in sorted(set(x["ano"] for x in r if x["nivel"] == 3)):
        yr = [x["pnl"] for x in r if x["nivel"] == 3 and x["ano"] == ano]
        w = sum(1 for p in yr if p > 0)
        print(
            f"  {ano}: n={len(yr):4d} WR={w/len(yr)*100:4.1f}% PnL={sum(yr):+9.0f}")
