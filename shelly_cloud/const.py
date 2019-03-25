"""
Shelly Cloud constant.

For more details about this platform, please refer to the documentation at
https://github.com/marcogazzola/custom_components/blob/master/README.md
"""

from datetime import timedelta

VERSION = '0.1.1b0'
REQUIREMENTS_LIST = ['shellypython>=0.1.1']
CONF_DOMAIN = 'domain'
DOMAIN = "shelly_cloud"

DEFAULT_NAME = 'Shelly'

# SCAN_INTERVAL = timedelta(seconds=30)
SCAN_INTERVAL = timedelta(minutes=2)
CONF_DEVICES = 'devices'
CONF_ENABLED_COMPONENTS = 'enabled_components'
MANAGED_COMPONENTS = ['sensor', 'cover', 'switch']

CONST_CONNECTED = 'Connected'
CONST_DISCONNECTED = 'Disconnected'
CONST_ENABLED = 'Enabled'
CONST_DISABLED = 'Disabled'
CONST_UPTODATE = 'Latest'
CONST_UPDATEAVAILABLE = 'New firmware available'
CONST_SENSOR_SYSTEM = 'SYSTEM'
CONST_SENSOR_MQTT = 'MQTT'
CONST_SENSOR_CLOUD = 'CLOUD'
CONST_SENSOR_WIFI = 'WIFI'
CONST_SENSOR_FIRMWARE = 'FIRMWARE'
CONST_SENSOR_RELAY = 'RELAY'
CONST_SENSOR_ROLLER = 'ROLLER'

SENSOR_TYPES = [
    CONST_SENSOR_SYSTEM, CONST_SENSOR_MQTT, CONST_SENSOR_CLOUD,
    CONST_SENSOR_WIFI, CONST_SENSOR_FIRMWARE
    # , CONST_SENSOR_RELAY, CONST_SENSOR_ROLLER
    ]

SENSOR_ICONS = {
    CONST_SENSOR_MQTT: 'mdi:lan',
    CONST_SENSOR_CLOUD: 'mdi:cloud-sync',
    CONST_SENSOR_WIFI: 'mdi:wifi',
    CONST_SENSOR_FIRMWARE: 'mdi:cellphone-arrow-down',
    CONST_SENSOR_RELAY: 'mdi:light-switch',
    CONST_SENSOR_ROLLER: 'mdi:window-open',
    CONST_SENSOR_SYSTEM: 'mdi:chip',
}
