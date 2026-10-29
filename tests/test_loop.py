import json
import os
import tempfile
import unittest

from agente import ledger, loop


class TestLoop(unittest.TestCase):
    def setUp(self):
        self.radice = tempfile.mkdtemp()
        self.stato = os.path.join(self.radice, "state")
        self.dashboard = os.path.join(self.radice, "dashboard", "data.json")
        os.makedirs(self.stato)
        os.makedirs(os.path.dirname(self.dashboard))
        with open(os.path.join(self.stato, "budget.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "inizio": "2026-11-02",
                    "giorni_stagione": 100,
                    "costo_riferimento_mese": 108,
                    "spesa_mese": 16,
                },
                f,
            )
        with open(os.path.join(self.stato, "catalogo.json"), "w", encoding="utf-8") as f:
            json.dump({"prodotti": []}, f)
        with open(os.path.join(self.stato, "metriche.json"), "w", encoding="utf-8") as f:
            json.dump({"listing": []}, f)
        with open(self.dashboard, "w", encoding="utf-8") as f:
            json.dump({"progetto": "Tino", "giornale": []}, f)
        ledger.append(
            os.path.join(self.stato, "ledger.jsonl"),
            "entrata", 100, "capitale", "bonifico", "capitale", "2026-11-02",
        )

    def _leggi(self):
        with open(self.dashboard, encoding="utf-8") as f:
            return json.load(f)

    def test_esecuzione_scrive_giornale_e_dashboard(self):
        codice = loop.main(
            ["--state", self.stato, "--dashboard", self.dashboard, "--today", "2026-11-02", "--no-llm"]
        )
        self.assertEqual(codice, 0)
        self.assertTrue(os.path.exists(os.path.join(self.stato, "giornale", "2026-11-02.md")))
        dash = self._leggi()
        self.assertEqual(dash["giorno"], 1)
        self.assertAlmostEqual(dash["incassato"], 100.0)
        self.assertAlmostEqual(dash["cassa"], 100.0)
        self.assertEqual(dash["costoMensile"], 108)
        self.assertEqual(len(dash["storicoMensile"]), 1)
        self.assertEqual(dash["storicoMensile"][0]["mese"], "2026-11")
        # il capitale è cassa, non fatturato
        self.assertAlmostEqual(dash["storicoMensile"][0]["ricavo"], 0.0)

    def test_copertura_con_ricavo(self):
        ledger.append(
            os.path.join(self.stato, "ledger.jsonl"),
            "entrata", 54, "vendite", "etsy", "ricavo", "2026-11-10",
        )
        loop.main(["--state", self.stato, "--dashboard", self.dashboard, "--today", "2026-11-15", "--no-llm"])
        dash = self._leggi()
        self.assertAlmostEqual(dash["incassato"], 154.0)
        self.assertAlmostEqual(dash["cassa"], 154.0)
        report = loop.costruisci_report(self.stato, "2026-11-15")
        self.assertAlmostEqual(report["copertura"], 50.0)
        self.assertIsNone(report["crescita"])

    def test_ledger_corrotto_blocca_l_esecuzione(self):
        percorso = os.path.join(self.stato, "ledger.jsonl")
        righe = [json.loads(r) for r in open(percorso, encoding="utf-8") if r.strip()]
        righe[0]["importo"] = 9999.0
        with open(percorso, "w", encoding="utf-8") as f:
            for r in righe:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
        with self.assertRaises(SystemExit):
            loop.costruisci_report(self.stato, "2026-11-15")


if __name__ == "__main__":
    unittest.main()
