#!/usr/bin/env bash
set -e

function pre_commit() {
  npm run lint
}

function pre_push() {
  stagedFiles=$(git diff --name-only --cached)
  isValidFile=false

  if "$stagedFiles" | grep "components/" ; then
    isValidFile=true
  elif "$stagedFiles" | grep "custom_components/"; then
    isValidFile=true
  elif "$stagedFiles" | grep "packages/"; then
    isValidFile=true
  elif "$stagedFiles" | grep "configuration.yaml"; then
    isValidFile=true
  fi

  if "$isValidFile" == true; then
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
