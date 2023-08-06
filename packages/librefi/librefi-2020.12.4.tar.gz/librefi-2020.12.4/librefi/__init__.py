# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from .librefi import LibreFi
from .logger import _Logger, LOG_LEVELS
from .utils import LFiError, FxckerError


def _real_main(argv=None):
    librefi = LibreFi(logger=_Logger, log_level=LOG_LEVELS.DEBUG)
    librefi._periodical_check()


def main(argv=None):
    try:
        _real_main(argv)
    except LFiError:
        sys.exit('ERROR (core): report this to librefi@selfisekai.rocks')
    except FxckerError:
        sys.exit('ERROR (fxcker): report this to librefi@selfisekai.rocks')
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')


__all__ = [
    'LibreFi',
    'main',
]
