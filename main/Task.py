import sys
import subprocess
import Util
import tempfile
import FzfYmlBase
from subprocess import PIPE
from Options import Options
from Variables import Variables
from Result import Result
from PostOperations import PostOperations


class Task():
    def __init__(self, source, source_transform, options, post_operations,
                 variables):
        # メンバ変数
        self.source = source
        self.source_transform = source_transform
        self.options = options
        self.variables = variables
        self.post_operations = post_operations

    def execute(self, tester=None):
        if tester is None:
            cmd = self._get_command()
            if FzfYmlBase.app_env['debug']:
                print(cmd)
            raw_output_text = _execute_fzf_command(cmd)
            if FzfYmlBase.app_env['debug']:
                print(raw_output_text)
            result = Result(raw_output_text)
            if FzfYmlBase.app_env['debug']:
                print(result.to_json())
            return result
        else:
            cmd = self._get_command(tester=tester)
            tester.test_command(cmd)
            result = tester.get_result()
            return result

    def output(self, result, tester=None):
        if len(result.key) > 0 and result.key in self.options.get_expects():
            operation_type = self.options.get_expects()[result.key]
            assert operation_type != 'task_switch'
            if operation_type == 'quit':
                sys.exit()
        self.post_operations.output(result, self.variables, tester=tester)

    def update(self, update_obj, result):
        result_obj = {
            'query': result.query,
            'key': result.key,
            'output': '\n'.join(result.selected),
        }
        source = update_obj.get('source', None)
        source_transform = update_obj.get('source_transform', None)
        options = ['query="{}"'.format(result.query.replace('"', r'\"'))]
        options.extend(update_obj.get('options', []))
        post_operations = update_obj.get('post_operations', {})

        if source:
            self.source = source
        if source_transform:
            self.source_transform = source_transform
        self.options.update(options)
        self.variables.update(update_obj.get('variables', {}),
                              result=result_obj)
        self.post_operations.update(post_operations)

    def _get_command(self, tester=None):
        if self.source_transform is not None:
            tmp_dir_name = tempfile._get_default_tempdir()
            tmp_transform = '{}/{}'.format(
                tmp_dir_name, next(tempfile._get_candidate_names()))
            tmp_index = '{}/{}'.format(tmp_dir_name,
                                       next(tempfile._get_candidate_names()))
            if tester:
                tmp_transform = './tmp_transform'
                tmp_index = './tmp_index'
            else:
                Util.touch_empty_file(tmp_transform)
                Util.touch_empty_file(tmp_index)
            self.options.insert_echo_index_preview(tmp_index)
            params = {
                'source':
                self._get_source(),
                'tmp_transform':
                tmp_transform,
                'source_transform':
                self._get_source_transform(),
                'option':
                self.options.get_text(self.variables, temp=tmp_transform),
                'tmp_index':
                tmp_index,
                'line_selector':
                FzfYmlBase.app_env['tool_dir'] + '/main/line_selector.py',
            }
            pipeline = []
            pipeline.append('{0[source]}')
            pipeline.append('tee {0[tmp_transform]}')
            pipeline.append('cat')
            pipeline.append('{0[source_transform]}')
            pipeline.append('fzf {0[option]}')
            pipeline.append('head -2')
            pipeline.append('cat - {0[tmp_index]}')
            pipeline.append(
                'python {0[line_selector]} -o -0 {0[tmp_transform]}')
            cmd = ' | '.join(pipeline).format(params)
            return cmd
        else:
            return '{} | fzf {}'.format(self._get_source(),
                                        self.options.get_text(self.variables))

    def _get_source(self):
        return self.variables.apply(self.source)

    def _get_source_transform(self):
        return self.variables.apply(self.source_transform)


def construct_base(base_task_obj, switch_expects):
    # コンストラクタはbase_task作成時にのみ呼ばれる
    post_operations = Util.expand_env_key(
        base_task_obj.get('post_operations', {}))
    return Task(
        base_task_obj['source'], base_task_obj.get('source_transform', None),
        Options(base_task_obj.get('options', []), post_operations.keys(),
                switch_expects), PostOperations(post_operations),
        Variables(base_task_obj.get('variables', {})))


def clone(task):
    return Task(task.source, task.source_transform, task.options,
                task.post_operations, task.variables)


def _execute_fzf_command(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=PIPE, text=True)
    return proc.stdout
