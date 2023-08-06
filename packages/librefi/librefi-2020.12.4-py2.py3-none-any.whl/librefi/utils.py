# -*- coding: utf-8 -*-
# flake8: noqa: E501
from __future__ import unicode_literals

import re
from datetime import datetime
import random

from .compat import (
    compat_parse_qs as parse_qs,
    compat_urllib_parse_quote as qs_quote,
    compat_urllib_parse_urlparse as urlparse,
    compat_str,
    py_major_ver,
)


class LFiError(Exception):
    pass


class FxckerError(Exception):
    pass


def get_user_agent():
    if bool(random.getrandbits(1)):
        # Google Chrome
        return ("Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
                ).format(platform=random.choice([
                    "Windows NT 10.0; Win64; x64",
                    "Windows NT 10.0; WOW64",
                    "Windows NT 10.0",
                ]), version=random.choice([
                    # https://en.wikipedia.org/wiki/Google_Chrome_version_history
                    # https://bin.ptrcnull.me/uruyewogug.js
                    "64.0.3282",
                    "65.0.3325",
                    "66.0.3359",
                    "67.0.3396",
                    "68.0.3440",
                    "69.0.3497",
                    "70.0.3538",
                    "71.0.3578",
                    "72.0.3626",
                    "73.0.3683",
                    "74.0.3729",
                    "75.0.3770",
                    "76.0.3809",
                    "77.0.3865",
                    "78.0.3904",
                    "79.0.3945",
                    "80.0.3987",
                    "81.0.4044",
                    "83.0.4103",
                    "84.0.4147",
                    "85.0.4183",
                    "86.0.4240",
                    "87.0",
                    "87.0",
                ]))
    else:
        # Mozilla Firefox
        return ("Mozilla/5.0 ({platform}; rv:{version}) Gecko/20100101 Firefox/{version}"
                ).format(platform=random.choice([
                    "Windows NT 10.0; Win64; x64",
                    "Windows NT 10.0",
                ]), version=random.choice([
                    # https://www.mozilla.org/en-US/firefox/releases/
                    # https://bin.ptrcnull.me/dijaboyewi.js
                    "80.0",
                    "79.0",
                    "78.0",
                    "77.0",
                    "76.0",
                    "75.0",
                    "74.0",
                    "73.0",
                    "72.0",
                    "71.0",
                    "70.0",
                    "69.0",
                    "68.0",
                ]))


def get_email_address():
    time_now = datetime.now()
    if time_now.month == 5 and time_now.day == 17:
        # https://en.wikipedia.org/wiki/International_Day_Against_Homophobia,_Transphobia_and_Biphobia
        return random.choice([
            "biuro@ordoiuris.pl",
            "kontakt@stronazycia.pl",
            "kontakt@petycjaonline.pl",
            "gejprzeciwkoswiatu@gmail.com",
            "biuro.prasowe@konfederacja.net",
            "biuro@pis.org.pl",
            "Zbigniew.Ziobro@sejm.pl",
        ])

    email = ""
    for i in range(random.randint(6, 18)):
        email += chr(97 + random.randint(0, 24))
    return email + "@" + random.choice([
        "gmail.com", "outlook.com", "live.com",
    ])


def regex_search_string(regexes, string, default=None, multiple=False, whole_match=False):
    if not isinstance(regexes, list):
        regexes = [regexes]
    results = []
    for regex in regexes:
        if multiple:
            matches = re.finditer(regex, string)
            for match in matches:
                if not whole_match:
                    match = match.group(1)
                results.append(match)
        else:
            match = re.search(regex, string)
            if match:
                if not whole_match:
                    match = match.group(1)
                return match
    if multiple:
        return results
    return default


def dump_qs(obj):
    if py_major_ver == 2:
        old_qs = obj.iteritems()
    else:
        old_qs = list(obj.items())
    # sorting by key to unify the result string between python versions
    # https://stackoverflow.com/a/3295662/8222484
    old_qs.sort()
    qs = []
    not_flat = True
    while not_flat:
        not_flat = False
        for old_qs_element in old_qs:
            if isinstance(old_qs_element[1], (compat_str, int, float)):
                qs.append((old_qs_element[0], old_qs_element[1]))
            elif isinstance(old_qs_element[1], (dict)):
                for subkey in old_qs_element[1]:
                    if old_qs_element[1][subkey] is not None:
                        qs.append(
                            (old_qs_element[0] + "[" + subkey + "]", old_qs_element[1][subkey]))
                        if isinstance(old_qs_element[1][subkey], (dict, list)):
                            not_flat = True
            elif isinstance(old_qs_element[1], (list)):
                for index in range(len(old_qs_element[1])):
                    element = old_qs_element[1][index]
                    if element is not None:
                        qs.append(
                            (old_qs_element[0] + "[" + compat_str(index) + "]", element))
                        if isinstance(element, (dict, list)):
                            not_flat = True
        if not_flat:
            old_qs = qs
            qs = []
    strng = ""
    for el in qs:
        strng += qs_quote(compat_str(el[0]).encode("utf-8")) + "=" + \
            qs_quote(compat_str(el[1]).encode("utf-8")) + "&"
    return strng[:-1]


def absolute_url(new_url, old_url):
    if new_url.startswith("http:") or new_url.startswith("https:"):
        return new_url

    old = urlparse(old_url)
    scheme = old.scheme if old.scheme is not None else "http"

    if new_url.startswith("://"):
        return scheme + new_url
    if new_url.startswith("//"):
        return scheme + ":" + new_url

    hostname = old.netloc

    if new_url.startswith("/"):
        return scheme + "://" + hostname + new_url

    # like "hostname/path?query", if other checks fail
    return scheme + "://" + new_url
