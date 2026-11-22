#!/usr/bin/env python3
"""Render 'The Sunday World' — Sunday 22 November 2026 in one image.

A 1024x1024 front page drawn entirely with PIL: masthead and a numbers
strip, three illustrated hero panels (asymmetric: one wide, two stacked),
six mid-tier story cards with small original scenes, a world map with
numbered markers, an 'Also on Sunday' roundup, and a date-check box that
lists the stories deliberately excluded as other days' news.

Every illustration is an original flat-style scene drawn in code below.
Run:  python3 render.py   ->  writes entry.png beside this file
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
PAPER = (246, 241, 230)
INK = (26, 24, 20)
MUTED = (96, 92, 84)
BRICK = (179, 64, 42)
TEAL = (20, 85, 90)
SAND = (227, 211, 172)
SEA = (222, 231, 224)
LINE = (150, 144, 128)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

F_MAST = ImageFont.truetype(SERIF_B, 46)
F_DATE = ImageFont.truetype(SANS_B, 19)
F_STAT_N = ImageFont.truetype(SANS_B, 30)
F_STAT_C = ImageFont.truetype(SANS, 10)
F_KICK = ImageFont.truetype(SANS_B, 11)
F_HERO_H = ImageFont.truetype(SANS_B, 17)
F_HERO_S = ImageFont.truetype(SANS, 11)
F_CREDIT = ImageFont.truetype(SANS, 9)
F_SEC = ImageFont.truetype(SANS_B, 13)
F_MID_H = ImageFont.truetype(SANS_B, 11)
F_ALSO = ImageFont.truetype(SANS, 11)
F_ALSO_B = ImageFont.truetype(SANS_B, 11)
F_DC = ImageFont.truetype(SANS, 10)
F_FOOT = ImageFont.truetype(SANS, 9)
F_MARK = ImageFont.truetype(SANS_B, 10)

MX = 22                      # page margin
CW = W - 2 * MX              # content width


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, width, step):
    for line in wrap(text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += step
    return y


# ---------------------------------------------------------------- scenes
def scene_cop31(d, x, y, w, h):
    """Summit hall at night: delegate rows, long tables, a big late clock."""
    d.rectangle([x, y, x + w, y + h], fill=(19, 44, 62))
    d.rectangle([x, y, x + w, y + int(h * 0.50)], fill=(23, 54, 74))
    for fx in (0.18, 0.5, 0.82):
        lx = x + int(w * fx)
        d.line([lx, y, lx, y + 10], fill=(240, 200, 120), width=2)
        d.ellipse([lx - 8, y + 8, lx + 8, y + 22], fill=(250, 214, 130))
    cx, cy, r = x + int(w * 0.87), y + int(h * 0.27), 19
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 242, 232), outline=(10, 10, 10), width=3)
    for a in range(12):
        ang = a * math.pi / 6
        d.ellipse([cx + int(14 * math.cos(ang)) - 1, cy + int(14 * math.sin(ang)) - 1,
                   cx + int(14 * math.cos(ang)) + 1, cy + int(14 * math.sin(ang)) + 1], fill=INK)
    d.line([cx, cy, cx + 3, cy - 12], fill=INK, width=3)
    d.line([cx, cy, cx - 9, cy + 2], fill=INK, width=4)
    skins = [(217, 180, 143), (185, 138, 94), (138, 90, 59), (232, 201, 160), (166, 116, 78)]
    suits = [(38, 44, 58), (48, 52, 66), (30, 36, 48), (56, 48, 44)]
    for ri, (fy, n, hr) in enumerate([(0.50, 7, 10), (0.65, 8, 11), (0.80, 9, 12)]):
        ry = y + int(h * fy)
        d.rectangle([x + 6, ry + hr + 2, x + w - 6, ry + hr + 7], fill=(107, 79, 53))
        for i in range(n):
            hx = x + int(w * (0.06 + 0.88 * (i + 0.5) / n))
            skin, suit = skins[(i + ri) % len(skins)], suits[(i + ri * 2) % len(suits)]
            d.pieslice([hx - hr, ry - hr, hx + hr, ry + hr], 180, 360, fill=suit)
            d.ellipse([hx - hr // 2, ry - hr - hr // 3, hx + hr // 2, ry - hr // 3 + hr // 2], fill=skin)
            d.rectangle([hx - hr + 3, ry + hr + 3, hx - hr + 12, ry + hr + 6], fill=(240, 238, 230))


def scene_sparta(d, x, y, w, h):
    """A freighter ablaze at night: flames, smoke, moon, dark sea."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 26, 42))
    for sx, sy in [(0.08, 0.14), (0.22, 0.30), (0.62, 0.10), (0.78, 0.26), (0.40, 0.18), (0.90, 0.12)]:
        px, py = x + int(w * sx), y + int(h * sy)
        d.ellipse([px, py, px + 2, py + 2], fill=(230, 235, 240))
    d.ellipse([x + w - 30, y + 7, x + w - 10, y + 27], fill=(238, 234, 214))
    d.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(18, 44, 66))
    for i in range(4):
        wy = y + int(h * (0.76 + 0.06 * i))
        d.line([x + 6 + (i % 2) * 10, wy, x + int(w * 0.5), wy], fill=(52, 92, 120), width=2)
    hx0, hy = x + int(w * 0.08), y + int(h * 0.60)
    hx1 = x + int(w * 0.90)
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 10, hy + 10), (hx0 + 6, hy + 10)], fill=(16, 18, 22))
    d.rectangle([hx0 + 6, hy - 8, hx1 - 22, hy], fill=(24, 28, 34))
    cols = [(150, 74, 60), (70, 96, 130), (120, 120, 118), (96, 120, 96)]
    seg = (hx1 - hx0 - 44) / 4
    for i in range(4):
        bx = hx0 + 10 + i * seg
        d.rectangle([bx, hy - 17, bx + seg - 2, hy - 8], fill=cols[i])
    d.rectangle([hx1 - 20, hy - 25, hx1 - 9, hy - 8], fill=(210, 208, 198))
    d.rectangle([hx1 - 18, hy - 21, hx1 - 11, hy - 17], fill=(250, 214, 130))
    for fx, fs in [(0.30, 1.0), (0.55, 0.75)]:
        bx, by = x + int(w * fx), hy - 10
        s = int(17 * fs)
        d.polygon([(bx - s // 2, by), (bx, by - s - 6), (bx + s // 2, by)], fill=(232, 106, 23))
        d.polygon([(bx - s // 4, by), (bx + 2, by - s // 2 - 3), (bx + s // 4, by)], fill=(245, 185, 33))
        for k in range(3):
            gx, gy = bx + 5 + k * 6, by - s - 9 - k * 5
            d.ellipse([gx - 5, gy - 3, gx + 5, gy + 3], fill=(120, 122, 126))
    d.line([x + int(w * 0.28), y + int(h * 0.80), x + int(w * 0.36), y + int(h * 0.80)], fill=(232, 120, 40), width=2)


def scene_hormuz(d, x, y, w, h):
    """Dusk over a strait: two headlands, a drone, radar rings, a tanker."""
    bands = [(64, 48, 84), (96, 58, 84), (150, 74, 66), (196, 108, 62)]
    bh = h // 2 // len(bands) + 1
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(38, 62, 84))
    d.polygon([(x, y + int(h * 0.52)), (x + int(w * 0.30), y + int(h * 0.44)),
               (x + int(w * 0.36), y + h // 2), (x, y + h // 2)], fill=(30, 30, 36))
    d.polygon([(x + w, y + int(h * 0.50)), (x + int(w * 0.70), y + int(h * 0.42)),
               (x + int(w * 0.64), y + h // 2), (x + w, y + h // 2)], fill=(30, 30, 36))
    tx, ty = x + int(w * 0.40), y + int(h * 0.62)
    d.polygon([(tx, ty), (tx + 46, ty), (tx + 40, ty + 6), (tx + 4, ty + 6)], fill=(14, 16, 20))
    d.rectangle([tx + 35, ty - 5, tx + 42, ty], fill=(190, 188, 178))
    for r in (8, 14, 20):
        d.ellipse([tx + 38 - r, ty - 5 - r, tx + 38 + r, ty - 5 + r], outline=(240, 220, 170))
    dx, dy = x + int(w * 0.52), y + int(h * 0.20)
    d.ellipse([dx - 8, dy - 3, dx + 8, dy + 3], fill=(16, 16, 20))
    for ax, ay in [(-11, -6), (11, -6), (-11, 6), (11, 6)]:
        d.line([dx, dy, dx + ax, dy + ay], fill=(16, 16, 20), width=2)
        d.ellipse([dx + ax - 3, dy + ay - 3, dx + ax + 3, dy + ay + 3], outline=(16, 16, 20), width=2)
    for k in range(4):
        px, py = dx - 22 + k * 6, dy + 10 + k * 5
        d.ellipse([px, py, px + 2, py + 2], fill=(250, 230, 180))


def thumb_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 226, 232))
    d.rectangle([x, y + h - 7, x + w, y + h], fill=(140, 132, 116))
    d.rectangle([x + 18, y + h - 26, x + 78, y + h - 7], fill=(120, 96, 84))
    d.rectangle([x + 84, y + h - 34, x + 94, y + h - 7], fill=(96, 78, 70))
    d.rectangle([x + 26, y + h - 40, x + 36, y + h - 26], fill=(96, 78, 70))
    for wx in range(24, 74, 12):
        d.rectangle([x + wx, y + h - 21, x + wx + 7, y + h - 15], fill=(250, 214, 130))
    fx, fy = x + 52, y + h - 28
    d.polygon([(fx - 7, fy), (fx, fy - 13), (fx + 7, fy)], fill=(232, 106, 23))
    d.polygon([(fx - 3, fy), (fx + 1, fy - 7), (fx + 3, fy)], fill=(245, 185, 33))
    for k in range(3):
        gx, gy = x + 29 + k * 4, y + 6 + k * 2
        d.ellipse([gx - 5, gy - 3, gx + 5, gy + 3], fill=(150, 150, 152))


def thumb_aid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    for bx, bh in [(6, 22), (26, 29), (96, 25), (120, 18)]:
        d.rectangle([x + bx, y + h - 7 - bh, x + bx + 16, y + h - 7], fill=(168, 156, 138))
    d.rectangle([x, y + h - 7, x + w, y + h], fill=(120, 110, 96))
    tx, ty = x + 34, y + h - 19
    d.rectangle([tx, ty, tx + 44, ty + 10], fill=(238, 236, 228))
    d.rectangle([tx + 44, ty + 3, tx + 56, ty + 10], fill=(196, 60, 44))
    d.rectangle([tx + 46, ty + 4, tx + 53, ty + 8], fill=(170, 205, 225))
    d.rectangle([tx + 17, ty + 2, tx + 25, ty + 8], fill=(196, 60, 44))
    d.rectangle([tx + 20, ty + 0, tx + 22, ty + 9], fill=(196, 60, 44))
    for wx in (tx + 10, tx + 46):
        d.ellipse([wx - 4, ty + 8, wx + 4, ty + 16], fill=(30, 30, 32))


def thumb_phone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 228))
    px, py = x + w // 2 - 12, y + 5
    d.rounded_rectangle([px, py, px + 24, py + h - 10], 5, fill=(34, 40, 48))
    d.rectangle([px + 3, py + 3, px + 21, py + h - 18], fill=(150, 196, 205))
    d.ellipse([px + 9, py + h - 16, px + 15, py + h - 10], fill=(240, 240, 235))
    for r in (10, 17, 24):
        d.arc([px + 12 - r, py + 10 - r, px + 12 + r, py + 10 + r], 200, 320, fill=(20, 85, 90), width=3)
    bx, by = x + w - 32, y + h - 24
    d.ellipse([bx, by, bx + 18, by + 18], fill=BRICK)
    d.line([bx + 4, by + 4, bx + 14, by + 14], fill=(255, 255, 255), width=3)
    d.line([bx + 14, by + 4, bx + 4, by + 14], fill=(255, 255, 255), width=3)


def thumb_sub(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 62, 92))
    for i in range(3):
        wy = y + 6 + i * 11
        d.line([x + 6 + (i % 2) * 10, wy, x + 40, wy], fill=(70, 120, 155), width=2)
    sx, sy = x + 28, y + h // 2 + 2
    d.ellipse([sx, sy - 8, sx + 92, sy + 8], fill=(16, 20, 26))
    d.rectangle([sx + 40, sy - 15, sx + 56, sy - 7], fill=(16, 20, 26))
    d.line([sx + 48, sy - 15, sx + 48, sy - 21], fill=(16, 20, 26), width=3)
    d.polygon([(sx + 2, sy), (sx - 7, sy - 7), (sx - 7, sy + 7)], fill=(16, 20, 26))
    for k in range(4):
        d.ellipse([sx + 15 + k * 16, sy - 2, sx + 19 + k * 16, sy + 2], fill=(250, 214, 130))


def thumb_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 226, 178))
    d.ellipse([x + w - 28, y + 4, x + w - 12, y + 20], fill=(250, 214, 90))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 190, 128))
    d.rectangle([x + 28, y + h - 12, x + 92, y + h - 3], fill=(226, 208, 160))
    for k in range(3):
        d.rectangle([x + 38 + k * 6, y + h - 26, x + 40 + k * 6, y + h - 11], fill=(240, 238, 228))
    d.rectangle([x + 36, y + h - 27, x + 54, y + h - 24], fill=(240, 238, 228))
    d.polygon([(x + 92, y + h - 26), (x + 100, y + h - 28), (x + 85, y + h - 7), (x + 79, y + h - 9)], fill=(150, 104, 60))
    d.ellipse([x + 112, y + h - 23, x + 120, y + h - 15], fill=(178, 34, 44))
    for k in range(3):
        d.ellipse([x + 100 + k * 5, y + h - 19 + k, x + 102 + k * 5, y + h - 17 + k], fill=(120, 120, 118))


def thumb_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(208, 220, 234))
    cx = x + w // 2
    d.rectangle([cx - 50, y + h - 10, cx + 50, y + h - 5], fill=(240, 238, 230))
    for k in range(6):
        d.rectangle([cx - 42 + k * 16, y + h - 22, cx - 38 + k * 16, y + h - 10], fill=(240, 238, 230))
    d.rectangle([cx - 50, y + h - 25, cx + 50, y + h - 21], fill=(226, 224, 214))
    d.pieslice([cx - 24, y + 3, cx + 24, y + 33], 180, 360, fill=(110, 130, 160))
    d.rectangle([cx - 24, y + 18, cx + 24, y + 21], fill=(226, 224, 214))
    d.line([cx, y + 3, cx, y - 1], fill=(90, 105, 130), width=2)


THUMBS = [thumb_factory, thumb_aid, thumb_phone, thumb_sub, thumb_cricket, thumb_capitol]

# ------------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 62), (-76, 58),
     (-80, 50), (-70, 45), (-75, 38), (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-94, 29),
     (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-86, 12), (-83, 9), (-79, 9), (-86, 13),
     (-92, 15), (-97, 16), (-102, 18), (-105, 22), (-110, 24), (-114, 29), (-120, 34),
     (-124, 40), (-124, 47), (-130, 55), (-145, 60), (-158, 58), (-165, 60)],
    [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 82), (-55, 80), (-58, 72), (-52, 64)],
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8), (-39, -13),
     (-40, -20), (-48, -26), (-52, -32), (-58, -38), (-62, -41), (-65, -45), (-67, -50),
     (-68, -54), (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20), (-75, -15),
     (-79, -8), (-80, -4), (-77, 1), (-77, 4)],
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (38, 22), (40, 15), (43, 12),
     (48, 11), (51, 10), (48, 4), (42, -2), (40, -10), (38, -18), (36, -22), (33, -26),
     (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10), (9, -1), (9, 4),
     (4, 6), (-2, 5), (-8, 4), (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-15, 25),
     (-13, 28), (-10, 31)],
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (-2, 50), (3, 53), (5, 58), (8, 55), (14, 54),
     (18, 56), (24, 58), (21, 60), (28, 60), (30, 62), (40, 64), (55, 68), (75, 70),
     (100, 72), (130, 72), (160, 70), (178, 68), (178, 65), (162, 62), (158, 55), (150, 50),
     (142, 50), (140, 45), (135, 40), (130, 38), (127, 40), (122, 38), (120, 32), (115, 28),
     (110, 22), (108, 15), (105, 8), (103, 5), (100, 8), (98, 12), (95, 16), (92, 16),
     (90, 22), (88, 22), (85, 20), (80, 15), (77, 8), (75, 12), (72, 18), (68, 22),
     (65, 25), (60, 25), (55, 26), (50, 29), (48, 30), (50, 25), (55, 22), (58, 20),
     (55, 17), (52, 15), (48, 14), (44, 12), (42, 15), (39, 20), (36, 24), (34, 28),
     (33, 30), (30, 36), (27, 37), (23, 36), (20, 38), (15, 38), (12, 38), (10, 37),
     (3, 37), (-2, 37), (-6, 36), (-9, 37)],
    [(109, 1), (113, 3), (117, 5), (119, 2), (116, -2), (112, -3), (109, -1)],
    [(113, -22), (122, -17), (130, -12), (136, -12), (141, -13), (142, -11), (146, -15),
     (150, -22), (153, -27), (150, -32), (147, -38), (141, -38), (136, -35), (133, -32),
     (129, -32), (124, -33), (118, -35), (115, -33), (113, -26)],
    [(167, -45), (170, -43), (172, -42), (174, -40), (175, -37), (176, -38), (174, -41),
     (172, -43), (169, -46)],
]
ISLANDS = [(100, -2), (104, -3), (110, -3), (115, -1), (120, -2), (125, -1), (131, -3),
           (138, -3), (95, 5), (80, 7), (121, 14), (122, 18), (130, 31), (133, 34),
           (137, 35), (140, 36), (141, 40), (142, 43), (-19, 65), (-17, 66)]

MARKERS = [  # (number, lon, lat, badge offset dx, dy)
    (1, 30.7, 36.9, 0, 0), (2, 27.0, 59.8, 0, 0), (3, 56.3, 26.6, 0, 0),
    (4, 106.3, -6.3, 0, 0), (5, 34.3, 31.4, -17, 13), (6, 116.4, 39.9, 0, 0),
    (7, 149.1, -35.3, 0, 0), (8, 174.8, -41.3, 0, 0), (9, -77.0, 38.9, 0, 0),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    def px(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)
    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=SAND, outline=(178, 160, 116))
    for lon, lat in ISLANDS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=SAND, outline=(178, 160, 116))
    for num, lon, lat, dx, dy in MARKERS:
        tx, ty = px(lon, lat)
        bx, by = tx + dx, ty + dy
        if dx or dy:
            d.line([tx, ty, bx, by], fill=BRICK, width=1)
            d.ellipse([tx - 2.5, ty - 2.5, tx + 2.5, ty + 2.5], fill=BRICK)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=BRICK, outline=(255, 250, 240), width=2)
        t = str(num)
        d.text((bx - F_MARK.getlength(t) / 2, by - 6), t, font=F_MARK, fill=(255, 250, 240))


# ---------------------------------------------------------------- content
STATS = [
    ("0", "deals agreed at COP31 as the Sunday plenary convenes"),
    ("2", "US drones the IRGC says it downed over Hormuz"),
    ("36", "workers missing after the Banten factory fire"),
    ("629–6", "India's record Test total in New Zealand"),
    ("10%", "Trump's proposed cap on credit-card interest"),
]

HERO_WIDE = dict(
    kicker="1 · ANTALYA, TÜRKIYE — CLIMATE",
    head="COP31 deadlocked into overtime: no deal as the summit runs on",
    summary=("A second day past the deadline, the presidency tables a new package for a "
             "Sunday plenary — its draft stripped of fossil fuels and the $120bn "
             "adaptation fund. The EU warns: a good deal, or none."),
    credit="Reuters")
HERO_R1 = dict(
    kicker="2 · GULF OF FINLAND — WAR AT SEA",
    head="Sparta II ablaze after drone strike",
    summary=("Hit by two drones in neutral waters; crew evacuated as it drifted "
             "ablaze into Finnish waters."),
    credit="Reuters")
HERO_R2 = dict(
    kicker="3 · STRAIT OF HORMUZ — CONFLICT",
    head="Tehran says it downed two US drones over the strait",
    summary=("IRGC claims an MQ-9 and an MQ-1 — its 58th and 19th — and "
             "released footage; no US reply."),
    credit="Al Jazeera")

MIDS = [
    ("4 · CIKANDE, INDONESIA", "36 missing in Banten candy-factory fire", "Reuters"),
    ("5 · GAZA CITY", "Strike kills 3 in Gaza food-aid vehicle", "Reuters · AFP"),
    ("6 · BEIJING", "China hits back at US phone-access ban", "Reuters"),
    ("7 · CANBERRA", "Australia scolds US over AUKUS report", "Reuters"),
    ("8 · WELLINGTON", "Pant ton lifts India to record 629-6", "Reuters"),
    ("9 · WASHINGTON", "Senate Democrats face a leadership test", "AP"),
]

ALSO = [
    "Bahrain: Iranian strike sets a civilian plant ablaze (Reuters)",
    "Two tankers hit by unidentified projectiles off Oman (UKMTO)",
    "Iran says a tanker struck a naval mine near Khasab (Reports)",
    "Zelenskyy ready for direct Putin talks at Miami G20 (Reuters)",
    "Spain extends bank levy to 2027, €1.4bn for housing (Reuters)",
    "Israel: Eisenkot's party opens talks with Likud (Newswire)",
    "France to seek UN action over Myanmar's ICJ defiance (Reuters)",
    "Bolsonaro remains in intensive care in Brasília (Reuters)",
    "Nepal PM Shah heads to India on first trip (Reports)",
    "Trump vows to work with Democrats to cap card interest (AP)",
    "Secret Hegseth memo curbs US–Canada defence ties (WaPo)",
    "Man convicted of arson over LA's Palisades fire (Reports)",
    "Sudan's RSF-led alliance claims Bau district (Nile Intel)",
    "Ghana's 'Heritage Series' notes honour Nkrumah, Annan (C54)",
    "Nvidia board refuses to reinstate Huang as CEO (WSJ)",
    "ECB succession race: Hernández de Cos vs Knot (AP)",
    "Oil rises on Gulf fears before Thanksgiving (Markets)",
    "US releases declassified UFO footage (Reports)",
    "Princess Kate tells her cancer story in 'Heal' (Reports)",
    "Depardieu, Houellebecq face misconduct probe (Reports)",
    "Alcaraz meets Zverev for ATP Finals title, Turin (BBC)",
    "Leaders Arsenal held 2-2 at Newcastle (Reuters)",
    "France set up rugby final vs Springboks (BBC)",
    "MacKinnon out 12 weeks; Bedard faces surgery (Reuters)",
]

DATE_CHECK = ("Left out as other days' news: the Guasave capture of 'El Chapo Isidro' and the "
              "Pannun-plot sentencing (both Fri 20 Nov), Bihar's Nitish Setu opening and the "
              "Basra power-station fire (both Sat 21 Nov), Norway's oil ruling (13 Nov). "
              "Not yet known: a final COP31 text, and the Las Vegas Grand Prix result.")


def hero_text(d, x, y, w, hero):
    d.text((x, y), hero["kicker"], font=F_KICK, fill=BRICK)
    y += 15
    y = text_block(d, x, y, hero["head"], F_HERO_H, INK, w, 19)
    y = text_block(d, x, y, hero["summary"], F_HERO_S, (56, 54, 50), w, 14)
    d.text((x, y + 1), "Source: " + hero["credit"], font=F_CREDIT, fill=MUTED)
    return y + 12


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    y = 10
    d.line([MX, y, W - MX, y], fill=INK, width=3)
    y += 5
    name = "THE SUNDAY WORLD"
    d.text(((W - F_MAST.getlength(name)) / 2, y), name, font=F_MAST, fill=INK)
    y += 56
    date = "SUNDAY · 22 NOVEMBER 2026"
    d.text(((W - F_DATE.getlength(date)) / 2, y), date, font=F_DATE, fill=BRICK)
    y += 25
    d.line([MX, y, W - MX, y], fill=INK, width=2)

    # Numbers strip
    y += 8
    sw = CW // 5
    for i, (num, cap) in enumerate(STATS):
        sx = MX + i * sw
        if i:
            d.line([sx - 8, y + 2, sx - 8, y + 40], fill=LINE, width=1)
        d.text((sx, y), num, font=F_STAT_N, fill=TEAL)
        text_block(d, sx, y + 36, cap, F_STAT_C, MUTED, sw - 16, 12)
    y += 64
    d.line([MX, y, W - MX, y], fill=LINE, width=1)

    # Heroes: wide COP31 panel left; Sparta II and Hormuz stacked right
    y += 10
    hero_top = y
    lw = 548
    scene_cop31(d, MX, hero_top, lw, 100)
    hero_text(d, MX, hero_top + 106, lw, HERO_WIDE)
    rx = MX + lw + 16
    rw = W - MX - rx
    scene_sparta(d, rx, hero_top, 128, 104)
    hero_text(d, rx + 138, hero_top + 2, rw - 138, HERO_R1)
    y2 = hero_top + 112
    d.line([rx, y2, W - MX, y2], fill=LINE, width=1)
    scene_hormuz(d, rx, y2 + 10, 128, 104)
    hero_text(d, rx + 138, y2 + 12, rw - 138, HERO_R2)
    y = hero_top + 224
    d.line([MX, y, W - MX, y], fill=INK, width=2)

    # Mid-tier cards
    y += 8
    d.text((MX, y), "SIX MORE OF THE DAY'S STORIES", font=F_SEC, fill=TEAL)
    y += 19
    cw6 = (CW - 5 * 10) // 6
    card_bottom = y
    for i, (kick, head, credit) in enumerate(MIDS):
        cx = MX + i * (cw6 + 10)
        THUMBS[i](d, cx, y, cw6, 40)
        ty = y + 44
        d.text((cx, ty), kick, font=F_CREDIT, fill=BRICK)
        ty += 11
        ty = text_block(d, cx, ty, head, F_MID_H, INK, cw6, 13.5)
        d.text((cx, ty + 1), credit, font=F_CREDIT, fill=MUTED)
        card_bottom = max(card_bottom, ty + 12)
    y = card_bottom + 4
    d.line([MX, y, W - MX, y], fill=LINE, width=1)

    # Bottom: ALSO roundup (left, two columns) + map (right)
    y += 8
    d.text((MX, y), "ALSO ON SUNDAY — 24 MORE STORIES", font=F_SEC, fill=TEAL)
    map_x = MX + 650
    d.text((map_x, y), "WHERE IT HAPPENED", font=F_SEC, fill=TEAL)
    y += 19
    half = (len(ALSO) + 1) // 2
    also_w = 310
    also_bottom = y
    for c in range(2):
        cx = MX + c * (also_w + 14)
        cy = y
        for j, item in enumerate(ALSO[c * half:(c + 1) * half], start=c * half + 10):
            d.text((cx, cy), f"{j}.", font=F_ALSO_B, fill=BRICK)
            cy = text_block(d, cx + 22, cy, item, F_ALSO, (40, 38, 34), also_w - 22, 13.5)
            cy += 4
        also_bottom = max(also_bottom, cy)
    draw_map(d, map_x, y, W - MX - map_x, 230)
    text_block(d, map_x, y + 236,
               "Red markers locate stories 1–9: Antalya, the Gulf of Finland, Hormuz, "
               "Cikande, Gaza City, Beijing, Canberra, Wellington and Washington.",
               F_CREDIT, MUTED, W - MX - map_x, 12)
    y = max(also_bottom, y + 272) + 6
    d.line([MX, y, W - MX, y], fill=LINE, width=1)

    # Date check box + footer
    y += 7
    d.rectangle([MX, y, W - MX, y + 46], outline=BRICK, width=2)
    d.text((MX + 8, y + 5), "DATE CHECK", font=F_KICK, fill=BRICK)
    text_block(d, MX + 92, y + 4, DATE_CHECK, F_DC, (56, 54, 50), CW - 104, 12.5)
    y += 52
    foot = ("Every story above happened, or was first reported, on Sunday 22 November 2026; "
            "officials' claims are attributed. 33 stories — sources named beside each one. "
            "All illustrations are original drawings.")
    d.text(((W - F_FOOT.getlength(foot)) / 2, y), foot, font=F_FOOT, fill=MUTED)
    print("page ends at y =", y + 10)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
