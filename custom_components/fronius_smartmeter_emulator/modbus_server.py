import asyncio
import logging
from homeassistant.core import HomeAssistant
from .const import UNIT_ID, REGISTER_AC_POWER, REGISTER_AC_IMPORT, REGISTER_AC_EXPORT

_LOGGER = logging.getLogger(__name__)

# --- Kompatibilitäts-Imports für unterschiedliche pymodbus-Versionen ---
try:
    # Neue API (pymodbus >=3.6)
    from pymodbus.server import StartTcpServer
    from pymodbus.datastore.context import ModbusServerContext
    from pymodbus.datastore.context import ModbusSingleSlaveContext as ModbusSlaveContext
    from pymodbus.datastore.store import ModbusSequentialDataBlock
    _LOGGER.debug("pymodbus neue API erkannt (>=3.6)")
except ImportError:
    try:
        # Alte API (pymodbus 3.0–3.5)
        from pymodbus.server.async_io import StartTcpServer
        from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock
        _LOGGER.debug("pymodbus mittlere API erkannt (3.0–3.5)")
    except ImportError:
        # Sehr alte API (pymodbus 2.x)
        from pymodbus.server.async import StartTcpServer
        from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock
        _LOGGER.debug("pymodbus alte API erkannt (2.x)")


async def start_modbus_server(
    hass: HomeAssistant,
    power_entity: str,
    import_entity: str = None,
    export_entity: str = None,
    unit_id: int = UNIT_ID,
    port: int = 1502
):
    """Start a Modbus TCP server (Fronius Smart Meter Emulator)"""

    datablock = ModbusSequentialDataBlock(0, [0] * 200)

    # Ab pymodbus 3.6+ → ModbusSingleSlaveContext statt ModbusSlaveContext möglich
    try:
        slave_context = ModbusSlaveContext(hr=datablock, zero_mode=True)
    except TypeError:
        slave_context = ModbusSlaveContext(di=None, co=None, hr=datablock, ir=None, zero_mode=True)

    context = ModbusServerContext(slaves={unit_id: slave_context}, single=False)

    async def update_registers():
        """Update Holding-Register alle 1s mit Werten aus Home Assistant."""
        while True:
            try:
                # Aktuelle Leistung
                state = hass.states.get(power_entity)
                if state:
                    slave_context.setValues(3, REGISTER_AC_POWER, [int(float(state.state))])

                # Importierte Energie
                if import_entity:
                    state = hass.states.get(import_entity)
                    if state:
                        slave_context.setValues(3, REGISTER_AC_IMPORT, [int(float(state.state))])

                # Exportierte Energie
                if export_entity:
                    state = hass.states.get(export_entity)
                    if state:
                        slave_context.setValues(3, REGISTER_AC_EXPORT, [int(float(state.state))])

            except Exception as e:
                _LOGGER.error(f"Fehler beim Aktualisieren der Register: {e}")

            await asyncio.sleep(1)

    _LOGGER.info(f"Starte Fronius Smart Meter Emulator (Unit-ID {unit_id}, Port {port})")

    await asyncio.gather(
        StartTcpServer(context=context, address=("0.0.0.0", port)),
        update_registers()
    )