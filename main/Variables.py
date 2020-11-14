import os
import re
import Util
import FzfYmlBase


class Variables():
    def __init__(self, vars_obj, args):
        # メンバ変数
        self.orig_variables = {}
        self.variables = {}

        # システム変数を設定
        self._add_system_vars(FzfYmlBase.app_env['yml_path'])
        # ymlファイルからの変数を設定
        self.orig_variables.update(vars_obj)
        # 引数を設定
        self.orig_variables.update(
            {'arg{}'.format(i + 1): a
             for i, a in enumerate(args)})

        self.variables = _expand(self.orig_variables)

    def _add_system_vars(self, yml_path):
        self.orig_variables['ymldir'] = os.path.dirname(yml_path)

    def update(self, obj):
        self.orig_variables = {**self.variables, **obj}
        self.variables = _expand_variables_with_obj(self.orig_variables,
                                                    self.variables)
        self.variables = Util.expand_object_as_shell(self.variables)

    def apply(self, text):
        return _expand_text(text, self.variables)


def _expand(variables):
    # 変数の展開
    variables = _expand_variables_with_obj(variables, variables)
    # シェルコマンドとして展開
    variables = Util.expand_object_as_shell(variables)
    return variables


def _expand_variables_with_obj(variables, obj):
    key = Util.find_obj_value(variables, r'{{\w+}}', regex=True)
    while key is not None:
        variables[key] = _expand_text(variables[key], obj)
        key = Util.find_obj_value(variables, r'{{\w+}}', regex=True)
    return variables


def _expand_text(text, obj):
    matches = [m for m in re.finditer(r'{{(\w+)}}', text)]
    for m in reversed(matches):
        text = '{}{}{}'.format(text[:m.start():], obj[m.group(1)],
                               text[m.end():])
    return text
