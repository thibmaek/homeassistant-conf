#!/usr/bin/env bash
set -e

function check_extension() {
  if basename "$1" | grep ".*\.yml$"; then
    echo "YAML files with extension .yml are not allowed!"
    exit 1
  fi
}

case "${1}" in
--about)
  echo "Disallows the usage of .yml extension instead of .yaml"
  ;;
*)
  for file in $(git diff-index --cached --name-only HEAD); do
    check_extension "$file"
  done
  ;;
esac
