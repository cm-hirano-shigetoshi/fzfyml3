import os
import sys
from FzfYmlBase import FzfYmlBase

if sys.argv[1] == 'run':
    fzfyml = FzfYmlBase(sys.argv[2:])
    fzfyml.run()
elif sys.argv[1] == 'debug':
    os.environ['FZFYML_DEBUG'] = '1'
    fzfyml = FzfYmlBase(sys.argv[2:])
    fzfyml.run()
elif sys.argv[1] == 'test':
    os.environ['FZFYML_TEST'] = '1'
    fzfyml = FzfYmlBase(sys.argv[2:])
    fzfyml.test()
