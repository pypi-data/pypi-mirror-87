# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._common import BaseFxcker
from ..utils import regex_search_string, dump_qs


class IPartnersFxcker(BaseFxcker):
    # made for McD-Hotspot (PL)
    def unfxck(self, location=None):
        startpage = self.request("GET", location)
        url = regex_search_string(
            r'<form method="POST" action=\'([^\']+)\'', startpage.text)
        username = regex_search_string(
            r'<input type="hidden" name="username" value="([^"]+)"',
            startpage.text)
        password = regex_search_string(
            r'<input type="hidden" name="password" value="([^"]+)"',
            startpage.text)
        success_url = regex_search_string(
            r'<input type="hidden" name="success_url" value="([^"]+)"',
            startpage.text)
        self.request("POST", url, data=dump_qs({
            "username": username,
            "password": password,
            "success_url": success_url,
        }), headers={
            "Content-Type": "application/x-www-form-urlencoded",
        })
        # should work (?)
        return True
