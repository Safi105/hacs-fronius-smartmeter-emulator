"""Beispiel-Sensorplattform für das Fronius Smartmeter Emulator."""

from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([FroniusSmartmeterEmulatorSensor()])

class FroniusSmartmeterEmulatorSensor(SensorEntity):
    """Ein einfacher Fronius Smartmeter Emulator Sensor."""

    def __init__(self):
        self._state = 0

    @property
    def name(self):
        return "Fronius Smartmeter Emulator Sensor"

    @property
    def state(self):
        return self._state
