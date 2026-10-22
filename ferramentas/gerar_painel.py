"""Gera o painel HTML interativo (``docs/painel/painel.html``) a partir das análises e dos candles do repositório.

O HTML é um arquivo único com os dados embutidos e usa Plotly via CDN (precisa de internet para abrir).

Uso: python ferramentas/gerar_painel.py [--refazer]   # --refazer recalcula os resultados em cache do M02/ANALISE_002
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
M02 = RAIZ / "motores" / "M02_microestrutura_barreiras"
M16 = RAIZ / "motores" / "M16_confluencia_multitf"
SAIDA = RAIZ / "docs" / "painel" / "painel.html"
INICIO_5MIN = "2024-06-19"

sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(M02 / "codigo"))
sys.path.insert(0, str(M16 / "codigo"))


def ler(path: Path, **kw) -> pd.DataFrame:
    return pd.read_csv(path, sep=";", decimal=",", **kw)


def limpo(x):
    if isinstance(x, (np.floating, float)):
        return None if not np.isfinite(x) else round(float(x), 4)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def registros(df: pd.DataFrame) -> list[dict]:
    return [{k: limpo(v) for k, v in r.items()} for r in df.to_dict("records")]


def rotulo(conj: str, nivel: int) -> str:
    return f"{conj} N{nivel}"


# ---------------------------------------------------------------------------------------------------------------- dados
def bloco_cobertura() -> list[dict]:
    c = pd.read_csv(RAIZ / "dados" / "catalogo_candles.csv")
    c = c[["lote", "arquivo", "serie", "natureza", "variante", "tf", "linhas", "inicio", "fim", "sessoes_completas"]]
    return registros(c)


def bloco_hipoteses() -> dict:
    texto = (RAIZ / "docs" / "INDICE_HIPOTESES.md").read_text(encoding="utf-8")
    secoes, atual = {}, None
    for linha in texto.splitlines():
        if linha.startswith("## "):
            atual = linha[3:].strip()
            continue
        if atual and atual != "Resumo" and linha.startswith("| ") and not linha.startswith("| id") and not linha.startswith("|---"):
            c = [x.strip() for x in re.split(r" \| ", linha.strip().strip("|").strip())]
            if len(c) >= 4:
                secoes.setdefault(atual, []).append({"id": c[0], "grupo": c[1], "texto": c[2].replace("\\|", "|"), "veredito": c[-1]})
    return secoes


def bloco_candles() -> dict:
    from motores.M01_fma_forca.teses.cores.analise_candles import calcular
    from tradetech.dados import carregar_serie

    dias: dict[str, dict] = {}
    for tf in (5, 15, 30, 60):
        d = carregar_serie("WINFUT", f"{tf}min")
        c = calcular(d[["dt", "o", "h", "l", "c", "v"]].copy())
        c = c[c["dt"] >= INICIO_5MIN]
        c["dia"] = c["dt"].dt.strftime("%Y-%m-%d")
        c["hhmm"] = c["dt"].dt.hour * 100 + c["dt"].dt.minute
        for dia, g in c.groupby("dia"):
            dias.setdefault(dia, {})[str(tf)] = {
                "t": g["hhmm"].astype(int).tolist(), "o": g["o"].round(0).astype(int).tolist(), "h": g["h"].round(0).astype(int).tolist(),
                "l": g["l"].round(0).astype(int).tolist(), "c": g["c"].round(0).astype(int).tolist(), "e": g["est"].astype(int).tolist(),
            }
    return dias


def carregar_eventos() -> pd.DataFrame:
    return ler(M16 / "analises" / "ANALISE_001_eventos_detalhe.csv.gz")


def bloco_alarmes(ev: pd.DataFrame) -> list[list]:
    e = ev[(ev["serie"] == "WINFUT") & (ev["modo"] == "A") & ev["sup"].notna()].copy()
    e["dia"] = pd.to_datetime(e["dia"]).dt.strftime("%Y-%m-%d")
    e["hhmm"] = pd.to_datetime(e["dt"]).dt.hour * 100 + pd.to_datetime(e["dt"]).dt.minute
    e = e[e["dia"] >= INICIO_5MIN]
    return [[r.dia, int(r.hhmm), int(r.base), r.conjunto, int(r.nivel), int(r.lado), limpo(r.ret_60), limpo(r.mfe), limpo(r.mae), limpo(r.atr)]
            for r in e.itertuples()]


def bloco_m16(ev: pd.DataFrame) -> dict:
    an = M16 / "analises"
    desc = ler(an / "ANALISE_001_eventos.csv")
    preg = ler(an / "ANALISE_001_pregoes.csv")
    desc["conjunto"] = desc["conjunto"].astype(str)
    desc["rot"] = [rotulo(c, n) for c, n in zip(desc["conjunto"], desc["nivel"])]

    # frequência do alerta
    p = preg.set_index(["base", "subset"])["pregoes"]
    linhas = []
    for (rot, modo, base), g in desc[desc["subset"].isin(["descoberta", "hold1"])].groupby(["rot", "modo", "base"]):
        dias = sum(p.get((base, s), 0) for s in ("descoberta", "hold1"))
        linhas.append({"rot": rot, "modo": modo, "base": int(base), "n": int(g["n_eventos"].sum()), "por_pregao": g["n_eventos"].sum() / dias})
    freq = linhas

    # MFE / MAE
    e = ev[(ev["serie"].str.startswith("WIN")) & (ev["modo"] == "A")].dropna(subset=["mfe", "mae"]).copy()
    e["rot"] = [rotulo(c, n) for c, n in zip(e["conjunto"], e["nivel"])]
    q = [0.10, 0.25, 0.5, 0.75, 0.90]
    boxes = []
    for (rot, base), g in e.groupby(["rot", "base"]):
        if len(g) < 30:
            continue
        r = {"rot": rot, "base": int(base), "n": len(g), "pct_mfe_maior": float((g["mfe"] > g["mae"]).mean() * 100)}
        for nome, serie_ in (("mfe", g["mfe"]), ("mae", g["mae"]), ("mfe_atr", g["mfe"] / g["atr"]), ("mae_atr", g["mae"] / g["atr"])):
            r[nome] = [float(serie_.quantile(x)) for x in q]
        boxes.append(r)

    # estratégias
    est = ler(an / "ANALISE_001_estrategias.csv")
    est["sup"] = est["sup"].fillna("").astype(str)
    est = est[est["sup"] != ""]
    est["rot"] = [rotulo(c, n) for c, n in zip(est["conjunto"], est["nivel"])]
    chave = ["base", "rot", "lado", "geom"]
    wide = est.pivot_table(index=chave, columns="subset", values=["n", "medio", "medio_R", "t_nulo", "wr", "wr_be"], aggfunc="first")
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    wide = wide.reset_index()
    for c in ("n_descoberta", "n_hold1", "n_hold2", "n_wdo", "t_nulo_descoberta", "t_nulo_hold1", "t_nulo_hold2", "medio_descoberta", "medio_hold1", "medio_hold2", "medio_R_wdo"):
        if c not in wide:
            wide[c] = np.nan
    wide["passa"] = ((wide["n_descoberta"] >= 30) & (wide["t_nulo_descoberta"] >= 3) & (wide["n_hold1"] >= 30) & (wide["medio_hold1"] > 0)
                     & (wide["t_nulo_hold1"] >= 2) & (wide["n_hold2"] >= 30) & (wide["medio_hold2"] > 0) & (wide["t_nulo_hold2"] >= 2) & (wide["medio_R_wdo"] > 0))
    cols = chave + ["n_descoberta", "n_hold1", "n_hold2", "n_wdo", "medio_descoberta", "medio_hold1", "medio_hold2", "medio_R_wdo",
                    "t_nulo_descoberta", "t_nulo_hold1", "t_nulo_hold2", "wr_descoberta", "wr_be_descoberta", "passa"]
    for c in cols:
        if c not in wide:
            wide[c] = np.nan
    estrategias = registros(wide[cols])

    # retorno alinhado: t por horizonte e subconjunto
    heat = []
    a = desc[desc["modo"] == "A"]
    for (rot, base), g in a.groupby(["rot", "base"]):
        d = g[g["subset"] == "descoberta"]
        if d.empty or d.iloc[0]["n_eventos"] < 30:
            continue
        for m in (5, 15, 30, 60):
            col, tcol = f"ret_{m}", f"t_ret_{m}"
            if col not in g or pd.isna(d.iloc[0].get(col)):
                continue
            row = {"rot": rot, "base": int(base), "h": m}
            for sub in ("descoberta", "hold1", "hold2", "wdo"):
                x = g[g["subset"] == sub]
                row[sub] = limpo(x.iloc[0][tcol]) if len(x) and pd.notna(x.iloc[0].get(tcol)) else None
                row[sub + "_ret"] = limpo(x.iloc[0][col]) if len(x) and pd.notna(x.iloc[0].get(col)) else None
                row[sub + "_n"] = int(x.iloc[0]["n_eventos"]) if len(x) else 0
            heat.append(row)

    # expansão relativa ao TF único
    exp = []
    for (base, nivel, sub), g in a.groupby(["base", "nivel", "subset"]):
        u = g[g["sup"].isna()]
        if u.empty:
            continue
        ru = u.iloc[0]["ratio_medio"]
        for r in g[g["sup"].notna()].itertuples():
            if r.n_eventos >= 20:
                exp.append({"rot": rotulo(r.conjunto, nivel), "subset": sub, "rel": r.ratio_medio / ru, "n": int(r.n_eventos), "base": int(base)})
    return {"freq": freq, "boxes": boxes, "estrategias": estrategias, "heat": heat, "exp": exp}


def bloco_m02(refazer: bool) -> dict:
    t = ler(M02 / "analises" / "ANALISE_001_trades.csv")
    t["dt_saida"] = pd.to_datetime(t["dt_saida"])
    t = t.sort_values("dt_saida")
    equity = []
    for (conj, perfil), g in t.groupby(["conjunto", "perfil"]):
        g = g.sort_values("dt_saida")
        equity.append({"nome": f"{conj} · {perfil}", "x": g["dt_saida"].dt.strftime("%Y-%m-%d %H:%M").tolist(), "y": g["pnl"].cumsum().round(1).tolist(),
                       "n": len(g), "medio": float(g["pnl"].mean())})
    f = t[(t["conjunto"] == "WINFUT 1min") & (t["perfil"] == "fiel")]
    hora = f.assign(h=f["hhmm_entrada"] // 100).groupby("h")["pnl"].agg(["mean", "count"]).reset_index()
    motivos = t.groupby(["perfil", "motivo"])["pnl"].agg(["count", "mean"]).reset_index()

    cache = M02 / "analises" / "ANALISE_002_cache.json"
    if cache.exists() and not refazer:
        c2 = json.loads(cache.read_text())
    else:
        import analise_002_timeframes as a2
        import mb_motor as mb
        from analise_001 import so_sessoes_completas
        from tradetech.dados import carregar_serie

        nulo, expb = [], []
        for serie in ("WINFUT", "WDOFUT"):
            for tf in a2.TFS:
                for sl, sg in a2.GEOMETRIAS:
                    r = a2.geometria_nula(serie, tf, sl, sg, reps=10)
                    nulo.append({"serie": serie, "tf": tf, "sl": sl, "sg": sg, "bruto": r["bruto"], "t": r["t"], "anos": r["anos positivos"]})
                    print("nulo", serie, tf, sl, sg, flush=True)
        for tf in a2.TFS:
            d0 = so_sessoes_completas(carregar_serie("WINFUT", f"{tf}min"))
            bp = mb.Params(sl_min=0.0, sg_min=0.0, gap_max_min=2 * tf, max_barras=max(4, int(round(100 / tf))))
            dd0 = mb.gerar_sinais(mb.preparar(d0, bp), bp)
            e = a2.expansao_apos_brilhante(dd0.dropna(subset=["atr"]))
            expb.append({"tf": tf, "eventos": e["eventos"], "razao": e["razão média"], "controle": e["controle"], "t": e["t"]})
        c2 = {"nulo": nulo, "expansao": expb}
        cache.write_text(json.dumps(c2, default=limpo))
    return {"equity": equity, "hora": registros(hora), "motivos": registros(motivos), **c2}


# ---------------------------------------------------------------------------------------------------------------- html
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refazer", action="store_true")
    args = ap.parse_args()
    ev = carregar_eventos()
    dados = {
        "cobertura": bloco_cobertura(),
        "hipoteses": bloco_hipoteses(),
        "candles": bloco_candles(),
        "alarmes": bloco_alarmes(ev),
        "m16": bloco_m16(ev),
        "m02": bloco_m02(args.refazer),
    }
    html = (Path(__file__).with_name("painel_template.html")).read_text(encoding="utf-8")
    html = html.replace("/*__DADOS__*/", "const DADOS = " + json.dumps(dados, separators=(",", ":"), default=limpo) + ";")
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(html, encoding="utf-8")
    print("gravado", SAIDA.relative_to(RAIZ), f"{SAIDA.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
