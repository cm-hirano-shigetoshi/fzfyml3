#!/usr/bin/env bash
set -u

TEST_DIR=$(dirname $0)
NTH_PROGRAM=$TEST_DIR/../main/nth.py

check() {
    if [[ $# > 3 ]];then
        DELIM_OPT="-d $4"
    else
        DELIM_OPT=""
    fi
    echo "$1" | \
        ${FZFYML3_PYTHON-python} $NTH_PROGRAM $DELIM_OPT -- "$2" | \
        grep -Fx "$3"
    if [[ $? != 0 ]]; then
        echo "[ANSWER] $3"
        echo "[OUTPUT] $(echo "$1" | ${FZFYML3_PYTHON-python} $NTH_PROGRAM $DELIM_OPT -- "$2")"
    fi
}

check ' X: a ::aaa:bbb:ccc: : : X	X ' '' ' X: a ::aaa:bbb:ccc: : : X	X '
check ' X: a ::aaa:bbb:ccc: : : X	X ' '1' 'X:'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '2' 'a'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-1' 'X'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-3' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '..' 'X: a ::aaa:bbb:ccc: : : X	X'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '2..7' 'a ::aaa:bbb:ccc: : : X	X'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '2..' 'a ::aaa:bbb:ccc: : : X	X'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-3..' ': X	X'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-3..,1' ': X	X X:'

check ' X: a ::aaa:bbb:ccc: : : X	X ' '' ' X: a ::aaa:bbb:ccc: : : X	X ' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '1' 'X' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '2' 'a' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-1' 'X	X' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-2' '' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '..' 'X: a ::aaa:bbb:ccc: : : X	X' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '2..7' 'a ::aaa:bbb:ccc:' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '2..' 'a ::aaa:bbb:ccc: : : X	X' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-3..' ': : X	X' ':'
check ' X: a ::aaa:bbb:ccc: : : X	X ' '-3..,1' ': : X	X  X' ':'

