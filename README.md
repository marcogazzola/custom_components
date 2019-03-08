[Shelly Cloud Custom Component](https://github.com/marcogazzola/custom_components) for homeassistant

# What this is:
This is a custom component to allow control of Shelly Cloud devices in [Homeassistant](https://home-assistant.io) using the unofficial Shelly API. Please note Shelly may cut off access at anytime.

# What it does:
Allows for control the states of Shelly Cloud products as home assistant sensors with the following features:

* Sensor System
* Sensor Wifi
* Sensor Firmware
* Sensor Cloud
* Sensor Mqtt

# Configuration
### Download python files
Reproduce the directory structure of the [master branch](https://github.com/marcogazzola/custom_components) in your config directory custom_components directory to create the folder `shelly_cloud`. Currently it should look like:
```
custom_components
  shelly_cloud
    sensor.py
```
### Configure HA
Once there you’ll need to **update your config** to include the following under the **sensor domain**:

***Mandatory config:***
```yaml
sensor:
  - platform: shelly_cloud
    ip_address: !secret shelly_ip_address
```
***Optional config:***
```yaml
sensor:
  - platform: shelly_cloud
    ip_address: !secret shelly_ip_address
    name: shelly
    monitored_conditions:
      - MQTT
      - CLOUD
      - WIFI
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
