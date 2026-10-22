"""Motor M03 — confluência de cor (M01) em múltiplos timeframes.

Implementa exatamente as definições congeladas em ``METODO.md``. A cor vem de ``calcular`` do M01 (``est`` ∈ −2..2);
a execução reaproveita o simulador do M02 (``mb_motor``).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
for p in (RAIZ, RAIZ / "src", RAIZ / "motores" / "M02_microestrutura_barreiras" / "codigo"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import mb_motor as mb  # noqa: E402
from motores.M01_fma_forca.teses.cores.analise_candles import calcular  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402

JANELA_INI, JANELA_FIM = 915, 1610
CONJUNTOS = {
    5: [(15,), (30,), (60,), (15, 30), (15, 60), (30, 60), (15, 30, 60)],
    15: [(30,), (60,), (30, 60)],
    30: [(60,)],
}
NIVEIS = (1, 2)
GEOMETRIAS = ((0.5, 1.5), (1.0, 2.0), (1.0, 3.0))
LADOS = {"continuação": 1, "fade": -1}
HORIZONTES_MIN = (5, 15, 30, 60)
TEMPO_MAX_MIN = 60
CUSTO_WIN = 5.0
PROB_NULO = 0.03
REPS_NULO = 20


def sessoes_completas(d: pd.DataFrame, frac: float = 0.9) -> pd.DataFrame:
    dia = d["dt"].dt.normalize()
    n = d.groupby(dia).size()
    ok = n[n >= frac * n.quantile(0.95)].index
    return d[dia.isin(ok)].reset_index(drop=True)


def estados(serie: str, tf: int, completo: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devolve (candles do TF, tabela de estados com instante de fechamento)."""
    d = carregar_serie(serie, f"{tf}min")
    if completo:
        d = sessoes_completas(d)
    c = calcular(d[["dt", "o", "h", "l", "c", "v"]].copy())
    s = c[["dt", "est", "fam"]].copy()
    s["fecha"] = s["dt"] + pd.Timedelta(minutes=tf)
    return d, s


@dataclass
class Dataset:
    nome: str
    serie: str
    tf_base: int
    x0: pd.DataFrame  # candles da base com ATR/hhmm/dia (mb.preparar)
    est_base: pd.DataFrame
    est_sup: dict[int, pd.DataFrame]


def montar(serie: str, tf_base: int) -> Dataset:
    d_base, s_base = estados(serie, tf_base, completo=True)
    sup = {tf: estados(serie, tf, completo=False)[1] for tf in (15, 30, 60) if tf > tf_base}
    x0 = mb.preparar(d_base[["dt", "o", "h", "l", "c"]], mb.Params(gap_max_min=2 * tf_base))
    return Dataset(serie, serie, tf_base, x0, s_base, sup)


def _cond(fam_ref: pd.Series, est_ref: pd.Series, fam_b: pd.Series, nivel: int) -> pd.Series:
    return (fam_ref == fam_b) & (est_ref.abs() >= nivel)


def eventos(ds: Dataset, sup: tuple[int, ...], nivel: int, modo: str) -> pd.Series:
    """Série indexada por ``dt`` da barra base: +1/−1 no evento, 0 caso contrário."""
    b = ds.est_base.copy()
    b = b[(b["fam"] != 0) & (b["est"].abs() >= nivel)]
    h = b["dt"].dt.hour * 100 + b["dt"].dt.minute
    b = b[(h >= JANELA_INI) & (h <= JANELA_FIM)]
    ok = pd.Series(True, index=b.index)
    for tf in sup:
        s = ds.est_sup[tf]
        if modo == "A":
            m = s.set_index("fecha")
            fam = b["fecha"].map(m["fam"])
            est = b["fecha"].map(m["est"])
        else:
            ss = s[["fecha", "fam", "est"]].rename(columns={"fecha": "f_sup"}).assign(fecha=lambda t: t["f_sup"]).sort_values("fecha")
            bb = b[["fecha"]].reset_index().sort_values("fecha")
            mm = pd.merge_asof(bb, ss, on="fecha", direction="backward", tolerance=pd.Timedelta(minutes=tf)).set_index("index")
            mesmo = mm["f_sup"].notna() & (mm["f_sup"].dt.normalize() == mm["fecha"].dt.normalize())
            fam = mm["fam"].where(mesmo)
            est = mm["est"].where(mesmo)
        ok &= _cond(fam.reindex(b.index), est.reindex(b.index), b["fam"], nivel).fillna(False)
    ev = pd.Series(0, index=ds.x0["dt"], dtype="int8")
    sel = b[ok]
    ev.loc[sel["dt"].to_numpy()] = sel["fam"].to_numpy().astype("int8")
    return ev


def _params(tf_base: int, sl: float, sg: float, custo: float) -> mb.Params:
    return mb.Params(
        sl_min=0.0, sg_min=0.0, mult_sl=sl, mult_sg=sg, gap_max_min=2 * tf_base,
        max_barras=TEMPO_MAX_MIN // tf_base, protecao_na_barra_de_entrada=True, stop_a_mercado=True, custo_pts=custo,
    )


def simular_eventos(ds: Dataset, ev: pd.Series, lado: int, sl: float, sg: float, custo: float) -> pd.DataFrame:
    p = _params(ds.tf_base, sl, sg, custo)
    sinal = (ev.reindex(ds.x0["dt"]).to_numpy() * lado).astype(np.int8)
    x = ds.x0.assign(sinal=sinal, ctx=np.where(sinal != 0, 9, 0).astype(np.int8))
    t = mb.simular(x, p)
    if t.empty:
        return t
    return t[["dia", "lado", "pnl", "pnl_bruto", "motivo", "atr_sinal", "mfe", "mae"]]


def nulo(ds: Dataset, sl: float, sg: float, custo: float, reps: int = REPS_NULO, prob: float = PROB_NULO) -> pd.DataFrame:
    """Entradas aleatórias (lado sorteado) com a mesma saída; devolve todos os trades de todas as repetições."""
    p = _params(ds.tf_base, sl, sg, custo)
    hm = ds.x0["hhmm"].to_numpy()
    na = (hm >= JANELA_INI) & (hm <= JANELA_FIM)
    out = []
    for r in range(reps):
        g = np.random.default_rng(1000 + r)
        sorteio = g.random(len(ds.x0)) < prob
        lado = g.choice([-1, 1], size=len(ds.x0))
        sinal = np.where(sorteio & na, lado, 0).astype(np.int8)
        x = ds.x0.assign(sinal=sinal, ctx=np.where(sinal != 0, 9, 0).astype(np.int8))
        t = mb.simular(x, p)
        if not t.empty:
            out.append(t[["dia", "pnl"]].assign(rep=r))
    return pd.concat(out, ignore_index=True)


def tabela_eventos(ds: Dataset, ev: pd.Series) -> pd.DataFrame:
    """Uma linha por evento com expansão de range, retornos alinhados e MFE/MAE."""
    x = ds.x0
    tf = ds.tf_base
    lado = ev.reindex(x["dt"]).to_numpy()
    idx = np.flatnonzero(lado != 0)
    if len(idx) == 0:
        return pd.DataFrame()
    o_prox = x["o"].shift(-1)
    media_hora = x.groupby("hhmm")["rng"].transform("mean")
    razao = (x["rng"].shift(-1) / media_hora.shift(-1)).where(x["dia"].shift(-1) == x["dia"])
    nb = TEMPO_MAX_MIN // tf
    hi = x["h"].shift(-1)[::-1].rolling(nb, min_periods=nb).max()[::-1]
    lo = x["l"].shift(-1)[::-1].rolling(nb, min_periods=nb).min()[::-1]
    ok_dia = x["dia"].shift(-nb) == x["dia"]
    dados = {"dt": x["dt"].to_numpy()[idx], "dia": x["dia"].to_numpy()[idx], "lado": lado[idx].astype(int),
             "atr": x["atr"].to_numpy()[idx], "ratio": razao.to_numpy()[idx]}
    for m in HORIZONTES_MIN:
        h = m // tf
        if h < 1 or m % tf:
            continue
        fut = (x["c"].shift(-h) - o_prox).where(x["dia"].shift(-h) == x["dia"])
        dados[f"ret_{m}"] = (fut.to_numpy()[idx]) * lado[idx]
    up = (hi - o_prox).to_numpy()[idx]
    dn = (o_prox - lo).to_numpy()[idx]
    valido = ok_dia.to_numpy()[idx]
    s = lado[idx]
    dados["mfe"] = np.where(valido, np.where(s > 0, up, dn), np.nan)
    dados["mae"] = np.where(valido, np.where(s > 0, dn, up), np.nan)
    return pd.DataFrame(dados)


def t_cluster(por_dia: pd.Series) -> float:
    if len(por_dia) < 3 or por_dia.std(ddof=1) == 0:
        return float("nan")
    return float(por_dia.mean() / (por_dia.std(ddof=1) / np.sqrt(len(por_dia))))


def metricas_estrategia(trades: pd.DataFrame, dias: pd.DatetimeIndex, media_nulo: float) -> dict:
    if trades.empty:
        return {"n": 0}
    s = trades.groupby("dia")["pnl"].sum().reindex(dias, fill_value=0.0)
    n_d = trades.groupby("dia").size().reindex(dias, fill_value=0)
    pnl = trades["pnl"]
    ganhos, perdas = pnl[pnl > 0], pnl[pnl < 0]
    payoff = ganhos.mean() / abs(perdas.mean()) if len(ganhos) and len(perdas) else np.nan
    return {
        "n": int(len(pnl)), "por_pregao": float(len(pnl) / len(dias)), "wr": float((pnl > 0).mean()),
        "wr_be": float(1 / (1 + payoff)) if payoff == payoff else np.nan,
        "medio": float(pnl.mean()), "medio_R": float((pnl / trades["atr_sinal"]).mean()),
        "pf": float(ganhos.sum() / -perdas.sum()) if len(perdas) and perdas.sum() < 0 else np.nan,
        "t_dia": t_cluster(s), "t_nulo": t_cluster(s - media_nulo * n_d),
        "total": float(pnl.sum()),
    }


def grade_estrategias():
    for base, conjuntos in CONJUNTOS.items():
        for sup, nivel, lado, geom in product(conjuntos, NIVEIS, LADOS, GEOMETRIAS):
            yield base, sup, nivel, lado, geom
