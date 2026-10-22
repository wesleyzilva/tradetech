"""ANALISE_003 — lado pela tabela fraco/forte do robô, no 5 min cruzado com o 15 min.

Faixas congeladas em ``HIPOTESES.md`` (CF-H10, CF-H11): fraco = 70 ≤ |F| < 85, forte = |F| ≥ 85.
Lado = sinal de F. O teste é se a continuação desse lado se sustenta fora da descoberta.

Uso: python motores/M16_confluencia_multitf/codigo/analise_003.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import analise_002 as base  # noqa: E402

PASTA = RAIZ / "motores" / "M16_confluencia_multitf" / "analises"
CORTE = pd.Timestamp("2025-06-30")
NOME = {0: "branco", 1: "fraco", 2: "forte"}
CELULAS = [("fraco", "fraco"), ("fraco", "forte"), ("forte", "fraco"), ("forte", "forte")]


def faixa(F: pd.Series) -> pd.Series:
    a = F.abs()
    return pd.Series(np.where(a >= 85, 2, np.where(a >= 70, 1, 0)), index=F.index).astype(int)


def montar(serie: str) -> pd.DataFrame:
    b = base.preparar(serie, 15, ancora=True)
    m = base.preparar(serie, 5, ancora=False)
    b = b[(b["hhmm"] >= 915) & (b["hhmm"] <= 1600)].copy()
    b["fx15"] = faixa(b["F"])
    b["lado15"] = np.sign(b["F"]).astype(int)
    mm = m[["fecha", "F"]].rename(columns={"fecha": "f5", "F": "F5"})
    mm["fecha"] = mm["f5"]
    bb = b[["fecha"]].reset_index()
    j = pd.merge_asof(bb.sort_values("fecha"), mm.sort_values("fecha"), on="fecha", direction="backward", tolerance=pd.Timedelta(minutes=5))
    j = j.set_index("index")
    mesmo = j["f5"].notna() & (j["f5"].dt.normalize() == j["fecha"].dt.normalize())
    b["F5"] = j["F5"].where(mesmo)
    b["fx5"] = faixa(b["F5"])
    b["lado5"] = np.sign(b["F5"]).astype(int)
    fut = b.set_index("fecha").sort_index()
    for h in (15, 60):
        cc = fut["c"].reindex(b["fecha"] + pd.Timedelta(minutes=h))
        cc.index = b.index
        dia = fut["dia"].reindex(b["fecha"] + pd.Timedelta(minutes=h))
        dia.index = b.index
        b[f"ret_{h}"] = (cc - b["c"]).where(dia == b["dia"])
    return b


def periodo(serie: str, dia: pd.Series) -> pd.Series:
    if serie == "WINFUT":
        return pd.Series(np.where(dia <= CORTE, "descoberta", "hold1"), index=dia.index)
    if serie == "WINM26":
        return pd.Series(np.where(dia <= base.CORTE_2026, "hold2", "fora"), index=dia.index)
    if serie == "WINQ26":
        return pd.Series(np.where(dia > base.CORTE_2026, "hold2", "fora"), index=dia.index)
    return pd.Series("wdo", index=dia.index)


def resumir(g: pd.DataFrame, lado: pd.Series) -> dict:
    r = (g["ret_60"] * lado).dropna()
    t = base.t_cluster((g["ret_60"] * lado).groupby(g["dia"]).sum())
    return {"n": int(r.shape[0]), "ret": float(r.mean()) if len(r) else np.nan, "t": t, "p": float((r > 0).mean()) if len(r) else np.nan}


def main() -> None:
    linhas = []
    for serie in ("WINFUT", "WINM26", "WINQ26", "WDOFUT"):
        d = montar(serie)
        d["per"] = periodo(serie, d["dia"])
        d = d[d["per"] != "fora"]
        for per, g in d.groupby("per"):
            cor5 = g["fx5"] > 0
            mesmo = cor5 & (g["fx15"] > 0) & (g["lado5"] == g["lado15"])
            oposto = cor5 & (g["fx15"] > 0) & (g["lado5"] == -g["lado15"])
            grupos = {
                "5 fraco, 15 branco": g[cor5 & (g["fx5"] == 1) & (g["fx15"] == 0)],
                "5 forte, 15 branco": g[cor5 & (g["fx5"] == 2) & (g["fx15"] == 0)],
                "5 fraco × 15 fraco": g[mesmo & (g["fx5"] == 1) & (g["fx15"] == 1)],
                "5 fraco × 15 forte": g[mesmo & (g["fx5"] == 1) & (g["fx15"] == 2)],
                "5 forte × 15 fraco": g[mesmo & (g["fx5"] == 2) & (g["fx15"] == 1)],
                "5 forte × 15 forte": g[mesmo & (g["fx5"] == 2) & (g["fx15"] == 2)],
                "5 colorido × 15 oposto": g[oposto],
            }
            for nome, gg in grupos.items():
                if len(gg) < 5:
                    continue
                linhas.append({"serie": serie, "per": per, "celula": nome, **resumir(gg, gg["lado5"])})
        print(serie, "ok", flush=True)
    res = pd.DataFrame(linhas)
    res.to_csv(PASTA / "ANALISE_003_fraco_forte.csv", index=False, sep=";", decimal=",", float_format="%.4f")

    def fmt(x, c=1):
        return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    ordem = ["5 fraco, 15 branco", "5 forte, 15 branco", "5 fraco × 15 fraco", "5 fraco × 15 forte", "5 forte × 15 fraco", "5 forte × 15 forte", "5 colorido × 15 oposto"]
    md = ["# ANALISE_003 — Lado pela tabela fraco/forte (5 min × 15 min)\n",
          "> Gerado por `codigo/analise_003.py`. Faixas e critério em `HIPOTESES.md` (CF-H10, CF-H11), congelados antes de rodar.\n",
          "Fraco = 70 ≤ |F| < 85. Forte = |F| ≥ 85. Lado = sinal de F. O número é o retorno de 60 min a favor desse lado, em pontos. "
          "`p` é a fração de eventos em que o lado acertou. Descoberta = WIN até 2025-06-30. Hold-out 1 = WIN de 2025-07 a 2025-12. 2026 = contratos M26 e Q26.\n",
          "No guia operacional, fraco se chama \"forte\" (F 70–85) e forte se chama \"exaustão\" (F ≥ 85). Os cortes são os mesmos.\n"]
    head = "| combinação | descoberta | hold-out 1 | 2026 | WDO |"
    md += [head, "|" + "|".join("---" for _ in range(5)) + "|"]

    def cel(nome, per, serie):
        x = res[(res["celula"] == nome) & (res["per"] == per) & (res["serie"] == serie)] if serie else \
            res[(res["celula"] == nome) & (res["per"] == per) & res["serie"].isin(["WINM26", "WINQ26"])]
        if serie is None and len(x):
            return f"{fmt(np.average(x['ret'], weights=x['n']), 0)} pts (n={int(x['n'].sum())})"
        if not len(x):
            return "—"
        return f"{fmt(x.iloc[0]['ret'], 0)} pts · t={fmt(x.iloc[0]['t'], 1)} · p={fmt(100 * x.iloc[0]['p'], 0)}% · n={int(x.iloc[0]['n'])}"

    for nome in ordem:
        md.append("| " + " | ".join([nome, cel(nome, "descoberta", "WINFUT"), cel(nome, "hold1", "WINFUT"), cel(nome, "hold2", None), cel(nome, "wdo", "WDOFUT")]) + " |")

    passa = []
    for nome in [f"5 {a} × 15 {b}" for a, b in CELULAS]:
        d = res[(res["celula"] == nome) & (res["per"] == "descoberta") & (res["serie"] == "WINFUT")]
        h = res[(res["celula"] == nome) & (res["per"] == "hold1") & (res["serie"] == "WINFUT")]
        if len(d) and len(h) and d.iloc[0]["n"] >= 80 and abs(d.iloc[0]["t"]) >= 3 and np.sign(h.iloc[0]["ret"]) == np.sign(d.iloc[0]["ret"]) and abs(h.iloc[0]["t"]) >= 2:
            passa.append(nome)
    fraco = res[(res["celula"] == "5 fraco, 15 branco") & (res["serie"] == "WINFUT")]
    forte = res[(res["celula"] == "5 forte, 15 branco") & (res["serie"] == "WINFUT")]

    def sinal_ok(df, per, positivo):
        x = df[df["per"] == per]
        if not len(x) or x.iloc[0]["n"] < 80:
            return False
        return (x.iloc[0]["ret"] > 0) == positivo and abs(x.iloc[0]["t"]) >= (3 if per == "descoberta" else 2)

    h11 = sinal_ok(fraco, "descoberta", True) and sinal_ok(fraco, "hold1", True) and sinal_ok(forte, "descoberta", False) and sinal_ok(forte, "hold1", False)
    md.append(f"\n**CF-H10:** {', '.join(passa) if passa else 'nenhuma das 4 combinações do mesmo lado passa'}.\n")
    md.append(f"**CF-H11:** {'fraco continua e forte reverte, nos dois períodos' if h11 else 'a história fraco-continua / forte-reverte não se sustenta'}.\n")
    md.append("Quatro células foram testadas. Uma delas pode passar de |t| = 2 por acaso; por isso o critério exige o mesmo sinal no hold-out.\n")
    (PASTA / "ANALISE_003_fraco_forte.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("gravado", "passa", passa, "h11", h11)


if __name__ == "__main__":
    main()
