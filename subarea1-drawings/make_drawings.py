"""Subarea 1 (pair 1 & 2) lab drawings, generated as true-scale SVG sheets.

Sheets are 11 x 17 in (431.8 x 279.4 mm) landscape. All drawings are 1:200,
so 1 m = 5 mm on paper. Print at 100% / "actual size" to keep the scale.
"""
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 431.8, 279.4          # sheet size, mm
S = 5.0                      # 1:200 -> 5 mm per metre
FF = 3.0                     # floor-to-floor height, m
FONT = "Helvetica, Arial, sans-serif"

# ---------------------------------------------------------------- the two buildings
LOT_W, LOT_D, SETBACK = 10.0, 20.0, 4.0
B1 = dict(key="T1", name="TASK 1 — NO ELEVATOR (4 FLOORS, MAX AREA)",
          short="BUILDING 1 · NO ELEVATOR", depth=14.0, floors=4, top=None,
          height=12.0, gfa=560, far="2.8", cov="70%", yard=2.0,
          floors_txt="4 × 140 m²", foot_txt="10 m × 14 m = 140 m²",
          why=["Without an elevator the building is limited to 4 floors.",
               "4 floors × 140 m² (max floor plate) = 560 m².",
               "Any smaller footprint would lose floor area, so",
               "70% coverage is as low as it can go."])
B2 = dict(key="T2", name="TASK 2 — LARGE BACKYARD (60% COVERAGE, MAX AREA)",
          short="BUILDING 2 · LARGE BACKYARD", depth=12.0, floors=8, top=4.0,
          height=27.0, gfa=1000, far="5.0", cov="60%", yard=4.0,
          floors_txt="8 × 120 m² + 1 × 40 m²", foot_txt="10 m × 12 m = 120 m²",
          why=["60% of 200 m² = 120 m² footprint (10 × 12 m).",
               "8 floors × 120 m² = 960 m²; 9 full floors = 1,080 m²",
               "would break the 1,000 m² (FAR 5.0) cap.",
               "A 40 m² 9th floor (10 × 4 m) makes exactly 1,000 m².",
               "Fallback if partial floors are not allowed:",
               "8 × 120 m² = 960 m², FAR 4.8, height 24 m."])


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Sheet:
    def __init__(self):
        self.el = []

    def add(self, s):
        self.el.append(s)

    def line(self, x1, y1, x2, y2, w=0.25, dash=None, color="#000", cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                 f'stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}"{d}/>')

    def poly(self, pts, fill="none", w=0.25, stroke="#000", dash=None, close=True):
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="{w}" stroke-linejoin="round"{d}/>')

    def rect(self, x, y, w, h, fill="none", sw=0.25, stroke="#000", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, cx, cy, r, fill="none", w=0.25, stroke="#000"):
        self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{w}"/>')

    def text(self, x, y, s, size=3.0, anchor="start", weight="normal", rot=0,
             fill="#000", italic=False):
        t = f' transform="rotate({rot:.2f} {x:.2f} {y:.2f})"' if rot else ""
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{t}>'
                 f'{esc(s)}</text>')

    def svg(self):
        defs = """<defs>
<pattern id="hatch" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="1.6" stroke="#000" stroke-width="0.12"/></pattern>
<pattern id="hatch2" patternUnits="userSpaceOnUse" width="0.9" height="0.9" patternTransform="rotate(-45)">
<line x1="0" y1="0" x2="0" y2="0.9" stroke="#000" stroke-width="0.12"/></pattern>
<pattern id="earth" patternUnits="userSpaceOnUse" width="2.4" height="2.4" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="2.4" stroke="#000" stroke-width="0.15"/>
<line x1="1.2" y1="0" x2="1.2" y2="1.0" stroke="#000" stroke-width="0.15"/></pattern>
<marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
<path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
</defs>"""
        body = "\n".join(self.el)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
                f'viewBox="0 0 {W} {H}">\n{defs}\n<rect width="{W}" height="{H}" fill="#fff"/>\n'
                f'{body}\n</svg>')


# ---------------------------------------------------------------- shared sheet furniture
def frame(sh, title, drawing, sheet_no, scale="1:200"):
    sh.rect(10, 10, W - 20, H - 20, sw=0.7)
    # title block (bottom right)
    x0, y0, bw, bh = W - 10 - 112, H - 10 - 62, 112, 62
    sh.rect(x0, y0, bw, bh, sw=0.5)
    rows = [(y0 + 14, None)]
    sh.text(x0 + 3, y0 + 6, "DESIGN LAB — LOT MASSING", 3.2, weight="bold")
    sh.text(x0 + 3, y0 + 11.5, drawing, 3.0)
    for yy in (14, 22, 30, 38, 46, 54):
        sh.line(x0, y0 + yy, x0 + bw, y0 + yy, 0.25)
    sh.line(x0 + 56, y0 + 22, x0 + 56, y0 + 62, 0.25)
    f = [(x0 + 3, y0 + 19.5, "NAME:", "________________________________________"),
         (x0 + 3, y0 + 27.5, "DATE:", "Nov 16, 2026"),
         (x0 + 59, y0 + 27.5, "SUBAREA:", "1  (pair 1 & 2)"),
         (x0 + 3, y0 + 35.5, "COURSE:", "______________"),
         (x0 + 59, y0 + 35.5, "LAB SECTION:", "________"),
         (x0 + 3, y0 + 43.5, "SCALE:", scale),
         (x0 + 59, y0 + 43.5, "SHEET:", f"{sheet_no} / 4"),
         (x0 + 3, y0 + 51.5, "PAPER:", "11 × 17 in"),
         (x0 + 59, y0 + 51.5, "PRINT:", "100% / actual size")]
    for xx, yy, k, v in f:
        sh.text(xx, yy, k, 2.3, weight="bold")
        sh.text(xx + (13 if k != "LAB SECTION:" and k != "SUBAREA:" else 21), yy, v, 2.6)
    sh.text(x0 + 3, y0 + 59.5, "Lot 10 m × 20 m = 200 m² · front setback 4 m · 3 m floor-to-floor", 2.2)
    # drawing title (top left)
    sh.text(20, 24, title, 6, weight="bold")


def north_arrow(sh, cx, cy, ang_deg=-90, r=7, label="N"):
    """ang_deg = screen direction of north (SVG angles, -90 = up)."""
    a = math.radians(ang_deg)
    tip = (cx + r * math.cos(a), cy + r * math.sin(a))
    tail = (cx - r * math.cos(a), cy - r * math.sin(a))
    left = (cx + 0.45 * r * math.cos(a + 2.3), cy + 0.45 * r * math.sin(a + 2.3))
    right = (cx + 0.45 * r * math.cos(a - 2.3), cy + 0.45 * r * math.sin(a - 2.3))
    sh.circle(cx, cy, r + 1.5, w=0.3)
    sh.poly([tip, left, (cx, cy), right], fill="#000", w=0.2)
    sh.poly([tip, left, (cx, cy)], fill="#fff", w=0.25)
    sh.line(cx, cy, *tail, 0.3)
    lx, ly = cx + (r + 4.5) * math.cos(a), cy + (r + 4.5) * math.sin(a) + 1.4
    sh.text(lx, ly, label, 4, anchor="middle", weight="bold")


def scale_bar(sh, x, y):
    """Graphic scale for 1:200 (0-20 m)."""
    for i, (a, b) in enumerate([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 15)]):
        fill = "#000" if i % 2 == 0 else "#fff"
        sh.rect(x + a * S, y, (b - a) * S, 2, fill=fill, sw=0.2)
    for m in (0, 5, 10, 15):
        sh.text(x + m * S, y + 6, f"{m}", 2.5, anchor="middle")
    sh.text(x + 15 * S + 3, y + 2, "m", 2.5)
    sh.text(x, y - 2.5, "SCALE 1:200  (1 m = 5 mm)", 2.5, weight="bold")


def dim_h(sh, x1, x2, y, label, ext_from=None, size=2.6, tick=1.2):
    """Horizontal dimension line with architectural ticks."""
    sh.line(x1 - 1.5, y, x2 + 1.5, y, 0.18)
    for x in (x1, x2):
        sh.line(x - tick * 0.7, y + tick * 0.7, x + tick * 0.7, y - tick * 0.7, 0.4)
        if ext_from is not None:
            sh.line(x, ext_from, x, y + (1.5 if y > ext_from else -1.5), 0.13)
    sh.text((x1 + x2) / 2, y - 1.0, label, size, anchor="middle")


def dim_v(sh, x, y1, y2, label, ext_from=None, size=2.6, tick=1.2, side=-1):
    sh.line(x, y1 - 1.5, x, y2 + 1.5, 0.18)
    for y in (y1, y2):
        sh.line(x - tick * 0.7, y + tick * 0.7, x + tick * 0.7, y - tick * 0.7, 0.4)
        if ext_from is not None:
            sh.line(ext_from, y, x + (1.5 if x > ext_from else -1.5), y, 0.13)
    tx = x - 1.2 if side < 0 else x + 1.2 + size * 0.75
    sh.text(tx, (y1 + y2) / 2, label, size, anchor="middle", rot=-90 if side < 0 else 90)


# ---------------------------------------------------------------- axonometric sheets
def axon_sheet(b, sheet_no, lot_name):
    sh = Sheet()
    frame(sh, f"AXONOMETRIC — {b['name']}", f"Axonometric · {b['short'].title()} · {lot_name}",
          sheet_no)
    ox, oy = 150.0, 238.0
    ex = (0.5, -math.sqrt(3) / 2)        # plan x (lot width) on screen, true length
    ey = (-math.sqrt(3) / 2, -0.5)       # plan y (depth from street) on screen, true length

    def P(x, y, z=0.0):
        return (ox + S * (x * ex[0] + y * ey[0]), oy + S * (x * ex[1] + y * ey[1] - z))

    # sidewalk + curb (context)
    sh.poly([P(0, -2.5), P(LOT_W, -2.5), P(LOT_W, 0), P(0, 0)], fill="#f2f2f2", w=0.18)
    sh.text(*P(5.6, -1.25), "SIDEWALK", 2.2, anchor="middle", rot=-60)
    # lot
    sh.poly([P(0, 0), P(LOT_W, 0), P(LOT_W, LOT_D), P(0, LOT_D)], fill="#fff", w=0.35)
    # setback line
    sh.line(*P(-0.8, SETBACK), *P(LOT_W + 0.8, SETBACK), 0.25, dash="2,1,0.4,1")
    # ground texture in front setback + backyard (light dots of grass)
    y_back = SETBACK + b["depth"]
    for yy in [i * 0.8 + 0.4 for i in range(int(LOT_D / 0.8))]:
        if SETBACK < yy < y_back:
            continue
        for xx in [j * 1.0 + 0.5 for j in range(10)]:
            px, py = P(xx + (0.4 if int(yy / 0.8) % 2 else 0), yy)
            sh.line(px, py, px + 0.5, py - 0.3, 0.12, color="#555")

    # buildings
    def box(x0, x1, y0, y1, z0, z1, levels):
        left = [P(x0, y0, z0), P(x0, y1, z0), P(x0, y1, z1), P(x0, y0, z1)]
        front = [P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)]
        top = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
        sh.poly(left, fill="#c9c9c9", w=0.45)
        sh.poly(front, fill="#ffffff", w=0.45)
        sh.poly(top, fill="#ececec", w=0.45)
        for z in levels:
            if z0 < z < z1:
                sh.line(*P(x0, y0, z), *P(x0, y1, z), 0.18)
                sh.line(*P(x0, y0, z), *P(x1, y0, z), 0.18)

    levels = [FF * i for i in range(1, 10)]
    zf = b["floors"] * FF
    box(0, LOT_W, SETBACK, y_back, 0, zf, levels)
    if b["top"]:
        box(0, LOT_W, SETBACK, SETBACK + b["top"], zf, zf + FF, levels)

    # floor numbers on the street facade
    for i in range(b["floors"]):
        px, py = P(LOT_W * 0.5, SETBACK, i * FF + 1.2)
        sh.text(px, py, f"FLOOR {i + 1} · {LOT_W * b['depth']:.0f} m²", 2.0, anchor="middle",
                rot=-60)
    if b["top"]:
        px, py = P(LOT_W * 0.5, SETBACK, zf + 1.2)
        sh.text(px, py, "FLOOR 9 · 40 m²", 2.0, anchor="middle", rot=-60)

    # --- dimensions in the ground plane along the left side (x = -2.5)
    def gdim(xa, ya, xb, yb, off, label, ang):
        # dimension line offset along -x (screen: -ex)
        a = P(xa - off, ya)
        c = P(xb - off, yb)
        sh.line(*a, *c, 0.18)
        for (px, py), (gx, gy) in ((a, P(xa, ya)), (c, P(xb, yb))):
            sh.line(gx - ex[0] * 0.6 * S, gy - ex[1] * 0.6 * S, px - ex[0] * 0.4 * S,
                    py - ex[1] * 0.4 * S, 0.12)
            sh.line(px - 0.9, py - 0.4, px + 0.9, py + 0.4, 0.4)
        mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
        sh.text(mx - ex[0] * 1.6, my - ex[1] * 1.6, label, 2.6, anchor="middle", rot=ang)

    gdim(0, 0, 0, SETBACK, 2.0, "4 m setback", 30)
    gdim(0, SETBACK, 0, y_back, 2.0, f"{b['depth']:.0f} m", 30)
    gdim(0, y_back, 0, LOT_D, 2.0, f"{b['yard']:.0f} m yard", 30)
    gdim(0, 0, 0, LOT_D, 5.0, "lot depth 20 m", 30)

    # width along the street (in front of the sidewalk, y = -4.5)
    a, c = P(0, -4.5), P(LOT_W, -4.5)
    sh.line(*a, *c, 0.18)
    for (px, py), xx in ((a, 0), (c, LOT_W)):
        g = P(xx, -2.5)
        sh.line(g[0] - ey[0] * 0.4 * S, g[1] - ey[1] * 0.4 * S, px - ey[0] * 0.4 * S,
                py - ey[1] * 0.4 * S, 0.12)
        sh.line(px - 0.4, py - 0.9, px + 0.4, py + 0.9, 0.4)
    m = P(LOT_W / 2, -5.6)
    sh.text(m[0], m[1], "10 m (full lot width)", 2.6, anchor="middle", rot=-60)

    # height dimension to the right of the street facade (x = 12)
    zt = b["height"]
    base = P(LOT_W + 2.2, SETBACK, 0)
    topp = P(LOT_W + 2.2, SETBACK, zt)
    sh.line(base[0], base[1] + 1.5, topp[0], topp[1] - 1.5, 0.18)
    for z in [0] + [FF * i for i in range(1, int(zt / FF) + 1)]:
        px, py = P(LOT_W + 2.2, SETBACK, z)
        g = P(LOT_W + 0.4, SETBACK, z)
        sh.line(g[0], g[1], px + 1.2, py - 0.6, 0.12)
        sh.line(px - 0.9, py + 0.9, px + 0.9, py - 0.9, 0.35 if z in (0, zt) else 0.2)
    mx = base[0] + 2.0
    sh.text(mx + 4.0, (base[1] + topp[1]) / 2, f"H = {zt:.0f} m", 3.2, anchor="middle",
            rot=90, weight="bold")
    sh.text(mx + 8.5, (base[1] + topp[1]) / 2,
            f"({int(zt / FF)} × 3 m floor-to-floor)", 2.4, anchor="middle", rot=90)

    # labels with leaders
    def leader(pt, tx, ty, s, anchor="start"):
        sh.line(pt[0], pt[1], tx, ty, 0.15)
        sh.circle(pt[0], pt[1], 0.45, fill="#000", w=0.1)
        sh.text(tx + (1 if anchor == "start" else -1), ty + 1, s, 2.6, anchor=anchor)

    leader(P(LOT_W * 0.6, SETBACK * 0.5), 205, 262, "FRONT SETBACK (4 m) — street side")
    leader(P(0.8, y_back + b["yard"] / 2), 60, 120 if b["floors"] > 4 else 150,
           f"BACKYARD {b['yard']:.0f} m deep ({LOT_W * b['yard']:.0f} m²)", anchor="end")
    rp = P(LOT_W * 0.55, (SETBACK + y_back) / 2 + (2 if b["top"] else 0), zf)
    leader(rp, 205, 52 if b["top"] else 150, f"ROOF · footprint {b['foot_txt']}")
    if b["top"]:
        leader(P(LOT_W * 0.5, SETBACK + 2, zf + FF), 84, 58,
               "PARTIAL 9th FLOOR 10 m × 4 m = 40 m²", anchor="end")
        sh.text(83, 62.5, "(flush with the street facade)", 2.6, anchor="end")

    north_arrow(sh, 40, 240, ang_deg=math.degrees(math.atan2(ex[1], ex[0])) if lot_name.startswith("LOT A")
                else math.degrees(math.atan2(-ex[1], -ex[0])))
    sh.text(40, 258, "north, in the ground plane", 2.2, anchor="middle")
    scale_bar(sh, W - 150, 180)
    sh.text(20, 31, f"{lot_name} · 1:200 plan-oblique axonometric (plan rotated 30°/60°, "
                    "all horizontal and vertical dimensions true length)", 2.8)

    # ---- chart
    cx0, cy0 = W - 10 - 140, 40
    rows = [("Lot", "10 m × 20 m = 200 m²"),
            ("Floors × floor area", b["floors_txt"]),
            ("Footprint", b["foot_txt"]),
            ("Lot coverage", f"{b['cov']}  ({LOT_W * b['depth']:.0f} ÷ 200)"),
            ("Building height", f"{b['height']:.0f} m  ({int(b['height'] / FF)} × 3 m)"),
            ("Gross floor area (GFA)", f"{b['gfa']:,} m²"),
            ("Floor area ratio (FAR)", f"{b['far']}  ({b['gfa']:,} ÷ 200)"),
            ("Front setback", "4 m"),
            ("Backyard depth", f"{b['yard']:.0f} m  (20 − 4 − {b['depth']:.0f})")]
    sh.text(cx0, cy0 - 3, "CHART", 4, weight="bold")
    rh = 7.5
    sh.rect(cx0, cy0, 130, rh * len(rows), sw=0.45)
    for i, (k, v) in enumerate(rows):
        y = cy0 + i * rh
        if i:
            sh.line(cx0, y, cx0 + 130, y, 0.2)
        sh.text(cx0 + 2, y + 5, k, 2.7, weight="bold")
        sh.text(cx0 + 52, y + 5, v, 2.9)
    sh.line(cx0 + 50, cy0, cx0 + 50, cy0 + rh * len(rows), 0.2)
    ry = cy0 + rh * len(rows) + 9
    sh.text(cx0, ry, "HOW IT WAS FOUND", 3.2, weight="bold")
    for i, s in enumerate(b["why"]):
        sh.text(cx0, ry + 6 + i * 4.6, s, 2.7)
    return sh


# ---------------------------------------------------------------- plan
X_A_BACK, X_A_FRONT = 0.0, 20.0
X_SW1, X_CURB1, X_CURB2, X_SW2 = 20.0, 22.5, 32.5, 35.0
X_B_FRONT, X_B_BACK = 35.0, 55.0
A_BLD = (X_A_FRONT - SETBACK - B1["depth"], X_A_FRONT - SETBACK)      # 2 .. 16
B_BLD = (X_B_FRONT + SETBACK, X_B_FRONT + SETBACK + B2["depth"])      # 39 .. 51
B_TOP = (X_B_FRONT + SETBACK, X_B_FRONT + SETBACK + B2["top"])        # 39 .. 43


def chain_marks():
    return [X_A_BACK, A_BLD[0], A_BLD[1], X_A_FRONT, X_CURB1, X_CURB2, X_SW2, B_BLD[0],
            B_BLD[1], X_B_BACK]


def chain_labels():
    return ["2", "14", "4", "2.5", "10", "2.5", "4", "12", "4"]


def tree_plan(sh, cx, cy, r):
    sh.circle(cx, cy, r, w=0.3)
    n = 10
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r * (0.82 if i % 2 else 0.95)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    sh.poly(pts, w=0.12)
    sh.circle(cx, cy, 0.5, fill="#000", w=0.1)


def person_plan(sh, cx, cy):
    sh.add(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="1.4" ry="0.75" fill="#fff" stroke="#000" '
           f'stroke-width="0.2"/>')
    sh.circle(cx, cy, 0.55, fill="#000", w=0.1)


def plan_sheet():
    sh = Sheet()
    frame(sh, "SITE PLAN — TWO LOTS FACING ACROSS THE STREET", "Site plan · Lots A & B", 3)
    px0, py0 = 34.0, 172.0                       # screen position of X=0, Y=0 (plan metres)

    def T(X, Y):
        return (px0 + X * S, py0 - Y * S)

    ymin, ymax = -11.0, 21.0
    # road surface + sidewalks
    sh.rect(*T(X_CURB1, ymax), (X_CURB2 - X_CURB1) * S, (ymax - ymin) * S, fill="#efefef", sw=0)
    for X in (X_CURB1, X_CURB2):
        sh.line(*T(X, ymin), *T(X, ymax), 0.4)
    for X in (X_SW1, X_SW2):
        sh.line(*T(X, ymin), *T(X, ymax), 0.3)
    sh.line(*T(27.5, ymin), *T(27.5, ymax), 0.25, dash="4,2.5")
    # sidewalk joints
    for X0, X1 in ((X_SW1, X_CURB1), (X_CURB2, X_SW2)):
        y = ymin
        while y <= ymax:
            sh.line(*T(X0, y), *T(X1, y), 0.1, color="#666")
            y += 1.5
    sh.text(*T(27.5 - 1.0, 15.0), "ROAD  10 m", 3.0, anchor="middle", rot=-90, weight="bold")
    sh.text(*T(21.25 + 0.4, 13.0), "SIDEWALK 2.5 m", 2.2, anchor="middle", rot=-90)
    sh.text(*T(33.75 + 0.4, 13.0), "SIDEWALK 2.5 m", 2.2, anchor="middle", rot=-90)
    # arrows of traffic
    for X, d in ((25, -1), (30, 1)):
        a, c = T(X, 4 - d * 3), T(X, 4 + d * 3)
        sh.add(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{c[0]:.2f}" y2="{c[1]:.2f}" '
               f'stroke="#888" stroke-width="0.3" marker-end="url(#arr)"/>')

    # neighbouring lots (dashed property lines)
    for X0, X1 in ((X_A_BACK, X_A_FRONT), (X_B_FRONT, X_B_BACK)):
        for Y in (-10, 20):
            sh.line(*T(X0, Y), *T(X1, Y), 0.2, dash="3,1,0.5,1")
        sh.line(*T(X0, ymin), *T(X0, ymax), 0.2, dash="3,1,0.5,1")
        sh.text(*T((X0 + X1) / 2, -5), "neighbouring lot", 2.4, anchor="middle",
                fill="#666", italic=True)
        sh.text(*T((X0 + X1) / 2, 15), "neighbouring lot", 2.4, anchor="middle",
                fill="#666", italic=True)
    # subject lots
    for X0, X1 in ((X_A_BACK, X_A_FRONT), (X_B_FRONT, X_B_BACK)):
        a = T(X0, 10)
        sh.rect(a[0], a[1], (X1 - X0) * S, 10 * S, sw=0.6)
    # setback lines
    for X in (X_A_FRONT - SETBACK, X_B_FRONT + SETBACK):
        sh.line(*T(X, -1.0), *T(X, 11.0), 0.25, dash="2,1,0.4,1")

    # section cut line A-A at Y = 5
    yc = 5.0
    a, c = T(-3.0, yc), T(58.8, yc)
    sh.line(a[0], a[1], c[0], c[1], 0.35, dash="7,1.5,1.2,1.5")
    for X, anchor in ((-3.6, "end"), (59.4, "start")):
        cx, cy = T(X, yc)
        sh.circle(cx, cy, 3.4, w=0.4)
        sh.text(cx, cy + 1.3, "A", 3.6, anchor="middle", weight="bold")
        # arrow showing viewing direction (looking north)
        sh.poly([(cx - 2.6, cy - 3.0), (cx + 2.6, cy - 3.0), (cx, cy - 7.0)], fill="#000", w=0.1)

    # buildings (roof plans)
    a = T(A_BLD[0], 10)
    sh.rect(a[0], a[1], (A_BLD[1] - A_BLD[0]) * S, 10 * S, fill="url(#hatch)", sw=0.8)
    a = T(B_BLD[0], 10)
    sh.rect(a[0], a[1], (B_BLD[1] - B_BLD[0]) * S, 10 * S, fill="url(#hatch)", sw=0.8)
    a = T(B_TOP[0], 10)
    sh.rect(a[0], a[1], (B_TOP[1] - B_TOP[0]) * S, 10 * S, fill="url(#hatch2)", sw=0.8)
    for X, Y, lines in (((A_BLD[0] + A_BLD[1]) / 2, 5.0,
                         ["BUILDING 1 — NO ELEVATOR", "4 floors · H 12 m", "10 × 14 m · 70%",
                          "GFA 560 m² · FAR 2.8"]),
                        ((B_TOP[1] + B_BLD[1]) / 2, 5.0,
                         ["BUILDING 2", "LARGE BACKYARD", "8 fl. + partial 9th", "H 27 m",
                          "10 × 12 m · 60%", "GFA 1,000 m²", "FAR 5.0"])):
        cx, cy = T(X, Y)
        h = len(lines) * 3.6
        sh.rect(cx - 19 if X < 30 else cx - 13.5, cy - h / 2 - 2.6, 38 if X < 30 else 27, h + 1.8,
                fill="#fff", sw=0.2)
        for i, s in enumerate(lines):
            sh.text(cx, cy - h / 2 + 1.0 + i * 3.6, s, 2.5 if i else 2.6, anchor="middle",
                    weight="bold" if i == 0 else "normal")
    cx, cy = T((B_TOP[0] + B_TOP[1]) / 2, 8.0)
    sh.rect(cx - 8.5, cy - 2.6, 17, 7.4, fill="#fff", sw=0.2)
    sh.text(cx, cy, "9th floor", 2.3, anchor="middle", weight="bold")
    sh.text(cx, cy + 3.3, "10 × 4 m", 2.3, anchor="middle")

    # lot labels
    for X, s in ((10, "LOT A · 10 × 20 m = 200 m²"), (45, "LOT B · 10 × 20 m = 200 m²")):
        sh.text(*T(X, 11.2), s, 2.7, anchor="middle", weight="bold")
    sh.text(*T(1.0, -1.2), "rear lot line", 2.0, fill="#444")
    sh.text(*T(54.0, -1.2), "rear lot line", 2.0, fill="#444", anchor="end")
    sh.text(*T(X_A_FRONT - SETBACK + 0.5, -2.2), "setback line", 2.0, fill="#444")
    sh.text(*T(X_B_FRONT + SETBACK - 0.5, -2.2), "setback line", 2.0, fill="#444", anchor="end")
    sh.text(*T(53.0, 0.6), "backyard 4 m", 2.0, anchor="middle")

    # trees + people (for scale)
    for X, Y, r in ((21.25, 18.0, 2.2), (21.25, -4.0, 2.2), (33.75, 8.0, 2.2),
                    (33.75, -8.0, 2.2), (53.0, 7.5, 1.8)):
        tree_plan(sh, *T(X, Y), r * S)
    for X, Y in ((1.0, 7.5), (1.0, 3.0)):          # shrubs in the 2 m yard
        tree_plan(sh, *T(X, Y), 0.85 * S)
    for X, Y in ((21.0, 6.5), (21.6, 1.0), (34.0, 2.5), (18.0, 3.0), (37.0, 7.0),
                 (52.5, 3.0), (53.6, 2.2)):
        person_plan(sh, *T(X, Y))

    # dimension chains
    yd1, yd2 = T(0, -13.5)[1], T(0, -16.5)[1]
    marks = chain_marks()
    for i, lab in enumerate(chain_labels()):
        x1, x2 = T(marks[i], 0)[0], T(marks[i + 1], 0)[0]
        dim_h(sh, x1, x2, yd1, lab + (" m" if i in (0,) else ""), size=2.4)
    for m in marks:
        x = T(m, 0)[0]
        sh.line(x, T(0, -0.5)[1] if m not in (X_CURB1, X_CURB2) else T(0, ymin)[1] + 1,
                x, yd1 + 1.5, 0.12, dash="0.8,0.8")
    dim_h(sh, T(0, 0)[0], T(20, 0)[0], yd2, "LOT A 20 m", size=2.4)
    dim_h(sh, T(20, 0)[0], T(35, 0)[0], yd2, "STREET R.O.W. 15 m", size=2.4)
    dim_h(sh, T(35, 0)[0], T(55, 0)[0], yd2, "LOT B 20 m", size=2.4)
    dim_h(sh, T(0, 0)[0], T(55, 0)[0], yd2 + 7, "55 m overall  (27.5 cm at 1:200)", size=2.6)
    dim_v(sh, T(-1.6, 0)[0], T(0, 10)[1], T(0, 0)[1], "10 m", size=2.4)
    dim_v(sh, T(56.4, 0)[0], T(0, 10)[1], T(0, 0)[1], "10 m", size=2.4, side=1)

    north_arrow(sh, 352, 60)
    scale_bar(sh, 335, 92)
    notes = ["LEGEND",
             "▨  roof of building (plan view)",
             "▩  roof of partial 9th floor",
             "– · –  front setback line (4 m)",
             "– – –  neighbouring property lines",
             "○  trees · ⬭ people (for scale)",
             "Ⓐ  section cut A–A, arrows look north",
             "",
             "Section A–A is cut through the",
             "middle of both lots and the street."]
    for i, s in enumerate(notes):
        sh.text(335, 112 + i * 5, s, 2.6, weight="bold" if i == 0 else "normal")
    return sh


# ---------------------------------------------------------------- section
def tree_elev(sh, T, X, h, r):
    bx, by = T(X, 0)
    cx, cy = T(X, h - r)
    sh.line(bx, by, cx, cy + r * S * 0.3, 0.5)
    sh.line(cx, cy + r * S * 0.5, cx - r * S * 0.4, cy, 0.25)
    sh.line(cx, cy + r * S * 0.4, cx + r * S * 0.45, cy - r * S * 0.1, 0.25)
    pts = []
    n = 16
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r * S * (0.88 if i % 2 else 1.0)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.95))
    sh.poly(pts, w=0.25)


def person_elev(sh, T, X, flip=False, h=1.75):
    def p(dx, z):
        return T(X + (-dx if flip else dx), z)
    hx, hy = p(0, h - 0.12)
    sh.circle(hx, hy, 0.12 * S, fill="#000", w=0.1)
    body = [p(-0.22, h - 0.28), p(0.22, h - 0.28), p(0.18, 0.85), p(-0.18, 0.85)]
    sh.poly(body, fill="#fff", w=0.25)
    sh.line(*p(-0.1, 0.85), *p(-0.14, 0), 0.45)
    sh.line(*p(0.1, 0.85), *p(0.16, 0), 0.45)


def section_sheet():
    sh = Sheet()
    frame(sh, "SECTION A–A — THROUGH BOTH LOTS AND THE STREET", "Section A–A · Lots A & B", 4)
    px0, gy = 30.0, 196.0

    def T(X, z):
        return (px0 + X * S, gy - z * S)

    road_z = -0.15
    # earth poché
    sh.poly([T(-3, 0), T(X_CURB1, 0), T(X_CURB1, road_z), T(X_CURB2, road_z), T(X_CURB2, 0),
             T(55.6, 0), T(55.6, -2.2), T(-3, -2.2)], fill="url(#earth)", w=0)
    sh.poly([T(-3, 0), T(X_CURB1, 0), T(X_CURB1, road_z), T(X_CURB2, road_z), T(X_CURB2, 0),
             T(55.6, 0)], close=False, w=0.8)
    sh.text(*T(27.5, 0.8), "ROAD 10 m", 2.6, anchor="middle", weight="bold")

    t = 0.3   # wall / slab thickness (m)

    def building(x0, x1, top_x1, floors, front_left):
        """Cut walls and slabs. front_left=True if the street facade is the right wall."""
        zf = floors * FF
        # slabs
        for i in range(floors + 1):
            z = i * FF
            a = T(x0, z)
            sh.rect(a[0], a[1], (x1 - x0) * S, t * S, fill="#000", sw=0)
        # walls with window openings (sill 0.9 m, head 2.4 m)
        def wall(xw, z0, z1):
            for i in range(int(round((z1 - z0) / FF))):
                zb = z0 + i * FF
                for za, zb2 in ((zb, zb + 0.9), (zb + 2.4, zb + FF)):
                    a = T(xw, zb2)
                    sh.rect(a[0], a[1], t * S, (zb2 - za) * S, fill="#000", sw=0)
                # glazing line
                ga, gb = T(xw + t / 2, zb + 0.9), T(xw + t / 2, zb + 2.4)
                sh.line(ga[0], ga[1], gb[0], gb[1], 0.25)
        wall(x0, 0, zf)
        wall(x1 - t, 0, zf)
        if top_x1 is not None:
            front_x = x1 - t if front_left else x0
            # partial floor at the street side
            if front_left:
                tx0, tx1 = x1 - (top_x1), x1
            else:
                tx0, tx1 = x0, x0 + top_x1
            a = T(tx0, zf + FF)
            sh.rect(a[0], a[1], (tx1 - tx0) * S, t * S, fill="#000", sw=0)
            wall(tx0, zf, zf + FF)
            wall(tx1 - t, zf, zf + FF)
            # parapet / roof edge line
        # building outline (thin, for the elevation beyond)
        return zf

    zA = building(A_BLD[0], A_BLD[1], None, 4, True)
    zB = building(B_BLD[0], B_BLD[1], B2["top"], 8, False)

    # floor labels
    for i in range(4):
        sh.text(*T((A_BLD[0] + A_BLD[1]) / 2, i * FF + 1.25), f"FLOOR {i + 1}", 2.3,
                anchor="middle")
    for i in range(8):
        sh.text(*T((B_BLD[0] + B_BLD[1]) / 2, i * FF + 1.25), f"FLOOR {i + 1}", 2.3,
                anchor="middle")
    sh.text(*T((B_TOP[0] + B_TOP[1]) / 2, 24 + 1.25), "FL 9", 2.3, anchor="middle")

    # trees + people
    tree_elev(sh, T, 21.25, 7.5, 2.2)
    tree_elev(sh, T, 33.75, 7.5, 2.2)
    tree_elev(sh, T, 53.0, 6.0, 1.7)
    tree_elev(sh, T, 1.0, 3.2, 0.9)
    for X, f in ((18.0, False), (21.8, True), (23.6, False), (34.3, True), (37.0, False),
                 (52.2, True), (54.0, False)):
        person_elev(sh, T, X, f)

    # property / setback marks
    for X in (X_A_BACK, X_A_FRONT, X_B_FRONT, X_B_BACK):
        sh.line(*T(X, -2.6), *T(X, 28.5), 0.2, dash="3,1,0.5,1")
    for X in (X_A_FRONT - SETBACK, X_B_FRONT + SETBACK):
        sh.line(*T(X, zB + 1.5 if X > 30 else zA + 1.5), *T(X, 28.5), 0.15, dash="1,1")
    sh.text(*T(X_A_BACK + 0.3, 29.4), "rear lot line", 2.0, fill="#444")
    sh.text(*T(X_A_FRONT - 0.3, 29.4), "front lot line", 2.0, fill="#444", anchor="end")
    sh.text(*T(X_B_FRONT + 0.3, 27.8), "front lot line", 2.0, fill="#444")
    sh.text(*T(X_B_BACK - 0.3, 27.8), "rear lot line", 2.0, fill="#444", anchor="end")
    sh.text(*T(10, 25.0), "LOT A", 3.2, anchor="middle", weight="bold")
    sh.text(*T(10, 23.3), "BUILDING 1 · NO ELEVATOR", 2.5, anchor="middle")
    sh.text(*T(10, 21.6), "4 floors · H 12 m · GFA 560 m² · FAR 2.8", 2.3, anchor="middle")
    sh.text(*T(27.5, 25.0), "STREET", 3.2, anchor="middle", weight="bold")
    sh.text(*T(27.5, 23.3), "sidewalk + road + sidewalk = 15 m", 2.3, anchor="middle")
    sh.text(*T(45, 32.6), "LOT B", 3.2, anchor="middle", weight="bold")
    sh.text(*T(45, 31.0), "BUILDING 2 · LARGE BACKYARD", 2.5, anchor="middle")
    sh.text(*T(45, 29.4), "8 floors + 40 m² 9th · H 27 m · GFA 1,000 m² · FAR 5.0", 2.3,
            anchor="middle")

    # height dimensions
    xa = T(-2.0, 0)[0]
    dim_v(sh, xa, T(0, 12)[1], T(0, 0)[1], "H = 12 m", ext_from=T(A_BLD[0], 0)[0], size=2.6)
    for i in range(1, 4):
        y = T(0, i * FF)[1]
        sh.line(xa - 0.6, y + 0.6, xa + 0.6, y - 0.6, 0.25)
    xb = T(56.3, 0)[0]
    dim_v(sh, xb, T(0, 27)[1], T(0, 0)[1], "H = 27 m (8 × 3 m + 3 m partial 9th)",
          ext_from=T(B_BLD[1], 0)[0], size=2.6, side=1)
    sh.line(T(B_TOP[1], 27)[0] + 1, T(0, 27)[1], xb + 1.5, T(0, 27)[1], 0.13)
    for i in range(1, 9):
        y = T(0, i * FF)[1]
        sh.line(xb - 0.6, y + 0.6, xb + 0.6, y - 0.6, 0.25)
    # level marks
    for z, lab in ((0, "±0.00 grade"), (12, "+12.00"), (24, "+24.00"), (27, "+27.00")):
        X = 16.6 if z == 12 else (43.6 if z == 27 else (51.6 if z == 24 else 56.0))
        if z == 0:
            continue
        x, y = T(X, z)
        sh.poly([(x, y), (x - 1.2, y - 1.6), (x + 1.2, y - 1.6)], fill="#000", w=0.1)
        sh.text(x + 1.8, y - 0.4, lab, 2.3)
    sh.text(*T(-2.5, 0.4), "±0.00", 2.2, anchor="end")

    # dimension chains below grade
    yd1, yd2 = T(0, -4.5)[1], T(0, -7.5)[1]
    marks = chain_marks()
    labels = ["2 yard", "14", "4 setback", "2.5", "10", "2.5", "4 setback", "12", "4 yard"]
    for i, lab in enumerate(labels):
        x1, x2 = T(marks[i], 0)[0], T(marks[i + 1], 0)[0]
        dim_h(sh, x1, x2, yd1, lab, size=2.2)
    for m in marks:
        x = T(m, 0)[0]
        sh.line(x, T(0, -2.4)[1], x, yd1 + 1.5, 0.12, dash="0.8,0.8")
    dim_h(sh, T(0, 0)[0], T(55, 0)[0], yd2 + 2, "55 m overall  (27.5 cm at 1:200)", size=2.6)

    scale_bar(sh, 335, 60)
    notes = ["NOTES",
             "Cut through the middle of both lots",
             "(line A–A on the site plan), looking north.",
             "Solid black = walls and floor slabs cut.",
             "Floor-to-floor height 3.0 m.",
             "Building 2's 40 m² 9th floor sits on",
             "the street side of the roof.",
             "People 1.75 m tall; trees for scale."]
    for i, s in enumerate(notes):
        sh.text(335, 82 + i * 5, s, 2.6, weight="bold" if i == 0 else "normal")
    return sh


if __name__ == "__main__":
    sheets = [axon_sheet(B1, 1, "LOT A (west side of the street)"),
              axon_sheet(B2, 2, "LOT B (east side of the street)"),
              plan_sheet(), section_sheet()]
    names = ["1-axon-task1-no-elevator", "2-axon-task2-large-backyard", "3-site-plan",
             "4-section-AA"]
    for sh, n in zip(sheets, names):
        with open(os.path.join(OUT, n + ".svg"), "w") as f:
            f.write(sh.svg())
    print("wrote", len(sheets), "sheets")
