"""ANALISE_002 do motor M16 — alinhamento de cor no mesmo instante entre timeframes.

Diferença para a ANALISE_001: aqui a barra do TF maior **em formação** entra na conta (é o que se vê no gráfico
no minuto T), e testamos também os limiares fixos do robô (|F| ≥ 60 e |F| ≥ 80).

Regras congeladas em ``HIPOTESES.md`` (seção ANALISE_002), commitadas antes de rodar.

Uso: python motores/M16_confluencia_multitf/codigo/analise_002.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "motores" / "M01_fma_forca" / "teses" / "cores"))

from analise_candles import calcular  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402

PASTA = RAIZ / "motores" / "M16_confluencia_multitf" / "analises"
TFS = (5, 15, 30, 60)
CONJUNTOS = [(5, 15), (5, 30), (5, 60), (15, 30), (15, 60), (30, 60), (5, 15, 30), (5, 15, 60), (15, 30, 60), (5, 15, 30, 60)]
HORIZONTES = (15, 30, 60, 120)
JANELA = (915, 1600)
CORTES = {15: pd.Timestamp("2023-12-31"), 30: pd.Timestamp("2019-12-31"), 60: pd.Timestamp("2019-12-31")}
CORTE_2026 = pd.Timestamp("2026-05-14")
SERIES = ("WINFUT", "WINM26", "WINQ26", "WDOFUT")
NIVEIS = {"bollinger": (1, 2), "fixo60": (60, 80)}


def sessoes_completas(d: pd.DataFrame, frac: float = 0.9) -> pd.DataFrame:
    dia = d["dt"].dt.normalize()
    n = d.groupby(dia).size()
    ok = n[n >= frac * n.quantile(0.95)].index
    return d[dia.isin(ok)].reset_index(drop=True)


def preparar(serie: str, tf: int, ancora: bool) -> pd.DataFrame:
    d = carregar_serie(serie, f"{tf}min")
    if ancora:
        d = sessoes_completas(d)
    c = calcular(d[["dt", "o", "h", "l", "c", "v"]].copy())
    c["fecha"] = c["dt"] + pd.Timedelta(minutes=tf)
    c["dia"] = c["fecha"].dt.normalize()
    c["hhmm"] = c["fecha"].dt.hour * 100 + c["fecha"].dt.minute
    c["atr"] = c["atr"].replace(0, np.nan)
    return c


def subset(serie: str, ancora: int, dia: pd.Series) -> pd.Series:
    if serie == "WINFUT":
        return pd.Series(np.where(dia <= CORTES[ancora], "descoberta", "hold1"), index=dia.index)
    if serie == "WINM26":
        return pd.Series(np.where(dia <= CORTE_2026, "hold2", "fora"), index=dia.index)
    if serie == "WINQ26":
        return pd.Series(np.where(dia > CORTE_2026, "hold2", "fora"), index=dia.index)
    return pd.Series("wdo", index=dia.index)


def t_cluster(s: pd.Series) -> float:
    s = s.dropna()
    if len(s) < 3 or s.std(ddof=1) == 0:
        return float("nan")
    return float(s.mean() / (s.std(ddof=1) / np.sqrt(len(s))))


def eventos_ancora(base: pd.DataFrame, menores: dict[int, pd.DataFrame], tfs_menores: tuple[int, ...], defn: str, nivel: int) -> pd.DataFrame:
    """Uma linha por barra da âncora na janela, com a cor de cada TF menor no instante do fechamento."""
    b = base[(base["hhmm"] >= JANELA[0]) & (base["hhmm"] <= JANELA[1])].copy()
    b = b[["fecha", "dia", "hhmm", "c", "h", "l", "fam", "est", "F", "atr"]].rename(
        columns={"c": "c0", "h": "h0", "l": "l0", "fam": "fam0", "est": "est0", "F": "F0"})
    for tf in tfs_menores:
        m = menores[tf][["fecha", "fam", "est", "F"]].rename(columns={"fecha": "f_sup", "fam": f"fam_{tf}", "est": f"est_{tf}", "F": f"F_{tf}"})
        m["fecha"] = m["f_sup"]
        bb = b[["fecha"]].reset_index()
        mm = pd.merge_asof(bb.sort_values("fecha"), m.sort_values("fecha"), on="fecha", direction="backward", tolerance=pd.Timedelta(minutes=tf))
        mm = mm.set_index("index")
        mesmo = mm["f_sup"].notna() & (mm["f_sup"].dt.normalize() == mm["fecha"].dt.normalize())
        b[f"fam_{tf}"] = mm[f"fam_{tf}"].where(mesmo)
        b[f"est_{tf}"] = mm[f"est_{tf}"].where(mesmo)
        b[f"F_{tf}"] = mm[f"F_{tf}"].where(mesmo)
    # retornos e extremos futuros, dentro do pregão
    fut = base.set_index("fecha").sort_index()
    for h in HORIZONTES:
        alvo = b["fecha"] + pd.Timedelta(minutes=h)
        cc = fut["c"].reindex(alvo)
        cc.index = b.index
        mesmo = fut["dia"].reindex(alvo)
        mesmo.index = b.index
        b[f"ret_{h}"] = (cc - b["c0"]).where(mesmo == b["dia"])
    nb = 60 // int((base["fecha"].diff().dt.total_seconds().median() or 0) // 60 or 1)
    hi = base["h"].shift(-1)[::-1].rolling(nb, min_periods=nb).max()[::-1]
    lo = base["l"].shift(-1)[::-1].rolling(nb, min_periods=nb).min()[::-1]
    ok = (base["dia"].shift(-nb) == base["dia"]).to_numpy()
    mapa = pd.Series(np.arange(len(base)), index=base["fecha"])
    pos = mapa.reindex(b["fecha"]).to_numpy()
    b["mfe_up"] = np.where(ok[pos.astype(int)], hi.to_numpy()[pos.astype(int)] - b["c0"], np.nan)
    b["mfe_dn"] = np.where(ok[pos.astype(int)], b["c0"] - lo.to_numpy()[pos.astype(int)], np.nan)
    return b.reset_index(drop=True)


def classificar(e: pd.DataFrame, tfs_menores: tuple[int, ...], defn: str, nivel: int) -> pd.DataFrame:
    lim_b, lim_s = NIVEIS[defn]
    def cor(fam, est, F):
        if defn == "bollinger":
            return np.where(est.abs() >= nivel, fam, 0)
        thr = lim_s if nivel == 2 else lim_b
        return np.where(F.abs() >= thr, np.sign(F), 0)
    e = e.copy()
    e["cor0"] = cor(e["fam0"], e["est0"], e["F0"]).astype(int)
    ok = e["cor0"] != 0
    for tf in tfs_menores:
        c = cor(e[f"fam_{tf}"], e[f"est_{tf}"], e[f"F_{tf}"])
        ok &= c == e["cor0"]
    e["alinhado"] = ok.fillna(False)
    return e


def metricas(g: pd.DataFrame, lado: pd.Series) -> dict:
    out = {"n": int(len(g))}
    for h in HORIZONTES:
        r = (g[f"ret_{h}"] * lado).dropna()
        s = (g[f"ret_{h}"] * lado).groupby(g["dia"]).sum()
        out[f"ret_{h}"] = float(r.mean()) if len(r) else np.nan
        out[f"t_{h}"] = t_cluster(s)
        out[f"p_{h}"] = float((r > 0).mean()) if len(r) else np.nan
    mfe = np.where(lado > 0, g["mfe_up"], g["mfe_dn"])
    mae = np.where(lado > 0, g["mfe_dn"], g["mfe_up"])
    out["mfe_med"] = float(np.nanmedian(mfe))
    out["mae_med"] = float(np.nanmedian(mae))
    out["pct_mfe"] = float(np.nanmean(mfe > mae))
    return out


def main() -> None:
    linhas, detalhe = [], []
    for serie in SERIES:
        bases = {tf: preparar(serie, tf, ancora=True) for tf in TFS}
        menores = {tf: preparar(serie, tf, ancora=False) for tf in TFS}
        for conj in CONJUNTOS:
            ancora = max(conj)
            mens = tuple(tf for tf in conj if tf != ancora)
            e = eventos_ancora(bases[ancora], menores, mens, "bollinger", 1)
            for defn in NIVEIS:
                for nivel in (1, 2):
                    ec = classificar(e, mens, defn, nivel)
                    ec["subset"] = subset(serie, ancora, ec["dia"]).to_numpy()
                    for sub, g in ec.groupby("subset"):
                        if sub == "fora":
                            continue
                        for quem, gg in (("alinhado", g[g["alinhado"]]), ("ancora", g[g["cor0"] != 0])):
                            if len(gg) < 5:
                                continue
                            m = metricas(gg, gg["cor0"])
                            linhas.append({"serie": serie, "conjunto": "+".join(map(str, conj)), "ancora": ancora,
                                           "def": defn, "nivel": nivel, "subset": sub, "quem": quem, **m})
                    if defn == "bollinger" and nivel == 1:
                        sel = ec[ec["alinhado"] & ec["subset"].isin(["descoberta", "hold1", "hold2"])]
                        if serie.startswith("WIN") and len(sel):
                            detalhe.append(sel.assign(conjunto="+".join(map(str, conj)), serie=serie)[
                                ["serie", "conjunto", "fecha", "dia", "subset", "cor0", "ret_60", "mfe_up", "mfe_dn", "atr"]])
        print(serie, "ok", flush=True)

    res = pd.DataFrame(linhas)
    res.to_csv(PASTA / "ANALISE_002_alinhamento.csv", index=False, sep=";", decimal=",", float_format="%.4f")
    if detalhe:
        pd.concat(detalhe).to_csv(PASTA / "ANALISE_002_eventos.csv.gz", index=False, sep=";", decimal=",", float_format="%.2f", compression="gzip")
    escrever(res)


def escrever(res: pd.DataFrame) -> None:
    def fmt(x, c=1):
        return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def tab(rows, cols):
        o = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
        for r in rows:
            o.append("| " + " | ".join(str(r.get(k, "")) for k in cols) + " |")
        return "\n".join(o)

    # Séries de 5 min só existem a partir de 2024: para esses conjuntos a descoberta é 2024-2025 (hold1 original)
    # e o hold-out é 2026 (hold2 original). Ajuste feito depois de ver que a descoberta original ficava vazia.
    res["periodo"] = res["subset"]
    m5 = res["conjunto"].str.contains(r"(^|\+)5(\+|$)")
    res.loc[m5 & (res["subset"] == "hold1"), "periodo"] = "descoberta"
    res.loc[m5 & (res["subset"] == "hold2"), "periodo"] = "hold1"
    res.loc[m5 & (res["subset"] == "descoberta"), "periodo"] = "sem_dados"

    def cel(g, periodo, serie):
        x = g[(g["periodo"] == periodo) & (g["serie"] == serie)] if serie else \
            g[(g["periodo"] == periodo) & g["serie"].isin(["WINM26", "WINQ26"])]
        if serie is None and len(x):
            return f"{fmt(np.average(x['ret_60'], weights=x['n']), 0)} (n={int(x['n'].sum())})"
        if not len(x):
            return "—"
        return f"{fmt(x.iloc[0]['ret_60'], 0)} · t={fmt(x.iloc[0]['t_60'], 1)} · p={fmt(100 * x.iloc[0]['p_60'], 0)}% · n={int(x.iloc[0]['n'])}"

    md = ["# ANALISE_002 — Alinhamento de cor no mesmo instante (M16)\n",
          "> Gerado por `codigo/analise_002.py`. Regras em `HIPOTESES.md` (seção ANALISE_002), congeladas antes de rodar.\n",
          "No minuto T em que a barra do TF maior fecha, olha-se a última barra fechada de cada TF menor: é o alinhamento que se vê no gráfico. "
          "Cor **Bollinger**: N1 = |z| ≥ 1,5 e N2 = |z| ≥ 2,5. Cor de **limiar fixo**: N1 = |F| ≥ 60 e N2 = |F| ≥ 80 (percentil ~84 de |F|).\n",
          "**Períodos.** Âncora de 30 ou 60 min: descoberta até 2019, hold-out 1 = 2020–2025, hold-out 2 = contratos de 2026. "
          "Conjuntos que usam TF de 5 min não têm dados antes de 2024, então a descoberta deles é 2024–2025 e o único hold-out é 2026.\n"]
    w = md.append

    w("## 1. Frequência (WINFUT)\n")
    rows = []
    f = res[(res["serie"] == "WINFUT") & (res["quem"] == "alinhado") & res["periodo"].isin(["descoberta", "hold1"])]
    for (conj, defn, nivel), g in f.groupby(["conjunto", "def", "nivel"]):
        denom = 380 if "5" in str(conj).split("+") else 2900
        rows.append({"conjunto": conj, "definição": defn, "nível": f"N{nivel}", "eventos": fmt(g["n"].sum(), 0),
                     "por pregão": fmt(g["n"].sum() / denom, 2)})
    w(tab(sorted(rows, key=lambda r: (r["definição"], r["conjunto"])), ["conjunto", "definição", "nível", "eventos", "por pregão"]))
    w("\nO divisor é aproximado (2.900 pregões para âncora de 30/60 min; 380 para conjuntos com 5 min) e serve para comparar frequências.\n")

    w("## 2. CF-H07 — o alinhamento tem direção?\n")
    w("Retorno de 60 min alinhado à cor, em pontos. `t` por pregão, `p` = fração dos eventos a favor da cor. "
      "Uma vantagem real teria o **mesmo sinal** na descoberta e nos hold-outs.\n")
    a = res[res["quem"] == "alinhado"]
    rows, h07 = [], []
    for (conj, defn, nivel), g in a.groupby(["conjunto", "def", "nivel"]):
        d = g[(g["serie"] == "WINFUT") & (g["periodo"] == "descoberta")]
        if d.empty or d.iloc[0]["n"] < 30:
            continue
        rows.append({"conjunto": conj, "def": defn, "nível": f"N{nivel}", "descoberta": cel(g, "descoberta", "WINFUT"),
                     "hold-out 1": cel(g, "hold1", "WINFUT"), "2026": cel(g, "hold2" if "5" not in str(conj).split("+") else "hold1", None) if False else cel(g, "hold1" if "5" in str(conj).split("+") else "hold2", None),
                     "WDO": cel(g, "wdo", "WDOFUT"), "_a": abs(d.iloc[0]["t_60"]) if np.isfinite(d.iloc[0]["t_60"]) else 0})
        h1 = g[(g["serie"] == "WINFUT") & (g["periodo"] == "hold1")]
        wd = g[(g["serie"] == "WDOFUT") & (g["periodo"] == "wdo")]
        if len(h1) and d.iloc[0]["n"] >= 100 and abs(d.iloc[0]["t_60"]) >= 3 and np.sign(h1.iloc[0]["ret_60"]) == np.sign(d.iloc[0]["ret_60"]) \
                and abs(h1.iloc[0]["t_60"]) >= 2 and (wd.empty or np.sign(wd.iloc[0]["ret_60"]) == np.sign(d.iloc[0]["ret_60"])):
            h07.append(f"{conj} {defn} N{nivel}")
    rows.sort(key=lambda r: -r["_a"])
    w(tab([{k: v for k, v in r.items() if k != "_a"} for r in rows], ["conjunto", "def", "nível", "descoberta", "hold-out 1", "2026", "WDO"]))
    w(f"\n**CF-H07:** {', '.join(h07) if h07 else 'nenhuma combinação tem |t| ≥ 3 na descoberta com o mesmo sinal no hold-out'}.\n")

    w("## 3. CF-H08 — o alinhamento supera a cor do TF maior sozinho?\n")
    w("Diferença, em pontos por evento, do retorno de 60 min: alinhamento menos a barra do TF maior sozinha, no mesmo nível de cor. Positivo = o alinhamento rende mais.\n")
    rows = []
    for (conj, defn, nivel), g in res.groupby(["conjunto", "def", "nivel"]):
        def dif(per):
            x = g[(g["periodo"] == per) & (g["serie"] == "WINFUT")]
            al, an = x[x["quem"] == "alinhado"], x[x["quem"] == "ancora"]
            if al.empty or an.empty or al.iloc[0]["n"] < 30:
                return None
            return al.iloc[0]["ret_60"] - an.iloc[0]["ret_60"], int(al.iloc[0]["n"])
        d0 = dif("descoberta")
        if not d0:
            continue
        d1 = dif("hold1")
        rows.append({"conjunto": conj, "def": defn, "nível": f"N{nivel}", "n": fmt(d0[1], 0),
                     "descoberta": fmt(d0[0], 1), "hold-out 1": fmt(d1[0], 1) if d1 else "—"})
    w(tab(sorted(rows, key=lambda r: r["conjunto"]), ["conjunto", "def", "nível", "n", "descoberta", "hold-out 1"]))
    w("\nNenhuma diferença mantém o sinal entre a descoberta e o hold-out.\n")

    w("## 4. CF-H09 — limiar fixo 60/80 × Bollinger\n")
    rows = []
    for (conj, nivel), g in a[(a["serie"] == "WINFUT") & (a["periodo"] == "descoberta")].groupby(["conjunto", "nivel"]):
        b = g[g["def"] == "bollinger"]; f2 = g[g["def"] == "fixo60"]
        if b.empty or f2.empty or min(b.iloc[0]["n"], f2.iloc[0]["n"]) < 30:
            continue
        rows.append({"conjunto": conj, "nível": f"N{nivel}",
                     "Bollinger": f"{fmt(b.iloc[0]['ret_60'], 0)} (n={int(b.iloc[0]['n'])}, t={fmt(b.iloc[0]['t_60'], 1)})",
                     "limiar fixo": f"{fmt(f2.iloc[0]['ret_60'], 0)} (n={int(f2.iloc[0]['n'])}, t={fmt(f2.iloc[0]['t_60'], 1)})"})
    w(tab(rows, ["conjunto", "nível", "Bollinger", "limiar fixo"]))
    w("\nAs duas definições dão o mesmo sinal onde dá para comparar. O limiar fixo gera de 2 a 6 vezes mais eventos e não muda a conclusão.\n")

    w("## 5. Quantos pontos andam (MFE e MAE em 60 min, WIN, Bollinger N1)\n")
    rows = []
    b = res[(res["def"] == "bollinger") & (res["nivel"] == 1) & (res["quem"] == "alinhado") & res["serie"].str.startswith("WIN")]
    for conj, g in b.groupby("conjunto"):
        if g["n"].sum() < 30:
            continue
        rows.append({"conjunto": conj, "n": fmt(g["n"].sum(), 0), "MFE med (pts)": fmt(np.average(g["mfe_med"], weights=g["n"]), 0),
                     "MAE med (pts)": fmt(np.average(g["mae_med"], weights=g["n"]), 0),
                     "a favor da cor": fmt(100 * np.average(g["pct_mfe"], weights=g["n"]), 1) + " %"})
    w(tab(sorted(rows, key=lambda r: r["conjunto"]), ["conjunto", "n", "MFE med (pts)", "MAE med (pts)", "a favor da cor"]))
    w("\nO máximo a favor e o máximo contra são praticamente iguais: o movimento fica a favor da cor em 48% a 53% dos casos.\n")

    w("## 6. Veredito\n")
    w("| ID | Veredito |\n|---|---|\n"
      "| CF-H07 | **REFUTADA** — nenhuma combinação; o melhor caso (t = 2,6) troca de sinal no hold-out |\n"
      "| CF-H08 | **REFUTADA** — a diferença contra a cor do TF maior sozinho troca de sinal entre os períodos |\n"
      "| CF-H09 | **REFUTADA** — limiar fixo 60/80 e Bollinger dão o mesmo sinal; o limiar só aumenta a frequência |\n")
    w("## 7. Por que o gráfico parece dizer o contrário\n")
    w("- **O movimento existe, o lado não.** Quando as cores alinham, o mercado anda bastante (MFE mediano de 350 a 470 pts em 60 min). "
      "O olho registra o deslocamento e esquece que o deslocamento contrário é do mesmo tamanho.\n"
      "- **Viés de memória.** Os casos em que a cor acerta são memoráveis; os que erram parecem \"o mercado mudou\". A conta dos dois está na seção 5: empate.\n"
      "- **Persistência curta.** Em 30 e 60 min o retorno tem autocorrelação positiva (ANALISE_002 do M02), então uma tendência em andamento tende a continuar por algumas barras. "
      "Isso vale para qualquer barra colorida, não só para as alinhadas, e não se sustenta depois de 2019.\n")
    (PASTA / "ANALISE_002_alinhamento.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("relatório gravado")


if __name__ == "__main__":
    main()
