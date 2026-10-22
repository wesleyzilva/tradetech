"""Réplica em Python do robô ``Robo_Microestrutura_Barreiras`` (NTSL) — motor M02.

Objetivo: reproduzir *fielmente* a lógica do fonte NTSL para medir o que ela faz nos candles
que temos, com custos e controles explícitos. Não é um otimizador.

Convenções (todas registradas em ``METODO.md`` do motor):

* Os sinais são avaliados no **fechamento** da barra ``i`` (como o NTSL).
* Ordens a mercado enviadas no fechamento de ``i`` são executadas na **abertura** de ``i+1``.
* Stop/alvo são ordens enviadas ao fim de cada barra com posição aberta (recalculadas a cada barra com o ATR
  da barra que acabou de fechar) e só passam a valer na barra seguinte; logo a **barra de entrada fica sem
  proteção** (``protecao_na_barra_de_entrada=False``, perfil fiel). O perfil ``True`` assume ordens ativas desde a
  abertura (perfil "ideal", útil como limite superior).
* Stop-limit (gatilho = ``vStop``; limite = ``vStop ∓ OffsetTicks``): se, ao enviar a ordem, o preço de
  fechamento já estiver além do limite, a ordem fica passiva (só executa se o preço voltar ao limite).
* Barra com stop e alvo no mesmo minuto: assume-se o stop primeiro (pessimista).
* ``Time`` do NTSL é tratado como HHMM e referido ao **horário da barra** do CSV (abertura). A diferença de
  1 barra não altera as janelas de forma material em 1 min (ver sensibilidade em ``ANALISE_001``).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Params:
    hora_ouro_ini: int = 915
    hora_ouro_fim: int = 1200
    consol_ini: int = 1200
    consol_fim: int = 1400
    mod_ini: int = 1400
    mod_fim: int = 1615
    zeramento: int = 1720
    periodo_atr: int = 20
    mult_sg: float = 2.5
    mult_sl: float = 0.5
    max_barras: int = 20
    offset: float = 5.0
    mult_brilhante: float = 1.70
    mult_escuro: float = 1.30
    sl_min: float = 35.0
    sg_min: float = 120.0
    periodo_media: int = 20
    contextos: tuple = (1, 2, 3)
    protecao_na_barra_de_entrada: bool = False
    custo_pts: float = 0.0
    slippage_stop_pts: float = 0.0
    stop_primeiro: bool = True
    gap_max_min: int = 10
    stop_a_mercado: bool = False


def hhmm(dt: pd.Series) -> np.ndarray:
    return (dt.dt.hour * 100 + dt.dt.minute).to_numpy()


def preparar(d: pd.DataFrame, p: Params) -> pd.DataFrame:
    """Calcula ATR (média simples do True Range, janela inclui a barra atual), estados e SMA."""
    d = d.sort_values("dt").reset_index(drop=True).copy()
    pc = d["c"].shift(1)
    rng = d["h"] - d["l"]
    tr = pd.concat([rng, (d["h"] - pc).abs(), (d["l"] - pc).abs()], axis=1).max(axis=1)
    tr.iloc[0] = rng.iloc[0]
    d["rng"] = rng
    d["tr"] = tr
    d["atr"] = tr.rolling(p.periodo_atr).mean()
    d["sma"] = d["c"].rolling(p.periodo_media).mean()
    brilhante = d["rng"] >= d["atr"] * p.mult_brilhante
    escuro = (d["rng"] >= d["atr"] * p.mult_escuro) & ~brilhante
    alta = d["c"] >= d["o"]
    est = np.zeros(len(d), dtype=np.int8)
    est[(escuro & alta).to_numpy()] = 1
    est[(escuro & ~alta).to_numpy()] = 2
    est[(brilhante & alta).to_numpy()] = 3
    est[(brilhante & ~alta).to_numpy()] = 4
    d["est"] = est
    d["hhmm"] = hhmm(d["dt"])
    d["dia"] = d["dt"].dt.normalize()
    return d


def janela_ativa(hm: np.ndarray, p: Params) -> np.ndarray:
    ouro = (hm >= p.hora_ouro_ini) & (hm < p.hora_ouro_fim)
    mod = (hm >= p.mod_ini) & (hm <= p.mod_fim)
    return ouro | mod


def gerar_sinais(d: pd.DataFrame, p: Params) -> pd.DataFrame:
    """Sinal (+1 compra, -1 venda) e contexto (1 fade alta, 2 fade baixa, 3 fluxo neutro) por barra."""
    est = d["est"].to_numpy()
    est_ant = np.r_[0, est[:-1]]
    c, o, h, l, sma = (d[k].to_numpy() for k in ("c", "o", "h", "l", "sma"))
    c1, o1, h1, l1 = (np.r_[np.nan, x[:-1]] for x in (c, o, h, l))
    ctx1 = (est_ant == 3) & (c1 > o1) & (c < l1)
    ctx2 = (est_ant == 4) & (c1 < o1) & (c > h1)
    neutro = (est == 0) & (est_ant == 0)
    ctx3c = neutro & (c > sma) & (c > o) & (c > h1)
    ctx3v = neutro & (c < sma) & (c < o) & (c < l1)
    sinal = np.zeros(len(d), dtype=np.int8)
    contexto = np.zeros(len(d), dtype=np.int8)
    ativos = set(p.contextos)
    # prioridade do NTSL: ctx1, ctx2, ctx3
    if 3 in ativos:
        sinal[ctx3c] = 1
        sinal[ctx3v] = -1
        contexto[ctx3c | ctx3v] = 3
    if 2 in ativos:
        sinal[ctx2] = 1
        contexto[ctx2] = 2
    if 1 in ativos:
        sinal[ctx1] = -1
        contexto[ctx1] = 1
    na_janela = janela_ativa(d["hhmm"].to_numpy(), p)
    sinal = np.where(na_janela, sinal, 0).astype(np.int8)
    contexto = np.where(sinal != 0, contexto, 0).astype(np.int8)
    d = d.copy()
    d["sinal"] = sinal
    d["ctx"] = contexto
    return d


def distancias(atr: float, p: Params) -> tuple[float, float]:
    sl = max(round(atr * p.mult_sl), p.sl_min)
    sg = max(round(atr * p.mult_sg), p.sg_min)
    return float(sl), float(sg)


@dataclass
class _Pos:
    lado: int
    entrada: float
    i_entrada: int
    ctx: int
    barras: int = 0
    stop: float | None = None
    stop_limite: float | None = None
    alvo: float | None = None
    stop_passivo: bool = False
    teve_passivo: bool = False
    sl_pts: float = 0.0
    sg_pts: float = 0.0
    mfe: float = 0.0
    mae: float = 0.0
    log: list = field(default_factory=list)


def _colocar_ordens(pos: _Pos, atr_i: float, close_i: float, p: Params) -> None:
    sl, sg = distancias(atr_i, p)
    pos.sl_pts, pos.sg_pts = sl, sg
    if pos.lado > 0:
        pos.alvo = pos.entrada + sg
        pos.stop = pos.entrada - sl
        pos.stop_limite = pos.stop - p.offset
        pos.stop_passivo = close_i <= pos.stop_limite
    else:
        pos.alvo = pos.entrada - sg
        pos.stop = pos.entrada + sl
        pos.stop_limite = pos.stop + p.offset
        pos.stop_passivo = close_i >= pos.stop_limite
    if p.stop_a_mercado:
        pos.stop_passivo = False
    pos.teve_passivo = pos.teve_passivo or pos.stop_passivo


def _avaliar_barra(pos: _Pos, o: float, h: float, l: float, p: Params):
    """Retorna (preço, motivo) se a posição sai dentro da barra, senão None."""
    lado = pos.lado
    stop, lim, alvo = pos.stop, pos.stop_limite, pos.alvo
    if lado > 0:
        toca_stop = l <= stop
        toca_alvo = h >= alvo
        if pos.stop_passivo:
            if h >= lim:
                preco = max(o, lim)
                return preco, "STOP_PASSIVO"
            toca_stop = False
        if toca_stop and (p.stop_primeiro or not toca_alvo):
            preco = o if o <= stop else stop
            if preco < lim and not p.stop_a_mercado:
                if h >= lim:
                    return lim, "STOP_PASSIVO"
                return None
            return preco - p.slippage_stop_pts, "SL"
        if toca_alvo:
            return max(o, alvo) if o >= alvo else alvo, "SG"
    else:
        toca_stop = h >= stop
        toca_alvo = l <= alvo
        if pos.stop_passivo:
            if l <= lim:
                preco = min(o, lim)
                return preco, "STOP_PASSIVO"
            toca_stop = False
        if toca_stop and (p.stop_primeiro or not toca_alvo):
            preco = o if o >= stop else stop
            if preco > lim and not p.stop_a_mercado:
                if l <= lim:
                    return lim, "STOP_PASSIVO"
                return None
            return preco + p.slippage_stop_pts, "SL"
        if toca_alvo:
            return min(o, alvo) if o <= alvo else alvo, "SG"
    return None


def simular(d: pd.DataFrame, p: Params) -> pd.DataFrame:
    """Percorre as barras e devolve uma linha por trade. ``d`` deve vir de ``preparar`` + ``gerar_sinais``."""
    o, h, l, c = (d[k].to_numpy(float) for k in ("o", "h", "l", "c"))
    atr = d["atr"].to_numpy(float)
    sinal = d["sinal"].to_numpy()
    ctxs = d["ctx"].to_numpy()
    hm = d["hhmm"].to_numpy()
    dia = d["dia"].to_numpy()
    dts = d["dt"].to_numpy()
    n = len(d)
    trades = []
    pos: _Pos | None = None

    def mesmo_pregao(i: int, j: int) -> bool:
        return j < n and dia[i] == dia[j] and (dts[j] - dts[i]) <= np.timedelta64(p.gap_max_min, "m")

    def fechar(preco: float, i_saida: int, motivo: str) -> None:
        nonlocal pos
        pnl = (preco - pos.entrada) * pos.lado
        trades.append(
            {
                "dt_entrada": dts[pos.i_entrada],
                "dt_saida": dts[i_saida],
                "dia": dia[pos.i_entrada],
                "lado": pos.lado,
                "ctx": pos.ctx,
                "entrada": pos.entrada,
                "saida": preco,
                "pnl_bruto": pnl,
                "pnl": pnl - p.custo_pts,
                "barras": i_saida - pos.i_entrada + 1,
                "motivo": motivo,
                "hhmm_entrada": hm[pos.i_entrada],
                "sl_pts": pos.sl_pts,
                "sg_pts": pos.sg_pts,
                "atr_sinal": atr[pos.i_entrada - 1],
                "armadilha": pos.teve_passivo,
                "mfe": pos.mfe,
                "mae": pos.mae,
            }
        )
        pos = None

    for i in range(n):
        if pos is not None:
            tem_ordens = pos.stop is not None
            if pos.i_entrada == i and p.protecao_na_barra_de_entrada:
                _colocar_ordens(pos, atr[i - 1], pos.entrada, p)
                tem_ordens = True
            # excursões (informativo)
            ex_fav = (h[i] - pos.entrada) if pos.lado > 0 else (pos.entrada - l[i])
            ex_adv = (pos.entrada - l[i]) if pos.lado > 0 else (h[i] - pos.entrada)
            pos.mfe = max(pos.mfe, ex_fav)
            pos.mae = max(pos.mae, ex_adv)
            if tem_ordens:
                r = _avaliar_barra(pos, o[i], h[i], l[i], p)
                if r is not None:
                    fechar(r[0], i, r[1])
        if pos is not None:
            pos.barras += 1
            fim = i + 1 >= n or not mesmo_pregao(i, i + 1)
            if pos.barras >= p.max_barras:
                fechar(c[i] if fim else o[i + 1], i, "TEMPO")
            elif hm[i] >= p.zeramento:
                fechar(c[i] if fim else o[i + 1], i, "ZERAMENTO")
            elif fim:
                fechar(c[i], i, "FIM_PREGAO")
            else:
                _colocar_ordens(pos, atr[i], c[i], p)
        if pos is None and sinal[i] != 0 and i + 1 < n and mesmo_pregao(i, i + 1) and not np.isnan(atr[i]):
            pos = _Pos(lado=int(sinal[i]), entrada=o[i + 1], i_entrada=i + 1, ctx=int(ctxs[i]))
    if pos is not None:
        fechar(c[n - 1], n - 1, "FIM_DADOS")
    out = pd.DataFrame(trades)
    return out


def rodar(df: pd.DataFrame, p: Params | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    p = p or Params()
    d = gerar_sinais(preparar(df, p), p)
    return d, simular(d, p)


def metricas(trades: pd.DataFrame, rr_nominal: float | None = None) -> dict:
    """Métricas descritivas em pontos; t-stat por pregão (cluster) para respeitar dependência intradia."""
    if trades.empty:
        return {"n": 0}
    pnl = trades["pnl"]
    ganhos = pnl[pnl > 0].sum()
    perdas = -pnl[pnl < 0].sum()
    por_dia = trades.groupby("dia")["pnl"].sum()
    t_dia = por_dia.mean() / (por_dia.std(ddof=1) / np.sqrt(len(por_dia))) if len(por_dia) > 2 and por_dia.std(ddof=1) > 0 else np.nan
    t_trade = pnl.mean() / (pnl.std(ddof=1) / np.sqrt(len(pnl))) if len(pnl) > 2 and pnl.std(ddof=1) > 0 else np.nan
    acum = pnl.cumsum()
    dd = (acum - acum.cummax()).min()
    wins = pnl[pnl > 0]
    loss = pnl[pnl < 0]
    payoff = wins.mean() / abs(loss.mean()) if len(wins) and len(loss) else np.nan
    wr = (pnl > 0).mean()
    return {
        "n": len(pnl),
        "pregoes": int(trades["dia"].nunique()),
        "trades_por_pregao": len(pnl) / trades["dia"].nunique(),
        "win_rate": wr,
        "pnl_total": pnl.sum(),
        "pnl_medio": pnl.mean(),
        "profit_factor": ganhos / perdas if perdas > 0 else np.nan,
        "payoff": payoff,
        "wr_breakeven": 1 / (1 + payoff) if payoff == payoff else np.nan,
        "t_trade": t_trade,
        "t_pregao": t_dia,
        "max_dd": dd,
        "pior_trade": pnl.min(),
        "melhor_trade": pnl.max(),
    }


def aleatorio_mesma_saida(d: pd.DataFrame, p: Params, n_rep: int = 200, seed: int = 7, prob_entrada: float | None = None) -> pd.DataFrame:
    """Controle: mesmas janelas e mesma gestão de saída, mas lado aleatório e entrada em barras sorteadas.

    ``prob_entrada`` é calibrada para igualar a frequência de sinais do robô (sinais por barra de janela).
    """
    rng = np.random.default_rng(seed)
    na_janela = janela_ativa(d["hhmm"].to_numpy(), p)
    freq = (d["sinal"].to_numpy() != 0).sum() / max(na_janela.sum(), 1) if prob_entrada is None else prob_entrada
    saidas = []
    for r in range(n_rep):
        sorteio = rng.random(len(d)) < freq
        lado = rng.choice([-1, 1], size=len(d))
        sinal = np.where(sorteio & na_janela, lado, 0).astype(np.int8)
        dd = d.copy()
        dd["sinal"] = sinal
        dd["ctx"] = np.where(sinal != 0, 9, 0).astype(np.int8)
        t = simular(dd, p)
        m = metricas(t)
        saidas.append({"rep": r, **m})
    return pd.DataFrame(saidas)


def com(p: Params, **kw) -> Params:
    return replace(p, **kw)
