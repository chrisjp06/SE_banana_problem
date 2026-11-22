"""Render saved command output as compact, readable terminal evidence panels."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
LOGS = ROOT / "deliverables" / "logs"
OUTPUT = ROOT / "deliverables" / "screenshots"
FONT_FILE = r"C:\Windows\Fonts\consola.ttf"
FONT = ImageFont.truetype(FONT_FILE, 23)
TITLE_FONT = ImageFont.truetype(FONT_FILE, 19)


def render(log_name: str, image_name: str, heading: str) -> None:
    source_lines = (LOGS / log_name).read_text(encoding="utf-8").splitlines()
    lines = []
    for line in source_lines:
        while len(line) > 108:
            lines.append(line[:108])
            line = line[108:]
        lines.append(line)

    width, top, row_height = 1500, 68, 32
    height = top + 28 + max(len(lines), 1) * row_height
    image = Image.new("RGB", (width, height), "#101820")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 52), fill="#263445")
    for x, color in ((20, "#f87171"), (44, "#fbbf24"), (68, "#34d399")):
        draw.ellipse((x, 19, x + 13, 32), fill=color)
    draw.text((100, 15), heading, font=TITLE_FONT, fill="#f3f4f6")

    y = top
    for line in lines:
        highlight = any(token in line.lower() for token in ("passed", "100%", "result:", "approved", "throughput:"))
        draw.text((28, y), line, font=FONT, fill="#86efac" if highlight else "#d1d5db")
        y += row_height
    image.save(OUTPUT / image_name)


render("buggy_processor_output.txt", "01_buggy_processor.png", "Original processor.py - valid sample run")
render("fuzz_failure_summary.txt", "02_hypothesis_failures.png", "Hypothesis findings - original processor.py")
render("fixed_processor_output.txt", "03_fixed_processor.png", "Fixed processor.py - valid sample run")
render("fixed_processor_invalid_output.txt", "04_fixed_invalid_inputs.png", "Fixed processor.py - malformed input handling")
render("fuzz_passes.txt", "05_hypothesis_passes.png", "Hypothesis rerun - fixed processor.py")
