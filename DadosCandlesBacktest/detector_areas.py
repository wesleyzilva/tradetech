"""
detector_areas.py — Detecção Automática de Áreas de Suporte/Resistência
========================================================================
Implementa: DadosCandlesBacktest/instructions.md

Algoritmo:
  1. Carrega candles (CSV) por ativo/timeframe
  2. Calcula F = (Corpo/Range) × (Volume/MediaVolume) × 100
  3. Gera áreas retangulares em torno de máximas/mínimas de candles com |F| >= forca_min
  4. Conta toques futuros em janela configurável
  5. Calcula density_score e strength por zona
  6. Exporta JSON + Markdown ordenados por relevância

Uso:
  python detector_areas.py                        # default: WDO+WIN, 5min+15min
  python detector_areas.py --ativo WD --tfs 15min
  python detector_areas.py --ativo WI --tfs 5min 15min --forca_minima 70
  python detector_areas.py --x_pontos_wdo 25 --x_pontos_win 1000

Saída (gerada em base_dir):
  areas_wdo.json / areas_wdo.md
  areas_win.json / areas_win.md
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ─── Parâmetros padrão (calibrados pelo backtest) ────────────────────────────
DEFAULT_CONFIG = {
    # x_pontos: distância vertical da área (SL/SG offset) por ativo e TF
    "x_pontos": {
        "WD": {"2min": 8,  "5min": 12, "15min": 20, "30min": 28, "60min": 40},
        "WI": {"2min": 200, "5min": 342, "15min": 822, "30min": 600, "60min": 1000},
    },
    "sl_minimo":            {"WD": 10,  "WI": 400},   # pontos mínimos de SL
    "sg_minimo":            {"WD": 20,  "WI": 800},   # pontos mínimos de SG
    # candles para média de volume
    "periodo_media_volume": 20,
    # |F| mínimo para gerar área
    "forca_minima":         55.0,
    # extensão horizontal da área
    "n_candles_extensao":   3,
    # janela de candles p/ contar toques
    "n_candles_janela":     50,
    "min_toques_relevante": 2,                          # filtro de relevância
}

# Duração em minutos por timeframe (para extensão horizontal)
TF_MINUTOS = {
    "2min": 2, "5min": 5, "15min": 15,
    "30min": 30, "60min": 60, "diario": 1440,
}


# ─── Carga de dados ──────────────────────────────────────────────────────────

def load_candles(prefixo: str, tf: str, base_dir: Path) -> pd.DataFrame:
    """Carrega e concatena todos os CSVs de um ativo/timeframe."""
    frames = []
    for pasta in sorted(base_dir.glob("*/")):
        for f in pasta.glob(f"*{prefixo}*_{tf}.csv"):
            try:
                df = pd.read_csv(f, sep=";", decimal=",",
                                 encoding="latin1", thousands=".")
                if len(df.columns) < 8:
                    continue
                cm = {
                    df.columns[1]: "Data", df.columns[2]: "Hora",
                    df.columns[3]: "Open",  df.columns[4]: "High",
                    df.columns[5]: "Low",   df.columns[6]: "Close",
                    df.columns[7]: "Volume",
                }
                df = df.rename(columns=cm)
                df["dt"] = pd.to_datetime(
                    df["Data"] + " " + df["Hora"], dayfirst=True, errors="coerce"
                )
                df = df.dropna(subset=["dt"]).sort_values(
                    "dt").reset_index(drop=True)
                for c in ["Open", "Close", "High", "Low"]:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
                df["Volume"] = pd.to_numeric(
                    df["Volume"], errors="coerce").fillna(0)
                frames.append(
                    df[["dt", "Open", "High", "Low", "Close", "Volume"]].dropna()
                )
            except Exception:
                pass

    if not frames:
        return pd.DataFrame()
    return (
        pd.concat(frames)
        .sort_values("dt")
        .drop_duplicates("dt")
        .reset_index(drop=True)
    )


# ─── Cálculo de Força F = M × A ──────────────────────────────────────────────

def calc_forca(df: pd.DataFrame, periodo_vol: int = 20) -> np.ndarray:
    """
    F = (Corpo/Range) × (Volume/MediaVolume) × 100  ∈ [-100, +100]

    Positivo = pressão compradora; Negativo = pressão vendedora.
    """
    corpo = df["Close"].values - df["Open"].values
    rng = np.where(
        (df["High"].values - df["Low"].values) > 0,
        df["High"].values - df["Low"].values,
        0.0001,
    )
    vol_media = (
        pd.Series(df["Volume"].values)
        .rolling(periodo_vol, min_periods=1)
        .mean()
        .clip(lower=1)
        .values
    )
    return np.clip((corpo / rng) * (df["Volume"].values / vol_media) * 100, -100, 100)


# ─── Geração de áreas retangulares ───────────────────────────────────────────

def gerar_areas(
    df: pd.DataFrame,
    forca: np.ndarray,
    x_pontos: float,
    forca_min: float,
    n_ext: int,
    tf_minutos: int,
) -> list:
    """
    Para cada candle com |F| >= forca_min gera dois retângulos:
      • área superior: high → high + x_pontos  (resistência / exaustão compradora)
      • área inferior: low - x_pontos → low    (suporte / exaustão vendedora)

    Extensão horizontal: t0 até t0 + n_ext × tf_minutos.
    """
    areas = []
    area_counter = [0]
    n = len(df)
    ext_delta = timedelta(minutes=tf_minutos * n_ext)

    def nova_area(i, tipo, p_inf, p_sup, direcao):
        area_counter[0] += 1
        return {
            "area_id":        f"A{area_counter[0]}",
            "tipo":           tipo,
            "timeframe":      f"{tf_minutos}min",
            "t0":             df["dt"].iloc[i].isoformat(),
            "t1":             (df["dt"].iloc[i] + ext_delta).isoformat(),
            "preco_inferior": round(float(p_inf), 2),
            "preco_superior": round(float(p_sup), 2),
            "candle_origem":  int(i),
            "forca":          round(float(forca[i]), 1),
            "direcao_candle": direcao,
            "toques":         0,
            "density_score":  0,
            "strength":       "fraca",
            "context_overlap": False,  # preenchido na análise multi-tf
        }

    for i in range(1, n - n_ext - 1):
        fa = abs(forca[i])
        if fa < forca_min:
            continue

        direcao = "alta" if forca[i] > 0 else "baixa"
        high = df["High"].iloc[i]
        low = df["Low"].iloc[i]

        # Área acima da máxima (resistência/exaustão compradora)
        tipo_sup = "resistencia" if direcao == "alta" else "rompimento_alta"
        areas.append(nova_area(i, tipo_sup, high, high + x_pontos, direcao))

        # Área abaixo da mínima (suporte/exaustão vendedora)
        tipo_inf = "suporte" if direcao == "baixa" else "rompimento_baixa"
        areas.append(nova_area(i, tipo_inf, low - x_pontos, low, direcao))

    return areas


# ─── Contagem de toques e scoring ────────────────────────────────────────────

def calcular_toques(areas: list, df: pd.DataFrame, janela: int = 50) -> list:
    """
    Conta quantos candles futuros (janela) tocam a faixa de cada área.
    Atualiza density_score e strength.

    Scoring:
      density_score = min(100, toques*5 + |F|*0.3)
      strength  — fraca: score<40 | média: 40-60 | alta: >60 e toques>=3
    """
    n = len(df)
    highs = df["High"].values
    lows = df["Low"].values

    for area in areas:
        i0 = area["candle_origem"]
        p_inf = area["preco_inferior"]
        p_sup = area["preco_superior"]
        toques = 0

        for j in range(i0 + 1, min(i0 + 1 + janela, n)):
            if lows[j] <= p_sup and highs[j] >= p_inf:
                toques += 1

        fa = abs(area["forca"])
        score = min(100, int(toques * 5 + fa * 0.3))

        area["toques"] = toques
        area["density_score"] = score
        area["strength"] = (
            "alta" if score > 60 and toques >= 3 else
            "media" if score >= 40 or toques >= 2 else
            "fraca"
        )

    return areas


def marcar_confluencia_mtf(areas_por_tf: dict) -> list:
    """
    Verifica context_overlap: área de tf menor é marcada True se seu range de
    preço intersecta alguma área de tf maior (≥ 3× o timeframe menor).

    Incrementa density_score em +15 quando há confluência.
    """
    tfs_sorted = sorted(areas_por_tf.keys())  # menor → maior
    todas = []

    for idx, tf in enumerate(tfs_sorted):
        areas_menores = areas_por_tf[tf]
        areas_maiores = [a for tf2 in tfs_sorted[idx + 1:]
                         for a in areas_por_tf[tf2]]

        for am in areas_menores:
            for am2 in areas_maiores:
                # intersecção de faixas de preço
                if am["preco_inferior"] <= am2["preco_superior"] and \
                   am["preco_superior"] >= am2["preco_inferior"]:
                    am["context_overlap"] = True
                    am["density_score"] = min(100, am["density_score"] + 15)
                    # reclassifica strength após boost
                    am["strength"] = (
                        "alta" if am["density_score"] > 60 and am["toques"] >= 3 else
                        "media" if am["density_score"] >= 40 or am["toques"] >= 2 else
                        "fraca"
                    )
                    break  # basta um overlap

        todas.extend(areas_menores)

    return todas


# ─── Persistência ────────────────────────────────────────────────────────────

def salvar_json(areas: list, caminho: Path) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(areas, f, ensure_ascii=False, indent=2)
    print(f"  -> JSON: {caminho.name}  ({len(areas)} areas)")


def salvar_markdown(areas: list, caminho: Path, titulo: str) -> None:
    lines = [
        f"# {titulo}",
        f"_Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        "| ID | Tipo | TF | Faixa preço | Toques | Score | Força | Strength | MTF |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for a in areas[:100]:
        faixa = f"{a['preco_inferior']} – {a['preco_superior']}"
        mtf = "✓" if a["context_overlap"] else ""
        lines.append(
            f"| {a['area_id']} | {a['tipo']} | {a['timeframe']} | {faixa} "
            f"| {a['toques']} | {a['density_score']} | {a['forca']:+.0f} "
            f"| {a['strength']} | {mtf} |"
        )
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  -> MD:   {caminho.name}")


# ─── Orquestração por ativo ───────────────────────────────────────────────────

def processar_ativo(
    prefixo: str, nome: str, tfs: list, config: dict, base_dir: Path
) -> list:
    print(f"\n{'-'*60}")
    print(f"  {nome}")
    print(f"{'-'*60}")

    areas_por_tf: dict = {}
    periodo_vol = config["periodo_media_volume"]
    forca_min = config["forca_minima"]
    n_ext = config["n_candles_extensao"]
    janela = config["n_candles_janela"]
    min_toques = config["min_toques_relevante"]

    for tf in tfs:
        tf_min = TF_MINUTOS.get(tf, 15)
        x = config["x_pontos"].get(prefixo, {}).get(tf, 20)

        df = load_candles(prefixo, tf, base_dir)
        if len(df) < 50:
            print(f"  [{tf}] dados insuficientes - SKIP")
            continue

        forca = calc_forca(df, periodo_vol)
        areas = gerar_areas(df, forca, x, forca_min, n_ext, tf_min)
        areas = calcular_toques(areas, df, janela)

        n_rel = sum(1 for a in areas if a["toques"] >= min_toques)
        print(
            f"  [{tf:6}] {len(df):6}c -> {len(areas):5} areas -> {n_rel} relevantes (x={x}pts)")
        areas_por_tf[tf] = areas

    if not areas_por_tf:
        print(f"  Nenhuma area gerada para {nome}")
        return []

    # Confluência multi-tf
    todas = marcar_confluencia_mtf(areas_por_tf)

    # Filtra e ordena por relevância
    for a in todas:
        a["ativo"] = nome
    relevantes = sorted(
        [a for a in todas if a["toques"] >= min_toques],
        key=lambda x: (-x["density_score"], -abs(x["forca"])),
    )

    # Salva
    slug = nome.lower()
    salvar_json(relevantes, base_dir / f"areas_{slug}.json")
    salvar_markdown(relevantes, base_dir / f"areas_{slug}.md",
                    f"Areas Detectadas - {nome}")

    return relevantes


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detector de Áreas S/R — TradeTech  (instructions.md)"
    )
    parser.add_argument("--ativo", default="todos",
                        choices=["WD", "WI", "todos"])
    parser.add_argument("--tfs", nargs="+",
                        default=["5min", "15min"],
                        help="Ex: 5min 15min 60min")
    parser.add_argument("--forca_minima", type=float, default=55.0)
    parser.add_argument("--min_toques",   type=int,   default=2)
    parser.add_argument("--x_pontos_wdo", type=float, default=None,
                        help="Override x_pontos WDO (todos os TFs)")
    parser.add_argument("--x_pontos_win", type=float, default=None,
                        help="Override x_pontos WIN (todos os TFs)")
    parser.add_argument("--base_dir", type=Path, default=Path("."))
    args = parser.parse_args()

    # shallow copy estrutural
    config = {k: v for k, v in DEFAULT_CONFIG.items()}
    config["x_pontos"] = {
        "WD": dict(DEFAULT_CONFIG["x_pontos"]["WD"]),
        "WI": dict(DEFAULT_CONFIG["x_pontos"]["WI"]),
    }
    config["forca_minima"] = args.forca_minima
    config["min_toques_relevante"] = args.min_toques

    if args.x_pontos_wdo:
        config["x_pontos"]["WD"] = {tf: args.x_pontos_wdo
                                    for tf in config["x_pontos"]["WD"]}
    if args.x_pontos_win:
        config["x_pontos"]["WI"] = {tf: args.x_pontos_win
                                    for tf in config["x_pontos"]["WI"]}

    ativos = []
    if args.ativo in ("WD", "todos"):
        ativos.append(("WD", "WDO"))
    if args.ativo in ("WI", "todos"):
        ativos.append(("WI", "WIN"))

    print(f"\nDetector de Areas S/R - TradeTech")
    print(f"  base_dir   : {args.base_dir.resolve()}")
    print(f"  timeframes : {args.tfs}")
    print(f"  forca_min  : {config['forca_minima']}")
    print(f"  min_toques : {config['min_toques_relevante']}")

    for prefixo, nome in ativos:
        processar_ativo(prefixo, nome, args.tfs, config, args.base_dir)

    print("\nConcluido.")


if __name__ == "__main__":
    main()
