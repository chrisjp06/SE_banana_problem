"""Render the captured terminal transcripts as readable PNG evidence sheets."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUT = ROOT / "deliverables" / "screenshots"
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT = ImageFont.truetype(FONT_PATH, 17)
SMALL = ImageFont.truetype(FONT_PATH, 14)


def render(sources: tuple[str, ...], target: str, heading: str) -> None:
    lines = []
    for source in sources:
        lines.extend((ROOT / "deliverables" / source).read_text(encoding="utf-8").splitlines())
    width, margin, line_height = 1400, 32, 24
    wrapped = []
    for line in lines:
        while len(line) > 135:
            wrapped.append(line[:135])
            line = line[135:]
        wrapped.append(line)
    height = 84 + margin + len(wrapped) * line_height
    image = Image.new("RGB", (width, height), "#101820")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 54), fill="#1f2937")
    draw.ellipse((18, 19, 30, 31), fill="#f87171")
    draw.ellipse((40, 19, 52, 31), fill="#fbbf24")
    draw.ellipse((62, 19, 74, 31), fill="#34d399")
    draw.text((95, 17), heading, font=SMALL, fill="#e5e7eb")
    y = 70
    for line in wrapped:
        color = "#86efac" if any(tag in line for tag in ("passed", "100%", "TOTAL")) else "#d1d5db"
        draw.text((margin, y), line, font=FONT, fill=color)
        y += line_height
    image.save(OUT / target)


render(("coverage_code_terminal.txt", "coverage_code_report.txt"),
       "code_coverage_terminal.png", "Lab 6 - Code Coverage Run")
render(("coverage_branch_terminal.txt", "coverage_branch_report.txt"),
       "branch_coverage_terminal.png", "Lab 6 - Branch Coverage Run")
