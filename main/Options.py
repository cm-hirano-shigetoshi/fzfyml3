import shlex
import Util


class Options():
    def __init__(self, options_obj, default_opts, post_operation_expects,
                 task_switch_expects):
        # メンバ変数
        self.options = {}
        self.expects = {}

        # FZF_DEFAULT_OPTSを取り込む
        self.options = _parse_option_text(default_opts)
        # 終了するコマンドをexpectでキャプチャする
        self.expects = {
            'esc': 'quit',
            'ctrl-c': 'quit',
            'ctrl-d': 'quit',
            'ctrl-g': 'quit',
            'ctrl-q': 'quit',
            'ctrl-z': 'quit',
        }
        # post_operationsのexpectを登録
        self.expects.update(
            {k: 'post_operation'
             for k in post_operation_expects})
        # task_switchのexpectを登録
        self.expects.update({k: 'task_switch' for k in task_switch_expects})
        # ymlで指定されたオプションを反映
        self.update(options_obj)
        # '--print-query'は強制的にON
        self.options.update({'print-query': True})

    def update(self, options_obj):
        option_text = ' '.join(['--{}'.format(o) for o in options_obj])
        self.options.update(_parse_option_text(option_text))

    def get_text(self, variables):
        return _get_option_text(self.options, variables, self.expects)


def _get_option_text(options, variables, expects):
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
            v = variables.apply(v)
            v = Util.expand_as_shell(v)
            text_list.append("--{}='{}'".format(k, v))
    text_list.append('--expect={}'.format(','.join(expects)))
    return ' '.join(text_list)


def _parse_option_text(option_text):
    def _is_bool_option(option):
        o = option[5:] if option.startswith('--no-') else option[2:]
        return o in get_bool_options()

    options = {}
    for option in shlex.split(option_text.strip()):
        if _is_bool_option(option):
            if option.startswith('--no-'):
                options[option[5:]] = False
            else:
                options[option[2:]] = True
        else:
            assert '=' in option
            (key, value) = option[2:].split('=')
            options[key] = value
    return options


def get_bool_options():
    return {
        'ansi': True,
        'border': True,
        'cycle': True,
        'exact': True,
        'exit-0': True,
        'extended': True,
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
        'hscroll': False,
        'mouse': False,
        'sort': False,
    }
