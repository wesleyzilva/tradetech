import unittest

import pandas as pd

from analise_areas import (
    AreaEvento,
    comparar_area_controle,
    confirmar_serie,
    medir_confirmacao_area,
    medir_confirmacao_multitf,
    medir_area_vs_controle_lateral,
    validar_evento,
)


class AreaTests(unittest.TestCase):
    def test_evento_valido_tem_areas_e_familia_corretas(self):
        evento = AreaEvento(
            dt="2026-01-01 09:00",
            ativo="WIN",
            timeframe="15min",
            familia=1,
            origem="ignicao",
            area_min=100.0,
            area_max=101.0,
            n_candles=3,
        )

        self.assertTrue(validar_evento(evento))

    def test_serie_vazia_nao_cria_confirmacao_positiva(self):
        resultado = confirmar_serie([])

        self.assertEqual(resultado["n_eventos"], 0)
        self.assertEqual(resultado["n_confirmados"], 0)
        self.assertEqual(resultado["taxa_confirmacao"], 0.0)

    def test_area_15min_conta_familia_5min_na_hora_apos_fechamento(self):
        evento = pd.DataFrame(
            [{
                "dt": pd.Timestamp("2026-01-01 09:00:00"),
                "fam": 1,
                "l": 100.0,
                "h": 101.0,
            }]
        )
        menor = pd.DataFrame(
            [
                {"dt": pd.Timestamp("2026-01-01 08:50:00"), "fam": 1, "l": 100.0, "h": 100.5},
                {"dt": pd.Timestamp("2026-01-01 09:15:00"), "fam": -1, "l": 100.5, "h": 101.0},
                {"dt": pd.Timestamp("2026-01-01 09:20:00"), "fam": 1, "l": 100.2, "h": 100.8},
                {"dt": pd.Timestamp("2026-01-01 09:25:00"), "fam": 1, "l": 100.2, "h": 100.8},
                {"dt": pd.Timestamp("2026-01-01 10:00:00"), "fam": 1, "l": 100.5, "h": 101.5},
            ]
        )

        resultado = medir_confirmacao_area(evento, menor, 15)

        self.assertEqual(resultado["n_eventos"], 1)
        self.assertEqual(resultado["n_confirmados"], 1)
        self.assertAlmostEqual(resultado["taxa_confirmacao"], 1.0)
        self.assertEqual(resultado["eventos_dentro"], 3)
        self.assertEqual(resultado["eventos_fora"], 0)

    def test_area_nao_pode_usar_eventos_que_nao_fazem_parte_da_area(self):
        evento = pd.DataFrame(
            [{
                "dt": pd.Timestamp("2026-01-01 09:00:00"),
                "fam": 1,
                "l": 100.0,
                "h": 101.0,
            }]
        )
        menor = pd.DataFrame(
            [
                {"dt": pd.Timestamp("2026-01-01 08:50:00"), "fam": 1, "l": 99.0, "h": 99.5},
                {"dt": pd.Timestamp("2026-01-01 09:15:00"), "fam": 1, "l": 101.05, "h": 102.0},
            ]
        )

        resultado = medir_confirmacao_area(evento, menor, 15)

        self.assertEqual(resultado["n_confirmados"], 0)
        self.assertEqual(resultado["eventos_dentro"], 0)
        self.assertEqual(resultado["taxa_confirmacao"], 0.0)

    def test_area_compara_com_controle_do_mesmo_intervalo(self):
        evento = pd.DataFrame(
            [{
                "dt": pd.Timestamp("2026-01-01 09:00:00"),
                "fam": 1,
                "l": 100.0,
                "h": 101.0,
            }]
        )
        area = pd.DataFrame(
            [{"dt": pd.Timestamp("2026-01-01 09:15:00"), "fam": 1, "l": 100.2, "h": 100.8}]
        )
        controle = pd.DataFrame(
            [{"dt": pd.Timestamp("2026-01-01 09:15:00"), "fam": -1, "l": 100.2, "h": 100.8}]
        )

        resultado = comparar_area_controle(evento, area, controle, 15)

        self.assertAlmostEqual(resultado["taxa_area"], 1.0)
        self.assertAlmostEqual(resultado["taxa_controle"], 0.0)
        self.assertAlmostEqual(resultado["diferenca_pontos"], 1.0)
        self.assertEqual(resultado["area"]["eventos_fora"], 0)
        self.assertEqual(resultado["controle"]["eventos_fora"], 0)

    def test_multitf_conta_confirmacao_posterior_por_par_de_timeframes(self):
        evento = pd.DataFrame(
            [{
                "dt": pd.Timestamp("2026-01-01 09:00:00"),
                "fam": 1,
                "l": 100.0,
                "h": 101.0,
            }]
        )
        menores = {
            "5min": pd.DataFrame([
                {"dt": pd.Timestamp("2026-01-01 09:15:00"), "fam": 1, "l": 100.2, "h": 100.8},
                {"dt": pd.Timestamp("2026-01-01 09:20:00"), "fam": 1, "l": 100.6, "h": 101.0},
            ]),
            "10min": pd.DataFrame([
                {"dt": pd.Timestamp("2026-01-01 09:20:00"), "fam": 1, "l": 100.5, "h": 101.1},
            ]),
        }

        resultado = medir_confirmacao_multitf(evento, menores, 15)

        self.assertEqual(resultado["n_timeframes"], 2)
        self.assertEqual(resultado["taxas"]["5min"], 1.0)
        self.assertEqual(resultado["taxas"]["10min"], 1.0)
        self.assertEqual(resultado["eventos_confirmados"], 2)

    def test_controle_lateral_parea_horario_e_largura_da_area(self):
        evento = pd.DataFrame([{
            "dt": pd.Timestamp("2026-01-01 09:00"),
            "fam": 1,
            "l": 100.0,
            "h": 101.0,
        }])
        menores = pd.DataFrame([
            {"dt": pd.Timestamp(f"2026-01-01 09:{m:02d}"), "fam": fam, "l": low, "h": high}
            for m, fam, low, high in [
                (20, 1, 100.0, 100.4),
                (25, 1, 99.0, 99.8),
                (30, 1, 101.2, 102.0),
                (35, -1, 99.0, 99.8),
            ]
        ])
        evento["dt"] = pd.Timestamp("2026-01-01 09:00")

        resultado = medir_area_vs_controle_lateral(evento, menores, 20, 5)

        self.assertEqual(resultado["n_avaliaveis"], 1)
        self.assertEqual(resultado["area_taxa"], 1.0)
        self.assertEqual(resultado["controle_inferior_taxa"], 1.0)
        self.assertEqual(resultado["controle_superior_taxa"], 1.0)
        self.assertEqual(resultado["diferenca_area_controle_pp"], 0.0)
        self.assertEqual(resultado["n_familia_area"], 1)

    def test_controle_lateral_exclui_janela_incompleta(self):
        evento = pd.DataFrame([{
            "dt": pd.Timestamp("2026-01-01 08:40"),
            "fam": 1,
            "l": 100.0,
            "h": 101.0,
        }])
        menores = pd.DataFrame([{
            "dt": pd.Timestamp("2026-01-01 10:00"),
            "fam": 1,
            "l": 100.0,
            "h": 101.0,
        }])

        resultado = medir_area_vs_controle_lateral(evento, menores, 20, 5)

        self.assertEqual(resultado["n_avaliaveis"], 0)
        self.assertEqual(resultado["n_incompletos"], 1)

    def test_controle_lateral_rejeita_janela_nao_divisivel(self):
        evento = pd.DataFrame(columns=["dt", "fam", "l", "h"])
        menores = pd.DataFrame(columns=["dt", "fam", "l", "h"])

        with self.assertRaises(ValueError):
            medir_area_vs_controle_lateral(evento, menores, 60, 7)


if __name__ == "__main__":
    unittest.main()
