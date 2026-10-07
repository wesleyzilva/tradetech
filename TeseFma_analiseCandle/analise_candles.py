from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA_ROOT = BASE.parent / "CandlesHistoryDatas"
PASTAS_PADRAO = ["2020_22", "2022_24", "2024_26", "2026", "CandlesHistoricos2026"]
TF_FOCO = ["5min", "15min", "30min", "60min"]
TF_ORD = {"5min": 5, "10min": 10, "15min": 15, "20min": 20, "30min": 30, "60min": 60}
SIMBOLO = {2: "🟢", 1: "🟩", 0: "⬜", -1: "🟥", -2: "🔴"}


def num(s):
    s = s.astype(str).str.strip().str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def ler_csv(path):
    raw = pd.read_csv(path, sep=";", encoding="latin1", dtype=str, header=None)
    if raw.empty:
        return pd.DataFrame(columns=["dt", "o", "h", "l", "c", "v", "q"]) 
    if str(raw.iloc[0, 0]).strip().lower() == "ativo":
        raw = raw.iloc[1:]
    cols = ["ativo", "data", "hora", "o", "h", "l", "c", "v", "q"]
    if raw.shape[1] == 8:
        cols.remove("hora")
    raw.columns = cols
    if "hora" in cols:
        stamp = raw["data"] + " " + raw["hora"]
        dt = pd.to_datetime(stamp, format="%d/%m/%Y %H:%M:%S", errors="coerce")
        if dt.isna().mean() > 0.5:
            dt = pd.to_datetime(stamp, format="%d/%m/%Y %H:%M", errors="coerce")
    else:
        dt = pd.to_datetime(raw["data"], format="%d/%m/%Y", errors="coerce")
    out = pd.DataFrame({"dt": dt, **{k: num(raw[k]) for k in ("o", "h", "l", "c", "v", "q")}})
    return out.dropna(subset=["dt", "o", "h", "l", "c"]).sort_values("dt").drop_duplicates("dt", keep="last").reset_index(drop=True)


def calcular(d, janela=20):
    d = d.copy()
    d["rng"] = d["h"] - d["l"]
    d["m"] = np.where(d["rng"] > 0, (d["c"] - d["o"]) / d["rng"].replace(0, np.nan).fillna(1.0), 0.0)
    v = d["v"].astype(float)
    media_v = v.rolling(janela).mean().shift(1)
    d["a"] = v / media_v.where(media_v > 0)
    d["F"] = d["m"] * d["a"] * 100.0
    d["mu"] = d["F"].rolling(janela).mean()
    d["sd"] = d["F"].rolling(janela).std(ddof=0)
    d["atr"] = d["rng"].rolling(janela).mean().shift(1)
    d["z"] = (d["F"] - d["mu"]) / d["sd"].where(d["sd"] > 1e-9)
    z, F = d["z"].to_numpy(), d["F"].to_numpy()
    d["est"] = np.select(
        [(z >= 2.5) & (F > 0), (z >= 1.5) & (F > 0), (z <= -2.5) & (F < 0), (z <= -1.5) & (F < 0)],
        [2, 1, -2, -1],
        default=0,
    ).astype("int8")
    d["fam"] = np.sign(d["est"]).astype("int8")
    d["hora"] = d["dt"].dt.hour
    d["dia"] = d["dt"].dt.normalize()
    d["am"] = d["m"].abs()
    d["aF"] = d["F"].abs()
    d["body_atr"] = (d["c"] - d["o"]).abs() / d["atr"].replace(0, np.nan).fillna(1.0)
    d["rng_atr"] = d["rng"] / d["atr"].replace(0, np.nan).fillna(1.0)
    return d.dropna(subset=["F", "mu", "sd", "atr"]).reset_index(drop=True)


def esperado_barras(tf):
    if tf.endswith("min"):
        per = int(tf.replace("min", ""))
        return 390 // per
    return 390


def fm(x, dec=2, sinal=False):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    if isinstance(x, str):
        return x
    if abs(x) >= 1000:
        s = f"{x:,.0f}"
    else:
        s = f"{x:.{dec}f}"
    if sinal and x > 0:
        s = "+" + s
    if sinal and x < 0:
        s = "-" + s.replace("-", "", 1)
    return s


def tstat(s):
    s = pd.Series(s).dropna()
    if s.empty or s.std(ddof=1) == 0:
        return np.nan
    return float(s.mean() / (s.std(ddof=1) / math.sqrt(len(s))))


def tabela(cols, rows, align=None):
    if not rows:
        return "| " + " | ".join(cols) + " |\n| " + " | ".join(["---"] * len(cols)) + " |"
    if align is None:
        align = "l" * len(cols)
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join(["---"] * len(cols)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(map(str, row)) + " |")
    return "\n".join([header, sep, *body])


def cabecalho_bloco(ctx):
    return (
        f"_Dados: {ctx.ativo} · pastas {', '.join(ctx.pastas)} · TFs: {', '.join(ctx.tfs)} · cobertura {ctx.cobertura:.0%} · limiares {ctx.k1:.1f}σ/{ctx.k2:.1f}σ_\n\n"
    )


def atualizar_doc(blocos, path):
    path = Path(path)
    texto = path.read_text(encoding="utf-8") if path.exists() else ""
    for bid, conteudo in blocos.items():
        inicio = f"<!-- AUTO:{bid}:INICIO -->"
        fim = f"<!-- AUTO:{bid}:FIM -->"
        bloco = f"{inicio}\n{conteudo}\n{fim}"
        if inicio in texto and fim in texto:
            pat = re.compile(rf"{re.escape(inicio)}.*?{re.escape(fim)}", re.S)
            texto = pat.sub(bloco, texto)
        else:
            texto = texto + "\n\n" + bloco
    path.write_text(texto, encoding="utf-8")


def clusters(d, g=1, incluir_neutro=False):
    d = d.sort_values("dt").reset_index(drop=True)
    fam = d["fam"].to_numpy() if "fam" in d.columns else np.sign(d["est"]).astype(int)
    est = d["est"].to_numpy() if "est" in d.columns else np.zeros(len(d), dtype=int)
    res, cur = [], None
    for i, f in enumerate(fam):
        ok = f != 0 if not incluir_neutro else True
        if f == 0 and not incluir_neutro:
            if cur:
                cur["gap"] += 1
                if cur["gap"] > g:
                    res.append(cur)
                    cur = None
        elif cur and cur["f"] == f:
            cur.update(last=i, gap=0, n=cur["n"] + 1, bri=cur["bri"] or abs(est[i]) == 2)
        else:
            if cur:
                res.append(cur)
            cur = dict(f=f, first=i, last=i, gap=0, n=1, bri=abs(est[i]) == 2)
    if cur:
        res.append(cur)
    out = []
    for r in res:
        s = d.iloc[r["first"]:r["last"] + 1]
        if r["n"] >= 2:
            out.append(
                pd.DataFrame(
                    [{
                        "first": r["first"],
                        "last": r["last"],
                        "n": r["n"],
                        "fam": r["f"],
                        "dt_ini": s["dt"].iloc[0],
                        "dt_fim": s["dt"].iloc[-1],
                        "rng": s["h"].max() - s["l"].min(),
                        "low": s["l"].min(),
                        "high": s["h"].max(),
                        "rng_atr": (s["h"].max() - s["l"].min()) / (s["atr"].replace(0, np.nan).fillna(1.0)).median(),
                        "bright": bool(r["bri"]),
                    }]
                )
            )
    if not out:
        return pd.DataFrame(columns=["first", "last", "n", "fam", "dt_ini", "dt_fim", "rng", "low", "high", "rng_atr", "bright"])
    return pd.concat(out, ignore_index=True)


@dataclass
class Contexto:
    pastas: list[str] = field(default_factory=lambda: PASTAS_PADRAO.copy())
    ativo: str = "WIN"
    tfs: list[str] = field(default_factory=lambda: ["5min", "10min", "15min", "20min", "30min", "60min"])
    tf_foco: list[str] = field(default_factory=lambda: ["5min", "15min"])
    cobertura: float = 0.8
    k1: float = 1.5
    k2: float = 2.5
    sazonal: int = 20
    _cache: dict = field(default_factory=dict, init=False, repr=False)

    def derivar(self, **kwargs):
        data = {k: v for k, v in self.__dict__.items() if k != "_cache"}
        data.update(kwargs)
        return Contexto(**data)

    def fontes(self, ativo=None):
        ativo = (ativo or self.ativo).upper()
        found = []
        if DATA_ROOT.exists():
            for pasta in self.pastas:
                p = DATA_ROOT / pasta
                if not p.exists():
                    continue
                files = list(p.glob(f"{ativo}*F_0_*.csv"))
                if files:
                    found.append(pasta)
        return found

    def _path_for(self, ativo, tf):
        ativo = ativo.upper()
        tf = str(tf)
        for pasta in self.pastas:
            pdir = DATA_ROOT / pasta
            if not pdir.exists():
                continue
            pats = [
                f"{ativo}FUT_F_0_{tf}.csv",
                f"{ativo}FUT_F_0_{tf}.CSV",
                f"{ativo}*_F_0_{tf}.csv",
                f"{ativo}*_F_0_{tf}.CSV",
            ]
            for pat in pats:
                matches = list(pdir.glob(pat))
                if matches:
                    return matches[0]
        raise FileNotFoundError(f"Nenhum CSV encontrado para {ativo} / {tf} em {DATA_ROOT}")

    def _load_series(self, ativo, tf):
        if (ativo, tf) in self._cache:
            return self._cache[(ativo, tf)]
        path = self._path_for(ativo, tf)
        data = ler_csv(path)
        if data.empty:
            self._cache[(ativo, tf)] = pd.DataFrame()
            return self._cache[(ativo, tf)]
        data = calcular(data)
        data["simbolo"] = ativo
        self._cache[(ativo, tf)] = data.sort_values("dt").reset_index(drop=True)
        return self._cache[(ativo, tf)]

    def serie(self, ativo, tf, incluir_atual=True):
        if not incluir_atual:
            d = self._load_series(ativo.upper(), str(tf)).copy()
            if len(d) <= 1:
                return d
            return d.iloc[:-1].reset_index(drop=True)
        return self._load_series(ativo.upper(), str(tf))


def _minhashtbl(x):
    x = pd.Series(x).dropna()
    if x.empty:
        return np.nan
    return float(x.median())


# Backwards-compat aliases used by the validation script.
PASTAS = PASTAS_PADRAO


__all__ = [
    "BASE",
    "DATA_ROOT",
    "PASTAS_PADRAO",
    "TF_FOCO",
    "TF_ORD",
    "Contexto",
    "atualizar_doc",
    "cabecalho_bloco",
    "calcular",
    "clusters",
    "esperado_barras",
    "fm",
    "ler_csv",
    "tabela",
    "tstat",
]
