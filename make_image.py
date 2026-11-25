"""Draw the 24 November newspaper front page using Pillow."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAPER = "#f6f1e5"
NAVY = "#14213d"
RED = "#b3001b"
RULE = "#a19887"
WHITE = "#fff8e9"
FONTS = Path("/usr/share/fonts/truetype")
BOLD = FONTS / "liberation/LiberationSans-Bold.ttf"
REGULAR = FONTS / "liberation/LiberationSans-Regular.ttf"
SERIF = FONTS / "dejavu/DejaVuSerif-Bold.ttf"


def fit_text(draw, box, text, face, size, color=NAVY, max_lines=2, center=False):
    """Measure ink bounds, wrap at spaces, and step down until the box fits."""
    x, y, right, bottom = box
    for font_size in range(size, 0, -1):
        font = ImageFont.truetype(str(face), font_size)

        def width(line):
            left, _, end, _ = draw.textbbox((0, 0), line, font=font)
            return end - left

        lines = [""]
        for word in text.split():
            candidate = f"{lines[-1]} {word}".strip()
            if lines[-1] and width(candidate) > right - x:
                lines.append(word)
            else:
                lines[-1] = candidate
        block = "\n".join(lines)
        align = "center" if center else "left"
        spacing = max(2, font_size // 10)
        left, top, end, base = draw.multiline_textbbox(
            (0, 0), block, font=font, spacing=spacing, align=align
        )
        if len(lines) <= max_lines and end - left <= right - x and base - top <= bottom - y:
            offset = (right - x - (end - left)) // 2 if center else 0
            draw.multiline_text(
                (x + offset - left, y - top), block, font=font,
                fill=color, spacing=spacing, align=align,
            )
            return y + base - top
    raise ValueError(f"Text does not fit: {text}")


def sea(draw):
    for y in range(75):
        draw.line((0, y, 959, y), fill=(17 + y // 8, 29 + y // 4, 52 + y // 5))
    draw.ellipse((139, 9, 217, 87), outline="#584d58", width=2)
    draw.ellipse((145, 15, 211, 81), fill="#bd7867")
    for index in range(29):
        x = (index * 193 + 51) % 940
        y = 5 + (index * 23) % 54
        draw.line((x, y, x + 2, y), fill="#577080")
    draw.rectangle((0, 75, 959, 181), fill="#214a5e")
    draw.rectangle((0, 104, 959, 181), fill="#153447")
    for index in range(55):
        x = (index * 137) % 920
        y = 80 + (index * 41) % 100
        draw.line((x, y, x + 12 + index % 25, y), fill="#2d596c", width=2)

    for index in range(18):
        y = 77 + index * 4
        x = 171 + (index * 17) % 40 - index * 3
        draw.line((x, y, x + 14 + index * 3, y), fill="#82666a", width=2)
    draw.polygon([(332, 94), (748, 94), (799, 82), (768, 121),
                  (742, 129), (360, 129)], fill="#9cabb1")
    draw.polygon([(354, 116), (772, 116), (742, 129), (367, 129)], fill="#677e89")
    draw.polygon([(421, 94), (445, 66), (497, 66), (508, 49), (579, 49),
                  (601, 75), (647, 75), (665, 94)], fill="#b6c2c4")
    draw.rectangle((467, 53, 485, 68), fill="#8ea1a9")
    draw.line((544, 49, 544, 16), fill="#b6c2c4", width=3)
    draw.line((523, 28, 565, 28), fill="#b6c2c4", width=3)
    for x in range(516, 572, 13):
        draw.rectangle((x, 56, x + 8, 62), fill="#324c5e")
    for x in range(393, 745, 34):
        draw.line((x, 103, x + 16, 103), fill="#718894", width=2)

    for x, y in [(126, 142), (238, 165), (413, 153)]:
        draw.line([(x - 43, y + 11), (x - 21, y + 7), (x + 5, y + 2)],
                  fill=WHITE, width=3)
        draw.line((x - 29, y + 13, x + 5, y + 6), fill="#94c1c4", width=2)
        draw.polygon([(x, y - 5), (x + 30, y - 5), (x + 42, y - 9),
                      (x + 33, y + 4), (x + 5, y + 5)],
                     fill="#101e2d", outline="#7996a1", width=2)
        draw.rectangle((x + 11, y - 9, x + 24, y - 5), fill="#52707c")
        draw.line((x + 18, y - 9, x + 18, y - 17), fill="#b0c3c9", width=2)
        draw.line((x + 14, y - 17, x + 22, y - 17), fill="#b0c3c9", width=2)
    for x in range(375, 745, 19):
        draw.line((x, 130, x + 9, 130), fill="#7598a2", width=2)
    draw.line((368, 113, 758, 113), fill="#526b79", width=2)
    draw.line((701, 92, 709, 85, 739, 80), fill="#adbfc4", width=3)


def chip(draw):
    for x in range(0, 960, 16):
        draw.line((x, 0, x, 181), fill="#20403c")
    for y in range(4, 182, 9):
        bend = 63 + y // 2
        draw.line([(0, y), (bend, y), (bend + 44, 45 + y // 2), (370, 45 + y // 2)],
                  fill="#628456", width=2)
        draw.ellipse((bend - 3, y - 3, bend + 3, y + 3), outline="#a3bd78")
    for x in range(196, 420, 10):
        draw.line((x, 10, x, 172), fill="#b9bd78", width=4)
    for y in range(27, 157, 8):
        draw.line((175, y, 440, y), fill="#b9bd78", width=3)
    draw.rounded_rectangle((185, 17, 429, 165), radius=9, fill="#102720",
                           outline="#a4b977", width=3)
    draw.rectangle((199, 29, 415, 152), fill="#365840", outline="#6a9565", width=2)
    for y in range(35, 151, 7):
        for x in range(204, 414, 7):
            draw.rectangle((x, y, x + 2, y + 2), fill="#789959")
    draw.rectangle((246, 43, 368, 139), fill="#223d32", outline="#c6d28d", width=3)
    for y in range(53, 130, 15):
        for x in range(256, 358, 17):
            draw.rectangle((x, y, x + 12, y + 9), fill="#74975a")
            draw.line((x + 2, y + 2, x + 9, y + 2), fill="#aac17b")
    for x in range(480, 939, 38):
        draw.line((x, 21, x, 157), fill="#284945")
    up = [(479, 143), (546, 138), (583, 146), (628, 109), (662, 115),
          (717, 73), (746, 80), (795, 29)]
    down = [(795, 29), (829, 64), (864, 58), (922, 94)]
    draw.polygon(up + down[1:] + [(922, 154), (479, 154)], fill="#2c4b40")
    for y in (42, 83, 123, 154):
        draw.line((475, y, 932, y), fill="#547567")
    for points, color in ((up, "#d7ec8c"), (down, "#ff9b82")):
        draw.line(points, fill=color, width=5, joint="curve")
        x, y = points[-1]
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)

    fit_text(draw, (759, 8, 819, 23), "MON", BOLD, 13, "#d7ec8c", max_lines=1, center=True)
    fit_text(draw, (879, 105, 924, 121), "TUE", BOLD, 13, "#ffb19e", max_lines=1)


def pharma(draw):
    draw.rectangle((0, 67, 471, 89), fill="#407876")
    for x in range(0, 472, 17):
        draw.line((x, 0, x, 67), fill="#32605f")
    for x in (29, 78, 362, 404):
        draw.line((x, 13, x + 21, 35, x + 47, 27), fill="#6f9991", width=2)
        for dx, y in ((0, 13), (21, 35), (47, 27)):
            draw.ellipse((x + dx - 4, y - 4, x + dx + 4, y + 4), outline="#9cbbb0")
    draw.ellipse((99, 70, 395, 87), fill="#305a5b")
    draw.rounded_rectangle((131, 20, 207, 79), radius=8, fill="#ae6940",
                           outline="#efb77c", width=2)
    draw.rectangle((137, 40, 201, 67), fill="#f0dfb9")
    for y, end in ((47, 191), (52, 183), (58, 174)):
        draw.line((145, y, end, y), fill="#946647")
    draw.rounded_rectangle((127, 9, 211, 27), radius=4, fill="#bad3c8")
    for x in range(133, 208, 6):
        draw.line((x, 13, x, 24), fill="#729a90")
    draw.polygon([(265, 14), (291, 14), (291, 36), (321, 75), (315, 81),
                  (241, 81), (235, 75), (265, 36)], fill="#619994",
                 outline="#c7e9d9", width=2)
    draw.polygon([(251, 57), (274, 59), (303, 55), (316, 74), (311, 77),
                  (245, 77), (241, 74)], fill="#a5d8a1")
    draw.line((260, 12, 296, 12), fill="#e0f2d8", width=4)
    for x, y in ((258, 69), (267, 62), (290, 68), (300, 73)):
        draw.ellipse((x, y, x + 4, y + 4), outline="#598c72")
    draw.rounded_rectangle((326, 62, 389, 81), radius=9, fill="#f4deb8")
    draw.rounded_rectangle((326, 62, 357, 81), radius=9, fill="#d98769")
    draw.rectangle((343, 62, 357, 81), fill="#d98769")


def court(draw):
    gold = "#f5d695"
    for y in range(3, 88, 4):
        draw.line((0, y, 471, y), fill="#44374f")
    for x in (35, 79, 123, 315, 359, 403):
        draw.arc((x, 7, x + 34, 70), 180, 360, fill="#665369", width=2)
        draw.line((x + 4, 38, x + 4, 88), fill="#665369")
        draw.line((x + 30, 38, x + 30, 88), fill="#665369")
    draw.ellipse((157, -21, 309, 110), fill="#54485e", outline="#8a7181")
    for inset in (24, 50):
        draw.ellipse((157 + inset, -21, 309 - inset, 110), outline="#8a7181")
    for y in (14, 33):
        draw.arc((163, y, 303, y + 36), 0, 180, fill="#806c81")
    draw.line((235, 16, 235, 73), fill="#a78256", width=1)
    for index in range(14):
        x = 22 + index * 32
        y = 52 + abs(x - 232) // 11
        draw.line((x, y - 12, x, 89), fill="#a48a91")
        draw.polygon([(x, y - 12), (x + 19, y - 10), (x + 19, y - 1),
                      (x, y - 4)], fill=("#997887", "#b19186", "#867998")[index % 3])
    draw.line((233, 13, 233, 75), fill=gold, width=5)
    draw.line((178, 30, 288, 30), fill=gold, width=4)
    draw.ellipse((228, 10, 238, 20), fill=gold)
    for x in (185, 281):
        draw.line((x - 19, 60, x, 29, x + 19, 60), fill=gold, width=2)
        draw.pieslice((x - 21, 49, x + 21, 71), 0, 180, fill=gold)
        draw.arc((x - 17, 53, x + 17, 68), 14, 166, fill="#ad8659")
    draw.rounded_rectangle((204, 75, 262, 81), radius=3, fill=gold)
    draw.line((198, 85, 268, 85), fill="#aa825e", width=2)


def orbit(draw):
    for index in range(104):
        x = (index * 127 + 18) % 472
        y = (index * 31 + index * index + 4) % 88
        draw.point((x, y), fill=("#637999", "#a3b7d2", "#dae4ef")[index % 3])
    draw.ellipse((-125, 70, 399, 230), fill="#233d62", outline="#7aacce", width=2)
    draw.arc((-118, 76, 392, 236), 205, 338, fill="#4d7296", width=2)
    draw.arc((204, 9, 492, 78), 195, 334, fill="#344c72")
    for x, y in ((62, 19), (198, 36), (229, 12), (452, 18)):
        draw.line((x - 2, y, x + 2, y), fill="#a2bdd3")
        draw.line((x, y - 2, x, y + 2), fill="#a2bdd3")
    draw.polygon([(112, 53), (137, 60), (101, 89), (51, 89)], fill="#b46458")
    draw.polygon([(115, 54), (130, 57), (99, 81), (76, 88)], fill="#ffc38a")
    draw.polygon([(109, 52), (145, 16), (166, 11), (160, 31), (125, 66)],
                 fill="#e0e5dd", outline="#91a7ba", width=2)
    draw.line((143, 20, 151, 27), fill="#4b6e98", width=5)
    draw.polygon([(111, 48), (100, 50), (96, 64), (106, 61)], fill="#8a9fac")
    draw.line((262, 45, 443, 45), fill="#becbd3", width=4)
    for left in (265, 378):
        draw.rectangle((left, 25, left + 61, 64), fill="#345e8e",
                       outline="#a1b8d6", width=2)
        for x in range(left + 7, left + 61, 8):
            draw.line((x, 27, x, 62), fill="#7094b8")
        draw.line((left, 44, left + 61, 44), fill="#a1b8d6")
    draw.rounded_rectangle((337, 17, 367, 71), radius=7, fill="#dee0d8",
                           outline="#8aa8bd", width=2)
    draw.rectangle((329, 39, 375, 50), fill="#9aaebf", outline="#e6e7dc")
    draw.ellipse((346, 24, 355, 33), fill="#38597a")
    for y in (37, 53, 58, 63):
        draw.line((341, y, 362, y), fill="#657b91")
    draw.line((352, 16, 352, 9, 363, 7), fill="#a1b8d6")
    draw.ellipse((359, 5, 367, 9), fill="#c4d4db")
    draw.line((117, 55, 152, 21), fill="#faf1da", width=2)


def illustration(page, x, y, width, height, background, paint, native_size=None):
    art = Image.new("RGB", native_size or (width, height), background)
    paint(ImageDraw.Draw(art))
    if native_size:
        art = art.resize((width, height), Image.Resampling.LANCZOS)
    page.paste(art, (x, y))


def main():
    page = Image.new("RGB", (1024, 1024), PAPER)
    draw = ImageDraw.Draw(page)

    draw.rectangle((32, 24, 991, 29), fill=RED)
    fit_text(draw, (32, 39, 992, 60), "THE WORLD IN ONE PICTURE",
             BOLD, 22, RED, max_lines=1, center=True)
    fit_text(draw, (40, 69, 984, 111), "TUESDAY 24 NOVEMBER 2026",
             SERIF, 52, max_lines=1, center=True)

    illustration(page, 32, 125, 960, 182, "#162e2d", chip)
    draw.rectangle((32, 125, 991, 416), outline=RULE)
    fit_text(draw, (48, 318, 974, 337), "NVIDIA  /  GLOBAL MARKETS",
             BOLD, 17, RED, max_lines=1)
    fit_text(draw, (48, 343, 975, 383), "JENSEN HUANG RETURNS, NVIDIA WHIPSAWS",
             BOLD, 42, max_lines=1)
    fit_text(draw, (48, 389, 975, 410),
             "Monday +31% (about $952bn added) · Tuesday about −6% · Taiwan’s TAIEX +9.1%",
             REGULAR, 23, max_lines=1)

    stories = [
        ("#14273d", sea, (960, 182), "UKRAINE  /  LIBYA",
         "KYIV CLAIMS WARSHIP HIT OFF LIBYA",
         "Kyiv says sea drones hit a Russian ship near Benghazi."),
        ("#294e51", pharma, None, "PHARMA  /  DEALS",
         "SANOFI TO BUY INSMED FOR $41BN",
         "Cash deal values Insmed at $175 a share."),
        ("#392f48", court, None, "JUSTICE  /  MYANMAR",
         "14 NATIONS BACK ROHINGYA RULING",
         "They recognise the ICJ’s genocide finding."),
        ("#151e39", orbit, None, "SPACE  /  CHINA",
         "SHENZHOU-24 HEADS TO TIANGONG",
         "Pakistani crew member is station’s first foreign astronaut."),
    ]
    for index, (background, paint, native_size, section, headline, subline) in enumerate(stories):
        x = (32, 520)[index % 2]
        y = (431, 638)[index // 2]
        illustration(page, x, y, 472, 90, background, paint, native_size)
        draw.rectangle((x, y, x + 471, y + 193), outline=RULE)
        fit_text(draw, (x + 13, y + 100, x + 459, y + 116),
                 section, BOLD, 15, RED, max_lines=1)
        fit_text(draw, (x + 13, y + 128, x + 459, y + 161),
                 headline, BOLD, 26, max_lines=1)
        fit_text(draw, (x + 13, y + 164, x + 459, y + 186),
                 subline, REGULAR, 18, max_lines=1)

    draw.rectangle((32, 846, 991, 962), outline=RULE)
    fit_text(draw, (46, 856, 978, 871), "ALSO TODAY", BOLD, 15, RED, max_lines=1)
    fit_text(draw, (46, 880, 978, 905),
             "Zaporizhzhia strike: 2 killed, 48 wounded  ·  Nepal: 5.6 quake  ·  Senegal: AFCON title restored",
             BOLD, 22, max_lines=1)
    draw.rectangle((32, 917, 991, 962), fill=NAVY)
    fit_text(draw, (48, 932, 976, 952),
             "MARKETS   ·   TAIEX +9.1%   ·   KOSPI +7%   ·   Nikkei +3.9%   ·   S&P −0.5%   ·   Nasdaq −1.5%",
             BOLD, 21, WHITE, max_lines=1)

    draw.line((32, 981, 991, 981), fill=RED, width=2)
    fit_text(draw, (32, 991, 992, 1012), "One day, one picture · 24 November 2026",
             REGULAR, 17, max_lines=1, center=True)
    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
