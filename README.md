[Shelly Cloud Custom Component](https://github.com/marcogazzola/custom_components) for homeassistant

# What this is:
This is a custom component to allow control of Shelly Cloud devices in [Homeassistant](https://home-assistant.io) using the unofficial Shelly API. Please note Shelly may cut off access at anytime.

# What it does:
Allows for control the states of Shelly Cloud products as home assistant sensors with the following features:

* Sensor System
* Sensor Wifi
* Sensor Mqtt
* Sensor Cloud
* Sensor Firmware

# Configuration
### Download python files
Reproduce the directory structure of the [master branch](https://github.com/marcogazzola/custom_components) in your config directory custom_components directory to create the folder `shelly_cloud`. Currently it should look like:
```
custom_components
  shelly_cloud
    __init__.py
    const.py
    sensor.py
```
### Configure HA
Once there you’ll need to **update your config** to include the following under the **sensor domain**:

```yaml
sensor:
  - platform: shelly_cloud
    ip_address: !secret shelly_ip_address
```

***Configuration Variables***
```
ip_address
  (string)(Required)The IP address or hostname of the Shelly you want to track.

scan_interval
  (time)(Optional)Minimum time interval between updates. Supported formats: scan_interval: 'HH:MM:SS', scan_interval: 'HH:MM' and Time period dictionary (see example below).
  Default value: 2 minutes

monitored_conditions
  (list)(Optional)Sensors to display in the frontend.
  Default value: All keys
  
  system
    will be created sensor that will expose system informations like mac address, working mode, model name, etc..

  wifi
    will be created sensor that will expose wifi informations like wifi quality (%), ip address, SSID

  mqtt
    will be created sensor that will expose mqtt status

  cloud
    will be created sensor that will expose cloud status

  firmware
    will be created sensor that will expose firmware inofrmations like current and new firmware versione
```

***Example***
```yaml
sensor:
  - platform: shelly_cloud
    ip_address: !secret shelly_ip_address
    name: shelly
    scan_interval:
      - minutes: 2
    monitored_conditions:
      - SYSTEM
      - WIFI
      - MQTT
      - CLOUD
      - FIRMWARE
```

### Configure [custom_updater](https://github.com/custom-components/custom_updater) component
After [installing the component](https://github.com/custom-components/custom_updater/wiki/Installation), configure it as follows:

```yaml
custom_updater:
  track:
    - components
  component_urls:
# Dev build (unstable)
#    - https://raw.githubusercontent.com/marcogazzola/custom_components/dev/custom_components.json
# Released build
    - https://raw.githubusercontent.com/marcogazzola/custom_components/master/custom_components.json
```


# Changelog
Complete changelog [here](https://github.com/marcogazzola/custom_components/blob/master/CHANGELOG.md).

# Contribute
<a href="https://www.buymeacoffee.com/Gazzolinho" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
<br>
<a href="https://paypal.me/pools/c/8cMcW6wRNZ" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


# License
[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0. This is required for Home Assistant contributions.
