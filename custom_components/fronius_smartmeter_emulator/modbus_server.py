import asyncio
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from homeassistant.core import HomeAssistant

# SunSpec-kompatible Register für Fronius Smart Meter
def create_context():
    # Hier einfache Dummy-Werte
    block = ModbusSequentialDataBlock(0, [0]*300)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block, unit=240)
    return ModbusServerContext(slaves=store, single=True)

async def start_server(hass: HomeAssistant, port: int = 5020):
    context = create_context()

    def run():
        StartTcpServer(context, address=("0.0.0.0", port))

    hass.loop.run_in_executor(None, run)
    hass.components.logger.getLogger(__name__).info(f"Fronius Smart Meter Emulator läuft auf Port {port}")
