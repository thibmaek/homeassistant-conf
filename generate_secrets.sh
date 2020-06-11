#!/usr/bin/env bash
set -e

if [ -f secrets.yaml ]; then
  echo "Clearing previous secrets test file..."
  echo "" > secrets.yaml
fi

# Mapfile is prefered but adds an extra space
# mapfile -t secrets < <(grep -r '!secret' . --exclude-dir=.vscode --exclude=generate_secrets.sh | sed -ne 's/^.*!secret//p' | sort | uniq)

# shellcheck disable=SC2207
secrets=($(grep -r '!secret' . --exclude-dir=.vscode --exclude-dir=esphome --exclude=generate_secrets.sh | sed -ne 's/^.*!secret//p' | sort | uniq))

function getValue() {
  if echo "$1" | grep -q "_port"; then
    echo "8080"
  elif echo "$1" | grep -q "_email"; then
    echo "user@mail.com"
  elif echo "$1" | grep -q "_host"; then
    echo "0.0.0.0"
  elif echo "$1" | grep -q "localhost"; then
    echo "0.0.0.0"
  elif echo "$1" | grep -q "_url"; then
    echo "http://endpoint.com"
  elif echo "$1" | grep -q "_token"; then
    echo "e2394ce1-9898-426c-b897-dd351ded18b2"
  elif echo "$1" | grep -q "_api_key"; then
    echo "e2394ce1-9898-426c-b897-dd351ded18b2"
  elif echo "$1" | grep -q "_secret"; then
    echo "e2394ce1-9898-426c-b897-dd351ded18b2"
  else
    echo "any value"
  fi
}

for secret in "${secrets[@]}"; do
  echo "Found secret: $secret"
  echo "$secret: \"$(getValue "$secret")\"" >> secrets.yaml
done
