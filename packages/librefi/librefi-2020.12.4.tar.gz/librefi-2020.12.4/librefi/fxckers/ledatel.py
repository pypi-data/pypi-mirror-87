# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._common import BaseFxcker


class LedatelFxcker(BaseFxcker):
    def unfxck(self):
        return False
