"""Telegram in due direzioni: Tino scrive, e risponde quando gli scrivi.

Il canale in uscita sta in `notifica.py`. Questo modulo aggiunge l'altra metà:
legge i messaggi che arrivano al bot (`getUpdates`), li interpreta come comandi
e risponde con i numeri veri, presi dal ledger — non con un testo inventato.

Tre regole che rendono il bot utilizzabile senza sorprese:

- **Un solo proprietario.** Il primo chat che scrive diventa il padrone del bot;
  gli altri vengono ignorati. Un bot pubblico con un token privato non deve
  rispondere a chiunque trovi il suo nome.
- **Offset in un file, non in memoria.** `state/telegram.json` tiene l'ultimo
  update consumato: due esecuzioni non rispondono due volte allo stesso messaggio.
- **Nessun modello nel giro.** Le risposte sono composizioni di numeri. Se il
  modello sbagliasse, il bot direbbe una cifra falsa in privato — e la fiducia in
  un numero si rompe una volta sola.
"""

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from . import loop, notifica

API = "https://api.telegram.org"
PERCORSO_STATO = "state/telegram.json"
TIMEOUT_SECONDI = 15
LUNGHEZZA_MASSIMA = 3900  # il limite di Telegram è 4096: si taglia prima


def _load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json(path, dati):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _euro(valore):
    return f"{valore:.2f} €".replace(".", ",")


def chiama(token, metodo, payload=None, timeout=TIMEOUT_SECONDI):
    """Chiamata alla Bot API senza dipendenze. Restituisce (ok, risultato)."""
    url = f"{API}/bot{token}/{metodo}"
    corpo = None if payload is None else json.dumps(payload).encode("utf-8")
    richiesta = urllib.request.Request(url, data=corpo, method="POST" if corpo else "GET")
    if corpo:
        richiesta.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
            dati = json.loads(risposta.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as errore:
        return False, f"HTTP {errore.code}: {errore.read().decode('utf-8', 'replace')[:300]}"
    except urllib.error.URLError as errore:
        return False, f"rete non raggiungibile: {errore.reason}"
    except ValueError:
        return False, "risposta non JSON"
    if not dati.get("ok"):
        return False, str(dati.get("description", "errore sconosciuto"))
    return True, dati.get("result")


def leggi_messaggi(token, offset=None, timeout=TIMEOUT_SECONDI):
    """Update non ancora consumati. None se la chiamata fallisce."""
    parametri = {"limit": 100, "timeout": 0}
    if offset:
        parametri["offset"] = offset
    ok, risultato = chiama(token, f"getUpdates?{urllib.parse.urlencode(parametri)}", timeout=timeout)
    if not ok:
        print(f"getUpdates: {risultato}")
        return None
    return risultato or []


def invia(token, chat_id, testo, timeout=TIMEOUT_SECONDI):
    """Manda un messaggio, spezzandolo se supera il limite di Telegram."""
    parti = [testo[i:i + LUNGHEZZA_MASSIMA] for i in range(0, len(testo), LUNGHEZZA_MASSIMA)] or [""]
    esiti = [notifica.invia_telegram(token, chat_id, parte, timeout=timeout) for parte in parti]
    return all(e["ok"] for e in esiti), esiti


def comando(testo):
    """`/stato@TinoMessagebot` → `/stato`. Testo libero → stringa vuota."""
    if not testo:
        return ""
    prima = testo.strip().split()[0].lower()
    if not prima.startswith("/"):
        return ""
    return prima.split("@")[0]


def aiuto():
    return "\n".join(
        [
            "Tino. Comandi:",
            "/stato — il conto del giorno",
            "/cassa — denaro, incassi e autonomia",
            "/catalogo — prodotti e prezzi",
            "/giornale — l'ultima pagina del giornale",
            "/aiuto — questo elenco",
            "",
            "I numeri arrivano dal ledger, non da un modello.",
        ]
    )


def rispondi(testo, stato="state", oggi=None, report=None, catalogo=None):
    """La risposta a un messaggio. Nessuna chiamata di rete: solo letture locali."""
    oggi = oggi or date.today().isoformat()
    cmd = comando(testo)

    if cmd in ("/stato", "/start", "/oggi"):
        report = report or loop.costruisci_report(stato, oggi)
        return notifica.componi(report)[0]

    if cmd == "/cassa":
        report = report or loop.costruisci_report(stato, oggi)
        autonomia = report["autonomia_giorni"]
        return "\n".join(
            [
                f"Cassa: {_euro(report['cassa'])}",
                f"Incassato in totale: {_euro(report['incassato_totale'])}",
                f"Speso in totale: {_euro(report['speso_totale'])}",
                f"Spesa agente: {_euro(report['spesa_mese'])}/mese",
                f"Autonomia: {'n/d' if autonomia is None else f'{autonomia} giorni'}",
            ]
        )

    if cmd == "/catalogo":
        if catalogo is None:
            catalogo = _load(f"{stato}/catalogo.json", {"prodotti": []})
        prodotti = catalogo.get("prodotti", [])
        if not prodotti:
            return "Catalogo vuoto."
        righe = [f"Catalogo ({len(prodotti)}):"]
        for voce in prodotti:
            righe.append(
                f"· {voce.get('titolo', '?')} — {_euro(float(voce.get('prezzo', 0)))} "
                f"· {voce.get('stato', '?')} · {voce.get('piattaforma', '?')}"
            )
        return "\n".join(righe)

    if cmd == "/giornale":
        cartella = f"{stato}/giornale"
        pagine = sorted(f for f in os.listdir(cartella) if f.endswith(".md")) if os.path.isdir(cartella) else []
        if not pagine:
            return "Giornale ancora vuoto."
        with open(os.path.join(cartella, pagine[-1]), encoding="utf-8") as f:
            return f.read().strip()[:LUNGHEZZA_MASSIMA]

    return aiuto()


def stato_salvato(percorso=PERCORSO_STATO):
    return _load(percorso, {"chat_id": None, "offset": 0, "ultimo": None})


def elabora(messaggi, salvato, stato="state", oggi=None, report=None, invia_funzione=None):
    """Consuma gli update e risponde. Restituisce (salvato aggiornato, n. risposte).

    `invia_funzione` esiste per i test: senza, si usa la Bot API vera.
    """
    oggi = oggi or date.today().isoformat()
    proprietario = salvato.get("chat_id")
    offset = salvato.get("offset") or 0
    risposte = 0

    for update in messaggi:
        offset = max(offset, int(update.get("update_id", 0)) + 1)
        messaggio = update.get("message") or update.get("edited_message") or {}
        chat = messaggio.get("chat") or {}
        chat_id = chat.get("id")
        testo = messaggio.get("text")
        if not chat_id or not testo:
            continue
        if proprietario is None:
            proprietario = chat_id
        if chat_id != proprietario:
            print(f"ignorato messaggio dal chat {chat_id}: il bot risponde solo al proprietario")
            continue
        risposta = rispondi(testo, stato=stato, oggi=oggi, report=report)
        if invia_funzione is None:
            continue  # senza canale di invio si aggiorna solo l'offset
        invia_funzione(chat_id, risposta)
        risposte += 1
        salvato["ultimo"] = {"data": oggi, "testo": testo[:200]}

    salvato["chat_id"] = proprietario
    salvato["offset"] = offset
    return salvato, risposte


def main(argv=None):
    parser = argparse.ArgumentParser(description="Legge i messaggi al bot e risponde.")
    parser.add_argument("--state", default="state")
    parser.add_argument("--stato-file", default=PERCORSO_STATO)
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true", help="mostra le risposte, non invia")
    args = parser.parse_args(argv)

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN assente: nessun messaggio da leggere")
        return 0

    salvato = stato_salvato(args.stato_file)
    messaggi = leggi_messaggi(token, salvato.get("offset"))
    if messaggi is None:
        return 1
    if not messaggi:
        print("nessun messaggio nuovo")
        return 0

    def invia_o_stampa(chat_id, testo):
        if args.dry_run:
            print(f"--- a {chat_id} ---\n{testo}")
            return
        ok, esiti = invia(token, chat_id, testo)
        print(f"risposta a {chat_id}: {'ok' if ok else 'errore'}")

    aggiornato, risposte = elabora(
        messaggi, salvato, stato=args.state, oggi=args.today, invia_funzione=invia_o_stampa
    )
    _write_json(args.stato_file, aggiornato)
    print(f"messaggi letti: {len(messaggi)} · risposte: {risposte} · proprietario: {aggiornato.get('chat_id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
