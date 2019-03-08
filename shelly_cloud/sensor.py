"""
Get Shelly information for a given host through web api.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""
import logging
import ipaddress

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_IP_ADDRESS,
    CONF_USERNAME, CONF_PASSWORD,
    CONF_MONITORED_CONDITIONS
    )
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import (Entity, generate_entity_id)
from homeassistant.util import Throttle
from .const import *
from . import VERSION
from shellypython.const import (WORKING_MODE_RELAY, WORKING_MODE_ROLLER)

REQUIREMENTS = ['shellypython>=0.0.4b1']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP_ADDRESS):
        vol.All(ipaddress.ip_address, cv.string),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_MONITORED_CONDITIONS, default=SENSOR_TYPES):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    })


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Shelly sensor."""

    ip_address = config.get(CONF_IP_ADDRESS)
    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    monitored_condition = config[CONF_MONITORED_CONDITIONS]

    shelly_data = ShellyData(
        ip_address, username, password, SCAN_INTERVAL_SECONDS, add_entities)
    shelly_data.update()

    monitored_condition.append(CONST_SENSOR_SYSTEM)

    if shelly_data is not None and shelly_data.data is not None:
        if shelly_data.data.working_mode_raw == WORKING_MODE_RELAY:
            if CONST_SENSOR_ROLLER in monitored_condition:
                monitored_condition.remove(CONST_SENSOR_ROLLER)
        elif shelly_data.data.working_mode_raw == WORKING_MODE_ROLLER:
            if CONST_SENSOR_RELAY in monitored_condition:
                monitored_condition.remove(CONST_SENSOR_RELAY)

    _LOGGER.info('if you have ANY issues with this, please report them here:'
                 ' https://github.com/marcogazzola/custom_components')

    _LOGGER.debug('Version %s', VERSION)

    sensors = []
    for variable in monitored_condition:
        sensors.append(ShellySensor(shelly_data, variable, name))

    add_entities(sensors, True)


class ShellySensor(Entity):
    """Implementation of Shelly sensor."""

    def __init__(self, shelly_data, sensor_type, name):
        """Initialize the sensor."""
        self.client_name = name
        self._name = sensor_type
        self.shelly_data = shelly_data
        self.type = sensor_type
        self._state = None
        self._unit_of_measurement = None
        self._attributes = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self.client_name, self._name)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the icon to represent this sensor."""
        if self.type in SENSOR_ICONS:
            return SENSOR_ICONS[self.type]

        return SENSOR_ICONS[CONST_SENSOR_SYSTEM]

    @property
    def state(self):
        """Return the expiration days for hostname."""
        return self._state

    @property
    def device_state_attributes(self):
        """Get the more info attributes."""
        return self._attributes

    def _empty_state_and_attributes(self):
        """Empty the state and attributes on an error."""
        from shellypython.const import (DEVICE_NOT_READY)

        self._state = DEVICE_NOT_READY
        self._attributes = None

    def update(self):
        """Get the current Shelly status."""
        self.shelly_data.update()

        if self.shelly_data is None or self.shelly_data.data is None:
            self._empty_state_and_attributes()
            return

        if self.type == CONST_SENSOR_SYSTEM:
            self._state = self.shelly_data.data.main_status
            attributes_data = (
                self.shelly_data.data.system.as_dict()
                if self.shelly_data.data.system is not None
                else None
                )
            attributes_data.update({'model': self.shelly_data.data.model})
            attributes_data.update(
                {'working_mode': self.shelly_data.data.working_mode}
                )
            attributes_data.update(
                {'host_name': self.shelly_data.data.host_name}
                )

            self._attributes = attributes_data
        elif self.type == CONST_SENSOR_MQTT:
            attributes_data = (
                self.shelly_data.data.mqtt
                if self.shelly_data.data.mqtt is not None
                else None)
            if attributes_data is None or not attributes_data.connected:
                self._state = CONST_DISCONNECTED
            else:
                self._state = CONST_CONNECTED
            self._attributes = None
        elif self.type == CONST_SENSOR_CLOUD:
            attributes_data = (
                self.shelly_data.data.cloud
                if self.shelly_data.data.cloud is not None
                else None)
            if attributes_data is None or not attributes_data.connected:
                self._state = CONST_DISCONNECTED
            else:
                self._state = CONST_CONNECTED
            self._attributes = None
        elif self.type == CONST_SENSOR_WIFI:
            attributes_data = (
                self.shelly_data.data.wifi_sta
                if self.shelly_data.data.wifi_sta is not None
                else None)
            if attributes_data is None or not attributes_data.connected:
                self._state = CONST_DISCONNECTED
                self._attributes = None
            else:
                self._state = "{} %".format(attributes_data.quality)
                self._attributes = {
                    "Ssid": attributes_data.ssid,
                    "Ip": attributes_data.ip,
                    "Rssi": attributes_data.rssi,
                    }
        elif self.type == CONST_SENSOR_FIRMWARE:
            attributes_data = (
                self.shelly_data.data.firmware
                if self.shelly_data.data.firmware is not None
                else None)
            if attributes_data is None or not attributes_data.has_update:
                self._state = CONST_UPTODATE
                self._attributes = (
                    {"Current version": attributes_data.old_version}
                    )
            else:
                self._state = CONST_UPDATEAVAILABLE
                self._attributes = {
                    "Current version": attributes_data.old_version,
                    "Latest version": attributes_data.new_version,
                    }
        elif self.type == CONST_SENSOR_FIRMWARE:
            attributes_data = (
                self.shelly_data.data.firmware
                if self.shelly_data.data.firmware is not None
                else None)
            if attributes_data is None or not attributes_data.has_update:
                self._state = CONST_UPTODATE
                self._attributes = (
                    {"Current version": attributes_data.old_version}
                    )
            else:
                self._state = CONST_UPDATEAVAILABLE
                self._attributes = {
                    "Current version": attributes_data.old_version,
                    "Latest version": attributes_data.new_version,
                    }

class ShellyData:
    """Get the latest data from ShellyData."""

    def __init__(
            self, ip_address, username, password, scan_interval, add_entities):
        """Initialize the data object."""
        self._ip_address = ip_address
        self._username = username
        self._password = password

        self.data = None

        # Apply throttling to methods using configured interval
        from datetime import timedelta
        timedelta_interval = timedelta(seconds=scan_interval)
        self.update = Throttle(timedelta_interval)(self._update)

    def _update(self):
        """Get the latest data from Shelly Api."""
        from shellypython.exception import ShellyException
        from shellypython.shelly import Shelly

        try:
            self.data = Shelly(self._ip_address).update_data()
        except ShellyException as error:
            _LOGGER.error(
                "Unable to connect to Shelly: %s %s", error,
                self._ip_address
                )
            self.data = None
