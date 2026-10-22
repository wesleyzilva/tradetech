"""Biblioteca compartilhada do repositório TradeTech (dados de candles e utilitários de estudo)."""

from .dados import (  # noqa: F401
    DADOS_CANDLES,
    RAIZ_REPO,
    carregar_arquivo,
    carregar_serie,
    catalogo_arquivos,
    ler_csv_profit,
)
