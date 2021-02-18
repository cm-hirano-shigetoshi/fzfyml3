#!/usr/bin/env python
import os
import sys
import argparse

sys.stdout.reconfigure(line_buffering=True)

p = argparse.ArgumentParser()
p.add_argument('-p',
               '--path',
               default='auto',
               help='auto|absolute|relative (auto)')
p.add_argument('--updir_depth',
               default='3',
               help='auto時に絶対パスと相対パスを切り替える深さ (3)')
p.add_argument('-t',
               '--tilde_home',
               action='store_true',
               help='ホームディレクトリを~にする (False)')
p.add_argument('-s',
               '--slash',
               action='store_true',
               help='ディレクトリの場合末尾に/をつける (False)')
p.add_argument('--curdir', default='.', help='相対パスの起点パス (.)')
args = p.parse_args()


def transform(line):
    is_dir = False
    if line == '~':
        line = os.environ['HOME']
        is_dir = True
    if line.startswith('~/'):
        line = '{}/{}'.format(os.environ['HOME'], line[2:])
        is_dir = os.path.isdir(line)
    if args.path == 'absolute':
        is_dir = os.path.isdir(line)
        line = os.path.abspath(line)
    elif args.path == 'relative':
        is_dir = os.path.isdir(line)
        line = os.path.relpath(line, args.curdir)
    else:
        is_dir = os.path.isdir(line)
        line = os.path.relpath(line, args.curdir)
        if line.startswith('../' * int(args.updir_depth)):
            line = os.path.abspath(line)
    if args.slash and is_dir:
        line += '/'
        line = line.replace('//', '/')
    if args.tilde_home and line.startswith(os.environ['HOME']):
        line = '~{}'.format(line[len(os.environ['HOME']):])
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
