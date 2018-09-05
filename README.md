# Home Assistant Conf

Personal configuration for [Home Assistant](https://home-assistant.io), specifically for Hass.io env.

> __NEVER EVER COMMIT WITHOUT USING SECRETS IN YOUR CONFIGURATION, ALWAYS EXCLUDE SENSITIVE FILES__

## Installation

This configuration is auto pulled at an interval and automatically restarts Home Assistant if `configuration.yaml` or `components/*` changed.
To replicate this behaviour, install the ConfigWatcher addon from [@vkorn/hassio-addons](https://github.com/vkorn/hassio-addons/tree/master/configwatcher) and set the following config in the addon configuration screen:

```json
{
  "base_dir": "/config",
  "check_delay": 5,
  "hassio_host": "http://172.17.0.2",
  "hass_host": "http://172.17.0.1:8123",
  "hass_key": "<homeassistant-key-here>",
  "notify": true,
  "notify_entity": "pushbullet",
  "hass_watch": [
    "components",
    "configuration.yaml"
  ],
  "addons": []
}
```

1. You need to first clone the repo by ssh'ing into Home Assistant, cd'ing to /config and cloning it there.
2. Create a [new personal access token](https://github.com/settings/tokens)
3. While still ssh'ed and in `/config` edit the remote url to add credentials in the file `.git/config`:

```ini
[remote "origin"]
  url = https://username@personal-access-tokengithub.com/thibmaek/homeassistant-conf
  fetch = +refs/heads/*:refs/remotes/origin/*
```
