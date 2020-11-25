#!/usr/bin/env python
import os
import re
import sys
import argparse

sys.stdout.reconfigure(line_buffering=True)

p = argparse.ArgumentParser()
p.add_argument('nth')
p.add_argument('-d', '--delimiter', default=None)
args = p.parse_args()


def filter_with_range(line, r):
    line = line.lstrip()
    if '..' not in r:
        # 単一要素指定
        islands = re.findall(r'\S+\s*', line)
        r = int(r) - 1 if int(r) > 0 else int(r)
        return islands[r]
    else:
        # 範囲指定
        def get_range_text(line, start, end):
            islands = re.findall(r'\S+\s*', line)
            start = int(start) - 1 if int(start) > 0 else int(start)
            if int(end) == -1:
                return ''.join(islands[start:])
            else:
                end = int(end) if int(end) > 0 else int(end) + 1
                return ''.join(islands[start:end])

        if r == '..':
            start = 1
            end = -1
            return get_range_text(line, start, end)
        elif r.startswith('..'):
            start = 1
            end = r[2:]
            return get_range_text(line, start, end)
        elif r.endswith('..'):
            start = r[:-2]
            end = -1
            return get_range_text(line, start, end)
        else:
            start = r[:r.find('.')]
            end = r[r.find('.') + 2:]
            return get_range_text(line, start, end)


def some_transform(line):
    if args.delimiter is None:
        if args.nth == '':
            return line
        ranges = args.nth.split(',')
        parts = []
        for r in ranges:
            result = filter_with_range(line, r)
            parts.append(result)
        output = ''.join(parts).rstrip()
        return output
    else:
        pass
    return line


try:
    line = sys.stdin.readline()
    while line:
        line = line.strip("\n")
        line = some_transform(line)
        print(line)
        line = sys.stdin.readline()
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
