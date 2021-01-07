#!/usr/bin/env python
import os
import sys
import argparse

sys.stdout.reconfigure(line_buffering=True)

p = argparse.ArgumentParser()
p.add_argument('-p', '--path', default='auto', help='auto|absolute|relative (auto)')
p.add_argument('--updir_depth', default='3', help='auto時に絶対パスと相対パスを切り替える深さ (3)')
args = p.parse_args()


def transform(line):
    slash = line.endswith('/') if line != '/' else False
    if args.path == 'absolute':
        line = os.path.abspath(line)
    elif args.path == 'relative':
        line = os.path.relpath(line)
    else:
        line = os.path.relpath(line)
        if line.startswith('../' * int(args.updir_depth)):
            line = os.path.abspath(line)
    if slash:
        line += '/'
    return line


try:
    line = sys.stdin.readline()
    while line:
        line = line.strip("\n")
        line = transform(line)
        print(line)
        line = sys.stdin.readline()
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
