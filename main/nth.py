#!/usr/bin/env python
import os
import re
import sys
import argparse

sys.stdout.reconfigure(line_buffering=True)

p = argparse.ArgumentParser()
p.add_argument('nth')
p.add_argument('-d', '--delimiter', default=None)
p.add_argument('-p', '--plus', action='store_true')
args = p.parse_args()


def filter_with_range(line, r, d):
    if d is None:
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
    else:
        if '..' not in r:
            # 単一要素指定
            r = int(r) - 1 if int(r) > 0 else int(r)
            return line.split(d)[r]
        else:
            # 範囲指定
            def get_range_text(line, start, end):
                islands = line.split(d)
                start = int(start) - 1 if int(start) > 0 else int(start)
                if int(end) == -1:
                    return d.join(islands[start:])
                else:
                    end = int(end) if int(end) > 0 else int(end) + 1
                    return d.join(islands[start:end])

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
    if args.nth == '':
        return line
    ranges = args.nth.split(',')
    parts = []
    for r in ranges:
        result = filter_with_range(line, r, args.delimiter)
        parts.append(result)
    output = ''.join(parts).lstrip().rstrip()
    return output


try:
    line = sys.stdin.readline()
    lines = []
    while line:
        line = line.strip("\n")
        line = some_transform(line)
        if args.plus:
            lines.append(line)
        else:
            print(line)
        line = sys.stdin.readline()
    if args.plus:
        print(' '.join(lines))
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
