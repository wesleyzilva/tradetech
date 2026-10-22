"""Leitura canônica dos CSVs exportados pelo Profit/Nelogica.

Formato bruto (separador ``;``, latin-1, linhas em ordem decrescente de data):

    Ativo;Data;Hora;Abertura;Máximo;Mínimo;Fechamento;Volume;Quantidade      (intradiário)
    Ativo;Data;Abertura;Máximo;Mínimo;Fechamento;Volume;Quantidade           (diário/semanal)

* O timestamp é o da **abertura** da barra (convenção Profit).
* Preço e volume usam notação brasileira (``167.093`` = 167093; ``5.597,894``; ``174830,00``).
* ``Volume`` é financeiro (R$); ``Quantidade`` é número de contratos.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

RAIZ_REPO = Path(__file__).resolve().parents[2]
DADOS_CANDLES = RAIZ_REPO / "dados" / "candles"

COLUNAS_INTRADIA = ["ativo", "data", "hora", "o", "h", "l", "c", "v", "q"]
COLUNAS_DIARIO = ["ativo", "data", "o", "h", "l", "c", "v", "q"]

_RE_NOME = re.compile(r"^(?P<serie>[A-Z0-9]+)_F_0_(?P<tf>[^_.]+)(?P<sufixo>_.+)?\.csv$", re.IGNORECASE)


def numero_br(serie: pd.Series) -> pd.Series:
    """Converte strings em notação brasileira para float (ponto = milhar, vírgula = decimal)."""
    s = serie.astype(str).str.strip()
    cientifico = s.str.contains("E", case=False, regex=False)
    limpo = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    sci = s.str.replace(",", ".", regex=False)
    return pd.to_numeric(limpo.where(~cientifico, sci), errors="coerce")


def ler_csv_profit(caminho: str | Path) -> pd.DataFrame:
    """Lê um CSV Profit e devolve colunas ``dt,o,h,l,c,v,q`` ordenadas por ``dt`` (sem remover duplicatas)."""
    bruto = pd.read_csv(caminho, sep=";", encoding="latin-1", dtype=str, header=None)
    if bruto.empty:
        return pd.DataFrame(columns=["dt", "o", "h", "l", "c", "v", "q"])
    if str(bruto.iloc[0, 0]).strip().lower() == "ativo":
        bruto = bruto.iloc[1:]
    intradia = bruto.shape[1] >= 9
    bruto = bruto.iloc[:, : 9 if intradia else 8]
    bruto.columns = COLUNAS_INTRADIA if intradia else COLUNAS_DIARIO
    if intradia:
        carimbo = bruto["data"].str.strip() + " " + bruto["hora"].str.strip()
        dt = pd.to_datetime(carimbo, format="%d/%m/%Y %H:%M:%S", errors="coerce")
        if dt.isna().mean() > 0.5:
            dt = pd.to_datetime(carimbo, format="%d/%m/%Y %H:%M", errors="coerce")
    else:
        dt = pd.to_datetime(bruto["data"].str.strip(), format="%d/%m/%Y", errors="coerce")
    saida = pd.DataFrame({"dt": dt, **{k: numero_br(bruto[k]) for k in ("o", "h", "l", "c", "v", "q")}})
    return saida.sort_values("dt", kind="stable").reset_index(drop=True)


def carregar_arquivo(caminho: str | Path) -> pd.DataFrame:
    """Como :func:`ler_csv_profit`, porém descartando linhas inválidas e timestamps duplicados (mantém o último)."""
    d = ler_csv_profit(caminho)
    d = d.dropna(subset=["dt", "o", "h", "l", "c"])
    return d.drop_duplicates("dt", keep="last").reset_index(drop=True)


def descrever_nome(caminho: str | Path) -> dict:
    """Extrai série, timeframe e sufixo do nome de arquivo no padrão ``<SERIE>_F_0_<TF>[_sufixo].csv``."""
    nome = Path(caminho).name
    m = _RE_NOME.match(nome)
    if not m:
        return {"serie": None, "tf": None, "sufixo": None}
    tf = m.group("tf").replace("Diário", "D1").replace("Diario", "D1").replace("Semanal", "W1")
    return {"serie": m.group("serie").upper(), "tf": tf, "sufixo": (m.group("sufixo") or "").lstrip("_") or None}


def classificar_serie(serie: str) -> dict:
    """Ativo (WIN/WDO) e natureza da série (contínua ``FUT``/``FUTV`` ou contrato com vencimento)."""
    ativo = serie[:3]
    resto = serie[3:]
    if resto == "FUT":
        natureza = "continuo"
    elif resto == "FUTV":
        natureza = "continuo_alt_volume"
    else:
        natureza = "contrato"
    return {"ativo": ativo, "natureza": natureza}


def catalogo_arquivos(raiz: Path | None = None) -> pd.DataFrame:
    """Lista todos os CSVs em ``dados/candles/<lote>/`` com metadados de nome (lote, série, tf, caminho)."""
    raiz = Path(raiz or DADOS_CANDLES)
    linhas = []
    for caminho in sorted(raiz.glob("*/*.csv")):
        info = descrever_nome(caminho)
        if info["serie"] is None:
            continue
        linhas.append(
            {
                "lote": caminho.parent.name,
                "arquivo": caminho.name,
                "caminho": caminho,
                **info,
                **classificar_serie(info["serie"]),
                "variante": "alt" if caminho.parent.name.endswith("_alt") else "padrao",
            }
        )
    return pd.DataFrame(linhas)


def carregar_serie(
    serie: str,
    tf: str,
    lotes: list[str] | None = None,
    raiz: Path | None = None,
    sufixo: str | None = None,
    variante: str = "padrao",
    liquido: bool = True,
) -> pd.DataFrame:
    """Concatena todos os lotes de ``serie``/``tf`` em uma única série ascendente e sem timestamps duplicados.

    Em caso de timestamp repetido entre lotes, vale o lote que aparece **por último** em ``lotes``
    (por padrão, ordem alfabética de lote, que coincide com a ordem cronológica).
    ``variante="padrao"`` exclui os lotes ``*_alt`` (exportação alternativa do WINFUT com preços **ajustados**,
    ~6.500-7.100 pts acima da série padrão em set-dez/2025): misturar as duas bases cria saltos falsos.
    A coluna ``lote`` identifica a origem de cada barra. Diferente do carregador legado de ``teses/cores``,
    isto **concatena** os lotes em vez de usar apenas o primeiro arquivo encontrado.
    """
    cat = catalogo_arquivos(raiz)
    if cat.empty:
        raise FileNotFoundError("nenhum CSV em dados/candles")
    sel = cat[(cat["serie"] == serie.upper()) & (cat["tf"] == tf)]
    sel = sel[sel["sufixo"].fillna("") == (sufixo or "")]
    sel = sel[sel["variante"] == variante]
    if lotes is not None:
        ordem = {l: i for i, l in enumerate(lotes)}
        sel = sel[sel["lote"].isin(ordem)].assign(_o=lambda x: x["lote"].map(ordem)).sort_values("_o")
    if sel.empty:
        raise FileNotFoundError(f"sem arquivos para {serie}/{tf} (lotes={lotes})")
    partes = []
    for _, r in sel.iterrows():
        d = carregar_arquivo(r["caminho"])
        d["lote"] = r["lote"]
        partes.append(d)
    todo = pd.concat(partes, ignore_index=True)
    todo = todo.drop_duplicates("dt", keep="last").sort_values("dt").reset_index(drop=True)
    if liquido and classificar_serie(serie.upper())["natureza"] == "contrato" and serie.upper().startswith("WIN"):
        todo = sessoes_liquidas(todo)
    return todo


QTD_MIN_WIN = 1_000_000


def sessoes_liquidas(d: pd.DataFrame, minimo: float = QTD_MIN_WIN) -> pd.DataFrame:
    """Mantém só os pregões com ``Quantidade`` diária ≥ ``minimo`` (padrão: 1 milhão de contratos, WIN).

    Um contrato com vencimento fora da janela líquida quase não negocia (WINM26 em jan–mar/2026: 68 a 17 mil por dia; em abril, 9 milhões),
    e as barras desses pregões têm preço parado e volume sem relação com o contrato líquido. A série contínua ``WINFUT`` já costura o contrato líquido.
    """
    dia = d["dt"].dt.normalize()
    q = d.groupby(dia)["q"].transform("sum")
    return d[q >= minimo].reset_index(drop=True)


def sessoes(d: pd.DataFrame) -> pd.Series:
    """Data (normalizada) de cada barra, usada como identificador de pregão."""
    return d["dt"].dt.normalize()


def problemas_ohlc(d: pd.DataFrame) -> dict:
    """Contagem de violações básicas de consistência OHLC."""
    h_ok = d["h"] >= d[["o", "c", "l"]].max(axis=1) - 1e-9
    l_ok = d["l"] <= d[["o", "c", "h"]].min(axis=1) + 1e-9
    return {
        "h_invalida": int((~h_ok).sum()),
        "l_invalida": int((~l_ok).sum()),
        "preco_nao_positivo": int((d[["o", "h", "l", "c"]] <= 0).any(axis=1).sum()),
        "range_zero": int((d["h"] == d["l"]).sum()),
        "volume_zero": int((d["v"].fillna(0) <= 0).sum()),
    }


__all__ = [
    "DADOS_CANDLES",
    "RAIZ_REPO",
    "carregar_arquivo",
    "carregar_serie",
    "catalogo_arquivos",
    "classificar_serie",
    "descrever_nome",
    "sessoes_liquidas",
    "ler_csv_profit",
    "numero_br",
    "problemas_ohlc",
    "sessoes",
]
