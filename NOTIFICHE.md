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

## Telegram — 3 minuti, gratis

1. Apri Telegram, cerca **@BotFather**, scrivi `/newbot`, scegli un nome. Ottieni un
   token che sembra `123456:ABC-DEF...`.
2. Apri la chat del bot appena creato e mandagli un messaggio qualsiasi ("ciao"). Un
   bot non può iniziare una conversazione: senza questo passo non può scriverti.
3. Visita `https://api.telegram.org/bot<TOKEN>/getUpdates` e copia il valore
   `message.chat.id`.
4. Su GitHub: Settings → Secrets and variables → Actions → due secret nuovi:
   `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`.
5. Prova: azioni → workflow **tino** → *Run workflow*. Il passo "Notifica al titolare"
   deve dire `telegram: ok`.

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
  bruciato, anche se lo cancelli dopo.
- **La notifica non è la dashboard.** La dashboard è la fonte pubblica e verificabile;
  il messaggio è un promemoria privato. Se i due divergono, ha ragione la dashboard.
- **Se l'invio fallisce, l'esecuzione non fallisce.** Il lavoro è già committato: il
  passo di notifica è `continue-on-error`, e l'errore resta visibile nei log di Actions.
- **Nessun dato di cliente nel messaggio.** Solo aggregati del ledger.

## Verificare senza inviare

```bash
python3 -m agente.notifica --dry-run
# → stampa il messaggio e i canali configurati
```
