"""Le metriche che decidono: copertura, crescita, ricavo per listing, potatura.

Le soglie sono quelle dichiarate in SISTEMA.md e OPERATIVO.md. Se cambi una soglia
qui, va cambiata anche nel documento: sono lo stesso numero.
"""

COSTO_RIFERIMENTO_MESE = 108.0   # agente a pieno regime: il metro della copertura
GIORNI_MINIMI = 30               # un listing si giudica dopo un mese
VISITE_MINIME = 50               # sotto questa soglia è invisibile


def copertura(ricavo_mese, costo_mese=COSTO_RIFERIMENTO_MESE):
    """Percentuale dei costi coperta dai ricavi del mese."""
    if costo_mese <= 0:
        return 0.0
    return ricavo_mese / costo_mese * 100.0


def crescita(ricavo_mese, ricavo_precedente):
    """Variazione percentuale mese su mese; None se non c'è una base."""
    if not ricavo_precedente or ricavo_precedente <= 0:
        return None
    return (ricavo_mese - ricavo_precedente) / ricavo_precedente * 100.0


def ricavo_per_listing(ricavo_mese, listing_attivi):
    if listing_attivi <= 0:
        return 0.0
    return ricavo_mese / listing_attivi


def da_potare(listing, giorni_minimi=GIORNI_MINIMI, visite_minime=VISITE_MINIME):
    """Listing da ritirare: dopo un mese, invisibile oppure senza un solo ordine."""
    out = []
    for voce in listing:
        if int(voce.get("giorni_online", 0)) < giorni_minimi:
            continue
        if int(voce.get("visite", 0)) < visite_minime or int(voce.get("ordini", 0)) == 0:
            out.append(voce)
    return out


def da_riscrivere(listing):
    """Listing visti ma poco cliccati: si riscrive titolo e primo tag."""
    out = []
    for voce in listing:
        if int(voce.get("giorni_online", 0)) < GIORNI_MINIMI:
            continue
        if int(voce.get("visite", 0)) >= VISITE_MINIME and float(voce.get("ctr", 0)) < 1.5:
            out.append(voce)
    return out


def autonomia(cassa, burn_giornaliero):
    """Giorni di cassa residui al burn effettivo. None se non c'è burn."""
    if not burn_giornaliero or burn_giornaliero <= 0:
        return None
    return int(cassa / burn_giornaliero)
