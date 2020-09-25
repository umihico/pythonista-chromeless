from .chromeless import Chromeless
from .picklelib import loads, dumps
try:
    from .__version__ import __version__
except Exception as e:
    from __version__ import __version__
