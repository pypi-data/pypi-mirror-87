#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import requests

from .connectors import get_connector
from .fxckers._map import fxckers_map
from .logger import _Logger, LOG_LEVELS


class LibreFi:
    def __init__(self, log_level=LOG_LEVELS.INFO, logger=_Logger):
        self.connector = get_connector()()
        self.current_fxcker = None
        self.log_level = log_level
        self.logger = logger
        self.log = self.logger(key="lfi:core", log_level=self.log_level)

        self.log.info("Initialized")

    def _periodical_check(self):
        self.log.debug("Doing periodical check")
        status = self.connector.status()
        self.log.debug("Disconnected" if not status["connected"]
                       else 'Connected to {} ("{}")'.format(
                            status["connection_type"],
                            status["connection_name"]))
        if not status["connected"]:
            self.current_fxcker = None
            networks = self.connector.list()
            chosen_network = None
            for network in networks:
                self._assign_fxcker_to_network(network)
                if self.current_fxcker:
                    chosen_network = network
                    break
            if chosen_network is not None:
                self.log.info(
                    'Connecting to "{}"'
                    .format(network["ssid"]))
                self.connector.connect(chosen_network)
                status = self.connector.status()
            else:
                self.log.info("No eligible network found")
        if status["connected"]:
            if not self.current_fxcker:
                self._assign_fxcker_to_network(
                    {"ssid": status["connection_name"]})
            if self.current_fxcker:
                self.log.debug("Checking internet access")
                check_req = requests.get(
                    "http://detectportal.firefox.com/success.txt",
                    allow_redirects=False)
                if check_req.text.strip() != "success":
                    self.log.info("No internet access, trying {}.unfxck()"
                                  .format(self.current_fxcker.FXCKER_KEY))
                    self.current_fxcker.unfxck(
                        location=check_req.headers.get("Location"),
                    )
                else:
                    self.log.debug("Internet access working")

    def _assign_fxcker_to_network(self, network):
        fxcker = None
        for fxck_element in fxckers_map:
            for fxck_net_name in fxck_element[0]:
                if fxck_net_name[:len("re:")] == "re:":
                    if re.match(fxck_net_name,
                                network["ssid"][len("re:"):]):
                        fxcker = fxck_element[1]
                        break
                elif fxck_net_name == network["ssid"]:
                    fxcker = fxck_element[1]
                    break
        if fxcker:
            self.current_fxcker = fxcker(
                logger=self.logger, log_level=self.log_level)
            self.log.info("Switched fxcker to {}".format(
                self.current_fxcker.FXCKER_KEY))
        return self.current_fxcker
