import json
import Util


class PostOperations():
    def __init__(self, post_operations_obj):
        # メンバ変数
        self.post_operations = []

        # メンバ変数への初期値格納
        self.post_operations = post_operations_obj

    def output(self, result, variables, tester=None):
        if result.key in self.post_operations:
            for operation in self.post_operations[result.key]:
                if type(operation) == str:
                    operation = {operation: None}
                for key, value in operation.items():
                    if key == 'print-query-key':
                        result.selected.insert(0, result.query)
                        result.selected.insert(1, result.key)
                        continue
                    if key == 'print-query':
                        result.selected.insert(0, result.query)
                        continue
                    if key == 'print-key':
                        result.selected.insert(0, result.key)
                        continue
                    if key == 'pipe':
                        assert type(value) is not None
                        value = variables.apply(value)
                        result.selected = Util.pipeline(
                            '\n'.join(result.selected), value).split('\n')
                        continue
                    if key == 'join':
                        delimiter = ' ' if value is None else value
                        assert type(delimiter) is str
                        result.selected = [delimiter.join(result.selected)]
                        continue
                    if key == 'json':
                        result.selected = [result.to_json()]
        _print_output(result, tester)

    def update(self, obj):
        self.post_operations.update(obj)


def _print_output(result, tester=None):
    if len(result.selected) == 1:
        text = result.selected[0]
    else:
        text = '\n'.join(result.selected) + '\n'
    if tester is not None:
        tester.test_output(text)
    print(text, end='')
