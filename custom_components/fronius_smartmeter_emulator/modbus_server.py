import asyncio
import logging
from pymodbus.server.async_io import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore.simulator import setup_simulator
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def start_modbus_server(hass: HomeAssistant, power_entity: str,
                              import_entity: str = None, export_entity: str = None,
                              unit_id: int = 240, port: int = 1502):
    """Start a Modbus TCP server (Fronius Smart Meter Emulator)"""

    datablock = ModbusSequentialDataBlock(0, [0]*100)
    store = setup_simulator({unit_id: datablock})

    async def update_registers():
        while True:
            try:
                # Aktuelle Leistung
                power_state = hass.states.get(power_entity)
                if power_state:
                    datablock.setValues(3, 0, [int(float(power_state.state))])

                # Importierte Energie
                if import_entity:
                    import_state = hass.states.get(import_entity)
                    if import_state:
                        datablock.setValues(3, 1, [int(float(import_state.state))])

                # Exportierte Energie
                if export_entity:
                    export_state = hass.states.get(export_entity)
                    if export_state:
                        datablock.setValues(3, 2, [int(float(export_state.state))])
            except Exception as e:
                _LOGGER.error(f"Fehler beim Aktualisieren der Register: {e}")

            await asyncio.sleep(1)

    # Start TCP Server und Update-Loop parallel
    await asyncio.gather(
        StartTcpServer(context=store, address=("0.0.0.0", port)),
        update_registers()
    )
