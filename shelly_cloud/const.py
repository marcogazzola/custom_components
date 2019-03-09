from datetime import timedelta

VERSION = '0.0.4b0'

CONF_DOMAIN = 'domain'

DEFAULT_NAME = 'Shelly'

SCAN_INTERVAL = timedelta(minutes=2)

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
    CONST_SENSOR_SYSTEM, CONST_SENSOR_MQTT, CONST_SENSOR_CLOUD, CONST_SENSOR_WIFI,
    CONST_SENSOR_FIRMWARE#, CONST_SENSOR_RELAY, CONST_SENSOR_ROLLER
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