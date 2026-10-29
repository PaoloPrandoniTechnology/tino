import unittest

from agente import notifica


REPORT = {
    "oggi": "2026-11-04",
    "giorno": 3,
    "ricavo_mese": 14.9,
    "ricavo_mese_precedente": 0.0,
    "copertura": 13.8,
    "crescita": None,
    "cassa": 84.1,
    "autonomia_giorni": 157,
    "catalogo": 1,
    "listing_attivi": 2,
    "da_potare": [],
    "da_riscrivere": [],
}


class TestComponi(unittest.TestCase):
    def test_il_messaggio_contiene_i_numeri_che_contano(self):
        testo, _ = notifica.componi(REPORT)
        self.assertIn("Giorno 3", testo)
        self.assertIn("14,90 €", testo)
        self.assertIn("copertura 14%", testo)
        self.assertIn("84,10 €", testo)
        self.assertNotIn("100.000", testo)

    def test_parametri_del_template_sono_quattro_e_nell_ordine_giusto(self):
        _, parametri = notifica.componi(REPORT)
        self.assertEqual(parametri, ["3", "14,90", "14", "84,10"])

    def test_giorno_assente_non_produce_none(self):
        report = dict(REPORT, giorno=None, autonomia_giorni=None)
        testo, parametri = notifica.componi(report)
        self.assertNotIn("None", testo)
        self.assertEqual(parametri[0], "0")

    def test_la_potatura_compare_solo_se_c_e_qualcosa_da_potare(self):
        testo, _ = notifica.componi(REPORT)
        self.assertNotIn("Da potare", testo)
        testo, _ = notifica.componi(dict(REPORT, da_potare=["Budget Familiare"]))
        self.assertIn("Da potare: Budget Familiare", testo)


class TestCanali(unittest.TestCase):
    def test_senza_variabili_non_c_e_nessun_canale(self):
        self.assertEqual(notifica.canali({}), [])

    def test_telegram_richiede_token_e_chat(self):
        self.assertEqual(notifica.canali({"TELEGRAM_BOT_TOKEN": "x"}), [])
        self.assertEqual(
            notifica.canali({"TELEGRAM_BOT_TOKEN": "x", "TELEGRAM_CHAT_ID": "1"}),
            ["telegram"],
        )

    def test_whatsapp_richiede_tutte_e_tre_le_variabili(self):
        parziale = {"WHATSAPP_TOKEN": "x", "WHATSAPP_PHONE_ID": "1"}
        self.assertEqual(notifica.canali(parziale), [])
        completo = dict(parziale, WHATSAPP_TO="393331234567")
        self.assertEqual(notifica.canali(completo), ["whatsapp"])

    def test_entrambi_configurati_vengono_usati_in_ordine(self):
        env = {
            "TELEGRAM_BOT_TOKEN": "x",
            "TELEGRAM_CHAT_ID": "1",
            "WHATSAPP_TOKEN": "y",
            "WHATSAPP_PHONE_ID": "2",
            "WHATSAPP_TO": "393331234567",
        }
        self.assertEqual(notifica.canali(env), ["telegram", "whatsapp"])


class TestInvio(unittest.TestCase):
    def test_invia_senza_canali_non_fa_chiamate(self):
        testo, risultati = notifica.invia(REPORT, env={})
        self.assertIn("Giorno 3", testo)
        self.assertEqual(risultati, [])


if __name__ == "__main__":
    unittest.main()
