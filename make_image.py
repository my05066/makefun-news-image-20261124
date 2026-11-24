"""Draw the 24 November newspaper front page using Pillow."""
from math import cos, pi, sin
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
    draw.rectangle((0, 61, 959, 181), fill="#193b51")
    draw.ellipse((145, 15, 211, 81), fill="#bd7867")
    draw.rectangle((0, 75, 959, 181), fill="#214a5e")
    draw.rectangle((0, 104, 959, 181), fill="#153447")
    for index in range(55):
        x = (index * 137) % 920
        y = 80 + (index * 41) % 100
        draw.line((x, y, x + 12 + index % 25, y), fill="#2d596c", width=2)

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
        draw.line((x - 41, y + 8, x + 10, y + 2), fill="#94c1c4", width=2)
        draw.polygon([(x, y - 5), (x + 27, y - 8), (x + 38, y - 4),
                      (x + 23, y + 4), (x + 5, y + 5)], fill="#cad8d6")
        draw.rectangle((x + 9, y - 8, x + 19, y - 4), fill="#6d939c")

    for outer, inner, color in [(43, 16, "#ec753d"), (25, 10, "#ffd08a")]:
        points = []
        for index in range(16):
            angle = index * pi / 8
            radius = outer if index % 2 == 0 else inner
            points.append((658 + radius * cos(angle), 83 + radius * sin(angle)))
        draw.polygon(points, fill=color)


def capitol(draw):
    draw.ellipse((192, 2, 282, 92), fill="#487fa5")
    draw.rectangle((0, 77, 472, 89), fill="#386484")
    draw.pieslice((201, 29, 273, 96), 180, 360, fill=WHITE)
    draw.rectangle((231, 22, 243, 31), fill=WHITE)
    draw.line((237, 13, 237, 25), fill=WHITE, width=3)
    draw.rectangle((193, 62, 281, 68), fill=WHITE)
    draw.rectangle((176, 70, 298, 75), fill="#cddce4")
    for x in range(184, 293, 15):
        draw.rectangle((x, 75, x + 5, 88), fill=WHITE)
    draw.rectangle((167, 85, 307, 89), fill=WHITE)


def chip(draw):
    for index, y in enumerate(range(15, 79, 12)):
        step = index * 13
        for path in (
            [(0, y), (107 + step, y), (136 + step, 44), (213, 44)],
            [(472, y), (365 - step, y), (336 - step, 44), (260, 44)],
        ):
            draw.line(path, fill="#3a7459", width=2)
    for x in range(216, 258, 8):
        draw.line((x, 15, x, 74), fill="#b9d9a5", width=3)
    for y in range(24, 67, 8):
        draw.line((205, y, 268, y), fill="#b9d9a5", width=3)
    draw.rounded_rectangle((212, 20, 261, 69), radius=4, fill="#80bb72")
    draw.rectangle((222, 30, 251, 59), fill="#254d3f", outline="#dbecad", width=2)
    draw.rectangle((231, 39, 242, 50), fill="#a5ce78")


def satellite(draw):
    for index in range(38):
        x, y = (index * 127 + 18) % 472, (index * 31 + 4) % 88
        draw.point((x, y), fill="#bec8da")
    draw.arc((-105, 57, 359, 210), 190, 332, fill="#496486", width=2)
    draw.line((104, 59, 249, 26), fill="#bccada", width=4)
    for x, y in [(111, 46), (197, 26)]:
        draw.polygon([(x, y), (x + 48, y - 11), (x + 54, y + 9),
                      (x + 6, y + 20)], fill="#426e9e", outline="#adc0da", width=2)
        draw.line((x + 3, y + 9, x + 51, y - 1), fill="#adc0da", width=1)
    draw.ellipse((159, 29, 198, 61), fill="#bbc9d8")
    draw.pieslice((164, 14, 194, 40), 180, 360, fill=WHITE)
    for angle in (0, pi / 3, 2 * pi / 3):
        points = []
        for index in range(49):
            t = index * 2 * pi / 48
            x = 23 * cos(t)
            y = 8 * sin(t)
            points.append((359 + x * cos(angle) - y * sin(angle),
                           44 + x * sin(angle) + y * cos(angle)))
        draw.line(points, fill="#f1a977", width=2)
    draw.ellipse((356, 41, 362, 47), fill="#ffd6a9")


def skyline(draw):
    draw.ellipse((64, 14, 135, 85), fill="#d8a285")
    for index in range(24):
        x = index * 20
        y = 49 + (index * 13) % 30
        draw.rectangle((x, y, x + 17, 89), fill="#6b4d57")
    for x, y, width in [(9, 68, 64), (109, 65, 40), (177, 56, 44),
                        (252, 69, 56), (334, 58, 43), (400, 71, 67)]:
        draw.rectangle((x, y, x + width, 89), fill=NAVY)
        for window in range(x + 8, x + width - 3, 11):
            draw.rectangle((window, y + 8, window + 2, y + 10), fill="#e1ad83")
    for x in (197, 355):
        draw.pieslice((x - 12, 43, x + 12, 67), 180, 360, fill=NAVY)
        draw.line((x, 37, x, 44), fill=NAVY, width=2)
    draw.line((440, 4, 314, 40), fill="#eb9b75", width=3)
    draw.line((358, 28, 314, 40), fill="#ffe0a7", width=3)
    draw.ellipse((309, 38, 315, 42), fill=WHITE)


def gavel(draw):
    draw.line((28, 29, 57, 55), fill=WHITE, width=6)
    draw.polygon([(15, 26), (32, 9), (46, 21), (28, 38)], fill=WHITE)
    draw.line((11, 24, 29, 5), fill="#f0bfae", width=4)
    draw.line((27, 41, 48, 21), fill="#f0bfae", width=4)
    draw.rounded_rectangle((8, 52, 37, 60), radius=2, fill=WHITE)


def illustration(page, x, y, width, height, background, paint):
    art = Image.new("RGB", (width, height), background)
    paint(ImageDraw.Draw(art))
    page.paste(art, (x, y))


def main():
    page = Image.new("RGB", (1024, 1024), PAPER)
    draw = ImageDraw.Draw(page)

    draw.rectangle((32, 24, 991, 28), fill=RED)
    fit_text(draw, (32, 38, 992, 54), "THE WORLD IN ONE PICTURE",
             BOLD, 17, RED, max_lines=1, center=True)
    fit_text(draw, (40, 63, 984, 108), "TUESDAY 24 NOVEMBER 2026",
             SERIF, 56, max_lines=1, center=True)

    illustration(page, 32, 122, 960, 182, "#12273c", sea)
    draw.rectangle((32, 122, 991, 449), outline=RULE)
    fit_text(draw, (50, 316, 974, 406),
             "UKRAINE SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
             BOLD, 55)
    fit_text(draw, (50, 418, 974, 438),
             "Seven unmanned boats strike near Benghazi — a Ka-27 helicopter destroyed and cargo ship Angara hit",
             REGULAR, 19, max_lines=1)

    stories = [
        (32, 462, "#274f77", capitol,
         "DEMOCRATS WIN BIGGEST HOUSE MAJORITY IN DECADES",
         "Midterm victory lets them block Trump's agenda for his final two years"),
        (519, 462, "#193e35", chip,
         "NVIDIA BRINGS BACK JENSEN HUANG AS CEO",
         "Board reversal after Trump's push — shares jump 33%"),
        (32, 674, "#182544", satellite,
         "ALLIES WARN RUSSIA MAY LAUNCH A NUCLEAR SPACE WEAPON",
         "NATO vows space defence after reports of a launch within weeks"),
        (519, 674, "#a95e58", skyline,
         "RUSSIAN STRIKES KILL AT LEAST 15 IN KYIV REGION",
         "Leaked data puts Russia's own Ukraine death toll near 500,000"),
    ]
    for x, y, background, paint, headline, subline in stories:
        illustration(page, x, y, 473, 90, background, paint)
        draw.rectangle((x, y, x + 472, y + 199), outline=RULE)
        text_bottom = fit_text(draw, (x + 14, y + 100, x + 459, y + 155),
                               headline, BOLD, 30)
        fit_text(draw, (x + 14, text_bottom + 9, x + 459, y + 190),
                 subline, REGULAR, 18)

    draw.rectangle((32, 886, 991, 968), outline=RULE)
    illustration(page, 43, 896, 68, 63, RED, gavel)
    fit_text(draw, (126, 902, 974, 951),
             "GTA VI HACKER GETS 7 YEARS IN LONDON — WALKS FREE ON TIME SERVED",
             BOLD, 29)

    draw.line((32, 981, 991, 981), fill=RED, width=2)
    fit_text(draw, (32, 991, 992, 1012), "One day, one picture · 24 November 2026",
             REGULAR, 17, max_lines=1, center=True)
    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
