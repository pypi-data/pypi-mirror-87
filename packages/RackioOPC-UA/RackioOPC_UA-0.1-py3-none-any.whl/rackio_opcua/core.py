# -*- coding: utf-8 -*-
"""rackio_opcua/core.py

This module implements the core app class and methods for Rackio OPC-UA.
"""

import json

from ._singleton import Singleton
from .folder import Folder
from .worker import OCPUAWorker

from .decorator import AppendWorker

from opcua import ua, uamethod, Server


class OPCUACore(Singleton):

    def __init__(self):

        super(OPCUACore, self).__init__()

        self.app = None
        self.port = None
        self.server = None
        self.idx = None
        self.worker = None

        self.folders = dict()

    def define_mapping(self, tag, mode, period=0.25):

        pass

    def define_device(self, device_name, folder_name="Default"):

        pass

    def define_folder(self, folder_name):

        server = self.server
        idx = self.idx

        folder = Folder(folder_name, server, idx)

        self.folders[folder_name] = folder

        return folder

    def get_mappings(self):

        result = list()

        for _, folder in self.folders.items():

            result += folder.get_mappings()

        return result

    def __call__(self, app=None, name="Rackio OPC-UA Server", port=4840, period=0.25):

        if not app:
            return self

        self.server = Server()
        endpoint = "opc.tcp://0.0.0.0:{}/rackio/server/".format(port)
        
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        self.server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])

        uri = "http://github.com/rack-io/rackio-opc-ua"
        self.idx = self.server.register_namespace(uri)

        self.period = period
        
        self.app = app

        worker = OCPUAWorker(self)
        app._start_workers = AppendWorker(app._start_workers, worker)

        return self