"""Konstanten für die Fronius Smartmeter Emulator Integration."""

DOMAIN = "fronius_smartmeter_emulator"

# Modbus Unit ID für Fronius Smart Meter
# Standardmäßig 240, da der Wechselrichter nur Meter mit dieser ID akzeptiert.
# Für Tests oder Multi-Meter-Setups könnte man sie theoretisch ändern.
UNIT_ID = 240

# Standard Modbus TCP Port
MODBUS_PORT = 1502

# Register-Offsets für Emulator (Beispiele aus Forum / AGG Soft)
REGISTER_AC_POWER = 89   # AC Leistung (W)
REGISTER_AC_IMPORT = 99  # Importierte Energie (Wh)
REGISTER_AC_EXPORT = 109 # Exportierte Energie (Wh)
