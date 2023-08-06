# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._common import BaseFxcker
from ..utils import regex_search_string, absolute_url, dump_qs


class JustWifiFxcker(BaseFxcker):
    # tested with Intercity_WiFi (PKP IC Dart)
    def unfxck(self, location=None):
        start = self.request(
            # flake8: noqa: E501
            "GET", location or "http://tank.justwifi.pl/connect?returnurl=http://detectportal.firefox.com/success.txt%3f",
            resource="start redir")
        redir_url = regex_search_string([
            r'window\.location\.href = "([^"]+)";',
        ], start.text)
        sgu = self.request("GET", redir_url, resource="splash page")
        glash_form_url = absolute_url(regex_search_string([
            r"\$\('#glash_form(?:_adv)?'\).attr\('action', '([^']+)'\);",
            r'<form action="([^"]+)"',
        ], sgu.text), redir_url)
        glash_token = regex_search_string(
            r'<input [^>]*name="glash_step\[_token\]" value="([^"]+)"',
            sgu.text)
        glash_gdc = regex_search_string(
            r'<input [^>]*name="glash_step\[gdc\]" value="([^"]+)" />',
            sgu.text, default=None)
        # /en/p/sgu/glash/forward -> /en/p/sgu/open
        sgu_open = self.request("POST", glash_form_url,
                                resource="glash forward",
                                data=dump_qs({
                                         "glash_step": {
                                             "gdc": glash_gdc,
                                             "_token": glash_token,
                                         },
                                }),
                                headers={
                                    "Referer": sgu.url,
                                    "Content-Type":
                                    "application/x-www-form-urlencoded",
                                },
                                )
        sgu_open_forward_url = absolute_url(regex_search_string(
            r'<form [^>]*action="([^"]+)"',
            sgu_open.text,
            default="http://connect.justwifi.pl/en/p/sgu/open/forward"
        ), sgu_open.url)
        sgu_open_token = regex_search_string(
            r'<input [^>]*name="form\[_token\]" value="([^"]+)"',
            sgu_open.text)
        sgu_after = self.request("POST", sgu_open_forward_url,
                                 resource="sgu after (ad redir page)",
                                 data=dump_qs({
                                     "form": {
                                         "_token": sgu_open_token
                                     }
                                 }), headers={
                                     "Referer": sgu_open.url,
                                     "Content-Type":
                                     "application/x-www-form-urlencoded",
                                 })
        cnt_url = regex_search_string([
            r"var cnt_url = '([^']+)';",
            r'<input [^>]*name="adv_step\[url\]" value="([^"]+)"',
        ], sgu_after.text)
        banner_url_encoded = regex_search_string([
            r"var banner_url_encoded = '([^']+)';",
        ], sgu_after.text, default="")
        bannerzone = regex_search_string([
            r"\$\(\"input\[name='adv_step\[bannerZone\]']\"\)\.val\('([^']+)'\);",
            r'<input [^>]*name="adv_step\[bannerZone\]" value="([^"]+)"',
        ], sgu_after.text)
        sgu_after_token = regex_search_string([
            r'<input [^>]*name="adv_step\[_token\] " value="([^"]+)"',
        ], sgu_after.text)
        sgu_after_form_url = absolute_url(regex_search_string([
            r'<form [^>]*action="([^"]+)"',
        ], sgu_after.text), sgu_after.url)
        self.request("POST", sgu_after_form_url,
                     resource="ad campaign redir",
                     data=dump_qs({
                         "adv_step": {
                             # "cta" | "nothanks" | "skip"
                             "action": "cta",
                             "bannerZone": bannerzone,
                             "url": cnt_url + banner_url_encoded
                             if cnt_url is str and banner_url_encoded is str
                             else "http://connect.justwifi.pl/en/mgbc/%s/l"
                             % (bannerzone),
                             "_token": sgu_after_token,
                         },
                     }), headers={
                         "Referer": sgu_after.url,
                         "Content-Type": "application/x-www-form-urlencoded",
                     })
        return True
