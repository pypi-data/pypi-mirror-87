# -*- coding: utf-8 -*-
"""rackio_opcua/folder.py

This module implements the folder class for RackioOPCUA.
"""

from .updater import TagUpdater
from .device import Device

class Folder:

    def __init__(self, name, server, idx):

        self.name = name
        self.server = server
        self.idx = idx

        self._folder = server.nodes.objects.add_folder(idx, name)

        self.devices = list()

    def define_device(self, name):

        folder = self._folder
        idx = self.idx

        device = Device(name, folder, idx)

        self.devices.append(device)

        return device

    def get_mappings(self):

        result = list()

        for device in self.devices:

            result += device.get_mappings()

        return result
    