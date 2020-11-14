import Util


class PostOperations():
    def __init__(self, post_operations_obj):
        # メンバ変数
        self.post_operations = {}

        # メンバ変数への初期値格納
        self.post_operations = _set_post_operations(post_operations_obj)

    def output(self, result, tester=None):
        if result.key in self.post_operations:
            for key, value in self.post_operations[result.key].items():
                if key == 'pipe':
                    assert type(value) is not None
                    result.selected = Util.pipeline('\n'.join(result.selected),
                                                    value).split('\n')
                    continue
                if key == 'join':
                    delimiter = ' ' if value is None else value
                    assert type(delimiter) is str
                    result.selected = [delimiter.join(result.selected)]
                    continue
                if key == 'json':
                    result.selected = [result.to_json()]
                    continue
        _print_output(result, tester)


def _set_post_operations(post_operations_obj):
    obj = {}
    for key, value in post_operations_obj.items():
        obj[key] = Util.array_to_obj(value)
    return obj


def _print_output(result, tester=None):
    if len(result.selected) == 1:
        text = result.selected[0]
    else:
        text = '\n'.join(result.selected) + '\n'
    if tester is not None:
        tester.test_output(text)
    print(text, end='')
