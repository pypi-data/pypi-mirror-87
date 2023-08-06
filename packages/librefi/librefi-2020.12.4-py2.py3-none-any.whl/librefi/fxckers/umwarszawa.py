# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._common import BaseFxcker
from ..utils import regex_search_string, dump_qs


class UMWarszawaFxcker(BaseFxcker):
    _BASE_URL = "https://hotspotsystem.um.warszawa.pl"

    def unfxck(self):
        start_page = self.request(
            "GET", self._BASE_URL + "/free/index.php").text
        id = regex_search_string(
            r'<input type="hidden" name="id" value="(\d+)"/>', start_page)
        self.request("POST", self._BASE_URL +
                     "/free/login.php", data=dump_qs({
                         "id": id,
                         "register": "I accept - Connect me",
                     }))
        return True
