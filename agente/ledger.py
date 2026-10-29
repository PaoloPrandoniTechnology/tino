"""Ledger append-only con catena di hash.

Ogni movimento è una riga JSON con `prev_hash` e `hash`. Il file si apre solo in
append: una riscrittura rompe la catena e `verify()` la rileva. Il workflow esegue
`--check` **prima** e **dopo** l'esecuzione e non committa se la catena è rotta.

Il capitale iniziale è un'entrata, ma **non è ricavo**: entra in cassa, non nel
fatturato. Per questo i ricavi si contano solo sulle righe con categoria "ricavo".
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

GENESIS = "0" * 64


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(entry):
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256(
        (_canon(body) + str(body.get("prev_hash", ""))).encode("utf-8")
    ).hexdigest()


def _righe(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for numero, riga in enumerate(f, 1):
            riga = riga.strip()
            if not riga:
                continue
            out.append((numero, json.loads(riga)))
    return out


def verify(path):
    """Ritorna (ok, messaggio). Non solleva eccezioni: la usa anche il CLI."""
    prev = GENESIS
    for numero, entry in _righe(path):
        if entry.get("prev_hash") != prev:
            return False, f"riga {numero}: prev_hash non collegato alla riga precedente"
        if entry.get("hash") != _hash(entry):
            return False, f"riga {numero}: hash non valido (contenuto modificato)"
        prev = entry["hash"]
    return True, "catena integra"


def append(path, tipo, importo, descrizione, fonte, categoria="", data=None):
    """Aggiunge un movimento. Rifiuta la scrittura se il ledger è già corrotto."""
    if tipo not in ("entrata", "uscita"):
        raise ValueError("tipo deve essere 'entrata' o 'uscita'")
    ok, msg = verify(path)
    if not ok:
        raise ValueError(f"ledger corrotto, scrittura rifiutata: {msg}")
    righe = _righe(path)
    prev = righe[-1][1]["hash"] if righe else GENESIS
    entry = {
        "data": data or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "tipo": tipo,
        "importo": round(float(importo), 2),
        "descrizione": descrizione,
        "fonte": fonte,
        "categoria": categoria,
        "prev_hash": prev,
    }
    entry["hash"] = _hash(entry)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    return entry


def entries(path):
    return [e for _, e in _righe(path)]


def totali(path):
    """Movimenti di cassa: il capitale è un'entrata, quindi entra qui."""
    inc = sum(e["importo"] for e in entries(path) if e["tipo"] == "entrata")
    spe = sum(e["importo"] for e in entries(path) if e["tipo"] == "uscita")
    return {
        "incassato": round(inc, 2),
        "speso": round(spe, 2),
        "cassa": round(inc - spe, 2),
    }


def ricavi_per_mese(path):
    """Ricavo (solo categoria 'ricavo'), uscite e altre entrate, per mese."""
    out = {}
    for e in entries(path):
        mese = str(e["data"])[:7]
        voce = out.setdefault(mese, {"ricavo": 0.0, "uscite": 0.0, "altre_entrate": 0.0})
        if e["tipo"] == "uscita":
            voce["uscite"] += e["importo"]
        elif e.get("categoria") == "ricavo":
            voce["ricavo"] += e["importo"]
        else:
            voce["altre_entrate"] += e["importo"]
    return {m: {k: round(v, 2) for k, v in d.items()} for m, d in sorted(out.items())}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Verifica il ledger append-only.")
    parser.add_argument("--check", metavar="PATH", help="percorso del ledger .jsonl")
    args = parser.parse_args(argv)
    if args.check:
        ok, msg = verify(args.check)
        print(("OK: " if ok else "ERRORE: ") + msg)
        return 0 if ok else 1
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
