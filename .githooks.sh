#!/usr/bin/env bash
set -e

function disallow_yml() {
  if basename "$1" | grep ".yml"; then
    echo "YAML files with extension .yml are not allowed!"
    exit 1
  fi
}

function pre_commit() {
  npm run lint
  disallow_yml "$@"
}

function pre_push() {
  stagedFiles=$(git diff --name-only --cached)
  isValidFile=false

  if echo "$stagedFiles" | grep "components/" ; then
    isValidFile=true
  elif echo "$stagedFiles" | grep "custom_components/"; then
    isValidFile=true
  elif echo "$stagedFiles" | grep "packages/"; then
    isValidFile=true
  elif echo "$stagedFiles" | grep "configuration.yaml"; then
    isValidFile=true
  fi

  if "$isValidFile" = true; then
    ./generate_secrets.sh && \
      git add secrets.test.yaml && \
      git commit --amend --no-edit --no-verify
  fi
}

function help() {
  echo "Run one of the available commands:"
  echo "  pre_commit, pre_push"
}

"${@:-help}"
