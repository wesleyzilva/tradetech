"""ANALISE_002 — M17: teste final em 2026 (ML-H08), um disparo, só nas células que passaram em 2018–2025.

Treina em WINFUT 2014–2025 e testa em WINM26 (até 2026-05-13) e WINQ26 (a partir de 2026-05-14). As células vêm de ANALISE_001:
lado = 60 min, h = 1, S2, árvores (única que cumpriu ML-H04); amplitude = os quatro modelos de S2 escolhidos pela regra de ML-H07.

Uso: python motores/M17_aprendizado_walkforward/codigo/analise_002.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ml_motor as m  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402

PASTA = m.RAIZ / "motores" / "M17_aprendizado_walkforward" / "analises"
CELULA_LADO = (60, 1, "S2", "hgb")
CELULAS_VOL = [(30, 1, "hgb"), (30, 2, "linear"), (60, 1, "linear"), (60, 2, "linear")]
Z_2026 = 1.65


def f(v, d=3):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}".replace(".", ",")


def tabela(tf: int, liquido: bool) -> pd.DataFrame:
    """Treino WINFUT 2014–2025 e teste 2026. ``liquido=False`` é o desenho congelado (cada contrato com a sua história inteira);
    ``liquido=True`` costura WINFUT + WINM26 (até 2026-05-13) + WINQ26 (depois) **só com pregões líquidos**, como a série contínua do Profit."""
    if not liquido:
        win = m.construir("WINFUT", tf)
        da = carregar_serie("WINM26", f"{tf}min", liquido=False)
        db = carregar_serie("WINQ26", f"{tf}min", liquido=False)
        a = m.construir("WINM26", tf, ate="2026-05-13 23:59", d=da)
        b = m.construir("WINQ26", tf, desde="2026-05-14", d=db)
        return pd.concat([win, a, b], ignore_index=True)
    w = carregar_serie("WINFUT", f"{tf}min")
    a = carregar_serie("WINM26", f"{tf}min")
    b = carregar_serie("WINQ26", f"{tf}min")
    d = pd.concat([w, a[a["dt"] <= "2026-05-13 23:59"], b[b["dt"] >= "2026-05-14"]], ignore_index=True).sort_values("dt").reset_index(drop=True)
    return m.construir("costurada", tf, d=d)


def rodar(liquido: bool) -> tuple[list, dict]:
    linhas_vol, lado = [], None
    for tf in (30, 60):
        x = tabela(tf, liquido)
        for (t, hh, tipo) in CELULAS_VOL:
            if t != tf:
                continue
            o = m.walk_forward(x, m.colunas("S2"), "vol", hh, tipo, anos=[2026])
            b1 = m.har(x, hh, anos=[2026])
            g = m.ganho_perda(o, b1)
            cobre = float((o["y"] <= o["p"] + o["res_tr"]).mean())
            cv = lambda s: float(s.std() / s.mean())
            linhas_vol.append({"tf": tf, "h": hh, "tipo": tipo, "n": len(o), "dias": o["dia"].nunique(), "skill_b1": g["skill"], "t": g["t_dia"], "cobertura": cobre,
                               "cv_prev": cv(np.exp(o["y"] - o["p"])), "cv_atr": cv(np.exp(o["y"]) * o["c"] / o["atr_px"])})
        if tf == CELULA_LADO[0]:
            o = m.walk_forward(x, m.colunas("S2"), "dir", CELULA_LADO[1], CELULA_LADO[3], anos=[2026])
            a, sd = m.auc_boot(o)
            lado = {"n": len(o), "dias": o["dia"].nunique(), "auc": a, "sd": sd, "z": (a - 0.5) / sd, "necessario": 0.5 + Z_2026 * sd, **m.economico(o)}
    return linhas_vol, lado


def bloco(titulo: str, linhas_vol: list, lado: dict) -> list[str]:
    md = [f"## {titulo}\n", "### Lado (60 min, h = 1, S2, árvores)\n",
          f"- Observações: {lado['n']} em {lado['dias']} pregões.",
          f"- AUC = **{f(lado['auc'], 4)}**, desvio bootstrap {f(lado['sd'], 4)}, `z` = **{f(lado['z'], 2)}** (critério `z ≥ {Z_2026}`, ou seja AUC ≥ {f(lado['necessario'], 4)}; em 2018–2025 foi 0,5208).",
          f"- Esperança bruta {f(lado['bruto_pb'], 2)} pb e líquida {f(lado['liq_pb'], 2)} pb por trade (custo 0,4 pb); t por pregão {f(lado['t_dia'], 2)}.\n",
          "### Amplitude (modelos de S2 escolhidos pela regra de ML-H07)\n",
          "| TF | h | modelo | n | pregões | ganho sobre B1 | t | cobertura do quantil 80% | CV range/previsto | CV range/ATR |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in linhas_vol:
        md.append(f"| {r['tf']} | {r['h']} | {r['tipo']} | {r['n']} | {r['dias']} | {f(r['skill_b1'] * 100, 2)} % | {f(r['t'], 1)} | {f(r['cobertura'] * 100, 1)} % | {f(r['cv_prev'], 3)} | {f(r['cv_atr'], 3)} |")
    return md + [""]


def main() -> None:
    md = ["# M17 — ANALISE_002: teste final em 2026 (ML-H08)\n",
          "Treino WINFUT 2014–2025, sem ajuste. Dois desenhos, porque o primeiro revelou um problema de dados que o protocolo não previa:\n",
          "1. **Como congelado:** WINM26 até 2026-05-13 e WINQ26 depois, cada contrato com toda a sua história.",
          "2. **Só pregões líquidos, série costurada:** contratos fora do vencimento líquido quase não negociam (WINM26 em jan–mar: 68 a 17 mil contratos por dia; em abril, 9 milhões; WINQ26 até maio: no máximo 17 mil, em junho 7,7 milhões). "
          "O corte é Quantidade diária ≥ 1 milhão, definido pelo salto nos dados, antes de ver o resultado do desenho 2. O desenho 1 já tinha sido rodado e visto.\n"]
    for liquido, titulo in ((False, "Desenho 1 — como congelado"), (True, "Desenho 2 — só pregões líquidos (valendo)")):
        lv, lado = rodar(liquido)
        md += bloco(titulo, lv, lado)
    (PASTA / "ANALISE_002_2026.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
