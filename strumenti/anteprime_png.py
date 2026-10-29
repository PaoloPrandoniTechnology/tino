"""Anteprime PNG per Etsy, 2000x1500, con l'aspetto del foglio Excel.

Richiede Pillow (strumento di produzione, non fa parte dell'agente: il runtime
resta senza dipendenze). I numeri sono coerenti con il workbook generato da
`strumenti/genera_budget.py`.
"""

import os

import matplotlib
from PIL import Image, ImageDraw, ImageFont

L, A = 2000, 1500
MARGINE = 120
CARTA = "#F7F7F4"
INCHIOSTRO = "#1B1D22"
GRIGIO = "#55595F"
TENUE = "#8B8F9A"
BORDO = "#D5D5CF"
EVIDENZA = "#EDEDEA"

CARTELLA = os.path.join("prodotti", "budget-familiare", "anteprime")

ENTRATE = [("Stipendio", 2000, [2000, 2000, 2000, 2000, 2000, 2000]),
           ("Altro reddito", 0, [0, 150, 0, 0, 300, 0])]
USCITE = [
    ("Casa (affitto o mutuo)", 700, [700, 700, 700, 700, 700, 700]),
    ("Spesa alimentare", 350, [342, 368, 355, 391, 377, 349]),
    ("Trasporti", 120, [118, 122, 120, 135, 120, 118]),
    ("Bollette", 150, [168, 154, 149, 172, 210, 158]),
    ("Salute", 60, [0, 60, 0, 45, 0, 60]),
    ("Svago", 120, [95, 140, 110, 88, 132, 120]),
    ("Altre spese", 100, [112, 98, 105, 130, 95, 118]),
]


def _font(dimensione, grassetto=False):
    nome = "DejaVuSans-Bold.ttf" if grassetto else "DejaVuSans.ttf"
    percorso = os.path.join(matplotlib.get_data_path(), "fonts", "ttf", nome)
    return ImageFont.truetype(percorso, dimensione)


def _eur(valore):
    testo = f"{valore:,.0f}".replace(",", ".")
    return f"{testo} €"


def _tela():
    img = Image.new("RGB", (L, A), CARTA)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 16, A], fill=INCHIOSTRO)
    return img, d


def _titolo(d, testo, sottotitolo=None, y=110, dim=76):
    d.text((MARGINE, y), testo, font=_font(dim, True), fill=INCHIOSTRO)
    if sottotitolo:
        d.text((MARGINE, y + dim + 24), sottotitolo, font=_font(34), fill=GRIGIO)
    d.line([MARGINE, y + dim + (100 if sottotitolo else 50), L - MARGINE, y + dim + (100 if sottotitolo else 50)], fill=BORDO, width=2)


def _tabella(d, x, y, larghezze, righe, allineamenti, altezza=62, evidenzia=()):
    f_header = _font(28, True)
    f_cella = _font(28)
    f_bold = _font(28, True)
    for indice, riga in enumerate(righe):
        cx = x
        for colonna, (testo, larghezza) in enumerate(zip(riga, larghezze)):
            riempimento = EVIDENZA if (indice == 0 or indice in evidenzia) else CARTA
            d.rectangle([cx, y, cx + larghezza, y + altezza], fill=riempimento, outline=BORDO, width=1)
            f = f_header if indice == 0 else (f_bold if indice in evidenzia else f_cella)
            allineamento = allineamenti[colonna]
            if allineamento == "r":
                box = d.textbbox((0, 0), testo, font=f)
                tx = cx + larghezza - 18 - (box[2] - box[0])
            elif allineamento == "c":
                box = d.textbbox((0, 0), testo, font=f)
                tx = cx + (larghezza - (box[2] - box[0])) / 2
            else:
                tx = cx + 18
            d.text((tx, y + (altezza - 34) / 2), testo, font=f, fill=INCHIOSTRO)
            cx += larghezza
        y += altezza
    return y


def _righe_budget():
    mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu"]
    righe = [["Categoria", "Tipo", "Budget"] + mesi + ["Totale"]]
    totale_entrate_mesi = [0] * 6
    totale_uscite_mesi = [0] * 6
    totale_entrate = 0
    totale_uscite = 0

    for nome, budget, valori in ENTRATE:
        righe.append([nome, "Entrata", _eur(budget)] + [_eur(v) for v in valori] + [_eur(sum(valori))])
        totale_entrate_mesi = [a + b for a, b in zip(totale_entrate_mesi, valori)]
        totale_entrate += sum(valori)
    righe.append(["TOTALE ENTRATE", "", _eur(sum(b for _, b, _ in ENTRATE))]
                 + [_eur(v) for v in totale_entrate_mesi] + [_eur(totale_entrate)])
    indice_totale_entrate = len(righe) - 1

    for nome, budget, valori in USCITE:
        righe.append([nome, "Uscita", _eur(budget)] + [_eur(v) for v in valori] + [_eur(sum(valori))])
        totale_uscite_mesi = [a + b for a, b in zip(totale_uscite_mesi, valori)]
        totale_uscite += sum(valori)
    righe.append(["TOTALE USCITE", "", _eur(sum(b for _, b, _ in USCITE))]
                 + [_eur(v) for v in totale_uscite_mesi] + [_eur(totale_uscite)])
    indice_totale_uscite = len(righe) - 1

    saldo = [1_150 if False else a - b for a, b in zip(totale_entrate_mesi, totale_uscite_mesi)]
    righe.append(["SALDO", "", ""] + [_eur(v) for v in saldo] + [_eur(totale_entrate - totale_uscite)])
    indice_saldo = len(righe) - 1

    return righe, (indice_totale_entrate, indice_totale_uscite, indice_saldo)


def copertina():
    img, d = _tela()
    d.text((MARGINE, 210), "Budget Familiare", font=_font(110, True), fill=INCHIOSTRO)
    d.text((MARGINE, 340), "2027", font=_font(110, True), fill=INCHIOSTRO)
    d.text((MARGINE, 520), "Entrate, uscite e risparmio in un foglio solo.",
           font=_font(42), fill=GRIGIO)
    righe = [
        "12 mesi in una schermata",
        "9 categorie modificabili",
        "Totale annuo e tasso di risparmio automatici",
    ]
    y = 650
    for r in righe:
        d.ellipse([MARGINE, y + 12, MARGINE + 16, y + 28], fill=INCHIOSTRO)
        d.text((MARGINE + 40, y), r, font=_font(40), fill=INCHIOSTRO)
        y += 76
    d.rectangle([MARGINE, 1130, L - MARGINE, 1134], fill=BORDO)
    d.text((MARGINE, 1180), "Foglio di calcolo Excel · download immediato", font=_font(34), fill=GRIGIO)
    d.text((MARGINE, 1300), "Excel 2016+  ·  LibreOffice  ·  Google Fogli", font=_font(28), fill=TENUE)
    img.save(os.path.join(CARTELLA, "01-copertina.png"), optimize=True)


def cosa_contiene():
    img, d = _tela()
    _titolo(d, "Cosa contiene", "Tre fogli, nessuna funzione da imparare")
    schede = [
        ("Budget", "9 categorie, budget mensile,\n12 mesi, totale e media"),
        ("Riepilogo", "Risparmio annuo, tasso di\nrisparmio, quota per categoria"),
        ("Istruzioni", "Tre righe. Il resto\nsono formule già scritte"),
    ]
    larghezza = (L - 2 * MARGINE - 80) // 3
    for i, (titolo, corpo) in enumerate(schede):
        x = MARGINE + i * (larghezza + 40)
        d.rounded_rectangle([x, 480, x + larghezza, 980], radius=18, fill=EVIDENZA)
        d.text((x + 40, 540), f"0{i + 1}", font=_font(64, True), fill=TENUE)
        d.text((x + 40, 640), titolo, font=_font(46, True), fill=INCHIOSTRO)
        d.multiline_text((x + 40, 730), corpo, font=_font(32), fill=GRIGIO, spacing=14)
    d.text((MARGINE, 1100), "Tu inserisci i numeri. I totali si calcolano da soli.",
           font=_font(38), fill=INCHIOSTRO)
    d.text((MARGINE, 1300), "Nessuna macro · nessun dato inviato · nessun abbonamento",
           font=_font(28), fill=TENUE)
    img.save(os.path.join(CARTELLA, "02-cosa-contiene.png"), optimize=True)


def foglio_budget():
    img, d = _tela()
    _titolo(d, "Foglio Budget", "12 mesi, 9 categorie, totali automatici", dim=64)
    righe, evidenzia = _righe_budget()
    larghezze = [500, 150, 190] + [160] * 6 + [210]
    _tabella(d, MARGINE, 360, larghezze, righe, ["l", "l", "r", "r", "r", "r", "r", "r", "r", "r"], evidenzia=evidenzia)
    d.text((MARGINE, 1360), "Valori di esempio: le formule lavorano sui tuoi numeri.",
           font=_font(28), fill=TENUE)
    img.save(os.path.join(CARTELLA, "03-foglio-budget.png"), optimize=True)


def riepilogo():
    img, d = _tela()
    _titolo(d, "Foglio Riepilogo", "Quanto resta davvero, a fine anno", dim=64)
    entrate = sum(sum(v) for _, _, v in ENTRATE)
    uscite = sum(sum(v) for _, _, v in USCITE)
    risparmio = entrate - uscite
    tasso = risparmio / entrate if entrate else 0
    kpi = [
        ("Entrate anno", _eur(entrate)),
        ("Uscite anno", _eur(uscite)),
        ("Risparmio", _eur(risparmio)),
        ("Tasso di risparmio", f"{tasso * 100:.1f}%".replace(".", ",")),
        ("Media risparmio/mese", _eur(risparmio / 12)),
    ]
    larghezza = (L - 2 * MARGINE - 4 * 24) // 5
    for i, (etichetta, valore) in enumerate(kpi):
        x = MARGINE + i * (larghezza + 24)
        d.rounded_rectangle([x, 400, x + larghezza, 620], radius=16, fill=EVIDENZA)
        d.text((x + 26, 430), etichetta, font=_font(26), fill=GRIGIO)
        d.text((x + 26, 500), valore, font=_font(44, True), fill=INCHIOSTRO)

    righe = [["Categoria", "Totale anno", "Media mese", "Quota uscite"]]
    for nome, _, valori in USCITE:
        totale = sum(valori)
        righe.append([
            nome,
            _eur(totale),
            _eur(totale / 6),
            f"{totale / uscite * 100:.1f}%".replace(".", ","),
        ])
    _tabella(d, MARGINE, 720, [700, 330, 330, 330], righe, ["l", "r", "r", "r"], altezza=66)
    d.text((MARGINE, 1300), "Quote e medie calcolate sulle uscite reali, non sul budget.",
           font=_font(28), fill=TENUE)
    img.save(os.path.join(CARTELLA, "04-riepilogo.png"), optimize=True)


def come_si_usa():
    img, d = _tela()
    _titolo(d, "Come si usa", "Tre passaggi, cinque minuti")
    passi = [
        ("1", "Sostituisci le categorie", "Le nove voci sono un esempio: metti le tue spese vere."),
        ("2", "Scrivi il budget del mese", "Una colonna sola, la C. È il tuo obiettivo di spesa."),
        ("3", "Inserisci le spese reali", "Mese per mese. Totali, medie e saldo si aggiornano."),
    ]
    y = 470
    for numero, titolo, corpo in passi:
        d.ellipse([MARGINE, y, MARGINE + 90, y + 90], fill=INCHIOSTRO)
        box = d.textbbox((0, 0), numero, font=_font(46, True))
        d.text((MARGINE + 45 - (box[2] - box[0]) / 2, y + 18), numero, font=_font(46, True), fill=CARTA)
        d.text((MARGINE + 130, y + 4), titolo, font=_font(44, True), fill=INCHIOSTRO)
        d.text((MARGINE + 130, y + 62), corpo, font=_font(32), fill=GRIGIO)
        y += 230
    d.rectangle([MARGINE, 1210, L - MARGINE, 1214], fill=BORDO)
    d.text((MARGINE, 1250), "Funziona in Excel, LibreOffice e Google Fogli. Nessuna installazione.",
           font=_font(30), fill=GRIGIO)
    img.save(os.path.join(CARTELLA, "05-come-si-usa.png"), optimize=True)


def costruisci():
    os.makedirs(CARTELLA, exist_ok=True)
    copertina()
    cosa_contiene()
    foglio_budget()
    riepilogo()
    come_si_usa()
    return CARTELLA


if __name__ == "__main__":
    cartella = costruisci()
    for nome in sorted(os.listdir(cartella)):
        if nome.endswith(".png"):
            percorso = os.path.join(cartella, nome)
            print(f"{nome}: {os.path.getsize(percorso) // 1024} KB")
