import sys
from Result import Result


class Tester():
    def __init__(self, test_array):
        # メンバ変数
        self.test_array = test_array

    def test_command(self, text):
        if 'answer_command' in self.test_array[0]:
            answer_command = self.test_array.pop(0)['answer_command']
            if not _is_same(answer_command, text):
                print('[TEST FAILED]: {}\nexpected: {}\n command: {}'.format(
                    'answer_command', _comparable(answer_command), _comparable(text)))
                sys.exit(1)
            if len(self.test_array) == 0:
                sys.exit(0)

    def test_output(self, text):
        if 'answer_output' in self.test_array[0]:
            answer_output = self.test_array.pop(0)['answer_output']
            if not _is_same(answer_output, text):
                print('[TEST FAILED]: {}\nexpected: {}\n  output: {}'.format(
                    'answer_output', _comparable(answer_output), _comparable(text)))
                sys.exit(1)
            if len(self.test_array) == 0:
                sys.exit(0)

    def get_result(self):
        assert 'result' in self.test_array[0]
        result_obj = self.test_array.pop(0)['result']
        result = Result('{}\n{}\n{}'.format(
            result_obj['query'], result_obj['key'],
            '\n'.join(result_obj['output']) + '\n'))
        return result


def _is_same(answer, text):
    return _comparable(answer) == _comparable(text)

def _comparable(string):
    return string.replace('\n', r'\n')
