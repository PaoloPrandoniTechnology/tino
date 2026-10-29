# Tino

**Un agente AI che parte con 100 € e deve smettere di pesare sui conti di chi lo
mantiene. Poi crescere.**

Nessun pubblico, nessuna rete di contatti, nessun cliente da chiamare. Tino vende
prodotti digitali dove i compratori esistono già — Etsy, Amazon KDP, Adobe Stock — e
lavora come si gestisce un catalogo: cerca domanda, produce l'oggetto che la soddisfa,
misura, pota il 30% peggiore, ricomincia. Quattro esecuzioni a settimana.

L'umano non vende, non scrive listing, non parla con nessuno. Approva le pubblicazioni,
firma il fiscale e risponde alle contestazioni difficili: **1-2 ore a settimana** nei
primi due mesi, mezz'ora a regime.

## Il traguardo non è una cifra

È una curva. Tre numeri, sempre gli stessi:

| Metrica | Cosa significa | Quando è un successo |
|---|---|---|
| **Copertura** | ricavo del mese ÷ costo del mese | ≥ 100% per tre mesi consecutivi |
| **Crescita** | ricavo mensile rispetto alla stagione precedente | ≥ +50% a ogni stagione |
| **Ricavo per listing** | quanto rende ogni prodotto attivo, non quanto produce in totale | stabile o crescente |

Copertura al 100% significa che l'agente non pesa più. Al 150% comincia a finanziare la
propria crescita. Sotto il 100% è un progetto sovvenzionato, e va detto.

**Perché non "guadagnare X €":** un importo promesso si smentisce alla prima verifica e
ti costa la credibilità che serve per tutto il resto. La copertura non si può barare:
o i conti tornano, o no.

## Come funziona, in cinque righe

La distribuzione non si costruisce, si affitta: si vende su marketplace che hanno già
i compratori dentro. L'agente produce, confeziona il listing, misura e pota; l'umano
approva e firma. Il modello non è un prodotto che vende, è un **catalogo che si
accumula**: ogni listing pubblicato continua a essere trovato anche quando l'agente
dorme. Il collo di bottiglia è la qualità, non la quantità — 2-4 listing a settimana,
mai di più, perché i contenuti generati in massa chiudono il negozio.

## Cosa c'è qui

| File | Cos'è |
|---|---|
| [SISTEMA.md](SISTEMA.md) | Architettura: principio, piattaforme verificate, equazione della crescita, kill rules. |
| [OPERATIVO.md](OPERATIVO.md) | Il runbook: la settimana, i sette passi di produzione, le soglie, la potatura, i soldi. |
| [PRODOTTI.md](PRODOTTI.md) | Cosa produce: famiglie di prodotto, listino, esclusioni, test di validità. |
| [AGENTE-FABBRICA.md](AGENTE-FABBRICA.md) | Il loop dell'agente, lo stato, il charter, il filtro di qualità umano. |
| [DISTRIBUZIONE.md](DISTRIBUZIONE.md) | Come trova visite: cosa si automatizza per via ufficiale, i tre formati, il funnel, i livelli di sostenibilità. |
| [INFRA.md](INFRA.md) | Dove vive: repository, cron, stato, segreti, costi reali. |
| [NOTIFICHE.md](NOTIFICHE.md) | Come il conto del giorno arriva sul telefono: Telegram e WhatsApp, passi e costi. |
| [REGOLAMENTO.md](REGOLAMENTO.md) | Le regole pubbliche: capitale, curva, contabilità, cosa si pubblica. |
| `agente/` | Il codice: ledger append-only, metriche, loop, chiamata opzionale al modello. |
| `dashboard/` | La vetrina: copertura, crescita, catalogo, movimenti, giornale di bordo. |
| `prodotti/` | Il primo prodotto: file Excel, anteprime, listing pronto da pubblicare. |

## Cosa vedi e cosa non vedi

Questo progetto vale quanto la possibilità di controllarlo. Quindi:

**Pubblico.** Capitale e ogni movimento del ledger, ricavi e costi aggregati, catalogo e
stato dei listing, decisioni con il motivo, giornale di bordo quotidiano, codice
dell'agente, storico dei commit.

**Non pubblico.** Dati personali e fiscali del titolare, credenziali e chiavi, dati dei
clienti oltre a quanto serve per evadere un ordine, i file vendibili (stanno in un
archivio privato: un file in un repo pubblico è un file gratis), comunicazioni private
con clienti e piattaforme.

Regola unica: **ogni numero pubblicato ha una fonte nel ledger.** Se la fonte non c'è,
il numero non si pubblica. Nessuna stima presentata come incasso, nessun follower
contato come cliente.

## Le regole che non si cambiano in corsa

1. **100 € esatti** di partenza. Nessun euro esterno, mai.
2. Autocopertura entro il **giorno 100**, sostenuta **tre mesi**.
3. Ogni stagione chiude con ricavo mensile **almeno +50%**.
4. Due stagioni senza crescita chiudono il progetto.
5. Sopra **25 €** di spesa decide l'umano, non l'agente.
6. Cassa sotto **7 giorni**: l'agente taglia i propri costi prima di chiedere altro lavoro.
7. Vietati trading, scommesse, crypto, follower e recensioni comprate, pubblicazione in massa.

Le regole complete, con le sanzioni, stanno in [REGOLAMENTO.md](REGOLAMENTO.md).

## Seguire il progetto

Il repository è la fonte: ogni esecuzione lascia un commit con data, diff e log. La
dashboard è un sito statico che legge `data.json` committato dall'agente — nessun
server, nessun database, nessun numero inserito a mano. I canali pubblicano gli stessi
numeri della dashboard, con la cadenza e i formati descritti in
[DISTRIBUZIONE.md](DISTRIBUZIONE.md): un video senza una cifra presa dal ledger non
esce.

```bash
python3 -m http.server 3000 -d dashboard
# → http://localhost:3000
```

Il ledger si verifica in un comando:

```bash
python3 -m agente.ledger --check state/ledger.jsonl
# → OK: catena integra
```

Se un movimento viene modificato o rimosso, la catena di hash si rompe e il controllo
fallisce: è il motivo per cui il ledger è append-only e non un foglio che si può
aggiustare.
