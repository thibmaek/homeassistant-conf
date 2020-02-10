#!/usr/bin/env bash

function setup_mock_env() {
  echo "wifi_ssid: home_wifi" > secrets.yaml
  echo "wifi_password: my_8_characters_long_key" >> secrets.yaml
  cat secrets.yaml
}

function run_all() {
  shopt -s globstar nullglob

  ESPHOME_CONFIGS=( **/*.yaml )
  for config in "${ESPHOME_CONFIGS[@]}"; do
    if [ "$config" == "common.yaml" ] || [ "$config" == "secrets.yaml" ]; then
      continue
    fi

    echo "🛠  Compiling ESPHome configuration: $config"
    if ! esphome "$config" compile; then
      exit 1
    fi
  done
}

"${@:-run_all}"
