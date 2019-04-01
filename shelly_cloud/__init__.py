"""
Shelly Cloud platform.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""

import logging
import voluptuous as vol
import asyncio
import ipaddress
import gc
from homeassistant.util.async_ import run_coroutine_threadsafe
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers import discovery
from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    CONF_SCAN_INTERVAL,
    CONF_USERNAME, CONF_PASSWORD, CONF_IP_ADDRESS,
    CONF_MONITORED_CONDITIONS, CONF_NAME)

from .const import (
    SENSOR_SCAN_INTERVAL, CONF_DEVICES, DOMAIN, REQUIREMENTS_LIST,
    DEFAULT_NAME, SENSOR_TYPES, MANAGED_COMPONENTS, VERSION,
    CONF_ENABLED_COMPONENTS, PLATFORM_STARTUP, PLATFORM_SCAN_INTERVAL,
    RELAY_TYPES, CONF_RELAY_TYPE)

from .shelly_data import ShellyData

REQUIREMENTS = REQUIREMENTS_LIST

_LOGGER = logging.getLogger(__name__)

SHELLY_CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS):
        vol.All(ipaddress.ip_address, cv.string),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SENSOR_SCAN_INTERVAL):
        cv.time_period,
    vol.Optional(CONF_MONITORED_CONDITIONS, default=SENSOR_TYPES):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_RELAY_TYPE, default='switch'):
        vol.All(cv.string, [vol.In(RELAY_TYPES)]),
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
    hass.data[DOMAIN][PLATFORM_STARTUP] = {}
    for item in MANAGED_COMPONENTS:
        hass.data[DOMAIN][item] = []
        hass.data[DOMAIN][PLATFORM_STARTUP].update({item: True})

    config = config.get(DOMAIN)

    async def setup_shelly(self):
        tasks = []
        for shelly in config[CONF_DEVICES]:
            ip_address = shelly.get(CONF_IP_ADDRESS, '')
            username = shelly.get(CONF_USERNAME, '')
            password = shelly.get(CONF_PASSWORD, '')
            name = shelly.get(CONF_NAME, DEFAULT_NAME)

            monitored_condition = shelly.get(
                CONF_MONITORED_CONDITIONS, SENSOR_TYPES)

            scan_interval = shelly.get(
                CONF_SCAN_INTERVAL, SENSOR_SCAN_INTERVAL)

            relay_type = shelly.get(CONF_RELAY_TYPE)

            shelly_data = ShellyData(
                ip_address, username, password,
                name, scan_interval, monitored_condition,
                relay_type, hass)

            # await shelly_data.async_update(hass)
            hass.data[DOMAIN][CONF_DEVICES][ip_address] = shelly_data
            tasks.append(
                hass.data[DOMAIN][CONF_DEVICES][ip_address].async_update(hass)
                )

        await asyncio.wait(tasks)
        del tasks
        gc.collect()

        _managed_components = config.get(
            CONF_ENABLED_COMPONENTS,
            MANAGED_COMPONENTS
        )

        for component in _managed_components:
            discovery.load_platform(hass, component, DOMAIN, {}, config)

        gc.collect()

        return True

    run_coroutine_threadsafe(setup_shelly(None), hass.loop)

    async_track_time_interval(hass, setup_shelly, PLATFORM_SCAN_INTERVAL)

    return True
