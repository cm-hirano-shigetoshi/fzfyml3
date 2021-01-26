#!/usr/bin/env bash
set -eu

TEST_DIR=$(dirname $0)
for f in $TEST_DIR/*.yml; do
    echo "$f"
    fzfyml3 test $f
done

bash $TEST_DIR/test_nth.sh

