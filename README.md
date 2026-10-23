# Glyph-MIDI-Controller

Board: PCB Cupid Glyph Mini 2040 (RP2040) — https://learn.pcbcupid.com/

A USB MIDI controller: 5 MX keys play notes, 3 knobs send modulation / pitch bend / expression, and a rotary encoder drives an OLED menu to change each key's note, velocity and channel. It shows up as the MIDI device **Glyph Mini 2040**, no drivers needed, on a laptop or (with an OTG cable) a phone. The board makes no sound itself: an app such as FluidSynth, VMPK, LMMS or G-Stomper plays it.

Based on Adafruit's [MIDI Keyset](https://learn.adafruit.com/midi-keyset) (CircuitPython, MIT), adapted to this board.

## Sketches
- `glyph_mini_2040_midi_keyset/` — **LATEST** `code.py` + `main.bmp` (the OLED main screen). Keys, encoder menu, SH1106 OLED and 3 pots. Pot readings are averaged over 8 samples, ignore moves of 2 steps or less and snap to 0/127 at the ends, so a knob left alone sends nothing. Without the OLED it still works as a MIDI keyboard.

Full documentation with wiring drawings: [`docs/Glyph_Mini_2040_MIDI_Keyset.pdf`](docs/Glyph_Mini_2040_MIDI_Keyset.pdf).

## Key wiring (MX switches)
| Key | Glyph Mini 2040 | Note |
|---|---|---|
| Key 1 | GP0 | 61 (C#4) |
| Key 2 | GP1 | 64 (E4) |
| Key 3 | GP2 | 66 (F#4) |
| Key 4 | GP3 | 68 (G#4) |
| Key 5 | GP4 | 73 (C#5) |

The other leg of every switch goes to GND. No resistors: the internal pull-ups are used. The OLED shows the notes one octave lower (C#3 for 61) because Adafruit's code counts octaves from C-2.

## Rotary encoder wiring
| Encoder | Glyph Mini 2040 |
|---|---|
| A (outer pin, 3-pin side) | GP14 |
| Common (middle pin) | GND |
| B (outer pin, 3-pin side) | GP15 |
| Switch (2-pin side) | GP8 and GND |

Turning the wrong way: swap the GP14 and GP15 wires.

## OLED wiring (SH1106 1.3", 128x64, I2C 0x3C)
| OLED | Glyph Mini 2040 |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | GP6 |
| SCL | GP7 |

GP6/GP7 is an I2C1 pair; the RP2040 can't swap SDA and SCL in software, so a swapped pair is not found. GP8/GP9 (the board's SDA/SCL labels) aren't used because GP8 is the encoder button.

## Potentiometer wiring (10 kΩ linear)
| Knob | Wiper (middle leg) | Outer legs | Sends |
|---|---|---|---|
| Pot A | GP29 | 3.3V and GND | CC 1, modulation |
| Pot B | GP28 | 3.3V and GND | pitch bend (middle of the pot = no bend) |
| Pot C | GP27 | 3.3V and GND | CC 11, expression |

Only GP26–GP29 read analog voltages. The GND end reads 127 and the 3.3V end 0; swap a pot's outer legs to reverse it. Never use 5V on any of these pins.

## Install
1. Install CircuitPython 10.x for the board: [circuitpython.org/board/pcbcupid_glyph_mini_2040](https://circuitpython.org/board/pcbcupid_glyph_mini_2040/). Hold BOOT while plugging in USB, then copy the `.uf2` onto the `RPI-RP2` drive; the board comes back as `CIRCUITPY`.
2. From the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) (10.x), copy into `CIRCUITPY/lib/`:
   `adafruit_midi/`, `adafruit_display_text/`, `adafruit_display_shapes/`, `adafruit_imageload/`, `adafruit_displayio_sh1106.mpy`, `adafruit_displayio_ssd1306.mpy`, `adafruit_debouncer.mpy`, `adafruit_ticks.mpy`, `simpleio.mpy`.
   Or with circup: `circup install adafruit_midi adafruit_display_text adafruit_display_shapes adafruit_imageload adafruit_displayio_sh1106 adafruit_displayio_ssd1306 adafruit_debouncer simpleio`
3. Copy `glyph_mini_2040_midi_keyset/code.py` and `main.bmp` to the root of `CIRCUITPY`. The board restarts by itself every time `code.py` is saved.

Tested with CircuitPython 10.3.1 (Glyph Mini 2040 build) and the 10.x library bundle.

## Controls
| Control | Action |
|---|---|
| Keys | play notes (hold several for a chord) |
| Turn encoder | move the outline between the 3 knob circles and 5 key boxes |
| Short press | open the selected item's edit screen; again = back |
| In the edit screen | turn = pick a line, long press = edit it, turn = change, long press = done |
| Double press | MIDI all notes off (CC 123) |

Edits made on the board are lost at restart; the defaults are in `code.py`.

## MIDI messages (channel 1)
| Control | Message |
|---|---|
| Keys | Note On / Note Off, velocity 120 |
| Pot A | CC 1 (modulation), 0–127 |
| Pot B | Pitch bend, full range |
| Pot C | CC 11 (expression), 0–127 |
| Encoder double press | CC 123 (all notes off) |

## Settings (top of `code.py`)
| Setting | Default | Meaning |
|---|---|---|
| `POTS_CONNECTED` | `True` | `False` silences the pots (use it while they aren't wired: floating pins send random values) |
| `POT_B_PITCH_BEND` | `True` | `False` = Pot B sends its CC number instead |
| `POT_C_INSTRUMENTS` | `False` | `True` = Pot C picks instruments (Program Change; last position = drums on channel 10) |
| `POT_DEADBAND` | `2` | steps a knob must move before it sends; raise to 3 if a knob jitters |
| `OLED_DRIVER`, `OLED_ADDRESS` | `"SH1106"`, `0x3C` | `"SSD1306"` / `0x3D` for Adafruit's own OLED |
| `OLED_SDA`, `OLED_SCL` | `board.GP6`, `board.GP7` | display pins |
| `OLED_CONTRAST` | `0xFF` | display brightness |

## Playing it
- **Linux laptop:** `fluidsynth -a pulseaudio -m alsa_seq /usr/share/sounds/sf2/FluidR3_GM.sf2` and, in a second terminal, `aconnect "Glyph Mini 2040" "FLUID Synth"`. `aseqdump -p "Glyph Mini 2040"` shows every message the board sends.
- **VMPK / LMMS:** select **Glyph Mini 2040** as MIDI input (ALSA). In LMMS, set Edit → Settings → MIDI to ALSA-Sequencer first.
- **Android:** USB-C OTG cable, then pick Glyph Mini 2040 as the MIDI input (e.g. G-Stomper). Keys, modulation and pitch bend work straight away; expression (CC 11) may need the app's MIDI Learn.

## Troubleshooting
- **Nothing works, no MIDI device:** the board started in safe mode because BOOT was held. Press RESET without touching BOOT.
- **"No OLED at 0x3c … No pull up found":** an OLED wire isn't touching its pin; reseat or solder SDA/SCL.
- **Pot reads a steady ~0.5 V and ignores turning:** the wiper isn't reaching the Glyph pad. Measure at the pad, not at the pot.
- **Encoder and its button both dead:** the encoder common pin or the switch isn't on GND.
- Most problems while building this were a wire not reaching its pad, so check contact before the code.
