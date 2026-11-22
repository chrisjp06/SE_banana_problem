"""Build the Lab 7 evidence PDF from captured and rendered command output."""

from pathlib import Path

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).parent
DEST = ROOT / "deliverables" / "Lab7_FuzzTesting_Evidence.pdf"
PAGE_W, PAGE_H = landscape(letter)

SECTIONS = [
    ("01_buggy_processor.png", "Original application run", "The starter program works for ordinary examples, but these normal inputs do not exercise its validation failures."),
    ("02_hypothesis_failures.png", "Hypothesis findings on the starter", "The property-based tests minimized malformed and missing inputs that caused crashes in each of the three functions."),
    ("03_fixed_processor.png", "Fixed application run", "The valid sample inputs continue to produce the expected rider decision, throughput, and restraint mapping."),
    ("04_fixed_invalid_inputs.png", "Fixed behavior on malformed input", "The interactive program now reports input errors cleanly instead of terminating with a Python exception."),
    ("05_hypothesis_passes.png", "Hypothesis rerun after the fix", "All three fuzz properties pass against the hardened implementation."),
]


def footer(pdf: canvas.Canvas, page: int) -> None:
    pdf.setStrokeColorRGB(0.82, 0.86, 0.9)
    pdf.line(36, 30, PAGE_W - 36, 30)
    pdf.setFont("Helvetica", 8)
    pdf.setFillColorRGB(0.3, 0.35, 0.4)
    pdf.drawString(36, 18, "Lab 7: Fuzz Testing with Hypothesis | Evidence panels rendered from saved command output")
    pdf.drawRightString(PAGE_W - 36, 18, f"Page {page}")


def cover(pdf: canvas.Canvas) -> None:
    pdf.setFillColorRGB(0.13, 0.27, 0.42)
    pdf.rect(0, PAGE_H - 145, PAGE_W, 145, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 27)
    pdf.drawString(48, PAGE_H - 72, "Lab 7: Fuzz Testing for Input Validation")
    pdf.setFont("Helvetica", 13)
    pdf.drawString(50, PAGE_H - 102, "Amusement Park Ride Access - Hypothesis findings and fix")

    pdf.setFillColorRGB(0.12, 0.16, 0.2)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(52, PAGE_H - 190, "What fuzzing found")
    findings = [
        "Rider specification parsing crashed for None, empty, and malformed height/pass values.",
        "Throughput parsing crashed for missing or malformed metrics and could divide by zero.",
        "Restraint lookup crashed for None and unknown zone prefixes.",
    ]
    pdf.setFont("Helvetica", 11)
    y = PAGE_H - 216
    for line in findings:
        pdf.drawString(64, y, "- " + line)
        y -= 22

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(52, y - 12, "Changes and result")
    pdf.setFont("Helvetica", 11)
    y -= 38
    for line in [
        "Invalid input now returns None from the helper functions; the CLI prints a clear validation message.",
        "Hypothesis checks arbitrary text and None, plus valid formats, boundary heights, invalid metrics, and known zones.",
        "Final fuzz rerun: 3 passed. The original fuzz run: 3 failed with minimized failing examples.",
    ]:
        pdf.drawString(64, y, "- " + line)
        y -= 22

    pdf.setFillColorRGB(0.35, 0.39, 0.44)
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(52, 76, "Evidence pages preserve captured PowerShell output as terminal-style images; they are not direct desktop captures.")
    footer(pdf, 1)
    pdf.showPage()


def evidence_page(pdf: canvas.Canvas, number: int, image_name: str, heading: str, description: str) -> None:
    pdf.setFillColorRGB(0.13, 0.27, 0.42)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(42, PAGE_H - 54, heading)
    pdf.setFillColorRGB(0.18, 0.21, 0.24)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(42, PAGE_H - 78, description)
    image_path = ROOT / "deliverables" / "screenshots" / image_name
    pdf.drawImage(
        ImageReader(str(image_path)), 36, 62,
        width=PAGE_W - 72, height=PAGE_H - 170,
        preserveAspectRatio=True, anchor="c", mask="auto",
    )
    footer(pdf, number)
    pdf.showPage()


def main() -> None:
    pdf = canvas.Canvas(str(DEST), pagesize=landscape(letter), pageCompression=1)
    pdf.setTitle("Lab 7 Fuzz Testing Evidence")
    pdf.setAuthor("Lab 7 Deliverables")
    cover(pdf)
    for number, (image_name, heading, description) in enumerate(SECTIONS, start=2):
        evidence_page(pdf, number, image_name, heading, description)
    pdf.save()


if __name__ == "__main__":
    main()
