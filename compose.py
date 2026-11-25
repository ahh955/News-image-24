#!/usr/bin/env python3
"""Compose news-image-20261124 v2: one-day newspaper front page for
Tuesday 24 November 2026. Written fresh for the v2 rebuild.
Reads 3 generated lead photos from panels/, draws everything else
(masthead, stats, map, lists) in code. Deterministic: no randomness,
no timestamps, fixed layout."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (179, 35, 27)
NAVY = (31, 58, 95)
TEAL = (15, 107, 92)
GREY = (110, 105, 95)
SEA = (207, 227, 238)
LAND = (232, 220, 192)
LAND_EDGE = (154, 143, 120)
DARK = (60, 58, 52)

FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = os.path.join(FDIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width, draw):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, fnt, width, draw, max_lines):
    """Wrap text; warn (not crash) if it needs more than max_lines."""
    lines = wrap(text, fnt, width, draw)
    if len(lines) > max_lines:
        print(f"WARN: text needs {len(lines)} lines (max {max_lines}): {text[:70]!r}")
    return lines[:max_lines]


def check_one_line(text, fnt, width, draw, tag):
    """Assert a string fits on one line; print warning with overflow."""
    w = draw.textlength(text, font=fnt)
    if w > width:
        print(f"WARN [{tag}]: one-liner {w:.0f}px > {width}px: {text[:80]!r}")
    return w <= width


def crop_fill(img, w, h):
    """Center-crop image to fill w x h exactly."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return img.crop((x, y, x + w, y + h))


# ---------------------------------------------------------------- stories
# label: REPORTED = happened / first reported 24 Nov as named sources report
#        it. CLAIM = one side's claim, not independently verified.
LEADS = [
    dict(n=1, kicker="ULLEUNG \u00b7 AIR SCARE", chip=NAVY,
         headline="Russian jets breach Korean air zone",
         deck=("Seoul alerts Ulleung Island as Russian jets enter the air "
               "defence zone."),
         source="Reuters", label="REPORTED", lon=130.9, lat=37.5,
         photo="lead1-jets"),
    dict(n=2, kicker="HORMUZ \u00b7 WAR", chip=RED,
         headline="Tankers burn in Hormuz",
         deck=("Iran's IRGC says tankers hit mines in the strait, a fourth "
               "reported later. US Central Command rejects the claim."),
         source="Press TV / Reuters", label="CLAIM", lon=56.5, lat=26.5,
         photo="lead2-hormuz"),
    dict(n=3, kicker="ASIA \u00b7 MARKETS", chip=TEAL,
         headline="Asia's markets roar back",
         deck=("Nikkei +3.9%, Kospi +6.3% to a record 5,006, Taiwan +9.1% "
               "as Huang returns to Nvidia."),
         source="WSJ", label="REPORTED", lon=139.7, lat=35.7,
         photo="lead3-markets"),
]

ALSO = [
    dict(n=4, kicker="PYONGYANG \u00b7 DIPLOMACY",
         headline="Kim mulls shutting Swiss office",
         deck=("Kim Yo Jong says the North may close its Swiss office over "
                "camp sanctions."),
         source="KCNA", label="REPORTED", lon=7.4, lat=46.9),
    dict(n=5, kicker="GAZA \u00b7 WAR",
         headline="Strike kills Hamas security chief",
         deck=("Airstrike kills Naim Abu Nahal, Hamas security chief; "
                "six killed across Gaza."),
         source="Reuters", label="REPORTED", lon=34.5, lat=31.5),
    dict(n=6, kicker="GULF OF FINLAND \u00b7 WAR",
         headline="Zelensky confirms ship strike",
         deck=("Kyiv says it hit the cargo ship Sparta II; it says the ship "
                "carried weapons."),
         source="Bloomberg", label="REPORTED", lon=26.5, lat=59.8),
    dict(n=7, kicker="UKRAINE \u00b7 WAR",
         headline="Russia's losses hit record year",
         deck=("Kyiv counts 432,519 casualties in 2026, passing 2024's "
                "record; unverified."),
         source="Kyiv Independent", label="CLAIM", lon=30.5, lat=50.4),
    dict(n=8, kicker="OSLO \u00b7 DEFENCE",
         headline="Norway pledges $7bn for 2027",
         deck=("Oslo will expand the DESNA air-defence system; at least "
                "$7bn in aid in 2027."),
         source="Reuters", label="REPORTED", lon=10.7, lat=59.9),
    dict(n=9, kicker="BERLIN \u00b7 POLITICS",
         headline="Germans refuse to pick a side",
         deck=("83% want neutrality between the US and China; Ukraine aid "
                "backing at 46%."),
         source="SCMP", label="REPORTED", lon=13.4, lat=52.5),
    dict(n=10, kicker="LONDON \u00b7 SECURITY",
         headline="MI5 warns Ukraine suppliers",
         deck=("Defence firms backing Kyiv face a higher Russian sabotage "
                "threat, MI5 warns."),
         source="Reuters", label="REPORTED", lon=-0.1, lat=51.5),
    dict(n=11, kicker="GOLF \u00b7 SPORT",
         headline="Three Koreans win LPGA cards",
         deck=("Kim Min-sun, Yoo Hyun-jo and Lee Da-yeon earn 2027 LPGA Tour "
                "cards."),
         source="Yonhap", label="REPORTED", lon=-88.0, lat=30.7),
    dict(n=12, kicker="SEOUL \u00b7 ECONOMY",
         headline="Shoppers lose heart again",
         deck=("Consumer sentiment falls for a second month, to 103.1, its "
                "lowest since April."),
         source="Yonhap", label="REPORTED", lon=126.3, lat=38.3),
    dict(n=13, kicker="SEOUL \u00b7 COURTS",
         headline="Election official arrested",
         deck=("Court orders arrest of election official accused of "
                "forging a vote-count sheet."),
         source="Yonhap", label="REPORTED", lon=128.3, lat=37.0),
    dict(n=14, kicker="MUMBAI \u00b7 MARKETS",
         headline="Exchanges shut for festival",
         deck=("NSE and BSE close for Guru Nanak Jayanti, the 557th birth "
                "anniversary."),
         source="CNBC TV18", label="REPORTED", lon=72.8, lat=19.1),
    dict(n=15, kicker="ASIA \u00b7 CURRENCIES",
         headline="Currencies hold steady",
         deck=("Currencies consolidate as risk-on mood returns; the won is "
                "flat near 1,341."),
         source="WSJ", label="REPORTED", lon=103.8, lat=1.35),
    dict(n=16, kicker="SEOUL \u00b7 CRYPTO",
         headline="Crypto rulebook unveiled",
         deck=("FSC drafts a Digital Asset Act: bank-led stablecoins, ICO "
                "ban ends, 20% cap."),
         source="CoinDesk", label="REPORTED", lon=126.0, lat=36.3),
    dict(n=17, kicker="KINBURN SPIT \u00b7 WAR",
         headline="100 civilians trapped",
         deck=("About 100 face severe food and medicine shortages under "
                "occupation."),
         source="Kyiv Independent", label="REPORTED", lon=31.8, lat=46.4),
    dict(n=18, kicker="NEW YORK \u00b7 COURTS",
         headline="Huawei guilty on 10 counts",
         deck=("Brooklyn jury convicts Huawei of bank fraud and stealing "
                "trade secrets."),
         source="Reuters", label="REPORTED", lon=-74.0, lat=40.7),
]

STATS = [
    ("3 MIN", "Ulleung alert lifted in 3 min"),
    ("4", "tankers IRGC says hit mines"),
    ("+9.1%", "Taiwan leads Asia's rally"),
    ("432,519", "Russian losses in 2026, Kyiv says"),
    ("10 of 12", "counts Huawei convicted on"),
    ("$7BN", "Norway's 2027 aid to Ukraine"),
]

# ---------------------------------------------------------------- map data
# Coarse continent outlines (lon, lat). Recognisable at newspaper size.
NORTH_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
                 (-135, 57), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
                 (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
                 (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-79, 9),
                 (-81, 13), (-84, 16), (-87, 21), (-90, 21), (-97, 26),
                 (-93, 30), (-89, 30), (-84, 30), (-81, 25), (-80, 32),
                 (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44),
                 (-60, 47), (-55, 47), (-60, 52), (-65, 58), (-68, 58),
                 (-78, 62), (-85, 66), (-92, 66), (-95, 69), (-110, 68),
                 (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68),
             (-25, 70), (-20, 74), (-30, 78), (-45, 80), (-58, 76),
             (-60, 70)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
                 (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
                 (-74, -50), (-70, -54), (-66, -55), (-68, -50), (-65, -45),
                 (-62, -41), (-58, -38), (-52, -33), (-48, -28), (-41, -23),
                 (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
                 (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
                 (-72, 12), (-77, 8)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
          (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, -1),
          (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (19, -34),
          (26, -34), (32, -29), (35, -24), (40, -16), (40, -11), (42, -4),
          (48, 11), (51, 11), (46, 6), (43, 2), (41, -2), (38, -8),
          (36, -18), (33, -26), (29, -31), (25, -34), (19, -34)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
           (0, 51), (3, 53), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60),
           (5, 62), (12, 64), (18, 69), (25, 71), (32, 70), (40, 68),
           (44, 68), (50, 69), (58, 69), (66, 72), (75, 72), (85, 74),
           (95, 76), (105, 77), (115, 73), (125, 72), (135, 71), (145, 72),
           (155, 70), (162, 66), (170, 66), (178, 65), (178, 62), (170, 60),
           (162, 60), (158, 53), (150, 59), (142, 54), (140, 48), (135, 43),
           (130, 42), (127, 40), (126, 38), (122, 37), (120, 32), (122, 28),
           (118, 25), (112, 22), (108, 18), (105, 10), (103, 8), (100, 7),
           (98, 10), (97, 16), (94, 17), (92, 21), (90, 22), (86, 20),
           (82, 17), (80, 13), (77, 8), (75, 12), (72, 20), (70, 23),
           (66, 25), (62, 25), (58, 26), (56, 27), (54, 26), (52, 28),
           (50, 29), (48, 30), (47, 30), (44, 29), (42, 27), (40, 23),
           (39, 21), (38, 18), (35, 16), (34, 28), (36, 36), (33, 36),
           (30, 36), (27, 37), (26, 38), (23, 36), (22, 37), (20, 39),
           (18, 40), (16, 38), (15, 38), (12, 44), (10, 44), (8, 44),
           (6, 43), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)]
UNITED_KINGDOM = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57),
                  (0, 53), (1, 51)]
JAPAN = [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (141, 39),
         (141, 41), (143, 42), (145, 44), (141, 45), (140, 42), (139, 38),
         (136, 37), (133, 35), (131, 33)]
SE_ASIA = [(95, 5), (98, 3), (100, -2), (103, -4), (106, -6), (110, -7),
           (114, -8), (118, -9), (122, -10), (126, -9), (128, -8), (130, -4),
           (132, -2), (134, -4), (137, -2), (140, -3), (141, -2), (138, 0),
           (135, 2), (132, 1), (130, 0), (128, 2), (126, 3), (124, 1),
           (122, 2), (120, 0), (118, 2), (116, 4), (114, 2), (112, 0),
           (110, -1), (108, 1), (106, 2), (104, 2), (101, 4), (98, 5)]
AUSTRALIA = [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
               (175, -40), (172, -43), (169, -46)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA,
              UNITED_KINGDOM, JAPAN, SE_ASIA, AUSTRALIA, NEW_ZEALAND]


# ---------------------------------------------------------------- drawing
def draw_pin(draw, x, y, num, r=8):
    """Numbered red map dot with white ring."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255),
                 width=1)
    f = font(SANS_B, 9 if num < 10 else 8)
    t = str(num)
    tw = draw.textlength(t, font=f)
    th = f.getbbox(t)[3] - f.getbbox(t)[1]
    draw.text((x - tw / 2, y - th / 2 - 1), t, font=f, fill=(255, 255, 255))


def draw_map(draw, box, pins):
    """World map with numbered pins. Pins closer than 18px are fanned out
    around their true spot with leader lines (Seoul triple, Ukraine pair)."""
    x0, y0, w, h = box
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=INK, width=1)
    lon0, lon1 = -180.0, 180.0
    lat0, lat1 = 78.0, -58.0  # top, bottom

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # pin positions
    pts = {}
    for p in pins:
        pts[p["n"]] = proj(p["lon"], p["lat"])
    # cluster pins closer than 18px
    nums = sorted(pts)
    used = set()
    clusters = []
    for a in nums:
        if a in used:
            continue
        grp = [a]
        used.add(a)
        for b in nums:
            if b in used:
                continue
            d = ((pts[a][0] - pts[b][0]) ** 2 + (pts[a][1] - pts[b][1]) ** 2) ** 0.5
            if d < 18:
                grp.append(b)
                used.add(b)
        clusters.append(grp)
    for grp in clusters:
        if len(grp) == 1:
            n = grp[0]
            draw_pin(draw, pts[n][0], pts[n][1], n)
            continue
        cx = sum(pts[n][0] for n in grp) / len(grp)
        cy = sum(pts[n][1] for n in grp) / len(grp)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=INK)
        import math
        for i, n in enumerate(grp):
            ang = -90 + i * (360.0 / len(grp))
            rad = math.radians(ang)
            fx = cx + 15 * math.cos(rad)
            fy = cy + 15 * math.sin(rad)
            draw.line([pts[n], (fx, fy)], fill=GREY, width=1)
            draw_pin(draw, fx, fy, n)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14  # margin
    RW = W - 2 * M  # 996

    # ---- masthead
    y = 10
    d.text((M, y), "THE WORLD IN ONE DAY", font=font(SANS_B, 15), fill=RED)
    right = "18 STORIES \u00b7 ALL FROM THIS ONE DAY"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 13)), y + 1),
           right, font=font(SANS_B, 13), fill=INK)
    d.line([(M, 32), (W - M, 32)], fill=INK, width=2)

    # ---- headline
    headline = "Tuesday 24 November 2026"
    hf = font(SERIF_B, 60)
    d.text((M, 36), headline, font=hf, fill=INK)
    sub = ("Russian jets breach Korean air zone \u00b7 Tankers burn in "
           "Hormuz \u00b7 Asia's markets roar back")
    d.text((M, 104), sub, font=font(SERIF_I, 17), fill=RED)
    d.line([(M, 126), (W - M, 126)], fill=INK, width=1)

    # ---- stat strip
    sy, sh = 132, 44
    col_w = RW / 6.0
    for i, (big, small) in enumerate(STATS):
        x = M + i * col_w
        if i > 0:
            d.line([(x - 5, sy + 2), (x - 5, sy + sh - 2)], fill=GREY, width=1)
        d.text((x, sy), big, font=font(SANS_B, 23), fill=RED)
        for j, ln in enumerate(fit_lines(small, font(SANS, 10), col_w - 12, d, 2)):
            d.text((x, sy + 26 + j * 12), ln, font=font(SANS, 10), fill=INK)
    d.line([(M, 182), (W - M, 182)], fill=INK, width=1)

    # ---- 3 lead panels
    ly, lw, gap = 190, 325, 10
    photo_h = 132
    for i, st in enumerate(LEADS):
        x = M + i * (lw + gap)
        # soft shadow + border
        d.rectangle([x + 2, ly + 2, x + lw + 2, ly + 252 + 2], fill=(210, 204, 188))
        d.rectangle([x, ly, x + lw, ly + 252], fill=(255, 255, 255),
                    outline=INK, width=1)
        # photo
        src = None
        for f in os.listdir(PANELS):
            if f.startswith("media-generation-" + st["photo"]):
                src = os.path.join(PANELS, f)
        if src is None:
            raise SystemExit(f"lead photo missing: {st['photo']}")
        ph = crop_fill(Image.open(src).convert("RGB"), lw - 2, photo_h)
        img.paste(ph, (x + 1, ly + 1))
        # tag chip on photo
        chip_txt = st["kicker"]
        cf = font(SANS_B, 10)
        cw = d.textlength(chip_txt, font=cf) + 12
        d.rectangle([x + 1, ly + 1, x + 1 + cw, ly + 1 + 19], fill=st["chip"])
        d.text((x + 7, ly + 4), chip_txt, font=cf, fill=(255, 255, 255))
        # kicker line: number circle + label pill
        ky = ly + photo_h + 10
        d.ellipse([x + 8, ky, x + 32, ky + 24], fill=RED)
        nf = font(SANS_B, 13)
        nt = str(st["n"])
        d.text((x + 20 - d.textlength(nt, font=nf) / 2, ky + 4), nt,
               font=nf, fill=(255, 255, 255))
        lab = st["label"]
        lf = font(SANS_B, 9)
        lw_lab = d.textlength(lab, font=lf) + 10
        lcol = RED if lab == "CLAIM" else DARK
        d.rounded_rectangle([x + lw - 8 - lw_lab, ky + 3, x + lw - 8, ky + 21],
                            radius=9, outline=lcol, width=1)
        d.text((x + lw - 8 - lw_lab + 5, ky + 6), lab, font=lf, fill=lcol)
        # headline (max 2 lines)
        hy = ky + 30
        hlines = fit_lines(st["headline"], font(SERIF_B, 19), lw - 16, d, 2)
        for j, ln in enumerate(hlines):
            d.text((x + 8, hy + j * 22), ln, font=font(SERIF_B, 19), fill=INK)
        # deck (max 3 lines), source folded into the wrapped text
        dy = hy + len(hlines) * 22 + 4
        dlines = fit_lines(st["deck"] + " \u2014 " + st["source"],
                           font(SERIF, 12), lw - 16, d, 3)
        for j, ln in enumerate(dlines):
            d.text((x + 8, dy + j * 15), ln, font=font(SERIF, 12), fill=INK)

    # ---- section headers
    hy2 = 446
    d.text((M, hy2), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=RED)
    d.text((M + 175, hy2 + 2), "numbers match the stories",
           font=font(SANS, 10), fill=GREY)
    d.text((424, hy2), "ALSO ON TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 14), fill=RED)
    d.line([(M, 468), (W - M, 468)], fill=INK, width=1)

    # ---- map (left) + legend under it
    draw_map(d, (M, 476, 396, 220), LEADS + ALSO)
    d.text((M, 700), "Pins mark stories 1\u201318. 3 is the markets story.",
           font=font(SANS, 10), fill=GREY)
    d.text((M, 714), "Seoul pins 12, 13, 16 and Ukraine pins 7, 17 are fanned",
           font=font(SANS, 10), fill=GREY)
    d.text((M, 728), "out from one dot so each number stays readable.",
           font=font(SANS, 10), fill=GREY)
    # legend box
    lx, ly2, lw2, lh2 = M, 748, 396, 136
    d.rectangle([lx, ly2, lx + lw2, ly2 + lh2], outline=INK, width=1,
                fill=(255, 255, 255))
    d.text((lx + 10, ly2 + 8), "HOW TO READ THE LABELS",
           font=font(SANS_B, 11), fill=RED)
    legend = [
        ("REPORTED", DARK,
         "Happened, or was first reported, on 24 Nov, as the named source "
         "reports it."),
        ("CLAIM", RED,
         "One side's claim. Not independently verified; the other side "
         "disputes it."),
    ]
    yy = ly2 + 30
    for lab, col, txt in legend:
        lf = font(SANS_B, 10)
        d.text((lx + 10, yy), lab, font=lf, fill=col)
        tx = lx + 10 + d.textlength(lab + "  ", font=lf)
        for j, ln in enumerate(fit_lines(txt, font(SANS, 10), lw2 - 20 -
                                         (tx - lx - 10), d, 2)):
            d.text((tx, yy + j * 13), ln, font=font(SANS, 10), fill=INK)
        yy += 30
    d.line([(lx + 10, yy + 2), (lx + lw2 - 10, yy + 2)], fill=GREY, width=1)
    note = ("Each story was checked against its named source: it happened, "
            "or was first reported, on Tuesday 24 November 2026.")
    for j, ln in enumerate(fit_lines(note, font(SERIF, 11), lw2 - 20, d, 3)):
        d.text((lx + 10, yy + 10 + j * 14), ln, font=font(SERIF, 11), fill=INK)

    # ---- ALSO ON list (right): 15 items, 2 lines each
    ax, aw = 424, W - M - 424  # 586
    iy = 476
    row_h = 27
    for st in ALSO:
        # line 1: number + kicker + headline
        n_txt = f"{st['n']}  "
        d.text((ax, iy), n_txt, font=font(SANS_B, 13), fill=RED)
        nx = ax + d.textlength(n_txt, font=font(SANS_B, 13))
        d.text((nx, iy + 1), st["kicker"], font=font(SANS_B, 11), fill=RED)
        kx = nx + d.textlength(st["kicker"], font=font(SANS_B, 11))
        head_txt = " \u2014 " + st["headline"]
        check_one_line(head_txt, font(SERIF_B, 13), aw - (kx - ax), d,
                       f"also-{st['n']}-head")
        d.text((kx, iy - 1), head_txt, font=font(SERIF_B, 13), fill=INK)
        # line 2: deck + source + label
        deck_txt = st["deck"] + " \u2014 " + st["source"]
        lab_txt = " \u00b7 " + st["label"]
        dw = d.textlength(deck_txt, font=font(SERIF, 11))
        lw_ = d.textlength(lab_txt, font=font(SANS_B, 10))
        check_one_line(deck_txt + lab_txt, font(SERIF, 11), aw, d,
                       f"also-{st['n']}-deck")
        d.text((ax, iy + 14), deck_txt, font=font(SERIF, 11), fill=INK)
        lcol = RED if st["label"] == "CLAIM" else DARK
        d.text((ax + dw, iy + 14), lab_txt, font=font(SANS_B, 10), fill=lcol)
        iy += row_h

    # ---- DATE CHECK box
    by = 892
    d.rectangle([M, by, W - M, by + 68], outline=RED, width=2,
                fill=(255, 255, 255))
    d.text((M + 10, by + 8), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    dc = ("Every story here happened, or was first reported, on Tuesday 24 "
          "November 2026. LEFT OUT \u2014 23 NOV: West Bank raids \u00b7 "
          "Israeli army suicides report \u00b7 Princeton student held \u00b7 "
          "space-weapon report \u00b7 22 NOV: Rangers 2\u20131 Motherwell \u00b7 "
          "19 NOV: GTA VI launch \u00b7 OCT: Indonesia farm plan.")
    for j, ln in enumerate(fit_lines(dc, font(SERIF, 12), RW - 130, d, 3)):
        d.text((M + 118, by + 9 + j * 15), ln, font=font(SERIF, 12), fill=INK)

    # ---- footer
    foot = ("Claims are attributed, not stated as fact \u00b7 Pictures: "
            "original generated images; map: drawn in code \u00b7 Sources: "
            "Reuters, Yonhap, Press TV, KCNA, MEE, SCMP, WSJ, CoinDesk, "
            "Kyiv Independent, US Dept. of Justice \u00b7 2026-11-24")
    fw = d.textlength(foot, font=font(SANS, 9))
    d.text(((W - fw) / 2, 968), foot, font=font(SANS, 9), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
