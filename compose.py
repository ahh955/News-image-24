#!/usr/bin/env python3
"""Build the news-image-20261124 front page: one PNG summing up
Tuesday 24 November 2026. Deterministic: same inputs, same bytes out.

Layout (1024 x 1024, cream newspaper paper):
  masthead date -> red standfirst -> stat strip -> 3 photo leads ->
  10 photo features -> world map + ALSO ON list -> DATE CHECK box.
Panel photos are original generated images in panels/; the map is
drawn from rough continent outlines below.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 12
INNER = W - 2 * MARGIN  # 1000

PAPER = (251, 244, 228)
INK = (18, 18, 18)
RED = (178, 24, 24)
DARKRED = (140, 18, 18)
GREY = (90, 90, 90)
SEA = (198, 224, 238)
LAND = (232, 214, 170)
LAND_EDGE = (170, 150, 110)
CHIP_NAVY = (30, 50, 110)
CHIP_TEAL = (20, 110, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def photo_cover(path, tw, th):
    """Open a panel photo, centre-crop it to fill tw x th exactly."""
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def badge(draw, cx, cy, num, r=9):
    """Red circle with a white story number."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    fnt = font(SANS_B, 11)
    txt = str(num)
    tw = draw.textlength(txt, font=fnt)
    draw.text((cx - tw / 2, cy - r + 1), txt, font=fnt, fill=(255, 255, 255))


def chip(draw, x, y, label, colour):
    """Small coloured tag overlaid on a photo, top-left."""
    fnt = font(SANS_B, 9)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 12
    h = 17
    draw.rectangle([x, y, x + w, y + h], fill=colour)
    draw.text((x + 6, y + 3), label, font=fnt, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories

LEADS = [
    {
        "num": 1, "img": "p01.jpg", "tag": "ULLEUNG · AIR SCARE",
        "chip": CHIP_NAVY,
        "head": "Russian jets breach Korean skies",
        "body": ("Seoul sounds an evacuation alert for Ulleung Island after "
                 "warplanes enter the air defence zone without notice. "
                 "The alert is lifted after 3 minutes. — Reuters"),
    },
    {
        "num": 2, "img": "p02.jpg", "tag": "HORMUZ · WAR",
        "chip": RED,
        "head": "Three tankers burn in Hormuz",
        "body": ("Iran's IRGC says three oil tankers hit naval mines and "
                 "caught fire in the strait overnight. The claims could not "
                 "be independently confirmed. — Press TV"),
    },
    {
        "num": 3, "img": "p03.jpg", "tag": "ASIA · MARKETS",
        "chip": CHIP_TEAL,
        "head": "Asia's markets roar back",
        "body": ("Nikkei +2.6%, Kospi +4%, SoftBank +15% as Wall Street's "
                 "best day since April lifts the region. — Reuters"),
    },
]

FEATURES = [
    {"num": 4, "img": "p04.jpg", "tag": "PYONGYANG · DIPLOMACY",
     "head": "Kim mulls shutting Swiss office",
     "body": ("North Korea threatens to close Switzerland's Pyongyang office "
              "over sanctions on a camp. — KCNA")},
    {"num": 5, "img": "p05.jpg", "tag": "WEST BANK · WAR",
     "head": "Raids at dawn in West Bank",
     "body": ("Israeli forces raid several towns in the early hours of "
              "Tuesday; troops open fire on eastern Gaza City. — MEE")},
    {"num": 6, "img": "p06.jpg", "tag": "ISRAEL · MILITARY",
     "head": "Army suicides hit 16-year high",
     "body": ("23 serving personnel have died by suicide this year, the "
              "highest number since 2010. — MEE")},
    {"num": 7, "img": "p07.jpg", "tag": "PRINCETON · US",
     "head": "Student 'overstayed visa in 2016'",
     "body": ("US says a detained Chinese PhD student at Princeton "
              "overstayed her authorised stay a decade ago. — SCMP")},
    {"num": 8, "img": "p08.jpg", "tag": "SPACE · WAR",
     "head": "Nuclear weapon 'may launch next month'",
     "body": ("Allies warn a Russian space weapon could destroy thousands "
              "of satellites. — Japan Times")},
    {"num": 9, "img": "p09.jpg", "tag": "BERLIN · POLITICS",
     "head": "Germans refuse to pick a side",
     "body": ("Vast majority want neutrality between the US and China, "
              "Berlin Pulse survey finds. — SCMP")},
    {"num": 10, "img": "p10.jpg", "tag": "INDONESIA · FOOD",
     "head": "12m hectares to become farms",
     "body": ("Jakarta plans to turn degraded land into food and biofuel "
              "farms; experts warn of the cost. — CNA")},
    {"num": 11, "img": "p11.jpg", "tag": "INDIA · GAMES",
     "head": "GTA VI fever grips India",
     "body": ("Gaming cafes packed and offices declare holidays as launch "
              "mania sweeps the country. — CNA")},
    {"num": 12, "img": "p12.jpg", "tag": "GOLF · SPORT",
     "head": "Three Koreans win LPGA cards",
     "body": ("Three of South Korea's best earn LPGA Tour cards through "
              "the qualifying tournament. — Yonhap")},
    {"num": 13, "img": "p13.jpg", "tag": "SEOUL · ECONOMY",
     "head": "Shoppers lose heart again",
     "body": ("Consumer sentiment falls for a second straight month on the "
              "stock correction and high loan rates. — Yonhap")},
]

ALSO = [
    ("14", "Seoul", "Election official arrested over forged vote-count sheet.",
     "Yonhap"),
    ("15", "Mumbai", "NSE and BSE shut for Guru Nanak Jayanti.",
     "Upstox"),
    ("16", "Asia", "Currencies steady, may strengthen on risk-on mood.",
     "WSJ"),
    ("17", "Seoul", "Crypto rulebook due today as FSC outlines Digital Asset Act.",
     "CoinDesk"),
    ("18", "Glasgow", "Rangers edge Motherwell 2-1 with a late winner at Fir Park.",
     "Archyworldys"),
]

STATS = [
    ("3 MIN", "Ulleung alert lifted in 3 min"),
    ("3", "tankers IRGC says hit mines"),
    ("+4%", "Kospi jumps on Tuesday"),
    ("+15%", "SoftBank surges before results"),
    ("23", "Israeli army suicides this year"),
    ("12M", "hectares Indonesia plans to farm"),
]

# Rough continent outlines, as (lon, lat) points. Schematic, drawn in code.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 62), (-60, 52), (-65, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-84, 30), (-90, 29), (-97, 26), (-97, 22),
     (-105, 20), (-110, 23), (-114, 29), (-120, 34), (-124, 42), (-124, 48),
     (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 76), (-40, 78),
     (-55, 77), (-58, 70), (-52, 64)],
    # South America
    [(-78, 8), (-72, 11), (-62, 10), (-52, 5), (-44, -3), (-35, -8),
     (-38, -15), (-40, -22), (-48, -28), (-52, -33), (-58, -38), (-62, -41),
     (-65, -45), (-68, -50), (-70, -54), (-72, -50), (-73, -42), (-72, -30),
     (-70, -20), (-75, -15), (-80, -6), (-81, 0), (-80, 6)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 53), (3, 55), (8, 57),
     (10, 59), (5, 60), (5, 62), (10, 64), (14, 67), (18, 69), (25, 71),
     (30, 70), (32, 68), (28, 66), (30, 62), (28, 60), (24, 58), (21, 55),
     (19, 54), (15, 54), (12, 54), (8, 54), (5, 53), (3, 51), (0, 50),
     (-2, 47), (-1, 44), (-2, 37), (-6, 36), (-9, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-2, 50)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (34, 28), (35, 22), (37, 18), (40, 15), (43, 12), (48, 11), (51, 10),
     (46, 5), (41, 0), (40, -5), (39, -12), (36, -18), (33, -25), (28, -32),
     (20, -35), (17, -32), (15, -27), (12, -18), (13, -12), (9, -1), (9, 4),
     (6, 5), (-2, 5), (-8, 5), (-13, 8), (-17, 15), (-16, 20), (-14, 25),
     (-10, 31)],
    # Asia (mainland, rough)
    [(28, 70), (35, 68), (45, 68), (55, 69), (65, 69), (75, 72), (85, 73),
     (95, 76), (105, 77), (115, 73), (125, 71), (135, 72), (142, 70),
     (142, 65), (140, 60), (135, 55), (130, 50), (127, 45), (122, 40),
     (120, 35), (118, 30), (115, 25), (110, 20), (108, 15), (105, 10),
     (103, 8), (100, 10), (98, 15), (95, 18), (92, 21), (90, 22), (88, 22),
     (85, 20), (82, 18), (80, 15), (78, 12), (77, 8), (75, 10), (72, 15),
     (70, 20), (68, 22), (66, 25), (62, 25), (58, 27), (54, 28), (52, 26),
     (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (32, 36), (30, 40),
     (28, 45), (30, 50), (32, 55), (30, 60), (28, 65)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (142, 43),
     (144, 44), (142, 42), (140, 38), (138, 35), (134, 33), (131, 31)],
    # Sumatra
    [(95, 5), (100, 0), (105, -5), (106, -6), (102, -2), (98, 2)],
    # Borneo
    [(109, 1), (113, 4), (117, 2), (118, -2), (115, -4), (110, -3)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -8),
     (142, -7), (136, -5)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (151, -24), (146, -19), (142, -15),
     (142, -11), (140, -17), (136, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (117, -20)],
    # New Zealand
    [(167, -45), (170, -42), (173, -39), (175, -37), (178, -38), (175, -40),
     (172, -43), (168, -46)],
]

# Story number -> (lon, lat) for the map pin. A few are nudged so
# crowded pins (Korea, the Levant) stay readable.
PINS = {
    1: (129.0, 39.5), 2: (56.5, 26.5), 3: (141.0, 36.5), 4: (119.0, 44.0),
    5: (32.0, 34.5), 6: (39.5, 27.0), 7: (-74.7, 40.35), 8: (37.6, 55.8),
    9: (13.4, 52.5), 10: (106.8, -6.2), 11: (72.9, 19.1), 12: (118.0, 31.0),
    13: (135.0, 29.0),
}

DATE_CHECK = (
    "Every story here happened, or was first reported, on Tuesday 24 November "
    "2026. LEFT OUT \u00b7 23 NOV: NATO emergency meeting \u00b7 Grok lawsuits "
    "filed \u00b7 Oxfam Gaza report \u00b7 Saryu-Kamala flag-off \u00b7 COP31 "
    "collapse \u00b7 22 NOV: Dymer drone strike \u00b7 17 NOV: Japan oil "
    "task force."
)

FOOTER = (
    "Claims are attributed, not stated as fact \u00b7 Pictures: original "
    "generated images; map: drawn in code \u00b7 Sources: Reuters, Yonhap, "
    "Press TV, KCNA, MEE, SCMP, Japan Times, CNA, WSJ, CoinDesk, Upstox "
    "\u00b7 2026-11-24"
)


# ---------------------------------------------------------------- sections

def masthead(draw):
    draw.text((MARGIN, 8), "THE WORLD IN ONE DAY",
              font=font(SANS_B, 13), fill=RED)
    right = "18 STORIES \u00b7 ALL FROM THIS ONE DAY"
    fnt = font(SANS_B, 11)
    draw.text((W - MARGIN - draw.textlength(right, font=fnt), 10), right,
              font=fnt, fill=INK)
    draw.line([(MARGIN, 27), (W - MARGIN, 27)], fill=INK, width=2)
    draw.text((MARGIN, 30), "Tuesday 24 November 2026",
              font=font(SERIF_B, 52), fill=INK)
    draw.text((MARGIN, 90),
              "Russian jets breach Korean skies \u00b7 Three tankers burn in "
              "Hormuz \u00b7 Asia's markets roar back",
              font=font(SERIF, 15), fill=DARKRED)
    draw.line([(MARGIN, 110), (W - MARGIN, 110)], fill=INK, width=1)


def stats(draw):
    y0, y1 = 114, 150
    col_w = INNER / 6
    for i, (num, cap) in enumerate(STATS):
        x = MARGIN + i * col_w
        if i:
            draw.line([(x - 5, y0 + 2), (x - 5, y1 - 2)], fill=GREY, width=1)
        draw.text((x, y0), num, font=font(SANS_B, 25), fill=RED)
        lines = wrap(draw, cap, font(SANS, 9), col_w - 12)
        draw_lines(draw, x + 1, y0 + 27, lines[:2], font(SANS, 9), INK, 11)
    draw.line([(MARGIN, 154), (W - MARGIN, 154)], fill=INK, width=1)


def lead_panel(img, draw, x, y, w, h, story):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    photo_h = 126
    img.paste(photo_cover(os.path.join(PANELS, story["img"]), w - 2,
                          photo_h), (x + 1, y + 1))
    chip(draw, x + 6, y + 6, story["tag"], story["chip"])
    tx = x + 8
    ty = y + photo_h + 12
    badge(draw, tx + 9, ty + 8, story["num"])
    draw.text((tx + 24, ty + 1), story["tag"], font=font(SANS_B, 10),
              fill=RED)
    head_lines = wrap(draw, story["head"], font(SERIF_B, 19), w - 16)
    hy = draw_lines(draw, tx, ty + 20, head_lines[:2], font(SERIF_B, 19),
                    INK, 21)
    body_lines = wrap(draw, story["body"], font(SANS, 10.5), w - 16)
    draw_lines(draw, tx, hy + 4, body_lines[:3], font(SANS, 10.5), INK, 12)


def feature_panel(img, draw, x, y, w, h, story):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    photo_h = 58
    img.paste(photo_cover(os.path.join(PANELS, story["img"]), w - 2,
                          photo_h), (x + 1, y + 1))
    tx = x + 6
    ty = y + photo_h + 9
    badge(draw, tx + 8, ty + 7, story["num"], r=8)
    draw.text((tx + 20, ty + 1), story["tag"], font=font(SANS_B, 8.5),
              fill=RED)
    head_lines = wrap(draw, story["head"], font(SERIF_B, 13), w - 12)
    hy = draw_lines(draw, tx, ty + 17, head_lines[:2], font(SERIF_B, 13),
                    INK, 15)
    body_lines = wrap(draw, story["body"], font(SANS, 9), w - 12)
    draw_lines(draw, tx, hy + 2, body_lines[:3], font(SANS, 9), INK, 10.5)


def world_map(img, draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)
    lon0, lon1, lat0, lat1 = -170, 190, -60, 85

    def project(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat1 - lat) / (lat1 - lat0) * h
        return (px, py)

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for num, (lon, lat) in sorted(PINS.items()):
        px, py = project(lon, lat)
        r = 5
        draw.ellipse([px - r - 1, py - r - 1, px + r + 1, py + r + 1],
                     fill=(255, 255, 255))
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED)
        fnt = font(SANS_B, 7)
        txt = str(num)
        tw = draw.textlength(txt, font=fnt)
        draw.text((px - tw / 2, py - 4), txt, font=fnt, fill=(255, 255, 255))


def also_on(draw, x, y, w, h):
    fnt_num = font(SANS_B, 11)
    fnt_txt = font(SANS, 11)
    row_h = h / len(ALSO)
    for i, (num, place, text, src) in enumerate(ALSO):
        ry = y + i * row_h
        draw.text((x, ry), num, font=fnt_num, fill=RED)
        full = "%s \u2014 %s %s" % (place, text, src)
        lines = wrap(draw, full, fnt_txt, w - 26)
        draw_lines(draw, x + 26, ry, lines[:2], fnt_txt, INK, 14)


def date_check(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    label = "DATE CHECK"
    fnt_lab = font(SANS_B, 11)
    fnt_txt = font(SANS, 10.5)
    lx = x + 8
    draw.text((lx, y + 7), label, font=fnt_lab, fill=RED)
    lw = draw.textlength(label, font=fnt_lab)
    lines = wrap(draw, DATE_CHECK, fnt_txt, w - int(lw) - 24)
    draw_lines(draw, lx + int(lw) + 10, y + 6, lines, fnt_txt, INK, 14)


# ---------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    masthead(draw)
    stats(draw)

    # Three lead panels.
    lead_y, lead_h = 160, 242
    gap = 8
    lw = (INNER - 2 * gap) // 3
    for i, story in enumerate(LEADS):
        x = MARGIN + i * (lw + gap)
        lead_panel(img, draw, x, lead_y, lw, lead_h, story)

    # Feature grid: 5 columns x 2 rows.
    feat_y, feat_h, feat_gap = 410, 148, 8
    bounds = [MARGIN + round(i * INNER / 5) for i in range(6)]
    for row in range(2):
        for col in range(5):
            story = FEATURES[row * 5 + col]
            x = bounds[col]
            w = bounds[col + 1] - bounds[col] - (feat_gap if col < 4 else 0)
            feature_panel(img, draw, x, feat_y + row * (feat_h + feat_gap),
                          w, feat_h, story)

    # Bottom section: map on the left, ALSO ON list on the right.
    sec_y = 722
    map_w = 430
    list_x = MARGIN + map_w + 14
    list_w = W - MARGIN - list_x
    draw.text((MARGIN, sec_y), "WHERE IT HAPPENED",
              font=font(SANS_B, 12), fill=RED)
    draw.text((MARGIN + 160, sec_y + 1), "numbers match the stories",
              font=font(SANS, 9), fill=GREY)
    draw.text((list_x, sec_y), "ALSO ON TUESDAY 24 NOVEMBER 2026",
              font=font(SANS_B, 12), fill=RED)
    map_h = 180
    world_map(img, draw, MARGIN, sec_y + 20, map_w, map_h)
    also_on(draw, list_x, sec_y + 22, list_w, map_h - 4)
    draw.text((MARGIN, sec_y + 20 + map_h + 4),
              "Pins mark stories 1\u201313; 3 is the markets story.",
              font=font(SANS, 9), fill=GREY)

    # DATE CHECK box + footer.
    date_check(draw, MARGIN, 940, INNER, 50)
    fnt_ft = font(SANS, 8.5)
    fw = draw.textlength(FOOTER, font=fnt_ft)
    draw.text(((W - fw) / 2, 998), FOOTER, font=fnt_ft, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
