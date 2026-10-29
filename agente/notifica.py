"""Notifiche: far arrivare il conto del giorno sul telefono del titolare.

Due canali, entrambi per via ufficiale e senza librerie esterne:

- **Telegram Bot API** — gratuito, si configura in tre minuti.
- **WhatsApp Business Cloud API** — a pagamento per messaggio e con una regola
  precisa: un messaggio che parte senza una richiesta del destinatario deve
  usare un *template* approvato da Meta. Il template di questo progetto si
  chiama `tino_giornata` e ha quattro parametri (giorno, ricavo, copertura,
  cassa); il testo da incollare in Meta Business Manager sta in NOTIFICHE.md.

Il canale si sceglie dalle variabili d'ambiente, non dal codice. Se non ce n'è
nessuna configurata lo script stampa il messaggio ed esce con 0: una notifica
mancante non deve far fallire un'esecuzione che ha già fatto il suo lavoro.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date

TELEGRAM_API = "https://api.telegram.org"
GRAPH_API = "https://graph.facebook.com/v21.0"
TEMPLATE_PREDEFINITO = "tino_giornata"
LINGUA_PREDEFINITA = "it"
TIMEOUT_SECONDI = 15


def _euro(valore):
    return f"{valore:.2f} €".replace(".", ",")


def componi(report):
    """Restituisce (testo per Telegram, parametri per il template WhatsApp)."""
    giorno = report.get("giorno") or 0
    crescita = report.get("crescita")
    autonomia = report.get("autonomia_giorni")
    righe = [
        f"Giorno {giorno} — {report['oggi']}",
        f"Ricavo del mese: {_euro(report['ricavo_mese'])} · copertura {report['copertura']:.0f}%",
        f"Crescita mese su mese: {'n/d' if crescita is None else f'{crescita:+.0f}%'}",
        f"Cassa: {_euro(report['cassa'])} · autonomia {'n/d' if autonomia is None else f'{autonomia} giorni'}",
        f"Catalogo: {report['catalogo']} {'prodotto' if report['catalogo'] == 1 else 'prodotti'} · "
        f"{report['listing_attivi']} listing attivi",
    ]
    da_potare = report.get("da_potare") or []
    da_riscrivere = report.get("da_riscrivere") or []
    if da_potare:
        righe.append(f"Da potare: {', '.join(da_potare)}")
    if da_riscrivere:
        righe.append(f"Da riscrivere: {', '.join(da_riscrivere)}")
    testo = "\n".join(righe)

    parametri = [
        str(giorno),
        f"{report['ricavo_mese']:.2f}".replace(".", ","),
        f"{report['copertura']:.0f}",
        f"{report['cassa']:.2f}".replace(".", ","),
    ]
    return testo, parametri


def _post_json(url, payload, headers=None, timeout=TIMEOUT_SECONDI):
    """POST JSON senza dipendenze. Restituisce (stato, corpo come testo)."""
    corpo = json.dumps(payload).encode("utf-8")
    richiesta = urllib.request.Request(url, data=corpo, method="POST")
    richiesta.add_header("Content-Type", "application/json")
    for chiave, valore in (headers or {}).items():
        richiesta.add_header(chiave, valore)
    try:
        with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
            return risposta.status, risposta.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as errore:
        return errore.code, errore.read().decode("utf-8", "replace")
    except urllib.error.URLError as errore:
        return 0, f"rete non raggiungibile: {errore.reason}"


def invia_telegram(token, chat_id, testo, timeout=TIMEOUT_SECONDI):
    stato, corpo = _post_json(
        f"{TELEGRAM_API}/bot{token}/sendMessage",
        {"chat_id": chat_id, "text": testo, "disable_web_page_preview": True},
        timeout=timeout,
    )
    ok = stato == 200 and '"ok":true' in corpo.replace(" ", "")
    return {"canale": "telegram", "ok": ok, "stato": stato, "risposta": corpo[:500]}


def invia_whatsapp(token, phone_number_id, destinatario, parametri,
                   template=TEMPLATE_PREDEFINITO, lingua=LINGUA_PREDEFINITA,
                   timeout=TIMEOUT_SECONDI):
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": lingua},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": p} for p in parametri],
                }
            ],
        },
    }
    stato, corpo = _post_json(
        f"{GRAPH_API}/{phone_number_id}/messages",
        payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    ok = stato == 200 and '"messages"' in corpo
    return {"canale": "whatsapp", "ok": ok, "stato": stato, "risposta": corpo[:500]}


def canali(env=None):
    """Canali configurati nell'ambiente, nell'ordine in cui vengono usati."""
    env = os.environ if env is None else env
    out = []
    if env.get("TELEGRAM_BOT_TOKEN") and env.get("TELEGRAM_CHAT_ID"):
        out.append("telegram")
    if all(env.get(k) for k in ("WHATSAPP_TOKEN", "WHATSAPP_PHONE_ID", "WHATSAPP_TO")):
        out.append("whatsapp")
    return out


def chat_imparato(stato="state"):
    """L'id del chat che il bot ha salvato dopo il primo messaggio ricevuto."""
    try:
        with open(os.path.join(stato, "telegram.json"), encoding="utf-8") as f:
            return json.load(f).get("chat_id")
    except (OSError, ValueError):
        return None


def ambiente_con_chat(stato="state", env=None):
    """L'ambiente, con il chat di Telegram imparato dal bot se il secret manca.

    Così il primo messaggio che scrivi al bot basta a far partire i digest: non
    serve copiare a mano un id da `getUpdates`.
    """
    env = dict(os.environ if env is None else env)
    if not env.get("TELEGRAM_CHAT_ID"):
        chat = chat_imparato(stato)
        if chat:
            env["TELEGRAM_CHAT_ID"] = str(chat)
    return env


def invia(report, env=None):
    env = os.environ if env is None else env
    testo, parametri = componi(report)
    risultati = []
    for canale in canali(env):
        if canale == "telegram":
            risultati.append(
                invia_telegram(env["TELEGRAM_BOT_TOKEN"], env["TELEGRAM_CHAT_ID"], testo)
            )
        elif canale == "whatsapp":
            risultati.append(
                invia_whatsapp(
                    env["WHATSAPP_TOKEN"],
                    env["WHATSAPP_PHONE_ID"],
                    env["WHATSAPP_TO"],
                    parametri,
                    template=env.get("WHATSAPP_TEMPLATE") or TEMPLATE_PREDEFINITO,
                    lingua=env.get("WHATSAPP_LINGUA") or LINGUA_PREDEFINITA,
                )
            )
    return testo, risultati


def main(argv=None):
    from . import loop

    parser = argparse.ArgumentParser(description="Manda il conto del giorno al titolare.")
    parser.add_argument("--state", default="state")
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true", help="stampa, non invia")
    args = parser.parse_args(argv)

    report = loop.costruisci_report(args.state, args.today)
    testo, parametri = componi(report)

    env = ambiente_con_chat(args.state)

    if args.dry_run:
        print(testo)
        print(f"canali configurati: {', '.join(canali(env)) or 'nessuno'}")
        return 0

    if not canali(env):
        print("nessun canale configurato: niente da inviare")
        print(testo)
        return 0

    _, risultati = invia(report, env)
    for voce in risultati:
        print(f"{voce['canale']}: {'ok' if voce['ok'] else 'errore ' + str(voce['stato'])}")
    return 0 if all(v["ok"] for v in risultati) else 1


if __name__ == "__main__":
    raise SystemExit(main())
