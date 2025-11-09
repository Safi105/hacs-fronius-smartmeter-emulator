from .modbus_server import start_server

DOMAIN = "fronius_smartmeter_emulator"

async def async_setup_entry(hass, entry):
    port = entry.data.get("port", 5020)
    hass.async_create_task(start_server(hass, port))
    return True
