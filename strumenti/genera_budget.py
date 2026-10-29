"""Genera il prodotto #1 (Budget Familiare Excel) senza dipendenze esterne.

Scrive un .xlsx valido utilizzando solo la standard library (zipfile + XML), più le
anteprime SVG e i testi del listing. Riproducibile: lanciarlo due volte dà lo stesso
risultato, e i test verificano la struttura del file generato.
"""

import os
import zipfile
from xml.sax.saxutils import escape as _esc

PRODOTTO = "Budget Familiare 2027"
CARTELLA = os.path.join("prodotti", "budget-familiare")

MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
ENTRATE = [("Stipendio", 2000), ("Altro reddito", 0)]
USCITE = [
    ("Casa (affitto o mutuo)", 700),
    ("Spesa alimentare", 350),
    ("Trasporti", 120),
    ("Bollette", 150),
    ("Salute", 60),
    ("Svago", 120),
    ("Altre spese", 100),
]

TITOLO_IT = (
    "Budget Familiare Excel 2027 | Gestione spese, entrate e risparmio | "
    "Foglio di calcolo mensile e annuale | Download immediato"
)

TAG_IT = [
    "budget familiare", "gestione spese", "excel budget", "foglio spese",
    "risparmio", "budget mensile", "planner finanze", "spese casa",
    "budget 2027", "excel italiano", "budget annuale", "controllo spese",
    "finanze personali",
]

TITOLO_EN = (
    "Family Budget Spreadsheet Excel 2027 | Monthly and yearly expense tracker | "
    "Income, savings rate, categories | Instant download"
)

TAG_EN = [
    "budget spreadsheet", "family budget", "expense tracker", "excel template",
    "budget planner", "savings tracker", "monthly budget", "income tracker",
    "budget 2027", "personal finance", "household budget", "money tracker",
    "excel download",
]

DESCRIZIONE = """# Budget Familiare 2027 — foglio di calcolo Excel

**Cosa è.** Un file Excel (.xlsx) per tenere entrate, uscite e risparmio di casa in un
posto solo. Dodici mesi in una schermata, categorie modificabili, totale annuale e
tasso di risparmio calcolati dalle formule.

**Cosa risolve.** Sai quanto entra e quanto esce, ma non quanto ti resta davvero.
Qui il saldo di ogni mese e il risparmio dell'anno si aggiornano da soli appena
inserisci una spesa: niente conti a mano, niente doppioni.

**Cosa contiene.**

- Foglio **Budget**: 9 categorie (2 entrate, 7 uscite), budget mensile, 12 mesi,
  totale annuo, media mensile e scostamento dal budget.
- Foglio **Riepilogo**: entrate e uscite dell'anno, risparmio, tasso di risparmio,
  media mensile e quota di ogni categoria sulle uscite totali.
- Foglio **Istruzioni**: tre righe, niente di più.

**Come si usa.** Sostituisci le categorie con le tue, scrivi il budget mensile nella
colonna C, poi inserisci le spese reali mese per mese. Tutto il resto è formula.

**Requisiti.** Excel 2016 o successivo, LibreOffice o Google Fogli. Nessuna macro,
nessun accesso a internet, nessun dato inviato da nessuna parte.

**Consegna.** Download immediato dopo l'acquisto. Il file è tuo, senza scadenza.

**Licenza.** Uso personale e familiare. Non è consentita la rivendita del file, anche
modificato.

**Nota.** Non è una consulenza finanziaria: è uno strumento di organizzazione delle spese.

---

*Contenuto realizzato con l'assistenza di strumenti di intelligenza artificiale e
verificato prima della pubblicazione: formule, categorie e istruzioni sono state
controllate a mano.*
"""


# ---------------------------------------------------------------- xlsx (stdlib)

def _col(n):
    """1 -> A, 27 -> AA."""
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _t(ref, testo, stile=0):
    return (
        f'<c r="{ref}" s="{stile}" t="inlineStr">'
        f'<is><t xml:space="preserve">{_esc(str(testo))}</t></is></c>'
    )


def _n(ref, numero, stile=2):
    return f'<c r="{ref}" s="{stile}"><v>{numero}</v></c>'


def _f(ref, formula, stile=2):
    return f'<c r="{ref}" s="{stile}"><f>{_esc(formula)}</f></c>'


def _foglio(righe, larghezze, congelata=None):
    cols = "".join(
        f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
        for i, w in enumerate(larghezze, 1)
    )
    corpo = "".join(f'<row r="{r}">{"".join(celle)}</row>' for r, celle in righe)
    pane = (
        f'<sheetViews><sheetView workbookViewId="0"><pane ySplit="{congelata}" '
        f'topLeftCell="A{congelata + 1}" activePane="bottomLeft" state="frozen"/>'
        f"</sheetView></sheetViews>"
        if congelata
        else ""
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"{pane}<cols>{cols}</cols><sheetData>{corpo}</sheetData></worksheet>"
    )


def _foglio_istruzioni():
    righe = [
        (1, [_t("A1", PRODOTTO, 5)]),
        (3, [_t("A3", "1. Apri il foglio Budget e sostituisci le categorie con le tue.", 1)]),
        (4, [_t("A4", "2. Scrivi il budget mensile nella colonna C, poi le spese reali mese per mese.", 1)]),
        (5, [_t("A5", "3. Il foglio Riepilogo calcola risparmio annuo e tasso di risparmio.", 1)]),
        (7, [_t("A7", "Nessuna macro. Nessun dato inviato. Funziona in Excel, LibreOffice e Google Fogli.", 0)]),
        (9, [_t("A9", "Licenza: uso personale e familiare. Non è consentita la rivendita del file.", 0)]),
    ]
    return _foglio(righe, [110])


def _foglio_budget():
    righe = []
    righe.append((1, [_t("A1", PRODOTTO, 5)]))
    intestazione = [_t("A3", "Categoria", 3), _t("B3", "Tipo", 3), _t("C3", "Budget mese", 3)]
    for i, mese in enumerate(MESI):
        intestazione.append(_t(f"{_col(4 + i)}3", mese, 3))
    intestazione += [_t("P3", "Totale anno", 3), _t("Q3", "Media mese", 3), _t("R3", "Delta vs budget", 3)]
    righe.append((3, intestazione))

    r = 4
    prima_entrata = r
    for nome, budget in ENTRATE:
        celle = [_t(f"A{r}", nome), _t(f"B{r}", "Entrata"), _n(f"C{r}", budget)]
        celle += [_n(f"{_col(4 + i)}{r}", 0) for i in range(12)]
        celle += [
            _f(f"P{r}", f"SUM(D{r}:O{r})"),
            _f(f"Q{r}", f'IFERROR(AVERAGE(D{r}:O{r}),0)'),
            _f(f"R{r}", f"P{r}-C{r}*12"),
        ]
        righe.append((r, celle))
        r += 1
    ultima_entrata = r - 1

    totale_entrate = r
    celle = [_t(f"A{r}", "TOTALE ENTRATE", 1), _t(f"B{r}", "", 1), _f(f"C{r}", f"SUM(C{prima_entrata}:C{ultima_entrata})", 2)]
    for i in range(12):
        lettera = _col(4 + i)
        celle.append(_f(f"{lettera}{r}", f"SUM({lettera}{prima_entrata}:{lettera}{ultima_entrata})"))
    celle += [
        _f(f"P{r}", f"SUM(D{r}:O{r})", 2),
        _f(f"Q{r}", f"P{r}/12", 2),
        _f(f"R{r}", f"P{r}-C{r}*12", 2),
    ]
    righe.append((r, celle))
    r += 1

    prima_uscita = r
    for nome, budget in USCITE:
        celle = [_t(f"A{r}", nome), _t(f"B{r}", "Uscita"), _n(f"C{r}", budget)]
        celle += [_n(f"{_col(4 + i)}{r}", 0) for i in range(12)]
        celle += [
            _f(f"P{r}", f"SUM(D{r}:O{r})"),
            _f(f"Q{r}", f'IFERROR(AVERAGE(D{r}:O{r}),0)'),
            _f(f"R{r}", f"P{r}-C{r}*12"),
        ]
        righe.append((r, celle))
        r += 1
    ultima_uscita = r - 1

    totale_uscite = r
    celle = [_t(f"A{r}", "TOTALE USCITE", 1), _t(f"B{r}", "", 1), _f(f"C{r}", f"SUM(C{prima_uscita}:C{ultima_uscita})", 2)]
    for i in range(12):
        lettera = _col(4 + i)
        celle.append(_f(f"{lettera}{r}", f"SUM({lettera}{prima_uscita}:{lettera}{ultima_uscita})"))
    celle += [
        _f(f"P{r}", f"SUM(D{r}:O{r})", 2),
        _f(f"Q{r}", f"P{r}/12", 2),
        _f(f"R{r}", f"P{r}-C{r}*12", 2),
    ]
    righe.append((r, celle))
    r += 1

    saldo = r
    celle = [_t(f"A{r}", "SALDO", 1), _t(f"B{r}", "", 1), _f(f"C{r}", f"C{totale_entrate}-C{totale_uscite}", 2)]
    for i in range(12):
        lettera = _col(4 + i)
        celle.append(_f(f"{lettera}{r}", f"{lettera}{totale_entrate}-{lettera}{totale_uscite}", 2))
    celle += [
        _f(f"P{r}", f"P{totale_entrate}-P{totale_uscite}", 2),
        _f(f"Q{r}", f"P{r}/12", 2),
        _f(f"R{r}", f"R{totale_entrate}-R{totale_uscite}", 2),
    ]
    righe.append((r, celle))

    larghezze = [26, 10, 12] + [8] * 12 + [13, 11, 15]
    return _foglio(righe, larghezze, congelata=3), saldo, totale_entrate, totale_uscite


def _foglio_riepilogo(tot_entrate, tot_uscite):
    righe = [
        (1, [_t("A1", "Riepilogo annuale", 5)]),
        (3, [_t("A3", "Entrate dell'anno", 1), _f("B3", f"Budget!P{tot_entrate}")]),
        (4, [_t("A4", "Uscite dell'anno", 1), _f("B4", f"Budget!P{tot_uscite}")]),
        (5, [_t("A5", "Risparmio dell'anno", 1), _f("B5", "B3-B4")]),
        (6, [_t("A6", "Tasso di risparmio", 1), _f("B6", "IFERROR(B5/B3,0)", 4)]),
        (7, [_t("A7", "Media entrate al mese", 1), _f("B7", "B3/12")]),
        (8, [_t("A8", "Media uscite al mese", 1), _f("B8", "B4/12")]),
        (10, [_t("A10", "Categoria", 3), _t("B10", "Totale anno", 3), _t("C10", "Media mese", 3), _t("D10", "Quota uscite", 3)]),
    ]
    prima_uscita = tot_uscite - len(USCITE) + 1
    for i, (nome, _) in enumerate(USCITE):
        r = 11 + i
        sorgente = prima_uscita + i
        righe.append(
            (
                r,
                [
                    _f(f"A{r}", f"Budget!A{sorgente}", 0),
                    _f(f"B{r}", f"Budget!P{sorgente}", 2),
                    _f(f"C{r}", f"IFERROR(B{r}/12,0)", 2),
                    _f(f"D{r}", f"IFERROR(B{r}/$B$4,0)", 4),
                ],
            )
        )
    return _foglio(righe, [30, 16, 14, 14], congelata=10)


STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="2">
<numFmt numFmtId="164" formatCode="#,##0.00\\ &quot;€&quot;"/>
<numFmt numFmtId="165" formatCode="0.0%"/>
</numFmts>
<fonts count="3">
<font><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="16"/><name val="Calibri"/></font>
</fonts>
<fills count="3">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFEDEDED"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="1"><border/></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="6">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
</cellXfs>
</styleSheet>"""


def scrivi_xlsx(percorso):
    budget, saldo, tot_entrate, tot_uscite = _foglio_budget()
    parti = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            "</Types>"
        ),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>"
        ),
        "xl/workbook.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Istruzioni" sheetId="1" r:id="rId1"/>'
            '<sheet name="Budget" sheetId="2" r:id="rId2"/>'
            '<sheet name="Riepilogo" sheetId="3" r:id="rId3"/></sheets>'
            '<calcPr calcId="0" fullCalcOnLoad="1"/></workbook>'
        ),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>'
            '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            "</Relationships>"
        ),
        "xl/styles.xml": STYLES,
        "xl/worksheets/sheet1.xml": _foglio_istruzioni(),
        "xl/worksheets/sheet2.xml": budget,
        "xl/worksheets/sheet3.xml": _foglio_riepilogo(tot_entrate, tot_uscite),
    }
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    with zipfile.ZipFile(percorso, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, contenuto in parti.items():
            z.writestr(nome, contenuto)
    return percorso


# ------------------------------------------------------------------- anteprime

def _svg(percorso, titolo, sottotitolo, righe, nota):
    corpo = "".join(
        f'<text x="80" y="{300 + i * 54}" font-family="Helvetica,Arial" font-size="26" fill="#1b1d22">{_esc(r)}</text>'
        for i, r in enumerate(righe)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900">
<rect width="1200" height="900" fill="#f7f7f4"/>
<rect x="0" y="0" width="18" height="900" fill="#1b1d22"/>
<text x="80" y="130" font-family="Helvetica,Arial" font-size="54" font-weight="bold" fill="#1b1d22">{_esc(titolo)}</text>
<text x="80" y="190" font-family="Helvetica,Arial" font-size="28" fill="#55595f">{_esc(sottotitolo)}</text>
<rect x="80" y="230" width="1040" height="1" fill="#d5d5cf"/>
{corpo}
<text x="80" y="820" font-family="Helvetica,Arial" font-size="22" fill="#55595f">{_esc(nota)}</text>
<text x="80" y="862" font-family="Helvetica,Arial" font-size="20" fill="#8b8f9a">Excel .xlsx · nessuna macro · Excel, LibreOffice, Google Fogli</text>
</svg>"""
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(svg)


def scrivi_anteprime(cartella):
    os.makedirs(cartella, exist_ok=True)
    _svg(
        os.path.join(cartella, "01-copertina.svg"),
        "Budget Familiare 2027",
        "Entrate, uscite e risparmio in un foglio solo",
        [
            "12 mesi in una schermata",
            "9 categorie modificabili",
            "Totale annuo e tasso di risparmio automatici",
        ],
        "Foglio di calcolo Excel · download immediato",
    )
    _svg(
        os.path.join(cartella, "02-cosa-contiene.svg"),
        "Cosa contiene",
        "Tre fogli, nessuna funzione da imparare",
        [
            "Budget — categorie, budget mensile, 12 mesi, totale e media",
            "Riepilogo — risparmio annuo, tasso, quota per categoria",
            "Istruzioni — tre righe",
        ],
        "Le formule sono già scritte: tu inserisci solo i numeri",
    )
    _svg(
        os.path.join(cartella, "03-come-si-usa.svg"),
        "Come si usa",
        "Tre passaggi, cinque minuti",
        [
            "1. Sostituisci le categorie con le tue",
            "2. Scrivi il budget del mese nella colonna C",
            "3. Inserisci le spese reali: i totali si aggiornano",
        ],
        "Nessun dato inviato, nessuna macro, nessun abbonamento",
    )


# --------------------------------------------------------------------- listing

def scrivi_listing(cartella):
    os.makedirs(cartella, exist_ok=True)
    with open(os.path.join(cartella, "titolo-it.txt"), "w", encoding="utf-8") as f:
        f.write(TITOLO_IT + "\n")
    with open(os.path.join(cartella, "titolo-en.txt"), "w", encoding="utf-8") as f:
        f.write(TITOLO_EN + "\n")
    with open(os.path.join(cartella, "tag-it.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(TAG_IT) + "\n")
    with open(os.path.join(cartella, "tag-en.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(TAG_EN) + "\n")
    with open(os.path.join(cartella, "descrizione.md"), "w", encoding="utf-8") as f:
        f.write(DESCRIZIONE)
    with open(os.path.join(cartella, "prezzo.txt"), "w", encoding="utf-8") as f:
        f.write(
            "Prezzo consigliato: 14,90 €\n\n"
            "Perché: i listing italiani comparabili stanno a 12,08 € con poche recensioni;\n"
            "quelli in inglese tra 13,99 e 25 $. 14,90 € sta sopra il cluster italiano\n"
            "senza uscire dal mercato, e lascia margine per un future bundle.\n"
        )


def costruisci(destinazione=CARTELLA):
    xlsx = os.path.join(destinazione, "Budget_Familiare_2027.xlsx")
    scrivi_xlsx(xlsx)
    scrivi_anteprime(os.path.join(destinazione, "anteprime"))
    scrivi_listing(os.path.join(destinazione, "listing"))
    return xlsx


if __name__ == "__main__":
    percorso = costruisci()
    print(f"prodotto generato: {percorso}")
