#!/usr/bin/env sh

echo ""
echo "Stubbing secrets from secrets.yaml..."
echo ""

{
  :;
  echo "# This file is an auto-generated stub of how the secrets file";
  echo "# signature should look like. Do not modify this directly";
  echo "# Signature: $(date +%x) - $(date | sha256sum)"
  echo "";
  sed 's/[ ].*//' < secrets.yaml
  echo "";
} >> secrets.example.yaml
