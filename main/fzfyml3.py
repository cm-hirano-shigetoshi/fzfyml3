import sys
from FzfYmlBase import FzfYmlBase

if sys.argv[1] == 'run':
    fzfyml = FzfYmlBase(sys.argv[2:])
    fzfyml.run()
elif sys.argv[1] == 'run-tmux':
    fzfyml = FzfYmlBase(sys.argv[2:], fzf='fzf-tmux')
    fzfyml.run()
elif sys.argv[1] == 'debug':
    fzfyml = FzfYmlBase(sys.argv[2:], debug=True)
    fzfyml.run()
elif sys.argv[1] == 'test':
    fzfyml = FzfYmlBase(sys.argv[2:])
    fzfyml.test()
