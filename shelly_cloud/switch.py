"""
Create cover for every Shelly Cloud with MQTT enabled
and Working Mode = Roller Shutter.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""

import logging

from collections import OrderedDict
from homeassistant.components.mqtt import (switch)
from .const import (
    CONF_DEVICES, DOMAIN as SHELLY_DOMAIN)

DEPENDENCIES = ['mqtt', 'shelly_cloud']

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config,
                               async_add_entities, discovery_info=None):
    """Setup switch platform"""
    _LOGGER.debug("init setup mqtt switch")

    from shellypython.const import (WORKING_MODE_RELAY)

    for ip_address, shelly_data in (
            hass.data[SHELLY_DOMAIN][CONF_DEVICES].items()):

        if (ip_address not in hass.data[SHELLY_DOMAIN]['switch']
                and shelly_data.data is not None
                and shelly_data.data.working_mode_raw == WORKING_MODE_RELAY
                and shelly_data.data.mqtt is not None
                and shelly_data.data.mqtt.connected
                and shelly_data.data.relays is not None):
            for index, relay in enumerate(shelly_data.data.relays):
                _name = (
                    "{}_{}".format(shelly_data.name, index)
                    if len(shelly_data.data.relays) > 1
                    else "{}".format(shelly_data.name)
                    )
                config = OrderedDict([
                    ("name", "{}".format(_name)),
                    ("state_topic", "shellies/{}/relay/{}".format(
                        shelly_data.data.host_name, index)),
                    ("command_topic", "shellies/{}/relay/{}/command".format(
                        shelly_data.data.host_name, index)),
                    ("payload_on", "on"),
                    ("payload_off", "off"),
                    ("retain", False),
                    ("qos", 0),
                    ("availability_topic", "shellies/{}/online".format(
                        shelly_data.data.host_name)),
                    ("payload_available", "true"),
                    ("payload_not_available",   "false"),
                    ("platform", "mqtt")])

                switch.hass = hass
                await switch.async_setup_platform(
                    hass, config, async_add_entities, discovery_info)

                hass.data[SHELLY_DOMAIN]['switch'].append(ip_address)

                hass.components.persistent_notification.async_create(
                    "Shelly Cloud switch created ip address: {}".format(
                        ip_address),
                    "Shelly Cloud", "switch.{}.{}".format(ip_address, index)
                )
