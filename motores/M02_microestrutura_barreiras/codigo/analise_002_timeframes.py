"""ANALISE_002 do motor M02 — risco/retorno por timeframe e utilidade da cor como alarme.

Perguntas:
  1. Existe timeframe/geometria (SL×SG) em que o sinal do M02 supere o acaso *com custo*?
  2. A barra brilhante (a "cor") funciona como alarme de volatilidade em todos os timeframes?

Regenera ``analises/ANALISE_002_timeframes_rr.md``.

Uso: python motores/M02_microestrutura_barreiras/codigo/analise_002_timeframes.py [--reps 50]

Grade pré-declarada (não escolher a melhor depois): TF ∈ {5,10,15,20,30,60} min; (SL, SG) em múltiplos do ATR ∈
{(0,5;2,5), (1;2), (1;3), (1;1)}; pisos de 35/120 pts desligados (não fazem sentido fora de 1 min); custo 5 pts por trade.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import mb_motor as mb  # noqa: E402
from analise_001 import fmt, so_sessoes_completas, tabela  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402

MD = RAIZ / "motores" / "M02_microestrutura_barreiras" / "analises" / "ANALISE_002_timeframes_rr.md"
TFS = (5, 10, 15, 20, 30, 60)
GEOMETRIAS = ((0.5, 2.5), (1.0, 2.0), (1.0, 3.0), (1.0, 1.0))
CUSTO = 5.0


def t_pregao(trades: pd.DataFrame) -> float:
    m = mb.metricas(trades)
    return m.get("t_pregao", np.nan)


def expansao_apos_brilhante(d: pd.DataFrame) -> dict:
    """Range da barra seguinte ÷ média do range no mesmo horário, após barra brilhante (>= 1,7 × ATR)."""
    d = d.copy()
    media_hora = d.groupby("hhmm")["rng"].transform("mean")
    razao_prox = (d["rng"].shift(-1) / media_hora.shift(-1))
    mesmo_dia = d["dia"].shift(-1) == d["dia"]
    evento = (d["est"] >= 3) & mesmo_dia
    base = razao_prox.where(mesmo_dia)
    x = razao_prox.where(evento)
    desvio = (x - base.mean()).groupby(d["dia"]).sum(min_count=1).fillna(0.0)
    t = desvio.mean() / (desvio.std(ddof=1) / np.sqrt(len(desvio))) if desvio.std(ddof=1) > 0 else np.nan
    return {"eventos": int(x.notna().sum()), "razão média": float(x.mean()), "controle": float(base.mean()), "t": float(t)}


def geometria_nula(serie: str, tf: int, sl: float, sg: float, reps: int = 20, prob: float = 0.15) -> dict:
    """Entrada aleatória (lado sorteado) com a geometria de saída: mede a esperança *da geometria* sozinha (perfil ideal)."""
    d0 = so_sessoes_completas(carregar_serie(serie, f"{tf}min"))
    p = mb.Params(sl_min=0.0, sg_min=0.0, gap_max_min=2 * tf, max_barras=max(4, int(round(100 / tf))), mult_sl=sl, mult_sg=sg,
                  protecao_na_barra_de_entrada=True)
    dd = mb.gerar_sinais(mb.preparar(d0, p), p)
    na = mb.janela_ativa(dd["hhmm"].to_numpy(), p)
    rows = []
    for r in range(reps):
        sorteio = np.random.default_rng(100 + r).random(len(dd)) < prob
        for lado in (1, -1):
            x = dd.copy()
            x["sinal"] = np.where(sorteio & na, lado, 0).astype(np.int8)
            x["ctx"] = 9
            t = mb.simular(x, p)
            rows.append(t[["dia", "pnl"]].assign(rep=r))
    t = pd.concat(rows)
    por_dia = t.groupby(["rep", "dia"])["pnl"].mean().groupby("dia").mean()
    corte = por_dia.index[len(por_dia) // 2]
    def tstat(x: pd.Series) -> float:
        return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 and x.std(ddof=1) > 0 else float("nan")
    anos = t.assign(ano=t["dia"].dt.year).groupby("ano")["pnl"].mean()
    return {"bruto": float(t["pnl"].mean()), "t": tstat(por_dia), "1ª metade": float(por_dia[por_dia.index < corte].mean()),
            "2ª metade": float(por_dia[por_dia.index >= corte].mean()), "anos positivos": f"{int((anos > 0).sum())}/{len(anos)}"}


def autocorrelacao(serie: str, tf: int) -> dict:
    """Autocorrelação de lag 1 do retorno intrabarra (C−O) ÷ ATR, dentro do pregão."""
    d0 = so_sessoes_completas(carregar_serie(serie, f"{tf}min"))
    p = mb.Params()
    d = mb.preparar(d0, p).dropna(subset=["atr"])
    r = (d["c"] - d["o"]) / d["atr"]
    mesmo = d["dia"] == d["dia"].shift(1)
    x, y = r[mesmo], r.shift(1)[mesmo]
    n = int(x.notna().sum())
    rho = float(np.corrcoef(x[x.notna() & y.notna()], y[x.notna() & y.notna()])[0, 1])
    return {"rho": rho, "t": rho * np.sqrt(n - 2) / np.sqrt(max(1 - rho**2, 1e-9)), "n": n}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=50)
    args = ap.parse_args()

    linhas_rr, linhas_exp, linhas_dados = [], [], []
    for tf in TFS:
        d0 = so_sessoes_completas(carregar_serie("WINFUT", f"{tf}min"))
        base_p = mb.Params(sl_min=0.0, sg_min=0.0, gap_max_min=2 * tf, max_barras=max(4, int(round(100 / tf))))
        dd0 = mb.gerar_sinais(mb.preparar(d0, base_p), base_p)
        linhas_dados.append({
            "TF": f"{tf} min", "barras": fmt(len(d0)), "pregões": fmt(d0["dt"].dt.normalize().nunique()),
            "início": d0["dt"].min().date(), "fim": d0["dt"].max().date(),
            "ATR mediano (pts)": fmt(dd0["atr"].median(), 0),
            "custo 5 pts ÷ ATR": f"{100 * CUSTO / dd0['atr'].median():.1f} %",
            "barras de tempo": base_p.max_barras,
        })
        e = expansao_apos_brilhante(dd0.dropna(subset=["atr"]))
        linhas_exp.append({"TF": f"{tf} min", "eventos": fmt(e["eventos"]), "range seguinte ÷ média da hora": fmt(e["razão média"]),
                           "controle": fmt(e["controle"]), "t (pregão)": fmt(e["t"])})
        for sl, sg in GEOMETRIAS:
            for perfil, prot in (("fiel", False), ("ideal", True)):
                p = mb.com(base_p, mult_sl=sl, mult_sg=sg, protecao_na_barra_de_entrada=prot, custo_pts=CUSTO)
                dd = mb.gerar_sinais(mb.preparar(d0, p), p)
                t = mb.simular(dd, p)
                m = mb.metricas(t)
                if m["n"] == 0:
                    continue
                reg = {"TF": f"{tf} min", "SL×ATR": fmt(sl, 1), "SG×ATR": fmt(sg, 1), "RR nominal": fmt(sg / sl, 1), "perfil": perfil,
                       "n": fmt(m["n"]), "trades/pregão": fmt(m["trades_por_pregao"], 1), "WR %": fmt(100 * m["win_rate"], 1),
                       "WR breakeven %": fmt(100 * m["wr_breakeven"], 1),
                       "bruto (pts)": fmt(m["pnl_medio"] + CUSTO), "líquido 5 pts": fmt(m["pnl_medio"]), "PF líq.": fmt(m["profit_factor"]),
                       "t (pregão)": fmt(m["t_pregao"])}
                if perfil == "ideal":
                    nulo = mb.aleatorio_mesma_saida(dd, p, n_rep=args.reps)
                    reg["percentil vs nulo"] = fmt(100 * float((nulo["pnl_medio"] < m["pnl_medio"]).mean()), 0)
                    reg["nulo líq. médio"] = fmt(nulo["pnl_medio"].mean())
                else:
                    reg["percentil vs nulo"] = "—"
                    reg["nulo líq. médio"] = "—"
                linhas_rr.append(reg)
        print(f"TF {tf} ok", flush=True)

    linhas_geo, linhas_ac = [], []
    for serie in ("WINFUT", "WDOFUT"):
        for tf in TFS:
            try:
                ac = autocorrelacao(serie, tf)
                linhas_ac.append({"série": serie, "TF": f"{tf} min", "ρ lag-1 (C−O ÷ ATR)": fmt(ac["rho"], 3), "t": fmt(ac["t"]), "n": fmt(ac["n"])})
                for sl, sg in ((0.5, 2.5), (1.0, 2.0)):
                    g = geometria_nula(serie, tf, sl, sg)
                    linhas_geo.append({"série": serie, "TF": f"{tf} min", "SL×ATR": fmt(sl, 1), "SG×ATR": fmt(sg, 1), "bruto (pts/trade)": fmt(g["bruto"]),
                                       "líquido 5 pts": fmt(g["bruto"] - CUSTO) if serie == "WINFUT" else "n/a (pontos de WDO)", "t (pregão)": fmt(g["t"]), "1ª metade": fmt(g["1ª metade"]),
                                       "2ª metade": fmt(g["2ª metade"]), "anos positivos": g["anos positivos"]})
            except Exception as exc:  # série sem esse timeframe
                print(f"{serie} {tf}min: {exc}", flush=True)
        print(f"{serie} geometria ok", flush=True)

    ideal = [l for l in linhas_rr if l["perfil"] == "ideal"]
    fiel = [l for l in linhas_rr if l["perfil"] == "fiel"]
    cols = ["TF", "SL×ATR", "SG×ATR", "RR nominal", "n", "trades/pregão", "WR %", "WR breakeven %", "bruto (pts)", "líquido 5 pts", "PF líq.", "t (pregão)", "percentil vs nulo", "nulo líq. médio"]

    md = ["# ANALISE_002 — Risco/retorno por timeframe e cor como alarme (M02)\n",
          "> Gerado por `motores/M02_microestrutura_barreiras/codigo/analise_002_timeframes.py`. Não editar à mão.\n",
          "## 1. Perguntas\n",
          "1. Em qual timeframe e com qual razão SL:SG o sinal do M02 supera o acaso **com custo**?\n"
          "2. A barra brilhante (a cor do robô) é um alarme de volatilidade em todos os timeframes?\n",
          "## 2. Dados e grade (pré-declarada)\n",
          "WINFUT contínuo, série padrão, pregões completos. Mesmos sinais do robô (3 contextos, mesmas janelas), pisos de 35/120 pts desligados (só fazem sentido em 1 min), "
          "tempo máximo ≈ 100 minutos em qualquer TF, custo de 5 pts/trade, entrada na abertura seguinte, stop primeiro. "
          "Grade: 6 TFs × 4 geometrias = 24 combinações — **nenhuma foi escolhida a posteriori**; com 24 testes, esperar ~1 combinação com |t| ≥ 2 por acaso.\n",
          tabela(linhas_dados, ["TF", "barras", "pregões", "início", "fim", "ATR mediano (pts)", "custo 5 pts ÷ ATR", "barras de tempo"]),
          "\nO custo fixo pesa 1/20 do ATR em 60 min mas mais de 1/5 em 5 min: **a escala favorece timeframes maiores por custo**, não por sinal.\n",
          "## 3. Risco/retorno × timeframe — perfil ideal (limite superior; ordens ativas desde a abertura)\n",
          tabela(ideal, cols),
          "\n`percentil vs nulo`: posição do resultado líquido do robô na distribuição de entradas aleatórias com a mesma saída e custo. ≥ 95 = sinal; ≤ 5 = pior que o acaso.\n",
          "## 4. Perfil fiel (barra de entrada sem proteção, como o NTSL v1)\n",
          tabela(fiel, ["TF", "SL×ATR", "SG×ATR", "RR nominal", "n", "WR %", "WR breakeven %", "bruto (pts)", "líquido 5 pts", "PF líq.", "t (pregão)"]),
          "\n## 5. Controle: a geometria de saída sozinha (entrada aleatória, perfil ideal)\n",
          "A coluna `nulo líq. médio` da seção 3 sugere que **a própria geometria (stop curto, alvo longo, ≤ ~100 min) tem esperança positiva em timeframes grandes**, "
          "independentemente do sinal. Esta seção isola esse efeito: entradas em barras sorteadas (15 % das barras de janela), lado sorteado, 20 repetições, "
          "t agregado por pregão, e replicação na série WDO (outro instrumento; o custo de 5 pts só vale para o WIN).\n",
          tabela(linhas_geo, ["série", "TF", "SL×ATR", "SG×ATR", "bruto (pts/trade)", "líquido 5 pts", "t (pregão)", "1ª metade", "2ª metade", "anos positivos"]),
          "\nExplicação candidata (hipótese MB-H13): retorno positivamente autocorrelacionado na escala do ATR — um stop curto corta a continuação adversa e deixa correr a favorável. "
          "Se for isso, aparece como ρ(lag 1) > 0:\n",
          tabela(linhas_ac, ["série", "TF", "ρ lag-1 (C−O ÷ ATR)", "t", "n"]),
          "\n## 6. A cor como alarme de volatilidade\n",
          "Evento: barra brilhante (range ≥ 1,7 × ATR20). Medida: range da barra seguinte ÷ média do range **no mesmo horário** (controle de sazonalidade intradiária). "
          "Razão > 1 = o alarme antecipa expansão. O `t` agrega por pregão a soma dos desvios em relação ao controle.\n",
          tabela(linhas_exp, ["TF", "eventos", "range seguinte ÷ média da hora", "controle", "t (pregão)"]),
          "\nComo o alarme descreve **tamanho** e não **direção**, ele serve para decidir *quando* ter alvo/stop mais largos ou ficar de fora, não para decidir lado.\n"]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"gravado {MD.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
