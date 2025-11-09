import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "fronius_smartmeter_emulator"

class FroniusSmartmeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Fronius Smart Meter Emulator", data=user_input)

        schema = vol.Schema({vol.Optional("port", default=5020): int})
        return self.async_show_form(step_id="user", data_schema=schema)
