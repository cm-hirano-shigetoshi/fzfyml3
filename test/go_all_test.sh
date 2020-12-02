#!/usr/bin/env bash
set -eu

TOOL_DIR=$(dirname $0)
for f in $TOOL_DIR/*.yml; do
    echo "$f"
    fzfyml3 test $f
done
