import os
import re
import Util
import FzfYmlBase


class Variables():
    def __init__(self, vars_obj):
        # メンバ変数
        # 変数展開する前のvariables
        self.orig_variables = {}
        # 変数展開した後のvariables
        self.variables = {}

        # システム変数を設定
        self._add_system_vars()
        # ymlファイルからの変数を設定
        self.orig_variables.update(vars_obj)
        # 引数を設定
        self.orig_variables.update({
            'arg{}'.format(i + 1): a
            for i, a in enumerate(FzfYmlBase.app_env['args'])
        })

        self.variables = _expand(self.orig_variables)

    def _add_system_vars(self):
        self.orig_variables['python'] = FzfYmlBase.app_env['python']
        self.orig_variables['yml_dir'] = os.path.dirname(
            FzfYmlBase.app_env['yml_path'])
        self.orig_variables['tool_dir'] = FzfYmlBase.app_env['tool_dir']

    def update(self, obj, result={}):
        self.variables = {**self.variables, **result}
        obj = {**obj, **result}
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
