"""Testes do simulador do motor M02 com cenários sintéticos mínimos."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "motores" / "M02_microestrutura_barreiras" / "codigo"))
sys.path.insert(0, str(RAIZ / "src"))

import mb_motor as mb  # noqa: E402


def serie(barras, sinais=None, atr=10.0, inicio="2026-01-05 10:00"):
    """barras: lista de (o, h, l, c). sinais: dict {indice: (lado, ctx)}."""
    dt = pd.date_range(inicio, periods=len(barras), freq="min")
    d = pd.DataFrame(barras, columns=["o", "h", "l", "c"])
    d.insert(0, "dt", dt)
    d["atr"] = atr
    d["sinal"] = np.int8(0)
    d["ctx"] = np.int8(0)
    for i, (lado, ctx) in (sinais or {}).items():
        d.loc[i, "sinal"] = lado
        d.loc[i, "ctx"] = ctx
    d["hhmm"] = d["dt"].dt.hour * 100 + d["dt"].dt.minute
    d["dia"] = d["dt"].dt.normalize()
    return d


PLANA = (100, 101, 99, 100)


class TesteSimulador(unittest.TestCase):
    def test_stop_longo_na_barra_seguinte_a_entrada(self):
        # sinal em 0 -> entra na abertura de 1; barra 1 sem proteção; ordens valem a partir da barra 2
        d = serie([PLANA, PLANA, (100, 101, 60, 70)], {0: (1, 3)})
        t = mb.simular(d, mb.Params())
        self.assertEqual(len(t), 1)
        self.assertEqual(t.loc[0, "motivo"], "SL")
        self.assertAlmostEqual(t.loc[0, "pnl"], -35.0)

    def test_alvo_longo(self):
        d = serie([PLANA, PLANA, (100, 230, 99, 200)], {0: (1, 3)})
        t = mb.simular(d, mb.Params())
        self.assertEqual(t.loc[0, "motivo"], "SG")
        self.assertAlmostEqual(t.loc[0, "pnl"], 120.0)

    def test_stop_e_alvo_na_mesma_barra_assume_stop(self):
        d = serie([PLANA, PLANA, (100, 230, 60, 150)], {0: (1, 3)})
        t = mb.simular(d, mb.Params())
        self.assertEqual(t.loc[0, "motivo"], "SL")

    def test_venda_simetrica(self):
        d = serie([PLANA, PLANA, (100, 140, 99, 130)], {0: (-1, 1)})
        t = mb.simular(d, mb.Params())
        self.assertEqual(t.loc[0, "motivo"], "SL")
        self.assertAlmostEqual(t.loc[0, "pnl"], -35.0)

    def test_barra_de_entrada_sem_protecao_no_perfil_fiel(self):
        # a própria barra de entrada atravessa o stop; no perfil fiel nada acontece nela
        d = serie([PLANA, (100, 101, 50, 99), PLANA], {0: (1, 3)})
        fiel = mb.simular(d, mb.Params(protecao_na_barra_de_entrada=False))
        ideal = mb.simular(d, mb.Params(protecao_na_barra_de_entrada=True))
        self.assertEqual(ideal.loc[0, "motivo"], "SL")
        self.assertNotEqual(fiel.loc[0, "motivo"], "SL")

    def test_stop_limit_passivo_quando_fechamento_ja_passou_do_limite(self):
        # entrada 100; stop 65, limite 60; barra de entrada fecha em 50 (< limite): ordem passiva
        d = serie([PLANA, (100, 101, 50, 50), (50, 55, 48, 52), (52, 61, 51, 60)], {0: (1, 3)})
        t = mb.simular(d, mb.Params())
        self.assertEqual(t.loc[0, "motivo"], "STOP_PASSIVO")
        self.assertAlmostEqual(t.loc[0, "saida"], 60.0)
        self.assertAlmostEqual(t.loc[0, "pnl"], -40.0)

    def test_stop_de_tempo_na_abertura_da_barra_seguinte(self):
        d = serie([PLANA] * 30, {0: (1, 3)})
        t = mb.simular(d, mb.Params(max_barras=20))
        self.assertEqual(t.loc[0, "motivo"], "TEMPO")
        self.assertEqual(t.loc[0, "barras"], 20)

    def test_sem_entrada_no_ultimo_candle_do_pregao(self):
        d = serie([PLANA, PLANA], {1: (1, 3)})
        t = mb.simular(d, mb.Params())
        self.assertTrue(t.empty)

    def test_custo_por_trade(self):
        d = serie([PLANA, PLANA, (100, 230, 99, 200)], {0: (1, 3)})
        t = mb.simular(d, mb.Params(custo_pts=10.0))
        self.assertAlmostEqual(t.loc[0, "pnl"], 110.0)
        self.assertAlmostEqual(t.loc[0, "pnl_bruto"], 120.0)

    def test_distancias_usam_piso(self):
        self.assertEqual(mb.distancias(10.0, mb.Params()), (35.0, 120.0))
        self.assertEqual(mb.distancias(100.0, mb.Params()), (50.0, 250.0))


class TesteSinais(unittest.TestCase):
    def test_janela_ativa(self):
        hm = np.array([900, 915, 1159, 1200, 1359, 1400, 1615, 1616])
        esperado = np.array([False, True, True, False, False, True, True, False])
        np.testing.assert_array_equal(mb.janela_ativa(hm, mb.Params()), esperado)

    def test_estados_por_amplitude_e_cor(self):
        n = 25
        base = [(100, 110, 90, 100)] * n  # range 20 -> ATR ~ 20
        d = pd.DataFrame(base, columns=["o", "h", "l", "c"])
        d.insert(0, "dt", pd.date_range("2026-01-05 10:00", periods=n, freq="min"))
        d["v"] = 1.0
        d.loc[22, ["o", "h", "l", "c"]] = (100, 140, 100, 139)  # range 40 >= 1.7*ATR, alta -> estado 3
        d.loc[23, ["o", "h", "l", "c"]] = (139, 139, 107, 108)  # range 32 ~ >= 1.3*ATR, baixa
        p = mb.preparar(d, mb.Params())
        self.assertEqual(int(p.loc[22, "est"]), 3)
        self.assertIn(int(p.loc[23, "est"]), (2, 4))


if __name__ == "__main__":
    unittest.main()
