from homeassistant.core import HomeAssistant
from .modbus_server import start_modbus_server

DOMAIN = "fronius_smartmeter_emulator"

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the Fronius Smart Meter Emulator from a config entry."""
    config = entry.data
    power_entity = config["power_entity"]
    import_entity = config.get("import_entity")
    export_entity = config.get("export_entity")
    unit_id = config.get("modbus_unit_id", 240)
    port = config.get("modbus_port", 1502)

    # Start the Modbus TCP server
    hass.async_create_task(
        start_modbus_server(
            hass,
            power_entity=power_entity,
            import_entity=import_entity,
            export_entity=export_entity,
            unit_id=unit_id,
            port=port
        )
    )

    return True
