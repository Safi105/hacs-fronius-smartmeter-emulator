import asyncio
import logging
from pymodbus.server.async_io import StartTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock
from homeassistant.core import HomeAssistant
from .const import UNIT_ID, REGISTER_AC_POWER, REGISTER_AC_IMPORT, REGISTER_AC_EXPORT

_LOGGER = logging.getLogger(__name__)

async def start_modbus_server(
    hass: HomeAssistant,
    power_entity: str,
    import_entity: str = None,
    export_entity: str = None,
    unit_id: int = UNIT_ID,
    port: int = 1502
):
    """
    Start a Modbus TCP server emulating a Fronius Smart Meter.

    - Unit-ID: 240 (konform WR)
    - Port: konfigurierbar (default 1502)
    - Registers:
        - AC Power: REGISTER_AC_POWER
        - Import Energy: REGISTER_AC_IMPORT
        - Export Energy: REGISTER_AC_EXPORT
    """

    # Erstelle Register-Block für Holding-Register (0–199)
    datablock = ModbusSequentialDataBlock(0, [0]*200)

    # Slave-Context für diese Unit-ID
    slave_context = ModbusSlaveContext(
        di=None,  # Discrete Inputs
        co=None,  # Coils
        hr=datablock,  # Holding Registers
        ir=None,  # Input Registers
        zero_mode=True  # Register ab 0 adressieren
    )

    # Server-Context für die Unit-ID
    context = ModbusServerContext(slaves={unit_id: slave_context}, single=False)

    async def update_registers():
        """Update Holding-Register alle 1s mit Home Assistant Entities."""
        while True:
            try:
                # Aktuelle Leistung
                state = hass.states.get(power_entity)
                if state:
                    slave_context.setValues(3, REGISTER_AC_POWER, [int(float(state.state))])

                # Importierte Energie (optional)
                if import_entity:
                    state = hass.states.get(import_entity)
                    if state:
                        slave_context.setValues(3, REGISTER_AC_IMPORT, [int(float(state.state))])

                # Exportierte Energie (optional)
                if export_entity:
                    state = hass.states.get(export_entity)
                    if state:
                        slave_context.setValues(3, REGISTER_AC_EXPORT, [int(float(state.state))])

            except Exception as e:
                _LOGGER.error(f"Fehler beim Aktualisieren der Modbus-Register: {e}")

            await asyncio.sleep(1)

    _LOGGER.info(f"Starte Fronius Smart Meter Emulator auf Port {port}, Unit-ID {unit_id}")
    
    # Server + Register-Update parallel starten
    await asyncio.gather(
        StartTcpServer(context=context, address=("0.0.0.0", port)),
        update_registers()
    )
