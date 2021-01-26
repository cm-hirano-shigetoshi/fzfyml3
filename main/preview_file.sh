#!/usr/bin/env bash
set -eu

if file -b $1 | grep -q 'text'; then
    cat $1
elif file -b $1 | grep -q 'directory'; then
    ls -l --color $1/
elif file -b $1 | grep -q 'executable'; then
    xxd $1
else
    file -b $1
fi
