"""Auditoria dos CSVs de candles em ``dados/candles``.

Gera:
  * ``dados/catalogo_candles.csv``           — uma linha por arquivo (cobertura, qualidade, flags);
  * ``docs/auditorias/AUDITORIA_DADOS.md``    — relatório legível (regenerado a cada execução).

Uso (a partir da raiz do repositório):
    python ferramentas/auditar_candles.py            # grava os dois arquivos
    python ferramentas/auditar_candles.py --dry-run  # só imprime o resumo
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from tradetech.dados import (  # noqa: E402
    DADOS_CANDLES,
    carregar_arquivo,
    carregar_serie,
    catalogo_arquivos,
    ler_csv_profit,
    problemas_ohlc,
)

SAIDA_CSV = RAIZ / "dados" / "catalogo_candles.csv"
SAIDA_MD = RAIZ / "docs" / "auditorias" / "AUDITORIA_DADOS.md"
LIMITE_EXPORT_LINHAS = 10_000
MIN_FRACAO_SESSAO_COMPLETA = 0.9


def minutos_tf(tf: str) -> int | None:
    if tf.endswith("min"):
        return int(tf[:-3])
    return None


def auditar_arquivo(row: pd.Series) -> dict:
    caminho = Path(row["caminho"])
    bruto = ler_csv_profit(caminho)
    d = bruto.dropna(subset=["dt", "o", "h", "l", "c"])
    dup = int(d["dt"].duplicated().sum())
    d = d.drop_duplicates("dt", keep="last")
    out = {
        "lote": row["lote"],
        "arquivo": row["arquivo"],
        "serie": row["serie"],
        "ativo": row["ativo"],
        "natureza": row["natureza"],
        "variante": row["variante"],
        "tf": row["tf"],
        "linhas": len(bruto),
        "linhas_invalidas": int(len(bruto) - len(d) - dup),
        "timestamps_duplicados": dup,
        "inicio": d["dt"].min().date().isoformat() if len(d) else None,
        "fim": d["dt"].max().date().isoformat() if len(d) else None,
        "md5": hashlib.md5(caminho.read_bytes()).hexdigest()[:10],
    }
    if d.empty:
        return out
    out.update(problemas_ohlc(d))
    out["preco_min"] = float(d["l"].min())
    out["preco_max"] = float(d["h"].max())
    out["preco_inteiro_pct"] = round(float(((d["c"] % 1) == 0).mean() * 100), 1)
    tf_min = minutos_tf(row["tf"])
    if tf_min:
        dia = d["dt"].dt.normalize()
        por_sessao = d.groupby(dia).size()
        ref = por_sessao.quantile(0.95)
        out["sessoes"] = int(len(por_sessao))
        out["barras_por_sessao_mediana"] = float(por_sessao.median())
        out["sessoes_completas"] = int((por_sessao >= MIN_FRACAO_SESSAO_COMPLETA * ref).sum())
        out["sessoes_ralas_pct"] = round(float((por_sessao < MIN_FRACAO_SESSAO_COMPLETA * ref).mean() * 100), 1)
        hh = d["dt"].dt.strftime("%H:%M")
        out["hora_primeira_barra"] = hh.min()
        out["hora_ultima_barra"] = hh.max()
    else:
        out["sessoes"] = int(len(d))
    out["possivel_truncamento_export"] = bool(len(bruto) == LIMITE_EXPORT_LINHAS)
    return out


def fmt_int(x) -> str:
    return f"{int(x):,}".replace(",", ".")


def fmt_num(v) -> str:
    """Formato brasileiro: milhar com ponto, decimal com vírgula."""
    if pd.isna(v):
        return "–"
    if float(v).is_integer():
        return fmt_int(v)
    return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tabela_md(df: pd.DataFrame, cols: list[str], rotulos: dict[str, str] | None = None) -> str:
    rotulos = rotulos or {}
    cab = "| " + " | ".join(rotulos.get(c, c) for c in cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"
    linhas = []
    for _, r in df.iterrows():
        cel = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating, int, np.integer)) and not isinstance(v, (bool, np.bool_)):
                cel.append(fmt_num(v))
            elif isinstance(v, pd.Timestamp):
                cel.append(v.strftime("%Y-%m-%d %H:%M") if (v.hour or v.minute) else v.strftime("%Y-%m-%d"))
            else:
                cel.append("–" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v))
        linhas.append("| " + " | ".join(cel) + " |")
    return "\n".join([cab, sep, *linhas])


def cobertura_liquida(serie: str, tf: str) -> dict | None:
    try:
        d = carregar_serie(serie, tf)
    except FileNotFoundError:
        return None
    dia = d["dt"].dt.normalize()
    n = d.groupby(dia).size()
    ref = n.quantile(0.95)
    ok = n[n >= MIN_FRACAO_SESSAO_COMPLETA * ref]
    if ok.empty:
        return None
    return {
        "serie": serie,
        "tf": tf,
        "sessoes_total": int(len(n)),
        "sessoes_completas": int(len(ok)),
        "primeira_completa": ok.index.min().date().isoformat(),
        "ultima_completa": ok.index.max().date().isoformat(),
    }


def consistencia_entre_tfs(serie: str, base_tf: str, tfs: list[str]) -> list[dict]:
    res = []
    try:
        base = carregar_serie(serie, base_tf).set_index("dt")
    except FileNotFoundError:
        return res
    agg = {"o": "first", "h": "max", "l": "min", "c": "last", "q": "sum"}
    for tf in tfs:
        try:
            alvo = carregar_serie(serie, tf).set_index("dt")
        except FileNotFoundError:
            continue
        m = minutos_tf(tf)
        r = base.drop(columns=["lote"]).resample(f"{m}min", label="left", closed="left").agg(agg).dropna()
        j = r.join(alvo, how="inner", rsuffix="_x")
        if j.empty:
            continue
        iguais = {k: float((j[k] - j[k + "_x"]).abs().lt(1e-6).mean()) for k in agg}
        res.append({"serie": serie, "de": base_tf, "para": tf, "barras_comuns": len(j), **{f"{k}_igual_pct": round(v * 100, 2) for k, v in iguais.items()}})
    return res


def base_ajustada_vs_padrao(serie: str, tf: str) -> dict | None:
    try:
        a = carregar_serie(serie, tf, variante="alt").set_index("dt")
        p = carregar_serie(serie, tf).set_index("dt")
    except FileNotFoundError:
        return None
    j = p.join(a, how="inner", rsuffix="_alt")
    if j.empty:
        return None
    dif = j["c_alt"] - j["c"]
    return {
        "serie": serie,
        "tf": tf,
        "barras_comuns": len(j),
        "dif_fechamento_min": float(dif.min()),
        "dif_fechamento_mediana": float(dif.median()),
        "dif_fechamento_max": float(dif.max()),
        "quantidade_igual_pct": round(float((j["q"] == j["q_alt"]).mean() * 100), 2),
        "inicio": j.index.min().date().isoformat(),
        "fim": j.index.max().date().isoformat(),
    }


def basis_contrato_vs_continuo(contrato: str, continuo: str, tf: str) -> dict | None:
    try:
        c = carregar_serie(contrato, tf).set_index("dt")
        f = carregar_serie(continuo, tf).set_index("dt")
    except FileNotFoundError:
        return None
    j = f.join(c, how="inner", lsuffix="", rsuffix="_ctr")
    if j.empty:
        return None
    dia = j.index.normalize()
    n = j.groupby(dia).size()
    liquidos = n[n >= 0.9 * n.quantile(0.95)].index
    jj = j[dia.isin(liquidos)]
    if jj.empty:
        jj = j
    dif = jj["c_ctr"] - jj["c"]
    return {
        "contrato": contrato,
        "continuo": continuo,
        "tf": tf,
        "barras_comuns": len(j),
        "dias_comuns": int(len(n)),
        "dias_liquidos": int(len(liquidos)),
        "dif_mediana": float(dif.median()),
        "dif_p5": float(dif.quantile(0.05)),
        "dif_p95": float(dif.quantile(0.95)),
        "primeiro_dia_liquido": liquidos.min().date().isoformat() if len(liquidos) else None,
    }


def saltos_overnight(serie: str, limite_pct: float = 1.5) -> pd.DataFrame:
    try:
        d = carregar_serie(serie, "D1")
    except FileNotFoundError:
        return pd.DataFrame()
    d = d.sort_values("dt").reset_index(drop=True)
    d["gap_pct"] = (d["o"] / d["c"].shift(1) - 1) * 100
    return d.loc[d["gap_pct"].abs() >= limite_pct, ["dt", "c", "o", "gap_pct"]]


def barras_extremas(serie: str, tf: str, n: int = 8) -> pd.DataFrame:
    try:
        d = carregar_serie(serie, tf)
    except FileNotFoundError:
        return pd.DataFrame()
    d = d.copy()
    d["rng"] = d["h"] - d["l"]
    d["atr"] = d["rng"].rolling(20).mean().shift(1)
    d["vol_med"] = d["q"].rolling(20).mean().shift(1)
    d["rng_x_atr"] = d["rng"] / d["atr"]
    d["q_x_media"] = d["q"] / d["vol_med"]
    d = d.dropna(subset=["rng_x_atr", "q_x_media"])
    return d.sort_values("q_x_media", ascending=False).head(n)[["dt", "o", "h", "l", "c", "q", "rng", "rng_x_atr", "q_x_media"]]


def montar_relatorio(cat: pd.DataFrame) -> str:
    L: list[str] = []
    a = L.append
    a("# Auditoria dos dados de candles")
    a("")
    a("> **Gerado por** `ferramentas/auditar_candles.py` — não editar à mão; rodar novamente após incluir novos CSVs. Catálogo por arquivo: [`dados/catalogo_candles.csv`](../../dados/catalogo_candles.csv).")
    a("")
    a("## 1. Resumo executivo")
    a("")
    win = cat[(cat["ativo"] == "WIN") & (cat["variante"] == "padrao")]
    wdo = cat[(cat["ativo"] == "WDO") & (cat["variante"] == "padrao")]
    a(f"- {len(cat)} arquivos em `dados/candles/` ({cat['lote'].nunique()} lotes, {cat['serie'].nunique()} séries). WIN: {len(win)} arquivos; WDO: {len(wdo)}.")
    a("- Todos os timestamps são da **abertura** da barra (convenção Profit). Preço/volume usam notação brasileira; o leitor canônico é `src/tradetech/dados.py`.")
    a(f"- Violações OHLC (máx < max(o,c) ou mín > min(o,c)): **{int(cat[['h_invalida','l_invalida']].fillna(0).sum().sum())}**. Timestamps duplicados dentro de arquivo: **{int(cat['timestamps_duplicados'].sum())}**.")
    a("- **Os nomes das pastas antigas (`2012_14`, `2024_26` …) não correspondiam ao conteúdo real**; os lotes foram renomeados pela cobertura verificada (ver §2).")
    a("- A exportação `2024-2025_alt` do WINFUT usa **preço ajustado** (centavos) e fica ~5.700–7.200 pts acima da série padrão: nunca misturar (ver §5).")
    a("")
    a("## 2. Lotes (cobertura real por arquivo mais longo)")
    a("")
    lotes = (
        cat.groupby("lote")
        .agg(arquivos=("arquivo", "count"), series=("serie", lambda s: ", ".join(sorted(set(s)))), inicio=("inicio", "min"), fim=("fim", "max"))
        .reset_index()
    )
    a(tabela_md(lotes, ["lote", "series", "arquivos", "inicio", "fim"], {"series": "séries", "arquivos": "arquivos", "inicio": "início", "fim": "fim"}))
    a("")
    a("Mapa antigo → novo: `2012_14`+`2014_16` → `2014-2015` · `2016_18` → `2016-2017` · `2018_20` → `2018-2019` · `2020_22` → `2020-2021` · `2022_24` → `2022-2023` · `2024_26` → `2024-2025` · `2026` (WINM26/WDOM26) → `2026-1S_M26` · `2026` (WINFUT/WINFUTV com sufixo de datas) e `CandlesHistoricos2026/WINFUT_*` → `2024-2025_alt` · `CandlesHistoricos2026/WINQ26_*` → `2026-2S_Q26`.")
    a("")
    a("## 3. Cobertura útil por timeframe (série padrão, sessões completas)")
    a("")
    a("Sessão completa = pelo menos 90% das barras do percentil 95 de barras/sessão do próprio arquivo. Contratos com vencimento têm início ralo (pouca liquidez) e por isso `sessoes_total` ≠ `sessoes_completas`.")
    a("")
    cob = []
    for serie in ["WINFUT", "WINJ26", "WINM26", "WINQ26", "WDOFUT", "WDOJ26", "WDOM26"]:
        for tf in ["1min", "5min", "10min", "15min", "20min", "30min", "60min", "D1", "W1"]:
            r = cobertura_liquida(serie, tf)
            if r:
                cob.append(r)
    cob = pd.DataFrame(cob)
    # séries contínuas históricas: todos os lotes padrão já entram em carregar_serie
    a(tabela_md(cob, ["serie", "tf", "primeira_completa", "ultima_completa", "sessoes_completas", "sessoes_total"], {"primeira_completa": "1ª sessão completa", "ultima_completa": "última sessão completa", "sessoes_completas": "sessões completas", "sessoes_total": "sessões no arquivo"}))
    a("")
    def sc(serie, tf):
        r = cob[(cob["serie"] == serie) & (cob["tf"] == tf)]
        return int(r["sessoes_completas"].iloc[0]) if len(r) else 0

    n1_fut, n1_q = sc("WINFUT", "1min"), sc("WINQ26", "1min")
    a("**Leituras importantes**")
    a("")
    a(f"- **1 min** (timeframe do robô atual): só existe WINFUT de 2025-09-26 a 2025-12-30 ({n1_fut} sessões completas) e WINQ26 de 2026-02-13 a 2026-07-24, onde só a parte final é líquida ({n1_q} sessões completas). Total ≈ {n1_fut + n1_q} sessões; não há 1 min para 2024, para o WINM26 nem para o WINV26.")
    a("- **5 min contínuo** começa em 2024-06-19; 10/15/20/30/60 min e diário começam em 2014 (60 min/diário), 2018 (20/30 min), 2020 (15 min), 2022 (10 min).")
    a("- Faltam de 2026-05-15 a 2026-06-17 em contrato líquido (WINM26 termina em 2026-05-14) e **tudo após 2026-07-24** (o contrato atual é WINV26; não há CSV).")
    a("- Arquivos com exatamente 10.000 linhas foram truncados pelo limite de exportação do Profit (§4).")
    a("")
    a("## 4. Qualidade por arquivo")
    a("")
    trunc = cat[cat["possivel_truncamento_export"] == True]  # noqa: E712
    a("**Possível truncamento por limite de exportação (10.000 linhas)**")
    a("")
    if trunc.empty:
        a("Nenhum.")
    else:
        a(tabela_md(trunc, ["lote", "arquivo", "linhas", "inicio", "fim"]))
    a("")
    ralas = cat[(cat["sessoes_ralas_pct"].fillna(0) > 20) & (cat["tf"] != "D1") & (cat["tf"] != "W1")]
    a("**Arquivos com > 20% de sessões ralas** (tipicamente contratos ainda sem liquidez):")
    a("")
    a(tabela_md(ralas, ["lote", "arquivo", "sessoes", "sessoes_completas", "sessoes_ralas_pct"], {"sessoes_ralas_pct": "% ralas"}) if len(ralas) else "Nenhum.")
    a("")
    fims = cat[(cat["variante"] == "padrao") & (cat["tf"] != "W1")].groupby(["serie", "lote"])["fim"].agg(["min", "max"]).reset_index()
    fims["dias_diferenca"] = (pd.to_datetime(fims["max"]) - pd.to_datetime(fims["min"])).dt.days
    div = fims[fims["dias_diferenca"] > 3]
    a("**Séries cujos timeframes terminam em datas diferentes** (exportações feitas em momentos distintos; use a interseção ao comparar timeframes):")
    a("")
    if div.empty:
        a("Nenhuma.")
    else:
        a(tabela_md(div, ["serie", "lote", "min", "max", "dias_diferenca"], {"min": "fim mais antigo", "max": "fim mais recente", "dias_diferenca": "dias de diferença"}))
    a("")
    rz = cat[(cat["range_zero"].fillna(0) > 0) & (cat["tf"] == "1min")]
    a("**Barras de 1 min com range zero** (O=H=L=C; ausência de negócio no minuto, não erro):")
    a("")
    a(tabela_md(rz, ["lote", "arquivo", "linhas", "range_zero"]) if len(rz) else "Nenhuma.")
    a("")
    a("## 5. Consistência entre fontes")
    a("")
    a("### 5.1 Entre timeframes (mesma série padrão, agregando o timeframe menor)")
    a("")
    a("Percentual de barras cujo OHLC/quantidade coincide exatamente com a agregação do timeframe menor (rótulo de abertura).")
    a("")
    cons = []
    cons += consistencia_entre_tfs("WINFUT", "1min", ["5min"])
    cons += consistencia_entre_tfs("WINFUT", "5min", ["15min", "30min", "60min"])
    cons += consistencia_entre_tfs("WDOFUT", "1min", ["5min"])
    cons += consistencia_entre_tfs("WDOFUT", "5min", ["15min", "30min", "60min"])
    cons += consistencia_entre_tfs("WINQ26", "1min", ["5min"])
    cons = pd.DataFrame(cons)
    a(tabela_md(cons, ["serie", "de", "para", "barras_comuns", "o_igual_pct", "h_igual_pct", "l_igual_pct", "c_igual_pct", "q_igual_pct"]))
    a("")
    a("Conclusão: preços e quantidade são coerentes entre timeframes. O **volume financeiro** (`Volume`) **não é aditivo** entre timeframes (≈ quantidade × preço × R$ 0,20 com preço de referência específico da barra); para features de volume use `Quantidade` ou o mesmo timeframe de origem.")
    a("")
    a("### 5.2 Série padrão × exportação ajustada (`*_alt`)")
    a("")
    aj = []
    for serie in ["WINFUT"]:
        for tf in ["5min", "10min", "15min", "20min", "30min", "60min", "D1"]:
            r = base_ajustada_vs_padrao(serie, tf)
            if r:
                aj.append(r)
    if aj:
        a(tabela_md(pd.DataFrame(aj), ["serie", "tf", "barras_comuns", "inicio", "fim", "dif_fechamento_min", "dif_fechamento_mediana", "dif_fechamento_max", "quantidade_igual_pct"], {"dif_fechamento_min": "Δ fech. mín", "dif_fechamento_mediana": "Δ fech. mediana", "dif_fechamento_max": "Δ fech. máx", "quantidade_igual_pct": "quantidade igual %"}))
    a("")
    a("A quantidade é idêntica, mas o nível de preço difere em milhares de pontos e a diferença **deriva ao longo do tempo** (ajuste de rolagem). Consequências: (i) pontos de SL/TP e ATR são comparáveis, níveis absolutos não; (ii) misturar as bases cria saltos falsos; (iii) `carregar_serie()` usa só a base padrão por omissão.")
    a("")
    a("### 5.3 Contrato × contínuo (basis)")
    a("")
    bs = []
    for ctr, cont in [("WINJ26", "WINFUT"), ("WDOJ26", "WDOFUT")]:
        for tf in ["5min", "15min"]:
            r = basis_contrato_vs_continuo(ctr, cont, tf)
            if r:
                bs.append(r)
    if bs:
        a(tabela_md(pd.DataFrame(bs), ["contrato", "continuo", "tf", "barras_comuns", "dias_comuns", "dias_liquidos", "primeiro_dia_liquido", "dif_mediana", "dif_p5", "dif_p95"]))
    a("")
    a("O contínuo (`WINFUT`/`WDOFUT`) troca de contrato na rolagem; o contrato explícito (J26, M26, Q26) tem liquidez irregular antes de virar o vencimento mais próximo.")
    a("")
    a("## 6. Saltos de rolagem e gaps overnight (WINFUT, diário)")
    a("")
    sj = saltos_overnight("WINFUT")
    if sj.empty:
        a("Nenhum gap ≥ 1,5%.")
    else:
        a(f"{len(sj)} aberturas com gap ≥ 1,5% sobre o fechamento anterior (rolagens e eventos de mercado se confundem).")
        a("")
        a(tabela_md(sj.tail(15), ["dt", "c", "o", "gap_pct"], {"dt": "data", "c": "fech. anterior", "o": "abertura", "gap_pct": "gap %"}))
    a("")
    a("Rolagens do WIN: meses pares (G, J, M, Q, V, Z), vencimento na quarta-feira mais próxima do dia 15. Estratégias intradiárias não são afetadas; qualquer análise overnight/diária precisa excluir ou ajustar essas datas.")
    a("")
    a("## 7. Barras com volume extremo (para inspeção antes de usar como evidência)")
    a("")
    for serie, tf in [("WINFUT", "1min"), ("WINFUT", "5min"), ("WINM26", "5min"), ("WINQ26", "1min")]:
        ex = barras_extremas(serie, tf, 5)
        if ex.empty:
            continue
        a(f"**{serie} {tf}** — maiores razões quantidade/média(20):")
        a("")
        a(tabela_md(ex, ["dt", "o", "h", "l", "c", "q", "rng_x_atr", "q_x_media"], {"rng_x_atr": "range/ATR20", "q_x_media": "q/média20"}))
        a("")
    a("Picos de volume na abertura (09:00–09:03) e em leilões são esperados; picos fora desses horários merecem checagem de unidade, rolagem ou notícia antes de entrar em estatísticas.")
    a("")
    a("## 8. Recomendações")
    a("")
    a("1. **Exportar 1 min do WINFUT (ou do contrato líquido de cada período) para 2024-01 → 2025-09 e 2026-01 → hoje**; sem isso o motor M02 (1 min) fica com poucas dezenas de sessões líquidas (ver §3).")
    a("2. **Exportar WINV26** (contrato atual) e fechar a janela 2026-05-15 → 2026-06-17 com o contrato líquido (WINM26 até o vencimento).")
    a("3. Padronizar a exportação: sempre **sem ajuste de preço**, sempre incluindo `Quantidade`, um arquivo por (série, timeframe) cobrindo o intervalo total, e anotar o período no nome (`WINFUT_F_0_1min_2024-01-02_2025-12-30.csv`).")
    a("4. Nas análises, usar `tradetech.carregar_serie(serie, tf)`: concatena lotes, remove duplicatas e exclui a base ajustada. Não usar globs recursivos sobre `dados/candles` (misturariam bases).")
    a("5. Preferir `Quantidade` (contratos) a `Volume` financeiro em features de esforço.")
    a("")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cat = catalogo_arquivos()
    linhas = [auditar_arquivo(r) for _, r in cat.iterrows()]
    df = pd.DataFrame(linhas)
    colunas = [
        "lote", "arquivo", "serie", "ativo", "natureza", "variante", "tf", "linhas", "inicio", "fim", "sessoes",
        "sessoes_completas", "sessoes_ralas_pct", "barras_por_sessao_mediana", "hora_primeira_barra", "hora_ultima_barra",
        "h_invalida", "l_invalida", "preco_nao_positivo", "range_zero", "volume_zero", "timestamps_duplicados",
        "linhas_invalidas", "possivel_truncamento_export", "preco_inteiro_pct", "preco_min", "preco_max", "md5",
    ]
    df = df[colunas].sort_values(["ativo", "serie", "tf", "lote"]).reset_index(drop=True)
    rel = montar_relatorio(df)
    if args.dry_run:
        print(rel)
        return
    SAIDA_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SAIDA_CSV, index=False, encoding="utf-8")
    SAIDA_MD.parent.mkdir(parents=True, exist_ok=True)
    SAIDA_MD.write_text(rel, encoding="utf-8")
    print(f"catálogo: {SAIDA_CSV.relative_to(RAIZ)} ({len(df)} arquivos)")
    print(f"relatório: {SAIDA_MD.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
