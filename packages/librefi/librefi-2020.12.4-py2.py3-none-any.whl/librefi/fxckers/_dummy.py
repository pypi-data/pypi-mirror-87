# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._common import BaseFxcker


# for just plain free wi-fi
class DummyFxcker(BaseFxcker):
    def unfxck(self):
        return True
