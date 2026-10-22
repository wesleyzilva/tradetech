"""Motor M18 — estrutura intradiária (momentum do dia, faixas, dia da semana, gap, faixa de abertura).

Implementa as definições congeladas em ``METODO.md``. Cada célula produz uma observação por pregão (em pb, já como excedente
sobre a deriva) e as estatísticas por período saem de ``estatisticas``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
for p in (RAIZ, RAIZ / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from tradetech.dados import carregar_serie  # noqa: E402

CUSTO_PB = 0.4
NSLOTS = 17
S_1000, S_1200_C, S_EOD = 1, 5, 16  # índices das barras: fechamento 10:00 = C[1]; 12:00 = C[5]; EOD = C[16]
ORIGENS = {"10:00": 2, "14:00": 10, "16:00": 14}
SAIDAS = {"10:00": 1, "12:00": 5, "EOD": 16}
FAIXAS_NOME = [f"{9 + (k * 30) // 60:02d}:{(k * 30) % 60:02d}" for k in range(NSLOTS)]
DISC, HOLD = (2014, 2019), (2020, 2025)
LIM_DESC, LIM_HOLD = 3.0, 2.0
ANOS_MIN_MESMO_SINAL = 8


class Dia:
    """Matrizes pregão × barra (abertura, máxima, mínima, fechamento) e variáveis diárias."""

    def __init__(self, serie: str):
        d = carregar_serie(serie, "30min")
        d["dia"] = d["dt"].dt.normalize()
        d["slot"] = (d["dt"].dt.hour * 60 + d["dt"].dt.minute - 9 * 60) // 30
        fecha_ant = d.groupby("dia")["c"].last().shift(1)
        diario = d.groupby("dia").agg(h=("h", "max"), l=("l", "min"))
        atrd = (diario["h"] - diario["l"]).rolling(20).mean().shift(1)
        u = d[(d["slot"] >= 0) & (d["slot"] < NSLOTS)]
        completo = u.groupby("dia")["slot"].nunique() == NSLOTS
        u = u[u["dia"].isin(completo[completo].index)]
        self.O, self.H, self.L, self.C = (u.pivot(index="dia", columns="slot", values=k).sort_index() for k in ("o", "h", "l", "c"))
        self.dias = self.O.index
        self.ano = pd.Series(self.dias.year, index=self.dias)
        self.dow = pd.Series(self.dias.dayofweek, index=self.dias)
        self.fecha_ant = fecha_ant.reindex(self.dias)
        self.atrd = atrd.reindex(self.dias)


def periodo(ano: int) -> str:
    if DISC[0] <= ano <= DISC[1]:
        return "desc"
    if HOLD[0] <= ano <= HOLD[1]:
        return "hold"
    return "novo"


def _excedente(ret: pd.Series, lado: pd.Series, deriva: pd.Series) -> pd.DataFrame:
    return pd.DataFrame({"x": lado * (ret - deriva), "bruto": lado * ret})


def _deriva(ret_todos: pd.Series, ano: pd.Series, chave: pd.Series | None = None) -> pd.Series:
    """Média dos retornos de todos os pregões do mesmo período (``desc``/``hold``; ano novo usa o próprio ano)."""
    per = ano.map(periodo)
    grupo = per.where(per != "novo", "n" + ano.astype(str))
    if chave is None:
        return ret_todos.groupby(grupo).transform("mean")
    return ret_todos.groupby([grupo, chave]).transform("mean")


def celulas(d: Dia) -> dict[str, tuple[str, pd.DataFrame]]:
    """Devolve ``{rotulo: (tipo, DataFrame[dia, x, bruto, grupo?])}``. ``tipo`` ∈ {"media", "welch"}."""
    out: dict[str, tuple[str, pd.DataFrame]] = {}
    O, C, H, L = d.O, d.C, d.H, d.L

    for nome, k in ORIGENS.items():
        entrada = O[k]
        ret = (C[S_EOD] - entrada) / entrada * 1e4
        lado = np.sign(entrada - O[0])
        ok = lado != 0
        dr = _deriva(ret, d.ano)
        out[f"ID-H01 · {nome}"] = ("media", _excedente(ret, lado, dr)[ok])

    ret_barra = (C - O) / O * 1e4
    excesso = ret_barra.sub(ret_barra.mean(axis=1), axis=0)
    for k in range(NSLOTS):
        out[f"ID-H02 · {FAIXAS_NOME[k]}"] = ("media", pd.DataFrame({"x": excesso[k], "bruto": ret_barra[k]}))

    ret_dia = (C[S_EOD] - O[0]) / O[0] * 1e4
    nomes_dow = ["seg", "ter", "qua", "qui", "sex"]
    for w in range(5):
        out[f"ID-H03 · {nomes_dow[w]}"] = ("welch", pd.DataFrame({"x": ret_dia, "bruto": ret_dia, "grupo": (d.dow == w)}))

    gap = O[0] - d.fecha_ant
    lado_gap = -np.sign(gap)
    grande = gap.abs() >= 0.5 * d.atrd
    for sn, s in SAIDAS.items():
        ret = (C[s] - O[0]) / O[0] * 1e4
        dr = _deriva(ret, d.ano)
        base = _excedente(ret, lado_gap, dr)
        ok = (lado_gap != 0) & lado_gap.notna() & d.atrd.notna()
        out[f"ID-H04 · gap, todos, saída {sn}"] = ("media", base[ok])
        out[f"ID-H04 · gap ≥ 0,5 ATRd, saída {sn}"] = ("media", base[ok & grande])

    for or_nome, or_slots, sinais in (("09:00–09:30", [0], [1, 2, 3]), ("09:00–10:00", [0, 1], [2, 3])):
        hi = H[or_slots].max(axis=1)
        lo = L[or_slots].min(axis=1)
        entrada_slot = pd.Series(np.nan, index=d.dias)
        lado = pd.Series(0.0, index=d.dias)
        for s in sinais:
            acima, abaixo = C[s] > hi, C[s] < lo
            novo = (lado == 0) & (acima | abaixo)
            lado = lado.where(~novo, acima.astype(float) - abaixo.astype(float))
            entrada_slot = entrada_slot.where(~novo, s + 1)
        tem = lado != 0
        for sn in ("12:00", "EOD"):
            e = SAIDAS[sn]
            pe = pd.Series(np.nan, index=d.dias)
            deriva = pd.Series(np.nan, index=d.dias)
            for s in range(1, 5):
                pe = pe.where(entrada_slot != s, O[s])
                r_all = (C[e] - O[s]) / O[s] * 1e4
                deriva = deriva.where(entrada_slot != s, _deriva(r_all, d.ano))
            ret = (C[e] - pe) / pe * 1e4
            out[f"ID-H05 · OR {or_nome}, saída {sn}"] = ("media", _excedente(ret, lado, deriva)[tem])
    return out


def _t(x: np.ndarray) -> float:
    n = len(x)
    if n < 3 or np.nanstd(x, ddof=1) == 0:
        return float("nan")
    return float(np.mean(x) / (np.std(x, ddof=1) / np.sqrt(n)))


def estatisticas(tipo: str, df: pd.DataFrame, ano: pd.Series, a0: int, a1: int) -> dict:
    """Média, t, acerto e n no intervalo de anos ``[a0, a1]``."""
    m = (ano.reindex(df.index) >= a0) & (ano.reindex(df.index) <= a1)
    g = df[m]
    if tipo == "media":
        x = g["x"].dropna().to_numpy()
        if len(x) < 3:
            return {"media": np.nan, "t": np.nan, "acerto": np.nan, "n": len(x)}
        return {"media": float(x.mean()), "t": _t(x), "acerto": float((g["bruto"].dropna() > 0).mean()), "n": len(x)}
    a = g[g["grupo"]]["x"].dropna().to_numpy()
    b = g[~g["grupo"]]["x"].dropna().to_numpy()
    if len(a) < 3 or len(b) < 3:
        return {"media": np.nan, "t": np.nan, "acerto": np.nan, "n": len(a)}
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    dif = float(a.mean() - b.mean())
    return {"media": dif, "t": float(dif / se), "acerto": float((a > b.mean()).mean()), "n": len(a)}


def por_ano(tipo: str, df: pd.DataFrame, ano: pd.Series) -> dict[int, float]:
    res = {}
    for a in sorted(ano.unique()):
        s = estatisticas(tipo, df, ano, a, a)
        res[int(a)] = s["media"]
    return res
