import logging
from ucapi_framework.setup_flow import SetupFlow
from intg_jblav.device import JBLAV
from intg_jblav.config import JBLAVConfig

_LOG = logging.getLogger(__name__)


class JBLAVSetupFlow(SetupFlow):
    """Setup flow for JBL AV Receiver integration."""

    async def async_setup(self):
        """Run setup."""
        action = self.get_input_value("action")

        if action == "reset":
            self.driver.clear_devices()

        name = self.get_input_value("name")
        host = self.get_input_value("host")
        port = int(self.get_input_value("port"))

        _LOG.info("Testing connection to JBL receiver at %s:%s", host, port)

        device = JBLAV(name=name, host=host, port=port)
        connected = await device.test_connection()

        if not connected:
            return self.async_abort(reason="cannot_connect")

        _LOG.info("Connection successful - Model: %s", device.model)

        config = JBLAVConfig(
            identifier=f"jblav_{host.replace('.', '_')}_{port}",
            name=name,
            host=host,
            port=port,
        )

        self.driver.add_device_config(config)
        self.driver.add_device(device, config)

        return self.async_finish()
