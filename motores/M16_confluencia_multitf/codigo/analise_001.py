"""ANALISE_001 do motor M16 — confluência de cor em múltiplos timeframes.

Executa as hipóteses CF-H01..CF-H06 exatamente como congeladas em ``HIPOTESES.md`` / ``METODO.md`` e regenera:
  * ``analises/ANALISE_001_confluencia.md``
  * ``analises/ANALISE_001_estrategias.csv`` (todas as 132 estratégias × conjuntos de dados)
  * ``analises/ANALISE_001_eventos.csv``     (estatísticas descritivas por conjunto/evento)

Uso: python motores/M16_confluencia_multitf/codigo/analise_001.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cf_motor as cf  # noqa: E402

RAIZ = cf.RAIZ
PASTA = RAIZ / "motores" / "M16_confluencia_multitf" / "analises"
CORTE_2026 = pd.Timestamp("2026-05-14")
CORTES = {5: pd.Timestamp("2025-06-30"), 15: pd.Timestamp("2023-12-31"), 30: pd.Timestamp("2019-12-31")}
SERIES = ("WINFUT", "WINM26", "WINQ26", "WDOFUT")
SUBS = ("descoberta", "hold1", "hold2", "wdo")


def subconjunto(serie: str, base: int, dia: pd.Series) -> pd.Series:
    if serie == "WINFUT":
        return pd.Series(np.where(dia <= CORTES[base], "descoberta", "hold1"), index=dia.index)
    if serie == "WINM26":
        return pd.Series(np.where(dia <= CORTE_2026, "hold2", "fora"), index=dia.index)
    if serie == "WINQ26":
        return pd.Series(np.where(dia > CORTE_2026, "hold2", "fora"), index=dia.index)
    return pd.Series("wdo", index=dia.index)


def fmt(x, casas=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    if isinstance(x, (int, np.integer)):
        return f"{x:,}".replace(",", ".")
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tabela(linhas: list[dict], colunas: list[str]) -> str:
    if not linhas:
        return "_(sem linhas)_"
    out = ["| " + " | ".join(colunas) + " |", "|" + "|".join("---" for _ in colunas) + "|"]
    for l in linhas:
        out.append("| " + " | ".join(str(l.get(c, "")) for c in colunas) + " |")
    return "\n".join(out)


def nome_conj(sup: tuple[int, ...], base: int) -> str:
    return f"{base}" + "".join(f"+{s}" for s in sup) if sup else f"{base} (TF único)"


def main() -> None:
    estr, evs, descr = [], [], []
    universo: dict[tuple[int, str], pd.DatetimeIndex] = {}
    media_nulo: dict[tuple[int, str, tuple, str], float] = {}

    for base, conjuntos in cf.CONJUNTOS.items():
        for serie in SERIES:
            ds = cf.montar(serie, base)
            sub_dia = subconjunto(serie, base, ds.x0["dia"])
            for s in SUBS:
                dias = pd.DatetimeIndex(sorted(ds.x0.loc[sub_dia == s, "dia"].unique()))
                if len(dias):
                    universo[(base, s)] = dias if (base, s) not in universo else universo[(base, s)].union(dias)
            custo = cf.CUSTO_WIN if serie.startswith("WIN") else 0.0
            for sl, sg in cf.GEOMETRIAS:
                tn = cf.nulo(ds, sl, sg, custo)
                tn["subset"] = subconjunto(serie, base, tn["dia"]).to_numpy()
                for s, g in tn.groupby("subset"):
                    media_nulo[(base, serie, (sl, sg), s)] = float(g["pnl"].mean())
            for sup in [()] + list(conjuntos):
                for nivel in cf.NIVEIS:
                    ev = cf.eventos(ds, sup, nivel, "A") if sup else cf.eventos(ds, (), nivel, "A")
                    for modo in (("A", "B") if sup else ("A",)):
                        e = ev if modo == "A" else cf.eventos(ds, sup, nivel, "B")
                        te = cf.tabela_eventos(ds, e)
                        if not te.empty:
                            te["subset"] = subconjunto(serie, base, te["dia"]).to_numpy()
                            te.insert(0, "conjunto", nome_conj(sup, base))
                            te.insert(1, "base", base)
                            te.insert(2, "serie", serie)
                            te.insert(3, "sup", "+".join(map(str, sup)))
                            te.insert(4, "nivel", nivel)
                            te.insert(5, "modo", modo)
                            evs.append(te)
                    for lado_nome, lado in cf.LADOS.items():
                        for sl, sg in cf.GEOMETRIAS:
                            t = cf.simular_eventos(ds, ev, lado, sl, sg, custo)
                            if t.empty:
                                continue
                            t = t.assign(base=base, serie=serie, sup="+".join(map(str, sup)), nivel=nivel, lado_nome=lado_nome,
                                         geom=f"{sl}/{sg}", conjunto=nome_conj(sup, base))
                            t["subset"] = subconjunto(serie, base, t["dia"]).to_numpy()
                            estr.append(t)
            print(f"base {base} {serie} ok", flush=True)

    trades = pd.concat(estr, ignore_index=True)
    trades = trades[trades["subset"] != "fora"]
    eventos = pd.concat(evs, ignore_index=True)
    eventos = eventos[eventos["subset"] != "fora"]

    # ------------------------------------------------------------------ estratégias
    linhas = []
    chaves = ["base", "conjunto", "sup", "nivel", "lado_nome", "geom"]
    por_dia_cache = {}
    for ch, g in trades.groupby(chaves + ["subset"]):
        base, conj, sup, nivel, lado_nome, geom, sub = ch
        sl, sg = map(float, geom.split("/"))
        serie_set = g["serie"].unique()
        mn = np.mean([media_nulo.get((base, s, (sl, sg), sub), np.nan) for s in serie_set])
        dias = universo[(base, sub)]
        m = cf.metricas_estrategia(g, dias, mn)
        if m["n"]:
            s_dia = g.groupby("dia")["pnl"].sum().reindex(dias, fill_value=0.0)
            por_dia_cache[ch] = s_dia
            linhas.append({"base": base, "conjunto": conj, "sup": sup, "nivel": nivel, "lado": lado_nome, "geom": geom, "subset": sub, "nulo_medio": mn, **m})
    res = pd.DataFrame(linhas)

    # CF-H05: diferença vs TF único (mesmo base, nível, lado, geometria), por pregão
    dif_t = {}
    for ch, s_dia in por_dia_cache.items():
        base, conj, sup, nivel, lado_nome, geom, sub = ch
        if sup == "":
            continue
        ch_unico = (base, nome_conj((), base), "", nivel, lado_nome, geom, sub)
        s_u = por_dia_cache.get(ch_unico)
        if s_u is None:
            continue
        dif_t[ch] = (float((s_dia - s_u).mean()), cf.t_cluster(s_dia - s_u))
    res["dif_unico"] = [dif_t.get((r.base, r.conjunto, r.sup, r.nivel, r.lado, r.geom, r.subset), (np.nan, np.nan))[0] for r in res.itertuples()]
    res["t_dif_unico"] = [dif_t.get((r.base, r.conjunto, r.sup, r.nivel, r.lado, r.geom, r.subset), (np.nan, np.nan))[1] for r in res.itertuples()]
    res.to_csv(PASTA / "ANALISE_001_estrategias.csv", index=False, sep=";", decimal=",", float_format="%.4f")

    larga = res.pivot_table(index=["base", "conjunto", "sup", "nivel", "lado", "geom"], columns="subset",
                            values=["n", "medio", "medio_R", "t_nulo", "t_dia", "wr", "wr_be", "pf", "por_pregao", "dif_unico", "t_dif_unico"], aggfunc="first")
    larga.columns = [f"{a}_{b}" for a, b in larga.columns]
    larga = larga.reset_index()
    for c in ("n_descoberta", "n_hold1", "n_hold2", "n_wdo"):
        if c not in larga:
            larga[c] = 0
    estrat = larga[larga["sup"] != ""].copy()
    estrat["passa"] = (
        (estrat["n_descoberta"] >= 30) & (estrat["t_nulo_descoberta"] >= 3)
        & (estrat["n_hold1"] >= 30) & (estrat["medio_hold1"] > 0) & (estrat["t_nulo_hold1"] >= 2)
        & (estrat["n_hold2"] >= 30) & (estrat["medio_hold2"] > 0) & (estrat["t_nulo_hold2"] >= 2)
        & (estrat["medio_R_wdo"] > 0)
    )
    estrat["passa_descoberta"] = (estrat["n_descoberta"] >= 30) & (estrat["t_nulo_descoberta"] >= 3)
    estrat["passa_h1"] = (estrat["n_hold1"] >= 30) & (estrat["medio_hold1"] > 0) & (estrat["t_nulo_hold1"] >= 2)
    n_total = len(estrat)
    for c in ("dif_unico_hold2", "dif_unico_hold1", "t_dif_unico_descoberta", "dif_unico_descoberta"):
        if c not in estrat:
            estrat[c] = np.nan
    estrat["passa_h05"] = (
        (estrat["n_descoberta"] >= 30) & (estrat["t_dif_unico_descoberta"] >= 2)
        & (estrat["dif_unico_hold1"] > 0) & (estrat["dif_unico_hold2"] > 0)
    )
    h05_desc = estrat[(estrat["n_descoberta"] >= 30) & (estrat["t_dif_unico_descoberta"] >= 2)]

    # ------------------------------------------------------------------ eventos (H01, H02, H03, H06)
    win_all = eventos[eventos["serie"].isin(["WINFUT"])]
    desc_rows = []
    for (base, conj, sup, nivel, modo), g in eventos.groupby(["base", "conjunto", "sup", "nivel", "modo"]):
        for sub in SUBS:
            gg = g[g["subset"] == sub]
            if gg.empty:
                continue
            dias = universo[(base, sub)]
            n = len(gg)
            row = {"base": base, "conjunto": conj, "sup": sup, "nivel": nivel, "modo": modo, "subset": sub, "n_eventos": n,
                   "eventos_por_pregao": n / len(dias), "ratio_medio": gg["ratio"].mean()}
            for m in cf.HORIZONTES_MIN:
                col = f"ret_{m}"
                if col in gg:
                    s = gg.groupby("dia")[col].sum().reindex(dias, fill_value=0.0)
                    row[f"ret_{m}"] = gg[col].mean()
                    row[f"t_ret_{m}"] = cf.t_cluster(s)
            row["mfe_med"] = gg["mfe"].median()
            row["mae_med"] = gg["mae"].median()
            row["mfe_p75"] = gg["mfe"].quantile(0.75)
            row["mfe_p90"] = gg["mfe"].quantile(0.90)
            row["mae_p75"] = gg["mae"].quantile(0.75)
            row["mfe_atr_med"] = (gg["mfe"] / gg["atr"]).median()
            row["mae_atr_med"] = (gg["mae"] / gg["atr"]).median()
            desc_rows.append(row)
    desc = pd.DataFrame(desc_rows)
    # CF-H01: expansão vs TF único (mesmo base, nível, subset); t Welch por pregão
    exp_rows = []
    for (base, conj, sup, nivel, sub), g in eventos[(eventos["modo"] == "A") & (eventos["sup"] != "")].groupby(["base", "conjunto", "sup", "nivel", "subset"]):
        u = eventos[(eventos["base"] == base) & (eventos["sup"] == "") & (eventos["nivel"] == nivel) & (eventos["subset"] == sub) & (eventos["serie"] == g["serie"].iloc[0])]
        if len(g) < 20 or len(u) < 20:
            continue
        a = g.groupby("dia")["ratio"].mean().dropna()
        b = u.groupby("dia")["ratio"].mean().dropna()
        se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)) if len(a) > 2 and len(b) > 2 else np.nan
        exp_rows.append({"base": base, "conjunto": conj, "nivel": nivel, "subset": sub, "n": len(g), "ratio_conf": g["ratio"].mean(), "ratio_unico": u["ratio"].mean(),
                         "dif": g["ratio"].mean() - u["ratio"].mean(), "t": (g["ratio"].mean() - u["ratio"].mean()) / se if se == se and se > 0 else np.nan})
    exp = pd.DataFrame(exp_rows)
    desc.to_csv(PASTA / "ANALISE_001_eventos.csv", index=False, sep=";", decimal=",", float_format="%.4f")

    # ------------------------------------------------------------------ relatório
    md = ["# ANALISE_001 — Confluência de cor em múltiplos timeframes (M16)\n",
          "> Gerado por `motores/M16_confluencia_multitf/codigo/analise_001.py`. Não editar à mão. Regras: `METODO.md` e `HIPOTESES.md` (congeladas antes de rodar; a Emenda 1 foi anterior a qualquer resultado).\n"]
    w = md.append

    w("## 1. Dados e poder estatístico\n")
    linhas = []
    for base in cf.CONJUNTOS:
        for sub in SUBS:
            if (base, sub) in universo:
                linhas.append({"base": f"{base} min", "conjunto": sub, "pregões": fmt(len(universo[(base, sub)])),
                               "início": universo[(base, sub)].min().date(), "fim": universo[(base, sub)].max().date()})
    w(tabela(linhas, ["base", "conjunto", "pregões", "início", "fim"]))
    w("")

    w("## 2. Frequência do alerta (CF-H06)\n")
    w("Eventos por pregão **no WINFUT inteiro** (descoberta + hold-out 1). `A` = TFs fecham juntos; `B` = TF superior fechou há no máximo 1 período.\n")
    linhas = []
    for (base, conj, nivel, modo), g in desc[(desc["subset"].isin(["descoberta", "hold1"]))].groupby(["base", "conjunto", "nivel", "modo"]):
        n = g["n_eventos"].sum()
        dias = sum(len(universo[(base, s)]) for s in ("descoberta", "hold1"))
        linhas.append({"conjunto": conj, "nível": f"N{nivel}", "modo": modo, "eventos": fmt(int(n)), "por pregão": fmt(n / dias, 2)})
    w(tabela(sorted(linhas, key=lambda r: (r["conjunto"], r["nível"], r["modo"])), ["conjunto", "nível", "modo", "eventos", "por pregão"]))
    w("")

    w("## 3. CF-H01 — a confluência antecipa mais expansão de range que a cor em TF único?\n")
    w("`ratio` = range da barra base seguinte ÷ média do mesmo horário. `t` = Welch por pregão (confluência − TF único). Apenas linhas com ≥ 20 eventos.\n")
    linhas = []
    for (base, conj, nivel), g in exp.groupby(["base", "conjunto", "nivel"]):
        r = {"conjunto": conj, "nível": f"N{nivel}"}
        for sub in ("descoberta", "hold1", "hold2", "wdo"):
            x = g[g["subset"] == sub]
            if len(x):
                x = x.iloc[0]
                r[sub] = f"{fmt(x['ratio_conf'])} vs {fmt(x['ratio_unico'])} (n={x['n']}, t={fmt(x['t'], 1)})"
        linhas.append(r)
    w(tabela(sorted(linhas, key=lambda r: (r["conjunto"], r["nível"])), ["conjunto", "nível", "descoberta", "hold1", "hold2", "wdo"]))
    h01_ok = []
    for (base, conj, nivel), g in exp.groupby(["base", "conjunto", "nivel"]):
        d = g[g["subset"] == "descoberta"]
        h1 = g[g["subset"] == "hold1"]
        h2 = g[g["subset"] == "hold2"]
        if len(d) and len(h1) and len(h2):
            if d.iloc[0]["t"] >= 3 and d.iloc[0]["dif"] > 0 and h1.iloc[0]["t"] >= 2 and h2.iloc[0]["t"] >= 2:
                h01_ok.append(f"{conj} N{nivel}")
    w(f"\n**Conjuntos que satisfazem CF-H01:** {', '.join(h01_ok) if h01_ok else 'nenhum'}.\n")

    w("## 4. CF-H02 — direção: retorno alinhado ao sinal (continuação > 0; fade < 0)\n")
    w("Retorno em pontos de `sinal × (c[i+h] − o[i+1])`; `t` por pregão. Modo A, conjuntos com ≥ 30 eventos na descoberta, ordenados por |t| na descoberta (top 20; a lista completa está no CSV).\n")
    linhas = []
    base_a = desc[(desc["modo"] == "A")]
    for (base, conj, nivel), g in base_a.groupby(["base", "conjunto", "nivel"]):
        d = g[g["subset"] == "descoberta"]
        if d.empty or d.iloc[0]["n_eventos"] < 30:
            continue
        for m in cf.HORIZONTES_MIN:
            col, tcol = f"ret_{m}", f"t_ret_{m}"
            if col not in d or pd.isna(d.iloc[0].get(col)):
                continue
            r = {"conjunto": conj, "nível": f"N{nivel}", "h (min)": m, "n desc.": int(d.iloc[0]["n_eventos"]), "_abs": abs(d.iloc[0][tcol]) if d.iloc[0][tcol] == d.iloc[0][tcol] else 0}
            for sub, rot in (("descoberta", "desc."), ("hold1", "hold1"), ("hold2", "hold2"), ("wdo", "WDO")):
                x = g[g["subset"] == sub]
                r[rot] = f"{fmt(x.iloc[0][col], 1)} (t={fmt(x.iloc[0][tcol], 1)})" if len(x) and col in x and pd.notna(x.iloc[0].get(col)) else "—"
            linhas.append(r)
    linhas.sort(key=lambda r: -r["_abs"])
    w(tabela(linhas[:20], ["conjunto", "nível", "h (min)", "n desc.", "desc.", "hold1", "hold2", "WDO"]))
    h02_ok = []
    for r in linhas:
        pass
    for (base, conj, nivel), g in base_a.groupby(["base", "conjunto", "nivel"]):
        for m in cf.HORIZONTES_MIN:
            col, tcol = f"ret_{m}", f"t_ret_{m}"
            if col not in g:
                continue
            v = {sub: g[g["subset"] == sub] for sub in SUBS}
            if any(v[s].empty or pd.isna(v[s].iloc[0].get(col)) for s in SUBS):
                continue
            sg = np.sign(v["descoberta"].iloc[0][col])
            if (abs(v["descoberta"].iloc[0][tcol]) >= 3 and v["descoberta"].iloc[0]["n_eventos"] >= 30
                    and all(np.sign(v[s].iloc[0][col]) == sg and abs(v[s].iloc[0][tcol]) >= 2 for s in ("hold1", "hold2"))
                    and np.sign(v["wdo"].iloc[0][col]) == sg):
                h02_ok.append(f"{conj} N{nivel} h={m}")
    w(f"\n**Combinações que satisfazem CF-H02:** {', '.join(h02_ok) if h02_ok else 'nenhuma'}.\n")

    w("## 5. CF-H03 — quantos pontos dá para capturar (MFE e MAE em 60 min, WIN)\n")
    w("Descritivo, modo A, a favor da cor (continuação). `MFE` = máximo favorável a partir da abertura seguinte; `MAE` = máximo adverso. Valores em pontos (e em ATR da base). "
      "Por simetria, o MFE do **fade** é o MAE da continuação e vice-versa. WIN descoberta + hold-outs 1 e 2 agrupados.\n")
    linhas = []
    sel = eventos[(eventos["serie"].str.startswith("WIN")) & (eventos["modo"] == "A")]
    for (base, conj, nivel), g in sel.groupby(["base", "conjunto", "nivel"]):
        g = g.dropna(subset=["mfe"])
        if len(g) < 30:
            continue
        linhas.append({"conjunto": conj, "nível": f"N{nivel}", "n": fmt(len(g)),
                       "MFE med / p75 / p90 (pts)": f"{fmt(g['mfe'].median(), 0)} / {fmt(g['mfe'].quantile(.75), 0)} / {fmt(g['mfe'].quantile(.9), 0)}",
                       "MAE med / p75 / p90 (pts)": f"{fmt(g['mae'].median(), 0)} / {fmt(g['mae'].quantile(.75), 0)} / {fmt(g['mae'].quantile(.9), 0)}",
                       "MFE med (ATR)": fmt((g["mfe"] / g["atr"]).median()), "MAE med (ATR)": fmt((g["mae"] / g["atr"]).median()),
                       "MFE > MAE %": fmt(100 * (g["mfe"] > g["mae"]).mean(), 1)})
    w(tabela(sorted(linhas, key=lambda r: (r["conjunto"], r["nível"])), ["conjunto", "nível", "n", "MFE med / p75 / p90 (pts)", "MAE med / p75 / p90 (pts)", "MFE med (ATR)", "MAE med (ATR)", "MFE > MAE %"]))
    w("\nLeitura: se `MFE > MAE %` ≈ 50 e as medianas são parecidas, a cor não indica lado — o que o alerta entrega é **amplitude** (quantos pontos o mercado vai andar), não direção.\n")

    w("## 6. CF-H04 e CF-H05 — estratégias com barreira\n")
    w(f"Total testado: **{n_total}** (sem contar TF único). Critério: descoberta `t_vs_nulo` ≥ 3 com n ≥ 30 **e** hold-outs 1 e 2 com média líquida > 0 e `t_vs_nulo` ≥ 2 **e** WDO bruto > 0.\n")
    w(f"- Passam a descoberta (t ≥ 3, n ≥ 30): **{int(estrat['passa_descoberta'].sum())}** de {n_total}")
    w(f"- Passam descoberta **e** hold-out 1: **{int((estrat['passa_descoberta'] & estrat['passa_h1']).sum())}**")
    w(f"- Passam **todos** os critérios (CF-H04): **{int(estrat['passa'].sum())}**\n")
    linhas = []
    top = estrat[estrat["n_descoberta"] >= 30].sort_values("t_nulo_descoberta", ascending=False).head(12)
    for r in top.itertuples():
        def c(sub):
            n = getattr(r, f"n_{sub}", 0)
            if not n or pd.isna(n):
                return "—"
            return f"n={int(n)} · {fmt(getattr(r, f'medio_{sub}'), 1)} pts · t={fmt(getattr(r, f't_nulo_{sub}'), 1)}"
        linhas.append({"conjunto": r.conjunto, "nível": f"N{r.nivel}", "lado": r.lado, "SL/SG (×ATR)": r.geom,
                       "descoberta": c("descoberta"), "hold1": c("hold1"), "hold2": c("hold2"),
                       "WDO (R)": fmt(getattr(r, "medio_R_wdo", np.nan), 2)})
    w("Top 12 pela descoberta (seleção feita **só** na descoberta; `t` = vs nulo; média líquida de 5 pts):\n")
    w(tabela(linhas, ["conjunto", "nível", "lado", "SL/SG (×ATR)", "descoberta", "hold1", "hold2", "WDO (R)"]))
    w("")

    w("### TF único (controle de comparação)\n")
    linhas = []
    un = larga[larga["sup"] == ""].copy()
    for r in un.sort_values(["base", "nivel", "lado", "geom"]).itertuples():
        if getattr(r, "n_descoberta", 0) and r.n_descoberta >= 30:
            linhas.append({"base": f"{r.base} min", "nível": f"N{r.nivel}", "lado": r.lado, "SL/SG": r.geom,
                           "descoberta": f"n={int(r.n_descoberta)} · {fmt(r.medio_descoberta, 1)} pts · WR {fmt(100 * r.wr_descoberta, 0)}% (BE {fmt(100 * r.wr_be_descoberta, 0)}%)",
                           "hold1": f"{fmt(r.medio_hold1, 1)} pts" if getattr(r, "n_hold1", 0) else "—",
                           "hold2": f"{fmt(r.medio_hold2, 1)} pts" if getattr(r, "n_hold2", 0) else "—"})
    w(tabela(linhas, ["base", "nível", "lado", "SL/SG", "descoberta", "hold1", "hold2"]))
    w("\n(Resultados completos em `ANALISE_001_estrategias.csv`. O total de estratégias é menor que 132 porque os conjuntos N2 com 3 TFs quase não geram eventos.)\n")
    w("### CF-H05 — confluência × TF único\n")
    w(f"- Estratégias em que a confluência supera o TF único na descoberta (t ≥ 2 por pregão, n ≥ 30): **{len(h05_desc)}**")
    w(f"- Dessas, com diferença positiva também nos hold-outs 1 **e** 2: **{int(estrat['passa_h05'].sum())}**")
    w("- Cuidado ao ler: a diferença é por **pregão**, e o TF único opera muito mais vezes (até ~9 por pregão no 5 min) pagando custo e perdendo na média. "
      "Parte da \"vantagem\" da confluência é só operar menos. Compare por trade nas tabelas acima.\n")

    w("## 7. Veredito automático (regras congeladas)\n")
    w(f"| ID | Veredito |\n|---|---|\n| CF-H01 | {'CONFIRMADA' if h01_ok else 'NÃO CONFIRMADA'} ({', '.join(h01_ok) or 'nenhum conjunto'}) |\n"
      f"| CF-H02 | {'CONFIRMADA' if h02_ok else 'NÃO CONFIRMADA'} ({', '.join(h02_ok) or 'nenhuma combinação'}) |\n"
      f"| CF-H03 | descritivo (seção 5) |\n"
      f"| CF-H04 | {'CONFIRMADA' if int(estrat['passa'].sum()) else 'NÃO CONFIRMADA'} ({int(estrat['passa'].sum())} de {n_total}) |\n"
      f"| CF-H05 | {'CONFIRMADA' if int(estrat['passa_h05'].sum()) else 'NÃO CONFIRMADA'} ({len(h05_desc)} passam na descoberta; {int(estrat['passa_h05'].sum())} replicam) |\n| CF-H06 | descritivo (seção 2) |\n")

    (PASTA / "ANALISE_001_confluencia.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("gravado", (PASTA / "ANALISE_001_confluencia.md").relative_to(RAIZ))


if __name__ == "__main__":
    main()
