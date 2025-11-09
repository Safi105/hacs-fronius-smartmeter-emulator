import asyncio
import logging
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore.simulator import setup_simulator

_LOGGER = logging.getLogger(__name__)

async def start_modbus_server(port=5020):
    """Startet einen Modbus-TCP-Server mit Dummy-Werten für den Fronius Smart Meter."""
    # Beispielregister: 0 = aktuelle Leistung, 1 = importierte Energie, 2 = exportierte Energie
    datablock = ModbusSequentialDataBlock(0, [0] * 100)

    # Simulator-Store (ersetzt ModbusSlaveContext/ServerContext)
    store = setup_simulator({0x00: datablock})

    _LOGGER.info(f"Starte Modbus TCP Server auf Port {port} …")
    await StartTcpServer(context=store, address=("0.0.0.0", port))
