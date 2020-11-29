import os
import re
import subprocess
from subprocess import PIPE
from subprocess import DEVNULL


def expand_env_key(expect_key_obj, prefix='FZFYML'):
    new_expect_key_obj = {}
    for key, value in expect_key_obj.items():
        if '=' in key:
            env_key = '{}_{}'.format(prefix, key.split('=')[0])
            new_key = os.environ.get(env_key, key.split('=')[1])
            assert (new_key not in new_expect_key_obj)
            new_expect_key_obj[new_key] = value
        else:
            assert (key not in new_expect_key_obj)
            new_expect_key_obj[key] = value
    return new_expect_key_obj


def array_to_obj(array):
    obj = {}
    for x in array:
        if type(x) is str:
            obj[x] = None
        elif type(x) is dict:
            obj.update(x)
    return obj


def find_obj_value(obj, pattern, regex=False):
    for k, v in obj.items():
        v = str(v)
        if regex:
            m = re.search(pattern, v)
            if m is not None:
                return k
        else:
            if v.find(pattern) >= 0:
                return k
    return None


def expand_object_as_shell(obj):
    for k, v in obj.items():
        obj[k] = expand_as_shell(v)
    return obj


def expand_as_shell(text, last_new_line=False):
    proc = subprocess.run('echo "{}"'.format(text),
                          shell=True,
                          stdout=PIPE,
                          stderr=PIPE,
                          text=True)
    if last_new_line:
        return proc.stdout
    else:
        return proc.stdout[:-1]


def pipeline(input_text, cmd, last_new_line=False):
    proc = subprocess.run(cmd,
                          shell=True,
                          input=input_text,
                          stdout=PIPE,
                          text=True)
    if last_new_line:
        return proc.stdout
    else:
        return proc.stdout[:-1]


def check_command_exit(cmd):
    try:
        subprocess.run(cmd,
                       shell=True,
                       stdout=DEVNULL,
                       stderr=DEVNULL,
                       check=True)
    except Exception:
        return False
    return True


def touch_empty_file(file_path):
    with open(file_path, 'w') as f:
        f.write('')
