"""
Shelly Cloud base entity class.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""

import logging
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)


class ShellyData:
    """Get the latest data from ShellyData."""

    def __init__(
            self, ip_address, username, password, name,
            scan_interval, monitored_conditions, hass=None):
        """Initialize the data object."""
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.monitored_conditions = monitored_conditions
        self.scan_interval = scan_interval
        self.name = name
        self.hass = hass
        self.data = None

        # Apply throttling to methods using configured interval
        self.update = Throttle(scan_interval)(self._update)

    async def async_update(self, hass):
        # devs = await self.async_get_devices()
        # self._update()
        await hass.async_add_executor_job(self._update)

    def _update(self):
        """Get the latest data from Shelly Api."""
        from shellypython.exception import ShellyException
        from shellypython.shelly import Shelly

        try:
            self.data = Shelly(
                self.ip_address,
                self.username,
                self.password).update_data()
        except ShellyException as error:
            _LOGGER.error(
                "Unable to connect to Shelly: %s %s", error,
                self.ip_address
                )
            self.data = None
