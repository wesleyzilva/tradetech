"""Implementação experimental das hipóteses de área.

Este módulo é descritivo. Não possui regras de entrada, SL, SG, risco,
quantidade ou decisão operacional.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class AreaEvento:
    """Referencia mínima de um evento dentro de uma área."""
    dt: str
    ativo: str
    timeframe: str
    familia: int
    origem: str
    area_min: float
    area_max: float
    n_candles: int


def listar_exemplos(pasta: Path) -> list[Path]:
    """Lista exemplos de área disponíveis no diretório de imagens ou resultados."""
    return sorted(pasta.glob("**/*"))


def validar_evento(evento: AreaEvento) -> bool:
    """Validação básica do evento, sem definir operação."""
    return all(
        [
            evento.dt,
            evento.ativo,
            evento.timeframe,
            evento.area_min <= evento.area_max,
            evento.n_candles > 0,
            evento.familia in {-2, -1, 0, 1, 2},
        ]
    )


def confirmar_serie(eventos: Iterable[AreaEvento]) -> dict[str, object]:
    """Calcula somente métricas descritivas da cadeia de confirmações."""
    itens = list(eventos)
    if not itens:
        return {
            "n_eventos": 0,
            "n_confirmados": 0,
            "taxa_confirmacao": 0.0,
            "familias": {},
        }

    return {
        "n_eventos": len(itens),
        "n_confirmados": len(itens),
        "taxa_confirmacao": 1.0,
        "familias": {str(familia): sum(1 for e in itens if e.familia == familia) for familia in sorted({e.familia for e in itens})},
    }


def medir_confirmacao_area(
    eventos: pd.DataFrame,
    menores: pd.DataFrame,
    tamanho_intervalo_minutos: int,
) -> dict[str, object]:
    """Conta a família maior dentro da área temporal e de preço do evento.

    A confirmação exige que o candle menor ocorra na janela de duração igual
    imediatamente posterior ao fechamento do evento maior e cruze a faixa
    [low, high] do evento. Os timestamps Profit são o início das barras.
    O resultado é somente descritivo e não representa direção, entrada, SL ou SG.
    """
    if eventos.empty or menores.empty:
        return {
            "n_eventos": 0,
            "n_confirmados": 0,
            "taxa_confirmacao": 0.0,
            "eventos_dentro": 0,
            "eventos_fora": 0,
            "familias": {},
        }

    eventos = eventos.copy()
    menores = menores.copy()
    eventos["dt"] = pd.to_datetime(eventos["dt"])
    menores["dt"] = pd.to_datetime(menores["dt"])
    duracao = pd.Timedelta(minutes=tamanho_intervalo_minutos)
    eventos["intervalo_inicial"] = eventos["dt"] + duracao
    eventos["intervalo_final"] = eventos["intervalo_inicial"] + duracao

    resultados = []
    for evento in eventos.itertuples(index=False):
        intervalo_inicio = evento.intervalo_inicial
        intervalo_fim = evento.intervalo_final
        candidatos = menores[
            (menores["dt"] >= intervalo_inicio)
            & (menores["dt"] < intervalo_fim)
        ].copy()
        dentro = candidatos[
            (candidatos["l"] <= evento.h)
            & (candidatos["h"] >= evento.l)
        ].copy()
        fora = candidatos[
            (candidatos["l"] > evento.h)
            | (candidatos["h"] < evento.l)
        ].copy()

        resultados.append({
            "familia_evento": int(evento.fam),
            "eventos_dentro": len(dentro),
            "eventos_fora": len(fora),
            "confirmacao": int((dentro["fam"] == evento.fam).sum() > 0),
            "eventos_familia": int((dentro["fam"] == evento.fam).sum()),
            "eventos_familia_fora": int((fora["fam"] == evento.fam).sum()),
        })

    linhas = pd.DataFrame(resultados)
    familias = linhas.groupby("familia_evento")["eventos_familia"].sum().to_dict()
    return {
        "n_eventos": len(linhas),
        "n_confirmados": int(linhas["confirmacao"].sum()),
        "taxa_confirmacao": float(linhas["confirmacao"].mean()) if not linhas.empty else 0.0,
        "eventos_dentro": int(linhas["eventos_dentro"].sum()),
        "eventos_fora": int(linhas["eventos_fora"].sum()),
        "eventos_familia_fora": int(linhas["eventos_familia_fora"].sum()),
        "taxa_familia_fora": float(linhas["eventos_familia_fora"].sum() / linhas["eventos_fora"].sum()) if linhas["eventos_fora"].sum() else 0.0,
        "familias": {str(familia): int(total) for familia, total in sorted(familias.items())},
    }


def comparar_area_controle(
    eventos: pd.DataFrame,
    area: pd.DataFrame,
    controle: pd.DataFrame,
    tamanho_intervalo_minutos: int,
) -> dict[str, object]:
    """Compara a taxa dentro da área com a mesma família fora da área."""
    area_medida = medir_confirmacao_area(eventos, area, tamanho_intervalo_minutos)
    controle_medida = medir_confirmacao_area(eventos, controle, tamanho_intervalo_minutos)
    return {
        "taxa_area": float(area_medida["taxa_confirmacao"]),
        "taxa_controle": float(controle_medida["taxa_confirmacao"]),
        "diferenca_pontos": float(area_medida["taxa_confirmacao"] - controle_medida["taxa_confirmacao"]),
        "area": area_medida,
        "controle": controle_medida,
    }


def medir_confirmacao_multitf(
    eventos: pd.DataFrame,
    menores_por_tf: dict[str, pd.DataFrame],
    tamanho_intervalo_minutos: int,
) -> dict[str, object]:
    """Calcula a confirmação A01 para cada timeframe menor do contexto."""
    if not menores_por_tf:
        return {
            "n_timeframes": 0,
            "taxas": {},
            "eventos_confirmados": 0,
        }

    taxas = {}
    eventos_confirmados = 0
    for nome, menores in menores_por_tf.items():
        resultado = medir_confirmacao_area(eventos, menores, tamanho_intervalo_minutos)
        taxas[nome] = float(resultado["taxa_confirmacao"])
        eventos_confirmados += int(resultado["n_confirmados"])

    return {
        "n_timeframes": len(menores_por_tf),
        "taxas": taxas,
        "eventos_confirmados": eventos_confirmados,
    }


def medir_area_vs_controle_lateral(
    eventos: pd.DataFrame,
    menores: pd.DataFrame,
    tamanho_intervalo_minutos: int,
    tamanho_candle_menor_minutos: int,
) -> dict[str, object]:
    """Compara a família do evento na área com duas faixas laterais pareadas.

    Para cada evento colorido, testa a faixa [l, h] e duas faixas adjacentes
    de largura idêntica: [l - largura, l) e (h, h + largura]. O teste usa a
    mesma janela temporal após o fechamento do evento; eventos só entram se
    houver todos os timestamps esperados de início de sub-barra. É uma comparação espacial descritiva, não testa
    reversão, direção futura nem relevância operacional.
    """
    if tamanho_intervalo_minutos <= 0 or tamanho_candle_menor_minutos <= 0:
        raise ValueError("Os tamanhos dos intervalos devem ser positivos.")
    if tamanho_intervalo_minutos % tamanho_candle_menor_minutos:
        raise ValueError("A janela deve conter um número inteiro de candles menores.")
    colunas = {"dt", "fam", "l", "h"}
    if not colunas.issubset(eventos.columns) or not colunas.issubset(menores.columns):
        raise ValueError("eventos e menores precisam conter dt, fam, l e h.")
    if eventos.empty or menores.empty:
        return {
            "n_eventos": 0,
            "n_avaliaveis": 0,
            "n_incompletos": 0,
            "area_taxa": 0.0,
            "n_familia_area": 0,
            "controle_inferior_taxa": 0.0,
            "n_familia_controle_inferior": 0,
            "controle_superior_taxa": 0.0,
            "n_familia_controle_superior": 0,
            "controle_lateral_taxa": 0.0,
            "diferenca_area_controle_pp": 0.0,
        }

    eventos = eventos[["dt", "fam", "l", "h"]].copy()
    menores = menores[["dt", "fam", "l", "h"]].copy()
    eventos["dt"] = pd.to_datetime(eventos["dt"])
    menores["dt"] = pd.to_datetime(menores["dt"])
    minutos = tamanho_intervalo_minutos
    duracao = pd.Timedelta(minutes=minutos)
    eventos["intervalo"] = eventos["dt"] + duracao
    menores["intervalo"] = menores["dt"].dt.floor(f"{minutos}min")
    por_intervalo = {dt: grupo for dt, grupo in menores.groupby("intervalo", sort=False)}
    esperados = tamanho_intervalo_minutos // tamanho_candle_menor_minutos
    observacoes: list[tuple[int, int, int]] = []
    n_incompletos = 0

    for evento in eventos.itertuples(index=False):
        if evento.fam == 0 or evento.h <= evento.l:
            continue
        candidatos = por_intervalo.get(evento.intervalo)
        if candidatos is None:
            n_incompletos += 1
            continue
        inicio = evento.intervalo
        fim = inicio + duracao
        candidatos = candidatos[(candidatos["dt"] >= inicio) & (candidatos["dt"] < fim)]
        timestamps_esperados = pd.date_range(
            start=inicio,
            periods=esperados,
            freq=f"{tamanho_candle_menor_minutos}min",
        )
        if (
            len(candidatos) != esperados
            or candidatos["dt"].duplicated().any()
            or not candidatos["dt"].sort_values().reset_index(drop=True).equals(
                pd.Series(timestamps_esperados, name="dt")
            )
        ):
            n_incompletos += 1
            continue

        largura = float(evento.h - evento.l)
        familia = int(evento.fam)
        na_area = (
            (candidatos["l"] <= evento.h)
            & (candidatos["h"] >= evento.l)
            & (candidatos["fam"] == familia)
        ).any()
        no_controle_inferior = (
            (candidatos["l"] <= evento.l)
            & (candidatos["h"] >= evento.l - largura)
            & (candidatos["h"] < evento.l)
            & (candidatos["fam"] == familia)
        ).any()
        no_controle_superior = (
            (candidatos["h"] >= evento.h)
            & (candidatos["l"] <= evento.h + largura)
            & (candidatos["l"] > evento.h)
            & (candidatos["fam"] == familia)
        ).any()
        observacoes.append((int(na_area), int(no_controle_inferior), int(no_controle_superior)))

    n_avaliaveis = len(observacoes)
    if not n_avaliaveis:
        area_taxa = inferior_taxa = superior_taxa = controle_taxa = diferenca = 0.0
    else:
        area_taxa = sum(x[0] for x in observacoes) / n_avaliaveis
        inferior_taxa = sum(x[1] for x in observacoes) / n_avaliaveis
        superior_taxa = sum(x[2] for x in observacoes) / n_avaliaveis
        controle_taxa = (inferior_taxa + superior_taxa) / 2
        diferenca = (area_taxa - controle_taxa) * 100

    return {
        "n_eventos": int((eventos["fam"] != 0).sum()),
        "n_avaliaveis": n_avaliaveis,
        "n_incompletos": n_incompletos,
        "area_taxa": float(area_taxa),
        "n_familia_area": int(sum(x[0] for x in observacoes)),
        "controle_inferior_taxa": float(inferior_taxa),
        "n_familia_controle_inferior": int(sum(x[1] for x in observacoes)),
        "controle_superior_taxa": float(superior_taxa),
        "n_familia_controle_superior": int(sum(x[2] for x in observacoes)),
        "controle_lateral_taxa": float(controle_taxa),
        "diferenca_area_controle_pp": float(diferenca),
    }


if __name__ == "__main__":
    print("TeseFma_areas — modo descritivo. Nenhuma regra operacional foi carregada.")
