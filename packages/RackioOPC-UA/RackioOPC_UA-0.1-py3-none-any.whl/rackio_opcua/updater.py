# updater.py
import logging
import time

from threading import Thread

from rackio import TagEngine


class TagUpdater(Thread):
    
    def __init__(self, opc_var, tag, mode, period):
        
        Thread.__init__(self)
        
        self._stopev = False
        self.opc_var = opc_var
        self.tag = tag
        self.mode = mode
        self.engine = TagEngine()

        self._period = period
        self.last = None

    def set_var(self):

        if self.mode == "write":

            self.opc_var.set_writable()
    
    def set_last(self):

        self.last = time.time()

    def sleep_elapsed(self):

        elapsed = time.time() - self.last

        if elapsed < self._period:
            time.sleep(self._period - elapsed)
        else:
            logging.warning("OPC UA Variable: Failed to update on time...")

        self.set_last()

    def read(self):

        value = self.engine.read_tag(self.tag)
        self.opc_var.set_value(value)

    def write(self):

        value = self.opc_var.get_value()
        self.engine.write_tag(self.tag, value)

    def stop(self):
        self._stopev = True

    def run(self):

        self.set_var()

        if self.mode == "read":
            action = self.read
        else:
            action = self.write
        
        self.set_last()

        while not self._stopev:
            action()
            self.sleep_elapsed()
