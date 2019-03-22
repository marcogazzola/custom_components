"""
Shelly Cloud platform.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""

import logging
import voluptuous as vol
import ipaddress

from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers import discovery
from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    CONF_SCAN_INTERVAL,
    CONF_USERNAME, CONF_PASSWORD, CONF_IP_ADDRESS,
    CONF_MONITORED_CONDITIONS, CONF_NAME)

from .const import (
    SCAN_INTERVAL, CONF_DEVICES, DOMAIN, REQUIREMENTS_LIST,
    DEFAULT_NAME, SENSOR_TYPES, MANAGED_COMPONENTS, VERSION,
    CONF_ENABLED_COMPONENTS)

from .shelly_data import ShellyData

REQUIREMENTS = REQUIREMENTS_LIST

_LOGGER = logging.getLogger(__name__)

SHELLY_CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS):
        vol.All(ipaddress.ip_address, cv.string),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL):
        cv.time_period,
    vol.Optional(CONF_MONITORED_CONDITIONS, default=SENSOR_TYPES):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})

vol.Schema({
    vol.Optional(CONF_ENABLED_COMPONENTS, default=MANAGED_COMPONENTS):
        vol.All(cv.ensure_list, [vol.In(MANAGED_COMPONENTS)]),
    DOMAIN: vol.Schema({
        vol.Optional(CONF_DEVICES):
            vol.All(cv.ensure_list, [SHELLY_CONFIG_SCHEMA]),
    }),
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config, discovery_info=None):
    """Set up the Shelly cloud component."""

    _LOGGER.info(
        'if you have ANY issues with this, please report them here:'
        ' https://github.com/marcogazzola/custom_components')

    _LOGGER.debug('Version %s', VERSION)

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][CONF_DEVICES] = {}
    for item in MANAGED_COMPONENTS:
        hass.data[DOMAIN][item] = []

    hass.data[DOMAIN][CONF_DEVICES]
    config = config.get(DOMAIN)

    async def setup_shelly(self):

        for shelly in config[CONF_DEVICES]:
            ip_address = shelly.get(CONF_IP_ADDRESS, '')
            username = shelly.get(CONF_USERNAME, '')
            password = shelly.get(CONF_PASSWORD, '')
            name = shelly.get(CONF_NAME, DEFAULT_NAME)
            _LOGGER.debug(name)
            monitored_condition = shelly.get(
                CONF_MONITORED_CONDITIONS, SENSOR_TYPES)
            _LOGGER.debug(monitored_condition)
            scan_interval = shelly.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
            _LOGGER.debug(ip_address)
            shelly_data = ShellyData(
                ip_address, username, password,
                name, scan_interval, monitored_condition, hass)

            await shelly_data.async_update(hass)

            hass.data[DOMAIN][CONF_DEVICES][ip_address] = shelly_data
            _LOGGER.debug(hass.data[DOMAIN][CONF_DEVICES][ip_address])

        managed_components = config.get(CONF_ENABLED_COMPONENTS, MANAGED_COMPONENTS)
        for component in managed_components:
            discovery.load_platform(hass, component, DOMAIN, {}, config)

        return True

    async_track_time_interval(hass, setup_shelly, SCAN_INTERVAL)

    await setup_shelly(None)

    return True
