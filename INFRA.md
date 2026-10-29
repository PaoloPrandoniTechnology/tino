# Dove vive Tino

L'agente non è un programma che gira su un computer: è **un processo che si sveglia,
legge dei file, lavora, scrive dei file e si addormenta**. Quindi "dove risiede" ha
quattro risposte separate, e solo una riguarda un server.

| Componente | Dove sta | Costo |
|---|---|---|
| **Cervello** (modello) | API remota (Anthropic/OpenAI). Nessun modello gira da te | ~1 € per esecuzione |
| **Casa** (codice + stato) | repository Git | 0 € |
| **Motore** (chi lo sveglia) | scheduler del repository (GitHub Actions) | 0 € |
| **Prodotti** (file vendibili) | bucket privato (Cloudflare R2) o repo privato di archiviazione | 0 € |
| **Vetrina** (dashboard) | hosting statico che legge `data.json` | 0 € |
| **Denaro** | Etsy / KDP / Adobe → conto dell'entità | commissioni di piattaforma |

Totale infrastruttura: **0 €/mese**. L'unica spesa variabile è l'API, ~16 €/mese al
ritmo di 4 esecuzioni a settimana.

## 1. Il cervello non risiede: si affitta

Ogni esecuzione è una chiamata API con il charter di [AGENTE-FABBRICA.md](AGENTE-FABBRICA.md)
e i file di stato come contesto. Non c'è memoria del modello tra un'esecuzione e
l'altra: la memoria sono i file. È deliberato — un agente con lo stato dentro il
modello è impossibile da ispezionare, e questo progetto vive di ispezione.

## 2. La casa: un repository Git

```
tino/                        (pubblico)
  agente/                    codice del loop, prompt, script
  state/
    keyword.json
    catalogo.json
    metriche.json
    budget.json
    giornale/2026-11-03.md
  dashboard/                 index.html + data.json (sito statico)
  .github/workflows/run.yml  cron + passi
```

Tre proprietà che un server non ti dà:

- **Storia immutabile**: il ledger è append-only perché la storia di Git è append-only.
  Riscrivere un movimento richiede un force-push, visibile a chiunque.
- **Auditabilità**: ogni esecuzione lascia un commit con data, diff e log. "I numeri
  sono veri" diventa verificabile invece che dichiarato.
- **Costo zero e zero manutenzione**: niente aggiornamenti di sistema, certificati o
  backup — il repo *è* il backup.

## 3. Il motore: GitHub Actions

Un workflow con `schedule` (4 cron a settimana, es. mar-mer-gio-ven alle 07:00) che:

1. fa checkout del repo;
2. installa le dipendenze;
3. esegue l'agente con la chiave API presa da un **Secret**;
4. committa stato, giornale e `data.json`;
5. carica i file prodotti come artifact e li copia sul bucket privato.

Limiti reali, da conoscere prima:

| Limite | Valore | Conseguenza |
|---|---|---|
| Durata massima di un job | 6 ore | irrilevante: le run durano 15-30 min |
| Cron su **repo privato** | richiede un piano a pagamento (GitHub Pro, ~4 $/mese) | per questo il repo del codice è pubblico |
| Cron su **repo pubblico** | gratuito, ma **disattivato dopo 60 giorni di inattività** | si risolve da sé: ogni run fa un commit |
| Puntualità del cron | può ritardare di minuti, a volte di più | nessun problema: non è un servizio in tempo reale |
| Log | pubblici se il repo è pubblico | mai stampare chiavi, mai dati dei clienti nei log |

**Il trucco che rende il sistema onesto**: l'approvazione umana è una **pull request**.
L'agente apre una PR con i file da pubblicare e il report; tu la leggi e fai merge.
Approvare = un click, tracciato, con data e nome. Chiunque può controllare in seguito
quante PR hai approvato senza guardare.

## 4. I prodotti non stanno nel repo pubblico

Un file vendibile in un repo pubblico è un file gratis. Quindi i prodotti finiti vanno
su un **bucket privato** (Cloudflare R2, 10 GB gratuiti, nessun costo di uscita) o in
un secondo repo privato usato solo come magazzino — senza cron, quindi senza piano a
pagamento. Da lì li scarichi tu e li carichi su Etsy: la pubblicazione è comunque un
atto del titolare, ed è anche il momento in cui dai l'occhiata di qualità.

## 5. La vetrina

La dashboard è un sito statico: legge `data.json` committato dall'agente. Va su
qualsiasi hosting statico (Cloudflare Pages, Sites, Netlify) collegato al repo. Zero
codice server, zero database, zero costi. Il giorno in cui servirà qualcosa di dinamico
(login, area riservata) si aggiunge un Worker, non un server.

## 6. La configurazione, e perché è questa

Repo pubblico, cron di GitHub Actions, dashboard statica, prodotti su archivio privato.
Costo: **0 €/mese**. È la configurazione in uso, non un'opzione fra tre.

- **Codice pubblico perché è il prodotto**: la promessa "i numeri sono veri" vale
  quanto la possibilità di verificarla. Un repo privato la trasformerebbe in una
  dichiarazione, e le dichiarazioni non si controllano.
- **Prodotti fuori dal repo**: un file vendibile in un repo pubblico è un file gratis.
- **Nessun server**: un VPS aggiungerebbe 4-5 €/mese, aggiornamenti, certificati e un
  punto di rottura, senza risolvere nessuno dei problemi attuali.

Si cambia solo quando servirà ciò che un cron non sa fare: rispondere in pochi minuti,
leggere dati che nessuna API espone, o job oltre le sei ore. A quel punto si aggiunge
un Worker, non si sposta tutto.

## 7. Il limite che nessuna infrastruttura risolve

Etsy **non espone i volumi di ricerca** e non consente lo scraping. Quindi la ricerca
delle keyword non è automatizzabile in modo affidabile: l'agente prepara la griglia di
valutazione, tu (o una persona) incolli i dati della prima pagina di risultati una
volta a settimana, l'agente filtra e decide. Sono 10 minuti di lavoro umano, e vanno
messi nel conto della supervisione — non nella colonna "automatico".

Chi promette un agente che "trova da solo i prodotti vincenti" sta vendendo uno scraper
che viola i termini di servizio della piattaforma, e chiude il negozio.

## 8. Stato del setup

**Fatto**: repo pubblico `PaoloPrandoniTechnology/tino`; workflow con quattro cron e
`workflow_dispatch`; verifica del ledger prima e dopo ogni esecuzione; commit
automatico di stato e dashboard; catena di hash sul ledger; dashboard statica che legge
`data.json`.

**Da fare**: archivio privato per i file vendibili, hosting statico per la dashboard,
Secret `ANTHROPIC_API_KEY` (opzionale: senza chiave il loop gira e produce report,
solo senza le due frasi di commento del modello).

**Controllo che vale la pena fare una volta**: provare a modificare un movimento del
ledger e verificare che il commit venga rifiutato. Se passa, la trasparenza è un
adesivo.
