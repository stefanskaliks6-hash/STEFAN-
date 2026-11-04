"""Build Group7_Data_Calculator.xlsx from data/group7_submissions.json.
Type each member's numbers into the 'Submissions' sheet; the 'Summary' sheet's
Average / Minimum / Maximum update automatically (blank cells are ignored)."""
import json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

here = pathlib.Path(__file__).parent
data = json.loads((here / "data/group7_submissions.json").read_text(encoding="utf-8"))

COLS = [("Member", None, 26), ("Address", "address", 34), ("Lot Size (m²)", "lot_m2", 14),
        ("Lot Value ($)", "lot_value", 16), ("Building ($)", "building_value", 16),
        ("Property Total ($)", "property_total", 18), ("GFA (m²)", "gfa_m2", 13),
        ("Previous Assessment ($)", "previous_assessment", 22), ("Floors", "floors", 9),
        ("Year built", "year_built", 11), ("FAR (GFA ÷ lot)", None, 15), ("Change vs previous", None, 18)]
NAVY, ROW = "003399", "E6E7F0"
hdr_font, hdr_fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor=NAVY)
thin = Side(style="thin", color="BFBFBF"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
money, area = '"$"#,##0', '#,##0'

wb = Workbook()
ws = wb.active; ws.title = "Submissions"
for c, (label, _, width) in enumerate(COLS, 1):
    cell = ws.cell(row=1, column=c, value=label)
    cell.font, cell.fill, cell.border = hdr_font, hdr_fill, box
    cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.column_dimensions[cell.column_letter].width = width
ws.row_dimensions[1].height = 32
n = len(data["members"])
for r, m in enumerate(data["members"], 2):
    sub = data["submissions"].get(m["last"], {})
    ws.cell(row=r, column=1, value=f'{m["first"]} {m["last"]}').font = Font(bold=True)
    for c, (_, key, _) in enumerate(COLS, 1):
        if key: ws.cell(row=r, column=c, value=sub.get(key))
    ws.cell(row=r, column=11, value=f'=IF(AND(ISNUMBER(G{r}),ISNUMBER(C{r}),C{r}>0),G{r}/C{r},"")')
    ws.cell(row=r, column=12, value=f'=IF(AND(ISNUMBER(F{r}),ISNUMBER(H{r}),H{r}>0),F{r}/H{r}-1,"")')
    for c in range(1, len(COLS) + 1):
        cell = ws.cell(row=r, column=c); cell.border = box
        if r % 2: cell.fill = PatternFill("solid", fgColor=ROW)
        cell.number_format = {3: area, 7: area, 4: money, 5: money, 6: money, 8: money, 11: "0.00", 12: "+0.0%;-0.0%"}.get(c, "General")
ws.freeze_panes = "C2"
last = n + 1
note = ws.cell(row=last + 2, column=1, value="Type numbers only (no $ or commas). Property Total should equal Lot Value + Building. "
               "Source: Ville de Montréal rôle d'évaluation foncière.")
note.font = Font(italic=True, color="595959")

sm = wb.create_sheet("Summary")
sm["A1"] = "Group 7 – Office Mid-Rise – Summary table"; sm["A1"].font = Font(bold=True, size=14)
for c, h in enumerate(["", "Average", "Minimum", "Maximum", "# entries"], 1):
    cell = sm.cell(row=3, column=c, value=h); cell.font, cell.fill, cell.border = hdr_font, hdr_fill, box
rows = [("Lot Size (m²)", "C", area), ("Lot Value ($)", "D", money), ("Building ($)", "E", money),
        ("Property Total ($)", "F", money), ("GFA (m²)", "G", area), ("Previous Assessment ($)", "H", money)]
for i, (label, col, nf) in enumerate(rows, 4):
    rng = f"Submissions!{col}2:{col}{last}"
    sm.cell(row=i, column=1, value=label).font = Font(bold=True)
    sm.cell(row=i, column=2, value=f'=IFERROR(AVERAGE({rng}),"—")')
    sm.cell(row=i, column=3, value=f'=IF(COUNT({rng})=0,"—",MIN({rng}))')
    sm.cell(row=i, column=4, value=f'=IF(COUNT({rng})=0,"—",MAX({rng}))')
    sm.cell(row=i, column=5, value=f'=COUNT({rng})')
    for c in range(1, 6):
        cell = sm.cell(row=i, column=c); cell.border = box
        if c in (2, 3, 4): cell.number_format = nf
        if i % 2 == 0: cell.fill = PatternFill("solid", fgColor=ROW)
for col, w in zip("ABCDE", (26, 18, 18, 18, 11)): sm.column_dimensions[col].width = w
sm["A11"] = "Copy these values into slide 2 of the deck (or re-run build_deck.js after filling data/group7_submissions.json)."
sm["A11"].font = Font(italic=True, color="595959")

out = here / "Group7_Data_Calculator.xlsx"; wb.save(out); print("wrote", out)
