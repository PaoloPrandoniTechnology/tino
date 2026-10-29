import json
import os
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET

from strumenti import genera_budget as g


class TestProdottoBudget(unittest.TestCase):
    def setUp(self):
        self.cartella = tempfile.mkdtemp()
        self.percorso = g.costruisci(self.cartella)

    def test_file_esiste_ed_e_uno_zip_valido(self):
        self.assertTrue(os.path.exists(self.percorso))
        with zipfile.ZipFile(self.percorso) as z:
            self.assertIsNone(z.testzip())
            nomi = set(z.namelist())
        for parte in [
            "[Content_Types].xml",
            "_rels/.rels",
            "xl/workbook.xml",
            "xl/_rels/workbook.xml.rels",
            "xl/styles.xml",
            "xl/worksheets/sheet1.xml",
            "xl/worksheets/sheet2.xml",
            "xl/worksheets/sheet3.xml",
        ]:
            self.assertIn(parte, nomi)

    def test_xml_delle_parti_e_ben_formato(self):
        with zipfile.ZipFile(self.percorso) as z:
            for nome in z.namelist():
                if nome.endswith(".xml") or nome.endswith(".rels"):
                    ET.fromstring(z.read(nome))

    def test_fogli_e_formule(self):
        with zipfile.ZipFile(self.percorso) as z:
            workbook = z.read("xl/workbook.xml").decode("utf-8")
            budget = z.read("xl/worksheets/sheet2.xml").decode("utf-8")
            riepilogo = z.read("xl/worksheets/sheet3.xml").decode("utf-8")
        for nome in ("Istruzioni", "Budget", "Riepilogo"):
            self.assertIn(f'name="{nome}"', workbook)
        self.assertIn("fullCalcOnLoad", workbook)
        self.assertGreaterEqual(budget.count("<f>"), 60)
        self.assertIn("TOTALE ENTRATE", budget)
        self.assertIn("TOTALE USCITE", budget)
        self.assertIn("SALDO", budget)
        self.assertIn("Budget!P", riepilogo)
        self.assertIn("IFERROR(B5/B3,0)", riepilogo)

    def test_anteprime_e_listing(self):
        anteprime = os.path.join(self.cartella, "anteprime")
        self.assertEqual(len(os.listdir(anteprime)), 3)
        for nome in os.listdir(anteprime):
            with open(os.path.join(anteprime, nome), encoding="utf-8") as f:
                self.assertIn("<svg", f.read())

        with open(os.path.join(self.cartella, "listing", "titolo-it.txt"), encoding="utf-8") as f:
            titolo = f.read().strip()
        self.assertLessEqual(len(titolo), 140)
        self.assertTrue(titolo.lower().startswith("budget familiare excel"))

        with open(os.path.join(self.cartella, "listing", "tag-it.txt"), encoding="utf-8") as f:
            tag = [t for t in f.read().split("\n") if t.strip()]
        self.assertEqual(len(tag), 13)
        for t in tag:
            self.assertLessEqual(len(t), 20, t)

        with open(os.path.join(self.cartella, "listing", "descrizione.md"), encoding="utf-8") as f:
            descrizione = f.read().lower()
        self.assertIn("intelligenza artificiale", descrizione)
        self.assertIn("non è una consulenza finanziaria", descrizione)


if __name__ == "__main__":
    unittest.main()
