#!/usr/bin/env python
import os
import sys
import argparse

sys.stdout.reconfigure(line_buffering=True)

mode = None
line_x = 1


def get_invisible_hex(num):
    return {
        '1': '01',
        '2': '02',
        '3': '03',
        '4': '04',
        '5': '05',
        '6': '06',
        '7': '07',
        '8': '0b',
        '9': '0c',
        '0': '10',
    }[num]


def revert_invisible_hex(hex):
    return {
        r'\x01': '1',
        r'\x02': '2',
        r'\x03': '3',
        r'\x04': '4',
        r'\x05': '5',
        r'\x06': '6',
        r'\x07': '7',
        r'\x0b': '8',
        r'\x0c': '9',
        r'\x10': '0',
    }[hex]


def invisible_encode(num):
    num = str(num)
    s = ''
    for n in num:
        s += get_invisible_hex(n)
    return bytes.fromhex(s).decode('utf8')


def invisible_erase(bytes_str):
    text = repr(bytes_str)[1:-1]
    return text[:text.rfind(r'\x11')]


def invisible_decode(bytes_str):
    array = []
    text = repr(bytes_str)[1:-1]
    while text[-4:] != r'\x11':
        array.append(revert_invisible_hex(text[-4:]))
        text = text[:-4]
    return ''.join(reversed(array))


def some_transform(line):
    if mode == 'encode':
        global line_x
        print('{}{}{}'.format(line, '\x11', invisible_encode(line_x)))
        line_x += 1
    elif mode == 'erase':
        print(invisible_erase(line))
    else:
        if line_x <= 2:
            print(line)
            line_x += 1
            return
        with open(mode, 'r') as f:
            i = invisible_decode(line)
            print(f.readlines()[int(i) - 1], end='')


p = argparse.ArgumentParser()
p.add_argument('mode', help='encode / decode')
args = p.parse_args()
mode = args.mode

try:
    line = sys.stdin.readline()
    while line:
        line = line.strip("\n")
        line = some_transform(line)
        line = sys.stdin.readline()
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
