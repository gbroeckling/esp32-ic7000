"""Generate professional circuit schematics for ESP32-IC7000 project."""
import schemdraw
import schemdraw.elements as elm

schemdraw.config(bgcolor='white')

# =============================================================================
# Schematic 1: CI-V Interface Circuit
# =============================================================================
with schemdraw.Drawing(file='images/civ_interface.png', show=False, dpi=150) as d:
    d.config(fontsize=14, color='black')

    # IC-7000 CI-V jack label
    d += elm.Dot().at((0, 3))
    d += elm.Label().at((-1.8, 3)).label('IC-7000\nCI-V TIP').color('darkred')

    # Bus line to junction
    d += elm.Line().right().length(2).at((0, 3))
    d += elm.Dot()

    # 10k pullup to 3.3V
    d += elm.Resistor().up().at((2, 3)).label('R1\n10kΩ', loc='right')
    d += elm.Label().label('+3.3V').color('red')

    # RX path
    d += elm.Resistor().right().at((2, 3)).label('R2  4.7kΩ', loc='top')
    d += elm.Line().right().length(1.5)
    d += elm.Label().label('ESP32 GPIO4\n(UART RX)').color('blue')

    # TX path
    d += elm.Line().down().at((2, 3)).length(2)
    d += elm.Diode().right().label('D1  1N4148', loc='top')
    d += elm.Line().right().length(1.5)
    d += elm.Label().label('ESP32 GPIO5\n(UART TX)').color('blue')

    # CI-V ground
    d += elm.Line().down().at((0, 3)).length(2)
    d += elm.Ground()
    d += elm.Label().at((-1.8, 1.5)).label('CI-V\nSLEEVE\n(GND)').color('darkred')

    # ESP32 ground
    d += elm.Line().down().at((7, 1)).length(0.5)
    d += elm.Ground()
    d += elm.Label().at((8, 0.8)).label('ESP32 GND').color('blue')

# =============================================================================
# Schematic 2: Power-On (PWRK) Circuit
# =============================================================================
with schemdraw.Drawing(file='images/pwrk_circuit.png', show=False, dpi=150) as d:
    d.config(fontsize=14, color='black')

    # PWRK source
    d += elm.Dot().at((0, 2))
    d += elm.Label().at((-2, 2)).label('IC-7000\nPWRK pin').color('darkred')

    # Pullup note
    d += elm.Resistor().up().at((0, 2)).label('Internal\n3.3V pullup\n(on radio)', loc='right')
    d += elm.Label().label('+3.3V').color('red')

    # Line to MOSFET drain
    d += elm.Line().right().length(3).at((0, 2))

    # N-MOSFET
    Q = d.add(elm.AnalogNFet().anchor('drain').label('Q1\n2N7000', loc='right'))

    # Gate to ESP32
    d += elm.Line().length(2.5).at(Q.gate).left()
    d += elm.Label().label('ESP32\nGPIO6').color('blue')

    # Source to ground
    d += elm.Line().down().at(Q.source).length(1)
    d += elm.Ground()

# =============================================================================
# Schematic 3: Full System Combined
# =============================================================================
with schemdraw.Drawing(file='images/complete_circuit.png', show=False, dpi=150) as d:
    d.config(fontsize=11, color='black')

    # ===== CI-V Section =====
    # Label
    d += elm.Label().at((-2, 8)).label('IC-7000 REMOTE Jack (3.5mm)').color('darkred')

    # CI-V tip
    d += elm.Dot().at((0, 7))
    d += elm.Label().at((-1, 7)).label('TIP').color('darkred')
    d += elm.Line().right().length(2).at((0, 7))
    d += elm.Dot()

    # Pullup
    d += elm.Resistor().up().at((2, 7)).label('10kΩ', loc='right')
    d += elm.Label().label('+3.3V').color('red')

    # RX
    d += elm.Resistor().right().at((2, 7)).label('4.7kΩ', loc='top')
    d += elm.Line().right().length(2)
    d += elm.Label().label('GPIO4 (RX)').color('blue')

    # TX
    d += elm.Line().down().at((2, 7)).length(2)
    d += elm.Diode().right().label('1N4148', loc='top')
    d += elm.Line().right().length(2)
    d += elm.Label().label('GPIO5 (TX)').color('blue')

    # CI-V GND
    d += elm.Line().down().at((0, 7)).length(2.5)
    d += elm.Ground()
    d += elm.Label().at((-1, 5.5)).label('SLEEVE').color('darkred')

    # ===== PWRK Section =====
    d += elm.Label().at((-2, 3.5)).label('IC-7000 Head Connector (10-pin)').color('darkred')

    d += elm.Dot().at((0, 2.5))
    d += elm.Label().at((-1, 2.5)).label('PWRK').color('darkred')
    d += elm.Line().right().length(3).at((0, 2.5))
    Q = d.add(elm.AnalogNFet().anchor('drain').label('2N7000', loc='right'))

    # Gate
    d += elm.Line().length(2).at(Q.gate).left()
    d += elm.Label().label('GPIO6').color('blue')

    # Source to ground
    d += elm.Line().down().at(Q.source).length(1)
    d += elm.Ground()

    # GND pin
    d += elm.Dot().at((0, 1))
    d += elm.Label().at((-1, 1)).label('GND').color('darkred')
    d += elm.Line().down().at((0, 1)).length(0.5)
    d += elm.Ground()

    # ESP32 label
    d += elm.Label().at((8, 8)).label('ESP32-S3').color('blue')
    d += elm.Label().at((8, 7.3)).label('Dev Board').color('blue')

    # ESP32 power
    d += elm.Label().at((8, 0.5)).label('USB-C\nPower').color('blue')

    # Common ground note
    d += elm.Label().at((3, -0.5)).label('All GND connected together').color('gray')

print("Schematics generated as PNG:")
print("  docs/images/civ_interface.png")
print("  docs/images/pwrk_circuit.png")
print("  docs/images/complete_circuit.png")
