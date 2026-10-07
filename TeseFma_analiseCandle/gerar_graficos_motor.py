from __future__ import annotations

import math
import re
import unicodedata
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA_ROOT = BASE.parent / "CandlesHistoryDatas"
OUT = BASE / "graficos_motor"
OUT.mkdir(exist_ok=True)

PASTAS = ["2020_22", "2022_24", "2024_26", "2026", "CandlesHistoricos2026"]
TFS = ["5min", "10min", "15min", "20min", "30min", "60min"]
TFS_FOCO = ["5min", "15min", "30min", "60min"]
ESTADOS = {2: "VL", 1: "VD", 0: "N", -1: "RD", -2: "RV"}


def num(s):
    s = s.astype(str).str.strip().str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def ler_csv(path):
    raw = pd.read_csv(path, sep=";", encoding="latin1", dtype=str, header=None)
    if str(raw.iloc[0, 0]).strip().lower() == "ativo":
        raw = raw.iloc[1:]
    cols = ["ativo", "data", "hora", "o", "h", "l", "c", "v", "q"]
    if raw.shape[1] == 8:
        cols.remove("hora")
    raw.columns = cols
    if "hora" in cols:
        stamp = raw["data"] + " " + raw["hora"]
        dt = pd.to_datetime(stamp, format="%d/%m/%Y %H:%M:%S", errors="coerce")
        if dt.isna().mean() > 0.5:
            dt = pd.to_datetime(stamp, format="%d/%m/%Y %H:%M", errors="coerce")
    else:
        dt = pd.to_datetime(raw["data"], format="%d/%m/%Y", errors="coerce")
    out = pd.DataFrame({"dt": dt, **{k: num(raw[k]) for k in ("o", "h", "l", "c", "v", "q")}})
    return out.dropna(subset=["dt", "o", "h", "l", "c"]).sort_values("dt").drop_duplicates("dt", keep="last").reset_index(drop=True)


def calcular(d, janela=20):
    d = d.copy()
    d["rng"] = d["h"] - d["l"]
    d["m"] = np.where(d["rng"] > 0, (d["c"] - d["o"]) / d["rng"].replace(0, np.nan).fillna(1.0), 0.0)
    v = d["v"].astype(float)
    media_v = v.rolling(janela).mean().shift(1)
    d["a"] = v / media_v.where(media_v > 0)
    d["F"] = d["m"] * d["a"] * 100
    d["mu"] = d["F"].rolling(janela).mean()
    d["sd"] = d["F"].rolling(janela).std(ddof=0)
    d["atr"] = d["rng"].rolling(janela).mean().shift(1)
    d["z"] = (d["F"] - d["mu"]) / d["sd"].where(d["sd"] > 1e-9)
    z, F = d["z"].to_numpy(), d["F"].to_numpy()
    d["est"] = np.select(
        [(z >= 2.5) & (F > 0), (z >= 1.5) & (F > 0), (z <= -2.5) & (F < 0), (z <= -1.5) & (F < 0)],
        [2, 1, -2, -1],
        default=0,
    ).astype("int8")
    d["fam"] = np.sign(d["est"]).astype("int8")
    d["hora"] = d["dt"].dt.hour
    d["dia"] = d["dt"].dt.normalize()
    d["am"] = d["m"].abs()
    return d.dropna(subset=["F", "mu", "sd", "atr"]).reset_index(drop=True)


def series_por_tf(tf):
    pat = re.compile(r"^([A-Z]{3}[A-Z0-9]+)_F_0_(.+)\.csv$")
    partes = []
    for prio, pasta in enumerate(PASTAS):
        directory = DATA_ROOT / pasta
        if not directory.exists():
            continue
        for path in sorted(directory.glob(f"WIN*_F_0_{tf}.csv")):
            if path.stat().st_size == 0:
                continue
            m = pat.match(unicodedata.normalize("NFC", path.name))
            if not m:
                continue
            d = ler_csv(path)
            if d.empty:
                continue
            d = calcular(d)
            d["simbolo"] = m.group(1)
            d["prio"] = prio
            partes.append(d)
    if not partes:
        return pd.DataFrame()
    t = pd.concat(partes, ignore_index=True)
    t["dia"] = t["dt"].dt.normalize()
    q = t.groupby(["dia", "prio", "simbolo"], as_index=False)["v"].sum()
    q = q[q["v"] >= 0.9 * q.groupby("dia")["v"].transform("max")]
    vencedores = q.sort_values(["dia", "prio", "simbolo"]).drop_duplicates("dia")[["dia", "prio", "simbolo"]]
    return t.merge(vencedores, on=["dia", "prio", "simbolo"]).sort_values("dt", kind="stable").reset_index(drop=True)


def medida_h27(d):
    d = d.copy()
    if d.empty:
        return {"can": np.nan, "rob": np.nan}
    d["rng_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
    dia = d.groupby("dia", sort=False)["F"]
    mu = dia.transform(lambda s: s.shift(1).rolling(20, min_periods=20).mean())
    mad = dia.transform(lambda s: s.shift(1).rolling(20, min_periods=20).apply(lambda x: np.median(np.abs(x - np.median(x))), raw=True))
    sigma = 1.4826 * mad.where(mad > 0)
    z_rob = (d["F"] - mu) / sigma.where(sigma > 1e-12)
    canon = (d["z"] >= 2.5) & (d["F"] > 0)
    robust = (z_rob >= 2.5) & (d["F"] > 0)
    next_rng = d.groupby("dia", sort=False)["rng_atr"].shift(-1)
    exp_c = next_rng[canon].mean() if canon.any() else np.nan
    exp_r = next_rng[robust].mean() if robust.any() else np.nan
    return {"can": float(exp_c) if np.isfinite(exp_c) else np.nan, "rob": float(exp_r) if np.isfinite(exp_r) else np.nan}


def medida_h28(d, ds):
    d = d.copy(); ds = ds.copy()
    if d.empty or ds.empty:
        return {"can": np.nan, "saz": np.nan}
    for x in (d, ds):
        x["hora"] = x["dt"].dt.hour
        x["dia"] = x["dt"].dt.normalize()
        x["alarme"] = x["F"].notna() & (x["z"].abs() >= 1.5) & (x["F"] != 0)
        x["rng_atr"] = x["rng"] / x["atr"].where(x["atr"] > 0)
        x["expansao"] = x.groupby("dia", sort=False)["rng_atr"].shift(-1)
    exp_c = d[d["alarme"]]["expansao"].mean()
    exp_s = ds[ds["alarme"]]["expansao"].mean()
    return {"can": float(exp_c), "saz": float(exp_s)}


def medida_h29(d):
    d = d.copy()
    if d.empty:
        return {"abs": np.nan, "ctrl": np.nan, "persist": np.nan, "t": np.nan}
    d["rng_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
    d["cor"] = np.sign(d["c"] - d["o"])
    d["retorno"] = d["cor"] * (d.groupby("dia")["c"].shift(-1) - d["o"])
    d["expansao"] = d.groupby("dia")["rng_atr"].shift(-1)
    sel = (d["a"] >= 2.0) & (d["am"].abs() < 0.3)
    abs_d = d[sel].copy()
    ctrl = d[~sel].copy()
    if abs_d.empty or ctrl.empty:
        return {"abs": np.nan, "ctrl": np.nan, "persist": np.nan, "t": np.nan}
    exp_abs = abs_d["expansao"].mean(); exp_ctrl = ctrl["expansao"].mean()
    t = ((exp_abs - exp_ctrl) / math.sqrt(abs_d["expansao"].var(ddof=1) / len(abs_d) + ctrl["expansao"].var(ddof=1) / len(ctrl))) if len(abs_d) > 1 and len(ctrl) > 1 else np.nan
    return {"abs": float(exp_abs), "ctrl": float(exp_ctrl), "persist": float(exp_abs / exp_ctrl if exp_ctrl > 0 else np.nan), "t": float(t) if np.isfinite(t) else np.nan}


def plot_distribuicao_forca():
    fig, axes = plt.subplots(1, len(TFS_FOCO), figsize=(16, 4.5), sharey=True)
    for ax, tf in zip(axes, TFS_FOCO):
        d = series_por_tf(tf)
        vals = d["F"].abs().dropna() if not d.empty else pd.Series([], dtype=float)
        if vals.empty:
            ax.text(0.5, 0.5, "sem dados", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
            continue
        bins = np.linspace(0, max(100.0, float(vals.quantile(0.99) * 1.3)), 60)
        ax.hist(vals, bins=bins, color="#4C78A8", alpha=0.8)
        ax.axvline(float(vals.quantile(0.90)), color="#E45756", linestyle="--", linewidth=2, label="P90")
        ax.axvline(float(vals.quantile(0.95)), color="#F58518", linestyle=":", linewidth=2, label="P95")
        ax.set_title(f"{tf}: |F|")
        ax.set_xlabel("|F|")
        ax.set_ylabel("candles")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "01_distribuicao_forca.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_estados_por_tf():
    fig, ax = plt.subplots(figsize=(10, 5))
    rows = []
    for tf in TFS_FOCO:
        d = series_por_tf(tf)
        if d.empty:
            continue
        c = d["est"].value_counts().reindex(sorted(ESTADOS.keys()), fill_value=0)
        pct = c / c.sum()
        rows.append(pd.DataFrame({"tf": tf, "estado": [ESTADOS[k] for k in sorted(ESTADOS.keys())], "pct": pct.values}))
    base = pd.concat(rows, ignore_index=True)
    piv = base.pivot(index="tf", columns="estado", values="pct").reindex(TFS_FOCO)
    colors = ["#2E86AB", "#A2D2FF", "#D9D9D9", "#F4A261", "#E76F51"]
    piv.plot(kind="bar", stacked=True, ax=ax, color=colors, edgecolor="none")
    ax.set_title("Frequência de estados por timeframe")
    ax.set_ylabel("% do total")
    ax.set_xlabel("timeframe")
    ax.set_ylim(0, 1.05)
    ax.legend(title="estado")
    ax.grid(axis="y", alpha=0.25, linestyle="--")
    fig.tight_layout()
    fig.savefig(OUT / "02_estados_por_tf.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_h29():
    labels, exp_abs, exp_ctrl, persist, tval = [], [], [], [], []
    for tf in ["5min", "15min"]:
        d = series_por_tf(tf)
        m = medida_h29(d)
        labels.append(tf)
        exp_abs.append(m["abs"])
        exp_ctrl.append(m["ctrl"])
        persist.append(m["persist"])
        tval.append(m["t"])

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(labels))
    w = 0.28
    ax.bar(x - w / 2, exp_abs, width=w, label="absorção", color="#2A9D8F")
    ax.bar(x + w / 2, exp_ctrl, width=w, label="controle", color="#9D9D9D")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("H29 — expansão futura da absorção vs controle")
    ax.set_ylabel("range futuro / ATR")
    ax.legend()
    for i, t in enumerate(tval):
        if np.isfinite(t):
            ax.text(i, max(exp_abs[i], exp_ctrl[i]) + 0.12, f"t={t:+.1f}", ha="center", va="bottom")
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "03_h29_absorcao_vs_controle.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, persist, color="#E76F51", alpha=0.85)
    ax.set_title("H29 — persistência do padrão de absorção")
    ax.set_ylabel("expansão absorção / controle")
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "04_h29_persistencia.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_h27_h28():
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    tfs = ["5min", "15min"]
    for ax, nome in zip(axes, ["H27", "H28"]):
        vals = []
        for tf in tfs:
            d = series_por_tf(tf)
            if nome == "H27":
                m = medida_h27(d)
                vals.append((tf, m["can"], m["rob"]))
            else:
                ds = series_por_tf(tf)
                ds["z"] = ds["F"].rolling(20).mean() / ds["F"].rolling(20).std(ddof=0)
                m = medida_h28(d, ds)
                vals.append((tf, m["can"], m["saz"]))
        labels = [v[0] for v in vals]
        canon = [v[1] for v in vals]
        alt = [v[2] for v in vals] if vals else [np.nan, np.nan]
        x = np.arange(len(labels))
        w = 0.32
        ax.bar(x - w / 2, canon, width=w, label="canônico", color="#4C78A8")
        ax.bar(x + w / 2, alt, width=w, label="variante", color="#E45756")
        ax.set_title(f"{nome} — expansão futura do evento: canônico vs variante")
        ax.set_ylabel("expansão / ATR")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "05_h27_h28.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_massa_aceleracao_forca():
    metrics = [
        ("m", "Massa: m (sinal do candle)", "m", "m", "Massa do candle"),
        ("a", "Aceleração: a (volume / média 20)", "a", "a", "Aceleração / volume"),
        ("F", "Força: |F| = |m*a*100|", "F", "|F|", "Força absoluta"),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=False)
    for ax, (key, title, col, label, subtitle) in zip(axes, metrics):
        samples = []
        for tf in TFS_FOCO:
            d = series_por_tf(tf)
            if d.empty:
                continue
            vals = d[col].abs() if key == "F" else d[col].dropna()
            if vals.empty:
                continue
            samples.append((tf, vals))
        if not samples:
            ax.text(0.5, 0.5, "sem dados", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off(); continue
        positions = np.arange(len(samples))
        bp = ax.boxplot([vals.to_numpy() for _, vals in samples], positions=positions, widths=0.55, patch_artist=True,
                        boxprops=dict(facecolor="#4C78A8", alpha=0.7), medianprops=dict(color="#E45756", linewidth=2),
                        whiskerprops=dict(color="#2F4B7C"), capprops=dict(color="#2F4B7C"))
        ax.set_xticks(positions)
        ax.set_xticklabels([tf for tf, _ in samples], rotation=0)
        ax.set_title(title)
        ax.set_ylabel(label)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        for i, (_, vals) in enumerate(samples):
            q90 = float(vals.quantile(0.90))
            ax.text(i + 1, q90, f"P90={q90:.1f}", ha="center", va="bottom", fontsize=8, color="#3B3B3B")
    fig.tight_layout()
    fig.savefig(OUT / "06_massa_aceleracao_forca.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_hipoteses_resumo():
    dados = [
        ("H29\nabsorção", 1.60, 1.70, 1.0),
        ("H39\nalarmes multi-TF", 1.89, 1.89, 0.8),
        ("H20\nvolatilidade", 1.44, 1.15, 0.7),
        ("H17\npersistência", 1.59, 1.11, 0.6),
    ]
    labels = [d[0] for d in dados]
    v5 = [d[1] for d in dados]
    v15 = [d[2] for d in dados]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(labels))
    w = 0.33
    ax.bar(x - w / 2, v5, width=w, label="5 min", color="#4C78A8")
    ax.bar(x + w / 2, v15, width=w, label="15 min", color="#E45756")
    ax.set_title("Resumo das hipóteses mais relevantes")
    ax.set_ylabel("expansão / efeito observado")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "07_hipoteses_resumo.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_dashboard_html():
    sections = [
        ("Massa, aceleração e força", ["06_massa_aceleracao_forca.png"]),
        ("Distribuição de força", ["01_distribuicao_forca.png", "02_estados_por_tf.png"]),
        ("H29 / absorção e persistência", ["03_h29_absorcao_vs_controle.png", "04_h29_persistencia.png"]),
        ("H27 / H28 / hipóteses", ["05_h27_h28.png", "07_hipoteses_resumo.png"]),
    ]
    html = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Motor F=m*a — dashboard HTML</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f4f6fb; color: #1d2736; }
    h1 { margin: 0 0 12px; }
    h2 { margin: 28px 0 12px; }
    .wrap { max-width: 1400px; margin: 0 auto; padding: 24px; }
    .intro { background: #ffffff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 20px; }
    .card { background: #fff; border-radius: 12px; padding: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .card img { width: 100%; height: auto; border-radius: 8px; background: #fafcff; }
    .label { font-weight: 700; margin-bottom: 8px; }
    .tiny { font-size: 12px; color: #59657a; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="intro">
      <h1>Motor F = m * a * k</h1>
      <p>Dashboard de inspeção visual do motor por parte: massa, aceleração, força e hipóteses principais.</p>
      <p class="tiny">Uso orientativo: estas visualizações documentam o comportamento do motor e não substituem decisão operacional isolada.</p>
    </div>
"""
    for title, files in sections:
        html += f"\n    <section>\n      <h2>{title}</h2>\n      <div class=\"grid\">\n"
        for f in files:
            html += f"        <div class=\"card\">\n          <div class=\"label\">{f}</div>\n          <img src=\"{f}\" alt=\"{f}\" />\n        </div>\n"
        html += "      </div>\n    </section>\n"
    html += "  </div>\n</body>\n</html>\n"
    (OUT / "dashboard_motor.html").write_text(html, encoding="utf-8")


def main():
    plot_distribuicao_forca()
    plot_estados_por_tf()
    plot_h29()
    plot_h27_h28()
    plot_massa_aceleracao_forca()
    plot_hipoteses_resumo()
    build_dashboard_html()
    print(f"Gráficos salvos em: {OUT}")
    for p in sorted(OUT.glob("*.png")):
        print(f"- {p.name}")
    print("- dashboard_motor.html")


if __name__ == "__main__":
    main()
