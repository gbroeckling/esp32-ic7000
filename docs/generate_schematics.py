"""Generate professional circuit schematics for ESP32-IC7000 project."""
import schemdraw
import schemdraw.elements as elm

# =============================================================================
# Schematic 1: CI-V Interface Circuit
# =============================================================================
with schemdraw.Drawing(file='images/civ_interface.svg', show=False) as d:
    d.config(fontsize=14)

    # IC-7000 CI-V jack label
    d += elm.Dot().at((0, 3))
    d += elm.Label().at((-1.5, 3)).label('IC-7000\nCI-V TIP').color('darkred')

    # Main bus line to junction
    d += elm.Line().right().length(2).at((0, 3))
    junc = d.here
    d += elm.Dot()

    # Pullup resistor to 3.3V
    d += elm.Resistor().up().at(junc).label('10kΩ', loc='right')
    d += elm.Label().label('+3.3V').color('red')

    # RX path
    d += elm.Resistor().right().at(junc).label('4.7kΩ', loc='top')
    d += elm.Line().right().length(1)
    d += elm.Label().label('GPIO4 (RX)').color('blue')

    # TX path - from junction down then right
    d += elm.Line().down().at(junc).length(2)
    txjunc = d.here
    d += elm.Diode().right().label('1N4148', loc='top')
    d += elm.Line().right().length(1)
    d += elm.Label().label('GPIO5 (TX)').color('blue')

    # Ground lines
    d += elm.Line().down().at((0, 3)).length(2)
    d += elm.Ground()
    d += elm.Label().at((-1.5, 1.5)).label('CI-V\nSLEEVE').color('darkred')

    d += elm.Line().down().at((7, 1)).length(0.5)
    d += elm.Ground()
    d += elm.Label().at((7.5, 1)).label('ESP32\nGND').color('blue')

# =============================================================================
# Schematic 2: Power-On (PWRK) Circuit
# =============================================================================
with schemdraw.Drawing(file='images/pwrk_circuit.svg', show=False) as d:
    d.config(fontsize=14)

    # PWRK source
    d += elm.Dot().at((0, 2))
    d += elm.Label().at((-1.5, 2)).label('IC-7000\nPWRK pin').color('darkred')

    # Line to MOSFET drain
    d += elm.Line().right().length(3).at((0, 2))

    # N-MOSFET
    Q = d.add(elm.AnalogNFet().anchor('drain').label('2N7000', loc='right'))

    # Gate connection
    d += elm.Line().length(2).at(Q.gate).left()
    d += elm.Label().label('GPIO6').color('blue')

    # Source to ground
    d += elm.Line().down().at(Q.source).length(1)
    d += elm.Ground()

    # Note
    d += elm.Label().at((0, -0.5)).label('Pulse GPIO6 HIGH for 200ms to toggle radio power').color('gray')

    # Pullup note
    d += elm.Label().at((-1.5, 2.8)).label('(3.3V pullup\non radio logic board)').color('gray')

# =============================================================================
# Schematic 3: Full CI-V + PWRK Combined
# =============================================================================
with schemdraw.Drawing(file='images/complete_circuit.svg', show=False) as d:
    d.config(fontsize=12)

    # === CI-V Section ===
    d += elm.Label().at((0, 7)).label('── CI-V Interface ──').color('darkred')

    d += elm.Dot().at((0, 5))
    d += elm.Label().at((-2, 5)).label('IC-7000\nREMOTE jack\n(3.5mm TIP)').color('darkred')

    # Bus line
    d += elm.Line().right().length(2).at((0, 5))
    civ_junc = d.here
    d += elm.Dot()

    # 10k pullup
    d += elm.Resistor().up().at(civ_junc).label('R1\n10kΩ', loc='right')
    d += elm.Label().label('+3.3V').color('red')

    # RX path
    d += elm.Resistor().right().at(civ_junc).label('R2  4.7kΩ', loc='top')
    rx_end = d.here
    d += elm.Line().right().length(2)
    d += elm.Label().label('ESP32-S3\nGPIO4 (RX)').color('blue')

    # TX path
    d += elm.Line().down().at(civ_junc).length(2)
    d += elm.Diode().right().label('D1  1N4148', loc='top')
    d += elm.Line().right().length(2)
    d += elm.Label().label('ESP32-S3\nGPIO5 (TX)').color('blue')

    # CI-V ground
    d += elm.Line().down().at((0, 5)).length(1)
    d += elm.Label().at((-2, 4.3)).label('SLEEVE').color('darkred')
    d += elm.Line().down().at((0, 4)).length(2.5)
    gnd1 = d.here
    d += elm.Ground()

    # === PWRK Section ===
    d += elm.Label().at((0, 1.5)).label('── Power Control ──').color('darkred')

    d += elm.Dot().at((0, 0))
    d += elm.Label().at((-2, 0)).label('IC-7000\nPWRK pin\n(10-pin hdr)').color('darkred')

    d += elm.Line().right().length(3).at((0, 0))
    Q = d.add(elm.AnalogNFet().anchor('drain').label('Q1\n2N7000', loc='right'))

    d += elm.Line().length(3).at(Q.gate).left()
    d += elm.Label().label('ESP32-S3\nGPIO6').color('blue')

    d += elm.Line().down().at(Q.source).length(1)
    d += elm.Ground()

    # ESP32 GND
    d += elm.Line().down().at((8, 3)).length(3.5)
    d += elm.Ground()
    d += elm.Label().at((8.5, 2)).label('ESP32\nGND').color('blue')

    # Common ground note
    d += elm.Label().at((4, -2.5)).label('All grounds connected (IC-7000 chassis + ESP32 GND)').color('gray')

print("Schematics generated:")
print("  docs/images/civ_interface.svg")
print("  docs/images/pwrk_circuit.svg")
print("  docs/images/complete_circuit.svg")
