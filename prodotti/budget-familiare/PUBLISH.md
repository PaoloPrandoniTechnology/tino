# Pubblica su Etsy — blocchi da incollare

Tutto quello che serve è qui. Tu fai solo click, login e incolla: il resto è già scritto.

## 0. I due link e le due azioni tue

| Cosa | Link | Cosa fai |
|---|---|---|
| Repository | https://github.com/new?name=tino&visibility=public | Crea repo `tino`, **pubblico**, senza README né .gitignore (ci sono già) |
| Negozio | https://www.etsy.com/sell | Apri il negozio: KYC, dati fiscali, IBAN |
| Listing | https://www.etsy.com/your/shops/me/tools/listings/create | Compila con i blocchi qui sotto |

Repository già creato e collegato: `https://github.com/PaoloPrandoniTechnology/tino`.
Per ripubblicare manualmente, dalla cartella del progetto:

```bash
bash COLLEGA-GITHUB.sh PaoloPrandoniTechnology
```

Lo script imposta il remote, committa quello che manca e pusha su `main`.
Se il push chiede la password: usa un **token** (GitHub → Settings → Developer settings →
Personal access tokens → Fine-grained → scope `Contents: write` sul repo `tino`), non la password
dell'account.

## 1. File da caricare

| Cosa | File |
|---|---|
| Prodotto | `Budget_Familiare_2027.xlsx` |
| Anteprima 1 | `anteprime/01-copertina.png` |
| Anteprima 2 | `anteprime/02-cosa-contiene.png` |
| Anteprima 3 | `anteprime/03-foglio-budget.png` |
| Anteprima 4 | `anteprime/04-riepilogo.png` |
| Anteprima 5 | `anteprime/05-come-si-usa.png` |

## 2. Titolo (incolla così com'è, 125 caratteri)

```
Budget Familiare Excel 2027 | Gestione spese, entrate e risparmio | Foglio di calcolo mensile e annuale | Download immediato
```

## 3. Tag — 13, uno per campo

```
budget familiare
gestione spese
excel budget
foglio spese
risparmio
budget mensile
planner finanze
spese casa
budget 2027
excel italiano
budget annuale
controllo spese
finanze personali
```

Se Etsy ti lascia un solo campo: `budget familiare, gestione spese, excel budget, foglio spese, risparmio, budget mensile, planner finanze, spese casa, budget 2027, excel italiano, budget annuale, controllo spese, finanze personali`

## 4. Descrizione (testo semplice, incolla così com'è)

```
Budget Familiare 2027 — foglio di calcolo Excel

COSA È
Un file Excel (.xlsx) per tenere entrate, uscite e risparmio di casa in un posto solo. Dodici mesi in una schermata, categorie modificabili, totale annuale e tasso di risparmio calcolati dalle formule.

COSA RISOLVE
Sai quanto entra e quanto esce, ma non quanto ti resta davvero. Qui il saldo di ogni mese e il risparmio dell'anno si aggiornano da soli appena inserisci una spesa: niente conti a mano, niente doppioni.

COSA CONTIENE
• Foglio Budget: 9 categorie (2 entrate, 7 uscite), budget mensile, 12 mesi, totale annuo, media mensile e scostamento dal budget.
• Foglio Riepilogo: entrate e uscite dell'anno, risparmio, tasso di risparmio, media mensile e quota di ogni categoria sulle uscite totali.
• Foglio Istruzioni: tre righe, niente di più.

COME SI USA
Sostituisci le categorie con le tue, scrivi il budget mensile nella colonna C, poi inserisci le spese reali mese per mese. Tutto il resto è formula.

REQUISITI
Excel 2016 o successivo, LibreOffice o Google Fogli. Nessuna macro, nessun accesso a internet, nessun dato inviato da nessuna parte.

CONSEGNA
Download immediato dopo l'acquisto. Il file è tuo, senza scadenza.

LICENZA
Uso personale e familiare. Non è consentita la rivendita del file, anche modificato.

NOTA
Non è una consulenza finanziaria: è uno strumento di organizzazione delle spese.

Contenuto realizzato con l'assistenza di strumenti di intelligenza artificiale e verificato prima della pubblicazione: formule, categorie e istruzioni sono state controllate a mano.
```

## 5. Prezzo e impostazioni

- **Prezzo: 14,90 €**
- Tipo: **Digital download** (consegna istantanea)
- Quantità: illimitata
- Categoria: scrivi `budget spreadsheet` nel campo categoria e scegli quella dove compaiono i listing simili — non inventare una categoria nuova
- Rinnovo automatico: attivo
- Spedizione: nessuna (è digitale)

## 6. Cosa controllare prima di premere Publish

1. Le cinque anteprime caricate, nell'ordine (la copertina per prima).
2. Il titolo non ha refusi e contiene "Budget Familiare Excel" all'inizio.
3. I 13 tag sono tutti nel campo, nessuno tagliato.
4. La descrizione contiene la frase sull'uso dell'AI (Etsy la richiede).
5. Il prezzo è 14,90 € e non c'è uno sconto di lancio.

## 7. Dopo la pubblicazione

Registra la commissione del listing nel ledger:

```bash
python3 -c "from agente import ledger; ledger.append('state/ledger.jsonl','uscita',0.19,'Listing Etsy #1','etsy','produzione','2026-11-02')"
python3 -m agente.loop --no-llm
git add -A && git commit -m "listing online: budget familiare 2027" && git push
```

Poi incolla qui il link del listing: lo aggiungo al catalogo e alla dashboard.
