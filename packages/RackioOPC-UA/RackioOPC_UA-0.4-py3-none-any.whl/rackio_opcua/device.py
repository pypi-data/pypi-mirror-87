# -*- coding: utf-8 -*-
"""rackio_opcua/device.py

This module implements the device class for RackioOPCUA.
"""
from rackio import TagEngine

from .updater import TagUpdater


class Device:

    def __init__(self, name, obj, idx):

        self.name = name
        self.obj = obj
        self.idx = idx

        self._device = obj.add_object(idx, name)

        self.mappings = list()
        self.devices = list()

    def define_device(self, name):

        obj = self._device
        idx = self.idx

        device = Device(name, obj, idx)

        self.devices.append(device)

        return device

    def define_mapping(self, tag, mode, period=0.25):

        dev = self._device
        idx = self.idx

        engine = TagEngine()

        value = engine.read_tag(tag)

        opc_var = dev.add_variable(idx, tag, value)

        mapping = TagUpdater(opc_var, tag, mode, period)
        self.mappings.append(mapping)

    def get_mappings(self):

        result = self.mappings

        for device in self.devices:
            result += device.get_mappings()
        
        return result

    
