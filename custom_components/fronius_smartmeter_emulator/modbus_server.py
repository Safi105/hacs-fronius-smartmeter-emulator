import asyncio
import logging
from pymodbus.server import ServerTcp
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore.simulator import setup_simulator

_LOGGER = logging.getLogger(__name__)

async def start_modbus_server(port=5020):
    """Startet einen Modbus-TCP-Server (kompatibel mit pymodbus >=3.6)."""

    # Register 0–99: Dummy-Werte für Smart Meter
    datablock = ModbusSequentialDataBlock(0, [0] * 100)

    # setup_simulator() ersetzt ModbusServerContext
    context = setup_simulator({0x00: datablock})

    server = ServerTcp(context, address=("0.0.0.0", port))
    _LOGGER.info(f"Starte Modbus TCP Server auf Port {port} (pymodbus ≥3.6)...")

    # AsyncIO-Server starten
    await server.serve_forever()
