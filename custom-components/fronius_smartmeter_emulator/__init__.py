"""Initialisiert die Fronius Smartmeter Emulator Integration."""
from homeassistant.core import HomeAssistant

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Integration (wird im Initialisierungsprozess geladen)."""
    return True
