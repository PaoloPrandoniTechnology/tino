# La distribuzione: come il progetto trova visite

Il catalogo senza traffico è inventario. Questo documento dice dove il traffico arriva,
cosa si può automatizzare per via ufficiale e cosa no.

## 1. Il vincolo, prima delle idee

Tre livelli di automazione, da tenere separati perché hanno regole diverse:

| Livello | Cosa si automatizza | Serve un umano? |
|---|---|---|
| **Creazione del prodotto** | file, anteprime, testi del listing | no |
| **Pubblicazione su marketplace** | bozza, immagini, file digitale, attivazione | una volta sola: autorizzazione dell'app e apertura del negozio |
| **Contenuti social** | scrittura, montaggio, caricamento | dipende dalla piattaforma (sotto) |

Cosa **non** è delegabile, in nessun caso: apertura degli account, KYC, dati fiscali,
accettazione dei termini, titolarità del conto. Non è un limite tecnico, è giuridico.

### Cosa dicono le API, a ottobre 2026

| Piattaforma | Pubblicazione via API | Requisiti reali |
|---|---|---|
| **Etsy** | sì: `createDraftListing`, `uploadListingImage`, `uploadListingFile`, poi attivazione | app "seller" per il proprio negozio, OAuth con `listings_w`, autorizzazione del titolare una volta |
| **Instagram** | sì: container + `media_publish`, anche Reels | account Business o Creator, app Meta; per i propri account basta l'accesso standard |
| **YouTube** | sì: upload diretto, anche Shorts | OAuth con scope di upload, quota giornaliera ampia |
| **TikTok** | solo con conferma esplicita del creatore prima dell'invio | l'invio non confermato è escluso dalle linee guida; senza audit del client il video resta privato |

Conseguenza operativa: **un solo tocco umano al giorno** su TikTok (pubblicare ciò che
l'agente ha già caricato nella casella), zero tocchi su Etsy, Instagram e YouTube dopo
l'autorizzazione iniziale. La scelta è fra un tocco e nessun TikTok: il canale più veloce
a far crescere un pubblico è anche l'unico che richiede una persona.

## 2. Lo scopo che fa guardare

Non "un'AI che guadagna". Quello lo dicono tutti e nessuno ci crede più. Lo scopo è un
altro, ed è l'unica cosa che questo progetto ha e gli altri no:

> **Un agente con 100 € deve coprire i propri costi in 100 giorni. Ogni euro è
> verificabile: il ledger è pubblico, con catena di hash, e il codice pure.**

Tre elementi che tengono insieme l'attenzione:

1. **Una posta in gioco con una data.** Giorno 100, copertura o resoconto del fallimento.
   Senza scadenza non c'è tensione, e senza tensione non c'è ritorno.
2. **Un personaggio senza faccia.** L'agente non parla di sé: mostra i conti. Il
   protagonista è il ledger, e il conflitto sono le decisioni (cosa potare, cosa tenere).
3. **La prova, subito.** Chi arriva può aprire il repository e controllare. È l'unica
   differenza difendibile rispetto a cento account che raccontano guadagni.

La frase da usare ovunque, e da non tradire mai: *"Non chiedermi di credermi: controlla."*

## 3. I tre formati (e nient'altro)

| Formato | Durata | Cosa contiene | Cadenza |
|---|---|---|---|
| **Il conto di oggi** | 15-25 s | tre numeri veri, una decisione presa | 3 volte a settimana |
| **Perché ho potato** | 30-45 s | il prodotto ucciso, il motivo, cosa cambia | 1 volta a settimana |
| **Cosa non ha funzionato** | 40-60 s | l'errore della settimana, senza morale | 1 volta a settimana |

Regola: **nessun contenuto senza un numero dentro.** Se un video non ha una cifra presa
dal ledger, non si pubblica. È il filtro che impedisce di scivolare nel contenuto
motivazionale, che è dove questi progetti muoiono.

Cosa non fare: b-roll generico, voce robotica che legge frasi generiche, "5 modi per",
teaser senza dati. Instagram penalizza esplicitamente i contenuti non originali o
superficialmente modificati, e TikTok esclude dal feed il materiale riutilizzato senza
aggiunta. Il vantaggio di questo progetto è che il materiale è **originale per
costruzione**: screenshot del ledger, grafici della dashboard, decisioni reali.

## 4. Il funnel, con i numeri

```
video → profilo → dashboard pubblica → iscrizione → prodotto
```

| Passaggio | Cosa si misura | Ordine di grandezza atteso |
|---|---|---|
| Video → visualizzazioni | retention a 3 secondi | decide tutto il resto |
| Visualizzazioni → visite alla dashboard | click sul link | ~0,5-2% |
| Dashboard → iscritti | form | 10-25% di chi arriva sul sito |
| Iscritti → acquirenti | conversion del lancio | 1-3% |

Con 40 video in tre mesi l'aspettativa onesta è **qualche centinaio o qualche migliaio
di follower**, non un numero garantito: la crescita dipende dalla ripetibilità del
formato, e nessun benchmark pubblico prevede i casi nuovi. Un video che sfonda può
spostare tutto, ma non è un piano.

## 5. Come il progetto diventa sostenibile

Cinque livelli, in ordine di margine per unità di sforzo. I primi tre sono automatici,
gli ultimi due richiedono tempo e credibilità.

| Livello | Cosa | Margine | Quando ha senso |
|---|---|---|---|
| **1. Catalogo su marketplace** | 40-130 listing su Etsy, KDP, Adobe | ~85% dopo commissioni | dal mese 1, rende dal mese 3-6 |
| **2. Negozio proprio** | gli stessi file, senza commissioni di piattaforma | ~95% | dal mese 4, quando c'è traffico da portare |
| **3. Affiliazione** | strumenti usati davvero (voce, video, hosting, storefront) | 10-50% ricorrente | dal mese 3, con 20-50k visualizzazioni al mese |
| **4. Contenuti sponsorizzati** | un marchio coerente, mai un prodotto che l'agente non userebbe | tariffa per post | da 10k follower, parte bassa dei listini |
| **5. Il sistema** | il metodo completo, con i conti di 100 giorni come prova | alta per unità | dal mese 6, solo dopo aver dimostrato la curva |

Il livello 1 è l'unico che non dipende dal pubblico: per questo esiste dal primo giorno.
Il livello 5 è quello che rende di più, ma **vendere il metodo prima di averlo
dimostrato è la scorciatoia che distrugge tutto**: chi compra verifica.

## 6. Cosa si pubblica e cosa no

Già regolato in [REGOLAMENTO.md](REGOLAMENTO.md) §7. Qui la parte specifica dei canali:

- **Sì**: numeri del ledger, decisioni con il motivo, prodotti potati e perché, codice,
  errori, costi dell'agente, tasso di copertura.
- **No**: dati personali e fiscali, credenziali, dati dei clienti, file vendibili,
  screenshot di messaggi privati, entità legale e coordinate bancarie.
- **Sempre**: etichetta di contenuto generato con AI dove la piattaforma la richiede
  (TikTok e Meta la chiedono per audio, video o immagini realistiche), e disclosure AI
  su ogni listing.
- **Mai**: un numero che non sia nel ledger. Un video che dichiara un incasso inesistente
  chiude il progetto più velocemente di cento giorni a zero.

## 7. Il primo mese di canali, in pratica

| Settimana | Cosa pubblica | Cosa costruisce |
|---|---|---|
| 1 | 3 video "il conto", presentazione del vincolo | account aperti, bio con link alla dashboard |
| 2 | 3 video + 1 "perché ho potato" | primo prodotto proprio in vendita |
| 3 | 3 video + 1 "cosa non ha funzionato" | modulo iscrizione, primo contenuto gratuito |
| 4 | 3 video + 1 "perché ho potato" | lettura dei numeri: quale formato trattiene |

Se dopo quattro settimane la retention a tre secondi è sotto il 30%, il problema è il
primo secondo dei video, non il progetto: si cambia l'apertura, non la strategia.
