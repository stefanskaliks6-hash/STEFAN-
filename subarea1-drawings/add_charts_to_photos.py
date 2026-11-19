"""Write the chart + calculation onto photos of the hand-drawn axonometrics.

Usage: python3 add_charts_to_photos.py <task1_image> <task2_image> <out_dir>
The inputs are screenshots of the scanned PDF; the photo area is cropped and upscaled 2x.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

CROP = (305, 283, 1695, 1063)   # photo area inside the Preview screenshot
K = 2                           # upscale factor
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
INK = (52, 52, 56, 225)
RULE = (80, 80, 84, 150)


def load(path):
    im = Image.open(path).convert("RGB").crop(CROP)
    return im.resize((im.width * K, im.height * K), Image.LANCZOS).convert("RGBA")


def write(im, x, y, rows, size, gap, rule_to, calc, calc_y, heading=None, skip_first_label=False):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(FONT, size * K)
    fb = ImageFont.truetype(BOLD, size * K)
    if heading:
        d.text((x * K, (y - gap) * K), heading, font=ImageFont.truetype(BOLD, int(size * 1.25) * K), fill=INK)
    for i, (label, value) in enumerate(rows):
        yy = (y + i * gap) * K
        if skip_first_label and i == 0:
            # the student already wrote "Total GFA:" on this line; add only the value
            d.text((label * K, yy), value, font=fb, fill=INK)
            continue
        d.text((x * K, yy), label, font=f, fill=INK)
        lw = d.textlength(label + " ", font=f)
        d.text((x * K + lw, yy), value, font=fb, fill=INK)
        d.line([(x * K, yy + (size + 6) * K), (rule_to * K, yy + (size + 6) * K)], fill=RULE, width=K)
    d.text((x * K, calc_y * K), "CALCULATION", font=fb, fill=INK)
    for i, s in enumerate(calc):
        d.text((x * K, (calc_y + (i + 1) * (size + 9)) * K), s, font=f, fill=INK)
    return Image.alpha_composite(im, layer).convert("RGB")


def main(p1, p2, out):
    t1 = load(p1)
    rows1 = [(1150, "560 m²"),
             ("Built FAR:", "560 ÷ 200 = 2.8"),
             ("Coverage:", "140 ÷ 200 = 70%"),
             ("Height:", "4 floors × 3 m = 12 m"),
             ("Footprint:", "10 m × 14 m = 140 m²"),
             ("Floor area × floors:", "140 m² × 4"),
             ("Number of floors:", "4")]
    calc1 = ["Max footprint = 70% × 200 = 140 m²",
             "GFA = 4 floors × 140 m² = 560 m²",
             "FAR = 560 ÷ 200 = 2.8  (max 5)",
             "Yard = 20 − 4 − 14 = 2 m  (20 m²)"]
    t1 = write(t1, 1030, 324, rows1, 12, 30, 1250, calc1, 540, skip_first_label=True)
    t1.save(f"{out}/task1-no-elevator-with-chart.png")

    t2 = load(p2)
    rows2 = [("Total GFA:", "1,000 m²"),
             ("Built FAR:", "1,000 ÷ 200 = 5.0"),
             ("Coverage:", "120 ÷ 200 = 60%"),
             ("Height:", "9 floors × 3 m = 27 m"),
             ("Footprint:", "10 m × 12 m = 120 m²"),
             ("Floor area × floors:", "120 m² × 8 + 40 m² × 1"),
             ("Number of floors:", "9  (8 full + 1 partial)")]
    calc2 = ["Footprint = 60% × 200 m² = 120 m²  (10 × 12 m)",
             "Max GFA = FAR 5 × 200 m² = 1,000 m²",
             "8 floors × 120 m² = 960 m²",
             "9th floor 10 m × 4 m = 40 m² → 960 + 40 = 1,000 m²",
             "Backyard = 20 − 4 − 12 = 4 m  (40 m²)"]
    t2 = write(t2, 720, 160, rows2, 14, 36, 1130, calc2, 430, heading="CHART")
    t2.save(f"{out}/task2-large-backyard-with-chart.png")

    t1.save(f"{out}/Subarea1-hand-drawn-axons-with-charts.pdf", save_all=True, append_images=[t2],
            resolution=200)


if __name__ == "__main__":
    main(*sys.argv[1:4])
