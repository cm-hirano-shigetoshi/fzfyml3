import os
import yaml
import Util
import Task
from Variables import Variables
from Tester import Tester

app_env = None


class FzfYmlBase():
    def __init__(self, args, debug=False):
        global app_env
        # アプリケーションの設定を格納
        app_env = {
            'debug': debug,
            'FZF_DEFAULT_OPTS': os.environ.get('FZF_DEFAULT_OPTS', ''),
            'yml_path': os.path.realpath(args.pop(0)),
            'tool_dir': '/'.join(os.path.realpath(__file__).split('/')[:-2]),
        }

        # FZF_DEFAULT_OPTSは取り込んで独自に使うので削除
        if 'FZF_DEFAULT_OPTS' in os.environ:
            del os.environ['FZF_DEFAULT_OPTS']

        # メンバ変数
        self.yml = {}
        self.args = args
        self.variables = None
        self.task_switch = {}
        self.tasks = []

        # メンバ変数への初期値格納
        with open(app_env['yml_path']) as f:
            self.yml = yaml.load(f, Loader=yaml.SafeLoader)
        self.variables = Variables(self.yml.get('variables', {}), self.args)
        self.task_switch = Util.expand_env_key(self.yml.get('task_switch', {}))
        self.tasks.append(
            Task.construct_base(self.yml['base_task'], self.variables,
                                set(self.task_switch.keys())))

    def run(self):
        result = self.tasks[0].execute()
        while not self._is_job_end(result):
            new_task = Task.clone(self.tasks[-1])
            new_task.update(self.task_switch[result.key], result)
            self.tasks.append(new_task)
            result = self.tasks[-1].execute()
        self.tasks[-1].output(result)

    def test(self):
        tester = Tester(self.yml['test'])
        result = self.tasks[0].execute(tester=tester)
        while not self._is_job_end(result):
            new_task = Task.clone(self.tasks[-1])
            new_task.update(self.task_switch[result.key])
            self.tasks.append(new_task)
            result = self.tasks[-1].execute(tester=tester)
        self.tasks[-1].output(result, tester=tester)

    def _is_job_end(self, result):
        if len(result.key) == 0:
            return True
        if result.key not in self.task_switch:
            return True
        return False
