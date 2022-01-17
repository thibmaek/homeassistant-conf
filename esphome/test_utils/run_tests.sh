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
  ESPHOME_CONFIGS=( devices/**/*.yaml )

  for config in "${ESPHOME_CONFIGS[@]}"; do
    echo "🛠  Compiling ESPHome configuration: $config"
    if ! esphome compile "$config"; then
      exit 1
    fi
  done
}

"${@:-compile_all}"
