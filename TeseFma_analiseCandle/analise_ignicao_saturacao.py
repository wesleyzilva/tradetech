"""Análise descritiva reproduzível de ignição e saturação Bollinger no WIN."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
OUT = BASE / "ANALISE_IGNICAO_SATURACAO.md"
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
from analise_candles import DATA_ROOT, calcular, ler_csv  # noqa: E402

TIMEFRAMES = ("5min", "15min")
HORIZONTES = (1, 3)
K_IGNICAO = 1.5
K_SATURACAO = 2.5
PASTAS_CANONICAS = ("2020_22", "2022_24", "2024_26", "2026")


def series_motor(tf: str) -> pd.DataFrame:
    """Monta a série com ler_csv/calcular do motor canônico e contratos ativos diários."""
    partes = []
    for prioridade, pasta in enumerate(PASTAS_CANONICAS):
        diretorio = DATA_ROOT / pasta
        if not diretorio.exists():
            continue
        for caminho in sorted(diretorio.glob(f"WIN*_F_0_{tf}.csv")):
            if caminho.stat().st_size == 0:
                continue
            ohlcv = ler_csv(caminho)
            if ohlcv.empty:
                continue
            d = calcular(ohlcv)
            d["simbolo"] = caminho.name.split("_F_0_")[0]
            d["prioridade_pasta"] = prioridade
            partes.append(d)
    if not partes:
        return pd.DataFrame()
    dados = pd.concat(partes, ignore_index=True)
    dados["dia"] = dados["dt"].dt.normalize()
    volume_dia = dados.groupby(["dia", "prioridade_pasta", "simbolo"], as_index=False)["v"].sum()
    volume_dia = volume_dia[
        volume_dia["v"] >= 0.9 * volume_dia.groupby("dia")["v"].transform("max")
    ]
    escolhidos = (
        volume_dia.sort_values(["dia", "prioridade_pasta", "simbolo"], kind="stable")
        .drop_duplicates("dia", keep="first")[["dia", "prioridade_pasta", "simbolo"]]
    )
    return (
        dados.merge(escolhidos, on=["dia", "prioridade_pasta", "simbolo"])
        .sort_values("dt", kind="stable")
        .reset_index(drop=True)
    )


def estatistica_diaria(valores: pd.Series) -> tuple[float, float, int, float]:
    valores = valores.dropna()
    if len(valores) < 2:
        return np.nan, np.nan, len(valores), np.nan
    media = float(valores.mean())
    erro = float(valores.std(ddof=1) / np.sqrt(len(valores)))
    t = media / erro if erro > 0 else np.nan
    return media, erro, len(valores), float(t)


def preparar(dados: pd.DataFrame) -> pd.DataFrame:
    dados = dados.sort_values("dt", kind="stable").reset_index(drop=True).copy()
    dados["dia"] = dados["dt"].dt.normalize()
    dados["hora"] = dados["dt"].dt.hour
    dados["z_direcional"] = dados["z"] * np.sign(dados["F"])
    dados["classe"] = np.select(
        [dados["z_direcional"] >= K_SATURACAO, dados["z_direcional"] >= K_IGNICAO],
        ["saturacao", "ignicao"],
        default="base",
    )
    dados["rng_atr"] = dados["rng"] / dados["atr"].where(dados["atr"] > 0)
    grupos = dados.groupby("dia", sort=False)
    for horizonte in HORIZONTES:
        dados[f"ret{horizonte}"] = np.sign(dados["F"]) * (
            grupos["c"].shift(-horizonte) - dados["c"]
        )
        dados[f"range_atr_h{horizonte}"] = grupos["rng_atr"].shift(-horizonte)
    return dados


def resumir_classe(dados: pd.DataFrame, classe: str) -> dict:
    eventos = dados[dados["classe"] == classe]
    controles = dados[dados["classe"] != classe]
    resumo = {
        "n": len(eventos),
        "dias_com_evento": int(eventos["dia"].nunique()),
        "eventos_por_dia": len(eventos) / max(1, dados["dia"].nunique()),
        "percentual": 100 * len(eventos) / max(1, len(dados)),
        "m_abs_mediana": float(eventos["m"].abs().median()),
        "a_mediana": float(eventos["a"].median()),
        "F_abs_mediana": float(eventos["F"].abs().median()),
        "z_direcional_mediana": float(eventos["z_direcional"].median()),
        "horizontes": {},
    }

    for horizonte in HORIZONTES:
        ret = f"ret{horizonte}"
        expansao = f"range_atr_h{horizonte}"
        rows = []
        for dia, eventos_dia in eventos.groupby("dia", sort=False):
            controle_dia = controles[controles["dia"] == dia]
            if controle_dia.empty:
                continue
            media_hora = controle_dia.groupby("hora")[[ret, expansao]].mean()
            comparacao = eventos_dia[["hora", ret, expansao]].join(
                media_hora, on="hora", rsuffix="_controle"
            ).dropna()
            if comparacao.empty:
                continue
            rows.append(
                {
                    "dia": dia,
                    "n": len(comparacao),
                    "retorno_evento": float(comparacao[ret].mean()),
                    "retorno_controle_hora": float(comparacao[f"{ret}_controle"].mean()),
                    "delta_retorno": float(
                        (comparacao[ret] - comparacao[f"{ret}_controle"]).mean()
                    ),
                    "range_evento": float(comparacao[expansao].mean()),
                    "range_controle_hora": float(
                        comparacao[f"{expansao}_controle"].mean()
                    ),
                    "delta_range": float(
                        (comparacao[expansao] - comparacao[f"{expansao}_controle"]).mean()
                    ),
                }
            )

        diario = pd.DataFrame(rows)
        ret_stats = estatistica_diaria(diario["delta_retorno"])
        range_stats = estatistica_diaria(diario["delta_range"])
        resumo["horizontes"][horizonte] = {
            "dias": len(diario),
            "retorno_alinhado_medio": float(diario["retorno_evento"].mean()),
            "proporcao_retorno_positivo": float((eventos[ret] > 0).mean()),
            "delta_retorno_diario": ret_stats,
            "range_atr_medio": float(diario["range_evento"].mean()),
            "delta_range_diario": range_stats,
        }
    return resumo


def fmt(v: float, casas: int = 2) -> str:
    return "—" if not np.isfinite(v) else f"{v:.{casas}f}"


def gerar_relatorio() -> str:
    series = {tf: preparar(series_motor(tf)) for tf in TIMEFRAMES}
    inicio = max(d["dt"].min() for d in series.values()).normalize()
    fim = min(d["dt"].max() for d in series.values()).normalize()
    series = {
        tf: d[(d["dia"] >= inicio) & (d["dia"] <= fim)].copy().reset_index(drop=True)
        for tf, d in series.items()
    }

    linhas = [
        "# WIN — análise descritiva de ignição e saturação Bollinger",
        "",
        f"_Gerado pelo script `analise_ignicao_saturacao.py`, usando `analise_candles.ler_csv()` e `analise_candles.calcular()`. Janela comum: {inicio:%Y-%m-%d} a {fim:%Y-%m-%d}. Limiares: ignição {K_IGNICAO:.1f}σ–<{K_SATURACAO:.1f}σ; saturação ≥{K_SATURACAO:.1f}σ._",
        "",
        "## Método",
        "",
        "- Escore direcional = `z × sign(F)`. A classe ignição usa [1.5, 2.5); saturação usa ≥2.5; o restante é controle/base.",
        "- `F`, `m`, `a`, `μ`, `σ`, `z`, `est` e `fam` vêm diretamente de `analise_candles.py`; o estudo não implementa uma fórmula paralela nem altera a regra do motor.",
        "- Retorno alinhado = `sign(F) × (fechamento futuro − fechamento do evento)`, em pontos.",
        "- Expansão = `range/ATR` do candle futuro. O controle usa candles de outras classes na mesma sessão e na mesma hora, com média calculada por sessão.",
        "- Efeitos e erros-padrão são calculados sobre a média diária dos eventos, não tratando cada candle como observação independente. Os valores t são descritivos, não decisão de hipótese nem correção para múltiplos testes.",
        "- Somente horizontes que permanecem no mesmo dia entram nas métricas. Para montar WIN contínuo, cada CSV de contrato é calculado pelo motor; por dia, mantém-se a série de maior volume, com a prioridade das pastas canônicas em empates.",
        "",
        "## Frequência e composição dos eventos",
        "",
        "| TF | Classe | Candles | % da amostra | Dias com evento | Eventos/dia | mediana abs(m) | mediana a | mediana abs(F) | mediana z direcional |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    sumarios = {}
    transicoes = {}
    for tf, d in series.items():
        sumarios[tf] = {}
        proxima_classe = d.groupby("dia", sort=False)["classe"].shift(-1)
        eventos_ignicao = d["classe"] == "ignicao"
        transicoes[tf] = {
            "n_ignicao": int(eventos_ignicao.sum()),
            "n_ignicao_para_saturacao": int(
                (eventos_ignicao & (proxima_classe == "saturacao")).sum()
            ),
        }
        transicoes[tf]["pct"] = (
            100 * transicoes[tf]["n_ignicao_para_saturacao"] / transicoes[tf]["n_ignicao"]
            if transicoes[tf]["n_ignicao"]
            else np.nan
        )
        for classe in ("ignicao", "saturacao"):
            r = resumir_classe(d, classe)
            sumarios[tf][classe] = r
            nome = "Ignição" if classe == "ignicao" else "Saturação"
            linhas.append(
                f"| {tf} | {nome} | {r['n']} | {fmt(r['percentual'], 2)}% | {r['dias_com_evento']} | {fmt(r['eventos_por_dia'])} | {fmt(r['m_abs_mediana'], 3)} | {fmt(r['a_mediana'], 3)} | {fmt(r['F_abs_mediana'])} | {fmt(r['z_direcional_mediana'])} |"
            )

    linhas += [
        "",
        "## Transição de ignição para saturação",
        "",
        "Percentual de eventos de ignição cuja barra seguinte, dentro da mesma sessão, é saturação:",
        "",
        "| TF | Ignições | Seguidas por saturação na próxima barra | Percentual |",
        "|---|---:|---:|---:|",
    ]
    for tf, r in transicoes.items():
        linhas.append(
            f"| {tf} | {r['n_ignicao']} | {r['n_ignicao_para_saturacao']} | {fmt(r['pct'], 2)}% |"
        )

    linhas += [
        "",
        "## O que acontece depois — evento versus controle por hora",
        "",
        "`Δ` compara a média diária dos eventos com a média dos candles-controle da mesma sessão e hora. `t_dia` é o efeito médio dividido pelo erro-padrão entre dias.",
        "",
        "| TF | Classe | h | Dias | Retorno alinhado (pts) | Δ retorno (pts) | t_dia retorno | range/ATR futuro | Δ range/ATR | t_dia range |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for tf in TIMEFRAMES:
        for classe in ("ignicao", "saturacao"):
            nome = "Ignição" if classe == "ignicao" else "Saturação"
            for horizonte in HORIZONTES:
                r = sumarios[tf][classe]["horizontes"][horizonte]
                dr, se_r, _, t_r = r["delta_retorno_diario"]
                dv, se_v, _, t_v = r["delta_range_diario"]
                linhas.append(
                    f"| {tf} | {nome} | {horizonte} | {r['dias']} | {fmt(r['retorno_alinhado_medio'], 1)} | {fmt(dr, 1)} ± {fmt(se_r, 1)} | {fmt(t_r)} | {fmt(r['range_atr_medio'], 3)} | {fmt(dv, 3)} ± {fmt(se_v, 3)} | {fmt(t_v)} |"
                )

    linhas += [
        "",
        "## Leitura atual",
        "",
        f"- **Saturação WIN 5min:** evento raro ({fmt(sumarios['5min']['saturacao']['percentual'], 2)}%); a expansão do próximo range/ATR é maior que o controle horário e o efeito diário continua marcado nos dois horizontes aqui medidos (t_dia {fmt(sumarios['5min']['saturacao']['horizontes'][1]['delta_range_diario'][3])} e {fmt(sumarios['5min']['saturacao']['horizontes'][3]['delta_range_diario'][3])}). O retorno alinhado médio, porém, não supera claramente o controle quando a unidade de análise é o dia. Isso sustenta uma descrição de atividade/volatilidade, não de direção.",
        "- **Ignição WIN 5min:** ocorre cerca de dez vezes por sessão nesta definição, mas as diferenças ajustadas por hora para retorno e expansão não mostram efeito diário claro nos horizontes testados.",
        "- **WIN 15min:** a saturação mostra contraste de expansão mais fraco e dependente do horizonte; ignição tampouco mostra aumento claro de atividade. Não misturar estes resultados com o 5min.",
        f"- No candle imediatamente seguinte, ignição transita para saturação em {transicoes['5min']['n_ignicao_para_saturacao']} de {transicoes['5min']['n_ignicao']} eventos no 5min ({fmt(transicoes['5min']['pct'], 2)}%); a tabela inclui também 15min. É uma taxa descritiva, não uma regra operacional.",
        "",
        "## Limites e próximos testes do motor",
        "",
        "1. Este é um recorte exploratório WIN 5min/15min; não é validação fora da amostra, não demonstra causalidade e não é análise de execução.",
        "2. Sobreposição de eventos e dependência intrassessão ainda podem afetar as incertezas. Um próximo teste estatístico deve usar bootstrap por sessão ou blocos temporais e controle pareado pré-especificado.",
        "3. Sensibilidade de limiar deve ser tratada como grade exploratória com correção por múltiplas comparações, ou como novas hipóteses congeladas antes do período de validação.",
        "4. Sem alteração de limiares, o achado inicial mais nítido é: saturação 5min está associada a expansão futura do range; a interpretação direcional permanece sem suporte claro neste teste.",
        "",
    ]
    return "\n".join(linhas)


def main() -> None:
    OUT.write_text(gerar_relatorio(), encoding="utf-8")
    print(f"Relatório gravado em: {OUT}")


if __name__ == "__main__":
    main()