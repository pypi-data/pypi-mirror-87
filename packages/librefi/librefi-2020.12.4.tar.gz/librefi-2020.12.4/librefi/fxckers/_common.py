# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from ..utils import get_user_agent, absolute_url


class BaseFxcker:
    def __init__(self, logger, log_level):
        self.cookie_jar = requests.cookies.RequestsCookieJar()
        self.user_agent = get_user_agent()
        self.log = logger(key=self.FXCKER_KEY, log_level=log_level)

    @property
    def FXCKER_KEY(self):
        return self.__class__.__name__[:-6]

    def request(self, method, url, resource=None,
                follow_redirects=True, redirect_count=0, **kwargs):
        kwargs["cookies"] = self.cookie_jar
        if not kwargs.get("headers"):
            kwargs["headers"] = {}
        if not kwargs["headers"].get("User-Agent"):
            kwargs["headers"]["User-Agent"] = self.user_agent
        if not kwargs.get("allow_redirects"):
            kwargs["allow_redirects"] = False
        self.log.info("Requesting " +
                      (resource if resource is not None
                       else (str(method) + " " + str(url)))
                      + (" (redirect #%d)" % (redirect_count)
                         if redirect_count > 0
                         else ""))
        sess = requests.Session()
        req = sess.request(method, url, **kwargs)
        self.cookie_jar.update(sess.cookies)
        if follow_redirects is True and req.headers.get("Location"):
            kwargs["data"] = None
            kwargs["headers"]["Referer"] = url
            new_url = absolute_url(req.headers.get("Location"), url)
            return self.request("GET", new_url,
                                resource=resource,
                                follow_redirects=follow_redirects,
                                redirect_count=(redirect_count + 1),
                                **kwargs)
        return req
