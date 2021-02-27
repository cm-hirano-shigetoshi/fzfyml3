import os
import yaml
import Util
import Task
from Tester import Tester

app_env = None


class FzfYmlBase():
    def __init__(self, yml_path, args, opts, fzf='fzf', debug=False):
        global app_env
        # アプリケーションの設定を格納
        app_env = {
            'fzf': fzf,
            'debug': debug,
            'python': os.environ.get('FZFYML3_PYTHON', 'python'),
            'FZF_DEFAULT_OPTS': os.environ.get('FZF_DEFAULT_OPTS', ''),
            'fzf_opts': '' if opts is None else opts,
            'yml_path': os.path.realpath(yml_path),
            'tool_dir': '/'.join(os.path.realpath(__file__).split('/')[:-2]),
            'args': args,
        }

        # FZF_DEFAULT_OPTSは取り込んで独自に使うので削除
        if 'FZF_DEFAULT_OPTS' in os.environ:
            del os.environ['FZF_DEFAULT_OPTS']

        # メンバ変数
        self.yml = {}
        self.task_switch = {}
        self.tasks = []

        # メンバ変数への初期値格納
        with open(app_env['yml_path']) as f:
            self.yml = yaml.load(f, Loader=yaml.SafeLoader)
        self.task_switch = Util.expand_env_key(self.yml.get('task_switch', {}))
        self.tasks.append(
            Task.construct_base(self.yml['base_task'],
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
        if 'FZF_DEFAULT_OPTS' in self.yml['test'][0]:
            app_env['FZF_DEFAULT_OPTS'] = self.yml['test'].pop(
                0)['FZF_DEFAULT_OPTS']
        else:
            app_env['FZF_DEFAULT_OPTS'] = ''
        tester = Tester(self.yml['test'])
        result = self.tasks[0].execute(tester=tester)
        while not self._is_job_end(result):
            new_task = Task.clone(self.tasks[-1])
            new_task.update(self.task_switch[result.key], result)
            self.tasks.append(new_task)
            result = self.tasks[-1].execute(tester=tester)
        self.tasks[-1].output(result, tester=tester)

    def _is_job_end(self, result):
        if len(result.key) == 0:
            return True
        if result.key not in self.task_switch:
            return True
        return False
