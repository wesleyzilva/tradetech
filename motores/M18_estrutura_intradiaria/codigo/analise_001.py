"""ANALISE_001 — M18: estrutura intradiária (ID-H01 a ID-H05), 35 testes declarados.

Uso: python motores/M18_estrutura_intradiaria/codigo/analise_001.py   (cerca de 10 s)
Com um WINFUT que inclua 2026, os anos novos aparecem como colunas nas tabelas por ano e não entram nos vereditos.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import id_motor as m  # noqa: E402

PASTA = m.RAIZ / "motores" / "M18_estrutura_intradiaria" / "analises"


def f(v, d=2):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}".replace(".", ",")


def medir(serie: str) -> tuple[m.Dia, dict]:
    d = m.Dia(serie)
    cel = m.celulas(d)
    res = {}
    for nome, (tipo, df) in cel.items():
        res[nome] = {
            "tipo": tipo,
            "desc": m.estatisticas(tipo, df, d.ano, *m.DISC),
            "hold": m.estatisticas(tipo, df, d.ano, *m.HOLD),
            "todo": m.estatisticas(tipo, df, d.ano, m.DISC[0], m.HOLD[1]),
            "anos": m.por_ano(tipo, df, d.ano),
        }
    return d, res


def passa(win: dict, wdo: dict) -> dict:
    s = np.sign(win["desc"]["media"])
    anos = [v for a, v in win["anos"].items() if m.DISC[0] <= a <= m.HOLD[1] and not np.isnan(v)]
    mesmos = int(sum(np.sign(v) == s for v in anos))
    cond = {
        "t_desc": abs(win["desc"]["t"]) >= m.LIM_DESC,
        "hold": np.sign(win["hold"]["media"]) == s and abs(win["hold"]["t"]) >= m.LIM_HOLD,
        "wdo": np.sign(wdo["todo"]["media"]) == s,
        "liquido": s * win["desc"]["media"] > m.CUSTO_PB and s * win["hold"]["media"] > m.CUSTO_PB,
        "anos": mesmos >= m.ANOS_MIN_MESMO_SINAL,
    }
    return {"passa": all(cond.values()), "cond": cond, "anos_mesmo_sinal": mesmos, "n_anos": len(anos),
            "margem": s * win["todo"]["media"] / m.CUSTO_PB}


def main() -> None:
    PASTA.mkdir(exist_ok=True)
    dw, rw = medir("WINFUT")
    dd, rd = medir("WDOFUT")
    linhas = []
    for nome in rw:
        p = passa(rw[nome], rd[nome])
        linhas.append({"celula": nome, "familia": nome[:6], **{f"{k}_{c}": rw[nome][k][c] for k in ("desc", "hold", "todo") for c in ("media", "t", "acerto", "n")},
                       "wdo_media": rd[nome]["todo"]["media"], "wdo_t": rd[nome]["todo"]["t"], "anos_mesmo_sinal": p["anos_mesmo_sinal"], "n_anos": p["n_anos"],
                       "margem": p["margem"], "passa": p["passa"], **{f"c_{k}": v for k, v in p["cond"].items()}})
    t = pd.DataFrame(linhas)
    t.to_csv(PASTA / "ANALISE_001_celulas.csv", index=False, sep=";", decimal=",")
    anos = sorted({a for r in rw.values() for a in r["anos"]})
    pd.DataFrame({n: r["anos"] for n, r in rw.items()}).T[anos].to_csv(PASTA / "ANALISE_001_por_ano.csv", sep=";", decimal=",")

    vered = {}
    for fam in ("ID-H01", "ID-H02", "ID-H03", "ID-H04", "ID-H05"):
        g = t[t["familia"] == fam]
        if g["passa"].any():
            vered[fam] = "CONFIRMADA"
        elif (g["desc_t"].abs() >= m.LIM_DESC).any():
            vered[fam] = "REFUTADA" if (np.sign(g[g["desc_t"].abs() >= m.LIM_DESC]["desc_media"]) != np.sign(g[g["desc_t"].abs() >= m.LIM_DESC]["hold_media"])).all() else "INCONCLUSIVA"
        else:
            vered[fam] = "REFUTADA"

    md = ["# M18 — ANALISE_001: estrutura intradiária\n",
          "Gerado por `codigo/analise_001.py`. Protocolo congelado em [`METODO.md`](../METODO.md) e [`HIPOTESES.md`](../HIPOTESES.md) antes de rodar. "
          f"WINFUT 30 min, {len(dw.dias)} pregões completos (2014–2025); WDOFUT, {len(dd.dias)}. Descoberta 2014–2019, hold-out 2020–2025. Valores em pb do preço de entrada, líquidos de nada (o custo é 0,4 pb).\n",
          "## 1. Resumo (calculado)\n",
          f"- Células com `|t| ≥ 3` na descoberta: **{int((t['desc_t'].abs() >= 3).sum())}** de 35 (por acaso esperaria-se ~{35 * 0.0027:.1f}).",
          f"- Células que passam o critério inteiro: **{int(t['passa'].sum())}**.",
          f"- Maior `|t|` na descoberta: {f(t['desc_t'].abs().max())}; maior `|t|` no hold-out: {f(t['hold_t'].abs().max())}.",
          "- Vereditos: " + "; ".join(f"{k} **{v}**" for k, v in vered.items()) + ".\n",
          "## 2. Todas as células, por |t| na descoberta\n",
          "`média` = excedente por trade (pb); `acerto` = fração dos pregões a favor do lado; `anos` = anos (de 12) com o mesmo sinal da descoberta; `margem` = média 2014–2025 no sentido do sinal ÷ custo (0,4 pb).\n",
          "| célula | desc: média | t | acerto | hold: média | t | acerto | WDO: média | t | anos | margem | passa |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in t.reindex(t["desc_t"].abs().sort_values(ascending=False).index).iterrows():
        md.append(f"| {r.celula} | {f(r.desc_media)} | {f(r.desc_t)} | {f(r.desc_acerto * 100, 1)} % | {f(r.hold_media)} | {f(r.hold_t)} | {f(r.hold_acerto * 100, 1)} % | {f(r.wdo_media)} | {f(r.wdo_t)} | {r.anos_mesmo_sinal}/{r.n_anos} | {f(r.margem, 1)} | {'sim' if r.passa else 'não'} |")
    top = t.reindex(t["desc_t"].abs().sort_values(ascending=False).index).head(8)["celula"].tolist()
    md += ["", "## 3. Por ano (excedente médio em pb) das 8 células com maior |t| na descoberta\n",
           "| célula | " + " | ".join(str(a) for a in anos) + " |", "|---|" + "---|" * len(anos)]
    for n in top:
        md.append(f"| {n} | " + " | ".join(f(rw[n]["anos"].get(a, np.nan), 1) for a in anos) + " |")
    md += ["", "Anos de 2026 em diante (quando existirem no `WINFUT`) aparecem como colunas novas aqui e não entram nos vereditos.\n"]
    (PASTA / "ANALISE_001_estrutura_intradiaria.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:12]))
    print(vered)


if __name__ == "__main__":
    main()
