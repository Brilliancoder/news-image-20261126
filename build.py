"""Render entry.png: a one-page broadsheet of world news for Thursday 26 November 2026.

Run at build time (needs Pillow + system Noto fonts): python3 build.py
main.py only copies the committed entry.png, so the graded program stays stdlib-only.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/noto/"
INK, PAPER, RULE, MUTED, RED = (22, 22, 26), (250, 247, 240), (60, 60, 60), (88, 88, 92), (178, 24, 30)
REGION = {  # kicker colour per region
    "MIDDLE EAST": (178, 24, 30), "EUROPE": (24, 70, 150), "AFRICA": (190, 110, 10),
    "ASIA": (20, 120, 90), "AMERICAS": (120, 50, 140), "SCIENCE": (30, 110, 160), "SPORT": (70, 90, 30),
}


def font(name, size):
    return ImageFont.truetype(FD + name, size)


def wrap(d, text, f, width, max_lines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    assert len(lines) <= max_lines, f"overflow ({len(lines)}>{max_lines}): {text}"
    return lines


def block(d, x, y, text, f, width, max_lines, fill, lh):
    for line in wrap(d, text, f, width, max_lines):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


HEROES = [
    ("MIDDLE EAST", "KUWAIT", "Drone attack in Kuwait kills two Italian technicians",
     "Rheinmetall staff die at an air-defence site. Italy and Kuwait blame Iranian drones; Iran denies any role."),
    ("EUROPE", "EU / ECB", "Spain's Hernández de Cos picked to succeed Lagarde at the ECB",
     "EU leaders agree the package at a Brussels summit; he would be the first Spaniard to lead the central bank."),
    ("AFRICA", "DR CONGO", "Congo's Ebola outbreak passes 12,000 confirmed cases",
     "Government data: 12,021 cases, 5,904 deaths. Fighting near Bunia forces some responders to evacuate."),
    ("ASIA", "NORTH KOREA", "Kim Jong Un tours nuclear-material plants, vows more warheads",
     "State media KCNA reports the visit, days after he ignored Trump's offer to meet."),
]

NUMBERS = [
    ("12,021", "confirmed Ebola cases in DR Congo"),
    ("77,000", "UK net migration, lowest since 1997*"),
    ("43–29", "Argentine Senate vote to suspend primaries"),
    ("10", "killed across Ukraine in a day of Russian attacks"),
    ("31", "dead in Giza tanker fire; driver detained"),
    ("18", "Chinese golf courses closing (AFP tally)"),
]

GRID = [
    ("MIDDLE EAST", "GAZA", "Israeli strikes kill 9, incl. Hamas-appointed deputy education minister"),
    ("EUROPE", "UKRAINE", "Ballistic missiles hit Kyiv; Russian attacks kill 10 nationwide"),
    ("AMERICAS", "USA / NATO", "Trump and Rutte urge no widening of Ukraine war after Florida talks"),
    ("AMERICAS", "ARGENTINA", "Senate votes 43–29 to suspend 2027 primaries, a boost for Milei"),
    ("EUROPE", "UK", "Net migration falls to 77,000, lowest since 1997 bar Covid years"),
    ("AFRICA", "GUINEA-BISSAU", "Junta delays elections to Nov 2028 on coup's first anniversary"),
    ("MIDDLE EAST", "YEMEN", "Saudi Arabia says it hit 50 Houthi targets in Sanaa, Hudaydah, Saada"),
    ("AFRICA", "NIGER", "Attack on National Guard post in Sanam kills 13 guardsmen"),
    ("AFRICA", "NIGERIA", "Gunmen kill 30 people and burn homes in Niger State"),
    ("ASIA", "BANGLADESH", "About 400 garment factories shut as wage protests block highways"),
    ("ASIA", "CHINA", "At least 18 golf courses close, 10 in Beijing, in new clampdown"),
    ("EUROPE", "SERBIA", "Parliament sets presidential election for 27 December"),
    ("EUROPE", "SPAIN", "Malta-flagged tanker sinks off Ibiza: 1 dead, 16 rescued"),
    ("ASIA", "THAILAND", "Blast and fire at Bangchak oil site in Bangkok injure 9"),
    ("EUROPE", "UK", "Man convicted of attempted murder of 14, incl. 2025 train stabbing"),
    ("AFRICA", "EGYPT", "Driver detained over Cairo Ring Road tanker fire that killed 31"),
    ("ASIA", "PAKISTAN", "Karachi building collapse toll rises to 4; 17 still missing"),
    ("SCIENCE", "NATURE", "Egoviruses: new order of large DNA viruses, poxvirus kin, found"),
    ("SPORT", "NFL THANKSGIVING", "Bears beat Lions 39–35; Eagles edge Cowboys 39–38; Bills top Chiefs"),
    ("AMERICAS", "USA", "Storm pushes 100th Macy's parade to Saturday, a first in its history"),
]


def render(path="entry.png"):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    M = 18

    # Masthead
    d.text((M, 10), "THE WORLD IN ONE PAGE", font=font("NotoSerifDisplay-Black.ttf", 44), fill=INK)
    d.text((M, 64), "World news of Thursday 26 November 2026  ·  events that happened or were first reported that day",
           font=font("NotoSans-Italic.ttf", 15), fill=MUTED)
    df = font("NotoSans-Black.ttf", 34)
    date = "THU 26 NOV 2026"
    d.rectangle((W - M - d.textlength(date, font=df) - 24, 12, W - M, 58), fill=RED)
    d.text((W - M - 12, 35), date, font=df, fill=PAPER, anchor="rm")
    d.line((M, 90, W - M, 90), fill=INK, width=3)

    # Hero stories, 2x2
    hk, hh, hb = font("NotoSans-Bold.ttf", 14), font("NotoSerif-Bold.ttf", 25), font("NotoSans-Regular.ttf", 16)
    cw, ch, top = (W - 2 * M - 16) // 2, 158, 100
    for i, (reg, place, head, body) in enumerate(HEROES):
        x, y = M + (i % 2) * (cw + 16), top + (i // 2) * (ch + 8)
        col = REGION[reg]
        d.rectangle((x, y, x + 6, y + ch - 6), fill=col)
        tx, tw = x + 16, cw - 20
        d.text((tx, y), f"{place}  ·  {reg}", font=hk, fill=col)
        yy = block(d, tx, y + 20, head, hh, tw, 2, INK, 31)
        block(d, tx, yy + 4, body, hb, tw, 2, RULE, 21)
    y0 = top + 2 * ch + 12
    d.line((M, y0, W - M, y0), fill=INK, width=2)

    # Numbers band
    nf, nl = font("NotoSans-Black.ttf", 30), font("NotoSans-SemiCondensed.ttf", 13)
    bw = (W - 2 * M) / len(NUMBERS)
    d.text((M, y0 + 6), "THE DAY IN NUMBERS", font=font("NotoSans-Bold.ttf", 12), fill=RED)
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * bw
        if i:
            d.line((x - 6, y0 + 26, x - 6, y0 + 100), fill=(200, 196, 186), width=1)
        d.text((x, y0 + 22), num, font=nf, fill=INK)
        block(d, x, y0 + 64, lab, nl, bw - 14, 2, MUTED, 16)
    y1 = y0 + 108
    d.line((M, y1, W - M, y1), fill=INK, width=2)

    # Grid of the other stories, 4 columns x 5 rows
    gk, gh = font("NotoSans-Bold.ttf", 12), font("NotoSans-SemiCondensedBold.ttf", 16)
    cols, gw = 4, (W - 2 * M - 3 * 12) / 4
    gh_row = (H - 22 - y1 - 8) / 5
    for i, (reg, place, head) in enumerate(GRID):
        x, y = M + (i % cols) * (gw + 12), y1 + 8 + (i // cols) * gh_row
        d.text((x, y), place, font=gk, fill=REGION[reg])
        block(d, x, y + 17, head, gh, gw, 3, INK, 21)
        if i // cols < 4:
            d.line((x, y + gh_row - 6, x + gw, y + gh_row - 6), fill=(200, 196, 186), width=1)

    d.text((W // 2, H - 4), "*excluding Covid years  ·  sources: AP, Reuters, AFP, BBC, ONS, KCNA via AP — see README",
           font=font("NotoSans-Regular.ttf", 11), fill=MUTED, anchor="md")
    im.save(path, optimize=True)


if __name__ == "__main__":
    render()
