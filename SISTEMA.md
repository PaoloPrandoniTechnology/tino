# Il sistema che si alimenta da solo

> Requisito: l'utente fa **solo supervisione** e il minor numero possibile di compiti
> fisici. Traguardo: **autocopertura**, poi **crescita mese su mese**. Non un importo
> in euro, una curva.

## 1. Il principio architetturale

**Non automatizzare lo scambio: affittare la distribuzione.**

Vendere richiede fiducia. La fiducia o la costruisci (pubblico, faccia, tempo) o la
prendi in prestito da un marketplace che ha già i compratori dentro. Non esiste una
terza strada, e questa è la differenza tra "ho un agente che produce" e "ho un sistema
che incassa".

Da qui due conseguenze che eliminano il 90% delle idee sbagliate:

1. **Le piattaforme che richiedono che il pubblico lo porti tu non servono**
   (Gumroad in vendita diretta, Lemon Squeezy, Whop come storefront). Sono casse,
   non canali.
2. **Le piattaforme che vietano l'automazione vanno escluse a priori** (Fiverr, Upwork).
   Non è un limite tecnico, è un rischio di ban permanente.

E una precisazione che va detta subito: **"100% autonomo" non esiste**, non per limiti
tecnici ma giuridici. Il denaro ha bisogno di un soggetto che faccia KYC, abbia un IBAN,
una partita IVA e una responsabilità. Nessuna piattaforma apre un conto a un agente.
L'autonomia possibile è **operativa**: la macchina produce, misura e itera; l'umano
resta il titolare legale e il filtro di qualità.

## 2. Cosa resta all'umano (quantificato)

| Attività | Frequenza | Tempo | Delegabile? |
|---|---|---|---|
| KYC, apertura negozi, dati fiscali | una volta | 2-3 h | No |
| Approvazione pubblicazione + qualità | per lotto | 30 min/settimana | No (policy + rischio ban) |
| Tasse, fatture, commercialista | mensile | 1-2 h | Al commercialista (a pagamento) |
| Contestazioni, rimborsi, assistenza difficile | raro | 30 min/settimana | Parzialmente (template) |
| Decisioni di strategia (cosa produrre, cosa potare) | settimanale | 1 h | No, ma è mezz'ora di lettura |
| **Totale primi 60 giorni** | | **4-6 h/settimana** | |
| **A regime** | | **2-3 h/mese** | |

**Compiti fisici: zero.** I prodotti digitali non si spediscono. Se in futuro vuoi il
fisico, Redbubble e Printful stampano e spediscono loro: l'umano non tocca niente.

## 3. Il motore: fabbrica di prodotti su marketplace con domanda propria

Sei componenti, in quest'ordine. Nessuno dei sei richiede che tu parli con qualcuno.

1. **Ricerca della domanda** — non "cosa so fare", ma "cosa stanno cercando". Si parte
   da keyword con domanda dimostrata e concorrenza bassa, non da intuizioni.
2. **Produzione** — l'agente costruisce l'asset (template, guida, pack, asset grafico,
   piccolo software). 2-4 ore per prodotto, non 40.
3. **Packaging e listing** — titolo, tag, descrizione, immagini. Su Etsy **la SEO del
   listing è il 70% del risultato**, non il prodotto.
4. **Pubblicazione** — l'umano approva. Obbligatorio: per le policy e perché un lotto
   sbagliato chiude il negozio.
5. **Misura** — visite, preferiti, conversione, ricavo per listing. Dati veri, non
   impressioni.
6. **Potatura** — ogni due settimane si uccide il 30% peggiore e si produce nuovo.
   Il modello è un **portafoglio**, non un prodotto: 8 prodotti su 10 rendono zero.

## 4. Le piattaforme ammesse (verificate a ottobre 2026)

| Piattaforma | Cosa ci vendi | AI ammessa | Commissioni | Payout | Traffico proprio | Verdetto |
|---|---|---|---|---|---|---|
| **Etsy** | digital download, template, pack | Sì, con **disclosure** in descrizione; vietati contenuti generati da bot, istruzioni funzionali (pattern, ricette) e bundle di prompt | 0,20 $/listing + 6,5% + processing; 12-15% su ordini da Offsite Ads | minimo giornaliero variabile (es. 25 $), versamenti settimanali | **Sì**, ricerca interna forte | **Primaria** |
| **Amazon KDP** | ebook, planner, libri | Sì, con **disclosure** AI su testo/immagini/traduzioni | royalty 35% o 70% | mensile, ~60 giorni dopo | Sì (Amazon) | **Primaria**, ma cassa lenta |
| **Adobe Stock** | immagini, illustrazioni | Sì, con **etichetta** "generato con AI" | royalty 33% (35% video) | 25 $ minimo, ≥45 giorni dalla prima vendita | Sì | **Secondaria** (volume) |
| **Redbubble** | stampa su prodotti fisici | nessun divieto generale trovato | ~50% fee (tier Standard) | soglia 10 € dal luglio 2026 | Sì | **Opzionale**: il fisico lo gestiscono loro |
| **Creative Market** | asset di design | etichetta AI prevista | ~50% al venditore | 20 $ minimo | Sì | Valutare (dati provvisori) |
| **Gumroad** | qualsiasi digitale | nessun divieto specifico | 10% + 0,50 $ diretto, **30%** via Discover | 100 $ minimo | solo Discover | Dopo, come cassa propria |
| **Whop** | community, digitale | nessun divieto specifico | 2,7% + 0,30 $ | 10 $ minimo | marketplace, non garantito | Dopo |
| **Lemon Squeezy** | digitale | nessun divieto | 5% + 0,50 $ | 50 $ minimo | **solo dopo 3 vendite** | Non per partire |
| **Envato** | template, asset | **AI non ammessa come componente principale** | ~50% | 50 $ | Sì | **Esclusa** |
| **Shutterstock** | stock | **AI-generated non accettata** | 15-40% | 25 $ | Sì | **Esclusa** |
| **Fiverr / Upwork** | servizi | AI ammessa, ma **account gestito da agente = rischio ban** (automazione e messaggistica automatizzata vietate) | 20% | 14 giorni | Sì | **Esclusa** |

Fonti ufficiali lette: [Etsy – cosa si può vendere](https://help.etsy.com/hc/en-us/articles/360024112614-What-Can-I-Sell-on-Etsy),
[Etsy – fee](https://help.etsy.com/hc/en-us/articles/115014483627-What-are-the-Fees-and-Taxes-for-Selling-on-Etsy),
[KDP – linee guida](https://kdp.amazon.com/en_US/help/topic/G200672390),
[KDP – royalty](https://kdp.amazon.com/help/topic/G200644210),
[Shutterstock – FAQ AI](https://submit.shutterstock.com/help/en/articles/10594676-ai-generated-content-on-shutterstock-contributor-faq),
[Gumroad – prezzi](https://gumroad.com/pricing),
[Lemon Squeezy – fee](https://docs.lemonsqueezy.com/help/getting-started/fees),
[Whop – fee](https://docs.whop.com/fees),
[Fiverr – linee guida AI](https://help.fiverr.com/hc/en-us/articles/34998793899665-Using-AI-on-Fiverr-Guidelines-for-freelancers-and-clients),
[Upwork – automazione](https://support.upwork.com/hc/en-us/articles/43342677368467-Use-bots-and-other-automation-properly).
Le voci Creative Market, Redbubble, Adobe Stock ed Envato provengono da risultati ufficiali
ma con pagina non accessibile: da riverificare prima di aprire un negozio.

## 5. I numeri di sopravvivenza

**Costo di riferimento: 108 €/mese** (3,58 €/giorno, agente a pieno regime). È questo
il numero su cui si misura la copertura, **non la spesa effettiva**: se il traguardo
fosse "ricavi ≥ quanto spendo", basterebbe far girare l'agente tre volte al mese per
dichiararsi autonomi. La spesa reale può essere più bassa in avvio; il metro no.

**Spesa effettiva in bootstrap: ~16 €/mese.** Quattro esecuzioni a settimana a ~1,00 €
= 52 esecuzioni in 90 giorni, circa 52 €. Con i 100 €: dominio 10 € + listing (30 ×
0,20 $) ~6 € + agente 52 € = **68 €**, restano 32 € di margine. Burn medio ~0,55 €/giorno.

**Break-even.** Con forfettario (5% per i primi cinque anni, sotto 85.000 €) e INPS sul
78% dell'imponibile, il prelievo effettivo è ~24%: per netto 108 €/mese servono circa
**143 €/mese lordi** (6 vendite a 25 €, oppure 40 a 4 €). Attenzione al numero che
spaventa: la copertura sui 108 € di riferimento arriva intorno al terzo mese, mentre
la cassa (grazie alla spesa in bootstrap) dura molto di più.

**Autonomia con 100 €.** A regime pieno (3,58 €/giorno) si spegne al **giorno 28**,
prima del primo versamento (Etsy settimanale, Adobe 45 giorni, KDP 60). A burn di
bootstrap (~0,55 €/giorno) la cassa copre ~175 giorni: è questa la ragione tecnica per
cui Tino non gira tutti i giorni, e va detta nel primo video.

**Aspettativa realistica, partendo da zero pubblico:** a 100 giorni 10-15 listing e
0-1.500 € totali; la copertura dei costi arriva intorno al terzo mese, non prima. I
marketplace impiegano 2-8 settimane a indicizzare un listing: i primi 45 giorni sono
quasi sempre a zero.

**Il numero che conta non è l'incasso: è la copertura.** Ricavo del mese diviso costo
del mese. 30% = l'agente lavora per te a un terzo del prezzo. 100% = non pesa più.
150% = comincia a crescere da solo.

## 6. Come crescono i guadagni nel tempo

Il modello non è un prodotto che vende: è un **catalogo che si accumula**. Ogni listing
pubblicato continua a esistere e a essere indicizzato anche quando l'agente dorme.
Quindi il ricavo non è lineare nel tempo: è una funzione del catalogo, e il catalogo
cresce a ogni settimana che passa.

**L'equazione, in soldi veri:**

```
ricavo mensile ≈ listing attivi × visite medie per listing × conversione × prezzo
```

Con numeri prudenti (10 visite al mese per listing, tipiche di un negozio nuovo):
40 × 10 × 1,5% × 22 € ≈ **132 €/mese**. Con 120 listing: ≈ **396 €/mese**.
Con 250 listing: ≈ **825 €/mese**.

A negozio maturo le visite per listing salgono (20-30): lo stesso catalogo di 40
listing rende allora 264-396 €/mese, senza un prodotto in più. **La crescita non
richiede solo più prodotti: richiede che quelli che hai vengano trovati.** Per questo
la SEO del listing vale più della produzione, e per questo la potatura è un'attività
di ricavo, non di pulizia.

**Il vincolo è la qualità, non la voglia.** 2-4 listing a settimana (10-16 al mese) è il
massimo compatibile con le policy e con un catalogo che non faccia schifo. Ecco perché
il traguardo è una curva a 12 mesi:

| Mese | Catalogo | Ricavo atteso | Copertura (costo 108 €) |
|---|---|---|---|
| 1 | 12 | 0-20 € | 0-20% |
| 3 | 35 | 60-150 € | 55-140% |
| 6 | 70 | 200-450 € | 185-415% |
| 12 | 130 | 500-1.500 € | 460-1.390% |

Le forbici sono ampie perché il 70-80% dei listing rende zero e uno o due pagano per
tutti. Il lavoro dell'agente è **trovare e potare**, non produrre di più.

**Il ciclo che si autoalimenta** (regola 6 del regolamento): 30% del ricavo netto torna
in capacità — più runtime, modelli migliori, poi advertising — 20% in riserva, il resto
al titolare. La capacità può crescere solo se cresce il ricavo. È questo che distingue
un sistema che si alimenta da un sistema che consuma il tuo conto in banca: **la spunta
la curva, non l'entusiasmo.**

**Le tre metriche della crescita**, da guardare una volta al mese e mai più spesso:

1. **Ricavo per listing attivo** — se scende, stai producendo prodotti sbagliati.
2. **Crescita mese su mese** — sotto +10% per tre mesi, il catalogo è pieno di rumore.
3. **Copertura** — sotto 100% non sei autonomo, sei sovvenzionato.

## 7. Le regole del sistema (kill rules)

- Dopo **45 giorni** senza una sola vendita: si cambia categoria di prodotto, non
  piattaforma (la piattaforma non è il problema se il traffico esiste).
- Un listing con **0 vendite e < 50 visite in 30 giorni** si ritira.
- Se il costo dell'agente supera il **40% dell'incasso** per due mesi, si riduce il runtime.
- Un **avviso di policy** ferma la produzione e apre una revisione umana.
- Due stagioni consecutive senza crescita: il progetto si ferma e si racconta.
  Fermarsi secondo regola è un finale, non una sconfitta.

## 8. I primi 30 giorni (2 ore di supervisione a settimana)

**Giorni 1-3** — Tre candidati di categoria (es. planner digitali, template per
professionisti, asset grafici). L'agente estrae 10 keyword con domanda e concorrenza
bassa da Etsy/Amazon. Scegli quella con il rapporto domanda/offerta migliore.
KYC Etsy, apertura negozio.

**Giorni 4-7** — 3 prodotti finiti + listing completi. Tu approvi e pubblichi.
Disclosure AI in ogni descrizione dove richiesta.

**Giorni 8-14** — Altri 3 prodotti, stessa categoria. Prime metriche (visite/preferiti).

**Giorni 15-30** — Potatura del 30% peggiore, 4 prodotti nuovi, primi aggiustamenti di
titoli e tag. Prime vendite attese: 0-3. Se zero, il problema è quasi sempre la SEO
del listing, non il prodotto.

## 9. Rischi specifici

1. **Ban per volume e bassa qualità** — Etsy vieta esplicitamente i contenuti generati
   da bot. Catalogo piccolo e curato, mai 500 listing.
2. **Cassa in ritardo** — KDP paga a 60 giorni: Etsy deve essere il primo negozio.
3. **Prodotti generici** — se non parti da una keyword con domanda vera, produci
   oggetti che nessuno cerca. La ricerca viene prima della produzione, sempre.
4. **Il racconto dell'autonomia** — se sei tu a pubblicare e rispondere, va detto:
   "4 ore a settimana di supervisione" è credibile, "zero" no.
5. **Dipendenza da una piattaforma** — un negozio chiuso azzera tutto: due marketplace
   in parallelo dal giorno 20.
6. **Crescita che sembra crescita** — un mese buono per stagionalità (Natale, Black
   Friday) non è una curva. Si giudica sul trimestre, mai sul mese singolo.
