# -*- coding: utf-8 -*-
"""rackio_opcua/worker.py

This module implements the worker for RackioOPCUA.
"""
import time

from threading import Thread


class OCPUAWorker(Thread):

    def __init__(self, core, *args, **kwargs):

        super(OCPUAWorker, self).__init__(*args, **kwargs)

        self.core = core

    def run(self):

        server = self.core.server

        server.start()

        for updater in self.core.get_mappings():

            updater.start()

        while True:

            time.sleep(0.25)

