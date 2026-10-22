import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tradetech.dados import sessoes_liquidas  # noqa: E402


class SessoesLiquidas(unittest.TestCase):
    def test_remove_pregao_com_quantidade_diaria_baixa(self):
        d = pd.DataFrame(
            {
                "dt": pd.to_datetime(["2026-01-05 09:00", "2026-01-05 10:00", "2026-04-06 09:00", "2026-04-06 10:00"]),
                "q": [30, 38, 4_000_000, 5_000_000],
            }
        )
        r = sessoes_liquidas(d)
        self.assertEqual(sorted(r["dt"].dt.strftime("%Y-%m-%d").unique()), ["2026-04-06"])
        self.assertEqual(len(r), 2)


if __name__ == "__main__":
    unittest.main()
