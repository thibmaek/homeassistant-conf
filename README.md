# Home Assistant Conf

[![Build Status](https://travis-ci.org/thibmaek/homeassistant-conf.svg?branch=master)](https://travis-ci.org/thibmaek/homeassistant-conf)
![Docker system](https://badgen.net/badge/Docker/Hass.io/?icon=docker)

> Personal configuration for [Home Assistant](https://home-assistant.io), specifically for Hass.io env.

## Installation

I use this configuration together with the Git Pull add-on to automatically fetch updates from this git repo and restart if needed:

```json
{
  ...
  "git_branch": "master",
  "git_command": "pull",
  "git_remote": "origin",
  "git_prune": true,
  "repository": "https://github.com/thibmaek/homeassistant-conf.git",
  "auto_restart": true,
  "restart_ignore": [
    "ui-lovelace.yaml",
    ".gitignore",
    "README.md",
    "secrets.test.yaml",
    ".yamllint",
    ".travis.yml"
  ],
  "repeat": {
    "active": true,
    "interval": 300
  }
}
```

1. You need to first clone the repo by ssh'ing into Home Assistant, cd'ing to your config dir (`/usr/share/hassio/homeassistant`) and cloning it there.
2. Enter the details above in the Git Pull add-on and adjust if needed
3. Start the add-on

## YAML Styleguide

- Use single quotes for single words
- Use double quotes for multiple words
- No quotes for MQTT topics
