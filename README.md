# Home Assistant Conf

[![Actions Status](https://github.com/thibmaek/homeassistant-conf/workflows/CI%20Pipeline/badge.svg)](https://github.com/thibmaek/homeassistant-conf/actions/workflows/ci-pipeline.yaml)
![Docker system](https://badgen.net/badge/Docker/home-assistant/?icon=docker)

> Personal configuration for [Home Assistant](https://home-assistant.io)

## Architecture

Check out [this diagram](https://whimsical.com/8gZ6KJPKUYjKcYVXVnyxJq) for an overview of how my homelab / HA instance is structured.

## Usage

<details>
  <summary>
    I use this configuration together with the Git Pull add-on to automatically fetch updates from this git repo and restart if needed:
  </summary>

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

</details>

## Tools

* Makefile to as simple task-runner
* [pre-commit](https://pre-commit.io) for git hooks
* [Github Actions](https://github.com/thibmaek/homeassistant-conf/actions) as CI pipeline
