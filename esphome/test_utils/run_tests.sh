#!/usr/bin/env bash
set -e
shopt -s globstar nullglob

info() {
  printf "\033[34m%s\033[0m\n" "$1"
  printf "\n"
}

function setup_mock_env() {
  mv "$(dirname "$0")/./secrets.mock.yaml" "$(dirname "$0")/../common/secrets.yaml"
}

function compile_all() {
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
