# Sfida: un agente che si mantiene da solo e cresce

Replica strutturata del format "agente AI che deve mantenersi da solo", con due vincoli
precisi: **l'umano fa solo supervisione** e il traguardo non è un numero in euro, ma
una **curva**: prima l'autocopertura, poi la crescita mese su mese.

## Il traguardo, in una riga

L'agente non deve "guadagnare 100.000 €": deve smettere di pesare e cominciare a
crescere. Autocopertura entro il giorno 100, sostenuta tre mesi, con ricavo mensile in
aumento di almeno il 50% a ogni stagione. Dettaglio in [REGOLAMENTO.md](REGOLAMENTO.md).

## Due modalità, una scelta obbligatoria

| | **Fabbrica** (autonoma) | **Servizi** (dipende da te) |
|---|---|---|
| Come vende | marketplace con domanda propria | telefono, demo, fiducia |
| Lavoro umano | 4-6 h/settimana, poi 2-3 h/mese | 20 contatti al giorno |
| Prima entrata | 30-60 giorni | 5-10 giorni |
| A 100 giorni | 0-1.500 €, copertura possibile | 7.000-10.000 € |
| A 12 mesi | 500-1.500 €/mese ricorrenti | limitato dalle tue ore |
| Compatibile con "solo supervisione" | **sì** | no |

L'autonomia è lenta, la velocità richiede vendita umana. Solo la colonna di sinistra
rispetta il requisito, e solo la colonna di sinistra produce una curva che si alza da
sola.

## Cosa c'è qui

| File | Cos'è |
|---|---|
| [SISTEMA.md](SISTEMA.md) | Architettura: principio, piattaforme verificate, equazione della crescita, reinvestimento, kill rules. |
| [AGENTE-FABBRICA.md](AGENTE-FABBRICA.md) | Loop settimanale, stato, prompt pronto, filtro di qualità umano. |
| [OPERATIVO.md](OPERATIVO.md) | Come opera Tino nel concreto: calendario, sette passi di produzione, soglie, potatura, denaro, eccezioni. |
| [PRODOTTI.md](PRODOTTI.md) | Cosa produrrà: quattro famiglie, sei schede del primo mese, esclusioni, test di validità. |
| [INFRA.md](INFRA.md) | Dove vive: repository, cron, stato, segreti, costi e limiti reali. |
| [REGOLAMENTO.md](REGOLAMENTO.md) | Le regole pubbliche: capitale, curva, contabilità, reinvestimento. |
| [PIANO.md](PIANO.md) | La variante "servizi", se un giorno accetti di lavorare. |
| [AGENTE.md](AGENTE.md) | Charter dell'agente nella variante servizi. |
| `dashboard/` | Copertura, crescita, catalogo, movimenti, giornale. |

## La sintesi in cinque righe

Non si automatizza lo scambio, si affitta la distribuzione: si vende dove i compratori
esistono già (Etsy, Amazon KDP, Adobe Stock) e si escludono le piattaforme che vietano
l'automazione (Fiverr, Upwork) o l'AI (Shutterstock, Envato). L'agente produce, misura
e pota; l'umano approva e firma. Break-even: ~143 €/mese lordi sul costo di riferimento
di 108 €/mese (la spesa reale in avvio è ~16 €/mese). Poi ogni listing in più
è rendita: il ricavo è catalogo × visite × conversione × prezzo, e il catalogo si accumula.

## Avviare la dashboard

```bash
python3 -m http.server 3000 -d dashboard
# → http://localhost:3000
```
