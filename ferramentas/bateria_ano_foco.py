"""Retrato descritivo do ano foco, comparado com os anos anteriores.

Não escolhe parâmetro. Mede, em cada janela e timeframe, a frequência da cor, o alarme de volatilidade
da barra brilhante e o retorno alinhado da cor. Serve para ver se o ano novo se comporta como os anteriores.

Quando entrar um export novo, basta colocá-lo em ``dados/candles/<lote>/`` e rodar de novo:
o leitor pega o lote sozinho. Séries do ano foco ficam em ``SERIES_ANO``.

Uso: python ferramentas/bateria_ano_foco.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "motores" / "M01_fma_forca" / "teses" / "cores"))

from analise_candles import calcular  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402

SAIDA = RAIZ / "docs" / "ano_foco" / "2026" / "RETRATO.md"
TFS = (5, 15, 30, 60)
SERIES_ANO = ("WINM26", "WINQ26")  # incluir WINV26 quando o export existir
JANELAS = [
    ("2014-2019", "WINFUT", "2014-01-01", "2019-12-31"),
    ("2020-2025", "WINFUT", "2020-01-01", "2025-12-31"),
    ("2026 M26", "WINM26", "2026-01-01", "2026-12-31"),
    ("2026 Q26", "WINQ26", "2026-01-01", "2026-12-31"),
]


def t_dias_com_evento(valor: pd.Series, dia: pd.Series) -> float:
    """t da média diária, só nos pregões em que houve evento. Dias sem evento não entram como zero."""
    s = valor.groupby(dia).mean().dropna()
    if len(s) < 3 or s.std(ddof=1) == 0:
        return float("nan")
    return float(s.mean() / (s.std(ddof=1) / np.sqrt(len(s))))


def medir(serie: str, tf: int, ini: str, fim: str) -> dict | None:
    try:
        d = carregar_serie(serie, f"{tf}min")
    except FileNotFoundError:
        return None
    d = d[(d["dt"] >= ini) & (d["dt"] <= fim + " 23:59")]
    if len(d) < 200:
        return None
    c = calcular(d[["dt", "o", "h", "l", "c", "v"]].copy())
    c["dia"] = c["dt"].dt.normalize()
    c["hhmm"] = c["dt"].dt.hour * 100 + c["dt"].dt.minute
    c["rng"] = c["h"] - c["l"]
    F = c["F"].abs()
    brilhante = c["est"].abs() == 2
    media_hora = c.groupby("hhmm")["rng"].transform("mean")
    ratio = (c["rng"].shift(-1) / media_hora.shift(-1)).where(c["dia"].shift(-1) == c["dia"])
    ret = (np.sign(c["F"]) * (c["c"].shift(-1) - c["c"]) / c["atr"]).where((c["dia"].shift(-1) == c["dia"]) & (c["est"].abs() >= 1))
    ret = ret.replace([np.inf, -np.inf], np.nan)
    r = ((c["c"] - c["o"]) / c["atr"]).replace([np.inf, -np.inf], np.nan)
    mesmo = c["dia"] == c["dia"].shift(1)
    x, y = r[mesmo], r.shift(1)[mesmo]
    ok = x.notna() & y.notna()
    rho = float(np.corrcoef(x[ok], y[ok])[0, 1]) if ok.sum() > 50 else float("nan")
    return {
        "pregoes": int(c["dia"].nunique()),
        "inicio": str(c["dt"].min().date()),
        "fim": str(c["dt"].max().date()),
        "atr": float(c["atr"].median()),
        "n1": float((c["est"].abs() >= 1).mean()),
        "n2": float(brilhante.mean()),
        "f60": float((F >= 60).mean()),
        "f80": float((F >= 80).mean()),
        "exp": float(ratio[brilhante].mean()),
        "exp_t": t_dias_com_evento((ratio - 1).where(brilhante), c["dia"]),
        "ret": float(ret.mean()),
        "ret_t": t_dias_com_evento(ret, c["dia"]),
        "ret_p": float((ret.dropna() > 0).mean()),
        "rho": rho,
    }


def fmt(x, casas=2, pct=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    if pct:
        x *= 100
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    tab: dict[tuple[int, str], dict] = {}
    for nome, serie, ini, fim in JANELAS:
        for tf in TFS:
            m = medir(serie, tf, ini, fim)
            if m:
                tab[(tf, nome)] = m
            print(nome, tf, "ok" if m else "sem dados", flush=True)

    nomes = [j[0] for j in JANELAS]
    md = ["# Retrato do ano foco — 2026\n",
          "> Gerado por `ferramentas/bateria_ano_foco.py`. Descritivo: compara o comportamento, não escolhe parâmetro do robô. "
          "Regra: `docs/05_TRILHA_ROBO.md`, seção do ano foco.\n",
          "Janelas fixas: 2014-2019 e 2020-2025 no WINFUT; 2026 em cada contrato, sem juntar preços. "
          f"Séries do ano: {', '.join(SERIES_ANO)}. Quando o export novo chegar, ele entra sozinho se estiver em `dados/candles/`.\n"]

    def tabela(tf: int, linhas_def: list[tuple[str, str, callable]]) -> None:
        md.append(f"## {tf} min\n")
        head = "| medida | " + " | ".join(nomes) + " |"
        md.append(head)
        md.append("|" + "|".join("---" for _ in range(len(nomes) + 1)) + "|")
        for rotulo, chave, fun in linhas_def:
            cel = []
            for n in nomes:
                m = tab.get((tf, n))
                cel.append(fun(m) if m else "—")
            md.append("| " + rotulo + " | " + " | ".join(cel) + " |")
        md.append("")

    cobertura = [("pregões", "pregoes", lambda m: fmt(m["pregoes"], 0)),
                 ("início real", "inicio", lambda m: m["inicio"]),
                 ("fim real", "fim", lambda m: m["fim"]),
                 ("ATR mediano (pts)", "atr", lambda m: fmt(m["atr"], 0))]
    cor = [("barras coloridas (N1)", "n1", lambda m: fmt(m["n1"], 1, pct=True) + " %"),
           ("barras brilhantes (N2)", "n2", lambda m: fmt(m["n2"], 1, pct=True) + " %"),
           ("|F| ≥ 60", "f60", lambda m: fmt(m["f60"], 1, pct=True) + " %"),
           ("|F| ≥ 80", "f80", lambda m: fmt(m["f80"], 1, pct=True) + " %")]
    sinal = [("range seguinte após brilhante ÷ média da hora", "exp", lambda m: f"{fmt(m['exp'])} (t={fmt(m['exp_t'], 1)})"),
             ("retorno alinhado da cor, 1 barra (×ATR)", "ret", lambda m: f"{fmt(m['ret'], 3)} (t={fmt(m['ret_t'], 1)}, acerto {fmt(m['ret_p'], 0, pct=True)} %)"),
             ("autocorrelação do retorno, lag 1", "rho", lambda m: fmt(m["rho"], 3))]
    for tf in TFS:
        if any((tf, n) in tab for n in nomes):
            tabela(tf, cobertura + cor + sinal)

    md.append("## Como ler\n")
    md.append("- **Alarme de volatilidade:** a razão do range seguinte acima de 1, com t alto, repete o que o M01 já mostrou. Se 2026 acompanha as colunas anteriores, o alarme continua válido neste ano.\n")
    md.append("- **Direção:** retorno alinhado perto de zero e acerto perto de 50% significam que a cor não escolhe o lado neste ano, como não escolheu nos anteriores.\n")
    md.append("- **Não comparar pontos entre M26 e Q26.** Os contratos têm níveis de preço diferentes; por isso o retorno está em múltiplos do ATR.\n")
    md.append("- Um número bom só em 2026 não vira parâmetro. Ele precisa aparecer também em 2020-2025 ou ficar marcado como comportamento do ano.\n")
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("gravado", SAIDA.relative_to(RAIZ))


if __name__ == "__main__":
    main()
