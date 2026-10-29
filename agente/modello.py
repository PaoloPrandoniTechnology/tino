"""Chiamata opzionale al modello per il commento del giornale.

Non è obbligatoria: senza chiave l'agente produce comunque il report, e il sistema
resta testabile offline. Qualsiasi errore restituisce None — il loop non deve mai
fallire perché l'API è lenta o giù.
"""

import json
import os
import urllib.request

ENDPOINT = "https://api.anthropic.com/v1/messages"
MODELLO = "claude-sonnet-4-5"


def commento(prompt, max_tokens=300):
    chiave = os.environ.get("ANTHROPIC_API_KEY")
    if not chiave:
        return None
    corpo = {
        "model": MODELLO,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    richiesta = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(corpo).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": chiave,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(richiesta, timeout=30) as risposta:
            dati = json.load(risposta)
        parti = dati.get("content") or []
        testo = " ".join(p.get("text", "") for p in parti if isinstance(p, dict)).strip()
        return testo or None
    except Exception as errore:  # rete, quota, formato: non è un errore fatale
        print(f"[modello] non disponibile: {errore}")
        return None
