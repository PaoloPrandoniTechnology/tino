import unittest

from agente import metrics


class TestMetrics(unittest.TestCase):
    def test_copertura(self):
        self.assertAlmostEqual(metrics.copertura(108, 108), 100.0)
        self.assertAlmostEqual(metrics.copertura(54, 108), 50.0)
        self.assertAlmostEqual(metrics.copertura(216, 108), 200.0)
        self.assertEqual(metrics.copertura(50, 0), 0.0)

    def test_crescita(self):
        self.assertAlmostEqual(metrics.crescita(150, 100), 50.0)
        self.assertAlmostEqual(metrics.crescita(80, 100), -20.0)
        self.assertIsNone(metrics.crescita(100, 0))
        self.assertIsNone(metrics.crescita(100, None))

    def test_ricavo_per_listing(self):
        self.assertAlmostEqual(metrics.ricavo_per_listing(132, 40), 3.3)
        self.assertEqual(metrics.ricavo_per_listing(132, 0), 0.0)

    def test_potatura(self):
        listing = [
            {"titolo": "invisibile", "giorni_online": 45, "visite": 12, "ordini": 3},
            {"titolo": "zero ordini", "giorni_online": 40, "visite": 300, "ordini": 0},
            {"titolo": "buono", "giorni_online": 40, "visite": 300, "ordini": 4},
            {"titolo": "troppo giovane", "giorni_online": 5, "visite": 0, "ordini": 0},
        ]
        potati = {v["titolo"] for v in metrics.da_potare(listing)}
        self.assertEqual(potati, {"invisibile", "zero ordini"})

    def test_riscrittura(self):
        listing = [
            {"titolo": "visto ma ignorato", "giorni_online": 40, "visite": 200, "ctr": 0.8},
            {"titolo": "ok", "giorni_online": 40, "visite": 200, "ctr": 3.2},
        ]
        da_riscrivere = {v["titolo"] for v in metrics.da_riscrivere(listing)}
        self.assertEqual(da_riscrivere, {"visto ma ignorato"})

    def test_autonomia(self):
        self.assertEqual(metrics.autonomia(96.42, 0.55), 175)
        self.assertIsNone(metrics.autonomia(96.42, 0))


if __name__ == "__main__":
    unittest.main()
