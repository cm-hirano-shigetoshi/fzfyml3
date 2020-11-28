#!/usr/bin/env python
import os
import sys
import argparse

sys.stdout.reconfigure(line_buffering=True)

p = argparse.ArgumentParser()
p.add_argument('target_file')
p.add_argument('-0', '--zero', action='store_true')
p.add_argument('-o', '--fzf_output', action='store_true')
args = p.parse_args()

try:
    stdin_lines = sys.stdin.readlines()
    if args.fzf_output:
        # query
        print(stdin_lines.pop(0), end='')
        # key
        print(stdin_lines.pop(0), end='')
    index_queue = [int(x) for x in stdin_lines.pop(0).split(' ')]
    if len(index_queue) == 0:
        sys.exit()
    index_set = set(index_queue)
    max_index = max(index_set)
    lines = {}
    with open(args.target_file, 'r') as f:
        i = 0 if not args.zero else -1
        while len(index_queue) > 0:
            index = index_queue.pop(0)
            if index in lines:
                print(lines[index])
                continue
            while True:
                i += 1
                line = f.readline()
                if i in index_set:
                    line = line.strip("\n")
                    lines[i] = line
                    if i == index:
                        print(line)
                        break
except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)
