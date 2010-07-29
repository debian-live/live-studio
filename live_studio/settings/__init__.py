import sys

from defaults import *

if sys.argv[1:2] == ['test']:
    from roles.test import *
elif sys.argv[1:2] == ['build']:
    exec "from roles.%s import *" % sys.argv[2]
else:
    from role import *

    try:
        from custom import *
    except ImportError:
        pass
