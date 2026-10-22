"""Motor M17 — aprendizado supervisionado com validação walk-forward.

Implementa as definições congeladas em ``METODO.md``: variáveis conhecidas no fechamento, rótulos de amplitude e de lado,
modelos com hiperparâmetros fixos, dobras anuais expansivas e estatística por pregão.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

RAIZ = Path(__file__).resolve().parents[3]
for p in (RAIZ, RAIZ / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from motores.M01_fma_forca.teses.cores.analise_candles import calcular  # noqa: E402
from tradetech.dados import carregar_serie, sessoes_liquidas  # noqa: E402

warnings.filterwarnings("ignore")

ANOS_TESTE = list(range(2018, 2026))
CUSTO_PB = 0.4
CORTE_RET = 6.0
HORIZONTES = (1, 2)
GRUPOS = {
    "A": ["ret1", "ret2", "ret4", "corpo", "rng_rel", "atr_ratio", "z20", "pos_dia", "ret_dia", "gap", "amp_ant"],
    "B": ["slot", "slot2", "dow"],
    "C": ["v_rel", "q_rel"],
    "V": ["lrng1", "lrng5", "lrng20", "B0"],
    "D": ["x_ret1", "x_ret2", "x_ret4", "x_ret_dia"],
    "E": ["F", "est", "z_cor"],
}
CONJUNTOS = {"S2": "ABCV", "S3": "ABCVD", "S4": "ABCVE"}
HAR = ["B0", "lrng1", "lrng5", "lrng20"]


def colunas(conjunto: str) -> list[str]:
    return [c for g in CONJUNTOS[conjunto] for c in GRUPOS[g]]


def _barras(d: pd.DataFrame, tf: int) -> pd.DataFrame:
    d = d.sort_values("dt").reset_index(drop=True).copy()
    d["dia"] = d["dt"].dt.normalize()
    d["rng"] = d["h"] - d["l"]
    d["atr"] = d["rng"].rolling(20).mean()
    d["slot"] = ((d["dt"].dt.hour * 60 + d["dt"].dt.minute - 9 * 60) // tf).astype(int)
    g = d.groupby("dia")
    d["abre_dia"] = g["o"].transform("first")
    d["max_dia"] = g["h"].cummax()
    d["min_dia"] = g["l"].cummin()
    return d


def _estrutura(d: pd.DataFrame) -> pd.DataFrame:
    a = d["atr"].replace(0, np.nan)
    x = pd.DataFrame({"dt": d["dt"]})
    for k in (1, 2, 4):
        x[f"ret{k}"] = ((d["c"] - d["c"].shift(k)) / a).clip(-CORTE_RET, CORTE_RET)
    x["corpo"] = (d["c"] - d["o"]) / a
    x["rng_rel"] = d["rng"] / a
    x["atr_ratio"] = d["rng"].rolling(5).mean() / d["rng"].rolling(60).mean()
    sma, dp = d["c"].rolling(20).mean(), d["c"].rolling(20).std(ddof=0)
    x["z20"] = (d["c"] - sma) / dp.replace(0, np.nan)
    amp = (d["max_dia"] - d["min_dia"]).replace(0, np.nan)
    x["pos_dia"] = ((d["c"] - d["min_dia"]) / amp).fillna(0.5)
    x["ret_dia"] = ((d["c"] - d["abre_dia"]) / a).clip(-CORTE_RET, CORTE_RET)
    fecha_ant = d.groupby("dia")["c"].last().shift(1)
    x["gap"] = ((d["abre_dia"] - d["dia"].map(fecha_ant)) / a).clip(-CORTE_RET, CORTE_RET)
    diario = d.groupby("dia").agg(h=("h", "max"), l=("l", "min"))
    rd = diario["h"] - diario["l"]
    amp_ant = rd.shift(1) / rd.shift(1).rolling(20).mean().shift(1)
    x["amp_ant"] = d["dia"].map(amp_ant)
    return x


def construir(serie: str, tf: int, cruz: pd.DataFrame | None = None, ate: str | None = None, desde: str | None = None, d: pd.DataFrame | None = None) -> pd.DataFrame:
    """Tabela de observações (uma por barra) com variáveis, rótulos e metadados. ``d`` substitui a leitura de ``serie``."""
    if d is None:
        d = carregar_serie(serie, f"{tf}min")
    d = _barras(d, tf)
    x = _estrutura(d)
    x["dow"] = d["dt"].dt.dayofweek
    x["slot"] = d["slot"]
    x["slot2"] = (d["slot"] - d["slot"].median()) ** 2
    for col, src in (("v_rel", "v"), ("q_rel", "q")):
        s = d[src].astype(float)
        media = s.groupby(d["slot"]).transform(lambda z: z.shift(1).rolling(20, min_periods=10).mean())
        x[col] = s / media.where(media > 0)
    lr = np.log((d["rng"] / d["c"]).where(d["rng"] > 0))
    x["lrng1"] = lr
    x["lrng5"] = lr.rolling(5).mean()
    x["lrng20"] = lr.rolling(20).mean()
    cor = calcular(d[["dt", "o", "h", "l", "c", "v"]].copy())[["dt", "F", "est", "z"]].rename(columns={"z": "z_cor"})
    x = x.merge(cor, on="dt", how="left")
    if cruz is not None:
        x = x.merge(cruz, on="dt", how="left")
    else:
        for c in GRUPOS["D"]:
            x[c] = np.nan
    x["dia"], x["ano"], x["c"], x["atr_px"] = d["dia"], d["dt"].dt.year, d["c"], d["atr"]
    x["hhmm"] = d["dt"].dt.hour * 100 + d["dt"].dt.minute
    x["fecha"] = d["dt"] + pd.Timedelta(minutes=tf)
    x["valido_hora"] = (x["fecha"].dt.hour * 60 + x["fecha"].dt.minute >= 9 * 60 + 30) & (x["fecha"].dt.hour * 60 + x["fecha"].dt.minute <= 17 * 60)
    for h in HORIZONTES:
        f = {"dia": d["dia"].shift(-h), "slot": d["slot"].shift(-h)}
        consecutivo = (f["dia"] == d["dia"]) & (f["slot"] == d["slot"] + h)
        hh = d["h"][::-1].rolling(h).max()[::-1].shift(-1)
        ll = d["l"][::-1].rolling(h).min()[::-1].shift(-1)
        x[f"y_vol{h}"] = np.log(((hh - ll) / d["c"]).where(consecutivo & ((hh - ll) > 0)))
        ret = (d["c"].shift(-h) - d["o"].shift(-1)) / d["o"].shift(-1) * 1e4
        x[f"ret{h}_pb"] = ret.where(consecutivo)
        x[f"y_dir{h}"] = (ret > 0).astype(float).where(consecutivo)
        base = x[f"y_vol{h}"].groupby(d["slot"]).transform(lambda z: z.shift(1).rolling(60, min_periods=30).mean())
        x[f"B0_{h}"] = base
    if ate:
        x = x[x["dt"] <= pd.Timestamp(ate)]
    if desde:
        x = x[x["dt"] >= pd.Timestamp(desde)]
    return x.reset_index(drop=True)


def cruzamento(serie: str, tf: int) -> pd.DataFrame:
    d = _barras(carregar_serie(serie, f"{tf}min"), tf)
    e = _estrutura(d)
    out = pd.DataFrame({"dt": d["dt"], "x_ret1": e["ret1"], "x_ret2": e["ret2"], "x_ret4": e["ret4"], "x_ret_dia": e["ret_dia"]})
    return out


def com_alvo(x: pd.DataFrame, h: int) -> pd.DataFrame:
    """Copia com ``B0`` apontando para a linha de base do horizonte ``h``."""
    y = x.copy()
    y["B0"] = y[f"B0_{h}"]
    return y


def modelo(tipo: str, alvo: str):
    if alvo == "vol":
        if tipo == "linear":
            return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=10.0))
        return HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=200, min_samples_leaf=200, l2_regularization=1.0, random_state=0)
    if tipo == "linear":
        return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(C=0.1, max_iter=500))
    return HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200, min_samples_leaf=200, l2_regularization=1.0, random_state=0)


def _prever(m, X, alvo):
    return m.predict(X) if alvo == "vol" else m.predict_proba(X)[:, 1]


def walk_forward(x: pd.DataFrame, cols: list[str], alvo: str, h: int, tipo: str, anos=ANOS_TESTE, rotulo: str | None = None) -> pd.DataFrame:
    """Previsões fora da amostra (uma linha por observação de teste) com ``dia``, ``ano``, ``y``, ``p`` e ``ret``."""
    y_col = rotulo or (f"y_vol{h}" if alvo == "vol" else f"y_dir{h}")
    x = com_alvo(x, h)
    ok = x["valido_hora"] & x[y_col].notna() & x["B0"].notna() & x["lrng20"].notna() & x["atr_ratio"].notna()
    x = x[ok].reset_index(drop=True)
    saida = []
    for ano in anos:
        tr, te = x[x["ano"] < ano], x[x["ano"] == ano]
        if len(tr) < 2000 or te.empty:
            continue
        m = modelo(tipo, alvo).fit(tr[cols], tr[y_col])
        p = _prever(m, te[cols], alvo)
        o = te[["dia", "ano", "B0", "lrng1", "lrng5", "lrng20", "c", "atr_px"]].copy()
        o["y"], o["p"], o["ret"] = te[y_col].to_numpy(), p, te[f"ret{h}_pb"].to_numpy()
        if alvo == "vol":
            o["res_tr"] = np.quantile(tr[y_col] - m.predict(tr[cols]), 0.8)
        saida.append(o[["dia", "ano", "y", "p", "ret", "B0", "lrng1", "lrng5", "lrng20", "c", "atr_px"] + (["res_tr"] if alvo == "vol" else [])])
    return pd.concat(saida, ignore_index=True)


def har(x: pd.DataFrame, h: int, anos=ANOS_TESTE) -> pd.DataFrame:
    """Linha de base B1: OLS em B0, lrng1, lrng5, lrng20, reajustada a cada dobra (mesmas linhas de teste do walk-forward)."""
    y_col = f"y_vol{h}"
    x = com_alvo(x, h)
    ok = x["valido_hora"] & x[y_col].notna() & x["B0"].notna() & x["lrng20"].notna() & x["atr_ratio"].notna()
    x = x[ok].reset_index(drop=True)
    saida = []
    for ano in anos:
        tr, te = x[x["ano"] < ano], x[x["ano"] == ano]
        if len(tr) < 2000 or te.empty:
            continue
        m = LinearRegression().fit(tr[HAR], tr[y_col])
        o = te[["dia", "ano", "B0"]].copy()
        o["y"], o["p"] = te[y_col].to_numpy(), m.predict(te[HAR])
        saida.append(o)
    return pd.concat(saida, ignore_index=True)


def auc(y: np.ndarray, p: np.ndarray) -> float:
    n1 = y.sum()
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return np.nan
    r = rankdata(p)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def _por_dia(df: pd.DataFrame):
    idx = df.groupby("dia").indices
    return list(idx.values())


def auc_boot(df: pd.DataFrame, reps: int = 400, seed: int = 0) -> tuple[float, float]:
    """AUC agregada e desvio bootstrap reamostrando pregões."""
    y, p = df["y"].to_numpy(), df["p"].to_numpy()
    base = auc(y, p)
    dias = _por_dia(df)
    g = np.random.default_rng(seed)
    vals = []
    for _ in range(reps):
        sel = g.integers(0, len(dias), len(dias))
        ii = np.concatenate([dias[k] for k in sel])
        vals.append(auc(y[ii], p[ii]))
    return base, float(np.nanstd(vals, ddof=1))


def t_dia(df: pd.DataFrame, col: str) -> tuple[float, float]:
    """Média por pregão (soma do dia) e t simples entre pregões."""
    s = df.groupby("dia")[col].sum()
    if len(s) < 3 or s.std(ddof=1) == 0:
        return float(s.mean()), np.nan
    return float(s.mean()), float(s.mean() / (s.std(ddof=1) / np.sqrt(len(s))))


def economico(df: pd.DataFrame) -> dict:
    """Esperança líquida por trade (pb): segue o lado previsto (p > 0,5)."""
    lado = np.where(df["p"] > 0.5, 1.0, -1.0)
    liq = lado * df["ret"].to_numpy() - CUSTO_PB
    d = df.assign(liq=liq)
    m, t = t_dia(d, "liq")
    return {"liq_pb": float(liq.mean()), "bruto_pb": float((lado * df["ret"].to_numpy()).mean()), "t_dia": t, "n": len(df)}


def auc_por_ano(df: pd.DataFrame) -> dict:
    return {int(a): auc(g["y"].to_numpy(), g["p"].to_numpy()) for a, g in df.groupby("ano")}


def perda(df: pd.DataFrame, ref: pd.DataFrame | None = None) -> pd.Series:
    """Perda quadrática por observação."""
    return (df["y"] - df["p"]) ** 2


def ganho_perda(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """Ganho de perda quadrática de ``a`` sobre ``b`` (b − a, positivo = a melhor), t por pregão e fração de anos positivos."""
    j = pd.DataFrame({"dia": a["dia"].to_numpy(), "ano": a["ano"].to_numpy(), "la": ((a["y"] - a["p"]) ** 2).to_numpy(), "lb": ((b["y"] - b["p"]) ** 2).to_numpy()})
    j["g"] = j["lb"] - j["la"]
    m, t = t_dia(j, "g")
    anos = j.groupby("ano").apply(lambda z: z["lb"].sum() - z["la"].sum())
    return {"skill": float(1 - j["la"].sum() / j["lb"].sum()), "t_dia": t, "anos_pos": int((anos > 0).sum()), "anos": int(len(anos))}


def auc_diff_boot(a: pd.DataFrame, b: pd.DataFrame, reps: int = 400, seed: int = 0) -> tuple[float, float]:
    """Diferença de AUC (a − b) nas mesmas observações e desvio bootstrap por pregão."""
    y, pa, pb = a["y"].to_numpy(), a["p"].to_numpy(), b["p"].to_numpy()
    base = auc(y, pa) - auc(y, pb)
    dias = _por_dia(a)
    g = np.random.default_rng(seed)
    vals = []
    for _ in range(reps):
        sel = g.integers(0, len(dias), len(dias))
        ii = np.concatenate([dias[k] for k in sel])
        vals.append(auc(y[ii], pa[ii]) - auc(y[ii], pb[ii]))
    return base, float(np.nanstd(vals, ddof=1))


def embaralhar_rotulo(x: pd.DataFrame, h: int, seed: int) -> pd.Series:
    """Placebo: permuta ``y_dir`` entre pregões do mesmo ano e do mesmo slot (quebra a ligação variável → rótulo)."""
    g = np.random.default_rng(seed)
    y = x[f"y_dir{h}"].copy()
    for _, idx in x.groupby(["ano", "slot"]).indices.items():
        v = y.iloc[idx].to_numpy().copy()
        g.shuffle(v)
        y.iloc[idx] = v
    return y
