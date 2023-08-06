# -*- coding: utf-8 -*-
"""rackio_opcua/device.py

This module implements the device class for RackioOPCUA.
"""
from rackio import TagEngine

from .updater import TagUpdater


class Device:

    def __init__(self, name, folder, idx):

        self.name = name
        self.folder = folder
        self.idx = idx

        self._device = folder.add_object(idx, name)

        self.mappings = list()

    def define_mapping(self, tag, mode, period=0.25):

        dev = self._device
        idx = self.idx

        engine = TagEngine()

        value = engine.read_tag(tag)

        opc_var = dev.add_variable(idx, tag, value)

        mapping = TagUpdater(opc_var, tag, mode, period)
        self.mappings.append(mapping)

    def get_mappings(self):

        return self.mappings

    
