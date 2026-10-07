"""validacao_econofisica.py - Valida o modelo F = m*a*k e a migracao dos limiares (Pareto -> Bollinger).

Usa o motor de analise_candles.py (mesmos dados e mesma definicao canonica) e regrava os blocos AUTO de
VALIDACAO_ECONOFISICA.md e HIPOTESES.md. Texto fora dos blocos AUTO e manual e nao e tocado.

Uso (a partir da pasta CandlesHistoryDatas):
    python TeseFma_analiseCandle/validacao_econofisica.py                    # atualiza os dois .md
    python TeseFma_analiseCandle/validacao_econofisica.py --dry-run          # imprime sem gravar
    python TeseFma_analiseCandle/validacao_econofisica.py --blocos v5_sinais h_painel
    python TeseFma_analiseCandle/validacao_econofisica.py --dia 2026-07-23   # imprime so o mapa de cores (e clusters)
    python TeseFma_analiseCandle/validacao_econofisica.py --ativo WDO --dry-run   # replica em outro ativo

Reuso: from validacao_econofisica import Val; v = Val(Contexto(cobertura=0.8)); v.d("5min")

Dependencias: pandas, numpy.
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np
import pandas as pd

from TeseFma_analiseCandle.analise_candles import (BASE, PASTAS_PADRAO, TF_FOCO, TF_ORD, Contexto, atualizar_doc, cabecalho_bloco, clusters,
                             esperado_barras, fm, tabela, tstat)

DOC_VAL = BASE / "VALIDACAO_ECONOFISICA.md"
DOC_HIP = BASE / "HIPOTESES.md"
TFS_VAL = ["5min", "10min", "15min", "20min", "30min", "60min"]
COBERTURA, SAZONAL = 0.8, 20
FX1, FX2 = 70.0, 85.0  # limiares fixos dos robos (V11-V16): ignicao / exaustao
SIMBOLO = {2: "🟢", 1: "🟩", 0: "⬜", -1: "🟥", -2: "🔴"}
A_BINS = [(0, 0.7, "baixo (<0.7)"), (0.7, 1.3, "normal (0.7–1.3)"), (1.3, 2.0, "alto (1.3–2)"), (2.0, np.inf, "choque (≥2)")]
M_BINS = [(0, 0.15, "doji (<0.15)"), (0.15, 0.35, "0.15–0.35"), (0.35, 0.55, "0.35–0.55"), (0.55, 0.75, "0.55–0.75"),
          (0.75, 0.90, "0.75–0.90"), (0.90, 1.01, "marubozu (≥0.90)")]
G_M = [(0, 0.3, "indecisão (<0.3)"), (0.3, 0.7, "médio (0.3–0.7)"), (0.7, 1.01, "eficiente (≥0.7)")]
LEITURA = {("choque (≥2)", "indecisão (<0.3)"): "absorção", ("choque (≥2)", "eficiente (≥0.7)"): "impulso",
           ("baixo (<0.7)", "eficiente (≥0.7)"): "deriva sem volume", ("baixo (<0.7)", "indecisão (<0.3)"): "inércia"}
SIG_F, SIG_A, SIG_M = "F = m·a", "a (só volume)", "\\|m\\| (só candle)"
SIG_C, SIG_R = "corpo/ATR (só preço)", "amplitude/ATR (só range)"
CL_BOLL, CL_PAR = "Bollinger: colorido", "Pareto equiparado ao colorido"


# ----------------------------------------------------------------------------- utilidades estatisticas
def gauss2(k):
    return math.erfc(k / math.sqrt(2))  # P(|Z| >= k)


def ajuste(x, y):
    """(inclinacao, R2) da regressao linear simples y ~ x."""
    p = np.polyfit(x, y, 1)
    return p[0], 1 - np.var(y - np.polyval(p, x)) / np.var(y)


def hill(x, frac=0.05):
    """Indice de cauda de Pareto (alfa) pelo estimador de Hill nos `frac` maiores valores."""
    x = np.sort(x[x > 0])[::-1]
    k = max(int(len(x) * frac), 10)
    return 1.0 / np.mean(np.log(x[:k] / x[k]))


def preparar(s):
    """Colunas auxiliares sobre a serie composta (todas as janelas 'proximo candle' ficam dentro do mesmo dia)."""
    d = s.copy()
    g = d.groupby("dia")
    d["cor"] = np.sign(d["c"] - d["o"])
    d["sf1"] = d["cor"] * (g["c"].shift(-1) - d["o"]) 
    d["sf3"] = d["cor"] * (g["c"].shift(-3) - d["o"]) 
    rng = d["rng"].where(d["rng"] > 0)
    atr = d["atr"].where(d["atr"] > 0)
    d["w_up"] = ((d["h"] - d[["o", "c"]].max(axis=1)) / rng).fillna(0)
    d["w_dn"] = ((d[["o", "c"]].min(axis=1) - d["l"]) / rng).fillna(0)
    d["rng_atr"] = d["rng"] / atr
    d["body_atr"] = (d["c"] - d["o"]).abs() / atr
    d["cor"] = np.sign(d["c"] - d["o"])
    d["am"], d["aF"] = d["m"].abs(), d["F"].abs()
    d["rng_next"] = g["rng_atr"].shift(-1)
    d["a_next"] = g["a"].shift(-1)
    d["cor_next"] = g["cor"].shift(-1)
    d["hora_next"] = g["hora"].shift(-1)
    d["exp_rng"] = d["rng_next"] / d.groupby("hora")["rng_next"].transform("mean")  # 1.00 = media daquela hora
    return d


def desfecho(d, sel, minimo=30):
    """O que acontece depois dos candles selecionados: atividade, persistencia da propria classe e retorno alinhado."""
    sel = sel.fillna(False).astype(bool)
    if sel.sum() < minimo:
        return None
    s = d[sel]
    exp = s["exp_rng"].dropna()
    prox = sel.groupby(d["dia"]).shift(-1)
    ok = sel & prox.notna()
    base = d["hora_next"].map(sel.groupby(d["hora"]).mean())  # P(classe | hora do proximo): remove a sazonalidade
    nz = s["sf1"].dropna()
    nz = nz[nz != 0]
    return dict(n=int(sel.sum()), pct=sel.mean(), exp=exp.mean(), t_exp=tstat(exp - 1),
                lift=prox[ok].astype(float).mean() / base[ok].mean(), pc=(nz > 0).mean(),
                sf1=s["sf1"].mean(), t1=tstat(s["sf1"]), sf3=s["sf3"].mean(), t3=tstat(s["sf3"]))


def p_mesma_cor(d, sel):
    x = d[sel & (d["cor"] != 0) & (d["cor_next"].fillna(0) != 0)]
    return (x["cor"] == x["cor_next"]).mean() if len(x) else np.nan


def medir_h27(d, janela=20, k=2.5):
    """Compara a classificação canônica com a variante robusta que exclui o candle atual."""
    if d.empty:
        return {"n_brilhante_canonico": 0, "n_brilhante_robusto": 0, "lift_brilhante_robusto": np.nan,
                "expansao_brilhante_robusto": np.nan, "expansao_brilhante_canonico": np.nan, "dif_expansao": np.nan}

    d = d.copy()
    if "dia" not in d.columns:
        d["dia"] = d["dt"].dt.normalize()
    d["rng_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
    grupo_F = d.groupby("dia", sort=False)["F"]
    mu = grupo_F.transform(lambda s: s.shift(1).rolling(janela, min_periods=janela).mean())
    mad = grupo_F.transform(lambda s: s.shift(1).rolling(janela, min_periods=janela).apply(
        lambda x: np.median(np.abs(x - np.median(x))), raw=True
    ))
    sigma = 1.4826 * mad.where(mad > 0)
    z_robusto = (d["F"] - mu) / sigma.where(sigma > 1e-12)
    d["canonico"] = (d["z"] >= k) & (d["F"] > 0)
    d["robusto"] = (z_robusto >= k) & (d["F"] > 0)

    canon_mask = d["canonico"]
    robust_mask = d["robusto"]
    canon = d[canon_mask]
    robust = d[robust_mask]
    next_rng = d.groupby("dia", sort=False)["rng_atr"].shift(-1)
    if robust.empty:
        return {"n_brilhante_canonico": int(canon.shape[0]), "n_brilhante_robusto": 0,
                "lift_brilhante_robusto": np.nan, "expansao_brilhante_robusto": np.nan,
                "expansao_brilhante_canonico": float(next_rng[canon_mask].mean()) if not canon.empty else np.nan,
                "dif_expansao": np.nan}

    base = d.groupby("hora")["rng_atr"].transform("mean")
    exp_rob = next_rng[robust_mask].mean()
    exp_can = next_rng[canon_mask].mean() if not canon.empty else np.nan
    lift = (next_rng[robust_mask] / base[robust_mask]).mean()
    return {"n_brilhante_canonico": int(canon.shape[0]), "n_brilhante_robusto": int(robust.shape[0]),
            "lift_brilhante_robusto": float(lift), "expansao_brilhante_robusto": float(exp_rob),
            "expansao_brilhante_canonico": float(exp_can) if np.isfinite(exp_can) else np.nan,
            "dif_expansao": float(abs(exp_rob - exp_can)) if np.isfinite(exp_can) else np.nan}


def medir_h28(canonico, sazonal, limiar=1.5, horizonte=1):
    """Compara o alerta de volatilidade canônico com a versão de volume sazonal."""
    if canonico.empty or sazonal.empty:
        return {"n_canonico": 0, "n_sazonal": 0, "expansao_canonico": np.nan, "expansao_sazonal": np.nan,
                "dif_expansao": np.nan, "cv_hora": np.nan, "veredito": "NÃO SUPORTADA"}

    for nome, d in (("canonico", canonico), ("sazonal", sazonal)):
        d = d.copy()
        if "hora" not in d.columns:
            d["hora"] = d["dt"].dt.hour
        if "dia" not in d.columns:
            d["dia"] = d["dt"].dt.normalize()
        d["alarme"] = d["F"].notna() & (d["z"].abs() >= limiar) & (d["F"] != 0)
        d["rng_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
        d["expansao"] = d.groupby("dia", sort=False)["rng_atr"].shift(-horizonte)
        d["h"] = d["hora"]
        if nome == "canonico":
            canon = d[d["alarme"]].copy()
        else:
            saz = d[d["alarme"]].copy()

    if canon.empty or saz.empty:
        return {"n_canonico": int(len(canon)), "n_sazonal": int(len(saz)), "expansao_canonico": np.nan,
                "expansao_sazonal": np.nan, "dif_expansao": np.nan, "cv_hora": np.nan, "veredito": "NÃO SUPORTADA"}

    exp_c = canon["expansao"].mean()
    exp_s = saz["expansao"].mean()
    dif = abs(exp_s - exp_c)
    cv_c = canon.groupby("hora").size().std(ddof=0) / canon.groupby("hora").size().mean() if not canon.empty else np.nan
    cv_s = saz.groupby("hora").size().std(ddof=0) / saz.groupby("hora").size().mean() if not saz.empty else np.nan
    cv_hora = cv_s / cv_c if np.isfinite(cv_c) and cv_c > 0 else np.nan
    ver = "CONFIRMADA" if np.isfinite(cv_hora) and cv_hora <= 0.80 and np.isfinite(dif) and dif <= 0.03 else "NÃO SUPORTADA"
    return {"n_canonico": int(len(canon)), "n_sazonal": int(len(saz)), "expansao_canonico": float(exp_c),
            "expansao_sazonal": float(exp_s), "dif_expansao": float(dif), "cv_hora": float(cv_hora), "veredito": ver}


def medir_h29(d, limiar_a=2.0, limiar_m=0.3, horizonte=1, minimo=30):
    """Compara a classe de absorção (a ≥ 2 com |m| < 0.3) contra o restante do mercado.

    A hipótese é estritamente descritiva: mede se o evento tem expansão e retorno próprios, sem atribuir
    qualidade operacional ou direção ao padrão.
    """
    if d.empty:
        return {"n_absorcao": 0, "n_controle": 0, "expansao_absorcao": np.nan, "expansao_controle": np.nan,
                "retorno_absorcao": np.nan, "retorno_controle": np.nan, "persistencia": np.nan,
                "t_exp": np.nan, "t_retorno": np.nan, "veredito": "NÃO SUPORTADA"}

    d = d.copy()
    if "hora" not in d.columns:
        d["hora"] = d["dt"].dt.hour
    if "dia" not in d.columns:
        d["dia"] = d["dt"].dt.normalize()
    d["rng_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
    d["cor"] = np.sign(d["c"] - d["o"])
    grupo_dia = d.groupby("dia", sort=False)
    d["retorno"] = d["cor"] * (grupo_dia["c"].shift(-horizonte) - d["o"])
    d["expansao"] = grupo_dia["rng_atr"].shift(-horizonte)
    sel = (d["a"] >= limiar_a) & (d["am"].abs() < limiar_m)
    abs_d = d[sel].copy()
    cont = d[~sel].copy()
    if abs_d.empty or cont.empty:
        return {"n_absorcao": int(sel.sum()), "n_controle": int((~sel).sum()), "expansao_absorcao": np.nan,
                "expansao_controle": np.nan, "retorno_absorcao": np.nan, "retorno_controle": np.nan,
                "persistencia": np.nan, "t_exp": np.nan, "t_retorno": np.nan, "veredito": "NÃO SUPORTADA"}
    if len(abs_d) < minimo:
        return {"n_absorcao": int(len(abs_d)), "n_controle": int(len(cont)), "expansao_absorcao": float(abs_d["expansao"].mean()),
                "expansao_controle": float(cont["expansao"].mean()), "retorno_absorcao": float(abs_d["retorno"].mean()),
                "retorno_controle": float(cont["retorno"].mean()), "persistencia": np.nan, "t_exp": np.nan, "t_retorno": np.nan,
                "veredito": "INCONCLUSIVA"}

    exp_abs = abs_d["expansao"].mean()
    exp_cont = cont["expansao"].mean()
    ret_abs = abs_d["retorno"].mean()
    ret_cont = cont["retorno"].mean()
    lift = exp_abs / exp_cont if exp_cont > 0 else np.nan

    def welch(a, b):
        if len(a) < 2 or len(b) < 2:
            return np.nan
        va, vb = a.var(ddof=1), b.var(ddof=1)
        se = np.sqrt(va / len(a) + vb / len(b))
        return float((a.mean() - b.mean()) / se) if se > 0 else np.nan

    t_exp = welch(abs_d["expansao"].dropna(), cont["expansao"].dropna())
    t_ret = welch(abs_d["retorno"].dropna(), cont["retorno"].dropna())
    ver = "CONFIRMADA" if (np.isfinite(t_exp) and abs(t_exp) >= 3 and np.isfinite(lift) and lift >= 1.5) else (
        "INCONCLUSIVA" if np.isfinite(t_exp) and abs(t_exp) >= 2 else "NÃO SUPORTADA")
    return {"n_absorcao": int(len(abs_d)), "n_controle": int(len(cont)), "expansao_absorcao": float(exp_abs),
            "expansao_controle": float(exp_cont), "retorno_absorcao": float(ret_abs), "retorno_controle": float(ret_cont),
            "persistencia": float(lift), "t_exp": float(t_exp) if np.isfinite(t_exp) else np.nan,
            "t_retorno": float(t_ret) if np.isfinite(t_ret) else np.nan, "veredito": ver}


def medir_h26(dados, minutos=100, min_janelas=2, tolerancia_cor=0.05, tolerancia_persistencia=0.15):
    """Compara frequência e persistência de estados em janelas físicas equivalentes.

    A hipótese é descritiva: mede similaridade de estado em um intervalo fixo de tempo,
    sem deduzir direção, risco ou qualidade operacional do sinal. A comparação global exige
    que as métricas permaneçam dentro das tolerâncias fixadas pelo próprio estudo.
    """
    resultados = {}
    for tf, d in dados.items():
        if isinstance(d, list):
            d = pd.DataFrame(d)
        if d.empty:
            resultados[tf] = {"janelas": 0, "colorido_pct": np.nan, "persistencia": np.nan, "veredito": "NÃO SUPORTADA"}
            continue

        d = d.sort_values("dt").reset_index(drop=True).copy()
        if "est" not in d.columns:
            d["est"] = 0
        if "dt" not in d.columns:
            resultados[tf] = {"janelas": 0, "colorido_pct": np.nan, "persistencia": np.nan, "veredito": "NÃO SUPORTADA"}
            continue

        inicio = d["dt"].min().floor("min")
        fim = d["dt"].max().floor("min")
        janelas = []
        for janela_inicio in pd.date_range(inicio, fim, freq=f"{minutos}min"):
            janela_fim = janela_inicio + pd.Timedelta(minutes=minutos)
            sel = (d["dt"] >= janela_inicio) & (d["dt"] < janela_fim)
            if sel.sum() == 0:
                continue
            janela = d[sel].copy()
            total = len(janela)
            colorido = (janela["est"] != 0).mean()
            estados = janela["est"].to_numpy()
            if total == 0:
                persistencia = np.nan
            else:
                corridas = []
                atual = estados[0]
                n = 1
                for estado in estados[1:]:
                    if estado == atual:
                        n += 1
                    else:
                        corridas.append(n)
                        atual = estado
                        n = 1
                corridas.append(n)
                persistencia = float(np.median(corridas)) / total if total > 0 else np.nan
            janelas.append({"colorido_pct": float(colorido), "persistencia": float(persistencia) if np.isfinite(persistencia) else np.nan})

        if len(janelas) < min_janelas:
            resultados[tf] = {"janelas": len(janelas), "colorido_pct": np.nan, "persistencia": np.nan,
                              "veredito": "INCONCLUSIVA"}
            continue

        coloridos = np.array([j["colorido_pct"] for j in janelas], dtype=float)
        persistencias = np.array([j["persistencia"] for j in janelas if np.isfinite(j["persistencia"])], dtype=float)
        resultado = {"janelas": len(janelas), "colorido_pct": float(coloridos.mean()), "persistencia": float(persistencias.mean()) if persistencias.size else np.nan}
        resultado["veredito"] = "CONFIRMADA" if np.isfinite(resultado["colorido_pct"]) and np.isfinite(resultado["persistencia"]) else "NÃO SUPORTADA"
        resultados[tf] = resultado

    if len(resultados) < 2:
        return resultados
    valores = {k: v for k, v in resultados.items() if np.isfinite(v["colorido_pct"]) and np.isfinite(v["persistencia"])}
    if len(valores) < 2:
        return resultados
    cor = max(v["colorido_pct"] for v in valores.values()) - min(v["colorido_pct"] for v in valores.values())
    pers = max(v["persistencia"] for v in valores.values()) - min(v["persistencia"] for v in valores.values())
    comparavel = cor <= tolerancia_cor and pers <= tolerancia_persistencia
    for tf, v in resultados.items():
        if tf not in valores:
            continue
        v["comparavel"] = comparavel
        v["dif_cor"] = cor
        v["dif_persistencia"] = pers
        if not comparavel:
            v["veredito"] = "INCONCLUSIVA"
    return resultados


def medir_h30(d, percentil=0.80):
    """Compara primeiro sinal de cor e brilho entre dias muito direcionais e os demais."""
    if d.empty:
        return {"n_top": 0, "n_total": 0, "direcao_top": np.nan, "direcao_outros": np.nan,
                "primeira_cor_top": np.nan, "primeira_cor_outros": np.nan, "brilhante_top": np.nan,
                "brilhante_outros": np.nan, "delta_hora": np.nan, "delta_brilhante": np.nan, "t_hora": np.nan,
                "t_brilhante": np.nan, "veredito": "NÃO SUPORTADA"}

    d = d.copy()
    if "dia" not in d.columns:
        d["dia"] = d["dt"].dt.normalize()
    if "hora" not in d.columns:
        d["hora"] = d["dt"].dt.hour

    dia_info = d.groupby("dia").agg(
        o=("o", "first"), c=("c", "last"), h=("h", "max"), l=("l", "min"),
        brilho=("est", lambda s: (s.abs() == 2).mean() if len(s) else np.nan),
    )
    dia_info["direcao"] = (dia_info["c"] - dia_info["o"]).abs() / (dia_info["h"] - dia_info["l"]).clip(lower=1e-9)
    primeira_hora = d[d["est"] != 0].groupby("dia")["hora"].first().rename("primeira_hora")
    dias = dia_info.join(primeira_hora).reset_index()
    dias["top"] = dias["direcao"].ge(dias["direcao"].quantile(percentil))
    if not dias["top"].any():
        return {"n_top": 0, "n_total": len(dias), "direcao_top": np.nan, "direcao_outros": np.nan,
                "primeira_cor_top": np.nan, "primeira_cor_outros": np.nan, "brilhante_top": np.nan,
                "brilhante_outros": np.nan, "delta_hora": np.nan, "delta_brilhante": np.nan,
                "t_hora": np.nan, "t_brilhante": np.nan, "veredito": "NÃO SUPORTADA"}

    top = dias[dias["top"]].copy()
    outros = dias[~dias["top"]].copy()
    primeira_hora = d[d["est"] != 0].groupby("dia")["hora"].first().rename("primeira_hora")
    dias["primeira_hora"] = dias["dia"].map(primeira_hora)
    top = dias[dias["top"]].copy()
    outros = dias[~dias["top"]].copy()
    delta_hora = float(top["primeira_hora"].mean() - outros["primeira_hora"].mean())
    delta_brilhante = float(top["brilho"].mean() - outros["brilho"].mean())

    def welch(a, b):
        va, vb = a.var(ddof=1), b.var(ddof=1)
        se = np.sqrt(va / len(a) + vb / len(b))
        return float((a.mean() - b.mean()) / se) if se > 0 else np.nan

    t_hora = welch(top["primeira_hora"], outros["primeira_hora"]) if len(top) > 1 and len(outros) > 1 else np.nan
    t_brilhante = welch(top["brilho"], outros["brilho"]) if len(top) > 1 and len(outros) > 1 else np.nan
    ver = "CONFIRMADA" if (np.isfinite(t_hora) and abs(t_hora) >= 3) or (np.isfinite(t_brilhante) and abs(t_brilhante) >= 3) else "NÃO SUPORTADA"
    return {"n_top": int(top.shape[0]), "n_total": int(dias.shape[0]), "direcao_top": float(top["direcao"].mean()),
            "direcao_outros": float(outros["direcao"].mean()), "primeira_cor_top": float(top["primeira_hora"].mean()),
            "primeira_cor_outros": float(outros["primeira_hora"].mean()), "brilhante_top": float(top["brilho"].mean()),
            "brilhante_outros": float(outros["brilho"].mean()), "delta_hora": delta_hora,
            "delta_brilhante": delta_brilhante, "t_hora": t_hora, "t_brilhante": t_brilhante, "veredito": ver}


def medir_h39(dados, tfs, limiar=1.5, horizonte=1):
    """Compara eventos de alarme coincidentes e isolados em dois ou mais timeframes."""
    eventos, isolados, coincidentes = [], [], []
    for tf in tfs:
        d = dados[tf].copy()
        d = d.sort_values("dt").reset_index(drop=True)
        if "hora" not in d.columns:
            d["hora"] = d["dt"].dt.hour
        if "dia" not in d.columns:
            d["dia"] = d["dt"].dt.normalize()
        d["alarme"] = d["F"].notna() & (d["z"].abs() >= limiar) & (d["F"] != 0)
        d["sinal"] = np.sign(d["F"])
        d["prio"] = tf
        d["range_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
        d["retorno"] = d["sinal"] * (d["c"].shift(-horizonte) - d["c"])
        d["range_futuro"] = d["rng"].shift(-horizonte) / d["atr"].shift(-horizonte).where(d["atr"].shift(-horizonte) > 0)
        eventos.append(d[d["alarme"]][["dt", "sinal", "range_atr", "range_futuro", "retorno", "prio"]])

    # A entrada experimental usada por H39 pode não conter colunas auxiliares de timestamp.
    if not eventos:
        return {"n_coincidentes": 0, "n_isolados": 0, "range_coincidente": np.nan, "range_isolado": np.nan,
                "retorno_coincidente": np.nan, "retorno_isolado": np.nan, "t_range": np.nan, "t_retorno": np.nan}

    alarmes = pd.concat(eventos, ignore_index=True)
    contagem = alarmes.groupby("dt").size()
    coincidentes = alarmes[alarmes["dt"].isin(contagem[contagem >= 2].index)].drop_duplicates("dt")
    isolados = alarmes[alarmes["dt"].isin(contagem[contagem == 1].index)].drop_duplicates("dt")
    if coincidentes.empty or isolados.empty:
        return {"n_coincidentes": int(len(coincidentes)), "n_isolados": int(len(isolados)),
                "range_coincidente": float(coincidentes["range_futuro"].mean()) if not coincidentes.empty else np.nan,
                "range_isolado": float(isolados["range_futuro"].mean()) if not isolados.empty else np.nan,
                "retorno_coincidente": float(coincidentes["retorno"].mean()) if not coincidentes.empty else np.nan,
                "retorno_isolado": float(isolados["retorno"].mean()) if not isolados.empty else np.nan,
                "t_range": np.nan, "t_retorno": np.nan}

    d_range = coincidentes["range_futuro"].mean() - isolados["range_futuro"].mean()
    d_retorno = coincidentes["retorno"].mean() - isolados["retorno"].mean()
    se_range = np.sqrt(coincidentes["range_futuro"].var(ddof=1) / len(coincidentes) + isolados["range_futuro"].var(ddof=1) / len(isolados))
    se_retorno = np.sqrt(coincidentes["retorno"].var(ddof=1) / len(coincidentes) + isolados["retorno"].var(ddof=1) / len(isolados))
    t_range = float(d_range / se_range) if se_range > 0 else np.nan
    t_retorno = float(d_retorno / se_retorno) if se_retorno > 0 else np.nan
    return {"n_coincidentes": int(len(coincidentes)), "n_isolados": int(len(isolados)),
            "range_coincidente": float(coincidentes["range_futuro"].mean()), "range_isolado": float(isolados["range_futuro"].mean()),
            "retorno_coincidente": float(coincidentes["retorno"].mean()), "retorno_isolado": float(isolados["retorno"].mean()),
            "t_range": t_range, "t_retorno": t_retorno}


def c_pct(r):
    return fm(r["pct"], 1, True) if r else "–"


def c_exp(r):
    return f"{r['exp']:.2f}× ({r['t_exp']:+.1f})" if r else "–"


def c_ret(r, h):
    return f"{fm(r[f'sf{h}'], 1, sinal=True)} ({fm(r[f't{h}'], 1, sinal=True)})" if r else "–"


def c_lift(r):
    return f"{r['lift']:.2f}" if r else "–"


def veredito_h39(metrica):
    """Veredito descritivo para H39: só aceita quando range e retorno satisfazem |t| ≥ 3."""
    if not metrica:
        return "NÃO SUPORTADA"
    t_range = metrica.get("t_range")
    t_retorno = metrica.get("t_retorno")
    if t_range is None or t_retorno is None:
        return "NÃO SUPORTADA"
    if abs(t_range) >= 3 and abs(t_retorno) >= 3:
        return "CONFIRMADA"
    if abs(t_range) >= 2 or abs(t_retorno) >= 2:
        return "INCONCLUSIVA"
    return "NÃO SUPORTADA"


def veredito_h30(metrica):
    """Veredito de H30: exige pelo menos uma diferença com |t| ≥ 3, sem inferir direção."""
    if not metrica:
        return "NÃO SUPORTADA"
    t_hora = metrica.get("t_hora")
    t_brilhante = metrica.get("t_brilhante")
    if t_hora is None and t_brilhante is None:
        return "NÃO SUPORTADA"
    if any(abs(t) >= 3 for t in (t_hora, t_brilhante) if t is not None):
        return "CONFIRMADA"
    if any(abs(t) >= 2 for t in (t_hora, t_brilhante) if t is not None):
        return "INCONCLUSIVA"
    return "NÃO SUPORTADA"


def comparar_vereditos_h32(base, comparacao, ids):
    """Compara os vereditos de H06–H20 entre a amostra base e a amostra de Robustez Temporal."""
    resultados = {tf: {} for tf in base}
    diferencas = {}
    aprovados = 0
    n_dados = 0
    for tf, mapa in base.items():
        for hid in ids:
            atual = mapa.get(hid)
            outro = comparacao.get(tf, {}).get(hid)
            if atual is None or outro is None:
                continue
            n_dados += 1
            if atual == outro:
                aprovados += 1
            else:
                diferencas.setdefault(tf, {})[hid] = (atual, outro)

    if n_dados == 0:
        veredito = "NÃO SUPORTADA"
    elif aprovados == n_dados:
        veredito = "CONFIRMADA"
    elif any(len(v) for v in diferencas.values()):
        veredito = "INCONCLUSIVA"
    else:
        veredito = "NÃO SUPORTADA"

    return {"veredito": veredito, "aprovados": aprovados, "total": n_dados, "diferencas": diferencas, "n_dados": n_dados}


# ----------------------------------------------------------------------------- dados e metricas (com cache)
class Val:
    """Series preparadas (definicao canonica e com volume sazonal) e metricas em cache."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.ctx_s = ctx.derivar(sazonal=SAZONAL)
        self._d, self._ds, self._m = {}, {}, {}

    def d(self, tf):
        if tf not in self._d:
            self._d[tf] = preparar(self.ctx.serie(self.ctx.ativo, tf))
        return self._d[tf]

    def ds(self, tf):
        if tf not in self._ds:
            self._ds[tf] = preparar(self.ctx_s.serie(self.ctx.ativo, tf))
        return self._ds[tf]

    def m(self, nome, tf):
        if (nome, tf) not in self._m:
            self._m[(nome, tf)] = getattr(self, "_m_" + nome)(tf)
        return self._m[(nome, tf)]

    def _m_pareto(self, tf):
        d, k1, k2 = self.d(tf), self.ctx.k1, self.ctx.k2
        x = d["aF"].to_numpy()
        n = len(x)
        desc = np.sort(x)[::-1]
        tot = desc.sum()
        ps = np.linspace(0.80, 0.995, 30)
        xq = np.quantile(x, ps)
        e = d["est"].abs()
        thr = [np.median(d["mu"] + k * d["sd"]) for k in (k1, k2)]
        return dict(
            n=n, p55=(x >= 55).mean(), p70=(x >= FX1).mean(), pct70=(x < FX1).mean(), p85=(x >= FX2).mean(),
            p100=(x >= 100).mean(), forte=((x >= FX1) & (x < FX2)).mean(), q96=np.quantile(x, 0.96),
            top20=desc[: int(n * 0.20)].sum() / tot, top4=desc[: int(n * 0.04)].sum() / tot,
            gini=2 * np.sum(np.arange(1, n + 1) * desc[::-1]) / (n * tot) - (n + 1) / n,
            alpha=hill(x), r2_pw=ajuste(np.log(xq), np.log(1 - ps))[1], r2_ex=ajuste(xq, np.log(1 - ps))[1], curt=d["F"].kurt(),
            thr1=thr[0], thr2=thr[1], pc1=(x < thr[0]).mean(), pc2=(x < thr[1]).mean(),
            col=(e > 0).mean(), esc=(e == 1).mean(), bri=(e == 2).mean(),
        )

    def _m_robo(self, tf):
        """Limiares fixos sob a definicao dos robos V11-V16: media de volume com o candle atual e F limitado a +-100."""
        d = self.d(tf)
        va = d["v"].rolling(20, min_periods=1).mean().clip(lower=1)
        x = (d["m"] * d["v"] / va * 100).clip(-100, 100).abs()
        return dict(p70=(x >= FX1).mean(), forte=((x >= FX1) & (x < FX2)).mean(), p85=(x >= FX2).mean(), teto=(x >= 99.999).mean())

    def _m_hora(self, tf):
        d, ds = self.d(tf), self.ds(tf)
        t = d.assign(f70=d["aF"] >= FX1, col=d["est"] != 0).groupby("hora").agg(
            n=("a", "size"), f70=("f70", "mean"), col=("col", "mean"), a=("a", "mean"), am=("am", "mean"))
        t = t.join(ds.assign(cols=ds["est"] != 0).groupby("hora").agg(cols=("cols", "mean"), a_s=("a", "mean")))
        t["n_dia"] = t["n"] / d["dia"].nunique()
        t["col_dia"] = t["n_dia"] * t["col"]
        mid = t[(t.index >= 9) & (t.index <= 17)]
        cv = {c: mid[c].std(ddof=0) / mid[c].mean() for c in ("f70", "col", "cols")}
        return t, cv

    def _m_dia(self, tf):
        d = self.d(tf)
        g = d.assign(f70=d["aF"] >= FX1, col=d["est"] != 0, bri=d["est"].abs() == 2).groupby("dia").agg(
            f70=("f70", "sum"), col=("col", "sum"), bri=("bri", "sum"), o=("o", "first"), c=("c", "last"), h=("h", "max"), l=("l", "min"))
        amp = (g["h"] - g["l"]).where(lambda s: s > 0)
        dire = (g["c"] - g["o"]).abs() / amp
        rho = lambda a, b: a.rank().corr(b.rank())  # noqa: E731
        return dict(f70=g["f70"].mean(), f70_cv=g["f70"].std() / g["f70"].mean(), col=g["col"].mean(), col_cv=g["col"].std() / g["col"].mean(),
                    bri=g["bri"].mean(), p10=g["col"].quantile(0.10), p90=g["col"].quantile(0.90), dias=len(g),
                    rho_f70_amp=rho(g["f70"], amp), rho_col_amp=rho(g["col"], amp), rho_col_dir=rho(g["col"], dire))

    def _m_dose(self, tf):
        d = self.d(tf)
        zd = d["z"] * np.sign(d["F"])  # z na direcao da cor do candle
        edges = [-np.inf, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, np.inf]
        nomes = ["< 0.5σ", "0.5–1.0σ", "1.0–1.5σ", "1.5–2.0σ", "2.0–2.5σ", "2.5–3.0σ", "3.0–4.0σ", "≥ 4.0σ"]
        return [(n, desfecho(d, (zd >= lo) & (zd < hi))) for n, lo, hi in zip(nomes, edges[:-1], edges[1:])]

    def _m_estados(self, tf):
        d = self.d(tf)
        e = d["est"]
        masks = {"VD": e == 1, "VL": e == 2, "RD": e == -1, "RV": e == -2, "N": e == 0,
                 "escuro": e.abs() == 1, "brilhante": e.abs() == 2, "colorido": e != 0}
        return {k: desfecho(d, m) for k, m in masks.items()}

    def _m_classes(self, tf):
        d = self.d(tf)
        x, e = d["aF"], d["est"].abs()
        qc, qb = (e > 0).mean(), (e == 2).mean()
        tc, tb = x.quantile(1 - qc), x.quantile(1 - qb)
        spec = [
            ("Pareto fixo: forte", f"{FX1:.0f} ≤ \\|F\\| < {FX2:.0f}", (x >= FX1) & (x < FX2)),
            ("Pareto fixo: exaustão", f"\\|F\\| ≥ {FX2:.0f}", x >= FX2),
            ("Pareto fixo: forte + exaustão", f"\\|F\\| ≥ {FX1:.0f}", x >= FX1),
            (CL_PAR, f"\\|F\\| ≥ {tc:.0f} (P{100 * (1 - qc):.0f})", x >= tc),
            ("Pareto equiparado ao brilhante", f"\\|F\\| ≥ {tb:.0f} (P{100 * (1 - qb):.1f})", x >= tb),
            ("Bollinger: escuro", f"{self.ctx.k1}σ ≤ z < {self.ctx.k2}σ", e == 1),
            ("Bollinger: brilhante", f"z ≥ {self.ctx.k2}σ", e == 2),
            (CL_BOLL, f"z ≥ {self.ctx.k1}σ", e > 0),
        ]
        return [(n, c, desfecho(d, m)) for n, c, m in spec]

    def _m_ablacao(self, tf):
        d = self.d(tf)
        q = (d["est"] != 0).mean()
        sinais = [(SIG_F, d["aF"]), (SIG_A, d["a"]), (SIG_M, d["am"]), (SIG_C, d["body_atr"]), (SIG_R, d["rng_atr"])]
        return q, [(n, desfecho(d, s >= s.quantile(1 - q))) for n, s in sinais]

    def _m_bins_a(self, tf):
        d, L = self.d(tf), []
        for lo, hi, nome in A_BINS:
            sel = (d["a"] >= lo) & (d["a"] < hi)
            nx = sel & d["a_next"].notna()
            L.append((nome, desfecho(d, sel), d.loc[sel, "rng_atr"].mean(), d.loc[sel, "body_atr"].mean(), d.loc[sel, "am"].mean(),
                      (d.loc[nx, "a_next"] >= 1.3).mean()))
        return L

    def _m_bins_m(self, tf):
        d, L = self.d(tf), []
        for lo, hi, nome in M_BINS:
            sel = (d["am"] >= lo) & (d["am"] < hi)
            L.append((nome, desfecho(d, sel), d.loc[sel, "rng_atr"].mean(), d.loc[sel, "a"].mean(),
                      d.loc[sel, "w_up"].mean(), d.loc[sel, "w_dn"].mean(), p_mesma_cor(d, sel)))
        return L

    def _m_grade(self, tf):
        d, L = self.d(tf), []
        for alo, ahi, an in A_BINS:
            for mlo, mhi, mn in G_M:
                sel = (d["a"] >= alo) & (d["a"] < ahi) & (d["am"] >= mlo) & (d["am"] < mhi)
                L.append((an, mn, LEITURA.get((an, mn), ""), desfecho(d, sel), (d["est"] != 0)[sel].mean()))
        return L

    def _m_impacto(self, tf):
        d = self.d(tf)
        faixa = pd.qcut(d["a"].clip(lower=1e-3), 20, duplicates="drop")
        g = d.groupby(faixa, observed=True).agg(a=("a", "mean"), y=("body_atr", "median"))
        g = g[(g["a"] > 0) & (g["y"] > 0)]
        beta, r2 = ajuste(np.log(g["a"].to_numpy()), np.log(g["y"].to_numpy()))
        return beta, r2, d["am"].rank().corr(d["a"].rank())

    def _m_acf(self, tf):
        d, ds, lags = self.d(tf), self.ds(tf), (1, 2, 3, 5, 10)
        return lags, {"a (canônico)": [d["a"].autocorr(k) for k in lags], "a (sazonal)": [ds["a"].autocorr(k) for k in lags],
                      "amplitude/ATR": [d["rng_atr"].autocorr(k) for k in lags], "m": [d["m"].autocorr(k) for k in lags],
                      "F": [d["F"].autocorr(k) for k in lags]}

    def _m_gauss(self, tf):
        z = self.d(tf)["z"].abs()
        return [(k, gauss2(k), (z >= k).mean()) for k in (1.0, 1.5, 2.0, 2.5, 3.0)]

    def _m_autoincl(self, tf):
        alt = self.ctx.serie(self.ctx.ativo, tf, incluir_atual=False)
        return (self.d(tf)["est"] != 0).mean(), (alt["est"] != 0).mean()

    def _m_escala(self, tf):
        d = self.d(tf)

        def est(F):
            mu, sd = F.rolling(20).mean(), F.rolling(20).std(ddof=0)
            z = (F - mu) / sd.where(sd > 1e-12)
            return np.select([(z >= 2.5) & (F > 0), (z >= 1.5) & (F > 0), (z <= -2.5) & (F < 0), (z <= -1.5) & (F < 0)], [2, 1, -2, -1], 0)

        return int((est(d["F"]) != est(d["F"] / 100.0)).sum()), len(d)

    def _m_clusters(self, tf):
        d, L = self.d(tf), {}
        for g in (0, 1):
            c = clusters(d, g, True)
            multi = c[c["n"] >= 2]
            L[g] = dict(n=len(c), multi=len(multi) / len(c), por_dia=len(multi) / d["dia"].nunique(),
                        faixa_atr=multi["rng_atr"].median(), faixa_pts=multi["rng"].median(), bri=multi["bright"].mean())
        return L

    def _m_cluster_retorno(self, tf):
        d = self.d(tf)
        return medir_retorno_cluster(d, n=5, controles=40, semente=0)

    def _m_h27(self, tf):
        d = self.d(tf)
        return medir_h27(d, janela=20, k=self.ctx.k2)

    def _m_h28(self, tf):
        return medir_h28(self.d(tf), self.ds(tf), limiar=1.5, horizonte=1)

    def _m_h29(self, tf):
        d = self.d(tf)
        return medir_h29(d, limiar_a=2.0, limiar_m=0.3, horizonte=1, minimo=30)

    def _m_h26(self, tf):
        d = self.d(tf)
        return medir_h26({tf: d}, minutos=100, min_janelas=2)[tf]

    def _m_h30(self, tf):
        d = self.d(tf)
        return medir_h30(d, percentil=0.80)

    def _m_h39(self, tf):
        dados = {t: self.d(t) for t in self.ctx.tf_foco if t in self.ctx.tfs}
        return medir_h39(dados, tfs=self.ctx.tf_foco, limiar=1.5, horizonte=1)

    def _m_transicoes(self, tf):
        d = self.d(tf)
        if d.empty:
            return {}
        fam = d["fam"].to_numpy()
        dt = d["dt"].to_numpy()
        delta = np.diff(dt, prepend=dt[0]).astype("timedelta64[m]").astype(float)
        gap_data = delta[1:] > TF_ORD[tf] * 1.5
        out, last = [], None
        for i, f in enumerate(fam):
            if f == 0:
                continue
            if last is None:
                last = (i, f)
                continue
            prev_i, prev_f = last
            neutral = i - prev_i - 1
            dt_min = (dt[i] - dt[prev_i]) / np.timedelta64(1, "m")
            out.append({"prev": prev_f, "next": f, "neutral": neutral, "espaco_min": float(dt_min), "mudou_familia": prev_f != f})
            last = (i, f)
        if not out:
            return {"transicoes": 0, "familias": {}, "neutros": [], "gap_data": 0.0}
        trans = pd.DataFrame(out)
        fam_stats = (trans.groupby(["prev", "next"]).agg(n=("neutral", "size"), neutros=("neutral", "mean"),
                     tempo=("espaco_min", "mean"), gaps=("mudou_familia", "mean"))
                     .sort_values(["n", "neutros"], ascending=False))
        return {"transicoes": len(trans), "familias": fam_stats.to_dict("index"),
                "neutros": trans["neutral"].describe(percentiles=[0.5, 0.9, 0.95, 0.99]).to_dict(),
                "gap_data": float(gap_data.mean()) if len(gap_data) else 0.0,
                "gap_duracao": float(np.median(delta[1:][gap_data])) if np.any(gap_data) else 0.0}


# ----------------------------------------------------------------------------- blocos do documento de validacao
def bloco_v1_pareto(v):
    tfs = [t for t in TFS_VAL if t in v.ctx.tfs]
    P = {tf: v.m("pareto", tf) for tf in tfs}
    A = [[tf, fm(p["p55"], 1, True), f"{fm(p['p70'], 1, True)} (P{p['pct70'] * 100:.0f})", fm(p["forte"], 1, True), fm(p["p85"], 1, True),
          fm(p["p100"], 1, True), f"{p['p85'] / p['forte']:.1f}×"] for tf, p in P.items()]
    B = [[tf, fm(p["top20"], 1, True), fm(p["top4"], 1, True), fm(p["gini"], 2), fm(p["alpha"], 2), fm(p["r2_pw"], 3), fm(p["r2_ex"], 3),
          fm(p["curt"], 0)] for tf, p in P.items()]
    R = [[tf, fm(r["p70"], 1, True), fm(r["forte"], 1, True), fm(r["p85"], 1, True), fm(r["teto"], 1, True), f"{r['p85'] / r['forte']:.1f}×"]
         for tf, r in ((t, v.m("robo", t)) for t in tfs)]
    C = [[tf, f"{p['thr1']:.0f} (P{p['pc1'] * 100:.0f})", f"{p['thr2']:.0f} (P{p['pc2'] * 100:.0f})", f"{p['q96']:.0f}", fm(p["col"], 1, True),
          fm(p["esc"], 1, True), fm(p["bri"], 2, True), f"{p['esc'] / p['bri']:.1f}×"] for tf, p in P.items()]
    partes = [cabecalho_bloco(v.ctx) + f"_Dias com cobertura < {v.ctx.cobertura:.0%} das barras esperadas foram descartados (contratos ilíquidos / pregões curtos)._\n",
              f"**A. Limiares fixos (70/85) dentro da distribuição de \\|F\\| — {v.ctx.ativo}**\n\n"
              + tabela(["TF", "\\|F\\|≥55", "\\|F\\|≥70 (percentil de 70)", "faixa 70–85 (\"forte\")", "\\|F\\|≥85 (\"exaustão\")", "\\|F\\|≥100", "exaustão ÷ forte"], A),
              f"\n**A2. Os mesmos limiares na definição usada pelos robôs — {v.ctx.ativo}** (média de volume com o candle atual e F limitado a ±100)\n\n"
              + tabela(["TF", "\\|F\\|≥70", "faixa 70–85", "\\|F\\|≥85", "no teto (\\|F\\| = 100)", "exaustão ÷ forte"], R),
              "\n**B. Concentração (Pareto) e cauda de \\|F\\|**\n\n"
              + tabela(["TF", "top 20% dos candles → % de Σ\\|F\\|", "top 4% → % de Σ\\|F\\|", "Gini", "α de Hill (top 5%)", "R² cauda log-log (Pareto)",
                        "R² cauda semilog (exponencial)", "curtose(F)"], B),
              "\n**C. Limiares de Bollinger (mediana de μ±kσ) traduzidos para a escala de \\|F\\|**\n\n"
              + tabela(["TF", f"μ+{v.ctx.k1}σ (percentil)", f"μ+{v.ctx.k2}σ (percentil)", "P96 de \\|F\\| (topo 4%)", "colorido", "escuro", "brilhante", "escuro ÷ brilhante"], C)]
    for tf in v.ctx.tf_foco:
        G = [[f"{k:.1f}σ", fm(g, 2, True), fm(m, 2, True), f"{m / g:.1f}×"] for k, g, m in v.m("gauss", tf)]
        a0, a1 = v.m("autoincl", tf)
        partes.append(f"\n**D.{tf}. Bollinger sobre F: realidade × curva normal — {v.ctx.ativo} {tf}**\n\n"
                      + tabela(["k", "normal P(\\|z\\|≥k)", "medido P(\\|z\\|≥k)", "medido ÷ normal"], G)
                      + f"\n\nAuto-inclusão: com o candle atual dentro de μ/σ, {fm(a0, 1, True)} dos candles ficam coloridos; "
                        f"excluindo-o da janela, {fm(a1, 1, True)} (diferença = extremos mascarados pelo próprio candle).")
    return "\n".join(partes)


def bloco_v1_comparacao(v):
    partes = [cabecalho_bloco(v.ctx), "_\"Equiparado\" = limiar fixo global calibrado para selecionar a mesma fração de candles que a classe de Bollinger "
              "(comparação justa: mesma frequência). Expansão = range do próximo candle ÷ ATR, dividido pela média da mesma hora (1.00 = normal); "
              "persistência = lift da própria classe no candle seguinte, ajustado por hora; retornos em pts alinhados à cor do candle (t entre parênteses)._"]
    for tf in v.ctx.tf_foco:
        L = [[n, c, c_pct(r), c_exp(r), c_lift(r), c_ret(r, 1), c_ret(r, 3)] for n, c, r in v.m("classes", tf)]
        partes.append(f"\n**{v.ctx.ativo} {tf}**\n\n" + tabela(["classe", "critério", "% candles", "expansão do range seguinte", "persistência (lift)", "μ h1", "μ h3"], L, "llrrrrr"))
    return "\n".join(partes)


def bloco_v1_hora(v):
    partes = [cabecalho_bloco(v.ctx)]
    D = []
    for tf in v.ctx.tf_foco:
        t, cv = v.m("hora", tf)
        L = [[f"{h:02d}h", f"{r['n_dia']:.1f}", fm(r["f70"], 1, True), fm(r["col"], 1, True), fm(r["col_dia"], 2), fm(r["cols"], 1, True), fm(r["a"], 2),
              fm(r["a_s"], 2), fm(r["am"], 2)] for h, r in t.iterrows()]
        L.append(["**CV 9h–17h**", "", f"**{cv['f70']:.2f}**", f"**{cv['col']:.2f}**", "", f"**{cv['cols']:.2f}**", "", "", ""])
        partes.append(f"\n**Densidade de cor por hora — {v.ctx.ativo} {tf}** (CV = desvio ÷ média entre as horas; menor = mais uniforme)\n\n"
                      + tabela(["hora", "candles/dia", "\\|F\\|≥70 (fixo)", "colorido (Bollinger)", "coloridos/dia (Bollinger)", "colorido (Bollinger + a sazonal)",
                                "a médio", "a sazonal médio", "\\|m\\| médio"], L))
        r = v.m("dia", tf)
        D.append([tf, fm(r["f70"], 1), fm(r["f70_cv"], 2), fm(r["rho_f70_amp"], 2, sinal=True), fm(r["col"], 1), fm(r["col_cv"], 2),
                  fm(r["rho_col_amp"], 2, sinal=True), fm(r["rho_col_dir"], 2, sinal=True)])
    partes.append(f"\n**Densidade de cor por dia — {v.ctx.ativo}** (ρ = correlação de postos entre a contagem diária e a amplitude máx−mín do dia / o quanto o dia foi direcional)\n\n"
                  + tabela(["TF", "\\|F\\|≥70 por dia (fixo)", "CV diário", "ρ com amplitude", "coloridos por dia (Bollinger)", "CV diário", "ρ com amplitude",
                            "ρ com \\|C−O\\|/amplitude"], D))
    return "\n".join(partes)


def bloco_v2_candle(v):
    partes = [cabecalho_bloco(v.ctx)]
    for tf in v.ctx.tf_foco:
        L = [[n, c_pct(r), fm(rg, 2), fm(a, 2), fm(wu, 2), fm(wd, 2), fm(pm, 1, True), c_exp(r), c_ret(r, 1)]
             for n, r, rg, a, wu, wd, pm in v.m("bins_m", tf)]
        d = v.d(tf)
        t, _ = v.m("hora", tf)
        _, acf = v.m("acf", tf)
        partes.append(f"\n**Faixas de \\|m\\| (corpo ÷ range) — {v.ctx.ativo} {tf}**\n\n"
                      + tabela(["\\|m\\|", "% candles", "range/ATR", "a médio", "pavio sup.", "pavio inf.", "P(mesma cor no próximo)", "range seguinte", "μ h1 alinhado"], L)
                      + f"\n\nEstacionariedade: \\|m\\| médio por hora varia só de {t['am'].min():.2f} a {t['am'].max():.2f} (m não tem sazonalidade intradiária); "
                        f"autocorrelação de m: lag1 {acf['m'][0]:+.3f}, lag2 {acf['m'][1]:+.3f}, lag3 {acf['m'][2]:+.3f}; "
                        f"P(mesma cor) geral = {fm(p_mesma_cor(d, d['cor'] == d['cor']), 1, True)}.")
    return "\n".join(partes)


def bloco_v3_volume(v):
    partes = [cabecalho_bloco(v.ctx)]
    for tf in v.ctx.tf_foco:
        L = [[n, c_pct(r), fm(rg, 2), fm(b, 2), fm(am, 2), c_exp(r), fm(pa, 1, True)] for n, r, rg, b, am, pa in v.m("bins_a", tf)]
        lags, acf = v.m("acf", tf)
        A = [[k, *[f"{x:+.2f}" for x in vals]] for k, vals in acf.items()]
        t, _ = v.m("hora", tf)
        partes.append(f"\n**Faixas de a (volume ÷ média dos 20 candles anteriores) — {v.ctx.ativo} {tf}**\n\n"
                      + tabela(["a", "% candles", "range/ATR (mesmo candle)", "corpo/ATR (mesmo candle)", "\\|m\\| médio", "range seguinte", "P(a seguinte ≥ 1.3)"], L)
                      + f"\n\n**Autocorrelação (persistência) — {v.ctx.ativo} {tf}**\n\n" + tabela(["série", *[f"lag {k}" for k in lags]], A)
                      + f"\n\nSazonalidade: a médio vai de {t['a'].min():.2f} (hora mais fraca) a {t['a'].max():.2f} (abertura); "
                        f"com o perfil sazonal removido, a médio por hora varia só de {t['a_s'].min():.2f} a {t['a_s'].max():.2f}.")
    return "\n".join(partes)


def bloco_v4_cruzamento(v):
    partes = [cabecalho_bloco(v.ctx)]
    for tf in v.ctx.tf_foco:
        beta, r2, rho = v.m("impacto", tf)
        G = [[an, mn, ln, c_pct(r), c_exp(r), c_lift(r), c_ret(r, 1), c_ret(r, 3), fm(cb, 0, True)] for an, mn, ln, r, cb in v.m("grade", tf)]
        q, ab = v.m("ablacao", tf)
        S = [[n, c_pct(r), c_exp(r), c_lift(r), c_ret(r, 1), c_ret(r, 3)] for n, r in ab]
        partes.append(f"\n**{v.ctx.ativo} {tf}**\n\nLei de impacto: corpo/ATR (mediana por faixa de a) ∝ a^β com β = {beta:.2f} (R² = {r2:.2f}); "
                      f"referências: raiz quadrada = 0.50, linear = 1.00. Correlação de postos entre \\|m\\| e a: ρ = {rho:+.2f}.\n\n"
                      f"*Grade a × \\|m\\|* (a = esforço, \\|m\\| = eficiência do candle)\n\n"
                      + tabela(["a", "\\|m\\|", "leitura", "% candles", "range seguinte", "persistência (lift)", "μ h1", "μ h3", "% colorido"], G, "lllrrrrrr")
                      + f"\n\n*Ablação a frequência igual* (cada sinal seleciona os {fm(q, 1, True)} candles mais intensos; direção = cor do candle)\n\n"
                      + tabela(["sinal", "% selecionado", "range seguinte", "persistência (lift)", "μ h1", "μ h3"], S))
    return "\n".join(partes)


def bloco_v5_sinais(v):
    partes = [cabecalho_bloco(v.ctx), "_Retornos em pts alinhados à cor do candle (positivo = o preço continuou na direção da cor); t entre parênteses. "
              "P(continua) = fração de h1 > 0 ignorando zeros._"]
    for tf in v.ctx.tf_foco:
        E = v.m("estados", tf)
        L = [[k, E[k]["n"], c_pct(E[k]), c_exp(E[k]), c_lift(E[k]), fm(E[k]["pc"], 1, True), c_ret(E[k], 1), c_ret(E[k], 3)]
             for k in ("VD", "VL", "RD", "RV", "N", "escuro", "brilhante", "colorido") if E[k]]
        D = [[n, c_pct(r), c_exp(r), c_lift(r), c_ret(r, 1)] for n, r in v.m("dose", tf)]
        partes.append(f"\n**{v.ctx.ativo} {tf} — por estado**\n\n" + tabela(["estado", "n", "% candles", "range seguinte", "persistência (lift)", "P(continua) h1", "μ h1", "μ h3"], L)
                      + f"\n\n**{v.ctx.ativo} {tf} — dose-resposta** (z do candle na direção da cor; cada linha é uma faixa de intensidade)\n\n"
                      + tabela(["z na direção da cor", "% candles", "range seguinte", "persistência (lift da faixa)", "μ h1"], D)
                      + "\n\n_Faixa ≥ 4σ: com janela de 20 candles incluindo o próprio candle, z não passa de √19 ≈ 4.36 e o evento infla σ das 19 barras seguintes; "
                        "por isso a persistência dessa faixa é ~0 (artefato do cálculo)._")
    return "\n".join(partes)


def clusters_dia(x, g=1):
    fam, est = x["fam"].to_numpy(), x["est"].to_numpy()
    res, cur = [], None
    for i, f in enumerate(fam):
        if f == 0:
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
    L = []
    for r in res:
        s = x.iloc[r["first"]: r["last"] + 1]
        if r["n"] >= 2:
            L.append([f"{s['dt'].iloc[0]:%H:%M}–{s['dt'].iloc[-1]:%H:%M}", "verde" if r["f"] > 0 else "vermelho", r["n"], f"{s['l'].min():.0f}", f"{s['h'].max():.0f}",
                      f"{s['h'].max() - s['l'].min():.0f}", "sim" if r["bri"] else "não"])
    return L


def _janela_contigua(d, inicio, fim, passo):
    """True if a candidate window stays in one session and has no missing bars."""
    janela = d.iloc[inicio:fim + 1]
    if janela.empty or janela["dt"].dt.normalize().nunique() != 1:
        return False
    if len(janela) > 1:
        deltas = janela["dt"].diff().dropna()
        if not (deltas == passo).all():
            return False
    return True


def _retorno_borda(d, inicio, fim, n, passo=None):
    """Retorno a uma das bordas em até n candles completos após o cluster."""
    janela = d.iloc[inicio:fim + 1]
    alvo = d.iloc[fim + 1:fim + 1 + n]
    if janela.empty or len(alvo) != n:
        return np.nan
    if passo is not None and not _janela_contigua(d, inicio, fim + n, passo):
        return np.nan
    baixo, alto = janela["l"].min(), janela["h"].max()
    return bool(((alvo["h"] >= alto) | (alvo["l"] <= baixo)).any())


def medir_retorno_cluster(d, n=5, controles=40, semente=None):
    """Retorno às bordas versus controles aleatórios válidos do mesmo horário e largura.

    Controles são amostrados por posição da série completa (não por índice da série filtrada),
    e janelas que cruzam sessão ou têm barras ausentes são descartadas.
    """
    vazio = {"n_clusters": 0, "n_posterior": 0, "p_retorno": np.nan, "p_controle": np.nan,
             "t": np.nan, "tamanho_mediano": np.nan}
    if d.empty or n <= 0 or controles <= 0:
        return vazio
    d = d.sort_values("dt").reset_index(drop=True).copy()
    if "hora" not in d.columns:
        d["hora"] = d["dt"].dt.hour

    diffs = d["dt"].diff().dropna()
    curtas = diffs[diffs < pd.Timedelta(hours=1)]
    if curtas.empty:
        return vazio
    passo = curtas.mode().iloc[0]
    rng = np.random.default_rng(semente)
    eventos, controles_linha, tamanhos = [], [], []
    fam = d["fam"].to_numpy()
    dia = d["dt"].dt.normalize().to_numpy()
    inicio = None
    candidatos = []
    for i, f in enumerate(fam):
        quebra = i > 0 and (dia[i] != dia[i - 1] or d.loc[i, "dt"] - d.loc[i - 1, "dt"] != passo)
        if quebra or f == 0:
            if inicio is not None and i - inicio >= 2:
                candidatos.append((inicio, i - 1))
            inicio = None
        if f != 0 and inicio is None:
            inicio = i
    if inicio is not None and len(d) - inicio >= 2:
        candidatos.append((inicio, len(d) - 1))

    for ini, fim in candidatos:
        observado = _retorno_borda(d, ini, fim, n, passo)
        if pd.isna(observado):
            continue
        hora = d.loc[ini, "hora"]
        span = fim - ini
        posibles = []
        for c_ini in range(len(d) - span - n):
            c_fim = c_ini + span
            limite = c_fim + n
            if d.loc[c_ini, "hora"] != hora or d.loc[limite, "hora"] != hora:
                continue
            if not _janela_contigua(d, c_ini, limite, passo):
                continue
            if c_ini <= fim + n and limite >= ini:
                continue
            posibles.append(c_ini)
        if not posibles:
            continue
        amostras = rng.choice(posibles, size=min(controles, len(posibles)), replace=False)
        control_values = [_retorno_borda(d, c_ini, c_ini + span, n, passo) for c_ini in amostras]
        control_values = [float(x) for x in control_values if not pd.isna(x)]
        if not control_values:
            continue
        eventos.append(float(observado))
        controles_linha.append(float(np.mean(control_values)))
        tamanhos.append(fim - ini + 1)

    if len(eventos) < 2:
        return {**vazio, "n_clusters": len(eventos), "n_posterior": len(controles_linha)}
    diffs_pareados = np.asarray(eventos) - np.asarray(controles_linha)
    return {"n_clusters": len(eventos), "n_posterior": len(controles_linha),
            "p_retorno": float(np.mean(eventos)), "p_controle": float(np.mean(controles_linha)),
            "t": float(tstat(pd.Series(diffs_pareados))), "tamanho_mediano": float(np.median(tamanhos))}


def fita(x):
    """Uma linha por hora; cada candle vira um quadrado/circulo colorido."""
    return "\n".join(f"{h:02d}h  " + "".join(SIMBOLO[int(e)] for e in g["est"]) for h, g in x.groupby("hora"))


def mapa_dia(d, dia, media_col=None, d_saz=None):
    x = d[d["dia"] == pd.Timestamp(dia)].reset_index(drop=True)
    if x.empty:
        return f"(sem candles em {dia})"
    nc = int((x["est"] != 0).sum())
    cl = clusters_dia(x)
    tab = tabela(["janela", "cor", "candles coloridos", "mínima", "máxima", "amplitude (pts)", "tem brilhante"], cl, "llrrrrl") if cl else "_Sem clusters de ≥ 2 candles coloridos._"
    ref = f" (média do período: {media_col:.1f})" if media_col else ""
    txt = (f"**{pd.Timestamp(dia):%d/%m/%Y}** · {x['simbolo'].iloc[0]} · abertura {x['o'].iloc[0]:.0f} · máx {x['h'].max():.0f} · mín {x['l'].min():.0f} · "
           f"fechamento {x['c'].iloc[-1]:.0f} · amplitude {x['h'].max() - x['l'].min():.0f} pts · candles coloridos: {nc}{ref}\n\n```text\n{fita(x)}\n```\n")
    if d_saz is not None:
        xs = d_saz[d_saz["dia"] == pd.Timestamp(dia)]
        if not xs.empty:
            txt += f"\nMesmo pregão com o volume sem sazonalidade (coloridos: {int((xs['est'] != 0).sum())})\n\n```text\n{fita(xs)}\n```\n"
    return txt + f"\nClusters (≥ 2 candles da mesma cor, tolerando 1 neutro)\n\n{tab}"


def bloco_v6_cor_dia(v):
    tf = v.ctx.tf_foco[0]
    d, r = v.d(tf), v.m("dia", tf)
    B = []
    for t in v.ctx.tf_foco:
        x, q = v.d(t), v.m("dia", t)
        B.append([t, f"{len(x) / q['dias']:.0f}", f"{q['col']:.1f} ({q['p10']:.0f}–{q['p90']:.0f})", f"{q['bri']:.1f}", fm((x["est"] != 0).mean(), 1, True),
                  fm((x["est"].abs() == 2).mean(), 2, True)])
    tam = d.groupby("dia").size()
    cheios = tam[tam >= 0.98 * esperado_barras(tf)].index
    g = d[d["dia"].isin(cheios[-121:-1])].groupby("dia").agg(o=("o", "first"), c=("c", "last"), h=("h", "max"), l=("l", "min"))
    direcional = ((g["c"] - g["o"]).abs() / (g["h"] - g["l"])).idxmax()
    legenda = " · ".join(f"{SIMBOLO[k]} {n}" for k, n in [(1, "verde escuro (VD)"), (2, "verde vivo (VL)"), (-1, "vermelho escuro (RD)"), (-2, "vermelho vivo (RV)"), (0, "neutro (N)")])
    ds = v.ds(tf)
    return (cabecalho_bloco(v.ctx) + "\n**Orçamento de cores por dia (o que o operador precisa ler)** — coloridos/dia mostra média e faixa p10–p90\n\n"
            + tabela(["TF", "candles/dia", "coloridos/dia", "brilhantes/dia", "% colorido", "% brilhante"], B)
            + f"\n\nLegenda dos mapas: {legenda} · cada linha = 1 hora · {v.ctx.ativo} {tf}\n\n**Pregão completo mais recente**\n\n"
            + mapa_dia(d, cheios[-1], r["col"], ds)
            + "\n\n**Pregão mais direcional dos 120 anteriores (maior |fechamento − abertura| ÷ amplitude)**\n\n" + mapa_dia(d, direcional, r["col"], ds))


def bloco_v7_clusters(v):
    L = []
    for tf in v.ctx.tf_foco:
        for g, r in v.m("clusters", tf).items():
            L.append([tf if g == 0 else "", g, r["n"], fm(r["multi"], 1, True), fm(r["por_dia"], 2), fm(r["faixa_pts"], 0), fm(r["faixa_atr"], 2), fm(r["bri"], 1, True)])
    return (cabecalho_bloco(v.ctx) + "\n**Candidatos a \"área\" (cluster com ≥ 2 candles de mesma cor) — insumo da próxima teoria**\n\n"
            + tabela(["TF", "tolerância (neutros)", "clusters", "% com ≥ 2 candles", "áreas por dia", "amplitude mediana (pts)", "amplitude mediana (ATR)", "com brilhante"], L))


def bloco_v8_transicoes(v):
    linhas = []
    for tf in v.ctx.tf_foco:
        m = v.m("transicoes", tf)
        neutros = m["neutros"]
        linhas.append([tf, m["transicoes"], f"{neutros['mean']:.2f} ({neutros['50%']:.2f} mediana; P90 {neutros['90%']:.2f})",
                       f"{m['gap_data']:.1%} (mediana {m['gap_duracao']:.0f} min)",
                       f"{m['familias'].get((1, -1), {}).get('n', 0)} · {m['familias'].get((-1, 1), {}).get('n', 0)}",
                       f"{m['familias'].get((1, 1), {}).get('n', 0)} · {m['familias'].get((-1, -1), {}).get('n', 0)}"])
    return (cabecalho_bloco(v.ctx) + "\n**Transições entre famílias de cor e gaps de barras intraday — descrição do motor, não aplicação operacional**\n\n"
            + "A transição registra o último candle não neutro antes e o primeiro depois de uma sequência de neutros. A contagem de neutros é a quantidade de barras entre os dois extremos; uma barra ausente é indicada pelo aumento de intervalo entre timestamps, mas não é identificado como market gap. A sequência pode significar absorção, atraso, indecisão ou transição de regime, mas não implica causalidade nem direção.\n\n"
            + tabela(["TF", "transições", "neutros entre famílias", "barras com gap ≥ 1.5×", "verde → vermelho / vermelho → verde", "verde → verde / vermelho → vermelho"], linhas)
            + "\n\n_Gap de dados = barra ausente ou intervalo maior que o nominal; price gap = salto de preço entre candles, que exige outra análise e não é inferido apenas pelo timestamp. Os valores acima não medem reversão, nem recomendam entrada, SL ou SG._")


def bloco_v9_cluster_retorno(v):
    linhas = []
    for tf in v.ctx.tf_foco:
        m = v.m("cluster_retorno", tf)
        linhas.append([tf, m["n_clusters"], f"{m['p_retorno']:.1%}", f"{m['p_controle']:.1%}", f"{m['t']:+.2f}", f"{m['tamanho_mediano']:.0f}"])
    return (cabecalho_bloco(v.ctx) + "\n**H31 — retorno às bordas dos clusters versus controle aleatório — descrição do motor, não aplicação operacional**\n\n"
            + "Um cluster é uma sequência de ±1 família com tolerância de um neutro; a fronteira é o intervalo entre a mínima do cluster e a máxima. O evento ocorre se um dos preços até cinco candles posteriores tocar a fronteira; o controle usa uma janela aleatória do mesmo horário e largura, sem sobreposição. A comparação mede diferença de proporção, não direção ou reversão.\n\n"
            + tabela(["TF", "clusters", "P(retorno) observado", "P(retorno) controle", "t de diferença", "tamanho mediano (candles)"], linhas)
            + "\n\n_A regra de decisão permanece: confirmar apenas se P(retorno) > controle e |t| ≥ 3; rejeição e rompimento ficam como estudos posteriores, sem inferência de entrada, SL ou SG._")


def bloco_v10_h27(v):
    linhas = []
    for tf in v.ctx.tf_foco:
        m = v.m("h27", tf)
        linhas.append([tf, m["n_brilhante_canonico"], m["n_brilhante_robusto"], f"{m['lift_brilhante_robusto']:.2f}",
                       f"{m['expansao_brilhante_robusto']:.2f}", f"{m['expansao_brilhante_canonico']:.2f}", f"{m['dif_expansao']:.2f}"])
    return (cabecalho_bloco(v.ctx) + "\n**H27 — classe brilhante com σ robusto (MAD) e μ/σ sem o candle atual**\n\n"
            + "O cálculo robusto usa a média e o MAD das 20 barras anteriores; o candle atual é removido da referência. A comparação mede frequência, lift do próximo candle e expansão do range relativo ao ATR, sem inferir direção ou operação.\n\n"
            + tabela(["TF", "brilhantes canônicos", "brilhantes robustos", "lift robusto", "expansão robusta", "expansão canônica", "|Δ expansão|"], linhas)
            + "\n\n_Regra: confirmar se o brilho robusto mantém ou aumenta o alerta de atividade sem perda de expansão; o critério pendente é lift ≥ 1.0 e diferença de expansão ≤ 0.03×._")


def bloco_v11_h28(v):
    linhas = []
    for tf in v.ctx.tf_foco:
        m = v.m("h28", tf)
        linhas.append([tf, m["n_canonico"], m["n_sazonal"], f"{m['expansao_canonico']:.2f}", f"{m['expansao_sazonal']:.2f}",
                       f"{m['dif_expansao']:.2f}", f"{m['cv_hora']:.2f}", m["veredito"]])
    return (cabecalho_bloco(v.ctx) + "\n**H28 — volume sazonal substitui o volume canônico sem perder o alerta de volatilidade**\n\n"
            + "A definição canônica usa a média de volume das 20 barras anteriores; a versão sazonal usa o perfil intradiário de 20 dias e remove o componente horário. A comparação mede a expansão seguinte do range e a dispersão horária dos eventos, sem atribuir direção ou qualidade operacional.\n\n"
            + tabela(["TF", "eventos canônicos", "eventos sazonais", "expansão canônica", "expansão sazonal", "|Δ expansão|", "CV horário relativo", "veredito"], linhas)
            + "\n\n_Regra: aceitar a hipótese somente se a expansão do range seguinte for preservada dentro de 0.03× e a dispersão horária da versão sazonal cair pelo menos 20% em relação à canônica. Nenhum desses números define entrada, SL ou SG._")


def bloco_v11_h30(v):
    linhas = []
    for tf in v.ctx.tf_foco:
        m = v.m("h30", tf)
        linhas.append([tf, m["n_top"], m["n_total"], f"{m['direcao_top']:.3f}", f"{m['direcao_outros']:.3f}",
                       f"{m['primeira_cor_top']:.2f} h", f"{m['primeira_cor_outros']:.2f} h",
                       f"{m['brilhante_top']:.2%}", f"{m['brilhante_outros']:.2%}", f"{m['delta_hora']:+.2f} h",
                       f"{m['delta_brilhante']:+.2%}", f"{m['t_hora']:+.2f}", f"{m['t_brilhante']:+.2f}"])
    return (cabecalho_bloco(v.ctx) + "\n**H30 — distribuição de cores em dias muito direcionais**\n\n"
            + "Um dia entra no grupo top quando \\|C−O\\|/amplitude está no percentil 80, com a primeira cor definida pelo primeiro candle colorido do pregão. A comparação mede hora da primeira cor e proporção de brilhantes, sem atribuir direção do movimento nem qualidade operacional aos padrões.\n\n"
            + tabela(["TF", "dias top", "dias totais", "direção média top", "direção média outros", "1ª cor top", "1ª cor outros",
                      "% brilhante top", "% brilhante outros", "Δ hora", "Δ brilho", "t hora", "t brilho"], linhas)
            + "\n\n_Regra: a hipótese é apoiada por uma diferença de hora ou de brilho com |t| ≥ 3 em sentido consistente; sem esse limite, o resultado permanece inconclusivo. Nenhuma conclusão sobre tendência, reversão, entrada, SL ou SG pode ser tirada destes números._")


def bloco_v12_h29(v):
    linhas = []
    for tf in v.ctx.tf_foco:
        m = v.m("h29", tf)
        linhas.append([tf, m["n_absorcao"], m["n_controle"], f"{m['expansao_absorcao']:.2f}", f"{m['expansao_controle']:.2f}",
                       f"{m['persistencia']:.2f}", f"{m['t_exp']:+.2f}", f"{m['t_retorno']:+.2f}"])
    return (cabecalho_bloco(v.ctx) + "\n**H29 — absorção como evento de atividade e persistência**\n\n"
            + "A absorção é definida como a ≥ 2 e \\|m\\| < 0.3. O teste compara a expansão do range seguinte e a persistência do evento contra o restante do mercado, sem atribuir direção ou recomendação operacional.\n\n"
            + tabela(["TF", "absortivos", "controle", "range/ATR absorção", "range/ATR controle", "persistência", "t expansão", "t retorno"], linhas)
            + "\n\n_Regra: confirmar a hipótese se range/ATR absorção > controle, persistência ≥ 1.50 e |t_exp| ≥ 3; não usar t_retorno como prova de direção. O retorno médio pode ser menor que o controle sem invalidar o comportamento de atividade._")


def bloco_v12_h39(v):
    m = v.m("h39", v.ctx.tf_foco[0])
    linha = [", ".join(v.ctx.tf_foco), m["n_coincidentes"], m["n_isolados"], f"{m['range_coincidente']:.2f}", f"{m['range_isolado']:.2f}",
             f"{m['retorno_coincidente']:.2f}", f"{m['retorno_isolado']:.2f}", f"{m['t_range']:+.2f}", f"{m['t_retorno']:+.2f}"]
    return (cabecalho_bloco(v.ctx) + "\n**H39 — alarmes coincidentes entre timeframes**\n\n"
            + "Um alarme ocorre quando |z| ≥ 1.5 e F tem sinal não nulo. Eventos coincidentes são alarmes em dois ou mais timeframes no mesmo timestamp; eventos isolados aparecem em somente um timeframe. O resultado abaixo compara o conjunto inteiro de eventos, sem inferir direção nem qualidade operacional.\n\n"
            + tabela(["timeframes", "eventos coincidentes", "eventos isolados", "range/ATR coincidente", "range/ATR isolado", "retorno coincidente", "retorno isolado", "t range", "t retorno"], [linha])
            + "\n\n_Regra: aceitar a hipótese somente se os eventos coincidentes tiverem maior range/ATR e retorno alinhado com |t| ≥ 3 em pelo menos um ajuste; o número de alarmes não prova direção, risco ou qualidade._")


# ----------------------------------------------------------------------------- hipoteses com veredito automatico
def veredito(ts, esperado):
    """Regra de significancia: |t| >= 3 confirma/refuta; 2 <= |t| < 3 em algum teste = inconclusiva; resto = nao suportada."""
    ts = [t for t in ts if t == t]
    if not ts:
        return "SEM DADOS"
    if all(t * esperado >= 3 for t in ts):
        return "CONFIRMADA"
    if all(t * esperado <= -3 for t in ts):
        return "REFUTADA"
    return "INCONCLUSIVA" if any(abs(t) >= 2 for t in ts) else "NÃO SUPORTADA"


def todos_ou_algum(conds):
    return "CONFIRMADA" if all(conds) else ("PARCIAL" if any(conds) else "NÃO SUPORTADA")


def hipoteses(v):
    foco, tfs = v.ctx.tf_foco, [t for t in TFS_VAL if t in v.ctx.tfs]
    P = {tf: v.m("pareto", tf) for tf in tfs}
    E = {tf: v.m("estados", tf) for tf in foco}
    Dia = {tf: v.m("dia", tf) for tf in foco}
    por_tf = lambda f: "; ".join(f"{tf}: {f(tf)}" for tf in foco)  # noqa: E731
    em_todos = lambda f: "; ".join(f"{tf}: {f(tf)}" for tf in tfs)  # noqa: E731
    H = []

    def add(i, grupo, enun, regra, evid, ver):
        H.append((i, grupo, enun, regra, evid, ver))

    # --- modelo F = m * a * k
    esc = [v.m("escala", tf) for tf in foco]
    add("H01", "Modelo", "k é cosmético: com limiares adaptativos o estado independe de k (F×k ⇒ mesmo z)", "0 divergências entre k=1 e k=100",
        por_tf(lambda tf: f"{v.m('escala', tf)[0]} de {v.m('escala', tf)[1]}"), "CONFIRMADA" if all(a == 0 for a, _ in esc) else "NÃO SUPORTADA")
    imp = {tf: v.m("impacto", tf) for tf in foco}
    add("H02", "Modelo", "m e a são componentes distintos (não redundantes)", "\\|ρ de postos\\| entre \\|m\\| e a < 0.30",
        por_tf(lambda tf: f"ρ = {imp[tf][2]:+.2f}"), "CONFIRMADA" if all(abs(imp[tf][2]) < 0.30 for tf in foco) else "NÃO SUPORTADA")
    add("H03", "Modelo", "O esforço (a) produz deslocamento: corpo/ATR cresce com a (lei de impacto)", "β > 0.25 e R² ≥ 0.80 (log-log, 20 faixas)",
        por_tf(lambda tf: f"β = {imp[tf][0]:.2f}, R² = {imp[tf][1]:.2f}"), "CONFIRMADA" if all(imp[tf][0] > 0.25 and imp[tf][1] >= 0.80 for tf in foco) else "NÃO SUPORTADA")
    ab = {tf: dict(v.m("ablacao", tf)[1]) for tf in foco}
    ex = lambda tf, k: ab[tf][k]["exp"]  # noqa: E731
    top = all(ex(tf, SIG_F) > max(ex(tf, SIG_A), ex(tf, SIG_M)) for tf in foco)
    meio = all(ex(tf, SIG_F) > ex(tf, SIG_M) for tf in foco)
    add("H04", "Modelo", "O cruzamento m×a prevê atividade futura melhor que m ou a isolados", "expansão do range seguinte de F > a e > \\|m\\| (frequência igual)",
        por_tf(lambda tf: f"F {ex(tf, SIG_F):.2f}× · a {ex(tf, SIG_A):.2f}× · \\|m\\| {ex(tf, SIG_M):.2f}×"), "CONFIRMADA" if top else ("PARCIAL" if meio else "NÃO SUPORTADA"))
    ts = [E[tf]["colorido"]["t1"] for tf in foco]
    ver = "CONFIRMADA" if all(abs(t) >= 3 for t in ts) and len({np.sign(t) for t in ts}) == 1 else ("INCONCLUSIVA" if any(abs(t) >= 2 for t in ts) else "NÃO SUPORTADA")
    add("H05", "Modelo", "A cor do candle extremo carrega direção (retorno h1 alinhado ≠ 0)", "\\|t\\| ≥ 3 com o mesmo sinal nos dois TFs",
        por_tf(lambda tf: f"μ h1 = {fm(E[tf]['colorido']['sf1'], 1, sinal=True)} pts (t = {E[tf]['colorido']['t1']:+.1f})"), ver)

    # --- Pareto -> Bollinger
    add("H06", "Pareto→Bollinger", "A regra 80/20 vale para \\|F\\|: os 20% maiores candles concentram ≥ 80% da energia Σ\\|F\\|", "top 20% ≥ 80% (estrito) · 65–80% (aproximado) · < 65% refuta",
        em_todos(lambda tf: fm(P[tf]["top20"], 0, True)), "CONFIRMADA" if all(P[t]["top20"] >= 0.80 for t in tfs) else ("PARCIAL" if all(P[t]["top20"] >= 0.65 for t in tfs) else "REFUTADA"))
    add("H07", "Pareto→Bollinger", "O limiar fixo 70 equivale ao percentil ~80 de \\|F\\| em todos os TFs (âncora Pareto)", "P(\\|F\\|≥70) entre 16% e 24% em todos os TFs",
        em_todos(lambda tf: fm(P[tf]["p70"], 1, True)), "CONFIRMADA" if all(0.16 <= P[t]["p70"] <= 0.24 for t in tfs) else "NÃO SUPORTADA")
    ok = [t for t in tfs if P[t]["r2_pw"] > P[t]["r2_ex"]]
    add("H08", "Pareto→Bollinger", "A cauda de \\|F\\| segue lei de potência (Pareto) e não exponencial", "R² log-log > R² semilog na cauda P80–P99.5",
        em_todos(lambda tf: f"{P[tf]['r2_pw']:.3f} vs {P[tf]['r2_ex']:.3f}"), "CONFIRMADA" if len(ok) == len(tfs) else ("PARCIAL" if ok else "REFUTADA"))
    rb = {tf: v.m("robo", tf) for tf in tfs}
    add("H09", "Pareto→Bollinger", "Com 70/85 fixos a hierarquia ignição < saturação se inverte (≥85 é mais comum que 70–85)", "P(≥85) > P(70–85) em todos os TFs, na definição nova e na dos robôs",
        em_todos(lambda tf: f"{fm(P[tf]['p85'], 1, True)} vs {fm(P[tf]['forte'], 1, True)} (robôs {fm(rb[tf]['p85'], 1, True)} vs {fm(rb[tf]['forte'], 1, True)})"),
        "CONFIRMADA" if all(P[t]["p85"] > P[t]["forte"] and rb[t]["p85"] > rb[t]["forte"] for t in tfs) else "NÃO SUPORTADA")
    add("H10", "Pareto→Bollinger", "Com Bollinger a hierarquia é preservada (brilhante é mais raro que escuro)", "brilhante < escuro em todos os TFs",
        em_todos(lambda tf: f"{fm(P[tf]['bri'], 1, True)} vs {fm(P[tf]['esc'], 1, True)}"), "CONFIRMADA" if all(P[t]["bri"] < P[t]["esc"] for t in tfs) else "NÃO SUPORTADA")
    add("H11", "Pareto→Bollinger", "Bollinger desacopla a quantidade diária de cores do regime de volatilidade do dia (o limiar fixo não)", "ρ(fixo, amplitude do dia) ≥ 0.15 e \\|ρ(Bollinger, amplitude)\\| < 0.10 nos dois TFs",
        por_tf(lambda tf: f"ρ fixo {Dia[tf]['rho_f70_amp']:+.2f} vs Bollinger {Dia[tf]['rho_col_amp']:+.2f}"),
        "CONFIRMADA" if all(Dia[tf]["rho_f70_amp"] >= 0.15 and abs(Dia[tf]["rho_col_amp"]) < 0.10 for tf in foco) else "NÃO SUPORTADA")
    cv = {tf: v.m("hora", tf)[1] for tf in foco}
    mel = [cv[tf]["col"] < cv[tf]["f70"] for tf in foco]
    add("H12", "Pareto→Bollinger", "Bollinger distribui a cor ao longo do dia de forma mais uniforme que o limiar fixo", "CV entre horas (9h–17h) menor que o do fixo nos dois TFs",
        por_tf(lambda tf: f"CV fixo {cv[tf]['f70']:.2f} vs Bollinger {cv[tf]['col']:.2f}"), "CONFIRMADA" if all(mel) else ("INCONCLUSIVA" if any(mel) else "REFUTADA"))
    sz = [cv[tf]["cols"] < 0.8 * cv[tf]["col"] for tf in foco]
    add("H13", "Pareto→Bollinger", "Remover a sazonalidade do volume (a sazonal) elimina a concentração de cor na abertura", "CV com a sazonal < 0.8 × CV canônico nos dois TFs",
        por_tf(lambda tf: f"CV {cv[tf]['col']:.2f} → {cv[tf]['cols']:.2f}"), "CONFIRMADA" if all(sz) else ("INCONCLUSIVA" if any(sz) else "NÃO SUPORTADA"))
    gz = {tf: {k: m / g for k, g, m in v.m("gauss", tf)} for tf in foco}
    add("H14", "Pareto→Bollinger", "A cauda de F é mais pesada que a normal: 2.5σ ocorre bem mais que o previsto por um Bollinger gaussiano", "medido ÷ normal ≥ 1.5 em 2.5σ",
        por_tf(lambda tf: f"{gz[tf][2.5]:.1f}× (α de Hill = {P[tf]['alpha']:.2f})"), "CONFIRMADA" if all(gz[tf][2.5] >= 1.5 for tf in foco) else "NÃO SUPORTADA")
    ai = {tf: v.m("autoincl", tf) for tf in foco}
    add("H15", "Pareto→Bollinger", "O candle atual dentro da janela de μ/σ mascara extremos (auto-inclusão)", "colorido sobe ≥ 1 p.p. ao excluir o candle atual",
        por_tf(lambda tf: f"{fm(ai[tf][0], 1, True)} → {fm(ai[tf][1], 1, True)}"), "CONFIRMADA" if all(ai[tf][1] - ai[tf][0] >= 0.01 for tf in foco) else "NÃO SUPORTADA")
    cl = {tf: {n: r for n, _, r in v.m("classes", tf)} for tf in foco}
    dif = {tf: cl[tf][CL_BOLL]["exp"] - cl[tf][CL_PAR]["exp"] for tf in foco}
    add("H16", "Pareto→Bollinger", "Em frequência igual, Bollinger e Pareto fixo preveem a atividade seguinte com a mesma qualidade (a migração é estrutural, não preditiva)",
        "\\|Δ expansão do range seguinte\\| ≤ 0.03× nos dois TFs", por_tf(lambda tf: f"Bollinger {cl[tf][CL_BOLL]['exp']:.2f}× vs Pareto equiparado {cl[tf][CL_PAR]['exp']:.2f}×"),
        "CONFIRMADA" if all(abs(x) <= 0.03 for x in dif.values()) else "NÃO SUPORTADA")

    # --- sinais (cores)
    add("H17", "Sinais", "Cor persiste: candle colorido é seguido de candle colorido acima do esperado para a hora", "lift ajustado por hora ≥ 1.30 (nos dois TFs = confirmada; em um = parcial)",
        por_tf(lambda tf: f"lift = {E[tf]['colorido']['lift']:.2f}"), todos_ou_algum([E[tf]["colorido"]["lift"] >= 1.3 for tf in foco]))
    add("H18", "Sinais", "Escuro = continuação (o preço segue na direção da cor — \"manter posição\")", "μ h1 alinhado > 0 com t ≥ 3 nos dois TFs",
        por_tf(lambda tf: f"μ h1 = {fm(E[tf]['escuro']['sf1'], 1, sinal=True)} (t = {E[tf]['escuro']['t1']:+.1f})"), veredito([E[tf]["escuro"]["t1"] for tf in foco], +1))
    add("H19", "Sinais", "Brilhante = exaustão (reversão à média após o clímax)", "μ h1 e μ h3 alinhados < 0 com t ≤ −3 nos dois TFs",
        por_tf(lambda tf: f"h1 {fm(E[tf]['brilhante']['sf1'], 1, sinal=True)} (t = {E[tf]['brilhante']['t1']:+.1f}); h3 {fm(E[tf]['brilhante']['sf3'], 1, sinal=True)} (t = {E[tf]['brilhante']['t3']:+.1f})"),
        veredito([E[tf]["brilhante"][k] for tf in foco for k in ("t1", "t3")], -1))
    add("H20", "Sinais", "Brilhante antecipa expansão de volatilidade (alerta de atividade, não de direção)", "range seguinte ≥ 1.10× a média da hora com t ≥ 3 nos dois TFs",
        por_tf(lambda tf: f"{E[tf]['brilhante']['exp']:.2f}× (t = {E[tf]['brilhante']['t_exp']:+.1f})"),
        "CONFIRMADA" if all(E[tf]["brilhante"]["exp"] >= 1.10 and E[tf]["brilhante"]["t_exp"] >= 3 for tf in foco) else "NÃO SUPORTADA")
    add("H21", "Sinais", "Neutro = sem vantagem direcional (abstenção)", "\\|t\\| < 3 em μ h1 nos dois TFs",
        por_tf(lambda tf: f"μ h1 = {fm(E[tf]['N']['sf1'], 1, sinal=True)} (t = {E[tf]['N']['t1']:+.1f})"), "CONFIRMADA" if all(abs(E[tf]["N"]["t1"]) < 3 for tf in foco) else "NÃO SUPORTADA")

    # --- operacao visual
    add("H22", "Operação", "A cor é rara o bastante para saltar aos olhos (saliência visual)", "nos TFs de foco: colorido ≤ 15% e brilhante ≤ 5%",
        por_tf(lambda tf: f"{fm(P[tf]['col'], 1, True)} / {fm(P[tf]['bri'], 1, True)}"), "CONFIRMADA" if all(P[t]["col"] <= 0.15 and P[t]["bri"] <= 0.05 for t in foco) else "NÃO SUPORTADA")
    hr = {tf: v.m("hora", tf)[0] for tf in foco}
    raz = {tf: (hr[tf].loc[9, "col"] * hr[tf].loc[9, "n"] / (hr[tf]["col"] * hr[tf]["n"]).sum()) / (hr[tf].loc[9, "n"] / hr[tf]["n"].sum()) for tf in foco}
    add("H23", "Operação", "A abertura (9h) concentra as cores acima do seu peso em candles", "fração das cores em 9h ÷ fração dos candles em 9h ≥ 1.5",
        por_tf(lambda tf: f"{raz[tf]:.1f}×"), "CONFIRMADA" if all(raz[tf] >= 1.5 for tf in foco) else "NÃO SUPORTADA")
    add("H24", "Operação", "A quantidade diária de cores não indica dia de tendência nem de alta volatilidade (orçamento de cor ~constante)",
        "\\|ρ\\| < 0.15 entre coloridos/dia e (amplitude do dia; \\|C−O\\|/amplitude) nos dois TFs",
        por_tf(lambda tf: f"ρ amplitude {Dia[tf]['rho_col_amp']:+.2f}; ρ direcional {Dia[tf]['rho_col_dir']:+.2f}; CV diário {Dia[tf]['col_cv']:.2f}"),
        "CONFIRMADA" if all(abs(Dia[tf]["rho_col_amp"]) < 0.15 and abs(Dia[tf]["rho_col_dir"]) < 0.15 for tf in foco) else "NÃO SUPORTADA")

    # --- proxima teoria
    cm = {tf: v.m("clusters", tf)[1] for tf in foco}
    add("H25", "Próxima teoria", "Clusters de cor similar formam áreas (faixas de preço) com comportamento próprio (suporte/resistência, retorno às bordas)",
        "teste de retorno/rejeição nas bordas do cluster — ainda não executado",
        por_tf(lambda tf: f"{fm(cm[tf]['multi'], 0, True)} dos clusters têm ≥ 2 candles; amplitude mediana {cm[tf]['faixa_atr']:.1f} ATR"), "PENDENTE")
    h26 = medir_h26({tf: v.d(tf) for tf in foco}, minutos=100)
    add("H26", "Janela física", "Em uma janela fixa de 100 minutos, frequência e persistência de estados são comparáveis entre 5 min e 15 min", "diferença de cor ≤ 5 p.p. e diferença de persistência ≤ 0.15; sem inferir direção, risco ou operação",
        por_tf(lambda tf: f"{h26[tf]['colorido_pct']:.1%} de candles coloridos; persistência {h26[tf]['persistencia']:.2f}; Δ cor {h26[tf]['dif_cor']:.1%}, Δ persistência {h26[tf]['dif_persistencia']:.2f}"),
        "CONFIRMADA" if all(h26[tf]["comparavel"] for tf in foco) else ("INCONCLUSIVA" if any(h26[tf].get("comparavel") is not None for tf in foco) else "NÃO SUPORTADA"))
    cr = {tf: v.m("cluster_retorno", tf) for tf in foco}
    add("H30", "Distribuição de cores", "Dias muito direcionais têm uma distribuição de cores diferente dos demais", "|Δ hora da 1ª cor| > 0 ou |Δ brilho| > 0 com |t| ≥ 3, sem inferir direção",
        por_tf(lambda tf: f"1ª cor {v.m('h30', tf)['primeira_cor_top']:.2f} h vs {v.m('h30', tf)['primeira_cor_outros']:.2f} h; brilho {v.m('h30', tf)['brilhante_top']:.1%} vs {v.m('h30', tf)['brilhante_outros']:.1%}; t = {v.m('h30', tf)['t_hora']:+.2f}, {v.m('h30', tf)['t_brilhante']:+.2f}"),
        "CONFIRMADA" if all(veredito_h30(v.m("h30", tf)) == "CONFIRMADA" for tf in foco) else ("INCONCLUSIVA" if any(veredito_h30(v.m("h30", tf)) == "INCONCLUSIVA" for tf in foco) else "NÃO SUPORTADA"))
    add("H29", "Absorção", "A absorção (a ≥ 2 e |m| < 0.3) tem atividade e persistência próprias", "range/ATR ≥ 1.50× e |t_exp| ≥ 3; não inferir direção, entrada ou SL",
        por_tf(lambda tf: f"range {v.m('h29', tf)['expansao_absorcao']:.2f}× vs {v.m('h29', tf)['expansao_controle']:.2f}×; persistência {v.m('h29', tf)['persistencia']:.2f}; t = {v.m('h29', tf)['t_exp']:+.2f}"),
        "CONFIRMADA" if all(v.m("h29", tf)["veredito"] == "CONFIRMADA" for tf in foco) else ("INCONCLUSIVA" if any(v.m("h29", tf)["veredito"] == "INCONCLUSIVA" for tf in foco) else "NÃO SUPORTADA"))
    cr = {tf: v.m("cluster_retorno", tf) for tf in foco}
    add("H31", "Áreas por cluster", "O preço retorna às bordas dos clusters em até N candles mais que janelas aleatórias do mesmo horário e largura",
        "P(retorno) > controle e |t| ≥ 3; rejeição e rompimento ficam para estudo posterior",
        por_tf(lambda tf: f"{cr[tf]['p_retorno']:.1%} vs {cr[tf]['p_controle']:.1%} (t = {cr[tf]['t']:+.2f}; n = {cr[tf]['n_clusters']})"),
        "CONFIRMADA" if all(cr[tf]["p_retorno"] > cr[tf]["p_controle"] and abs(cr[tf]["t"]) >= 3 for tf in foco) else ("INCONCLUSIVA" if any(abs(cr[tf]["t"]) >= 2 for tf in foco) else "NÃO SUPORTADA"))
    tr = {tf: v.m("transicoes", tf) for tf in foco}
    add("H40", "Transições", "A duração das transições de família é descrita por mediana e percentis, sem inferir causalidade ou direção", "mediana ≤ 3 em ambos os TFs e P90 ≤ 25, com gaps de timestamp separados da contagem de neutros",
        por_tf(lambda tf: f"mediana {tr[tf]['neutros']['50%']:.2f}; P90 {tr[tf]['neutros']['90%']:.2f}; gaps {tr[tf]['gap_data']:.1%}"),
        "CONFIRMADA" if all(tr[tf]["neutros"]["50%"] <= 3 and tr[tf]["neutros"]["90%"] <= 25 for tf in foco) else "NÃO SUPORTADA")
    h39 = {tf: v.m("h39", tf) for tf in foco}
    h39_ver = all(veredito_h39(m) == "CONFIRMADA" for m in h39.values())
    add("H39", "Alarmes multi-TF", "Alarms coincidentes em dois ou mais timeframes têm maior próximo range/retorno do que alarmes isolados", "range/ATR e retorno médios maiores, com |t| ≥ 3; não usar contagem como prova de direção",
        por_tf(lambda tf: f"{h39[tf]['range_coincidente']:.2f} vs {h39[tf]['range_isolado']:.2f}; retorno {h39[tf]['retorno_coincidente']:.2f} vs {h39[tf]['retorno_isolado']:.2f}; t = {h39[tf]['t_range']:+.2f}, {h39[tf]['t_retorno']:+.2f}"), "CONFIRMADA" if h39_ver else "NÃO SUPORTADA")
    return H


def bloco_h_painel(v):
    H = hipoteses(v)
    w = {}
    if v.ctx.ativo == "WIN" and v.ctx.fontes("WDO"):
        w = {h[0]: h[5] for h in hipoteses(Val(v.ctx.derivar(ativo="WDO")))}
    L = [[i, g, e, r, ev, f"**{ver}**", w.get(i, "–")] for i, g, e, r, ev, ver in H]
    resumo = " · ".join(f"{k}: {n}" for k, n in pd.Series([h[5] for h in H]).value_counts().items())
    rep = f" Replicação em WDO: {sum(w.get(h[0]) == h[5] for h in H)} de {len(H)} vereditos idênticos." if w else ""
    return (cabecalho_bloco(v.ctx) + f"_Veredito calculado pelo script a partir dos dados (regra de significância: \\|t\\| ≥ 3). Resumo: {resumo}.{rep}_\n\n"
            + tabela(["id", "grupo", "hipótese", "regra de decisão", f"evidência ({v.ctx.ativo})", "veredito", "veredito WDO"], L, "lllllll"))


BLOCOS_VAL = {
    "v1_pareto": bloco_v1_pareto,
    "v1_comparacao": bloco_v1_comparacao,
    "v1_hora": bloco_v1_hora,
    "v2_candle": bloco_v2_candle,
    "v3_volume": bloco_v3_volume,
    "v4_cruzamento": bloco_v4_cruzamento,
    "v5_sinais": bloco_v5_sinais,
    "v6_cor_dia": bloco_v6_cor_dia,
    "v7_clusters": bloco_v7_clusters,
    "v8_transicoes": bloco_v8_transicoes,
    "v9_cluster_retorno": bloco_v9_cluster_retorno,
    "v10_h27": bloco_v10_h27,
    "v11_h28": bloco_v11_h28,
    "v11_h30": bloco_v11_h30,
    "v12_h29": bloco_v12_h29,
    "v12_h39": bloco_v12_h39,
}
BLOCOS_HIP = {"h_painel": bloco_h_painel}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ativo", default="WIN")
    ap.add_argument("--pastas", nargs="+", default=PASTAS_PADRAO)
    ap.add_argument("--tf-foco", nargs="+", default=TF_FOCO)
    ap.add_argument("--cobertura", type=float, default=COBERTURA)
    ap.add_argument("--blocos", nargs="+", choices=[*BLOCOS_VAL, *BLOCOS_HIP])
    ap.add_argument("--dia", help="AAAA-MM-DD: imprime so o mapa de cores do dia (1o TF de foco)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.ativo != "WIN" and not args.dry_run and not args.dia:
        ap.error("os .md documentam o WIN; para outro ativo use --dry-run")
    v = Val(Contexto(args.pastas, args.ativo, TFS_VAL, args.tf_foco, cobertura=args.cobertura))
    if args.dia:
        print(mapa_dia(v.d(args.tf_foco[0]), args.dia, d_saz=v.ds(args.tf_foco[0])))
        return
    todos = {**BLOCOS_VAL, **BLOCOS_HIP}
    saida = {bid: todos[bid](v) for bid in (args.blocos or todos)}
    if args.dry_run:
        for bid, texto in saida.items():
            print(f"\n===== {bid} =====\n{texto}")
        return
    for doc, blocos in ((DOC_VAL, BLOCOS_VAL), (DOC_HIP, BLOCOS_HIP)):
        sel = {b: t for b, t in saida.items() if b in blocos}
        if sel:
            atualizar_doc(sel, doc)
            print(f"{doc.name}: {len(sel)} bloco(s) atualizado(s)")


if __name__ == "__main__":
    main()
