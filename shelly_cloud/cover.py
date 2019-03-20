"""
Create cover for every Shelly Cloud with MQTT enabled 
and Working Mode = Roller Shutter.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""

import logging

from collections import OrderedDict
from homeassistant.util import Throttle
from homeassistant.components.mqtt import (cover)
from .const import (
    CONF_DEVICES, DOMAIN as SHELLY_DOMAIN, SCAN_INTERVAL)

DEPENDENCIES = ['mqtt', 'shelly_cloud']

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config,
                               async_add_entities, discovery_info=None):
    """Setup cover platform"""
    _LOGGER.debug("init setup mqtt cover")

    from shellypython.const import (WORKING_MODE_ROLLER)

    for ip_address, shelly_data in (
            hass.data[SHELLY_DOMAIN][CONF_DEVICES].items()):

        if (ip_address not in hass.data[SHELLY_DOMAIN]['cover']
                and shelly_data.data is not None
                and shelly_data.data.working_mode_raw == WORKING_MODE_ROLLER
                and shelly_data.data.mqtt is not None
                and shelly_data.data.mqtt.connected):

            config = OrderedDict([
                ("name", shelly_data.name),
                ("state_topic", "shellies/{}/roller/0".format(
                    shelly_data.data.host_name)),
                ("command_topic", "shellies/{}/roller/0/command".format(
                    shelly_data.data.host_name)),
                ("position_topic", "shellies/{}/roller/0/pos".format(
                    shelly_data.data.host_name)),
                ("set_position_topic",
                    "shellies/{}/roller/0/command/pos".format(
                        shelly_data.data.host_name)),
                ("payload_open", "open"),
                ("payload_close", "close"),
                ("payload_stop", "stop"),
                ("state_open", 100),
                ("state_closed", 0),
                ("retain", False),
                ("optimistic", False),
                ("qos", 0),
                ("position_open", 100),
                ("position_closed", 0),
                ("availability_topic", "shellies/{}/online".format(
                    shelly_data.data.host_name)),
                ("payload_available", "true"),
                ("payload_not_available","false"),
                ("platform", "mqtt")])

            cover.hass = hass
            await cover.async_setup_platform(
                hass, config, async_add_entities, discovery_info)

            hass.data[SHELLY_DOMAIN]['cover'].append(ip_address)

            hass.components.persistent_notification.async_create(
                "Shelly Cloud cover created ip address: {}".format(ip_address),
                "Shelly Cloud", "cover.{}".format(ip_address)
            )
