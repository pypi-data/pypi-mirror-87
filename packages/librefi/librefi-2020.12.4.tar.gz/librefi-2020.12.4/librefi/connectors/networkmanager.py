# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess
import pipes
import re


class NetworkManagerConnector:
    NMCLI_BASE = ["nmcli", "--mode", "tabular", "--terse", "--colors", "no"]

    def _call_nmcli(self, args, parse=True):
        try:
            subp = subprocess.check_output(self.NMCLI_BASE + args).decode("utf-8")
        except subprocess.CalledProcessError as err:
            subp = err.output.decode("utf-8")

        if parse:
            # if no output
            if subp.strip() == "":
                return []

            return [
                [field.replace("\\:", ":")
                    for field in re.split(r"(?<!\\):", line)]
                for line in subp.strip().split("\n")]

        return subp

    def status(self):
        infs = self._call_nmcli(["--fields", "TYPE,NAME",
                                 "connection", "show",
                                 "--active"])
        for inf in infs:
            if inf[0] == "802-3-ethernet":
                return {
                    "connected": True,
                    "connection_type": "wired",
                    "connection_name": inf[1],
                }
        for inf in infs:
            if inf[0] == "802-11-wireless":
                return {
                    "connected": True,
                    "connection_type": "wifi",
                    "connection_name": inf[1],
                }
        return {
            "connected": False,
        }

    def list(self):
        infs = self._call_nmcli(["--fields", "SSID,SIGNAL,SECURITY,IN-USE",
                                 "device", "wifi", "list"])
        networks = []
        for inf in infs:
            networks.append({
                "ssid": inf[0],
                "signal": int(inf[1]),
                "is_open": inf[2] == "",  # does it require password?
                "currently_connected": inf[3] == "*",
            })
        return networks

    def rescan(self):
        self._call_nmcli(["device", "wifi", "rescan"], parse=False)

    def connect(self, network):
        self._call_nmcli(["device", "wifi", "connect",
                          pipes.quote(network["ssid"])], parse=False)
