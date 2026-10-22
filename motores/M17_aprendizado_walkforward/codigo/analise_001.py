"""ANALISE_001 — M17: amplitude e lado com walk-forward 2018–2025 (WIN) e replicação no WDO.

Aplica o protocolo congelado em ``METODO.md`` e ``HIPOTESES.md`` (ML-H01 a ML-H07). O teste final de 2026 (ML-H08) fica em
``analise_002.py`` e só roda para o que passar aqui.

Uso: python motores/M17_aprendizado_walkforward/codigo/analise_001.py   (cerca de 10 a 15 min)
"""

from __future__ import annotations

import pickle
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ml_motor as m  # noqa: E402

PASTA = m.RAIZ / "motores" / "M17_aprendizado_walkforward" / "analises"
ATIVOS = {"WINFUT": "WDOFUT", "WDOFUT": "WINFUT"}
TFS = (30, 60)
TIPOS = ("linear", "hgb")
N_PLACEBO = 10
Z_LADO = 3.0


def dados(ativo: str, tf: int) -> pd.DataFrame:
    return m.construir(ativo, tf, m.cruzamento(ATIVOS[ativo], tf))


def rodar_ativo(ativo: str, placebos: bool) -> dict:
    res = {"vol": {}, "dir": {}, "har": {}, "plac": []}
    for tf in TFS:
        x = dados(ativo, tf)
        for h in m.HORIZONTES:
            res["har"][(tf, h)] = m.har(x, h)
            for conj, tipo in product(m.CONJUNTOS, TIPOS):
                cols = m.colunas(conj)
                res["vol"][(tf, h, conj, tipo)] = m.walk_forward(x, cols, "vol", h, tipo)
                res["dir"][(tf, h, conj, tipo)] = m.walk_forward(x, cols, "dir", h, tipo)
        if placebos:
            for k in range(N_PLACEBO):
                zs = []
                for h in m.HORIZONTES:
                    x[f"y_plac{h}"] = m.embaralhar_rotulo(x, h, 100 * k + h)
                    for conj, tipo in product(m.CONJUNTOS, TIPOS):
                        o = m.walk_forward(x, m.colunas(conj), "dir", h, tipo, rotulo=f"y_plac{h}")
                        a, sd = m.auc_boot(o, reps=150, seed=k)
                        zs.append((a - 0.5) / sd)
                res["plac"].append({"tf": tf, "rep": k, "z_max": float(np.max(zs)), "z_min": float(np.min(zs))})
                print(f"  {ativo} {tf}min placebo {k + 1}/{N_PLACEBO}: z_max={np.max(zs):.2f}", flush=True)
    return res


def tabela_lado(res: dict) -> pd.DataFrame:
    linhas = []
    for (tf, h, conj, tipo), o in res["dir"].items():
        a, sd = m.auc_boot(o)
        eco = m.economico(o)
        por_ano = m.auc_por_ano(o)
        linhas.append({
            "tf": tf, "h": h, "conj": conj, "tipo": tipo, "auc": a, "sd": sd, "z": (a - 0.5) / sd,
            "anos_acima": int(sum(v > 0.5 for v in por_ano.values())), "anos": len(por_ano),
            "auc_desc": m.auc(o[o["ano"] <= 2021]["y"].to_numpy(), o[o["ano"] <= 2021]["p"].to_numpy()),
            "auc_conf": m.auc(o[o["ano"] >= 2022]["y"].to_numpy(), o[o["ano"] >= 2022]["p"].to_numpy()),
            "liq_pb": eco["liq_pb"], "bruto_pb": eco["bruto_pb"], "t_dia": eco["t_dia"], "n": eco["n"],
        })
    return pd.DataFrame(linhas)


def tabela_vol(res: dict) -> pd.DataFrame:
    linhas = []
    for (tf, h, conj, tipo), o in res["vol"].items():
        b1 = res["har"][(tf, h)]
        g = m.ganho_perda(o, b1)
        base = m.ganho_perda(b1, b1.assign(p=b1["B0"]))
        linhas.append({"tf": tf, "h": h, "conj": conj, "tipo": tipo, "skill_b1": g["skill"], "t_b1": g["t_dia"], "anos_pos": g["anos_pos"], "anos": g["anos"],
                       "skill_b0": 1 - ((o["y"] - o["p"]) ** 2).sum() / ((o["y"] - o["B0"]) ** 2).sum(), "skill_har_b0": base["skill"]})
    return pd.DataFrame(linhas)


def diferencas(res: dict) -> pd.DataFrame:
    linhas = []
    for tf, h, tipo in product(TFS, m.HORIZONTES, TIPOS):
        for novo in ("S3", "S4"):
            ov, ob = res["vol"][(tf, h, novo, tipo)], res["vol"][(tf, h, "S2", tipo)]
            gv = m.ganho_perda(ov, ob)
            od, obd = res["dir"][(tf, h, novo, tipo)], res["dir"][(tf, h, "S2", tipo)]
            da, dsd = m.auc_diff_boot(od, obd)
            linhas.append({"tf": tf, "h": h, "tipo": tipo, "novo": novo, "vol_skill": gv["skill"], "vol_t": gv["t_dia"], "vol_anos": gv["anos_pos"],
                           "dir_dauc": da, "dir_z": da / dsd})
    return pd.DataFrame(linhas)


def calibracao(res: dict) -> pd.DataFrame:
    linhas = []
    for tf, h in product(TFS, m.HORIZONTES):
        cand = {tipo: res["vol"][(tf, h, "S2", tipo)] for tipo in TIPOS}
        desc = {t: ((o[o["ano"] <= 2021]["y"] - o[o["ano"] <= 2021]["p"]) ** 2).mean() for t, o in cand.items()}
        tipo = min(desc, key=desc.get)
        o = cand[tipo].copy()
        cobre = o["y"] <= o["p"] + o["res_tr"]
        por_ano = cobre.groupby(o["ano"]).mean()
        raz_p = np.exp(o["y"] - o["p"])
        raz_atr = np.exp(o["y"]) * o["c"] / o["atr_px"]
        cv = lambda s: float(s.std() / s.mean())
        linhas.append({"tf": tf, "h": h, "tipo": tipo, "cobertura": float(cobre.mean()), "min_ano": float(por_ano.min()), "max_ano": float(por_ano.max()),
                       "cv_prev": cv(raz_p), "cv_atr": cv(raz_atr), "reducao_cv": 1 - cv(raz_p) / cv(raz_atr)})
    return pd.DataFrame(linhas)


def f(v, d=3):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}".replace(".", ",")


def md_lado(t: pd.DataFrame, placebo_max: float | None) -> list[str]:
    out = ["| TF | h | conj | modelo | AUC | z | anos > 0,5 | AUC 18–21 | AUC 22–25 | líq. pb | t dia |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in t.sort_values("z", ascending=False).iterrows():
        out.append(f"| {r.tf} | {r.h} | {r.conj} | {r.tipo} | {f(r.auc, 4)} | {f(r.z, 2)} | {r.anos_acima}/{r.anos} | {f(r.auc_desc, 4)} | {f(r.auc_conf, 4)} | {f(r.liq_pb, 2)} | {f(r.t_dia, 2)} |")
    return out


def veredito_lado(win: pd.DataFrame, wdo: pd.DataFrame, placebo_max: float, conj: tuple[str, ...]) -> tuple[pd.DataFrame, list]:
    """Células que cumprem o critério de ML-H04 para os conjuntos dados."""
    w = win[win["conj"].isin(conj)]
    ok = []
    for _, r in w.iterrows():
        rr = wdo[(wdo["tf"] == r.tf) & (wdo["h"] == r.h) & (wdo["conj"] == r.conj) & (wdo["tipo"] == r.tipo)].iloc[0]
        if r.z >= Z_LADO and r.anos_acima >= 6 and r.liq_pb > 0 and r.t_dia >= 2 and r.z > placebo_max and rr.auc > 0.5:
            ok.append((r.tf, r.h, r.conj, r.tipo))
    return w, ok


def escrever(win: dict, wdo: dict, tl_w, tl_d, tv_w, tv_d, df_w, df_d, cal_w, cal_d) -> None:
    pmax = max(p["z_max"] for p in win["plac"])
    pdist = pd.DataFrame(win["plac"])
    md = ["# M17 — ANALISE_001: amplitude e lado com walk-forward\n",
          "Gerado por `codigo/analise_001.py`. Protocolo congelado em [`METODO.md`](../METODO.md) e [`HIPOTESES.md`](../HIPOTESES.md) antes de rodar. "
          "Teste fora da amostra em 8 anos (2018–2025), treino expansivo, estatística por pregão.\n"]

    sec = []

    sec += ["## 2. Lado (ML-H04 a ML-H06)\n",
            f"Limiar `z ≥ {Z_LADO}`. **Placebo** (rótulo embaralhado entre pregões do mesmo ano e slot, 10 repetições por TF): maior `z` observado = **{f(pmax, 2)}**; mediana dos `z_max` = {f(pdist['z_max'].median(), 2)}. "
            "Cada repetição roda as 12 células de um TF (2 horizontes × 3 conjuntos × 2 modelos) sobre ruído puro; esse é o `z` que o acaso entrega.\n"]
    for nome, t in (("WIN (decide)", tl_w), ("WDO (replica)", tl_d)):
        sec += [f"### {nome}\n"] + md_lado(t, pmax) + [""]
    h4, ok4 = veredito_lado(tl_w, tl_d, pmax, ("S2",))
    h5, ok5 = veredito_lado(tl_w, tl_d, pmax, ("S3",))
    h6, ok6 = veredito_lado(tl_w, tl_d, pmax, ("S4",))
    sec += [f"Células de S2 que cumprem todo o critério de ML-H04: **{len(ok4)}** {ok4 if ok4 else ''}. S3: **{len(ok5)}** {ok5 if ok5 else ''}. S4: **{len(ok6)}** {ok6 if ok6 else ''}.\n"]

    sec += ["## 3. Amplitude (ML-H01 a ML-H03)\n",
            "`skill_b1` = 1 − perda do modelo ÷ perda da linha de base HAR (B1), fora da amostra. Positivo = o modelo ganha de B1. `skill_b0` compara com a média do slot (B0).\n"]
    for nome, t in (("WIN (decide)", tv_w), ("WDO (replica)", tv_d)):
        sec += [f"### {nome}\n", "| TF | h | conj | modelo | skill vs B1 | t dia | anos > 0 | skill vs B0 |", "|---|---|---|---|---|---|---|---|"]
        for _, r in t.sort_values(["tf", "h", "conj", "tipo"]).iterrows():
            sec.append(f"| {r.tf} | {r.h} | {r.conj} | {r.tipo} | {f(r.skill_b1 * 100, 2)} % | {f(r.t_b1, 1)} | {r.anos_pos}/{r.anos} | {f(r.skill_b0 * 100, 1)} % |")
        sec.append("")
    sec += ["### O que S3 (WDO/WIN) e S4 (cor) acrescentam a S2\n", "Amplitude: ganho de perda sobre S2 (positivo = melhora). Lado: diferença de AUC e seu `z`.\n"]
    for nome, d in (("WIN", df_w), ("WDO", df_d)):
        sec += [f"**{nome}**\n", "| TF | h | modelo | acréscimo | amplitude: ganho | t dia | anos > 0 | lado: ΔAUC | z |", "|---|---|---|---|---|---|---|---|---|"]
        for _, r in d.iterrows():
            sec.append(f"| {r.tf} | {r.h} | {r.tipo} | {r.novo} | {f(r.vol_skill * 100, 3)} % | {f(r.vol_t, 1)} | {r.vol_anos}/8 | {f(r.dir_dauc, 4)} | {f(r.dir_z, 2)} |")
        sec.append("")

    sec += ["## 4. Dimensionar o stop pela amplitude prevista (ML-H07)\n",
            "Modelo de S2 com menor perda em 2018–2021 (regra congelada). Distância `D = exp(previsto + quantil 80% dos resíduos do treino)`. Cobertura = fração dos eventos em que o range da janela ficou dentro de `D` (alvo 80%). "
            "`CV` = desvio ÷ média de `range ÷ previsto` e de `range ÷ ATR`; menor é mais previsível.\n"]
    for nome, c in (("WIN", cal_w), ("WDO", cal_d)):
        sec += [f"**{nome}**\n", "| TF | h | modelo | cobertura | pior ano | melhor ano | CV range/previsto | CV range/ATR | redução do CV |", "|---|---|---|---|---|---|---|---|---|"]
        for _, r in c.iterrows():
            sec.append(f"| {r.tf} | {r.h} | {r.tipo} | {f(r.cobertura * 100, 1)} % | {f(r.min_ano * 100, 1)} % | {f(r.max_ano * 100, 1)} % | {f(r.cv_prev, 3)} | {f(r.cv_atr, 3)} | {f(r.reducao_cv * 100, 1)} % |")
        sec.append("")
    melhor = tl_w.sort_values("z", ascending=False).iloc[0]
    vb = tv_w[tv_w["conj"] == "S2"]
    resumo = ["## 1. Resumo (calculado)\n",
              f"- **Lado, WIN:** maior `z` = {f(melhor.z, 2)} (AUC {f(melhor.auc, 4)}, TF {melhor.tf}, h {melhor.h}, {melhor.conj}, {melhor.tipo}); maior `z` do placebo = {f(pmax, 2)}; células de S2/S3/S4 que cumprem o critério inteiro: {len(ok4)}/{len(ok5)}/{len(ok6)}.",
              f"- **Lado, WIN:** {int((tl_w['z'] >= Z_LADO).sum())} de {len(tl_w)} células passam `z ≥ {Z_LADO}`; AUC máxima = {f(tl_w['auc'].max(), 4)}; esperança líquida máxima = {f(tl_w['liq_pb'].max(), 2)} pb por trade.",
              f"- **Amplitude, WIN (S2 contra B1):** ganho de {f(vb['skill_b1'].min() * 100, 2)} % a {f(vb['skill_b1'].max() * 100, 2)} % da perda quadrática; contra a média do slot (B0): {f(vb['skill_b0'].min() * 100, 1)} % a {f(vb['skill_b0'].max() * 100, 1)} %.",
              ""]
    md += resumo + sec
    (PASTA / "ANALISE_001_walkforward.md").write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    PASTA.mkdir(exist_ok=True)
    win = rodar_ativo("WINFUT", placebos=True)
    wdo = rodar_ativo("WDOFUT", placebos=False)
    tl_w, tl_d = tabela_lado(win), tabela_lado(wdo)
    tv_w, tv_d = tabela_vol(win), tabela_vol(wdo)
    df_w, df_d = diferencas(win), diferencas(wdo)
    cal_w, cal_d = calibracao(win), calibracao(wdo)
    for nome, t in (("lado_win", tl_w), ("lado_wdo", tl_d), ("vol_win", tv_w), ("vol_wdo", tv_d), ("dif_win", df_w), ("dif_wdo", df_d), ("cal_win", cal_w), ("cal_wdo", cal_d)):
        t.to_csv(PASTA / f"ANALISE_001_{nome}.csv", index=False, sep=";", decimal=",")
    pd.DataFrame(win["plac"]).to_csv(PASTA / "ANALISE_001_placebo.csv", index=False, sep=";", decimal=",")
    with open(PASTA / "_cache_001.pkl", "wb") as fh:
        pickle.dump((tl_w, tl_d, tv_w, tv_d, df_w, df_d, cal_w, cal_d, win["plac"]), fh)
    escrever(win, wdo, tl_w, tl_d, tv_w, tv_d, df_w, df_d, cal_w, cal_d)
    print("ok")


if __name__ == "__main__":
    main()
