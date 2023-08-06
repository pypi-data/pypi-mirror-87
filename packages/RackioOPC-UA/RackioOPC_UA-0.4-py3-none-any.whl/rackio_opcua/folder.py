# -*- coding: utf-8 -*-
"""rackio_opcua/folder.py

This module implements the folder class for RackioOPCUA.
"""
from rackio import TagEngine

from .updater import TagUpdater
from .device import Device

class Folder:

    def __init__(self, name, server, idx):

        self.name = name
        self.server = server
        self.idx = idx

        self._folder = server.nodes.objects.add_folder(idx, name)

        self.folders = list()
        self.devices = list()
        self.mappings = list()
    
    def define_folder(self, folder_name):

        server = self.server
        idx = self.idx

        folder = Folder(folder_name, server, idx)

        self.folders.append(folder)

        return folder

    def define_device(self, name):

        folder = self._folder
        idx = self.idx

        device = Device(name, folder, idx)

        self.devices.append(device)

        return device

    def define_mapping(self, tag, mode, period=0.25):

        dev = self._folder
        idx = self.idx

        engine = TagEngine()

        value = engine.read_tag(tag)

        opc_var = dev.add_variable(idx, tag, value)

        mapping = TagUpdater(opc_var, tag, mode, period)
        self.mappings.append(mapping)

    def get_mappings(self):

        result = self.mappings
        
        for folder in self.folders:

            result += folder.get_mappings()

        for device in self.devices:

            result += device.get_mappings()

        return result
    