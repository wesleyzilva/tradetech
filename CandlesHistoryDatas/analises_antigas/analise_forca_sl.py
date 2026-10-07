"""
Analise Estatistica Completa — F=MA Semaforo
============================================
Responde:
  1. Distribuicao dos valores de Forca (justifica limiar 55 vs outro valor)
  2. Tail behavior: apos F>=threshold, o que acontece nos proximos N candles?
  3. Stop Loss otimo: menor SL que protege com >70% de precisao
  4. Validacao 2 tons vs 3 tons: F fraco (55-70) vs F forte (>70) se comportam diferente?
  5. Gerenciamento de risco: sizing e break-even ideais

Uso:
  python analise_forca_sl.py
  (executar de dentro de DadosCandlesBacktest/)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
PERIODOS_MEDIA = 20        # periodo da media de volume
LIMIAR_FRACO = 55        # inicio da zona sinal (atual)
LIMIAR_FORTE = 70        # segundo checkpoint alerta
LIMIAR_MAXIMO = 85        # zona de exaustao?

# Pares de (arquivo_gatilho, arquivo_direcao, arquivo_contexto) por tripleta
TRIPLETAS = [
    {
        "nome": "WDO 60/30/15",
        "ativo": "WDO",
        "tf_gatilho": "15min",
        "tf_direcao": "30min",
        "tf_contexto": "60min",
        "i_dir": 2,
        "i_ctx": 4,
        "ponto_val": 1.0,   # 1 ponto WDO = R$10 por contrato
    },
    {
        "nome": "WIN 60/30/15",
        "ativo": "WIN",
        "tf_gatilho": "15min",
        "tf_direcao": "30min",
        "tf_contexto": "60min",
        "i_dir": 2,
        "i_ctx": 4,
        "ponto_val": 0.20,  # 1 ponto WIN = R$0.20 por contrato
    },
    {
        "nome": "WDO 30/15/5",
        "ativo": "WDO",
        "tf_gatilho": "5min",
        "tf_direcao": "15min",
        "tf_contexto": "30min",
        "i_dir": 3,
        "i_ctx": 6,
        "ponto_val": 1.0,
    },
    {
        "nome": "WIN 30/15/5",
        "ativo": "WIN",
        "tf_gatilho": "5min",
        "tf_direcao": "15min",
        "tf_contexto": "30min",
        "i_dir": 3,
        "i_ctx": 6,
        "ponto_val": 0.20,
    },
]

# Periodos de dados disponíveis (pastas)
PASTAS = sorted(Path(".").glob("*/"))

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────


def load_csvs(ativo_prefix, tf):
    """Carrega todos os CSVs de um ativo/TF em todas as pastas disponíveis."""
    frames = []
    for pasta in PASTAS:
        for f in pasta.glob(f"*{ativo_prefix}*_{tf}.csv"):
            try:
                df = pd.read_csv(f, sep=";", decimal=",", encoding="latin1",
                                 thousands=".")
                # Estrutura fixa por posição (evita problemas de encoding em acentos):
                # col[0]=Ativo, [1]=Data, [2]=Hora, [3]=Abertura, [4]=Máximo,
                # [5]=Mínimo, [6]=Fechamento, [7]=Volume, [8]=Quantidade
                if len(df.columns) < 8:
                    continue
                col_map = {
                    df.columns[1]: "Data",
                    df.columns[2]: "Hora",
                    df.columns[3]: "Open",
                    df.columns[4]: "High",
                    df.columns[5]: "Low",
                    df.columns[6]: "Close",
                    df.columns[7]: "Volume",
                }
                df = df.rename(columns=col_map)
                df["datetime"] = pd.to_datetime(
                    df["Data"] + " " + df["Hora"], dayfirst=True, errors="coerce"
                )
                df = df.dropna(subset=["datetime"]).sort_values(
                    "datetime").reset_index(drop=True)
                for col in ["Open", "Close", "High", "Low"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                df["Volume"] = pd.to_numeric(
                    df["Volume"], errors="coerce").fillna(0)
                df = df.dropna(subset=["Open", "Close", "High", "Low"])
                frames.append(
                    df[["datetime", "Open", "High", "Low", "Close", "Volume"]])
            except Exception as e:
                print(f"  [SKIP] {f}: {e}")
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames).sort_values("datetime").drop_duplicates("datetime")
    out = out.reset_index(drop=True)
    return out


def calc_forca(df, periodo_media=20):
    """Calcula F=MA para cada candle."""
    corpo = df["Close"] - df["Open"]
    rng = (df["High"] - df["Low"]).replace(0, 0.0001)
    vol_med = df["Volume"].rolling(
        periodo_media, min_periods=1).mean().clip(lower=1)
    f = (corpo / rng) * (df["Volume"] / vol_med) * 100
    return f.clip(-100, 100)


def ema(series, n):
    return series.ewm(span=n, adjust=False).mean()


def alinhamento_mtf(df_g, i_dir, i_ctx):
    """Retorna série booleana: True se alinhamento multi-TF OK."""
    close = df_g["Close"]
    med_dir = ema(close, i_dir)
    med_ctx = ema(close, i_ctx)
    ctx_alta = (close > med_ctx) & (med_ctx > med_ctx.shift(i_ctx))
    ctx_baixa = (close < med_ctx) & (med_ctx < med_ctx.shift(i_ctx))
    dir_alta = (close > med_dir) & (med_dir > med_dir.shift(i_dir))
    dir_baixa = (close < med_dir) & (med_dir < med_dir.shift(i_dir))
    return (ctx_alta & dir_alta) | (ctx_baixa & dir_baixa)

# ─────────────────────────────────────────────
# ANALISE 1: Distribuicao de Forca
# ─────────────────────────────────────────────


def analise_distribuicao(df, nome):
    print(f"\n{'='*60}")
    print(f"DISTRIBUICAO DE FORCA — {nome}")
    print(f"Total candles: {len(df)}")
    f = calc_forca(df)
    fabs = f.abs()

    buckets = [0, 30, 55, 70, 85, 100]
    labels = ["0-30 (ruído)", "30-55 (fraco)", "55-70 (sinal fraco)",
              "70-85 (sinal forte)", "85-100 (exaustao)"]
    for i in range(len(buckets)-1):
        lo, hi = buckets[i], buckets[i+1]
        n = ((fabs >= lo) & (fabs < hi)).sum()
        pct = n / len(f) * 100
        print(f"  {labels[i]:30s}: {n:6d} ({pct:5.1f}%)")

    n_compra = (f >= LIMIAR_FRACO).sum()
    n_venda = (f <= -LIMIAR_FRACO).sum()
    print(
        f"\n  Sinais de COMPRA (F>={LIMIAR_FRACO}): {n_compra} ({n_compra/len(f)*100:.1f}%)")
    print(
        f"  Sinais de VENDA  (F<=-{LIMIAR_FRACO}): {n_venda} ({n_venda/len(f)*100:.1f}%)")
    return f

# ─────────────────────────────────────────────
# ANALISE 2: Comportamento pos-sinal (SL otimo)
# ─────────────────────────────────────────────


def analise_stop_loss(df, nome, ponto_val=1.0):
    """
    Para cada sinal F>=limiar, simula o pior movimento adverso nos proximos
    1, 2, 3, 5, 8 candles para determinar o SL minimo necessario.
    """
    print(f"\n{'='*60}")
    print(f"ANALISE STOP LOSS — {nome}")

    f = calc_forca(df)
    df = df.copy()
    df["forca"] = f

    candles_ahead = [1, 2, 3, 5, 8]

    # Para sinais de COMPRA: pior movimento adverso = maximo de (entry - Low_futuro)
    # Para sinais de VENDA : pior movimento adverso = maximo de (High_futuro - entry)
    resultados_compra = {n: [] for n in candles_ahead}
    resultados_venda = {n: [] for n in candles_ahead}

    # Para cada nivel de SL, qual % de trades sobrevive?
    for idx in range(20, len(df) - max(candles_ahead)):
        row = df.iloc[idx]
        fc = row["forca"]
        entry = row["Close"]

        if fc >= LIMIAR_FRACO:
            futures = df.iloc[idx+1: idx+1+max(candles_ahead)]
            for n in candles_ahead:
                sub = futures.head(n)
                if len(sub) == 0:
                    continue
                pior_adverso = entry - sub["Low"].min()  # quanto caiu
                resultados_compra[n].append(pior_adverso)

        elif fc <= -LIMIAR_FRACO:
            futures = df.iloc[idx+1: idx+1+max(candles_ahead)]
            for n in candles_ahead:
                sub = futures.head(n)
                if len(sub) == 0:
                    continue
                pior_adverso = sub["High"].max() - entry  # quanto subiu
                resultados_venda[n].append(pior_adverso)

    # Percentis de adversidade (SL que suportaria X% das trades)
    print(f"\n  COMPRA — Pior movimento adverso em N candles (pontos):")
    print(f"  {'SL cobre %':>12} | " +
          " | ".join(f"{n:>6}c" for n in candles_ahead))
    for pct in [50, 70, 80, 90, 95]:
        vals = [np.percentile(resultados_compra[n], pct) if resultados_compra[n] else 0
                for n in candles_ahead]
        print(f"  P{pct:02d} ({100-pct:2d}% stop) | " +
              " | ".join(f"{v:7.1f}" for v in vals))

    print(f"\n  VENDA — Pior movimento adverso em N candles (pontos):")
    print(f"  {'SL cobre %':>12} | " +
          " | ".join(f"{n:>6}c" for n in candles_ahead))
    for pct in [50, 70, 80, 90, 95]:
        vals = [np.percentile(resultados_venda[n], pct) if resultados_venda[n] else 0
                for n in candles_ahead]
        print(f"  P{pct:02d} ({100-pct:2d}% stop) | " +
              " | ".join(f"{v:7.1f}" for v in vals))

    # Range medio do candle (para calibrar SL em % do range)
    range_medio = (df["High"] - df["Low"]).mean()
    print(f"\n  Range medio do candle ({nome}): {range_medio:.1f} pts")
    print(
        f"  SL = 0.5x range: {range_medio*0.5:.1f} pts  |  1x: {range_medio:.1f} pts  |  1.5x: {range_medio*1.5:.1f} pts")

    return resultados_compra, resultados_venda, range_medio

# ─────────────────────────────────────────────
# ANALISE 3: 2 tons — F fraco vs F forte
# ─────────────────────────────────────────────


def analise_dois_tons(df, nome):
    """
    Compara o comportamento no candle SEGUINTE entre sinais fracos (55-70)
    e sinais fortes (>70). Responde: vale a pena diferenciar?
    """
    print(f"\n{'='*60}")
    print(f"VALIDACAO 2 TONS — {nome}")
    print(f"  Fraco = F em [55,70) | Forte = F em [70,100]")

    f = calc_forca(df)
    df = df.copy()
    df["forca"] = f

    grupos = {
        "fraco_compra":  (f >= LIMIAR_FRACO) & (f < LIMIAR_FORTE),
        "forte_compra":  (f >= LIMIAR_FORTE),
        "fraco_venda":   (f <= -LIMIAR_FRACO) & (f > -LIMIAR_FORTE),
        "forte_venda":   (f <= -LIMIAR_FORTE),
    }

    print(f"\n  {'Grupo':20s} | n     | Win% 1c | Win% 2c | Win% 3c | Avg move 1c")
    for nome_g, mask in grupos.items():
        idxs = df.index[mask & (df.index < len(df)-3)].tolist()
        if len(idxs) < 20:
            print(f"  {nome_g:20s} | {len(idxs):5d} | insuf.")
            continue

        is_long = "compra" in nome_g
        wins1, wins2, wins3 = 0, 0, 0
        moves = []
        for i in idxs:
            entry = df.iloc[i]["Close"]
            if i+1 >= len(df):
                continue
            c1 = df.iloc[i+1]
            mov1 = (c1["Close"] - entry) if is_long else (entry - c1["Close"])
            moves.append(mov1)
            if mov1 > 0:
                wins1 += 1
            if i+2 < len(df):
                c2 = df.iloc[i+2]
                mov2 = (c2["Close"] -
                        entry) if is_long else (entry - c2["Close"])
                if mov2 > 0:
                    wins2 += 1
            if i+3 < len(df):
                c3 = df.iloc[i+3]
                mov3 = (c3["Close"] -
                        entry) if is_long else (entry - c3["Close"])
                if mov3 > 0:
                    wins3 += 1

        n = len(idxs)
        avg_move = np.mean(moves) if moves else 0
        print(f"  {nome_g:20s} | {n:5d} | {wins1/n*100:6.1f}% | {wins2/n*100:6.1f}% | {wins3/n*100:6.1f}% | {avg_move:+.1f} pts")

# ─────────────────────────────────────────────
# ANALISE 4: Winrate com MTF (confirmacao 3 TFs)
# ─────────────────────────────────────────────


def analise_mtf_vs_sem(df_g, nome, i_dir, i_ctx):
    """Compara winrate com alinhamento MTF vs sem alinhamento."""
    print(f"\n{'='*60}")
    print(f"MTF vs SEM MTF — {nome}")

    f = calc_forca(df_g)
    df_g = df_g.copy()
    df_g["forca"] = f
    df_g["mtf_ok"] = alinhamento_mtf(df_g, i_dir, i_ctx)

    for usa_mtf in [False, True]:
        label = "COM MTF" if usa_mtf else "SEM MTF"
        if usa_mtf:
            mask = (f.abs() >= LIMIAR_FRACO) & df_g["mtf_ok"]
        else:
            mask = f.abs() >= LIMIAR_FRACO

        idxs = df_g.index[mask & (df_g.index < len(df_g)-5)].tolist()
        wins1, wins3, wins5 = 0, 0, 0
        for i in idxs:
            is_long = df_g.iloc[i]["forca"] > 0
            entry = df_g.iloc[i]["Close"]
            for nc, wins_list in [(1, [wins1, wins3, wins5][0:1]),
                                  (3, [wins1, wins3, wins5][1:2]),
                                  (5, [wins1, wins3, wins5][2:3])]:
                pass  # rebuilt below

        # simpler rebuild
        w1 = w3 = w5 = 0
        for i in idxs:
            is_long = df_g.iloc[i]["forca"] > 0
            entry = df_g.iloc[i]["Close"]
            if i+1 < len(df_g):
                m = (df_g.iloc[i+1]["Close"] -
                     entry) if is_long else (entry - df_g.iloc[i+1]["Close"])
                if m > 0:
                    w1 += 1
            if i+3 < len(df_g):
                m = (df_g.iloc[i+3]["Close"] -
                     entry) if is_long else (entry - df_g.iloc[i+3]["Close"])
                if m > 0:
                    w3 += 1
            if i+5 < len(df_g):
                m = (df_g.iloc[i+5]["Close"] -
                     entry) if is_long else (entry - df_g.iloc[i+5]["Close"])
                if m > 0:
                    w5 += 1

        n = len(idxs)
        if n == 0:
            print(f"  {label}: sem dados")
            continue
        print(
            f"  {label:8s} n={n:5d}  win@1c={w1/n*100:.1f}%  win@3c={w3/n*100:.1f}%  win@5c={w5/n*100:.1f}%")

# ─────────────────────────────────────────────
# ANALISE 5: Otimizacao SL x TP (R:R ideal)
# ─────────────────────────────────────────────


def analise_rr(df, nome, ponto_val=1.0, capital=10000, risco_pct=1.0):
    """
    Testa grades de SL/TP em pontos e calcula resultado liquido.
    Objetivo: menor SL com melhor resultado.
    """
    print(f"\n{'='*60}")
    print(f"OTIMIZACAO SL x TP — {nome}")
    print(
        f"  Capital: R${capital:,.0f}  Risco por trade: {risco_pct}%  (R${capital*risco_pct/100:.0f})")

    f = calc_forca(df)
    df = df.copy()
    df["forca"] = f
    df["mtf_ok"] = alinhamento_mtf(df, 2, 4)

    mask = (f.abs() >= LIMIAR_FRACO) & df["mtf_ok"]
    idxs = df.index[mask & (df.index < len(df)-10)].tolist()

    range_medio = (df["High"] - df["Low"]).mean()

    sls = [range_medio * m for m in [0.3, 0.5, 0.75, 1.0, 1.5, 2.0]]
    rrs = [1.0, 1.5, 2.0, 2.5, 3.0]

    best = {"resultado": -999999, "sl": 0, "rr": 0, "winrate": 0, "n": 0}
    print(f"\n  Range medio: {range_medio:.1f} pts")
    print(f"\n  {'SL (pts)':>10} | {'RR':>4} | {'TP (pts)':>9} | {'n':>5} | {'Wins':>5} | {'Win%':>6} | {'Resultado R$':>13}")

    for sl_pts in sls:
        for rr in rrs:
            tp_pts = sl_pts * rr
            wins = losses = 0
            for i in idxs:
                is_long = df.iloc[i]["forca"] > 0
                entry = df.iloc[i]["Close"]
                target = entry + tp_pts if is_long else entry - tp_pts
                stop = entry - sl_pts if is_long else entry + sl_pts
                outcome = None
                for j in range(i+1, min(i+11, len(df))):
                    h = df.iloc[j]["High"]
                    l = df.iloc[j]["Low"]
                    if is_long:
                        if l <= stop:
                            outcome = "loss"
                            break
                        if h >= target:
                            outcome = "win"
                            break
                    else:
                        if h >= stop:
                            outcome = "loss"
                            break
                        if l <= target:
                            outcome = "win"
                            break
                if outcome is None:
                    cl = df.iloc[min(i+10, len(df)-1)]["Close"]
                    outcome = "win" if ((is_long and cl > entry) or (
                        not is_long and cl < entry)) else "loss"
                if outcome == "win":
                    wins += 1
                else:
                    losses += 1

            n = wins + losses
            if n == 0:
                continue
            winrate = wins / n
            risco_r = capital * risco_pct / 100
            contratos = max(1, int(risco_r / (sl_pts * ponto_val)))
            resultado = (wins * tp_pts - losses * sl_pts) * \
                contratos * ponto_val

            print(
                f"  {sl_pts:10.1f} | {rr:4.1f} | {tp_pts:9.1f} | {n:5d} | {wins:5d} | {winrate*100:5.1f}% | R${resultado:>12,.0f}")
            if resultado > best["resultado"]:
                best = {"resultado": resultado, "sl": sl_pts, "rr": rr,
                        "winrate": winrate, "n": n, "tp": tp_pts, "contratos": contratos}

    print(
        f"\n  *** MELHOR: SL={best['sl']:.1f}pts  RR={best['rr']:.1f}  TP={best.get('tp', 0):.1f}pts")
    print(
        f"      Win%={best['winrate']*100:.1f}%  n={best['n']}  Resultado=R${best['resultado']:,.0f}")
    print(
        f"      Contratos sugeridos (risco {risco_pct}% de R${capital:,}): {best['contratos']}")
    return best


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    resultados_finais = {}

    for trip in TRIPLETAS:
        nome = trip["nome"]
        ativo = trip["ativo"]
        tf_g = trip["tf_gatilho"]
        i_dir = trip["i_dir"]
        i_ctx = trip["i_ctx"]
        pv = trip["ponto_val"]

        print(f"\n{'#'*60}")
        print(f"# TRIPLETA: {nome}")
        print(f"{'#'*60}")

        # Tenta WDO/WIN generico (FUT) e contratos especificos (J26 etc)
        prefixos = [f"WD" if ativo == "WDO" else f"WI"]
        df_g = pd.concat([load_csvs(p, tf_g)
                         for p in prefixos], ignore_index=True)
        df_g = df_g.sort_values("datetime").drop_duplicates(
            "datetime").reset_index(drop=True)

        if len(df_g) < 100:
            print(
                f"  Dados insuficientes para {nome} ({len(df_g)} linhas) — pulando")
            continue

        print(f"  Candles carregados (TF gatilho {tf_g}): {len(df_g)}")
        print(
            f"  Periodo: {df_g['datetime'].min().date()} a {df_g['datetime'].max().date()}")

        analise_distribuicao(df_g, nome)
        analise_dois_tons(df_g, nome)
        rc, rv, range_med = analise_stop_loss(df_g, nome, pv)
        analise_mtf_vs_sem(df_g, nome, i_dir, i_ctx)
        best_rr = analise_rr(df_g, nome, pv)

        resultados_finais[nome] = {
            "range_medio_pts": round(range_med, 2),
            "melhor_sl_pts": round(best_rr["sl"], 2),
            "melhor_rr": best_rr["rr"],
            "melhor_tp_pts": round(best_rr.get("tp", 0), 2),
            "winrate": round(best_rr["winrate"] * 100, 1),
            "resultado_r": round(best_rr["resultado"], 2),
            "contratos_suger": best_rr["contratos"],
        }

    print(f"\n{'='*60}")
    print("RESUMO FINAL")
    print(f"{'='*60}")
    for k, v in resultados_finais.items():
        print(f"\n{k}:")
        for ck, cv in v.items():
            print(f"  {ck:22s}: {cv}")

    with open("resultados_analise_forca.json", "w", encoding="utf-8") as fj:
        json.dump(resultados_finais, fj, indent=2, ensure_ascii=False)
    print("\n[OK] Salvo em resultados_analise_forca.json")
