import os
import tempfile
import unittest

from agente import notifica, telegram

REPORT = {
    "oggi": "2026-11-04",
    "giorno": 3,
    "mese": "2026-11",
    "ricavo_mese": 14.9,
    "ricavo_mese_precedente": 0.0,
    "incassato_totale": 14.9,
    "speso_totale": 0.0,
    "cassa": 84.1,
    "costo_riferimento": 108.0,
    "spesa_mese": 16.0,
    "copertura": 13.8,
    "crescita": None,
    "autonomia_giorni": 157,
    "catalogo": 1,
    "listing_attivi": 2,
    "ricavo_per_listing": 7.45,
    "da_potare": [],
    "da_riscrivere": [],
}

CATALOGO = {
    "prodotti": [
        {"titolo": "Budget Familiare 2027", "prezzo": 14.9, "stato": "pronto", "piattaforma": "etsy"}
    ]
}


class TestComando(unittest.TestCase):
    def test_comando_normale(self):
        self.assertEqual(telegram.comando("/stato"), "/stato")

    def test_il_suffisso_del_bot_viene_tolto(self):
        self.assertEqual(telegram.comando("/stato@TinoMessagebot"), "/stato")

    def test_maiuscole_e_spazi(self):
        self.assertEqual(telegram.comando("   /CAssa  ora "), "/cassa")

    def test_testo_libero_non_e_un_comando(self):
        self.assertEqual(telegram.comando("ciao tino"), "")
        self.assertEqual(telegram.comando(""), "")
        self.assertEqual(telegram.comando(None), "")


class TestRisposte(unittest.TestCase):
    def test_stato_contiene_i_numeri_del_report(self):
        testo = telegram.rispondi("/stato", report=REPORT)
        self.assertIn("Giorno 3", testo)
        self.assertIn("14,90 €", testo)
        self.assertIn("84,10 €", testo)
        self.assertNotIn("None", testo)

    def test_start_fa_la_stessa_cosa_di_stato(self):
        self.assertEqual(telegram.rispondi("/start", report=REPORT), telegram.rispondi("/stato", report=REPORT))

    def test_cassa_elenca_incassi_e_autonomia(self):
        testo = telegram.rispondi("/cassa", report=REPORT)
        self.assertIn("Cassa: 84,10 €", testo)
        self.assertIn("Incassato in totale: 14,90 €", testo)
        self.assertIn("157 giorni", testo)

    def test_catalogo_mostra_prezzo_e_stato(self):
        testo = telegram.rispondi("/catalogo", catalogo=CATALOGO)
        self.assertIn("Budget Familiare 2027", testo)
        self.assertIn("14,90 €", testo)
        self.assertIn("pronto", testo)

    def test_catalogo_vuoto_lo_dice(self):
        self.assertEqual(telegram.rispondi("/catalogo", catalogo={"prodotti": []}), "Catalogo vuoto.")

    def test_giornale_legge_l_ultima_pagina(self):
        with tempfile.TemporaryDirectory() as cartella:
            os.makedirs(os.path.join(cartella, "giornale"))
            for nome, testo in (("2026-11-03.md", "vecchio"), ("2026-11-04.md", "Giorno 2 — nuovo")):
                with open(os.path.join(cartella, "giornale", nome), "w", encoding="utf-8") as f:
                    f.write(testo)
            self.assertIn("nuovo", telegram.rispondi("/giornale", stato=cartella))

    def test_comando_sconosciuto_restituisce_l_aiuto(self):
        self.assertEqual(telegram.rispondi("/boh", report=REPORT), telegram.aiuto())
        self.assertIn("/cassa", telegram.rispondi("ciao", report=REPORT))


class TestElabora(unittest.TestCase):
    def test_il_primo_chat_diventa_proprietario_e_riceve_risposta(self):
        inviati = []
        aggiornato, risposte = telegram.elabora(
            [{"update_id": 7, "message": {"chat": {"id": 42}, "text": "/stato"}}],
            {"chat_id": None, "offset": 0},
            report=REPORT,
            invia_funzione=lambda chat, testo: inviati.append((chat, testo)),
        )
        self.assertEqual(aggiornato["chat_id"], 42)
        self.assertEqual(aggiornato["offset"], 8)
        self.assertEqual(risposte, 1)
        self.assertIn("Giorno 3", inviati[0][1])

    def test_un_altro_chat_viene_ignorato(self):
        inviati = []
        aggiornato, risposte = telegram.elabora(
            [{"update_id": 9, "message": {"chat": {"id": 99}, "text": "/stato"}}],
            {"chat_id": 42, "offset": 8},
            report=REPORT,
            invia_funzione=lambda chat, testo: inviati.append((chat, testo)),
        )
        self.assertEqual(risposte, 0)
        self.assertEqual(inviati, [])
        self.assertEqual(aggiornato["chat_id"], 42)
        self.assertEqual(aggiornato["offset"], 10)

    def test_un_update_gia_consumato_non_viene_ripetuto(self):
        aggiornato, _ = telegram.elabora(
            [{"update_id": 3, "message": {"chat": {"id": 42}, "text": "/stato"}}],
            {"chat_id": 42, "offset": 4},
            report=REPORT,
            invia_funzione=lambda chat, testo: None,
        )
        self.assertEqual(aggiornato["offset"], 4)

    def test_messaggi_senza_testo_non_rompono_niente(self):
        aggiornato, risposte = telegram.elabora(
            [{"update_id": 1, "message": {"chat": {"id": 42}, "sticker": {}}}],
            {"chat_id": None, "offset": 0},
            report=REPORT,
            invia_funzione=lambda chat, testo: None,
        )
        self.assertEqual(risposte, 0)
        self.assertEqual(aggiornato["offset"], 2)


class TestChatImparato(unittest.TestCase):
    def test_senza_file_non_c_e_chat(self):
        with tempfile.TemporaryDirectory() as cartella:
            self.assertIsNone(notifica.chat_imparato(cartella))

    def test_il_chat_salvato_entra_nell_ambiente(self):
        with tempfile.TemporaryDirectory() as cartella:
            telegram._write_json(os.path.join(cartella, "telegram.json"), {"chat_id": 4242, "offset": 0})
            env = notifica.ambiente_con_chat(cartella, env={"TELEGRAM_BOT_TOKEN": "x"})
            self.assertEqual(env["TELEGRAM_CHAT_ID"], "4242")
            self.assertEqual(notifica.canali(env), ["telegram"])

    def test_il_secret_ha_la_precedenza(self):
        with tempfile.TemporaryDirectory() as cartella:
            telegram._write_json(os.path.join(cartella, "telegram.json"), {"chat_id": 4242, "offset": 0})
            env = notifica.ambiente_con_chat(cartella, env={"TELEGRAM_CHAT_ID": "1"})
            self.assertEqual(env["TELEGRAM_CHAT_ID"], "1")


if __name__ == "__main__":
    unittest.main()
