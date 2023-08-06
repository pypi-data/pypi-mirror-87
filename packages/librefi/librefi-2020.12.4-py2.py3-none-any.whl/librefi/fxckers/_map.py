# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._dummy import DummyFxcker
from .umwarszawa import UMWarszawaFxcker
from .ledatel import LedatelFxcker
from .ipartners import IPartnersFxcker
from .kfchotspot import KFCHotspotFxcker
from .justwifi import JustWifiFxcker

fxckers_map = [
    ([r"re:MZK Opole \d{3}(?: (?:2.4|5)GHz)?"], DummyFxcker),
    (["UM-Warszawa"], UMWarszawaFxcker),
    (["Pendolino_WiFi"], LedatelFxcker),
    (["McD-Hotspot"], IPartnersFxcker),
    (["KFC Hotspot"], KFCHotspotFxcker),
    ([
        "Intercity_WiFi",
        "_PKP_WIFI",
    ], JustWifiFxcker),
]

__all__ = ['fxckers_map']
