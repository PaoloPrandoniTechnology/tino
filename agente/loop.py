"""Esecuzione dell'agente: legge lo stato, calcola, scrive.

L'uscita è sempre la stessa: un report a schermo, un file di giornale, e il
`data.json` della dashboard rigenerato dal ledger.
"""

import argparse
import json
import os
from datetime import date

from . import ledger, metrics


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


def mese_precedente(mese):
    anno, numero = int(mese[:4]), int(mese[5:7])
    numero -= 1
    if numero == 0:
        anno, numero = anno - 1, 12
    return f"{anno:04d}-{numero:02d}"


def _percorso_ledger(dashboard):
    candidato = os.path.join(os.path.dirname(os.path.dirname(dashboard)), "state", "ledger.jsonl")
    return candidato if os.path.exists(candidato) else os.path.join("state", "ledger.jsonl")


def costruisci_report(stato, oggi):
    budget = _load(f"{stato}/budget.json", {})
    catalogo = _load(f"{stato}/catalogo.json", {"prodotti": []})
    metriche = _load(f"{stato}/metriche.json", {"listing": []})
    percorso = f"{stato}/ledger.jsonl"

    ok, msg = ledger.verify(percorso)
    if not ok:
        raise SystemExit(f"ledger non valido: {msg}")

    totali = ledger.totali(percorso)
    mesi = ledger.ricavi_per_mese(percorso)
    corrente = oggi[:7]
    mesi.setdefault(corrente, {"ricavo": 0.0, "uscite": 0.0, "altre_entrate": 0.0})

    ricavo = round(mesi[corrente].get("ricavo", 0.0), 2)
    prec = mese_precedente(corrente)
    ricavo_prec = round(mesi.get(prec, {}).get("ricavo", 0.0), 2)
    costo_riferimento = float(budget.get("costo_riferimento_mese", metrics.COSTO_RIFERIMENTO_MESE))
    spesa_mese = float(budget.get("spesa_mese", 0.0))
    burn = spesa_mese / 30.0 if spesa_mese else 0.0

    inizio = budget.get("inizio")
    giorno = (date.fromisoformat(oggi) - date.fromisoformat(inizio)).days + 1 if inizio else None

    listing = metriche.get("listing", [])
    prodotti = catalogo.get("prodotti", [])

    return {
        "oggi": oggi,
        "giorno": giorno,
        "mese": corrente,
        "ricavo_mese": ricavo,
        "ricavo_mese_precedente": ricavo_prec,
        "incassato_totale": totali["incassato"],
        "speso_totale": totali["speso"],
        "cassa": totali["cassa"],
        "costo_riferimento": costo_riferimento,
        "spesa_mese": spesa_mese,
        "copertura": round(metrics.copertura(ricavo, costo_riferimento), 1),
        "crescita": metrics.crescita(ricavo, ricavo_prec),
        "autonomia_giorni": metrics.autonomia(totali["cassa"], burn),
        "catalogo": len(prodotti),
        "listing_attivi": len(listing),
        "ricavo_per_listing": round(metrics.ricavo_per_listing(ricavo, len(listing)), 2),
        "da_potare": [v.get("titolo", "?") for v in metrics.da_potare(listing)],
        "da_riscrivere": [v.get("titolo", "?") for v in metrics.da_riscrivere(listing)],
    }


def testo_giornale(report, commento=None):
    crescita = report["crescita"]
    righe = [
        f"# Giorno {report['giorno']} — {report['oggi']}",
        "",
        f"- Ricavo del mese: **{report['ricavo_mese']:.2f} €** (mese precedente {report['ricavo_mese_precedente']:.2f} €)",
        f"- Copertura sul costo di riferimento {report['costo_riferimento']:.0f} €: **{report['copertura']:.0f}%**",
        f"- Crescita mese su mese: **{'n/d' if crescita is None else f'{crescita:+.0f}%'}**",
        f"- Cassa: **{report['cassa']:.2f} €** · autonomia {report['autonomia_giorni']} giorni",
        f"- Catalogo: {report['catalogo']} prodotti · {report['listing_attivi']} listing attivi · {report['ricavo_per_listing']:.2f} € per listing",
        f"- Spesa agente: {report['spesa_mese']:.2f} €/mese",
        "",
        f"**Da potare** ({len(report['da_potare'])}): {', '.join(report['da_potare']) or 'nessuno'}",
        f"**Da riscrivere** ({len(report['da_riscrivere'])}): {', '.join(report['da_riscrivere']) or 'nessuno'}",
        "",
    ]
    if commento:
        righe += [commento, ""]
    return "\n".join(righe)


def aggiorna_dashboard(percorso, report):
    dash = _load(percorso, {})
    percorso_ledger = _percorso_ledger(percorso)
    mesi = ledger.ricavi_per_mese(percorso_ledger)
    if not mesi:
        mesi = {report["mese"]: {"ricavo": report["ricavo_mese"], "uscite": 0.0, "altre_entrate": 0.0}}
    storico = [
        {"mese": m, "ricavo": v.get("ricavo", 0.0), "costi": report["costo_riferimento"]}
        for m, v in sorted(mesi.items())
    ]
    movimenti = [
        {
            "data": e["data"],
            "tipo": e["tipo"],
            "importo": e["importo"],
            "descrizione": e["descrizione"],
            "fonte": e["fonte"],
        }
        for e in ledger.entries(percorso_ledger)
    ]
    giornale = list(dash.get("giornale", []))
    if not any(g.get("data") == report["oggi"] for g in giornale):
        giornale.append(
            {
                "giorno": report["giorno"] or 0,
                "data": report["oggi"],
                "titolo": f"Giorno {report['giorno']} — copertura {report['copertura']:.0f}%",
                "testo": (
                    f"Ricavo del mese {report['ricavo_mese']:.2f} €, cassa {report['cassa']:.2f} €, "
                    f"autonomia {report['autonomia_giorni']} giorni. Catalogo: {report['catalogo']} prodotti."
                ),
            }
        )
    dash.update(
        {
            "giorno": report["giorno"] or dash.get("giorno", 1),
            "incassato": report["incassato_totale"],
            "speso": report["speso_totale"],
            "cassa": report["cassa"],
            "catalogo": report["catalogo"],
            "costoMensile": report["costo_riferimento"],
            "spesaMese": report["spesa_mese"],
            "storicoMensile": storico,
            "movimenti": movimenti,
            "giornale": giornale,
        }
    )
    _write_json(percorso, dash)
    return dash


def main(argv=None):
    parser = argparse.ArgumentParser(description="Esecuzione dell'agente Tino.")
    parser.add_argument("--state", default="state")
    parser.add_argument("--dashboard", default="dashboard/data.json")
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--no-llm", action="store_true", help="nessuna chiamata al modello")
    args = parser.parse_args(argv)

    report = costruisci_report(args.state, args.today)

    commento = None
    if not args.no_llm:
        from . import modello

        prompt = (
            "Sei Tino, un agente che deve coprire i propri costi con un catalogo di prodotti "
            "digitali. Scrivi 2 frasi, in italiano, senza emoji e senza promesse: cosa dicono i "
            f"numeri di oggi e cosa farai nella prossima esecuzione.\n\n{json.dumps(report, ensure_ascii=False)}"
        )
        commento = modello.commento(prompt)

    os.makedirs(f"{args.state}/giornale", exist_ok=True)
    with open(f"{args.state}/giornale/{args.today}.md", "w", encoding="utf-8") as f:
        f.write(testo_giornale(report, commento))
    aggiorna_dashboard(args.dashboard, report)

    print(testo_giornale(report, commento))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
