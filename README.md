# Glyph MIDI Controller

A six-key USB MIDI controller built with the [PCB Cupid Glyph Mini 2040](https://learn.pcbcupid.com/) and CircuitPython. The keys send notes, three knobs control a synth, and a rotary encoder operates a 128 x 64 OLED menu. The board **does not make sound by itself**: a computer or phone app receives its MIDI messages and plays the sound.

This repository matches the [six-switch PCB design](https://spell.pcbcupid.com/explore/01a13685-d20e-7e50-fb2f-0dd55dda1933/preview), not the older five-key wiring. It is based on Adafruit's [MIDI Keyset](https://learn.adafruit.com/midi-keyset). The current `code.py` defaults to an **SSD1306, 128 x 64, I2C address 0x3C**. SH1106 is also supported by changing one setting.

## What you need

- Glyph Mini 2040 with the six-switch controller PCB, six switches, three 10 kOhm linear potentiometers, a rotary encoder with push button, and a 128 x 64 I2C OLED.
- A USB **data** cable and a Windows, Linux, or Android device with a MIDI app. VMPK is one Windows option.
- [CircuitPython 10.x for the Glyph Mini 2040](https://circuitpython.org/board/pcbcupid_glyph_mini_2040/) and the matching [10.x library bundle](https://circuitpython.org/libraries).

CircuitPython 10.3.1 and the 10.x bundle were used during the board setup described here. Use the same major version for firmware and libraries.

## Wiring at a glance

| Part | Glyph Mini 2040 pin | Other connection |
| --- | --- | --- |
| OLED SDA | GP0 | OLED VCC to 3V3, OLED GND to GND |
| OLED SCL | GP1 | I2C clock |
| Switches 1-6 | GP2, GP3, GP4, GP5, GP6, GP7 in order | Other leg of each switch to GND |
| Encoder A / B | GP8 / GP9 | Encoder common **C** to GND |
| Encoder push button S2 | GP10 | S1 to GND |
| Pot A / B / C wipers (middle legs) | GP26 / GP27 / GP28 | Outer legs to 3V3 and GND |

The switches and encoder button use the RP2040's internal pull-ups; no external pull-up resistors are needed. Use **3.3 V**, never 5 V, for the OLED and pots. If a pot turns in the opposite direction you want, swap its two outer legs.

**Encoder PCB check:** In the PCB preview, encoder `C` and button `S1` share a net. Confirm that net also reaches the Glyph's main GND. If it does not, the encoder/button needs a GND jumper. The code cannot repair a missing ground connection.

## Install on a new board

1. Download the **Glyph Mini 2040** CircuitPython 10.x `.uf2` from the board link above. Hold the board's BOOT button while connecting USB. Windows should show an `RPI-RP2` drive.
2. Copy the `.uf2` to `RPI-RP2`. The board restarts as `CIRCUITPY`. Open `CIRCUITPY/boot_out.txt` and check that the Board ID says `pcbcupid_glyph_mini_2040`.
3. Unzip the matching **10.x** CircuitPython library bundle. Copy these into `CIRCUITPY/lib/`:
   - Folders: `adafruit_midi`, `adafruit_display_text`, `adafruit_display_shapes`
   - Files: `adafruit_displayio_ssd1306.mpy`, `adafruit_displayio_sh1106.mpy`, `adafruit_debouncer.mpy`, `adafruit_ticks.mpy`, `simpleio.mpy`
4. Copy [`glyph_mini_2040_midi_keyset/code.py`](glyph_mini_2040_midi_keyset/code.py) to the **root** of `CIRCUITPY` as `code.py`. It runs automatically. You do not need to copy `main.bmp`; the OLED screen is drawn by the code.
5. Plug the board in normally, without holding BOOT. The OLED shows a short music-note animation, then the knob values and six note keys.

To update only the program later, replace `CIRCUITPY/code.py`. You do not need to flash the `.uf2` again. Keep a backup of a working `code.py` before replacing it.

### Choose the OLED type

Near the top of `code.py`, set `OLED_DRIVER` to `"SSD1306"` or `"SH1106"`. The default `OLED_ADDRESS` is `0x3C`; some modules use `0x3D`. This layout requires a **128 x 64** display. SDA remains GP0 and SCL remains GP1 for either driver. The SH1106 path includes its two-column offset.

If the serial log says `OLED found` but the picture is blank or shifted, check the driver and address. That log confirms an I2C response; it does not prove the selected display chip is correct. The MIDI controls can still run if the OLED is absent.

## Make sound with VMPK on Windows

1. Connect the Glyph normally, then open VMPK. The Glyph is a **MIDI input**, not an audio speaker. Windows may show it as `CircuitPython Audio` or another CircuitPython/USB MIDI name.
2. In VMPK's MIDI setup or Connections window, select that USB MIDI device as the **input**. Keep a working synth or MIDI **output** selected. Enable MIDI Thru if VMPK offers it.
3. Press a physical switch. Its VMPK key should light and the synth should play. A mouse click making sound proves only that VMPK's output works; it does not prove the Glyph input is selected.

If the input name is unclear, unplug the Glyph, note which MIDI input disappears, and reconnect it. Close other apps that may be holding the MIDI port while testing.

To read a CircuitPython error, open the board's USB serial port in a serial terminal at 115200 baud. On Windows it appears as a USB Serial Device COM port. Press Ctrl+C to stop `code.py` and Ctrl+D to restart it. Close the terminal before another app needs that port.

## Controls and screen

| Action | Result |
| --- | --- |
| Press a switch | Send Note On; release sends Note Off. Several keys can make a chord. |
| Turn Pot A | Modulation, MIDI CC 1. |
| Turn Pot B | Pitch bend. Centre is normal pitch. |
| Turn Pot C | Expression, MIDI CC 11. |
| Turn encoder | Move the outline between the three knobs and six keys. |
| Short press encoder | Open the selected item's edit page; press again to return. |
| In the edit page | Turn to choose a line; long press to edit; turn to change; long press to finish. |
| Double press encoder | Send All Notes Off on all 16 MIDI channels. |

The OLED shows live knob values and the six assigned notes. A pressed key fills its box while held, with a brief outline pop. The startup music-note animation lasts about 1.7 seconds. Menu edits last until the next restart; they are **not saved** to flash. To make a change permanent, edit the defaults in `code.py`.

Default notes are MIDI numbers **61, 64, 66, 68, 73, 75** for keys 1-6. Those are commonly named C#4, E4, F#4, G#4, C#5, D#5. The OLED uses a naming table starting at C-2, so its printed octave number is one lower; the MIDI note number is unchanged. Default velocity is 120 and default channel is MIDI channel 1.

## Settings you may change

| Setting in `code.py` | Default | Meaning |
| --- | --- | --- |
| `OLED_DRIVER` / `OLED_ADDRESS` | `"SSD1306"` / `0x3C` | Match your display chip and I2C address. |
| `POTS_CONNECTED` | `True` | Set `False` if pots are not wired yet; floating analog pins can send random MIDI. |
| `POT_B_PITCH_BEND` | `True` | Set `False` to make Pot B send its configured CC instead. |
| `POT_C_INSTRUMENTS` | `False` | Set `True` to select General MIDI instruments; the last zone selects drums on channel 10. |
| `POT_DEADBAND` | `2` | A knob must move more than this many steps before sending again. |
| `control_settings` | See code | Default notes, velocities, channels, pot CC numbers, and ranges. Channels are shown as 1-16 on the OLED and stored as 0-15 in code. |

The code averages eight ADC readings and ignores small changes to reduce knob jitter. Pot A/B/C are on GP26/GP27/GP28. `OLED_CONTRAST` applies to the SH1106 path; SSD1306 uses its driver default.

## Troubleshooting

| Symptom | First check |
| --- | --- |
| Only `RPI-RP2` appears | Release BOOT and press RESET without touching BOOT. If it stays in bootloader mode, reinstall the correct board `.uf2`. |
| `CIRCUITPY` appears but no MIDI input | Check `boot_out.txt`, then open the CircuitPython serial console for a `code.py` error. Confirm the `lib` files and folders above are present. |
| VMPK mouse keys sound, physical keys do nothing | Select the Glyph as VMPK **MIDI input** and enable MIDI Thru. Check that the board's serial console prints key presses. |
| Only some switches work | With power off, check each switch closes its GPIO to GND only while pressed. The PCB pins are GP2-GP7 in switch order. |
| OLED blank or wrong image | Check 3V3/GND, SDA GP0, SCL GP1, driver type, and `0x3C` versus `0x3D`. |
| Encoder does not work | Check GP8/GP9/GP10 and that encoder common `C` and button `S1` reach GND. |
| Knobs jump without touching them | Confirm 3V3, GND, and the wiper connections at GP26-GP28; then try `POT_DEADBAND = 3`. |

## Repository files

- `glyph_mini_2040_midi_keyset/code.py` - the file to copy to `CIRCUITPY`.
- `docs/Glyph_Mini_2040_MIDI_Keyset.pdf` - printable quick-start and wiring reference.
- `docs/build_guide.py` - rebuilds that PDF with `python docs/build_guide.py` after installing `reportlab`; it is not copied to the board.
- `README.md` - the complete beginner setup and use guide.

## Tiny glossary

- **GPIO / GP:** a numbered electrical pin on the Glyph Mini 2040.
- **MIDI:** messages such as "play note 61"; a synth app turns them into sound.
- **CC (Control Change):** a MIDI message often used for knob positions.
- **I2C:** the two-wire connection used by the OLED (SDA and SCL).
- **UF2:** the CircuitPython firmware file copied to `RPI-RP2` during first setup.
