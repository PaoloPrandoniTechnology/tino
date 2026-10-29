import json
import os
import tempfile
import unittest

from agente import ledger


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.cartella = tempfile.mkdtemp()
        self.percorso = os.path.join(self.cartella, "ledger.jsonl")

    def _scrivi_righe(self, righe):
        with open(self.percorso, "w", encoding="utf-8") as f:
            for r in righe:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")

    def test_catena_integra_dopo_due_movimenti(self):
        ledger.append(self.percorso, "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02")
        ledger.append(self.percorso, "uscita", 1, "esecuzione", "api", "agente", "2026-11-02")
        ok, msg = ledger.verify(self.percorso)
        self.assertTrue(ok, msg)
        self.assertEqual(len(ledger.entries(self.percorso)), 2)

    def test_totali(self):
        ledger.append(self.percorso, "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02")
        ledger.append(self.percorso, "uscita", 3.58, "esecuzione", "api", "agente", "2026-11-02")
        ledger.append(self.percorso, "entrata", 25, "vendita", "etsy", "ricavo", "2026-11-10")
        t = ledger.totali(self.percorso)
        self.assertAlmostEqual(t["incassato"], 125.0)
        self.assertAlmostEqual(t["speso"], 3.58)
        self.assertAlmostEqual(t["cassa"], 121.42)

    def test_capitale_non_e_ricavo(self):
        ledger.append(self.percorso, "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02")
        ledger.append(self.percorso, "entrata", 19, "vendita", "etsy", "ricavo", "2026-11-10")
        mesi = ledger.ricavi_per_mese(self.percorso)
        self.assertAlmostEqual(mesi["2026-11"]["ricavo"], 19.0)
        self.assertAlmostEqual(mesi["2026-11"]["altre_entrate"], 100.0)

    def test_manomissione_rilevata(self):
        ledger.append(self.percorso, "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02")
        ledger.append(self.percorso, "uscita", 1, "esecuzione", "api", "agente", "2026-11-02")
        righe = [json.loads(r) for r in open(self.percorso, encoding="utf-8") if r.strip()]
        righe[0]["importo"] = 10000.0
        self._scrivi_righe(righe)
        ok, msg = ledger.verify(self.percorso)
        self.assertFalse(ok)
        self.assertIn("hash non valido", msg)

    def test_scrittura_rifiutata_su_ledger_corrotto(self):
        ledger.append(self.percorso, "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02")
        righe = [json.loads(r) for r in open(self.percorso, encoding="utf-8") if r.strip()]
        righe[0]["importo"] = 5.0
        self._scrivi_righe(righe)
        with self.assertRaises(ValueError):
            ledger.append(self.percorso, "entrata", 1, "prova", "test")

    def test_riga_rimossa_rompe_la_catena(self):
        ledger.append(self.percorso, "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02")
        ledger.append(self.percorso, "uscita", 1, "esecuzione", "api", "agente", "2026-11-02")
        righe = [json.loads(r) for r in open(self.percorso, encoding="utf-8") if r.strip()]
        self._scrivi_righe(righe[1:])
        ok, msg = ledger.verify(self.percorso)
        self.assertFalse(ok)
        self.assertIn("prev_hash", msg)


if __name__ == "__main__":
    unittest.main()
