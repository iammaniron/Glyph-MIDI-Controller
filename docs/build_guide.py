"""Build the printable guide. Requires: pip install reportlab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "Glyph_Mini_2040_MIDI_Keyset.pdf"
INK = colors.HexColor("#183038")
TEAL = colors.HexColor("#087F72")
PALE = colors.HexColor("#EAF6F3")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"],
                          fontName="Helvetica-Bold", fontSize=21,
                          leading=25, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="SubCustom", parent=styles["Normal"],
                          fontSize=10, leading=15, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle(name="HeadingCustom", parent=styles["Heading2"],
                          fontSize=12, leading=15, textColor=TEAL,
                          spaceBefore=13, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["Normal"],
                          fontSize=9, leading=13, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="SmallCustom", parent=styles["Normal"],
                          fontSize=8, leading=11, textColor=INK))
styles.add(ParagraphStyle(name="HeaderCell", parent=styles["SmallCustom"],
                          textColor=colors.white, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CenterCustom", parent=styles["SmallCustom"],
                          alignment=TA_CENTER))


def p(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def section(title, *paragraphs):
    return KeepTogether([p(title, "HeadingCustom"), *(p(x) for x in paragraphs)])


def table(headers, rows, widths):
    data = [[p(cell, "HeaderCell") for cell in headers]]
    data += [[p(cell, "SmallCustom") for cell in row] for row in rows]
    result = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, TEAL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return result


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.line(17 * mm, 17 * mm, 193 * mm, 17 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK)
    canvas.drawString(17 * mm, 12 * mm, "Glyph Mini 2040 MIDI Controller - beginner guide")
    canvas.drawRightString(193 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


story = [
    p("Glyph Mini 2040<br/>MIDI Controller", "TitleCustom"),
    p("Six keys, three knobs, an encoder, and a 128 x 64 OLED. The board sends USB MIDI; your computer or phone app makes the sound.", "SubCustom"),
    section("1. What you need",
            "Glyph Mini 2040 and the six-switch PCB; six switches; three 10 kOhm linear pots; an encoder with push button; a 128 x 64 I2C OLED; and a USB data cable.",
            "Download CircuitPython 10.x for the PCB Cupid Glyph Mini 2040 and the matching 10.x CircuitPython library bundle. The board setup was checked with CircuitPython 10.3.1."),
    p("2. Wiring", "HeadingCustom"),
    table(["Part", "GPIO", "Also connect"], [
        ["OLED SDA / SCL", "GP0 / GP1", "VCC to 3V3; GND to GND"],
        ["Switches 1-6", "GP2 through GP7", "Other leg of each to GND"],
        ["Encoder A / B", "GP8 / GP9", "Common C to GND"],
        ["Encoder button S2", "GP10", "S1 to GND"],
        ["Pot A / B / C wipers", "GP26 / GP27 / GP28", "Outer legs to 3V3 and GND"],
    ], [175, 105, 225]),
    Spacer(1, 6),
    p("<b>Use 3.3 V, never 5 V.</b> The encoder C and S1 share a PCB net. Check that this net reaches main GND; add a GND jumper if your board does not connect it.", "SmallCustom"),
    p("3. Install CircuitPython and code", "HeadingCustom"),
    p("<b>1.</b> Hold BOOT while connecting USB. Copy the board-specific CircuitPython 10.x .uf2 to RPI-RP2. The board should restart as CIRCUITPY."),
    p("<b>2.</b> Check CIRCUITPY/boot_out.txt for Board ID: pcbcupid_glyph_mini_2040."),
    p("<b>3.</b> Put these folders in CIRCUITPY/lib: adafruit_midi, adafruit_display_text, adafruit_display_shapes. Add these files: adafruit_displayio_ssd1306.mpy, adafruit_displayio_sh1106.mpy, adafruit_debouncer.mpy, adafruit_ticks.mpy, simpleio.mpy."),
    p("<b>4.</b> Copy glyph_mini_2040_midi_keyset/code.py to the root of CIRCUITPY as code.py. No main.bmp is needed. Later code changes require only replacing code.py, not reflashing the .uf2."),
    p("4. OLED choice", "HeadingCustom"),
    p("The code defaults to <b>SSD1306 at 0x3C</b>. For an SH1106, set OLED_DRIVER = \"SH1106\" near the top of code.py. If your 128 x 64 module uses address 0x3D, change OLED_ADDRESS to 0x3D. SDA is always GP0 and SCL is always GP1."),
    p("5. Make sound on Windows", "HeadingCustom"),
    p("Open VMPK's MIDI setup, choose the Glyph/CircuitPython USB MIDI device as <b>input</b>, keep a working synth as <b>output</b>, and enable MIDI Thru if offered. A mouse click making sound tests only the output. Press a physical switch to test the input."),
    PageBreak(),
    p("6. Controls", "HeadingCustom"),
    table(["Control", "Result"], [
        ["Six switches", "Notes 61, 64, 66, 68, 73, 75; press = Note On, release = Note Off"],
        ["Pot A / B / C", "Modulation CC1 / pitch bend / expression CC11"],
        ["Turn encoder", "Move the OLED selection among three pots and six keys"],
        ["Short press", "Enter selected edit page; press again to leave"],
        ["Long press in edit", "Start or finish changing the selected value"],
        ["Double press", "All Notes Off on every MIDI channel"],
    ], [145, 360]),
    Spacer(1, 6),
    p("The startup music-note animation lasts about 1.7 seconds. Menu edits reset when the board restarts; change defaults in code.py to keep them.", "SmallCustom"),
    p("7. First checks when something fails", "HeadingCustom"),
    table(["What you see", "Check"], [
        ["RPI-RP2, not CIRCUITPY", "Release BOOT, tap RESET, then reinstall the correct .uf2 if needed."],
        ["CIRCUITPY but no MIDI", "Read the serial console for a code.py error; verify the lib folders/files."],
        ["VMPK mouse works, board keys do not", "Select the board as MIDI input; enable MIDI Thru; check serial key prints."],
        ["OLED blank or shifted", "Check 3V3/GND, GP0/GP1, SSD1306 vs SH1106, and 0x3C vs 0x3D."],
        ["Encoder dead", "Check GP8/GP9/GP10 and that common C/S1 reaches GND."],
        ["Knobs jitter", "Check wipers at GP26-GP28, 3V3/GND, then try POT_DEADBAND = 3."],
    ], [190, 315]),
    Spacer(1, 12),
    p("Full instructions, current code, and PCB link: github.com/pcbcupid/Glyph-MIDI-Controller", "CenterCustom"),
    p("Original project documentation: @Dinesh v (2026). Updated for the six-key PCB and current firmware.", "CenterCustom"),
]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=17 * mm,
                        rightMargin=17 * mm, topMargin=17 * mm,
                        bottomMargin=23 * mm, title="Glyph Mini 2040 MIDI Controller")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
