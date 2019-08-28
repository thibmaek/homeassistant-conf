#!/usr/bin/env bash
set -e

if [ -f secrets.test.yaml ]; then
  echo "Clearing previous secrets test file..."
  rm -rf secrets.test.yaml
fi

# Mapfile is prefered but adds an extra space
# mapfile -t secrets < <(grep -r '!secret' . --exclude-dir=.vscode --exclude=generate_secrets.sh | sed -ne 's/^.*!secret//p' | sort | uniq)
secrets=($(grep -r '!secret' . --exclude-dir=.vscode --exclude-dir=esphome --exclude=generate_secrets.sh | sed -ne 's/^.*!secret//p' | sort | uniq))

for secret in "${secrets[@]}"; do
  echo "Found secret: $secret"
  echo "$secret: \"any value\"" >> secrets.test.yaml
done
