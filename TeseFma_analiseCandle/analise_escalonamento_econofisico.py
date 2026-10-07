"""Teste descritivo de escalonamento F=m*a no motor canônico do WIN."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
OUT = BASE / "ANALISE_ESCALONAMENTO_ECONOFISICO.md"
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from analise_ignicao_saturacao import TIMEFRAMES, series_motor  # noqa: E402

SESSOES = [(9, 10, "abertura 09h"), (10, 12, "manhã 10–11h"), (12, 14, "meio-dia 12–13h"), (14, 18, "tarde 14–17h")]
N_BINS = 20
N_BOOT = 300
SEED = 20261006


def curva_quantil(
    dados: pd.DataFrame,
    xcol: str,
    n_bins: int = N_BINS,
    edges: np.ndarray | None = None,
) -> tuple[pd.DataFrame, float, float, np.ndarray | None]:
    """Curva mediana de impacto em faixas equifrequentes e inclinação log-log."""
    amostra = dados[[xcol, "body_atr"]].replace([np.inf, -np.inf], np.nan).dropna()
    amostra = amostra[(amostra[xcol] > 0) & (amostra["body_atr"] > 0)]
    if len(amostra) < n_bins * 10:
        return pd.DataFrame(), np.nan, np.nan, edges
    if edges is None:
        quantiles = np.quantile(amostra[xcol], np.linspace(0, 1, n_bins + 1))
        internal = np.unique(quantiles[1:-1])
        edges = np.concatenate(([-np.inf], internal, [np.inf]))
    if len(edges) < 4:
        return pd.DataFrame(), np.nan, np.nan, edges
    amostra["bin"] = pd.cut(amostra[xcol], bins=edges, include_lowest=True, duplicates="drop")
    curva = amostra.groupby("bin", observed=True).agg(
        n=(xcol, "size"), x=(xcol, "median"), y=("body_atr", "median")
    )
    curva = curva[(curva["x"] > 0) & (curva["y"] > 0)]
    if len(curva) < 3:
        return curva, np.nan, np.nan, edges
    beta, intercepto = np.polyfit(np.log(curva["x"]), np.log(curva["y"]), 1)
    pred = intercepto + beta * np.log(curva["x"])
    ss_res = float(((np.log(curva["y"]) - pred) ** 2).sum())
    ss_tot = float(((np.log(curva["y"]) - np.log(curva["y"]).mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    curva = curva.reset_index(drop=True)
    return curva, float(beta), float(r2), edges


def bootstrap_beta_por_dia(dados: pd.DataFrame, n_boot: int = N_BOOT) -> tuple[float, float]:
    """IC percentil de beta reamostrando pregões inteiros, não candles isolados."""
    dias = dados["dia"].drop_duplicates().to_numpy()
    if len(dias) < 30:
        return np.nan, np.nan
    por_dia = {dia: dados[dados["dia"] == dia] for dia in dias}
    rng = np.random.default_rng(SEED)
    betas = []
    for _ in range(n_boot):
        sorteados = rng.choice(dias, size=len(dias), replace=True)
        amostra = pd.concat([por_dia[dia] for dia in sorteados], ignore_index=True)
        _, beta, _, _ = curva_quantil(amostra, "a")
        if np.isfinite(beta):
            betas.append(beta)
    if not betas:
        return np.nan, np.nan
    return float(np.quantile(betas, 0.025)), float(np.quantile(betas, 0.975))


def bootstrap_beta_com_faixas_fixas(
    dados: pd.DataFrame,
    edges: np.ndarray,
    n_boot: int = N_BOOT,
) -> tuple[float, float]:
    """IC do beta de validação reamostrando pregões, com bordas de treino congeladas."""
    dias = dados["dia"].drop_duplicates().to_numpy()
    if len(dias) < 30:
        return np.nan, np.nan
    por_dia = {dia: dados[dados["dia"] == dia] for dia in dias}
    rng = np.random.default_rng(SEED + 1)
    betas = []
    for _ in range(n_boot):
        sorteados = rng.choice(dias, size=len(dias), replace=True)
        amostra = pd.concat([por_dia[dia] for dia in sorteados], ignore_index=True)
        _, beta, _, _ = curva_quantil(amostra, "a", edges=edges)
        if np.isfinite(beta):
            betas.append(beta)
    if not betas:
        return np.nan, np.nan
    return float(np.quantile(betas, 0.025)), float(np.quantile(betas, 0.975))


def fnum(valor: float, casas: int = 3) -> str:
    return "—" if not np.isfinite(valor) else f"{valor:.{casas}f}"


def analisar_tf(tf: str, dados: pd.DataFrame) -> tuple[list[str], dict]:
    d = dados.sort_values("dt", kind="stable").copy()
    d["hora"] = d["dt"].dt.hour
    d["dia"] = d["dt"].dt.normalize()
    d["body_atr"] = (d["c"] - d["o"]).abs() / d["atr"].where(d["atr"] > 0)
    d["abs_m"] = d["m"].abs()
    d["abs_F"] = d["F"].abs()
    linhas = [
        f"\n## {tf}\n",
        f"Amostra: {len(d):,} candles, {d['dia'].nunique():,} pregões, de {d['dt'].min():%Y-%m-%d} a {d['dt'].max():%Y-%m-%d}.".replace(",", "."),
    ]

    medidas = {}
    for sinal, xcol, titulo in (("a", "a", "Esforço de volume a"), ("|m|", "abs_m", "Eficiência geométrica |m|"), ("|F|", "abs_F", "Produto |F|=|m·a·100|")):
        curva, beta, r2, _ = curva_quantil(d, xcol)
        rho = d[xcol].rank().corr(d["body_atr"].rank()) if len(d) else np.nan
        medidas[sinal] = {"beta": beta, "r2": r2, "rho": float(rho)}
        linhas.append(f"\n### {titulo}\n\n- Spearman com corpo/ATR: ρ={fnum(rho)}. Curva mediana em faixas equifrequentes: β={fnum(beta, 2)}, R² log-log={fnum(r2, 3)}.")
        if sinal == "a" and not curva.empty:
            linhas += ["", "| Faixa | a mediano | corpo/ATR mediano | n |", "|---:|---:|---:|---:|"]
            linhas += [f"| {i + 1} | {r.x:.3f} | {r.y:.3f} | {int(r.n)} |" for i, r in curva.iterrows()]

    lo, hi = bootstrap_beta_por_dia(d)
    medidas["a"]["beta_ci95"] = [lo, hi]
    linhas.append(f"\nIC percentil 95% de β(a), bootstrap por pregão ({N_BOOT} réplicas, semente {SEED}): [{fnum(lo, 2)}, {fnum(hi, 2)}].")

    linhas += ["", "### Estabilidade intradiária do escalonamento de a", "", "| Faixa horária | Candles | Pregões | β(a) | R² log-log | ρ(a, corpo/ATR) |", "|---|---:|---:|---:|---:|---:|"]
    for h0, h1, nome in SESSOES:
        parte = d[d["hora"].between(h0, h1 - 1)]
        curva, beta, r2, _ = curva_quantil(parte, "a")
        rho = parte["a"].rank().corr(parte["body_atr"].rank()) if len(parte) > 1 else np.nan
        linhas.append(f"| {nome} | {len(parte)} | {parte['dia'].nunique()} | {fnum(beta, 2)} | {fnum(r2, 3)} | {fnum(rho)} |")

    linhas.append("\n**Leitura:** β<1 é compatível com retornos decrescentes do deslocamento mediano conforme aumenta o esforço de volume; β≈1 seria proporcionalidade; β>1 seria superlinear. Isso descreve associação entre variáveis construídas pelo próprio motor, não causalidade física provada.")
    return linhas, medidas


def validar_temporal(dados: pd.DataFrame, corte: pd.Timestamp) -> dict:
    """Estima bins em treino e aplica exatamente as mesmas bordas ao holdout."""
    treino = dados[dados["dt"] < corte].copy()
    validacao = dados[dados["dt"] >= corte].copy()
    treino["body_atr"] = (treino["c"] - treino["o"]).abs() / treino["atr"].where(treino["atr"] > 0)
    validacao["body_atr"] = (validacao["c"] - validacao["o"]).abs() / validacao["atr"].where(validacao["atr"] > 0)
    curva_treino, beta_treino, r2_treino, edges = curva_quantil(treino, "a")
    curva_validacao, beta_validacao, r2_validacao, _ = curva_quantil(
        validacao, "a", edges=edges
    )
    ic_validacao = bootstrap_beta_com_faixas_fixas(validacao, edges) if edges is not None else (np.nan, np.nan)
    criterio_treino = bool(np.isfinite(beta_treino) and np.isfinite(r2_treino) and beta_treino > 0.25 and r2_treino >= 0.80)
    criterio_validacao = bool(
        np.isfinite(beta_validacao)
        and np.isfinite(r2_validacao)
        and beta_validacao > 0.25
        and r2_validacao >= 0.80
    )
    return {
        "treino": treino,
        "validacao": validacao,
        "n_treino": len(treino),
        "n_validacao": len(validacao),
        "dias_treino": int(treino["dt"].dt.normalize().nunique()),
        "dias_validacao": int(validacao["dt"].dt.normalize().nunique()),
        "beta_treino": beta_treino,
        "r2_treino": r2_treino,
        "beta_validacao": beta_validacao,
        "r2_validacao": r2_validacao,
        "ic95_validacao": ic_validacao,
        "criterio_treino": criterio_treino,
        "criterio_validacao": criterio_validacao,
        "faixas_treino": len(curva_treino),
        "faixas_validacao": len(curva_validacao),
    }


def gerar_relatorio() -> str:
    series = {tf: series_motor(tf) for tf in TIMEFRAMES}
    inicio = max(d["dt"].min() for d in series.values() if not d.empty).normalize()
    fim = min(d["dt"].max() for d in series.values() if not d.empty).normalize()
    series = {
        tf: d[(d["dt"].dt.normalize() >= inicio) & (d["dt"].dt.normalize() <= fim)].copy()
        for tf, d in series.items()
    }
    corte = inicio + pd.DateOffset(months=12)
    linhas = [
        "# WIN — escalonamento econofísico do motor F=m·a",
        "",
        f"_Gerado por `analise_escalonamento_econofisico.py`. Janela comum entre timeframes: {inicio:%Y-%m-%d} a {fim:%Y-%m-%d}. Parser e cálculo: motor Python canônico._",
        "",
        "## Pergunta",
        "",
        "Como o deslocamento corporal normalizado pelo ATR (`body/ATR`) escala com esforço volumétrico `a`, eficiência geométrica `|m|` e produto `|F|`, e a relação varia entre faixas horárias?",
        "",
        "## Definições e desenho",
        "",
        "- Usa `ler_csv()` e `calcular()` de `analise_candles.py`; mantém a definição e janela do motor. Calcula cada contrato dentro do próprio arquivo, seleciona por pregão o contrato com volume próximo do máximo, aplica a prioridade das pastas canônicas e não mistura rolagens dentro de janelas móveis.",
        "- `body/ATR = |Close−Open| / ATR`; `a = volume / média de volume anterior`; `m = (Close−Open)/range`; `F = m×a×100`.",
        "- Para cada variável, agrupa observações positivas em 20 quantis, calcula a mediana de x e body/ATR em cada faixa e ajusta `log(body/ATR) = α + β log(x)`. Também reporta Spearman candle a candle. O `R² log-log` é descritivo e calculado sobre as 20 medianas das faixas.",
        "- O intervalo de confiança do β para `a` reamostra pregões inteiros; não reamostra candles independentes. Sessões horárias estão fixadas antes da leitura: 09h; 10–11h; 12–13h; 14–17h.",
        "- São medidas internas descritivas: `body/ATR` já é derivado do preço no mesmo candle e `a` participa de F. Logo, associação e ajuste não estabelecem causalidade física independente.",
        f"- Validação temporal H03: treino = início da janela até {(corte - pd.Timedelta(days=1)):%Y-%m-%d} (12 meses); holdout = {corte:%Y-%m-%d} a {fim:%Y-%m-%d}. Quantis e bordas são calculados apenas no treino e congelados no holdout.",
    ]
    resultados = {}
    holdouts = {}
    for tf in TIMEFRAMES:
        bloco, medidas = analisar_tf(tf, series[tf])
        linhas.extend(bloco)
        resultados[tf] = medidas
        holdouts[tf] = validar_temporal(series[tf], corte)

    linhas += [
        "",
        "## H03 — validação temporal sem alterar a hipótese",
        "",
        "Regra original: β>0.25 e R²≥0.80 na relação log-log entre a e body/ATR, estimada sobre 20 faixas. Para evitar recalibrar no holdout, as bordas equifrequentes são aprendidas no treino e mantidas fixas na validação.",
        "",
        "Este é um anexo de robustez para H03, não uma nova hipótese nem alteração do critério original. O corte temporal é fixado pelo desenho e os quantis de treino são reutilizados sem recalibração no holdout.",
        "",
        "| TF | Período treino | n treino | β treino | R² treino | Critério treino | Período holdout | n holdout | β holdout | IC95% β holdout (pregão) | R² holdout | Critério holdout |",
        "|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---|",
    ]
    treino_fim = corte - pd.Timedelta(days=1)
    for tf, r in holdouts.items():
        lo, hi = r["ic95_validacao"]
        linhas.append(
            f"| {tf} | {inicio:%Y-%m-%d}–{treino_fim:%Y-%m-%d} | {r['n_treino']} ({r['dias_treino']} pregões) | {fnum(r['beta_treino'], 2)} | {fnum(r['r2_treino'], 3)} | {'passa' if r['criterio_treino'] else 'não passa'} | {corte:%Y-%m-%d}–{fim:%Y-%m-%d} | {r['n_validacao']} ({r['dias_validacao']} pregões) | {fnum(r['beta_validacao'], 2)} | [{fnum(lo, 2)}, {fnum(hi, 2)}] | {fnum(r['r2_validacao'], 3)} | {'passa' if r['criterio_validacao'] else 'não passa'} |"
        )

    linhas += ["", "## Síntese", ""]
    for tf in TIMEFRAMES:
        m = resultados[tf]["a"]
        ci = m["beta_ci95"]
        linhas.append(
            f"- **{tf}:** escalonamento `a → body/ATR` β={fnum(m['beta'], 2)}, R²={fnum(m['r2'], 3)}, ρ={fnum(m['rho'])}, IC95% por pregão [{fnum(ci[0], 2)}, {fnum(ci[1], 2)}]."
        )
    linhas += [
        "",
        "A hipótese mecanicista mais estreita compatível com este desenho é: ‘maior a acompanha maior corpo/ATR mediano’, caso a relação positiva se replique por pregões e faixas horárias. Mesmo se sustentada, isso não prova volume como força causal nem permite chamar `a` de aceleração física: volume de contratos é uma proxy de atividade/fluxo.",
        "A H03 permanece a mesma hipótese. Este holdout é uma verificação temporal do critério existente, não uma hipótese nova. A decisão de replicação exige que treino e holdout satisfaçam separadamente β>0.25 e R²≥0.80. O IC95% do holdout informa a incerteza do beta, mas não foi acrescentado à regra original.",
        "",
        "## Próximo teste rigoroso",
        "",
        "1. Congelar este desenho e replicar β em blocos temporais sem sobreposição (ex.: estimação 2020–2023; verificação 2024–2026), incluindo intervalos por pregão.",
        "2. Comparar a contribuição incremental de `a` além de `|m|` por regressão/validação por blocos, pois `F` já contém ambos; reportar desempenho descritivo em body/ATR, não direção nem rentabilidade.",
        "3. Se blocos temporais discordarem, reportar não-estacionariedade em vez de escolher outra faixa pós-hoc.",
        "",
    ]
    return "\n".join(linhas)


def main() -> None:
    OUT.write_text(gerar_relatorio(), encoding="utf-8")
    print(f"Relatório gravado em: {OUT}")


if __name__ == "__main__":
    main()
