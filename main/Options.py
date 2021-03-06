import re
import shlex
import Util
import FzfYmlBase


class Options():
    def __init__(self, options_yml, post_operation_expects,
                 task_switch_expects):
        # メンバ変数
        self.post_operation_expects = post_operation_expects
        self.task_switch_expects = task_switch_expects
        self.options_yml = options_yml
        self.echo_index_file_in_preview = None

    def insert_echo_index_preview(self, file_path):
        self.echo_index_file_in_preview = file_path

    def get_options(self):
        # FZF_DEFAULT_OPTSを取り込む
        options = _parse_option_text(FzfYmlBase.app_env['FZF_DEFAULT_OPTS'])
        # ymlで指定されたオプションを反映
        options.update(
            _parse_option_text(' '.join(
                ['--{}'.format(o) for o in self.options_yml])))
        # '--print-query'は強制的にON
        options.update({'print-query': True})
        if self.echo_index_file_in_preview is not None:
            options['preview'] = 'echo {} > {}; '.format(
                '{+n}', self.echo_index_file_in_preview) + options.get(
                    'preview', '')
        return options

    def get_expects(self):
        # 終了するコマンドをexpectでキャプチャする
        expects = {
            'esc': 'quit',
            'ctrl-c': 'quit',
            'ctrl-d': 'quit',
            'ctrl-g': 'quit',
            'ctrl-q': 'quit',
            'ctrl-z': 'quit',
        }
        # post_operationsのexpectを登録
        expects.update(
            {k: 'post_operation'
             for k in self.post_operation_expects})
        # task_switchのexpectを登録
        expects.update({k: 'task_switch' for k in self.task_switch_expects})
        return expects

    def get_text(self, variables, temp=None):
        options = self.get_options()
        expects = self.get_expects()
        return _get_option_text(options, variables, expects, temp=temp)

    def update(self, obj):
        self.options_yml.extend(obj)


def _get_option_text(options, variables, expects, temp):
    def _get_bool_option_text(key, b):
        if get_bool_options()[key] == b:
            if get_bool_options()[key] is True:
                return '--{}'.format(key)
            else:
                return '--no-{}'.format(key)
        else:
            return ''

    text_list = []
    for k, v in options.items():
        if type(v) is bool:
            bool_option = _get_bool_option_text(k, v)
            if len(bool_option) > 0:
                text_list.append(bool_option)
        else:
            if temp is not None and (k == 'preview' or k == 'bind'):
                v = _expand_nth(v, temp, options.get('delimiter', None))
            v = variables.apply(v)
            if k == 'preview' or k == 'bind':
                text_list.append("--{}='{}'".format(k, v))
            else:
                v = Util.expand_as_shell(v)
                v = v.replace('"', r'\"')
                text_list.append('--{}="{}"'.format(k, v))
    text_list.append('--expect={}'.format(','.join(expects)))
    return ' '.join(text_list)


def _parse_option_text(option_text):
    def _get_expanded_abbr(option_text):
        option_queue = shlex.split(option_text.strip())
        while len(option_queue) > 0:
            option = option_queue.pop(0)
            if len(option) != 2:
                yield option
            else:
                long_option = get_long_option(option)
                if long_option.endswith('='):
                    yield '{}"{}"'.format(long_option, option_queue.pop(0))
                else:
                    yield long_option

    def _is_bool_option(option):
        o = option[5:] if option.startswith('--no-') else option[2:]
        return o in get_bool_options()

    options = {}
    for option in _get_expanded_abbr(option_text):
        if _is_bool_option(option):
            if option.startswith('--no-'):
                options[option[5:]] = False
            else:
                options[option[2:]] = True
        else:
            assert '=' in option
            sp = option[2:].split('=')
            (key, value) = (sp[0], '='.join(sp[1:]))
            options[key] = value
    return options


def get_long_option(option):
    return {
        '-x': '--extended',
        '+x': '--no-extended',
        '-e': '--exact',
        '-n': '--nth=',
        '-d': '--delimiter=',
        '+s': '--on-sort',
        '-m': '--multi',
        '-q': '--query=',
        '-1': '--select-1',
        '-0': '--exit-0',
        '-f': '--filter=',
    }[option]


def get_bool_options():
    return {
        'ansi': True,
        'border': True,
        'cycle': True,
        'exact': True,
        'exit-0': True,
        'filepath-word': True,
        'literal': True,
        'multi': True,
        'phony': True,
        'print-query': True,
        'print0': True,
        'read0': True,
        'reverse': True,
        'select-1': True,
        'sync': True,
        'tac': True,
        'bold': False,
        'extended': False,
        'hscroll': False,
        'mouse': False,
        'sort': False,
    }


def _expand_nth(cmd, temp, delimiter):
    line_selector = FzfYmlBase.app_env['tool_dir'] + '/main/line_selector.py'
    nth_filter = FzfYmlBase.app_env['tool_dir'] + '/main/nth.py'
    matches = [m for m in re.finditer(r'{?{(\+?)([-0-9\.,]*)}}?', cmd)]
    for m in reversed(matches):
        if m.group(0).startswith('{{') and m.group(0).endswith('}}'):
            cmd = cmd[:m.start()] + '{' + m.group(1) + m.group(
                2) + '}' + cmd[m.end():]
        else:
            cmd = cmd[:m.start(
            )] + '$(echo {} | {} {} --zero {} | {} {} {}{}-- "{}")'.format(
                '{' + m.group(1) + 'n}', FzfYmlBase.app_env['python'],
                line_selector, temp, FzfYmlBase.app_env['python'], nth_filter,
                '--plus ' if len(m.group(1)) > 0 else '',
                '--delimiter "{}" '.format(delimiter)
                if delimiter is not None else '', m.group(2)) + cmd[m.end():]
    return cmd
