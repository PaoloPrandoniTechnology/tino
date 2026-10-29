# Come Tino ti manda un messaggio

Dopo ogni esecuzione l'agente può mandarti il conto del giorno sul telefono. Il
messaggio è corto, sempre uguale nella forma, e contiene solo numeri presi dal ledger:

```
Giorno 3 — 2026-11-04
Ricavo del mese: 14,90 € · copertura 14%
Crescita mese su mese: n/d
Cassa: 84,10 € · autonomia 157 giorni
Catalogo: 1 prodotti · 2 listing attivi
```

Due canali. Il codice è lo stesso: cambiano solo le variabili d'ambiente.

## Telegram — una volta configurato, va da sé

Il bot è **@TinoMessagebot** (`t.me/TinoMessagebot`). Funziona in due direzioni: manda il
conto del giorno dopo ogni esecuzione e risponde quando gli scrivi.

1. Apri la chat del bot e scrivigli un messaggio: `/start`. Un bot non può iniziare una
   conversazione, quindi questo passo non è aggirabile — è l'unico tocco tuo.
2. Su GitHub: Settings → Secrets and variables → Actions → un solo secret,
   `TELEGRAM_BOT_TOKEN`. Il token te lo dà **@BotFather** con `/newbot` (o `/token` se il
   bot esiste già).
3. Da quel momento il workflow **telegram** controlla i messaggi ogni 15 minuti, impara
   il tuo chat id dal primo messaggio e lo salva in `state/telegram.json`. Il digest
   delle esecuzioni parte da solo, senza copiare id a mano.
4. Prova: azioni → workflow **tino** → *Run workflow*. Il passo "Notifica al titolare"
   deve dire `telegram: ok`.

Se preferisci non far imparare l'id, si può fissare il secret `TELEGRAM_CHAT_ID`: ha la
precedenza sul valore salvato nel repository.

### I comandi

| Messaggio | Risposta |
|---|---|
| `/stato` (o `/start`) | il conto del giorno: ricavo, copertura, cassa, catalogo |
| `/cassa` | incassato, speso, spesa dell'agente, giorni di autonomia |
| `/catalogo` | prodotti con prezzo, stato e piattaforma |
| `/giornale` | l'ultima pagina del giornale, per intero |
| `/aiuto` | l'elenco dei comandi |

Qualsiasi altro testo riceve l'elenco dei comandi. Le risposte sono composte dai numeri
del ledger, senza passare dal modello: un bot che inventa una cifra in privato fa danni
che non si vedono sulla dashboard.

Due regole di sicurezza, entrambe nel codice:

- **un solo proprietario**: il primo chat che scrive diventa il padrone del bot, gli
altri vengono ignorati (nessun bot pubblico che risponde a chi trova il nome);
- **offset salvato**: `state/telegram.json` ricorda l'ultimo messaggio consumato, così
due esecuzioni ravvicinate non rispondono due volte.

Costo: zero. Limite: Telegram consegna in un secondo o due, e il messaggio può
contenere tutto il report.

## WhatsApp — 40 minuti, a pagamento, per via ufficiale

WhatsApp **non** permette a un terzo di collegarsi al tuo account: l'unico modo legale
è la Business Cloud API di Meta. Tre cose che vanno sapute prima di iniziare:

- serve **un numero dedicato** che non sia già registrato su WhatsApp (un numero
  virtuale da 2-3 €/mese va bene; il tuo numero personale no);
- i messaggi che partono senza che tu abbia scritto prima devono usare un
  **template approvato** (approvazione: fino a 24 ore);
- si paga **per messaggio consegnato**: un template *utility* verso un numero
  italiano costa **0,0248 €**. Quattro esecuzioni a settimana fanno circa 0,40 €/mese.

Passi:

1. **developers.facebook.com** → *My Apps* → *Create app* → caso d'uso
   **WhatsApp** → collega un *business portfolio*.
2. Nella sezione *WhatsApp → API Setup*: aggiungi il numero dedicato, verificalo via
   SMS, annota il **Phone Number ID** (non il numero di telefono: l'ID).
3. **Il template.** *WhatsApp → Template → Create template*. Categoria **Utility**,
   lingua **Italiano**, nome **tino_giornata**, corpo esatto:

   ```
   Tino, giorno {{1}}. Ricavo del mese {{2}} euro, copertura {{3}} per cento, cassa {{4}} euro.
   ```

   Quattro parametri, nell'ordine in cui l'agente li manda. Attendi l'approvazione.
4. **Token permanente.** *Business Settings → Users → System users* → nuovo utente di
   sistema → assegna l'app e l'account WhatsApp → genera token con
   `whatsapp_business_messaging` e `whatsapp_business_management`. È l'unico token che
   non scade: quello mostrato in *API Setup* dura 24 ore.
5. Collega un metodo di pagamento all'account WhatsApp Business, altrimenti in
   produzione l'invio viene rifiutato.
6. Su GitHub, tre secret: `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `WHATSAPP_TO`
   (il tuo numero personale, con prefisso, senza `+`: `393331234567`). Il quarto,
   `WHATSAPP_TEMPLATE`, serve solo se chiami il template diversamente.
7. Prova con *Run workflow*: il passo deve dire `whatsapp: ok`.

## Regole

- **Un segreto non entra mai nel repository.** Token e numeri stanno nei secret di
  GitHub o in un `.env` locale ignorato: un token in un repo pubblico è un token
  bruciato, anche se lo cancelli dopo. Un token incollato in una chat, in un ticket o
  in un messaggio va considerato esposto: si revoca con `/revoke` su @BotFather, che ne
  emette uno nuovo, e si aggiorna il secret. Costa trenta secondi.
- **La notifica non è la dashboard.** La dashboard è la fonte pubblica e verificabile;
  il messaggio è un promemoria privato. Se i due divergono, ha ragione la dashboard.
- **Se l'invio fallisce, l'esecuzione non fallisce.** Il lavoro è già committato: il
  passo di notifica è `continue-on-error`, e l'errore resta visibile nei log di Actions.
- **Nessun dato di cliente nel messaggio.** Solo aggregati del ledger.

## Verificare senza inviare

```bash
python3 -m agente.notifica --dry-run   # stampa il digest e i canali configurati
python3 -m agente.telegram --dry-run    # legge i messaggi e mostra le risposte
```
