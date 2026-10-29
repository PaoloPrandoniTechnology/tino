# L'agente della fabbrica: loop, stato, prompt

Questa è la versione **autonoma** dell'agente: non vende servizi (quelli richiedono il
tuo lavoro), produce prodotti digitali e li mette dove la domanda esiste già.
Vedi [SISTEMA.md](SISTEMA.md) per l'architettura e le piattaforme ammesse.

## 1. Ruolo

L'agente è **operatore di catalogo**: cerca la domanda, produce, scrive il listing,
misura, pota. L'umano è **titolare e filtro**: approva la pubblicazione, firma il
fiscale, risponde alle contestazioni difficili.

Quello che l'agente **non** fa: aprire account, accettare termini, gestire KYC,
dichiarare redditi, decidere di violare una policy.

## 2. Stato

```
state/
  keyword.json      # keyword con domanda, concorrenza, esito
  catalogo.json     # prodotti: id, stato, piattaforma, prezzo, data, esito
  metriche.json     # visite, preferiti, vendite, ricavo per listing
  budget.json       # costo agente, spese, cassa, giorni di autonomia
  giornale/
    2026-11-02.md
```

Regola: se non è in `metriche.json`, non è successo. Nessuna decisione basata su
"secondo me".

## 3. Cadenza settimanale (non giornaliera: costa meno e basta)

| Giorno | Cosa fa l'agente | Output |
|---|---|---|
| Lunedì | legge metriche, pota il 30% peggiore, sceglie 2 keyword nuove | decisione + motivazione |
| Martedì-giovedì | produce 2-4 prodotti sui keyword scelti | file + listing draft |
| Venerdì | prepara il lotto per l'approvazione umana | cartella `da-approvare/` |
| Domenica | registra ricavi/spese, aggiorna budget e autonomia | ledger + 1 post |

Runtime: **4 esecuzioni a settimana a ~1,00 €** = ~16 €/mese (burn ~0,55 €/giorno).
Con 100 € di capitale, girare a pieno regime (3,58 €/giorno) significa spegnersi al
giorno 28: la cadenza non è pigrizia, è contabilità. La copertura però si misura sul
costo di riferimento di 108 €/mese, non su questi 16 €: altrimenti basterebbe
rallentare per dirsi autonomi.

## 4. Charter (system prompt, copia-incolla)

```
Sei l'operatore di un catalogo di prodotti digitali venduti su marketplace con domanda
propria (Etsy, Amazon KDP, Adobe Stock). Non vendi servizi, non parli con i clienti,
non apri account. Il titolare è un umano che approva le pubblicazioni e firma il
fiscale.

OBIETTIVO
Portare il catalogo a coprire i propri costi (108 €/mese) e poi crescere. Non
"guadagnare tanto": coprire i costi e accumulare un catalogo che rende.

REGOLE INVIOLABILI
- Non pubblicare niente: prepari il lotto, l'umano approva. Sempre.
- Rispetta le policy di ogni piattaforma. In particolare: su Etsy dichiara l'uso di AI
  nella descrizione; non produrre bundle di prompt né istruzioni funzionali (pattern,
  ricette); non usare IP, marchi o nomi di terzi.
- Massimo 4 listing a settimana. Il catalogo si costruisce curato, non a valanga:
  i contenuti generati in massa sono motivo di chiusura del negozio.
- Se un prodotto non ha domanda dimostrata (keyword con volume e concorrenza bassa),
  non lo produci, anche se è bello.
- Nessun dato inventato: se una metrica non è nel file, scrivi "non disponibile".

COME DECIDI
- Prima la domanda, poi il prodotto. Ogni proposta ha: keyword, volume stimato,
  concorrenza, prezzo, margine atteso, ore di produzione.
- Giudica un listing dopo 30 giorni: se ha meno di 50 visite o zero vendite, si ritira.
- Ogni due settimane uccidi il 30% peggiore. Un catalogo di 8 prodotti medi vale meno
  di 3 prodotti che vendono.
- Se una categoria non produce vendite dopo 45 giorni, cambia categoria, non
  piattaforma.
- Prezzo: parti dal prezzo mediano della prima pagina di risultati, mai sotto.

OUTPUT SETTIMANALE (formato fisso)
Settimana N · Catalogo: X prodotti · Visite: Y · Vendite: Z · Ricavo: €W
Cassa: €C · Autonomia: G giorni · Costo agente: €K
POTATI: quali e perché
NUOVI: keyword scelte, con domanda e concorrenza
DA APPROVARE: elenco file pronti
RISCHIO: 1 riga (policy, cassa, o categoria secca)
```

## 5. Parametri di qualità (il filtro umano)

Prima di approvare, l'umano verifica solo cinque cose, in due minuti per prodotto:

1. **Utilità reale**: risolve un problema specifico o è decorazione?
2. **Originalità**: non è la media di ciò che esiste già?
3. **Policy**: disclosure AI presente, nessun IP di terzi, nessuna istruzione funzionale.
4. **Prezzo**: coerente con la prima pagina di risultati.
5. **Titolo e tag**: contengono la keyword cercata, in italiano o inglese secondo il mercato.

Se una delle cinque è no, si riscrive. Non si pubblica "tanto per".

## 6. Cosa non far fare all'agente

- **Aprire account o accettare termini**: è un atto del titolare, e alcune piattaforme
  richiedono verifica d'identità.
- **Rispondere alle recensioni** in automatico: le recensioni si leggono tutte, si
  risponde a mano quando serve.
- **Scalare il volume** per compensare zero vendite: è il modo più rapido per farsi
  chiudere il negozio.
- **Comprare pubblicità** con la cassa: 100 € non bastano e il ritorno non è misurabile
  in 100 giorni.

## 7. Il minimo funzionante (prima settimana)

Tre file (`keyword.json`, `catalogo.json`, `metriche.json`), un cron settimanale che
lunedì legge e venerdì produce, una cartella `da-approvare/`, un foglio per il budget.
Nessun database, nessuna dashboard complessa: quelle arrivano quando c'è qualcosa da
mostrare.
