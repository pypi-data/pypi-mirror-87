"""Import *contents* of all submodules.

This is a dynamic (run-time) versions of this:
from .std  import *
from .misc import *
from .math import *
...

Don't want to put this in pylib/__init__.py,
(even if just using __all__, which won't yield submodule contents),
coz then I cannot selectively import a submodule (eg pylib.math.py)
without executing the others.
"""

# from importlib import import_module
from pathlib import Path as _Path # mangle to avoid cleaning up std.py:Path below.

def import_contents(f):
    """https://stackoverflow.com/a/41991139/38281"""

    module = __import__(__package__+"."+f.stem, fromlist=['*'])
    # module = import_module("."+f.stem, __package__)

    # Filter keys
    if hasattr(module, '__all__'):
        keys = module.__all__
    else:
        keys = [k for k in dir(module) if not k.startswith('_')]

    # Update globals
    globals().update({k: getattr(module, k) for k in keys})

# https://stackoverflow.com/a/60861023
for f in _Path(__file__).parent.glob("*.py"):
    if f!=_Path(__file__) and not f.stem.startswith("_"):
        import_contents(f)
# Recursive solution (if that's ever needed):
# https://stackoverflow.com/q/3365740

# Clean up.
del _Path, f
