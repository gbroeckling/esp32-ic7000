# Build Notes — ESP32-S3 IC-7000 Headless Controller

## Project Status
- **ESPHome custom component**: Written, not yet tested on hardware
- **Wiring**: Designed, not yet built
- **PWRK pin**: Not yet identified on the 10-pin connector
- **Radio**: IC-7000 body available, head stolen

## Critical Discovery
The IC-7000 head's ONLY role in power-on is grounding the PWRK line. No handshake, no protocol — just a wire to ground. Once powered on, CI-V gives full control. The head is not needed for any radio function after boot.

**Source**: https://www.danplanet.com/blog/2021/07/11/fixing-a-dead-icom-ic-7000/

Key quote: "To power the radio on, the control head brings the PWRK line to ground, which the CPU notices, and powers on the rest of the radio by energizing the main relay through a driver transistor."

The PWRK line has a 3.3V pullup on the logic board's regulator.

## Parts List

| Part | Value/Type | Purpose | Where to buy |
|------|-----------|---------|-------------|
| ESP32-S3 dev board | Any S3 devkit | Main controller | Amazon/AliExpress |
| R1 | 10kΩ resistor | CI-V bus pullup to 3.3V | Any electronics supplier |
| R2 | 4.7kΩ resistor | CI-V RX series protection | Any electronics supplier |
| D1 | 1N4148 signal diode | CI-V TX open-drain isolation | Any electronics supplier |
| Q1 | 2N7000 N-channel MOSFET | PWRK power-on switch | Any electronics supplier |
| J1 | 3.5mm mono plug + cable | Connects to IC-7000 CI-V jack | Any electronics supplier |
| SW1 | Momentary push button | Manual power-on backup (optional) | Any electronics supplier |

## Wiring Summary

### CI-V Interface (3.5mm REMOTE jack on rear panel)
```
3.5mm TIP ──┬── 10kΩ to +3.3V (pullup)
            ├── 4.7kΩ ── ESP32 GPIO4 (RX)
            └── 1N4148 cathode ── ESP32 GPIO5 (TX)
3.5mm SLEEVE ── GND
```

### Power-On (PWRK pin on 10-pin head connector)
```
PWRK pin ── 2N7000 DRAIN
             2N7000 GATE ── ESP32 GPIO6
             2N7000 SOURCE ── GND
```
Pulse GPIO6 HIGH for 200ms to toggle radio power.

## Finding the PWRK Pin

1. Connect DC power to radio (13.8V), no head attached
2. Multimeter on DC volts, black probe on chassis GND
3. Probe each of the 10 pogo pins on the front connector
4. Find the ~3.3V pin (pulled up by logic board) — this is PWRK
5. Briefly short it to GND — if relay clicks and fans spin, that's it
6. Mark the pin number

**Warning**: One pin carries +13.8V (head power supply). Don't short that.

**Expected pin voltages**:
- GND pins: 0V (multiple)
- PWRK: ~3.3V
- Head power: ~13.8V
- Serial data/clock: varying
- Video out: fluctuating
- Audio/speaker: 0V or floating

## CI-V Protocol Quick Reference

- **Address**: IC-7000 = 0x70, Controller = 0xE0
- **Baud**: 19200 (default, changeable in radio menu)
- **Frame**: FE FE [TO] [FROM] [CMD] [SUB] [DATA] FD
- **ACK**: FB, **NAK**: FA

### Essential Commands
| Cmd | Sub | Function |
|-----|-----|----------|
| 0x03 | — | Read frequency |
| 0x05 | — | Set frequency (5 bytes BCD, LSB first) |
| 0x04 | — | Read mode |
| 0x06 | — | Set mode (1 byte mode + 1 byte filter) |
| 0x07 | 0x00/0x01 | Select VFO A/B |
| 0x0F | — | Split ON(0x01)/OFF(0x00) |
| 0x14 | 0x01 | AF gain (0-255) |
| 0x14 | 0x02 | RF gain (0-255) |
| 0x14 | 0x03 | Squelch (0-255) |
| 0x14 | 0x0A | TX power (0-255) |
| 0x14 | 0x0B | MIC gain (0-255) |
| 0x15 | 0x02 | Read S-meter |
| 0x15 | 0x11 | Read power meter |
| 0x15 | 0x12 | Read SWR meter |
| 0x16 | 0x02 | Preamp ON/OFF |
| 0x16 | 0x12 | AGC (1=fast, 2=mid, 3=slow) |
| 0x16 | 0x22 | Noise blanker ON/OFF |
| 0x1C | 0x00 | PTT (0x00=RX, 0x01=TX) |

### Mode Codes
| 0x00=LSB | 0x01=USB | 0x02=AM | 0x03=CW | 0x04=RTTY |
| 0x05=FM | 0x06=WFM | 0x07=CW-R | 0x08=RTTY-R |

### BCD Frequency Examples
14.250.000 Hz → `00 00 25 41 00` (LSB first)
146.520.000 Hz → `00 00 20 65 41` (LSB first)
446.000.000 Hz → `00 00 00 60 44` (LSB first)

## ESPHome Configuration

### GPIO Assignments (ESP32-S3)
| GPIO | Function |
|------|----------|
| GPIO4 | UART RX (CI-V data in) |
| GPIO5 | UART TX (CI-V data out) |
| GPIO6 | PWRK power-on (via MOSFET) |

### Files
| File | Purpose |
|------|---------|
| ic7000.yaml | Main ESPHome config |
| secrets.yaml | WiFi credentials (edit before flash) |
| components/icom_civ/__init__.py | ESPHome component registration |
| components/icom_civ/icom_civ.h | CI-V protocol header |
| components/icom_civ/icom_civ.cpp | CI-V protocol implementation |
| components/icom_civ/sensor.py | Frequency/S-meter/PTT sensors |
| components/icom_civ/switch.py | PTT/Power switches |
| components/icom_civ/text_sensor.py | Mode text sensor |

### Flash Command
```bash
esphome run ic7000.yaml
```

### Access
- Web UI: http://<ESP32_IP>:80
- Home Assistant: auto-discovered via ESPHome integration
- Fallback AP: SSID "IC7000-Fallback", password "ic7000setup"

## Reference Documents (in docs/ folder)
- IC-7000_Instruction_Manual.pdf — full user manual with CI-V reference
- IC-7000_Service_Manual.pdf — schematics, board layouts, PWRK circuit
- HARDWARE_REFERENCE.md — all connector pinouts
- images/ — schematics and manual page extracts

## Key Links
- Power-on circuit: https://www.danplanet.com/blog/2021/07/11/fixing-a-dead-icom-ic-7000/
- CIVmasterLib: https://github.com/WillyIoBrok/CIVmasterLib
- CI-V hardware interface: https://werner.rothschopf.net/microcontroller/202102_arduino_antennaswitch_civ_en.htm
- ESPHome UART: https://esphome.io/components/uart/
- DM5AL SKT-7000 (reference): https://dm5al.de/?page_id=241
- 3D-printable OPC-1443 connector: https://www.thingiverse.com/thing:4583814

## IC-7000 Specs
| Spec | Value |
|------|-------|
| Frequency | HF 0.03–60 MHz, VHF 118–174 MHz, UHF 420–450 MHz |
| Modes | LSB, USB, AM, CW, RTTY, FM, WFM |
| TX power | HF: 100W, VHF: 50W, UHF: 35W |
| CI-V address | 0x70 (default) |
| CI-V baud | 19200 (default) |
| CI-V connector | 3.5mm mono jack (rear, labeled REMOTE) |
| Head connector | 10-pin pogo (front, proprietary) |
| Power | 13.8V DC, 20A TX |

## Replacement Head Sources
If you'd rather buy a replacement head than build this:
- eBay: search "IC-7000 control head" or "IC-7000 front panel"
- QRZ.com swap forum
- eHam.net classifieds
- Expect $150-250 used (radio discontinued 2012)
