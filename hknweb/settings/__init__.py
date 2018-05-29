import os
import sys

HKNWEB_MODE = os.environ['HKNWEB_MODE'].lower()

if HKNWEB_MODE == 'dev':
    from .dev import *
elif HKNWEB_MODE == 'prod':
    from .prod import *
else:
    print("HKNWEB_MODE is not a valid value")
    sys.exit()
