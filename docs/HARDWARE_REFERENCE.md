# IC-7000 Hardware Reference

## Radio Photos & Connector Locations

### Rear Panel
![IC-7000 Rear Panel](https://www.rigpix.com/icom/ic7000_back_lrg.jpg)

*Source: [RigPix IC-7000](https://www.rigpix.com/icom/ic7000.htm)*

### Front Panel (with head attached)
![IC-7000 Front](https://www.rigpix.com/icom/ic7000_lrg.jpg)

*Source: [RigPix IC-7000](https://www.rigpix.com/icom/ic7000.htm)*

---

## Rear Panel Connector Map

Looking at the rear panel left-to-right:

```
┌──────────────────────────────────────────────────────────────────────┐
│                        IC-7000 REAR PANEL                            │
│                        (looking at back of radio)                    │
│                                                                      │
│  ┌─────┐  ┌─────┐  ┌───┐ ┌───┐ ┌────┐ ┌────┐ ┌────┐ ┌───┐ ┌────┐ │
│  │ ANT │  │ ANT │  │GND│ │DC │ │KEY │ │ACC │ │DATA│ │MIC│ │VOUT│ │
│  │  1  │  │  2  │  │   │ │13V│ │3.5 │ │13p │ │6p  │ │8p │ │RCA │ │
│  │SO239│  │SO239│  │win│ │Mol│ │mono│ │DIN │ │DIN │ │   │ │    │ │
│  └─────┘  └─────┘  └───┘ └───┘ └────┘ └────┘ └────┘ └───┘ └────┘ │
│                                                                      │
│  ┌────┐ ┌──────┐ ┌────┐ ┌────┐                                     │
│  │RTTY│ │REMOTE│ │TUNR│ │EXSP│                                     │
│  │3.5 │ │ 3.5  │ │ 4p │ │3.5 │                                     │
│  │mono│ │ mono │ │    │ │    │                                     │
│  └────┘ └──────┘ └────┘ └────┘                                     │
│           ▲                                                          │
│           │                                                          │
│        CI-V PORT                                                     │
│     (this is what                                                    │
│      we connect to)                                                  │
└──────────────────────────────────────────────────────────────────────┘
```

### Connector Details

| Label | Connector | Function | Used in this project? |
|-------|-----------|----------|-----------------------|
| ANT 1 | SO-239 | HF/6m antenna | No |
| ANT 2 | SO-239 | VHF/UHF antenna | No |
| GND | Wing nut | Chassis ground | Yes (common ground) |
| DC 13.8V | Molex 4-pin | Power input | No (existing power cable) |
| KEY | 3.5mm stereo | CW keyer paddle | No |
| ACC | 13-pin DIN | Accessory (TNC, amp) | No |
| DATA | 6-pin mini-DIN | Digital modes (TNC) | No |
| MIC | 8-pin | Microphone | No |
| VOUT | RCA | Video output to monitor | No (no head = no video) |
| RTTY | 3.5mm mono | FSK RTTY | No |
| **REMOTE** | **3.5mm mono** | **CI-V control** | **YES — ESP32 connects here** |
| TUNER | 4-pin | AH-4 auto-tuner | No |
| EXT SP | 3.5mm stereo | External speaker | No |

---

## CI-V Jack (REMOTE) — 3.5mm Mono

```
        ┌───────────────┐
        │   3.5mm MONO  │
        │   PLUG        │
        │               │
   TIP ─┤  ●            │─── CI-V Data (bidirectional)
        │               │
SLEEVE ─┤  ═════════════│─── Ground
        │               │
        └───────────────┘
```

**TIP** = CI-V data line (open-drain, TTL levels, half-duplex)
**SLEEVE** = Ground

---

## 10-Pin Head Connector (Front of Main Body)

When the head is removed, you see 10 pogo pins arranged in a row on the front of the main body.

```
    IC-7000 MAIN BODY (head removed, looking at front)
    ┌─────────────────────────────────────────┐
    │                                         │
    │     ○  ○  ○  ○  ○  ○  ○  ○  ○  ○      │
    │     1  2  3  4  5  6  7  8  9  10      │
    │                                         │
    │     └──────── 10 pogo pins ────────┘    │
    │                                         │
    └─────────────────────────────────────────┘

    Pin numbering: left-to-right when looking at the front
    of the main body with the radio right-side up.
```

### Expected Pin Functions (verify with multimeter)

Based on the IC-7000 service manual and the power-on circuit analysis:

| Pin | Expected Function | Voltage (radio off, DC connected) |
|-----|-------------------|-----------------------------------|
| ? | GND | 0V |
| ? | GND | 0V |
| ? | +13.8V (head power) | ~13.8V |
| ? | +5V or +3.3V (logic) | 3.3V or 5V |
| ? | **PWRK (power on)** | **~3.3V (pullup)** |
| ? | Serial data (head↔body) | Varies |
| ? | Serial clock | Varies |
| ? | Composite video out | Fluctuating |
| ? | Audio | Varies |
| ? | Speaker return | 0V or floating |

### How to Identify PWRK

1. Connect DC power to the radio (13.8V)
2. Do NOT connect the head
3. Multimeter on DC volts, black probe on chassis GND
4. Probe each of the 10 pins
5. Find the one reading ~3.3V — this is likely PWRK
6. Momentarily short that pin to GND with a jumper wire
7. If the relay clicks and fans spin — **that's PWRK**
8. Mark it!

**Important:** The +13.8V pin will also be live. Don't short that to ground.

---

## OPC-1443 Separation Cable Reference

The original separation cable (OPC-1443) is a 3.5m cable with 10-pin connectors on both ends. It carries all signals between the head and body.

For this project, we only need two pins from this connector:
- **PWRK** — momentary ground to power on
- **GND** — ground reference

Everything else (display, buttons, encoder) is replaced by the ESP32 + CI-V.

### 3D Printable Connector

A 3D-printable connector for the OPC-1443 pogo pins is available:
- [Thingiverse: IC7000 OPC-1443 connector by IN3EOV](https://www.thingiverse.com/thing:4583814)
- [Thingiverse: IC7000 OPC-1443 connector by duk3luk3](https://www.thingiverse.com/thing:5329707)

These can be useful for making a clean connection to just the PWRK and GND pins.

---

## ACC Socket Pinout (13-pin DIN)

For reference — not used in this project, but useful for future expansion:

```
        ┌───────────┐
       ╱  8  7  6  5 ╲
      │  9  10 11 12 13│
       ╲   1  2  3  4 ╱
        └───────────┘
```

| Pin | Function |
|-----|----------|
| 1 | RTTY (FSK) |
| 2 | GND |
| 3 | SEND (TX trigger) |
| 4 | MOD (modulation in) |
| 5 | AF OUT (audio out) |
| 6 | SQUELCH open |
| 7 | N/C |
| 8 | +13.8V (200mA max) |
| 9-13 | Various |

---

## DATA Socket Pinout (6-pin mini-DIN)

```
      ┌─────┐
     ╱ 5   6 ╲
    │ 3   4   │
     ╲ 1   2 ╱
      └─────┘
```

| Pin | Function |
|-----|----------|
| 1 | DATA IN (1200 bps) |
| 2 | GND |
| 3 | PTT |
| 4 | DATA OUT (1200 bps) |
| 5 | AF OUT |
| 6 | SQUELCH |

---

## Microphone Connector Pinout (8-pin)

```
      ┌───────┐
     ╱ 6 7  8 ╲
    │ 3  4  5  │
     ╲  1  2  ╱
      └───────┘
```

| Pin | Function |
|-----|----------|
| 1 | +8V |
| 2 | UP/DOWN |
| 3 | AF (mic audio) |
| 4 | PTT |
| 5 | GND |
| 6 | MIC sense (HM-151 detect) |
| 7 | N/C |
| 8 | SQL open |

---

## Power Requirements

| Parameter | Value |
|-----------|-------|
| Input voltage | 13.8V DC ±15% |
| RX current | ~1.2A |
| TX current (100W) | ~20A |
| Connector | Molex 4-pin |
| Fuse | 30A (in DC cable) |

**Note:** The radio is very sensitive to voltage below 13V. Ensure clean, stable 13.8V power.
