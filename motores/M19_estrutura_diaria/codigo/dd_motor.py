"""Motor M19 — estrutura diária e semanal (momentum/reversão, compressão, vencimento, dia anterior).

Implementa ``METODO.md``. Reaproveita as estatísticas do M18 (``id_motor``): média, t, Welch e tabela por ano.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
for p in (RAIZ, RAIZ / "src", RAIZ / "motores" / "M18_estrutura_intradiaria" / "codigo"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import id_motor as im  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402


def barras(ativo: str, tf: str) -> pd.DataFrame:
    d = carregar_serie(ativo, tf).set_index("dt")[["o", "h", "l", "c"]].astype(float)
    return d


def semanal_do_diario(D: pd.DataFrame) -> pd.DataFrame:
    """Barras semanais (segunda a sexta) montadas do diário. O ``W1`` do Profit só traz 521 semanas e deixa buracos em 2018–2019."""
    inicio = D.index.to_period("W-FRI").start_time
    g = D.groupby(inicio)
    return pd.DataFrame({"o": g["o"].first(), "h": g["h"].max(), "l": g["l"].min(), "c": g["c"].last()})


def semanas_vencimento(anos: range) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Segunda a sexta da semana que contém a quarta-feira mais próxima do dia 15 dos meses pares (regra do WIN)."""
    out = []
    for a in anos:
        for mes in (2, 4, 6, 8, 10, 12):
            d15 = pd.Timestamp(a, mes, 15)
            off = (2 - d15.dayofweek + 3) % 7 - 3
            qua = d15 + pd.Timedelta(days=off)
            seg = qua - pd.Timedelta(days=2)
            out.append((seg, seg + pd.Timedelta(days=4)))
    return out


def _lado_celula(ret: pd.Series, lado: pd.Series, ano: pd.Series, ok: pd.Series) -> pd.DataFrame:
    return im._excedente(ret, lado, im._deriva(ret, ano))[ok]


def celulas(ativo: str) -> tuple[dict[str, tuple[str, bool, pd.DataFrame]], pd.Series]:
    """``{rotulo: (tipo, com_custo, df)}`` e a série de ano (índice = datas diárias)."""
    D = barras(ativo, "D1")
    W = semanal_do_diario(D)
    out: dict[str, tuple[str, bool, pd.DataFrame]] = {}
    ano_d = pd.Series(D.index.year, index=D.index)
    ano_w = pd.Series(W.index.year, index=W.index)

    for k in (5, 20):
        lado = np.sign(D["c"] / D["c"].shift(k) - 1)
        ent, sai = D["o"].shift(-1), D["c"].shift(-1)
        ret = (sai - ent) / ent * 1e4
        ok = (lado != 0) & ret.notna() & lado.notna()
        out[f"DD-H01 · diário k={k}"] = ("media", True, _lado_celula(ret, lado, ano_d, ok))
    for k in (1, 4):
        lado = np.sign(W["c"] / W["c"].shift(k) - 1)
        ent, sai = W["o"].shift(-1), W["c"].shift(-1)
        ret = (sai - ent) / ent * 1e4
        ok = (lado != 0) & ret.notna() & lado.notna()
        out[f"DD-H01 · semanal k={k}"] = ("media", True, _lado_celula(ret, lado, ano_w, ok))

    R = D["h"] - D["l"]
    atr20 = R.rolling(20).mean()
    razao = R.shift(-1) / atr20
    desvio = razao - im._deriva(razao, ano_d)
    nr7 = R == R.rolling(7).min()
    inside = (D["h"] < D["h"].shift(1)) & (D["l"] > D["l"].shift(1))
    for nome, ev in (("NR7", nr7), ("inside bar", inside)):
        ok = ev & desvio.notna()
        out[f"DD-H02 · {nome}"] = ("media", False, pd.DataFrame({"x": desvio, "bruto": desvio})[ok])

    flag = pd.Series(False, index=D.index)
    for seg, sex in semanas_vencimento(range(D.index.year.min(), D.index.year.max() + 1)):
        flag |= (D.index >= seg) & (D.index <= sex)
    amp = R / atr20.shift(1)
    ret_dia = (D["c"] - D["o"]) / D["o"] * 1e4
    ok = amp.notna()
    out["DD-H03 · amplitude na semana do vencimento"] = ("welch", False, pd.DataFrame({"x": amp, "bruto": amp, "grupo": flag})[ok])
    out["DD-H03 · retorno do dia na semana do vencimento"] = ("welch", False, pd.DataFrame({"x": ret_dia, "bruto": ret_dia, "grupo": flag}))

    corpo = np.sign(D["c"] - D["o"]).shift(1)
    out["DD-H04 · corpo de ontem"] = ("media", True, _lado_celula(ret_dia, corpo, ano_d, (corpo != 0) & corpo.notna()))
    cp = ((D["c"] - D["l"]) / (D["h"] - D["l"]).replace(0, np.nan)).shift(1)
    lado_cp = pd.Series(np.where(cp >= 0.8, 1.0, np.where(cp <= 0.2, -1.0, 0.0)), index=D.index)
    out["DD-H04 · posição do fechamento de ontem"] = ("media", True, _lado_celula(ret_dia, lado_cp, ano_d, (lado_cp != 0) & cp.notna()))
    return out, ano_d
