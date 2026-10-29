# Come opera Tino, nel concreto

Questo è il runbook: non la strategia, l'operatività. Cosa succede lunedì mattina,
cosa produce l'agente, cosa guarda l'umano, quando si pota, dove finiscono i soldi.

## 0. In una frase

Tino non "guadagna": **trova domanda, costruisce l'oggetto che la soddisfa, lo mette
dove la gente lo cerca, misura, pota.** Quattro esecuzioni a settimana, per sempre.

## 1. La settimana

| Quando | Chi | Cosa fa | Output | Tempo |
|---|---|---|---|---|
| Lun 07:00 | agente | legge le metriche della settimana, calcola ricavo per listing, pota il 30% peggiore, sceglie 2 keyword | `potati.md` + 2 keyword con numeri | 1 esecuzione |
| Lun 08:00 | umano | legge il report (10 righe) e approva la potatura | sì/no su 2-3 righe | 15 min |
| Mar-gio | agente | produce 2-4 prodotti sulle keyword scelte, confeziona, scrive i listing | `da-approvare/` con file + bozze | 2 esecuzioni |
| Ven 08:00 | umano | **qualità**: 5 check per prodotto, 2 minuti l'uno; pubblica quello che passa | listing online | 45-60 min |
| Dom 18:00 | agente | registra ricavi e spese, aggiorna budget e autonomia, scrive il post della settimana | ledger + 1 post | 1 esecuzione |

Totale umano: **1,5-2 ore a settimana** nei primi due mesi, mezz'ora a regime. Se
pubblicare ti prende di più, il collo di bottiglia è la qualità dell'agente e va
corretta la produzione, non aggiunto tempo tuo.

## 2. Il ciclo di produzione, in sette passi

**Passo 1 — Keyword (agente, ~10 min).** Estrae 20 candidate da Etsy, Amazon e Pinterest.
Le filtra con quattro criteri, tutti obbligatori:

| Criterio | Soglia | Se non passa |
|---|---|---|
| Domanda | ≥ 500 ricerche/mese stimate, o ≥ 20 annunci "best seller" nella categoria | keyword scartata |
| Concorrenza | ≤ 3 venditori con > 1.000 recensioni nei primi 12 risultati | scartata o nicchia più stretta |
| Prezzo mediano | ≥ 12 € nella prima pagina | scartata (sotto, il margine non paga il listing) |
| Stagionalità | non dipendente da una data | ok solo come prodotto secondario |

Output: **2 keyword**, ognuna con volume, concorrenza, prezzo mediano e un link ai
primi tre risultati. Se nessuna passa, la settimana si salta: non si produce per
riempire il calendario.

**Passo 2 — Scheda prodotto (agente, ~10 min).** Chi compra, quale problema ha, in che
formato lo risolvi, quanto costa, in cosa è diverso dai primi tre risultati. Una pagina.

**Passo 3 — Produzione (agente, 40-90 min).** Un prodotto = un problema. Se la scheda
contiene due problemi, si spezza in due prodotti.

**Passo 4 — Confezione (agente, ~20 min).** File utilizzabile senza spiegazioni, 5
immagini di anteprima (la prima deve far capire cosa è in 2 secondi), istruzioni
d'uso, licenza chiara (uso personale / commerciale).

**Passo 5 — Listing (agente, ~15 min).** Titolo ≤ 140 caratteri con la keyword in
testa, 13 tag, descrizione in quattro blocchi (cosa è / cosa risolve / cosa contiene /
licenza), disclosure AI dove richiesta, prezzo allineato alla prima pagina.

**Passo 6 — Qualità (umano, 2-5 min).** Cinque domande, in ordine:

1. Un estraneo capisce cosa compra dalla prima immagine?
2. Risolve un problema o è decorazione?
3. La keyword cercata è nel titolo, nelle prime parole?
4. Disclosure presente? Nessun IP, marchio o nome di terzi?
5. Il prezzo regge il confronto con i primi tre risultati?

Due "no" = si riscrive. Un prodotto bocciato non si pubblica "tanto per": costa 0,20 $
e, se va male, abbassa la qualità percepita del negozio.

**Passo 7 — Pubblicazione (umano, 2 min).** Caricamento, prezzo, download automatico,
eventuale prova d'acquisto.

## 3. Come legge i numeri

**Ogni lunedì, per listing:** visite, preferiti, ordini, ricavo, tasso di conversione.
**Una volta al mese, per il negozio:** ricavo per listing attivo, crescita mese su mese,
copertura sul costo di riferimento.

Soglie operative, non opinioni:

| Situazione | Soglia | Azione |
|---|---|---|
| Listing invisibile | < 50 visite a 30 giorni | potatura immediata |
| Listing visto ma non comprato | CTR > 2% ma conversione < 1% | cambia prezzo o rifai le anteprime |
| Trovato ma cliccato poco | impression alte, CTR < 1,5% | riscrivi titolo e primo tag |
| Vende | ≥ 2 ordini a settimana | clona **il formato** in 3 varianti |
| Categoria secca | 45 giorni, zero ordini totali | cambia categoria, non piattaforma |

## 4. La potatura (il lavoro che genera ricavo)

Ogni due settimane: si ordina per **ricavo per visita**, si ritira il 30% peggiore.
I file non si cancellano: si spostano in `state/potati/` con una riga di motivo
("keyword sbagliata", "prodotto debole", "prezzo fuori mercato").

Serve a due cose: tenere il negozio pulito (la qualità media è un segnale per l'algoritmo)
e capire **perché** un prodotto non ha funzionato. Dopo tre potature, i motivi ricorrenti
dicono dove l'agente sbaglia: di solito è la scelta della keyword, non l'esecuzione.

## 5. Il denaro

**Entrate.** Etsy versa settimanalmente sopra il minimo; KDP paga a ~60 giorni; Adobe
Stock a 45 giorni dal primo pagamento. Per questo Etsy è il primo negozio aperto e KDP
il secondo: non per il margine, per la velocità della cassa.

**Tasse.** Partita IVA forfettaria (5% per i primi cinque anni sotto 85.000 €) + INPS
sul 78% dell'imponibile: prelievo effettivo ~24%. Su 100 € incassati restano ~76 €, e
**la copertura si calcola sul netto**. Fatture e dichiarazione: commercialista, 1-2 ore
di tuo tempo all'anno, non al mese.

**Ripartizione (regola 6).** Del netto mensile: **30% capacità**, **20% riserva**,
**50% al titolare**. Esempio su 300 € netti: 90 € tornano in runtime e modelli, 60 €
restano in riserva, 150 € sono tuoi.

**Prelievi.** Consentiti solo quando la cassa supera 3 volte il costo mensile di
riferimento (324 €). Prima di allora i soldi restano dentro: è la differenza tra un
progetto e una paghetta.

## 6. Le eccezioni (albero delle decisioni)

| Evento | Cosa fa l'agente | Cosa fa l'umano |
|---|---|---|
| **Avviso di policy** | ferma la produzione, non tocca nulla | rilegge la policy, corregge il catalogo, riparte con 1 prodotto |
| **Prodotto che decolla** (>3 ordini/giorno) | prepara 3 varianti dello stesso formato | approva in priorità, lascia indietro il resto |
| **Cassa < 10 giorni** | taglia runtime e tool, produce un prodotto a costo zero | decide se continuare o chiudere secondo regola |
| **Contestazione o rimborso** | prepara i fatti | risponde entro 24 h, rimborsa sotto 50 € senza discutere |
| **Recensione negativa** | non risponde | risponde a mano, mai template, senza difendersi |
| **Nessuna keyword valida** | salta la settimana e lo scrive | nessuna azione: saltare è la risposta corretta |
| **Due stagioni senza crescita** | prepara il resoconto finale | chiude e pubblica i conti |

## 7. Cosa Tino non farà mai

- Pubblicare senza approvazione umana.
- Aprire account o accettare termini di servizio.
- Comprare recensioni, follower o pubblicità senza tre mesi di copertura.
- Produrre in massa per compensare zero vendite.
- Toccare dati dei clienti oltre a quanto serve per evadere un ordine.
- Dire un numero che non è nel ledger.

## 8. Il primo giorno, letteralmente

1. Apri il conto dell'entità, versa 100 €, registra il movimento con fonte.
2. Apri il negozio Etsy: KYC, dati fiscali, metodo di pagamento. (2-3 ore, una volta.)
3. Fai girare l'esecuzione #1: 20 keyword, filtri, 2 scelte.
4. Approva o boccia le 2 keyword. Se bocci, l'agente ne propone altre 4.
5. Metti in `state/` i tre file vuoti: `keyword.json`, `catalogo.json`, `metriche.json`.
6. Pubblica il primo aggiornamento con i numeri veri: 100 €, 16 €/mese di spesa, ~175
   giorni di autonomia di cassa, obiettivo copertura sul costo di riferimento.
7. Giovedì: primo lotto in `da-approvare/`. Venerdì: primo listing online.

Da lì in poi non cambia nulla: quattro esecuzioni a settimana, un'ora di supervisione,
una potatura ogni due settimane. Se in sei settimane non c'è una vendita, il problema
è la keyword o il prezzo — non il numero di prodotti.
