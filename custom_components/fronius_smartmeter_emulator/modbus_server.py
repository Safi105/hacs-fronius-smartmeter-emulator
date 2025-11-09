import asyncio
import logging
from pymodbus.server import ServerTcp
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore.simulator import setup_simulator
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

async def start_modbus_server(hass: HomeAssistant, power_entity: str,
                              import_entity: str = None, export_entity: str = None,
                              unit_id: int = 240, port: int = 1502):
    """Start a Modbus TCP server emulating Fronius Smart Meter."""

    # Erstelle 100 Dummy-Register
    datablock = ModbusSequentialDataBlock(0, [0] * 100)

    # Modbus Simulator-Store
    store = setup_simulator({unit_id: datablock})

    # AsyncIO Server starten
    server = ServerTcp(store, address=("0.0.0.0", port))
    _LOGGER.info(f"Fronius Smart Meter Emulator läuft auf Port {port} mit Unit ID {unit_id}")

    async def update_registers():
        while True:
            try:
                # Aktuelle Leistung
                power_state = hass.states.get(power_entity)
                if power_state:
                    datablock.setValues(3, 0, [int(float(power_state.state))])  # Holding Register 0

                # Importierte Energie
                if import_entity:
                    import_state = hass.states.get(import_entity)
                    if import_state:
                        datablock.setValues(3, 1, [int(float(import_state.state))])  # Holding Register 1

                # Exportierte Energie
                if export_entity:
                    export_state = hass.states.get(export_entity)
                    if export_state:
                        datablock.setValues(3, 2, [int(float(export_state.state))])  # Holding Register 2

            except Exception as e:
                _LOGGER.error(f"Fehler beim Aktualisieren der Modbus-Register: {e}")

            await asyncio.sleep(1)  # Update alle 1s

    # Server und Register-Update parallel laufen lassen
    await asyncio.gather(server.serve_forever(), update_registers())
