"""ANALISE_001 do motor M02 — o robô ``Robo_Microestrutura_Barreiras_v1`` tem vantagem nos candles que temos?

Regenera ``analises/ANALISE_001_baseline.md`` e ``analises/ANALISE_001_trades.csv``.

Uso (a partir da raiz do repositório):
    python motores/M02_microestrutura_barreiras/codigo/analise_001.py [--reps 100]

Tudo em pontos de WIN (1 ponto = R$ 0,20 por contrato). Nada é otimizado: os parâmetros são os do fonte NTSL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import mb_motor as mb  # noqa: E402
from tradetech.dados import carregar_serie  # noqa: E402

PASTA = RAIZ / "motores" / "M02_microestrutura_barreiras" / "analises"
MD = PASTA / "ANALISE_001_baseline.md"
CSV = PASTA / "ANALISE_001_trades.csv"

CUSTOS = (0.0, 2.0, 5.0)
HORIZONTES = (1, 5, 10, 20)


def so_sessoes_completas(d: pd.DataFrame, frac: float = 0.9) -> pd.DataFrame:
    """Mantém sessões com >= ``frac`` das barras do p95 de barras/sessão (descarta início ralo de contrato)."""
    dia = d["dt"].dt.normalize()
    n = d.groupby(dia).size()
    ok = n[n >= frac * n.quantile(0.95)].index
    return d[dia.isin(ok)].reset_index(drop=True)


def carregar(serie: str, tf: str, inicio: str | None = None) -> pd.DataFrame:
    d = so_sessoes_completas(carregar_serie(serie, tf))
    if inicio:
        d = d[d["dt"] >= inicio].reset_index(drop=True)
    return d


def fmt(x, casas=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    if isinstance(x, (int, np.integer)):
        return f"{x:,}".replace(",", ".")
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tabela(linhas: list[dict], colunas: list[str]) -> str:
    out = ["| " + " | ".join(colunas) + " |", "|" + "|".join("---" for _ in colunas) + "|"]
    for l in linhas:
        out.append("| " + " | ".join(str(l.get(c, "")) for c in colunas) + " |")
    return "\n".join(out)


def linha_metricas(nome: str, t: pd.DataFrame) -> dict:
    m = mb.metricas(t)
    if m["n"] == 0:
        return {"cenário": nome, "n": 0}
    return {
        "cenário": nome,
        "n": fmt(m["n"]),
        "pregões": fmt(m["pregoes"]),
        "trades/pregão": fmt(m["trades_por_pregao"], 1),
        "WR %": fmt(100 * m["win_rate"], 1),
        "WR breakeven %": fmt(100 * m["wr_breakeven"], 1),
        "médio (pts)": fmt(m["pnl_medio"]),
        "PF": fmt(m["profit_factor"]),
        "t (pregão)": fmt(m["t_pregao"]),
        "total (pts)": fmt(m["pnl_total"], 0),
        "DD máx (pts)": fmt(m["max_dd"], 0),
        "pior (pts)": fmt(m["pior_trade"], 0),
    }


COLS_M = ["cenário", "n", "pregões", "trades/pregão", "WR %", "WR breakeven %", "médio (pts)", "PF", "t (pregão)", "total (pts)", "DD máx (pts)", "pior (pts)"]


def agrupar(t: pd.DataFrame, chave: str, rotulos: dict | None = None) -> list[dict]:
    linhas = []
    for k, g in t.groupby(chave):
        m = mb.metricas(g)
        linhas.append(
            {
                chave: (rotulos or {}).get(k, k),
                "n": fmt(m["n"]),
                "WR %": fmt(100 * m["win_rate"], 1),
                "médio (pts)": fmt(m["pnl_medio"]),
                "PF": fmt(m["profit_factor"]),
                "total (pts)": fmt(m["pnl_total"], 0),
                "pior (pts)": fmt(m["pior_trade"], 0),
            }
        )
    return linhas


def retornos_futuros(d: pd.DataFrame, p: mb.Params) -> list[dict]:
    """Hipótese MB-H01: o estado (barra escura/brilhante) tem retorno futuro diferente do incondicional?

    Retorno medido da abertura da barra seguinte (o que o robô consegue executar) até o fechamento de ``h`` barras
    depois, dentro do mesmo pregão. Média e t-stat agrupados por pregão (dependência intradia).
    """
    d = d.copy()
    na_janela = mb.janela_ativa(d["hhmm"].to_numpy(), p)
    o_prox = d["o"].shift(-1)
    linhas = []
    nomes = {0: "neutro", 1: "escuro alta", 2: "escuro baixa", 3: "brilhante alta", 4: "brilhante baixa"}
    for h in HORIZONTES:
        fut = d["c"].shift(-h) - o_prox
        mesmo_dia = d["dia"].shift(-h) == d["dia"]
        r = fut.where(mesmo_dia & na_janela)
        base = r.mean()
        for est, nome in nomes.items():
            sel = r[d["est"] == est].dropna()
            if len(sel) < 30:
                continue
            dif = (r.where(d["est"] == est) - base).groupby(d["dia"]).sum(min_count=1).fillna(0.0)
            dif = dif[d.groupby("dia")["dia"].size().reindex(dif.index).notna()]
            t = dif.mean() / (dif.std(ddof=1) / np.sqrt(len(dif))) if len(dif) > 2 and dif.std(ddof=1) > 0 else np.nan
            linhas.append(
                {
                    "h (barras)": h,
                    "estado": nome,
                    "n": fmt(len(sel)),
                    "retorno médio (pts)": fmt(sel.mean()),
                    "incondicional (pts)": fmt(base),
                    "diferença (pts)": fmt(sel.mean() - base),
                    "t (pregão)": fmt(t),
                }
            )
    return linhas


def retorno_alinhado_sinais(d: pd.DataFrame, ctx: int) -> list[dict]:
    """Retorno alinhado ao lado do sinal (entrada na abertura seguinte), para todos os sinais do contexto ``ctx``."""
    o_prox = d["o"].shift(-1)
    sel = (d["ctx"] == ctx) & (d["sinal"] != 0)
    linhas = []
    for h in HORIZONTES:
        fut = (d["c"].shift(-h) - o_prox) * d["sinal"]
        ok = sel & (d["dia"].shift(-h) == d["dia"])
        r = fut.where(ok)
        por_dia = r.groupby(d["dia"]).sum(min_count=1).fillna(0.0)
        t = por_dia.mean() / (por_dia.std(ddof=1) / np.sqrt(len(por_dia))) if por_dia.std(ddof=1) > 0 else np.nan
        x = r.dropna()
        linhas.append({"h (barras)": h, "n sinais": fmt(len(x)), "retorno alinhado médio (pts)": fmt(x.mean()),
                       "% positivos": fmt(100 * (x > 0).mean(), 1), "t (pregão)": fmt(t)})
    return linhas


def pctl(valor: float, amostra: pd.Series) -> float:
    return 100 * float((amostra < valor).mean())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=100)
    args = ap.parse_args()

    p_fiel = mb.Params()
    p_ideal = mb.com(p_fiel, protecao_na_barra_de_entrada=True)

    conj = {
        "WINFUT 1min": carregar("WINFUT", "1min"),
        "WINQ26 1min": carregar("WINQ26", "1min"),
    }
    conj_5 = {
        "WINFUT 5min": carregar("WINFUT", "5min"),
        "WINM26 5min": carregar("WINM26", "5min"),
        "WINQ26 5min": carregar("WINQ26", "5min"),
    }

    md: list[str] = []
    w = md.append
    todos_trades = []

    resultados = {}
    for nome, d in {**conj, **conj_5}.items():
        for perfil, p in (("fiel", p_fiel), ("ideal", p_ideal)):
            dd, t = mb.rodar(d, p)
            t["conjunto"] = nome
            t["perfil"] = perfil
            resultados[(nome, perfil)] = (dd, t)
            todos_trades.append(t)

    # ---------------------------------------------------------------- cabeçalho
    w("# ANALISE_001 — Baseline do motor M02 (Robo_Microestrutura_Barreiras_v1)\n")
    w("> Gerado por `motores/M02_microestrutura_barreiras/codigo/analise_001.py`. **Não edite à mão**: reexecute o script.\n")
    w("## 1. Pergunta\n")
    w("O robô, exatamente como está no fonte NTSL de 22/10/2026, tem vantagem estatística nos candles de WIN que temos? "
      "Nenhum parâmetro foi otimizado: a réplica (`mb_motor.py`, validada por `tests/test_mb_motor.py`) usa os valores do fonte.\n")
    w("## 2. Dados usados\n")
    linhas = []
    for nome, d in {**conj, **conj_5}.items():
        linhas.append({"conjunto": nome, "barras": fmt(len(d)), "pregões completos": fmt(d["dt"].dt.normalize().nunique()),
                       "início": d["dt"].min().date(), "fim": d["dt"].max().date()})
    w(tabela(linhas, ["conjunto", "barras", "pregões completos", "início", "fim"]))
    w("\nSó entram pregões com ≥ 90 % das barras do p95 (descarta início ralo de contrato). Série **padrão** (sem `_alt`). "
      "O robô foi desenhado para 1 min: só há ~99 pregões nesse timeframe (ver `docs/auditorias/AUDITORIA_DADOS.md`). "
      "O 5 min entra como teste de **escala/robustez**, não como validação do robô (20 barras de 5 min = 100 min).\n")
    w("**Convenções da simulação:** sinal no fechamento → entrada na abertura seguinte; stop e alvo recalculados a cada barra "
      "(logo a barra de entrada fica sem proteção no perfil *fiel*; o perfil *ideal* assume ordens ativas desde a abertura); "
      "stop antes do alvo na mesma barra; custo e slippage em pontos por trade (aqui 0 salvo onde dito). Ver `METODO.md`.\n")

    # ---------------------------------------------------------------- baseline
    w("## 3. Resultado bruto (sem custos)\n")
    linhas = []
    for (nome, perfil), (_, t) in resultados.items():
        linhas.append(linha_metricas(f"{nome} — {perfil}", t))
    w(tabela(linhas, COLS_M))
    w("\n**Leitura:** `WR breakeven` é a taxa de acerto necessária dado o payoff observado; o robô fica abaixo dela quando "
      "`WR %` < `WR breakeven %`. `t (pregão)` agrega o PnL por pregão (cluster) — |t| < 2 não se distingue de ruído.\n")

    # ---------------------------------------------------------------- custos
    w("## 4. Sensibilidade a custos (perfil fiel)\n")
    linhas = []
    for nome, d in conj.items():
        dd = resultados[(nome, "fiel")][0]
        for c in CUSTOS:
            t = mb.simular(dd, mb.com(p_fiel, custo_pts=c))
            linhas.append(linha_metricas(f"{nome} — custo {fmt(c, 0)} pt", t))
    w(tabela(linhas, COLS_M))
    w("\nCusto realista de WIN (corretagem + emolumentos + slippage de uma ponta a mercado) fica na ordem de 2–5 pontos por "
      "volta; com ~30 trades por pregão o custo come toda a margem mesmo se houvesse edge bruto.\n")

    # ---------------------------------------------------------------- decomposição
    base = pd.concat([resultados[(n, "fiel")][1] for n in conj], ignore_index=True)
    w("## 5. Decomposição (WINFUT + WINQ26 1 min, perfil fiel, sem custo)\n")
    w("### 5.1 Por contexto\n")
    w("Contexto 1 = fade de alta brilhante (vende); 2 = fade de baixa brilhante (compra); 3 = rompimento em fluxo neutro com SMA20.\n")
    w(tabela(agrupar(base, "ctx", {1: "1 — fade alta", 2: "2 — fade baixa", 3: "3 — fluxo neutro"}), ["ctx", "n", "WR %", "médio (pts)", "PF", "total (pts)", "pior (pts)"]))
    sinais = pd.concat([resultados[(n, "fiel")][0] for n in conj], ignore_index=True)
    cont = sinais.loc[sinais["sinal"] != 0, "ctx"].value_counts().sort_index()
    w("\nSinais **gerados** (antes de descartar os que chegam com posição aberta): "
      + ", ".join(f"ctx {k}: {fmt(int(v))}" for k, v in cont.items())
      + ". Os fades (ctx 1 e 2) quase nunca disparam porque exigem *rompimento da mínima/máxima da barra brilhante já no fechamento da barra seguinte*; "
        "na prática o robô é um rompedor de fluxo neutro com SMA20.\n")
    w("\n### 5.2 Por motivo de saída\n")
    w(tabela(agrupar(base, "motivo"), ["motivo", "n", "WR %", "médio (pts)", "PF", "total (pts)", "pior (pts)"]))
    w("\n`STOP_PASSIVO` = stop-limit enviado quando o fechamento já estava além do limite (a ordem fica passiva e só executa se o "
      "preço voltar): é a **armadilha do stop-limit** — a perda realizada excede em muito o SL nominal. "
      "`SL` e `SG` são as barreiras normais; `TEMPO` é a barreira temporal de 20 barras.\n")
    n_pass = int((base["motivo"] == "STOP_PASSIVO").sum())
    perda_pass = base.loc[base["motivo"] == "STOP_PASSIVO", "pnl"].sum()
    w(f"Saídas por `STOP_PASSIVO`: **{fmt(n_pass)}** trades ({fmt(100 * n_pass / len(base), 1)} % do total) somam **{fmt(perda_pass, 0)} pts**; "
      f"o PnL total do robô é {fmt(base['pnl'].sum(), 0)} pts.\n")
    arm = base[base["armadilha"]]
    sem = base[~base["armadilha"]]
    w("Trades em que o stop-limit chegou a ficar **passivo** em algum momento (armadilha), saindo por qualquer motivo:\n")
    w(tabela([
        {"grupo": "com armadilha", "n": fmt(len(arm)), "médio (pts)": fmt(arm["pnl"].mean()), "total (pts)": fmt(arm["pnl"].sum(), 0), "pior (pts)": fmt(arm["pnl"].min(), 0)},
        {"grupo": "sem armadilha", "n": fmt(len(sem)), "médio (pts)": fmt(sem["pnl"].mean()), "total (pts)": fmt(sem["pnl"].sum(), 0), "pior (pts)": fmt(sem["pnl"].min(), 0)},
    ], ["grupo", "n", "médio (pts)", "total (pts)", "pior (pts)"]))
    w("")
    w("### 5.3 Por lado\n")
    w(tabela(agrupar(base, "lado", {1: "compra", -1: "venda"}), ["lado", "n", "WR %", "médio (pts)", "PF", "total (pts)", "pior (pts)"]))
    w("\n### 5.4 Por hora de entrada\n")
    base = base.assign(hora=(base["hhmm_entrada"] // 100).astype(int))
    w(tabela(agrupar(base, "hora"), ["hora", "n", "WR %", "médio (pts)", "PF", "total (pts)", "pior (pts)"]))
    w("\n### 5.5 Distância do stop\n")
    sl_floor = (base["sl_pts"] <= p_fiel.sl_min).mean() * 100
    w(f"O stop nominal é `max(0,5×ATR, 35)`. Em **{fmt(sl_floor, 1)} %** dos trades o piso de 35 pts é o que vale "
      f"(ATR1min mediano na entrada = {fmt(base['atr_sinal'].median(), 1)} pts; SL mediano = {fmt(base['sl_pts'].median(), 0)} pts; SG mediano = {fmt(base['sg_pts'].median(), 0)} pts). "
      "Um stop dessa ordem em 1 min está dentro do ruído de uma única barra.\n")
    mae_ult = (base["mae"] >= base["sl_pts"]).mean() * 100
    w(f"MAE ≥ SL em {fmt(mae_ult, 1)} % dos trades; MFE ≥ SG em {fmt(100 * (base['mfe'] >= base['sg_pts']).mean(), 1)} %.\n")

    # ---------------------------------------------------------------- controle aleatório
    w("## 6. Controle: entrada aleatória com a mesma saída\n")
    w(f"Mesmas janelas, mesma frequência de sinais, lado sorteado, **mesma geometria de saída** (SL/SG/tempo, perfil fiel); {args.reps} repetições. "
      "Se o robô não supera esse controle, o desempenho vem da geometria de saída e do custo, não do sinal.\n")
    linhas = []
    for nome in conj:
        dd, t = resultados[(nome, "fiel")]
        nulo = mb.aleatorio_mesma_saida(dd, p_fiel, n_rep=args.reps)
        m = mb.metricas(t)
        linhas.append({
            "conjunto": nome,
            "robô: médio (pts)": fmt(m["pnl_medio"]),
            "nulo: média": fmt(nulo["pnl_medio"].mean()),
            "nulo p5": fmt(nulo["pnl_medio"].quantile(0.05)),
            "nulo p95": fmt(nulo["pnl_medio"].quantile(0.95)),
            "percentil do robô": fmt(pctl(m["pnl_medio"], nulo["pnl_medio"]), 0),
            "robô: PF": fmt(m["profit_factor"]),
            "nulo: PF médio": fmt(nulo["profit_factor"].mean()),
        })
    w(tabela(linhas, ["conjunto", "robô: médio (pts)", "nulo: média", "nulo p5", "nulo p95", "percentil do robô", "robô: PF", "nulo: PF médio"]))
    w("\nPercentil do robô acima de 95 indicaria sinal; abaixo de 5, sinal *pior* que o acaso.\n")

    # ---------------------------------------------------------------- por contexto vs nulo (isolando sinais)
    w("## 7. Teste de hipótese de sinal: retorno futuro por estado (MB-H01)\n")
    w("Independente das barreiras: retorno da abertura da barra seguinte até o fechamento `h` barras depois, só dentro das janelas "
      "de entrada, por estado da barra de sinal. Se os fades (brilhante alta → cair; brilhante baixa → subir) existissem, "
      "`brilhante alta` teria retorno **negativo** e `brilhante baixa` **positivo**, com |t| ≥ 3.\n")
    dd1 = resultados[("WINFUT 1min", "fiel")][0]
    dd2 = resultados[("WINQ26 1min", "fiel")][0]
    juntos = pd.concat([dd1, dd2], ignore_index=True)
    w(tabela(retornos_futuros(juntos, p_fiel), ["h (barras)", "estado", "n", "retorno médio (pts)", "incondicional (pts)", "diferença (pts)", "t (pregão)"]))
    w("\n**Replicação por conjunto** (só estados brilhantes; 20 testes na tabela acima ⇒ um |t| ≈ 3 isolado não basta, "
      "o que importa é o sinal repetir em conjuntos independentes):\n")
    linhas = []
    for nome, d in {**conj, **conj_5}.items():
        for l in retornos_futuros(resultados[(nome, "fiel")][0], p_fiel):
            if l["estado"].startswith("brilhante") and l["h (barras)"] in (1, 5, 10):
                linhas.append({"conjunto": nome, **l})
    w(tabela(linhas, ["conjunto", "h (barras)", "estado", "n", "diferença (pts)", "t (pregão)"]))
    w("\nCritério (`docs/01_CONVENCOES.md`): mesmo sinal em ≥ 2 conjuntos independentes, |t| ≥ 3 na descoberta e |t| ≥ 2 no teste. "
      "O `t (pregão)` aqui é a média por pregão da soma dos desvios dos eventos em relação ao incondicional (pregões sem evento contam zero). "
      "A interpretação fica em `HIPOTESES.md` (MB-H01).\n")

    w("### 7.1 Retorno alinhado dos sinais do contexto 3 (MB-H02)\n")
    w("Todos os sinais de fluxo neutro (não só os que viram trade), retorno na direção do sinal da abertura seguinte até `h` barras depois. "
      "Positivo = o rompimento tem continuação; zero ou negativo = não há edge direcional antes das barreiras.\n")
    linhas = []
    for nome in {**conj, **conj_5}:
        for l in retorno_alinhado_sinais(resultados[(nome, "fiel")][0], 3):
            linhas.append({"conjunto": nome, **l})
    w(tabela(linhas, ["conjunto", "h (barras)", "n sinais", "retorno alinhado médio (pts)", "% positivos", "t (pregão)"]))
    w("")

    # ---------------------------------------------------------------- escala
    w("## 8. Teste de escala (5 min)\n")
    w("Mesmos parâmetros em barras de 5 min (ATR 5× maior, pisos de 35/120 pts irrelevantes, 20 barras = 100 min). "
      "Não valida o robô, mas diz se o conceito (fade de barra brilhante, rompimento neutro) sobrevive a uma escala em que o piso de stop não domina.\n")
    linhas = []
    for nome in conj_5:
        for perfil in ("fiel", "ideal"):
            linhas.append(linha_metricas(f"{nome} — {perfil}", resultados[(nome, perfil)][1]))
    w(tabela(linhas, COLS_M))
    w("")

    # ---------------------------------------------------------------- estabilidade temporal
    w("## 9. Estabilidade temporal (perfil fiel, sem custo)\n")
    linhas = []
    for nome in conj:
        t = resultados[(nome, "fiel")][1].sort_values("dt_entrada")
        meio = t["dia"].sort_values().unique()
        corte = meio[len(meio) // 2]
        linhas.append(linha_metricas(f"{nome} — 1ª metade", t[t["dia"] < corte]))
        linhas.append(linha_metricas(f"{nome} — 2ª metade", t[t["dia"] >= corte]))
    w(tabela(linhas, COLS_M))
    w("")

    # ---------------------------------------------------------------- conclusões automáticas
    m_f = mb.metricas(resultados[("WINFUT 1min", "fiel")][1])
    m_q = mb.metricas(resultados[("WINQ26 1min", "fiel")][1])
    w("## 10. Conclusões desta análise\n")
    w(f"1. **Sem vantagem bruta.** Perfil fiel, sem custo: média de {fmt(m_f['pnl_medio'])} pts/trade (WINFUT) e {fmt(m_q['pnl_medio'])} pts/trade (WINQ26); "
      f"t por pregão de {fmt(m_f['t_pregao'])} e {fmt(m_q['t_pregao'])}. Com custo, só piora (seção 4).")
    w("2. **Frequência excessiva** (dezenas de trades por pregão) multiplica o custo; a barreira de 35 pts é ruído em 1 min.")
    w("3. **Risco estrutural de execução**: a barra de entrada sem proteção e o stop-limit passivo geram perdas muito maiores que o SL nominal (seção 5.2).")
    w("4. **O controle aleatório** (seção 6) separa o efeito do sinal do efeito da geometria de saída.")
    w("5. **As hipóteses de fade** (MB-H01, seção 7) devem ser lidas com o limiar |t| ≥ 3 do `docs/01_CONVENCOES.md`; "
      "todas as cifras acima são **amostras curtas** (≈ 99 pregões de 1 min) e não substituem uma validação com mais dados.")
    w("\n## 11. Limitações\n")
    w("- Amostra de 1 min: 64 + 35 pregões; os resultados têm largura de intervalo grande.\n"
      "- Candles sem fila de ordens: não se sabe se o stop-limit realmente executaria; o modelo é pessimista (fiel) ou otimista (ideal), e a verdade está entre os dois.\n"
      "- `Time` do NTSL assumido igual ao horário de abertura da barra do CSV.\n"
      "- Preços de contratos distintos (WINFUT contínuo × WINQ26) são tratados separadamente; não há rolagem dentro de um mesmo conjunto 1 min.\n"
      "- Volume do CSV é financeiro, não usado por este motor.\n")
    w("## 12. Próximos deltas sugeridos\n")
    w("Registrados em `HIPOTESES.md` (IDs `MB-H*`) com status; cada delta deve criar `deltas/DELTA_NNN_*.md` a partir do template `docs/templates/DELTA.md`.\n")

    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    pd.concat(todos_trades, ignore_index=True).to_csv(CSV, index=False, sep=";", decimal=",", float_format="%.2f")
    print(f"gravado {MD.relative_to(RAIZ)} e {CSV.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
