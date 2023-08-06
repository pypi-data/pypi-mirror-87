# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..compat import compat_sys_platform
from ..utils import LFiError


def get_connector():
    if compat_sys_platform == "linux":
        from .networkmanager import NetworkManagerConnector
        return NetworkManagerConnector
    raise LFiError('Could not find a connector')
