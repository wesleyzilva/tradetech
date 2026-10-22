"""Diagnóstico da ANALISE_001 (robustez, não altera vereditos): empates, variáveis univariadas e o comportamento da célula que passou.

Uso: python motores/M17_aprendizado_walkforward/codigo/diagnostico_001.py   (cerca de 1 min)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ml_motor as m  # noqa: E402

PASTA = m.RAIZ / "motores" / "M17_aprendizado_walkforward" / "analises"


def f(v, d=3):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}".replace(".", ",")


def main() -> None:
    md = ["# M17 — Diagnóstico da ANALISE_001\n",
          "Robustez do que apareceu na análise principal. Nada aqui muda um veredito; serve para entender de onde vem o sinal de lado e quão grande ele é.\n"]
    md += ["## 1. Empates no rótulo\n",
           "O rótulo `y_dir` trata `ret = 0` como queda. Sem esses casos (cerca de 0,4% a 1,3% das barras), com o mesmo modelo S2:\n",
           "| TF | h | modelo | AUC sem empates | z |", "|---|---|---|---|---|"]
    xs = {}
    for tf in (30, 60):
        x = m.construir("WINFUT", tf, m.cruzamento("WDOFUT", tf))
        xs[tf] = x
        for h in m.HORIZONTES:
            xe = x.copy()
            xe.loc[xe[f"ret{h}_pb"] == 0, f"y_dir{h}"] = np.nan
            for tipo in ("linear", "hgb"):
                o = m.walk_forward(xe, m.colunas("S2"), "dir", h, tipo)
                a, sd = m.auc_boot(o, 200)
                md.append(f"| {tf} | {h} | {tipo} | {f(a, 4)} | {f((a - 0.5) / sd, 2)} |")
    md += ["", "## 2. De onde vem o sinal (AUC univariada, descritiva, toda a amostra WIN, h = 1)\n",
           "AUC < 0,5 significa que valor alto da variável acompanha queda na barra seguinte (reversão); > 0,5, alta (continuação). Descritivo: não é teste fora da amostra.\n"]
    for tf in (30, 60):
        xv = m.com_alvo(xs[tf], 1)
        xv = xv[xv["valido_hora"] & xv["y_dir1"].notna()]
        r = {c: m.auc(xv["y_dir1"].to_numpy(), xv[c].fillna(xv[c].median()).to_numpy()) for c in m.colunas("S4") + m.GRUPOS["D"]}
        top = sorted(r.items(), key=lambda kv: -abs(kv[1] - 0.5))[:8]
        md += [f"**{tf} min:** " + "; ".join(f"`{k}` {f(v, 4)}" for k, v in top) + "\n"]
    md += ["## 3. A célula que passou (WIN, 60 min, h = 1, S2, árvores)\n"]
    o = m.walk_forward(xs[60], m.colunas("S2"), "dir", 1, "hgb")
    eco = m.economico(o)
    pa = m.auc_por_ano(o)
    md += ["| ano | AUC | trades | líq. pb por trade |", "|---|---|---|---|"]
    for ano, g in o.groupby("ano"):
        e = m.economico(g)
        md.append(f"| {ano} | {f(pa[ano], 4)} | {e['n']} | {f(e['liq_pb'], 2)} |")
    por_dia = o.groupby("dia").size().mean()
    pts = eco["liq_pb"] * 1e-4 * o["c"].mean()
    md += ["", f"Agregado: AUC {f(m.auc(o['y'].to_numpy(), o['p'].to_numpy()), 4)}; esperança líquida {f(eco['liq_pb'], 2)} pb por trade (bruta {f(eco['bruto_pb'], 2)}); t por pregão {f(eco['t_dia'], 2)}; {f(por_dia, 1)} trades por pregão.",
           f"Em pontos do WIN (preço médio do período {f(float(o['c'].mean()), 0)}): cerca de {f(pts, 1)} pts líquidos por trade, ou {f(pts * por_dia, 0)} pts por pregão por contrato, com custo de 5 pts e entrada exata na abertura da barra seguinte.",
           "Um slippage de 5 pts por lado (10 por trade) já zera isso: o sinal existe estatisticamente, mas a margem econômica é da ordem do custo.\n"]
    ate = o.assign(liq=np.where(o["p"] > 0.5, 1, -1) * o["ret"] - m.CUSTO_PB)
    md += ["### Sensibilidade ao custo (esperança por trade, pb)\n", "| custo por trade (pb) | esperança | t por pregão |", "|---|---|---|"]
    for c in (0.4, 0.8, 1.2, 1.6):
        oo = o.assign(liq=np.where(o["p"] > 0.5, 1, -1) * o["ret"] - c)
        mm, t = m.t_dia(oo, "liq")
        md.append(f"| {f(c, 1)} | {f(oo['liq'].mean(), 2)} | {f(t, 2)} |")
    (PASTA / "DIAGNOSTICO_001.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
