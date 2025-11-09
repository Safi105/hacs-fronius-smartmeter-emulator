from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import selector

DOMAIN = "fronius_smartmeter_emulator"

class FroniusSmartMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fronius Smart Meter Emulator."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Fronius Smart Meter Emulator", data=user_input)

        # Formular
        data_schema = vol.Schema({
            vol.Required(
                "power_entity",
                description={"suggested_value": None}
            ): selector({"entity": {"domain": "sensor"}}),  # Required: aktuelle Leistung

            vol.Optional(
                "import_entity",
                description={"suggested_value": None}
            ): selector({"entity": {"domain": "sensor"}}),  # Optional: importierte Energie

            vol.Optional(
                "export_entity",
                description={"suggested_value": None}
            ): selector({"entity": {"domain": "sensor"}}),  # Optional: exportierte Energie

            vol.Optional(
                "modbus_unit_id", default=240
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=247)),

            vol.Optional(
                "modbus_port", default=1502
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)
