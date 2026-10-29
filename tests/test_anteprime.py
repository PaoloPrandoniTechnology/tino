import os
import struct
import unittest

CARTELLA = os.path.join("prodotti", "budget-familiare", "anteprime")
ATTESE = [
    "01-copertina.png",
    "02-cosa-contiene.png",
    "03-foglio-budget.png",
    "04-riepilogo.png",
    "05-come-si-usa.png",
]


class TestAnteprime(unittest.TestCase):
    def test_ci_sono_cinque_png(self):
        for nome in ATTESE:
            percorso = os.path.join(CARTELLA, nome)
            self.assertTrue(os.path.exists(percorso), nome)
            self.assertGreater(os.path.getsize(percorso), 20_000, f"{nome} troppo piccolo")

    def test_dimensioni_e_formato(self):
        for nome in ATTESE:
            with open(os.path.join(CARTELLA, nome), "rb") as f:
                intestazione = f.read(26)
            self.assertEqual(intestazione[:8], b"\x89PNG\r\n\x1a\n", nome)
            larghezza, altezza = struct.unpack(">II", intestazione[16:24])
            self.assertEqual((larghezza, altezza), (2000, 1500), nome)


if __name__ == "__main__":
    unittest.main()
