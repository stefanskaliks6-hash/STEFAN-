"""Alternative massing for Subarea 1 (same chart numbers, different building shapes).

Task 1: 8.75 m x 16 m footprint (140 m2), full buildable depth, 1.25 m side yard.
Task 2: 10 m x 12 m footprint (120 m2); the 40 m2 9th floor is 5 m x 8 m on the back half.
Writes four SVG sheets to ./alternative (render with render.js, OUTDIR=alternative).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_drawings as md  # noqa: E402
from make_drawings import (Sheet, frame, north_arrow, scale_bar, dim_h, dim_v,  # noqa: E402
                           tree_plan, person_plan, tree_elev, person_elev,
                           S, FF, W, LOT_W, LOT_D, SETBACK)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alternative")
ISO = math.cos(math.radians(30))

A1 = dict(name="TASK 1: NO ELEVATOR (ALTERNATIVE)", short="Building 1 · No Elevator · Alt.",
          bx=(1.25, 10.0), by=(4.0, 20.0), floors=4, top=None, H=12.0,
          dchain=[(0, 4, "4 m front setback"), (4, 20, "16 m building depth")],
          wchain=[(0, 1.25, "1.25"), (1.25, 10, "8.75 m building")],
          chart=[("Total GFA", "560 m²"), ("Built FAR", "2.8   (560 m² ÷ 200 m² lot)"),
                 ("Coverage", "70%   (140 m² ÷ 200 m² lot)"), ("Height", "12 m   (4 floors × 3 m)"),
                 ("Dimensions of Building Footprint", "8.75 m × 16 m = 140 m²"),
                 ("Area of Floor(s) × Number of Floor(s)", "140 m² × 4 floors"),
                 ("Number of floors", "4")],
          note="Lot 10 m × 20 m = 200 m² · front setback 4 m · rear yard 0 m · side yard 1.25 m",
          why=["Task: 4 floors that maximize the built area, then the",
               "smallest footprint that still gives that area.",
               "Max footprint = 70% × 200 m² = 140 m² → GFA 4 × 140 = 560 m².",
               "Only the footprint AREA is fixed (140 m²); its shape is a choice.",
               "Depth: all 16 m behind the 4 m setback (min back setback 0 m).",
               "Width: 140 ÷ 16 = 8.75 m → 1.25 m side yard (min side setback 0).",
               "Check: 6 m ≤ 12 m ≤ 27 m · 40% ≤ 70% ≤ 70% · FAR 2.8 ≤ 5",
               "Check: depth 16 m ≤ 16 m available · width 8.75 m ≤ 10 m"])
A2 = dict(name="TASK 2: LARGE BACKYARD (ALTERNATIVE)", short="Building 2 · Large Backyard · Alt.",
          bx=(0.0, 10.0), by=(4.0, 16.0), floors=8, top=(0.0, 5.0, 8.0, 16.0), H=27.0,
          dchain=[(0, 4, "4 m front setback"), (4, 16, "12 m building depth"), (16, 20, "4 m yard")],
          wchain=[(0, 10, "10 m frontage (full lot width)")],
          chart=[("Total GFA", "1,000 m²"), ("Built FAR", "5.0   (1,000 m² ÷ 200 m² lot)"),
                 ("Coverage", "60%   (120 m² ÷ 200 m² lot)"), ("Height", "27 m   (9 floors × 3 m)"),
                 ("Dimensions of Building Footprint", "10 m × 12 m = 120 m²"),
                 ("Area of Floor(s) × Number of Floor(s)", "120 m² × 8 floors + 40 m² × 1 floor"),
                 ("Number of floors", "9  (8 full + 1 partial)")],
          note="Lot 10 m × 20 m = 200 m² · front setback 4 m · rear yard 4 m · 9th floor 5 m × 8 m at the back",
          why=["Task: 60% coverage, maximize the built area.",
               "Footprint = 60% × 200 m² = 120 m² = 10 m × 12 m; full width keeps",
               "the backyard as one usable 10 m × 4 m space (40 m²).",
               "Max GFA = FAR 5 × 200 m² = 1,000 m²; max 27 m ÷ 3 m = 9 floors.",
               "8 × 120 m² = 960 m²; a full 9th floor = 1,080 m² > 1,000 m².",
               "Remaining 40 m² = 9th floor 5 m × 8 m on the back half of the roof.",
               "960 + 40 = 1,000 m² (partial top floor, as in Lab 6).",
               "Check: 6 m ≤ 27 m ≤ 27 m · 40% ≤ 60% ≤ 70% · FAR 5.0 ≤ 5"])


# ---------------------------------------------------------------- axonometric
def axon_sheet(b, sheet_no, lot_name, leaders):
    sh = Sheet()
    frame(sh, f"AXONOMETRIC VIEW — {b['name']}", f"Axonometric (isometric) · {b['short']}", sheet_no)
    ox, oy = 140.0, 245.0
    ex, ey = (ISO, -0.5), (-ISO, -0.5)

    def P(x, y, z=0.0):
        return (ox + S * (x * ex[0] + y * ey[0]), oy + S * (x * ex[1] + y * ey[1] - z))

    CON = "#9a9a9a"
    (x0, x1), (y0, y1) = b["bx"], b["by"]
    zf, zt = b["floors"] * FF, b["H"]

    def con(p, q):
        sh.line(p[0], p[1], q[0], q[1], 0.12, color=CON)

    # construction lines
    for yy in sorted({0, y0, y1, LOT_D}):
        con(P(-3, yy), P(LOT_W + 3, yy))
    for xx in sorted({0, x0, x1, LOT_W}):
        con(P(xx, -3), P(xx, LOT_D + 3))
    for xx, yy in ((x0, y0), (x1, y0), (x0, y1)):
        con(P(xx, yy, 0), P(xx, yy, zt + 2.5))
    for z in [FF * i for i in range(1, int(zt / FF) + 1)]:
        con(P(LOT_W, SETBACK, z), P(LOT_W + 1.2, SETBACK, z))

    # sidewalk, lot, setback line, grass
    sh.poly([P(0, -2.5), P(LOT_W, -2.5), P(LOT_W, 0), P(0, 0)], fill="#f2f2f2", w=0.18)
    sh.text(*P(5.0, -1.55), "SIDEWALK 2.5 m", 2.2, anchor="middle", rot=-30)
    sh.poly([P(0, 0), P(LOT_W, 0), P(LOT_W, LOT_D), P(0, LOT_D)], fill="#fff", w=0.35)
    sh.line(*P(-0.8, SETBACK), *P(LOT_W + 0.8, SETBACK), 0.25, dash="2,1,0.4,1")
    for yy in [i * 0.8 + 0.4 for i in range(int(LOT_D / 0.8))]:
        for xx in [j * 1.0 + 0.5 for j in range(10)]:
            gx = xx + (0.4 if int(yy / 0.8) % 2 else 0)
            if x0 - 0.3 < gx < x1 + 0.3 and y0 - 0.3 < yy < y1 + 0.3:
                continue
            if gx > LOT_W:
                continue
            px, py = P(gx, yy)
            sh.line(px, py, px + 0.5, py - 0.3, 0.12, color="#555")

    def box(ax0, ax1, ay0, ay1, az0, az1):
        left = [P(ax0, ay0, az0), P(ax0, ay1, az0), P(ax0, ay1, az1), P(ax0, ay0, az1)]
        front = [P(ax0, ay0, az0), P(ax1, ay0, az0), P(ax1, ay0, az1), P(ax0, ay0, az1)]
        top = [P(ax0, ay0, az1), P(ax1, ay0, az1), P(ax1, ay1, az1), P(ax0, ay1, az1)]
        sh.poly(left, fill="#c9c9c9", w=0.5)
        sh.poly(front, fill="#ffffff", w=0.5)
        sh.poly(top, fill="#ececec", w=0.5)
        for z in [FF * i for i in range(1, 10)]:
            if az0 < z < az1:
                sh.line(*P(ax0, ay0, z), *P(ax0, ay1, z), 0.18)
                sh.line(*P(ax0, ay0, z), *P(ax1, ay0, z), 0.18)

    box(x0, x1, y0, y1, 0, zf)
    area = (x1 - x0) * (y1 - y0)
    for i in range(b["floors"]):
        sh.text(*P((x0 + x1) / 2, y0, i * FF + 1.1), f"FLOOR {i + 1} · {area:.0f} m²", 2.1,
                anchor="middle", rot=-30)
    if b["top"]:
        tx0, tx1, ty0, ty1 = b["top"]
        box(tx0, tx1, ty0, ty1, zf, zf + FF)
        sh.text(*P((tx0 + tx1) / 2, ty0, zf + 1.1), "FLOOR 9 · 40 m²", 1.9, anchor="middle", rot=-30)

    def tick(px, py, d):
        a = math.atan2(d[1], d[0]) + math.radians(45)
        sh.line(px - math.cos(a), py - math.sin(a), px + math.cos(a), py + math.sin(a), 0.4)

    def gdim(ya, yb, off, label):
        a, c = P(-off, ya), P(-off, yb)
        sh.line(*a, *c, 0.18)
        for yy, (px, py) in ((ya, a), (yb, c)):
            g, q = P(-0.4, yy), P(-off - 0.6, yy)
            sh.line(g[0], g[1], q[0], q[1], 0.12)
            tick(px, py, ey)
        m = P(-off - 0.9, (ya + yb) / 2)
        sh.text(m[0], m[1], label, 2.5, anchor="middle", rot=30)

    def fdim(xa, xb, off, label):
        a, c = P(xa, -off), P(xb, -off)
        sh.line(*a, *c, 0.18)
        for xx, (px, py) in ((xa, a), (xb, c)):
            g, q = P(xx, -2.9), P(xx, -off - 0.6)
            sh.line(g[0], g[1], q[0], q[1], 0.12)
            tick(px, py, ex)
        m = P((xa + xb) / 2, -off - 1.1)
        sh.text(m[0], m[1] + 1.0, label, 2.4, anchor="middle", rot=-30)

    for ya, yb, lab in b["dchain"]:
        gdim(ya, yb, 2.0, lab)
    gdim(0, LOT_D, 5.0, "lot depth 20 m")
    for xa, xb, lab in b["wchain"]:
        fdim(xa, xb, 4.5, lab)
    if len(b["wchain"]) > 1:
        fdim(0, LOT_W, 7.3, "10 m lot frontage")

    hx = LOT_W + 2.4
    base, topp = P(hx, SETBACK, 0), P(hx, SETBACK, zt)
    sh.line(base[0], base[1] + 1.5, topp[0], topp[1] - 1.5, 0.18)
    for z in [0] + [FF * i for i in range(1, int(zt / FF) + 1)]:
        px, py = P(hx, SETBACK, z)
        if z in (0, zt):
            tick(px, py, (0, -1))
        else:
            sh.line(px - 0.6, py, px + 0.6, py, 0.25)
    if b["top"] and b["top"][2] > SETBACK:      # top floor set back: extend the 27 m line to it
        sh.line(*P(b["top"][1], b["top"][2], zt), *P(hx + 0.4, SETBACK, zt), 0.12, color=CON)
    sh.text(base[0] + 4.2, (base[1] + topp[1]) / 2, f"HEIGHT {zt:.0f} m", 3.2, anchor="middle",
            rot=90, weight="bold")
    sh.text(base[0] + 8.4, (base[1] + topp[1]) / 2, f"{int(zt / FF)} floors × 3 m", 2.4,
            anchor="middle", rot=90)

    for (px_, py_, pz_), tx, ty, lines, anchor in leaders:
        pt = P(px_, py_, pz_)
        sh.line(pt[0], pt[1], tx, ty, 0.15)
        sh.circle(pt[0], pt[1], 0.45, fill="#000", w=0.1)
        for i, s in enumerate(lines):
            sh.text(tx + (1 if anchor == "start" else -1), ty + 1 + i * 3.6, s, 2.6, anchor=anchor)

    nang = math.degrees(math.atan2(ex[1], ex[0])) if sheet_no == 1 else \
        math.degrees(math.atan2(-ex[1], -ex[0]))
    north_arrow(sh, 36, 112, ang_deg=nang)
    sh.text(36, 130, "north (ground plane)", 2.2, anchor="middle")
    scale_bar(sh, W - 152, 196)
    sh.text(20, 31, f"{lot_name} · scale 1:200 · isometric: plan axes at 30° to the horizontal, "
                    "all lengths measured true along the axes", 2.8)

    cx0, cy0, cw, kw = W - 10 - 142, 40, 140, 64
    rows = b["chart"]
    sh.text(cx0, cy0 - 3, "CHART", 4, weight="bold")
    rh = 7.5
    sh.rect(cx0, cy0, cw, rh * len(rows), sw=0.45)
    for i, (k, v) in enumerate(rows):
        y = cy0 + i * rh
        if i:
            sh.line(cx0, y, cx0 + cw, y, 0.2)
        sh.text(cx0 + 2, y + 5, k, 2.6, weight="bold")
        sh.text(cx0 + kw + 2, y + 5, v, 2.8)
    sh.line(cx0 + kw, cy0, cx0 + kw, cy0 + rh * len(rows), 0.2)
    sh.text(cx0, cy0 + rh * len(rows) + 4.5, b["note"], 2.3)
    ry = cy0 + rh * len(rows) + 13
    sh.text(cx0, ry, "CALCULATION", 3.2, weight="bold")
    for i, s in enumerate(b["why"]):
        sh.text(cx0, ry + 5.5 + i * 4.3, s, 2.55, weight="bold" if s.startswith("Check") else "normal")
    return sh


# ---------------------------------------------------------------- plan
XA_B, XA_F = 0.0, 20.0
X_SW1, X_C1, X_C2, X_SW2 = 20.0, 22.5, 32.5, 35.0
XB_F, XB_B = 35.0, 55.0
# Lot A: lot width axis = north, so plan Y = local x.  Lot B: plan Y = 10 - local x.
A_X = (XA_F - A1["by"][1], XA_F - A1["by"][0])          # 0 .. 16
A_Y = A1["bx"]                                           # 1.25 .. 10
B_X = (XB_F + A2["by"][0], XB_F + A2["by"][1])          # 39 .. 51
B_Y = (0.0, 10.0)
B_TX = (XB_F + A2["top"][2], XB_F + A2["top"][3])       # 43 .. 51
B_TY = (LOT_W - A2["top"][1], LOT_W - A2["top"][0])     # 5 .. 10
YC = 7.0                                                 # section cut, metres from the south lot line
MARKS = [XA_B, A_X[1], XA_F, X_C1, X_C2, X_SW2, B_X[0], B_X[1], XB_B]


def plan_sheet():
    sh = Sheet()
    frame(sh, "PLAN VIEW — BOTH SITUATIONS, 15 m APART (ALTERNATIVE)",
          "Plan view · alternative massing · Lots A & B", 3)
    sh.text(20, 31, "Lots face each other across a 15 m street: 2.5 m sidewalk + 10 m road + 2.5 m sidewalk · scale 1:200", 2.8)
    px0, py0 = 34.0, 172.0

    def T(X, Y):
        return (px0 + X * S, py0 - Y * S)

    def rect(x0, x1, y0, y1, **kw):
        a = T(x0, y1)
        sh.rect(a[0], a[1], (x1 - x0) * S, (y1 - y0) * S, **kw)

    ymin, ymax = -11.0, 21.0
    rect(X_C1, X_C2, ymin, ymax, fill="#efefef", sw=0)
    for X in (X_C1, X_C2):
        sh.line(*T(X, ymin), *T(X, ymax), 0.4)
    for X in (X_SW1, X_SW2):
        sh.line(*T(X, ymin), *T(X, ymax), 0.3)
    sh.line(*T(27.5, ymin), *T(27.5, ymax), 0.25, dash="4,2.5")
    for X0, X1 in ((X_SW1, X_C1), (X_C2, X_SW2)):
        y = ymin
        while y <= ymax:
            sh.line(*T(X0, y), *T(X1, y), 0.1, color="#666")
            y += 1.5
    sh.text(*T(26.5, 15.0), "ROAD  10 m", 3.0, anchor="middle", rot=-90, weight="bold")
    sh.text(*T(21.65, 13.0), "SIDEWALK 2.5 m", 2.2, anchor="middle", rot=-90)
    sh.text(*T(34.15, 13.0), "SIDEWALK 2.5 m", 2.2, anchor="middle", rot=-90)
    for X, d in ((25, -1), (30, 1)):
        a, c = T(X, 4 - d * 3), T(X, 4 + d * 3)
        sh.add(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{c[0]:.2f}" y2="{c[1]:.2f}" '
               f'stroke="#888" stroke-width="0.3" marker-end="url(#arr)"/>')
    for X0, X1 in ((XA_B, XA_F), (XB_F, XB_B)):
        for Y in (-10, 20):
            sh.line(*T(X0, Y), *T(X1, Y), 0.2, dash="3,1,0.5,1")
        sh.line(*T(X0, ymin), *T(X0, ymax), 0.2, dash="3,1,0.5,1")
        sh.text(*T((X0 + X1) / 2, -5), "neighbouring lot", 2.4, anchor="middle", fill="#666", italic=True)
        sh.text(*T((X0 + X1) / 2, 15), "neighbouring lot", 2.4, anchor="middle", fill="#666", italic=True)
        rect(X0, X1, 0, 10, sw=0.6)
    for X in (XA_F - SETBACK, XB_F + SETBACK):
        sh.line(*T(X, -1.0), *T(X, 11.0), 0.25, dash="2,1,0.4,1")

    # section cut A-A
    a, c = T(-3.0, YC), T(58.8, YC)
    sh.line(a[0], a[1], c[0], c[1], 0.35, dash="7,1.5,1.2,1.5")
    for X in (-3.6, 59.4):
        cx, cy = T(X, YC)
        sh.circle(cx, cy, 3.4, w=0.4)
        sh.text(cx, cy + 1.3, "A", 3.6, anchor="middle", weight="bold")
        sh.poly([(cx - 2.6, cy - 3.0), (cx + 2.6, cy - 3.0), (cx, cy - 7.0)], fill="#000", w=0.1)

    # buildings
    rect(*A_X, *A_Y, fill="url(#hatch)", sw=0.8)
    rect(*B_X, *B_Y, fill="url(#hatch)", sw=0.8)
    rect(*B_TX, *B_TY, fill="url(#hatch2)", sw=0.8)

    def label(X, Y, lines, w):
        cx, cy = T(X, Y)
        h = len(lines) * 3.6
        sh.rect(cx - w / 2, cy - h / 2 - 2.6, w, h + 1.8, fill="#fff", sw=0.2)
        for i, s in enumerate(lines):
            sh.text(cx, cy - h / 2 + 1.0 + i * 3.6, s, 2.5 if i else 2.6, anchor="middle",
                    weight="bold" if i == 0 else "normal")

    label(8.0, 4.4, ["BUILDING 1 — NO ELEVATOR", "4 floors · H 12 m", "8.75 × 16 m · 70%",
                     "GFA 560 m² · FAR 2.8"], 38)
    label(45.0, 2.6, ["BUILDING 2 — LARGE BACKYARD", "8 fl. + 9th · H 27 m",
                      "10 × 12 m · 60% · FAR 5.0"], 44)
    label(47.0, 8.3, ["9th floor", "5 × 8 m = 40 m²"], 22)

    for X, s in ((10, "LOT A · 10 × 20 m = 200 m²"), (45, "LOT B · 10 × 20 m = 200 m²")):
        sh.text(*T(X, 11.2), s, 2.7, anchor="middle", weight="bold")
    sh.text(*T(1.0, -1.2), "rear lot line", 2.0, fill="#444")
    sh.text(*T(54.0, -1.2), "rear lot line", 2.0, fill="#444", anchor="end")
    sh.text(*T(XA_F - SETBACK + 0.5, -2.2), "setback line", 2.0, fill="#444")
    sh.text(*T(XB_F + SETBACK - 0.5, -2.2), "setback line", 2.0, fill="#444", anchor="end")
    sh.text(*T(8.0, 0.33), "side yard 1.25 m", 2.0, anchor="middle")
    sh.text(*T(53.0, 0.6), "backyard 4 m", 2.0, anchor="middle")

    for X, Y, r in ((21.25, 18.0, 2.2), (21.25, -4.0, 2.2), (33.75, 8.0, 2.2),
                    (33.75, -8.0, 2.2), (53.0, 7.5, 1.8), (18.0, 8.2, 1.5)):
        tree_plan(sh, *T(X, Y), r * S)
    for X, Y in ((3.0, 0.62), (13.5, 0.62)):
        tree_plan(sh, *T(X, Y), 0.5 * S)
    for X, Y in ((21.0, 6.0), (21.6, 1.0), (34.0, 2.5), (17.6, 3.0), (37.0, 3.5),
                 (52.5, 3.0), (53.6, 2.2)):
        person_plan(sh, *T(X, Y))

    yd1, yd2 = T(0, -13.5)[1], T(0, -16.5)[1]
    labs = ["16", "4", "2.5", "10", "2.5", "4", "12", "4"]
    for i, lab in enumerate(labs):
        dim_h(sh, T(MARKS[i], 0)[0], T(MARKS[i + 1], 0)[0], yd1, lab + (" m" if i == 0 else ""), size=2.4)
    for m in MARKS:
        x = T(m, 0)[0]
        sh.line(x, T(0, -0.5)[1] if m not in (X_C1, X_C2) else T(0, ymin)[1] + 1, x, yd1 + 1.5,
                0.12, dash="0.8,0.8")
    dim_h(sh, T(0, 0)[0], T(20, 0)[0], yd2, "LOT A 20 m", size=2.4)
    dim_h(sh, T(20, 0)[0], T(35, 0)[0], yd2, "STREET R.O.W. 15 m", size=2.4)
    dim_h(sh, T(35, 0)[0], T(55, 0)[0], yd2, "LOT B 20 m", size=2.4)
    dim_h(sh, T(0, 0)[0], T(55, 0)[0], yd2 + 7, "55 m overall  (27.5 cm at 1:200)", size=2.6)
    # Lot A width split: 1.25 m side yard + 8.75 m building
    xa = T(-1.6, 0)[0]
    dim_v(sh, xa, T(0, 10)[1], T(0, 1.25)[1], "8.75 m", size=2.4)
    sh.line(xa, T(0, 1.25)[1], xa, T(0, 0)[1] + 1.5, 0.18)
    sh.line(xa - 0.84, T(0, 0)[1] + 0.84, xa + 0.84, T(0, 0)[1] - 0.84, 0.4)
    sh.text(xa - 1.2, T(0, 0.2)[1], "1.25", 2.0, anchor="end")
    # Lot B width split: 9th floor on the north half
    xb = T(56.4, 0)[0]
    dim_v(sh, xb, T(0, 10)[1], T(0, 5)[1], "5 m", size=2.4, side=1)
    dim_v(sh, xb, T(0, 5)[1], T(0, 0)[1], "5 m", size=2.4, side=1)

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
             "Section A–A is cut 7 m from the south",
             "lot line, through both buildings and",
             "Building 2's 9th floor."]
    for i, s in enumerate(notes):
        sh.text(335, 112 + i * 5, s, 2.6, weight="bold" if i == 0 else "normal")
    return sh


# ---------------------------------------------------------------- section
def section_sheet():
    sh = Sheet()
    frame(sh, "SECTION VIEW A–A — BOTH BUILDINGS, 15 m APART (ALTERNATIVE)",
          "Section A–A · alternative massing · Lots A & B", 4)
    sh.text(20, 31, "Cut along line A–A on the plan view (7 m from the south lot line), looking north · "
                    "2.5 m sidewalk + 10 m road + 2.5 m sidewalk between the lots · scale 1:200", 2.8)
    px0, gy = 30.0, 196.0

    def T(X, z):
        return (px0 + X * S, gy - z * S)

    rz = -0.15
    sh.poly([T(-3, 0), T(X_C1, 0), T(X_C1, rz), T(X_C2, rz), T(X_C2, 0), T(55.6, 0),
             T(55.6, -2.2), T(-3, -2.2)], fill="url(#earth)", w=0)
    sh.poly([T(-3, 0), T(X_C1, 0), T(X_C1, rz), T(X_C2, rz), T(X_C2, 0), T(55.6, 0)], close=False, w=0.8)
    sh.text(*T(27.5, 0.8), "ROAD 10 m", 2.6, anchor="middle", weight="bold")
    t = 0.3

    def wall(xw, z0, z1):
        for i in range(int(round((z1 - z0) / FF))):
            zb = z0 + i * FF
            for za, zb2 in ((zb, zb + 0.9), (zb + 2.4, zb + FF)):
                a = T(xw, zb2)
                sh.rect(a[0], a[1], t * S, (zb2 - za) * S, fill="#000", sw=0)
            ga, gb = T(xw + t / 2, zb + 0.9), T(xw + t / 2, zb + 2.4)
            sh.line(ga[0], ga[1], gb[0], gb[1], 0.25)

    def building(x0, x1, floors, top=None):
        zf = floors * FF
        for i in range(floors + 1):
            a = T(x0, i * FF)
            sh.rect(a[0], a[1], (x1 - x0) * S, t * S, fill="#000", sw=0)
        wall(x0, 0, zf)
        wall(x1 - t, 0, zf)
        if top:
            tx0, tx1 = top
            a = T(tx0, zf + FF)
            sh.rect(a[0], a[1], (tx1 - tx0) * S, t * S, fill="#000", sw=0)
            wall(tx0, zf, zf + FF)
            wall(tx1 - t, zf, zf + FF)

    building(*A_X, 4)
    building(*B_X, 8, B_TX)
    for i in range(4):
        sh.text(*T((A_X[0] + A_X[1]) / 2, i * FF + 1.25), f"FLOOR {i + 1}", 2.3, anchor="middle")
    for i in range(8):
        sh.text(*T((B_X[0] + B_X[1]) / 2, i * FF + 1.25), f"FLOOR {i + 1}", 2.3, anchor="middle")
    sh.text(*T((B_TX[0] + B_TX[1]) / 2, 24 + 1.25), "FLOOR 9 (5 × 8 m)", 2.3, anchor="middle")

    tree_elev(sh, T, 21.25, 7.5, 2.2)
    tree_elev(sh, T, 33.75, 7.5, 2.2)
    tree_elev(sh, T, 53.0, 6.0, 1.7)
    tree_elev(sh, T, 18.0, 5.0, 1.5)
    for X, fl in ((16.9, False), (21.8, True), (23.6, False), (34.3, True), (37.0, False),
                  (52.0, True), (54.1, False)):
        person_elev(sh, T, X, fl)

    for X in (XA_B, XA_F, XB_F, XB_B):
        sh.line(*T(X, -2.6), *T(X, 28.5), 0.2, dash="3,1,0.5,1")
    sh.line(*T(XA_F - SETBACK, 13.5), *T(XA_F - SETBACK, 28.5), 0.15, dash="1,1")
    sh.line(*T(XB_F + SETBACK, 25.5), *T(XB_F + SETBACK, 28.5), 0.15, dash="1,1")
    sh.text(*T(XA_B + 0.3, 29.4), "rear lot line", 2.0, fill="#444")
    sh.text(*T(XA_F - 0.3, 29.4), "front lot line", 2.0, fill="#444", anchor="end")
    sh.text(*T(XB_F + 0.3, 22.0), "front lot line", 2.0, fill="#444")
    sh.text(*T(XB_B - 0.3, 22.0), "rear lot line", 2.0, fill="#444", anchor="end")
    sh.text(*T(10, 25.0), "LOT A", 3.2, anchor="middle", weight="bold")
    sh.text(*T(10, 23.3), "BUILDING 1 · NO ELEVATOR", 2.5, anchor="middle")
    sh.text(*T(10, 21.6), "8.75 × 16 m · 4 floors · H 12 m · GFA 560 m² · FAR 2.8", 2.3, anchor="middle")
    sh.text(*T(10, 19.9), "no rear yard (back setback min 0 m)", 2.3, anchor="middle")
    sh.text(*T(27.5, 25.0), "STREET", 3.2, anchor="middle", weight="bold")
    sh.text(*T(27.5, 23.3), "sidewalk + road + sidewalk = 15 m", 2.3, anchor="middle")
    sh.text(*T(45, 32.0), "LOT B", 3.2, anchor="middle", weight="bold")
    sh.text(*T(45, 30.4), "BUILDING 2 · LARGE BACKYARD", 2.5, anchor="middle")
    sh.text(*T(45, 28.8), "10 × 12 m · 8 floors + 40 m² 9th · H 27 m · GFA 1,000 m² · FAR 5.0", 2.3,
            anchor="middle")

    xa = T(-2.0, 0)[0]
    dim_v(sh, xa, T(0, 12)[1], T(0, 0)[1], "H = 12 m", ext_from=T(A_X[0], 0)[0], size=2.6)
    for i in range(1, 4):
        y = T(0, i * FF)[1]
        sh.line(xa - 0.6, y + 0.6, xa + 0.6, y - 0.6, 0.25)
    xb = T(56.3, 0)[0]
    dim_v(sh, xb, T(0, 27)[1], T(0, 0)[1], "H = 27 m (8 × 3 m + 3 m partial 9th)",
          ext_from=T(B_X[1], 0)[0], size=2.6, side=1)
    sh.line(T(B_TX[1], 27)[0] + 1, T(0, 27)[1], xb + 1.5, T(0, 27)[1], 0.13)
    for i in range(1, 9):
        y = T(0, i * FF)[1]
        sh.line(xb - 0.6, y + 0.6, xb + 0.6, y - 0.6, 0.25)

    def level(X, z, lab, left=False):
        x, y = T(X, z)
        sh.poly([(x, y), (x - 1.2, y - 1.6), (x + 1.2, y - 1.6)], fill="#000", w=0.1)
        sh.text(x + (-1.8 if left else 1.8), y - 0.4, lab, 2.3, anchor="end" if left else "start")
    level(16.6, 12, "+12.00")
    level(38.4, 24, "+24.00", left=True)
    level(42.4, 27, "+27.00", left=True)
    sh.text(*T(-2.5, 0.4), "±0.00", 2.2, anchor="end")
    sh.text(*T(-1.0, -1.2), "WEST", 2.4, anchor="end", weight="bold")
    sh.text(*T(56.0, -1.2), "EAST", 2.4, weight="bold")

    yd1, yd2 = T(0, -4.5)[1], T(0, -7.5)[1]
    labels = ["16 building", "4 setback", "2.5", "10", "2.5", "4 setback", "12", "4 yard"]
    for i, lab in enumerate(labels):
        dim_h(sh, T(MARKS[i], 0)[0], T(MARKS[i + 1], 0)[0], yd1, lab, size=2.2)
    for m in MARKS:
        x = T(m, 0)[0]
        sh.line(x, T(0, -2.4)[1], x, yd1 + 1.5, 0.12, dash="0.8,0.8")
    dim_h(sh, T(0, 0)[0], T(55, 0)[0], yd2 + 2, "55 m overall  (27.5 cm at 1:200)", size=2.6)

    scale_bar(sh, 335, 60)
    north_arrow(sh, 352, 150)
    sh.text(352, 168, "plan north (section looks north)", 2.2, anchor="middle")
    notes = ["NOTES",
             "Cut 7 m from the south lot line",
             "(line A–A on the plan view), looking north.",
             "Solid black = walls and floor slabs cut.",
             "Floor-to-floor height 3.0 m.",
             "Building 1 runs the full 16 m behind",
             "the setback (no rear yard).",
             "Building 2's 40 m² 9th floor (5 × 8 m)",
             "sits on the back half of the roof.",
             "People 1.75 m tall; trees for scale."]
    for i, s in enumerate(notes):
        sh.text(335, 82 + i * 5, s, 2.6, weight="bold" if i == 0 else "normal")
    return sh


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    lead1 = [((6, 2, 0), 212, 212, ["FRONT SETBACK 4 m (street side)"], "start"),
             ((0.6, 11, 0), 51, 183, ["SIDE YARD 1.25 m", "(side setback min 0 m)"], "end"),
             ((6, 12, 12), 212, 118, ["ROOF", "footprint 8.75 m × 16 m = 140 m²"], "start"),
             ((9.5, 19.5, 12), 212, 96, ["REAR WALL ON THE REAR LOT LINE", "(back setback min 0 m)"], "start")]
    lead2 = [((6, 2, 0), 212, 212, ["FRONT SETBACK 4 m (street side)"], "start"),
             ((0.5, 18, 0), 51, 183, ["BACKYARD 4 m deep", "(40 m²)"], "end"),
             ((7.5, 10, 24), 212, 62, ["ROOF OF 8th FLOOR", "footprint 10 m × 12 m = 120 m²"], "start"),
             ((2.5, 12, 27), 100, 50, ["PARTIAL 9th FLOOR 5 m × 8 m = 40 m²", "(on the back half of the roof)"], "end")]
    sheets = [axon_sheet(A1, 1, "LOT A (west side of the street)", lead1),
              axon_sheet(A2, 2, "LOT B (east side of the street)", lead2),
              plan_sheet(), section_sheet()]
    names = ["1-axon-task1-alt", "2-axon-task2-alt", "3-plan-alt", "4-section-alt"]
    for sh, n in zip(sheets, names):
        with open(os.path.join(OUT, n + ".svg"), "w") as fh:
            fh.write(sh.svg())
    print("wrote", len(sheets), "alternative sheets to", OUT)
