"""Validação temporal descritiva de H29 com a definição canônica do motor."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parent
OUT = BASE / "VALIDACAO_TEMPORAL_H29.md"
if str(BASE.parent) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(BASE.parent))
from TeseFma_analiseCandle.analise_escalonamento_econofisico import TIMEFRAMES, series_motor  # noqa: E402
from TeseFma_analiseCandle.validacao_econofisica import medir_h29  # noqa: E402
INICIO = pd.Timestamp("2024-06-19")
CORTE = pd.Timestamp("2025-06-19")
FIM = pd.Timestamp("2026-05-14")
N_BOOT = 3000
SEED = 20261006


def fmt(valor: float, casas: int = 3) -> str:
    return "—" if pd.isna(valor) else f"{valor:.{casas}f}"


def delta_expansao_por_pregao_hora(dados: pd.DataFrame) -> pd.Series:
    """Diferença diária pareada por hora: absorção menos controles da mesma hora."""
    d = dados.sort_values("dt", kind="stable").copy()
    d["dia"] = d["dt"].dt.normalize()
    d["hora"] = d["dt"].dt.hour
    d["rng_atr"] = d["rng"] / d["atr"].where(d["atr"] > 0)
    d["expansao"] = d.groupby("dia", sort=False)["rng_atr"].shift(-1)
    evento = (d["a"] >= 2.0) & (d["m"].abs() < 0.3)
    d["evento"] = evento
    # Construir deltas por dia/hora apenas onde haja amostra dos dois lados.
    # Depois agrega por pregão ponderando pelas ocorrências H29 de cada hora,
    # para não contar uma sessão com muitos eventos como muitos pregões.
    estratos = []
    for (dia, hora), grupo in d.groupby(["dia", "hora"], sort=False):
        eventos = grupo.loc[grupo["evento"], "expansao"].dropna()
        controles = grupo.loc[~grupo["evento"], "expansao"].dropna()
        if len(eventos) >= 1 and len(controles) >= 2:
            estratos.append(
                {
                    "dia": dia,
                    "n_eventos": len(eventos),
                    "delta": float(eventos.mean() - controles.mean()),
                }
            )
    if not estratos:
        return pd.Series(dtype=float)
    estratos_df = pd.DataFrame(estratos)
    deltas = []
    for _, sessao in estratos_df.groupby("dia", sort=False):
        deltas.append(float(np.average(sessao["delta"], weights=sessao["n_eventos"])))
    return pd.Series(deltas, dtype=float)


def bootstrap_delta_diario(deltas: pd.Series) -> tuple[float, float, float, int, float]:
    """Média, IC percentil e t de Student entre diferenças diárias pareadas."""
    values = deltas.to_numpy(dtype=float)
    n = len(values)
    if n < 2:
        return float(np.mean(values)) if n else float("nan"), float("nan"), float("nan"), n, float("nan")
    mean = float(values.mean())
    se = float(values.std(ddof=1) / np.sqrt(n))
    t_day = mean / se if se > 0 else float("nan")
    rng = np.random.default_rng(SEED)
    picks = rng.integers(0, n, size=(N_BOOT, n))
    boot = values[picks].mean(axis=1)
    ci_low, ci_high = np.quantile(boot, [0.025, 0.975])
    return mean, float(ci_low), float(ci_high), n, float(t_day)


def calcular() -> tuple[str, dict]:
    linhas = [
        "# H29 — validação temporal da hipótese de absorção",
        "",
        f"_Gerado por `validar_h29_temporal.py`. Universo comum WIN: {INICIO:%Y-%m-%d} a {FIM:%Y-%m-%d}. Parser, features e cálculo de F vêm de `analise_candles.py`; critério de H29 vem de `validacao_econofisica.medir_h29()`._",
        "",
        "## Desenho preservado",
        "",
        "- Evento canônico: `a ≥ 2` e `|m| < 0.3`; horizonte = próximo candle da mesma sessão.",
        "- Regra original de H29: razão média range/ATR do evento para controle ≥1.50 e |t_exp|≥3; não se interpreta retorno como direção.",
        "- Corte temporal pré-fixado para este anexo: treino 2024-06-19 a 2025-06-18; holdout 2025-06-19 a 2026-05-14.",
        "- Não há busca de limiar ou edição da definição após observar o holdout. Trata-se de robustez temporal de H29, não de nova hipótese.",
        "",
        "| TF | Bloco | Candles | Pregões | Eventos H29 | Expansão evento | Expansão controle | Razão | t_exp Welch | Critério H29 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    resultados: dict[str, dict] = {}
    sensibilidade: list[dict] = []
    for tf in TIMEFRAMES:
        d = series_motor(tf).copy()
        d["dia"] = d["dt"].dt.normalize()
        resultados[tf] = {}
        for nome, inicio, fim in (
            ("treino", INICIO, CORTE - pd.Timedelta(days=1)),
            ("holdout", CORTE, FIM),
        ):
            s = d[(d["dia"] >= inicio) & (d["dia"] <= fim)].copy()
            m = medir_h29(s, limiar_a=2.0, limiar_m=0.3, horizonte=1, minimo=30)
            passa = (
                m["n_absorcao"] >= 30
                and pd.notna(m["persistencia"])
                and m["persistencia"] >= 1.50
                and pd.notna(m["t_exp"])
                and abs(m["t_exp"]) >= 3
            )
            m["passa_criterio"] = passa
            m["candles"] = len(s)
            m["dias"] = int(s["dia"].nunique())
            resultados[tf][nome] = m
            deltas = delta_expansao_por_pregao_hora(s)
            delta_mean, ci_low, ci_high, n_days, t_day = bootstrap_delta_diario(deltas)
            sensibilidade.append({
                "tf": tf,
                "bloco": nome,
                "mean": delta_mean,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "n_days": n_days,
                "t_day": t_day,
            })
            linhas.append(
                f"| {tf} | {nome} | {len(s)} | {s['dia'].nunique()} | {m['n_absorcao']} | {fmt(m['expansao_absorcao'])} | {fmt(m['expansao_controle'])} | {fmt(m['persistencia'])} | {fmt(m['t_exp'])} | {'passa' if passa else 'não passa'} |"
            )

    linhas += [
        "",
        "## Sensibilidade: efeito pareado por pregão",
        "",
        f"Para controlar a sazonalidade horária e a dependência intrassessão, em cada estrato pregão×hora com ≥1 evento e ≥2 controles calcula-se a diferença entre expansão média do evento e dos controles. Os estratos são agregados a uma diferença por pregão, ponderando pelo número de eventos H29; IC percentil bootstrap por pregão ({N_BOOT} réplicas, semente {SEED}). Esta é sensibilidade, não altera a regra histórica de H29.",
        "",
        "| TF | Bloco | Pregões elegíveis | Δ range/ATR pareado | IC95% bootstrap | t sobre diferenças diárias |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in sensibilidade:
        linhas.append(
            f"| {r['tf']} | {r['bloco']} | {r['n_days']} | {fmt(r['mean'])} | [{fmt(r['ci_low'])}, {fmt(r['ci_high'])}] | {fmt(r['t_day'])} |"
        )

    linhas += [
        "",
        "## Interpretação",
        "",
        "O critério original H29 (Welch candle a candle, razão ≥1.50 e |t|≥3) passa em treino e holdout para 5min e 15min. A sensibilidade mais estrita, com controles da mesma hora e erro agregado por pregão, tem IC95% acima de zero nos dois blocos do 5min; nos dois blocos do 15min os IC95% incluem zero. Portanto, a robustez temporal do efeito intradiário é mais convincente no 5min; no 15min, a incerteza por pregão não sustenta o mesmo grau de estabilidade. Nenhum desses resultados prova direção, causalidade ou resultado operacional.",
        "",
        "## Limitações estatísticas importantes",
        "",
        "- O t de decisão original é o Welch existente em H29 e trata candles de evento/controle como observações independentes. A tabela de sensibilidade agrega em pregão e controla a hora para reduzir esse problema; é evidência complementar e mais conservadora, não substitui nem reescreve o critério histórico.",
        "- O holdout preserva o corte cronológico e a regra fixa, mas os dados de treino e holdout pertencem ao mesmo ativo e a regimes de mercado temporalmente próximos; não equivale a replicação externa independente.",
        "- A sensibilidade por pregão×hora é complementar ao Welch histórico, que continua sendo o único critério de aprovação de H29. O pareamento reduz diferenças horárias e dependência intrassessão, mas não torna independentes pregões próximos nem corrige por todos os testes da tese.",
        "- Para 5min, o acervo canônico disponível não cobre 2020–2023; o split comum aqui começa em 2024-06-19.",
        "",
    ]
    return "\n".join(linhas), resultados


def main() -> None:
    texto, _ = calcular()
    OUT.write_text(texto, encoding="utf-8")
    print(f"Relatório gravado em: {OUT}")


if __name__ == "__main__":
    main()
