#!/usr/bin/env python3
"""Draw the front page of 26 November 2026 as one 1024x1024 PNG.

A newspaper front page: masthead, one lead story (Houthis hit the Saudi
Ras Tanura refinery, Brent crude tops $94) and six more stories of the day
-- Hormuz mines, Gaza strike, BepiColombo at Mercury, the chess world
championship, the Cairo tanker fire, and the US tariff plan for Taiwan.
Every illustration is drawn from scratch with PIL primitives.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (18, 18, 18)
RED = (158, 24, 24)
BLUE = (24, 58, 110)
GREY = (96, 96, 96)
LINE = (18, 18, 18)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, spacing=4):
    x, y = xy
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def kicker(draw, xy, text, color=RED):
    f = font(SANS_B, 15)
    draw.text(xy, text.upper(), font=f, fill=color)
    return xy[1] + 20


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- frame ---------------------------------------------------------------
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

# ---- masthead ------------------------------------------------------------
d.text((W // 2, 44), "THE WORLD TODAY", font=font(SERIF, 66),
       fill=INK, anchor="mt")
d.line([60, 128, W - 60, 128], fill=INK, width=3)
d.line([60, 134, W - 60, 134], fill=INK, width=1)
f_date = font(SANS_B, 19)
d.text((60, 146), "THURSDAY, 26 NOVEMBER 2026", font=f_date, fill=INK)
d.text((W - 60, 146), "ONE DAY  •  ONE PAGE", font=f_date,
       fill=INK, anchor="rt")
d.line([60, 178, W - 60, 178], fill=INK, width=1)

# ---- lead story: Houthis hit Ras Tanura ----------------------------------
ly = 192
d.rectangle([60, ly, W - 60, ly + 232], outline=INK, width=2)
# illustration panel on the right: burning refinery at dusk
px0, py0, px1, py1 = W - 330, ly + 12, W - 72, ly + 220
d.rectangle([px0, py0, px1, py1], fill=(32, 26, 22))
d.rectangle([px0, py1 - 46, px1, py1], fill=(58, 40, 26))
d.text((px0 + 12, py0 + 8), "RAS TANURA", font=font(SANS_B, 15), fill=(250, 205, 60))
# refinery towers, flames sitting on their tops (below the label)
for tx, th in [(px0 + 26, 70), (px0 + 66, 92), (px0 + 106, 64), (px0 + 146, 84)]:
    top = py1 - 46 - th
    d.rectangle([tx, top, tx + 22, py1 - 46], fill=(12, 12, 12))
    d.rectangle([tx + 6, top - 14, tx + 16, top], fill=(12, 12, 12))
    cx = tx + 11
    d.ellipse([cx - 13, top - 34, cx + 13, top - 8], fill=(232, 116, 24))
    d.ellipse([cx - 6, top - 26, cx + 6, top - 14], fill=(250, 205, 60))
d.text((px0 + 12, py1 - 40), "BRENT  $94+", font=font(SANS_B, 20), fill=(255, 255, 255))
# lead text on the left
lx = 78
y = kicker(d, (lx, ly + 14), "Middle East  •  Energy")
y = para(d, (lx, y + 2), "Houthis hit Saudi\nrefinery as oil\ntops $94",
         font(SERIF, 40), 590, spacing=2)
para(d, (lx, y + 8),
     "Yemen's Houthis say they struck the Ras Tanura refinery and Riyadh's\nfinancial district. Brent crude jumps past $94 a barrel on supply fears.",
     font(SANS, 15), 590, spacing=3)

# ---- six stories, 2 columns x 3 rows ------------------------------------
stories = [
    ("Strait of Hormuz", "Two tankers hit\nmines in Hormuz",
     "Two oil tankers strike naval\nmines in the strait that\ncarries a fifth of the\nworld's seaborne oil.",
     "sea"),
    ("Gaza", "Israeli strike kills\nHamas colonel",
     "Israel kills a senior Hamas\nsecurity chief in Gaza. The\nceasefire, weeks old, is\nunder growing strain.",
     "city"),
    ("Space", "BepiColombo reaches\nMercury orbit",
     "After an eight-year voyage,\nthe European-Japanese probe\nslips into orbit around\nMercury, a first.",
     "planet"),
    ("Chess", "Gukesh–Sindarov:\nGame 2 is a draw",
     "The world championship\nmatch in Geneva stays level\nafter a 20-move draw in\nthe second game.",
     "board"),
    ("Egypt", "Cairo tanker crash\nkills at least 30",
     "A fuel tanker crashes and\nbursts into flames on a\nhighway outside Cairo,\nkilling at least 30 people.",
     "fire"),
    ("Trade", "US proposes 15%\ntariff on Taiwan",
     "Washington floats tariffs of\nup to 15% on Taiwan's goods.\nTaipei shares slide as\nmarkets weigh the plan.",
     "chart"),
]

gx, gy = 60, 440
cw, chh = 442, 165
gap = 20


def draw_icon(box, kind):
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=INK, width=1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "sea":
        d.rectangle([x0, y0, x1, y1], fill=(28, 68, 110))
        d.polygon([(x0 + 60, y1 - 34), (x0 + 60, y0 + 26), (x0 + 96, y1 - 34)],
                  fill=(240, 240, 240))
        d.rectangle([x0 + 40, y1 - 40, x0 + 150, y1 - 22], fill=(18, 18, 18))
        d.ellipse([x0 + 130, y0 + 22, x0 + 156, y0 + 48], fill=(250, 205, 60))
        d.line([x0, y1 - 14, x1, y1 - 14], fill=(255, 255, 255), width=2)
    elif kind == "city":
        d.rectangle([x0, y0, x1, y1], fill=(226, 214, 190))
        for bx, bh in [(x0 + 14, 58), (x0 + 52, 78), (x0 + 94, 52), (x0 + 132, 68)]:
            d.rectangle([bx, y1 - bh, bx + 32, y1], fill=(58, 56, 52))
            for wy in range(y1 - bh + 8, y1 - 8, 14):
                d.rectangle([bx + 6, wy, bx + 12, wy + 6], fill=(250, 205, 60))
        # jagged crack down the middle of the skyline
        d.line([(x0 + 92, y0 + 8), (x0 + 84, y0 + 30), (x0 + 96, y0 + 52),
                (x0 + 86, y0 + 74), (x0 + 94, y1 - 6)], fill=RED, width=3)
    elif kind == "planet":
        d.rectangle([x0, y0, x1, y1], fill=(12, 14, 34))
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(196, 148, 96))
        d.ellipse([cx - 52, cy - 12, cx + 52, cy + 12], outline=(250, 205, 60), width=2)
        for sx, sy in [(x0 + 20, y0 + 18), (x1 - 24, y0 + 30), (x0 + 34, y1 - 20)]:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    elif kind == "board":
        for r in range(4):
            for c in range(4):
                col = (18, 18, 18) if (r + c) % 2 == 0 else (240, 240, 240)
                d.rectangle([x0 + c * 22, y0 + r * 22, x0 + (c + 1) * 22,
                             y0 + (r + 1) * 22], fill=col)
        d.rectangle([x0 + 6, y0 + 6, x0 + 82, y0 + 82], outline=INK, width=2)
        d.text((x0 + 96, y0 + 30), "♞", font=font(SANS_B, 34), fill=INK)
    elif kind == "fire":
        d.rectangle([x0, y0, x1, y1], fill=(40, 30, 24))
        for fx, fy, fr, col in [(cx - 18, cy + 6, 22, (232, 116, 24)),
                                (cx + 14, cy - 2, 18, (250, 205, 60)),
                                (cx, cy - 18, 13, (250, 240, 160))]:
            d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=col)
        d.rectangle([x0 + 16, y1 - 18, x1 - 16, y1 - 10], fill=(120, 120, 120))
    elif kind == "chart":
        d.rectangle([x0, y0, x1, y1], fill=(232, 238, 244))
        pts = [(x0 + 16, y0 + 30), (x0 + 56, y0 + 44), (x0 + 96, y0 + 40),
               (x0 + 136, y0 + 62), (x0 + 168, y0 + 78)]
        d.line(pts, fill=RED, width=4)
        d.polygon([(x0 + 168, y0 + 78), (x0 + 150, y0 + 74), (x0 + 164, y0 + 60)],
                  fill=RED)
        d.text((x0 + 12, y0 + 8), "-1,927", font=font(SANS_B, 16), fill=RED)


for i, (kick, head, body, kind) in enumerate(stories):
    col, row = i % 2, i // 2
    x = gx + col * (cw + gap)
    y = gy + row * (chh + 12)
    d.rectangle([x, y, x + cw, y + chh], outline=INK, width=1)
    draw_icon((x + 10, y + 10, x + 188, y + 98), kind)
    tx = x + 200
    yy = kicker(d, (tx, y + 12), kick)
    yy = para(d, (tx, yy + 1), head, font(SERIF, 21), cw - 212, spacing=1)
    para(d, (tx, yy + 4), body, font(SANS, 13), cw - 212, spacing=2)

# ---- footer --------------------------------------------------------------
fy = gy + 3 * chh + 2 * 12 + 10
d.line([60, fy, W - 60, fy], fill=INK, width=2)
d.text((60, fy + 8),
       "THE WORLD TODAY  •  Six stories that defined Thursday, 26 November 2026.",
       font=font(SANS_B, 16), fill=INK)
d.text((W - 60, fy + 8), "Drawn from the day's reporting",
       font=font(SANS, 13), fill=GREY, anchor="rt")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
