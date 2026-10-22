"""ANALISE_001 — M19: estrutura diária e semanal (DD-H01 a DD-H04), 10 testes declarados.

Uso: python motores/M19_estrutura_diaria/codigo/analise_001.py   (poucos segundos)
Com um WINFUT que inclua 2026, os anos novos aparecem como colunas e não entram nos vereditos.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_motor as dm  # noqa: E402

im = dm.im
PASTA = dm.RAIZ / "motores" / "M19_estrutura_diaria" / "analises"


def f(v, d=2):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}".replace(".", ",")


def medir(ativo: str) -> dict:
    cel, ano_d = dm.celulas(ativo)
    res = {}
    for nome, (tipo, custo, df) in cel.items():
        ano = pd.Series(df.index.year, index=df.index)
        res[nome] = {"tipo": tipo, "custo": custo, "desc": im.estatisticas(tipo, df, ano, *im.DISC), "hold": im.estatisticas(tipo, df, ano, *im.HOLD),
                     "todo": im.estatisticas(tipo, df, ano, im.DISC[0], im.HOLD[1]), "anos": im.por_ano(tipo, df, ano)}
    return res


def passa(w: dict, d: dict) -> dict:
    s = np.sign(w["desc"]["media"])
    anos = [v for a, v in w["anos"].items() if im.DISC[0] <= a <= im.HOLD[1] and not np.isnan(v)]
    mesmos = int(sum(np.sign(v) == s for v in anos))
    cond = {
        "t_desc": abs(w["desc"]["t"]) >= im.LIM_DESC,
        "hold": np.sign(w["hold"]["media"]) == s and abs(w["hold"]["t"]) >= im.LIM_HOLD,
        "wdo": np.sign(d["todo"]["media"]) == s,
        "anos": mesmos >= im.ANOS_MIN_MESMO_SINAL,
    }
    if w["custo"]:
        cond["liquido"] = s * w["desc"]["media"] > im.CUSTO_PB and s * w["hold"]["media"] > im.CUSTO_PB
    return {"passa": all(cond.values()), "mesmos": mesmos, "n_anos": len(anos), "margem": s * w["todo"]["media"] / im.CUSTO_PB if w["custo"] else np.nan}


def main() -> None:
    PASTA.mkdir(exist_ok=True)
    rw, rd = medir("WINFUT"), medir("WDOFUT")
    linhas = []
    for nome in rw:
        p = passa(rw[nome], rd[nome])
        linhas.append({"celula": nome, "familia": nome[:6], **{f"{k}_{c}": rw[nome][k][c] for k in ("desc", "hold", "todo") for c in ("media", "t", "acerto", "n")},
                       "wdo_media": rd[nome]["todo"]["media"], "wdo_t": rd[nome]["todo"]["t"], "anos_mesmo_sinal": p["mesmos"], "n_anos": p["n_anos"], "margem": p["margem"], "passa": p["passa"]})
    t = pd.DataFrame(linhas)
    t.to_csv(PASTA / "ANALISE_001_celulas.csv", index=False, sep=";", decimal=",")
    anos = sorted({a for r in rw.values() for a in r["anos"]})
    pd.DataFrame({n: r["anos"] for n, r in rw.items()}).T[anos].to_csv(PASTA / "ANALISE_001_por_ano.csv", sep=";", decimal=",")
    vered = {}
    for fam in ("DD-H01", "DD-H02", "DD-H03", "DD-H04"):
        g = t[t["familia"] == fam]
        forte = g[g["desc_t"].abs() >= im.LIM_DESC]
        if g["passa"].any():
            vered[fam] = "CONFIRMADA"
        elif forte.empty or (np.sign(forte["desc_media"]) != np.sign(forte["hold_media"])).all():
            vered[fam] = "REFUTADA"
        else:
            vered[fam] = "INCONCLUSIVA"
    md = ["# M19 — ANALISE_001: estrutura diária e semanal\n",
          "Gerado por `codigo/analise_001.py`. Protocolo congelado em [`METODO.md`](../METODO.md) e [`HIPOTESES.md`](../HIPOTESES.md) antes de rodar. "
          "WINFUT D1 e W1, 2014–2025; replicação em WDOFUT. Descoberta 2014–2019, hold-out 2020–2025. Poder baixo (≈ 1.500 dias e ≈ 310 semanas por período): nulo = \"não detectável\".\n",
          "## 1. Resumo (calculado)\n",
          f"- Células com `|t| ≥ 3` na descoberta: **{int((t['desc_t'].abs() >= 3).sum())}** de 10; passam o critério inteiro: **{int(t['passa'].sum())}**.",
          f"- Maior `|t|` na descoberta: {f(t['desc_t'].abs().max())}; no hold-out: {f(t['hold_t'].abs().max())}.",
          "- Vereditos: " + "; ".join(f"{k} **{v}**" for k, v in vered.items()) + ".\n",
          "## 2. Células\n",
          "Média: excedente em pb por trade (DD-H01, DD-H04), desvio da razão de amplitude (DD-H02) ou diferença semana − demais (DD-H03: razão de amplitude e pb).\n",
          "| célula | desc: média | t | acerto | n | hold: média | t | acerto | WDO: média | t | anos | margem | passa |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in t.reindex(t["desc_t"].abs().sort_values(ascending=False).index).iterrows():
        md.append(f"| {r.celula} | {f(r.desc_media, 3)} | {f(r.desc_t)} | {f(r.desc_acerto * 100, 1)} % | {int(r.desc_n)} | {f(r.hold_media, 3)} | {f(r.hold_t)} | {f(r.hold_acerto * 100, 1)} % | {f(r.wdo_media, 3)} | {f(r.wdo_t)} | {r.anos_mesmo_sinal}/{r.n_anos} | {f(r.margem, 1)} | {'sim' if r.passa else 'não'} |")
    md += ["", "## 3. Por ano (média da célula)\n", "| célula | " + " | ".join(str(a) for a in anos) + " |", "|---|" + "---|" * len(anos)]
    for n in t.reindex(t["desc_t"].abs().sort_values(ascending=False).index)["celula"]:
        md.append(f"| {n} | " + " | ".join(f(rw[n]["anos"].get(a, np.nan), 2) for a in anos) + " |")
    (PASTA / "ANALISE_001_estrutura_diaria.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
