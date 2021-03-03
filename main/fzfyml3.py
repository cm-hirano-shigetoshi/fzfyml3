import argparse
from FzfYmlBase import FzfYmlBase

p = argparse.ArgumentParser()
p.add_argument('subcmd', help='run|run-tmux|debug|test')
p.add_argument('yml_path', help='yml file path')
p.add_argument('args', nargs='*', help='arguments')
p.add_argument('--fzf_opts', default=None)
p.add_argument('--rebind_keys', default=None)
args = p.parse_args()

if args.subcmd == 'run':
    fzfyml = FzfYmlBase(args.yml_path, args.args, args.fzf_opts,
                        args.rebind_keys)
    fzfyml.run()
elif args.subcmd == 'run-tmux':
    fzfyml = FzfYmlBase(args.yml_path,
                        args.args,
                        args.fzf_opts,
                        args.rebind_keys,
                        fzf='fzf-tmux')
    fzfyml.run()
elif args.subcmd == 'debug':
    fzfyml = FzfYmlBase(args.yml_path,
                        args.args,
                        args.fzf_opts,
                        args.rebind_keys,
                        debug=True)
    fzfyml.run()
elif args.subcmd == 'test':
    fzfyml = FzfYmlBase(args.yml_path, args.args, args.fzf_opts,
                        args.rebind_keys)
    fzfyml.test()
