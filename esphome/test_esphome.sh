#!/usr/bin/env bash
set -e

info() {
  printf "\033[34m%s\033[0m\n" "$1"
  printf "\n"
}

function setup_mock_env() {
  echo "wifi_ssid: home_wifi" > secrets.yaml
  echo "wifi_password: my_8_characters_long_key" >> secrets.yaml
  cat secrets.yaml
}

function compile_all() {
  shopt -s globstar nullglob

  ESPHOME_CONFIGS=( **/*.yaml )
  for config in "${ESPHOME_CONFIGS[@]}"; do
    if echo "$config" | grep -q "_archive/"; then
      info "Skipping archived config ($config)"
      continue
    fi

    if echo "$config" | grep -q "common/"; then
      info "Skipping shared config ($config)"
      continue
    fi

    echo "🛠  Compiling ESPHome configuration: $config"
    if ! esphome "$config" compile; then
      exit 1
    fi
  done
}

"${@:-compile_all}"
