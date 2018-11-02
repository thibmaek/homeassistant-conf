#!/usr/bin/env sh

echo ""
echo "Stubbing secrets from secrets.yaml"
echo ""

sed 's/[ ].*//' < secrets.yaml > secrets.example.yaml
