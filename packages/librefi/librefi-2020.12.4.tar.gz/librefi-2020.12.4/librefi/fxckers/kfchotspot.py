# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._common import BaseFxcker
from ..utils import regex_search_string


class KFCHotspotFxcker(BaseFxcker):
    def unfxck(self, location):
        splash = self.request("GET", location)
        url = regex_search_string(
            r'<a href="([^"]+)" [^>]+id="accept-button">Chcę połączyć się',
            splash.text)
        self.request("GET", url)
        return True
